"""Culinarium · Station 05 · Farben messen (26.10.2026). Zwei Rechnungen je Fläche: häufigster Ton (Modus über 32er-Stufen, Mittel
der Pixel in dieser Stufe) und Median derselben Fläche. Ergebnis: _bau/messung.json. Flächen in Anteilen der Bildbreite/-höhe."""
import json, os
from collections import Counter
from PIL import Image
import statistics as st
P = os.path.expanduser('~/Desktop/Website-Projekte/Culinarium Hannover/')
H = os.path.dirname(os.path.abspath(__file__))

def hx(c): return '#%02X%02X%02X' % tuple(int(round(v)) for v in c)

def miss(datei, box, filt=None):
    im = Image.open(P + datei).convert('RGB'); w, h = im.size
    b = tuple(int(round(v * (w if i % 2 == 0 else h))) for i, v in enumerate(box))
    px = list(im.crop(b).getdata())
    if filt: px = [p for p in px if filt(p)]
    stufe = Counter((r >> 3, g >> 3, bb >> 3) for r, g, bb in px)
    top = stufe.most_common(1)[0][0]
    inn = [p for p in px if (p[0] >> 3, p[1] >> 3, p[2] >> 3) == top]
    modus = [sum(c[i] for c in inn) / len(inn) for i in range(3)]
    med = [st.median(c[i] for c in px) for i in range(3)]
    return dict(datei=datei, groesse=[w, h], box=list(b), hex=hx(modus), median=hx(med), anteil_modus=round(len(inn) / len(px), 3), pixel=len(px))

hell = lambda p: sum(p) > 690
dunkel = lambda p: sum(p) < 300
IG = '_quelle/extern/ig/'
PLAKATE = [('2024-11', 'Ski', IG + '2024-11-06_culinarium_hannover_DCCf-ikoaGs-1.jpg'),
           ('2025-02', 'Panther auf Thron', IG + '2025-02-04_culinarium_hannover_DFqbLG2s_dc-1.jpg'),
           ('2025-06', 'Gärtnerin', IG + '2025-05-17_culinarium_hannover_DJw8OqGMY1G-1.jpg'),
           ('2025-11', 'Kürbis', IG + '2025-10-13_culinarium_hannover_DPwlqcfiKcA-1.jpg'),
           ('2026-03', 'Panther mit Eisbecher', IG + '2026-03-06_culinarium_hannover_DVjkofijp6R-1.jpg'),
           ('2026-09', 'Mondfrau', IG + '2026-07-29_culinarium_hannover_DbYnkdkjrNy-1.jpg')]
out = {'plakate': []}
for k, n, d in PLAKATE:
    out['plakate'].append(dict(abend=k, motiv=n,
        band=miss(d, (.06, .77, .94, .97), hell),             # warmweisses Band unter dem Bild
        tinte=miss(d, (.12, .80, .88, .87), dunkel),          # Wortmarke CULINARIUM
        bild=miss(d, (.05, .03, .96, .73))))                  # Illustration: häufigster Ton = Grund des Plakats
json.dump(out, open(os.path.join(H, 'messung.json'), 'w'), ensure_ascii=False, indent=1)
for p in out['plakate']:
    print(p['abend'], p['motiv'], '| band', p['band']['hex'], p['band']['median'], '| tinte', p['tinte']['hex'], p['tinte']['median'], '| bild', p['bild']['hex'], p['bild']['median'], p['bild']['anteil_modus'])

# ---------------------------------------------------------------- Fotos von Rudi (_quelle/vom-kunden/drive)
D = '_quelle/vom-kunden/drive/'
FOTOS = [('Putz', 'warme Wand hinter dem Tisch mit Kerze und Apothekerflasche', D + '4029.jpg', (.10, .20, .40, .50), None),
         ('Flur', 'orange Wand im Flur zur Bar, Licht der Hängelampe', D + '3887.jpg', (.02, .20, .10, .40), None),
         ('Kerze', 'Kerze auf der Tafel, beleuchtetes Wachs', D + '3855.jpg', (.42, .74, .50, .86), lambda p: 420 < sum(p) < 690),
         ('Honig', 'Glasballon mit hellem Sirup an der Bar', D + '3937.jpg', (.30, .55, .42, .75), None),
         ('Schiefertisch', 'dunkle Tischplatte unter dem Glas', D + '5369.jpg', (.05, .82, .95, .98), None),
         ('Barnacht', 'Dunkel hinter dem Glas, ebd.', D + '5369.jpg', (.05, .02, .95, .20), None),
         ('Ziegel', 'Klinker an der Ecke Haasemannstraße, über den Schildern', D + '5541.jpg', (.00, .10, .08, .50), None),
         ('Campari', 'roter Drink im Stielglas, gereicht über den Tisch', D + '4026.jpg', (.74, .72, .86, .86), lambda p: p[0] > p[1] + 70 and p[0] > 110)]
out['fotos'] = []
for n, was, d, box, f in FOTOS:
    r = miss(d, box, f); r.update(name=n, was=was); out['fotos'].append(r)
    print(n, r['hex'], r['median'], r['anteil_modus'], r['box'])
# Rahmenlinie der Plakate: graue Pixel ohne Farbstich im Band
lin = miss(IG + '2026-03-06_culinarium_hannover_DVjkofijp6R-1.jpg', (.03, .73, .97, .99), lambda p: 380 < sum(p) < 600 and max(p) - min(p) < 14)
out['rahmen'] = lin; print('Rahmen', lin['hex'], lin['median'], lin['pixel'])
json.dump(out, open(os.path.join(H, 'messung.json'), 'w'), ensure_ascii=False, indent=1)
