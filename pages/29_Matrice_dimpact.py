import streamlit as st

st.set_page_config(
    page_title="Matrice d'impact",
    page_icon="🎯",
    layout="wide"
)

import pandas as pd
from utils.db import read_table

# ==========================
# Constantes
# ==========================

TOTAL_EPCI_FRANCE = 1189  # Total des EPCI en France (dénominateur fixe)


# ==========================
# Chargement des données
# ==========================

@st.cache_resource(ttl="2d")
def load_data():
    df_user_actifs_ct_mois = read_table('user_actifs_ct_mois')
    df_activite_semaine = read_table('activite_semaine')
    df_ct_actives = read_table('ct_actives')
    df_pap_52 = read_table('pap_statut_5_fiches_modifiees_52_semaines')
    df_fap_52 = read_table('nb_fap_52')
    return df_user_actifs_ct_mois, df_activite_semaine, df_ct_actives, df_pap_52, df_fap_52


df_user_actifs_ct_mois, df_activite_semaine, df_ct_actives, df_pap_52, df_fap_52 = load_data()

# Exclusion BE/conseillers/internes via intersection des emails avec activite_semaine
df_user_actifs_ct_mois = df_user_actifs_ct_mois[
    df_user_actifs_ct_mois.email.isin(df_activite_semaine.email.to_list())
].copy()

# Normalisation des dates (gestion tz aware + alignement sur début de mois)
df_user_actifs_ct_mois['mois'] = pd.to_datetime(df_user_actifs_ct_mois['mois'], errors='coerce')
if getattr(df_user_actifs_ct_mois['mois'].dt, 'tz', None) is not None:
    df_user_actifs_ct_mois['mois'] = df_user_actifs_ct_mois['mois'].dt.tz_localize(None)
df_user_actifs_ct_mois = df_user_actifs_ct_mois.dropna(subset=['mois', 'email']).copy()
df_user_actifs_ct_mois['mois'] = df_user_actifs_ct_mois['mois'].dt.to_period('M').dt.to_timestamp()


# ==========================
# Helpers
# ==========================

def _last_complete_month(today: pd.Timestamp | None = None) -> pd.Timestamp:
    """Retourne le 1er jour du dernier mois complet (mois précédent le mois en cours)."""
    if today is None:
        today = pd.Timestamp.now().normalize()
    current_month = today.to_period('M').to_timestamp()
    return (current_month - pd.DateOffset(months=1)).normalize()


MOIS_REF = _last_complete_month()
MOIS_REF_M12 = (MOIS_REF - pd.DateOffset(months=12)).normalize()


def _format_mois_fr(ts: pd.Timestamp) -> str:
    mois_fr = {
        1: "janvier", 2: "février", 3: "mars", 4: "avril",
        5: "mai", 6: "juin", 7: "juillet", 8: "août",
        9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
    }
    return f"{mois_fr.get(ts.month, ts.month)} {ts.year}"


def kpi_card(
    label: str,
    valeur_actuelle: float,
    valeur_precedente: float | None = None,
    fmt: str = "number",
    suffixe: str = "",
    delta_color: str = "normal",
    help_text: str | None = None,
):
    """Affiche un st.metric uniforme.

    Paramètres :
    - fmt : "number" (entier formaté) ou "percent" (en %, 1 décimale)
    - suffixe : suffixe à coller à la valeur (ex: " utilisateurs")
    """
    if fmt == "percent":
        val_str = f"{valeur_actuelle * 100:.1f}%"
        if valeur_precedente is not None:
            delta = (valeur_actuelle - valeur_precedente) * 100
            delta_str = f"{delta:+.1f} pts"
        else:
            delta_str = None
    else:
        val_str = f"{int(round(valeur_actuelle)):,}".replace(",", " ") + suffixe
        if valeur_precedente is not None:
            delta = valeur_actuelle - valeur_precedente
            delta_str = f"{int(round(delta)):+,}".replace(",", " ")
        else:
            delta_str = None

    st.metric(label, val_str, delta=delta_str, delta_color=delta_color, help=help_text)


# ==========================
# Pré-calculs partagés
# ==========================

# Set des collectivites EPCI (categorie == 'EPCI')
epci_ids = set(
    df_ct_actives.loc[df_ct_actives['categorie'] == 'EPCI', 'collectivite_id']
                  .dropna()
                  .unique()
                  .tolist()
)


def collectivites_actives_12m(mois_fin: pd.Timestamp) -> set:
    """Set des collectivite_id avec au moins une activité sur les 12 mois finissant à mois_fin (inclus)."""
    mois_debut = (mois_fin - pd.DateOffset(months=11)).normalize()
    mask = (df_user_actifs_ct_mois['mois'] >= mois_debut) & (df_user_actifs_ct_mois['mois'] <= mois_fin)
    return set(df_user_actifs_ct_mois.loc[mask, 'collectivite_id'].dropna().unique().tolist())


def epci_avec_pap_actif_52(mois_fin: pd.Timestamp) -> set:
    """Set des collectivite_id (EPCI) ayant au moins un PAP avec statut='actif' au mois_fin."""
    df = df_pap_52.copy()
    df['mois'] = pd.to_datetime(df['mois'], errors='coerce').dt.to_period('M').dt.to_timestamp()
    df = df[(df['mois'] == mois_fin) & (df['statut'] == 'actif')]
    return set(df['collectivite_id'].dropna().unique().tolist())


def retention_4_sur_12(mois_fin: pd.Timestamp) -> tuple[int, int]:
    """Retourne (nb_ct_retenues, nb_ct_actives) sur la fenêtre 12 mois finissant à mois_fin."""
    mois_debut = (mois_fin - pd.DateOffset(months=11)).normalize()
    df = df_user_actifs_ct_mois[
        (df_user_actifs_ct_mois['mois'] >= mois_debut)
        & (df_user_actifs_ct_mois['mois'] <= mois_fin)
    ]
    if df.empty:
        return 0, 0
    nb_mois_par_ct = df.groupby('collectivite_id')['mois'].nunique()
    nb_ct_actives = int(nb_mois_par_ct.shape[0])
    nb_ct_retenues = int((nb_mois_par_ct >= 4).sum())
    return nb_ct_retenues, nb_ct_actives


def utilisateurs_actifs_du_mois(mois: pd.Timestamp) -> int:
    """Nombre d'utilisateurs uniques actifs au mois donné."""
    df = df_user_actifs_ct_mois[df_user_actifs_ct_mois['mois'] == mois]
    return int(df['email'].nunique())


def utilisateurs_actifs_12m(mois_fin: pd.Timestamp) -> int:
    """Nombre d'utilisateurs uniques actifs sur les 12 mois finissant à mois_fin (inclus)."""
    mois_debut = (mois_fin - pd.DateOffset(months=11)).normalize()
    mask = (df_user_actifs_ct_mois['mois'] >= mois_debut) & (df_user_actifs_ct_mois['mois'] <= mois_fin)
    return int(df_user_actifs_ct_mois.loc[mask, 'email'].nunique())


def pap_actifs_52_du_mois(mois: pd.Timestamp) -> int:
    """Nombre de PAP actifs (statut='actif', définition 52 semaines) au mois donné."""
    df = df_pap_52.copy()
    df['mois'] = pd.to_datetime(df['mois'], errors='coerce').dt.to_period('M').dt.to_timestamp()
    df = df[(df['mois'] == mois) & (df['statut'] == 'actif')]
    return int(df['plan'].nunique())


def fap_actifs_52_semaines(mois: pd.Timestamp) -> int:
    """Nombre de FAP actives (fiches d'action pilotables, statut='actif', définition 52 semaines) au mois donné."""
    df = df_fap_52.copy()
    df['mois'] = pd.to_datetime(df['mois'], errors='coerce').dt.to_period('M').dt.to_timestamp()
    df = df[(df['mois'] == mois) & (df['statut'] == 'actif')]
    return int(df['fiche_id'].iloc[0])


# ==========================
# Interface
# ==========================

st.title("🎯 Matrice d'impact")
st.caption(f"Toutes les statistiques présentées sont pour {_format_mois_fr(MOIS_REF)} et sont comparées à celle de {_format_mois_fr(MOIS_REF_M12)}.")


# ==========================
# 1. UTILISABLE
# ==========================
st.markdown("---")
st.markdown("## 1. Utilisable")
st.info("En attente du survey Posthog.")


# ==========================
# 2. UTILISÉ
# ==========================
st.markdown("---")
st.markdown("## 2. Utilisé")

col1, col2, col3, col4 = st.columns(4)

# --- Utilisateurs actifs ---
with col1:
    st.badge("Activité", icon=":material/person_check:", color="orange")
    nb_users_actuel = utilisateurs_actifs_du_mois(MOIS_REF)
    nb_users_precedent = utilisateurs_actifs_du_mois(MOIS_REF_M12)
    kpi_card(
        label=f"Utilisateurs actifs",
        valeur_actuelle=nb_users_actuel,
        valeur_precedente=nb_users_precedent,
        fmt="number",
        help_text=f"Nombre d'utilisateurs actifs au cours de {_format_mois_fr(MOIS_REF)}. Tout utilisateurs confondu : agents, conseillers, bureaux d'études, etc.",
    )

# --- Taux de pénétration ---
with col2:
    st.badge("Taux de pénétration", icon=":material/trending_up:", color="orange")
    epci_actifs_12m = collectivites_actives_12m(MOIS_REF) & epci_ids
    epci_actifs_12m_prev = collectivites_actives_12m(MOIS_REF_M12) & epci_ids

    taux_penetration_actuel = len(epci_actifs_12m) / TOTAL_EPCI_FRANCE if TOTAL_EPCI_FRANCE else 0
    taux_penetration_prev = len(epci_actifs_12m_prev) / TOTAL_EPCI_FRANCE if TOTAL_EPCI_FRANCE else 0

    kpi_card(
        label=f"Activation des EPCI",
        valeur_actuelle=taux_penetration_actuel,
        valeur_precedente=taux_penetration_prev,
        fmt="percent",
        help_text=f"% d'EPCI avec au moins un utilisateur actif sur les 12 derniers mois.",
    )

# --- Utilisations complètes ---
with col3:
    st.badge("Utilisations complètes", icon=":material/check_circle:", color="orange")
    epci_pap_actuel = epci_avec_pap_actif_52(MOIS_REF) & epci_ids
    epci_pap_prev = epci_avec_pap_actif_52(MOIS_REF_M12) & epci_ids

    set_a_actuel = epci_actifs_12m & epci_pap_actuel
    set_a_prev = epci_actifs_12m_prev & epci_pap_prev

    taux_complet_actuel = len(set_a_actuel) / TOTAL_EPCI_FRANCE if TOTAL_EPCI_FRANCE else 0
    taux_complet_prev = len(set_a_prev) / TOTAL_EPCI_FRANCE if TOTAL_EPCI_FRANCE else 0

    kpi_card(
        label=f"EPCI en pilotage",
        valeur_actuelle=taux_complet_actuel,
        valeur_precedente=taux_complet_prev,
        fmt="percent",
        help_text=f"% d'EPCI avec au moins un plan d'action pilotable actif au cours de {_format_mois_fr(MOIS_REF)}. Un plan d'action pilotable actif est un plan dont 5 fiches, avec au moins un titre, une personne pilote et un statut, ont modifiées sur les 12 derniers mois.",
    )

# --- Taux de rétention ---
with col4:
    st.badge("Taux de rétention", icon=":material/radio_button_checked:", color="orange")
    nb_ret_actuel, nb_act_actuel = retention_4_sur_12(MOIS_REF)
    nb_ret_prev, nb_act_prev = retention_4_sur_12(MOIS_REF_M12)

    taux_retention_actuel = (nb_ret_actuel / nb_act_actuel) if nb_act_actuel else 0
    taux_retention_prev = (nb_ret_prev / nb_act_prev) if nb_act_prev else 0

    kpi_card(
        label=f"Rétention des collectivités",
        valeur_actuelle=taux_retention_actuel,
        valeur_precedente=taux_retention_prev,
        fmt="percent",
        help_text=f"% des collectivités s'étant connectées au moins 1 fois sur 4 mois différents au cours des 12 derniers mois. Métrique choisie pour rendre compte de la temporalité de l'usage de la plateforme par les agents des collectivités (suivi trimestriel).",
    )


# ==========================
# 3. UTILE
# ==========================
st.markdown("---")

col_utile, col_impactant = st.columns(2)
with col_utile:
    st.markdown("## 3. Utile")

    st.badge("Pilotage des actions de la transition écologique", icon=":material/add_notes:", color="blue")

    nb_fap_actifs_actuel = fap_actifs_52_semaines(MOIS_REF)
    nb_fap_actifs_prev = fap_actifs_52_semaines(MOIS_REF_M12)

    col_fap, _, _ = st.columns(3)
    with col_fap:
        kpi_card(
            label=f"Fiches actions pilotables actives",
            valeur_actuelle=nb_fap_actifs_actuel,
            valeur_precedente=nb_fap_actifs_prev,
            fmt="number",
            help_text=f"Nombre de fiches actions pilotables actives en {_format_mois_fr(MOIS_REF)}. Une fiche action pilotable active est une fiche, avec au moins un titre, une personne pilote et un statut, qui a été modifiée sur les 12 derniers mois.",
        )


# ==========================
# 4. IMPACTANT
# ==========================
with col_impactant:
    st.markdown("## 4. Impactant")

    st.badge("Pilotage de la transition écologique", icon=":material/globe_book:", color="blue")

    nb_pap_actifs_actuel = pap_actifs_52_du_mois(MOIS_REF)
    nb_pap_actifs_prev = pap_actifs_52_du_mois(MOIS_REF_M12)

    col_pap, _, _ = st.columns(3)
    with col_pap:
        kpi_card(
            label=f"Plans d'action pilotables actifs",
            valeur_actuelle=nb_pap_actifs_actuel,
            valeur_precedente=nb_pap_actifs_prev,
            fmt="number",
            help_text=f"Nombre de plans d'action pilotables actifs en {_format_mois_fr(MOIS_REF)}. Un plan d'action pilotable actif est un plan dont 5 fiches, avec au moins un titre, une personne pilote et un statut, ont modifiées sur les 12 derniers mois.",
        )


# ==========================
# 5. EFFICIENT
# ==========================
st.markdown("---")
st.markdown("## 5. Efficient")

BUDGET_ANNUEL = 1_600_000  # Budget annuel brut alloué à la plateforme (€)

mois_debut_12m = (MOIS_REF - pd.DateOffset(months=11)).normalize()
mois_debut_12m_prev = (MOIS_REF_M12 - pd.DateOffset(months=11)).normalize()

nb_users_12m_actuel = utilisateurs_actifs_12m(MOIS_REF)
nb_users_12m_prev = utilisateurs_actifs_12m(MOIS_REF_M12)

nb_ct_12m_actuel = len(collectivites_actives_12m(MOIS_REF))
nb_ct_12m_prev = len(collectivites_actives_12m(MOIS_REF_M12))

col_b, col_u, col_c, col_a = st.columns(4)

# --- Budget annuel brut ---
with col_b:
    st.badge("Budget", icon=":material/account_balance:", color="violet")
    kpi_card(
        label="Budget annuel brut",
        valeur_actuelle=BUDGET_ANNUEL,
        fmt="number",
        suffixe=" €",
        help_text="Budget annuel brut alloué à la plateforme Territoires en Transitions.",
    )

# --- Coût par utilisateur actif (12 mois) ---
with col_u:
    st.badge("Coût d'usage", icon=":material/payments:", color="violet")
    cout_user_actuel = (BUDGET_ANNUEL / nb_users_12m_actuel) if nb_users_12m_actuel else 0
    cout_user_prev = (BUDGET_ANNUEL / nb_users_12m_prev) if nb_users_12m_prev else 0
    kpi_card(
        label="Coût par utilisateur actif",
        valeur_actuelle=cout_user_actuel,
        valeur_precedente=cout_user_prev,
        fmt="number",
        suffixe=" €",
        delta_color="inverse",
        help_text=(
            f"Budget annuel brut divisé par le nombre d'utilisateurs uniques actifs "
            f"sur les 12 derniers mois (de {_format_mois_fr(mois_debut_12m)} à {_format_mois_fr(MOIS_REF)}). "
            f"Comparé à la même fenêtre 12 mois finissant en {_format_mois_fr(MOIS_REF_M12)}."
        ),
    )

# --- Coût par collectivité active (12 mois) ---
with col_c:
    st.badge("Coût d'usage", icon=":material/payments:", color="violet")
    cout_ct_actuel = (BUDGET_ANNUEL / nb_ct_12m_actuel) if nb_ct_12m_actuel else 0
    cout_ct_prev = (BUDGET_ANNUEL / nb_ct_12m_prev) if nb_ct_12m_prev else 0
    kpi_card(
        label="Coût par collectivité active",
        valeur_actuelle=cout_ct_actuel,
        valeur_precedente=cout_ct_prev,
        fmt="number",
        suffixe=" €",
        delta_color="inverse",
        help_text=(
            f"Budget annuel brut divisé par le nombre de collectivités actives "
            f"sur les 12 derniers mois (de {_format_mois_fr(mois_debut_12m)} à {_format_mois_fr(MOIS_REF)}). "
            f"Comparé à la même fenêtre 12 mois finissant en {_format_mois_fr(MOIS_REF_M12)}."
        ),
    )

# --- Coût par fiche action pilotable active ---
with col_a:
    st.badge("Coût d'usage", icon=":material/payments:", color="violet")
    cout_fap_actuel = (BUDGET_ANNUEL / nb_fap_actifs_actuel) if nb_fap_actifs_actuel else 0
    cout_fap_prev = (BUDGET_ANNUEL / nb_fap_actifs_prev) if nb_fap_actifs_prev else 0
    kpi_card(
        label="Coût par action pilotable active",
        valeur_actuelle=cout_fap_actuel,
        valeur_precedente=cout_fap_prev,
        fmt="number",
        suffixe=" €",
        delta_color="inverse",
        help_text=(
            f"Budget annuel brut divisé par le nombre de fiches actions pilotables actives "
            f"en {_format_mois_fr(MOIS_REF)} (définition 52 semaines)."
        ),
    )
