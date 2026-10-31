#!/usr/bin/env python3
"""Le Livre (Marke) · Culinarium Hannover, lokaler Server (Port 9085; Nachbau des Schäfli, dort nur gelesen): liefert die Website (website/) unter / und Le Livre
(_werkzeuge/livre/) nur lesend aus, das gemeinsame Kleid der Werkzeuge (_werkzeuge/oberflaeche/) unter /assets/oberflaeche/, und beantwortet /api/…:
   python3 _werkzeuge/livre/server.py [port]           danach http://127.0.0.1:9085/_werkzeuge/livre/
   LIVRE_KI=1 python3 _werkzeuge/livre/server.py       Markenprüfung mit Claude (nur auf Roberts Wort, Regel 54); ohne den Schalter Probe-Antwort

GET  /_werkzeuge/livre/api/stand                                   Zahlen für La Maison (Fotos, Dateien), Fotos ohne Original
GET  /_werkzeuge/livre/api/bild?k=<foto>&f=instagram|story|web|druck[&x=0..1][&y=0..1]   das Foto in fertiger Grösse als Download
POST /_werkzeuge/livre/api/pruefen {name, typ, daten, sprache}    Markenprüfung; nichts wird gespeichert
POST /_werkzeuge/livre/api/fehler  {zeit, art, text, wo, seite, browser}   Skriptfehler aus dem Browser (R03), nach _werkzeuge/livre/_qa/fehler.jsonl
GET  /marke/livre.json                                             dieselbe livre.json (Stand-Weg von La Maison, Master 4.1); /marke/api/… = /_werkzeuge/livre/api/…

Sicherheit (Master Werkzeug-Bau L12, Muster Carlton-Livre): nur Anfragen vom eigenen Rechner (403), nur mit eigener Adresse im Host (421), Schreibwege nur
von der eigenen Seite (Origin/Sec-Fetch-Site, 403), Grenzen je Minute nur auf die Wege des Werkzeugs (429), Grösse (413), nur JSON (415), gesperrte Pfade
(Quellen, Sicherungen, Daten, alles mit _ ausser den Werkzeug-Ordnern, Prüfordner), Sicherheitskopfzeilen. Eigener Prozess, nur die eigene PID beenden."""
import collections, http.server, json, os, socketserver, sys, threading, time, urllib.parse

HIER = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HIER))            # Culinarium Hannover
WURZEL = os.path.join(PROJ, 'website')                   # die Website, nur gelesen
# Wege ausserhalb der Website: Le Livre selbst, die Nachbarn (nur ihre Oberflächen) und das gemeinsame Kleid
# (nur die Oberflächen der Nachbarn, ihre Server-Teile laufen auf ihren eigenen Servern)
UMLEITEN = {'/_werkzeuge/livre/': HIER, '/assets/oberflaeche/': os.path.join(PROJ, '_werkzeuge', 'oberflaeche'),
            **{f'/_werkzeuge/{w}/': os.path.join(PROJ, '_werkzeuge', w) for w in ('maison', 'imprimerie', 'carte', 'reception', 'registre', 'bureau')}}
sys.path.insert(0, HIER)
import livre as LV  # noqa: E402

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9085
API = ('/_werkzeuge/livre/api/', '/marke/api/')
OFFEN_MIT_STRICH = ('/_werkzeuge/livre/', '/_werkzeuge/imprimerie/', '/_werkzeuge/maison/', '/_werkzeuge/carte/', '/_werkzeuge/reception/', '/_werkzeuge/registre/', '/_werkzeuge/bureau/')   # die einzigen Ordner mit _ am Anfang, die ausgeliefert werden
GESPERRT_ENDUNG = ('.py', '.pyc', '.md', '.log', '.jsonl', '.sh', '.env', '.gut', '.bak', '.diff')
GRENZE = {'lesen': (900, 60), 'bild': (120, 60), 'pruefen': (20, 60), 'fehler': (60, 60)}   # Anfragen je Minute, nur Wege des Werkzeugs (Falle 9: nie auf Schriften und Bilder)
GROESSE = {'pruefen': 45 * 1024 * 1024, 'fehler': 8 * 1024}
ZAEHLER = collections.defaultdict(collections.deque)
SCHLOSS = threading.Lock()


def zu_viel(art):
    n, s = GRENZE[art]
    jetzt = time.time()
    with SCHLOSS:
        q = ZAEHLER[art]
        while q and q[0] < jetzt - s:
            q.popleft()
        if len(q) >= n:
            return int(q[0] + s - jetzt) + 1
        q.append(jetzt)
    return 0


def gesperrt(pfad):
    p = urllib.parse.unquote(pfad)
    if '..' in p or '\x00' in p or '/.' in p or '\\' in p:
        return True
    if p.endswith(GESPERRT_ENDUNG) or any(x in p for x in ('/_daten/', '/_sicherung/', '/_quelle/', '/__pycache__/', '/_qa/', '/_dienste/', '/_studio/', '/_recherche/')):
        return True
    teile = p.split('/')[1:]
    if p.startswith(OFFEN_MIT_STRICH):
        rest = teile[2:]                                   # innerhalb eines Werkzeug-Ordners: nichts mit _, keine Prüfordner, keine Online-Quellen
        return any(t.startswith('_') for t in rest) or (teile[1] == 'livre' and rest[:1] in (['pruefung'], ['online']))
    return any(t.startswith('_') for t in teile[:-1]) or (teile and teile[-1].startswith('_'))


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=WURZEL, **k)

    def log_message(self, *a):
        pass

    def translate_path(self, path):
        p = urllib.parse.unquote(path.split('?', 1)[0].split('#', 1)[0])
        for vor, ziel in UMLEITEN.items():
            if p.startswith(vor):
                rest = [t for t in p[len(vor):].split('/') if t and t not in ('.', '..')]
                return os.path.join(ziel, *rest)
        return super().translate_path(path)

    def end_headers(self):
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'same-origin')
        self.send_header('Cross-Origin-Resource-Policy', 'same-origin')
        if self.path.split('?')[0].endswith(('.js', '.css', '.html', '.json', '/')):
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def _senden(self, code, daten, typ='application/json; charset=utf-8', kopf=None):
        if not isinstance(daten, (bytes, bytearray)):
            daten = json.dumps(daten, ensure_ascii=False, separators=(',', ':')).encode()
        self.send_response(code)
        self.send_header('Content-Type', typ)
        self.send_header('Content-Length', str(len(daten)))
        for k, v in (kopf or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(daten)

    def _wache(self, schreiben=False):
        """None, wenn die Anfrage durch darf, sonst (Code, Meldung)."""
        if self.client_address[0] not in ('127.0.0.1', '::1', '::ffff:127.0.0.1'):
            return 403, 'HERKUNFT · Le Livre antwortet nur auf diesem Rechner.'
        host = (self.headers.get('Host') or '').lower()
        if host not in (f'localhost:{PORT}', f'127.0.0.1:{PORT}', f'[::1]:{PORT}'):
            return 421, 'HOST · Unbekannte Adresse.'
        if schreiben:
            o = self.headers.get('Origin')
            if o and o.lower() not in (f'http://localhost:{PORT}', f'http://127.0.0.1:{PORT}', f'http://[::1]:{PORT}'):
                return 403, 'HERKUNFT · Anfragen von fremden Seiten werden abgewiesen.'
            if (self.headers.get('Sec-Fetch-Site') or 'same-origin') not in ('same-origin', 'none'):
                return 403, 'HERKUNFT · Anfragen von fremden Seiten werden abgewiesen.'
        return None

    def _api_weg(self, pfad):
        for a in API:
            if pfad.startswith(a):
                return pfad[len(a):].strip('/')
        return None

    def do_HEAD(self):
        return self.do_GET()

    def do_GET(self):
        w = self._wache()
        if w:
            return self._senden(w[0], {'fehler': w[1]})
        u = urllib.parse.urlparse(self.path)
        was = self._api_weg(u.path)
        if was is not None:
            warte = zu_viel('bild' if was == 'bild' else 'lesen')
            if warte:
                return self._senden(429, {'fehler': 'GRENZE · Zu viele Anfragen. Bitte kurz warten.'}, kopf={'Retry-After': str(warte)})
            try:
                r = LV.get(was, urllib.parse.parse_qs(u.query))
                if isinstance(r, tuple):
                    d, typ, name = r
                    return self._senden(200, d, typ, {'Content-Disposition': f'attachment; filename="{name}"', 'Cache-Control': 'no-store'})
                return self._senden(200, r)
            except ValueError as e:
                return self._senden(400, {'fehler': str(e)})
            except Exception as e:  # noqa: BLE001
                return self._senden(500, {'fehler': 'SERVER · ' + type(e).__name__})
        if u.path == '/marke/livre.json':            # Stand-Weg von La Maison (Master 4.1), dieselbe Datei
            self.path = '/_werkzeuge/livre/livre.json' + (('?' + u.query) if u.query else '')
            u = urllib.parse.urlparse(self.path)
        if gesperrt(u.path):
            return self.send_error(404)
        return super().do_GET() if self.command == 'GET' else super().do_HEAD()

    def do_POST(self):
        w = self._wache(schreiben=True)
        if w:
            return self._senden(w[0], {'fehler': w[1]})
        u = urllib.parse.urlparse(self.path)
        was = self._api_weg(u.path)
        if was not in ('pruefen', 'fehler'):
            return self._senden(404, {'fehler': 'WEG · Unbekannte Anfrage.'})
        warte = zu_viel(was)
        if warte:
            return self._senden(429, {'fehler': 'GRENZE · Zu viele Anfragen. Bitte kurz warten.'}, kopf={'Retry-After': str(warte)})
        if 'json' not in (self.headers.get('Content-Type') or ''):
            return self._senden(415, {'fehler': 'EINGABE · Erwartet wird JSON.'})
        try:
            n = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            n = -1
        if n < 0 or n > GROESSE[was]:
            return self._senden(413, {'fehler': 'GROESSE · Die Datei ist zu gross (höchstens 30 MB).' if was == 'pruefen' else 'GROESSE · Zu gross.'})
        try:
            d = json.loads(self.rfile.read(n) or b'{}')
        except ValueError:
            return self._senden(400, {'fehler': 'EINGABE · Die Anfrage ist kein lesbares JSON.'})
        try:
            return self._senden(200, LV.post(was, d))
        except ValueError as e:
            return self._senden(400, {'fehler': str(e)})
        except Exception as e:  # noqa: BLE001
            return self._senden(500, {'fehler': 'SERVER · ' + type(e).__name__})


class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    print(f'Le Livre auf http://127.0.0.1:{PORT}/_werkzeuge/livre/' + ('' if LV._ki_an() else '  (Markenprüfung ohne Claude: Probe-Antwort)'), flush=True)
    S(('127.0.0.1', PORT), H).serve_forever()
