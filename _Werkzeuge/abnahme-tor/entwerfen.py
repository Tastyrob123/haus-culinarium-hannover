#!/usr/bin/env python3
"""Muster aus «Entwerfen»: die Beispiel-Aufträge des Editors (IDEEN in studio.js), beantwortet von der Probe-Antwort des Werkstatt-Servers
(serve.py probe, mit Varianten: «Fünf Entwürfe anlegen»), ohne KI und ohne Kosten. Aufruf: python3 entwerfen.py <werkstatt-ordner> <aus.json>"""
import sys, os, json, re, importlib.util
WS, AUS = sys.argv[1], sys.argv[2]
os.chdir(WS); sys.argv = ['serve.py']
spec = importlib.util.spec_from_file_location('serve_tor', os.path.join(WS, 'serve.py')); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ideen = re.findall(r"^\s+'([^']+)',$", open('studio.js', encoding='utf-8').read().split('const IDEEN = [')[1].split('];')[0], re.M)
out = []
for t in ideen:
    r = m.probe({'haus': 'culinarium', 'auftrag': t, 'varianten': True})['entwuerfe']
    for i, v in enumerate(r['varianten']):
        out.append({'quelle': 'Entwerfen', 'gruppe': t, 'titel': f"{t[:60]} · Entwurf {i + 1}: {v['titel']}", 'format': r['format'], 'seiten': v['seiten']})
json.dump(out, open(AUS, 'w', encoding='utf-8'), ensure_ascii=False)
print('Entwerfen:', len(ideen), 'Aufträge,', len(out), 'Entwürfe')
