"""Ein Server für alle Werkzeuge. Start: python3 unterbau/serve.py [port]   (Standard 8970)

Liefert die Dateien des Ordners aus und beantwortet:

  GET    /api/haus/<haus>                         haeuser/<haus>/haus.json
  GET    /api/stand/<haus>/<werkzeug>             live, entwurf, Kennungen, offen
  PUT    /api/entwurf/<haus>/<werkzeug>           {daten, erwartet, wer}
  DELETE /api/entwurf/<haus>/<werkzeug>           Entwurf verwerfen
  POST   /api/veroeffentlichen/<haus>/<werkzeug>  {wer, notiz}
  GET    /api/verlauf/<haus>/<werkzeug>
  GET    /api/fassung/<haus>/<werkzeug>/<fassung>
  POST   /api/zurueckholen/<haus>/<werkzeug>      {fassung, wer}
  GET    /api/protokoll/<haus>/<werkzeug>
  *      /api/x/<werkzeug>/<rest>                 eigene Wege eines Werkzeugs:
                                                  werkzeuge/<werkzeug>/api.py, Funktion
                                                  bearbeite(methode, rest, daten, speicher) → (status, antwort)

Fehler kommen als {"fehler": "...", "stichwort": "..."} mit passendem Status (409 = Konflikt).
"""
import importlib.util
import json
import mimetypes
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import speicher  # noqa: E402

WURZEL = Path(__file__).resolve().parent.parent
GESPERRT = ('daten', '.git', 'unterbau', '__pycache__')
mimetypes.add_type('font/woff2', '.woff2')


class Fehler(Exception):
    def __init__(self, status, text, stichwort):
        super().__init__(text)
        self.status, self.text, self.stichwort = status, text, stichwort


def _werkzeug_api(name):
    pfad = WURZEL / 'werkzeuge' / name / 'api.py'
    if not speicher._NAME.match(name) or not pfad.exists():
        raise Fehler(404, 'Dieses Werkzeug hat keine eigenen Wege', 'weg-unbekannt')
    spec = importlib.util.spec_from_file_location(f'werkzeug_{name.replace("-", "_")}', pfad)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)  # bei jedem Aufruf frisch, damit Änderungen ohne Neustart greifen
    return modul


class Antwort(BaseHTTPRequestHandler):
    server_version = 'Werkzeuge/1'

    def log_message(self, fmt, *args):
        sys.stderr.write('%s %s\n' % (self.log_date_time_string(), fmt % args))

    def _json(self, status, daten):
        roh = json.dumps(daten, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(roh)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(roh)

    def _koerper(self):
        n = int(self.headers.get('Content-Length') or 0)
        if n > 20 * 1024 * 1024:
            raise Fehler(413, 'Zu gross', 'zu-gross')
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode('utf-8'))
        except ValueError:
            raise Fehler(400, 'Die Anfrage ist kein gültiges JSON', 'anfrage-unlesbar')

    def _api(self, methode, teile):
        if not teile:
            raise Fehler(404, 'Weg unbekannt', 'weg-unbekannt')
        was, rest = teile[0], teile[1:]
        if was == 'x' and rest:
            daten = self._koerper() if methode in ('POST', 'PUT', 'DELETE') else {}
            return _werkzeug_api(rest[0]).bearbeite(methode, rest[1:], daten, speicher)
        if was == 'haus' and len(rest) == 1 and methode == 'GET':
            if not speicher._NAME.match(rest[0]):
                raise Fehler(404, 'Haus unbekannt', 'haus-unbekannt')
            p = WURZEL / 'haeuser' / rest[0] / 'haus.json'
            if not p.exists():
                raise Fehler(404, 'Haus unbekannt', 'haus-unbekannt')
            return 200, json.loads(p.read_text(encoding='utf-8'))
        if was == 'fassung' and len(rest) == 3 and methode == 'GET':
            return 200, speicher.fassung_lesen(*rest)
        if len(rest) != 2:
            raise Fehler(404, 'Weg unbekannt', 'weg-unbekannt')
        haus, werkzeug = rest
        if was == 'stand' and methode == 'GET':
            return 200, speicher.lesen(haus, werkzeug)
        if was == 'verlauf' and methode == 'GET':
            return 200, speicher.verlauf(haus, werkzeug)
        if was == 'protokoll' and methode == 'GET':
            return 200, speicher.protokoll(haus, werkzeug)
        if was == 'entwurf' and methode == 'PUT':
            k = self._koerper()
            if 'daten' not in k:
                raise Fehler(400, 'Es fehlt «daten»', 'anfrage-unvollstaendig')
            return 200, speicher.entwurf_schreiben(haus, werkzeug, k['daten'], k.get('erwartet'), k.get('wer', ''))
        if was == 'entwurf' and methode == 'DELETE':
            return 200, speicher.entwurf_verwerfen(haus, werkzeug, self._koerper().get('wer', ''))
        if was == 'veroeffentlichen' and methode == 'POST':
            k = self._koerper()
            return 200, speicher.veroeffentlichen(haus, werkzeug, k.get('wer', ''), k.get('notiz', ''))
        if was == 'zurueckholen' and methode == 'POST':
            k = self._koerper()
            return 200, speicher.zurueckholen(haus, werkzeug, k.get('fassung', ''), k.get('wer', ''))
        raise Fehler(404, 'Weg unbekannt', 'weg-unbekannt')

    def _bedien(self, methode):
        pfad = unquote(urlparse(self.path).path)
        teile = [t for t in pfad.split('/') if t]
        if teile[:1] == ['api']:
            try:
                status, daten = self._api(methode, teile[1:])
                return self._json(status, daten)
            except Fehler as f:
                return self._json(f.status, {'fehler': f.text, 'stichwort': f.stichwort})
            except speicher.Konflikt as f:
                return self._json(409, {'fehler': str(f), 'stichwort': 'konflikt'})
            except speicher.Unbekannt as f:
                return self._json(404, {'fehler': str(f), 'stichwort': 'unbekannt'})
            except speicher.Beschaedigt as f:
                return self._json(500, {'fehler': str(f), 'stichwort': 'beschaedigt'})
            except Exception as f:  # nichts verschlucken: Meldung nach aussen und ins Protokoll
                sys.stderr.write(f'FEHLER {methode} {pfad}: {f!r}\n')
                return self._json(500, {'fehler': 'Unerwarteter Fehler: ' + str(f), 'stichwort': 'unerwartet'})
        if methode != 'GET':
            return self._json(405, {'fehler': 'Nicht erlaubt', 'stichwort': 'nicht-erlaubt'})
        if any(t in GESPERRT or t.startswith('.') for t in teile):
            return self._json(404, {'fehler': 'Nicht gefunden', 'stichwort': 'nicht-gefunden'})
        ziel = (WURZEL / '/'.join(teile)).resolve()
        if WURZEL not in ziel.parents and ziel != WURZEL:
            return self._json(404, {'fehler': 'Nicht gefunden', 'stichwort': 'nicht-gefunden'})
        if ziel.is_dir():
            if not pfad.endswith('/'):
                self.send_response(301)
                self.send_header('Location', pfad + '/')
                self.end_headers()
                return
            ziel = ziel / 'index.html'
        if not ziel.is_file():
            return self._json(404, {'fehler': 'Nicht gefunden', 'stichwort': 'nicht-gefunden'})
        roh = ziel.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mimetypes.guess_type(ziel.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(len(roh)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(roh)

    def do_GET(self): self._bedien('GET')
    def do_POST(self): self._bedien('POST')
    def do_PUT(self): self._bedien('PUT')
    def do_DELETE(self): self._bedien('DELETE')


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8970
    print(f'Werkzeuge auf http://127.0.0.1:{port}/  (Muster: /stamm/muster.html)')
    ThreadingHTTPServer(('127.0.0.1', port), Antwort).serve_forever()
