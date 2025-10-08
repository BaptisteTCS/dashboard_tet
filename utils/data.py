import pandas as pd
from .db import read_table


# Remplacez ces loaders par vos vraies sources (SQL, CSV, API).
# Ils renvoient des DataFrame aux schémas attendus par les fonctions de plotting.


def load_df_pap() -> pd.DataFrame:
    """Charge la table des passages PAP depuis la base Postgres.

    La table source est "pap_date_passage" (schéma par défaut). Elle doit contenir
    au moins les colonnes utilisées par les graphiques: passage_pap, nom_plan,
    plan, collectivite_id, nom, import.
    """
    df = read_table("pap_date_passage")
    return df


def load_df_ct() -> pd.DataFrame:
    # Dérivé de df_pap: première apparition par collectivite_id
    return pd.DataFrame(columns=[
        'collectivite_id', 'passage_pap', 'nom', 'import'
    ])


def load_df_pap_notes() -> pd.DataFrame:
    # Colonnes: semaine (datetime), plan_id, collectivite_id, score, scores détaillés
    df = read_table("pap_note")
    return df


def load_df_plan_pilote() -> pd.DataFrame:
    # Colonnes: created_at (datetime), user_id, plan_id, collectivite_id, nom
    return pd.DataFrame(columns=['created_at', 'user_id', 'plan_id', 'collectivite_id', 'nom'])


def load_df_plan_referent() -> pd.DataFrame:
    # Colonnes: created_at (datetime), user_id, plan_id, collectivite_id, nom
    return pd.DataFrame(columns=['created_at', 'user_id', 'plan_id', 'collectivite_id', 'nom'])


def load_df_sharing() -> pd.DataFrame:
    # Colonnes: created_at (datetime), collectivite_id
    return pd.DataFrame(columns=['created_at', 'collectivite_id'])


def load_df_score_indicateur() -> pd.DataFrame:
    # Colonnes: collectivite_id, action_id
    return pd.DataFrame(columns=['collectivite_id', 'action_id'])


