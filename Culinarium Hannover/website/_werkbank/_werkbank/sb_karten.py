#!/usr/bin/env python3
"""Werkbank Culinarium, Kapitel IV «Karten und Unterlagen»: die Karten von La Carte neben der Karte, wie sie heute auf dem Tisch lag (Werkbank-Chat 28.10.2026).
Culinarium hat keine Speisekarte, sondern zu jedem Abend eine gedruckte Karte am Platz. La Carte (Chat culinarium-carte, Lieferung 28.10.2026) setzt sie neu;
die PDFs kommen aus _werkzeuge/carte/pruef/aus/abend-<datum>.pdf (feste Schriften, kein Type 3). «Heute» ist das Foto der gedruckten Karte, nur wo es eines
aus dem eigenen Profil gibt (keine Story mit Gäste-Namen im Bild): September 2023 (Beitrag CxQg56AItz6) und Februar 2025 (Highlight vom 22.02.2025).
   python3 _werkbank/sb_karten.py  → unterlagen/pdf/<ziel>.pdf, _werkbank/heute/<ziel>.pdf, _werkbank/unterlagen.json (danach Kit unterlagen.py)"""
import json, os, shutil
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PROJ = os.path.dirname(os.path.dirname(ROOT))
CARTE = os.path.join(PROJ, '_werkzeuge', 'carte', 'pruef', 'aus')
KARTEN = [  # Ziel, Abend (La Carte), Name, Foto der gedruckten Karte
    ('abend-2025-02-21', 'abend-2025-02-21', 'Februar 2025', '_quelle/extern/ig-highlights/2025-02-22_highlight-4865-06.jpg'),
    ('abend-2023-09-15', 'abend-2023-09-15', 'September 2023', '_quelle/extern/ig/2023-09-16_culinarium_hannover_CxQg56AItz6-2.jpg'),
]


def bau():
    os.makedirs(os.path.join(ROOT, 'unterlagen', 'pdf'), exist_ok=True); os.makedirs(os.path.join(W, 'heute'), exist_ok=True)
    plan = []
    for ziel, quelle, name, foto in KARTEN:
        q = os.path.join(CARTE, quelle + '.pdf')
        if not os.path.exists(q):
            print('fehlt', q); continue
        shutil.copy2(q, os.path.join(ROOT, 'unterlagen', 'pdf', ziel + '.pdf'))
        h = os.path.join(W, 'heute', ziel + '.pdf')
        Image.open(os.path.join(PROJ, foto)).convert('RGB').save(h, 'PDF', resolution=150)
        plan.append(dict(ziel=ziel, quelle=os.path.relpath(h, ROOT), name='Karte ' + name, gruppe='Die Abende', seiten=0, b=210, h=297, dazu='', fehlt=''))
    json.dump(plan, open(os.path.join(W, 'unterlagen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Karten:', ', '.join(p['ziel'] for p in plan))


if __name__ == '__main__':
    bau()
