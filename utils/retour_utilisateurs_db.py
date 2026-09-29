"""Accès OLAP pour la revue des retours utilisateurs.

La page Streamlit ne parle ni à Notion ni à OpenAI : tout est préparé chaque
nuit par datalore/pipeline_retours_utilisateurs.py, qui alimente
retours_utilisateurs_analyse, _backlog et _cycles. Seule la table
retours_utilisateurs_tickets est écrite ici, à la validation humaine.
"""

import pandas as pd
import streamlit as st
from sqlalchemy import text

from utils.db import get_engine

DDL_VALIDATIONS = """
CREATE TABLE IF NOT EXISTS retours_utilisateurs_tickets (
    feedback_id     TEXT PRIMARY KEY,
    ticket_id       TEXT,
    cycle_id        TEXT,
    feedback_titre  TEXT,
    ticket_titre    TEXT,
    choix_ia        BOOLEAN,
    score_ia        DOUBLE PRECISION,
    valide_at       TIMESTAMPTZ DEFAULT now(),
    notion_sync_at  TIMESTAMPTZ
)
"""

TABLES_PIPELINE = (
    "retours_utilisateurs_analyse",
    "retours_utilisateurs_backlog",
    "retours_utilisateurs_cycles",
)


@st.cache_resource(show_spinner=False)
def _table_validations():
    """La page est propriétaire de cette table ; les trois autres viennent du
    pipeline nocturne."""
    with get_engine().begin() as conn:
        conn.execute(text(DDL_VALIDATIONS))
    return True


def pipeline_pret():
    """False tant que le pipeline nocturne n'a jamais tourné."""
    with get_engine().connect() as conn:
        return all(
            conn.execute(
                text("SELECT to_regclass(:nom)"), {"nom": f"public.{nom}"}
            ).scalar()
            for nom in TABLES_PIPELINE
        )


@st.cache_data(ttl="10m", show_spinner=False)
def charger_cycles():
    """[(cycle_id, cycle_name)] triés par nom."""
    with get_engine().connect() as conn:
        rows = conn.execute(
            text("SELECT cycle_id, cycle_name FROM retours_utilisateurs_cycles")
        ).all()
    return sorted(((r[0], r[1]) for r in rows), key=lambda c: c[1] or "")


@st.cache_data(ttl="10m", show_spinner=False)
def charger_backlog():
    """Tous les couples (ticket, cycle) du backlog, pour la recherche manuelle."""
    with get_engine().connect() as conn:
        rows = conn.execute(
            text("""
                SELECT ticket_id, ticket_titre, cycle_id, cycle_name, statut
                FROM retours_utilisateurs_backlog
                ORDER BY cycle_name, ticket_titre
            """)
        ).mappings().all()
    return [dict(r) for r in rows]


def statistiques():
    """Compteurs d'avancement de la revue."""
    _table_validations()
    with get_engine().connect() as conn:
        return dict(conn.execute(text("""
            SELECT
                count(*) FILTER (WHERE a.sans_epic) AS sans_epic,
                count(*) FILTER (WHERE a.sans_epic AND a.analyse_at IS NULL) AS non_analyses,
                count(v.feedback_id) AS valides,
                count(*) FILTER (
                    WHERE a.sans_epic AND a.analyse_at IS NOT NULL
                      AND v.feedback_id IS NULL
                ) AS a_traiter,
                max(a.analyse_at) AS derniere_analyse
            FROM retours_utilisateurs_analyse a
            LEFT JOIN retours_utilisateurs_tickets v ON v.feedback_id = a.feedback_id
        """)).mappings().one())


def charger_lot(taille, recents_dabord=True):
    """Prochains retours à trancher : sans EPIC, analysés, pas encore validés."""
    _table_validations()
    ordre = "DESC" if recents_dabord else "ASC"
    with get_engine().connect() as conn:
        rows = conn.execute(
            text(f"""
                SELECT a.feedback_id, a.titre, a.citation, a.url, a.created_time,
                       a.cycle_id, a.cycle_name, a.tickets, a.erreur
                FROM retours_utilisateurs_analyse a
                LEFT JOIN retours_utilisateurs_tickets v
                       ON v.feedback_id = a.feedback_id
                WHERE a.sans_epic
                  AND a.analyse_at IS NOT NULL
                  AND v.feedback_id IS NULL
                ORDER BY a.created_time {ordre} NULLS LAST
                LIMIT :limite
            """),
            {"limite": taille},
        ).mappings().all()
    return [{**r, "tickets": r["tickets"] or []} for r in rows]


def charger_validations(limite=200):
    _table_validations()
    with get_engine().connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT valide_at, feedback_titre, ticket_titre, cycle_id, choix_ia
                FROM retours_utilisateurs_tickets
                ORDER BY valide_at DESC
                LIMIT :limite
            """),
            conn,
            params={"limite": limite},
        )


def sauvegarder_validations(rows):
    """Upsert des choix utilisateurs, tout le lot dans une transaction."""
    if not rows:
        return
    _table_validations()
    with get_engine().begin() as conn:
        conn.execute(
            text("""
                INSERT INTO retours_utilisateurs_tickets
                    (feedback_id, ticket_id, cycle_id, feedback_titre, ticket_titre,
                     choix_ia, score_ia, valide_at)
                VALUES
                    (:feedback_id, :ticket_id, :cycle_id, :feedback_titre,
                     :ticket_titre, :choix_ia, :score_ia, now())
                ON CONFLICT (feedback_id) DO UPDATE SET
                    ticket_id = EXCLUDED.ticket_id,
                    cycle_id = EXCLUDED.cycle_id,
                    feedback_titre = EXCLUDED.feedback_titre,
                    ticket_titre = EXCLUDED.ticket_titre,
                    choix_ia = EXCLUDED.choix_ia,
                    score_ia = EXCLUDED.score_ia,
                    valide_at = now(),
                    notion_sync_at = NULL
            """),
            rows,
        )
