#!/usr/bin/env python3
"""Werkbank Culinarium: Bilder in der Grösse, in der sie gezeigt werden (Abnahme-Tor 4, 30.10.2026: WebKit-Tab stürzte beim Durchklicken ab,
die Startseite hielt rund 130 Megapixel dekodiert). Gemessen in WebKit bei 1440 und 1000 (doppelte Dichte) und 390 (dreifache Dichte):
grösste angezeigte Breite je Bild, dazu etwas Luft. Am Rechner bleibt jedes Bild Pixel für Pixel gleich scharf.
Nur Bilder, die die Werkbank selbst baut oder aus dem Kit übernimmt; Feed und Beigaben-Seiten bleiben unberührt.
Läuft in haus.nach_bau zuletzt, wiederholbar (verkleinert nur, was breiter ist).   python3 _werkbank/bild_mass.py [<website/_werkbank>]"""
import glob, os, sys
from PIL import Image

MASS = {                          # Datei (Muster) unter werkbank/: grösste Breite in Pixeln
    'img/auftakt.webp': 1440,     # Fenster im Auftakt, gezeigt bis 637 px
    'img/ins-bild-*.webp': 1280,  # Werkzeug-Schirme, gezeigt bis 620 px
    'img/ins-geraet.webp': 1560,  # Gerät um die Schirme, gezeigt bis 769 px
    'img/ml-*.webp': 420,         # Mail-Abzüge im Fächer, gezeigt bis 133 px
    'img/sag-haus.webp': 1000,    # Haus im Vorschlag, gezeigt bis 481 px
    'img/pdf-*.webp': 560,        # PDF-Seiten im Vorschlag, gezeigt bis 266 px
}


def anwenden(root):
    n = 0
    for muster, breite in MASS.items():
        for f in glob.glob(os.path.join(root, 'werkbank', muster)):
            im = Image.open(f)
            if im.width <= breite:
                continue
            im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') else 'RGB')
            im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS).save(f, 'WEBP', quality=86, method=5)
            n += 1
    return n


if __name__ == '__main__':
    print('bild-mass:', anwenden(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Bilder')
