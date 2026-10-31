#!/usr/bin/env python3
"""Das Besucherbuch (Le Registre) · Culinarium Hannover, lokaler Server (Port 9086): liefert aus dem Projekt von Culinarium nur, was das Werkzeug braucht (lesend),
und /api/registre.   python3 server.py [port]      danach http://127.0.0.1:9086/_werkzeuge/registre/
Kopie des server.py des Besucherbuchs der Taverne zum Schäfli (dort nach Schlössli, Gasterntal, Doldenhorn und Carlton-Europe gebaut, nur kopiert).
Die Website liegt in website/ neben _werkzeuge/. /_werkzeuge/… kommt aus dem Projekt, alles andere (/assets/, die Seiten) aus website/.
Die Oberfläche der Häuser (/assets/oberflaeche/) liegt unter _werkzeuge/oberflaeche/ (Kleid culinarium, gemeinsam für alle Werkzeuge des Hauses,
einziger Schreiber ist der Chat der Zentrale «culinarium-maison»). Sie gewinnt auch, wenn in website/assets/oberflaeche/ eine Kopie liegt; website/ ist nur Rückfall.

GET  /api/registre?tage=30       Vorführ-Betrieb: jeder bekommt Beispielwerte (als Beispiel gekennzeichnet).
     &k=<Schlüssel>              echte Werte (Schlüssel nur in ~/Desktop/Website-Projekte/_Schluessel/culinarium-hannover.txt; seine Prüfsumme steht in anschluss.py).
POST /api/registre               eine Zeile von messung.js (lokal zum Ausprobieren; schreibt in _daten/).
Nur Anfragen vom eigenen Rechner werden beantwortet (Master 7a: lokales Werkzeug).
Sicherheit (Prüfung 16.10.2026, Werkzeug-Master 5.2): Anfragen einer fremden Seite (Origin ≠ diese Adresse) 403, mehr als GRENZE Anfragen je Minute 429,
Zeile über 300 Zeichen 413. Beispielwerte kommen aus registre.ablage_heute (dieselbe Rechnung wie das Werkzeug ohne Server-Teil).
POST /api/registre?fehler=1      Skriptfehler des Werkzeugs (Fehlermelder in index.html), nur ins Protokoll des Servers, nichts gespeichert."""
import collections, hashlib, http.server, json, os, re, socketserver, sys, threading, time, urllib.parse

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(HIER))          # Projektordner von Culinarium: _werkzeuge/ liegt dort
PROJ = os.path.join(WURZEL, 'website')                   # die Website: Schriften, Fotos, Seiten
STAMM_OF = os.path.join(WURZEL, '_werkzeuge', 'oberflaeche')   # Oberfläche der Häuser mit dem Kleid von Culinarium, bis Station 14 sie nach website/assets/ legt
sys.path.insert(0, HIER)
import anschluss as AN  # noqa: E402   Dienst /api/registre (dieselben Antworten wie der Hausserver serve.py, Patch in LIEFERUNG.md); Schalter VORFUEHRUNG und Schlüssel dort
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9086
GRENZE = {'GET': 600, 'POST': 120}   # je Minute und Absender
_ZAEHL, _ZSCHLOSS = collections.defaultdict(collections.deque), threading.Lock()
ERLAUBT = ('/_werkzeuge/registre/', '/_werkzeuge/maison/', '/assets/', '/maison/')   # mehr braucht das Werkzeug nicht; dazu die Seiten der Website (.html in der Wurzel) für «Website ansehen»


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=WURZEL, **k)

    def log_message(self, *a):
        pass

    def translate_path(self, path):
        p = super().translate_path(path)   # unter WURZEL (Projekt): gilt für /_werkzeuge/…
        rel = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
        if rel.startswith('/_werkzeuge/'):
            return p
        w = os.path.normpath(os.path.join(PROJ, rel.lstrip('/')))   # alles andere aus website/
        if not (w == PROJ or w.startswith(PROJ + os.sep)):
            return os.path.join(PROJ, '__nicht_da__')
        if rel.startswith('/assets/oberflaeche/'):   # das gemeinsame Kleid unter _werkzeuge/oberflaeche/ gilt (Änderungen nur über den Chat der Zentrale); website/ nur als Rückfall
            q = os.path.normpath(os.path.join(STAMM_OF, rel[len('/assets/oberflaeche/'):]))
            if q.startswith(STAMM_OF + os.sep) and os.path.isfile(q):
                return q
        return w

    def end_headers(self):
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'same-origin')
        if self.path.endswith(('.js', '.css', '.html', '.json')) or self.path.endswith('/') or '?' in self.path:
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def _fremd(self):
        if self.client_address[0] not in ('127.0.0.1', '::1', '::ffff:127.0.0.1'):
            return True
        o = self.headers.get('Origin')   # fremde Seite im Browser des Hauses (eine Seite im Netz schickt an localhost): abweisen
        return bool(o) and o not in (f'http://localhost:{PORT}', f'http://127.0.0.1:{PORT}')

    def _zu_viel(self, art):
        jetzt, k = time.time(), (self.client_address[0], art)
        with _ZSCHLOSS:
            q = _ZAEHL[k]
            while q and q[0] < jetzt - 60:
                q.popleft()
            q.append(jetzt)
            return len(q) > GRENZE[art]

    def _json(self, code, d):
        b = json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self._fremd():
            return self.send_error(403)
        u = urllib.parse.urlsplit(self.path)
        if u.path.startswith('/api/') and self._zu_viel('GET'):   # nur der Dienst zählt, nicht Schriften und Bilder
            return self._json(429, {'fehler': 'GRENZE · Zu viele Anfragen, bitte eine Minute warten.'})
        if u.path == '/api/registre':
            return self._json(*AN.antwort_get(u.query))
        if u.path in ('/', ''):
            self.send_response(302); self.send_header('Location', '/_werkzeuge/registre/'); self.end_headers(); return
        p = self._weg(u.path)   # entschlüsselt prüfen: genau der Weg, den der Server danach öffnet (Prüfung 17.10.2026: %2e%2e und %79 umgingen die Sperren)
        if p is None or not (p.startswith(ERLAUBT) or re.fullmatch(r'/[a-z0-9-]+\.html', p)) or '/_daten/' in p or '/_pruefung' in p or '/_sicherung' in p \
                or p.endswith(('.py', '.pyc', '.md', '.log', '.txt', '.csv', '.jsonl', '.sh', '.patch')) or '/abnahme' in p:
            return self.send_error(404)
        return super().do_GET()

    @staticmethod
    def _weg(roh):
        """Weg so, wie translate_path ihn liest (einmal entschlüsselt). Kein Teil mit Punkt am Anfang («..», «.env»), kein Rückstrich, kein Nullzeichen."""
        p = urllib.parse.unquote(roh)
        if '\\' in p or '\x00' in p or any(t.startswith('.') for t in p.split('/') if t):
            return None
        return p

    def do_HEAD(self):
        return self.do_GET() if not self._fremd() else self.send_error(403)

    def do_POST(self):
        if self._fremd():
            return self.send_error(403)
        u = urllib.parse.urlsplit(self.path)
        if u.path != '/api/registre':
            return self.send_error(404)
        if self._zu_viel('POST'):
            return self._json(429, {'fehler': 'GRENZE · Zu viele Anfragen, bitte eine Minute warten.'})
        try:
            n = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            n = -1
        if n < 0 or n > 300:
            self.close_connection = True
            return self._json(413, {'fehler': 'GROESSE · Eine Zeile hat höchstens 300 Zeichen.'})
        roh = self.rfile.read(n) if n else b''
        code, d = AN.antwort_post(u.query, roh, self.client_address[0], self.headers.get('User-Agent') or '')
        if d is not None:
            return self._json(code, d)
        self.send_response(code); self.send_header('Cache-Control', 'no-store'); self.end_headers()


class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 128   # viele Seiten melden gleichzeitig (Prüfung Q04: 140 Meldungen auf einmal); Vorgabe 5 wies unter Last Verbindungen ab


if __name__ == '__main__':
    print(f'Das Besucherbuch · Culinarium Hannover: http://127.0.0.1:{PORT}/_werkzeuge/registre/', flush=True)
    S(('127.0.0.1', PORT), H).serve_forever()
