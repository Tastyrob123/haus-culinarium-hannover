#!/usr/bin/env python3
"""Führt die Teil-Inventare eines Werkzeugs zu einem Inventar zusammen (doppelte Zustände nach Kennung entfernt) und legt
Bilder und Stichproben daneben, so dass auswertung.py sie wie einen einzigen Lauf liest.  Aufruf: teile_zusammen.py <lauf>"""
import glob, json, os, shutil, sys
L = sys.argv[1]; ziele = {}
for d in sorted(glob.glob(os.path.join(L, '_teile', '*', '*', 'inventar.json'))):
    ziele.setdefault(os.path.basename(os.path.dirname(d)), []).append(os.path.dirname(d))
for k, teile in ziele.items():
    Z = os.path.join(L, k); os.makedirs(os.path.join(Z, 'bilder'), exist_ok=True)
    ges, sigs, weg = None, set(), set()
    for t in teile:
        j = json.load(open(os.path.join(t, 'inventar.json'), encoding='utf-8')); teil = os.path.basename(os.path.dirname(t))
        if ges is None: ges = dict(j, zustaende=[], kanten=[], nichtErreicht=[], fehler=[], voll=True, teile=[])
        for z in j['zustaende']:
            if z.get('fremd'): weg.add(z['id']); continue   # nur besucht, ein anderer Teil hat gemessen
            if z.get('sig') and z['sig'] in sigs: weg.add(z['id']); continue
            sigs.add(z.get('sig')); ges['zustaende'].append(z)
        for f in ('kanten', 'nichtErreicht', 'fehler'): ges[f] += j.get(f, [])
        ges['voll'] = ges['voll'] and bool(j.get('voll', True)); ges['teile'].append({'teil': teil, 'zustaende': len(j['zustaende'])})
        if os.path.isdir(os.path.join(t, 'bilder')): shutil.copytree(os.path.join(t, 'bilder'), os.path.join(Z, 'bilder'), dirs_exist_ok=True)
        for s in glob.glob(os.path.join(t, 'stich-*')):
            n = os.path.basename(s)
            if os.path.isdir(s): shutil.copytree(s, os.path.join(Z, n), dirs_exist_ok=True)
            elif n.endswith('.json'):
                sj = json.load(open(s, encoding='utf-8')); sj['zustaende'] = [z for z in sj['zustaende'] if z['id'] not in weg]
                json.dump(sj, open(os.path.join(Z, n[:-5] + '-' + teil + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(ges, open(os.path.join(Z, 'inventar.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(k, len(teile), 'Teile,', len(ges['zustaende']), 'Zustände,', len(weg), 'doppelt entfernt')
