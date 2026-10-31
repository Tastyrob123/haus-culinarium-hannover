#!/usr/bin/env python3
"""La Carte · Culinarium Hannover: feste Schnitte aus den variablen Schriften der Website (28.10.2026, Muster der Tafel im Schäfli).
Chromium bettet variable Schriften im PDF als «Type 3» ein; die Apple-Vorschau zeigt sie dann weich (Fehlerbuch 10a, 21.10.2026). Darum setzt der
Satz feste Schnitte (TrueType je Stärke, aus der variablen Schrift der Website instanziiert, Lizenz SIL OFL wie das Original).
Fraunces mit weichen Enden wie die Website (SOFT 100), Titel mit WONK 1 und grosser optischer Grösse, Rudis Zeilen ohne WONK (ruhige Versalien).
    python3 _werkzeuge/carte/fonts_statisch.py      → fonts/Fraunces-<schnitt>.ttf, fonts/Instrument-<stärke>.ttf, fonts/Urbanist-<stärke>.ttf, fonts/DMMono-400.ttf
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HIER = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HIER, 'fonts')
Q = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website', 'assets', 'schrift')
SCHNITTE = {
    'fraunces-soft.woff2': [('Fraunces-titel-340', {'wght': 340, 'opsz': 144, 'SOFT': 100, 'WONK': 1}),
                            ('Fraunces-zeile-320', {'wght': 320, 'opsz': 48, 'SOFT': 100, 'WONK': 0}),
                            ('Fraunces-zeile-400', {'wght': 400, 'opsz': 48, 'SOFT': 100, 'WONK': 0})],
    'instrument.woff2': [('Instrument-400', {'wght': 400}), ('Instrument-500', {'wght': 500})],
    'urbanist.woff2': [('Urbanist-500', {'wght': 500}), ('Urbanist-600', {'wght': 600})],
}
if __name__ == '__main__':
    os.makedirs(F, exist_ok=True)
    for quelle, liste in SCHNITTE.items():
        for name, achsen in liste:
            t = TTFont(os.path.join(Q, quelle))
            s = instancer.instantiateVariableFont(t, achsen, updateFontNames=False)
            s.flavor = None
            s.save(os.path.join(F, name + '.ttf'))
            print(name)
    t = TTFont(os.path.join(Q, 'dmmono.woff2')); t.flavor = None; t.save(os.path.join(F, 'DMMono-400.ttf')); print('DMMono-400')
