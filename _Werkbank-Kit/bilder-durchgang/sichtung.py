import os, re, glob, json, sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
W = os.path.expanduser('~/Desktop/Website-Projekte/')
H = [('carlton', 'Carlton-Europe Interlaken'), ('dolden', 'Waldhotel Doldenhorn'), ('ruedi', 'Landgasthof Ruedihus'), ('gaster', 'Berghotel Gasterntal')]
S = sys.argv[1]; alle = []
for kurz, ordner in H:
    R = W + ordner + '/'; gef = {}
    for f in sorted(glob.glob(R + '*.html')):
        n = os.path.basename(f)
        if re.match(r'(varianten|konzept|vorschau)', n): continue
        t = open(f, encoding='utf-8').read()
        for m in re.findall(r'assets/(?:img|v7|v8|hochgerechnet)/[\w\-./]+?\.(?:webp|jpg|jpeg|png)', t):
            gef.setdefault(m, set()).add(n.replace('.html', ''))
    # nach Motiv bündeln (Grössen-Anhänge weg), grösste Datei zählt
    mot = {}
    for pfad, seiten in gef.items():
        b = re.sub(r'-(s|m|l|k|klein|mittel|gross|\d{3,4})(?=\.\w+$)', '', pfad)
        p = R + pfad
        if not os.path.exists(p): continue
        try: w, h = Image.open(p).size
        except Exception: continue
        e = mot.setdefault(b, {'pfad': p, 'w': w, 'h': h, 'seiten': set()})
        if w * h > e['w'] * e['h']: e.update(pfad=p, w=w, h=h)
        e['seiten'] |= seiten
    man = {}
    try: man = json.load(open(R + 'assets/img/manifest.json'))
    except Exception: pass
    for b, e in mot.items():
        key = os.path.basename(b).rsplit('.', 1)[0]
        if e['w'] < 500 or '/logo' in b or key.startswith(('ehre-', 'logo', 'film-')): continue
        im = Image.open(e['pfad']).convert('L'); g = im.resize((1000, max(1, round(im.height * 1000 / im.width))), Image.LANCZOS)
        a = np.asarray(g).astype(np.float32)
        lap = np.asarray(g.filter(ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], 1, 128))).astype(np.float32) - 128
        m = man.get(key, {})
        alle.append({'haus': kurz, 'key': key, 'pfad': e['pfad'], 'w': e['w'], 'h': e['h'], 'seiten': sorted(e['seiten']), 'scharf': round(float(lap.var()), 1),
                     'hell': round(float(a.mean()), 0), 'kontrast': round(float(a.std()), 0), 'orig': m.get('original') or ([m.get('quelle_w')] if m.get('quelle_w') else None), 'quelle': m.get('quelle', '')})
    print(kurz, len([x for x in alle if x['haus'] == kurz]), 'Motive')
json.dump(alle, open(S + '/sichtung/alle.json', 'w'), ensure_ascii=False, indent=0)
# Bögen: 4 x 4, je Haus, nach Schärfe aufsteigend
for kurz, _ in H:
    l = sorted([x for x in alle if x['haus'] == kurz], key=lambda x: x['scharf'])
    for n in range(0, len(l), 16):
        B = Image.new('RGB', (4 * 400, 4 * 300), (30, 30, 30)); d = ImageDraw.Draw(B)
        for i, x in enumerate(l[n:n + 16]):
            im = Image.open(x['pfad']).convert('RGB'); im.thumbnail((396, 268)); cx, cy = (i % 4) * 400, (i // 4) * 300
            B.paste(im, (cx + 2, cy + 2)); d.text((cx + 4, cy + 274), f"{n + i} {x['key'][:26]} {x['w']}px s{x['scharf']:.0f}", fill=(255, 255, 255))
        B.save(f"{S}/sichtung/{kurz}-{n // 16}.jpg", quality=80)
