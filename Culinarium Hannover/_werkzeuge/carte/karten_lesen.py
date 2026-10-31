#!/usr/bin/env python3
"""La Carte · Culinarium Hannover: liest die Menükarten der Abende aus der Website (28.10.2026, C26 in der Form des Hauses).

Culinarium hat keine Speisekarte, sondern je Abend eine Menükarte: Gänge (Apéritif, Vorspeise, Hauptgang, Dessert, Absacker), zu jedem Gang Rudis
Teller und Momos Drink. Die Website führt diese Karten schon wörtlich, abgelesen von Fotos der gedruckten Karten (website/abende_info.py KARTEN,
Robert 27.10.2026), Datum, Preis und Zeile «BY MOMO X RUDI» je Abend stehen in website/bau.py ABENDE (aus den Beiträgen von @culinarium_hannover).
Nichts wird abgetippt: beide Dateien werden als Text gelesen (ast, nie importiert: der Import von bau.py baut die Website, Master 9) und
geschrieben nach _daten/quelle/<karte>.json. Zwei Prüfwege, bricht bei jeder Abweichung ab:
  1. Wort für Wort: jedes Wort der Daten steht in der Quelle (abende_info.py), jede Zeile der Quelle in den Daten.
  2. Gegen die gebaute Website: jeder Teller und jeder Drink steht genau so in website/abende.html (Menükarte im Abend), der Preis in der Kopfzeile.

Dazu die Karte «Der nächste Abend» (art abend, C08/C24 in der Form des Hauses): solange das Haus den nächsten Abend nicht eingetragen hat, steht dort als
Beispiel die jüngste ganz lesbare Karte (beschriftet «Beispiel», Fehlerbuch 10a: Beispiele statt Leere, nie erfundene Echtdaten).

    python3 _werkzeuge/carte/karten_lesen.py         schreibt _daten/quelle/ und prüft
"""
import ast, html, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website')
QD = os.path.join(HIER, '_daten', 'quelle')
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
# Gänge der Abende in fester Reihenfolge (so stehen sie auf jeder Karte des Hauses); Schlüssel der Karte «Der nächste Abend» (satz.js ABEND)
GAENGE = [('amuse', 'Amuse Bouche'), ('aperitif', 'Apéritif'), ('vorspeise', 'Vorspeise'), ('haupt', 'Hauptgang'), ('dessert', 'Dessert'), ('absacker', 'Absacker')]


class Fehler(Exception):
    pass


def _zuweisung(datei, name):
    """Den Wert einer Zuweisung NAME = … aus einer Python-Datei als Baum holen (ohne die Datei auszuführen)."""
    baum = ast.parse(open(datei, encoding='utf-8').read())
    for k in baum.body:
        if isinstance(k, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in k.targets):
            return k.value
    raise Fehler(f'{name} steht nicht in {datei}')


def _wert(knoten, namen):
    """Literale, Verkettung mit + und bekannte Namen (TM, IG, HL); Aufrufe (Bilderlisten) werden zu None."""
    if isinstance(knoten, ast.Constant):
        return knoten.value
    if isinstance(knoten, ast.Name):
        return namen.get(knoten.id)
    if isinstance(knoten, ast.BinOp) and isinstance(knoten.op, ast.Add):
        a, b = _wert(knoten.left, namen), _wert(knoten.right, namen)
        return a + b if a is not None and b is not None else None
    if isinstance(knoten, (ast.List, ast.Tuple)):
        w = [_wert(x, namen) for x in knoten.elts]
        return w if isinstance(knoten, ast.List) else tuple(w)
    if isinstance(knoten, ast.Dict):
        return {_wert(k, namen): _wert(v, namen) for k, v in zip(knoten.keys, knoten.values)}
    if isinstance(knoten, ast.Call) and getattr(knoten.func, 'id', '') == 'dict':
        return {kw.arg: _wert(kw.value, namen) for kw in knoten.keywords}
    return None


def quellen():
    ai = os.path.join(PROJ, 'abende_info.py')
    namen = {'IG': '_quelle/extern/ig/', 'HL': '_quelle/extern/ig-highlights/', 'TM': '_quelle/extern/ig-team/'}
    karten = _wert(_zuweisung(ai, 'KARTEN'), namen)
    info = _wert(_zuweisung(ai, 'INFO'), namen)
    abende = ast.literal_eval(_zuweisung(os.path.join(PROJ, 'bau.py'), 'ABENDE'))
    return karten, info, abende, open(ai, encoding='utf-8').read()


def iso(jahr, datum):
    """«Fr 15. und Sa 16. September» + «2023» → 2023-09-15 (der erste Abend des Termins)."""
    m = re.search(r'(\d{1,2})\.(?:\s+und\s+\w{2}\s+\d{1,2}\.)?\s+(' + '|'.join(MONATE) + ')', datum)
    if not m:
        raise Fehler(f'Datum nicht lesbar: {datum}')
    return '%s-%02d-%02d' % (jahr, MONATE.index(m.group(2)) + 1, int(m.group(1)))


def kurzname(jahr, datum):
    """«Fr 15. und Sa 16. September», 2023 → «15./16. September 2023»; ein Abend allein → «21. Oktober 2023»."""
    tage = re.findall(r'(\d{1,2})\.', datum)
    monat = next(x for x in MONATE if x in datum)
    return '%s %s %s' % ('/'.join(t + '.' for t in tage), monat, jahr)


def lesen():
    karten, info, abende, ai_text = quellen()
    aus = {}
    for jahr, datum, zusatz, preis, pid, mit in abende:
        key = pid or 'ohne-%s' % jahr
        k = karten.get(key)
        if not k:
            continue
        inf = info.get(key) or {}
        ab = iso(jahr, datum)
        ziel = 'abend-' + ab
        gaenge = []
        for g, teller, drink in k['gaenge']:
            if g not in dict((b, a) for a, b in GAENGE):
                raise Fehler(f'{ziel}: Gang «{g}» kennt La Carte nicht ({[b for a, b in GAENGE]})')
            gaenge.append({'gang': g, 'teller': teller, 'drink': drink})
        aus[ziel] = dict(ziel=ziel, art='satz', key=key, name=kurzname(jahr, datum), unter=inf.get('motto') or inf.get('titel') or '',
                         gruppe='Frühere Abende', ab=ab, datum='%s %s' % (datum, jahr), preis=preis, mit=mit, zusatz=zusatz,
                         motto=inf.get('motto') or '', titel=inf.get('titel') or '', plakat=pid or '', gaenge=gaenge,
                         upgrade=list(k.get('upgrade') or []), voll=bool(k.get('voll')), foto_der_karte=k['quelle'],
                         quelle='website/abende_info.py KARTEN[%r] · website/bau.py ABENDE (%s)' % (key, k['quelle']))
    if not aus:
        raise Fehler('Keine Menükarte in website/abende_info.py gefunden')
    pruefe(aus, karten, ai_text)
    return aus


def naechster(aus):
    """Karte «Der nächste Abend»: Beispiel aus der jüngsten ganz lesbaren Karte, jedes Feld wörtlich von dort."""
    voll = [d for d in aus.values() if d['voll'] and not d['upgrade']]
    b = max(voll, key=lambda d: d['ab'])
    tag = dict(zu=False, hinweis='')
    for s, name in GAENGE:
        g = next((x for x in b['gaenge'] if x['gang'] == name), None)
        tag[s], tag[s + '_z'] = (g['teller'], g['drink']) if g else ('', '')
    return dict(ziel='abend', art='abend', name='Der nächste Abend', unter='Menü und Drinks', gruppe='Der nächste Abend',
                quelle='Beispiel aus %s (%s)' % (b['ziel'], b['quelle']), beispiel_aus=b['ziel'],
                abend=dict(ab=b['ab'], titel='Menü', motto=b['motto'], mit=b['mit'], preis=b['preis'], zusatz='', hinweis='', fuss='',
                           tage=[tag], beispiel=True))


WORT = re.compile(r'[0-9A-Za-zÄÖÜäöüßéèêàâçÉÈÀ]+')


def pruefe(aus, karten, ai_text):
    """1. Wort für Wort gegen abende_info.py, 2. gegen die gebaute Website abende.html."""
    quelle = set(w.lower() for w in WORT.findall(ai_text))
    try:
        seite = html.unescape(open(os.path.join(PROJ, 'abende.html'), encoding='utf-8').read())
    except OSError:
        raise Fehler('website/abende.html fehlt (Website erst bauen)')
    fehl = []
    for z, d in aus.items():
        k = karten[d['key']]
        if len(d['gaenge']) != len(k['gaenge']):
            fehl.append(f'{z}: {len(d["gaenge"])} Gänge, Quelle {len(k["gaenge"])}')
        for g, (g0, t0, d0) in zip(d['gaenge'], k['gaenge']):
            if (g['gang'], g['teller'], g['drink']) != (g0, t0, d0):
                fehl.append(f'{z}: {g} ≠ Quelle')
            for t in (g['teller'], g['drink']):
                for w in WORT.findall(t):
                    if w.lower() not in quelle:
                        fehl.append(f'{z}: Wort «{w}» nicht in der Quelle')
                if t and t not in seite:
                    fehl.append(f'{z}: «{t[:60]}» steht nicht in website/abende.html')
        for u in d['upgrade']:
            if u not in seite:
                fehl.append(f'{z}: Upgrade «{u}» steht nicht in website/abende.html')
        if d['preis'] not in seite:
            fehl.append(f'{z}: Preis {d["preis"]} steht nicht in website/abende.html')
    if fehl:
        raise Fehler('Prüfung gegen die Quelle: ' + '; '.join(fehl[:12]))
    return True


def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    t = p + '.neu'
    with open(t, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    json.load(open(t, encoding='utf-8'))
    os.replace(t, p)


if __name__ == '__main__':
    try:
        aus = lesen()
    except Fehler as e:
        sys.exit('ABBRUCH · ' + str(e))
    aus['abend'] = naechster(aus)
    bericht = {}
    for z, d in aus.items():
        _schreib(os.path.join(QD, z + '.json'), d)
        n = len(d.get('gaenge') or d['abend']['tage'])
        bericht[z] = dict(name=d['name'], gaenge=len(d.get('gaenge', [])), drinks=sum(1 for g in d.get('gaenge', []) if g['drink']), preis=d.get('preis') or d['abend']['preis'], voll=d.get('voll', True))
        print(f'{z}: {d["name"]} · {d.get("unter", "")} · {bericht[z]["gaenge"]} Gänge, {bericht[z]["drinks"]} Drinks · {bericht[z]["preis"]}')
    _schreib(os.path.join(QD, 'pruefung.json'), dict(geprueft='Wort für Wort gegen website/abende_info.py, Teller/Drinks/Preise gegen website/abende.html', karten=bericht))
    print('Prüfung: gleich (Quelle und gebaute Website)')
