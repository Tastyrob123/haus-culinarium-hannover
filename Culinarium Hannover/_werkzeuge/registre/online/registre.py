"""Das Besucherbuch (Le Registre) · Culinarium Hannover online (Vercel-Funktion /api/registre, 28.10.2026). Kopie der Taverne zum Schäfli, dort nach Schlössli und Berghotel Gasterntal
(_werkzeuge/registre/online/registre.py, dort nach Doldenhorn und Carlton-Europe, nur kopiert), Vorbild Grand Beau-Rivage api/registre.py (dort nur gelesen).
GET   ?tage=30            Vorführ-Betrieb: Beispielwerte (registre.ablage_heute, dieselbe Rechnung wie das Werkzeug ohne Server-Teil und die Stube)
      &k=<Schlüssel>      echte Werte (Prüfsumme unten; Schlüssel nur in ~/Desktop/Website-Projekte/_Schluessel/culinarium-hannover.txt)
POST                      eine Zeile von assets/js/messung.js (Website, Quelle vorschlag/messung.js); ?fehler=1 Skriptfehler des Werkzeugs, nur ins Protokoll
Speicher: nur ein EIGENER privater Blob-Speicher mit REGISTRE_READ_WRITE_TOKEN (Master 4.6: damit Le Registre die anderen Werkzeuge nicht scharf
schaltet und nie in deren Speicher schreibt). Fehlt er: Ordner unter /tmp (nichts hält), echte Werte gibt es dann keine.
Sicherheit: POST nur von der eigenen Adresse (Origin) sonst 403, Zeile über 300 Zeichen 413, je Instanz höchstens 120 POST und 600 GET je
Minute und Absender (429), Tagesgrenze MAX_TAG in registre.py. Keine Fehlerspur in Antworten. Kein Name, keine Adresse gespeichert.
Geht das Haus in Betrieb: VORFUEHRUNG = False hier, in anschluss.py (lokaler Dienst) und in _werkzeuge/registre/registre.js (Entscheid Robert)."""
from http.server import BaseHTTPRequestHandler
import collections, concurrent.futures, hashlib, json, os, sys, threading, time, urllib.parse

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
if os.environ.get('REGISTRE_READ_WRITE_TOKEN'):
    os.environ['BLOB_READ_WRITE_TOKEN'] = os.environ['REGISTRE_READ_WRITE_TOKEN']
    os.environ.pop('BLOB_LOKAL', None)
else:   # nie in den gemeinsamen Speicher der anderen Werkzeuge
    os.environ['BLOB_READ_WRITE_TOKEN'] = ''
    os.environ['BLOB_LOKAL'] = '/tmp/culinarium-hannover-registre-demo'
os.environ['REGISTRE_GEHEIM'] = hashlib.sha256(('registre|' + os.environ.get('REGISTRE_READ_WRITE_TOKEN', 'ohne')).encode()).hexdigest()
import _speicher as SP  # noqa: E402

VORFUEHRUNG = True
SCHLUESSEL = 'f04c5cb0b86365e3510f65ef03e89c959d16338e9d8717a0c6f9fcb57638b8b7'   # SHA-256 des eigenen Schlüssels von Culinarium (wie anschluss.py, G09)
GRENZE = {'GET': 600, 'POST': 120}

import importlib.util  # noqa: E402
# Die Logik heisst wie diese Datei: deshalb nach Pfad geladen (Fall F10 des Rivage), nie über den Namen.
_ORT = next(p for p in (os.path.join(HIER, '_lib', 'registre', 'registre.py'), os.path.join(os.path.dirname(HIER), 'registre.py')) if os.path.exists(p))
_SPEC = importlib.util.spec_from_file_location('registre_logik', _ORT)
RG = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(RG)


def _lies(tag):
    roh, etag = SP.get(f'registre/{tag}.json', mit_etag=True)
    try:
        d = json.loads(roh) if roh else {}
    except ValueError:
        d = {}
    return (d if isinstance(d, dict) else {}), etag


def _schreib(tag, d, marke):
    try:
        SP.put(f'registre/{tag}.json', json.dumps(d, ensure_ascii=False, separators=(',', ':')), 'application/json', 'private', if_match=marke)
    except SP.Konflikt:
        raise RG.Konflikt()
    except SP.Fehler as e:   # gleichzeitiges Schreiben: der Speicher antwortet 400 «conflicting operation» statt 412
        if 'conflicting operation' in str(e):
            raise RG.Konflikt()
        raise


def _tage_lesen(tage):
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        return dict(zip(tage, (x[0] for x in pool.map(_lies, tage))))


RG._lies, RG._schreib, RG._tage_lesen = _lies, _schreib, _tage_lesen
_ZAEHL, _ZS = collections.defaultdict(collections.deque), threading.Lock()


def _zu_viel(wer, art):
    jetzt = time.time()
    with _ZS:
        q = _ZAEHL[(wer, art)]
        while q and q[0] < jetzt - 60:
            q.popleft()
        q.append(jetzt)
        return len(q) > GRENZE[art]


class handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _wer(self):
        h = self.headers
        return (h.get('x-real-ip') or (h.get('x-forwarded-for') or '').split(',')[0]).strip()

    def do_GET(self):
        if _zu_viel(self._wer(), 'GET'):
            return SP.sende(self, 429, {'fehler': 'GRENZE · Zu viele Anfragen, bitte eine Minute warten.'})
        _, q = SP.weg_von(self.path)
        echt = (not VORFUEHRUNG or hashlib.sha256((q.get('k') or [''])[0].encode()).hexdigest() == SCHLUESSEL) and bool(os.environ.get('REGISTRE_READ_WRITE_TOKEN'))
        tage = (q.get('tage') or ['30'])[0]
        if (q.get('export') or [''])[0]:   # Datenexport: nur echte Werte, nur mit Schlüssel
            if not echt:
                return SP.sende(self, 403, {'fehler': 'ZUGANG · Die Besuche gibt es nur mit Schlüssel.'})
            try:
                return SP.sende(self, 200, RG.ausfuhr(tage))
            except Exception as e:  # noqa: BLE001
                return SP.sende(self, 500, {'fehler': 'SERVER · Ausfuhr fehlgeschlagen (' + type(e).__name__ + ').'})
        try:
            d = RG.ablage_heute(tage) if (q.get('beispiel') or [''])[0] or not echt else RG.stand(tage)
        except Exception as e:  # noqa: BLE001
            return SP.sende(self, 500, {'fehler': 'SERVER · Auswertung fehlgeschlagen (' + type(e).__name__ + ').'})
        return SP.sende(self, 200, d)

    def do_POST(self):
        h = self.headers
        o, host = h.get('Origin') or '', h.get('x-forwarded-host') or h.get('Host') or ''
        if o and urllib.parse.urlsplit(o).netloc != host:
            return SP.sende(self, 403, {'fehler': 'HERKUNFT · Nur von der eigenen Website.'})
        if _zu_viel(self._wer(), 'POST'):
            return SP.sende(self, 429, {'fehler': 'GRENZE · Zu viele Anfragen, bitte eine Minute warten.'})
        try:
            n = int(h.get('Content-Length') or 0)
        except ValueError:
            n = -1
        if n < 0 or n > 300:
            return SP.sende(self, 413, {'fehler': 'GROESSE · Eine Zeile hat höchstens 300 Zeichen.'})
        roh = self.rfile.read(n) if n else b''
        _, q = SP.weg_von(self.path)
        if (q.get('fehler') or [''])[0]:
            print('Das Besucherbuch, Fehler im Browser:', roh.decode('utf-8', 'replace')[:300].replace('\n', ' '))
        else:
            try:
                RG.melde(roh, self._wer(), h.get('User-Agent') or '', h.get('x-vercel-ip-country') or '',
                         urllib.parse.unquote(h.get('x-vercel-ip-city') or ''), h.get('x-vercel-ip-country-region') or '')
            except Exception:  # noqa: BLE001  die Website wartet auf keine Antwort
                pass
        self.send_response(204); self.send_header('Cache-Control', 'no-store'); self.end_headers()
