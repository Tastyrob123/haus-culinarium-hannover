#!/usr/bin/env python3
"""Gutschein für beide Häuser aus der Werkstatt (Robert 21.10.2026: Fassung 3, hell und dunkel) in die Drucksachen der Werkbank legen.
Läuft in bau_alles.sh nach papier_druck.js/papier_seiten.py und vor material.py. Liest nur aus _werkzeuge/imprimerie/pruefung/drucksachen/."""
import os, subprocess, tempfile
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(W)
Q = os.path.join(os.path.dirname(ROOT), '_werkzeuge', 'imprimerie', 'pruefung', 'drucksachen')
PAAR = [('07-gutschein-005.pdf', 'gutschein'), ('08-gutschein-006.pdf', 'gutschein-r')]   # hell, dunkel


def main():
    quellen = [os.path.join(Q, q) for q, _ in PAAR]
    for q in quellen:
        if not os.path.exists(q):
            raise SystemExit(f'Gutschein der Werkstatt fehlt: {q}')
    with tempfile.TemporaryDirectory() as tmp:
        for q, name in PAAR:
            subprocess.run(['pdftoppm', '-r', '300', '-png', '-singlefile', os.path.join(Q, q), os.path.join(tmp, name)], check=True)
            im = Image.open(os.path.join(tmp, name + '.png')).convert('RGB')
            ziel = os.path.join(W, 'roh', 'papier', name + '.png')   # daraus macht papier_seiten.py die Bilder der Seite, bau.py die der Werkbank
            breite = Image.open(ziel).width if os.path.exists(ziel) else 2000
            im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS).save(ziel)
    subprocess.run(['pdfunite', *quellen, os.path.join(ROOT, 'drucksachen', 'pdf', 'taverne-zum-schaefli-gutschein.pdf')], check=True)
    print('Gutschein der Werkstatt übernommen (hell, dunkel)')


if __name__ == '__main__':
    main()
