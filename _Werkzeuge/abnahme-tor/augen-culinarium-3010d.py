#!/usr/bin/env python3
"""Augen-Urteile der Augenprüfung vom 30.10.2026 (Lauf dok-3010d), über Titel/ID an die Dokumente gebunden.
Angesehen: alle 117 Vorlagen, alle 39 Vorschläge, alle 40 Entwerfen-Muster, Stichprobe 60 Muster und 30 Arten (Kontaktbögen bogen/).
Aufruf: python3 augen-culinarium-3010.py <lauf> <augen.json>"""
import json, sys, re
LAUF, AUS = sys.argv[1], sys.argv[2]
D = json.load(open(LAUF + '/dokumente.json', encoding='utf-8'))['dokumente']
A_KRIT = [7, 8, 10, 11, 13, 14, 19, 20, 22, 23, 25, 29]
FUNDE = [   # Lauf dok-3010d (dokumente.js v105, vorlagen.js v49): kein Augen-Fund
]
ANGESEHEN_ALLE = {'Vorlage', 'Vorschlag', 'Entwerfen'}
augen = {}; n = 0
for q in ('Muster', 'Art'):
    for k in A_KRIT: augen[f'{q}/*/{k}'] = {'urteil': 'gruen', 'notiz': 'Auge an der Stichprobe (60 Muster, 30 Arten), kein Fund'}
for d in D:
    if d['quelle'] in ANGESEHEN_ALLE:
        for k in A_KRIT: augen[f"{d['quelle']}/{d['id']}/{k}"] = {'urteil': 'gruen', 'notiz': 'Auge am Kontaktbogen, kein Fund'}
    for q, muster, k, notiz in FUNDE:
        if re.fullmatch(q, d['quelle']) and re.search(muster, d['titel'] or '') and not (k == 7 and d['quelle'] == 'Entwerfen' and 'An der langen' not in json.dumps(d, ensure_ascii=False) and 'Plakat für den nächsten Abend' not in d['titel']):
            augen[f"{d['quelle']}/{d['id']}/{k}"] = {'urteil': 'rot', 'notiz': notiz}; n += 1
json.dump(augen, open(AUS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(augen), 'Urteile,', n, 'Augen-Funde')
