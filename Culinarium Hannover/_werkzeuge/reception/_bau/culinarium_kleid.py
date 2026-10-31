#!/usr/bin/env python3
"""Kleid von La Réception fürs Culinarium Hannover (28.10.2026): rechnet die Farben der Kopie aus dem Schäfli (Farbwelt «Riegel und Kalk»)
in die Farbwelt A «Plakat» des Culinarium um (Werte wie _werkzeuge/oberflaeche/kleid/culinarium.css, aus website/assets/culinarium.css):
  Ochsenblut (Farbton 0–12°, Sättigung bis 0,6), dunkel (Helligkeit bis 0,30)  → Nacht/Schiefer (Farbton 250°, #16151A · #1C1B21 · #3A3845), Helligkeit bleibt
  Ochsenblut, mittel (0,30 bis 0,46)                                          → Kerze tief (Farbton 16°, #B15736), Betonung auf Hell
  Schildgold (Farbton 28–40°, Helligkeit 0,45 bis 0,72)                         → Kerze (Farbton 16°, #EF7649), Helligkeit bleibt
  helles Gold (0,72 bis 0,82, Sättigung ab 0,36)                               → Kerze hell (#F5A689), Linien und Zeichen auf Dunkel
  Kalk (über 0,72)                                                             → Warmweiss (Farbton 10°, #FAF4F4 · #F3ECEA · #E9E0DE)
Grau, Grün (gespeichert) und Rot der Warnungen (Sättigung über 0,6) bleiben. Schriften: Petrona → Fraunces (weiche Enden, SOFT 100), Instrument Sans
und DM Mono bleiben, Dateien wie in website/assets/schrift/. Tapete aus website/assets/zeichen/.
Einmal angewendet am 28.10.2026 auf die frische Kopie aus dem Schäfli; erneut nur auf frische Kopien (sonst wird doppelt umgerechnet)."""
import colorsys, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATEIEN = ['studio/studio.css', 'studio/hell.css', 'studio/schweben.css', 'reception.css', 'culinarium-reception.css', 'gastgeber.css', 'brief-pdf.css',
           'brief-pdf.js', 'reception.js', 'studio/rundgang.js', 'studio/zur-werkbank.js', 'studio/auswahl.js', 'pruefung.html', 'anleitung.html',
           'index.html', 'brief-pdf.html', 'studio/anleitung.js', 'pruefung.js']


def neu_rgb(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hg = h * 360
    if hg <= 12 and 0.06 < s <= 0.6 and l <= 0.46:          # Ochsenblut
        if l <= 0.30:
            h2, s2 = 250 / 360, 0.11
        else:
            h2, s2 = 16 / 360, 0.52
    elif 28 <= hg <= 41 and s > 0.06:
        if 0.45 <= l <= 0.72:                               # Schildgold → Kerze
            h2, s2 = 16 / 360, min(max(s * 1.9, 0.45), 0.84)
        elif 0.72 < l <= 0.82 and s >= 0.36:                # helles Gold → Kerze hell
            h2, s2 = 16 / 360, 0.82
        elif l > 0.72:                                      # Kalk → Warmweiss
            h2, s2 = 10 / 360, min(s * 0.7, 0.3)
        else:
            return None
    else:
        return None
    r2, g2, b2 = colorsys.hls_to_rgb(h2, l, s2)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def hexe(m):
    t = m.group(1)
    if len(t) == 3:
        t = ''.join(c * 2 for c in t)
    x = neu_rgb(int(t[0:2], 16), int(t[2:4], 16), int(t[4:6], 16))
    return m.group(0) if x is None else '#%02x%02x%02x' % x


def rgba(m):
    x = neu_rgb(int(m.group(2)), int(m.group(3)), int(m.group(4)))
    return m.group(0) if x is None else f'{m.group(1)}({x[0]},{x[1]},{x[2]}{m.group(5)}'


def um(s):
    s = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F\w])', hexe, s)
    s = re.sub(r'(rgba?)\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(\s*[,)])', rgba, s)
    s = re.sub(r'%23([0-9a-fA-F]{6})', lambda m: '%23' + hexe(re.match(r'#(\w+)', '#' + m.group(1)))[1:], s)   # Farben in eingebetteten SVG
    # Schriften: Fraunces (variabel 100–900, weiche Enden) statt Petrona; nie fett
    s = re.sub(r"@font-face\{font-family:'Petrona';font-style:normal;font-weight:500 700;[^}]*\}\n?", '', s)
    s = s.replace('assets/schrift/Petrona-var.woff2', 'assets/schrift/fraunces-soft.woff2').replace('assets/schrift/InstrumentSans-normal-400_600.woff2', 'assets/schrift/instrument.woff2')
    s = s.replace('assets/schrift/DMMono-normal-400.woff2', 'assets/schrift/dmmono.woff2')
    s = s.replace("'Petrona'", "'Fraunces'").replace('"Petrona"', '"Fraunces"').replace('font-family:Petrona,', 'font-family:Fraunces,')
    s = s.replace('assets/zeichen/tapete-a-dunkel.svg', 'assets/zeichen/tapete-dunkel.svg')
    return s


if __name__ == '__main__':
    for d in sys.argv[1:] or DATEIEN:
        p = os.path.join(C, d)
        alt = open(p, encoding='utf-8').read()
        neu = um(alt)
        open(p, 'w', encoding='utf-8').write(neu)
        print(d, 'geändert' if neu != alt else 'gleich')
