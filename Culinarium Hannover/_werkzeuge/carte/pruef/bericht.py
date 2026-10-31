#!/usr/bin/env python3
"""Die Tafel (La Carte) · Berghotel Gasterntal — Prüfbericht aus pruef/aus/ (ergebnis.json je Bedienlauf, Protokolle .txt) nach PRUEFUNG-2026-10-17.md.
    python3 _werkzeuge/carte/pruef/bericht.py"""
import datetime, glob, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HIER, 'aus')
ZIEL = os.path.join(os.path.dirname(HIER), 'PRUEFUNG-2026-10-17.md')


def letzte(f):
    try:
        z = [x for x in open(os.path.join(A, f), encoding='utf-8', errors='replace').read().strip().splitlines() if x.strip()]
        return z[-1] if z else ''
    except OSError:
        return 'fehlt'


laeufe, zeilen = [], {}
for f in sorted(glob.glob(os.path.join(A, 'lauf-*', 'ergebnis.json')), key=lambda x: (('chromium', 'webkit', 'firefox').index(x.split('lauf-')[1].split('-')[0]), -int(re.search(r'-(\d+)/', x).group(1)))):
    e = json.load(open(f))
    k = f"{ {'chromium': 'Chromium', 'webkit': 'Safari-Kern', 'firefox': 'Firefox'}[e['browser']]} {e['breite']}×{e['hoehe']}"
    laeufe.append((k, e['gruen'], e['gesamt']))
    for z in e['zeilen']:
        zeilen.setdefault((z['id'], z['n']), {})[k] = z['ok']
w = []
w.append('# Prüfbericht Die Tafel (La Carte) · Berghotel Gasterntal (Bau-Chat, 17.10.2026)\n')
w.append(f'Erzeugt {datetime.datetime.now():%d.%m.%Y %H:%M} aus `pruef/aus/` mit `pruef/bericht.py`. Alle Läufe mit Wegwerf-Daten auf dem eigenen Port 8971 an der Probe-Kopie «_Probe Gasterntal Carte 1710»; das Werkzeug des Hauses und die Website blieben unberührt (Anschluss nur an einer APFS-Kopie). Die unabhängige Abnahme macht ein Prüf-Chat.\n')
w.append('## Bedienung im Browser (`pruef/lauf.js`, jede Zeile der Funktionsliste gedrückt)\n')
w.append('| Browser und Fenster | grün |\n|---|---|')
for k, g, n in laeufe:
    w.append(f'| {k} | {g} von {n} |')
rot = [(i, n, [k for k, v in r.items() if not v]) for (i, n), r in zeilen.items() if not all(r.values())]
w.append('\nZeilen mit Rot: ' + (str(len(rot)) if rot else 'keine') + '\n')
for i, n, ks in rot:
    w.append(f'- {i} {n}: {", ".join(ks)}')
w.append('\n## Weitere Prüfungen\n')
w.append('| Prüfung | Ergebnis |\n|---|---|')
for name, f in [('Rundlauf, Wortlaut gegen die Originale, Druck gegen die PDFs der Website (`pruefe.py alles`)', 'pruefe.txt'),
                ('Vorschau = PDF, Chromium (`gleich.js`)', 'gleich-chromium.txt'), ('Vorschau = PDF, Safari-Kern', 'gleich-webkit.txt'),
                ('Online-Fassung auf dem Rechner (`online_probe.js`)', 'online-chromium.txt'), ('Anschluss an die Website an einer APFS-Kopie (`anschluss.js`)', 'anschluss.txt'),
                ('Flüssigkeit Chromium, ungebremst und gedrosselt 4×/6× (`fluessig.js`)', 'fluessig-chromium.txt'), ('Flüssigkeit Safari-Kern', 'fluessig-webkit.txt')]:
    w.append(f'| {name} | {letzte(f)} |')
for f in ('pruefe.txt', 'fluessig-chromium.txt', 'fluessig-webkit.txt', 'gleich-chromium.txt', 'anschluss.txt'):
    p = os.path.join(A, f)
    if os.path.exists(p):
        t = [x for x in open(p, encoding='utf-8', errors='replace').read().splitlines() if x.strip() and 'Deprecation' not in x]
        w.append(f'\n### {f}\n\n```\n' + '\n'.join(t[-40:]) + '\n```')
w.append('\n## Zeilen je Browser\n')
ks = [k for k, _, _ in laeufe]
w.append('| Nr | Zeile | ' + ' | '.join(ks) + ' |\n|---|---|' + '---|' * len(ks))
for (i, n), r in zeilen.items():
    w.append(f'| {i} | {n} | ' + ' | '.join('ok' if r.get(k) else ('–' if k not in r else 'ROT') for k in ks) + ' |')
open(ZIEL, 'w', encoding='utf-8').write('\n'.join(w) + '\n')
print('\n'.join(w[:30]))
print('…', ZIEL)
