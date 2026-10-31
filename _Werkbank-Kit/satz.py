#!/usr/bin/env python3
"""Schreibt die Satzdateien der Unterlagen: python3 satz.py "<Projektordner>"  → _werkbank/satz/u-<ziel>.html + unterlagen.json"""
import json, os
import kern as K
from kern import H, W
import satz_daten as D   # im Projekt: _werkbank/satz_daten.py

SATZ = os.path.join(W, 'satz'); os.makedirs(SATZ, exist_ok=True)
css = open(os.path.join(K.KIT, 'satz.css'), encoding='utf-8').read()
t = H.SCHRIFT['titel']
kopf = K.druckschrift_css()
kopf += f":root{{--titel:'{t[0]}',{H.SCHRIFT.get('titel_folge', 'Georgia,serif')};--tg:{H.SCHRIFT.get('druckgewicht', 400)};--muster:{H.MUSTER};--musterb:{getattr(H, 'MUSTER_DRUCK', '40mm')}}}\n"
K.schreib(os.path.join(SATZ, 'satz.css'), kopf + K.faerbe(css) + getattr(H, 'CSS_SATZ', ''))
plan = []
for d in D.DOKS:
    b, h = d['format'] or ((297, 210) if d['quer'] else (210, 297))
    doc = f'''<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><title>{K.e(d['name'])} · {K.e(H.NAME)}</title>
<link rel="stylesheet" href="satz.css"><style>@page{{size:{b}mm {h}mm;margin:0}}</style></head><body>{''.join(d['seiten'])}</body></html>'''
    K.schreib(os.path.join(SATZ, 'u-' + d['ziel'] + '.html'), doc)
    plan.append({'ziel': d['ziel'], 'quelle': d['quelle'], 'name': d['name'], 'gruppe': d['gruppe'], 'seiten': len(d['seiten']), 'b': b, 'h': h, 'dazu': d['dazu'], 'fehlt': d['fehlt'],
                 # wenn die Idee weniger Seiten hat als das Original (GBR seit 11.10.2026): je neue Seite die Seite des Originals, die daneben gezeigt wird
                 **({'alt_seiten': d['alt_seiten']} if d.get('alt_seiten') else {})})
    print('gesetzt:', d['ziel'], len(d['seiten']), 'Seiten')
json.dump(plan, open(os.path.join(W, 'unterlagen.json'), 'w'), ensure_ascii=False, indent=1)
