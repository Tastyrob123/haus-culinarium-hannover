#!/usr/bin/env python3
"""Culinarium Hannover · Bild für den Schluss von «Alle Abende» (27.10.2026).
Robert: «Das nächste Plakat kommt bestimmt … dann ist ein Bild mit einem Weinglas sinnlos».
Eine dunkle Wand mit allen echten Plakaten seit dem ersten Pop-up, in der Reihenfolge der Abende; der letzte Platz ist leer, nur das Klebeband hängt schon.
Schreibt _zuschnitt/plakatwand.jpg. Aufruf: python3 website/plakatwand.py"""
import os, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau

random.seed(7)
W, H, S, G = 3000, 1800, 540, 44                    # Wand, Plakat, Abstand
COLS, ROWS = 5, 3
X0 = (W - COLS * S - (COLS - 1) * G) // 2
Y0 = (H - ROWS * S - (ROWS - 1) * G) // 2

# Wand: fast schwarz, leicht warm, mit feinem Korn
wand = Image.new('RGB', (W, H), (22, 19, 22))
korn = Image.effect_noise((W, H), 18).convert('L')
wand = Image.composite(Image.new('RGB', (W, H), (34, 30, 33)), wand, korn.point(lambda v: int(v * .35)))

quellen = [bau.BILD['pop23'][0]] + ['%s' % bau.BILD['p_' + a[4]][0] for a in bau.ABENDE if a[4]]


def band(img, cx, cy, ang):
    t = Image.new('RGBA', (84, 26), (214, 200, 176, 105))
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))


wand = wand.convert('RGBA')
for i in range(COLS * ROWS):
    c, r = i % COLS, i // COLS
    x, y = X0 + c * (S + G), Y0 + r * (S + G)
    ang = random.uniform(-1.4, 1.4)
    if i < len(quellen):
        p = ImageOps.fit(Image.open(os.path.join(bau.PROJ, quellen[i])).convert('RGB'), (S, S), Image.LANCZOS).convert('RGBA')
        p = p.rotate(ang, expand=True, resample=Image.BICUBIC)
        sch = Image.new('RGBA', p.size, (0, 0, 0, 0))
        sch.putalpha(p.getchannel('A').point(lambda v: int(v * .55)))
        sch = sch.filter(ImageFilter.GaussianBlur(14))
        wand.alpha_composite(sch, (x - (p.width - S) // 2 + 8, y - (p.height - S) // 2 + 14))
        wand.alpha_composite(p, (x - (p.width - S) // 2, y - (p.height - S) // 2))
    else:
        # der freie Platz: ein heller Rand vom alten Plakat, das Klebeband hängt schon
        leer = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(leer)
        d.rectangle((0, 0, S - 1, S - 1), outline=(120, 108, 104, 70), width=3)
        leer = leer.rotate(ang, expand=True, resample=Image.BICUBIC)
        wand.alpha_composite(leer, (x - (leer.width - S) // 2, y - (leer.height - S) // 2))
    band(wand, x + 14, y + 4, -38 + ang)
    band(wand, x + S - 14, y + 4, 38 + ang)

# leicht abdunkeln, zu den Rändern mehr (Text steht hell darüber)
wand = wand.convert('RGB')
dunkel = Image.new('L', (W, H), 0)
ImageDraw.Draw(dunkel).ellipse((-W * .15, -H * .25, W * 1.15, H * 1.25), fill=255)
dunkel = dunkel.filter(ImageFilter.GaussianBlur(260))
schwarz = Image.new('RGB', (W, H), (10, 9, 12))
wand = Image.composite(Image.blend(wand, schwarz, .52), Image.blend(wand, schwarz, .68), dunkel)
z = os.path.join(bau.HIER, '_zuschnitt', 'plakatwand.jpg')
wand.save(z, 'JPEG', quality=90)
print(z, wand.size, len(quellen), 'Plakate')
