#!/usr/bin/env python3
"""L’Imprimerie · Culinarium Hannover, eigener Prüfserver:  python3 serve.py [port]   (Standard 9087) → http://127.0.0.1:9087/_werkzeuge/imprimerie/
Bildet die Wege des Hauses nach (Vorlage: Prüfserver der Werkstatt der Taverne zum Schäfli, dort nur gelesen), damit L’Imprimerie hier genau so läuft wie unter /_werkzeuge/imprimerie/
und online (/werkzeuge/imprimerie/): Le Livre liegt daneben unter /_werkzeuge/livre/, die Fotos der Website unter /assets/bild/, das Oberflächen-Paket unter
/assets/oberflaeche/ (_werkzeuge/oberflaeche/, Chat «culinarium-maison»), Schriften und Zeichen der Website unter /assets/schrift/ und /assets/zeichen/. Alles nur lesend, nur diese Wege.

KI: Ohne ausdrückliches IMPRIMERIE_KI=1 antwortet /api/entwurf mit einer Probe-Antwort aus den Vorlagen des Hauses (kostet nichts, Regel 54).
Ein Schlüssel wird nie aus dem Vault gelesen; nur ANTHROPIC_API_KEY aus der Umgebung, und nur zusammen mit IMPRIMERIE_KI=1.
Wache wie online (api/entwurf.py wache): fremde Herkunft 403, nur JSON 415, Grösse 413, 40 Entwürfe je Stunde und Absender 429.
Markenprüfung (POST /_werkzeuge/livre/api/pruefen) geht an den Server von Le Livre (LIVRE_SERVER, Standard http://127.0.0.1:9085, _werkzeuge/livre/server.py des Hauses)."""
import glob, json, os, re, sys, time, urllib.error, urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote

HIER = os.path.dirname(os.path.abspath(__file__))
DH = os.path.dirname(os.path.dirname(HIER))                   # Culinarium Hannover (Projektordner)
WEB = os.path.join(DH, 'website')                              # die Website des Hauses (nur gelesen)
LIVRE = os.path.join(DH, '_werkzeuge', 'livre')
sys.path.insert(0, os.path.join(HIER, 'api'))
import entwurf as E  # noqa: E402
import plakat as P  # noqa: E402   (Abend beschreiben → Vorschläge, Probe aus der Motiv-Sammlung)

WEG = '/_werkzeuge/imprimerie/'
KI = os.environ.get('IMPRIMERIE_KI') == '1' and bool(os.environ.get('ANTHROPIC_API_KEY'))
LIVRE_SERVER = os.environ.get('LIVRE_SERVER', 'http://127.0.0.1:9085')
NUR_LESEN = {   # Weg → Ordner, nur diese Dateiarten
    '/_werkzeuge/livre/livre.json': (os.path.join(LIVRE, 'livre.json'), None),
    '/_werkzeuge/livre/dateien/': (os.path.join(LIVRE, 'dateien'), r'\.(png|svg|webp|jpg|css|json|ase|zip|ttf|woff2?)$'),
    '/_werkzeuge/livre/fotos/': (os.path.join(LIVRE, 'fotos'), r'\.(webp|jpg|png)$'),
    '/assets/bild/': (os.path.join(WEB, 'assets', 'bild'), r'\.(webp|jpg|png|svg)$'),
    # Werkzeug-Oberfläche «Die Bühne» des Hauses: _werkzeuge/oberflaeche/ (einziger Schreiber Chat «culinarium-maison»), solange es website/assets/oberflaeche/ nicht gibt
    '/assets/oberflaeche/': (os.path.join(WEB, 'assets', 'oberflaeche') if os.path.isdir(os.path.join(WEB, 'assets', 'oberflaeche')) else os.path.join(DH, '_werkzeuge', 'oberflaeche'), r'\.(css|js|svg)$'),
    '/assets/schrift/': (os.path.join(WEB, 'assets', 'schrift'), r'\.(woff2?|ttf)$'),
    '/assets/zeichen/': (os.path.join(WEB, 'assets', 'zeichen'), r'\.svg$'),
}


MONATE = ['januar', 'februar', 'märz', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'dezember']
def menue_datum(ueber):
    """Datum einer Menükarte («Fr 27. und Sa 28. November 2026», «Dezember 2025») oder None"""
    import datetime
    m = re.search(r'(\d{1,2})\.?\s+(' + '|'.join(MONATE) + r')\s+(\d{4})', ueber.lower()) or re.search(r'()(' + '|'.join(MONATE) + r')\s+(\d{4})', ueber.lower())
    return datetime.date(int(m.group(3)), MONATE.index(m.group(2)) + 1, int(m.group(1)) if m.group(1) else 1) if m else None


def menue_kommt(ueber):
    """True, wenn das Datum einer Menükarte heute oder später liegt"""
    import datetime
    d = menue_datum(ueber)
    return bool(d and d >= datetime.date.today())


def probe(daten):
    """Nachgestellte Antwort im Format der KI, gebaut aus den geprüften Vorlagen des Hauses (Wörter des Auftrags gegen Titel und Text)."""
    if str(daten.get('haus') or 'culinarium') != 'culinarium':
        raise ValueError('Unbekanntes Haus')
    if daten.get('bildtext'):
        return {'bildtext': {'text': '[Bildtext der KI] · Probe ohne KI: ' + str(daten['bildtext'].get('art') or 'Beitrag'), 'hashtags': ['#Hannover', '#Linden'],
                             'hinweise': ['Beispiel: So sieht der Bildtext aus; mit eingeschalteter KI schreibt das Studio ihn zum Bild.'], 'sprache': daten['bildtext'].get('sprache', 'de')}, 'verbrauch': {}}
    if str(daten.get('haus') or 'culinarium') != 'culinarium':   # wie api/entwurf.py: nur das eigene Haus
        raise ValueError('Unbekanntes Haus')
    auftrag = str(daten.get('auftrag') or '').strip()[:1500]
    if len(auftrag) < 4:
        raise ValueError('Auftrag fehlt')
    a_low = auftrag.lower()
    woerter = {w for w in re.findall(r'[a-zäöüé]{4,}', a_low)}
    # Abnahme-Tor 29.10.: Wortstamm statt nur ganzes Wort («Platzkarten» findet «Platzkarte»), Arten auch über ihre Alltagsnamen
    ART_WORT = {'tischkarte': ('platzkarte', 'tischkarte', 'namensschild', 'tischnummer'), 'menuekarte': ('menükarte', 'menuekarte', 'speisekarte'),
                'abendplakat': ('plakat des abends',), 'plakat': ('plakat', 'aushang an der wand'), 'flyer': ('flyer',), 'story': ('story',), 'instagram': ('instagram', 'beitrag'),
                'gutschein': ('gutschein',), 'einladung': ('einladung',), 'aushang': ('aushang',), 'hinweiskarte': ('hinweis',), 'newsletter': ('newsletter', 'e-mail')}
    trifft = lambda w, t: w in t or (len(w) > 6 and (w[:-1] in t or w[:-2] in t))
    dc = 'dirty chicken' in a_low or 'dirty-chicken' in a_low   # Dirty-Chicken-Aufträge nehmen immer die Dirty-Chicken-Marke (Ton «dc», Zeichen 3)
    beste = []
    for f in glob.glob(os.path.join(HIER, 'haeuser', 'culinarium', 'vorlagen', '*.json')):
        if f.endswith('index.json'):
            continue
        d = json.load(open(f, encoding='utf-8'))
        if daten.get('format') and d['format'] != daten['format']:
            continue
        art = os.path.basename(f)[:-5]   # nennt der Auftrag die Art («Flyer», «Plakat», «Platzkarten» …), geht diese vor (Demo-Check Schlössli 21.10.2026)
        art_bonus = 3 if art in a_low or any(x in a_low for x in ART_WORT.get(art, ())) else 0
        for v in d['vorlagen']:
            if v['vorlage'] == 'menue' and menue_kommt(v['inhalt'].get('ueber', '')):
                continue   # Menükarte eines kommenden Abends: dafür ist kein Menü belegt (Abnahme-Tor 30.10.2026), nie als Beispiel
            t = (v['titel'] + ' ' + json.dumps(v['inhalt'], ensure_ascii=False)).lower()
            menue_bonus = 4 + ((menue_datum(v['inhalt'].get('ueber', '')) or __import__('datetime').date(2000, 1, 1)).toordinal() - 730000) / 1e5 if v['vorlage'] == 'menue' and re.search(r'men[üu]e?karte|\bmen[üu]\b', a_low) and re.search(r'\d{1,2}\.\s+\w+\s+\d{4}', v['inhalt'].get('ueber', '')) else 0   # bei Gleichstand der jüngste vergangene Abend mit vollem Datum (wie website/abende_info.py)   # «Menükarte am Tisch …» ist eine Menükarte, nicht die Karte «Pairing zum Gang» (30.10.2026)
            beste.append((sum(trifft(w, t) for w in woerter) + art_bonus + menue_bonus + (4 if dc and v.get('ton') == 'dc' else 0) - (4 if not dc and v.get('ton') == 'dc' else 0), d['format'], v, art))
    beste.sort(key=lambda x: -x[0])
    if not beste:
        raise ValueError('Keine passende Vorlage')
    _, fmt, v, art_v = beste[0]
    # Entwürfe in anderen Aufbauten brauchen Titel und Text: fehlen sie der Vorlage (Plakat nur mit Motiv), kommen sie aus der nächsten Vorlage mit Text
    text_inhalt = v['inhalt'] if v['inhalt'].get('titel') else next((x[2]['inhalt'] for x in beste if x[2]['inhalt'].get('titel') and x[3] == art_v), None) or next((x[2]['inhalt'] for x in beste if x[2]['inhalt'].get('titel')), {})
    def inhalt_fuer(vorlage):
        if vorlage == v['vorlage']:
            return v['inhalt']
        i = dict(text_inhalt); i.pop('liste', None) if vorlage not in ('karte', 'menue', 'programm') else None
        if v['inhalt'].get('bild') and not (str(v['inhalt']['bild']).startswith(('pl_', 'po_')) and text_inhalt.get('bild')): i['bild'] = v['inhalt']['bild']   # Rudis Illustrationen gibt es nur klein: in grossen Fotoaufbauten das Foto der Textvorlage
        return i
    NAMEN = ['Lena Brandt', 'Jonas Albers', 'Mira Okafor', 'Paul Wendt', 'Sophie Krüger']   # Platzkarten mit Namen: je Entwurf ein Beispielname
    def seite(vorlage, ton, n=0):
        i = inhalt_fuer(vorlage)
        if art_v == 'tischkarte' and 'namen' in a_low and i.get('titel'): i = dict(i, titel=NAMEN[n % len(NAMEN)])
        return {'vorlage': vorlage, 'ton': 'dc' if dc else ton, 'inhalt': i}
    hinweis = ['Beispiel: gewählt wurde die passendste fertige Vorlage «' + v['titel'] + '». Mit eingeschalteter KI schreibt das Studio die Texte zum Auftrag.']
    if daten.get('varianten') and v['vorlage'] == 'menue':
        # Menükarten (Abnahme-Tor 29.10.2026: Entwürfe 2–5 als Aushang und Titelblatt füllten nur 40 %): alle fünf im Menükarten-Satz der Vorlagen,
        # gleicher Inhalt, verschieden in Ausrichtung, Rahmen und Grund, wie die Menükarten der Bibliothek selbst
        grund = dict(v.get('stil') or {})
        def mstil(ausr, rahmen): return dict(grund, ausr=ausr, rahmen=rahmen)
        def mseite(ton, st): return {'vorlage': 'menue', 'ton': 'dc' if dc else ton, 'inhalt': v['inhalt'], 'stil': st}
        A = {'l': 'links', 'c': 'mittig'}; R = {'ohne': 'ohne Rahmen', 'einfach': 'mit Rahmen'}; T = {'hell': 'Warmweiss', 'creme': 'Plakatpapier', 'dunkel': 'Nacht'}
        # Abnahme-Tor 30.10.2026: die fünf waren fast gleich (der Aufbau «menue» setzt Ausrichtung und Rahmen selbst). Jetzt verschieden in Aufbau, Gewichtung
        # und Satz, immer derselbe Abend: Menükarte, Menükarte im anderen Ton, Teller und Drinks als Liste, nur die Drinks, die Teller in Rudis Zeilen
        mi = v['inhalt']; L = [e for e in mi.get('liste', []) if e.get('name') or e.get('detail')]
        def kseite(ton, inhalt): return {'vorlage': 'karte', 'ton': 'dc' if dc else ton, 'inhalt': dict(inhalt, fuss=mi.get('fuss', ''), akzent=mi.get('akzent'))}
        teller = [e for e in L if e.get('name')]
        varianten = [{'titel': 'Wie die Vorlage', 'seiten': [dict(seite(v['vorlage'], v['ton'], 0), stil=v.get('stil'))]},
                     {'titel': 'Menükarte, ' + ('Violett' if dc else T['dunkel' if v['ton'] != 'dunkel' else 'creme']), 'seiten': [mseite('dunkel' if v['ton'] != 'dunkel' else 'creme', grund)]},
                     {'titel': 'Teller und Drinks als Liste, ' + ('Violett' if dc else T['creme']), 'seiten': [kseite('creme', dict(ueber=mi.get('ueber', ''), titel=mi.get('titel', 'Menü'),
                         liste=[dict(name=e.get('name') or e.get('gang') or e.get('detail'), detail=e.get('detail', '') if (e.get('name') or e.get('gang')) else '', preis='') for e in L]))]},
                     {'titel': 'Die Drinks, ' + ('Violett' if dc else T['hell']), 'seiten': [kseite('hell', dict(ueber=mi.get('ueber', ''), titel='Die Drinks',
                         liste=[dict(name=e.get('gang', ''), detail=e['detail'], preis='') for e in L if e.get('detail')]))]}
                     if sum(1 for e in L if e.get('detail')) >= 3 else
                     {'titel': 'Menükarte, ' + ('Violett' if dc else T['creme' if v['ton'] != 'creme' else 'hell']), 'seiten': [mseite('creme' if v['ton'] != 'creme' else 'hell', grund)]}]
        rudi = teller and all('|' in e['name'] and len(e['name']) <= 44 and all(len(x.strip()) <= 22 for x in e['name'].split('|')) for e in teller)   # nur kurze Zeilen wie Rudis eigene
        if not rudi:
            varianten.append({'titel': 'Menükarte, ' + ('Violett' if dc else T['creme' if v['ton'] != 'creme' else 'hell']), 'seiten': [mseite('creme' if v['ton'] != 'creme' else 'hell', grund)]})
        else:   # Rudis Zeilen: Versalien mit «/» (Hausregel)
            varianten.append({'titel': 'Die Teller in Rudis Zeilen, ' + ('Violett' if dc else T['dunkel']), 'seiten': [kseite('dunkel', dict(ueber=mi.get('ueber', ''), titel='Vom Pass',
                liste=[dict(name=' / '.join(x.strip() for x in re.split(r'\s*[|·]\s*', e['name'])).upper(), detail=e.get('detail', ''), preis='') for e in teller]))]})   # mit dem Drink darunter, sonst bleibt unten ein Loch
        return {'entwuerfe': {'name': v['titel'], 'format': fmt, 'varianten': varianten, 'hinweise': hinweis}, 'verbrauch': {}}
    if daten.get('varianten'):
        andere = [('buehne', 'dunkel'), ('fenster', 'creme'), ('geteilt', 'hell'), ('aushang', 'dunkel'), ('deckel', 'creme')]
        varianten = [{'titel': 'Wie die Vorlage', 'seiten': [seite(v['vorlage'], v['ton'], 0)]}]
        for a, t in andere:
            if len(varianten) == 5:
                break
            if (a, t) != (v['vorlage'], v['ton']) and not (dc and a == v['vorlage']) and (a not in ('buehne', 'fenster', 'geteilt') or v['inhalt'].get('bild') or text_inhalt.get('bild')):
                varianten.append({'titel': {'buehne': 'Foto gross', 'fenster': 'Ruhig im Rahmen', 'geteilt': 'Foto und Text', 'aushang': 'Nur Schrift', 'deckel': 'Titelblatt'}[a] + ', ' + ('Violett' if dc else {'dunkel': 'Nacht', 'creme': 'Plakatpapier', 'hell': 'Warmweiss'}[t]), 'seiten': [seite(a, t, len(varianten))]})
        schon = {(x['seiten'][0]['vorlage'], x['seiten'][0]['ton']) for x in varianten}   # auffüllen ohne Doppel: Titelblatt und Nur Schrift in den Tönen, die noch fehlen
        for a, t in [('deckel', 'hell'), ('deckel', 'dunkel'), ('aushang', 'creme'), ('aushang', 'hell'), ('deckel', 'creme')]:
            if len(varianten) == 5: break
            if (a, 'dc' if dc else t) in schon: continue
            schon.add((a, 'dc' if dc else t))
            varianten.append({'titel': {'aushang': 'Nur Schrift', 'deckel': 'Titelblatt'}[a] + ', ' + ('Violett' if dc else {'dunkel': 'Nacht', 'creme': 'Plakatpapier', 'hell': 'Warmweiss'}[t]), 'seiten': [seite(a, t, len(varianten))]})
        while len(varianten) < 5:
            varianten.append({'titel': 'Titelblatt, ' + ('Violett' if dc else 'Warmweiss'), 'seiten': [seite('deckel', 'hell', len(varianten))]})
        return {'entwuerfe': {'name': v['titel'], 'format': fmt, 'varianten': varianten, 'hinweise': hinweis}, 'verbrauch': {}}
    return {'entwurf': {'name': v['titel'], 'format': fmt, 'seiten': [seite(v['vorlage'], v['ton'])], 'hinweise': hinweis}, 'verbrauch': {}}


def entwurf_antwort(kopf, ip, roh):
    """Für einen Server des Hauses (Anschluss in LIEFERUNG.md): POST /_werkzeuge/imprimerie/api/entwurf → (code, antwort). Gleiche Wache und Probe wie hier."""
    nein = E.wache({k.lower(): v for k, v in kopf.items()}, ip)
    if nein:
        return nein[0], {'fehler': nein[1]}
    try:
        daten = json.loads(roh or b'{}')
        return 200, (E.entwurf(daten) if KI else probe(daten))
    except ValueError as e:
        return 400, {'fehler': str(e)}
    except Exception as e:
        return 502, {'fehler': str(e)}


DOK_VB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haeuser', 'culinarium', 'vorschau-dok')   # fertige Vorschaubilder der Galerien (29.10.)
VB_INDEX = os.path.join(DOK_VB, 'index.json')
import threading  # noqa: E402
VB_SPERRE = threading.Lock()


def vb_index():
    try:
        return json.load(open(VB_INDEX, encoding='utf-8'))
    except Exception:
        return {}


def vb_ablegen(k, roh, k2=''):
    """Vorschau einer Galerie-Karte ablegen («Arten und Vorlagen» … «hakt mega beim Scrollen», Robert 29.10.2026): das Blatt kommt als PNG aus dem Browser
    (DS.png, derselbe Satz wie im Editor), hier als WebP gespeichert; der Schlüssel enthält Inhalt und Stand von Satz, Vorlagen und dokumente.js."""
    import io
    from PIL import Image
    im = Image.open(io.BytesIO(roh)).convert('RGB')
    if im.width > 1400 or im.height > 2600:
        im.thumbnail((1400, 2600))
    os.makedirs(DOK_VB, exist_ok=True)
    im.save(os.path.join(DOK_VB, k + '.webp'), 'WEBP', quality=86, method=4)
    f = im.getpixel((min(4, im.width - 1), min(4, im.height - 1)))   # Papierfarbe am Rand für den Platzhalter
    with VB_SPERRE:
        ix = vb_index(); ix[k] = '#%02x%02x%02x' % f; t = VB_INDEX + '.neu'
        if k2:   # derselbe Inhalt ohne Stand: das neue Bild löst das alte ab, das alte wird gelöscht (sonst sammeln sich nach jedem Stand alte Bilder)
            z = ix.setdefault('_z', {}); alt = z.get(k2); z[k2] = k
            if alt and alt != k and alt not in z.values():
                ix.pop(alt, None)
                try:
                    os.remove(os.path.join(DOK_VB, alt + '.webp'))
                except OSError:
                    pass
        json.dump(ix, open(t, 'w', encoding='utf-8'), separators=(',', ':')); os.replace(t, VB_INDEX)
    return ix[k]


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HIER, **k)

    def _json(self, code, o):
        b = json.dumps(o, ensure_ascii=False).encode('utf-8')
        self.send_response(code); self.send_header('content-type', 'application/json; charset=utf-8'); self.send_header('content-length', str(len(b))); self.end_headers()
        self.wfile.write(b)

    def _plakat_mit_lebenszeichen(self, daten):
        """Antwort sofort beginnen (200), während des Malens Leerzeichen schicken (JSON erlaubt sie vorn), am Ende das Ergebnis oder {fehler}."""
        import threading
        erg = {}
        def arbeit():
            try:
                erg['out'] = P.antwort(daten, live=os.environ.get('PLAKAT_KI', '1') != '0')
            except Exception as e:
                erg['out'] = {'fehler': str(e)}
        t = threading.Thread(target=arbeit, daemon=True); t.start()
        self.close_connection = True
        try:
            self.send_response(200); self.send_header('content-type', 'application/json; charset=utf-8'); self.send_header('connection', 'close'); self.end_headers()
            self.wfile.flush()
            while t.is_alive():
                t.join(5)
                if t.is_alive():
                    self.wfile.write(b' '); self.wfile.flush()
            self.wfile.write(json.dumps(erg['out'], ensure_ascii=False).encode('utf-8')); self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            t.join()   # Browser weg: fertig malen lassen, die Bilder liegen danach in den Fotos des Hauses

    def translate_path(self, path):
        p = unquote(path.split('?')[0].split('#')[0])
        for weg, (ziel, art) in NUR_LESEN.items():
            if p == weg or (weg.endswith('/') and p.startswith(weg)):
                f = os.path.normpath(os.path.join(ziel, p[len(weg):])) if weg.endswith('/') else ziel
                if (f == ziel or f.startswith(ziel + os.sep)) and (art is None or re.search(art, f)):
                    return f
                return os.path.join(HIER, '__gesperrt__')
        if p.startswith(WEG):
            return super().translate_path(path.replace(WEG, '/', 1))
        return os.path.join(HIER, '__gesperrt__')

    def send_head(self):
        """Nie ausliefern: Punkt-Dateien, Prüfordner, Quellen (Python, Markdown), Daten der KI. Online gehen sie gar nicht erst mit."""
        teile = [x for x in unquote(self.path.split('?')[0].split('#')[0]).split('/') if x]
        if teile[:2] == ['_werkzeuge', 'imprimerie']:
            innen = teile[2:]
            if any(x.startswith('.') or x == '__pycache__' for x in innen) or (innen and innen[0] in ('_qa', 'api', '_archiv-ki-2810')) or (innen and innen[-1].endswith(('.py', '.pyc', '.md'))):
                self.send_error(404); return None
        return super().send_head()

    def do_GET(self):
        p = self.path.split('?')[0]
        if p in ('/', '/_werkzeuge/imprimerie'):
            self.send_response(302); self.send_header('location', WEG); self.end_headers(); return
        if p == WEG + 'api/entwurf':   # Lebenszeichen wie online (pruefung.html), ohne KI-Aufruf
            return self._json(200, {'ok': True, 'modell': E.MODELL, 'schluessel': KI, 'probe': not KI})
        if p == WEG + 'api/vorschau':   # welche Galerie-Vorschauen fertig liegen: {schlüssel: farbe}
            return self._json(200, vb_index())
        if p == WEG + 'api/plakat':   # alle schon entstandenen Vorschläge für «Abend beschreiben» (Robert 29.10.)
            try:
                return self._json(200, P.alle())
            except Exception as e:
                return self._json(502, {'fehler': str(e)})
        if self._gezippt():
            return
        return super().do_GET()

    GZ = {}   # (Pfad, Stand) → gzip-Bytes
    def _gezippt(self):
        """Text (JS, CSS, JSON, HTML, SVG) gzip-komprimiert und mit Last-Modified, damit der Browser beim nächsten Mal nur fragt (304) statt alles neu zu laden
        (29.10.2026: gedrosselt 12 s bis zum ersten Knopf; online komprimiert der Anbieter ohnehin). Gibt False zurück, wenn das normale Ausliefern übernimmt."""
        import gzip, email.utils
        if 'gzip' not in (self.headers.get('accept-encoding') or ''):
            return False
        pfad = self.translate_path(self.path)
        if os.path.isdir(pfad) and self.path.split('?')[0].endswith('/') and os.path.isfile(os.path.join(pfad, 'index.html')):   # auch die Startseite selbst (30.10.: kam mit 35 KB statt 10 KB)
            pfad = os.path.join(pfad, 'index.html')
        if not os.path.isfile(pfad) or os.path.splitext(pfad)[1].lower() not in ('.js', '.css', '.json', '.html', '.svg', '.txt', '.md'):
            return False
        st = os.stat(pfad); stand = (pfad, st.st_mtime_ns, st.st_size)
        lm = email.utils.formatdate(st.st_mtime, usegmt=True); ims = self.headers.get('if-modified-since')
        if ims:
            try:
                if int(st.st_mtime) <= email.utils.parsedate_to_datetime(ims).timestamp():
                    self.send_response(304); self.send_header('last-modified', lm); self.end_headers(); return True
            except Exception:
                pass
        z = H.GZ.get(stand)
        if z is None:
            z = gzip.compress(open(pfad, 'rb').read(), 6); H.GZ = {k: v for k, v in H.GZ.items() if k[0] != pfad}; H.GZ[stand] = z
        self.send_response(200); self.send_header('content-type', self.guess_type(pfad)); self.send_header('content-encoding', 'gzip'); self.send_header('vary', 'accept-encoding')
        self.send_header('content-length', str(len(z))); self.send_header('last-modified', lm); self.end_headers(); self.wfile.write(z)
        return True

    def end_headers(self):   # Vorschaubilder der Plakat-Liste tragen ?v=<Stand> und dürfen lange im Cache bleiben (29.10.), alles andere frisch
        self.send_header('cache-control', 'public, max-age=31536000, immutable' if '/haeuser/' in self.path and ('/vorschau/' in self.path or '/vorschau-dok/' in self.path) else 'no-store' if '/api/' in self.path else 'no-cache')
        super().end_headers()

    def do_POST(self):
        p = self.path.split('?')[0]
        marke = p == '/_werkzeuge/livre/api/pruefen'
        vb = p == WEG + 'api/vorschau'   # Vorschaubild einer Galerie-Karte (PNG, bis 4 MB), zählt nicht als Anfrage
        nein = E.wache({k.lower(): v for k, v in self.headers.items()}, self.client_address[0], groesse=25_000_000 if marke else 4_000_000 if vb else E.GROESSE, zaehlen=not (marke or vb))
        if nein:
            return self._json(nein[0], {'fehler': nein[1]})
        n = int(self.headers.get('content-length') or 0)
        roh = self.rfile.read(n)
        if vb:
            import base64
            try:
                d = json.loads(roh or b'{}'); k = str(d.get('k') or '')[:40]; k2 = str(d.get('k2') or '')[:40]; png = base64.b64decode(str(d.get('png') or '').split(',')[-1])
            except Exception:
                k, png = '', b''
            if not re.fullmatch(r'[0-9a-f]{16}', k) or (k2 and not re.fullmatch(r'[0-9a-f]{16}', k2)) or not png.startswith(b'\x89PNG'):
                return self._json(400, {'fehler': 'Vorschau: Schlüssel oder Bild ungültig'})
            try:
                return self._json(200, {'farbe': vb_ablegen(k, png, k2)})
            except Exception as e:
                return self._json(500, {'fehler': 'Vorschau: ' + str(e)[:80]})
        if marke:   # an den Server von Le Livre (eigener Chat), unverändert
            req = urllib.request.Request(LIVRE_SERVER + p, data=roh, method='POST', headers={'content-type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=240) as r:
                    code, b = r.status, r.read()
            except urllib.error.HTTPError as e:
                code, b = e.code, e.read()
            except Exception as e:
                code, b = 502, json.dumps({'fehler': 'LIVRE · Le Livre ist nicht erreichbar (' + str(e)[:80] + ')'}, ensure_ascii=False).encode('utf-8')
            self.send_response(code); self.send_header('content-type', 'application/json; charset=utf-8'); self.send_header('content-length', str(len(b))); self.end_headers()
            return self.wfile.write(b)
        if p == WEG + 'api/plakat' and '"nr"' in (roh or b'').decode('utf-8', 'replace'):   # ein Vorschlag malt minutenlang: sofort antworten, alle 5 s ein Leerzeichen
            return self._plakat_mit_lebenszeichen(json.loads(roh or b'{}'))                       # als Lebenszeichen, sonst gibt Safari nach 60 s auf (29.10.)
        if p == WEG + 'api/plakat':   # Abend beschreiben: neue Motive live, sobald der Schlüssel am Server liegt (Robert 28.10.); PLAKAT_KI=0 schaltet ab
            try:
                out, code = P.antwort(json.loads(roh or b'{}'), live=os.environ.get('PLAKAT_KI', '1') != '0'), 200
            except ValueError as e:
                out, code = {'fehler': str(e)}, 400
            except Exception as e:
                out, code = {'fehler': str(e)}, 502
            time.sleep(.6)
            return self._json(code, out)
        if p != WEG + 'api/entwurf':
            return self.send_error(404)
        try:
            daten = json.loads(roh or b'{}')
            out, code = (E.entwurf(daten) if KI else probe(daten)), 200
        except ValueError as e:
            out, code = {'fehler': str(e)}, 400
        except Exception as e:
            out, code = {'fehler': str(e)}, 502
        if not KI:
            time.sleep(.4)
        self._json(code, out)

    def log_message(self, f, *a):
        if '/api/' in str(a[:1]):
            sys.stderr.write(f % a + '\n')


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9087
    print(f'L’Imprimerie · Culinarium Hannover: http://127.0.0.1:{port}{WEG}  (KI: {"echt" if KI else "Probe, ohne Kosten"})')
    ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
