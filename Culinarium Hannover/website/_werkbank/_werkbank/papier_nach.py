#!/usr/bin/env python3
"""Nach papier_seiten.py (Kit): Untersetzer-Seite in den Worten des Hauses (Tor 4, 30.10.2026). Gleich grosse Stücke heissen «je 94 mm» statt
«94 bis 94 mm», Du statt Sie, ß wie auf den anderen Seiten. Aufruf: python3 _werkbank/papier_nach.py (im Ordner website/_werkbank)."""
import os, re
HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for ordner in ('untersetzer', 'drucksachen'):
    p = os.path.join(HIER, ordner, 'index.html')
    if not os.path.exists(p):
        continue
    t = open(p, encoding='utf-8').read()
    n = re.sub(r'(\d+) bis \1 mm', r'je \1 mm', t).replace('und Ihre Unterlagen im selben Stil', 'und eure Unterlagen im selben Stil').replace('Originalgrösse', 'Originalgröße')
    if n != t:
        open(p, 'w', encoding='utf-8').write(n)
        print('papier-nach:', ordner)
