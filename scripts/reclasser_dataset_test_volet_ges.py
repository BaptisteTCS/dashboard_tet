"""Reclasse les fiches du dataset de test avec Haiku et le prompt actuel, puis régénère l'Excel.

Garde les mêmes fiches, dans le même ordre (lues dans dataset_test_<N>_fiches.csv).
3 runs par fiche, une fiche par appel, même message que le script de stabilité.
Sortie : dataset_test_<N>_fiches_<OUT_SUFFIX>.xlsx (+ .csv), à côté de l'Excel d'origine, qui n'est pas modifié.
Lecture seule sur la prod (contexte plan > axe).

    python scripts/reclasser_dataset_test_volet_ges.py
"""

from __future__ import annotations

import ast
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import construire_dataset_test_volet_ges as cd  # noqa: E402
import stabilite_mistral_volet_ges as s  # noqa: E402
from utils import classification_volet_ges_v2 as v2  # noqa: E402
from utils.verify_classification_volet_ges import engine_prod_readonly, load_secrets  # noqa: E402

MODEL = "claude-haiku-5-5"
PROMPT_VERSION = "v2.3"
OUT_SUFFIX = "v2_3"
PREV_SUFFIX = "v2_2"  # version précédente, pour compter les changements
N_RUNS = 3
WORKERS = 8
RUNS_DIR = ROOT / "data" / f"stabilite_volet_ges_{OUT_SUFFIX}" / MODEL / "dataset_test"
_lock = threading.RLock()


def log(msg: str) -> None:
    with _lock:
        print(msg, flush=True)


def main() -> int:
    csv_path = cd.OUT_DIR / f"dataset_test_{cd.N}_fiches.csv"
    xlsx_path = cd.OUT_DIR / f"dataset_test_{cd.N}_fiches_{OUT_SUFFIX}.xlsx"
    out_csv = xlsx_path.with_suffix(".csv")
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    old_haiku = df["haiku"].map(ast.literal_eval)

    # Description brute, telle qu'envoyée au modèle par le script de stabilité.
    raw = {}
    for cid in df["collectivite_id"].unique():
        f = pd.read_csv(cd.HAIKU_DIR / str(cid) / "fiches.csv", encoding="utf-8")
        raw.update({int(r["id"]): (r["titre"], r["description"]) for _, r in f.iterrows()})

    secrets = load_secrets()
    engine = engine_prod_readonly(secrets)
    ctx_axes: dict[int, str] = {}
    for cid in df["collectivite_id"].unique():
        ctx_axes.update(v2.fetch_contexte_axes(engine, int(cid)))

    system_prompt = v2.load_system_prompt()
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    (RUNS_DIR / "prompt_utilise.md").write_text(system_prompt, encoding="utf-8")
    client = v2.make_client(MODEL, secrets)

    runs_path = RUNS_DIR / "runs.json"
    results: dict[str, dict] = json.loads(runs_path.read_text(encoding="utf-8")) if runs_path.exists() else {}
    jobs = []
    for fid in df["fiche_id"].astype(int):
        titre, desc = raw[fid]
        msg = v2.build_user_message(titre, desc, ctx_axes.get(fid))
        for r in range(1, N_RUNS + 1):
            if f"{fid}:{r}" not in results:
                jobs.append((fid, r, msg))
    log(f"{len(jobs)} appels à faire ({len(results)} déjà faits)")

    def run(job):
        fid, r, msg = job
        return job, v2.classify_fiche(client, system_prompt, msg, log=log, label=f"fiche{fid} run{r}", model=MODEL)

    with ThreadPoolExecutor(WORKERS) as ex:
        for n, fut in enumerate(as_completed([ex.submit(run, j) for j in jobs]), start=1):
            (fid, r, _), (classif, infos) = fut.result()
            with _lock:
                results[f"{fid}:{r}"] = {"classif": classif, **infos}
                if n % 50 == 0 or n == len(jobs):
                    runs_path.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
                    log(f"  {n}/{len(jobs)}")

    tokens = {"input": 0, "cached": 0, "cache_write": 0, "output": 0}
    for v in results.values():
        for k in tokens:
            tokens[k] += v["tokens"].get(k, 0)
    retries = sum(v["essais"] - 1 for v in results.values())
    tronques = sum(v["tokens"].get("tronque", 0) for v in results.values())

    runs_col, maj_col, stable_col = [], [], []
    for fid in df["fiche_id"].astype(int):
        runs = [results[f"{fid}:{r}"]["classif"] for r in range(1, N_RUNS + 1)]
        runs_col.append(runs)
        maj_col.append(s.majority(runs))
        stable_col.append(all(x == runs[0] for x in runs))
    df["runs"], df["haiku"], df["stable"] = runs_col, maj_col, stable_col
    df["n_leviers"] = df["haiku"].map(len)

    pool = cd.load_pool()
    ctx = cd.fetch_contextes(sorted(df["collectivite_id"].unique()))
    note = (
        f"Pré-remplissage : vote majoritaire de Claude Haiku 5.5 sur 3 runs, prompt {PROMPT_VERSION} "
        "(prompts/classification_volet_ges_v2.md, une fiche par appel). Le tirage des fiches et la "
        "colonne « Vivier » du tableau ci-dessous viennent de la version précédente du prompt."
    )
    cd.write_excel(df, pool, {}, ctx, xlsx_path, prefill_note=note)
    df.drop(columns=["runs"]).assign(haiku=df["haiku"].map(str)).to_csv(out_csv, index=False, encoding="utf-8-sig")

    changed = sum(a != b for a, b in zip(old_haiku, df["haiku"]))
    print(f"Coût : {v2.cost_usd(tokens, MODEL):.3f} $ — cache {tokens['cached'] / max(tokens['input'], 1):.0%}")
    print(f"Réponses invalides rejouées : {retries} — réponses tronquées à 3 leviers : {tronques}")
    print(f"Stables 3/3 : {sum(stable_col)}/{len(df)}")
    print(f"Vote majoritaire différent de la v2.1 (Excel d'origine) : {changed}/{len(df)}")
    prev_csv = cd.OUT_DIR / f"dataset_test_{cd.N}_fiches_{PREV_SUFFIX}.csv"
    if prev_csv.exists():
        prev = pd.read_csv(prev_csv, encoding="utf-8-sig")
        prev = dict(zip(prev["fiche_id"].astype(int), prev["haiku"].map(ast.literal_eval)))
        diff = [fid for fid, h in zip(df["fiche_id"].astype(int), df["haiku"]) if prev.get(fid) != h]
        print(f"Vote majoritaire différent de {PREV_SUFFIX} : {len(diff)}/{len(df)}")
        for fid in diff:
            print(f"  {fid}: {prev.get(fid)} -> {df.loc[df['fiche_id'] == fid, 'haiku'].iloc[0]}")
    print("Leviers par fiche :", df["n_leviers"].value_counts().sort_index().to_dict())
    print("Fichier :", xlsx_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
