#!/usr/bin/env python3
"""Le Bureau (Website pflegen) · Culinarium Hannover — eigener Server (28.10.2026, nach dem Vorbild des Schäfli). python3 _werkzeuge/bureau/serve.py [port]   (Standard 9082)

Das Werkzeug selbst ist der Schreibtisch des Stamms (~/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website/, Schicht über den gebauten
Seiten, Probe-Kopie _probe/culinarium/, Speicher _Werkzeuge/daten/). Dieser Server legt den Rahmen des Hauses darum, wie bei den anderen
Werkzeugen von Culinarium:
  /_werkzeuge/bureau/…        Seite des Werkzeugs (index.html, bureau.css) aus diesem Ordner
  /assets/oberflaeche/…        gemeinsamer Werkzeug-Rahmen des Hauses (_werkzeuge/oberflaeche/, Kleid culinarium)
  /assets/…                    Schriften und Fotos der Website (website/assets/, nur gelesen)
  /_werkzeuge/bureau/api/termine…   Termine der Abende (termine.py): Entwurf, Stand, Verlauf; buchen.js der Probe-Kopie wird mit dem Stand gefüllt
  /_werkzeuge/bureau/vorschau/…      die Probe-Kopie mit den Terminen des Entwurfs (Vorschau in der Ansicht «Termine»)
  alles andere                 wie der Server des Stamms (unterbau/serve.py): /api/…, /stamm/…, /werkzeuge/website/…, /haeuser/…
Sicherheit (Master Werkzeug-Bau 5.2/5.3, S01–S03): hört nur auf 127.0.0.1, nur Anfragen an diese Adresse (421), schreibende Wege nur von der
eigenen Seite (403) und nur als JSON, höchstens 3 MB je Anfrage (413), Grenze je Absender und Minute für die Wege des Werkzeugs (429, Retry-After),
feste Kopfzeilen gegen Einbetten und fremde Skripte (die Vorschau der Seiten läuft als srcdoc im Rahmen und braucht deren eigene Skripte).
Daten: WERKZEUGE_DATEN (Wegwerf-Ordner für Prüfläufe), sonst die echten unter _Werkzeuge/daten/."""
import os
import re
import sys
import threading
import time
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parent.parent
OBERFLAECHE = PROJEKT / '_werkzeuge' / 'oberflaeche'
ASSETS = PROJEKT / 'website' / 'assets'
STAMM = Path(os.path.expanduser('~/Desktop/Website-Projekte/_Werkzeuge'))
sys.path.insert(0, str(STAMM / 'unterbau'))
import serve as stamm  # noqa: E402  (Server des Stamms: Wege, Speicher, Dateien)
sys.path.insert(0, str(HIER))
import termine as T  # noqa: E402  (Termine der Abende, Daten aus website/assets/buchen.js)

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('BUREAU_PORT', '9082'))
GROSS = 3_000_000
GROSS_FOTO = 36 * 1024 * 1024        # eigenes Foto: bis 25 MB, als Base64 gut ein Drittel mehr (Master 6, F71)
WEG_FOTO = 64 * 1024 * 1024          # Rest einer zu grossen Anfrage wird bis hier gelesen und verworfen, dann 413 (sonst bricht der Browser mit «Verbindung getrennt» ab)
DATEN = HIER / '_daten'               # Fehlerprotokoll des Browsers (R03), nie ausgeliefert
if os.environ.get('WERKZEUGE_DATEN'):   # Prüfläufe mit Wegwerf-Daten schreiben ihre Probe-Fehler nicht ins echte Protokoll (Demo-Check 21.10.2026)
    DATEN = Path(os.environ['WERKZEUGE_DATEN']) / 'bureau-fehler'
GRENZEN = {'alle': 900, 'schreiben': 60}
if os.environ.get('BUREAU_PRUEFLAUF'):   # fester Prüflauf (pruef.js) schreibt in einer Minute mehr als ein Mensch; Grenze selbst prüft der Lauf nicht
    GRENZEN = {'alle': 90000, 'schreiben': 6000}
_ZAEHLER, _SCHLOSS = {}, threading.Lock()
ENDUNG_OK = {'.html', '.css', '.js', '.json', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.woff2', '.ttf', '.ico', '.avif', '.gif', '.txt'}
KOPF = {'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer', 'X-Frame-Options': 'SAMEORIGIN',
        'Permissions-Policy': 'camera=(), microphone=(), geolocation=()', 'Cross-Origin-Opener-Policy': 'same-origin'}
# Ohne script-src: die Vorschau setzt die Seite als srcdoc in den Rahmen, srcdoc erbt die Regel der Werkzeug-Seite, und die Seite samt Klick-Skript
# der Vorschau braucht eingebettete Skripte (Fund Ruedihus 2: Vorschau von der Regel ausnehmen). Einbetten, Formulare und base bleiben gesperrt.
CSP = "frame-ancestors 'self'; base-uri 'self'; form-action 'self'; object-src 'none'"


TEIL = {'maison': 'zentrale', 'carte': 'karten', 'imprimerie': 'druck', 'reception': 'gaeste', 'livre': 'marke', 'registre': 'besuche'}


PORTE = {'maison': 9081, 'carte': 9083, 'reception': 9084, 'livre': 9085, 'registre': 9086, 'imprimerie': 9087}   # AUFTRAG-GEMEINSAM.md, je Werkzeug-Chat ein Port


def nachbar(k):
    """Adresse eines anderen Werkzeugs des Hauses: was es in der Kette angibt (_kette/11-werkbank/werkzeuge/<teil>/stand.json › adresse),
    sonst sein Port aus dem gemeinsamen Auftrag (Zentrale 9081, Karten 9083 …). Jedes Werkzeug läuft bis zur Auslieferung auf eigenem Port;
    ein Kopf-Knopf «/_werkzeuge/maison/» führt sonst hier ins Leere."""
    import json
    try:
        a = json.loads((PROJEKT / '_kette' / '11-werkbank' / 'werkzeuge' / TEIL[k] / 'stand.json').read_text(encoding='utf-8')).get('adresse') or ''
    except (OSError, ValueError, KeyError):
        a = ''
    return a if urlparse(a).hostname in ('127.0.0.1', 'localhost') else f'http://127.0.0.1:{PORTE[k]}/_werkzeuge/{k}/'


def zu_viele(wer, art):
    jetzt = time.time()
    with _SCHLOSS:
        z = [t for t in _ZAEHLER.get((wer, art), []) if jetzt - t < 60]
        z.append(jetzt)
        _ZAEHLER[(wer, art)] = z
        return len(z) > GRENZEN[art]


_FEHLER_SCHLOSS = threading.Lock()


def fehler_merken(d):
    """R03: Skriptfehler des Browsers, angehängt unter einem Schloss (F34), höchstens 1 MB, dann neu begonnen."""
    import json
    DATEN.mkdir(exist_ok=True)
    p = DATEN / 'fehler.jsonl'
    zeile = json.dumps({'zeit': time.strftime('%Y-%m-%dT%H:%M:%S'), 'text': str(d.get('text') or '')[:400], 'stichwort': str(d.get('stichwort') or '')[:40],
                        'wo': str(d.get('wo') or '')[:120], 'quelle': str(d.get('quelle') or '')[:200]}, ensure_ascii=False)
    with _FEHLER_SCHLOSS:
        if p.exists() and p.stat().st_size > 1_000_000:
            p.replace(DATEN / 'fehler.alt.jsonl')
        with open(p, 'a', encoding='utf-8') as f:
            f.write(zeile + '\n')


def fehler_lesen(n=50):
    import json
    p = DATEN / 'fehler.jsonl'
    if not p.exists():
        return []
    aus = []
    for z in p.read_text(encoding='utf-8').splitlines()[-n:]:
        try:
            aus.append(json.loads(z))
        except ValueError:
            continue
    return aus[::-1]


class Antwort(stamm.Antwort):
    server_version = 'Bureau-Culinarium/1'

    def handle_one_request(self):
        """Leistung (29.10.2026): Antwort erst sammeln, dann Text gepackt senden (wie online, Vercel packt auch) und Schriften sowie Dateien mit ?v=
        (Fassung aus dem Inhalt) behaltbar machen. Der Server des Stamms bleibt unverändert; nur dieser Rahmen von Culinarium packt."""
        import gzip, io
        echt, puffer = self.wfile, io.BytesIO()
        self.wfile = puffer
        try:
            super().handle_one_request()
        finally:
            self.wfile = echt
            roh = puffer.getvalue()
            if roh:
                kopf, trenn, rumpf = roh.partition(b'\r\n\r\n')
                zeilen = kopf.split(b'\r\n')
                n = {z.split(b':', 1)[0].strip().lower(): z for z in zeilen[1:] if b':' in z}
                art = n.get(b'content-type', b'').split(b':', 1)[-1].strip().lower()
                weg = urlparse(getattr(self, 'path', '') or '').path
                if trenn and zeilen[0].split(b' ')[1:2] == [b'200'] and getattr(self, 'command', '') == 'GET':
                    import hashlib
                    v = (re.search(r'[?&]v=([0-9a-f]{6,40})', getattr(self, 'path', '') or '') or [None, None])[1]
                    if (weg.endswith('.woff2') or (v and hashlib.sha1(rumpf).hexdigest().startswith(v))) and '/api/' not in weg:   # nur behalten, wenn die Nummer zum Inhalt passt
                        zeilen = [z for z in zeilen if not z.lower().startswith(b'cache-control:')] + [b'Cache-Control: public, max-age=31536000, immutable']
                    if (len(rumpf) > 1024 and b'content-encoding' not in n and 'gzip' in (self.headers.get('Accept-Encoding') or '' if self.headers else '')
                            and re.match(rb'(text/|application/(json|javascript|xml)|image/svg)', art)):
                        rumpf = gzip.compress(rumpf, 6)
                        zeilen = [z for z in zeilen if not z.lower().startswith(b'content-length:')] + [b'Content-Length: ' + str(len(rumpf)).encode(), b'Content-Encoding: gzip', b'Vary: Accept-Encoding']
                    roh = b'\r\n'.join(zeilen) + trenn + rumpf
                echt.write(roh)
                echt.flush()

    def end_headers(self):
        for k, v in KOPF.items():
            self.send_header(k, v)
        self.send_header('Content-Security-Policy', CSP)
        super().end_headers()

    def _datei(self, wurzel, rest):
        ziel = (wurzel / rest).resolve()
        if wurzel.resolve() not in ziel.parents or not ziel.is_file() or ziel.suffix.lower() not in ENDUNG_OK or any(t.startswith('.') or t in ('_daten', '__pycache__') for t in Path(rest).parts):
            return self._json(404, {'fehler': 'Nicht gefunden', 'stichwort': 'nicht-gefunden'})
        roh = ziel.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', stamm.mimetypes.guess_type(ziel.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(len(roh)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(roh)

    def _pruefseite(self):
        """Prüfseite des Stamms im Kleid des Hauses (Demo-Check 21.10.2026, aus dem Vorbild): ohne den Weltknopf «Grandhotel/Landhaus»
        des Stamms, mit dem Namen des Werkzeugs aus WO_HAUS.namen.website und «Zum Werkzeug» zurück in dieses Werkzeug. Die Datei des Stamms bleibt
        unverändert; hier werden nur Kopf und Stile eingesetzt, die Stilfassung aus dem Inhalt (M20)."""
        import hashlib
        def v(p):
            return hashlib.sha1(p.read_bytes()).hexdigest()[:10] if p.is_file() else '1'
        ob = OBERFLAECHE
        roh = (STAMM / 'werkzeuge' / 'website' / 'pruefung.html').read_text(encoding='utf-8')
        roh = roh.replace('<title>Prüfung · Website pflegen</title>', '<title>Prüfung · Website pflegen · Culinarium</title>')
        roh = roh.replace('<link rel="stylesheet" href="/stamm/welt.css">', f'<script src="/assets/oberflaeche/kleid/culinarium.js?v={v(ob / "kleid/culinarium.js")}"></script>\n<link rel="stylesheet" href="/stamm/welt.css">')
        roh = roh.replace('<script src="/stamm/welt.js"></script>', '<script src="/stamm/welt.js" data-haus="culinarium"></script>')
        roh = re.sub(r'(<link rel="stylesheet" href="pruefung\.css\?v=[^"]*">)', lambda m: m.group(1) + f'\n<link rel="stylesheet" href="/assets/oberflaeche/grund.css?v={v(ob / "grund.css")}"><link rel="stylesheet" href="/assets/oberflaeche/kleid/culinarium.css?v={v(ob / "kleid/culinarium.css")}">'
                     f'\n<link rel="stylesheet" href="/_werkzeuge/bureau/bureau.css?v={v(HIER / "bureau.css")}"><link rel="stylesheet" href="/_werkzeuge/bureau/pruefung-haus.css?v={v(HIER / "pruefung-haus.css")}">', roh, 1)
        roh = roh.replace('<button data-welt-knopf></button>', '')
        roh = re.sub(r'(<script src="pruefung\.js\?v=[^"]*"></script>)', lambda m: m.group(1) + f'\n<script src="/_werkzeuge/bureau/pruefung-haus.js?v={v(HIER / "pruefung-haus.js")}"></script>', roh, 1)
        daten = roh.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(daten)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(daten)

    def _termine(self, methode, weg):
        """Termine der Abende (termine.py). GET: Lage · GET pruefung · POST speichern / veroeffentlichen / verwerfen / zurueckholen."""
        import json
        try:
            if methode == 'GET' and weg == '':
                return self._json(200, T.lage())
            if methode == 'GET' and weg == 'pruefung':
                return self._json(200, {'punkte': T.pruefung()})
            if methode != 'POST' or weg not in ('speichern', 'veroeffentlichen', 'verwerfen', 'zurueckholen'):
                return self._json(404, {'fehler': 'Nicht gefunden', 'stichwort': 'nicht-gefunden'})
            try:
                d = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)).decode('utf-8') or '{}')
            except ValueError:
                return self._json(400, {'fehler': 'Die Anfrage ist kein gültiges JSON', 'stichwort': 'anfrage-unlesbar'})
            erw = str(d.get('erwartet') or '')
            if weg == 'speichern':
                return self._json(200, T.speichern(d.get('termine'), erw))
            if weg == 'veroeffentlichen':
                return self._json(200, T.veroeffentlichen(erw, d.get('notiz') or ''))
            if weg == 'verwerfen':
                return self._json(200, T.verwerfen(erw))
            return self._json(200, T.zurueckholen(d.get('nr'), erw))
        except T.Fehler as e:
            return self._json(e.status, {'fehler': e.text, 'stichwort': e.stichwort})

    def _ueberblick(self):
        """Stand-Weg für La Maison (Master 4.1): {aenderungen, zuletzt:{zeit}, bereiche, seiten}. Texte und Fotos aus dem Stamm
        (/api/x/website/ueberblick/culinarium), dazu die Termine: was im Entwurf wartet, zählt mit; zuletzt ist die jüngste Veröffentlichung von beidem."""
        try:
            status, s = stamm._werkzeug_api('website').bearbeite('GET', ['ueberblick', 'culinarium'], {}, stamm.speicher)
        except Exception as e:   # noqa: BLE001  (der Stand-Weg antwortet immer, die Zentrale zeigt dann «antwortet nicht» nicht fälschlich)
            status, s = 500, {'fehler': str(e)[:200], 'stichwort': 'unerwartet'}
        if status != 200:
            return self._json(status, s)
        try:
            l = T.lage()
            n = T.wartend(l)
            s = dict(s, aenderungen=int(s.get('aenderungen') or 0) + n, termine={'wartet': n, 'zahl': len(l['entwurf'] if l['entwurf'] is not None else l['stand'])})
            z = (l.get('zuletzt') or {}).get('zeit')
            if z and z > ((s.get('zuletzt') or {}).get('zeit') or ''):
                s['zuletzt'] = {'zeit': z, 'was': 'Termine'}
        except T.Fehler as e:
            s = dict(s, termine={'fehler': e.text, 'stichwort': e.stichwort})
        return self._json(200, s)

    def _probe_datei(self, teil, rest, termine, ordner='_probe'):
        """Eine Datei der Probe-Kopie; buchen.js gefüllt mit den Terminen des Stands oder des Entwurfs. Pfad nie ausserhalb der Kopie."""
        wurzel = (Path(os.environ.get('WEBSITE_PROBE') or STAMM / 'werkzeuge' / 'website' / ordner) / 'culinarium' / teil).resolve()
        ziel = (wurzel / rest).resolve()
        if wurzel not in ziel.parents or not ziel.is_file() or ziel.suffix.lower() not in ENDUNG_OK | {'.mp4', '.woff'} or any(t.startswith('.') for t in Path(rest).parts):
            return self._json(404, {'fehler': 'Nicht gefunden', 'stichwort': 'nicht-gefunden'})
        roh = ziel.read_bytes()
        if rest == 'assets/buchen.js':
            try:
                roh = T.ausliefern(roh.decode('utf-8'), termine).encode('utf-8')
            except T.Fehler:
                pass   # Quelle unlesbar: die Datei, wie sie ist (die Website zeigt dann ihre eigenen Termine), die Prüfung meldet es
        self.send_response(200)
        self.send_header('Content-Type', stamm.mimetypes.guess_type(ziel.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(len(roh)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(roh)

    def _bedien(self, methode):
        if self.headers.get('Host', '') not in (f'127.0.0.1:{PORT}', f'localhost:{PORT}'):
            return self._json(421, {'fehler': 'Falsche Adresse', 'stichwort': 'fremder-host'})
        pfad = unquote(urlparse(self.path).path)
        werkzeug = pfad.startswith('/api/') or pfad.startswith('/_werkzeuge/bureau/api/')
        schreibt = methode in ('POST', 'PUT', 'DELETE')
        if werkzeug and zu_viele(self.client_address[0], 'schreiben' if schreibt else 'alle'):
            self.send_response(429)
            self.send_header('Retry-After', '60')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        if schreibt:
            herkunft = self.headers.get('Origin')
            if herkunft not in (f'http://127.0.0.1:{PORT}', f'http://localhost:{PORT}'):
                return self._json(403, {'fehler': 'Nur von der eigenen Seite', 'stichwort': 'fremde-herkunft'})
            laenge = int(self.headers.get('Content-Length') or 0)
            foto = pfad.startswith('/api/x/website/hochladen/')
            if laenge > (GROSS_FOTO if foto else GROSS):
                rest = min(laenge, WEG_FOTO)
                while rest > 0:
                    stueck = self.rfile.read(min(rest, 1 << 20))
                    if not stueck:
                        break
                    rest -= len(stueck)
                self.close_connection = True
                return self._json(413, {'fehler': 'Das Foto ist grösser als 25 MB.' if foto else 'Zu gross', 'stichwort': 'bild-gross' if foto else 'zu-gross'})
            if not (self.headers.get('Content-Type') or '').startswith('application/json') and int(self.headers.get('Content-Length') or 0):
                return self._json(415, {'fehler': 'Nur JSON', 'stichwort': 'anfrage-unlesbar'})
        if methode == 'POST' and pfad == '/_werkzeuge/bureau/api/fehler':
            import json
            try:
                fehler_merken(json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)).decode('utf-8') or '{}'))
            except ValueError:
                return self._json(400, {'fehler': 'Unlesbar', 'stichwort': 'anfrage-unlesbar'})
            return self._json(200, {'ok': True})
        if methode == 'POST' and pfad.startswith('/api/x/website/hochladen/'):
            # Fotos sind grösser als die Grenze des Stamm-Servers (20 MB): hier lesen, dann direkt das Werkzeug fragen
            import json
            try:
                daten = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)).decode('utf-8') or '{}')
            except ValueError:
                return self._json(400, {'fehler': 'Die Anfrage ist kein gültiges JSON', 'stichwort': 'anfrage-unlesbar'})
            status, antwort = stamm._werkzeug_api('website').bearbeite('POST', pfad.strip('/').split('/')[3:], daten, stamm.speicher)
            return self._json(status, antwort)
        if methode == 'GET' and pfad == '/_werkzeuge/bureau/api/ueberblick':
            return self._ueberblick()
        if pfad.startswith('/_werkzeuge/bureau/api/termine'):
            return self._termine(methode, pfad[len('/_werkzeuge/bureau/api/termine'):].strip('/'))
        if methode == 'GET' and pfad.startswith('/_werkzeuge/bureau/vorschau/'):
            return self._probe_datei('online', pfad[len('/_werkzeuge/bureau/vorschau/'):] or 'index.html', 'entwurf')
        m = re.fullmatch(r'/werkzeuge/website/(_probe[\w-]*)/culinarium/online/(assets/buchen\.js)', pfad) if methode == 'GET' else None
        if m:   # veröffentlichte Termine: buchen.js der Probe-Kopie wird beim Ausliefern mit dem Stand gefüllt (termine.py)
            return self._probe_datei('online', m.group(2), 'stand', m.group(1))
        if methode == 'GET' and pfad == '/_werkzeuge/bureau/api/fehler':
            return self._json(200, {'fehler': fehler_lesen()})
        if methode == 'GET' and pfad == '/werkzeuge/website/pruefung.html':
            return self._pruefseite()
        if methode == 'GET':
            if pfad in ('/', '/_werkzeuge/bureau'):
                self.send_response(301)
                self.send_header('Location', '/_werkzeuge/bureau/' + ('?' + urlparse(self.path).query if urlparse(self.path).query else ''))
                self.end_headers()
                return
            if pfad.startswith('/_werkzeuge/bureau/'):
                rest = pfad[len('/_werkzeuge/bureau/'):] or 'index.html'
                if rest.endswith('.py') or rest.endswith('.sh'):
                    return self._json(404, {'fehler': 'Nicht gefunden', 'stichwort': 'nicht-gefunden'})
                return self._datei(HIER, rest)
            teile = pfad.strip('/').split('/')
            if len(teile) >= 2 and teile[0] == '_werkzeuge' and teile[1] in TEIL:
                self.send_response(302)
                self.send_header('Location', nachbar(teile[1]))
                self.send_header('Content-Length', '0')
                self.end_headers()
                return
            if pfad.startswith('/assets/oberflaeche/'):
                return self._datei(OBERFLAECHE, pfad[len('/assets/oberflaeche/'):])
            if pfad.startswith('/assets/'):
                return self._datei(ASSETS, pfad[len('/assets/'):])
            m = re.fullmatch(r'/werkzeuge/website/(_probe[\w-]*)/culinarium/(grundlage|online)/assets/daten/([\w-]+\.json)', pfad)
            if m:   # Weindaten der Seiten (assets/daten/wein*.json): der Stamm sperrt jeden Pfad mit «daten» (Schutz seines Speichers), Weinkarte und Weinwelt blieben in der Vorschau leer (Demo-Check 21.10.2026)
                return self._datei(STAMM / 'werkzeuge' / 'website' / m.group(1) / 'culinarium' / m.group(2) / 'assets' / 'daten', m.group(3))
        return super()._bedien(methode)


if __name__ == '__main__':
    os.chdir(STAMM)
    print(f'Le Bureau (Culinarium) auf http://127.0.0.1:{PORT}/_werkzeuge/bureau/')
    ThreadingHTTPServer(('127.0.0.1', PORT), Antwort).serve_forever()
