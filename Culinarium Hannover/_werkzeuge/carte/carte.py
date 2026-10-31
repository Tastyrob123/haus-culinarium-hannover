"""La Carte · Culinarium Hannover — Server-Teil (28.10.2026). Kopie der Tafel im Schäfli (dort aus dem Schlössli, Gasterntal, Ruedihus, Waldhotel
Doldenhorn, La Carte des Carlton-Europe und mission_control.py des Grand Beau-Rivage), auf die Menükarten des Culinarium umgeschrieben: je Abend eine
Karte (Gänge mit Rudis Teller und Momos Drink; Satz aus den Daten der Website, karten_lesen.py → satz_bau.py → einlesen.py) und «Der nächste Abend»
als Abend mit festen Gängen (C08/C24 in der Form des Hauses). Eingehängt in _werkzeuge/carte/serve.py unter /_werkzeuge/carte/api/.

Ablage (_daten/, nur dieses Werkzeug schreibt dort):
  stand/<karte>.json        was veröffentlicht ist (die Wahrheit der Karte, eingelesen mit einlesen.py)
  entwurf/<karte>.json      was gerade bearbeitet wird (.vorher = Stand vor dem letzten Speichern)
  verlauf/<karte>/<zeit>.*  jede frühere Fassung (Daten und PDF), jeder verworfene Entwurf
  live/<karte>.pdf          die veröffentlichte PDF · probe/<karte>.pdf  die Probe des Entwurfs
  grundstand/<karte>.json   der Stand beim Einlesen (zum Vergleich und als «Ursprünglicher Stand»)
  protokoll.jsonl           wer hat wann was getan · fehler.log  Fehler des Servers · sicherung/  tägliche Sicherung
  einstellungen.json        Anschluss an die Website (aus, bis das Haus und Robert es wollen)

Die Karten sind ein Baum aus dem fertigen Satz des Projekts (einlesen.py): Seiten, Elemente (Tag und Merkmale), Texte und feste Teile. Das Haus
ändert Texte, Reihenfolge, Sichtbarkeit und Gestaltung; Tags, Merkmale und feste Teile müssen aus dem eingelesenen Grundstand der Karte stammen
(neue Merkmale oder fremdes HTML weist der Server ab, siehe _bausteine()).

Sicherheit nach Master 7a (Stand im Abschnitt «Sicherheit» der STAND.md): Rollen und Rechte je Weg, Protokoll mit Namen, Grenze für zu viele
Anfragen (serve.py), Sicherungen und Verlauf, Prüfung jeder Eingabe, Daten nie still leer, Umziehen über «schema» (migriere), Zurückholen.
Kein Passwort (Robert 15.10.2026: vorerst keines); bei der Auslieferung ans Haus kommt die Anmeldung davor."""
import datetime, html, json, os, re, shutil, subprocess, tarfile, threading, time

HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(HIER))
PROJ = os.path.join(_WURZEL, 'website')   # Culinarium: Website in website/
K = os.environ.get('CARTE_DATEN') or os.path.join(HIER, '_daten')
SCHEMA = 1
# Demo vor dem Auftrag (Demo-Check 21.10.2026): liegt die Datei DEMO neben carte.py, schreibt das Werkzeug nie in die Website (Anschluss gesperrt, Meldung «Demo»)
DEMO = os.path.exists(os.path.join(HIER, 'DEMO')) and not os.environ.get('CARTE_ECHT')
# «Der nächste Abend» und je früherem Abend mit überlieferter Karte eine Menükarte (karten_lesen.py legt sie in _daten/quelle/ an, neueste zuerst)
ZIELE = ['abend'] + sorted((f[:-5] for f in os.listdir(os.path.join(HIER, '_daten', 'quelle')) if f.startswith('abend-') and f.endswith('.json')), reverse=True)
ROLLEN = {'kueche': 'Küche', 'service': 'Service', 'direktion': 'Direktion'}
RECHTE = {   # wer darf welchen Weg (Lesen dürfen alle)
    'entwurf': {'kueche', 'service', 'direktion'}, 'verwerfen': {'kueche', 'service', 'direktion'}, 'probe': {'kueche', 'service', 'direktion'},
    'veroeffentlichen': {'direktion'}, 'zurueckholen': {'direktion'}, 'einstellungen': {'direktion'}, 'reparatur': {'direktion'},
}
# Culinarium: keine Speise-, Wein- oder Spa-Karte (C19 betrifft nicht), sondern Menükarten je Abend. Küche (Rudi) und Service (Momo, Bar) ändern
# alle Karten und drucken Proben; die Karte des nächsten Abends darf die Küche auch veröffentlichen (sie wechselt jeden Abend), die früheren die Direktion.
NUR = {}
KUECHE_LIVE = {'abend'}   # was die Küche selbst veröffentlichen darf
_SCHLOSS = threading.RLock()
BAU = {'laeuft': False, 'ziel': '', 'schritt': '', 'schritte': [], 'fehler': '', 'fertig': '', 'start': 0, 'ende': 0, 'bericht': {}}
START = time.time()
NODE_PW = os.path.join(os.path.expanduser('~'), 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright')
PORT_STD = '9083'


class Fehler(Exception):
    """Fehler mit Stichwort (für die Meldung im Werkzeug und den Eintrag «Was tun?»)"""
    def __init__(self, stichwort, text, status=400):
        super().__init__(text)
        self.stichwort, self.text, self.status = stichwort, text, status


def _jetzt():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def _p(art, z):
    return os.path.join(K, art, z + '.json')


def protokoll(wer, rolle, was, z='', **mehr):
    os.makedirs(K, exist_ok=True)
    e = dict(zeit=_jetzt(), wer=wer or 'unbekannt', rolle=rolle or '', was=was, karte=z, **mehr)
    with open(os.path.join(K, 'protokoll.jsonl'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(e, ensure_ascii=False) + '\n')


def fehler_log(text):
    os.makedirs(K, exist_ok=True)
    with open(os.path.join(K, 'fehler.log'), 'a', encoding='utf-8') as f:
        f.write(f'{_jetzt()}  {text}\n')


def _lies(p):
    """Datei lesen. Beschädigt: nie still als leer, sondern aus der letzten Fassung im Verlauf oder .vorher holen, sonst abbrechen."""
    try:
        with open(p, encoding='utf-8') as f:
            return migriere(json.load(f))
    except FileNotFoundError:
        return None
    except ValueError as e:
        z = os.path.basename(p)[:-5]
        for kandidat in [p + '.vorher'] + _verlauf_dateien(z) + _sicherungen(os.path.relpath(p, K)):
            try:
                if isinstance(kandidat, tuple):   # aus dem täglichen Archiv
                    with tarfile.open(kandidat[0]) as tar:
                        d = migriere(json.load(tar.extractfile(kandidat[1])))
                    kandidat = kandidat[0]
                else:
                    with open(kandidat, encoding='utf-8') as f:
                        d = migriere(json.load(f))
                kaputt = p + '.kaputt-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
                shutil.copy2(p, kaputt)
                _schreib(p, d)
                fehler_log(f'beschaedigt: {os.path.relpath(p, K)} ({e}); aus {os.path.relpath(kandidat, K)} geholt, die kaputte Datei liegt als {os.path.basename(kaputt)}')
                protokoll('Server', '', 'aus-sicherung', z, datei=os.path.relpath(kandidat, K))
                return d
            except (OSError, ValueError):
                continue
        raise Fehler('KAPUTT', f'{os.path.relpath(p, K)} lässt sich nicht lesen und es gibt keine Sicherung.', 500)


def _sicherungen(rel):
    """Die täglichen Archive (neueste zuerst), die diese Datei enthalten"""
    d = os.path.join(K, 'sicherung')
    if not os.path.isdir(d):
        return []
    aus = []
    for x in sorted((x for x in os.listdir(d) if x.endswith('.tar.gz')), reverse=True):
        try:
            with tarfile.open(os.path.join(d, x)) as tar:
                if rel in tar.getnames():
                    aus.append((os.path.join(d, x), rel))
        except (OSError, tarfile.TarError):
            continue
    return aus


def _verlauf_dateien(z):
    d = os.path.join(K, 'verlauf', z)
    if not os.path.isdir(d):
        return []
    return [os.path.join(d, x) for x in sorted((x for x in os.listdir(d) if x.endswith('.json') and not x.startswith('verworfen')), reverse=True)]


def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    t = p + '.neu'
    with open(t, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    with open(t, encoding='utf-8') as f:
        json.load(f)   # prüfen, bevor es gilt
    os.replace(t, p)


def migriere(d):
    """Umziehen der Daten: ältere Fassungen auf das heutige Schema heben. Jede neue Fassung des Schemas bekommt hier ihren Schritt."""
    if not isinstance(d, dict):
        return d
    if 'schema' not in d:
        d['schema'] = 1
    if d['schema'] > SCHEMA:
        raise Fehler('SCHEMA', f'Die Karte stammt aus einer neueren Fassung dieses Werkzeugs (Schema {d["schema"]}).', 500)
    return d


def _ziel(z):
    if z not in ZIELE:
        raise Fehler('ZIEL', 'Diese Karte gibt es nicht.', 404)
    return z


def _recht(rolle, weg, z=''):
    if rolle not in ROLLEN:
        raise Fehler('ROLLE', 'Trag zuerst oben rechts ein, wer du bist und in welcher Rolle du arbeitest.', 403)
    if rolle == 'kueche' and weg in ('veroeffentlichen', 'zurueckholen') and z in KUECHE_LIVE:
        return
    if rolle not in RECHTE[weg]:
        raise Fehler('RECHT', f'In der Rolle «{ROLLEN[rolle]}» ist das nicht freigegeben. Bitte die Direktion fragen.', 403)
    if rolle in NUR and z and z not in NUR[rolle]:
        raise Fehler('RECHT', 'Nicht freigegeben.', 403)


# ---------------------------------------------------------------- Prüfen der Daten (jede Eingabe, bevor sie gespeichert wird)
def _text_ok(x, wo):
    if isinstance(x, str):
        if len(x) > 4000:
            return f'{wo}: Der Text ist zu lang.'
        if re.search(r'<\s*/?\s*(script|iframe|object|embed|style|link|meta)\b|javascript:|\bon\w+\s*=', x, re.I):
            return f'{wo}: Der Text enthält etwas, das wie Programmcode aussieht.'
    return ''


TAGE_OK = {'section', 'div', 'header', 'footer', 'main', 'article', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'span', 'b', 'i', 'em', 'strong', 'small',
           'sup', 'sub', 'br', 'img', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'col', 'colgroup', 'figure', 'figcaption'}
_BAUSTEINE = {}


def _bausteine(z):
    """Was in dieser Karte an Tags, Merkmalen und festen Teilen vorkommen darf: genau das, was der eingelesene Grundstand enthält.
    Das Haus kann Texte ändern, Einträge kopieren, verschieben, ausblenden und gestalten, aber kein neues HTML und keine neuen Merkmale schreiben."""
    p = _p('grundstand', z)
    try:
        m = os.path.getmtime(p)
    except OSError:
        return None
    if _BAUSTEINE.get(z, (None,))[0] != m:
        el, roh, seite = set(), set(), set()

        def geh(x):
            if isinstance(x, dict):
                if x.get('fn') == 'el':
                    el.add((x['a'][0], x['a'][1]))
                    for y in x['a'][2:]:
                        geh(y)
                elif x.get('fn') == 'roh':
                    roh.add(x['a'][0])
                elif x.get('fn') == 'seite':
                    seite.add(x['a'][0])
                    for y in x['a'][1:]:
                        geh(y)
        with open(p, encoding='utf-8') as f:
            g = json.load(f)
        for x in g.get('seiten', []):
            geh(x)
        _BAUSTEINE[z] = (m, dict(el=el, roh=roh, seite=seite, teile=g.get('teile', []), kopf=g.get('kopf'), fuss=g.get('fuss')))
    return _BAUSTEINE[z][1]


def _knoten_ok(n, wo, B, tiefe=0):
    """Ein Teil des Baums: Text (geprüft), Element mit bekanntem Tag und Merkmalen aus dem Grundstand, fester Teil aus dem Grundstand."""
    if tiefe > 40:
        return 'Die Karte ist zu tief verschachtelt.'
    if isinstance(n, str):
        return _text_ok(n, wo)
    if not isinstance(n, dict) or not isinstance(n.get('a'), list):
        return f'{wo}: Angaben in falscher Form.'
    fn, a = n.get('fn'), n['a']
    erlaubt = {'fn', 'a', 'aus', 'leer', 'lage', 'id'}
    if set(n) - erlaubt:
        return f'{wo}: unbekannte Angabe.'
    if 'id' in n and not (isinstance(n['id'], str) and re.fullmatch(r'[a-z]{1,4}\d{1,5}', n['id'])):
        return f'{wo}: unbekannte Kennung.'
    if fn == 'roh':
        return '' if len(a) == 1 and a[0] in B['roh'] else f'{wo}: ein fester Teil, den es in dieser Karte nicht gibt.'
    if fn == 'el':
        if len(a) < 2 or (a[0], a[1]) not in B['el'] or a[0] not in TAGE_OK:
            return f'{wo}: ein Baustein, den es in dieser Karte nicht gibt.'
        kinder = a[2:]
    elif fn == 'seite':
        if not a or a[0] not in B['seite']:
            return f'{wo}: eine Seite, die es in dieser Karte nicht gibt.'
        kinder = a[1:]
    else:
        return f'{wo}: unbekannter Baustein «{fn}».'
    if len(kinder) > 2000:
        return f'{wo}: zu viele Teile.'
    for k in kinder:
        f = _knoten_ok(k, wo, B, tiefe + 1)
        if f:
            return f
    return ''


LAGE_ZAHL = {'x': (-400, 400), 'y': (-400, 400), 's': (0.2, 5), 't': (0.2, 6), 'z': (0.5, 4), 'mt': (-40, 100), 'mb': (-40, 100), 'b': (0.5, 450), 'd': (0.05, 5), 'h': (3, 150)}
# Schäfli 21.10.2026: Schriften und Farben genau die von satz/satz.js (SCHRIFT, FARBE). Im Schlössli standen hier noch die des Gasterntal: jede Farbe
# und die Titelschrift aus «Gestalten» wurde beim Speichern abgewiesen (PRUEF). Prüfung: pruef/gleich.js speichert eine Gestaltung.
# Culinarium 28.10.2026: Schriften und Farben genau die von satz/satz.js (SCHRIFT, FARBE); nie fett, nie kursiv (Textart nur normal oder Versalien).
LAGE_WAHL = {'f': {'titel', 'zeile', 'instrument', 'etikett', 'mono'}, 'c': {'nacht', 'schiefer', 'tinte', 'leise', 'kerze', 'kerzet', 'kerzeh', 'papier', 'weiss'},
             'a': {'normal', 'versal'}, 'al': {'links', 'mitte', 'rechts'}}


def _lage_ok(v, tiefe=0):
    """Anordnung und Gestalten (Fortgeschritten): nur bekannte Felder, Zahlen in vernünftigen Grenzen, Wahlen aus der Liste des Hauses"""
    if tiefe > 4 or not isinstance(v, dict):
        return 'Eine Gestaltung hat eine unbekannte Form.'
    for k, w in v.items():
        if k in LAGE_ZAHL:
            lo, hi = LAGE_ZAHL[k]
            if not isinstance(w, (int, float)) or isinstance(w, bool) or not lo <= w <= hi:
                return f'Eine Gestaltung liegt ausserhalb der Grenzen ({k}).'
        elif k in LAGE_WAHL:
            if w not in LAGE_WAHL[k]:
                return f'Eine Gestaltung hat eine unbekannte Wahl ({k}).'
        elif k == 'aus':
            if not isinstance(w, bool):
                return 'Eine Gestaltung hat eine unbekannte Angabe.'
        elif isinstance(w, dict):   # Linie eines Eintrags, Teile der Seite, Elemente der Woche
            f = _lage_ok(w, tiefe + 1)
            if f:
                return f
        else:
            return 'Eine Gestaltung hat eine unbekannte Angabe.'
    return ''


def _gestalt_ok(x, tiefe=0):
    if tiefe > 16:
        return ''
    if isinstance(x, dict):
        for k, v in x.items():
            if k == 'lage':
                f = _lage_ok(v)
            else:
                f = _gestalt_ok(v, tiefe + 1)
            if f:
                return f
    elif isinstance(x, list):
        for v in x:
            f = _gestalt_ok(v, tiefe + 1)
            if f:
                return f
    return ''


def pruefe(d, z):
    """Was ein Entwurf haben muss, bevor er gespeichert wird. Gibt die erste Unstimmigkeit in Alltagssprache zurück."""
    if not isinstance(d, dict):
        return 'Die Karte hat keine Daten.'
    if d.get('ziel') != z:
        return 'Die Daten gehören zu einer anderen Karte.'
    f = _gestalt_ok({'seiten': d.get('seiten'), 'abend': d.get('abend')})
    if f:
        return f
    art = d.get('art')
    if art != ('abend' if z == 'abend' else 'satz'):   # Ruedihus 17.10.2026 (im Gasterntal übernommen): vorher entschied die Art in den Daten, ob die Satz-Prüfung lief (Lücke)
        return 'Unbekannte Art von Karte.'
    if art == 'abend':
        w = d.get('abend')
        if not isinstance(w, dict) or not re.fullmatch(r'\d{4}-\d\d-\d\d', str(w.get('ab', ''))) or not isinstance(w.get('tage'), list) or len(w['tage']) != 1:
            return 'Datum oder Menü des Abends fehlen.'
        for i, t in enumerate(w['tage']):
            for k, v in t.items():
                if k not in GAENGE_FELDER + ('zu', 'hinweis'):
                    return f'Menü: unbekanntes Feld «{k}».'
                f = _text_ok(v, 'Menü')
                if f or not isinstance(v, (str, bool)):
                    return f or 'Menü: falsche Angabe.'
        if set(w) - {'ab', 'titel', 'motto', 'mit', 'preis', 'zusatz', 'hinweis', 'fuss', 'tage', 'beispiel', 'lage'}:
            return 'Der Abend hat ein unbekanntes Feld.'
        for k in ('titel', 'motto', 'mit', 'preis', 'zusatz', 'hinweis', 'fuss'):
            f = _text_ok(w.get(k, ''), k)
            if f:
                return f
        return ''
    if not isinstance(d.get('seiten'), list) or not d['seiten']:
        return 'Die Karte hat keine Seiten.'
    if len(d['seiten']) > 60:
        return 'Die Karte hat zu viele Seiten.'
    if art != 'satz':
        return 'Unbekannte Art von Karte.'
    B = _bausteine(z)
    if B is None:
        return 'Der Grundstand der Karte fehlt (python3 _werkzeuge/carte/einlesen.py --grund).'
    if d.get('teile') != B['teile'] or d.get('kopf') != B['kopf'] or d.get('fuss') != B['fuss']:
        return 'Die festen Teile der Karte (Zeichen, Bilder, Kopf der Datei) lassen sich nicht ändern.'
    for i, s in enumerate(d['seiten']):
        if s.get('fn') != 'seite':
            return f'Seite {i + 1} ist kein Blatt.'
        f = _knoten_ok(s, f'Seite {i + 1}', B)
        if f:
            return f
    if not any(not s.get('aus') for s in d['seiten']):
        return 'Auf der Karte steht keine Seite mehr.'
    return ''


# ---------------------------------------------------------------- Lesen
def einstellungen():
    e = {'anschluss_pdf': False}
    try:
        with open(os.path.join(K, 'einstellungen.json'), encoding='utf-8') as f:
            e.update(json.load(f))
    except (OSError, ValueError):
        pass
    if DEMO:
        e.update(anschluss_pdf=False, demo=True)
    return e


def status():
    aus = []
    for z in ZIELE:
        s, e = _lies(_p('stand', z)), _lies(_p('entwurf', z))
        if not s:
            continue
        pdf = os.path.join(K, 'live', z + '.pdf')
        live = os.path.exists(pdf)
        if not live:   # noch nichts veröffentlicht: die PDF, die heute auf der Website liegt (website_pdfs)
            pdf = next((os.path.join(PROJ, r) for r in website_pdfs(z) if os.path.exists(os.path.join(PROJ, r))), os.path.join(PROJ, 'unterlagen', 'pdf', z + '.pdf'))
        aus.append(dict(live=live, ziel=z, name=s.get('name', z), unter=s.get('unter', ''), gruppe=s.get('gruppe', ''), art=s.get('art'), format=s.get('format'),
                        seiten=len([x for x in s.get('seiten', []) if not x.get('aus')]) if s.get('art') != 'abend' else 1, ab=(s.get('abend') or {}).get('ab') or s.get('ab', ''),
                        entwurf=bool(e) and _inhalt(e) != _inhalt(s), entwurf_zeit=(e or {}).get('gespeichert', '') if e else '', entwurf_wer=(e or {}).get('wer', '') if e else '',
                        pdf_zeit=datetime.datetime.fromtimestamp(os.path.getmtime(pdf)).strftime('%d.%m.%Y %H:%M') if os.path.exists(pdf) else '',
                        stand_zeit=s.get('veroeffentlicht', ''), stand_wer=s.get('wer', ''), verlauf=len(verlauf(z))))
    return dict(karten=aus, bau=dict(BAU), einstellungen=einstellungen(), rollen=ROLLEN, rechte={k: sorted(v) for k, v in RECHTE.items()})


# Gänge eines Abends (satz.js ABEND): Feld = Rudis Teller, Feld_z = Momos Drink dazu
GAENGE_FELDER = ('amuse', 'amuse_z', 'aperitif', 'aperitif_z', 'vorspeise', 'vorspeise_z', 'haupt', 'haupt_z', 'dessert', 'dessert_z', 'absacker', 'absacker_z')


def _tag_leer(t):
    return not t.get('zu') and not any(str(t.get(k, '')).strip() for k in GAENGE_FELDER)


def _inhalt(d):
    """Was zählt, wenn Entwurf und Stand verglichen werden"""
    return json.dumps({k: d.get(k) for k in ('seiten', 'abend', 'css')}, ensure_ascii=False, sort_keys=True)


def karte(z):
    _ziel(z)
    s = _lies(_p('stand', z))
    if not s:
        raise Fehler('LEER', 'Diese Karte ist noch nicht eingelesen (python3 _werkzeuge/carte/einlesen.py).', 500)
    e = _lies(_p('entwurf', z))
    return dict(stand=s, entwurf=e if e and _inhalt(e) != _inhalt(s) else None, entwurf_zeit=e.get('gespeichert', '') if e else '',
                entwurf_wer=e.get('wer', '') if e else '')


def grundstand(z):
    _ziel(z)
    return _lies(_p('grundstand', z))


# ---------------------------------------------------------------- Schreiben
def entwurf(z, d, was, wer, rolle, erwartet=None):
    _ziel(z)
    _recht(rolle, 'entwurf', z)
    f = pruefe(d, z)
    if f:
        raise Fehler('PRUEF', f)
    with _SCHLOSS:
        alt = _lies(_p('entwurf', z)) or _lies(_p('stand', z))
        # erwartet: Zeitstempel, den der Browser zuletzt gesehen hat ('' = noch nie veröffentlicht und kein Entwurf). 16.10.2026: vorher wurde ein leerer
        # Stempel gar nicht geprüft, dann überschrieb das zweite Fenster das erste still, solange eine Karte nie veröffentlicht war.
        if erwartet is not None and alt and (alt.get('gespeichert') or alt.get('veroeffentlicht') or '') != (erwartet or ''):
            raise Fehler('KONFLIKT', f'Inzwischen hat {alt.get("wer") or "jemand"} diese Karte geändert ({alt.get("gespeichert") or alt.get("veroeffentlicht")}). Bitte neu laden; deine Eingabe ist nicht verloren, sie steht noch im Fenster.', 409)
        if alt and _inhalt(alt) == _inhalt(d):
            return dict(ok=True, geaendert=False, zeit=alt.get('gespeichert', alt.get('veroeffentlicht', '')))
        if os.path.exists(_p('entwurf', z)):
            shutil.copy2(_p('entwurf', z), _p('entwurf', z) + '.vorher')
        neu = dict(d, schema=SCHEMA, gespeichert=_jetzt(), wer=wer)
        neu.pop('veroeffentlicht', None)
        _schreib(_p('entwurf', z), neu)
    protokoll(wer, rolle, 'entwurf', z, text=str(was)[:200])
    return dict(ok=True, geaendert=True, zeit=neu['gespeichert'])


def verwerfen(z, wer, rolle):
    _ziel(z)
    _recht(rolle, 'verwerfen', z)
    p = _p('entwurf', z)
    with _SCHLOSS:
        if os.path.exists(p):
            ziel = os.path.join(K, 'verlauf', z, 'verworfen-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.json')
            os.makedirs(os.path.dirname(ziel), exist_ok=True)
            shutil.move(p, ziel)
            if os.path.exists(p + '.vorher'):
                os.remove(p + '.vorher')
            protokoll(wer, rolle, 'verworfen', z, aufbewahrt=os.path.basename(ziel))
    return dict(ok=True)


def verlauf(z):
    d = os.path.join(K, 'verlauf', z)
    if not os.path.isdir(d):
        return []
    aus = []
    zeit = lambda x: re.sub(r'\D', '', x)[:14]
    for f in sorted((x for x in os.listdir(d) if x.endswith('.json')), key=zeit, reverse=True):
        try:
            with open(os.path.join(d, f), encoding='utf-8') as fh:
                x = json.load(fh)
        except (OSError, ValueError):
            continue
        aus.append(dict(datei=f, art='verworfen' if f.startswith('verworfen') else 'stand', zeit=x.get('veroeffentlicht') or x.get('gespeichert') or '',
                        wer=x.get('wer', ''), pdf=os.path.exists(os.path.join(d, f[:-5] + '.pdf'))))
    return aus


def version(z, datei):
    _ziel(z)
    if datei == 'grundstand':
        return grundstand(z)
    if not re.fullmatch(r'[\w.-]+\.json', datei or '') or '..' in datei:
        raise Fehler('DATEI', 'Diese Fassung gibt es nicht.', 404)
    d = _lies(os.path.join(K, 'verlauf', z, datei))
    if d is None:
        raise Fehler('DATEI', 'Diese Fassung gibt es nicht.', 404)
    return d


def zurueckholen(z, datei, wer, rolle):
    _recht(rolle, 'zurueckholen', z)
    d = dict(version(z, datei))
    for x in ('veroeffentlicht', 'gespeichert', 'wer'):
        d.pop(x, None)
    return entwurf(z, d, f'Fassung {datei} in den Entwurf geholt', wer, rolle)


# ---------------------------------------------------------------- Drucken (node + Playwright, wie pdf/druck.js) und prüfen
def drucke(z, art, aus):
    """art: 'stand' | 'entwurf'. Gibt den Bericht des Drucks zurück (Seiten, Schriftmass je Seite, was nicht passt)."""
    os.makedirs(os.path.dirname(aus), exist_ok=True)
    try:
        r = subprocess.run(['node', os.path.join(HIER, 'drucke.js'), z, art, aus], capture_output=True, text=True, timeout=240,
                           env=dict(os.environ, CARTE_PORT=os.environ.get('CARTE_PORT', PORT_STD)))
    except subprocess.TimeoutExpired:
        raise Fehler('DRUCK', 'Der Druck dauerte länger als vier Minuten und wurde abgebrochen.', 500)
    if r.returncode:
        fehler_log(f'Druck {z} ({art}) gescheitert: {(r.stderr or r.stdout)[-500:]}')
        raise Fehler('DRUCK', 'Die PDF liess sich nicht drucken. Läuft node, und ist Playwright installiert?', 500)
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        raise Fehler('DRUCK', 'Der Druck hat keinen Bericht geliefert.', 500)


LEISE = re.compile(r'^[\s·*|–\-]*$')


def texte(d):
    """Jeder Text, der auf der Karte steht (für «PDF = Daten»): alle Texte sichtbarer Elemente, ausgeblendete und leere zählen nicht"""
    if d.get('art') == 'abend':
        w = d['abend']
        aus = [v for t in w['tage'] if not t.get('zu') for k, v in t.items() if k in GAENGE_FELDER and str(v).strip()]
        aus += [t['hinweis'] for t in w['tage'] if t.get('zu') and str(t.get('hinweis', '')).strip()]
        return aus + [w[k] for k in ('titel', 'motto', 'mit', 'preis', 'zusatz', 'hinweis', 'fuss') if str(w.get(k, '')).strip()]
    aus = []

    def geh(x):
        if isinstance(x, str):
            if x.strip() and not LEISE.match(x):
                aus.append(x)
            return
        if not isinstance(x, dict) or x.get('aus'):
            return
        if x.get('fn') == 'roh':
            t = re.sub(r'<svg\b.*?</svg>|<[^>]+>|\ue010\d+\ue011', ' ', x['a'][0], flags=re.S)
            t = html.unescape(t)
            if t.strip() and not LEISE.match(t):
                aus.append(t)
            return
        kinder = x['a'][2:] if x.get('fn') == 'el' else x['a'][1:]
        if x.get('fn') == 'el' and x['a'][0] in ('img', 'svg'):
            return
        for y in kinder:
            geh(y)
    for s in d['seiten']:
        geh(s)
    return aus


def _norm(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\*\*|__|\\\*', '', t).replace('~', ' ').replace(' | ', ' ').replace('→', ' ').replace('☐', ' ').replace('◆', ' ')
    t = t.replace('\xa0', ' ').replace('’', "'").replace('‘', "'").replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('œ', 'oe')
    return re.sub(r'[^0-9a-zäöüéèêëàâîïôùûçß]+', '', t.lower())


WORT = re.compile(r'[0-9a-zäöüéèêëàâîïôùûçœß]+')


def _woerter(t):
    t = re.sub(r'[\ue000-\uf8ff]\d*[\ue000-\uf8ff]?', ' ', t)
    t = t.replace('\xad', '').replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('ﬀ', 'ff').replace('ﬃ', 'ffi').replace('œ', 'oe').replace('Œ', 'OE')
    t = re.sub(r'(\w)-\s*\n\s*(?=[a-zäöü])', r'\1', t)   # Trennung am Zeilenende
    return WORT.findall(t.lower())


def pdf_gleich_text(d, text, layout=''):
    """Steht jeder Text der Daten in der PDF? Doldenhorn 17.10.2026: Wort für Wort, unabhängig von der Reihenfolge im PDF. Die Karten stehen in
    Spalten und Kästen; ein Absatz, der umbricht, liegt im Text der PDF nicht am Stück (pdftotext und PyMuPDF lesen Spalten verschieden). Darum:
    jedes Wort jedes Textes muss in der PDF vorkommen, und zusammen nicht öfter, als die PDF es enthält (gezählt). Wo das nicht reicht (gesperrte
    Versalien, senkrechte Schrift, Trennung), muss der Text ohne Zwischenräume am Stück in der PDF stehen."""
    from collections import Counter
    ist = Counter(_woerter(text))
    strom = ''.join(_woerter(text))   # Zeichen ohne Zwischenraum: gesperrte Schrift (Versalien mit Abstand) und senkrechte Zeilen liest die PDF Buchstabe für Buchstabe
    # Schäfli 21.10.2026: gesperrte Versalien (Name des Hauses, Gänge) liest pdftotext Buchstabe für Buchstabe, und eine Fusszeile mitten unter den
    # Preisen liegt im Lesefluss zwischen ihnen. Zweiter Strom aus dem Text in Zeilen (pdftotext -layout): dort steht jede Zeile am Stück.
    strom2 = ''.join(_woerter(layout)) if layout else ''
    einheiten = [x for x in texte(d) if _woerter(x)]
    soll = Counter(w for x in einheiten for w in _woerter(x))
    zuviel = soll - ist
    fehlt = [x for x in einheiten if any(w in zuviel for w in _woerter(x)) and ''.join(_woerter(x)) not in strom and ''.join(_woerter(x)) not in strom2]
    return dict(woerter=sum(soll.values()), einheiten=len(einheiten), fehlt={x[:60]: 1 for x in fehlt}, woerter_fehlen=dict(list(zuviel.items())[:10]) if fehlt else {})


def pdf_gleich_daten(d, pdf):
    r = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True)
    if r.returncode:
        raise Fehler('PRUEFWERK', 'pdftotext fehlt (poppler). Ohne die Prüfung wird nichts veröffentlicht.', 500)
    r2 = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True)
    return pdf_gleich_text(d, r.stdout, r2.stdout if not r2.returncode else '')


# ---------------------------------------------------------------- Probe und Veröffentlichen
def probe(z, wer, rolle):
    _ziel(z)
    _recht(rolle, 'probe', z)
    art = 'entwurf' if os.path.exists(_p('entwurf', z)) else 'stand'
    aus = os.path.join(K, 'probe', z + '.pdf')
    b = drucke(z, art, aus)
    protokoll(wer, rolle, 'probe', z, seiten=b.get('seiten'), art=art)
    return dict(ok=True, url=f'/_werkzeuge/carte/api/pdf?z={z}&q=probe&t={int(time.time())}', seiten=b.get('seiten'), art=art, mass=b.get('mass'), warn=b.get('warn', []))


SCHRITTE = ['Der Entwurf wird geprüft', 'Die Karte wird gesetzt und gedruckt', 'PDF und Daten werden verglichen', 'Die neue Fassung wird übernommen']


def veroeffentlichen(z, wer, rolle):
    _ziel(z)
    _recht(rolle, 'veroeffentlichen', z)
    with _SCHLOSS:
        if BAU['laeuft']:
            raise Fehler('BAU', 'Gerade wird schon eine Karte veröffentlicht. Bitte kurz warten.', 409)
        e, s = _lies(_p('entwurf', z)), _lies(_p('stand', z))
        if not e or _inhalt(e) == _inhalt(s):
            return dict(ok=True, geaendert=False)
        f = pruefe(e, z)
        if f:
            raise Fehler('PRUEF', f)
        BAU.update(laeuft=True, ziel=z, schritt=SCHRITTE[0], schritte=SCHRITTE, fehler='', fertig='', start=time.time(), ende=0, bericht={})
    threading.Thread(target=_veroeffentlichen, args=(z, e, s, wer, rolle), daemon=True).start()
    return dict(ok=True, gestartet=True)


def _veroeffentlichen(z, e, s, wer, rolle):
    tmp = os.path.join(K, 'probe', z + '-neu.pdf')
    try:
        BAU['schritt'] = SCHRITTE[1]
        b = drucke(z, 'entwurf', tmp)
        if not b.get('seiten') or os.path.getsize(tmp) < 2000:
            raise Fehler('DRUCK', 'Die PDF ist leer.', 500)
        if b.get('fehler'):
            raise Fehler('PASST', 'Nicht alles passt auf die Seiten: ' + '; '.join(b['fehler'][:3]) + '. Bitte Einträge auf die nächste Seite schieben.', 409)
        BAU['schritt'] = SCHRITTE[2]
        v = pdf_gleich_daten(e, tmp)
        if v['fehlt']:
            raise Fehler('PDF', 'In der PDF fehlen Texte der Karte: ' + ' | '.join(list(v['fehlt'])[:5]), 500)
        BAU['schritt'] = SCHRITTE[3]
        zeit = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        with _SCHLOSS:
            vd = os.path.join(K, 'verlauf', z)
            os.makedirs(vd, exist_ok=True)
            shutil.copy2(_p('stand', z), os.path.join(vd, zeit + '.json'))
            live = os.path.join(K, 'live', z + '.pdf')
            if os.path.exists(live):
                shutil.copy2(live, os.path.join(vd, zeit + '.pdf'))
            os.makedirs(os.path.dirname(live), exist_ok=True)
            os.replace(tmp, live)
            neu = dict(e, veroeffentlicht=_jetzt(), wer=wer)
            neu.pop('gespeichert', None)
            _schreib(_p('stand', z), neu)
            for x in (_p('entwurf', z), _p('entwurf', z) + '.vorher'):
                if os.path.exists(x):
                    os.remove(x)
        anschluss = _anschluss(z, live)
        n = b.get('seiten', 0)
        BAU.update(laeuft=False, schritt='', ende=time.time(), bericht=dict(woerter=v['woerter'], mass=b.get('mass'), warn=b.get('warn', []), anschluss=anschluss),
                   fertig=f'{n} Seite{"" if n == 1 else "n"}, {v["woerter"]} Wörter geprüft')
        protokoll(wer, rolle, 'veroeffentlicht', z, seiten=n, woerter=v['woerter'], voriger=f'verlauf/{z}/{zeit}.json', anschluss=anschluss)
    except Exception as ex:  # noqa: BLE001  nichts ausgetauscht, solange der Druck nicht geprüft ist
        text = ex.text if isinstance(ex, Fehler) else str(ex)
        BAU.update(laeuft=False, schritt='', fehler=text[-500:], ende=time.time())
        fehler_log(f'Veröffentlichen {z} abgebrochen (nichts geändert): {text[-300:]}')
        protokoll(wer, rolle, 'veroeffentlichen-abgebrochen', z, grund=text[:200])
        if os.path.exists(tmp):
            os.remove(tmp)


# Wo die Website die PDF der Karte zeigen würde: website/unterlagen/pdf/<karte>.pdf, eine Quelle für Werkzeug, Website und PDF (Robert 17.10.2026:
# «La Carte ist die eine Quelle der Speisekarten»). Die Website des Culinarium verlinkt heute keine Karten-PDF; sie zeigt die Menükarte im Abend
# (abende.html) aus website/abende_info.py KARTEN. Mit Anschluss liest sie die Karten aus karten.json (C27, Einbau in website/ offen, Revier der Website).
WEBSITE_PDF = {z: (None, None) for z in ZIELE}   # kein Feld «… als PDF» in der Website des Culinarium


def website_pdfs(z):
    """Die Dateien der Website für die PDF dieser Karte. Hat Le Bureau die Angabe «… als PDF» auf eine andere eigene Datei gestellt, gilt diese."""
    feld, std = WEBSITE_PDF[z]
    ziel = std
    if feld:
        try:
            with open(os.path.join(PROJ, 'inhalt', 'stand.json'), encoding='utf-8') as f:
                w = (json.load(f).get('fakten') or {}).get(feld)
            if isinstance(w, str) and re.fullmatch(r'assets/pdf/[\w.-]+\.pdf', w):
                ziel = w
        except (OSError, ValueError):
            pass
    return ['unterlagen/pdf/' + z + '.pdf'] + ([ziel] if ziel else [])


def _anschluss(z, live):
    """Nach dem Veröffentlichen: karten.json im Revier des Werkzeugs immer neu (web.py, C27: die Karten in der Form der Website). Mit Anschluss geht
    die PDF zusätzlich nach website/unterlagen/pdf/<karte>.pdf (die vorige liegt im Verlauf). Solange die Datei DEMO liegt oder der Anschluss aus ist
    (Standard: die Website ist eine Designstudie und wird nicht still verändert), schreibt La Carte nie in website/."""
    try:
        import web
        teil = web.anschliessen(K, ZIELE, _lies)
    except Exception as e:  # noqa: BLE001  die PDF ist schon richtig, die Datei meldet ihren Fehler einzeln
        fehler_log(f'karten.json {z}: {e!r}')
        teil = 'karten.json nicht geschrieben: ' + str(e)[:120]
    if DEMO:
        return 'demo · ' + teil
    if not einstellungen().get('anschluss_pdf'):
        return 'aus · ' + teil
    zeit = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    aus = []
    for rel in website_pdfs(z):
        ziel = os.path.join(PROJ, rel)
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        if os.path.exists(ziel):
            sd = os.path.join(K, 'verlauf', z, 'website-' + zeit + '-' + rel.replace('/', '_'))   # Gasterntal 17.10.2026: zwei Namen, die sich nur in Gross/Klein unterscheiden, sind auf dem Mac dieselbe Datei
            os.makedirs(os.path.dirname(sd), exist_ok=True)
            shutil.copy2(ziel, sd)
        shutil.copy2(live, ziel + '.neu')
        os.replace(ziel + '.neu', ziel)
        with open(ziel, 'rb') as f1, open(live, 'rb') as f2:   # nachprüfen
            if f1.read() != f2.read():
                raise Fehler('ANSCHLUSS', f'{rel}: nach dem Kopieren nicht gleich.', 500)
        aus.append(rel)
    return ' und '.join(aus) + ' · ' + teil


def setze_einstellungen(d, wer, rolle):
    _recht(rolle, 'einstellungen')
    if DEMO and d.get('anschluss_pdf'):
        raise Fehler('DEMO', 'Demo: Der Anschluss an die Website wird erst mit dem Auftrag eingeschaltet. Die Website bleibt, wie sie ist.', 409)
    e = einstellungen()
    if 'anschluss_pdf' in d:
        e['anschluss_pdf'] = bool(d['anschluss_pdf'])
    e.pop('demo', None)
    _schreib(os.path.join(K, 'einstellungen.json'), e)
    protokoll(wer, rolle, 'einstellungen', '', **e)
    return e


# ---------------------------------------------------------------- Sicherung, Protokoll, Zustand
def sicherung():
    """Einmal am Tag: Stand, Entwürfe, Verlauf und Einstellungen als Archiv (14 Tage aufbewahrt)."""
    d = os.path.join(K, 'sicherung')
    os.makedirs(d, exist_ok=True)
    name = os.path.join(d, datetime.date.today().isoformat() + '.tar.gz')
    if os.path.exists(name):
        return name
    with tarfile.open(name + '.neu', 'w:gz') as tar:
        for teil in ('stand', 'entwurf', 'verlauf', 'live', 'einstellungen.json', 'protokoll.jsonl'):
            p = os.path.join(K, teil)
            if os.path.exists(p):
                tar.add(p, arcname=teil)
    os.replace(name + '.neu', name)
    for alt in sorted(x for x in os.listdir(d) if x.endswith('.tar.gz'))[:-14]:
        os.remove(os.path.join(d, alt))
    return name


def protokoll_lesen(n=80, z=''):
    try:
        with open(os.path.join(K, 'protokoll.jsonl'), encoding='utf-8') as f:
            zeilen = [json.loads(x) for x in f if x.strip()]
    except (OSError, ValueError):
        return []
    if z:
        zeilen = [x for x in zeilen if x.get('karte') == z]
    return zeilen[-n:][::-1]


def gesund():
    """Zustand für die Überwachung: Daten lesbar, Druckwerkzeuge da, Platz, letzte Fehler."""
    pruef = {}
    for z in ZIELE:
        try:
            pruef[z] = bool(_lies(_p('stand', z)))
        except Fehler:
            pruef[z] = False
    werkzeug = {'node': shutil.which('node') is not None, 'pdftotext': shutil.which('pdftotext') is not None, 'playwright': os.path.isdir(NODE_PW)}
    groesse = 0
    for d, _, fs in os.walk(K):
        groesse += sum(os.path.getsize(os.path.join(d, f)) for f in fs)
    try:
        with open(os.path.join(K, 'fehler.log'), encoding='utf-8') as f:
            fehler = [x.rstrip() for x in f.readlines()[-5:]]
    except OSError:
        fehler = []
    ok = all(pruef.values()) and all(werkzeug.values())
    return dict(ok=ok, karten=pruef, werkzeug=werkzeug, speicher_mb=round(groesse / 1e6, 1), seit=int(time.time() - START), fehler=fehler,
                browserfehler=browserfehler_lesen())


# ---------------------------------------------------------------- Fehler aus dem Browser (R03) und Prüfung (R23)
def browserfehler(d):
    """Ein Skriptfehler aus dem Browser (fehlermelder.js). Ohne Rolle erlaubt, nur Text, kurz; höchstens die letzten 200 bleiben."""
    text = d.get('text') if isinstance(d.get('text'), str) else ''
    if not text.strip():
        raise Fehler('FORM', 'Ohne Text.')
    e = dict(zeit=_jetzt(), text=re.sub(r'[\x00-\x1f]', ' ', text)[:500], seite=re.sub(r'[^\w.-]', '', str(d.get('seite', '')))[:40])
    p = os.path.join(K, 'browserfehler.jsonl')
    with _SCHLOSS:
        try:
            with open(p, encoding='utf-8') as f:
                zeilen = f.readlines()[-199:]
        except OSError:
            zeilen = []
        zeilen.append(json.dumps(e, ensure_ascii=False) + '\n')
        os.makedirs(K, exist_ok=True)
        with open(p + '.neu', 'w', encoding='utf-8') as f:
            f.writelines(zeilen)
        os.replace(p + '.neu', p)
    return dict(ok=True)


def browserfehler_lesen(n=20):
    try:
        with open(os.path.join(K, 'browserfehler.jsonl'), encoding='utf-8') as f:
            return [json.loads(x) for x in f.readlines()[-n:] if x.strip()][::-1]
    except (OSError, ValueError):
        return []


def pruefung():
    """Alles für die Prüfseite: Zustand, Sicherungen, Verlauf je Karte, Entwürfe, letzte Fehler."""
    g = gesund()
    sd = os.path.join(K, 'sicherung')
    sich = sorted((x for x in os.listdir(sd) if x.endswith('.tar.gz')), reverse=True) if os.path.isdir(sd) else []
    karten = []
    for z in ZIELE:
        try:
            s, e = _lies(_p('stand', z)), _lies(_p('entwurf', z))
        except Fehler:
            s, e = None, None
        karten.append(dict(ziel=z, name=(s or {}).get('name', z), lesbar=bool(s), entwurf=bool(e) and bool(s) and _inhalt(e) != _inhalt(s),
                           stand=(s or {}).get('veroeffentlicht', ''), verlauf=len(verlauf(z)), grundstand=os.path.exists(_p('grundstand', z))))
    probe = os.path.join(K, 'probe')
    return dict(g, sicherungen=[dict(datei=x, mb=round(os.path.getsize(os.path.join(sd, x)) / 1e6, 2)) for x in sich], kartenliste=karten,
                probe_pdfs=len([x for x in os.listdir(probe) if x.endswith('.pdf')]) if os.path.isdir(probe) else 0, bau=dict(BAU))


def werkzeugname():
    """Name des Werkzeugs aus der einen Stelle (_werkzeuge/oberflaeche/kleid/culinarium.js, WO_HAUS.namen.karten); Ersatz der Arbeitsname"""
    try:
        with open(os.path.join(_WURZEL, '_werkzeuge', 'oberflaeche', 'kleid', 'culinarium.js'), encoding='utf-8') as f:
            m = re.search(r"namen:\s*\{[^}]*?karten:\s*'([^']+)'", f.read())
        return m.group(1) if m else 'La Carte'
    except OSError:
        return 'La Carte'


def export():
    """Alle Daten von La Carte in einer Datei (Master 9d Nr. 21): je Karte Stand, Entwurf und Ursprung, dazu Verlauf, Einstellungen, Protokoll."""
    karten = {}
    for z in ZIELE:
        try:
            karten[z] = dict(stand=_lies(_p('stand', z)), entwurf=_lies(_p('entwurf', z)), ursprung=_lies(_p('grundstand', z)),
                             verlauf={x['datei']: version(z, x['datei']) for x in verlauf(z)})
        except Fehler as e:
            karten[z] = dict(fehler=e.text)
    return dict(werkzeug=f'{werkzeugname()} · Culinarium Hannover', zeit=_jetzt(), schema=SCHEMA, karten=karten, einstellungen=einstellungen(), protokoll=protokoll_lesen(10000))


def reparatur(d, wer, rolle):
    """Reparaturen der Prüfseite (nur Direktion): Sicherung jetzt, Probe-PDFs wegräumen, Fehlerlisten leeren. Nichts davon ändert eine Karte."""
    _recht(rolle, 'reparatur')
    art = d.get('art')
    if art == 'sicherung':
        p = os.path.join(K, 'sicherung', datetime.date.today().isoformat() + '.tar.gz')
        if os.path.exists(p):
            os.remove(p)
        name = sicherung()
        aus = dict(ok=True, text=f'Sicherung angelegt: {os.path.basename(name)}')
    elif art == 'probe':
        d0 = os.path.join(K, 'probe')
        n = 0
        for x in (os.listdir(d0) if os.path.isdir(d0) else []):
            if x.endswith('.pdf') and not x.endswith('-neu.pdf'):
                os.remove(os.path.join(d0, x))
                n += 1
        aus = dict(ok=True, text=f'{n} Probe-PDF weggeräumt.')
    elif art == 'fehler':
        for x in ('browserfehler.jsonl', 'fehler.log'):
            p = os.path.join(K, x)
            if os.path.exists(p):
                os.replace(p, p + '.' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.alt')
        aus = dict(ok=True, text='Fehlerlisten geleert (die alten liegen daneben).')
    else:
        raise Fehler('WEG', 'Diese Reparatur gibt es nicht.', 404)
    protokoll(wer, rolle, 'reparatur', '', art=art)
    return aus


# ---------------------------------------------------------------- Wege
def get(was, q, wer='', rolle=''):
    z = (q.get('z') or [''])[0]
    if was == 'status':
        return status()
    if was == 'karte':
        return karte(z)
    if was == 'grundstand':
        return grundstand(z)
    if was == 'verlauf':
        return dict(liste=verlauf(_ziel(z)))
    if was == 'version':
        return version(z, (q.get('datei') or [''])[0])
    if was == 'protokoll':
        return dict(liste=protokoll_lesen(z=z))
    if was == 'gesund':
        return gesund()
    if was == 'pruefung':
        return pruefung()
    if was == 'export':
        return export()
    raise Fehler('WEG', 'Unbekannte Anfrage.', 404)


def post(was, d, wer, rolle):
    z = d.get('z', '')
    if was == 'entwurf':
        return entwurf(z, d.get('daten'), d.get('was', ''), wer, rolle, d.get('erwartet'))
    if was == 'verwerfen':
        return verwerfen(z, wer, rolle)
    if was == 'probe':
        return probe(z, wer, rolle)
    if was == 'veroeffentlichen':
        return veroeffentlichen(z, wer, rolle)
    if was == 'zurueckholen':
        return zurueckholen(z, d.get('datei', ''), wer, rolle)
    if was == 'einstellungen':
        return setze_einstellungen(d, wer, rolle)
    if was == 'fehler':
        return browserfehler(d)
    if was == 'reparatur':
        return reparatur(d, wer, rolle)
    raise Fehler('WEG', 'Unbekannte Anfrage.', 404)
