import networkx as nx
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from networkx.algorithms.community import louvain_communities, modularity
from matplotlib import pyplot as plt
from pycirclize import Circos
from pyvis.network import Network
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist, squareform
from sqlalchemy import text

from utils.db import get_engine

st.set_page_config(
    page_title="Usages des features",
    page_icon="🕸️",
    layout="wide",
)

PALETTE = [
    "#2E7D32",
    "#1565C0",
    "#EF6C00",
    "#6A1B9A",
    "#C62828",
    "#00838F",
    "#AD1457",
    "#5D4037",
    "#F9A825",
    "#455A64",
]

VUE_JACCARD = "Réseau Jaccard"
VUE_COMMUNAUTES = "Communautés"
VUE_CORDES = "Diagramme en cordes"
VUE_PROFILS = "Profils d'usage"
VUE_CARTE = "Carte des usages"
VUES = [VUE_JACCARD, VUE_COMMUNAUTES, VUE_CORDES, VUE_PROFILS, VUE_CARTE]

CAPTIONS = {
    VUE_JACCARD: (
        "Chaque nœud est une feature. Sa taille reflète le nombre de collectivités "
        "qui l'utilisent, sa couleur le module. Un lien n'apparaît que si l'indice "
        "de Jaccard dépasse le seuil."
    ),
    VUE_COMMUNAUTES: (
        "Les features reliées au-dessus du seuil sont regroupées en communautés : "
        "des ensembles souvent utilisés ensemble. Une feature pont relie plusieurs "
        "communautés entre elles."
    ),
    VUE_CORDES: (
        "Un ruban relie deux features utilisées ensemble. Son épaisseur est le nombre "
        "de collectivités en commun, parmi les paires dont le Jaccard dépasse le seuil. "
        "Les features sont regroupées par module."
    ),
    VUE_PROFILS: (
        "Les collectivités (lignes) et les features (colonnes) sont regroupées par "
        "similarité d'usage, avec une distance de Jaccard. La bande de gauche est le "
        "profil, celle du haut le module."
    ),
    VUE_CARTE: (
        "Chaque point est une collectivité. La position rapproche les usages similaires. "
        "La couleur reprend les profils du clustering hiérarchique."
    ),
}


@st.cache_data(ttl=3600, show_spinner="Chargement de feature_all…")
def charger_feature_all() -> pd.DataFrame:
    """Charge les usages collectivité × feature depuis l'OLAP."""
    engine = get_engine()
    query = text(
        """
        SELECT collectivite_id, feature
        FROM feature_all
        WHERE collectivite_id IS NOT NULL
          AND feature IS NOT NULL
          AND collectivite_id in (select collectivite_id from pap_statut_5_fiches_modifiees_13_semaines where mois>='2026-01-01' and statut='actif')
        """
    )
    with engine.connect() as conn:
        return pd.read_sql_query(query, conn)


def _distances(valeurs: np.ndarray) -> np.ndarray:
    distances = pdist(valeurs, metric="jaccard")
    return np.nan_to_num(distances, nan=1.0)


@st.cache_data(show_spinner="Clustering des profils…")
def clusteriser(matrice: pd.DataFrame, n_clusters: int):
    """Clustering hiérarchique (Jaccard, lien moyen) sur les deux axes."""
    valeurs = matrice.to_numpy(dtype=bool)
    n_clusters = min(n_clusters, len(matrice))
    z_lignes = linkage(_distances(valeurs), method="average")
    z_colonnes = linkage(_distances(valeurs.T), method="average")
    clusters = pd.Series(
        fcluster(z_lignes, t=n_clusters, criterion="maxclust"),
        index=matrice.index,
        name="cluster",
    )
    return z_lignes, z_colonnes, clusters


@st.cache_data(show_spinner="Projection des collectivités…")
def projeter(matrice: pd.DataFrame, methode: str) -> np.ndarray:
    """Projette les collectivités en 2D (UMAP ou t-SNE, distance de Jaccard)."""
    valeurs = matrice.to_numpy(dtype=bool)
    n = len(matrice)
    if methode == "umap":
        import umap

        reducteur = umap.UMAP(
            n_neighbors=max(2, min(15, n - 1)),
            min_dist=0.3,
            metric="jaccard",
            random_state=42,
        )
        coords = reducteur.fit_transform(valeurs)
    else:
        from sklearn.manifold import TSNE

        distances = squareform(_distances(valeurs))
        np.fill_diagonal(distances, 0.0)
        coords = TSNE(
            n_components=2,
            metric="precomputed",
            init="random",
            perplexity=min(30, n - 1),
            random_state=42,
        ).fit_transform(distances)

    # Beaucoup de collectivités ont le même profil et se superposeraient.
    rng = np.random.default_rng(42)
    ecart = float(np.std(coords))
    return coords + rng.normal(0, 0.05 * ecart, coords.shape)


def couleurs_des_clusters(clusters: pd.Series, n_clusters: int) -> dict:
    ids = sorted(clusters.unique())
    palette = sns.color_palette("Set2", max(n_clusters, len(ids))).as_hex()
    return dict(zip(ids, palette))


def afficher_reseau(
    matrice, usage, co_usage, jaccard, couleur_module, modules, seuil, figer: bool
):
    # pap_actif est quasi systématique : elle écrase le réseau.
    pap_actif_retiree = "pap_actif" in matrice.columns
    features = [feature for feature in matrice.columns if feature != "pap_actif"]
    if not features:
        st.info("Aucune feature à afficher une fois pap_actif retirée.")
        return
    n_collectivites = len(matrice)
    net = Network(
        height="850px",
        width="100%",
        bgcolor="#FFFFFF",
        font_color="#222222",
        notebook=False,
        cdn_resources="in_line",
    )

    taille_max = float(usage.reindex(features).max())
    for feature in features:
        n = int(usage[feature])
        net.add_node(
            feature,
            label=feature,
            size=10 + 40 * np.sqrt(n / taille_max),
            color=couleur_module[modules[feature]],
            title=(
                f"{feature}\n{n} collectivités ({n / n_collectivites:.0%})\n"
                f"Module : {modules[feature]}"
            ),
            font={"size": 14},
        )

    nb_liens = 0
    for i, a in enumerate(features):
        for b in features[i + 1 :]:
            j = float(jaccard.loc[a, b])
            if j >= seuil:
                net.add_edge(
                    a,
                    b,
                    value=j,
                    color={"color": "#9E9E9E", "opacity": 0.2 + 0.6 * j},
                    title=(
                        f"{a} ↔ {b}\nJaccard : {j:.2f}\n"
                        f"{int(co_usage.loc[a, b])} collectivités en commun"
                    ),
                )
                nb_liens += 1

    net.force_atlas_2based(
        gravity=-60,
        central_gravity=0.01,
        spring_length=120,
        spring_strength=0.08,
        damping=0.6,
    )

    html = net.generate_html()
    if figer:
        # La physique place les nœuds, puis on fige le graphe.
        html = html.replace(
            "network = new vis.Network(container, data, options);",
            """network = new vis.Network(container, data, options);
                  container.style.visibility = "hidden";
                  network.once("stabilizationIterationsDone", function () {
                      network.setOptions({ physics: false });
                      network.fit();
                      container.style.visibility = "visible";
                  });""",
            1,
        )

    st.caption(
        f"{n_collectivites} collectivités · {len(features)} features · "
        f"{nb_liens} liens (Jaccard ≥ {seuil:.2f})"
        + (" · pap_actif retirée" if pap_actif_retiree else "")
    )
    modules_visibles = {
        modules[feature]: couleur_module[modules[feature]] for feature in features
    }
    st.markdown(_legende_modules(modules_visibles), unsafe_allow_html=True)
    st.iframe(html, height=900)


def afficher_cordes(usage, co_usage, jaccard, couleur_feature, modules, seuil):
    # Co-usage filtré par Jaccard, sans la diagonale.
    mat = co_usage.where(jaccard >= seuil, 0).astype(float)
    valeurs = mat.to_numpy(copy=True)
    np.fill_diagonal(valeurs, 0)
    mat = pd.DataFrame(valeurs, index=mat.index, columns=mat.columns)

    ordre = (
        pd.DataFrame({"module": modules, "usage": usage})
        .sort_values(["module", "usage"], ascending=[True, False])
        .index.tolist()
    )
    mat = mat.loc[ordre, ordre]
    # Triangle supérieur : sinon chaque lien est dessiné deux fois.
    mat = pd.DataFrame(np.triu(mat.to_numpy()), index=ordre, columns=ordre)

    garder = (mat.sum(axis=0) + mat.sum(axis=1)) > 0
    mat = mat.loc[garder, garder]
    if mat.shape[0] < 2:
        st.info("Aucun lien au-dessus de ce seuil de Jaccard.")
        return

    circos = Circos.chord_diagram(
        mat,
        space=2,
        cmap={feature: couleur_feature[feature] for feature in mat.index},
        label_kws=dict(size=8, orientation="vertical", r=105),
        link_kws=dict(ec="none", alpha=0.45, direction=0),
    )
    fig = circos.plotfig(figsize=(11, 11))
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def afficher_profils(matrice, couleur_feature, n_clusters: int):
    if len(matrice) < 2 or matrice.shape[1] < 2:
        st.info("Il faut au moins deux collectivités et deux features.")
        return

    features = matrice.columns.tolist()
    z_lignes, z_colonnes, clusters = clusteriser(matrice, n_clusters)
    couleurs = couleurs_des_clusters(clusters, n_clusters)

    g = sns.clustermap(
        matrice,
        row_linkage=z_lignes,
        col_linkage=z_colonnes,
        row_colors=clusters.map(couleurs).rename("Profil"),
        col_colors=pd.Series(couleur_feature).reindex(features).rename("Module"),
        cmap="Greens",
        yticklabels=False,
        xticklabels=True,
        figsize=(12, 14),
        dendrogram_ratio=(0.12, 0.12),
        cbar_pos=None,
        linewidths=0,
    )
    g.ax_heatmap.set_xticklabels(
        g.ax_heatmap.get_xticklabels(), rotation=90, fontsize=8
    )
    g.ax_heatmap.set_ylabel(f"{len(matrice)} collectivités")
    g.ax_heatmap.set_xlabel("")
    g.fig.suptitle("Profils d'usage des features", y=1.01)
    st.pyplot(g.fig, use_container_width=True)
    plt.close(g.fig)

    profils = matrice.groupby(clusters).mean().T.round(2)
    profils.columns = [
        f"Profil {c} (n={(clusters == c).sum()})" for c in profils.columns
    ]
    st.subheader("Taux d'usage par profil")
    st.dataframe(profils, use_container_width=True)


def afficher_carte(matrice, n_clusters: int, methode: str):
    if len(matrice) < 4:
        st.info("La projection demande au moins quatre collectivités.")
        return

    _, _, clusters = clusteriser(matrice, n_clusters)
    couleurs = couleurs_des_clusters(clusters, n_clusters)
    coords = projeter(matrice, methode)
    projection = pd.DataFrame(
        {
            "x": coords[:, 0],
            "y": coords[:, 1],
            "collectivite_id": matrice.index,
            "nb_features": matrice.sum(axis=1).to_numpy(),
            "profil": clusters.astype(str).to_numpy(),
            "features": matrice.apply(
                lambda ligne: "<br>".join(ligne.index[ligne == 1]), axis=1
            ).to_numpy(),
        }
    )
    fig = px.scatter(
        projection,
        x="x",
        y="y",
        color="profil",
        size="nb_features",
        size_max=14,
        hover_data={
            "collectivite_id": True,
            "nb_features": True,
            "features": True,
            "x": False,
            "y": False,
        },
        color_discrete_map={str(k): v for k, v in couleurs.items()},
        template="simple_white",
        title=f"Carte des usages ({methode.upper()}, distance de Jaccard)",
    )
    fig.update_traces(marker=dict(line=dict(width=0.5, color="white"), opacity=0.8))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(height=750, legend_title_text="Profil")
    st.plotly_chart(fig, use_container_width=True)


def _graphe_jaccard(features, jaccard, seuil: float) -> nx.Graph:
    graphe = nx.Graph()
    graphe.add_nodes_from(features)
    for i, a in enumerate(features):
        for b in features[i + 1 :]:
            poids = float(jaccard.loc[a, b])
            if poids >= seuil:
                graphe.add_edge(a, b, weight=poids, distance=max(1e-6, 1 - poids))
    return graphe


def _detecter_communautes(graphe: nx.Graph, resolution: float):
    if graphe.number_of_nodes() == 0:
        return []
    communautes = louvain_communities(
        graphe, weight="weight", resolution=resolution, seed=42
    )
    return sorted(communautes, key=len, reverse=True)


def _modularite(graphe: nx.Graph, communautes) -> float:
    if graphe.number_of_edges() == 0 or not communautes:
        return 0.0
    return float(modularity(graphe, communautes, weight="weight"))


def _jaccard_interne(jaccard, groupe) -> float:
    groupe = list(groupe)
    if len(groupe) < 2:
        return np.nan
    sous = jaccard.loc[groupe, groupe].to_numpy()
    return float(sous[np.triu_indices(len(groupe), k=1)].mean())


def _tableau_robustesse(features, jaccard, resolution: float, seuil_actuel: float):
    seuils = [0.2, 0.25, 0.3, 0.35, 0.4, 0.5]
    if round(seuil_actuel, 2) not in seuils:
        seuils = sorted(set(seuils + [round(float(seuil_actuel), 2)]))
    lignes = []
    for seuil in seuils:
        graphe = _graphe_jaccard(features, jaccard, seuil)
        communautes = _detecter_communautes(graphe, resolution)
        lignes.append(
            {
                "Seuil": seuil,
                "Liens": graphe.number_of_edges(),
                "Communautés": len(communautes),
                "Isolées": sum(len(groupe) == 1 for groupe in communautes),
                "Modularité": round(_modularite(graphe, communautes), 2),
            }
        )
    return pd.DataFrame(lignes)


def afficher_communautes(
    matrice, usage, jaccard, modules, seuil: float, resolution: float
):
    features = matrice.columns.tolist()
    n_collectivites = len(matrice)
    graphe = _graphe_jaccard(features, jaccard, seuil)
    communautes = _detecter_communautes(graphe, resolution)
    modularite = _modularite(graphe, communautes)

    for u, v, data in graphe.edges(data=True):
        data["distance"] = max(1e-6, 1 - data["weight"])
    degre = dict(graphe.degree(weight="weight"))
    intermediarite = nx.betweenness_centrality(graphe, weight="distance")
    communaute_de = {
        feature: i + 1
        for i, groupe in enumerate(communautes)
        for feature in groupe
    }

    detail = pd.DataFrame(
        {
            "Communauté": pd.Series(communaute_de),
            "Module": modules,
            "Collectivités": usage.astype(int),
            "Taux d'usage": usage / n_collectivites,
            "Degré": pd.Series(degre),
            "Intermédiarité": pd.Series(intermediarite),
        }
    ).sort_values(["Communauté", "Degré"], ascending=[True, False])
    detail.index.name = "Feature"

    groupes = [groupe for groupe in communautes if len(groupe) >= 2]
    isolees = sorted(next(iter(groupe)) for groupe in communautes if len(groupe) == 1)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "Modularité",
        f"{modularite:.2f}",
        help="Proche de 1, les groupes sont nets. Proche de 0, le découpage ne fait pas mieux que le hasard.",
    )
    c2.metric("Communautés", len(groupes), help="Groupes d'au moins deux features.")
    c3.metric(
        "Features isolées",
        len(isolees),
        help="Features sans lien au-dessus du seuil : elles ne rejoignent aucun groupe.",
    )
    c4.metric("Liens", graphe.number_of_edges())

    if not groupes:
        st.info(
            "Aucune communauté : baissez le seuil de Jaccard pour relier davantage de features."
        )
    else:
        st.subheader("Groupes de features utilisées ensemble")
        for debut in range(0, len(groupes), 2):
            colonnes = st.columns(2)
            for colonne, (numero, groupe) in zip(
                colonnes, enumerate(groupes[debut : debut + 2], start=debut + 1)
            ):
                with colonne:
                    with st.container(border=True):
                        coeur = max(groupe, key=lambda feature: degre[feature])
                        interne = _jaccard_interne(jaccard, groupe)
                        st.markdown(f"**Communauté {numero}** · {len(groupe)} features")
                        st.metric(
                            "Jaccard interne",
                            "—" if np.isnan(interne) else f"{interne:.2f}",
                            help="Similarité moyenne des paires du groupe. Proche de 1, elles sont presque toujours utilisées ensemble.",
                        )
                        st.markdown(f"Feature la plus liée : **{coeur}**")
                        comptes = modules[list(groupe)].value_counts()
                        st.caption(
                            "Modules : "
                            + ", ".join(
                                f"{module} ({nombre})"
                                for module, nombre in comptes.items()
                            )
                        )
                        st.dataframe(
                            detail.loc[detail["Communauté"] == numero].drop(
                                columns="Communauté"
                            ),
                            column_config={
                                "Taux d'usage": st.column_config.NumberColumn(
                                    format="percent"
                                ),
                                "Degré": st.column_config.NumberColumn(
                                    format="%.2f",
                                    help="Somme des Jaccard avec les features liées.",
                                ),
                                "Intermédiarité": st.column_config.NumberColumn(
                                    format="%.3f",
                                    help="À quel point la feature sert de passage entre les autres.",
                                ),
                            },
                            use_container_width=True,
                        )

    if isolees:
        st.caption("Sans groupe : " + ", ".join(isolees))

    st.subheader("Features pont")
    st.caption(
        "Une feature pont est un passage entre des groupes qui se parlent peu. "
        "On retient les cinq intermédiarités les plus hautes."
    )
    ponts = detail.nlargest(5, "Intermédiarité")
    if float(ponts["Intermédiarité"].max() or 0) <= 0:
        st.info("Pas de pont : les groupes ne sont pas reliés entre eux.")
    else:
        st.dataframe(
            ponts[["Communauté", "Module", "Intermédiarité", "Taux d'usage"]],
            column_config={
                "Taux d'usage": st.column_config.NumberColumn(format="percent"),
                "Intermédiarité": st.column_config.NumberColumn(format="%.3f"),
            },
            use_container_width=True,
        )

    if groupes:
        st.subheader("Communautés et modules du produit")
        st.caption(
            "Une communauté qui mélange plusieurs modules signale des modules utilisés ensemble."
        )
        dans_un_groupe = detail["Communauté"].isin(range(1, len(groupes) + 1))
        croisement = pd.crosstab(
            detail.loc[dans_un_groupe, "Communauté"].map(lambda i: f"Communauté {i}"),
            detail.loc[dans_un_groupe, "Module"],
        )
        fig = px.imshow(
            croisement,
            text_auto=True,
            color_continuous_scale="Greens",
            aspect="auto",
            labels={"x": "Module", "y": "Communauté", "color": "Features"},
        )
        fig.update_layout(
            height=max(280, 48 * len(croisement) + 80),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sensibilité au seuil")
    st.caption(
        "Même résolution, plusieurs seuils de Jaccard. Une structure stable garde "
        "un nombre de communautés et une modularité proches. Le trait pointillé est le seuil actuel."
    )
    robustesse = _tableau_robustesse(features, jaccard, resolution, seuil)
    gauche, droite = st.columns(2)
    with gauche:
        fig_groupes = px.line(
            robustesse,
            x="Seuil",
            y="Communautés",
            markers=True,
            template="simple_white",
        )
        fig_groupes.add_vline(x=seuil, line_dash="dash", line_color="#9E9E9E")
        fig_groupes.update_layout(height=320, yaxis_title="Communautés")
        st.plotly_chart(fig_groupes, use_container_width=True)
    with droite:
        fig_mod = px.line(
            robustesse,
            x="Seuil",
            y="Modularité",
            markers=True,
            template="simple_white",
        )
        fig_mod.add_vline(x=seuil, line_dash="dash", line_color="#9E9E9E")
        fig_mod.update_layout(height=320, yaxis_title="Modularité")
        st.plotly_chart(fig_mod, use_container_width=True)
    st.dataframe(robustesse, hide_index=True, use_container_width=True)

    with st.expander("Toutes les features"):
        st.dataframe(
            detail,
            column_config={
                "Taux d'usage": st.column_config.NumberColumn(format="percent"),
                "Degré": st.column_config.NumberColumn(format="%.2f"),
                "Intermédiarité": st.column_config.NumberColumn(format="%.3f"),
            },
            use_container_width=True,
        )


def _legende_modules(couleur_module: dict) -> str:
    return " ".join(
        f"<span style='color:{couleur_module[module]}'>●</span> {module}"
        for module in sorted(couleur_module)
    )


st.title("Usages des features")

df = charger_feature_all()
if df.empty:
    st.info("La table feature_all ne contient aucune ligne.")
    st.stop()

matrice = pd.crosstab(df["collectivite_id"], df["feature"]).gt(0).astype(int)

with st.sidebar:
    exclues = st.multiselect(
        "Features à retirer",
        options=sorted(matrice.columns.tolist()),
        placeholder="Aucune",
        help="Ces features sont exclues de toutes les représentations.",
    )

if exclues:
    matrice = matrice.drop(columns=exclues)
matrice = matrice.loc[:, matrice.sum(axis=0) > 0]
matrice = matrice.loc[matrice.sum(axis=1) > 0]
if matrice.empty:
    st.info("Toutes les features ont été retirées.")
    st.stop()

features = matrice.columns.tolist()
usage = matrice.sum(axis=0)
co_usage = matrice.T.dot(matrice)
union = usage.to_numpy()[:, None] + usage.to_numpy()[None, :] - co_usage.to_numpy()
jaccard = pd.DataFrame(
    np.divide(
        co_usage.to_numpy(),
        union,
        out=np.zeros(union.shape, dtype=float),
        where=union > 0,
    ),
    index=features,
    columns=features,
)

modules = pd.Series({feature: feature.split("_")[0] for feature in features})
couleur_module = {
    module: PALETTE[i % len(PALETTE)]
    for i, module in enumerate(sorted(modules.unique()))
}
couleur_feature = {
    feature: couleur_module[modules[feature]] for feature in features
}

vue = st.segmented_control(
    "Représentation",
    options=VUES,
    default=VUE_JACCARD,
)
if vue is None:
    vue = VUE_JACCARD

st.caption(CAPTIONS[vue])

with st.sidebar:
    seuil_jaccard = 0.5
    resolution = 1.0
    n_clusters = 5
    methode = "umap"
    if vue in (VUE_JACCARD, VUE_COMMUNAUTES, VUE_CORDES):
        seuil_jaccard = st.slider(
            "Seuil de Jaccard",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            key="seuil_jaccard",
            help="Liens affichés seulement au-dessus de ce seuil.",
        )
    figer_reseau = True
    if vue == VUE_JACCARD:
        figer_reseau = st.checkbox(
            "Figer le graphe",
            value=True,
            help="Décochez pour laisser les nœuds bouger après le placement.",
        )
    if vue == VUE_COMMUNAUTES:
        resolution = st.slider(
            "Résolution",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Au-dessus de 1, des groupes plus petits et plus nombreux. En dessous, des groupes plus gros.",
        )
    if vue in (VUE_PROFILS, VUE_CARTE):
        n_clusters = st.slider(
            "Nombre de profils",
            min_value=2,
            max_value=max(2, min(12, len(matrice))),
            value=min(5, len(matrice)),
            help="Découpage des collectivités issu du clustering hiérarchique.",
        )
    if vue == VUE_CARTE:
        methode = st.radio("Méthode", ["umap", "tsne"], horizontal=True)

if vue == VUE_JACCARD:
    afficher_reseau(
        matrice,
        usage,
        co_usage,
        jaccard,
        couleur_module,
        modules,
        seuil_jaccard,
        figer_reseau,
    )
elif vue == VUE_COMMUNAUTES:
    afficher_communautes(matrice, usage, jaccard, modules, seuil_jaccard, resolution)
elif vue == VUE_CORDES:
    afficher_cordes(
        usage, co_usage, jaccard, couleur_feature, modules, seuil_jaccard
    )
elif vue == VUE_PROFILS:
    afficher_profils(matrice, couleur_feature, n_clusters)
else:
    afficher_carte(matrice, n_clusters, methode)
