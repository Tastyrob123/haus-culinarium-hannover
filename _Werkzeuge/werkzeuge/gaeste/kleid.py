"""Kleid · die wenigen Bilder, die das Werkzeug «gaeste» je Haus zeigt: Kulisse, drei Kacheln, Tapete, Zeichen oder Schriftzug.

Liest sie aus dem Projekt des Hauses (NUR lesen) und legt verkleinerte Kopien nach werkzeuge/gaeste/kleid/<haus>/.
Welche Bilder, steht in quellen.json unter «kleid». Erzeugt wird nichts, es sind die Fotos und Zeichen des Hauses.
Start:  python3 werkzeuge/gaeste/kleid.py <haus>      (braucht Pillow; nur beim Einrichten eines Hauses, nicht im Betrieb)
"""
import json
import os
import shutil
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
WURZEL = HIER.parent.parent


def _bild(quelle, ziel, eintrag, breite, guete):
    from PIL import Image
    im = Image.open(quelle).convert('RGB')
    l, o, r, u = eintrag.get('ausschnitt') or [0, 0, 1, 1]
    im = im.crop((int(l * im.width), int(o * im.height), int(r * im.width), int(u * im.height)))
    if im.width > breite:
        im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
    im.save(ziel, 'WEBP', quality=guete, method=6)
    return im.size


def baue(haus):
    stamm = json.loads((WURZEL / 'haeuser' / haus / 'haus.json').read_text(encoding='utf-8'))
    rezept = (json.loads((HIER / 'quellen.json').read_text(encoding='utf-8')).get(haus) or {}).get('kleid')
    if not rezept:
        raise SystemExit(f'Für «{haus}» steht in quellen.json kein Kleid.')
    q = Path(os.path.expanduser(stamm['quelle']))
    ziel = HIER / 'kleid' / haus
    ziel.mkdir(parents=True, exist_ok=True)
    aus = {'kulisse': None, 'kacheln': {}, 'tapete': None, 'zeichen': None, 'schriftzug': None, 'quellen': {}}
    if rezept.get('kulisse'):
        g = _bild(q / rezept['kulisse']['datei'], ziel / 'kulisse.webp', rezept['kulisse'], 1800, 58)
        aus['kulisse'], aus['quellen']['kulisse'] = 'kulisse.webp', rezept['kulisse']['datei']
        print('kulisse', g, (ziel / 'kulisse.webp').stat().st_size)
    for name, e in (rezept.get('kacheln') or {}).items():
        g = _bild(q / e['datei'], ziel / f'k-{name}.webp', e, 960, 72)
        aus['kacheln'][name], aus['quellen']['k-' + name] = f'k-{name}.webp', e['datei']
        print('kachel', name, g, (ziel / f'k-{name}.webp').stat().st_size)
    for name, datei in (('tapete', 'tapete.webp'), ('zeichen', 'zeichen.webp'), ('schriftzug', 'schriftzug.svg')):
        if rezept.get(name):
            shutil.copyfile(q / rezept[name], ziel / datei)
            aus[name], aus['quellen'][name] = datei, rezept[name]
    (ziel / 'kleid.json').write_text(json.dumps(aus, ensure_ascii=False, indent=1), encoding='utf-8')
    return aus


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    print(json.dumps(baue(sys.argv[1]), ensure_ascii=False))
