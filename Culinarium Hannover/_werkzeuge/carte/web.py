"""La Carte · Culinarium Hannover — die Karten als Daten für die Website (28.10.2026, C27 in der Form des Hauses).

Die Website zeigt die Menükarte jedes Abends im Fenster des Abends (abende.html, gebaut aus website/abende_info.py KARTEN: je Gang Gang, Teller, Drink).
Dieses Modul liest aus jeder veröffentlichten Karte genau diese Form (zeilen) und schreibt alle Karten nach karten.json:
  _werkzeuge/carte/anschluss/karten.json          immer nach dem Veröffentlichen (im Revier des Werkzeugs, ändert die Website nicht)
  _kette/10-kartenmacher/karten.json               Paket der Kette, Station 10 (python3 _werkzeuge/carte/web.py kette)
Schlüssel = Plakat-ID des Abends wie in website/bau.py ABENDE («ohne-2023» für den Abend ohne Plakat). Die Website liest die Datei erst, wenn ihr
Bau sie vor abende_info.KARTEN nimmt (Einbau in website/, nicht Revier von La Carte; bis dahin bleibt jede Seite Byte für Byte, wie sie ist).
Der nächste Abend steht unter «naechster» mit Datum, ohne Plakat-ID (die gibt es erst mit dem Beitrag des Hauses)."""
import datetime, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS = os.path.dirname(os.path.dirname(HIER))
GAENGE = [('amuse', 'Amuse Bouche'), ('aperitif', 'Apéritif'), ('vorspeise', 'Vorspeise'), ('haupt', 'Hauptgang'), ('dessert', 'Dessert'), ('absacker', 'Absacker')]


def _klasse(n):
    m = re.search(r'\sclass="([^"]*)"', n['a'][1] or '')
    return m.group(1).split() if m else []


def _text(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict) and x.get('fn') == 'el':
        return ''.join(_text(y) for y in x['a'][2:])
    return ''


def zeilen(d):
    """Gänge der Karte als [(Gang, Teller, Drink)], Preis, Upgrade; ausgeblendete Einträge zählen nicht."""
    if d.get('art') == 'abend':
        w = d['abend']
        t = w['tage'][0]
        g = [(name, t.get(k, '').strip(), t.get(k + '_z', '').strip()) for k, name in GAENGE if (t.get(k, '') + t.get(k + '_z', '')).strip()]
        return dict(ab=w['ab'], titel=w.get('titel', ''), motto=w.get('motto', ''), mit=w.get('mit', ''), preis=w.get('preis', ''), gaenge=g, upgrade=[],
                    beispiel=bool(w.get('beispiel')))
    gaenge, upgrade, preis = [], [], ''

    def geh(x, im_upgrade=False):
        if not isinstance(x, dict) or x.get('aus'):
            return
        if x.get('fn') == 'seite':
            for y in x['a'][1:]:
                geh(y)
            return
        if x.get('fn') != 'el':
            return
        kl = _klasse(x)
        nonlocal preis
        if 'sb-upg' in kl:
            for y in x['a'][2:]:
                geh(y, True)
            return
        if 'sb-m' in kl:
            f = {k: '' for k in ('sb-gn', 'sb-n', 'sb-dr')}
            for y in x['a'][2:]:
                if isinstance(y, dict) and y.get('fn') == 'el' and not y.get('aus'):
                    for k in f:
                        if k in _klasse(y):
                            f[k] = _text(y).strip()
            if im_upgrade:
                upgrade.append(f['sb-n'])
            else:
                gaenge.append((f['sb-gn'], f['sb-n'], f['sb-dr']))
            return
        if 'sb-p' in kl:
            preis = ' '.join(_text(y).strip() for y in x['a'][2:][0]['a'][2:] if isinstance(y, dict) and y['a'][0] in ('b', 'small'))
            return
        for y in x['a'][2:]:
            geh(y, im_upgrade)
    for s in d.get('seiten', []):
        geh(s)
    return dict(ab=d.get('ab', ''), preis=preis, gaenge=gaenge, upgrade=upgrade)


def karten_json(K, ziele, lies):
    """Alle veröffentlichten Karten (Stand) in der Form der Website."""
    aus = {'stand': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'quelle': 'La Carte (_werkzeuge/carte/_daten/stand/)', 'abende': {}, 'naechster': None}
    for z in ziele:
        s = lies(os.path.join(K, 'stand', z + '.json'))
        if not s:
            continue
        if z == 'abend':
            aus['naechster'] = zeilen(s)
        else:
            aus['abende'][s.get('key') or z] = dict(zeilen(s), karte=z, name=s.get('name', ''))
    return aus


def schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    json.load(open(p + '.neu', encoding='utf-8'))
    os.replace(p + '.neu', p)


def anschliessen(K, ziele, lies):
    """Nach jedem Veröffentlichen: karten.json im Revier des Werkzeugs (nie in website/)."""
    eigen = os.path.realpath(K) == os.path.realpath(os.path.join(HIER, '_daten'))   # Prüfläufe mit Wegwerf-Daten schreiben neben ihre Daten, nie über die Datei des Hauses
    schreib(os.path.join(HIER if eigen else K, 'anschluss', 'karten.json'), karten_json(K, ziele, lies))
    return 'anschluss/karten.json'


if __name__ == '__main__':
    sys.path.insert(0, HIER)
    import carte
    d = karten_json(carte.K, carte.ZIELE, carte._lies)
    if sys.argv[1:] == ['kette']:
        schreib(os.path.join(HAUS, '_kette', '10-kartenmacher', 'karten.json'), d)
        print('_kette/10-kartenmacher/karten.json:', len(d['abende']), 'Abende + nächster Abend')
    else:
        schreib(os.path.join(HIER, 'anschluss', 'karten.json'), d)
        print('anschluss/karten.json:', len(d['abende']), 'Abende + nächster Abend')
