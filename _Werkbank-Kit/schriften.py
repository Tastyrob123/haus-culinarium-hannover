#!/usr/bin/env python3
"""Feste Schriftschnitte für den Druck: python3 schriften.py "<Projektordner>"  →  _werkbank/fonts/*.ttf
   Variable Schriften schreibt Chromium als «Type 3» in die PDF, die Apple-Vorschau zeichnet sie weich. Mit festen
   TrueType-Schnitten bleibt die Schrift scharf. Prüfen: pdffonts <datei.pdf> (kein «Type 3»).
   H.DRUCKQUELLEN = [(Quelle in assets/fonts, Zielname ohne .ttf, Gewicht oder None für «wie sie ist»)]"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
import kern as K
from kern import H, ROOT, W

Z = os.path.join(W, 'fonts'); os.makedirs(Z, exist_ok=True)
NAME = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold'}
STD = [('InstrumentSans-normal-400_600.woff2', 'InstrumentSans-Regular', 400), ('InstrumentSans-normal-400_600.woff2', 'InstrumentSans-Medium', 500), ('InstrumentSans-normal-400_600.woff2', 'InstrumentSans-SemiBold', 600), ('DMMono-normal-400.woff2', 'DMMono-Regular', None)]
for quelle, ziel, g in STD + list(H.DRUCKQUELLEN):
    q = os.path.join(ROOT, 'assets', 'fonts', quelle)
    if not os.path.exists(q):
        q = os.path.join(K.KIT, 'fonts', quelle)
    f = TTFont(q)
    if g and 'fvar' in f:
        f = instancer.instantiateVariableFont(f, {'wght': g}, inplace=False)
        fam = ziel.split('-')[0]
        for rec in f['name'].names:
            if rec.nameID in (1, 16): rec.string = fam + ' Druck'
            if rec.nameID in (2, 17): rec.string = NAME[g]
            if rec.nameID in (4,): rec.string = f'{fam} Druck {NAME[g]}'
            if rec.nameID in (6,): rec.string = f'{fam}Druck-{NAME[g]}'
        f['OS/2'].usWeightClass = g
    f.flavor = None
    f.save(os.path.join(Z, ziel + '.ttf'))
    print(ziel + '.ttf', os.path.getsize(os.path.join(Z, ziel + '.ttf')) // 1024, 'KB', 'variabel' if 'fvar' in f else 'fest')
