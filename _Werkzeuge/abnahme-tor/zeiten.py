#!/usr/bin/env python3
"""Abnahme-Tor (schnell) · Messwerte eines Laufs: Zustände, Dauer, Sekunden je Zustand, Rückwege, gleiche Layouts.
Aufruf: python3 zeiten.py <lauf-ordner>"""
import json, glob, os, sys, statistics
LAUF = sys.argv[1]
ges = {'zustaende': 0, 'min': 0.0, 'gleich': 0, 'nachgespielt': 0, 'funde': 0}
print(f"{'Werkzeug':28} {'Zust.':>5} {'min':>6} {'s/Zust':>7} {'gleich':>6} {'nachgesp.':>9} {'Funde 1440':>10} {'alle Breiten':>12}")
for inv in sorted(glob.glob(os.path.join(LAUF, '*', 'inventar.json'))):
    I = json.load(open(inv, encoding='utf-8')); k = os.path.basename(os.path.dirname(inv)); zs = I['zustaende']
    if not zs: continue
    m = I.get('dauerMin') or 0
    funde = sum(len(z.get('funde', [])) for z in zs)
    alle = funde
    for st in glob.glob(os.path.join(os.path.dirname(inv), 'stich-*.json')):
        alle += sum(len(z.get('funde', [])) for z in json.load(open(st, encoding='utf-8'))['zustaende'])
    gleich = sum(1 for z in zs if z.get('gleichWie'))
    ng = (I.get('zaehler') or {}).get('nachgespielt', '')
    print(f"{k:28} {len(zs):5} {m:6.1f} {60 * m / len(zs):7.1f} {gleich:6} {str(ng):>9} {funde:10} {alle:12}")
    ges['zustaende'] += len(zs); ges['min'] += m; ges['gleich'] += gleich; ges['funde'] += alle; ges['nachgespielt'] += ng or 0
print(f"{'SUMME':28} {ges['zustaende']:5} {ges['min']:6.1f} {60 * ges['min'] / max(1, ges['zustaende']):7.1f} {ges['gleich']:6} {ges['nachgespielt']:9} {'':10} {ges['funde']:12}")
print(f"Rechnerzeit aller Tore: {ges['min']:.0f} min (nacheinander); Uhrzeit mit 3 parallel siehe lauf.out")
