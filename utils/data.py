import pandas as pd
from .db import read_table

def load_df_pap() -> pd.DataFrame:
    df = read_table("pap_date_passage")
    return df

def load_df_pap_statut_semaine() -> pd.DataFrame:
    df = read_table("pap_statut_semaine")
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

def load_df_pap_notes() -> pd.DataFrame:
    df_notes = read_table("pap_note", columns=['collectivite_id', 'plan_id', 'nom', 'nom_ct', 'score_pilotabilite', 'score_budget', 'score_indicateur', 'score_objectif', 'score_avancement', 'score_referentiel', 'c_referentiel', 'score', 'semaine'])
    df_ct = read_table("collectivite", columns=['collectivite_id', 'type_collectivite', 'nature_collectivite', 'region_name', 'departement_name', 'population_totale'])
    df = pd.merge(df_notes, df_ct, on='collectivite_id', how='left')
    return df

def load_df_collectivite() -> pd.DataFrame:
    df = read_table("collectivite", columns=['collectivite_id', 'type_collectivite', 'nature_collectivite', 'region_name', 'departement_name', 'population_totale'])
    return df

def load_df_calendly_events() -> pd.DataFrame:
    df = read_table("calendly_events")
    return df

def load_df_calendly_invitees() -> pd.DataFrame:
    df = read_table("calendly_invitees")
    return df

def load_df_bizdev_contact_collectivite() -> pd.DataFrame:
    df = read_table("bizdev_contact_collectivite")
    return df

def load_df_pap_statut_semaine_12_mois() -> pd.DataFrame:
    df = read_table("pap_statut_semaine_12_mois")
    return df

def load_df_contribution_semaine() -> pd.DataFrame:
    df = read_table("contribution_semaine")
    return df

def load_df_activite_semaine() -> pd.DataFrame:
    df = read_table("activite_semaine")
    return df

def load_df_fa_pilotable_12_mois_statut_semaine() -> pd.DataFrame:
    df = read_table("fa_pilotable_12_mois_statut_semaine")
    return df

def load_df_fa_pilotable() -> pd.DataFrame:
    df = read_table("fa_pilotable")
    return df

def load_df_fa_contribution_semaine() -> pd.DataFrame:
    df = read_table("fa_contribution_semaine")
    return df

def load_df_pap_note_max_by_collectivite() -> pd.DataFrame:
    """Charge les notes PAP (snapshot) par collectivité avec le nom de la collectivité.
    Utilise pap_note_snapshot qui contient une seule note par plan PAP (dernière semaine)."""
    from .db import get_engine
    import pandas as pd
    from sqlalchemy import text
    
    engine = get_engine()
    query = text("""
        SELECT 
            collectivite_id,
            nom_ct as nom_collectivite,
            nom as nom_plan,
            score as score_pap,
            semaine as derniere_semaine,
            plan_id
        FROM pap_note_snapshot
    """)
    
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    
    return df

def load_df_analyse_campagne_region() -> pd.DataFrame:
    """Charge les données d'analyse de la campagne région."""
    df = read_table("analyse_campagne_region")
    return df

def load_df_campagne_region_reached() -> pd.DataFrame:
    """Charge la liste des collectivités reached pour la campagne région."""
    df = read_table("regions_reached")
    return df