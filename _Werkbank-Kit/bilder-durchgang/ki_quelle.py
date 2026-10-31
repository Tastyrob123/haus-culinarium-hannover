"""Überarbeitete Fotos gehen dem Original vor (Robert 08.10.2026: jedes Foto, das per KI besser wird, wird ersetzt).

Wer diese Datei einbindet (`import ki_quelle` als erste Zeile nach den Importen eines Bild-Skripts), bekommt beim Öffnen eines
Quellfotos aus einem Ordner `_quelle/` die überarbeitete Fassung, sofern sie unter
~/Desktop/Website-Projekte/_KI-Fassungen/<Pfad des Originals ab Website-Projekte>.png liegt.
Die Fassung wird auf das Seitenverhältnis des Originals beschnitten und nie kleiner als das Original geliefert, damit jeder
Zuschnitt im Bau gleich bleibt. Das Original wird nie angefasst; Datei löschen = Original gilt wieder.
Mit KI_LOG=<Datei> wird nur mitgeschrieben, welche Quellfotos ein Bau öffnet (für die Sichtung)."""
import os, sys, json
from PIL import Image, ImageOps
WURZEL = os.path.realpath(os.path.expanduser('~/Desktop/Website-Projekte')) + '/'
KI = WURZEL + '_KI-Fassungen/'
LOG = os.environ.get('KI_LOG'); AUS = os.environ.get('KI_AUS')
_open = Image.open
def ki_pfad(p):
    try: a = os.path.realpath(os.path.abspath(os.fspath(p)))
    except TypeError: return None, None
    if not a.startswith(WURZEL) or '/_quelle/' not in a or a.startswith(KI): return None, None
    if '/_quelle/ki/' in a or '/erzeugt' in a or not a.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')): return None, None
    return a, KI + os.path.relpath(a, WURZEL) + '.png'
def offen(p, *arg, **kw):
    a, ziel = ki_pfad(p)
    if a and LOG:
        f = sys._getframe(1)
        with open(LOG, 'a', encoding='utf-8') as l: l.write(json.dumps([a, f.f_code.co_filename, f.f_code.co_name, f.f_lineno, str(f.f_locals.get('name', f.f_locals.get('n', '')))], ensure_ascii=False) + '\n')
    if a and not AUS and os.path.exists(ziel):
        ow, oh = ImageOps.exif_transpose(_open(a)).size
        im = _open(ziel).convert('RGB'); w, h = im.size
        if w / h > ow / oh: nw = round(h * ow / oh); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else: nh = round(w * oh / ow); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        if im.width < ow: im = im.resize((ow, oh), Image.LANCZOS)
        return im
    return _open(p, *arg, **kw)
Image.open = offen
