"""Collectivité sélectionnée, partagée entre les pages via st.session_state.

st.session_state est commun à toutes les pages d'une même session : une page
écrit la collectivité choisie avec `set_selected_collectivite`, les autres la
relisent avec `get_selected_collectivite` ou pré-sélectionnent leur selectbox
avec `default_collectivite_index`.

Le paramètre d'URL ?collectivite_id= reste prioritaire au premier chargement,
pour garder les liens partageables.
"""

import streamlit as st

SESSION_SELECTED_COLLECTIVITE = "collectivite_selectionnee"


def _to_int(value) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def set_selected_collectivite(collectivite_id: int | None) -> None:
    """Mémorise la collectivité pour les autres pages de la session."""
    cid = _to_int(collectivite_id)
    if cid is not None:
        st.session_state[SESSION_SELECTED_COLLECTIVITE] = cid


def get_selected_collectivite() -> int | None:
    """Collectivité mémorisée, à défaut celle du paramètre d'URL, sinon None."""
    cid = _to_int(st.session_state.get(SESSION_SELECTED_COLLECTIVITE))
    if cid is not None:
        return cid
    return _to_int(st.query_params.get("collectivite_id"))


def default_collectivite_index(collectivite_ids: list[int]) -> int:
    """Index de pré-sélection dans un selectbox, 0 si la collectivité est absente."""
    cid = get_selected_collectivite()
    if cid is not None and cid in collectivite_ids:
        return collectivite_ids.index(cid)
    return 0
