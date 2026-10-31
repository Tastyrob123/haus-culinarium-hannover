#!/usr/bin/env python3
"""La Réception (Team hinter dem Gäste-Chat) · Culinarium Hannover. Am Rechner aus dem Projektordner: python3 _werkzeuge/reception/server.py [port]   (Standard 9084)
Kopie des Gastgebers der Taverne zum Schäfli (28.10.2026, dort nur gelesen), dort aus dem Schlössli, Ruedihus, Doldenhorn und Carlton-Europe, Funktion wie La Réception des Grand Beau-Rivage.
Culinarium sind Food-Pairing-Abende an der langen Tafel in der Bar Walk on the Wild Side (Linden): Warteliste für den nächsten Abend, Plätze, eigene Feier, Nachrichten, Allergien.

Ein Server für drei Dinge:
  /                               die Website aus website/ des Projekts, nur lesen (Warteliste auf Der Abend, Vormerken im Fuss)
  /assets/oberflaeche/            das gemeinsame Kleid der Werkzeuge des Culinarium (_werkzeuge/oberflaeche/, nur lesen; einziger Schreiber culinarium-maison)
  /api/gast                       der Chat («Chat ausprobieren»): gast/gast.py mit dem Wissen des Culinarium, dazu reception.py
  /_werkzeuge/reception/          La Réception, das Werkzeug des Teams; /_werkzeuge/reception/api/<was> sein Server-Teil,
                                  darunter «formular»: die Formulare der Website (baustein/anfrage.js) legen dort ihre Anfragen ab

KI nur auf ausdrücklichen Schalter (Regel 54, Robert 16.10.2026: Claude-Schlüssel gesperrt): ohne RECEPTION_KI=1 antworten Chat, Brief, Übersetzen
und Wissen-Einlesen mit Probe-Antworten (probe_ki.py), sichtbar beschriftet. Mit RECEPTION_KI=1 nimmt der Server den Schlüssel nur aus der Umgebung
(ANTHROPIC_API_KEY), nie aus einer Datei; der Vault wird nie gelesen.

Antwortet nur auf dem eigenen Rechner (127.0.0.1) und nur Aufrufen von der eigenen Seite. Nichts an der Website wird geschrieben;
geschrieben wird nur unter _werkzeuge/reception/daten/ (oder RECEPTION_DATEN). Ein Passwort gibt es auf Roberts Wort (15.10.2026) vorerst nicht;
bei der Auslieferung an das Haus kommt eine Anmeldung davor (Master, Abschnitt 7a)."""
import datetime, importlib.util, json, mimetypes, os, posixpath, re, sys, threading, time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote, quote

HIER = os.path.dirname(os.path.realpath(__file__))
PROJ = os.path.dirname(os.path.dirname(HIER))   # Projektordner des Culinarium
WEB = os.path.join(PROJ, 'website')            # die Website, nur gelesen
WERK = os.path.join(PROJ, '_werkzeuge')        # die Werkzeuge des Hauses (hier nur gelesen, ausser reception/daten)
sys.path.insert(0, HIER)
import reception  # noqa: E402

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9084
VERBOTEN = ('_sicherung', '_studio', '_dienste', '_werkbank', '_recherche', '_qa', '_varianten-online', '_werkzeuge/reception/daten', '_werkzeuge/reception/gast',
            '_werkzeuge/reception/_bau', '_werkzeuge/reception/pruefung', '_werkzeuge/reception/online', '_daten', '_varianten', '_zuschnitt', '_alt', '.env', '__pycache__', 'potenzialanalyse')   # nie ausliefern
_GAST, _SCHLOSS, _SCHLOSS_KI = None, threading.Lock(), threading.Lock()
# Sicherheit (Master Werkzeug-Bau 5.2, Muster _werkzeuge/carte/serve.py): Grenzen je Absender und Minute. Schreiben höher als bei La Carte (60),
# weil der Brief beim Gestalten jede Änderung einzeln sichert; PDF wie die Drucke von La Carte.
GRENZEN = {'alle': 900, 'schreiben': 120, 'pdf': 8, 'formular': int(os.environ.get('RECEPTION_FORMULAR_GRENZE') or 6)}   # formular: Gäste der Website, öffentlich, deshalb eng (6 je Minute und Absender; Prüfläufe höher)
GROESSE = {'wissen_einlesen': 40_000_000}   # Fotos und Dokumente fürs Wissen reisen als Daten mit; alles andere höchstens 3 MB
GROESSE_SONST = 3_000_000
_ZAEHLER, _ZSCHLOSS = {}, threading.Lock()


def zu_viel(wer, art):
    jetzt = time.time()
    with _ZSCHLOSS:
        liste = [t for t in _ZAEHLER.get((wer, art), []) if jetzt - t < 60]
        if len(liste) >= GRENZEN[art]:
            _ZAEHLER[(wer, art)] = liste
            return True
        liste.append(jetzt)
        _ZAEHLER[(wer, art)] = liste
        return False


def zustand():
    """Für pruefung.html: läuft alles? Liest nur, ruft keine KI und holt keinen Schlüssel."""
    import glob, shutil, tempfile
    d = reception.DATEN
    p = []
    def punkt(gruppe, was, stand, text, stichwort=''):
        p.append({'gruppe': gruppe, 'was': was, 'stand': stand, 'text': text, 'stichwort': stichwort})
    punkt('Server', 'Server-Teil läuft', 'gut', f'Port {PORT}, nur 127.0.0.1')
    echt = os.environ.get('RECEPTION_KI') == '1'
    ki = ('Schlüssel aus der Umgebung' if os.environ.get('ANTHROPIC_API_KEY') else 'RECEPTION_KI=1, aber kein Schlüssel in der Umgebung') if echt else 'Probe ohne KI (Standard, Regel 54)'
    punkt('Server', 'Assistent', 'gut' if echt and os.environ.get('ANTHROPIC_API_KEY') else 'rot' if echt else 'gelb', ki, 'KI')
    try:
        os.makedirs(d, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=d, prefix='.probe-', delete=True) as f:
            f.write(b'ok')
        punkt('Daten', 'Ablage beschreibbar', 'gut', os.path.relpath(d, PROJ) if d.startswith(PROJ) else 'eigener Ordner (Prüflauf)')
    except OSError as e:
        punkt('Daten', 'Ablage beschreibbar', 'rot', str(e)[:120], 'DATEI')
    kaputt, gut, zahl = [], 0, {}
    for art in ('anfragen', 'fragen'):
        fs = glob.glob(os.path.join(d, art, '*', '*.json'))
        zahl[art] = len(fs)
        for f in fs:
            try:
                json.load(open(f, encoding='utf-8'))
            except (OSError, ValueError):
                kaputt.append(os.path.relpath(f, d))
    for f in glob.glob(os.path.join(d, '**', '*.json'), recursive=True):
        if os.path.exists(f + '.gut'):
            gut += 1
    punkt('Daten', 'Anfragen und Fragen lesbar', 'rot' if kaputt else 'gut',
          (f'{len(kaputt)} beschädigt: ' + ', '.join(kaputt[:3])) if kaputt else f"{zahl['anfragen']} Anfragen, {zahl['fragen']} Fragen, alle lesbar", 'DATEI' if kaputt else '')
    punkt('Daten', 'Sicherung der letzten guten Fassung', 'gut', f'{gut} Dateien mit Sicherung (.gut), entsteht beim zweiten Speichern')
    for n in ('gast_wissen.txt', 'gast_umgebung.txt'):
        q = os.path.join(HIER, 'gast', n)
        punkt('Wissen', n, 'gut' if os.path.getsize(q) > 1000 else 'rot', f'{os.path.getsize(q) // 1024} kB') if os.path.exists(q) else punkt('Wissen', n, 'rot', 'fehlt', 'WISSEN')
    try:
        sb = json.load(open(os.path.join(HIER, 'steckbrief.json'), encoding='utf-8'))
        z = sum(len(g.get('zeilen') or []) for b in sb.get('bereiche') or [] for g in b.get('gruppen') or [])
        punkt('Wissen', 'Steckbrief «Das weiss der Chat»', 'gut' if z else 'gelb', f'{z} belegte Zeilen')
    except (OSError, ValueError) as e:
        punkt('Wissen', 'Steckbrief «Das weiss der Chat»', 'rot', str(e)[:100], 'WISSEN')
    vl = [n for n in reception.VORLAGEN_DATEIEN if os.path.exists(os.path.join(HIER, 'vorlagen', n))]
    punkt('Brief', 'Ton der Briefe', 'gut' if vl else 'gelb', (f'{len(vl)} Vorlagen aus dem Wortlaut der Website (vorlagen/)' if vl else 'Das Haus hat keine eigenen Mail-Vorlagen; der Brief hält sich an den Ton des Markenbuchs'), '' if vl else 'ENTWURF')
    web = sum(1 for f in glob.glob(os.path.join(d, 'anfragen', '*', '*.json')) if (lambda s: '"web": true' in s and '"beispiel": true' not in s)(open(f, encoding='utf-8', errors='replace').read()))
    try:
        ein = 'anfrage.js' in open(os.path.join(WEB, 'abend.html'), encoding='utf-8').read()
    except OSError:
        ein = False
    punkt('Website', 'Formulare der Website', 'gut' if ein else 'gelb', (f'eingebaut, {web} echte Anfragen über die Website (ohne Beispiele)' if ein else f'Warteliste noch nicht angeschlossen (Baustein baustein/anfrage.js, Einbau durch den Website-Chat); {web} echte Anfragen über die Website (ohne Beispiele)'), '' if ein else 'FORMULAR')
    o = reception.ONLINE_STAND
    punkt('Website', 'Einträge von der Online-Website', 'gelb' if o['fehler'] or not o['zeit'] else 'gut',
          (f"zuletzt abgeholt {o['zeit'][11:16]} Uhr, {o['neu']} neu" if o['zeit'] and not o['fehler'] else f"Abholen hakt: {o['fehler']}" if o['fehler'] else 'noch nicht abgeholt') + f" (alle {ABHOLEN} s von {reception.ONLINE_API})", 'FORMULAR' if o['fehler'] else '')
    node = shutil.which('node') or next((x for x in ('/opt/homebrew/bin/node', '/usr/local/bin/node') if os.path.exists(x)), None)
    pw = os.path.exists(os.path.expanduser('~/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'))
    punkt('Brief', 'PDF-Satz (node mit Chromium)', 'gut' if node and pw else 'rot', ('node ' + node + (', Playwright da' if pw else ', Playwright fehlt')) if node else 'node fehlt', '' if node and pw else 'PDF')
    punkt('Sicherheit', 'Grenzen je Absender und Minute', 'gut', f"{GRENZEN['alle']} Aufrufe, {GRENZEN['schreiben']} Änderungen, {GRENZEN['pdf']} PDF, {GRENZEN['formular']} Formulare; höchstens 3 MB je Anfrage, 40 MB beim Einlesen, 12 kB je Formular")
    punkt('Sicherheit', 'Anmeldung', 'gelb', 'noch keine (Roberts Wort 15.10.2026), kommt vor der Auslieferung', 'ANMELDUNG')
    try:
        fehler = [json.loads(z) for z in open(os.path.join(d, 'fehler.jsonl'), encoding='utf-8').read().splitlines()[-30:] if z.strip()]
    except (OSError, ValueError):
        fehler = []
    return {'zeit': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'punkte': p, 'fehler': fehler[::-1]}


def export_zip(daten):
    """Alle Daten von La Réception als eine Datei (Master Website-Bau 9d Punkt 21, Datenexport): Anfragen mit Briefen, Fragen, Nachträge,
    Wissen des Teams. Ohne Sicherungen (.gut) und ohne halbe Dateien (.neu)."""
    import io, zipfile
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w', zipfile.ZIP_DEFLATED) as z:
        for w, _, fs in os.walk(daten):
            for f in sorted(fs):
                if f.endswith(('.gut', '.neu')) or f.startswith('.') or f == 'fehler.jsonl':
                    continue
                p = os.path.join(w, f)
                z.write(p, os.path.join('la-reception', os.path.relpath(p, daten)))
        z.writestr('la-reception/LIESMICH.txt', reception.NAME + ' · Culinarium Hannover: alle Daten, Stand ' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M') +
                   '.\nanfragen/: je Anfrage eine Datei mit Brief · fragen/: Fragen an den Chat (12 Monate) · nachgetragen.json: Antworten des Teams · gedaechtnis/: Wissen des Teams.\n')
    return b.getvalue()


def fehler_merken(text):
    """Skriptfehler aus dem Browser (Fehlermelder in index.html) in daten/fehler.jsonl, höchstens 500 Zeilen; liest pruefung.html."""
    p = os.path.join(reception.DATEN, 'fehler.jsonl')
    with _ZSCHLOSS:
        try:
            alt = open(p, encoding='utf-8').read().splitlines()[-499:]
        except OSError:
            alt = []
        alt.append(json.dumps({'zeit': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'text': str(text)[:600]}, ensure_ascii=False))
        with open(p + '.neu', 'w', encoding='utf-8') as f:
            f.write('\n'.join(alt) + '\n')
        os.replace(p + '.neu', p)


def schluessel():
    """Nur aus der Umgebung (Regel 54: die Schlüssel im Vault sind gesperrt, kein Lesen von Dateien). Ohne Schlüssel: klare Meldung statt stillem Versagen."""
    if not os.environ.get('ANTHROPIC_API_KEY'):
        raise ValueError('KI · Kein Schlüssel gesetzt. Das Werkzeug läuft mit Probe-Antworten, bis ein Schlüssel in der Umgebung steht.')


def gast():
    """Lädt gast/gast.py einmal (dieselbe Datei wie online api/gast.py, Wissen daneben) und hängt La Réception an."""
    global _GAST
    with _SCHLOSS:
        if _GAST is None:
            p = os.path.join(HIER, 'gast', 'gast.py')
            if not os.path.exists(p):
                raise ValueError('CHAT · Der Chat fehlt am Rechner. Einmal python3 _werkzeuge/reception/_bau/gast_bau.py laufen lassen.')
            s = importlib.util.spec_from_file_location('gast_culinarium', p)
            g = importlib.util.module_from_spec(s)
            s.loader.exec_module(g)
            if os.environ.get('RECEPTION_KI') != '1':   # Standard: Probe-Antworten, kein Schlüssel, keine Kosten (probe_ki.py); echte KI nur mit RECEPTION_KI=1
                import probe_ki
                g._api = probe_ki.api
                print('Probe-Betrieb: keine KI, Antworten aus probe_ki.py', flush=True)
            else:   # RECEPTION_KI=1: der Schlüssel muss in der Umgebung stehen; Öffnen, Eingang, Wissen und Brief gestalten kosten nichts
                roh_api = g._api

                def api_mit_schluessel(koerper):
                    with _SCHLOSS_KI:
                        schluessel()
                    return roh_api(koerper)
                g._api = api_mit_schluessel
            reception.einbinden(g)
            H._ip = g.handler._ip
            _GAST = g
        return _GAST


class H(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *a):
        pass

    def fremd(self, art='alle'):
        """Nur der eigene Rechner, nur die eigene Adresse, nur die eigene Seite (Schutz gegen Einbetten, fremde Formulare und umgeleitete Namen),
        dazu die Grenze je Absender und Minute. Antwortet selbst und gibt True zurück, wenn die Anfrage nicht weiter darf."""
        if self.client_address[0] not in ('127.0.0.1', '::1'):
            self.sende(403, {'fehler': 'HERKUNFT · Nur am eigenen Rechner.'}); return True
        if not re.fullmatch(rf'(localhost|127\.0\.0\.1|\[::1\]):{PORT}', self.headers.get('Host') or ''):
            self.sende(421, {'fehler': 'HOST · Falsche Adresse.'}); return True
        h = self.headers.get('Origin') or ''
        if h and not re.fullmatch(rf'http://(localhost|127\.0\.0\.1|\[::1\]):{PORT}', h):
            self.sende(403, {'fehler': 'HERKUNFT · Nicht erlaubt.'}); return True
        wer = self.client_address[0]
        if art and (zu_viel(wer, 'alle') or (art != 'alle' and zu_viel(wer, art))):   # Grenze nur für Aufrufe der Schnittstelle, nie für Seiten, Bilder, Schriften (Abnahme 17.10.2026: schnelles Neuladen lief sonst in 429, die Seite blieb weiss)
            self.sende(429, {'fehler': 'GRENZE · Zu viele Anfragen in kurzer Zeit. Bitte eine Minute warten.'}, kopf={'Retry-After': '60'}); return True
        return False

    def sende(self, code, daten, art='application/json; charset=utf-8', kopf=None):
        roh = daten if isinstance(daten, bytes) else json.dumps(daten, ensure_ascii=False).encode('utf-8')
        # Leistung (29.10.2026): Text gepackt wie online (Vercel packt auch), Schriften und Dateien mit ?v= (Fassung aus dem Inhalt) darf der Browser behalten
        gepackt = False
        if len(roh) > 1024 and 'gzip' in (self.headers.get('Accept-Encoding') or '') and re.match(r'(text/|application/(json|javascript|xml)|image/svg)', art):
            import gzip
            roh, gepackt = gzip.compress(roh, 6), True
        pfad = urlparse(self.path).path
        import hashlib
        v = (re.search(r'[?&]v=([0-9a-f]{6,40})', self.path) or [None, None])[1]
        behalten = code == 200 and self.command in ('GET', 'HEAD') and '/api/' not in pfad and (pfad.endswith('.woff2') or bool(v and hashlib.sha1(daten if isinstance(daten, bytes) else b'').hexdigest().startswith(v)))   # nur behalten, wenn die Nummer zum Inhalt passt
        self.send_response(code)
        self.send_header('Content-Type', art)
        self.send_header('Content-Length', str(len(roh)))
        if gepackt:
            self.send_header('Content-Encoding', 'gzip'); self.send_header('Vary', 'Accept-Encoding')
        self.send_header('Cache-Control', 'public, max-age=31536000, immutable' if behalten else 'no-store')
        # Einbetten nur auf der eigenen Seite und in der Karte der Kette (127.0.0.1:8978, Robert bestätigt dort); X-Frame-Options kennt keine Ausnahme, deshalb frame-ancestors
        self.send_header('Content-Security-Policy', "frame-ancestors 'self' http://127.0.0.1:8978 http://localhost:8978")
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'same-origin')
        self.send_header('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
        for k, v in (kopf or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(roh)

    # wird von gast.py benutzt (handler._sende / _ip)
    def _sende(self, code, daten):
        return self.sende(code, daten)

    def _ip(self):
        return self.client_address[0]

    def do_HEAD(self):
        return self.do_GET()

    def do_GET(self):
        u = urlparse(self.path)
        if self.fremd('alle' if '/api/' in u.path or u.path.startswith('/api') else None):
            return
        teile = [t for t in posixpath.normpath(unquote(u.path)).split('/') if t and t not in ('.', '..')]
        rel = '/'.join(teile)
        if '/api/' in '/' + rel + '/' and (self.headers.get('Sec-Fetch-Site') or 'same-origin') not in ('same-origin', 'none'):   # E15: Daten nur für die eigene Seite
            return self.sende(403, {'fehler': 'HERKUNFT · Nur von der eigenen Seite.'})
        try:
            if rel == '_werkzeuge/reception/api/zustand':   # Prüfseite: ohne den Chat zu laden
                return self.sende(200, zustand())
            if rel == '_werkzeuge/reception/api/export':    # alle Daten als eine Datei (Prüfseite)
                name = re.sub(r'[^A-Za-z0-9-]+', '-', reception.NAME.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')).strip('-') + '-Culinarium-' + datetime.date.today().isoformat() + '.zip'   # Name aus kleid/culinarium.js
                return self.sende(200, export_zip(reception.DATEN), 'application/zip', {'Content-Disposition': f'attachment; filename="{name}"'})
            if rel == '_werkzeuge/reception/api/anfragen':   # Eingang öffnen: zuerst abholen, was online liegt
                reception.online_abholen()
            if rel.startswith('_werkzeuge/reception/api/'):
                gast()   # lädt den Chat einmal und hängt La Réception und das Gedächtnis an (wie serve.py des Grand Beau-Rivage)
                return self.sende(200, reception.get(rel.rsplit('/', 1)[1], parse_qs(u.query)))
            if rel == 'api/gast':
                g = gast()
                return self.sende(200, {'ok': True, 'modell': g.MODELL, 'wissen_zeichen': len(g.WISSEN), 'tal_zeichen': len(g.TAL)})
            if any(rel == v or rel.startswith(v + '/') for v in VERBOTEN) or any(t in ('_daten', 'daten', '_bau', '_sicherung', '_quelle') or t.startswith(('daten.', '_daten.')) for t in teile[:-1]) or '.vor-' in rel or '.stand-vor-' in rel or rel.endswith(('.py', '.md', '.jsonl', '.gut', '.neu', '.sh', '.log')):
                return self.sende(404, b'Nicht gefunden', 'text/plain; charset=utf-8')
            if rel.startswith('assets/oberflaeche/') and os.path.isfile(os.path.join(WERK, 'oberflaeche', *teile[2:])):   # das gemeinsame Kleid der Werkzeuge (bis Station 14 es nach website/assets/ legt)
                p = os.path.join(WERK, 'oberflaeche', *teile[2:])
            elif teile and teile[0] == '_werkzeuge':   # die Werkzeuge des Hauses: nur ihre Dateien, nie ihre Daten
                p = os.path.join(PROJ, *teile)
            else:
                p = os.path.join(WEB, *teile)
            if os.path.isdir(p):
                if not u.path.endswith('/'):
                    return self.sende(301, b'', 'text/plain', {'Location': u.path + '/'})
                p = os.path.join(p, 'index.html')
            if not rel:
                p = os.path.join(WEB, 'index.html')
            if not os.path.isfile(p):
                return self.sende(404, b'Nicht gefunden', 'text/plain; charset=utf-8')
            with open(p, 'rb') as f:
                daten = f.read()
            art = mimetypes.guess_type(p)[0] or 'application/octet-stream'
            if art.startswith('text/') or art in ('application/javascript', 'image/svg+xml'):
                art += '; charset=utf-8'
            return self.sende(200, daten, art)
        except ValueError as e:
            return self.sende(422, {'fehler': str(e)})
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:  # noqa: BLE001
            return self.sende(500, {'fehler': 'SERVER · ' + type(e).__name__ + ': ' + str(e)[:200]})

    def do_POST(self):
        u = urlparse(self.path)
        rel = u.path.strip('/')
        if rel == 'api/anfrage':   # die Formulare der Website (assets/anfrage.js) schicken online an /api/anfrage; hier landen sie gleich im Eingang
            rel = '_werkzeuge/reception/api/formular'
        if rel == 'api/frage':     # der Gäste-Chat der Website (online _online/api/frage.py): hier dieselbe Zuordnung, die Frage gleich unter «Das wurde gefragt»
            if self.fremd('formular'):
                self.close_connection = True
                return
            try:
                n = int(self.headers.get('Content-Length') or 0)
                d = json.loads(self.rfile.read(n).decode('utf-8')) if 0 < n <= 20000 else {}
                q = re.sub(r'\s+', ' ', str(d.get('frage') or '')).strip()[:600]
                if not q:
                    return self.sende(422, {'fehler': 'Bitte stell eine Frage.'})
                a = chat_zuordnung().antworte(q, 'en' if d.get('sprache') == 'en' else 'de')
                if d.get('probe') is True or 'probe=1' in (self.headers.get('Referer') or ''):   # Tor 3 (30.10.2026): Proben nicht unter die Gästefragen
                    return self.sende(200, {'text': a['text'], 'belegt': a['belegt'], 'aktion': a.get('aktion', '')})
                reception.lege_frage({'frage': q, 'antwort': a['text'], 'belegt': a['belegt'], 'thema': ','.join(a.get('fids') or []), 'sprache': 'de'})
                return self.sende(200, {'text': a['text'], 'belegt': a['belegt'], 'aktion': a.get('aktion', '')})
            except (ValueError, UnicodeDecodeError):
                return self.sende(422, {'fehler': 'EINGABE · Die Anfrage ist kein gültiges JSON.'})
        was = rel.rsplit('/', 1)[1] if '/' in rel else rel
        if self.fremd('pdf' if was == 'brief_pdf' else 'formular' if was == 'formular' else 'schreiben' if rel.startswith('_werkzeuge/reception/api/') else 'alle'):
            self.close_connection = True
            return
        try:
            n = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            n = -1
        try:
            if rel == 'api/gast':
                if n < 0 or n > GROESSE_SONST:
                    self.close_connection = True
                    return self.sende(413, {'fehler': 'GROESSE · Die Anfrage ist zu gross.'})
                return gast().handler.do_POST(self)
            if rel == 'api/zahlen':        # Zählung der Website: hier nicht gebraucht
                self.rfile.read(max(0, min(n, 4000)))
                return self.sende(204, b'', 'text/plain')
            if rel.startswith('_werkzeuge/reception/api/'):
                if not (self.headers.get('Origin') or '').startswith('http://'):   # nur Aufrufe von der eigenen Seite (fremde stehen schon oben)
                    self.close_connection = True
                    return self.sende(403, {'fehler': 'HERKUNFT · Nur von der eigenen Seite.'})
                if n < 0 or n > (12000 if was == 'formular' else GROESSE.get(was, GROESSE_SONST)):
                    self.close_connection = True   # nicht lesen: die Verbindung wird geschlossen
                    return self.sende(413, {'fehler': 'GROESSE · Die Anfrage ist zu gross.'})
                if 'json' not in (self.headers.get('Content-Type') or 'application/json'):
                    self.close_connection = True
                    return self.sende(415, {'fehler': 'EINGABE · Nur JSON.'})
                try:
                    d = json.loads(self.rfile.read(n).decode('utf-8') or '{}')
                except (ValueError, UnicodeDecodeError):
                    raise ValueError('EINGABE · Die Anfrage ist kein gültiges JSON.')
                if not isinstance(d, dict):
                    raise ValueError('EINGABE · Kein Objekt.')
                if was == 'fehler':          # Skriptfehler aus dem Browser (Fehlermelder in index.html)
                    fehler_merken(d.get('text', ''))
                    return self.sende(200, {'ok': True})
                if was == 'fehler_leeren':   # Reparatur der Prüfseite (mit Doppelklick bestätigt)
                    try:
                        os.remove(os.path.join(reception.DATEN, 'fehler.jsonl'))
                    except OSError:
                        pass
                    return self.sende(200, {'ok': True})
                if was == 'formular':        # Formular der Website (baustein/anfrage.js): ohne Chat, ohne KI; Probe nur aus einer Seite mit ?probe=1
                    d['probe'] = 'probe=1' in (self.headers.get('Referer') or '')
                    return self.sende(200, reception.post('formular', d))
                gast()
                if was == 'brief_pdf':       # der Brief als fertige A4-PDF (Chromium), zum Laden
                    roh, name = reception.brief_pdf(d.get('id'), PORT)
                    return self.sende(200, roh, 'application/pdf', {'Content-Disposition': "attachment; filename=\"Brief.pdf\"; filename*=UTF-8''" + quote(name)})
                return self.sende(200, reception.post(was, d))
            self.close_connection = True
            return self.sende(404, {'fehler': 'Unbekannt.'})
        except ValueError as e:
            return self.sende(422, {'fehler': str(e)})
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:  # noqa: BLE001
            return self.sende(500, {'fehler': 'SERVER · ' + type(e).__name__ + ': ' + str(e)[:200]})


_CHAT = None


def chat_zuordnung():
    """Die Zuordnung des Gäste-Chats der Website (_online/api/frage.py) mit dem Wissen aus steckbrief.json, wie online (online.py stell baut es genauso)."""
    global _CHAT
    if _CHAT is None:
        spec = importlib.util.spec_from_file_location('website_frage', os.path.join(PROJ, '_online', 'api', 'frage.py'))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        sb = json.load(open(os.path.join(HIER, 'steckbrief.json'), encoding='utf-8'))
        m.WISSEN = [{'fid': z['fid'], 'bereich': b['bereich'], 'gruppe': g['gruppe'], 'was': z['was'], 'angabe': z['angabe']}
                    for b in sb['bereiche'] for g in b['gruppen'] for z in g['zeilen']]
        _CHAT = m
    return _CHAT


ABHOLEN = int(os.environ.get('RECEPTION_ABHOLEN') or 60)   # Sekunden zwischen zwei Abrufen des Online-Eingangs (reception.online_abholen)


def abholen_lauf():
    while True:
        reception.online_abholen()
        time.sleep(ABHOLEN)


if __name__ == '__main__':
    os.makedirs(reception.DATEN, exist_ok=True)
    threading.Thread(target=abholen_lauf, daemon=True).start()   # Anfragen der Website (Vercel, /api/anfrage) in den Eingang
    print(f'La Réception · Culinarium Hannover: http://127.0.0.1:{PORT}/_werkzeuge/reception/  ·  Website: http://127.0.0.1:{PORT}/' + ('' if os.environ.get('RECEPTION_KI') == '1' else '  ·  Probe ohne KI'), flush=True)
    ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
