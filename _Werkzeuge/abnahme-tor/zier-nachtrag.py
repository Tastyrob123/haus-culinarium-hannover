#!/usr/bin/env python3
"""Überträgt die Funde zu Kriterium 24 (oder mit --art die Funde einer Art, z. B. wortbruch) aus einem Nachlauf ohne Bilder (dok-tor.js --ohne-bilder) in einen Hauptlauf; Zuordnung über Quelle, Titel, Format, Aufbau.
Aufruf: python3 zier-nachtrag.py <hauptlauf> <nachlauf>"""
import json, sys, os
H, N = sys.argv[1], sys.argv[2]
key = lambda d: (d['quelle'], d['titel'], d.get('format'), tuple(d.get('aufbau') or []), tuple(d.get('ton') or []))
HD = json.load(open(os.path.join(H, 'dokumente.json'), encoding='utf-8')); ND = json.load(open(os.path.join(N, 'dokumente.json'), encoding='utf-8'))
ART = sys.argv[sys.argv.index('--art') + 1] if '--art' in sys.argv else None
wahl = (lambda f: f.get('art') == ART) if ART else (lambda f: f.get('k') == 24)
neu = {key(d): [f for f in d['funde'] if wahl(f)] for d in ND['dokumente']}
n = fehlt = 0
for d in HD['dokumente']:
    k = key(d)
    if k not in neu: fehlt += 1; continue
    d['funde'] = [f for f in d['funde'] if not wahl(f)] + neu[k]; n += len(neu[k])
json.dump(HD, open(os.path.join(H, 'dokumente.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(n, 'Funde', ART or 'zu Kriterium 24', 'übertragen;', fehlt, 'Dokumente ohne Gegenstück im Nachlauf')
