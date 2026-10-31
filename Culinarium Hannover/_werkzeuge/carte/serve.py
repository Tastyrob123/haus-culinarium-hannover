#!/usr/bin/env python3
"""La Carte · Culinarium Hannover — eigener Server (28.10.2026, Kopie aus der Tafel im Schäfli, dort aus Schlössli, Ruedihus,
Waldhotel Doldenhorn und La Carte des Carlton-Europe). python3 _werkzeuge/carte/serve.py [port]   (Standard 9083)

Liefert das Werkzeug (/_werkzeuge/carte/, darin auch Satz, Schriften und Fotos der Karte; die Werkzeug-Oberfläche kommt aus dem Haus unter
/assets/oberflaeche/), die Wege /_werkzeuge/carte/api/… (carte.py) und,
nur lesend, für die Ansicht «Website» die Seiten der Website mit assets/ und die PDFs unter unterlagen/pdf/. Sonst nichts aus dem Projekt.
Sicherheit (Master 7a): hört nur auf 127.0.0.1 und nimmt nur Anfragen an diese Adresse an (gegen DNS-Rebinding), schreibende Wege nur von
der eigenen Seite (Origin) und nur als JSON, höchstens 3 MB je Anfrage, Grenze für zu viele Anfragen je Absender, feste Kopfzeilen gegen
Einbetten, fremde Skripte und Schnüffeln. Fehler stehen mit Stichwort in der Antwort und in _daten/fehler.log."""
import gzip, json, mimetypes, os, re, sys, threading, time, traceback, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HIER = os.path.dirname(os.path.realpath(__file__))   # realpath: sonst liefert ein Projekt hinter einem Verweis (z. B. /var → /private/var) jede Datei als 404
WURZEL = os.path.dirname(os.path.dirname(HIER))   # Ordner, in dem _werkzeuge/ liegt
# Culinarium: die Website liegt in website/ neben _werkzeuge/
PROJ = os.path.join(WURZEL, 'website')
OBERFLAECHE = os.path.join(WURZEL, '_werkzeuge', 'oberflaeche')   # gemeinsamer Rahmen der Werkzeuge, bis Station 14 ihn nach website/assets/ legt
sys.path.insert(0, HIER)
import carte  # noqa: E402

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('CARTE_PORT', '9083'))
os.environ['CARTE_PORT'] = str(PORT)
GROSS = 3_000_000
# was aus dem Projekt gelesen werden darf (nur Dateien darunter, nie Python, nie Daten)
FREI = ('assets/', 'unterlagen/pdf/')
WEBSEITE = re.compile(r'^[a-z0-9-]+\.html$')   # Seiten der Website (nur gelesen) für die Ansicht «Website» in der Vorschau
WERK_GESPERRT = ('_daten', 'pruef/aus')
ENDUNG_OK = {'.html', '.css', '.js', '.json', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.woff2', '.woff', '.ttf', '.pdf', '.ico', '.mp4', '.webm', '.avif', '.gif'}
KOPF = {
    'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer', 'X-Frame-Options': 'SAMEORIGIN',
    'Content-Security-Policy': "default-src 'self'; img-src 'self' data: blob:; style-src 'self' 'unsafe-inline'; script-src 'self'; "
                               "font-src 'self'; connect-src 'self'; frame-src 'self' blob:; object-src 'self' blob:; frame-ancestors 'self'; base-uri 'self'; form-action 'self'",
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=()', 'Cross-Origin-Opener-Policy': 'same-origin',
}
# Grenzen je Absender und Minute: alle Anfragen, schreibende, Drucke
GRENZEN = {'alle': 900, 'schreiben': 60, 'druck': 8}
_ZAEHLER, _ZSCHLOSS = {}, threading.Lock()


def _api_weg(pfad):
    """Wege des Werkzeugs: /_werkzeuge/carte/api/<was> (so auch online, 16.10.2026) und weiter /api/<was> für ältere Aufrufe."""
    for v in ('/_werkzeuge/carte/api/', '/api/'):
        if pfad.startswith(v):
            return pfad[len(v):]
    return None


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


class Weg(BaseHTTPRequestHandler):
    server_version = 'LaCarte'
    sys_version = ''

    def log_message(self, f, *a):   # leise; Fehler stehen in _daten/fehler.log
        pass

    def _kopf(self, status, typ, laenge, mehr=None):
        self.send_response(status)
        self.send_header('Content-Type', typ)
        self.send_header('Content-Length', str(laenge))
        for k, v in KOPF.items():
            if k not in (mehr or {}):   # eigene Kopfzeile ersetzt die feste (z. B. CSP der Website-Seiten)
                self.send_header(k, v)
        for k, v in (mehr or {}).items():
            self.send_header(k, v)
        self.end_headers()

    def _json(self, status, d):
        b = json.dumps(d, ensure_ascii=False).encode('utf-8')
        mehr = {'Cache-Control': 'no-store'}
        if len(b) > 2000 and 'gzip' in (self.headers.get('Accept-Encoding') or ''):   # Schlössli 20.10.2026: Karten sind bis 140 kB, gepackt rund ein Siebtel (Slow 4G)
            b = gzip.compress(b, 6)
            mehr.update({'Content-Encoding': 'gzip', 'Vary': 'Accept-Encoding'})
        self._kopf(status, 'application/json; charset=utf-8', len(b), mehr)
        self.wfile.write(b)

    def _fehler(self, status, stichwort, text):
        self._json(status, {'fehler': text, 'stichwort': stichwort})

    def _host_ok(self):
        h = (self.headers.get('Host') or '').lower()
        return h in (f'127.0.0.1:{PORT}', f'localhost:{PORT}')

    def _wer(self):
        wer = urllib.parse.unquote(self.headers.get('X-Carte-Wer') or '').strip()[:60]
        rolle = (self.headers.get('X-Carte-Rolle') or '').strip()[:20]
        return wer, rolle

    def _datei(self, rel):
        rel = rel.lstrip('/')
        if rel.startswith('_werkzeuge/carte/'):
            basis = WURZEL
        elif rel.startswith('assets/oberflaeche/') and not os.path.isdir(os.path.join(PROJ, 'assets', 'oberflaeche')):
            basis, rel = OBERFLAECHE, rel[len('assets/oberflaeche/'):]
        else:
            basis = PROJ
        p = os.path.realpath(os.path.join(basis, rel))
        if not p.startswith(os.path.realpath(basis) + os.sep) or os.path.splitext(p)[1].lower() not in ENDUNG_OK:
            return self._fehler(404, 'DATEI', 'Nicht gefunden.')
        if basis == OBERFLAECHE:
            rel = 'assets/oberflaeche/' + rel
        werk = os.path.realpath(HIER) + os.sep
        if p.startswith(werk):
            if any(p[len(werk):].startswith(g) for g in WERK_GESPERRT):
                return self._fehler(404, 'DATEI', 'Nicht gefunden.')
        elif not any(rel.startswith(f) for f in FREI) and not WEBSEITE.match(rel):
            return self._fehler(404, 'DATEI', 'Nicht gefunden.')
        if not os.path.isfile(p):
            return self._fehler(404, 'DATEI', 'Nicht gefunden.')
        typ = mimetypes.guess_type(p)[0] or 'application/octet-stream'
        text = typ.startswith('text/') or typ in ('application/javascript', 'application/json', 'image/svg+xml')
        if text:
            typ += '; charset=utf-8'
        st = os.stat(p)
        etag = f'"{st.st_mtime_ns:x}-{st.st_size:x}"'
        if self.headers.get('If-None-Match') == etag:
            self.send_response(304)
            self.send_header('ETag', etag)
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        with open(p, 'rb') as f:
            b = f.read()
        mehr = {'Cache-Control': 'no-cache', 'ETag': etag, 'Vary': 'Accept-Encoding'}
        if WEBSEITE.match(rel):   # Seite der Website: ihre eigenen Skripte dürfen laufen, eingebettet nur bei La Carte
            mehr['Content-Security-Policy'] = "frame-ancestors 'self'"
        if (text or typ.startswith('font/ttf')) and len(b) > 800 and 'gzip' in (self.headers.get('Accept-Encoding') or ''):   # TTF der Karten-Schriften packen sich gut (Slow 4G)
            b = gzip.compress(b, 6)
            mehr['Content-Encoding'] = 'gzip'
        self._kopf(200, typ, len(b), mehr)
        self.wfile.write(b)

    def do_GET(self):
        if not self._host_ok():
            return self._fehler(421, 'HOST', 'Falsche Adresse.')
        u = urllib.parse.urlparse(self.path)
        # 16.10.2026: gezählt werden nur die Wege des Werkzeugs (wie online, wo Vercel die Dateien ausliefert); Schriften und Bilder einer Seite
        # zählten sonst mit, und nach etwa einem Dutzend Neuladen in einer Minute startete La Carte nicht mehr («Zu viele Anfragen»).
        if _api_weg(u.path) is not None and zu_viel(self.client_address[0], 'alle'):
            return self._fehler(429, 'GRENZE', 'Zu viele Anfragen in kurzer Zeit. Bitte eine Minute warten.')
        try:
            if u.path in ('/', '/_werkzeuge/carte', '/_werkzeuge/carte/'):
                if u.path != '/_werkzeuge/carte/':
                    self.send_response(302)
                    self.send_header('Location', '/_werkzeuge/carte/')
                    self.send_header('Content-Length', '0')
                    self.end_headers()
                    return
                return self._datei('_werkzeuge/carte/index.html')
            api = _api_weg(u.path)
            if api is not None:
                was = api
                q = urllib.parse.parse_qs(u.query)
                if was == 'pdf':
                    return self._pdf(q)
                if was == 'druckdaten':
                    return self._druckdaten(q)
                if was == 'webseite':
                    return self._webseite(q)
                if was == 'export':
                    b = json.dumps(carte.export(), ensure_ascii=False, indent=1).encode('utf-8')
                    name = time.strftime('la-carte-culinarium-hannover-%Y-%m-%d.json')
                    self._kopf(200, 'application/json; charset=utf-8', len(b), {'Cache-Control': 'no-store', 'Content-Disposition': f'attachment; filename="{name}"'})
                    return self.wfile.write(b)
                return self._json(200, carte.get(was, q, *self._wer()))
            return self._datei(urllib.parse.unquote(u.path))
        except carte.Fehler as e:
            return self._fehler(e.status, e.stichwort, e.text)
        except (BrokenPipeError, ConnectionResetError):   # Browser hat während der Antwort neu geladen: kein Fehler des Werkzeugs
            return None
        except Exception as e:  # noqa: BLE001
            carte.fehler_log(f'GET {self.path}: {e!r} {traceback.format_exc()[-600:]}')
            return self._fehler(500, 'SERVER', 'Im Server ist etwas schiefgegangen. Es steht im Fehlerprotokoll.')

    def _druckdaten(self, q):
        """Daten für die Druckseite: stand | entwurf | grundstand | verlauf:<datei>"""
        z, art = (q.get('z') or [''])[0], (q.get('q') or ['stand'])[0]
        carte._ziel(z)
        if art == 'entwurf':
            k = carte.karte(z)
            d = k['entwurf'] or k['stand']
        elif art == 'grundstand':
            d = carte.grundstand(z)
        elif art.startswith('verlauf:'):
            d = carte.version(z, art[8:])
        else:
            d = carte.karte(z)['stand']
        return self._json(200, d)

    def _webseite(self, q):
        """Ansicht «Website» (C07): die Seite der Website, wie sie heute gebaut ist (abende.html zeigt die Menükarte im Fenster des Abends; das Werkzeug
        öffnet dort den Abend der Karte). Die Website liest La Carte erst mit dem Einbau von karten.json in ihren Bau (web.py, offen); bis dahin zeigt
        die Ansicht den Stand der Website, der Entwurf steht in der Ansicht «Karte»."""
        z, seite = (q.get('z') or [''])[0], (q.get('seite') or [''])[0]
        carte._ziel(z)
        h = None
        if not h:
            self.send_response(302)
            self.send_header('Location', '/' + (seite if WEBSEITE.match(seite) else ''))
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        h = h.replace('<head>', '<head><base href="/">', 1).replace('<html', '<html data-carte-entwurf="1"', 1)
        b = h.encode('utf-8')
        self._kopf(200, 'text/html; charset=utf-8', len(b), {'Cache-Control': 'no-store', 'Content-Security-Policy': "frame-ancestors 'self'"})
        self.wfile.write(b)

    def _pdf(self, q):
        z, art = (q.get('z') or [''])[0], (q.get('q') or ['live'])[0]
        carte._ziel(z)
        if art not in ('live', 'probe'):
            return self._fehler(404, 'DATEI', 'Diese PDF gibt es nicht.')
        p = os.path.join(carte.K, art, z + '.pdf')
        if not os.path.isfile(p) and art == 'live':   # noch nichts veröffentlicht: die PDF, die heute auf der Website liegt 
            p = next((os.path.join(PROJ, r) for r in carte.website_pdfs(z) if os.path.isfile(os.path.join(PROJ, r))), os.path.join(PROJ, 'unterlagen', 'pdf', z + '.pdf'))
        if not os.path.isfile(p):
            return self._fehler(404, 'DATEI', 'Diese PDF gibt es noch nicht. Sie entsteht beim ersten Veröffentlichen.' if art == 'live' else 'Noch keine Probe gedruckt.')
        with open(p, 'rb') as f:
            b = f.read()
        name = urllib.parse.quote(f'{z}{"-probe" if art == "probe" else ""}.pdf')
        self._kopf(200, 'application/pdf', len(b), {'Cache-Control': 'no-store', 'Content-Disposition': f"inline; filename*=UTF-8''{name}"})
        self.wfile.write(b)

    def do_POST(self):
        if not self._host_ok():
            return self._fehler(421, 'HOST', 'Falsche Adresse.')
        o = self.headers.get('Origin')
        if o and o not in (f'http://127.0.0.1:{PORT}', f'http://localhost:{PORT}'):
            return self._fehler(403, 'HERKUNFT', 'Anfragen nur aus dem Werkzeug selbst.')
        if not (self.headers.get('Content-Type') or '').startswith('application/json'):
            return self._fehler(415, 'FORM', 'Nur JSON.')
        n = int(self.headers.get('Content-Length') or 0)
        if n > GROSS:
            return self._fehler(413, 'GROSS', 'Die Daten sind zu gross.')
        u = urllib.parse.urlparse(self.path)
        was = _api_weg(u.path) or ''
        ip = self.client_address[0]
        if zu_viel(ip, 'alle') or zu_viel(ip, 'schreiben') or (was in ('probe', 'veroeffentlichen') and zu_viel(ip, 'druck')):
            return self._fehler(429, 'GRENZE', 'Zu viele Änderungen in kurzer Zeit. Bitte eine Minute warten.')
        try:
            d = json.loads(self.rfile.read(n) or b'{}')
            if not isinstance(d, dict):
                raise ValueError
        except ValueError:
            return self._fehler(400, 'FORM', 'Die Anfrage ist kein gültiges JSON.')
        wer, rolle = self._wer()
        try:
            r = carte.post(was, d, wer, rolle)
            if was == 'veroeffentlichen':
                carte.sicherung()
            return self._json(200, r)
        except carte.Fehler as e:
            return self._fehler(e.status, e.stichwort, e.text)
        except Exception as e:  # noqa: BLE001
            carte.fehler_log(f'POST {self.path}: {e!r} {traceback.format_exc()[-600:]}')
            return self._fehler(500, 'SERVER', 'Im Server ist etwas schiefgegangen. Es steht im Fehlerprotokoll.')

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (BrokenPipeError, ConnectionResetError):   # der Browser hat neu geladen, während eine Antwort lief: kein Fehler des Werkzeugs
            pass


if __name__ == '__main__':
    try:
        carte.sicherung()
    except Exception as e:  # noqa: BLE001
        carte.fehler_log(f'Sicherung beim Start: {e!r}')
    srv = ThreadingHTTPServer(('127.0.0.1', PORT), Weg)
    srv.daemon_threads = True
    print(f'La Carte · Culinarium Hannover: http://127.0.0.1:{PORT}/_werkzeuge/carte/', flush=True)
    srv.serve_forever()
