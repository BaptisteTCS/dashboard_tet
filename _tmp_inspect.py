import tomllib

import pandas as pd
from sqlalchemy import create_engine, text

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_colwidth", 60)

secrets = tomllib.load(open(".streamlit/secrets.toml", "rb"))


def engine(key):
    url = secrets[key]
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return create_engine(url)


olap = engine("DATABASE_URL")
prod = engine("database_prod")

with olap.connect() as conn:
    df_actions = pd.read_sql_query(
        text("select collectivite_id, levier, categorie, fiche_action_id from priorisation_action"),
        conn,
    )
    df_ref = pd.read_sql_query(
        text("select id, levier, categorie, titre from priorisation_action_reference"),
        conn,
    )

print("ids reference: min/max", df_ref["id"].min(), df_ref["id"].max(), "n =", len(df_ref))

ids = tuple(int(i) for i in df_actions["fiche_action_id"].unique())
with prod.connect() as conn:
    df_fiches = pd.read_sql_query(
        text("select id, collectivite_id, titre from fiche_action where id = ANY(:ids)"),
        conn,
        params={"ids": list(ids)},
    )

ref_index = {(r["levier"], int(r["categorie"]), int(r["id"])) for _, r in df_ref.iterrows()}
ref_ids = set(df_ref["id"].astype(int))
prod_ids = set(df_fiches["id"].astype(int))

rows = []
for _, r in df_actions.iterrows():
    fid = int(r["fiche_action_id"])
    rows.append(
        {
            "coll": r["collectivite_id"],
            "levier": r["levier"][:28],
            "cat": r["categorie"],
            "fid": fid,
            "ref_meme_volet": (r["levier"], int(r["categorie"]), fid) in ref_index,
            "ref_id_existe": fid in ref_ids,
            "prod_existe": fid in prod_ids,
        }
    )
print(pd.DataFrame(rows).to_string())

both = [r for r in rows if r["ref_meme_volet"] and r["prod_existe"]]
print("ambigus (ref meme volet ET prod):", len(both))
print("ni ref volet ni prod:", len([r for r in rows if not r["ref_meme_volet"] and not r["prod_existe"]]))
