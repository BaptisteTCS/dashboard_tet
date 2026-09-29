"""Pipeline nocturne : retours utilisateurs Notion -> tickets du backlog -> OLAP.

À COPIER-COLLER TEL QUEL dans une cellule Datalore, puis planifier en exécution
quotidienne. Le script est autonome : il ne dépend d'aucun autre fichier du repo.

Prérequis Datalore
------------------
1. Environnement :
       pip install openai requests pandas sqlalchemy "psycopg[binary]"
2. Secrets (onglet Secrets du notebook, injectés en variables d'environnement) :
       NOTION_TOKEN     token d'intégration Notion
       OPENAI_API_KEY   clé OpenAI
       DATABASE_URL     base OLAP (la même que le secret DATABASE_URL de Streamlit)
   Optionnel : MAX_PAR_NUIT pour borner le nombre de retours analysés par run.

Ce qu'il fait, dans l'ordre
---------------------------
1. recharge les cycles permanents et tout le backlog de tickets depuis Notion,
   et les réécrit dans retours_utilisateurs_cycles / retours_utilisateurs_backlog ;
2. recharge tous les retours utilisateurs et met à jour leurs métadonnées
   (titre, citation, url, date, présence d'un EPIC) dans retours_utilisateurs_analyse ;
3. pour les retours sans EPIC, pas encore validés à la main et sans analyse
   valide, appelle le modèle en deux passes (cycle puis tickets) et enregistre
   les propositions.

Le script est idempotent : une nuit sans nouveau retour ne consomme aucun token.
La page Streamlit ne fait plus que lire ces tables.
"""

import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests
from openai import OpenAI
from sqlalchemy import create_engine, text

# ============================================================================
# 1. Configuration
# ============================================================================

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
DATABASE_URL = os.environ.get("DATABASE_URL", "")

CYCLES_DB_ID = "bb5a958ae20e487799fe6bafaa57abd0"
DATA_SOURCE_ID = "e2e6f1b5-56bf-4d17-9c70-308ef18133fb"
FEEDBACKS_DB_ID = "1f36523d57d7800d976be22dace0d9e1"

# Epics permanents qui ne sont pas des cycles de roadmap.
EXCLUDED_IDS = {
    "640246a970e24e65b381035be02ed13c",
    "1ac1e3c7ae33453a8a5af80030ecc668",
    "fb511bcf0f514ac49d5971e6c26a8059",
}

COL_EPIC = "EPIC"
COL_TITRE = "Titre"
COL_CITATION = "Citation"
COL_DATE = "Created time"

MODEL = "gpt-5-mini"
EFFORT = "medium"
WORKERS = 8
MAX_TICKETS = 3
# Plafond de retours analysés par exécution. 0 ou absent = pas de limite ;
# mettre la variable d'environnement MAX_PAR_NUIT pour borner la facture.
MAX_PAR_NUIT = int(os.environ.get("MAX_PAR_NUIT", "0")) or None

CONFIANCES = {"haute", "moyenne", "faible"}

# Descriptions des cycles : ce qui guide le choix du modèle.
CYCLE_DESCRIPTIONS = {
    "Améliorations Actions": "Actions, fiches actions, sous-actions.",
    "Améliorations Benchmark / Collectivités / Inspirations": "Se comparer avec d'autres collectivités ou rechercher les autres collectivités sur la plateforme",
    "Améliorations EDL / Référentiel": "Référentiel, état des lieux, mesures, sous-mesures, taches, programme TETE, référentiel CAE, référentiel ECI, référentiel climat-ressource, audit, labellisation",
    "Améliorations Indicateurs": "Indicateurs, open data",
    "Améliorations Plans": "Plan d'action, axes, sous-axes. Niveau opérationnel au desssus de l'action",
    "Améliorations Rôles & Droits": "Droits des users, rôles, permissions",
    "Améliorations Site internet": "Site publique. Pas en rapport avec l'app, c'est un site vitrine qui n'a rien de fonctionnel.",
    "Améliorations Tableau de Bord (TDB)": "Tableau de bord, modules",
    "Améliorations Transverses": "Bénéfique pour toute l'app. Tout ce qui ne concerne aucun des autres cycles en particulier.",
    "Améliorations aide à la priorisation (SNBC, Mondrian, …)": "Mondrian, trajectoire SNBC, outil d'aide à la priorisation, leviers.",
}


def verifier_configuration():
    manquants = [
        nom for nom, valeur in [
            ("NOTION_TOKEN", NOTION_TOKEN),
            ("OPENAI_API_KEY", OPENAI_API_KEY),
            ("DATABASE_URL", DATABASE_URL),
        ] if not valeur
    ]
    if manquants:
        raise RuntimeError(
            "Secrets manquants : " + ", ".join(manquants)
            + ". Ajoutez-les dans l'onglet Secrets du notebook Datalore."
        )


client_ai = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def get_engine():
    url = DATABASE_URL
    if url.startswith("postgresql://") and "+" not in url.split("://", 1)[0]:
        try:
            import psycopg  # noqa: F401
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        except ImportError:
            pass
    return create_engine(url, pool_pre_ping=True, pool_recycle=300)


# ============================================================================
# 2. Notion
# ============================================================================


def notion_headers(version):
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": version,
        "Content-Type": "application/json",
    }


def norm(i):
    return i.replace("-", "") if i else None


def build_filter(database_id, prop_name, value, headers):
    r = requests.get(
        f"https://api.notion.com/v1/databases/{database_id}", headers=headers
    )
    r.raise_for_status()
    props = r.json()["properties"]
    if prop_name not in props:
        raise KeyError(f"Propriété '{prop_name}' introuvable. Disponibles : {list(props)}")
    ptype = props[prop_name]["type"]
    operators = {
        "select": "equals",
        "status": "equals",
        "multi_select": "contains",
        "rich_text": "equals",
        "title": "equals",
    }
    if ptype not in operators:
        raise ValueError(f"Type '{ptype}' non géré (relation, formule...)")
    return {"property": prop_name, ptype: {operators[ptype]: value}}


def get_permanent_cycles(database_id, cycle_value="Permanent"):
    headers = notion_headers("2022-06-28")
    items = []
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {
        "page_size": 100,
        "filter": build_filter(database_id, "Cycle", cycle_value, headers),
    }
    while True:
        r = requests.post(url, headers=headers, json=payload)
        if not r.ok:
            print(r.status_code, r.text)
            r.raise_for_status()
        data = r.json()
        for page in data["results"]:
            title_prop = page["properties"].get("Name", {}).get("title", [])
            items.append({
                "id": page["id"].replace("-", ""),
                "name": "".join(t["plain_text"] for t in title_prop) or None,
            })
        if not data.get("has_more"):
            break
        payload["start_cursor"] = data["next_cursor"]
        time.sleep(0.34)
    return items


def query_ds(ds_id, filter_=None):
    headers = notion_headers("2025-09-03")
    url = f"https://api.notion.com/v1/data_sources/{ds_id}/query"
    results, payload = [], {"page_size": 100}
    if filter_:
        payload["filter"] = filter_
    while True:
        r = requests.post(url, headers=headers, json=payload)
        if not r.ok:
            print(r.status_code, r.text)
            r.raise_for_status()
        data = r.json()
        results.extend(data["results"])
        if not data.get("has_more"):
            break
        payload["start_cursor"] = data["next_cursor"]
        time.sleep(0.34)
    return results


def find_relation_prop(ds_id, target_db_id):
    """Trouve la propriété relation du Kanban qui pointe vers la base des cycles."""
    headers = notion_headers("2025-09-03")
    r = requests.get(f"https://api.notion.com/v1/data_sources/{ds_id}", headers=headers)
    r.raise_for_status()
    props = r.json()["properties"]
    relations = {n: p["relation"] for n, p in props.items() if p["type"] == "relation"}
    for name, rel in relations.items():
        if norm(rel.get("database_id")) == norm(target_db_id):
            return name
    raise KeyError(f"Aucune relation vers {target_db_id} dans {list(relations)}")


def charger_backlog():
    """Cycles permanents et tickets du Kanban rattachés à ces cycles.

    L'index par cycle est construit ici et non dérivé de tickets_par_id : un
    ticket peut appartenir à plusieurs cycles.
    """
    cycle_names = {
        c["id"]: c["name"] or c["id"]
        for c in get_permanent_cycles(CYCLES_DB_ID)
        if c["id"] not in EXCLUDED_IDS
    }
    rel_prop = find_relation_prop(DATA_SOURCE_ID, CYCLES_DB_ID)

    tickets_par_id = {}
    for cycle_id, cycle_name in cycle_names.items():
        linked = query_ds(
            DATA_SOURCE_ID, {"property": rel_prop, "relation": {"contains": cycle_id}}
        )
        for t in linked:
            ticket_id = t["id"].replace("-", "")
            title = t["properties"].get("Name", {}).get("title", [])
            statut = t["properties"].get("Statut", {}).get("status") or {}
            row = tickets_par_id.setdefault(ticket_id, {
                "id": ticket_id,
                "cycle_ids": [],
                "ticket": "".join(seg["plain_text"] for seg in title) or None,
                "statut": statut.get("name"),
                "url": t.get("url"),
            })
            row["cycle_ids"].append(cycle_id)

    tickets_par_cycle = {cycle_id: [] for cycle_id in cycle_names}
    for t in tickets_par_id.values():
        for cycle_id in t["cycle_ids"]:
            tickets_par_cycle[cycle_id].append(t["id"])

    return {
        "cycle_names": cycle_names,
        "tickets_par_id": tickets_par_id,
        "tickets_par_cycle": tickets_par_cycle,
    }


def prop_value(p):
    """Convertit une propriété Notion en valeur Python simple."""
    t = p["type"]
    v = p.get(t)
    if t in ("title", "rich_text"):
        return "".join(seg["plain_text"] for seg in v) or None
    if t in ("select", "status"):
        return v["name"] if v else None
    if t == "multi_select":
        return ", ".join(o["name"] for o in v) or None
    if t == "relation":
        return [r["id"].replace("-", "") for r in v]
    if t == "people":
        return ", ".join(u.get("name") or u["id"] for u in v) or None
    if t == "date":
        return v["start"] if v else None
    if t == "unique_id":
        return v["number"] if v else None
    if t in ("formula", "rollup"):
        return v.get(v["type"]) if v else None
    if t == "files":
        return [f.get("name") for f in v]
    if t in ("created_by", "last_edited_by"):
        return v.get("name") or v.get("id")
    return v  # number, checkbox, url, email, phone_number, created_time...


def charger_feedbacks():
    headers = notion_headers("2025-09-03")
    r = requests.get(
        f"https://api.notion.com/v1/databases/{FEEDBACKS_DB_ID}", headers=headers
    )
    r.raise_for_status()
    rows = []
    for ds in r.json()["data_sources"]:
        for page in query_ds(ds["id"]):
            row = {"id": page["id"].replace("-", ""), "url": page["url"]}
            row.update({name: prop_value(p) for name, p in page["properties"].items()})
            rows.append(row)
    return pd.DataFrame(rows)


def epic_vide(v):
    if isinstance(v, (list, tuple, set)):
        return len(v) == 0
    if v is None:
        return True
    try:
        if pd.isna(v):
            return True
    except (TypeError, ValueError):
        pass
    return not str(v).strip()


# ============================================================================
# 3. OLAP
# ============================================================================

DDL = """
CREATE TABLE IF NOT EXISTS retours_utilisateurs_cycles (
    cycle_id    TEXT PRIMARY KEY,
    cycle_name  TEXT,
    maj_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS retours_utilisateurs_backlog (
    ticket_id     TEXT,
    cycle_id      TEXT,
    ticket_titre  TEXT,
    statut        TEXT,
    cycle_name    TEXT,
    url           TEXT,
    maj_at        TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (ticket_id, cycle_id)
);

CREATE TABLE IF NOT EXISTS retours_utilisateurs_analyse (
    feedback_id          TEXT PRIMARY KEY,
    titre                TEXT,
    citation             TEXT,
    url                  TEXT,
    created_time         TEXT,
    sans_epic            BOOLEAN,
    cycle_id             TEXT,
    cycle_name           TEXT,
    confiance            TEXT,
    justification        TEXT,
    tickets              JSONB,
    ticket_justification TEXT,
    erreur               TEXT,
    model                TEXT,
    analyse_at           TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS retours_utilisateurs_tickets (
    feedback_id     TEXT PRIMARY KEY,
    ticket_id       TEXT,
    cycle_id        TEXT,
    feedback_titre  TEXT,
    ticket_titre    TEXT,
    choix_ia        BOOLEAN,
    score_ia        DOUBLE PRECISION,
    valide_at       TIMESTAMPTZ DEFAULT now(),
    notion_sync_at  TIMESTAMPTZ
);
"""


def creer_tables(engine):
    with engine.begin() as conn:
        for statement in filter(None, (s.strip() for s in DDL.split(";"))):
            conn.execute(text(statement))


def ecrire_backlog(engine, backlog):
    """Remplacement complet du miroir OLAP du backlog Notion."""
    cycles = [
        {"cycle_id": cid, "cycle_name": nom}
        for cid, nom in backlog["cycle_names"].items()
    ]
    tickets = [
        {
            "ticket_id": t["id"],
            "cycle_id": cid,
            "ticket_titre": t["ticket"],
            "statut": t["statut"],
            "cycle_name": backlog["cycle_names"][cid],
            "url": t.get("url"),
        }
        for t in backlog["tickets_par_id"].values()
        for cid in t["cycle_ids"]
    ]
    if not cycles or not tickets:
        raise RuntimeError("Backlog Notion vide, écriture annulée")

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM retours_utilisateurs_cycles"))
        conn.execute(
            text("""
                INSERT INTO retours_utilisateurs_cycles (cycle_id, cycle_name, maj_at)
                VALUES (:cycle_id, :cycle_name, now())
            """),
            cycles,
        )
        conn.execute(text("DELETE FROM retours_utilisateurs_backlog"))
        conn.execute(
            text("""
                INSERT INTO retours_utilisateurs_backlog
                    (ticket_id, cycle_id, ticket_titre, statut, cycle_name, url, maj_at)
                VALUES
                    (:ticket_id, :cycle_id, :ticket_titre, :statut, :cycle_name, :url, now())
            """),
            tickets,
        )
    return len(cycles), len(tickets)


def ecrire_metadonnees(engine, df):
    """Métadonnées des retours, sans toucher aux colonnes d'analyse."""
    lignes = [
        {
            "feedback_id": r["id"],
            "titre": r.get(COL_TITRE),
            "citation": r.get(COL_CITATION),
            "url": r.get("url"),
            "created_time": str(r.get(COL_DATE)) if r.get(COL_DATE) else None,
            "sans_epic": epic_vide(r.get(COL_EPIC)),
        }
        for r in df.to_dict("records")
    ]
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO retours_utilisateurs_analyse
                    (feedback_id, titre, citation, url, created_time, sans_epic)
                VALUES
                    (:feedback_id, :titre, :citation, :url, :created_time, :sans_epic)
                ON CONFLICT (feedback_id) DO UPDATE SET
                    titre = EXCLUDED.titre,
                    citation = EXCLUDED.citation,
                    url = EXCLUDED.url,
                    created_time = EXCLUDED.created_time,
                    sans_epic = EXCLUDED.sans_epic
            """),
            lignes,
        )
    return len(lignes)


def lire_analyses(engine):
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT feedback_id, tickets, erreur, analyse_at
                FROM retours_utilisateurs_analyse
            """)
        ).mappings().all()
    return {r["feedback_id"]: dict(r) for r in rows}


def lire_valides(engine):
    with engine.connect() as conn:
        return {
            r[0] for r in conn.execute(
                text("SELECT feedback_id FROM retours_utilisateurs_tickets")
            )
        }


def ecrire_analyses(engine, analyses):
    if not analyses:
        return
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE retours_utilisateurs_analyse SET
                    cycle_id = :cycle_id,
                    cycle_name = :cycle_name,
                    confiance = :confiance,
                    justification = :justification,
                    tickets = CAST(:tickets AS JSONB),
                    ticket_justification = :ticket_justification,
                    erreur = :erreur,
                    model = :model,
                    analyse_at = now()
                WHERE feedback_id = :feedback_id
            """),
            [
                {
                    "feedback_id": a["feedback_id"],
                    "cycle_id": a.get("cycle_id"),
                    "cycle_name": a.get("cycle_name"),
                    "confiance": a.get("confiance"),
                    "justification": a.get("justification"),
                    "tickets": json.dumps(a.get("tickets") or [], ensure_ascii=False),
                    "ticket_justification": a.get("ticket_justification"),
                    "erreur": a.get("erreur"),
                    "model": a.get("model"),
                }
                for a in analyses.values()
            ],
        )


# ============================================================================
# 4. Passe 1 : feedback -> cycle
# ============================================================================

SYSTEM_PROMPT = """Tu es analyste produit chez Territoires en Transitions.

Territoires en Transitions est une plateforme publique qui accompagne les
collectivités françaises dans leur transition écologique. Elle leur permet de :
- construire et suivre leurs plans d'actions ;
- suivre des indicateurs (de suivi, de résultat, avec valeurs et objectifs) ;
- visualiser des trajectoires (notamment SNBC territorialisée) ;
- remplir leur référentiel CAE (Climat Air Énergie) et ECI (Économie Circulaire),
  dans le cadre du programme TETE de l'ADEME.

Tu reçois un retour d'un utilisateur de la plateforme et la liste des cycles de
notre roadmap produit. Ta tâche : rattacher ce retour à UN SEUL cycle.

Règles :
- tu dois toujours choisir un cycle, l'abstention n'est pas autorisée ;
- tu réponds avec le CODE du cycle (ex : C07), jamais avec son nom ni un autre
  identifiant, et uniquement un code présent dans la liste fournie ;
- tu juges sur le sujet fonctionnel du retour, pas sur le ton ni l'urgence ;
- si plusieurs cycles sont plausibles, tu prends le plus spécifique et tu
  positionnes la confiance à "moyenne" ou "faible".
- si aucun cycle ne semble correspondre, tu le mets dans "Améliorations transverses" avec une confiance faibe

Règles empiriques:
- Les titres des feedback ont souvent un préfixe, si c'est l'un deux, on peut déjà associer le cycle correspondant : 
    - PA : Améliorations Plans
    - TDB : Améliorations Tableau de Bord (TDB)
    - FA : Améliorations Actions
    - Site internet : Améliorations Site internet
- Les demande de liens entre actions et mesures vont dans "Améliorations EDL / Référentiel"
- Tout ce qui concerne les PPT vont dans "Améliorations Plans"

Tu réponds uniquement en JSON, au format exact :
{"code": "C07", "confiance": "haute|moyenne|faible", "justification": "une phrase courte"}"""


def construire_contexte_cycles(backlog):
    """Attribue un code court à chaque cycle et renvoie (texte_contexte, code -> cycle_id).

    Le modèle choisit un code Cnn plutôt qu'un id Notion : les identifiants
    hexadécimaux de 32 caractères sont systématiquement hallucinés.
    """
    ordonnes = sorted(backlog["cycle_names"].items(), key=lambda kv: kv[1])
    code_vers_id = {}
    lignes = []
    for i, (cycle_id, name) in enumerate(ordonnes, start=1):
        code = f"C{i:02d}"
        code_vers_id[code] = cycle_id
        description = CYCLE_DESCRIPTIONS.get(name, "")
        lignes.append(f"{code} | {name}" + (f" : {description}" if description else ""))
    return "\n".join(lignes), code_vers_id


def strip_json_fences(txt):
    if not txt:
        return ""
    t = txt.strip()
    if t.startswith("```"):
        t = t.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
    return t


def appeler_modele(system_prompt, prompt):
    # Le system prompt passe dans input et non dans instructions : avec
    # text.format=json_object, l'API exige le mot "json" dans input.
    kwargs = {
        "model": MODEL,
        "input": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "reasoning": {"effort": EFFORT},
        "text": {"format": {"type": "json_object"}},
    }
    try:
        response = client_ai.responses.create(**kwargs)
    except TypeError:
        kwargs.pop("text", None)
        response = client_ai.responses.create(**kwargs)
    return json.loads(strip_json_fences(response.output_text or ""))


def classify_feedback(titre, citation, contexte_cycles, code_vers_id, cycle_names,
                      max_retries=3):
    """Choisit un cycle pour un feedback. Renvoie un dict, jamais d'exception."""
    prompt = f"""Cycles disponibles :
{contexte_cycles}

Retour utilisateur :
Titre : {titre or "(vide)"}
Citation : {citation or "(vide)"}

Quel cycle correspond à ce retour ?"""
    derniere_erreur = None

    for tentative in range(1, max_retries + 1):
        try:
            data = appeler_modele(SYSTEM_PROMPT, prompt)
            code = str(data.get("code", "")).strip().upper()
            if code not in code_vers_id:
                raise ValueError(f"code hors liste : {code!r}")
            confiance = str(data.get("confiance", "")).strip().lower()
            cycle_id = code_vers_id[code]
            return {
                "cycle_id": cycle_id,
                "cycle_name": cycle_names[cycle_id],
                "confiance": confiance if confiance in CONFIANCES else "moyenne",
                "justification": data.get("justification"),
                "erreur": None,
            }
        except Exception as e:
            derniere_erreur = f"{type(e).__name__}: {e}"
            if tentative < max_retries:
                time.sleep(2 ** (tentative - 1))

    return {
        "cycle_id": None,
        "cycle_name": None,
        "confiance": None,
        "justification": None,
        "erreur": derniere_erreur,
    }


# ============================================================================
# 5. Passe 2 : feedback -> tickets
# ============================================================================

SYSTEM_PROMPT_TICKET = """Tu es analyste produit chez Territoires en Transitions.

Territoires en Transitions est une plateforme publique qui accompagne les
collectivités françaises dans leur transition écologique : plans d'actions,
indicateurs, trajectoires (SNBC territorialisée), référentiels CAE (Climat Air
Énergie) et ECI (Économie Circulaire) du programme TETE de l'ADEME.

Tu reçois un retour d'un utilisateur de la plateforme et la liste complète des
tickets de notre backlog, regroupés par cycle de roadmap.

Ta tâche : identifier le ou les tickets existants qui traitent déjà le sujet de
ce retour.

Règles :
- il est normal qu'aucun ticket ne corresponde. Dans ce cas tu renvoies une liste
  vide. Ne force jamais un rapprochement approximatif : un retour sans ticket est
  une information utile, il signale un manque dans la roadmap ;
- un ticket ne correspond que s'il traite le même sujet fonctionnel, pas
  seulement le même thème général ;
- au plus 3 tickets, classés du plus probable au moins probable ;
- le score est un nombre entre 0 et 1 qui sert à ordonner tes candidats entre eux ;
- tu réponds avec le CODE du ticket (ex : T0042), jamais avec son titre, et
  uniquement des codes présents dans la liste fournie ;
- le cycle indiqué avec le retour vient d'une analyse préalable : c'est une
  indication, pas une contrainte. Tu peux retenir un ticket d'un autre cycle.

Tu réponds uniquement en JSON, au format exact :
{"tickets": [{"code": "T0042", "score": 0.8}], "justification": "une phrase courte"}"""


def construire_contexte_tickets(backlog, inclure_statut=True):
    """Liste tous les tickets groupés par cycle, avec un code court par ticket.

    Ce bloc est identique pour tous les feedbacks : c'est lui qui constitue le
    préfixe mis en cache par l'API. Un ticket rattaché à plusieurs cycles
    apparaît une fois par cycle, ce qui rend le cycle du code choisi non ambigu.
    """
    code_vers_ticket = {}
    lignes = []
    n = 0
    for cycle_id, cycle_name in sorted(
        backlog["cycle_names"].items(), key=lambda kv: kv[1]
    ):
        ids = backlog["tickets_par_cycle"].get(cycle_id) or []
        if not ids:
            continue
        lignes.append(f"\n## {cycle_name}")
        for tid in sorted(ids, key=lambda i: backlog["tickets_par_id"][i]["ticket"] or ""):
            t = backlog["tickets_par_id"][tid]
            n += 1
            code = f"T{n:04d}"
            code_vers_ticket[code] = {
                "id": tid,
                "titre": t["ticket"],
                "cycle_id": cycle_id,
                "cycle_name": cycle_name,
            }
            statut = f" | {t['statut']}" if inclure_statut and t["statut"] else ""
            lignes.append(f"{code} | {t['ticket']}{statut}")
    return "\n".join(lignes).strip(), code_vers_ticket


def classify_ticket(titre, citation, cycle_name, contexte_tickets, code_vers_ticket,
                    max_retries=3):
    """Retourne 0 à MAX_TICKETS tickets pour un feedback. Ne lève jamais."""
    prompt = f"""Tickets du backlog, groupés par cycle :
{contexte_tickets}

Retour utilisateur :
Titre : {titre or "(vide)"}
Citation : {citation or "(vide)"}
Cycle identifié à l'étape précédente (indication) : {cycle_name or "(inconnu)"}

Quels tickets existants traitent déjà ce sujet ?"""
    derniere_erreur = None

    for tentative in range(1, max_retries + 1):
        try:
            data = appeler_modele(SYSTEM_PROMPT_TICKET, prompt)
            bruts = data.get("tickets") or []
            if not isinstance(bruts, list):
                raise ValueError(f"'tickets' n'est pas une liste : {bruts!r}")

            retenus, vus = [], set()
            for item in bruts:
                code = str((item or {}).get("code", "")).strip().upper()
                if code not in code_vers_ticket:
                    raise ValueError(f"code hors liste : {code!r}")
                if code in vus:
                    continue
                vus.add(code)
                try:
                    score = float((item or {}).get("score", 0))
                except (TypeError, ValueError):
                    score = 0.0
                retenus.append({**code_vers_ticket[code], "score": min(max(score, 0.0), 1.0)})

            retenus.sort(key=lambda t: t["score"], reverse=True)
            return {
                "tickets": retenus[:MAX_TICKETS],
                "ticket_justification": data.get("justification"),
                "erreur": None,
            }
        except Exception as e:
            derniere_erreur = f"{type(e).__name__}: {e}"
            if tentative < max_retries:
                time.sleep(2 ** (tentative - 1))

    return {"tickets": [], "ticket_justification": None, "erreur": derniere_erreur}


# ============================================================================
# 6. Orchestration
# ============================================================================


def a_rejouer(analyse, backlog):
    """Rejoue si l'analyse est absente, en échec, ou pointe vers un ticket qui
    n'existe plus dans le backlog."""
    if not analyse or not analyse.get("analyse_at") or analyse.get("erreur"):
        return True
    return any(
        t.get("id") not in backlog["tickets_par_id"]
        for t in analyse.get("tickets") or []
    )


def analyser(feedbacks, backlog):
    """Passe 1 (cycle) puis passe 2 (tickets). Renvoie {feedback_id: analyse}."""
    contexte_cycles, code_vers_id = construire_contexte_cycles(backlog)
    contexte_tickets, code_vers_ticket = construire_contexte_tickets(backlog)
    cycle_names = backlog["cycle_names"]
    print(f"   contexte tickets : ~{len(contexte_tickets) // 4} tokens de préfixe")

    analyses = {
        r["id"]: {"feedback_id": r["id"], "titre": r.get(COL_TITRE), "model": MODEL}
        for r in feedbacks
    }
    verrou = threading.Lock()

    faits = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {
            pool.submit(
                classify_feedback,
                r.get(COL_TITRE), r.get(COL_CITATION),
                contexte_cycles, code_vers_id, cycle_names,
            ): r["id"]
            for r in feedbacks
        }
        for future in as_completed(futures):
            analyses[futures[future]].update(future.result())
            faits += 1
            if faits % 20 == 0 or faits == len(feedbacks):
                print(f"   passe 1 : {faits}/{len(feedbacks)}")

    def passe_2(row):
        return classify_ticket(
            row.get(COL_TITRE), row.get(COL_CITATION),
            analyses[row["id"]].get("cycle_name"),
            contexte_tickets, code_vers_ticket,
        )

    def fusionner(analyse, resultat):
        """Le ticket retenu fait autorité sur le cycle de la passe 1."""
        analyse["tickets"] = resultat["tickets"]
        analyse["ticket_justification"] = resultat["ticket_justification"]
        if resultat["erreur"]:
            analyse["erreur"] = resultat["erreur"]
        if resultat["tickets"]:
            analyse["cycle_id"] = resultat["tickets"][0]["cycle_id"]
            analyse["cycle_name"] = resultat["tickets"][0]["cycle_name"]

    # Le premier appel part seul : il amorce le cache de préfixe côté API.
    # Lancés ensemble, les N premiers workers le rateraient tous en même temps.
    fusionner(analyses[feedbacks[0]["id"]], passe_2(feedbacks[0]))
    faits = 1
    restants = feedbacks[1:]
    if restants:
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {pool.submit(passe_2, r): r["id"] for r in restants}
            for future in as_completed(futures):
                with verrou:
                    fusionner(analyses[futures[future]], future.result())
                    faits += 1
                    if faits % 20 == 0 or faits == len(feedbacks):
                        print(f"   passe 2 : {faits}/{len(feedbacks)}")

    return analyses


def recapitulatif(analyses):
    total = len(analyses)
    echecs = [a for a in analyses.values() if a.get("erreur")]
    sans_ticket = [a for a in analyses.values() if not a.get("tickets") and not a.get("erreur")]
    print(f"\n{total} retours analysés")
    print(f"   {total - len(sans_ticket) - len(echecs)} avec au moins un ticket candidat")
    print(f"   {len(sans_ticket)} sans ticket (manques de la roadmap)")
    print(f"   {len(echecs)} en échec")
    confiances = pd.Series([a.get("confiance") for a in analyses.values()]).value_counts()
    if len(confiances):
        print("\nConfiance de la passe 1 :")
        print(confiances.to_string())
    for a in echecs:
        print(f"   échec {a['feedback_id']} : {a.get('erreur')}")


def main():
    debut = time.time()
    verifier_configuration()
    engine = get_engine()
    creer_tables(engine)

    print("1/4 Backlog Notion")
    backlog = charger_backlog()
    n_cycles, n_tickets = ecrire_backlog(engine, backlog)
    print(f"   {n_cycles} cycles, {n_tickets} couples (ticket, cycle) écrits")

    print("2/4 Retours utilisateurs Notion")
    df = charger_feedbacks()
    n = ecrire_metadonnees(engine, df)
    sans_epic = [r for r in df.to_dict("records") if epic_vide(r.get(COL_EPIC))]
    print(f"   {n} retours, dont {len(sans_epic)} sans EPIC")

    print("3/4 Sélection")
    valides = lire_valides(engine)
    analyses_existantes = lire_analyses(engine)
    a_traiter = [
        r for r in sans_epic
        if r["id"] not in valides
        and a_rejouer(analyses_existantes.get(r["id"]), backlog)
    ]
    # Les plus récents d'abord : c'est par là que la revue humaine commence.
    a_traiter.sort(key=lambda r: str(r.get(COL_DATE) or ""), reverse=True)
    if MAX_PAR_NUIT:
        a_traiter = a_traiter[:MAX_PAR_NUIT]
    print(f"   {len(valides)} déjà validés à la main, {len(a_traiter)} à analyser")

    if not a_traiter:
        print("4/4 Rien à analyser, sortie")
        print(f"\nTerminé en {time.time() - debut:.0f}s")
        return

    print("4/4 Analyse")
    analyses = analyser(a_traiter, backlog)
    ecrire_analyses(engine, analyses)
    recapitulatif(analyses)
    print(f"\nTerminé en {time.time() - debut:.0f}s")


main()
