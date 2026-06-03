"""Navigation entre les étapes du parcours Priorisation (1 → 4)."""

import streamlit as st

PAGE_DIAGNOSTIC = "pages/30_priorisation.py"
PAGE_FAISABILITE = "pages/32_priorisation_faisabilite.py"
PAGE_ACTION = "pages/33_priorisation_action.py"
PAGE_SYNTHESE = "pages/34_priorisation_synthese.py"


def switch_priorisation_page(page_path: str, collectivite_id: int | None) -> None:
    if collectivite_id is not None:
        st.query_params.from_dict({"collectivite_id": str(collectivite_id)})
    st.switch_page(page_path)


def render_etape_1_suivant(collectivite_id: int, key: str = "nav_diag_suivant") -> None:
    if st.button("Définir des cibles à prioriser", type="primary", key=key):
        switch_priorisation_page(PAGE_FAISABILITE, collectivite_id)


def render_etape_2_nav(
    collectivite_id: int,
    back_key: str = "nav_fais_retour",
    forward_key: str = "nav_fais_suivant",
) -> None:
    col_retour, col_suivant = st.columns(2)
    with col_retour:
        if st.button("Retour", key=back_key):
            switch_priorisation_page(PAGE_DIAGNOSTIC, collectivite_id)
    with col_suivant:
        if st.button(
            "Explorer les actions de référence",
            type="primary",
            key=forward_key,
        ):
            switch_priorisation_page(PAGE_ACTION, collectivite_id)


def render_etape_3_nav(
    collectivite_id: int,
    back_key: str = "nav_action_retour",
    forward_key: str = "nav_action_suivant",
) -> None:
    col_retour, col_suivant = st.columns(2)
    with col_retour:
        if st.button("Retour", key=back_key):
            switch_priorisation_page(PAGE_FAISABILITE, collectivite_id)
    with col_suivant:
        if st.button("Voir la synthèse", type="primary", key=forward_key):
            switch_priorisation_page(PAGE_SYNTHESE, collectivite_id)


def render_etape_4_retour(
    collectivite_id: int,
    key: str = "nav_synth_retour",
) -> None:
    if st.button("Retour", key=key):
        switch_priorisation_page(PAGE_ACTION, collectivite_id)
