#!/usr/bin/env python3
"""Gegenprobe «Das weiss der Chat» ↔ Website des Culinarium (28.10.2026, Muster Schäfli): stimmt jede Zeile des Steckbriefs noch mit der Website?
Liest steckbrief.json und den Wortlaut der Website, wie ihn ein Gast sieht (_bau/website-text/*.txt; vorher frisch holen:
node _werkzeuge/reception/_bau/website_text.js), dazu website/bar.html (das Fenster der Bar-Seite zeigt seinen Satz erst beim Scrollen) und
gast/gast_umgebung.txt (Vorverkauf laut Instagram, Kontaktwege). Jeder Beleg muss dort wörtlich stehen; dazu die Kernangaben einzeln
(Telefon, Adresse, Zeiten, Preis, Plätze, Instagram). Rot heisst: die Website hat sich geändert, Wissen neu bauen (_bau/culinarium_wissen.py,
steckbrief_bau.py). Aufruf: python3 _werkzeuge/reception/pruefung/steckbrief_gegen_website.py"""
import json, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PROJ = os.path.dirname(os.path.dirname(C))
norm = lambda t: re.sub(r'\s+', ' ', t).strip()
web = norm(' '.join(open(os.path.join(C, '_bau', 'website-text', f), encoding='utf-8').read() for f in os.listdir(os.path.join(C, '_bau', 'website-text')) if f.endswith('.txt')))
bar = norm(re.sub(r'<[^>]+>', ' ', open(os.path.join(PROJ, 'website', 'bar.html'), encoding='utf-8').read()))
umg = norm(open(os.path.join(C, 'gast', 'gast_umgebung.txt'), encoding='utf-8').read())
alle = web + ' ' + bar + ' ' + umg
sb = json.load(open(os.path.join(C, 'steckbrief.json'), encoding='utf-8'))
rot, n = [], 0
for b in sb['bereiche']:
    for g in b['gruppen']:
        for z in g['zeilen']:
            for bl in [z['beleg']] + z.get('mehr', []):
                n += 1
                if bl not in alle:
                    rot.append(f"{b['bereich']} / {z['was']}: «{bl[:70]}»")
KERN = [('Telefon der Bar', '+49 163 3909578', web), ('Adresse', 'Haasemannstraße 13', web), ('PLZ', '30449 Hannover', web),
        ('Freitag ab 19 Uhr', 'Freitag ab 19 Uhr', web), ('Samstag ab 17 Uhr', 'Samstag ab 17 Uhr', web), ('Preis zuletzt', '89,00 EUR', web),
        ('Vierzehn Plätze', 'vierzehn Plätze pro Abend', web), ('Termin offen', 'Der nächste Termin steht noch nicht fest', web),
        ('Bar Donnerstag', 'Donnerstag 19 bis 1 Uhr', web), ('Bar Freitag und Samstag', 'Freitag und Samstag 19 bis 2 Uhr', web),
        ('Rückgabe', 'Tickets nicht rückerstattet werden können', web), ('Instagram Culinarium', '@culinarium_hannover', web),
        ('Instagram Dirty Chicken', '@dirtychicken.hannover', web), ('Plus Code', '9PC7+49 Hannover', web)]
for was, t, q in KERN:
    if t not in q:
        rot.append(f'Kern {was}: «{t}» nicht auf der Website')
print(f'{n} Belege, {len(KERN)} Kernangaben: ' + ('alle auf der Website' if not rot else f'{len(rot)} rot'))
for r in rot:
    print('ROT', r)
sys.exit(1 if rot else 0)
