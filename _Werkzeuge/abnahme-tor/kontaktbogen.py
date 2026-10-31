#!/usr/bin/env python3
"""Abnahme-Tor · Kontaktbögen für die Augenprüfung (Kriterien A): je Bogen bis zu 15 Blätter mit Nummer und Titel, rote Rahmen an maschinellen Funden.
Aufruf: python3 kontaktbogen.py <lauf> <ziel-ordner> [--quellen Vorlage,Art,Entwerfen,Vorschlag] [--je 15]"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
LAUF, ZIEL = sys.argv[1], sys.argv[2]
arg = lambda n, d=None: sys.argv[sys.argv.index('--' + n) + 1] if '--' + n in sys.argv else d
QU = arg('quellen', 'Vorlage,Art,Entwerfen,Vorschlag').split(','); JE = int(arg('je', 15))
# Stichprobe je Quelle: --stichprobe Muster=60,Art=30 nimmt gleichmässig verteilt so viele Blätter
STICH = dict((x.split('=')[0], int(x.split('=')[1])) for x in arg('stichprobe', '').split(',') if '=' in x)
os.makedirs(ZIEL, exist_ok=True)
D = json.load(open(os.path.join(LAUF, 'dokumente.json'), encoding='utf-8'))['dokumente']
try: FONT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 15)
except Exception: FONT = ImageFont.load_default()
ZW, ZH = 470, 560
for q in QU:
    ds = [d for d in D if d['quelle'] == q]
    if q in STICH and len(ds) > STICH[q]: ds = [ds[round(i * (len(ds) - 1) / (STICH[q] - 1))] for i in range(STICH[q])]
    for b in range(0, len(ds), JE):
        teil = ds[b:b + JE]; bogen = Image.new('RGB', (ZW * 5, ZH * ((len(teil) + 4) // 5)), (128, 128, 128))
        for i, d in enumerate(teil):
            zelle = Image.new('RGB', (ZW, ZH), (128, 128, 128)); x = 6
            seiten = [s for s in range(len(d.get('bilder', []))) if os.path.exists(os.path.join(LAUF, 'blatt', f"{d['id']}-{s}.png"))]
            for s in seiten:
                im = Image.open(os.path.join(LAUF, 'blatt', f"{d['id']}-{s}.png")).convert('RGB'); dr = ImageDraw.Draw(im)
                for f in d['funde']:
                    r = f.get('r')
                    if r and f.get('seite', 0) == s and f.get('art') != 'zeilen-kandidat': dr.rectangle([r['x'], r['y'], r['x'] + max(r['w'], 4), r['y'] + max(r['h'], 4)], outline=(255, 31, 90), width=5)
                im.thumbnail(((ZW - 12) // len(seiten) - 4, ZH - 52)); zelle.paste(im, (x, 6)); x += im.size[0] + 4
            dz = ImageDraw.Draw(zelle); dz.text((6, ZH - 44), f"{d['id']} {d['titel'][:52]}", fill=(255, 255, 255), font=FONT)
            dz.text((6, ZH - 24), f"{d.get('format')} · {'/'.join(x or '' for x in d.get('aufbau', []))} · {len([f for f in d['funde'] if f.get('art') != 'zeilen-kandidat'])} Funde", fill=(255, 225, 120), font=FONT)
            bogen.paste(zelle, ((i % 5) * ZW, (i // 5) * ZH))
        name = f"{q.lower()}-{b // JE + 1:02d}.jpg"; bogen.save(os.path.join(ZIEL, name), quality=80); print(name, len(teil))
