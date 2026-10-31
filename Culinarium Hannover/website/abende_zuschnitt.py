#!/usr/bin/env python3
"""Culinarium · Story-Bilder der Abende sauber zuschneiden (Robert 27.10.2026: «keine Instagram-Namen, keine leeren Bereiche oben und unten»).
Erst den Rahmen der Story weg (Fotofläche wird erkannt), dann je Bild der Streifen mit Namen, Handles oder Schrift.
Werte: Anteil der Fotofläche, der oben, unten, links, rechts wegfällt. Ergebnis in _quelle/extern/ig-zuschnitt-2/.
Aufruf: python3 website/abende_zuschnitt.py"""
import os
import numpy as np
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
Q = os.path.join(HIER, '..', '_quelle/extern/')
ZIEL = os.path.join(Q, 'ig-zuschnitt-2')

# Datei: (oben, unten, links, rechts)
SCHNITT = {
    'ig-highlights/2023-09-22_highlight-3094-02.jpg': (0, .32, 0, 0),     # Schrift rechts unten
    'ig-highlights/2023-09-22_highlight-3094-03.jpg': (.07, .32, 0, 0),   # Name oben, Hashtags unten
    'ig-highlights/2023-10-21_highlight-3138-02.jpg': (.07, .14, 0, 0),   # Name oben, «Momo zaubert wieder!» unten
    'ig-highlights/2023-10-21_highlight-3138-03.jpg': (.07, .22, 0, 0),   # Name oben, Schrift unter dem Teller
    'ig-highlights/2023-10-21_highlight-3138-05.jpg': (.06, 0, 0, 0),     # Name oben
    'ig-highlights/2023-11-18_highlight-0707-02.jpg': (.06, .20, 0, 0),   # Name oben, Handles unten
    'ig/2024-01-29_culinarium_hannover_C2sFkpSscHP-1.jpg': (0, 0, 0, 0),  # nur der Rand
    'ig-highlights/2024-04-27_highlight-8299-03.jpg': (.34, 0, 0, 0),     # Name und Handles oben
    'ig-highlights/2024-04-29_highlight-8299-05.jpg': (.08, .06, 0, 0),   # Name oben, Handle unten
    'ig-highlights/2024-07-20_highlight-4589-03.jpg': (.09, .12, 0, 0),   # Handle und Zeichen unten
    'ig-highlights/2025-02-22_highlight-4865-02.jpg': (0, .16, 0, 0),     # Schrift unten
    'ig-highlights/2025-06-15_highlight-6684-07.jpg': (.07, .10, 0, 0),   # Name oben, Handles unten
    'ig-highlights/2025-06-15_highlight-6684-09.jpg': (.14, .06, .06, .06),  # grauer Rand mit Name
    'ig-highlights/2025-06-15_highlight-6684-10.jpg': (.52, .07, 0, 0),   # Name oben, Schrift in der Mitte
    'ig-highlights/2025-06-15_highlight-6684-11.jpg': (.07, .02, 0, 0),   # Name oben
    'ig-highlights/2025-06-15_highlight-6684-12.jpg': (.07, .02, 0, 0),   # Name oben
}


def flaeche(im):
    """Fotofläche einer Story: Zeilen mit Struktur, dann Spalten, die sich vom Hintergrund abheben."""
    g = np.asarray(im.convert('L'), dtype=float)
    zeilen = np.where(g.std(axis=1) > 18)[0]
    if not len(zeilen):
        return 0, 0, im.width, im.height
    t, b = zeilen[0], zeilen[-1]
    sub = g[t:b]
    spalten = np.where(np.abs(sub - sub[:, :3].mean(axis=1, keepdims=True)).mean(axis=0) > 14)[0]
    l, r = (spalten[0], spalten[-1]) if len(spalten) else (0, im.width)
    return int(l), int(t), int(r), int(b)


def main():
    os.makedirs(ZIEL, exist_ok=True)
    for datei, (o, u, li, re_) in SCHNITT.items():
        im = Image.open(os.path.join(Q, datei)).convert('RGB')
        l, t, r, b = flaeche(im)
        w, h = r - l, b - t
        box = (l + int(w * li), t + int(h * o), r - int(w * re_), b - int(h * u))
        im.crop(box).save(os.path.join(ZIEL, os.path.basename(datei)), quality=92)
        print(os.path.basename(datei), box)


if __name__ == '__main__':
    main()
