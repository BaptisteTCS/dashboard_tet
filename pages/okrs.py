

# -- Retro data --

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def plot_monthly_fiches_agg(df, projection=True, agg="sum"):

    df = df.copy()
    df['created_at'] = pd.to_datetime(df['created_at'])

    df['year'] = df['created_at'].dt.year
    df['month'] = df['created_at'].dt.month

    # emails distinct par collectivite
    df_counts = (
        df.groupby(['year','month','collectivite_id'])['email']
        .nunique()
        .reset_index(name='nb_emails')
    )

    if agg == "mean":

        df_monthly = (
            df_counts.groupby(['year','month'])['nb_emails']
            .mean()
            .reset_index(name='nb_fiches')
        )

    elif agg == "intensity":

        emails = (
            df_counts.groupby(['year','month'])['nb_emails']
            .sum()
        )

        collectivites = (
            df_counts.groupby(['year','month'])['collectivite_id']
            .nunique()
        )

        df_monthly = (
            (emails / collectivites)
            .reset_index(name='nb_fiches')
        )

    else:

        df_monthly = (
            df_counts.groupby(['year','month'])['nb_emails']
            .sum()
            .reset_index(name='nb_fiches')
        )

    df_pivot = df_monthly.pivot(index='month', columns='year', values='nb_fiches')
    df_pivot = df_pivot.reindex(range(1, 13))

    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]

    color_2025 = "#4380f5"
    color_2026 = "#F0806A"

    plt.figure(figsize=(9,5))

    today = datetime.today()
    current_year = today.year
    current_month = today.month

    for year, color in [(2025, color_2025), (2026, color_2026)]:

        if year not in df_pivot.columns:
            continue

        y = df_pivot[year].copy()

        # si projection désactivée ou si ce n'est pas l'année courante
        if not projection or year != current_year:
            plt.plot(df_pivot.index, y,
                     marker="o", linewidth=2,
                     color=color, label=str(year))
            continue

        # mois complets uniquement
        if current_month > 1:
            plt.plot(df_pivot.index[:current_month-1],
                     y.iloc[:current_month-1],
                     marker="o",
                     linewidth=2,
                     color=color,
                     label=str(year))

        # projection mois courant
        if pd.notna(y.iloc[current_month-1]):

            projected = y.iloc[current_month-1] * 2

            plt.plot(
                [current_month-1, current_month],
                [y.iloc[current_month-2], projected],
                linestyle="--",
                marker="o",
                linewidth=2,
                color=color
            )

    plt.xticks(range(1,13), months)

    plt.grid(alpha=0.2)
    plt.legend(frameon=False)

    plt.tight_layout()
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def plot_monthly_fiches(df, projection=True):

    df = df.copy()
    df['created_at'] = pd.to_datetime(df['created_at'])

    df['year'] = df['created_at'].dt.year
    df['month'] = df['created_at'].dt.month

    df_monthly = (
        df.groupby(['year', 'month'])
        .size()
        .reset_index(name='nb_fiches')
    )

    df_pivot = df_monthly.pivot(index='month', columns='year', values='nb_fiches')
    df_pivot = df_pivot.reindex(range(1, 13))

    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]

    color_2025 = "#5FA8D3"
    color_2026 = "#F0806A"

    plt.figure(figsize=(9,5))

    today = datetime.today()
    current_year = today.year
    current_month = today.month

    for year, color in [(2025, color_2025), (2026, color_2026)]:

        if year not in df_pivot.columns:
            continue

        y = df_pivot[year].copy()

        # si projection désactivée ou si ce n'est pas l'année courante
        if not projection or year != current_year:
            plt.plot(df_pivot.index, y,
                     marker="o", linewidth=2,
                     color=color, label=str(year))
            continue

        # mois complets uniquement
        if current_month > 1:
            plt.plot(df_pivot.index[:current_month-1],
                     y.iloc[:current_month-1],
                     marker="o",
                     linewidth=2,
                     color=color,
                     label=str(year))

        # projection mois courant
        if pd.notna(y.iloc[current_month-1]):

            projected = y.iloc[current_month-1] * 2

            plt.plot(
                [current_month-1, current_month],
                [y.iloc[current_month-2], projected],
                linestyle="--",
                marker="o",
                linewidth=2,
                color=color
            )

    plt.xticks(range(1,13), months)

    plt.grid(alpha=0.2)
    plt.legend(frameon=False)

    plt.tight_layout()
    plt.show()

# SQL (postgresql) request
df_42 = None # TODO: execute the following query:
# select count(*), count(distinct collectivite_id) as nb_ct
# from fiche_action
# where created_at>'2025-01-01' and created_at <'2025-03-16'


# SQL (postgresql) request
df_43 = None # TODO: execute the following query:
# select count(*), count(distinct collectivite_id) as nb_ct
# from fiche_action
# where created_at>'2026-01-01'


# SQL (postgresql) request
df_fa = None # TODO: execute the following query:
# select id, created_at
# from fiche_action
# where created_at>'2025-01-01'


plot_monthly_fiches(df_fa)

# SQL (postgresql) request
df_44 = None # TODO: execute the following query:
# select count(*), count(distinct collectivite_id)
# from pap_date_passage
# where passage_pap>'2025-01-01' and passage_pap <'2025-03-16'


# SQL (postgresql) request
df_45 = None # TODO: execute the following query:
# select count(*), count(distinct collectivite_id)
# from pap_date_passage
# where passage_pap>'2026-01-01'


# SQL (postgresql) request
df_46 = None # TODO: execute the following query:
# select plan, passage_pap as created_at
# from pap_date_passage
# where passage_pap>'2025-01-01'


plot_monthly_fiches(df_46)

# SQL (postgresql) request
df_47 = None # TODO: execute the following query:
# with ct_pap as (select collectivite_id, min(passage_pap) as passage_pap
# from pap_date_passage
# group by collectivite_id)
# 
# select *
# from ct_pap
# where passage_pap>'2025-01-01' and passage_pap <'2025-03-16'


# SQL (postgresql) request
df_48 = None # TODO: execute the following query:
# with ct_pap as (select collectivite_id, min(passage_pap) as passage_pap
# from pap_date_passage
# group by collectivite_id)
# 
# select *
# from ct_pap
# where passage_pap>'2026-01-01'


# SQL (postgresql) request
df_49 = None # TODO: execute the following query:
# with ct_pap as (select collectivite_id, min(passage_pap) as created_at
# from pap_date_passage
# group by collectivite_id)
# 
# select *
# from ct_pap
# where created_at>'2025-01-01'


# SQL (postgresql) request
df_60 = None # TODO: execute the following query:
# select *
# from pap_date_passage


df = df_60.sort_values('passage_pap').drop_duplicates('collectivite_id', keep='first').copy()

df[(df.passage_pap > '2025-01-01') & (df.passage_pap < '2025-03-16') & (df['import']=='Autonome')]

df[(df.passage_pap > '2026-01-01') & (df['import']=='Autonome')]

plot_monthly_fiches(df_49)

# SQL (postgresql) request
df_50 = None # TODO: execute the following query:
# select count(distinct email) as nb_users, count(distinct collectivite_id) as nb_collectivite
# from activite_semaine
# where semaine>'2025-01-01' and semaine<'2025-03-16'


# SQL (postgresql) request
df_51 = None # TODO: execute the following query:
# select count(distinct email) as nb_users, count(distinct collectivite_id) as nb_collectivite
# from activite_semaine
# where semaine>'2026-01-01'


# SQL (postgresql) request
df_52 = None # TODO: execute the following query:
# SELECT DISTINCT
#     date_trunc('month', semaine::timestamp) AS created_at,
#     email
# FROM activite_semaine
# where semaine>='2025-01-01'
# ORDER BY created_at;


plot_monthly_fiches(df_52, projection=False)

# SQL (postgresql) request
df_56 = None # TODO: execute the following query:
# SELECT DISTINCT
#     date_trunc('month', semaine::timestamp) AS created_at,
#     collectivite_id
# FROM activite_semaine
# where semaine>='2025-01-01'
# ORDER BY created_at;


plot_monthly_fiches(df_56, projection=False)

# SQL (postgresql) request
df_57 = None # TODO: execute the following query:
# SELECT DISTINCT
#     date_trunc('month', semaine::timestamp) AS created_at,
#     collectivite_id,
#     email
# FROM activite_semaine
# WHERE semaine >= '2025-01-01'
# ORDER BY created_at;


plot_monthly_fiches_agg(df_57, agg="mean", projection=False)

# SQL (postgresql) request
df_53 = None # TODO: execute the following query:
# select count(distinct user_id) as nb_user, count(distinct collectivite_id) as nb_collectivite 
# from private_utilisateur_droit pud
# join collectivite c on c.id=pud.collectivite_id
# where pud.created_at>'2025-01-01' and pud.created_at<'2025-03-16' and c.type!='test'


# SQL (postgresql) request
df_54 = None # TODO: execute the following query:
# select count(distinct user_id) as nb_user, count(distinct collectivite_id) as nb_collectivite 
# from private_utilisateur_droit pud
# join collectivite c on c.id=pud.collectivite_id
# where pud.created_at>'2026-01-01' and c.type!='test'


# SQL (postgresql) request
df_55 = None # TODO: execute the following query:
# select pud.created_at
# from private_utilisateur_droit pud
# join collectivite c on c.id=pud.collectivite_id
# where pud.created_at>'2025-01-01' and c.type!='test'


plot_monthly_fiches(df_55)

# SQL (postgresql) request
df_62 = None # TODO: execute the following query:
# SELECT
#     date_trunc('month', semaine::timestamp) AS created_at,
#     collectivite_id,
#     email
# FROM activite_semaine
# WHERE semaine >= '2025-01-01'
# ORDER BY created_at;


df_62[(df_62.created_at=='2025-01-01') | (df_62.created_at=='2025-02-01')].groupby('email').size().mean()

df_62[(df_62.created_at=='2026-01-01') | (df_62.created_at=='2026-02-01')].groupby('email').size().mean()

