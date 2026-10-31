#!/usr/bin/env python3
"""Feste Druckschnitte von Fraunces und Urbanist für Culinarium (Werkbank-Chat 28.10.2026). Der Kit (schriften.py) setzt nur die Achse «wght» fest
und kennt keine Gewichte unter 400; Fraunces hat dazu SOFT, opsz und WONK. Hier werden alle Achsen fest gesetzt wie auf der Website
(SOFT 100, WONK 0, opsz 36), sonst schreibt Chromium die Schrift als «Type 3» in die PDF.   python3 _werkbank/druckschrift.py → _werkbank/fonts/*.ttf"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

W = os.path.dirname(os.path.abspath(__file__))
Q = os.path.join(os.path.dirname(os.path.dirname(W)), 'assets', 'schrift')
Z = os.path.join(W, 'fonts'); os.makedirs(Z, exist_ok=True)
SCHNITTE = [('fraunces-soft.woff2', 'Fraunces-Light', 'Fraunces Druck', 'Light', dict(wght=340, SOFT=100, WONK=0, opsz=36)),
            ('fraunces-soft.woff2', 'Fraunces-Regular', 'Fraunces Druck', 'Regular', dict(wght=420, SOFT=100, WONK=0, opsz=36)),
            ('urbanist.woff2', 'Urbanist-Medium', 'Urbanist Druck', 'Medium', dict(wght=500)),
            ('urbanist.woff2', 'Urbanist-SemiBold', 'Urbanist Druck', 'SemiBold', dict(wght=600))]


def bau():
    for quelle, ziel, fam, stil, achsen in SCHNITTE:
        f = instancer.instantiateVariableFont(TTFont(os.path.join(Q, quelle)), achsen, inplace=False)
        for rec in f['name'].names:
            if rec.nameID in (1, 16): rec.string = fam
            if rec.nameID in (2, 17): rec.string = stil
            if rec.nameID == 4: rec.string = f'{fam} {stil}'
            if rec.nameID == 6: rec.string = f'{fam.replace(" ", "")}-{stil}'
        f['OS/2'].usWeightClass = achsen['wght']
        f.flavor = None
        f.save(os.path.join(Z, ziel + '.ttf'))
        print(ziel + '.ttf', 'variabel' if 'fvar' in f else 'fest')


if __name__ == '__main__':
    bau()
