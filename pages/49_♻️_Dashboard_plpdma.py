import streamlit as st

st.set_page_config(
    page_title="Dashboard PLPDMA",
    page_icon="♻️",
    layout="wide",
)

import html
import re
import unicodedata

import pandas as pd
from sqlalchemy import text

from utils.db import get_engine_prod

PLAN_ECONOMIE_CIRCULAIRE = 5

THEMES = [
    {
        "label": "Biodéchets, gestion de proximité, compostage",
        "keywords": [
            "biodechet",
            "compost",
            "lombricompost",
            "bokashi",
            "bioseau",
            "gestion de proximite",
        ],
    },
    {
        "label": "Réemploi",
        "keywords": [
            "reemploi",
            "re-emploi",
            "reutilisation",
            "reparation",
            "ressourcerie",
            "repair cafe",
        ],
    },
    {
        "label": "Sobriété",
        "keywords": [
            "sobriet",
            "stop pub",
            "stop-pub",
            "achat durable",
            "achats durables",
            "achats responsables",
            "achat responsable",
            "commande publique",
            "eco-exempl",
            "eco exempl",
            "exemplar",
            "usage unique",
            "vaisselle jetable",
            "eco-conception",
            "ecoconception",
            "suremballage",
            "consommation responsable",
        ],
    },
    {
        "label": "Communication et sensibilisation des usagers",
        "audience": "usagers",
    },
    {
        "label": "Communication et sensibilisation des professionnels",
        "audience": "professionnels",
    },
    {
        "label": "Tarification incitative ou redevance spéciale",
        "keywords": [
            "tarification incitative",
            "redevance incitative",
            "redevance speciale",
        ],
    },
    {
        "label": "Déchets verts",
        "keywords": [
            "dechet vert",
            "dechets verts",
            "vegetal",
            "vegetaux",
            "broyat",
            "broyage",
            "tonte",
            "jardinage",
        ],
    },
    {
        "label": "Gaspillage alimentaire",
        "keywords": ["gaspillage alimentaire"],
    },
]

USAGER_WORDS = ("usager", "habitant", "citoyen", "grand public", "scolaire", "famille", "foyer", "enfant")
PRO_WORDS = ("professionnel", "entreprise", "commercant", "artisan", "metier de bouche")
SENSIB_USAGERS = ("sensibil", "sensibl", "communic", "campagne", "animation")
SENSIB_PRO = ("sensibil", "sensibl", "communic", "campagne", "accompagn", "former")

TAG_RE = re.compile(r"<[^>]+>")
YEAR_RE = re.compile(r"(20\d{2})\s*[-–—/]\s*(20\d{2})")
ETP_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*etp", re.IGNORECASE)
DMA_RE = re.compile(
    r"(reduir\w*|reduction|baisse|diminution).{0,70}?(\d+(?:[.,]\d+)?)\s*%"
)
DMA_RE_AFTER = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*%\s+de\s+(diminution|reduction|baisse).{0,40}?dma"
)


def _strip_html(value) -> str:
    plain = html.unescape(TAG_RE.sub(" ", "" if value is None else str(value)))
    return re.sub(r"\s+", " ", plain).strip()


def _fold(value) -> tuple[str, list[int]]:
    """Texte sans accent, avec l'index de chaque caractère dans le texte d'origine."""
    plain = _strip_html(value).replace("’", "'").replace("`", "'")
    chars: list[str] = []
    index: list[int] = []
    for i, ch in enumerate(plain):
        if ch.isspace():
            if chars and chars[-1] != " ":
                chars.append(" ")
                index.append(i)
            continue
        folded = unicodedata.normalize("NFD", ch)
        folded = "".join(c for c in folded if unicodedata.category(c) != "Mn").lower()
        for c in folded:
            chars.append(c)
            index.append(i)
    return "".join(chars), index


def _norm(value) -> str:
    return _fold(value)[0]


def _is_plpdma(nom: str) -> bool:
    folded = _norm(nom)
    return (
        "plpdma" in folded
        or "programme local de prevention des dechets menagers" in folded
        or "programme local prevention des dechets menagers" in folded
    )


def _themes_of(titre: str, objectifs: str) -> list[str]:
    title = _norm(titre)
    blob = f"{title} {_norm(objectifs)}"
    found: list[str] = []
    for theme in THEMES:
        audience = theme.get("audience")
        if audience == "usagers":
            has_sensib = any(k in title for k in SENSIB_USAGERS)
            has_public = any(k in title for k in USAGER_WORDS)
            has_pro = any(k in title for k in PRO_WORDS)
            if has_sensib and (has_public or not has_pro):
                found.append(theme["label"])
        elif audience == "professionnels":
            has_sensib = any(k in title for k in SENSIB_PRO)
            if has_sensib and any(k in title for k in PRO_WORDS):
                found.append(theme["label"])
        elif any(k in blob for k in theme["keywords"]):
            found.append(theme["label"])
    return found


def _etp_of(ressources: str) -> float:
    values = [float(token.replace(",", ".")) for token in ETP_RE.findall(_strip_html(ressources))]
    return max(values) if values else 0.0


def _excerpt(plain: str, index: list[int], start: int, end: int) -> str:
    if not index:
        return ""
    start = max(0, min(start, len(index) - 1))
    end = max(start + 1, min(end, len(index)))
    snippet = plain[index[start] : index[end - 1] + 1]
    return re.sub(r"\s+", " ", snippet).strip()


def _extract_dma(blobs: list[str]) -> tuple[str, str]:
    """Repère un pourcentage de réduction des DMA, pas un pourcentage de composition."""
    best: tuple[float, str, str] | None = None
    for raw in blobs:
        folded, index = _fold(raw)
        if "%" not in folded:
            continue
        plain = _strip_html(raw)
        matches = [(m, m.group(2)) for m in DMA_RE.finditer(folded)]
        matches += [(m, m.group(1)) for m in DMA_RE_AFTER.finditer(folded)]
        for match, pct_raw in matches:
            pct = float(pct_raw.replace(",", "."))
            if pct < 5 or pct > 40:
                continue
            before = folded[match.start() : match.end()]
            after = folded[match.end() :]
            next_pct = re.search(r"\d+(?:[.,]\d+)?\s*%", after)
            after_clause = after[: next_pct.start()] if next_pct else after
            after_clause = after_clause[:45]
            window = f"{before}{after_clause}"
            focused = (
                "dma" in before
                or "dma" in after_clause
                or "production de dechets" in before
                or "gisement global" in window
            )
            if not focused:
                continue
            noisy = any(
                token in window
                for token in ("gaspillage", "biodechet", "alimentaire", "textile", "veget", "emballage", "papier")
            )
            if noisy and "dma" not in window and "production de dechets" not in before:
                continue
            score = (3 if "dma" in window else 1) + pct / 100
            excerpt = _excerpt(plain, index, match.start(), match.end() + len(after_clause))
            if best is None or score > best[0]:
                best = (score, pct_raw.replace(".", ","), excerpt)
    if best is None:
        return "", ""
    return f"-{best[1]} %", best[2]


def _temporalite(nom: str, date_debut, date_fin) -> str:
    if pd.notna(date_debut) or pd.notna(date_fin):
        debut = pd.to_datetime(date_debut).strftime("%d/%m/%Y") if pd.notna(date_debut) else ""
        fin = pd.to_datetime(date_fin).strftime("%d/%m/%Y") if pd.notna(date_fin) else ""
        return " – ".join(part for part in (debut, fin) if part)
    match = YEAR_RE.search(nom or "")
    if match:
        return f"{match.group(1)} – {match.group(2)}"
    return ""


def _query(sql: str, params: dict) -> pd.DataFrame:
    engine = get_engine_prod()
    with engine.connect() as conn:
        return pd.read_sql_query(text(sql), conn, params=params)


@st.cache_data(ttl="1d", show_spinner="Chargement des plans PLPDMA…")
def load_plpdma() -> tuple[pd.DataFrame, pd.DataFrame]:
    plans = _query(
        """
        SELECT a.id AS plan_id, a.nom, c.nom AS collectivite,
               a.date_debut, a.date_fin, a.description
        FROM axe a
        JOIN collectivite c ON c.id = a.collectivite_id
        WHERE a.type = :type_plan
          AND a.id = a.plan
          AND c.type <> 'test'
        """,
        {"type_plan": PLAN_ECONOMIE_CIRCULAIRE},
    )
    plans = plans[plans["nom"].fillna("").map(_is_plpdma)].copy()
    if plans.empty:
        return plans, pd.DataFrame()

    ids = plans["plan_id"].astype(int).tolist()
    axes = _query(
        """
        WITH RECURSIVE tree AS (
            SELECT id AS plan_id, id, 0 AS depth
            FROM axe
            WHERE id = ANY(:ids)
            UNION ALL
            SELECT t.plan_id, a.id, t.depth + 1
            FROM axe a
            JOIN tree t ON a.parent = t.id
            WHERE t.depth < 6
        )
        SELECT plan_id,
               count(*) FILTER (WHERE depth = 1) AS nb_axes,
               count(*) FILTER (WHERE depth >= 2) AS nb_sous_axes
        FROM tree
        GROUP BY plan_id
        """,
        {"ids": ids},
    )
    actions = _query(
        """
        WITH RECURSIVE tree AS (
            SELECT id AS plan_id, id, 0 AS depth
            FROM axe
            WHERE id = ANY(:ids)
            UNION ALL
            SELECT t.plan_id, a.id, t.depth + 1
            FROM axe a
            JOIN tree t ON a.parent = t.id
            WHERE t.depth < 6
        )
        SELECT DISTINCT
            t.plan_id,
            fa.id AS fiche_id,
            fa.titre,
            fa.description,
            fa.objectifs,
            fa.ressources,
            fa.budget_previsionnel
        FROM tree t
        JOIN fiche_action_axe faa ON faa.axe_id = t.id
        JOIN fiche_action fa ON fa.id = faa.fiche_id
        WHERE fa.parent_id IS NULL
          AND (fa.deleted IS NULL OR fa.deleted = false)
        """,
        {"ids": ids},
    )
    budgets = _query(
        """
        WITH RECURSIVE tree AS (
            SELECT id AS plan_id, id, 0 AS depth
            FROM axe
            WHERE id = ANY(:ids)
            UNION ALL
            SELECT t.plan_id, a.id, t.depth + 1
            FROM axe a
            JOIN tree t ON a.parent = t.id
            WHERE t.depth < 6
        ),
        fiches AS (
            SELECT DISTINCT t.plan_id, fa.id AS fiche_id
            FROM tree t
            JOIN fiche_action_axe faa ON faa.axe_id = t.id
            JOIN fiche_action fa ON fa.id = faa.fiche_id
            WHERE fa.parent_id IS NULL
              AND (fa.deleted IS NULL OR fa.deleted = false)
        )
        SELECT f.plan_id, coalesce(sum(fab.budget_previsionnel), 0) AS budget_lignes
        FROM fiches f
        JOIN fiche_action_budget fab ON fab.fiche_id = f.fiche_id
        GROUP BY f.plan_id
        """,
        {"ids": ids},
    )

    if actions.empty:
        actions = pd.DataFrame(
            columns=["plan_id", "fiche_id", "titre", "description", "objectifs", "ressources", "budget_previsionnel"]
        )

    actions["etp"] = actions["ressources"].map(_etp_of)
    actions["themes"] = [
        _themes_of(titre, objectifs)
        for titre, objectifs in zip(actions["titre"].fillna(""), actions["objectifs"].fillna(""))
    ]

    budget_fa = actions.groupby("plan_id")["budget_previsionnel"].sum()
    etp_plan = actions.groupby("plan_id")["etp"].sum()
    nb_actions = actions.groupby("plan_id")["fiche_id"].nunique()
    budget_lignes = budgets.set_index("plan_id")["budget_lignes"] if not budgets.empty else pd.Series(dtype=float)
    axes_idx = axes.set_index("plan_id") if not axes.empty else pd.DataFrame()

    rows = []
    action_rows = []
    plans_by_id = plans.set_index("plan_id")
    for plan_id, plan in plans_by_id.iterrows():
        sub = actions[actions["plan_id"] == plan_id]
        blobs = [plan["description"] or "", plan["nom"] or ""]
        blobs += sub["objectifs"].fillna("").tolist()
        blobs += sub["description"].fillna("").tolist()
        blobs += sub["titre"].fillna("").tolist()
        objectif, extrait = _extract_dma(blobs)

        budget_action = float(budget_fa.get(plan_id, 0) or 0)
        budget_detail = float(budget_lignes.get(plan_id, 0) or 0)
        budget = budget_action if budget_action > 0 else budget_detail
        etp = float(etp_plan.get(plan_id, 0) or 0)
        n_actions = int(nb_actions.get(plan_id, 0) or 0)
        axe_row = axes_idx.loc[plan_id] if plan_id in axes_idx.index else None

        rows.append(
            {
                "plan_id": int(plan_id),
                "Collectivité": plan["collectivite"],
                "Intitulé": plan["nom"],
                "Temporalité": _temporalite(plan["nom"], plan["date_debut"], plan["date_fin"]),
                "Objectif de réduction DMA": objectif,
                "Extrait": extrait,
                "Nb d'axes": int(axe_row["nb_axes"]) if axe_row is not None else 0,
                "Nb de sous-axes": int(axe_row["nb_sous_axes"]) if axe_row is not None else 0,
                "Nb d'actions": n_actions,
                "Budget alloué": budget if budget > 0 else None,
                "ETP pilotes": round(etp, 2) if etp > 0 else None,
            }
        )
        for _, action in sub.iterrows():
            action_rows.append(
                {
                    "plan_id": int(plan_id),
                    "Collectivité": plan["collectivite"],
                    "Titre": action["titre"],
                    "Thèmes": ", ".join(action["themes"]),
                    "ETP": action["etp"] if action["etp"] else None,
                }
            )

    df_plans = pd.DataFrame(rows).sort_values(
        ["Collectivité", "Intitulé"], na_position="last"
    )
    if action_rows:
        df_actions = pd.DataFrame(action_rows)
    else:
        df_actions = pd.DataFrame(columns=["plan_id", "Collectivité", "Titre", "Thèmes", "ETP"])
    return df_plans.reset_index(drop=True), df_actions.reset_index(drop=True)


def _theme_summary(df_actions: pd.DataFrame, nb_plans: int) -> pd.DataFrame:
    rows = []
    for theme in THEMES:
        label = theme["label"]
        if df_actions.empty:
            n_plans, n_actions = 0, 0
        else:
            mask = df_actions["Thèmes"].fillna("").str.contains(label, regex=False)
            n_plans = int(df_actions.loc[mask, "plan_id"].nunique())
            n_actions = int(mask.sum())
        rows.append(
            {
                "Thème": label,
                "Plans": n_plans,
                "Part des plans": (n_plans / nb_plans) if nb_plans else 0,
                "Actions": n_actions,
            }
        )
    return pd.DataFrame(rows)


# ==========================
# Interface
# ==========================

st.title("♻️ Dashboard PLPDMA")
st.caption(
    "Recensement des plans d'actions de la rubrique Économie circulaire et déchets "
    "dont l'intitulé est un PLPDMA, puis lecture de leurs actions."
)

with st.expander("Critères de recensement et de lecture"):
    st.markdown(
        """
Un plan est retenu s'il est de type **Plan Économie Circulaire & Déchets**
et si son intitulé contient **PLPDMA** ou **programme local de prévention des déchets ménagers**.
Les autres plans de cette rubrique (feuilles de route économie circulaire, contrats déchets, etc.)
sont écartés. Les collectivités de test sont écartées.

Un plan est **exploitable** dès qu'il porte au moins une action non supprimée.
Les axes sont les enfants directs du plan, les sous-axes tous les niveaux en dessous.
Les sous-actions ne sont pas comptées dans les actions.

L'objectif de réduction des DMA, le budget et les ETP n'ont pas de champ dédié au plan.
L'objectif est recherché dans les textes (réduction, baisse ou diminution, de 5 à 40 %,
rattachée aux DMA, au gisement global ou à la production de déchets).
Le budget est la somme des budgets prévisionnels d'actions, ou à défaut des lignes budgétaires annuelles.
Les ETP sont lus dans le champ ressources de chaque action : s'il y a plusieurs valeurs
(montée en charge), la plus haute est retenue, puis les actions sont additionnées.
        """
    )
    st.markdown("**Thèmes recherchés dans les actions**")
    for theme in THEMES:
        if theme.get("keywords"):
            st.markdown(f"- **{theme['label']}** : {', '.join(theme['keywords'])}")
        elif theme.get("audience") == "usagers":
            st.markdown(
                f"- **{theme['label']}** : le titre contient un mot de communication "
                f"({', '.join(SENSIB_USAGERS)}) et vise les usagers, ou ne vise pas les professionnels."
            )
        else:
            st.markdown(
                f"- **{theme['label']}** : le titre contient un mot de communication "
                f"({', '.join(SENSIB_PRO)}) et vise les professionnels."
            )

df_plans_all, df_actions_all = load_plpdma()

if df_plans_all.empty:
    st.info("Aucun plan PLPDMA trouvé dans la rubrique Économie circulaire et déchets.")
    st.stop()

collectivites = sorted(df_plans_all["Collectivité"].dropna().unique())
selection = st.multiselect(
    "Rechercher une ou plusieurs collectivités",
    options=collectivites,
    placeholder="Toutes les collectivités",
)
if selection:
    df_plans = df_plans_all[df_plans_all["Collectivité"].isin(selection)].copy()
    df_actions = df_actions_all[df_actions_all["Collectivité"].isin(selection)].copy()
else:
    df_plans = df_plans_all
    df_actions = df_actions_all

exploitables = df_plans[df_plans["Nb d'actions"] > 0]
vides = df_plans[df_plans["Nb d'actions"] == 0]

st.markdown("---")
cols = st.columns(5)
cols[0].metric("Plans PLPDMA", len(df_plans))
cols[1].metric("Plans exploitables", len(exploitables))
cols[2].metric(
    "Objectif DMA repéré",
    int(exploitables["Objectif de réduction DMA"].fillna("").ne("").sum()),
)
cols[3].metric("Budget renseigné", int(exploitables["Budget alloué"].notna().sum()))
cols[4].metric("ETP renseignés", int(exploitables["ETP pilotes"].notna().sum()))

st.subheader("Plans exploitables")
st.caption(
    "La durée réglementaire d'un PLPDMA est de 6 ans. "
    "La temporalité vient des dates du plan, ou à défaut des années présentes dans l'intitulé. "
    "L'extrait montre la phrase d'où l'objectif DMA a été lu."
)

table_cols = [
    "Collectivité",
    "Intitulé",
    "Temporalité",
    "Objectif de réduction DMA",
    "Nb d'axes",
    "Nb de sous-axes",
    "Nb d'actions",
    "Budget alloué",
    "ETP pilotes",
    "Extrait",
]
st.dataframe(
    exploitables[table_cols],
    width="stretch",
    hide_index=True,
    column_config={
        "Budget alloué": st.column_config.NumberColumn(format="%.0f €"),
        "ETP pilotes": st.column_config.NumberColumn(format="%.2f"),
        "Intitulé": st.column_config.TextColumn(width="medium"),
        "Extrait": st.column_config.TextColumn(width="large"),
    },
)

if not vides.empty:
    with st.expander(f"{len(vides)} plans recensés sans action"):
        st.dataframe(
            vides[["Collectivité", "Intitulé", "Temporalité"]],
            width="stretch",
            hide_index=True,
        )

st.markdown("---")
st.subheader("Thèmes des actions")
st.caption(
    "Une action est comptée dans un thème dès que son titre ou ses objectifs correspondent. "
    "Une même action peut porter plusieurs thèmes. "
    "La communication est lue sur le titre seul, pour ne pas compter chaque description qui mentionne une sensibilisation."
)

summary = _theme_summary(df_actions, len(exploitables))
st.dataframe(
    summary,
    width="stretch",
    hide_index=True,
    column_config={
        "Part des plans": st.column_config.ProgressColumn(
            min_value=0,
            max_value=1,
            format="percent",
        ),
    },
)

st.markdown("---")
st.subheader("Actions d'un plan")

if exploitables.empty:
    st.info("Aucun plan exploitable pour cette sélection.")
else:
    options = {
        int(row.plan_id): f"{row.Collectivité} — {row.Intitulé}"
        for row in exploitables.itertuples(index=False)
    }
    chosen = st.selectbox(
        "Plan",
        options=list(options),
        format_func=lambda plan_id: options[plan_id],
    )
    detail = df_actions[df_actions["plan_id"] == chosen][["Titre", "Thèmes", "ETP"]]
    st.dataframe(
        detail.sort_values("Titre", na_position="last"),
        width="stretch",
        hide_index=True,
        column_config={"ETP": st.column_config.NumberColumn(format="%.2f")},
    )
