"""Onglet 2 — Actions de référence (choix des actions)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.priorisation_data import (
    CATEGORIES,
    PriorisationContext,
    load_actions_choisies,
    save_priorisation_action,
    selections_from_db,
)
from utils.priorisation_text import (
    clean_rich_text,
    origine_label,
    parse_ids,
    short_description,
)

# ==========================
# Constantes
# ==========================

# Faisabilité 2 = À discuter, 3 = Prioritaire
FAISABILITE_ELIGIBLE = {2, 3}

ACTIONS_PAR_SECTION = 6
ACTIONS_PAR_LIGNE = 2
CIBLES_PAGE_SIZE = 3
DESCRIPTION_MAX_LEN = 180

LABEL_AJOUTER = "Ajouter à ma sélection"
LABEL_SELECTIONNEE = "Sélectionnée"

SECTION_ACTIONS = "actions"
SECTION_REFERENCE = "reference"
SECTION_COLLECTIVITES = "collectivites"

ORIGINE_REFERENCE = "Référence"

SESSION_SELECTIONS = "action_selections_v2"
SESSION_COLLECTIVITE = "action_collectivite_id_v2"
SESSION_EXPANDED_CIBLES = "action_expanded_cibles"
SESSION_VISIBLE_CIBLES_COUNT = "action_visible_cibles_count"
SESSION_FLASH = "action_flash"


# ==========================
# Sélection des cibles prioritaires
# ==========================


def calc_enjeu(
    levier: str,
    cat: int,
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
) -> float:
    """Enjeu d'une cible = abs(réduction levier) × poids catégorie."""
    poids = weights.get(levier, {}).get(cat, 0.0)
    if poids <= 0 or levier not in reductions:
        return 0.0
    return abs(float(reductions[levier])) * poids


def is_cible_prioritaire(
    levier: str,
    cat: int,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
    faisabilites: dict[tuple[str, int], int],
) -> bool:
    """
    Cible éligible au choix d'actions si :
    (a) dans le périmètre (absente de priorisation_hors_competence),
    (b) peu mobilisée (note 0 ou 1),
    (c) faisabilité « À discuter » (2) ou « Prioritaire » (3).
    """
    if (levier, cat) in exclusions:
        return False
    poids = weights.get(levier, {}).get(cat, 0.0)
    if poids <= 0:
        return False
    if notes.get((levier, cat), 0) not in (0, 1):
        return False
    return faisabilites.get((levier, cat)) in FAISABILITE_ELIGIBLE


def build_cibles_prioritaires(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
    faisabilites: dict[tuple[str, int], int],
) -> list[dict]:
    """Liste des cibles prioritaires triées par enjeu décroissant."""
    cibles: list[dict] = []
    for levier in leviers:
        if levier not in reductions:
            continue
        for cat in range(1, 7):
            if not is_cible_prioritaire(
                levier, cat, notes, exclusions, weights, faisabilites
            ):
                continue
            cibles.append(
                {
                    "levier": levier,
                    "categorie_id": cat,
                    "categorie": CATEGORIES[cat],
                    "enjeu": calc_enjeu(levier, cat, reductions, weights),
                }
            )
    cibles.sort(key=lambda c: c["enjeu"], reverse=True)
    return cibles


def fiches_reference_pour_cible(
    levier: str,
    cat: int,
    df_actions_reference: pd.DataFrame,
) -> pd.DataFrame:
    """Actions de référence disponibles pour une cible (levier × catégorie)."""
    empty = pd.DataFrame(
        columns=["id", "intitule", "description", "origine", "reference"]
    )
    if df_actions_reference.empty:
        return empty

    df = df_actions_reference[
        (df_actions_reference["levier"] == levier)
        & (df_actions_reference["categorie"] == cat)
    ]
    if df.empty:
        return empty

    rows = [
        {
            "id": int(row["id"]),
            "intitule": clean_rich_text(row["titre"]) or f"Action #{int(row['id'])}",
            "description": row["description"],
            "origine": ORIGINE_REFERENCE,
            "reference": True,
        }
        for _, row in df.iterrows()
    ]
    return pd.DataFrame(rows).sort_values("intitule")


def fiches_autres_collectivites(
    levier: str,
    cat: int,
    collectivite_id: int,
    df_priorisation_all: pd.DataFrame,
    df_fiches_action: pd.DataFrame,
    nom_par_id: dict[int, str],
) -> pd.DataFrame:
    """
    Fiches disponibles pour une cible : ids des autres collectivités dans
    priorisation (OLAP), résolues via fiche_action (prod).
    """
    rows: list[dict] = []
    df_autres = df_priorisation_all[
        (df_priorisation_all["levier"] == levier)
        & (df_priorisation_all["categorie"] == cat)
        & (df_priorisation_all["collectivite_id"] != collectivite_id)
    ]
    seen: set[tuple[int, int]] = set()

    for _, row in df_autres.iterrows():
        ct_id = int(row["collectivite_id"])
        ct_nom = nom_par_id.get(ct_id, f"Collectivité #{ct_id}")
        for aid in parse_ids(row["ids"]):
            dedupe = (ct_id, aid)
            if dedupe in seen:
                continue
            seen.add(dedupe)

            df_f = df_fiches_action[
                (df_fiches_action["id"] == aid)
                & (df_fiches_action["collectivite_id"] == ct_id)
            ]
            if df_f.empty:
                continue

            fiche = df_f.iloc[0]
            rows.append(
                {
                    "id": aid,
                    "intitule": fiche.get("titre") or f"Fiche #{aid}",
                    "description": fiche.get("description"),
                    "origine": ct_nom,
                    "reference": False,
                }
            )

    if not rows:
        return pd.DataFrame(
            columns=["id", "intitule", "description", "origine", "reference"]
        )

    return pd.DataFrame(rows).sort_values(
        ["origine", "intitule"], ascending=[True, True]
    )


def fiches_pour_cible(
    levier: str,
    cat: int,
    collectivite_id: int,
    df_priorisation_all: pd.DataFrame,
    df_fiches_action: pd.DataFrame,
    df_actions_reference: pd.DataFrame,
    nom_par_id: dict[int, str],
) -> pd.DataFrame:
    """Actions de référence puis actions des autres collectivités."""
    df_ref = fiches_reference_pour_cible(levier, cat, df_actions_reference)
    df_autres = fiches_autres_collectivites(
        levier,
        cat,
        collectivite_id,
        df_priorisation_all,
        df_fiches_action,
        nom_par_id,
    )
    return pd.concat([df_ref, df_autres], ignore_index=True)


# ==========================
# État de sélection
# ==========================


def selections() -> dict[tuple[str, int], set[tuple[int, bool]]]:
    """Sélections par cible ; une action = (fiche_action_id, action de référence)."""
    return st.session_state.setdefault(SESSION_SELECTIONS, {})


def is_fiche_selected(levier: str, cat: int, fiche_id: int, reference: bool) -> bool:
    return (fiche_id, reference) in selections().get((levier, cat), set())


def toggle_fiche_selection(
    levier: str, cat: int, fiche_id: int, reference: bool
) -> None:
    current = selections()
    ids = current.setdefault((levier, cat), set())
    fiche = (fiche_id, reference)
    if fiche in ids:
        ids.discard(fiche)
    else:
        ids.add(fiche)
    if not ids:
        current.pop((levier, cat), None)


def nb_selections_cible(levier: str, cat: int) -> int:
    return len(selections().get((levier, cat), set()))


def selections_to_rows() -> list[tuple[str, int, int, bool]]:
    return saved_to_rows(selections())


def saved_to_rows(
    saved: dict[tuple[str, int], set[tuple[int, bool]]],
) -> list[tuple[str, int, int, bool]]:
    rows = [
        (levier, cat, fiche_id, reference)
        for (levier, cat), ids in saved.items()
        for fiche_id, reference in ids
    ]
    return sorted(rows, key=lambda x: (x[0], x[1], x[2], x[3]))


def is_section_expanded(levier: str, cat: int, section: str) -> bool:
    expanded: set[tuple[str, int, str]] = st.session_state.get(
        SESSION_EXPANDED_CIBLES, set()
    )
    return (levier, cat, section) in expanded


def toggle_section_expanded(levier: str, cat: int, section: str) -> None:
    expanded = st.session_state.setdefault(SESSION_EXPANDED_CIBLES, set())
    key = (levier, cat, section)
    if key in expanded:
        expanded.discard(key)
    else:
        expanded.add(key)


def show_more_cibles(total: int) -> None:
    current = st.session_state.get(SESSION_VISIBLE_CIBLES_COUNT, CIBLES_PAGE_SIZE)
    st.session_state[SESSION_VISIBLE_CIBLES_COUNT] = min(
        current + CIBLES_PAGE_SIZE, total
    )


def init_session_selections(
    collectivite_id: int,
    saved: dict[tuple[str, int], set[tuple[int, bool]]],
    *,
    reset_pagination: bool = True,
) -> None:
    if (
        st.session_state.get(SESSION_COLLECTIVITE) == collectivite_id
        and SESSION_SELECTIONS in st.session_state
    ):
        return
    st.session_state[SESSION_SELECTIONS] = {
        key: set(ids) for key, ids in saved.items()
    }
    st.session_state[SESSION_COLLECTIVITE] = collectivite_id
    if reset_pagination:
        st.session_state[SESSION_EXPANDED_CIBLES] = set()
        st.session_state[SESSION_VISIBLE_CIBLES_COUNT] = CIBLES_PAGE_SIZE


def message_sauvegarde(nom_collectivite: str, n: int) -> str:
    if n == 0:
        return (
            f"Choix enregistrés pour **{nom_collectivite}** "
            "(aucune action sélectionnée)."
        )
    return (
        f"Choix enregistrés pour **{nom_collectivite}** "
        f"({n} action{'s' if n > 1 else ''})."
    )


# ==========================
# Rendu
# ==========================


def render_action_card(fiche: pd.Series, levier: str, cat: int) -> None:
    """Card d'une action : origine, titre, description et bouton de sélection."""
    fid = int(fiche["id"])
    reference = bool(fiche["reference"])
    section = SECTION_REFERENCE if reference else SECTION_COLLECTIVITES
    selected = is_fiche_selected(levier, cat, fid, reference)

    titre = fiche.get("intitule") or f"Action #{fid}"
    description = clean_rich_text(fiche.get("description"))

    with st.container(border=True):
        col_origine, col_etat = st.columns([3, 2], vertical_alignment="center")
        with col_origine:
            if reference:
                st.badge(
                    "Action de référence",
                    icon=":material/cards_star:",
                    color="orange",
                )
            else:
                st.badge(
                    origine_label(fiche.get("origine")),
                    icon=":material/location_city:",
                    color="blue",
                )
        with col_etat:
            if selected:
                st.badge(
                    "Sélectionnée", icon=":material/check_circle:", color="green"
                )

        st.markdown(f"**{titre}**")

        st.caption(
            short_description(description, DESCRIPTION_MAX_LEN)
            if description
            else "Aucune description disponible."
        )

        st.button(
            LABEL_SELECTIONNEE if selected else LABEL_AJOUTER,
            key=f"card_{section}_{levier}_{cat}_{fid}",
            type="primary" if selected else "secondary",
            icon=":material/check:" if selected else ":material/add:",
            width="stretch",
            on_click=toggle_fiche_selection,
            args=(levier, cat, fid, reference),
            help="Cliquez à nouveau pour retirer l'action de votre sélection."
            if selected
            else None,
        )


def render_grille_actions(df: pd.DataFrame, levier: str, cat: int) -> None:
    """Grille d'actions sur deux colonnes, paginée."""
    if df.empty:
        return

    expanded = is_section_expanded(levier, cat, SECTION_ACTIONS)
    visible = df if expanded else df.head(ACTIONS_PAR_SECTION)

    fiches = [fiche for _, fiche in visible.iterrows()]
    for start in range(0, len(fiches), ACTIONS_PAR_LIGNE):
        cols = st.columns(ACTIONS_PAR_LIGNE, gap="medium")
        for col, fiche in zip(cols, fiches[start : start + ACTIONS_PAR_LIGNE]):
            with col:
                render_action_card(fiche, levier, cat)

    reste = len(df) - len(visible)
    if reste > 0:
        st.button(
            f"Afficher {reste} action{'s' if reste > 1 else ''} de plus",
            key=f"more_{SECTION_ACTIONS}_{levier}_{cat}",
            icon=":material/expand_more:",
            width="stretch",
            on_click=toggle_section_expanded,
            args=(levier, cat, SECTION_ACTIONS),
        )
    elif expanded:
        st.button(
            "Afficher moins",
            key=f"less_{SECTION_ACTIONS}_{levier}_{cat}",
            icon=":material/expand_less:",
            width="stretch",
            on_click=toggle_section_expanded,
            args=(levier, cat, SECTION_ACTIONS),
        )


def render(ctx: PriorisationContext) -> None:
    st.warning(
        """
**Les actions à explorer pour vos volets prioritaires.**

Pour chaque volet que vous avez jugé pertinent ou à discuter avec vos élus, vous retrouverez :
- **Actions de référence** : actions recommandées par l'Ademe
- **Actions des autres collectivités** : actions menées par d'autres collectivités

Cliquez sur **"Ajouter à ma sélection"** pour constituer votre ensemble d'actions. Elles vous serviront de ressources pour vos prochaines planifications et vos discussions avec vos élus, vos comités, etc.

Une fois votre sélection terminée, cliquez sur **"Sauvegarder"** en bas de page pour la valider. Vous retrouverez ensuite vos actions sur votre tableau de bord de synthèse.
""",
        icon=":material/tips_and_updates:",
    )

    saved_df = load_actions_choisies(ctx.collectivite_id)
    saved = selections_from_db(saved_df)
    init_session_selections(ctx.collectivite_id, saved)

    cibles = build_cibles_prioritaires(
        ctx.leviers_reduction,
        ctx.reductions,
        ctx.notes,
        ctx.exclusions,
        ctx.weights,
        ctx.faisabilites,
    )

    if not cibles:
        st.info(
            "Aucun levier prioritaire pour cette collectivité. Vérifiez le diagnostic, "
            "le périmètre et l'arbitrage politique (faisabilité « À discuter » ou "
            "« Prioritaire » sur des leviers peu mobilisés).",
            icon=":material/filter_alt_off:",
        )
        st.caption(
            "Revenez à l'onglet **Priorisation des actions** pour arbitrer "
            "la pertinence des volets, ou passez à l'onglet **Tableau de bord**."
        )
        return

    n_visible_cibles = st.session_state.get(
        SESSION_VISIBLE_CIBLES_COUNT, CIBLES_PAGE_SIZE
    )
    visible_cibles = cibles[:n_visible_cibles]

    st.info(
        "Les volets ont été classés par potentiel de réduction CO₂ "
        "(d'après la SNBC).",
        icon=":material/sort:",
    )

    for rank, cible in enumerate(visible_cibles, start=1):
        levier = cible["levier"]
        cat = cible["categorie_id"]
        cat_label = cible["categorie"]
        enjeu = cible["enjeu"]

        st.divider()
        st.subheader(f"{rank}. {levier} — {cat_label}")
        st.caption(f"Potentiel du volet : **{enjeu:.0f}** ktCO₂e")

        nb_cible = nb_selections_cible(levier, cat)
        if nb_cible:
            st.caption(
                f"**{nb_cible}** action{'s' if nb_cible > 1 else ''} "
                f"sélectionnée{'s' if nb_cible > 1 else ''}"
            )

        df_actions = fiches_pour_cible(
            levier,
            cat,
            ctx.collectivite_id,
            ctx.df_priorisation_all,
            ctx.df_fiches_action,
            ctx.df_actions_reference,
            ctx.nom_par_id,
        )

        if df_actions.empty:
            st.info(
                "Aucune action disponible pour ce volet.",
                icon=":material/search_off:",
            )
            continue

        render_grille_actions(df_actions, levier, cat)

    if len(cibles) > n_visible_cibles:
        restants = len(cibles) - n_visible_cibles
        st.button(
            f"Afficher plus de volets ({restants} restant{'s' if restants > 1 else ''})",
            key="action_show_more_cibles",
            icon=":material/expand_more:",
            width="stretch",
            on_click=show_more_cibles,
            args=(len(cibles),),
        )

    st.divider()

    to_save = selections_to_rows()
    modifie = to_save != saved_to_rows(saved)

    col_resume, col_save = st.columns([3, 1], vertical_alignment="center")
    with col_resume:
        if modifie:
            st.warning(
                "Modifications non enregistrées.", icon=":material/pending_actions:"
            )
        else:
            st.caption("Votre sélection est à jour.")
    with col_save:
        sauvegarder = st.button(
            "Sauvegarder",
            type="primary",
            icon=":material/save:",
            width="stretch",
            key="action_save",
        )

    if sauvegarder:
        try:
            save_priorisation_action(ctx.collectivite_id, to_save)
            load_actions_choisies.clear()
            st.session_state.pop(SESSION_COLLECTIVITE, None)
            init_session_selections(
                ctx.collectivite_id,
                selections_from_db(load_actions_choisies(ctx.collectivite_id)),
                reset_pagination=False,
            )
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
        "Passez à l'onglet **Tableau de bord** pour retrouver vos actions sauvegardées "
        "et la vue d'ensemble."
    )
