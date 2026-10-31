#!/usr/bin/env python3
"""La Carte · Culinarium Hannover: liest die Menükarten der Abende einmal als Daten ein (28.10.2026, C17).
Kopie von einlesen.py der Tafel im Schäfli (dort aus Schlössli, Gasterntal, Ruedihus, Doldenhorn).

Nichts wird abgetippt. karten_lesen.py liest die Menükarten aus der Website (_daten/quelle/<karte>.json, Wort für Wort gegen
website/abende_info.py und gegen die gebaute Seite abende.html geprüft), satz_bau.py setzt sie im Kleid des Culinarium nach satz/u-<karte>.html.
Dieses Skript zerlegt den Satz in einen Baum: Elemente (Tag, Merkmale, Kinder), Texte (das, was das Haus ändert) und feste Teile (Wortmarke).
Aus diesem Baum setzt satz/satz.js dasselbe HTML Zeichen für Zeichen wieder (python3 _werkzeuge/carte/pruefe.py rund).

«Der nächste Abend» (C08/C24 in der Form des Hauses: Gänge mit Rudis Teller und Momos Drink, Datum, Preis) wird als Abend angelegt, jedes Feld
wörtlich aus _daten/quelle/abend.json; satz.js setzt daraus das Blatt (A4 hoch wie die anderen Menükarten).

Geschrieben wird nur in _werkzeuge/carte/ (_daten/, bilder/z/, bilder/fotos.json).

    python3 _werkzeuge/carte/einlesen.py            nur wo noch kein Stand liegt (ein Stand des Hauses wird nie überschrieben)
    python3 _werkzeuge/carte/einlesen.py --grund    nur den Grundstand neu (_daten/grundstand/), für den Rundlauf und «Ursprünglicher Stand»
"""
import datetime, html, json, os, re, shutil, sys

HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(HIER))
PROJ = os.path.join(_WURZEL, 'website')   # Culinarium: Website in website/
QD = os.path.join(HIER, '_daten', 'quelle')
DATEN = os.environ.get('CARTE_DATEN') or os.path.join(HIER, '_daten')
sys.path.insert(0, HIER)

# Karten, die La Carte pflegt: Kennung = Satz satz/u-<kennung>.html = Name der PDF (je Abend eine Menükarte, karten_lesen.py)
KARTEN = {}
for _f in sorted(os.listdir(QD)):
    if _f.startswith('abend-') and _f.endswith('.json'):
        _q = json.load(open(os.path.join(QD, _f), encoding='utf-8'))
        KARTEN[_q['ziel']] = dict(name=_q['name'], unter=_q['unter'], gruppe=_q['gruppe'], quelle=_q['quelle'], ab=_q['ab'], plakat=_q['plakat'], key=_q['key'])
LEER_TAG = {'img', 'br', 'hr', 'meta', 'link', 'input', 'wbr', 'col', 'source'}
A, Z = '', ''          # Platzhalter für feste Teile (Bilder als data:, Zeichen als svg) im Baum
TOKEN = re.compile(r'<!--.*?-->|<svg\b.*?</svg>|</?([a-zA-Z][\w-]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>', re.S)


class Teile:
    """Feste Teile einer Karte: jedes nur einmal gespeichert, im Baum steht der Platzhalter."""
    def __init__(self):
        self.liste, self.idx = [], {}

    def ref(self, s):
        if s not in self.idx:
            self.idx[s] = len(self.liste)
            self.liste.append(s)
        return f'{A}{self.idx[s]}{Z}'

    def at(self, s):   # data:-Bilder in Merkmalen
        return re.sub(r'data:[a-z]+/[\w.+-]+;base64,[A-Za-z0-9+/=]+', lambda m: self.ref(m.group(0)), s)


def text_kind(raw, T):
    """Text zwischen Tags: als Text (wenn er sich genau so wieder schreibt), sonst fest"""
    t = html.unescape(raw)
    if html.escape(t) == raw:
        return t
    return {'fn': 'roh', 'a': [T.at(raw)]}


def baum(s, T):
    """HTML → Liste von Kindern (Texte, Elemente {fn:'el', a:[tag, merkmale, *kinder]}, feste Teile {fn:'roh'})"""
    wurzel = {'fn': 'el', 'a': ['#', '']}
    stapel = [wurzel]
    pos = 0
    for m in TOKEN.finditer(s):
        if m.start() > pos:
            stapel[-1]['a'].append(text_kind(s[pos:m.start()], T))
        tok = m.group(0)
        pos = m.end()
        if tok.startswith('<!--'):
            stapel[-1]['a'].append({'fn': 'roh', 'a': [tok]})
            continue
        if tok.startswith('<svg'):
            stapel[-1]['a'].append({'fn': 'roh', 'a': [T.ref(tok) if len(tok) > 200 else tok]})
            continue
        tag, at = m.group(1), m.group(2)
        if tok.startswith('</'):
            oben = stapel.pop()
            assert oben['a'][0] == tag, ('Tag passt nicht', oben['a'][0], tag, s[max(0, m.start() - 80):m.start() + 20])
            continue
        el = {'fn': 'el', 'a': [tag, T.at(at)]}
        stapel[-1]['a'].append(el)
        if tag.lower() not in LEER_TAG and not at.rstrip().endswith('/'):
            stapel.append(el)
    if pos < len(s):
        stapel[-1]['a'].append(text_kind(s[pos:], T))
    assert len(stapel) == 1, ('offene Tags', [x['a'][0] for x in stapel])
    return wurzel['a'][2:]


def lies(kennung):
    pfad = os.path.join(HIER, 'satz', 'u-' + kennung + '.html')
    h = open(pfad, encoding='utf-8').read()
    b = h.index('<body>') + len('<body>')
    e = h.rindex('</body>')
    kopf, koerper, fuss = h[:b], h[b:e], h[e:]
    T = Teile()
    seiten = []
    for x in baum(koerper, T):
        if isinstance(x, dict) and x['fn'] == 'el' and x['a'][0] == 'section':
            seiten.append({'fn': 'seite', 'a': x['a'][1:]})
        else:
            raise AssertionError(('zwischen den Seiten steht etwas', kennung, str(x)[:120]))
    fmt = re.search(r'@page\{size:(\d+)mm (\d+)mm', kopf)
    k = KARTEN[kennung]
    return dict(art='satz', ziel=kennung, name=k['name'], unter=k['unter'], gruppe=k['gruppe'], quelle=k['quelle'], ab=k['ab'], plakat=k['plakat'], key=k['key'], schema=1,
                format=[int(fmt.group(1)), int(fmt.group(2))], kopf=kopf, fuss=fuss, seiten=seiten, teile=T.liste)


def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    t = p + '.neu'
    with open(t, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    json.load(open(t, encoding='utf-8'))
    os.replace(t, p)


# Fotos des Hauses für Liste und Kacheln (Bildregister BILD in website/bau.py, ausgeliefert unter website/assets/bild/<schlüssel>-<breite>.webp):
# je Abend sein Plakat (p_<Beitrags-ID>), ohne Plakat das erste Bild des Abends; «Der nächste Abend» die Tafel der Bar (Schlüssel aus BILD, nicht geraten)
FOTO_NAECHSTER = 'tafelleer'


def foto_von(k):
    if k.get('plakat'):
        return 'p_' + k['plakat']
    return 'ab_%s_0' % k['key'].replace('-', '_')


def vorschaubilder():
    """Kleine Bilder für die Liste und die Kacheln (112 × 112 px aus der kleinsten Liefergrösse der Website); fotos.json: Karte → Schlüssel."""
    from PIL import Image
    ziel = os.path.join(HIER, 'bilder', 'z')
    os.makedirs(ziel, exist_ok=True)
    fotos = {k: foto_von(v) for k, v in KARTEN.items()}
    fotos['abend'] = FOTO_NAECHSTER
    for nm in sorted(set(fotos.values())):
        q = os.path.join(PROJ, 'assets', 'bild', nm + '-640.webp')
        if not os.path.isfile(q):
            raise SystemExit(f'Bild fehlt: {q}')
        im = Image.open(q).convert('RGB'); w, h = im.size; k = min(w, h)
        im.crop(((w - k) // 2, (h - k) // 2, (w - k) // 2 + k, (h - k) // 2 + k)).resize((112, 112), Image.LANCZOS).save(os.path.join(ziel, nm + '.webp'), 'WEBP', quality=80)
    _schreib(os.path.join(HIER, 'bilder', 'fotos.json'), fotos)
    return len(set(fotos.values()))


GAENGE = ('amuse', 'aperitif', 'vorspeise', 'haupt', 'dessert', 'absacker')   # Gänge eines Abends (satz.js ABEND, karten_lesen.py GAENGE)


def abend():
    """«Der nächste Abend» (C08/C24 in der Form des Hauses): jedes Feld wörtlich aus _daten/quelle/abend.json (Beispiel, bis das Haus einträgt)."""
    d = json.load(open(os.path.join(QD, 'abend.json'), encoding='utf-8'))
    t = d['abend']['tage'][0]
    assert all(g in t and g + '_z' in t for g in GAENGE), ('Abend hat eine andere Form als erwartet', list(t))
    return dict(art='abend', ziel='abend', name=d['name'], unter=d['unter'], gruppe=d['gruppe'], quelle=d['quelle'],
                schema=1, format=[210, 297], abend=d['abend'], seiten=[], teile=[])


def alle():
    aus = {'abend': abend()}
    aus.update({k: lies(k) for k in KARTEN})
    return aus


if __name__ == '__main__':
    grund_nur = '--grund' in sys.argv
    karten = alle()
    print('Vorschaubilder:', vorschaubilder())
    for kennung, d in karten.items():
        _schreib(os.path.join(DATEN, 'grundstand', kennung + '.json'), d)
        ziel = os.path.join(DATEN, 'stand', kennung + '.json')
        if grund_nur:
            continue
        if os.path.exists(ziel):
            print(f'{kennung}: Stand liegt schon, bleibt (Grundstand erneuert)')
            continue
        _schreib(ziel, dict(d, veroeffentlicht=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wer='Einlesen'))
        print(f'{kennung}: {len(d["seiten"]) or 1} Seiten eingelesen, {len(d["teile"])} feste Teile')
