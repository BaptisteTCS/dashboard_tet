"""Stabilité de Mistral Large 4 (raisonnement « low ») sur la classification volet GES.

Envoie N fois (3 par défaut) exactement le même prompt sur les mêmes lots de
fiches, puis recense les écarts entre les runs. Lecture seule sur la prod.

Le prompt, les lots et la validation viennent de utils/verify_classification_volet_ges.py.

Exemples :

    python scripts/stabilite_mistral_volet_ges.py 5119 4999 4322 4111
    python scripts/stabilite_mistral_volet_ges.py 4111 --runs 3
    python scripts/stabilite_mistral_volet_ges.py --report-only
    python scripts/stabilite_mistral_volet_ges.py 3914 5033 --prompt v2 --model claude-haiku-5-5

--prompt v2 : prompt de prompts/classification_volet_ges_v2.md, une fiche par appel,
codes de leviers et JSON contraint (utils/classification_volet_ges_v2.py). Sorties dans
data/stabilite_volet_ges_v2_1/<modèle>/ (le dossier data/stabilite_mistral_volet_ges_v2/
garde le premier test v2, fait avec la version précédente du prompt).
--model : mistral-large-4 (défaut), mistral-small-2603 ou claude-haiku-5-5 (v2 seulement).

Sorties (cumulatives) dans data/stabilite_mistral_volet_ges/ :
    <id>/fiches.csv, <id>/prod.csv, <id>/run1.json…, <id>/meta.json
    rapport.md          rapport complet, toutes collectivités traitées
    ecarts.csv          une ligne par fiche et par collectivité
    motifs_ecarts.md    analyse des motifs ; le bloc AUTO est régénéré à chaque run,
                        le reste du fichier (analyse rédigée) est conservé.
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from itertools import combinations
from pathlib import Path
from typing import Any

import pandas as pd
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.verify_classification_volet_ges import (  # noqa: E402
    CATEGORIE_ENUM_TO_ID,
    CATEGORIES,
    LEVIER_ID_TO_LABEL,
    LEVIERS_SET,
    _truncate,
    build_plan_texte,
    build_prompt_classification,
    engine_prod_readonly,
    fetch_classification_prod,
    fetch_collectivite,
    fetch_fiches_a_classifier,
    load_secrets,
    strip_json_fences,
    validate_classification,
)
from utils import classification_volet_ges_v2 as v2  # noqa: E402

OUT_BY_PROMPT = {
    "v1": ROOT / "data" / "stabilite_mistral_volet_ges",
    "v2": ROOT / "data" / "stabilite_mistral_volet_ges_v2",
}
PROMPT_VERSION = "v1"
OUT = OUT_BY_PROMPT[PROMPT_VERSION]
V2_MODEL = v2.DEFAULT_MODEL
MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
MODEL = "mistral-large-4"
MAX_TOKENS = 40000
# "none" est refusé par l'API pour mistral-large-4 (valeurs acceptées : low, medium, high).
REASONING_EFFORT = "low"
AUTO_START = "<!-- AUTO-STATS:START (régénéré par le script, ne pas éditer) -->"
AUTO_END = "<!-- AUTO-STATS:END -->"

CAT_SHORT = {
    1: "Aménagement",
    2: "Planification",
    3: "Financement",
    4: "Gouvernance",
    5: "Exemplarité",
    6: "Sensibilisation",
}

Classif = dict[int, dict[str, list[int]]]
_lock = threading.RLock()  # réentrant : log() est aussi appelé sous ce verrou


def log(msg: str) -> None:
    with _lock:
        print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


# ---------------------------------------------------------------- Mistral


def mistral_client(secrets: dict[str, Any]) -> OpenAI:
    import os

    key = (
        os.environ.get("MISTRAL_API_KEY")
        or os.environ.get("mistral_api_key")
        or str(secrets.get("mistral_api_key") or "")
    )
    if not key:
        raise RuntimeError("mistral_api_key absente (env ou .streamlit/secrets.toml).")
    return OpenAI(base_url=MISTRAL_BASE_URL, api_key=key, timeout=900.0)


def _message_text(response: Any) -> str:
    content = response.choices[0].message.content
    if isinstance(content, list):
        parts = []
        for part in content:
            get = part.get if isinstance(part, dict) else (lambda k, p=part: getattr(p, k, None))
            if get("type") == "text":
                parts.append(str(get("text") or ""))
        return "".join(parts)
    return str(content or "")


def call_mistral(client: OpenAI, prompt: str) -> tuple[Any, dict[str, int]]:
    body: dict[str, Any] = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
        "max_tokens": MAX_TOKENS,
        "extra_body": {"reasoning_effort": REASONING_EFFORT},
    }
    last: Exception | None = None
    for attempt in range(1, 6):
        try:
            resp = client.chat.completions.create(**body)
            usage = getattr(resp, "usage", None)
            tokens = {
                "input": int(getattr(usage, "prompt_tokens", 0) or 0),
                "output": int(getattr(usage, "completion_tokens", 0) or 0),
            }
            return json.loads(strip_json_fences(_message_text(resp))), tokens
        except json.JSONDecodeError:
            raise
        except Exception as e:  # 429 / 5xx : backoff
            last = e
            msg = str(e).lower()
            if "429" in msg or "rate" in msg or "503" in msg or "502" in msg or "timeout" in msg:
                wait = min(5 * attempt, 30)
                log(f"    Mistral indisponible ({type(e).__name__}), retry dans {wait}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError(f"Échec Mistral : {last}")


# ---------------------------------------------------------------- runs


def run_batch(
    client: OpenAI, batch: pd.DataFrame, label: str
) -> tuple[Classif, dict[str, Any]]:
    """Un lot : jusqu'à 3 essais si le JSON est invalide. Renvoie (classif, infos)."""
    known = set(batch["id"].astype(int))
    prompt = build_prompt_classification(build_plan_texte(batch))
    errors: list[str] = []
    tokens = {"input": 0, "output": 0}
    for attempt in range(1, 4):
        t0 = time.time()
        try:
            data, tk = call_mistral(client, prompt)
            tokens["input"] += tk["input"]
            tokens["output"] += tk["output"]
            parsed = validate_classification(data, known, LEVIERS_SET)
            log(f"  {label} ok ({time.time() - t0:.0f}s)")
            return parsed, {"essais": attempt, "erreurs": errors, "tokens": tokens}
        except (ValueError, json.JSONDecodeError) as e:
            errors.append(f"{type(e).__name__}: {e}")
            log(f"  {label} réponse invalide, essai {attempt}/3 : {e}")
    raise RuntimeError(f"{label} : 3 réponses invalides : {errors}")


def load_run(path: Path) -> Classif:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {int(k): v for k, v in raw.items()}


def save_run(path: Path, classif: Classif) -> None:
    path.write_text(
        json.dumps({str(k): classif[k] for k in sorted(classif)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def process_collectivites(ids: list[int], n_runs: int, batch_size: int, workers: int) -> None:
    secrets = load_secrets()
    engine = engine_prod_readonly(secrets)
    client = v2.make_client(V2_MODEL, secrets) if PROMPT_VERSION == "v2" else mistral_client(secrets)
    if PROMPT_VERSION == "v2":
        # Trace du prompt exact utilisé pour ce run.
        (OUT / "prompt_utilise.md").write_text(v2.load_system_prompt(), encoding="utf-8")

    jobs = []
    state: dict[tuple[int, int], Classif] = {}
    metas: dict[int, dict[str, Any]] = {}

    for cid in ids:
        coll = fetch_collectivite(engine, cid)
        fiches = fetch_fiches_a_classifier(engine, cid)
        prod = fetch_classification_prod(engine, cid)
        d = OUT / str(cid)
        d.mkdir(parents=True, exist_ok=True)
        fiches.to_csv(d / "fiches.csv", index=False, encoding="utf-8")
        prod.to_csv(d / "prod.csv", index=False, encoding="utf-8")
        meta_path = d / "meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        meta.update(
            {
                "collectivite_id": cid,
                "nom": coll["nom"],
                "prompt": PROMPT_VERSION,
                "modele": V2_MODEL if PROMPT_VERSION == "v2" else MODEL,
                "reasoning_effort": (
                    v2.MODELS[V2_MODEL]["reasoning_effort"] if PROMPT_VERSION == "v2" else REASONING_EFFORT
                ),
                "temperature": "défaut API",
                "batch_size": 1 if PROMPT_VERSION == "v2" else batch_size,
                "n_runs": n_runs,
                "n_fiches": len(fiches),
            }
        )
        meta.setdefault("lots", {})
        metas[cid] = meta
        log(f"=== {coll['nom']} ({cid}) — {len(fiches)} fiches, {n_runs} runs")

        if PROMPT_VERSION == "v2":
            contexte = v2.fetch_contexte_axes(engine, cid)
            for r in range(1, n_runs + 1):
                existing = load_run(d / f"run{r}.json")
                state[(cid, r)] = existing
                for _, row in fiches.iterrows():
                    fid = int(row["id"])
                    if fid in existing:
                        continue
                    msg = v2.build_user_message(row["titre"], row["description"], contexte.get(fid))
                    jobs.append((cid, r, f"fiche{fid}", msg))
            continue

        batches = [fiches.iloc[s : s + batch_size] for s in range(0, len(fiches), batch_size)]
        for r in range(1, n_runs + 1):
            existing = load_run(d / f"run{r}.json")
            state[(cid, r)] = existing
            for b_idx, batch in enumerate(batches, start=1):
                if set(batch["id"].astype(int)) <= set(existing):
                    continue
                jobs.append((cid, r, f"lot{b_idx}", batch))

    def run_job(cid: int, r: int, key: str, payload: Any) -> tuple[Classif, dict[str, Any]]:
        label = f"{cid} run{r} {key}"
        if PROMPT_VERSION == "v2":
            classif, infos = v2.classify_fiche(
                client, system_prompt, payload, log=log, label=label, model=V2_MODEL
            )
            return {int(key.removeprefix("fiche")): classif}, infos
        return run_batch(client, payload, label)

    system_prompt = v2.load_system_prompt() if PROMPT_VERSION == "v2" else ""
    log(f"{len(jobs)} appels à faire ({workers} en parallèle)")
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(run_job, cid, r, key, payload): (cid, r, key)
            for cid, r, key, payload in jobs
        }
        for fut in as_completed(futures):
            cid, r, b = futures[fut]
            try:
                classif, infos = fut.result()
            except Exception as e:
                failures.append(f"{cid} run{r} {b}: {e}")
                log(f"  ÉCHEC {cid} run{r} {b}: {e}")
                continue
            with _lock:
                state[(cid, r)].update(classif)
                save_run(OUT / str(cid) / f"run{r}.json", state[(cid, r)])
                metas[cid]["lots"][f"run{r}_{b}"] = infos
                done = sum(len(v["lots"]) for v in metas.values())
                if PROMPT_VERSION == "v2" and done % 50 == 0:
                    log(f"  {done} appels terminés")
                (OUT / str(cid) / "meta.json").write_text(
                    json.dumps(metas[cid], ensure_ascii=False, indent=2), encoding="utf-8"
                )

    for cid, meta in metas.items():
        meta["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        (OUT / str(cid) / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    if failures:
        log("Lots en échec (relancer la même commande pour les reprendre) :")
        for f in failures:
            log(f"  - {f}")


# ---------------------------------------------------------------- analyse


def prod_classif(prod: pd.DataFrame) -> Classif:
    out: dict[int, dict[str, set[int]]] = defaultdict(lambda: defaultdict(set))
    for _, row in prod.iterrows():
        label = LEVIER_ID_TO_LABEL.get(str(row["levier_id"]), str(row["levier_id"]))
        cat = CATEGORIE_ENUM_TO_ID.get(str(row["categorie"]))
        if cat:
            out[int(row["fiche_id"])][label].add(cat)
    return {f: {lv: sorted(c) for lv, c in m.items()} for f, m in out.items()}


def fmt(classif: dict[str, list[int]]) -> str:
    if not classif:
        return "(aucun levier)"
    return " | ".join(
        f"{lv} [{', '.join(str(c) for c in sorted(cats))}]" for lv, cats in sorted(classif.items())
    )


def pairs_of(classif: dict[str, list[int]]) -> set[tuple[str, int]]:
    return {(lv, c) for lv, cats in classif.items() for c in cats}


def majority(runs: list[dict[str, list[int]]]) -> dict[str, list[int]]:
    need = len(runs) // 2 + 1
    cnt = Counter(p for r in runs for p in pairs_of(r))
    out: dict[str, set[int]] = defaultdict(set)
    for (lv, c), n in cnt.items():
        if n >= need:
            out[lv].add(c)
    return {lv: sorted(c) for lv, c in out.items()}


def analyse_fiche(runs: list[dict[str, list[int]]]) -> dict[str, Any]:
    n = len(runs)
    stable = all(r == runs[0] for r in runs)
    leviers = sorted({lv for r in runs for lv in r})
    presence = {lv: sum(lv in r for r in runs) for lv in leviers}
    intermittents = [lv for lv in leviers if presence[lv] < n]
    cat_instables = [
        lv
        for lv in leviers
        if presence[lv] == n and len({tuple(r[lv]) for r in runs}) > 1
    ]
    vide_vs_classee = any(not r for r in runs) and any(r for r in runs)

    # Échanges de leviers (un run met A, un autre met B à la place)
    swaps: list[tuple[str, str]] = []
    cat_confusions: list[tuple[int, int]] = []
    cat_ajouts: list[tuple[str, int]] = []
    for a, b in combinations(runs, 2):
        only_a = set(a) - set(b)
        only_b = set(b) - set(a)
        for x in only_a:
            for y in only_b:
                swaps.append(tuple(sorted((x, y))))
        for lv in set(a) & set(b):
            ca, cb = set(a[lv]), set(b[lv])
            if ca == cb:
                continue
            xa, xb = ca - cb, cb - ca
            if xa and xb:
                for x in xa:
                    for y in xb:
                        cat_confusions.append(tuple(sorted((x, y))))
            else:
                for c in xa | xb:
                    cat_ajouts.append((lv, c))

    all_pairs = Counter(p for r in runs for p in pairs_of(r))
    return {
        "stable": stable,
        "intermittents": intermittents,
        "presence": presence,
        "cat_instables": cat_instables,
        "vide_vs_classee": vide_vs_classee,
        "swaps": swaps,
        "cat_confusions": cat_confusions,
        "cat_ajouts": cat_ajouts,
        "pairs_count": all_pairs,
    }


def type_ecart(a: dict[str, Any]) -> str:
    if a["stable"]:
        return "stable"
    if a["vide_vs_classee"]:
        return "vide_vs_classee"
    if a["intermittents"] and a["cat_instables"]:
        return "levier_et_categorie"
    if a["intermittents"]:
        return "levier_intermittent"
    return "categorie_instable"


TYPE_LABELS = {
    "vide_vs_classee": "Classée dans certains runs, aucun levier dans d'autres",
    "levier_intermittent": "Levier présent dans certains runs seulement",
    "levier_et_categorie": "Levier intermittent et catégories instables",
    "categorie_instable": "Mêmes leviers, catégories différentes",
    "stable": "Stables",
}


def load_collectivite(d: Path) -> dict[str, Any] | None:
    meta_path = d / "meta.json"
    if not meta_path.exists():
        return None
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    n_runs = int(meta.get("n_runs", 3))
    runs = [load_run(d / f"run{r}.json") for r in range(1, n_runs + 1)]
    fiches = pd.read_csv(d / "fiches.csv", encoding="utf-8")
    ids = [int(x) for x in fiches["id"]]
    complets = all(set(ids) <= set(r) for r in runs)
    prod_df = pd.read_csv(d / "prod.csv", encoding="utf-8") if (d / "prod.csv").stat().st_size > 5 else pd.DataFrame()
    prod = prod_classif(prod_df) if not prod_df.empty else {}
    return {
        "meta": meta,
        "runs": runs,
        "fiches": fiches.set_index("id"),
        "ids": ids,
        "complets": complets,
        "prod": prod,
    }


def build_reports() -> None:
    colls = []
    for d in sorted(p for p in OUT.iterdir() if p.is_dir()):
        c = load_collectivite(d)
        if c is None:
            continue
        if not c["complets"]:
            log(f"{d.name} : runs incomplets, ignorée dans le rapport")
            continue
        colls.append(c)
    if not colls:
        log("Aucune collectivité complète.")
        return

    rows: list[dict[str, Any]] = []
    glob = defaultdict(Counter)
    per_coll_summary = []
    lines_detail: list[str] = []

    for c in colls:
        meta, runs = c["meta"], c["runs"]
        cid, nom = meta["collectivite_id"], meta["nom"]
        n_runs = len(runs)
        type_counts: Counter = Counter()
        pair_levels: Counter = Counter()
        n_maj_prod = 0
        n_prod = 0
        detail_by_type: dict[str, list[str]] = defaultdict(list)

        for fid in c["ids"]:
            fr = [r.get(fid, {}) for r in runs]
            a = analyse_fiche(fr)
            t = type_ecart(a)
            type_counts[t] += 1
            for _, k in a["pairs_count"].items():
                pair_levels[k] += 1
            maj = majority(fr)
            prod = c["prod"].get(fid, {})
            if prod or maj:
                n_prod += 1
                n_maj_prod += int(maj == prod)

            # stats globales
            if not a["stable"]:
                glob["type"][t] += 1
            for lv in a["intermittents"]:
                glob["levier_intermittent"][lv] += 1
            for lv in a["cat_instables"]:
                glob["levier_cat_instable"][lv] += 1
            for s in set(a["swaps"]):
                glob["swap"][f"{s[0]} ↔ {s[1]}"] += 1
            for cc in set(a["cat_confusions"]):
                glob["cat_conf"][f"{cc[0]} {CAT_SHORT[cc[0]]} ↔ {cc[1]} {CAT_SHORT[cc[1]]}"] += 1
            for lv, cat in set(a["cat_ajouts"]):
                glob["cat_ajout"][f"{cat} {CAT_SHORT[cat]}"] += 1
            for lv, k in a["presence"].items():
                if k < n_runs:
                    glob["presence_k"][k] += 1

            titre = str(c["fiches"].at[fid, "titre"]) if fid in c["fiches"].index else ""
            desc = str(c["fiches"].at[fid, "description"]) if fid in c["fiches"].index else ""
            desc = "" if desc == "nan" else desc
            row = {
                "collectivite_id": cid,
                "collectivite_nom": nom,
                "fiche_id": fid,
                "titre": titre,
                "type_ecart": t,
                "leviers_intermittents": " ; ".join(
                    f"{lv} ({a['presence'][lv]}/{n_runs})" for lv in a["intermittents"]
                ),
                "leviers_categorie_instable": " ; ".join(a["cat_instables"]),
                **{f"run{i + 1}": fmt(r) for i, r in enumerate(fr)},
                "majorite": fmt(maj),
                "prod": fmt(prod),
                "majorite_egale_prod": maj == prod,
            }
            rows.append(row)

            if t != "stable":
                block = [f"#### Fiche {fid} — {titre or '(sans titre)'}", ""]
                for i, r in enumerate(fr, start=1):
                    block.append(f"- **Run {i} :** {fmt(r)}")
                block.append(f"- **Prod :** {fmt(prod)}")
                if a["intermittents"]:
                    block.append(
                        "- Leviers intermittents : "
                        + ", ".join(f"{lv} ({a['presence'][lv]}/{n_runs})" for lv in a["intermittents"])
                    )
                if a["cat_instables"]:
                    block.append("- Catégories instables sur : " + ", ".join(a["cat_instables"]))
                d_txt = _truncate(desc, 500)
                if d_txt:
                    block += ["", f"> {d_txt}"]
                block.append("")
                detail_by_type[t].append("\n".join(block))

        n = len(c["ids"])
        n_stable = type_counts["stable"]
        n_pairs = sum(pair_levels.values())
        lots = meta.get("lots", {})
        retries = sum(max(0, int(v.get("essais", 1)) - 1) for v in lots.values())
        tok_in = sum(v.get("tokens", {}).get("input", 0) for v in lots.values())
        tok_out = sum(v.get("tokens", {}).get("output", 0) for v in lots.values())
        tok_cached = sum(v.get("tokens", {}).get("cached", 0) for v in lots.values())
        tok_write = sum(v.get("tokens", {}).get("cache_write", 0) for v in lots.values())
        cout = v2.cost_usd(
            {"input": tok_in, "cached": tok_cached, "cache_write": tok_write, "output": tok_out},
            meta.get("modele", v2.DEFAULT_MODEL),
        )
        per_coll_summary.append(
            {
                "cid": cid,
                "nom": nom,
                "n": n,
                "stable": n_stable,
                "pairs": n_pairs,
                "pairs_full": pair_levels[n_runs],
                "types": type_counts,
                "maj_prod": (n_maj_prod, n_prod),
                "prod_vide": not c["prod"],
                "retries": retries,
                "tokens": (tok_in, tok_out),
                "date": meta.get("date", ""),
            }
        )

        lines_detail += [
            f"## {nom} ({cid})",
            "",
            f"- Fiches : **{n}** — stables sur les {n_runs} runs : **{n_stable}** "
            f"({n_stable / n:.0%}), instables : **{n - n_stable}**",
            f"- Paires levier × catégorie distinctes proposées : {n_pairs} — "
            + ", ".join(f"{k}/{n_runs} runs : {pair_levels[k]}" for k in range(n_runs, 0, -1)),
            (
                "- Aucune classification en prod pour cette collectivité"
                if not c["prod"]
                else f"- Vote majoritaire = prod : {n_maj_prod}/{n_prod} fiches classées d'un côté ou de l'autre"
            ),
            f"- Réponses JSON invalides rejouées : {retries}",
            f"- Appels : {len(lots)} — tokens d'entrée {tok_in:_} (dont {tok_cached:_} en cache, "
            f"{tok_cached / tok_in if tok_in else 0:.0%}), sortie {tok_out:_} — "
            f"coût estimé {cout:.2f} $ pour les {n_runs} runs".replace("_", " "),
            f"- Date : {meta.get('date', '')}",
            "",
        ]
        for t in ["vide_vs_classee", "levier_intermittent", "levier_et_categorie", "categorie_instable"]:
            if detail_by_type[t]:
                lines_detail += [f"### {TYPE_LABELS[t]} ({len(detail_by_type[t])})", ""]
                lines_detail += detail_by_type[t]

    # ---- rapport.md
    head = [
        "# Stabilité Mistral Large 4 — classification volet GES",
        "",
        f"Modèle `{colls[0]['meta'].get('modele', MODEL)}`, "
        f"raisonnement `{colls[0]['meta'].get('reasoning_effort') or 'aucun'}`, température par défaut de l'API. "
        + (
            "Prompt v2 (`prompts/classification_volet_ges_v2.md`), une fiche par appel, "
            "codes de leviers et JSON contraint, "
            if PROMPT_VERSION == "v2"
            else "Même prompt (`pages/26_run_impact.py`), mêmes lots de 25 fiches, "
        )
        + f"{len(colls[0]['runs'])} runs indépendants. Lecture seule sur la prod.",
        "",
        f"Mis à jour le {datetime.now():%Y-%m-%d %H:%M}.",
        "",
        "## Synthèse",
        "",
        "| Collectivité | Fiches | Stables | Instables | % stable | Paires 3/3 | Majorité = prod |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for s in per_coll_summary:
        head.append(
            f"| {s['nom']} ({s['cid']}) | {s['n']} | {s['stable']} | {s['n'] - s['stable']} | "
            f"{s['stable'] / s['n']:.0%} | {s['pairs_full']}/{s['pairs']} | "
            + ("non classée en prod |" if s["prod_vide"] else f"{s['maj_prod'][0]}/{s['maj_prod'][1]} |")
        )
    tot_n = sum(s["n"] for s in per_coll_summary)
    tot_s = sum(s["stable"] for s in per_coll_summary)
    head += [
        f"| **Total** | **{tot_n}** | **{tot_s}** | **{tot_n - tot_s}** | **{tot_s / tot_n:.0%}** | | |",
        "",
        "« Paires 3/3 » : paires levier × catégorie données par les 3 runs, sur toutes les paires proposées au moins une fois.",
        "",
    ]
    (OUT / "rapport.md").write_text("\n".join(head + lines_detail), encoding="utf-8")
    pd.DataFrame(rows).to_csv(OUT / "ecarts.csv", index=False, encoding="utf-8-sig")

    # ---- bloc auto de motifs_ecarts.md
    n_inst = tot_n - tot_s

    def top(counter: Counter, k: int = 12) -> list[str]:
        return [f"| {name} | {cnt} |" for name, cnt in counter.most_common(k)] or ["| — | 0 |"]

    auto = [
        AUTO_START,
        "",
        f"_Statistiques recalculées le {datetime.now():%Y-%m-%d %H:%M} sur "
        f"{len(colls)} collectivités : "
        + ", ".join(f"{s['nom']} ({s['cid']})" for s in per_coll_summary)
        + "._",
        "",
        f"- Fiches analysées : **{tot_n}**, instables : **{n_inst}** ({n_inst / tot_n:.0%})",
        "",
        "### Types d'écart (fiches instables)",
        "",
        "| Type | Fiches | Part des instables |",
        "|---|---:|---:|",
    ]
    for t in ["vide_vs_classee", "levier_intermittent", "levier_et_categorie", "categorie_instable"]:
        cnt = glob["type"][t]
        auto.append(f"| {TYPE_LABELS[t]} | {cnt} | {cnt / n_inst:.0%} |" if n_inst else f"| {TYPE_LABELS[t]} | 0 | — |")
    auto += [
        "",
        "### Leviers les plus intermittents (fiches où le levier n'apparaît pas dans tous les runs)",
        "",
        "| Levier | Fiches |",
        "|---|---:|",
        *top(glob["levier_intermittent"]),
        "",
        "### Leviers stables mais dont les catégories changent",
        "",
        "| Levier | Fiches |",
        "|---|---:|",
        *top(glob["levier_cat_instable"]),
        "",
        "### Catégories ajoutées ou retirées selon le run (même levier)",
        "",
        "| Catégorie | Fiches |",
        "|---|---:|",
        *top(glob["cat_ajout"]),
        "",
        "### Catégories échangées entre runs (même levier)",
        "",
        "| Échange | Fiches |",
        "|---|---:|",
        *top(glob["cat_conf"]),
        "",
        "### Leviers échangés entre runs (un run met A, un autre B)",
        "",
        "| Échange | Fiches |",
        "|---|---:|",
        *top(glob["swap"]),
        "",
        AUTO_END,
    ]
    motifs = OUT / "motifs_ecarts.md"
    auto_txt = "\n".join(auto)
    if motifs.exists():
        txt = motifs.read_text(encoding="utf-8")
        if AUTO_START in txt and AUTO_END in txt:
            pre = txt.split(AUTO_START)[0]
            post = txt.split(AUTO_END, 1)[1]
            txt = pre + auto_txt + post
        else:
            txt = txt.rstrip() + "\n\n## Statistiques\n\n" + auto_txt + "\n"
    else:
        txt = (
            "# Motifs des écarts entre runs — Mistral Large 4\n\n"
            "## Analyse\n\n_(à rédiger)_\n\n## Statistiques\n\n" + auto_txt + "\n"
        )
    motifs.write_text(txt, encoding="utf-8")
    log(f"Rapport : {OUT / 'rapport.md'}")
    log(f"Motifs  : {motifs}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("collectivite_ids", nargs="*", type=int)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--workers", type=int, default=4, help="Appels Mistral en parallèle")
    parser.add_argument("--report-only", action="store_true", help="Régénère rapport et stats")
    parser.add_argument("--prompt", choices=sorted(OUT_BY_PROMPT), default="v1")
    parser.add_argument("--model", choices=sorted(v2.MODELS), default=v2.DEFAULT_MODEL)
    args = parser.parse_args()

    global OUT, PROMPT_VERSION, V2_MODEL
    PROMPT_VERSION = args.prompt
    V2_MODEL = args.model
    OUT = (
        ROOT / "data" / "stabilite_volet_ges_v2_1" / V2_MODEL
        if PROMPT_VERSION == "v2"
        else OUT_BY_PROMPT[PROMPT_VERSION]
    )
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.report_only:
        if not args.collectivite_ids:
            parser.error("donner au moins un identifiant de collectivité")
        process_collectivites(args.collectivite_ids, args.runs, args.batch_size, args.workers)
    build_reports()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
