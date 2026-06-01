"""Assemblage PDF pour l'export synthèse priorisation."""

from __future__ import annotations

import base64
import re
from io import BytesIO
from typing import Any

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas

PAGE_SIZE = landscape(A4)
MARGIN = 40
TITLE_Y = PAGE_SIZE[1] - 40
CONTENT_TOP = PAGE_SIZE[1] - 75
CONTENT_BOTTOM = MARGIN
LINE_HEIGHT = 14
BODY_SIZE = 10
HEADING_SIZE = 11


def _decode_data_url(data_url: str) -> bytes:
    payload = data_url.split(",", 1)[-1]
    return base64.b64decode(payload)


def sanitize_filename(name: str) -> str:
    safe = re.sub(r"[^\w\-]+", "_", name.strip(), flags=re.UNICODE)
    return safe.strip("_") or "collectivite"


def _new_canvas() -> tuple[canvas.Canvas, BytesIO]:
    buffer = BytesIO()
    return canvas.Canvas(buffer, pagesize=PAGE_SIZE), buffer


def _draw_page_title(c: canvas.Canvas, title: str) -> None:
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, TITLE_Y, title)


def _draw_image_page(c: canvas.Canvas, title: str, png_data_url: str | None) -> None:
    _draw_page_title(c, title)
    if not png_data_url:
        _draw_wrapped(
            c,
            "Graphique non disponible pour cette collectivité.",
            MARGIN,
            CONTENT_TOP,
            PAGE_SIZE[0] - 2 * MARGIN,
        )
        return
    img = ImageReader(BytesIO(_decode_data_url(png_data_url)))
    img_w, img_h = img.getSize()
    page_w, page_h = PAGE_SIZE
    avail_w = page_w - 2 * MARGIN
    avail_h = CONTENT_TOP - CONTENT_BOTTOM
    scale = min(avail_w / img_w, avail_h / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    draw_x = MARGIN + (avail_w - draw_w) / 2
    draw_y = CONTENT_BOTTOM + (avail_h - draw_h) / 2
    c.drawImage(img, draw_x, draw_y, width=draw_w, height=draw_h)


def _draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    max_width: float,
    *,
    font: str = "Helvetica",
    size: int = BODY_SIZE,
    leading: int = LINE_HEIGHT,
) -> float:
    c.setFont(font, size)
    for line in simpleSplit(text, font, size, max_width):
        if y < CONTENT_BOTTOM:
            c.showPage()
            y = CONTENT_TOP
        c.drawString(x, y, line)
        y -= leading
    return y


def _draw_faisabilite_page(
    c: canvas.Canvas,
    collectivite_nom: str,
    top_leviers: list[dict[str, Any]],
) -> None:
    _draw_page_title(
        c,
        f"Top 10 leviers sous-mobilisés — {collectivite_nom}",
    )
    y = CONTENT_TOP
    page_w, _ = PAGE_SIZE
    max_width = page_w - 2 * MARGIN

    if not top_leviers:
        y = _draw_wrapped(
            c,
            "Aucun angle mort identifié pour cette collectivité.",
            MARGIN,
            y,
            max_width,
        )
        return

    y = _draw_wrapped(
        c,
        "Arbitrages enregistrés à l'étape « Faisabilité politique » :",
        MARGIN,
        y,
        max_width,
        font="Helvetica-Bold",
        size=HEADING_SIZE,
    )
    y -= 4

    for entry in top_leviers:
        header = (
            f"{entry['rank']}. {entry['levier']} "
            f"— potentiel non mobilisé : {entry['potentiel']:.0f} ktCO₂e"
        )
        if y < CONTENT_BOTTOM + 3 * LINE_HEIGHT:
            c.showPage()
            y = CONTENT_TOP
        y = _draw_wrapped(
            c, header, MARGIN, y, max_width, font="Helvetica-Bold", size=HEADING_SIZE
        )
        for cat_entry in entry["categories"]:
            line = f"    · {cat_entry['categorie']} : {cat_entry['faisabilite']}"
            y = _draw_wrapped(c, line, MARGIN, y, max_width)
        y -= 6


def _draw_cibles_page(
    c: canvas.Canvas,
    collectivite_nom: str,
    n_cibles: int,
    n_actions: int,
    cibles_par_levier: dict[str, list[str]],
) -> None:
    _draw_page_title(c, f"Cibles priorisées — {collectivite_nom}")
    y = CONTENT_TOP
    page_w, _ = PAGE_SIZE
    max_width = page_w - 2 * MARGIN

    y = _draw_wrapped(
        c,
        f"Nombre de cibles priorisées : {n_cibles}",
        MARGIN,
        y,
        max_width,
        font="Helvetica-Bold",
        size=HEADING_SIZE,
    )
    y = _draw_wrapped(
        c,
        f"Nombre d'actions retenues : {n_actions}",
        MARGIN,
        y,
        max_width,
        font="Helvetica-Bold",
        size=HEADING_SIZE,
    )
    y -= 8
    y = _draw_wrapped(
        c,
        "Liste des cibles priorisées, classées par levier :",
        MARGIN,
        y,
        max_width,
        font="Helvetica-Bold",
        size=HEADING_SIZE,
    )
    y -= 4

    if not cibles_par_levier:
        _draw_wrapped(
            c,
            "Aucune cible priorisée enregistrée.",
            MARGIN,
            y,
            max_width,
        )
        return

    for levier, categories in cibles_par_levier.items():
        if y < CONTENT_BOTTOM + 2 * LINE_HEIGHT:
            c.showPage()
            y = CONTENT_TOP
        y = _draw_wrapped(
            c, levier, MARGIN, y, max_width, font="Helvetica-Bold", size=HEADING_SIZE
        )
        for categorie in categories:
            y = _draw_wrapped(c, f"    · {categorie}", MARGIN, y, max_width)
        y -= 4


def build_cibles_par_levier(df_actions) -> dict[str, list[str]]:
    """Cibles priorisées groupées par levier (tri alphabétique)."""
    from utils.priorisation_impact_charts import CATEGORIES

    grouped: dict[str, list[str]] = {}
    if df_actions is None or df_actions.empty:
        return grouped
    pairs = df_actions[["levier", "categorie"]].drop_duplicates()
    for _, row in pairs.iterrows():
        levier = row["levier"]
        categorie = CATEGORIES[int(row["categorie"])]
        grouped.setdefault(levier, []).append(categorie)
    for levier in grouped:
        grouped[levier] = sorted(set(grouped[levier]))
    return dict(sorted(grouped.items()))


def build_compte_rendu_pdf(
    collectivite_nom: str,
    *,
    diagnostic_bar_png: str | None,
    diagnostic_treemap_png: str | None,
    top_leviers_faisabilite: list[dict[str, Any]],
    n_cibles_priorisees: int,
    n_actions_retenues: int,
    cibles_par_levier: dict[str, list[str]],
    synthese_treemap_png: str | None,
    synthese_bar_png: str | None,
    threshold_pct: int,
) -> bytes:
    """Assemble le compte rendu PDF 6 pages A4 paysage."""
    c, buffer = _new_canvas()

    _draw_image_page(
        c,
        f"Impact Chart — diagnostic ({threshold_pct} %) — {collectivite_nom}",
        diagnostic_bar_png,
    )
    c.showPage()

    _draw_image_page(
        c,
        f"Impact Map — diagnostic ({threshold_pct} %) — {collectivite_nom}",
        diagnostic_treemap_png,
    )
    c.showPage()

    _draw_faisabilite_page(c, collectivite_nom, top_leviers_faisabilite)
    c.showPage()

    _draw_cibles_page(
        c,
        collectivite_nom,
        n_cibles_priorisees,
        n_actions_retenues,
        cibles_par_levier,
    )
    c.showPage()

    _draw_image_page(
        c,
        f"Impact Map — synthèse (actions retenues) — {collectivite_nom}",
        synthese_treemap_png,
    )
    c.showPage()

    _draw_image_page(
        c,
        f"Impact Chart — synthèse (actions retenues) — {collectivite_nom}",
        synthese_bar_png,
    )

    c.save()
    return buffer.getvalue()


def build_synthese_pdf(collectivite_nom: str, treemap_png_b64: str) -> bytes:
    """Rétrocompatibilité : PDF 1 page treemap uniquement."""
    c, buffer = _new_canvas()
    _draw_image_page(c, f"Synthèse — {collectivite_nom}", treemap_png_b64)
    c.save()
    return buffer.getvalue()
