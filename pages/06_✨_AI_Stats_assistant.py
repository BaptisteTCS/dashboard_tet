import json
import logging
import re
from pathlib import Path
from typing import Callable, Optional

import pandas as pd
import streamlit as st
from openai import OpenAI
from sqlalchemy import text

from utils.db import get_engine
from utils.db_text import tables_text

st.set_page_config(layout="wide", page_title="IA Transitos", page_icon="🧠")

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)



# === CONFIGURATION ===
MODEL = "gpt-5"
REASONING_EFFORT = "medium"
MAX_OUTPUT_TOKENS = 32000
MAX_TOOL_ITERATIONS = 5

PREVIEW_ROWS = 20      # apercu renvoye au modele (protege le contexte)
MAX_TABLE_ROWS = 1000  # plafond d'affichage d'un tableau
MAX_CHART_ROWS = 1000  # plafond d'affichage d'un graphe

# Garde-fous en dur : mots-cles interdits (detection par word-boundary pour ne
# pas matcher des colonnes comme "created_at" qui contient "create").

FORBIDDEN = (
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "create",
    "truncate",
    "grant",
    "revoke",
)
_FORBIDDEN_REGEX = re.compile(
    r"\b(" + "|".join(FORBIDDEN) + r")\b", re.IGNORECASE
)


@st.cache_resource(show_spinner=False)
def get_openai_client() -> OpenAI:
    """Instance OpenAI mise en cache pour tous les tours de conversation."""
    return OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))


@st.cache_data(show_spinner=False)
def load_olap_doc() -> str:
    """Charge la documentation des tables de statistiques (schema public / OLAP)."""
    try:
        doc_path = Path(__file__).resolve().parent.parent / "data" / "bdd_olap.md"
        return doc_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Impossible de charger data/bdd_olap.md : %s", exc)
        return ""


OLAP_DOC = load_olap_doc()


# === GARDE-FOUS + EXECUTION SQL ===
def safe_run_sql(sql: str, limit: int) -> tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Valide puis execute une requete SELECT en lecture seule.

    Regles de securite (en dur) :
    - Aucun mot-cle de modification (FORBIDDEN), detecte par word-boundary.
    - La requete doit commencer par SELECT ou WITH.
    - Une seule instruction (pas de ';' en milieu de requete).
    - Emballage systematique dans un sous-select avec LIMIT pour garantir le
      plafond de lignes meme si le modele oublie le LIMIT.

    Retourne (dataframe, None) en cas de succes, (None, message_erreur) sinon.
    """
    if not sql or not sql.strip():
        return None, "Requete SQL vide."

    cleaned = sql.strip()

    # Retirer un eventuel formatage markdown (```sql ... ```)
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*", "", cleaned).strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

    # Strip du ';' final eventuel
    cleaned = cleaned.rstrip().rstrip(";").rstrip()

    # Anti multi-statement : un ';' restant signifie plusieurs instructions
    if ";" in cleaned:
        return None, "Plusieurs instructions SQL detectees : une seule requete SELECT est autorisee."

    # Doit commencer par SELECT ou WITH
    if not re.match(r"^\s*(select|with)\b", cleaned, re.IGNORECASE):
        return None, "Seules les requetes SELECT (ou WITH ... SELECT) sont autorisees."

    # Mots-cles interdits
    match = _FORBIDDEN_REGEX.search(cleaned)
    if match:
        return None, (
            f"Requete refusee : commande de modification non autorisee ({match.group(1).upper()})."
        )

    # Emballage pour garantir le plafond de lignes
    wrapped = f"SELECT * FROM (\n{cleaned}\n) AS _sub LIMIT {int(limit)}"

    try:
        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql_query(text(wrapped), conn)
        return df, None
    except Exception as exc:  # noqa: BLE001
        return None, f"Erreur d'execution : {exc}"


def _count_rows(sql: str) -> Optional[int]:
    """Compte le nombre total de lignes du sous-select (best-effort)."""
    cleaned = sql.strip().rstrip(";").rstrip()
    count_sql = f"SELECT count(*) AS n FROM (\n{cleaned}\n) AS _sub"
    try:
        engine = get_engine()
        with engine.connect() as conn:
            row = conn.execute(text(count_sql)).mappings().first()
        return int(row["n"]) if row is not None else None
    except Exception:  # noqa: BLE001
        return None


# === DEFINITION DES OUTILS (function calling) ===
TOOLS = [
    {
        "type": "function",
        "name": "run_sql_query",
        "description": (
            "Execute une requete SQL SELECT en lecture seule pour recuperer des donnees "
            "et repondre a l'utilisateur en langage naturel. "
            f"ATTENTION : ne renvoie qu'un apercu limite a {PREVIEW_ROWS} lignes maximum "
            "(pour ne pas saturer le contexte), mais fournit le nombre total de lignes. "
            "Si l'utilisateur veut voir plus de lignes ou la liste complete, utilise plutot display_table."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "Requete SQL SELECT valide (PostgreSQL).",
                }
            },
            "required": ["sql"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "display_table",
        "description": (
            "Affiche un tableau complet des resultats a l'utilisateur (st.dataframe). "
            f"A utiliser quand l'utilisateur veut voir de nombreuses lignes ou la liste complete "
            f"(jusqu'a {MAX_TABLE_ROWS} lignes). Fournir la requete SQL SELECT."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "Requete SQL SELECT valide (PostgreSQL).",
                }
            },
            "required": ["sql"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "display_chart",
        "description": (
            "Affiche un graphique en courbes (line chart natif) a l'utilisateur. "
            "A utiliser UNIQUEMENT si l'utilisateur demande explicitement un graphe / une courbe / "
            "une visualisation d'evolution. Fournir la requete SQL, la colonne x (souvent une annee "
            "ou une date) et une ou plusieurs colonnes y numeriques."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "Requete SQL SELECT valide (PostgreSQL) renvoyant les colonnes x et y.",
                },
                "x_column": {
                    "type": "string",
                    "description": "Nom de la colonne a utiliser en abscisse (axe x).",
                },
                "y_columns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Nom(s) de la/des colonne(s) numerique(s) a tracer en ordonnee (axe y).",
                },
            },
            "required": ["sql", "x_column", "y_columns"],
            "additionalProperties": False,
        },
    },
]


# === PROMPT SYSTEME ===
SYSTEM_PROMPT = f"""
Tu es un assistant analytique expert PostgreSQL pour la plateforme Territoires en Transition.
Tu converses en langage naturel (en francais) avec l'utilisateur et tu utilises des outils
(function calling) pour interroger la base de donnees et afficher des resultats quand c'est utile.

### DEUX SCHEMAS IMPORTANTS (distinction cruciale) :
Cette base contient deux schemas complementaires. C'est A TOI de comprendre lequel utiliser
(ou de croiser les deux) selon la question :

- **prod** : contient les DONNEES APPLICATIVES de production (miroir de l'app en prod) :
  collectivites, fiches action, plans, axes, indicateurs, labellisation, droits utilisateurs, etc.
  Toutes ces tables sont prefixees `prod.` (ex: `prod.collectivite`, `prod.fiche_action`, `prod.axe`).
  A utiliser pour le detail applicatif fin (contenu precis d'une fiche action, d'un plan, etc.).

- **public** : contient les DONNEES DE STATISTIQUES / METRIQUES, pre-agregees et alimentees
  quotidiennement depuis la prod (frequentation, activite, PAP, scoring, labellisation, exports
  ADEME/Airtable, indicateurs OD, etc.). Toutes ces tables sont prefixees `public.`
  (ex: `public.activite_semaine`, `public.ct_actives`, `public.pap_date_passage`, `public.fa_distrib`).
  A PRIVILEGIER pour les questions de stats / metriques / usage : c'est plus fiable et plus rapide.

Regles de choix du schema :
- Question sur l'usage, la frequentation, les metriques, les stats publiques, les OKRs, l'activation,
  le scoring PAP, la labellisation agregee -> schema `public` (tables deja calculees).
- Question sur le detail applicatif precis d'une collectivite / fiche action / plan / indicateur -> schema `prod`.
- Tu peux CROISER les deux schemas via `collectivite_id` (JOIN) quand c'est pertinent.
- Attention : les tables `public.collectivite`, `public.cot`, `public.labellisation`, etc. sont des
  versions STATS (colonnes et semantique differentes des tables `prod.*` du meme nom). Fie-toi au schema fourni.

### Filtrage des collectivites de test :
- Dans le schema `prod`, exclus systematiquement les collectivites de test : `prod.collectivite.type != 'test'`.
- Dans le schema `public` (stats), les collectivites de test et les utilisateurs internes sont DEJA exclus
  par construction : inutile de re-filtrer.

### Contexte du schema (liste des tables et colonnes, prod.* et public.*) :
{tables_text}

### Documentation detaillee des tables de statistiques (schema public / OLAP) :
{OLAP_DOC}

### Outils a ta disposition :
- run_sql_query(sql) : execute une requete SELECT et te renvoie un APERCU (au maximum {PREVIEW_ROWS} lignes)
  ainsi que le nombre total de lignes et de colonnes. Utilise-le pour recuperer des donnees et
  repondre directement en langage naturel. Comme l'apercu est limite a {PREVIEW_ROWS} lignes, si
  l'utilisateur veut consulter davantage de lignes (ex: "les 50 premiers", "la liste complete",
  "toutes les collectivites"), n'essaie pas de tout lister dans le texte : utilise display_table.
- display_table(sql) : affiche un tableau complet a l'utilisateur (jusqu'a {MAX_TABLE_ROWS} lignes).
- display_chart(sql, x_column, y_columns) : affiche un graphique en courbes. A utiliser UNIQUEMENT
  si l'utilisateur demande explicitement un graphe / une courbe / une visualisation graphique.
  Choisis une colonne x pertinente (souvent une annee ou une date, triee) et des colonnes y numeriques.

### Regles de decision :
- Pour une question simple dont la reponse tient en quelques lignes -> run_sql_query puis reponse en texte.
- Pour "montre-moi / affiche / liste" un grand nombre de lignes -> display_table.
- Pour un graphe / courbe / evolution demande explicitement -> display_chart.
- Tu peux enchainer plusieurs outils si necessaire (ex: explorer avec run_sql_query puis display_table).
- Apres avoir affiche un tableau ou un graphe, ajoute toujours un court commentaire en langage naturel.

### Regles SQL :
- Utilise UNIQUEMENT des requetes SELECT (jamais INSERT, UPDATE, DELETE, DROP, etc.).
- Utilise des jointures explicites (JOIN ... ON ...).
- Limite-toi aux tables et colonnes presentes dans le schema.
- Exclus les collectivites de test comme indique plus haut (prod.collectivite.type != 'test' pour le schema prod ; deja exclues dans le schema public).
- Prefixe TOUJOURS tes tables avec leur schema (prod. ou public.) pour lever toute ambiguite.
- N'INTERROGE JAMAIS `information_schema` (ni `pg_catalog`) pour explorer/decouvrir les tables ou colonnes.
  L'INTEGRALITE du schema (tables et colonnes des schemas prod.* et public.*) t'est DEJA fournie ci-dessus :
  fie-toi exclusivement a ces informations. Ne fais pas de requete d'exploration prealable
  (ex: `SELECT ... FROM information_schema.columns WHERE column_name ILIKE '%...%'`) :
  passe directement a la requete metier qui repond a la question.

### Informations importantes (metier, s'appliquent aux tables du schema prod) :
- Les plans (ou plan d'action) sont contenus dans la table prod.axe (lorsque id=plan), le lien est fait avec les fiches actions par prod.fiche_action_axe.
- Un indicateur est "personnalise" lorsque prod.indicateur_definition.collectivite_id est non null.
- Le budget d'investissement pour une fiche action est dans prod.fiche_action_budget avec type='investissement'.
- Dans notre langage courant, on appelle "mesure" ou "mesure du referentiel" ce qui est une action dans notre base de donnees.
- Une fiche action liee a une fiche action se trouve dans prod.fiche_action_lien et une fiche action liee a une mesure se trouve dans prod.fiche_action_action.
- Le droit des utilisateurs se trouve dans prod.private_utilisateur_droit, dans la colonne niveau_acces.
- On appelle souvent FA ou action ce qui est en fait une fiche_action dans notre base de donnees.
- Une sous-action est une action (prod.fiche_action) dont le parent_id est non null.
- Le nombre d'étoile est dans la table prod.labellisation
- Une collectivité avec un cot est juste une collectivité dans la table prod.cot, une collectivité sans cot n'est pas dans cette table.
- La completion du référentiel est le calcul (point_fait+point_programme+point_pas_fait)/point_potentiel*100 de la table score_snapshot (%)
- Les conseillers sont les utilisateurs qui ont au moins une fois private_collectivite_membre.fonction='conseiller'
- Quand on parler d'indicateurs, on donne très souvent son 'identifiant_referentiel' qui peut ressembler à cae_43.a ou covoit_lieu par exemple.
- Quand on parle de valeurs d'indicateurs, il faut cherchr dans la table prod.indicateur_valeur. La colonne 'indicateur_id' est l'id de l'indicateur de prod.indicateur_definition.

### Ton :
- Professionnel, factuel, concis. N'invente jamais de chiffres : appuie-toi uniquement sur les resultats des outils.
"""


# === STREAMING + BOUCLE AGENT ===
def _stream_and_collect(
    client: OpenAI,
    *,
    on_text_chunk: Optional[Callable[[str], None]] = None,
    on_tool_call_started: Optional[Callable[[], None]] = None,
    **create_kwargs,
) -> tuple[object, str]:
    """
    Execute client.responses.create en streaming.
    Retourne (final_response, accumulated_text).
    """
    accumulated_text = ""
    final_response = None
    tool_call_signaled = False

    stream = client.responses.create(stream=True, **create_kwargs)
    for event in stream:
        event_type = getattr(event, "type", "")
        if event_type == "response.output_text.delta":
            delta = getattr(event, "delta", "") or ""
            if delta:
                accumulated_text += delta
                if on_text_chunk:
                    on_text_chunk(accumulated_text)
        elif event_type == "response.output_item.added":
            item = getattr(event, "item", None)
            if item is not None and getattr(item, "type", "") == "function_call":
                if on_tool_call_started and not tool_call_signaled:
                    on_tool_call_started()
                    tool_call_signaled = True
        elif event_type == "response.completed":
            final_response = getattr(event, "response", None)

    return final_response, accumulated_text.strip()


def _extract_final_text(response_obj: object, fallback_text: str = "") -> str:
    """Recupere le texte final depuis un objet response, avec fallback sur le stream."""
    if response_obj is not None:
        text_out = (getattr(response_obj, "output_text", "") or "").strip()
        if text_out:
            return text_out
        logger.warning(
            "Stream completed without output_text. status=%s incomplete_details=%s",
            getattr(response_obj, "status", None),
            getattr(response_obj, "incomplete_details", None),
        )
    return fallback_text.strip()


def _render_table_artifact(container, df: pd.DataFrame, sql: str, key_suffix: str) -> None:
    """Affiche un tableau (st.dataframe) + bouton de telechargement CSV."""
    container.caption(f"{len(df)} ligne(s) x {len(df.columns)} colonne(s)")
    container.dataframe(df, width="stretch")
    csv = df.to_csv(index=False).encode("utf-8")
    container.download_button(
        label="💾 Telecharger (CSV)",
        data=csv,
        file_name="resultats_requete.csv",
        mime="text/csv",
        key=f"download_{key_suffix}",
    )


def _render_chart_artifact(
    container, df: pd.DataFrame, x_column: str, y_columns: list[str]
) -> None:
    """Affiche un line chart natif a partir des colonnes x/y."""
    if x_column and x_column in df.columns:
        chart_df = df.set_index(x_column)
    else:
        chart_df = df
    valid_y = [c for c in (y_columns or []) if c in chart_df.columns]
    if valid_y:
        chart_df = chart_df[valid_y]
    container.line_chart(chart_df)


def _execute_tool_calls(
    function_calls: list,
    *,
    artifacts: list,
    sql_queries: list,
    render_container,
    on_status: Optional[Callable[[str], None]] = None,
    key_prefix: str = "",
) -> list[dict]:
    """
    Execute chaque function_call, rend les artifacts en live, les accumule pour
    la persistance, et renvoie les function_call_output a renvoyer au modele.
    """
    tool_outputs: list[dict] = []

    for idx, call in enumerate(function_calls):
        name = getattr(call, "name", "")
        try:
            args = json.loads(getattr(call, "arguments", "") or "{}")
        except json.JSONDecodeError:
            args = {}

        sql = args.get("sql", "")
        if sql:
            sql_queries.append(sql)

        if name == "run_sql_query":
            if on_status:
                on_status("Querying the database...")
            df, err = safe_run_sql(sql, limit=PREVIEW_ROWS)
            if err:
                payload = {"error": err}
            else:
                total = _count_rows(sql)
                payload = {
                    "columns": list(df.columns),
                    "column_count": len(df.columns),
                    "total_row_count": total if total is not None else len(df),
                    "preview_row_count": len(df),
                    "preview_rows": json.loads(df.to_json(orient="records", date_format="iso")),
                    "note": (
                        f"Apercu limite a {PREVIEW_ROWS} lignes. Pour afficher plus de lignes "
                        "a l'utilisateur, utilise display_table."
                    ),
                }

        elif name == "display_table":
            if on_status:
                on_status("Preparing the table...")
            df, err = safe_run_sql(sql, limit=MAX_TABLE_ROWS)
            if err:
                payload = {"error": err}
                render_container.error(err)
            else:
                key_suffix = f"{key_prefix}_{idx}"
                _render_table_artifact(render_container, df, sql, key_suffix)
                artifacts.append({"kind": "table", "df": df, "sql": sql})
                payload = {
                    "status": "tableau affiche a l'utilisateur",
                    "row_count": len(df),
                    "column_count": len(df.columns),
                }

        elif name == "display_chart":
            if on_status:
                on_status("Preparing the chart...")
            x_column = args.get("x_column", "")
            y_columns = args.get("y_columns", []) or []
            df, err = safe_run_sql(sql, limit=MAX_CHART_ROWS)
            if err:
                payload = {"error": err}
                render_container.error(err)
            else:
                try:
                    _render_chart_artifact(render_container, df, x_column, y_columns)
                    artifacts.append(
                        {
                            "kind": "chart",
                            "df": df,
                            "sql": sql,
                            "x_column": x_column,
                            "y_columns": y_columns,
                        }
                    )
                    payload = {
                        "status": "graphique affiche a l'utilisateur",
                        "row_count": len(df),
                        "x_column": x_column,
                        "y_columns": y_columns,
                    }
                except Exception as exc:  # noqa: BLE001
                    err = f"Erreur d'affichage du graphique : {exc}"
                    render_container.error(err)
                    payload = {"error": err}

        else:
            payload = {"error": f"Outil inconnu : {name}"}

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(payload, ensure_ascii=False, default=str),
            }
        )

    return tool_outputs


def run_stats_agent(
    user_request: str,
    *,
    previous_response_id: Optional[str],
    render_container,
    key_prefix: str,
    on_status: Optional[Callable[[str], None]] = None,
    on_text_chunk: Optional[Callable[[str], None]] = None,
) -> tuple[str, list, list, Optional[str]]:
    """
    Execute un tour de conversation de l'agent.

    Retourne (texte_final, artifacts, sql_queries, nouveau_response_id).
    """
    client = get_openai_client()

    # Chainage via previous_response_id pour garder le contexte cote serveur.
    if previous_response_id:
        initial_input: list[dict] = [{"role": "user", "content": user_request}]
        chain_kwargs: dict = {"previous_response_id": previous_response_id}
    else:
        initial_input = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request},
        ]
        chain_kwargs = {}

    def _on_tool_call_started() -> None:
        if on_status:
            on_status("Preparing a query...")

    current_response, streamed_text = _stream_and_collect(
        client,
        model=MODEL,
        input=initial_input,
        tools=TOOLS,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        reasoning={"effort": REASONING_EFFORT},
        on_text_chunk=on_text_chunk,
        on_tool_call_started=_on_tool_call_started,
        **chain_kwargs,
    )

    artifacts: list = []
    sql_queries: list = []

    for iteration in range(MAX_TOOL_ITERATIONS):
        if current_response is None:
            break

        function_calls = [
            item
            for item in (current_response.output or [])
            if getattr(item, "type", "") == "function_call"
        ]
        if not function_calls:
            break

        tool_outputs = _execute_tool_calls(
            function_calls,
            artifacts=artifacts,
            sql_queries=sql_queries,
            render_container=render_container,
            on_status=on_status,
            key_prefix=f"{key_prefix}_it{iteration}",
        )
        if not tool_outputs:
            break

        if on_status:
            on_status("Generating response...")

        current_response, streamed_text = _stream_and_collect(
            client,
            model=MODEL,
            previous_response_id=current_response.id,
            input=tool_outputs,
            tools=TOOLS,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            reasoning={"effort": REASONING_EFFORT},
            on_text_chunk=on_text_chunk,
        )

    final_text = _extract_final_text(current_response, streamed_text)
    new_response_id = (
        getattr(current_response, "id", None) if current_response is not None else None
    )
    return final_text, artifacts, sql_queries, new_response_id


# === RENDU D'UN MESSAGE ASSISTANT (live + historique) ===
def render_assistant_message(message: dict, *, key_prefix: str) -> None:
    """Rend un message assistant : texte, artifacts (tableau/graphe) puis SQL en expander."""
    if message.get("content"):
        st.markdown(message["content"])

    for idx, artifact in enumerate(message.get("artifacts", [])):
        if artifact["kind"] == "table":
            _render_table_artifact(
                st.container(),
                artifact["df"],
                artifact.get("sql", ""),
                key_suffix=f"{key_prefix}_{idx}",
            )
        elif artifact["kind"] == "chart":
            _render_chart_artifact(
                st.container(),
                artifact["df"],
                artifact.get("x_column", ""),
                artifact.get("y_columns", []),
            )

    sql_queries = message.get("sql_queries", [])
    if sql_queries:
        with st.expander(f"📝 Voir les requetes SQL ({len(sql_queries)})"):
            for q in sql_queries:
                st.code(q, language="sql")


# === INITIALISATION SESSION ===
if "messages" not in st.session_state:
    st.session_state.messages = []
if "previous_response_id" not in st.session_state:
    st.session_state.previous_response_id = None

# En-tete minimaliste
st.markdown(
    """
<div style='text-align: center; padding: 1rem 0 2rem 0;'>
    <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🧠 IA Transitos</h1>
    <p style='color: #666; font-size: 1rem;'>Langae naturel, tableaux et graphes pour les transitos.</p>
</div>
""",
    unsafe_allow_html=True,
)

# Bouton de reinitialisation et compteur
col1, col2 = st.columns([3, 1])
with col1:
    num_messages = len(st.session_state.messages)
    if num_messages > 0:
        st.caption(f"💬 {num_messages} message(s) dans la conversation")
with col2:
    if st.button("🔄 Nouvelle conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.previous_response_id = None
        st.rerun()

# Avertissement si le contexte devient trop long
if len(st.session_state.messages) >= 20:
    st.warning(
        "⚠️ **Attention** : Le contexte s'allonge a chaque requete, ce qui augmente les couts "
        "et peut ralentir les reponses. Il est recommande de lancer une nouvelle conversation.",
        icon="⚠️",
    )

# Affichage de l'historique des messages
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            render_assistant_message(message, key_prefix=f"history_{idx}")

# Zone de saisie
user_request = st.chat_input(
    "Posez votre question en langage naturel"
)

# === TRAITEMENT DE LA REQUETE ===
if user_request:
    st.session_state.messages.append({"role": "user", "content": user_request})

    with st.chat_message("user"):
        st.markdown(user_request)

    with st.chat_message("assistant"):
        # Le statut (progression) est repliable ; la reponse et les artefacts sont
        # rendus EN DEHORS du statut pour rester toujours visibles.
        status = st.status("Thinking...", expanded=True)
        response_placeholder = st.empty()
        artifacts_container = st.container()
        sql_container = st.container()

        try:
            def update_status(label: str) -> None:
                status.update(label=label, state="running")

            def update_text(current_text: str) -> None:
                response_placeholder.markdown(current_text)

            key_prefix = f"turn_{len(st.session_state.messages)}"

            final_text, artifacts, sql_queries, new_response_id = run_stats_agent(
                user_request,
                previous_response_id=st.session_state.previous_response_id,
                render_container=artifacts_container,
                key_prefix=key_prefix,
                on_status=update_status,
                on_text_chunk=update_text,
            )

            response_placeholder.markdown(final_text)

            if sql_queries:
                with sql_container.expander(f"📝 Voir les requetes SQL ({len(sql_queries)})"):
                    for q in sql_queries:
                        st.code(q, language="sql")

            status.update(label="Reponse terminee", state="complete", expanded=False)

            if new_response_id:
                st.session_state.previous_response_id = new_response_id

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": final_text,
                    "artifacts": artifacts,
                    "sql_queries": sql_queries,
                }
            )
        except Exception as exc:  # noqa: BLE001
            status.update(label="Erreur pendant le traitement", state="error")
            error_msg = f"❌ Erreur de generation : {exc}"
            st.error(error_msg)
            st.session_state.messages.append(
                {"role": "assistant", "content": error_msg}
            )
