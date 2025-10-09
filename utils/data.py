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

def load_df_pap_statut_semaine() -> pd.DataFrame:
    # Dérivé de df_pap: première apparition par collectivite_id
    df = read_table("pap_statut_semaine")
    return df


def load_df_pap_notes() -> pd.DataFrame:
    # Colonnes: semaine (datetime), plan_id, collectivite_id, score, scores détaillés
    df = read_table("pap_note")
    return df

def load_df_pap_notes_summed() -> pd.DataFrame:

    df = read_table("pap_note")

    df_scores = (
        df.groupby('semaine')[[
            'score_pilotabilite', 'score_budget', 'score_indicateur',
            'score_objectif', 'score_avancement', 'score_referentiel'
        ]]
        .sum()
        .reset_index()
        .melt(
            id_vars='semaine',
            var_name='type_score',
            value_name='somme'
        )
    )

    d = {'score_pilotabilite' : 'Pilotabilité',
        'score_objectif' : 'Objectif',
        'score_indicateur' : 'Indicateur',
        'score_referentiel' : 'Référentiel',
        'score_budget' : 'Budget',
        'score_avancement' : 'Avancement'}

    df_scores['type_score'] = df_scores['type_score'].map(d)
    df_scores['semaine'] = pd.to_datetime(df_scores['semaine'])
    df_scores['somme'] = round(df_scores['somme'], 0).astype(int)

    return df_scores


def load_df_typologie_fiche() -> pd.DataFrame:
    df = read_table("evolution_typologie_fa")
    return df

def load_df_airtable_pipeline_semaine() -> pd.DataFrame:
    df = read_table("airtable_sync_semaine", columns=['semaine', 'pipeline'])
    return df
