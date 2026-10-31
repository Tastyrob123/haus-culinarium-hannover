#!/usr/bin/env python3
"""La Carte · Culinarium Hannover — Prüfungen der Karten (28.10.2026, Muster: pruefe.py der Tafel im Schäfli). Für «wortlaut» muss der Server laufen
(python3 _werkzeuge/carte/serve.py, Port aus CARTE_PORT, Standard 9083).

    python3 _werkzeuge/carte/pruefe.py rund        Satz von La Carte = Satz des Projekts, Zeichen für Zeichen (pruef/rund.js, Grundstand)
    python3 _werkzeuge/carte/pruefe.py wortlaut    jede Karte aus dem veröffentlichten Stand drucken und Wort für Wort gegen ihre Quelle prüfen
                                                   (_daten/quelle/<karte>.json, aus der Website gelesen): gezählt je Wort, Gross und Klein gleich;
                                                   erlaubt dazu nur, was der Satz bewusst gibt (Fusszeile, «Ticket», «Upgrade nach Wahl», Titel «Menü»)
    python3 _werkzeuge/carte/pruefe.py website     die Karten des Werkzeugs in der Form der Website (web.py zeilen) = die Menükarten, die die
                                                   Website heute zeigt (website/abende_info.py KARTEN): Gang, Teller, Drink, Upgrade, Preis je Abend
    python3 _werkzeuge/carte/pruefe.py schrift     jede PDF: nur feste Schnitte (pdffonts, kein Type 3), keine zerfallenen Wörter (pdftotext)
    python3 _werkzeuge/carte/pruefe.py alles
Nur gelesen wird website/; geschrieben wird nur nach pruef/aus/."""
import collections, json, os, re, subprocess, sys, unicodedata

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
AUS = os.path.join(HIER, 'pruef', 'aus')
QD = os.path.join(HIER, '_daten', 'quelle')
KARTEN = sorted(f[:-5] for f in os.listdir(QD) if f.endswith('.json') and f.startswith('abend'))


def druck(z, art='stand'):
    os.makedirs(AUS, exist_ok=True)
    p = os.path.join(AUS, z + '.pdf')
    r = subprocess.run(['node', os.path.join(HIER, 'drucke.js'), z, art, p], capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise SystemExit(f'Druck {z} gescheitert: {r.stderr[-400:]}')
    return p


def rund():
    r = subprocess.run(['node', os.path.join(HIER, 'pruef', 'rund.js')], capture_output=True, text=True)
    print(r.stdout.strip())
    return r.returncode == 0


MUSTER = r'[0-9a-zäöüéèêëàâîïôùûçœß]+'


def _text(pfad, layout=False):
    t = subprocess.run(['pdftotext'] + (['-layout'] if layout else []) + [pfad, '-'], capture_output=True, text=True).stdout
    t = unicodedata.normalize('NFC', t).replace('\xa0', ' ').replace('\xad', '')
    for a, b in (('ﬁ', 'fi'), ('ﬂ', 'fl'), ('ﬀ', 'ff'), ('ﬃ', 'ffi'), ('’', "'"), ('‘', "'")):
        t = t.replace(a, b)
    return re.sub(r'[-]', ' ', t)


def _w(t):
    """Wörter gezählt; Bindestriche fallen auf beiden Seiten weg (pdftotext liest «FETA-» am Zeilenende und «KÄSE» als «FETAKÄSE»)"""
    return collections.Counter(re.findall(MUSTER, unicodedata.normalize('NFC', t).lower().replace('-', '')))


def _soll(q):
    """Alle Wörter, die laut Quelle auf der Karte stehen."""
    if q['art'] == 'abend':
        a = q['abend']
        t = a['tage'][0]
        teile = [v for k, v in t.items() if k not in ('zu', 'hinweis') and v] + [a['preis'], a['mit'], a['motto'] or a['titel'] or 'Menü']
        teile += ['Amuse Bouche' if t['amuse'] or t['amuse_z'] else '', 'Apéritif' if t['aperitif'] or t['aperitif_z'] else '', 'Vorspeise' if t['vorspeise'] or t['vorspeise_z'] else '',
                  'Hauptgang' if t['haupt'] or t['haupt_z'] else '', 'Dessert' if t['dessert'] or t['dessert_z'] else '', 'Absacker' if t['absacker'] or t['absacker_z'] else '']
        return ' '.join(teile)
    teile = [x for g in q['gaenge'] for x in (g['gang'], g['teller'], g['drink'])] + q['upgrade'] + [q['preis'], q['mit'], q['motto'] or q['titel'] or 'Menü', q['datum']]
    return ' '.join(teile)


def wortlaut():
    import satz_bau
    ok = True
    for z in KARTEN:
        q = json.load(open(os.path.join(QD, z + '.json'), encoding='utf-8'))
        p = druck(z)
        neu = _w(_text(p))
        alt = _w(_soll(q))
        dazu_ok = _w(satz_bau.FUSS + ' Ticket')
        if q.get('upgrade'):
            dazu_ok += _w('Upgrade nach Wahl')
        if q['art'] == 'abend':   # Datum setzt der Satz aus dem Tag («Fr 21. und Sa 22. Februar 2025»), dazu der Satz zum Beispiel
            dazu_ok += _w('Fr Sa und Januar Februar März April Mai Juni Juli August September Oktober November Dezember 0123456789 2024 2025 2026 2027 '
                          + ' '.join(str(i) for i in range(1, 32)) + ' Beispiel bitte die Gänge des nächsten Abends eintragen')
        fehlt, dazu = alt - neu, (neu - alt) - collections.Counter({k: 10 ** 6 for k in dazu_ok})
        gleich = not fehlt and not dazu
        ok = ok and gleich
        print(f'{z}: {sum(alt.values())} Wörter in der Quelle, {sum(neu.values())} im Druck · ' + ('Wortlaut gleich' if gleich else 'ABWEICHUNG'))
        if not gleich:
            print('   fehlt im Druck:', ' '.join(sorted(fehlt.elements()))[:400])
            print('   kommt dazu:    ', ' '.join(sorted(dazu.elements()))[:400])
    print('\nWortlaut gegen die Quellen:', 'alle Karten stimmen' if ok else 'ABWEICHUNGEN')
    return ok


def website():
    """Daten von La Carte (Stand) in der Form der Website = KARTEN der Website. Teller: « / » der Karte = « | » der Website (Trennzeichen, satz_bau.rudi)."""
    import carte, web, karten_lesen
    karten, _info, _abende, _t = karten_lesen.quellen()
    ok = True
    n = lambda t: re.sub(r'\s*[|/]\s*', ' / ', (t or '').strip())
    for z in carte.ZIELE:
        if z == 'abend':
            continue
        s = carte._lies(carte._p('stand', z))
        ist = web.zeilen(s)
        k = karten[s['key']]
        soll_g = [(g, n(t), d) for g, t, d in k['gaenge']]
        ist_g = [(g, n(t), d) for g, t, d in ist['gaenge']]
        q = json.load(open(os.path.join(QD, z + '.json'), encoding='utf-8'))
        gleich = soll_g == ist_g and list(k.get('upgrade') or []) == ist['upgrade'] and ist['preis'] == q['preis']
        ok = ok and gleich
        print(f'{z} ({s["key"]}): ' + ('wie die Website' if gleich else f'ANDERS: {ist_g} ≠ {soll_g} oder Preis {ist["preis"]} ≠ {q["preis"]}'))
    print('\nKarten gegen die Website:', 'gleich' if ok else 'ABWEICHUNGEN')
    return ok


def schrift():
    ok = True
    for z in KARTEN:
        p = os.path.join(AUS, z + '.pdf')
        if not os.path.exists(p):
            p = druck(z)
        f = subprocess.run(['pdffonts', p], capture_output=True, text=True).stdout
        typ3 = 'Type 3' in f
        einzeln = re.findall(r'(?:\b\w\b ){4,}', _text(p))   # zerfallene Wörter («H A N D …»)
        gut = not typ3 and not einzeln
        ok = ok and gut
        namen = sorted(set(re.findall(r'^([A-Z]{6}\+\S+)', f, re.M)))
        print(f'{z}: ' + ('feste Schnitte, ganze Wörter' if gut else f'SCHRIFT: Type 3={typ3}, zerfallen={einzeln[:3]}') + f' · {", ".join(x.split("+")[1] for x in namen)}')
    print('\nSchriften der PDFs:', 'gut' if ok else 'FEHLER')
    return ok


if __name__ == '__main__':
    was = sys.argv[1] if len(sys.argv) > 1 else 'alles'
    r = {'rund': rund, 'wortlaut': wortlaut, 'website': website, 'schrift': schrift}
    ergebnis = [r[x]() for x in (r if was == 'alles' else [was])]
    print('\nGESAMT:', 'GRÜN' if all(ergebnis) else 'ROT')
    sys.exit(0 if all(ergebnis) else 1)
