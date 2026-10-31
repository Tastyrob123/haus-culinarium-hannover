"""Culinarium · Station 05 · Wortmarke und Zeile neben freie Schriften gelegt (26.10.2026).
Quelle: _quelle/logo/nachgezogen/wortmarke-und-zeile-aus-plakat-2026-09.png (Original-Pixel aus dem Plakat 2014 px).
Je Schrift: Wort gesetzt, auf dieselbe Box gebracht, Deckung (Schnitt durch Vereinigung) der schwarzen Flächen. Dazu das Breitenverhältnis
(Breite/Höhe des gesetzten Worts gegen das Original). Ausgabe: match.json + Vergleichsbild _bau/tmp/vergleich-*.png"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
P = os.path.expanduser('~/Desktop/Website-Projekte/Culinarium Hannover/')
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(H, 'tmp'); os.makedirs(T, exist_ok=True)
FD = sys.argv[1]
src = Image.open(P + '_quelle/logo/nachgezogen/wortmarke-und-zeile-aus-plakat-2026-09.png').convert('L')
w, h = src.size
def maske(im, schwelle=128):
    m = im.point(lambda v: 255 if v < schwelle else 0); return m.crop(m.getbbox())
WORT = maske(src.crop((0, 0, w, int(h * .45))))
ZEILE = maske(src.crop((0, int(h * .78), w, h)))

def setze(font, text, gr=300):
    f = font
    b = f.getbbox(text); im = Image.new('L', (b[2] - b[0] + 40, b[3] - b[1] + 40), 255)
    ImageDraw.Draw(im).text((20 - b[0], 20 - b[1]), text, font=f, fill=0); return maske(im)

def deckung(a, b):
    b = b.resize(a.size, Image.LANCZOS).point(lambda v: 255 if v > 127 else 0)
    pa, pb = a.tobytes(), b.tobytes()
    s = sum(1 for x, y in zip(pa, pb) if x and y); u = sum(1 for x, y in zip(pa, pb) if x or y)
    return s / u

def lade(datei, achsen):
    f = ImageFont.truetype(os.path.join(FD, datei), 300)
    if achsen:
        try:
            ax = f.get_variation_axes(); werte = [achsen.get(a['name'].decode() if isinstance(a['name'], bytes) else a['name'], a['maximum']) for a in ax]
            f.set_variation_by_axes(werte)
        except Exception as e: print('achsen', datei, e)
    return f
TITEL = [('Fraunces 900 Soft', 'Fraunces[SOFT,WONK,opsz,wght].ttf', {'Softness': 100, 'Wonky': 1, 'Optical size': 144, 'Weight': 900}),
         ('Gravitas One', 'GravitasOne.ttf', None), ('Abril Fatface', 'AbrilFatface-Regular.ttf', None), ('Chonburi', 'Chonburi-Regular.ttf', None),
         ('Rozha One', 'RozhaOne-Regular.ttf', None), ('Yeseva One', 'YesevaOne-Regular.ttf', None), ('DM Serif Display', 'DMSerifDisplay-Regular.ttf', None),
         ('Gloock', 'Gloock-Regular.ttf', None), ('Playfair Display 900', 'PlayfairDisplay[wght].ttf', {'Weight': 900}), ('Bodoni Moda 900', 'BodoniModa[opsz,wght].ttf', {'Weight': 900, 'Optical size': 96}),
         ('Bagel Fat One', 'BagelFatOne-Regular.ttf', None), ('Holtwood One SC', 'HoltwoodOneSC-Regular.ttf', None), ('Calistoga', 'Calistoga-Regular.ttf', None),
         ('Unbounded 900', 'Unbounded[wght].ttf', {'Weight': 900}), ('Syne 800', 'Syne[wght].ttf', {'Weight': 800}), ('Krona One', 'KronaOne-Regular.ttf', None),
         ('Rubik Mono One', 'RubikMonoOne-Regular.ttf', None), ('Dela Gothic One', 'DelaGothicOne-Regular.ttf', None)]
ZEILEN = [('Fredoka 600', 'Fredoka[wdth,wght].ttf', {'Weight': 600, 'Width': 125}), ('Fredoka 700', 'Fredoka[wdth,wght].ttf', {'Weight': 700, 'Width': 125}),
          ('Nunito 900', 'Nunito[wght].ttf', {'Weight': 900}), ('Quicksand 700', 'Quicksand[wght].ttf', {'Weight': 700}), ('Baloo 2 800', 'Baloo2[wght].ttf', {'Weight': 800}),
          ('Varela Round', 'VarelaRound-Regular.ttf', None), ('M PLUS Rounded 1c 800', 'MPLUSRounded1c-ExtraBold.ttf', None), ('M PLUS Rounded 1c 900', 'MPLUSRounded1c-Black.ttf', None),
          ('Comfortaa 700', 'Comfortaa[wght].ttf', {'Weight': 700}), ('Sniglet 800', 'Sniglet-ExtraBold.ttf', None), ('Righteous', 'Righteous-Regular.ttf', None),
          ('Lexend 800', 'Lexend[wght].ttf', {'Weight': 800}), ('Outfit 800', 'Outfit[wght].ttf', {'Weight': 800}), ('Unbounded 700', 'Unbounded[wght].ttf', {'Weight': 700})]
erg = {'wort': [], 'zeile': []}
for art, liste, text, ziel in (('wort', TITEL, 'CULINARIUM', WORT), ('zeile', ZEILEN, 'A UNiQUE EXPERiENCE BY MOMO X RUDi', ZEILE)):
    zv = ziel.size[0] / ziel.size[1]
    blatt = [ziel.convert('RGB')]
    for n, d, ax in liste:
        try: f = lade(d, ax)
        except Exception as e: print('fehlt', n, e); continue
        m = setze(f, text if art == 'wort' else text.replace('RUDi', 'RUDI'))
        erg[art].append(dict(name=n, datei=d, deckung=round(deckung(ziel, m), 3), breite=round((m.size[0] / m.size[1]) / zv, 3)))
        blatt.append(ImageOps.invert(m).convert('RGB'))
    erg[art].sort(key=lambda x: -x['deckung'])
    # Vergleichsbild: Original oben, dann die Schriften in Reihenfolge der Liste, je 70 px hoch
    zh = 64; rows = [b.resize((int(b.size[0] * zh / b.size[1]), zh)) for b in blatt]
    W = max(r.size[0] for r in rows) + 260; im = Image.new('RGB', (W, (zh + 16) * len(rows)), 'white'); d = ImageDraw.Draw(im)
    namen = ['ORIGINAL'] + [x[0] for x in liste]
    for i, r in enumerate(rows):
        im.paste(r, (250, i * (zh + 16) + 8)); d.text((8, i * (zh + 16) + 30), namen[i] if i < len(namen) else '', fill=(200, 0, 0))
    im.save(os.path.join(T, 'vergleich-%s.png' % art))
json.dump(erg, open(os.path.join(H, 'match.json'), 'w'), ensure_ascii=False, indent=1)
for art in erg:
    print(art); [print('  %-24s %.3f  Breite %.2f' % (x['name'], x['deckung'], x['breite'])) for x in erg[art]]
