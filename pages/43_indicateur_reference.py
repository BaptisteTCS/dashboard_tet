import streamlit as st

st.set_page_config(
    page_title="Indicateurs de référence",
    page_icon="🌞",
    layout="wide",
)

import os
import re
import time

import anthropic
import pandas as pd
from sqlalchemy import text
from streamlit_elements import elements, mui, nivo

from utils.db import get_engine

_COULEUR_BAR = "#5B8FF9"
_BAR_ROW_PX = 40
_BAR_MIN_HEIGHT = 280

_MODELE_HAIKU = "claude-haiku-4-5"
_THEME_EXCLU = "non_classable"
_MAX_LIBELLES = 3

theme_actif = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#31333F",
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 12,
            "fill": "#333333",
        }
    },
    "tooltip": {
        "container": {
            "background": "rgba(255, 255, 255, 0.95)",
            "color": "#31333F",
            "fontSize": "13px",
            "fontFamily": "Source Sans Pro, sans-serif",
            "borderRadius": "4px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
            "padding": "8px 12px",
            "border": "1px solid rgba(0, 0, 0, 0.1)",
        }
    },
}


# ==========================
# Chargement des données
# ==========================


@st.cache_data(ttl="1d", show_spinner="Chargement des indicateurs de référence…")
def load_indicateur_reference() -> pd.DataFrame:
    engine = get_engine()
    query = text('SELECT theme, libelle, nb_ct FROM public.indicateur_reference')
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    df["nb_ct"] = pd.to_numeric(df["nb_ct"], errors="coerce").fillna(0).astype(int)
    return df


def _theme_to_nivo_bar(df: pd.DataFrame) -> list[dict]:
    """Barres horizontales : plus forte valeur en haut."""
    if df.empty:
        return []
    agg = (
        df.groupby("theme", dropna=False)
        .size()
        .reset_index(name="nb_indicateurs")
        .sort_values("nb_indicateurs", ascending=False)
    )
    agg["theme"] = agg["theme"].fillna("Non renseigné").astype(str)
    return agg.to_dict(orient="records")[::-1]


# ==========================
# Catalogue envoyé au modèle
# ==========================


@st.cache_data(show_spinner=False)
def build_catalogue(df: pd.DataFrame) -> tuple[str, dict[int, str], dict[int, dict]]:
    """Numérote thèmes et libellés une fois pour toutes.

    Le texte produit doit être stable d'un rerun à l'autre : c'est lui qui sert
    de préfixe mis en cache côté Anthropic.
    """
    work = df.dropna(subset=["theme", "libelle"]).copy()
    work["theme"] = work["theme"].astype(str).str.strip()
    work["libelle"] = work["libelle"].astype(str).str.strip()
    work = work[work["theme"].str.lower() != _THEME_EXCLU]
    work = work.sort_values(["theme", "libelle"], kind="stable")

    lignes: list[str] = []
    themes: dict[int, str] = {}
    libelles: dict[int, dict] = {}
    num_libelle = 0

    for num_theme, (nom_theme, sous_df) in enumerate(work.groupby("theme", sort=False), 1):
        themes[num_theme] = nom_theme
        lignes.append(f"T{num_theme} {nom_theme}")
        for ligne in sous_df.itertuples(index=False):
            num_libelle += 1
            libelles[num_libelle] = {
                "num_theme": num_theme,
                "theme": nom_theme,
                "libelle": ligne.libelle,
                "nb_ct": int(ligne.nb_ct),
            }
            lignes.append(f"{num_libelle} {ligne.libelle}")

    return "\n".join(lignes), themes, libelles


# ==========================
# Appel Claude Haiku
# ==========================

_INSTRUCTIONS = """L'utilisateur te donne le titre d'une ACTION de transition écologique menée par une collectivité française (ex : "Aménager des pistes cyclables", "Rénover l'éclairage public").
Tu dois trouver dans le catalogue ci-dessous les indicateurs qui permettent de mesurer l'avancement ou l'impact de cette action (ex : pour "Aménager des pistes cyclables" -> "Linéaire de pistes cyclables").

Le catalogue liste des thèmes (lignes "T<num> <thème>") suivis de leurs libellés d'indicateurs (lignes "<num> <libellé>").

1. Choisis LE thème le plus pertinent pour l'action.
2. Dans ce thème uniquement, choisis de 0 à 3 libellés, du plus au moins pertinent. Au moins 1, sauf si vraiment aucun indicateur ne permet de mesurer cette action.

Un indicateur pertinent mesure ce que l'action produit ou transforme, pas seulement le sujet dont elle parle.

Réponds uniquement par : T<num du thème>:<num>,<num>,<num>
Si aucun libellé ne correspond : T<num du thème>:0
Aucun autre texte, aucune explication.

CATALOGUE :
"""

_RE_REPONSE = re.compile(r"T?\s*(\d+)\s*:\s*([\d,\s]*)")


def _get_anthropic_api_key() -> str:
    try:
        depuis_secrets = st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        depuis_secrets = ""
    return str(depuis_secrets or os.getenv("ANTHROPIC_API_KEY") or "")


@st.cache_resource(show_spinner=False)
def get_anthropic_client() -> anthropic.Anthropic | None:
    """Client réutilisé entre les reruns pour garder le pool de connexions HTTPS."""
    cle = _get_anthropic_api_key()
    if not cle:
        return None
    return anthropic.Anthropic(api_key=cle)


@st.cache_data(ttl="1h", show_spinner=False)
def suggerer_indices(texte: str, catalogue_txt: str) -> tuple[int | None, list[int]]:
    """Renvoie (numéro de thème, numéros de libellés) choisis par Haiku."""
    client = get_anthropic_client()
    if client is None:
        raise RuntimeError(
            "Clé ANTHROPIC_API_KEY manquante : configurez-la dans secrets.toml "
            "ou dans les variables d'environnement."
        )

    reponse = client.messages.create(
        model=_MODELE_HAIKU,
        max_tokens=24,
        # Le SDK anthropic 1.0 a retiré temperature de la signature : extra_body
        # est la voie documentée, et fonctionne aussi sur les versions 0.x.
        extra_body={"temperature": 0},
        system=[
            {
                "type": "text",
                "text": _INSTRUCTIONS + catalogue_txt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": texte}],
    )

    brut = "".join(bloc.text for bloc in reponse.content if bloc.type == "text")
    correspondance = _RE_REPONSE.search(brut)
    if not correspondance:
        return None, []

    num_theme = int(correspondance.group(1))
    nums_libelles = [
        int(morceau)
        for morceau in correspondance.group(2).split(",")
        if morceau.strip().isdigit() and int(morceau) > 0
    ]
    return num_theme, nums_libelles[:_MAX_LIBELLES]


def _joli_theme(nom: str) -> str:
    """Les thèmes sont stockés en snake_case, illisible et interprété par markdown."""
    return nom.replace("_", " ").capitalize()


def resoudre_suggestion(
    texte: str,
    catalogue_txt: str,
    themes: dict[int, str],
    libelles: dict[int, dict],
) -> dict:
    num_theme, nums_libelles = suggerer_indices(texte, catalogue_txt)
    retenus = [libelles[num] for num in nums_libelles if num in libelles]
    # Si le modèle a mal numéroté le thème, on le redéduit des libellés retenus.
    nom_theme = themes.get(num_theme) if num_theme else None
    if retenus and (nom_theme is None or retenus[0]["num_theme"] != num_theme):
        nom_theme = retenus[0]["theme"]
    return {"theme": nom_theme, "libelles": retenus}


# ==========================
# Interface
# ==========================

st.title("📐 Indicateurs de référence")

df = load_indicateur_reference()

if df.empty:
    st.warning("Aucun indicateur de référence trouvé.")
    st.stop()

tab_suggestion, tab_exploration = st.tabs(["✨ Suggestion", "🔎 Exploration"])


with tab_suggestion:
    catalogue_txt, themes_catalogue, libelles_catalogue = build_catalogue(df)

    st.caption("Saisis le titre d'une action pour obtenir les indicateurs de référence qui permettent d'en mesurer l'avancement.")

    with st.form("form_suggestion", border=False):
        col_texte, col_bouton = st.columns([6, 1], vertical_alignment="bottom")
        texte_saisi = col_texte.text_input(
            "Titre de l'action",
            placeholder="ex : Aménager des pistes cyclables",
        )
        soumis = col_bouton.form_submit_button("Entrer", type="primary", width="stretch")

    if soumis and texte_saisi.strip():
        debut = time.perf_counter()
        try:
            resultat = resoudre_suggestion(
                texte_saisi.strip(),
                catalogue_txt,
                themes_catalogue,
                libelles_catalogue,
            )
        except Exception as erreur:  # clé absente, quota, réseau…
            st.session_state["suggestion_resultat"] = None
            st.error(f"Échec de la suggestion : {erreur}")
        else:
            resultat["duree"] = time.perf_counter() - debut
            resultat["texte"] = texte_saisi.strip()
            st.session_state["suggestion_resultat"] = resultat
    elif soumis:
        st.info("Saisis le titre d'une action pour lancer la recherche.")

    resultat = st.session_state.get("suggestion_resultat")
    if resultat:
        if resultat["libelles"]:
            st.badge(_joli_theme(resultat["theme"]), icon=":material/category:", color="blue")
            for rang, item in enumerate(resultat["libelles"], 1):
                with st.container(border=True):
                    st.markdown(f"**{rang}. {item['libelle']}**")
                    st.caption(f"{item['nb_ct']:,} collectivités")
        else:
            message = "Aucun indicateur de référence ne permet de mesurer cette action."
            if resultat["theme"]:
                message += f" Thème le plus proche : **{_joli_theme(resultat['theme'])}**."
            st.info(message)
        st.caption(f"Répondu en {resultat['duree']:.2f} s")


with tab_exploration:
    st.caption(
        f"{len(df):,} indicateurs · {df['theme'].nunique():,} thèmes · "
        f"{int(df['nb_ct'].sum()):,} collectivités cumulées"
    )

    st.dataframe(df, width="stretch", hide_index=True)

    st.markdown("---")
    st.subheader("Nombre d'indicateurs par thème")

    bar_data = _theme_to_nivo_bar(df)
    max_label_len = max(len(row["theme"]) for row in bar_data)
    chart_height = max(_BAR_MIN_HEIGHT, len(bar_data) * _BAR_ROW_PX + 70)
    left_margin = min(320, max(100, max_label_len * 7))

    with elements("indicateur_reference_theme_bar"):
        with mui.Box(sx={"height": chart_height}):
            nivo.Bar(
                data=bar_data,
                keys=["nb_indicateurs"],
                indexBy="theme",
                layout="horizontal",
                margin={"top": 16, "right": 56, "bottom": 50, "left": left_margin},
                padding=0.35,
                valueScale={"type": "linear", "min": 0},
                indexScale={"type": "band", "round": True},
                colors=[_COULEUR_BAR],
                borderRadius=4,
                borderColor={"from": "color", "modifiers": [["darker", 0.4]]},
                axisTop=None,
                axisRight=None,
                axisBottom={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": "Nombre d'indicateurs",
                    "legendPosition": "middle",
                    "legendOffset": 40,
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 8,
                    "tickRotation": 0,
                },
                enableLabel=True,
                labelSkipWidth=16,
                labelSkipHeight=12,
                labelTextColor="#ffffff",
                animate=True,
                motionConfig="gentle",
                theme=theme_actif,
            )
