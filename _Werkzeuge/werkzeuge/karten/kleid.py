"""Kleid · was das Werkzeug «karten» je Haus vom Haus selbst zeigt: Zeichen (oder Schriftzug), Tapete, ein Foto je Karte.

Liest sie aus dem Projekt des Hauses (NUR lesen) und legt Kopien nach werkzeuge/karten/kleid/<haus>/ (wie werkzeuge/gaeste/kleid.py).
Welche Dateien, steht in quellen.json unter «kleid». Erzeugt wird nichts, es sind Zeichen und Fotos des Hauses.
Ohne Kleid zeigt das Werkzeug einen Ring mit den Anfangsbuchstaben und Kacheln mit Initialen, und druckt den Namen des Hauses.

    python3 werkzeuge/karten/kleid.py <haus>      (braucht Pillow; nur beim Einrichten eines Hauses, nicht im Betrieb)

Das Zeichen wird beim Kopieren auf reine Zeichnung beschränkt (nur Formen und ihre Masse, keine Skripte, keine Verweise,
keine eigenen Farben): es wird in die gedruckte Karte eingesetzt und nimmt dort die Farbe der Welt an.
"""
import json
import os
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HIER = Path(__file__).resolve().parent
WURZEL = HIER.parent.parent
FORMEN = {'svg', 'g', 'path', 'circle', 'ellipse', 'rect', 'polygon', 'polyline', 'line'}
MASSE = {'viewBox', 'd', 'transform', 'points', 'cx', 'cy', 'r', 'rx', 'ry', 'x', 'y', 'x1', 'y1', 'x2', 'y2', 'width', 'height', 'fill-rule', 'clip-rule'}


def zeichnung(quelle):
    """SVG des Hauses → (reine Zeichnung als Text, Breite, Höhe)."""
    wurzel = ET.parse(quelle).getroot()

    def rein(e, oben=False):
        name = e.tag.split('}')[-1]
        if name not in FORMEN:
            return None
        neu = ET.Element(name)
        for k, v in e.attrib.items():
            k = k.split('}')[-1]
            if k in MASSE and not (oben and k in ('width', 'height')) and 'url(' not in v and 'javascript' not in v.lower():
                neu.set(k, v)
        for kind in e:
            r = rein(kind)
            if r is not None:
                neu.append(r)
        return neu
    svg = rein(wurzel, True)
    if svg is None or not svg.get('viewBox'):
        raise SystemExit(f'{quelle} ist keine Zeichnung mit viewBox.')
    _, _, b, h = (float(x) for x in svg.get('viewBox').replace(',', ' ').split())
    svg.set('xmlns', 'http://www.w3.org/2000/svg')
    svg.set('fill', 'currentColor')
    svg.set('aria-hidden', 'true')
    return ET.tostring(svg, encoding='unicode'), b, h


def foto(quelle, ziel, kante=320):
    from PIL import Image
    im = Image.open(quelle).convert('RGB')
    seite = min(im.width, im.height)          # Quadrat aus der Mitte, wie die Kacheln im Original
    l, o = (im.width - seite) // 2, (im.height - seite) // 2
    im = im.crop((l, o, l + seite, o + seite)).resize((kante, kante), Image.LANCZOS)
    im.save(ziel, 'WEBP', quality=78, method=6)


def baue(haus):
    stamm = json.loads((WURZEL / 'haeuser' / haus / 'haus.json').read_text(encoding='utf-8'))
    rezept = (json.loads((HIER / 'quellen.json').read_text(encoding='utf-8')).get(haus) or {}).get('kleid')
    if not rezept:
        raise SystemExit(f'Für «{haus}» steht in quellen.json kein Kleid.')
    q = Path(os.path.expanduser(stamm['quelle']))
    ziel = HIER / 'kleid' / haus
    ziel.mkdir(parents=True, exist_ok=True)
    aus = {'zeichen': None, 'zeichen_mass': None, 'tapete': None, 'fotos': {}, 'quellen': {}}
    if rezept.get('zeichen'):
        text, b, h = zeichnung(q / rezept['zeichen'])
        (ziel / 'zeichen.svg').write_text(text, encoding='utf-8')
        aus['zeichen'], aus['zeichen_mass'], aus['quellen']['zeichen'] = 'zeichen.svg', [b, h], rezept['zeichen']
    if rezept.get('tapete'):
        shutil.copyfile(q / rezept['tapete'], ziel / 'tapete.webp')
        aus['tapete'], aus['quellen']['tapete'] = 'tapete.webp', rezept['tapete']
    for karte, datei in (rezept.get('fotos') or {}).items():
        foto(q / datei, ziel / f'f-{karte}.webp')
        aus['fotos'][karte], aus['quellen']['f-' + karte] = f'f-{karte}.webp', datei
    (ziel / 'kleid.json').write_text(json.dumps(aus, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return aus


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    print(json.dumps(baue(sys.argv[1]), ensure_ascii=False))
