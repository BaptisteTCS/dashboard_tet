"""Programme TETE : simulation de règles de sortie des collectivités engagées.

Engagée = a un COT ou une labellisation (base prod).
Deux règles de sortie réglables :
- toujours à la 1ère étoile, obtenue il y a plus de X ans (sans jamais être monté plus haut) ;
- aucune activité depuis plus de X ans (connexion des membres ou modification des mesures).
X = 0 désactive la règle. Les dates limites sont calculées à partir de la date du jour.
"""

import pandas as pd
import streamlit as st
from sqlalchemy import text

from utils.db import get_engine_prod

SQL_CT = """
with engagees as (
    select collectivite_id from cot
    union
    select collectivite_id from labellisation
),
membres as (
    -- Membres actifs hors conseillers et partenaires (fonction vide incluse)
    select pud.collectivite_id, max(u.last_sign_in_at) as derniere_connexion
    from private_utilisateur_droit pud
    join auth.users u on u.id = pud.user_id
    left join private_collectivite_membre pcm
        on pcm.user_id = pud.user_id and pcm.collectivite_id = pud.collectivite_id
    where pud.active
      and (pcm.fonction is null or pcm.fonction not in ('conseiller', 'partenaire'))
    group by 1
),
modifs as (
    select collectivite_id, max(modified_at) as derniere_modif
    from (
        select collectivite_id, modified_at from action_statut
        union all
        select collectivite_id, modified_at from action_commentaire
    ) m
    group by 1
)
select e.collectivite_id,
       c.nom,
       (cot.collectivite_id is not null) as cot,
       m.derniere_connexion,
       mo.derniere_modif
from engagees e
left join collectivite c on c.id = e.collectivite_id
left join cot on cot.collectivite_id = e.collectivite_id
left join membres m on m.collectivite_id = e.collectivite_id
left join modifs mo on mo.collectivite_id = e.collectivite_id
"""

SQL_LABELS = """
with dernier as (
    select distinct on (collectivite_id, referentiel)
           collectivite_id, referentiel::text as referentiel, etoiles
    from labellisation
    order by collectivite_id, referentiel, obtenue_le desc, id desc
)
select d.collectivite_id, d.referentiel, d.etoiles as etoiles_actuelles,
       a.max_etoiles, a.premiere_etoile_le
from dernier d
join (
    select collectivite_id, referentiel::text as referentiel,
           max(etoiles) as max_etoiles,
           min(obtenue_le) filter (where etoiles = 1) as premiere_etoile_le
    from labellisation
    group by 1, 2
) a using (collectivite_id, referentiel)
"""

DEF_CONNEXION = "Connexion d'un membre (hors conseillers et partenaires)"
DEF_MODIF = "Modification sur les mesures"


@st.cache_data(ttl=3600, show_spinner="Chargement des données prod…")
def charger_donnees():
    with get_engine_prod().connect() as conn:
        ct = pd.read_sql(text(SQL_CT), conn)
        labels = pd.read_sql(text(SQL_LABELS), conn)
    for col in ["derniere_connexion", "derniere_modif"]:
        ct[col] = pd.to_datetime(ct[col], utc=True)
    labels["premiere_etoile_le"] = pd.to_datetime(labels["premiere_etoile_le"])
    return ct, labels


def date_limite(ans):
    """Date du jour moins `ans` années."""
    return pd.Timestamp.now(tz="UTC").normalize() - pd.DateOffset(years=ans)


def libelle_curseur(ans):
    if ans == 0:
        return "Désactivé"
    return f"{ans} an{'s' if ans > 1 else ''} (avant le {date_limite(ans):%d/%m/%Y})"


def simuler(ct, labels, *, ans_etoile, ans_inactif, definition):
    df = ct.copy()

    # Règle 1 : labellisations bloquées à la 1ère étoile avant la date limite.
    # La collectivité sort si toutes ses labellisations sont bloquées (COT ou non).
    if ans_etoile:
        seuil = date_limite(ans_etoile).tz_localize(None)
        lab = labels.assign(
            bloquee=(labels["etoiles_actuelles"] == 1)
            & (labels["max_etoiles"] == 1)
            & (labels["premiere_etoile_le"] < seuil)
        )
        toutes_bloquees = lab.groupby("collectivite_id")["bloquee"].all()
        ids = toutes_bloquees[toutes_bloquees].index
        df["perdue_etoile"] = df["collectivite_id"].isin(ids)
    else:
        df["perdue_etoile"] = False

    # Règle 2 : aucune activité depuis la date limite (date vide = inactive)
    if ans_inactif:
        seuil = date_limite(ans_inactif)
        col = "derniere_connexion" if definition == DEF_CONNEXION else "derniere_modif"
        df["perdue_inactif"] = df[col].isna() | (df[col] < seuil)
    else:
        df["perdue_inactif"] = False

    df["perdue"] = df["perdue_etoile"] | df["perdue_inactif"]
    return df


st.title("🎓 Programme TETE")
st.caption("Source : base prod. Collectivité engagée = a un COT ou une labellisation.")

ct, labels = charger_donnees()
nb_engagees = len(ct)
nb_cot = int(ct["cot"].sum())

zone_metrics = st.container()

st.divider()
r1, r2 = st.columns(2, gap="large")
with r1:
    ans_etoile = st.select_slider(
        "Toujours à la 1ère étoile, obtenue il y a plus de",
        options=list(range(7)),
        value=0,
        format_func=libelle_curseur,
    )
with r2:
    ans_inactif = st.select_slider(
        "Aucune activité depuis plus de",
        options=list(range(7)),
        value=0,
        format_func=libelle_curseur,
    )
    definition = st.radio(
        "Activité mesurée par",
        [DEF_CONNEXION, DEF_MODIF],
        horizontal=True,
    )

res = simuler(ct, labels, ans_etoile=ans_etoile, ans_inactif=ans_inactif, definition=definition)
nb_perdues = int(res["perdue"].sum())
nb_cot_restants = int((res["cot"] & ~res["perdue"]).sum())

with zone_metrics:
    m1, m2, m3 = st.columns(3)
    m1.metric("Collectivités engagées", nb_engagees - nb_perdues, delta=-nb_perdues or None)
    m2.metric("Collectivités COT", nb_cot_restants, delta=(nb_cot_restants - nb_cot) or None)
    m3.metric("Collectivités perdues", nb_perdues)

perdues = res[res["perdue"]].copy()
if not perdues.empty:
    perdues["raison"] = perdues.apply(
        lambda r: " + ".join(
            n for n, ok in [("1ère étoile", r["perdue_etoile"]), ("inactive", r["perdue_inactif"])] if ok
        ),
        axis=1,
    )
    affichage = perdues[
        ["collectivite_id", "nom", "cot", "raison", "derniere_connexion", "derniere_modif"]
    ].rename(
        columns={
            "collectivite_id": "ID",
            "nom": "Collectivité",
            "cot": "COT",
            "raison": "Raison",
            "derniere_connexion": "Dernière connexion",
            "derniere_modif": "Dernière modif mesures",
        }
    ).sort_values(["Raison", "Collectivité"])
    for col in ["Dernière connexion", "Dernière modif mesures"]:
        affichage[col] = affichage[col].dt.date
    with st.expander(f"Voir les {nb_perdues} collectivités perdues"):
        st.dataframe(affichage, hide_index=True, use_container_width=True)
        st.download_button(
            "Télécharger (CSV)",
            affichage.to_csv(index=False).encode("utf-8-sig"),
            file_name="programme_tete_perdues.csv",
            mime="text/csv",
        )
