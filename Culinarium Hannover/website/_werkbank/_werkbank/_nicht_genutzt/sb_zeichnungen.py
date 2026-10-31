#!/usr/bin/env python3
"""Die Zeichnungen der Speisekarte des Hauses als saubere Linien (Station 10, 19.10.2026).
   python3 _werkbank/sb_zeichnungen.py   →  _werkbank/sb/{frankreich,italien,iberien,blatt}.svg
   Quelle: die Bilder in ../_quelle/website/pdf/Speisekarte-Oktober.pdf (pdfimages): drei Länderumrisse und das Blatt-Ornament zwischen
   zwei Linien. Nichts ist neu gezeichnet; potrace zieht die Linien des Hauses nach, damit sie im Druck scharf bleiben und die Farbe
   der Seite annehmen (currentColor)."""
import os, re, subprocess, tempfile
import numpy as np
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HIER, '..', '..', '_quelle', 'website', 'pdf', 'Speisekarte-Oktober.pdf')
ZIEL = os.path.join(HIER, 'sb'); os.makedirs(ZIEL, exist_ok=True)


def nachziehen(maske, name, mal=3, grau=None):
    """maske: True = Linie (oder grau: Graubild, dunkel = Linie, wird weich vergrössert und erst dann geschwellt)."""
    from PIL import ImageFilter
    m = Image.fromarray(grau) if grau is not None else Image.fromarray((~maske * 255).astype('uint8')).convert('L')
    m = m.resize((m.width * mal, m.height * mal), Image.BICUBIC)
    if grau is not None:
        m = m.filter(ImageFilter.GaussianBlur(mal * .6))
    m = m.point(lambda v: 0 if v < (205 if grau is not None else 170) else 255).convert('1')
    with tempfile.TemporaryDirectory() as t:
        pbm = os.path.join(t, 'a.pbm'); m.save(pbm)
        svg = subprocess.run(['potrace', pbm, '-s', '-o', '-', '--turdsize', '8', '--alphamax', '1.1', '--opttolerance', '0.4'],
                             capture_output=True, text=True, check=True).stdout
    svg = re.sub(r'<\?xml.*?\?>|<!DOCTYPE.*?>|<metadata>.*?</metadata>', '', svg, flags=re.S)
    svg = svg.replace('fill="#000000"', 'fill="currentColor"')
    svg = re.sub(r'width="[^"]*pt" height="[^"]*pt"', '', svg, count=1)
    open(os.path.join(ZIEL, name + '.svg'), 'w').write(svg.strip())
    print(name, m.size)


with tempfile.TemporaryDirectory() as t:
    subprocess.run(['pdfimages', '-png', PDF, os.path.join(t, 'b')], check=True)
    b = lambda n: np.array(Image.open(os.path.join(t, f'b-{n:03d}.png')).convert('L'))
    nachziehen(b(0) < 128, 'italien')            # schwarze Linie auf Weiss
    nachziehen(b(3) > 128, 'frankreich')         # Linie steckt in der Maske des Bildes (helle Stellen = sichtbar)
    nachziehen(b(5) < 128, 'iberien')
    orn = b(1)
    spalten = np.where((orn < 200).sum(0) > 20)[0]          # das Blatt steht in der Mitte, links und rechts die Doppellinie
    c = int(spalten.mean())
    nachziehen(None, 'blatt', mal=8, grau=orn[:, c - 34:c + 35])
