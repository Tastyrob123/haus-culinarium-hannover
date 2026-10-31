#!/usr/bin/env python3
"""Werkbank Culinarium: letzter Farbgang (28.10.2026, Vorlage sb_farbe.py des Schäfli). Die Bausteine kommen aus den Werkbänken des Schäfli
(Ochsenblut, Gold, Kalk), des Ruedihus und des Schlössli. Hier wird jede dieser Farben, die noch in den gebauten Seiten steht, auf die Töne der
Culinarium-Seite umgerechnet (website/assets/culinarium.css :root): dunkel wird Nacht und Schiefer der Bar (#16151A, #222028, #3A3845), die Mitte
Kerze (#EF7649, #B15736), hell wird Warmweiß der Plakate (#FAF4F4). Helligkeit bleibt. Fotos werden nicht angefasst, nur Text in CSS und HTML. Mehrfach anwendbar."""
import colorsys, glob, os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
FEST = {'#fd9964': '#ef7649', '#e8875a': '#ef7649', '#fec7aa': '#f5a689', '#c42e13': '#b15736', '#a8260f': '#b15736', '#e0a96a': '#ef7649', '#7d433a': '#3a3845', '#e6007e': '#e6007e'}   # Signalfarben der Vorlagen; Magenta ist die Schnittlinie im Druckbogen
HAUS = {(0x16, 0x15, 0x1a), (0x0f, 0x0e, 0x13), (0x1c, 0x1b, 0x21), (0x22, 0x20, 0x28), (0x26, 0x25, 0x2e), (0x3a, 0x38, 0x45), (0xfa, 0xf4, 0xf4), (0xf2, 0xea, 0xea),
        (0xff, 0xfb, 0xfa), (0xef, 0x76, 0x49), (0xf5, 0xa6, 0x89), (0xb1, 0x57, 0x36), (0x5b, 0x57, 0x63), (0x26, 0x24, 0x2d), (0x89, 0x53, 0xa9)}


def _ton(r, g, b):
    if (r, g, b) in HAUS:
        return r, g, b
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    grad = h * 360
    if s < .1 or l > .985 or l < .02 or not (grad <= 70 or 195 <= grad <= 248 or grad >= 350):
        return r, g, b
    if l < .45:          # Nacht und Schiefer der Bar
        nh, ns = 250 / 360, .1
    elif l < .86:        # Kerze aus den Abendfotos
        nh, ns = 16 / 360, .72 if l < .7 else .78
    else:                # Warmweiß der Plakate
        nh, ns = 0, .38
    nr, ng, nb = colorsys.hls_to_rgb(nh, l, ns)
    return round(nr * 255), round(ng * 255), round(nb * 255)


_blau = _ton


def faerbe(t):
    def hexf(m):
        x = m.group(1)
        if len(x) == 3:
            x = ''.join(c * 2 for c in x)
        if len(x) != 6:
            return m.group(0)
        k = '#' + x.lower()
        if k in FEST:
            return FEST[k]
        return '#%02x%02x%02x' % _blau(*(int(x[i:i + 2], 16) for i in (0, 2, 4)))
    t = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![0-9a-fA-F-])', hexf, t)
    t = re.sub(r'(rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', lambda m: '%s(%d,%d,%d' % ((m.group(1),) + _blau(int(m.group(2)), int(m.group(3)), int(m.group(4)))), t)
    return t


def nur_style(t):
    """In HTML nur <style>-Blöcke und style=""-Werte umrechnen, nie Text, Adressen oder eingebettete Bilder."""
    t = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + faerbe(m.group(2)) + m.group(3), t, flags=re.S)
    t = re.sub(r'(style=")([^"]*)(")', lambda m: m.group(1) + faerbe(m.group(2)) + m.group(3), t)
    t = re.sub(r'(<meta name="theme-color" content=")(#[0-9a-fA-F]{6})', lambda m: m.group(1) + faerbe(m.group(2)), t)
    t = re.sub(r'(<svg\b.*?</svg>)', lambda m: faerbe(m.group(1)) if 'data:image' not in m.group(1) else m.group(1), t, flags=re.S)
    return t


def ohne_fett(t):
    """Nie fett (Tasty-Sprache Stufe 2 Nr. 8): kräftige Schnitte werden Medium, Titel bleiben Regular."""
    t = re.sub(r'font-weight:\s*(?:600|700|800|900|bold)\b', 'font-weight:500', t)
    return re.sub(r'(font:\s*)(?:600|700|800|900|bold)\b', r'\g<1>500', t)


def anwenden():
    n = 0
    for p in glob.glob(os.path.join(ROOT, 'werkbank', '**', '*.css'), recursive=True):
        a = open(p, encoding='utf-8').read(); b = ohne_fett(faerbe(a))
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    seiten = (glob.glob(os.path.join(ROOT, 'werkbank', '**', '*.html'), recursive=True)
              + [os.path.join(ROOT, d, 'index.html') for d in ('unterlagen', 'drucksachen', 'untersetzer', 'feed', 'material', 'mails')])
    for p in seiten:
        if not os.path.exists(p):
            continue
        a = open(p, encoding='utf-8').read(); b = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + ohne_fett(m.group(2)) + m.group(3), nur_style(a), flags=re.S)
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    return n


if __name__ == '__main__':
    print('umgefärbt:', anwenden(), 'Dateien')
