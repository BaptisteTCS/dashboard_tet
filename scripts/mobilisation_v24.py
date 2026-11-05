"""Stabilité de la classification v2.4 et des notes de mobilisation calculées, sur un échantillon de collectivités.

Pour chaque collectivité : fiches (hors abandonnées et en pause) avec leurs sous-actions,
N runs de la classification v2.4 (Claude Haiku 5.5, une fiche par appel), puis notes de
chaque case levier × catégorie calculées par le code à partir des verdicts « structurante ».

Sorties dans data/mobilisation_v2_4/claude-haiku-5-5/ :
- <cid>/fiches.json, <cid>/runs.json (reprise possible) ;
- notes.csv : une ligne par case (notes par run, note retenue, note actuelle en prod) ;
- classification.csv : classification retenue par fiche ;
- rapport.md.

Lecture seule sur la prod (collectivite, fiche_action, axe, collectivite_volet_ges).

    python scripts/mobilisation_v24.py                 # 21 collectivités, 3 runs
    python scripts/mobilisation_v24.py 4999 --runs 1   # une collectivité
    python scripts/mobilisation_v24.py --report-only
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import text

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils import classification_volet_ges_v2 as v2  # noqa: E402
from utils import classification_volet_ges_v2_4 as v24  # noqa: E402
from utils.verify_classification_volet_ges import (  # noqa: E402
    CATEGORIE_ENUM_TO_ID,
    LEVIER_ID_TO_LABEL,
    engine_prod_readonly,
    load_secrets,
)

ECHANTILLON = [13693, 1609, 3893, 3914, 4026, 4097, 4111, 4322, 4576, 4637, 4707,
               4939, 4973, 4994, 4999, 5005, 5033, 5119, 5300, 5390, 6030]
OUT = ROOT / "data" / "mobilisation_v2_4" / v24.MODEL
_lock = threading.RLock()


def log(msg: str) -> None:
    with _lock:
        print(msg, flush=True)


# ---------------------------------------------------------------- runs


def prepare(engine, cid: int) -> dict[str, Any]:
    d = OUT / str(cid)
    d.mkdir(parents=True, exist_ok=True)
    path = d / "fiches.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    info = v24.fetch_collectivite_info(engine, cid)
    fiches = v24.fetch_fiches(engine, cid)
    ctx = v2.fetch_contexte_axes(engine, cid)
    data = {
        "collectivite": info,
        "fiches": [
            {
                "id": int(r.id),
                "titre": r.titre,
                "statut": r.statut,
                "n_sous_actions": len(r.sous_actions),
                "message": v24.build_user_message(info, r.titre, r.description, ctx.get(int(r.id)), r.sous_actions),
            }
            for r in fiches.itertuples()
        ],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return data


def run_all(ids: list[int], n_runs: int, workers: int) -> None:
    secrets = load_secrets()
    engine = engine_prod_readonly(secrets)
    client = v2.make_client(v24.MODEL, secrets)
    system_prompt = v24.load_system_prompt()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "prompt_utilise.md").write_text(system_prompt, encoding="utf-8")

    results: dict[int, dict[str, Any]] = {}
    jobs = []
    for cid in ids:
        data = prepare(engine, cid)
        rp = OUT / str(cid) / "runs.json"
        results[cid] = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
        for f in data["fiches"]:
            for r in range(1, n_runs + 1):
                if f"{f['id']}:{r}" not in results[cid]:
                    jobs.append((cid, f["id"], r, f["message"]))
        log(f"{data['collectivite']['nom']} ({cid}) : {len(data['fiches'])} fiches")
    log(f"{len(jobs)} appels à faire")

    def work(job):
        cid, fid, r, msg = job
        return job, v24.classify_fiche(client, system_prompt, msg, log=log, label=f"{cid}/{fid} run{r}")

    def save(cid):
        (OUT / str(cid) / "runs.json").write_text(json.dumps(results[cid], ensure_ascii=False), encoding="utf-8")

    with ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for n, fut in enumerate(as_completed(futs), start=1):
            try:
                (cid, fid, r, _), (classif, infos) = fut.result()
            except Exception as e:  # une fiche en échec ne bloque pas les autres
                log(f"  ÉCHEC : {e}")
                continue
            with _lock:
                results[cid][f"{fid}:{r}"] = {"classif": classif, **infos}
                if n % 200 == 0 or n == len(jobs):
                    for c in ids:
                        save(c)
                    log(f"  {n}/{len(jobs)}")
    for c in ids:
        save(c)


# ---------------------------------------------------------------- analyse


def majority(runs: list[v24.Classif]) -> v24.Classif:
    """Classification la plus fréquente ; sinon, levier par levier, ce qu'au moins la moitié des runs donnent."""
    keyed = Counter(json.dumps(r, sort_keys=True) for r in runs)
    top, cnt = keyed.most_common(1)[0]
    if cnt * 2 > len(runs):
        return json.loads(top)
    half = len(runs) / 2
    out: v24.Classif = {}
    for lev in {lv for r in runs for lv in r}:
        present = [r[lev] for r in runs if lev in r]
        if len(present) < half:
            continue
        cats = Counter(c for p in present for c in p["categories"])
        keep = sorted(c for c, k in cats.items() if k >= len(present) / 2) or [cats.most_common(1)[0][0]]
        struct = sum(p["structurante"] for p in present) * 2 > len(present)
        out[lev] = {"categories": keep, "structurante": struct}
    return out


def fetch_notes_prod(engine, ids: list[int]) -> pd.DataFrame:
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text(
                "SELECT collectivite_id, levier_id::text AS levier_id, categorie::text AS categorie, note, fiche_ids "
                "FROM collectivite_volet_ges WHERE collectivite_id = ANY(:ids)"
            ),
            conn,
            params={"ids": ids},
        )
    df["levier"] = df["levier_id"].map(LEVIER_ID_TO_LABEL)
    df["categorie"] = df["categorie"].map(CATEGORIE_ENUM_TO_ID).astype(int)
    return df


def report(ids: list[int]) -> None:
    engine = engine_prod_readonly(load_secrets())
    prod = fetch_notes_prod(engine, ids)
    prod_notes = {(int(r.collectivite_id), r.levier, int(r.categorie)): (int(r.note), list(r.fiche_ids or []))
                  for r in prod.itertuples()}

    case_rows, fiche_rows, coll_rows = [], [], []
    tokens = {"input": 0, "cached": 0, "cache_write": 0, "output": 0}
    retries = tronques = 0
    struct_pairs = Counter()
    for cid in ids:
        d = OUT / str(cid)
        if not (d / "runs.json").exists():
            continue
        data = json.loads((d / "fiches.json").read_text(encoding="utf-8"))
        res = json.loads((d / "runs.json").read_text(encoding="utf-8"))
        n_runs = max(int(k.split(":")[1]) for k in res)
        for v in res.values():
            for k in tokens:
                tokens[k] += v["tokens"].get(k, 0)
            retries += v["essais"] - 1
            tronques += v["tokens"].get("tronque", 0)
        titres = {f["id"]: f["titre"] for f in data["fiches"]}
        par_run: list[dict[int, v24.Classif]] = [{} for _ in range(n_runs)]
        maj: dict[int, v24.Classif] = {}
        n_stable_classif = n_stable_full = 0
        fiches_ok = [f for f in data["fiches"] if all(f"{f['id']}:{r}" in res for r in range(1, n_runs + 1))]
        for f in fiches_ok:
            fid = f["id"]
            runs = [res[f"{fid}:{r}"]["classif"] for r in range(1, n_runs + 1)]
            for r, c in enumerate(runs):
                par_run[r][fid] = c
            maj[fid] = majority(runs)
            sans_struct = [{lv: i["categories"] for lv, i in c.items()} for c in runs]
            stable_classif = all(x == sans_struct[0] for x in sans_struct)
            stable_full = all(x == runs[0] for x in runs)
            n_stable_classif += stable_classif
            n_stable_full += stable_full
            for lev in set.intersection(*(set(c) for c in runs)) if runs else set():
                vals = {c[lev]["structurante"] for c in runs}
                struct_pairs["stable" if len(vals) == 1 else "instable"] += 1
            fiche_rows.append({
                "collectivite_id": cid, "fiche_id": fid, "titre": f["titre"], "n_sous_actions": f["n_sous_actions"],
                "classification": json.dumps(maj[fid], ensure_ascii=False), "stable_classif": stable_classif,
                "stable_complet": stable_full,
            })
        notes_runs = [v24.notes_from_classification(pr) for pr in par_run]
        notes_maj = v24.notes_from_classification(maj)
        keys = set().union(*(set(n) for n in notes_runs)) | set(notes_maj) | {
            (lv, cat) for (c, lv, cat) in prod_notes if c == cid}
        for lev, cat in sorted(keys):
            run_notes = [n.get((lev, cat), {}).get("note", 0) for n in notes_runs]
            vide = {"structurantes": [], "peu_importantes": []}
            comptes = {}
            for i, n in enumerate(notes_runs):
                c = n.get((lev, cat), vide)
                comptes[f"n_struct_run{i + 1}"] = len(c["structurantes"])
                comptes[f"n_peu_run{i + 1}"] = len(c["peu_importantes"])
            m = notes_maj.get((lev, cat), {"note": 0, "structurantes": [], "peu_importantes": []})
            p = prod_notes.get((cid, lev, cat))
            case_rows.append({
                "collectivite_id": cid, "levier": lev, "categorie": cat,
                **comptes,
                **{f"note_run{i + 1}": x for i, x in enumerate(run_notes)},
                "stable": len(set(run_notes)) == 1, "ecart_runs": max(run_notes) - min(run_notes),
                "note": m["note"],
                "structurantes": json.dumps(m["structurantes"]), "peu_importantes": json.dumps(m["peu_importantes"]),
                "note_prod": p[0] if p else None, "fiche_ids_prod": json.dumps(p[1]) if p else None,
            })
        coll_rows.append({"cid": cid, "nom": data["collectivite"]["nom"], "type": data["collectivite"]["type_label"],
                          "pop": data["collectivite"]["population"], "fiches": len(fiches_ok),
                          "stable_classif": n_stable_classif, "stable_full": n_stable_full, "runs": n_runs})
        _ = titres

    cases = pd.DataFrame(case_rows)
    fiches = pd.DataFrame(fiche_rows)
    cases.to_csv(OUT / "notes.csv", index=False, encoding="utf-8-sig")
    fiches.to_csv(OUT / "classification.csv", index=False, encoding="utf-8-sig")

    # cases notées dans au moins un run (hors cases vides partout)
    actives = cases[(cases[[c for c in cases.columns if c.startswith("note_run")]].max(axis=1) > 0)]
    comp = cases[cases["note_prod"].notna()].copy()
    comp_actives = comp[(comp["note"] > 0) | (comp["note_prod"] > 0)]
    lines = [
        "# Notes de mobilisation calculées (classification v2.4) — stabilité et comparaison avec la prod",
        "",
        f"Mis à jour le {datetime.now():%Y-%m-%d %H:%M}. Claude Haiku 5.5, prompt `prompts/classification_volet_ges_v2_4.md`, "
        f"une fiche par appel, {coll_rows[0]['runs'] if coll_rows else '?'} runs. Lecture seule sur la prod.",
        "",
        "## Synthèse",
        "",
        f"- Fiches : **{len(fiches)}** dans {len(coll_rows)} collectivités",
        f"- Classification identique (leviers + catégories) sur tous les runs : **{fiches['stable_classif'].mean():.0%}**",
        f"- Classification et verdicts « structurante » identiques : **{fiches['stable_complet'].mean():.0%}**",
        f"- Verdict « structurante » identique, pour les leviers retenus par tous les runs : "
        f"**{struct_pairs['stable'] / max(sum(struct_pairs.values()), 1):.0%}** ({sum(struct_pairs.values())} paires fiche × levier)",
        f"- Cases levier × catégorie notées dans au moins un run : **{len(actives)}**",
        f"- … dont note identique sur tous les runs : **{actives['stable'].mean():.0%}** ; écart de 1 point : "
        f"{(actives['ecart_runs'] == 1).mean():.0%} ; écart de 2 points ou plus : {(actives['ecart_runs'] >= 2).mean():.0%}",
        f"- Coût : {v2.cost_usd(tokens, v24.MODEL):.2f} $ — réponses invalides rejouées : {retries} — tronquées à 3 leviers : {tronques}",
        "",
        "## Par collectivité",
        "",
        "| Collectivité | Type | Population | Fiches | Classif. stable | Cases notées | Notes stables |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for c in coll_rows:
        a = actives[actives["collectivite_id"] == c["cid"]]
        lines.append(
            f"| {c['nom']} ({c['cid']}) | {c['type']} | {c['pop'] or '—'} | {c['fiches']} | "
            f"{c['stable_classif'] / max(c['fiches'], 1):.0%} | {len(a)} | {a['stable'].mean() if len(a) else 0:.0%} |"
        )
    dist_new = actives["note"].value_counts().sort_index().to_dict()
    lines += [
        "",
        "## Répartition des notes (note retenue, cases notées dans au moins un run)",
        "",
        f"- Nouvelle note : {dist_new}",
    ]
    if len(comp):
        ct = pd.crosstab(comp_actives["note_prod"].astype(int), comp_actives["note"], rownames=["prod"], colnames=["nouvelle"])
        lines += [
            "",
            f"## Comparaison avec la note actuelle en prod ({comp['collectivite_id'].nunique()} collectivités notées en prod)",
            "",
            f"- Cases non nulles dans l'une ou l'autre : {len(comp_actives)}",
            f"- Même note : {(comp_actives['note'] == comp_actives['note_prod']).mean():.0%} ; "
            f"nouvelle plus haute : {(comp_actives['note'] > comp_actives['note_prod']).mean():.0%} ; "
            f"plus basse : {(comp_actives['note'] < comp_actives['note_prod']).mean():.0%}",
            f"- Note moyenne : prod {comp_actives['note_prod'].mean():.2f}, nouvelle {comp_actives['note'].mean():.2f}",
            "",
            "Croisement (lignes : note prod, colonnes : nouvelle note) :",
            "",
            "| prod \\ nouvelle | " + " | ".join(str(c) for c in ct.columns) + " |",
            "|---|" + "---:|" * len(ct.columns),
            *[f"| {i} | " + " | ".join(str(v) for v in row) + " |" for i, row in zip(ct.index, ct.values)],
        ]
    lines += ["", "## Comparaison des règles de notation", "",
              "Mêmes classifications ; seule la règle qui transforme les comptes de fiches en note change.", "",
              "| Règle | Notes stables (3 runs) | Écart ≥ 2 points | Répartition (cases notées) | Même note que la prod | Note moyenne (prod → nouvelle) |",
              "|---|---:|---:|---|---:|---|"]
    n_runs_max = max((c["runs"] for c in coll_rows), default=0)
    for regle, (libelle, _) in v24.REGLES.items():
        rn = pd.DataFrame({
            i: [v24.note_case(s, p, regle) for s, p in zip(cases[f"n_struct_run{i}"], cases[f"n_peu_run{i}"])]
            for i in range(1, n_runs_max + 1)
        })
        maj = [v24.note_case(len(json.loads(s)), len(json.loads(p)), regle)
               for s, p in zip(cases["structurantes"], cases["peu_importantes"])]
        act = rn.max(axis=1) > 0
        stable = (rn.nunique(axis=1) == 1)[act].mean()
        ecart2 = ((rn.max(axis=1) - rn.min(axis=1)) >= 2)[act].mean()
        dist = pd.Series(maj)[act].value_counts().sort_index().to_dict()
        cmp_ = cases.assign(note_r=maj)
        cmp_ = cmp_[cmp_["note_prod"].notna() & ((cmp_["note_r"] > 0) | (cmp_["note_prod"] > 0))]
        lines.append(
            f"| {libelle} | {stable:.0%} | {ecart2:.0%} | {dist} | {(cmp_['note_r'] == cmp_['note_prod']).mean():.0%} | "
            f"{cmp_['note_prod'].mean():.2f} → {cmp_['note_r'].mean():.2f} |"
        )
    (OUT / "rapport.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", type=int)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    ids = a.ids or ECHANTILLON
    if not a.report_only:
        run_all(ids, a.runs, a.workers)
    report(ids)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
