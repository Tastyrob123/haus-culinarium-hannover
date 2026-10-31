"""Culinarium · Station 05 · Wortmarke, Zeile und Zeichen als Vektor (26.10.2026).
Quelle: Original-Pixel aus dem grössten Plakat (Mondfrau, 2014 × 2003, Beitrag DbYnkdkjrNy), ausgeschnitten von Station 03:
_quelle/logo/nachgezogen/wortmarke-und-zeile-aus-plakat-2026-09.png. Vierfach vergrössert, leicht geglättet, Schwelle in der Mitte zwischen
Tinte #3A3845 und Band #FAF4F4, dann potrace. Form nicht verändert; Deckung gegen das Original wird gemessen und ausgegeben.
Ergebnis: marke/zeichen/wortmarke.svg, zeile.svg, wortmarke-mit-zeile.svg, c.svg (der erste Buchstabe), x.svg (das x aus MOMO X RUDI)."""
import os, re, subprocess, json
from PIL import Image, ImageFilter
P = os.path.expanduser('~/Desktop/Website-Projekte/Culinarium Hannover/')
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(H, 'tmp'); Z = os.path.join(os.path.dirname(H), 'marke', 'zeichen')
os.makedirs(T, exist_ok=True); os.makedirs(Z, exist_ok=True)
src = Image.open(P + '_quelle/logo/nachgezogen/wortmarke-und-zeile-aus-plakat-2026-09.png').convert('L')
W, Hh = src.size
SW = (0x3A * .3 + 0x38 * .59 + 0x45 * .11 + 0xFA * .3 + 0xF4 * .59 + 0xF4 * .11) / 2   # Mitte zwischen Tinte und Band (Luminanz)

def bitmap(box, name, k=4):
    im = src.crop(box)
    im = im.resize((im.width * k, im.height * k), Image.LANCZOS).filter(ImageFilter.GaussianBlur(k * .55))
    bw = im.point(lambda v: 0 if v < SW else 255).convert('1')
    p = os.path.join(T, name + '.pbm'); bw.save(p); return p, bw

def potrace(pbm, name):
    out = os.path.join(T, name + '.svg')
    subprocess.run(['potrace', pbm, '-s', '-o', out, '-t', '12', '-a', '1.0', '-O', '0.35', '--flat'], check=True)
    return open(out).read()

def bereinige(svg, farbe='currentColor'):
    """potrace-SVG → viewBox in Pixeln der vergrösserten Quelle, ein <path>, ohne Transform-Gruppe."""
    w = float(re.search(r'width="([\d.]+)pt"', svg).group(1)); h = float(re.search(r'height="([\d.]+)pt"', svg).group(1))
    tr = re.search(r'<g transform="([^"]+)"', svg).group(1)
    pfade = re.findall(r'<path d="([^"]+)"', svg, re.S)
    d = ' '.join(' '.join(p.split()) for p in pfade)
    return w, h, tr, d

def schreib(name, w, h, tr, d, vb=None, farbe='currentColor'):
    vb = vb or '0 0 %g %g' % (w, h)
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" fill="%s"><g transform="%s"><path fill-rule="evenodd" d="%s"/></g></svg>' % (vb, farbe, tr, d))
    open(os.path.join(Z, name + '.svg'), 'w').write(s); return s

def bbox_dunkel(box):
    m = src.crop(box).point(lambda v: 255 if v < SW else 0); b = m.getbbox()
    return (box[0] + b[0], box[1] + b[1], box[0] + b[2], box[1] + b[3])

PAD = 6
wb = bbox_dunkel((0, 0, W, int(Hh * .45))); wb = (wb[0] - PAD, wb[1] - PAD, wb[2] + PAD, wb[3] + PAD)
zb = bbox_dunkel((0, int(Hh * .78), W, Hh)); zb = (zb[0] - PAD, zb[1] - PAD, zb[2] + PAD, zb[3] + PAD)
erg = {}
for name, box in (('wortmarke', wb), ('zeile', zb)):
    pbm, bw = bitmap(box, name)
    w, h, tr, d = bereinige(potrace(pbm, name))
    schreib(name, w, h, tr, d); schreib(name + '-tinte', w, h, tr, d, farbe='#3A3845')
    erg[name] = dict(box=list(box), w=w, h=h, tr=tr, d=d)
# Wortmarke mit Zeile: Lage aus dem Plakat übernommen (beide Teile mit demselben Massstab, k=4)
k = 4
x0 = min(wb[0], zb[0])
dxw, dxz, dy = (wb[0] - x0) * k, (zb[0] - x0) * k, (zb[1] - wb[1]) * k
Wg = (max(wb[2], zb[2]) - x0) * k; Hg = (zb[3] - wb[1]) * k
s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" fill="currentColor"><g transform="translate(%g 0)"><g transform="%s"><path fill-rule="evenodd" d="%s"/></g></g>'
     '<g transform="translate(%g %g)"><g transform="%s"><path fill-rule="evenodd" d="%s"/></g></g></svg>'
     % (Wg, Hg, dxw, erg['wortmarke']['tr'], erg['wortmarke']['d'], dxz, dy, erg['zeile']['tr'], erg['zeile']['d']))
open(os.path.join(Z, 'wortmarke-mit-zeile.svg'), 'w').write(s)

# Deckung prüfen: SVG gerendert gegen die Quelle (gleiche Box)
def render(name, size):
    """potrace rendert dieselbe Spur als Graustufenbild (-g), dann zurück auf die Grösse des Originals."""
    pgm = os.path.join(T, name + '-r.pgm')
    subprocess.run(['potrace', os.path.join(T, name + '.pbm'), '-g', '-o', pgm, '-t', '12', '-a', '1.0', '-O', '0.35'], check=True)
    return Image.open(pgm).convert('L').resize(size, Image.LANCZOS)
for name, box in (('wortmarke', wb), ('zeile', zb)):
    o = src.crop(box).point(lambda v: 1 if v < SW else 0)
    r = render(name, o.size).point(lambda v: 1 if v < 128 else 0)
    a, b = o.tobytes(), r.tobytes(); s_ = sum(1 for x, y in zip(a, b) if x and y); u = sum(1 for x, y in zip(a, b) if x or y)
    erg[name]['deckung'] = round(s_ / u, 4); print(name, 'Deckung gegen Original', erg[name]['deckung'], 'Box', box)

# Zeichen: die einzelnen Flächen der Wortmarke (Buchstaben) nach x sortiert; C = erste, x aus der Zeile = Fläche bei «MOMO X RUDI»
def teile(d):
    return [t.strip() for t in re.split(r'(?=M)', d) if t.strip()]
json.dump({k_: {kk: vv for kk, vv in v.items() if kk != 'd'} for k_, v in erg.items()}, open(os.path.join(H, 'zeichen.json'), 'w'), indent=1)

# ---------------------------------------------------------------- Einzelzeichen: Spalten ohne Tinte trennen die Buchstaben
def laeufe(box):
    m = src.crop(box).point(lambda v: 1 if v < SW else 0); w_, h_ = m.size; px = m.load()
    voll = [any(px[x, y] for y in range(h_)) for x in range(w_)]
    r, an = [], None
    for x, v in enumerate(voll + [False]):
        if v and an is None: an = x
        if not v and an is not None: r.append((box[0] + an, box[0] + x)); an = None
    return r
lw = laeufe(wb); lz = laeufe(zb)
print('Wortmarke Läufe', len(lw), 'Zeile Läufe', len(lz))
def einzel(name, x0, x1, box):
    b = bbox_dunkel((x0, box[1], x1, box[3])); b = (b[0] - PAD, b[1] - PAD, b[2] + PAD, b[3] + PAD)
    pbm, bw = bitmap(b, name); w, h, tr, d = bereinige(potrace(pbm, name)); schreib(name, w, h, tr, d); return b
cb = einzel('c', lw[0][0], lw[0][1], wb)
xb = einzel('x', lz[23][0], lz[23][1], zb) if len(lz) > 23 else None
print('C', cb, 'x', xb)
