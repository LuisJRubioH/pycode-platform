"""
Render del certificado a PDF con reportlab.

Función pura `render_certificate_pdf(...) -> bytes`: dado el nombre del
destinatario, el título del track, la fecha de emisión y el código de
verificación, devuelve los bytes de un PDF A4 apaisado listo para descargar.

No toca la base de datos ni el request — recibe datos planos para que sea
fácil de testear y reutilizar por Track.
"""

from datetime import datetime
from io import BytesIO

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# Paleta alineada con el frontend (primary/emerald de Tailwind).
_INK = HexColor("#0f172a")  # slate-900
_MUTED = HexColor("#475569")  # slate-600
_ACCENT = HexColor("#4f46e5")  # indigo-600
_GOLD = HexColor("#d97706")  # amber-600

_MONTHS_ES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


def _format_date_es(value: datetime) -> str:
    """`26 de mayo de 2026` sin depender del locale del sistema."""
    return f"{value.day} de {_MONTHS_ES[value.month - 1]} de {value.year}"


def render_certificate_pdf(
    *,
    recipient_name: str,
    track_title: str,
    issued_at: datetime,
    verification_code: str,
    verify_url: str,
) -> bytes:
    """Genera el PDF del certificado y devuelve sus bytes."""
    buffer = BytesIO()
    page_w, page_h = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    c.setTitle(f"Certificado PyCode — {recipient_name}")
    c.setAuthor("PyCode Platform")

    cx = page_w / 2

    # Marco decorativo doble.
    c.setStrokeColor(_ACCENT)
    c.setLineWidth(3)
    c.rect(12 * mm, 12 * mm, page_w - 24 * mm, page_h - 24 * mm)
    c.setStrokeColor(_GOLD)
    c.setLineWidth(1)
    c.rect(16 * mm, 16 * mm, page_w - 32 * mm, page_h - 32 * mm)

    # Marca de la plataforma.
    c.setFillColor(_ACCENT)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(cx, page_h - 34 * mm, "PyCode Platform")

    # Título del certificado.
    c.setFillColor(_INK)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(cx, page_h - 58 * mm, "Certificado de finalización")

    # Subtítulo "Se otorga a".
    c.setFillColor(_MUTED)
    c.setFont("Helvetica", 14)
    c.drawCentredString(cx, page_h - 78 * mm, "Se otorga a")

    # Nombre del destinatario.
    c.setFillColor(_INK)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(cx, page_h - 96 * mm, recipient_name)

    # Línea bajo el nombre.
    c.setStrokeColor(_GOLD)
    c.setLineWidth(1)
    c.line(cx - 80 * mm, page_h - 100 * mm, cx + 80 * mm, page_h - 100 * mm)

    # Cuerpo.
    c.setFillColor(_MUTED)
    c.setFont("Helvetica", 14)
    c.drawCentredString(
        cx,
        page_h - 114 * mm,
        "por completar satisfactoriamente el proyecto capstone del",
    )
    c.setFillColor(_ACCENT)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(cx, page_h - 126 * mm, track_title)

    # Pie: fecha (izquierda) y verificación (derecha).
    c.setFillColor(_MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(30 * mm, 30 * mm, f"Emitido el {_format_date_es(issued_at)}")

    c.drawRightString(page_w - 30 * mm, 34 * mm, f"Código: {verification_code}")
    c.setFont("Helvetica", 8)
    c.drawRightString(page_w - 30 * mm, 28 * mm, f"Verifica en {verify_url}")

    c.showPage()
    c.save()
    return buffer.getvalue()
