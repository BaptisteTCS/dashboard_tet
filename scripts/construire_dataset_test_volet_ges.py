"""Construit le dataset de test (fiches à vérifier à la main) à partir des runs Haiku.

Vivier : fiches des collectivités classées par Haiku (prompt v2, 3 runs) qui ont un titre
et une description d'au moins MIN_DESCRIPTION caractères (texte, HTML retiré).
Tirage : N fiches dont la répartition du nombre de leviers (vote majoritaire Haiku)
reproduit celle du vivier ; au plus MAX_PAR_COLLECTIVITE fiches par collectivité ;
dans chaque strate, priorité aux leviers encore peu représentés.

Sortie : data/dataset_test_volet_ges/dataset_test_<N>_fiches.xlsx (+ .csv des fiches tirées).
Lecture seule sur la prod (contexte plan > axe).

    python scripts/construire_dataset_test_volet_ges.py
"""

from __future__ import annotations

import html
import math
import random
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import stabilite_mistral_volet_ges as s  # noqa: E402
from utils import classification_volet_ges_v2 as v2  # noqa: E402
from utils.verify_classification_volet_ges import (  # noqa: E402
    CATEGORIES,
    LEVIER_ID_TO_LABEL,
    engine_prod_readonly,
    load_secrets,
)

HAIKU_DIR = ROOT / "data" / "stabilite_volet_ges_v2_1" / "claude-haiku-5-5"
OUT_DIR = ROOT / "data" / "dataset_test_volet_ges"
N = 100
MIN_DESCRIPTION = 50
MAX_PAR_COLLECTIVITE = 10
SEED = 2026

# Libellés du prompt v2 (le code vehicules_electriques s'affiche « Voiture électrique »).
LABEL_V2 = dict(LEVIER_ID_TO_LABEL)
LABEL_V2["vehicules_electriques"] = "Voiture électrique"
V1_LABEL_TO_CODE = {label: code for code, label in LEVIER_ID_TO_LABEL.items()}


def html_to_text(raw: str) -> str:
    if not isinstance(raw, str) or raw.strip().lower() == "nan":
        return ""
    t = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>", "\n", raw)
    t = re.sub(r"(?i)<li[^>]*>", "• ", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t).replace("\xa0", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()


def load_pool() -> pd.DataFrame:
    rows = []
    for d in sorted(p for p in HAIKU_DIR.iterdir() if p.is_dir()):
        c = s.load_collectivite(d)
        if c is None or not c["complets"]:
            continue
        nom = c["meta"]["nom"]
        for fid in c["ids"]:
            f = c["fiches"].loc[fid]
            titre = " ".join(str(f["titre"] if isinstance(f["titre"], str) else "").split())
            desc = html_to_text(f["description"])
            runs = [r.get(fid, {}) for r in c["runs"]]
            maj = s.majority(runs)
            rows.append(
                {
                    "collectivite_id": int(d.name),
                    "collectivite": nom,
                    "fiche_id": int(fid),
                    "titre": titre,
                    "description": desc,
                    "haiku": maj,
                    "n_leviers": len(maj),
                    "stable": all(r == runs[0] for r in runs),
                    "runs": runs,
                }
            )
    df = pd.DataFrame(rows)
    return df[(df["titre"].str.len() > 0) & (df["description"].str.len() >= MIN_DESCRIPTION)].reset_index(drop=True)


def quotas(dist: pd.Series, n: int) -> dict[int, int]:
    """Répartition proportionnelle (méthode du plus fort reste)."""
    raw = dist / dist.sum() * n
    q = {k: int(math.floor(v)) for k, v in raw.items()}
    for k in (raw - pd.Series(q)).sort_values(ascending=False).index[: n - sum(q.values())]:
        q[k] += 1
    return q


def sample(pool: pd.DataFrame) -> pd.DataFrame:
    rng = random.Random(SEED)
    q = quotas(pool["n_leviers"].value_counts().sort_index(), N)
    chosen: list[int] = []
    per_coll: Counter = Counter()
    lev_count: Counter = Counter()
    for k in sorted(q, reverse=True):  # strates riches en leviers d'abord : meilleure couverture
        idx = list(pool.index[pool["n_leviers"] == k])
        rng.shuffle(idx)
        for _ in range(q[k]):
            best, best_score = None, None
            for i in idx:
                if i in chosen or per_coll[pool.at[i, "collectivite_id"]] >= MAX_PAR_COLLECTIVITE:
                    continue
                # Score : leviers peu vus d'abord, puis collectivités peu vues.
                levs = list(pool.at[i, "haiku"])
                score = (sum(lev_count[l] for l in levs) / max(len(levs), 1), per_coll[pool.at[i, "collectivite_id"]])
                if best_score is None or score < best_score:
                    best, best_score = i, score
            if best is None:
                break
            chosen.append(best)
            per_coll[pool.at[best, "collectivite_id"]] += 1
            lev_count.update(list(pool.at[best, "haiku"]))  # les clés (leviers), pas les catégories
    out = pool.loc[chosen].copy()
    out["ordre_aleatoire"] = [rng.random() for _ in range(len(out))]
    return out.sort_values("ordre_aleatoire").drop(columns="ordre_aleatoire").reset_index(drop=True), q


def fetch_contextes(ids: list[int]) -> dict[int, str]:
    engine = engine_prod_readonly(load_secrets())
    out: dict[int, str] = {}
    for cid in ids:
        out.update(v2.fetch_contexte_axes(engine, cid))
    return out


def leviers_list(classif: dict[str, list[int]]) -> list[tuple[str, str]]:
    """[(libellé v2, "1, 3"), …] dans l'ordre des codes."""
    items = []
    for v1_label, cats in classif.items():
        code = V1_LABEL_TO_CODE[v1_label]
        items.append((LABEL_V2[code], ", ".join(str(c) for c in sorted(cats))))
    return sorted(items)


# ---------------------------------------------------------------- Excel

FONT = "Arial"
HEADER_FILL = PatternFill("solid", start_color="1F3864")
INPUT_FILL = PatternFill("solid", start_color="FFF2CC")
HAIKU_FILL = PatternFill("solid", start_color="F2F2F2")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def style_header(ws, row: int, ncols: int) -> None:
    for col in range(1, ncols + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = Font(name=FONT, bold=True, color="FFFFFF")
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = BORDER


def write_excel(
    df: pd.DataFrame,
    pool: pd.DataFrame,
    q: dict[int, int],
    ctx: dict[int, str],
    path: Path,
    prefill_note: str = "Pré-remplissage : vote majoritaire de Claude Haiku 5.5 sur 3 runs "
    "(prompt prompts/classification_volet_ges_v2.md, une fiche par appel).",
) -> None:
    wb = Workbook()

    # --- Mode d'emploi
    ws0 = wb.active
    ws0.title = "Mode d'emploi"
    lines = [
        ("Dataset de test — classification volet GES", True),
        ("", False),
        (f"{len(df)} fiches tirées parmi {len(pool)} fiches qui ont un titre et une description "
         f"(≥ {MIN_DESCRIPTION} caractères), dans {pool['collectivite_id'].nunique()} collectivités.", False),
        (prefill_note, False),
        ("", False),
        ("Ce qu'il faut faire (onglet « Fiches », cellules sur fond jaune)", True),
        ("1. Lire le titre, la description et le contexte.", False),
        ("2. Corriger les colonnes Levier 1 à 3 (liste déroulante) et Catégories 1 à 3.", False),
        ("   Catégories : entiers de 1 à 6 séparés par une virgule, par exemple « 1, 3 ».", False),
        ("   Aucun levier : laisser les colonnes Levier vides.", False),
        ("3. Mettre le statut : « Validé tel quel » ou « Corrigé ».", False),
        ("4. Noter si besoin un commentaire (règle discutable, fiche ambiguë…).", False),
        ("", False),
        ("Exemple de ligne remplie : Levier 1 = Vélo et transport en commun · Catégories 1 = 1, 3 · "
         "Levier 2 = (vide) · Statut = Corrigé.", False),
        ("", False),
        ("Ne pas modifier l'onglet « Haiku (brut) » : il sert à mesurer la précision de Haiku après correction.", False),
        ("Colonne « Haiku stable 3/3 » : Oui si les 3 runs de Haiku ont donné exactement la même réponse.", False),
        ("", False),
        ("Catégories", True),
    ]
    lines += [(f"{k} — {v}", False) for k, v in CATEGORIES.items()]
    lines += [("", False), ("Répartition du nombre de leviers (vote Haiku)", True)]
    for row_i, (txt, bold) in enumerate(lines, start=1):
        c = ws0.cell(row=row_i, column=1, value=txt)
        c.font = Font(name=FONT, bold=bold, size=12 if row_i == 1 else 10)
    r0 = len(lines) + 1
    for col, h in enumerate(["Nombre de leviers", "Vivier (fiches)", "Vivier (%)", "Dataset (fiches)"], start=1):
        ws0.cell(row=r0, column=col, value=h)
    style_header(ws0, r0, 4)
    dist = pool["n_leviers"].value_counts().sort_index()
    for i, (k, v) in enumerate(dist.items(), start=1):
        vals = [k, int(v), v / dist.sum(), int((df["n_leviers"] == k).sum())]
        for col, val in enumerate(vals, start=1):
            c = ws0.cell(row=r0 + i, column=col, value=val)
            c.font = Font(name=FONT)
            c.border = BORDER
            if col == 3:
                c.number_format = "0%"
    ws0.column_dimensions["A"].width = 110
    for col in "BCD":
        ws0.column_dimensions[col].width = 16

    # --- Fiches
    ws = wb.create_sheet("Fiches")
    headers = [
        "N°", "Collectivité", "Id collectivité", "Id fiche", "Contexte (plan > axe)", "Titre", "Description",
        "Haiku stable 3/3",
        "Levier 1", "Catégories 1", "Levier 2", "Catégories 2", "Levier 3", "Catégories 3",
        "Statut", "Commentaire",
    ]
    widths = [5, 22, 10, 10, 30, 40, 80, 9, 34, 11, 34, 11, 34, 11, 16, 40]
    for col, h in enumerate(headers, start=1):
        ws.cell(row=1, column=col, value=h)
        ws.column_dimensions[get_column_letter(col)].width = widths[col - 1]
    style_header(ws, 1, len(headers))
    ws.row_dimensions[1].height = 32
    for i, row in df.iterrows():
        r = i + 2
        levs = leviers_list(row["haiku"])
        desc = row["description"]
        if len(desc) > 32000:
            desc = desc[:32000] + " […]"
        vals = [
            i + 1, row["collectivite"], row["collectivite_id"], row["fiche_id"],
            ctx.get(row["fiche_id"], "non renseigné"), row["titre"], desc,
            "Oui" if row["stable"] else "Non",
        ]
        for j in range(3):
            vals += list(levs[j]) if j < len(levs) else [None, None]
        vals += ["À vérifier", None]
        for col, val in enumerate(vals, start=1):
            c = ws.cell(row=r, column=col, value=val)
            c.font = Font(name=FONT, size=10)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = BORDER
            if 9 <= col <= 16:
                c.fill = INPUT_FILL
            if col in (10, 12, 14):
                c.number_format = "@"
        ws.row_dimensions[r].height = 120
    ws.freeze_panes = "G2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(df) + 1}"
    last = len(df) + 1
    dv_lev = DataValidation(type="list", formula1=f"'Référentiel leviers'!$B$2:$B${len(LABEL_V2) + 1}", allow_blank=True)
    dv_lev.error = "Choisir un levier de la liste (onglet « Référentiel leviers »)."
    dv_stat = DataValidation(type="list", formula1='"À vérifier,Validé tel quel,Corrigé"', allow_blank=False)
    ws.add_data_validation(dv_lev)
    ws.add_data_validation(dv_stat)
    for col in ("I", "K", "M"):
        dv_lev.add(f"{col}2:{col}{last}")
    dv_stat.add(f"O2:O{last}")

    # --- Haiku (brut)
    wr = wb.create_sheet("Haiku (brut)")
    hb = ["Id fiche", "Vote majoritaire (codes)", "Run 1", "Run 2", "Run 3"]
    for col, h in enumerate(hb, start=1):
        wr.cell(row=1, column=col, value=h)
    style_header(wr, 1, len(hb))

    def fmt_codes(classif: dict[str, list[int]]) -> str:
        if not classif:
            return "(aucun levier)"
        return " | ".join(
            f"{V1_LABEL_TO_CODE[l]} [{', '.join(str(c) for c in sorted(cats))}]" for l, cats in sorted(classif.items())
        )

    for i, row in df.iterrows():
        vals = [row["fiche_id"], fmt_codes(row["haiku"])] + [fmt_codes(x) for x in row["runs"]]
        for col, val in enumerate(vals, start=1):
            c = wr.cell(row=i + 2, column=col, value=val)
            c.font = Font(name=FONT, size=10)
            c.alignment = Alignment(wrap_text=True, vertical="top")
    for col, w in zip("ABCDE", [10, 60, 50, 50, 50]):
        wr.column_dimensions[col].width = w

    # --- Référentiel leviers
    wl = wb.create_sheet("Référentiel leviers")
    for col, h in enumerate(["Code", "Libellé"], start=1):
        wl.cell(row=1, column=col, value=h)
    style_header(wl, 1, 2)
    for i, (code, label) in enumerate(LABEL_V2.items(), start=2):
        wl.cell(row=i, column=1, value=code).font = Font(name=FONT, size=10)
        wl.cell(row=i, column=2, value=label).font = Font(name=FONT, size=10)
    wl.column_dimensions["A"].width = 48
    wl.column_dimensions["B"].width = 58

    wb.move_sheet("Fiches", offset=-1)
    wb.active = wb.sheetnames.index("Fiches")
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def main() -> int:
    pool = load_pool()
    df, q = sample(pool)
    ctx = fetch_contextes(sorted(df["collectivite_id"].unique()))
    path = OUT_DIR / f"dataset_test_{len(df)}_fiches.xlsx"
    write_excel(df, pool, q, ctx, path)
    df.drop(columns=["runs"]).assign(haiku=df["haiku"].map(str)).to_csv(
        OUT_DIR / f"dataset_test_{len(df)}_fiches.csv", index=False, encoding="utf-8-sig"
    )
    print("Vivier :", len(pool), "fiches —", pool["n_leviers"].value_counts().sort_index().to_dict())
    print("Quotas :", q, "— tirées :", df["n_leviers"].value_counts().sort_index().to_dict())
    print("Par collectivité :", df["collectivite_id"].value_counts().to_dict())
    print("Leviers couverts :", len({l for h in df["haiku"] for l in h}), "/ 29")
    print("Fichier :", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
