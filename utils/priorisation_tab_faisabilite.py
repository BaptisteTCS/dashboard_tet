"""Onglet 1 — Priorisation des actions (arbitrage de faisabilité)."""

from __future__ import annotations

import streamlit as st

from utils.priorisation_data import (
    CATEGORIES,
    PriorisationContext,
    load_faisabilite,
    save_faisabilite,
)

# ==========================
# Constantes
# ==========================

FAISABILITE_OPTIONS = (
    "Non pertinent",
    "A discuter avec l'élu",
    "Pertinent",
)

# Notes de mobilisation : 0 = non mobilisé, 1 = partiellement, 2 = bien, 3 = pleinement
NOTES_SOUS_MOBILISEES = (0, 1)

# 1 = Non pertinent, 2 = A discuter avec l'élu, 3 = Pertinent
FAISABILITE_TO_INT = {label: i for i, label in enumerate(FAISABILITE_OPTIONS, start=1)}
INT_TO_FAISABILITE = {v: k for k, v in FAISABILITE_TO_INT.items()}

TOP_N_INITIAL = 5
TOP_N_MAX = 10

SESSION_FAISABILITE = "faisabilite_choices"
SESSION_COLLECTIVITE = "faisabilite_collectivite_id"
SESSION_SHOW_MORE = "faisabilite_show_more"
SESSION_FLASH = "faisabilite_flash"


# ==========================
# Potentiel non mobilisé
# ==========================


def volet_dans_perimetre(
    levier: str,
    cat: int,
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> bool:
    """Volet sur lequel la collectivité peut agir : pas hors compétence et poids > 0."""
    if (levier, cat) in exclusions:
        return False
    return weights.get(levier, {}).get(cat, 0.0) > 0


def volet_est_mobilise(
    levier: str,
    cat: int,
    notes: dict[tuple[str, int], int],
) -> bool:
    """Volet bien (2) ou pleinement (3) mobilisé : plus rien à arbitrer dessus."""
    return notes.get((levier, cat), 0) not in NOTES_SOUS_MOBILISEES


def potentiel_volet(
    levier: str,
    cat: int,
    reduction: float,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> float:
    """
    Potentiel d'un volet (levier × catégorie) : abs(réduction du levier) × poids
    de la catégorie. Nul si le volet est déjà mobilisé ou hors du périmètre.
    """
    if not volet_dans_perimetre(levier, cat, exclusions, weights):
        return 0.0
    if volet_est_mobilise(levier, cat, notes):
        return 0.0
    return abs(reduction) * weights[levier][cat]


def volets_perimetre(
    levier: str,
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> list[int]:
    """Volets du levier sur lesquels la collectivité peut agir."""
    return [
        cat
        for cat in range(1, 7)
        if volet_dans_perimetre(levier, cat, exclusions, weights)
    ]


def volets_sous_mobilises(
    levier: str,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> list[int]:
    """Volets arbitrables : non ou partiellement mobilisés, dans le périmètre."""
    return [
        cat
        for cat in volets_perimetre(levier, exclusions, weights)
        if not volet_est_mobilise(levier, cat, notes)
    ]


def calc_potentiel_non_mobilise(
    levier: str,
    reduction: float,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> float:
    """Somme des potentiels des volets non ou partiellement mobilisés du levier."""
    return sum(
        potentiel_volet(levier, cat, reduction, notes, exclusions, weights)
        for cat in range(1, 7)
    )


def top_leviers_sous_mobilises(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
    n: int = TOP_N_MAX,
) -> list[tuple[str, float]]:
    """Top N leviers par potentiel non mobilisé décroissant."""
    scored: list[tuple[str, float]] = []
    for levier in leviers:
        if levier not in reductions:
            continue
        potentiel = calc_potentiel_non_mobilise(
            levier, reductions[levier], notes, exclusions, weights
        )
        if potentiel > 0:
            scored.append((levier, potentiel))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:n]


# ==========================
# Arbitrages de faisabilité
# ==========================


def set_categorie_faisabilite(
    levier: str,
    cat: int,
    label: str,
    faisabilites: dict[tuple[str, int], int],
) -> None:
    faisabilites[(levier, cat)] = FAISABILITE_TO_INT[label]


def faisabilite_commune(
    levier: str,
    cats: tuple[int, ...],
    faisabilites: dict[tuple[str, int], int],
) -> str | None:
    """Label partagé par tous les volets du levier, None si les choix diffèrent."""
    valeurs = {faisabilites.get((levier, cat)) for cat in cats}
    if len(valeurs) != 1:
        return None
    (valeur,) = valeurs
    return INT_TO_FAISABILITE.get(valeur) if valeur else None


def faisabilites_from_db(
    df,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> dict[tuple[str, int], int]:
    """Charge les arbitrages persistés en ne gardant que les volets encore arbitrables."""
    result: dict[tuple[str, int], int] = {}
    for _, row in df.iterrows():
        levier = row["levier"]
        cat = int(row["categorie"])
        fais = int(row["faisabilite"])
        if fais not in INT_TO_FAISABILITE:
            continue
        if cat not in volets_sous_mobilises(levier, notes, exclusions, weights):
            continue
        result[(levier, cat)] = fais
    return result


def collect_faisabilites_to_save(
    faisabilites: dict[tuple[str, int], int],
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> list[tuple[str, int, int]]:
    """Liste triée des arbitrages valides à persister (catégories renseignées uniquement)."""
    rows: list[tuple[str, int, int]] = []
    for (levier, cat), fais in faisabilites.items():
        if fais not in INT_TO_FAISABILITE:
            continue
        if cat not in volets_sous_mobilises(levier, notes, exclusions, weights):
            continue
        rows.append((levier, cat, fais))
    return sorted(rows, key=lambda x: (x[0], x[1]))


def init_session_faisabilite(
    collectivite_id: int,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> None:
    if st.session_state.get(SESSION_COLLECTIVITE) == collectivite_id:
        return
    df = load_faisabilite(collectivite_id)
    st.session_state[SESSION_FAISABILITE] = faisabilites_from_db(
        df, notes, exclusions, weights
    )
    st.session_state[SESSION_COLLECTIVITE] = collectivite_id
    st.session_state.pop(SESSION_SHOW_MORE, None)


def sync_segmented_key(key: str, label: str | None) -> None:
    """Synchronise un segmented control : sélectionné ou indéterminé (default=None)."""
    if label is not None:
        st.session_state[key] = label
    elif key in st.session_state:
        del st.session_state[key]


def message_sauvegarde(nom_collectivite: str, n: int) -> str:
    if n == 0:
        return (
            f"Arbitrage enregistré pour **{nom_collectivite}** "
            "(aucun volet renseigné)."
        )
    if n == 1:
        return (
            f"Arbitrage enregistré pour **{nom_collectivite}** "
            f"({n} volet)."
        )
    return (
        f"Arbitrage enregistré pour **{nom_collectivite}** "
        f"({n} volets)."
    )


# ==========================
# Callbacks widgets
# ==========================


def _on_categorie_change(levier: str, cat: int) -> None:
    key = f"faisabilite_cat_{levier}_{cat}"
    label = st.session_state[key]
    faisabilites = st.session_state[SESSION_FAISABILITE]
    set_categorie_faisabilite(levier, cat, label, faisabilites)


def _on_tout_change(levier: str, cats: tuple[int, ...]) -> None:
    label = st.session_state[f"faisabilite_tout_{levier}"]
    if label is None:
        return
    faisabilites = st.session_state[SESSION_FAISABILITE]
    for cat in cats:
        set_categorie_faisabilite(levier, cat, label, faisabilites)


# ==========================
# Rendu
# ==========================


def render(ctx: PriorisationContext) -> None:
    st.warning(
        """
**Arbitrez la pertinence d'agir sur chaque levier.**

Indiquez la pertinence d'agir au regard de vos contraintes et de vos priorités politiques :
- **Non pertinent** : ce levier n'entre pas dans vos priorités actuelles
- **Pertinent** : ce levier correspond à une priorité pour votre collectivité
- **À discuter avec l'élu** : la décision nécessite un arbitrage politique

Nous vous proposerons ensuite des **actions de référence**, et vous pourrez explorer **les actions menées par d'autres collectivités**.
""",
        icon=":material/tips_and_updates:",
    )

    with st.expander("Définition des leviers et catégories"):
        st.info("""
**Vos actions, regroupées par volet.**

Toutes les actions de vos plans d'actions déposés sur Territoires en Transitions ont été regroupées par volet, soit le croisement entre :
- **un levier** : vélo, rénovation, véhicule électrique, etc.
- **une catégorie** : aménagement, planification, financement, gouvernance, exemplarité, sensibilisation.

Le potentiel de réduction des émissions de GES de chaque volet a été estimé à partir de la Stratégie nationale bas carbone (SNBC) et des Mondrians de la transition écologique.
""")

        st.info("""
**1. Aménagement & infrastructures**

Les actions physiques sur le territoire, au bénéfice des habitants et des acteurs économiques : urbanisme, mobilités douces, espaces verts, renaturation, réseaux (eau, chaleur, assainissement), équipements publics. C'est le levier le plus structurant, mais aussi le plus lourd en investissement.

**2. Planification**

Les documents cadres et actes juridiques qui orientent l'action du territoire : PLU/PLUi, PCAET, SCoT, règlements locaux, zones à faibles émissions, arrêtés municipaux. Un levier puissant, car il s'impose durablement à tous les acteurs.

**3. Financement & fiscalité**

L'orientation des flux économiques : subventions aux particuliers et aux entreprises, tarification incitative (déchets, eau), budgets participatifs écologiques, fiscalité locale verte. Agit sur les signaux prix et sur la capacité d'investissement des acteurs du territoire.

**4. Gouvernance & partenariats**

La manière dont la collectivité pilote sa politique de transition : élu référent, service dédié, feuille de route, coopération intercommunale, partenariats privés et associatifs, concertation citoyenne, suivi et évaluation. Répond à la question : comment décide-t-on, et avec qui ?

**5. Exemplarité interne**

La transition appliquée au fonctionnement propre de la collectivité : rénovation du patrimoine bâti, flotte de véhicules, restauration collective (écoles, crèches, EHPAD), commande publique responsable, numérique responsable, formation des agents. Le périmètre sur lequel la collectivité a le plus de prise directe.

**6. Sensibilisation & accompagnement**

L'information, l'éducation et le conseil aux habitants, aux entreprises et aux associations : guichet unique rénovation, animations scolaires, ateliers, communication, accompagnement de projets citoyens. Un impact plus diffus, mais indispensable à l'adhésion et au passage à l'action.
""")

    if SESSION_FAISABILITE not in st.session_state:
        st.session_state[SESSION_FAISABILITE] = {}

    init_session_faisabilite(
        ctx.collectivite_id, ctx.notes, ctx.exclusions, ctx.weights
    )
    faisabilites: dict[tuple[str, int], int] = st.session_state[SESSION_FAISABILITE]

    top = top_leviers_sous_mobilises(
        ctx.leviers_reduction,
        ctx.reductions,
        ctx.notes,
        ctx.exclusions,
        ctx.weights,
    )

    if not top:
        st.info(
            "Aucun levier sous mobilisé identifié pour cette collectivité "
            "(tous les volets dans le périmètre sont bien mobilisés, "
            "ou aucune réduction disponible).",
            icon=":material/task_alt:",
        )
        st.caption(
            "Passez à l'onglet **Actions de référence** pour explorer les actions."
        )
        return

    show_more = st.session_state.get(SESSION_SHOW_MORE, False)
    n_visible = TOP_N_MAX if show_more else TOP_N_INITIAL
    visible_top = top[:n_visible]

    st.subheader(
        f"Les {len(visible_top)} leviers au plus fort potentiel de réduction GES "
        "pour votre collectivité"
    )

    for rank, (levier, potentiel) in enumerate(visible_top, start=1):
        with st.container(border=True):
            cats_arbitrables = tuple(
                volets_sous_mobilises(
                    levier, ctx.notes, ctx.exclusions, ctx.weights
                )
            )

            col_titre, col_tout = st.columns([2, 3], vertical_alignment="center")
            with col_titre:
                st.markdown(f"**{rank}. {levier}**")
            with col_tout:
                if cats_arbitrables:
                    tout_key = f"faisabilite_tout_{levier}"
                    sync_segmented_key(
                        tout_key,
                        faisabilite_commune(levier, cats_arbitrables, faisabilites),
                    )

                    st.segmented_control(
                        f"Tout - {levier}",
                        options=list(FAISABILITE_OPTIONS),
                        key=tout_key,
                        default=None,
                        label_visibility="collapsed",
                        on_change=_on_tout_change,
                        args=(levier, cats_arbitrables),
                    )

            with st.expander("Détail par catégorie"):
                for cat in volets_perimetre(levier, ctx.exclusions, ctx.weights):
                    c1, c2 = st.columns([1, 4], vertical_alignment="center")
                    with c1:
                        st.caption(CATEGORIES[cat])
                    with c2:
                        if volet_est_mobilise(levier, cat, ctx.notes):
                            st.badge(
                                "Mobilisé",
                                icon=":material/check_circle:",
                                color="green",
                            )
                            continue

                        cat_key = f"faisabilite_cat_{levier}_{cat}"
                        cat_val = faisabilites.get((levier, cat))
                        cat_label = (
                            INT_TO_FAISABILITE.get(cat_val) if cat_val else None
                        )
                        sync_segmented_key(cat_key, cat_label)

                        st.segmented_control(
                            CATEGORIES[cat],
                            options=list(FAISABILITE_OPTIONS),
                            key=cat_key,
                            default=None,
                            label_visibility="collapsed",
                            on_change=_on_categorie_change,
                            args=(levier, cat),
                        )

            st.caption(
                "Potentiel de réduction du levier non mobilisé : "
                f"**{potentiel:.0f}** ktCO₂e"
            )

    if len(top) > TOP_N_INITIAL and not show_more:
        if st.button("Afficher plus", type="secondary", key="faisabilite_show_more_btn"):
            st.session_state[SESSION_SHOW_MORE] = True
            st.rerun()
    elif len(top) > TOP_N_INITIAL and show_more:
        if st.button(
            "Afficher moins", type="secondary", key="faisabilite_show_less_btn"
        ):
            st.session_state[SESSION_SHOW_MORE] = False
            st.rerun()

    st.markdown("---")

    if st.button("Sauvegarder", type="primary", key="faisabilite_save"):
        to_save = collect_faisabilites_to_save(
            faisabilites, ctx.notes, ctx.exclusions, ctx.weights
        )
        try:
            save_faisabilite(ctx.collectivite_id, to_save)
            load_faisabilite.clear()
            st.session_state[SESSION_FLASH] = (
                "success",
                message_sauvegarde(ctx.nom, len(to_save)),
            )
        except Exception as e:
            st.session_state[SESSION_FLASH] = (
                "error",
                f"Erreur lors de l'enregistrement : {e}",
            )
        st.rerun()

    flash = st.session_state.pop(SESSION_FLASH, None)
    if flash is not None:
        niveau, message = flash
        if niveau == "success":
            st.success(message, icon=":material/save:")
        else:
            st.error(message, icon=":material/error:")

    st.caption(
        "Passez à l'onglet **Actions de référence** pour explorer les actions "
        "sur vos volets prioritaires."
    )
