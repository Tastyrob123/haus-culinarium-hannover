#!/usr/bin/env python3
"""Abnahme-Tor · Vergleich zweier Läufe je Werkzeug: findet der neue Lauf jede Fundstelle des alten wieder?
Eine Fundstelle = Art + Stelle (Selektor) + Meldung ohne Zahlen, über alle Breiten. Dazu Zustände und Dauer.
Aufruf: python3 vergleich.py <lauf-alt> <lauf-neu> [k …]    (Lauf-Ordner mit <k>/inventar.json und <k>/stich-*.json)"""
import json, glob, os, re, sys, collections
ALT, NEU = sys.argv[1], sys.argv[2]; KS = sys.argv[3:]
def stellen(lauf, k):
    S = collections.Counter(); zs = 0; breiten = set()
    for f in [os.path.join(lauf, k, 'inventar.json')] + glob.glob(os.path.join(lauf, k, 'stich-*.json')):
        if not os.path.exists(f): continue
        I = json.load(open(f, encoding='utf-8')); w = I['groesse'][0]; breiten.add(w)
        if f.endswith('inventar.json'): zs = len(I['zustaende'])
        for z in I['zustaende']:
            for x in z.get('funde', []):
                if not x.get('k'): continue
                S[(x['art'], re.sub(r'\d+', '#', x.get('sel') or ''), re.sub(r'[\d.,]+', '#', x.get('info') or '')[:70])] += 1
    return S, zs, breiten
ks = KS or sorted({os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ALT, '*', 'inventar.json'))})
ges = {'alt': 0, 'wieder': 0, 'neu': 0}
for k in ks:
    a, za, ba = stellen(ALT, k); n, zn, bn = stellen(NEU, k)
    if not za and not zn: continue
    wieder = [s for s in a if s in n]; fehlt = [s for s in a if s not in n]; dazu = [s for s in n if s not in a]
    ges['alt'] += len(a); ges['wieder'] += len(wieder); ges['neu'] += len(dazu)
    print(f"== {k}: alt {za} Zustände ({'/'.join(map(str, sorted(ba, reverse=True)))}) → neu {zn} Zustände ({'/'.join(map(str, sorted(bn, reverse=True)))}) · Fundstellen alt {len(a)}, davon wiedergefunden {len(wieder)}, fehlen {len(fehlt)}, neu dazu {len(dazu)}")
    for s in fehlt[:12]: print(f"   FEHLT  {s[0]:12} {s[1][:50]:50} {s[2][:60]}")
    for s in dazu[:6]: print(f"   dazu   {s[0]:12} {s[1][:50]:50} {s[2][:60]}")
print(f"SUMME: Fundstellen alt {ges['alt']}, wiedergefunden {ges['wieder']}, neu dazu {ges['neu']}")
