from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/Florian_Senger_Business_Card_Print.pdf"

with open(ROOT / "content/card.yml", encoding="utf-8") as f:
    d = yaml.safe_load(f)

# Finished size 85 x 55 mm + 3 mm bleed on every side
BLEED = 3 * mm
TRIM_W = 85 * mm
TRIM_H = 55 * mm
PAGE_W = TRIM_W + 2 * BLEED
PAGE_H = TRIM_H + 2 * BLEED

BLUE = HexColor("#15579d")
DARK = HexColor("#22282f")
MUTED = HexColor("#626b75")
PALE = HexColor("#f2f6fa")

CARD_URL = "https://florian1senger1-maker.github.io/business-card/"

def dots(c):
    """Restrained dotted background echoing the electronic card."""
    c.saveState()
    c.setFillColor(HexColor("#d7e4f2"))

    x0 = PAGE_W - 28 * mm
    y0 = PAGE_H - 4 * mm

    for row in range(22):
        for col in range(16):
            x = x0 + col * 2.2 * mm
            y = y0 - row * 2.2 * mm

            # Curved / tapering field rather than a rectangle
            boundary = 5 + int(row * 0.42)
            if col >= boundary:
                c.circle(x, y, 0.30 * mm, fill=1, stroke=0)

    c.restoreState()

def front(c):
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    dots(c)

    left = BLEED + 5 * mm
    top = PAGE_H - BLEED - 6 * mm

    c.setFillColor(BLUE)
    c.rect(left, top - 24 * mm, 0.7 * mm, 24 * mm, fill=1, stroke=0)

    x = left + 4 * mm

    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(x, top - 3 * mm, d["name"].upper())

    c.setFillColor(DARK)
    c.setFont("Helvetica", 8.5)
    c.drawString(x, top - 9 * mm, d["title"])

    c.setFillColor(BLUE)
    c.rect(x, top - 14 * mm, 13 * mm, 0.55 * mm, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 5.7)
    c.drawString(x, top - 18 * mm, "DECISION SUPPORT  |  ANALYTICS  |  AUTOMATION")

    c.setFillColor(DARK)
    c.setFont("Helvetica-Oblique", 6.3)
    c.drawString(x, top - 22.5 * mm,
                 "Helping organisations make better decisions using data.")

    # Contact strip
    band_y = BLEED + 8 * mm
    c.setFillColor(PALE)
    c.roundRect(left, band_y, TRIM_W - 10 * mm, 10 * mm,
                2 * mm, fill=1, stroke=0)

    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 5.5)
    c.drawString(x, band_y + 6.2 * mm, "EMAIL")
    c.drawString(x + 39 * mm, band_y + 6.2 * mm, "PHONE")

    c.setFillColor(DARK)
    c.setFont("Helvetica", 6.2)
    c.drawString(x, band_y + 3.1 * mm, d["email"])
    c.drawString(x + 39 * mm, band_y + 3.1 * mm, d["phone"])

    c.showPage()

def back(c):
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    dots(c)

    # Blue accent
    c.setFillColor(BLUE)
    c.rect(BLEED + 5 * mm, BLEED + 5 * mm,
           0.7 * mm, TRIM_H - 10 * mm, fill=1, stroke=0)

    # QR - vector, no rasterisation
    qr_code = qr.QrCodeWidget(CARD_URL)
    bounds = qr_code.getBounds()
    qr_size = 30 * mm
    scale = qr_size / (bounds[2] - bounds[0])

    drawing = Drawing(qr_size, qr_size,
                      transform=[scale, 0, 0, scale, 0, 0])
    drawing.add(qr_code)

    qr_x = BLEED + 11 * mm
    qr_y = BLEED + (TRIM_H - 30 * mm) / 2
    renderPDF.draw(drawing, c, qr_x, qr_y)

    text_x = qr_x + 35 * mm
    centre_y = PAGE_H / 2

    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(text_x, centre_y + 8 * mm, "SCAN TO CONNECT")

    c.setFillColor(DARK)
    c.setFont("Helvetica", 6.5)
    c.drawString(text_x, centre_y + 3 * mm, "Email  |  Phone  |  LinkedIn")

    c.setFont("Helvetica", 6.5)
    c.drawString(text_x, centre_y, "Business Problem Evaluation Framework")

    c.setFillColor(BLUE)
    c.rect(text_x, centre_y - 5 * mm, 12 * mm, 0.55 * mm,
           fill=1, stroke=0)

    c.setFillColor(DARK)
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(text_x, centre_y - 10 * mm,
                 "Start with the problem,")
    c.drawString(text_x, centre_y - 14 * mm,
                 "not the technology.")

    c.showPage()

OUT.parent.mkdir(exist_ok=True)

c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
c.setTitle("Florian Senger - Business Card - Print")
c.setAuthor("Florian Senger")

front(c)
back(c)
c.save()

print(OUT)
