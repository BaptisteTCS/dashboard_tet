import pandas as pd


# Remplacez ces loaders par vos vraies sources (SQL, CSV, API).
# Ils renvoient des DataFrame aux schémas attendus par les fonctions de plotting.


def load_df_pap() -> pd.DataFrame:
    # Colonnes attendues: passage_pap (datetime), nom_plan, plan, collectivite_id, nom, import
    return pd.DataFrame(columns=[
        'passage_pap', 'nom_plan', 'plan', 'collectivite_id', 'nom', 'import'
    ])


def load_df_ct() -> pd.DataFrame:
    # Dérivé de df_pap: première apparition par collectivite_id
    return pd.DataFrame(columns=[
        'collectivite_id', 'passage_pap', 'nom', 'import'
    ])


def load_df_pap_notes() -> pd.DataFrame:
    # Colonnes: semaine (datetime), plan_id, collectivite_id, score, scores détaillés
    return pd.DataFrame(columns=[
        'semaine', 'plan_id', 'collectivite_id', 'score',
        'score_pilotabilite', 'score_indicateur', 'score_objectif',
        'score_referentiel', 'score_avancement', 'score_budget',
        'nom_ct', 'nom', 'c_referentiel'
    ])


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


