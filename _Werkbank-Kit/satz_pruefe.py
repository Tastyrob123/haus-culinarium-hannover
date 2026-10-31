#!/usr/bin/env python3
"""Vergleicht den Wortlaut jeder neu gesetzten Unterlage mit dem Original des Hauses.
   python3 satz_pruefe.py "<Projektordner>" [ziel …]   Meldet je Unterlage, was im neuen Blatt fehlt und was dazugekommen ist.
   Gezählt werden nur Buchstaben und Ziffern, Gross/Klein egal. Zusätzlich ein Zeichenvergleich ohne Leerzeichen,
   weil Originale Wörter über Stücke verteilen. Bewusste Abweichungen stehen je Unterlage in dazu/fehlt (satz_daten.py)."""
import collections, json, os, re, subprocess, sys, unicodedata
import kern as K
from kern import ROOT, W

MUSTER = r'[0-9a-zäöüéèêëàâîïôùûçœß]+'


def text(pfad):
    t = subprocess.run(['pdftotext', pfad, '-'], capture_output=True, text=True).stdout
    t = unicodedata.normalize('NFC', t).replace('\xa0', ' ').replace('\xad', '')
    for a, b in (('ﬁ', 'fi'), ('ﬂ', 'fl'), ('ﬀ', 'ff'), ('ﬃ', 'ffi'), ('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'), ('«', '"'), ('»', '"'), ('➢', ' ')):
        t = t.replace(a, b)
    t = re.sub(r'[\ue000-\uf8ff]', ' ', t)   # Zeichen aus Symbolschriften (Pfeile, Aufzählungspunkte)
    return re.sub(r'_{3,}', ' ', t)


W_ = lambda t: collections.Counter(re.findall(MUSTER, unicodedata.normalize('NFC', t).lower()))
plan = json.load(open(os.path.join(W, 'unterlagen.json')))
nur = [a for a in sys.argv[2:]]
gut = 0
for d in plan:
    if nur and d['ziel'] not in nur:
        continue
    alt_t, neu_t = text(os.path.join(ROOT, d['quelle'])), text(os.path.join(ROOT, 'unterlagen', 'pdf', d['ziel'] + '.pdf'))
    alt, neu = W_(alt_t) - W_(d['fehlt']), W_(neu_t) - W_(d['dazu'])
    fehlt, dazu = alt - neu, neu - alt
    # zweiter Blick ohne Leerzeichen: gleiche Zeichenfolge heisst nur anders getrennt
    za = collections.Counter(''.join(sorted((alt - neu).elements())))
    zn = collections.Counter(''.join(sorted((neu - alt).elements())))
    np_alt = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', os.path.join(ROOT, d['quelle'])], capture_output=True, text=True).stdout).group(1))
    np_neu = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', os.path.join(ROOT, 'unterlagen', 'pdf', d['ziel'] + '.pdf')], capture_output=True, text=True).stdout).group(1))
    ok = not fehlt and not dazu
    nur_trennung = (not ok) and za == zn
    gut += ok or nur_trennung
    print(f"── {d['ziel']}: {sum(alt.values())} Wörter im Original, {sum(neu.values())} neu · Seiten {np_alt} → {np_neu}" + ('' if np_alt == np_neu else '  ← SEITENZAHL WEICHT AB') + ('  ✓ Wortlaut gleich' if ok else ('  ✓ gleich bis auf Trennung' if nur_trennung else '')))
    if not ok and not nur_trennung:
        if fehlt: print('   fehlt im neuen Blatt:', ' '.join(f'{k}×{v}' if v > 1 else k for k, v in sorted(fehlt.items())))
        if dazu: print('   neu dazugekommen:   ', ' '.join(f'{k}×{v}' if v > 1 else k for k, v in sorted(dazu.items())))
print(f'{gut} von {len([d for d in plan if not nur or d["ziel"] in nur])} ohne Abweichung')
