"""Assemblage PDF pour l'export Impact Map + Impact Chart."""

import base64
import re
from io import BytesIO

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def _decode_data_url(data_url: str) -> bytes:
    payload = data_url.split(",", 1)[-1]
    return base64.b64decode(payload)


def sanitize_filename(name: str) -> str:
    """Nom de fichier sûr à partir du nom de collectivité."""
    safe = re.sub(r"[^\w\-]+", "_", name.strip(), flags=re.UNICODE)
    return safe.strip("_") or "collectivite"


def build_priorisation_pdf(
    collectivite_nom: str,
    treemap_png_b64: str,
    bar_png_b64: str,
    threshold_pct: int,
) -> bytes:
    """Assemble un PDF 2 pages A4 paysage (treemap puis impact chart)."""
    buffer = BytesIO()
    page_size = landscape(A4)
    page_w, page_h = page_size
    margin = 40
    title_y = page_h - 40
    image_top = page_h - 70
    image_bottom = margin

    c = canvas.Canvas(buffer, pagesize=page_size)

    pages = [
        (f"Impact Map — {collectivite_nom}", treemap_png_b64),
        (
            f"Impact Chart ({threshold_pct} %) — {collectivite_nom}",
            bar_png_b64,
        ),
    ]

    for title, png_data_url in pages:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, title_y, title)

        img = ImageReader(BytesIO(_decode_data_url(png_data_url)))
        img_w, img_h = img.getSize()
        avail_w = page_w - 2 * margin
        avail_h = image_top - image_bottom
        scale = min(avail_w / img_w, avail_h / img_h)
        draw_w = img_w * scale
        draw_h = img_h * scale
        draw_x = margin + (avail_w - draw_w) / 2
        draw_y = image_bottom + (avail_h - draw_h) / 2

        c.drawImage(img, draw_x, draw_y, width=draw_w, height=draw_h)
        c.showPage()

    c.save()
    return buffer.getvalue()
