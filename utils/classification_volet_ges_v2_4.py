"""Classification volet GES v2.4 : leviers, catégories et « structurante », une fiche par appel.

Reprend la v2 (prompt en cache, sortie contrainte, Claude Haiku 5.5) et ajoute :
- le verdict `structurante` (bool) pour chaque levier, qui sert à calculer la note de
  mobilisation de chaque case levier × catégorie (voir `note_case`) ;
- une ligne « Collectivité : type, population » en tête du message ;
- les titres des sous-actions de la fiche ;
- l'exclusion des fiches et sous-actions abandonnées ou en pause.

Lecture seule : ce module n'écrit rien en base.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from utils import classification_volet_ges_v2 as v2
from utils.verify_classification_volet_ges import LEVIER_ID_TO_LABEL, VALID_CATEGORIES

ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH = ROOT / "prompts" / "classification_volet_ges_v2_4.md"
PROMPT_VERSION = "v2.4"
MODEL = "claude-haiku-5-5"
MAX_LEVIERS = v2.MAX_LEVIERS
STATUTS_EXCLUS = ("Abandonné", "En pause")

TYPE_LABELS = {
    "CC": "communauté de communes",
    "CA": "communauté d'agglomération",
    "CU": "communauté urbaine",
    "METRO": "métropole",
    "POLEM": "pôle métropolitain",
    "EPT": "établissement public territorial",
    "epci": "intercommunalité",
    "PETR": "pôle d'équilibre territorial et rural",
    "SIVU": "syndicat intercommunal",
    "SIVOM": "syndicat intercommunal",
    "SMF": "syndicat mixte",
    "SMO": "syndicat mixte",
    "commune": "commune",
    "departement": "département",
    "region": "région",
}

ANTHROPIC_SCHEMA = json.loads(json.dumps(v2.ANTHROPIC_SCHEMA))
_item = ANTHROPIC_SCHEMA["properties"]["leviers"]["items"]
_item["properties"]["structurante"] = {"type": "boolean"}
_item["required"] = ["levier", "categories", "structurante"]


def load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------- données (lecture seule)


def fetch_collectivite_info(engine: Engine, collectivite_id: int) -> dict[str, Any]:
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT id, nom, type, nature_insee, population FROM collectivite WHERE id = :id"),
            {"id": collectivite_id},
        ).mappings().first()
    if row is None:
        raise ValueError(f"Collectivité {collectivite_id} introuvable.")
    code = row["nature_insee"] if row["type"] == "epci" and row["nature_insee"] else row["type"]
    return {
        "id": int(row["id"]),
        "nom": str(row["nom"]),
        "type_code": code,
        "type_label": TYPE_LABELS.get(str(code), str(code or "collectivité")),
        "population": int(row["population"]) if row["population"] is not None else None,
    }


def fetch_fiches(engine: Engine, collectivite_id: int) -> pd.DataFrame:
    """Fiches du plan (axe + parent null) ∪ fiches classées en prod, hors supprimées,
    abandonnées ou en pause. Colonnes : id, titre, description, statut, sous_actions (liste de titres)."""
    sql_fiches = text(
        """
        SELECT DISTINCT fa.id, fa.titre, fa.description, fa.statut::text AS statut
        FROM fiche_action fa
        LEFT JOIN fiche_action_axe faa ON faa.fiche_id = fa.id
        LEFT JOIN fiche_action_volet_ges vg ON vg.fiche_id = fa.id
        WHERE fa.collectivite_id = :cid
          AND fa.parent_id IS NULL
          AND COALESCE(fa.deleted, false) = false
          AND COALESCE(fa.statut::text, '') <> ALL(:exclus)
          AND (faa.fiche_id IS NOT NULL OR vg.fiche_id IS NOT NULL)
        ORDER BY fa.id
        """
    )
    sql_sous = text(
        """
        SELECT parent_id, id, titre
        FROM fiche_action
        WHERE collectivite_id = :cid
          AND parent_id IS NOT NULL
          AND COALESCE(deleted, false) = false
          AND COALESCE(statut::text, '') <> ALL(:exclus)
        ORDER BY parent_id, id
        """
    )
    params = {"cid": collectivite_id, "exclus": list(STATUTS_EXCLUS)}
    with engine.connect() as conn:
        df = pd.read_sql_query(sql_fiches, conn, params=params)
        sous = pd.read_sql_query(sql_sous, conn, params=params)
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)
    df["id"] = df["id"].astype(int)
    df["titre"] = df["titre"].fillna("").astype(str)
    df["description"] = df["description"].fillna("").astype(str)
    titres = (
        sous.assign(titre=sous["titre"].fillna("").astype(str).str.strip())
        .query("titre != ''")
        .groupby("parent_id")["titre"]
        .apply(list)
        .to_dict()
    )
    df["sous_actions"] = df["id"].map(lambda i: titres.get(i, []))
    return df


# ---------------------------------------------------------------- message et validation


def build_user_message(
    collectivite: dict[str, Any],
    titre: str,
    description: str,
    contexte: str | None,
    sous_actions: list[str],
) -> str:
    pop = collectivite.get("population")
    pop_txt = f"{pop:,} habitants".replace(",", " ") if pop else "population non renseignée"
    msg = f"Collectivité : {collectivite['type_label']}, {pop_txt}\n" + v2.build_user_message(
        titre, description, contexte
    )
    titres = [" ".join(t.split()) for t in sous_actions if t and t.strip()]
    if titres:
        msg += "\nSous-actions : " + " ; ".join(titres)
    return msg


Classif = dict[str, dict[str, Any]]  # libellé -> {"categories": [..], "structurante": bool}


def validate(data: Any) -> Classif:
    if not isinstance(data, dict) or not isinstance(data.get("leviers"), list):
        raise ValueError('JSON attendu : {"leviers": [...]}')
    out: dict[str, dict[str, Any]] = {}
    for item in data["leviers"]:
        code = item.get("levier") if isinstance(item, dict) else None
        if code not in LEVIER_ID_TO_LABEL:
            raise ValueError(f"Levier inconnu : {code!r}")
        cats = item.get("categories")
        if not isinstance(cats, list) or not cats:
            raise ValueError(f"Catégories vides pour {code}")
        parsed = {int(c) for c in cats}
        if not parsed <= VALID_CATEGORIES:
            raise ValueError(f"Catégorie invalide pour {code} : {cats}")
        struct = item.get("structurante")
        if not isinstance(struct, bool):
            raise ValueError(f"structurante manquant pour {code}")
        cur = out.setdefault(LEVIER_ID_TO_LABEL[code], {"categories": set(), "structurante": False})
        cur["categories"] |= parsed
        cur["structurante"] = cur["structurante"] or struct
    if len(out) > MAX_LEVIERS:
        raise ValueError(f"{len(out)} leviers (maximum {MAX_LEVIERS})")
    return {k: {"categories": sorted(v["categories"]), "structurante": v["structurante"]} for k, v in out.items()}


def _call(client: Any, system_prompt: str, user_message: str) -> tuple[Any, dict[str, int]]:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_message}],
        tools=[
            {
                "name": v2.TOOL_NAME,
                "description": "Renvoie la classification de la fiche action.",
                "input_schema": ANTHROPIC_SCHEMA,
                "strict": True,
            }
        ],
        tool_choice={"type": "tool", "name": v2.TOOL_NAME},
    )
    u = response.usage
    read = int(getattr(u, "cache_read_input_tokens", 0) or 0)
    write = int(getattr(u, "cache_creation_input_tokens", 0) or 0)
    tokens = {
        "input": int(u.input_tokens or 0) + read + write,
        "cached": read,
        "cache_write": write,
        "output": int(u.output_tokens or 0),
    }
    for block in response.content:
        if getattr(block, "type", None) == "tool_use":
            data = dict(block.input)
            if isinstance(data.get("leviers"), list) and len(data["leviers"]) > MAX_LEVIERS:
                data["leviers"] = data["leviers"][:MAX_LEVIERS]
                tokens["tronque"] = 1
            return data, tokens
    raise json.JSONDecodeError("pas d'appel d'outil dans la réponse", "", 0)


def classify_fiche(client: Any, system_prompt: str, user_message: str, log=print, label: str = "") -> tuple[Classif, dict[str, Any]]:
    """Une fiche, un appel. Rejoue jusqu'à 3 fois une réponse invalide ; attend sur 429/5xx."""
    tokens = {"input": 0, "cached": 0, "cache_write": 0, "output": 0}
    errors: list[str] = []
    essais = attentes = 0
    while essais < 3:
        try:
            data, tk = _call(client, system_prompt, user_message)
        except json.JSONDecodeError as e:
            essais += 1
            errors.append(f"JSONDecodeError: {e}")
            continue
        except Exception as e:
            if v2._is_unavailable(e) and attentes < 20:
                attentes += 1
                log(f"    {label} API indisponible ({type(e).__name__}), nouvel essai dans 10 s")
                time.sleep(10)
                continue
            raise
        essais += 1
        for k, val in tk.items():
            tokens[k] = tokens.get(k, 0) + val
        try:
            return validate(data), {"essais": essais, "erreurs": errors, "tokens": tokens}
        except ValueError as e:
            errors.append(f"ValueError: {e}")
            log(f"  {label} réponse invalide, essai {essais}/3 : {e}")
    raise RuntimeError(f"{label} : 3 réponses invalides : {errors}")


# ---------------------------------------------------------------- notes de mobilisation


def _regle_a(s: int, p: int) -> int:
    if s >= 2:
        return 3
    if s == 1 or p >= 2:
        return 2
    return 1 if p == 1 else 0


def _regle_b(s: int, p: int) -> int:
    if s >= 1 or p >= 3:
        return 3
    return p  # 0, 1 ou 2 actions peu importantes


REGLES = {
    "A": (
        "Règle A — 1 : une peu importante · 2 : plusieurs peu importantes ou une structurante · "
        "3 : au moins deux structurantes",
        _regle_a,
    ),
    "B": (
        "Règle B — 1 : une peu importante · 2 : deux peu importantes · "
        "3 : une structurante ou au moins trois peu importantes",
        _regle_b,
    ),
}
REGLE_DEFAUT = "A"


def note_case(n_structurantes: int, n_peu_importantes: int, regle: str = REGLE_DEFAUT) -> int:
    """Note d'une case à partir du nombre de fiches structurantes et peu importantes (0 = aucune action)."""
    return REGLES[regle][1](n_structurantes, n_peu_importantes)


def notes_from_classification(classif_by_fiche: dict[int, Classif]) -> dict[tuple[str, int], dict[str, Any]]:
    """(levier, catégorie) -> {note, structurantes: [ids], peu_importantes: [ids]}."""
    cases: dict[tuple[str, int], dict[str, list[int]]] = {}
    for fid, classif in classif_by_fiche.items():
        for levier, info in classif.items():
            for cat in info["categories"]:
                c = cases.setdefault((levier, int(cat)), {"structurantes": [], "peu_importantes": []})
                c["structurantes" if info["structurante"] else "peu_importantes"].append(int(fid))
    return {
        key: {
            "note": note_case(len(c["structurantes"]), len(c["peu_importantes"])),
            "structurantes": sorted(c["structurantes"]),
            "peu_importantes": sorted(c["peu_importantes"]),
        }
        for key, c in cases.items()
    }
