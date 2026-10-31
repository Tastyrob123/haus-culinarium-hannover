"""Le Livre online · Culinarium Hannover (Vercel-Funktion api/livre.py; Kopie von online/livre_online.py des Schäfli, dort nur gelesen). Vorbereitet, nicht hochgeladen.
Wege (vercel.json → /api/livre?__weg=…): /werkzeuge/livre/api/stand|bild|pruefen|fehler, /_werkzeuge/livre/api/… und /marke/api/… (L’Imprimerie).
Logik unverändert in api/_lib/livre/livre.py (= _werkzeuge/livre/livre.py), Daten aus api/_lib/livre/livre.json (= _werkzeuge/livre/livre.json). Unterschiede zum Rechner:
- Fotos zum Herunterladen kommen aus der Website selbst (/assets/bild/… und /werkzeuge/livre/fotos/…), nicht aus den Originalen (die liegen nicht online);
  «Druck» liefert deshalb die Website-Grösse, Dateiname und Fenster sagen es («websitegroesse», api/stand → nur_website).
- PDFs werden mit PyMuPDF gelesen (requirements.txt), nicht mit pdftoppm.
- Gespeichert wird nichts, der Speicher (Blob) wird nicht gebraucht.
Sicherheit: Schreibwege nur von der eigenen Seite (Origin/Sec-Fetch-Site, 403), Grenzen je Absender und Instanz (429), Grösse (413, Vercel nimmt höchstens
4,5 MB an, die Oberfläche verkleinert Bilder vorher), Fehlerberichte nur ins Protokoll der Funktion.
KI (Regel 54): Claude nur, wenn am Vercel-Projekt ANTHROPIC_API_KEY gesetzt ist (Roberts Wort) und LIVRE_KI nicht 0 ist; sonst Probe-Antwort. Im Dateisystem
wird online nie ein Schlüssel gesucht."""
from http.server import BaseHTTPRequestHandler
import collections, importlib.util, io, json, os, sys, threading, time, urllib.error, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import _speicher as SP  # noqa: E402

LIB = os.path.join(HIER, '_lib', 'livre')
os.environ.setdefault('LIVRE_JSON', os.path.join(LIB, 'livre.json'))
os.environ.setdefault('LIVRE_FEHLER', '/tmp/culinarium-livre-fehler.jsonl')
os.environ['LIVRE_KI'] = '1' if os.environ.get('ANTHROPIC_API_KEY') and os.environ.get('LIVRE_KI') != '0' else '0'
_spec = importlib.util.spec_from_file_location('livre_kern', os.path.join(LIB, 'livre.py'))   # nach Pfad laden: nie mit dieser Datei verwechseln (F10)
LV = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(LV)
from PIL import Image, ImageOps  # noqa: E402

HOST = {'basis': ''}
GRENZE = {'bild': (60, 60), 'pruefen': (8, 600), 'fehler': (30, 60), 'lesen': (300, 60)}   # je Absender: Anfragen je Zeitraum (s)
GESAMT_PRUEFEN = (200, 86400)                                                             # je Instanz und Tag (KI-Kosten)
ZAEHLER = collections.defaultdict(collections.deque)
SCHLOSS = threading.Lock()


def _zu_viel(schluessel, n, s):
    jetzt = time.time()
    with SCHLOSS:
        q = ZAEHLER[schluessel]
        while q and q[0] < jetzt - s:
            q.popleft()
        if len(q) >= n:
            return int(q[0] + s - jetzt) + 1
        q.append(jetzt)
    return 0


def _web_adresse(fl):
    """Weg der grössten Fassung (in livre.json von der Seite des Werkzeugs aus) als Adresse auf der Website."""
    return '/' + fl[6:] if fl.startswith('../../') else '/werkzeuge/livre/' + fl


def _quelle_bild(k):
    d = LV._eintrag(k)
    try:
        with urllib.request.urlopen(urllib.request.Request(HOST['basis'] + _web_adresse(d['fl']), headers={'x-werkzeug': 'livre'}), timeout=20) as r:
            roh = r.read()
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(roh)))
    except (urllib.error.HTTPError, urllib.error.URLError, OSError):
        raise ValueError('QUELLE · Das Foto liegt nicht auf der Website.')
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); grund = Image.new('RGBA', im.size, LV.PAPIER + (255,)); grund.alpha_composite(im); im = grund
    return im.convert('RGB'), False


LV._quelle_bild = _quelle_bild
LV.ohne_original = lambda: [d['k'] for d in LV._livre()['fotos']]


class handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _basis(self):
        host = self.headers.get('host', '')
        lokal = host.split(':')[0] in ('127.0.0.1', 'localhost', '[::1]')    # Probe auf dem Rechner (pruefung/online_probe.py): ohne Vercel keine Kopfzeile, also http
        proto = self.headers.get('x-forwarded-proto') or ('http' if lokal else 'https')
        HOST['basis'] = f"{proto}://{host}"

    def _absender(self):
        return (self.headers.get('x-forwarded-for') or self.client_address[0] or '?').split(',')[0].strip()

    def _grenze(self, art):
        n, s = GRENZE[art]
        w = _zu_viel(art + ':' + self._absender(), n, s)
        if not w and art == 'pruefen':
            w = _zu_viel('pruefen:alle', *GESAMT_PRUEFEN)
        if w:
            SP.sende(self, 429, {'fehler': 'GRENZE · Zu viele Anfragen. Bitte kurz warten.'}, kopf={'Retry-After': str(w)})
            return True
        return False

    def _fremd(self):
        o = (self.headers.get('origin') or '').lower()
        if o and o != HOST['basis'].lower():
            return True
        return (self.headers.get('sec-fetch-site') or 'same-origin') not in ('same-origin', 'none')

    def do_GET(self):
        pfad, q = SP.weg_von(self.path)
        self._basis()
        was = pfad.rstrip('/').rsplit('/', 1)[-1]
        if was == 'bild':
            if self._grenze('bild'):
                return
            try:
                g = lambda n, s='': (q.get(n) or [s])[0]
                d, typ, name = LV.bild(g('k'), g('f', 'web'), g('x', '.5') or .5, g('y', '.5') or .5)
                return SP.sende(self, 200, d, typ, {'Content-Disposition': 'attachment; filename="' + name + '"'})
            except ValueError as e:
                return SP.sende(self, 400, {'fehler': str(e)})
            except Exception as e:  # noqa: BLE001
                return SP.sende(self, 500, {'fehler': 'SERVER · ' + type(e).__name__})
        if was == 'stand':
            if self._grenze('lesen'):
                return
            return SP.antwort(self, lambda: dict(LV.stand(), online=True, pruefung_ki=LV._ki_an(), nur_website=True, ohne_original=LV.ohne_original()))
        return SP.sende(self, 404, {'fehler': 'WEG · Unbekannte Anfrage.'})

    def do_POST(self):
        pfad, q = SP.weg_von(self.path)
        self._basis()
        was = pfad.rstrip('/').rsplit('/', 1)[-1]
        if was not in ('pruefen', 'fehler'):
            return SP.sende(self, 404, {'fehler': 'WEG · Unbekannte Anfrage.'})
        if self._fremd():
            return SP.sende(self, 403, {'fehler': 'HERKUNFT · Anfragen von fremden Seiten werden abgewiesen.'})
        if self._grenze(was):
            return
        if 'json' not in (self.headers.get('content-type') or ''):
            return SP.sende(self, 415, {'fehler': 'EINGABE · Erwartet wird JSON.'})
        hoechstens = 4_400_000 if was == 'pruefen' else 8 * 1024
        try:
            n = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            n = hoechstens + 1
        if n > hoechstens:
            return SP.sende(self, 413, {'fehler': 'GROESSE · Die Datei ist zu gross. Online geht ein Entwurf bis rund 3 MB.' if was == 'pruefen' else 'GROESSE · Zu gross.'})
        if was == 'fehler':
            def melde():
                d = SP.koerper(self, hoechstens)
                print('LIVRE-FEHLER', json.dumps({k: str(d.get(k) or '')[:300] for k in ('zeit', 'art', 'text', 'wo', 'seite', 'browser')} if isinstance(d, dict) else {}, ensure_ascii=False))
                return {'ok': True}
            return SP.antwort(self, melde)
        return SP.antwort(self, lambda: LV.pruefen(SP.koerper(self, hoechstens)))
