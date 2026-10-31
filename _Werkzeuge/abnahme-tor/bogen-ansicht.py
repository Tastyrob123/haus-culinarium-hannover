#!/usr/bin/env python3
"""Abnahme-Tor · Augenprüfung: Ansichten einer Seite (ganzseite.js) als Bögen zu je 6 (2 × 3, halbe Grösse, nummeriert).
Aufruf: python3 bogen-ansicht.py <augen-ordner>"""
import sys, glob, os, re
from PIL import Image, ImageDraw
A = sys.argv[1]; aus = os.path.join(A, 'boegen'); os.makedirs(aus, exist_ok=True)
gruppen = {}
for f in sorted(glob.glob(os.path.join(A, '*-[0-9][0-9].jpg'))):
    gruppen.setdefault(re.sub(r'-\d\d\.jpg$', '', os.path.basename(f)), []).append(f)
for name, fs in gruppen.items():
    for b in range(0, len(fs), 6):
        teil = fs[b:b + 6]; ims = [Image.open(f).convert('RGB') for f in teil]; w, h = ims[0].size; s = .5 if w > 800 else 1
        tw, th = int(w * s), int(h * s); cols = 2 if w > 800 else 3; rows = (len(ims) + cols - 1) // cols
        bogen = Image.new('RGB', (cols * tw + (cols - 1) * 8, rows * th + (rows - 1) * 8), (255, 255, 255)); d = ImageDraw.Draw(bogen)
        for i, im in enumerate(ims):
            x, y = (i % cols) * (tw + 8), (i // cols) * (th + 8); bogen.paste(im.resize((tw, th)), (x, y))
            d.rectangle([x, y, x + 34, y + 18], fill=(255, 31, 90)); d.text((x + 4, y + 3), os.path.basename(teil[i])[-6:-4], fill=(255, 255, 255))
        bogen.save(os.path.join(aus, f'{name}-b{b // 6:02d}.jpg'), quality=78)
print(len(os.listdir(aus)))
