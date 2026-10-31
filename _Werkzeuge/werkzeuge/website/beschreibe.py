#!/usr/bin/env python3
"""Hilfe beim Schreiben der Beschreibung eines Hauses. Liest nur, schreibt nichts.

  python3 werkzeuge/website/beschreibe.py <haus> <seite>               Gerüst der Seite: Abschnitte mit id und Klassen
  python3 werkzeuge/website/beschreibe.py <haus> <seite> '<selektor>'  was ein Selektor trifft, mit den Stellen darin
  python3 werkzeuge/website/beschreibe.py <haus> --pruefe              jeder Bereich der Beschreibung: Einträge und Felder, die fehlen

So findet man «jedes» (ein Eintrag) und «wo» (ein Feld im Eintrag) für haeuser/<haus>.json, ohne einen Wert abzutippen."""
import json
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
import schicht as S  # noqa: E402
import ausgabe as A  # noqa: E402


def name(k):
    a = k['attrs']
    return k['tag'] + ('#' + a['id'] if a.get('id') else '') + ''.join('.' + c for c in (a.get('class') or '').split())


def geruest(k, src, tiefe=0, bis=4):
    for c in k['kids']:
        if 'tag' not in c or c['tag'] in S.AUS or c.get('es') is None:
            continue
        zeigen = c['tag'] in S.BLOECKE | S.FEST | {'main', 'div', 'ul', 'ol', 'dl', 'table', 'h1', 'h2', 'h3', 'form'} and (c['attrs'].get('id') or c['attrs'].get('class') or c['tag'] in S.BLOECKE)
        if zeigen and tiefe < bis:
            print('  ' * tiefe + name(c) + '   ' + S.klar(src[c['se']:c['es']])[:60])
        geruest(c, src, tiefe + (1 if zeigen else 0), bis)


def baum_zeigen(k, src, z, tiefe=0):
    t = next((x for x in z['texte'] if x['k'] is k and x['art'] == 'el'), None)
    f = next((x for x in z['fotos'] if x['k'] is k), None)
    print('  ' * tiefe + name(k) + (f'   = «{t["t"][:70]}»' if t else '') + (f'   Foto {f["b"]}' if f else ''))
    if not t:
        for c in k['kids']:
            if 'tag' in c and c['tag'] not in S.AUS:
                baum_zeigen(c, src, z, tiefe + 1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    haus = sys.argv[1]
    b = json.loads((HIER / 'haeuser' / f'{haus}.json').read_text(encoding='utf-8'))
    regeln = {'gesperrt': b.get('gesperrt') or [], 'auslassen': b.get('auslassen') or [], 'bild_groessen': b.get('bild_groessen')}
    if sys.argv[2] == '--pruefe':
        import importlib.util
        sys.path.insert(0, str(HIER.parent.parent / 'unterbau'))
        spec = importlib.util.spec_from_file_location('api', HIER / 'api.py')
        api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(api)
        for k, d in (b.get('bereiche') or {}).items():
            if d.get('an') is False:
                print(f'{k}: ausgeschaltet')
                continue
            r = api.bereich(haus, k, S.leer())
            print(f'{k}: {len(r["eintraege"])} Einträge' + (' · FEHLT: ' + '; '.join(r['fehlt']) if r['fehlt'] else ''))
            for e in r['eintraege'][:int(sys.argv[3]) if len(sys.argv) > 3 else 3]:
                print('   ', e['seite'], '·', e['titel'][:50], '·', ', '.join(f'{f["label"]} ({len(f["teile"])})' for f in e['felder']))
        sys.exit(0)
    src = (A.probe_ordner() / haus / 'grundlage' / sys.argv[2]).read_bytes().decode('utf-8')
    z = S.zerlege(src, regeln)
    if len(sys.argv) == 3:
        geruest(z['baum'].wurzel, src)
    else:
        treffer = S.waehle(z['baum'].wurzel, sys.argv[3])
        print(len(treffer), 'Treffer')
        for k in treffer[:int(sys.argv[4]) if len(sys.argv) > 4 else 2]:
            baum_zeigen(k, src, z)
            print()
