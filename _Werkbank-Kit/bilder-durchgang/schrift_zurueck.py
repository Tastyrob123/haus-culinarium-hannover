#!/usr/bin/env python3
"""Schrift im Bild aus dem echten Foto zurücksetzen, mit dem Ton des überarbeiteten Bildes.
   python3 schrift_zurueck.py original.jpg ueberarbeitet.png x0,y0,x1,y1 [x0,y0,x1,y1 ...]   (Kasten in Anteilen 0 bis 1, überschreibt die PNG)"""
import sys
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageDraw
org_p, neu_p, kasten = sys.argv[1], sys.argv[2], [tuple(float(v) for v in k.split(',')) for k in sys.argv[3:]]
neu = Image.open(neu_p).convert('RGB'); W, H = neu.size
org = ImageOps.exif_transpose(Image.open(org_p)).convert('RGB').resize((W, H), Image.LANCZOS)
a = np.asarray(org).astype(np.float32); b = np.asarray(neu).astype(np.float32)
ta = np.asarray(org.filter(ImageFilter.GaussianBlur(24))).astype(np.float32) + 1; tb = np.asarray(neu.filter(ImageFilter.GaussianBlur(24))).astype(np.float32) + 1
m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
for x0, y0, x1, y1 in kasten: d.rectangle([int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)], fill=255)
mm = (np.asarray(m.filter(ImageFilter.GaussianBlur(8))).astype(np.float32) / 255)[..., None]
Image.fromarray((np.clip(a * tb / ta, 0, 255) * mm + b * (1 - mm)).astype(np.uint8)).save(neu_p)
