#!/usr/bin/env python3
"""Werkbank Culinarium: «Heute und neu» ohne heutige Website (Werkbank-Chat 28.10.2026). Culinarium steht heute nur auf Instagram; als «heute»
dienen die Aufnahmen des Spähers vom 25.10.2026 (_qa/spaeher/, Rechner 1440 × 900 doppelt dicht, ohne Anmeldung, Cookie-Fenster abgelehnt),
als «neu» die Aufnahmen der neuen Seite (ansichten/Rechner, ansicht_lang.js). Nichts wird online abgerufen.
   python3 _werkbank/sb_heute.py  → ansichten/Vorher/<slug>-alt.jpg und <slug>-neu.jpg (gelesen von H.VORHER im Kit-Bau)"""
import os, shutil
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__))
SP = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(W))), '_qa', 'spaeher')
Z = os.path.join(W, 'ansichten', 'Vorher')
PAARE = [('startseite', 'ig-profil-rechner.jpg', 'Rechner/Startseite.jpg'),
         ('abend', 'ig-post-DbYnkdkjrNy.jpg', 'Rechner/Der Abend.jpg'),
         ('abende', 'ig-post-DVjkofijp6R.jpg', 'Rechner/Alle Abende.jpg')]


def bau():
    os.makedirs(Z, exist_ok=True)
    for slug, alt, neu in PAARE:
        a, n = os.path.join(SP, alt), os.path.join(W, 'ansichten', neu)
        if not (os.path.exists(a) and os.path.exists(n)):
            print('fehlt', slug); continue
        im = Image.open(n).convert('RGB')
        if im.width < 2880:   # beide Hälften gleich groß, sonst springt der Schieber
            im = im.resize((2880, round(im.height * 2880 / im.width)), Image.LANCZOS)
        im.save(os.path.join(Z, slug + '-neu.jpg'), quality=90)
        shutil.copy2(a, os.path.join(Z, slug + '-alt.jpg'))
        print('Vorher', slug)
    os.makedirs(os.path.join(W, 'ansichten', 'Heute'), exist_ok=True)   # der Kit zeigt den Vergleich nur, wenn es «heute» gibt
    shutil.copy2(os.path.join(SP, 'ig-profil-rechner.jpg'), os.path.join(W, 'ansichten', 'Heute', 'Startseite.jpg'))


if __name__ == '__main__':
    bau()
