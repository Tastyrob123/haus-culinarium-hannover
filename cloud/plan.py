#!/usr/bin/env python3
"""Verteilt den Abnahmelauf auf Rechner: je Werkzeug-Teil ein Rechner (Teil-Inventar in WebKit 1440, danach die Stichproben
1280/1000/390 desselben Teils), je Werkzeug-Gruppe × Browser × Breite ein Messlauf-Rechner, je Ziel ein Bewegungs-Rechner."""
import json, os, sys
WS = os.environ.get('GITHUB_WORKSPACE') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = json.load(open(os.path.join(WS, 'cloud', 'haus.json'), encoding='utf-8'))
roh = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get('NUR', ''))
# Probe-Schalter in der Liste: «teile=3» nur die ersten drei Teile je Ziel, «nurtor» ohne Messlauf und Bewegung
woerter = [x.strip() for x in roh.split(',')]
TEILMAX = next((int(x[6:]) for x in woerter if x.startswith('teile=')), None)
NURTOR = 'nurtor' in woerter
roh = ','.join(x for x in woerter if not x.startswith('teile=') and x != 'nurtor')
nur = [x.strip() for x in roh.split(',') if x.strip()]
nur += [H.get('namen', {})[n] for n in list(nur) if n in H.get('namen', {})] + [a for a, b in H.get('namen', {}).items() if b in nur]
passt = lambda k: not nur or any(k == n or k.split('-')[0] == n for n in nur)
tor = list(dict.fromkeys(z['k'] for z in json.load(open(os.path.join(WS, H['tor_ziele']), encoding='utf-8'))['ziele'] if passt(z['k']) and z['k'] not in H.get('auslassen', [])))   # auslassen: Ziele, die ein anderes Ziel schon ganz abdeckt
# Teilgrösse aus den zuletzt gemessenen Zuständen (haus.json «zustaende», nach jedem Lauf aus zeiten.json nachgeführt): höchstens «zustaende_je_teil» je Rechner
import math
JE = H.get('zustaende_je_teil', 16)
teile = [{'k': k, 'zweig': f'{i}/{n}', 'name': f'{k}-z{i}'} for k in tor for n in [max(1, math.ceil(H.get('zustaende', {}).get(k, 1) / JE))] for i in range(1, n + 1) if not TEILMAX or i <= TEILMAX]
mess = json.load(open(os.path.join(WS, H['mess_ziele']), encoding='utf-8'))
mess = mess['ziele'] if isinstance(mess, dict) else mess
gruppen = {}
for z in mess:
    if passt(z['k']): gruppen.setdefault(z['k'].split('-')[0], []).append(z['k'])
messm = [{'gruppe': g, 'ks': ','.join(ks), 'browser': b, 'w': w} for g, ks in gruppen.items() for b in H['browser'] for w in H['mess_groessen']]
if NURTOR: messm, tor_bew = [], []
else: tor_bew = tor
aus = {'teile': json.dumps(teile), 'mess': json.dumps(messm), 'bewegung': json.dumps(tor_bew),
       'anzahl': str(len(teile) + len(messm) + len(tor_bew))}
for k, v in aus.items(): print(f'{k}={v}')
if os.environ.get('GITHUB_OUTPUT'):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        for k, v in aus.items(): f.write(f'{k}={v}\n')
