"""Zweite Rechnung für die Zeile «A UNiQUE EXPERiENCE BY MOMO X RUDI»: Buchstabe für Buchstabe mit Sperrung gesetzt, Sperrung so gewählt,
dass die Zeile so breit ist wie im Original (Verhältnis Breite/Höhe), dann Deckung wie in match.py."""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont
sys.argv = sys.argv[:2]
import match as Mt
FD = sys.argv[1]
TEXT = 'A UNiQUE EXPERiENCE BY MOMO X RUDI'
def setze(f, sp):
    gr = 300; x = 20; im = Image.new('L', (int(len(TEXT) * gr * 1.4), gr * 2), 255); d = ImageDraw.Draw(im)
    for c in TEXT:
        d.text((x, 40), c, font=f, fill=0); x += f.getlength(c) + sp * gr
    return Mt.maske(im)
zv = Mt.ZEILE.size[0] / Mt.ZEILE.size[1]
L = [('Lexend 800', 'Lexend[wght].ttf', {'Weight': 800}), ('Lexend 700', 'Lexend[wght].ttf', {'Weight': 700}), ('Urbanist 800', 'Urbanist[wght].ttf', {'Weight': 800}),
     ('Urbanist 900', 'Urbanist[wght].ttf', {'Weight': 900}), ('Outfit 800', 'Outfit[wght].ttf', {'Weight': 800}), ('Righteous', 'Righteous-Regular.ttf', None),
     ('M PLUS Rounded 1c 900', 'MPLUSRounded1c-Black.ttf', None), ('Nunito 900', 'Nunito[wght].ttf', {'Weight': 900}), ('Baloo 2 800', 'Baloo2[wght].ttf', {'Weight': 800}),
     ('Fredoka 700 schmal', 'Fredoka[wdth,wght].ttf', {'Weight': 700, 'Width': 75})]
erg = []
for n, d, ax in L:
    f = Mt.lade(d, ax); lo, hi = -0.05, 0.6
    for _ in range(18):
        mid = (lo + hi) / 2; m = setze(f, mid)
        if m.size[0] / m.size[1] < zv: lo = mid
        else: hi = mid
    m = setze(f, (lo + hi) / 2)
    erg.append(dict(name=n, datei=d, sperrung_em=round((lo + hi) / 2, 3), deckung=round(Mt.deckung(Mt.ZEILE, m), 3)))
erg.sort(key=lambda x: -x['deckung'])
json.dump(erg, open(os.path.join(Mt.H, 'match_zeile.json'), 'w'), ensure_ascii=False, indent=1)
[print('%-24s %.3f  Sperrung %.3f em' % (x['name'], x['deckung'], x['sperrung_em'])) for x in erg]
