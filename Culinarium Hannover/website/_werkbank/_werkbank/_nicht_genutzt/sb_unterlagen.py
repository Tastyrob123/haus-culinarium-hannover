#!/usr/bin/env python3
"""Seite «Unterlagen» des Schlössli (Station 10): setzt die Fächer aus den gesetzten Karten und baut die Seite mit dem Kit.
   python3 _werkbank/sb_unterlagen.py "<website>"   →  unterlagen/index.html (Kit unterlagen.py)
   Vorher: satz.py, satz_druck.js, satz_pruefe.py (alle sechs ohne Abweichung)."""
import os, sys
sys.path.insert(0, os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit'))
import kern as K
K.H.FAECHER = [('speisekarte', 'Die Karte nach Ländern'), ('weinkarte', 'Weinkarte'), ('laestermeile', 'Lästermeile'), ('bankett', 'Bankettmenü')]
K.H.UNTERLAGEN.setdefault('pflege', ('Karten selbst ändern in La Carte', 'http://127.0.0.1:8970/werkzeuge/karten/?haus=schloessli'))
import unterlagen
unterlagen.baue()
ziel = os.path.join(K.ROOT, 'unterlagen', 'index.html')
t = open(ziel, encoding='utf-8').read().replace(f'Unterlagen des {K.H.NAME}', f'Unterlagen der {K.H.NAME}')   # die Wirtschaft
open(ziel, 'w', encoding='utf-8').write(t)
print('Unterlagen-Seite:', ziel)
