import streamlit as st

st.set_page_config(
    page_title="Comparaison des notes de mobilisation",
    page_icon="⚖️",
    layout="wide",
)

import pandas as pd
from streamlit_echarts import st_echarts

from utils.priorisation_data import (
    build_category_weights,
    hors_competence_pairs,
    load_hors_competence,
    load_poids_categories,
)
from utils.priorisation_matrice_leviers import (
    CHART_HEIGHT,
    X_SEUIL_DEFAULT,
    build_matrice_echarts_options,
    build_matrice_leviers,
)
from utils.classification_volet_ges_v2_4 import REGLES, note_case
from utils.mobilisation_v24_compare import (
    NOTE_LABELS_V24,
    load_collectivites_v24,
    load_notes_prod,
    load_notes_v24,
    load_potentiels,
)

CAT_LABELS = {
    1: "1 Aménagement",
    2: "2 Planification",
    3: "3 Financement",
    4: "4 Gouvernance",
    5: "5 Exemplarité",
    6: "6 Sensibilisation",
}

st.title("⚖️ Comparaison des notes de mobilisation")
st.markdown(
    "**Note actuelle** : table `collectivite_volet_ges` de la prod (ancien prompt de notation, lecture seule).  \n"
    "**Nouvelle note** : calculée à partir de la classification v2.4 (Claude Haiku 5.5, une fiche par appel), "
    "selon le nombre de fiches structurantes et peu importantes de chaque case, avec la règle choisie ci-dessous "
    "(0 = aucune action dans les deux règles)."
)
regle = st.radio(
    "Règle de calcul de la nouvelle note",
    list(REGLES),
    format_func=lambda r: REGLES[r][0],
    key="comparaison_mobilisation_regle",
)

notes_v24 = load_notes_v24()
collectivites = load_collectivites_v24()
if notes_v24.empty or not collectivites:
    st.warning("Aucun résultat : lancez d'abord `python scripts/mobilisation_v24.py`.")
    st.stop()

ids = sorted(set(notes_v24["collectivite_id"]) & set(collectivites), key=lambda c: collectivites[c]["nom"])
cid = st.selectbox(
    "Collectivité",
    ids,
    format_func=lambda c: f"{collectivites[c]['nom']} ({c})",
    key="comparaison_mobilisation_cid",
)
info = collectivites[cid]
fiches_titres = info["fiches"]
st.caption(
    f"{info['type_label']} · {info['population'] or '?'} habitants · {len(fiches_titres)} fiches classées "
    "(hors abandonnées et en pause)"
)

# ---------------------------------------------------------------- données
new = notes_v24[notes_v24["collectivite_id"] == cid].copy()
# Note retenue (classification majoritaire) et notes de chaque run, recalculées avec la règle choisie.
new["note"] = [note_case(len(s), len(p), regle) for s, p in zip(new["structurantes"], new["peu_importantes"])]
run_ids = sorted(int(c.removeprefix("n_struct_run")) for c in new.columns if c.startswith("n_struct_run"))
for i in run_ids:
    new[f"note_run{i}"] = [note_case(s, p, regle) for s, p in zip(new[f"n_struct_run{i}"], new[f"n_peu_run{i}"])]
new["stable"] = new[[f"note_run{i}" for i in run_ids]].nunique(axis=1) == 1
prod = load_notes_prod(cid)
weights = build_category_weights(load_poids_categories())
exclusions = hors_competence_pairs(load_hors_competence(cid))
try:
    potentiels, source_potentiels = load_potentiels(cid)
except Exception as e:  # API indisponible : on affiche quand même les notes
    potentiels, source_potentiels = {}, f"indisponible ({type(e).__name__})"

notes_new = {(r.levier, int(r.categorie)): int(r.note) for r in new.itertuples()}
notes_prod = {(r.levier, int(r.categorie)): int(r.note) for r in prod.itertuples()}
leviers = sorted(set(potentiels) | {lv for lv, _ in notes_new} | {lv for lv, _ in notes_prod})
for lv in leviers:  # cases sans action = 0 des deux côtés
    for cat in range(1, 7):
        notes_new.setdefault((lv, cat), 0)
        notes_prod.setdefault((lv, cat), 0)

if prod.empty:
    st.info("Cette collectivité n'a pas encore de notes en prod : seule la nouvelle note est affichée.")

# ---------------------------------------------------------------- chiffres clés
cases = pd.DataFrame(
    [
        {"levier": lv, "categorie": cat, "note_prod": notes_prod[(lv, cat)], "note_new": notes_new[(lv, cat)]}
        for lv in leviers
        for cat in range(1, 7)
        if (lv, cat) not in exclusions
    ]
)
actives = cases[(cases["note_prod"] > 0) | (cases["note_new"] > 0)]
stab = new[new[[c for c in new.columns if c.startswith("note_run")]].max(axis=1) > 0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Cases notées (actuelle → nouvelle)", f"{(cases['note_prod'] > 0).sum()} → {(cases['note_new'] > 0).sum()}")
c2.metric(
    "Même note",
    f"{(actives['note_prod'] == actives['note_new']).mean():.0%}" if len(actives) else "—",
    help="Parmi les cases notées dans l'une ou l'autre version.",
)
c3.metric(
    "Note moyenne des cases notées",
    f"{actives['note_prod'].mean():.2f} → {actives['note_new'].mean():.2f}" if len(actives) else "—",
)
c4.metric(
    "Nouvelle note stable sur les runs",
    f"{stab['stable'].mean():.0%}" if len(stab) else "—",
    help="Part des cases dont la note calculée est identique sur les 3 runs de la classification.",
)

# ---------------------------------------------------------------- matrices
st.subheader("Matrices d'impact")
st.caption(
    f"Potentiel de réduction : {source_potentiels}. Mobilisation = moyenne des notes pondérée par les poids des "
    f"catégories (OLAP), divisée par 3. Seuil : {X_SEUIL_DEFAULT:.0f} %."
)
show_labels = st.toggle("Afficher tous les libellés", value=False)

matrices = {}
if potentiels:
    col_old, col_new = st.columns(2)
    for col, titre, notes, key in (
        (col_old, "Note actuelle (prod)", notes_prod, "old"),
        (col_new, "Nouvelle note (v2.4)", notes_new, "new"),
    ):
        df_m, _ = build_matrice_leviers(leviers, notes, weights, potentiels, exclusions)
        matrices[key] = df_m
        with col:
            st.markdown(f"**{titre}** — {int((df_m['quadrant'] == 'angles_morts').sum()) if len(df_m) else 0} angles morts")
            if df_m.empty:
                st.info("Aucun levier à afficher.")
            else:
                st_echarts(
                    options=build_matrice_echarts_options(df_m, x_seuil=X_SEUIL_DEFAULT, show_all_labels=show_labels),
                    height=f"{CHART_HEIGHT}px",
                    key=f"cmp_matrice_{key}_{cid}_{regle}_{int(show_labels)}",
                )
else:
    st.warning("Pas de potentiel de réduction disponible : les matrices ne peuvent pas être tracées.")

# ---------------------------------------------------------------- par levier
if matrices.get("old") is not None and matrices.get("new") is not None and len(matrices["new"]):
    st.subheader("Par levier")
    m = matrices["old"][["levier", "mobilisation_pct", "quadrant_label"]].merge(
        matrices["new"][["levier", "mobilisation_pct", "quadrant_label", "potentiel_ktco2e"]],
        on="levier",
        suffixes=("_old", "_new"),
        how="outer",
    )
    m["ecart"] = m["mobilisation_pct_new"] - m["mobilisation_pct_old"]
    m = m.sort_values("potentiel_ktco2e", ascending=False)
    st.dataframe(
        m[["levier", "potentiel_ktco2e", "mobilisation_pct_old", "mobilisation_pct_new", "ecart",
           "quadrant_label_old", "quadrant_label_new"]],
        column_config={
            "levier": "Levier",
            "potentiel_ktco2e": st.column_config.NumberColumn("Potentiel (ktCO₂e)", format="%.1f"),
            "mobilisation_pct_old": st.column_config.NumberColumn("Mobilisation actuelle", format="%.0f %%"),
            "mobilisation_pct_new": st.column_config.NumberColumn("Nouvelle mobilisation", format="%.0f %%"),
            "ecart": st.column_config.NumberColumn("Écart (points)", format="%+.0f"),
            "quadrant_label_old": "Quadrant actuel",
            "quadrant_label_new": "Nouveau quadrant",
        },
        hide_index=True,
        use_container_width=True,
    )

# ---------------------------------------------------------------- par case
st.subheader("Par case levier × catégorie")
detail = new.set_index(["levier", "categorie"])
rows = []
for r in actives.itertuples():
    key = (r.levier, r.categorie)
    d = detail.loc[key] if key in detail.index else None
    runs = [int(d[c]) for c in detail.columns if c.startswith("note_run")] if d is not None else []
    prod_ids = next((x for x in prod.loc[(prod["levier"] == r.levier) & (prod["categorie"] == r.categorie), "fiche_ids"]), [])
    rows.append({
        "Levier": r.levier,
        "Catégorie": CAT_LABELS[r.categorie],
        "Note actuelle": int(r.note_prod),
        "Nouvelle note": int(r.note_new),
        "Écart": int(r.note_new) - int(r.note_prod),
        "Notes des runs": " / ".join(map(str, runs)) if runs else "—",
        "Stable": bool(d["stable"]) if d is not None else True,
        "Structurantes": len(d["structurantes"]) if d is not None else 0,
        "Peu importantes": len(d["peu_importantes"]) if d is not None else 0,
        "Fiches en prod": len(prod_ids),
    })
df_cases = pd.DataFrame(rows)

f1, f2 = st.columns([1, 2])
with f1:
    seulement_ecarts = st.toggle("Seulement les cases qui changent", value=False)
with f2:
    filtre_levier = st.multiselect("Leviers", sorted(df_cases["Levier"].unique()) if len(df_cases) else [])
view = df_cases
if seulement_ecarts and len(view):
    view = view[view["Écart"] != 0]
if filtre_levier:
    view = view[view["Levier"].isin(filtre_levier)]
st.dataframe(view, hide_index=True, use_container_width=True)
if len(df_cases):
    st.caption(
        "Répartition des nouvelles notes : "
        + " · ".join(f"{NOTE_LABELS_V24[n]} {k}" for n, k in df_cases["Nouvelle note"].value_counts().sort_index().items())
    )

# ---------------------------------------------------------------- détail d'une case
st.subheader("Fiches d'une case")
if len(df_cases):
    choix = st.selectbox(
        "Case",
        list(zip(df_cases["Levier"], df_cases["Catégorie"])),
        format_func=lambda k: f"{k[0]} — {k[1]}",
    )
    lv, cat_label = choix
    cat = int(cat_label.split()[0])
    d = detail.loc[(lv, cat)] if (lv, cat) in detail.index else None
    prod_ids = next((x for x in prod.loc[(prod["levier"] == lv) & (prod["categorie"] == cat), "fiche_ids"]), [])
    fiches_rows = []
    if d is not None:
        fiches_rows += [{"Fiche": i, "Titre": fiches_titres.get(i, "?"), "Nouvelle classification": "Structurante"} for i in d["structurantes"]]
        fiches_rows += [{"Fiche": i, "Titre": fiches_titres.get(i, "?"), "Nouvelle classification": "Peu importante"} for i in d["peu_importantes"]]
    nouveaux = {r["Fiche"] for r in fiches_rows}
    for i in prod_ids:
        if i not in nouveaux:
            fiches_rows.append({"Fiche": i, "Titre": fiches_titres.get(i, "(hors périmètre v2.4)"), "Nouvelle classification": "Absente"})
    for r in fiches_rows:
        r["Dans la case en prod"] = r["Fiche"] in prod_ids
    st.dataframe(pd.DataFrame(fiches_rows), hide_index=True, use_container_width=True)
