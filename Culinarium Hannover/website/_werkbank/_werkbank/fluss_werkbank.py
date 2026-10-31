#!/usr/bin/env python3
"""Baustein in der Werkbank Culinarium (Werkbank-Chat 28.10.2026), über das Schäfli kopiert; die Herkunft steht darunter wie in der Vorlage.
Werkbank Landgasthof Ruedihus, Flüssigkeit (12.10.2026, Regel 55): Nachlauf nach jedem Bau.

1. Bildstufen: Bilder, die grösser liegen als gezeigt (Vorher/Nachher 2880 px, Brief-Foto 2400 px, Laptop-Standbild 1800 px, die drei Fotos im
   Prüfbericht 1100 px), bekommen eine kleinere Stufe daneben (werkbank/eigen/<name>-s.webp, der Kit-Bau leert nur img/) und ein srcset.
   Rechner mit einfacher Dichte und Handys laden so die passende Grösse, hochauflösende Schirme weiter die grosse Datei.
2. Vorher/Nachher: das erste Bildpaar lag eager, obwohl der Abschnitt weit unter dem ersten Blick steht → lazy wie alle anderen.
Eingehängt in haus.py: anwenden() in nach_bau(). Mehrfach anwendbar."""
import os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
IMG, EIGEN = os.path.join(ROOT, 'werkbank', 'img'), os.path.join(ROOT, 'werkbank', 'eigen')
STUFEN = [   # Anfang des Namens, Breite der kleinen Stufe, sizes
    ('vh-', 1440, '(min-width:1000px) 62vw, 100vw'),
    ('bf-haus', 1300, '(min-width:1560px) 1480px, 94vw'),
    ('lap-schirm', 1000, '(min-width:1040px) 46vw, 76vw'),
    ('gt-', 560, '(min-width:1000px) 26vw, 46vw'),
    ('vi-familie', 800, '(min-width:700px) 640px, 92vw'),
]


def anwenden(pfad):
    from PIL import Image
    if not os.path.exists(pfad):
        return False
    t = alt = open(pfad, encoding='utf-8').read()
    os.makedirs(EIGEN, exist_ok=True)

    def stufe(m):
        tag, name = m.group(0), m.group(1)
        regel = next((r for r in STUFEN if name.startswith(r[0])), None)
        if not regel or 'srcset=' in tag:
            return tag
        q, z = os.path.join(IMG, name + '.webp'), os.path.join(EIGEN, name + '-s.webp')
        if not os.path.exists(q):
            return tag
        im = Image.open(q)
        if im.width <= regel[1] * 1.15:
            return tag
        if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(q):
            im.convert('RGB').resize((regel[1], round(im.height * regel[1] / im.width)), Image.LANCZOS).save(z, 'WEBP', quality=80, method=5)
        return tag.replace(f'src="img/{name}.webp"', f'src="img/{name}.webp" srcset="eigen/{name}-s.webp {regel[1]}w, img/{name}.webp {im.width}w" sizes="{regel[2]}"', 1)

    t = re.sub(r'<img src="img/([a-z0-9-]+)\.webp"[^>]*>', stufe, t)
    # Vorher/Nachher: auch das erste Paar lazy
    t = re.sub(r'(<img src="img/vh-[a-z0-9-]+\.webp"(?:(?! loading=)[^>])*?)( class="ld)', r'\1 loading="lazy" decoding="async"\2', t)
    if t != alt:
        open(pfad, 'w', encoding='utf-8').write(t)
    return t != alt
