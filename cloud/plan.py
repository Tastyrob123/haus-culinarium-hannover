#!/usr/bin/env python3
"""Verteilt den Abnahmelauf auf Rechner: je Werkzeug ein Inventar-Rechner, je Werkzeug und Breite ein Stichproben-Rechner,
je Werkzeug-Gruppe, Browser und Breite ein Messlauf-Rechner. Schreibt die Listen für GitHub Actions (GITHUB_OUTPUT)."""
import json, os, sys
WS = os.environ.get('GITHUB_WORKSPACE') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = json.load(open(os.path.join(WS, 'cloud', 'haus.json'), encoding='utf-8'))
nur = [x.strip() for x in (sys.argv[1] if len(sys.argv) > 1 else os.environ.get('NUR', '')).split(',') if x.strip()]
passt = lambda k: not nur or any(k == n or k.startswith(n + '-') or k.split('-')[0] == n for n in nur)
tor = [z['k'] for z in json.load(open(os.path.join(WS, H['tor_ziele']), encoding='utf-8'))['ziele']]
tor = list(dict.fromkeys(k for k in tor if passt(k)))
mess = json.load(open(os.path.join(WS, H['mess_ziele']), encoding='utf-8'))
mess = mess['ziele'] if isinstance(mess, dict) else mess
gruppen = {}
for z in mess:
    if passt(z['k']): gruppen.setdefault(z['k'].split('-')[0], []).append(z['k'])
stich = [{'k': k, 'g': g} for k in tor for g in H['tor_groessen']]
messm = [{'gruppe': g, 'ks': ','.join(ks), 'browser': b, 'w': w} for g, ks in gruppen.items() for b in H['browser'] for w in H['mess_groessen']]
aus = {'tor': json.dumps(tor), 'stich': json.dumps(stich), 'mess': json.dumps(messm),
       'anzahl': str(len(tor) + len(stich) + len(messm))}
for k, v in aus.items(): print(f'{k}={v}')
if os.environ.get('GITHUB_OUTPUT'):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        for k, v in aus.items(): f.write(f'{k}={v}\n')
