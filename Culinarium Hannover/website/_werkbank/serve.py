#!/usr/bin/env python3
"""Vorschau-Server der Werkbank Culinarium (Werkbank-Chat 28.10.2026), nur lokal:  python3 website/_werkbank/serve.py [port], Standard 9088.
Zwei Wurzeln, damit alles der Werkbank im eigenen Revier website/_werkbank/ bleibt und die Wege trotzdem wie beim Schäfli sind:
zuerst website/_werkbank/ (werkbank/, unterlagen/, drucksachen/, feed/, mails/, material/ …), sonst website/ (die Website selbst, nur gelesen).
Mehrfädig, ohne Zwischenspeicher. Die Quellen der Werkbank (_werkbank/_werkbank/) werden nicht ausgeliefert."""
import http.server, os, socketserver, sys, urllib.parse, urllib.request, urllib.error

# Werkzeuge im Laptop bedienen (Robert 29.10.2026): /_werkzeuge/<werkzeug>/ reicht dieser Server an den Prüfserver des Werkzeugs weiter, damit das
# Werkzeug als gleiche Herkunft eingebettet werden kann (die Werkzeug-Server erlauben Rahmen nur von sich selbst); ihre Antworten bleiben sonst unverändert.
WERKZEUG_PORT = {'maison': 9081, 'oberflaeche': 9081, 'bureau': 9082, 'carte': 9083, 'reception': 9084, 'livre': 9085, 'registre': 9086, 'imprimerie': 9087}

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(HIER)
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9088


class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        teil = urllib.parse.unquote(path.split('?', 1)[0].split('#', 1)[0]).lstrip('/')
        teil = os.path.normpath(teil) if teil else ''
        if teil.startswith('..'):
            return os.path.join(HIER, '__nicht__')
        if teil.startswith('_werkbank/fonts/') or teil.startswith('_werkbank/satz/'):   # feste Druckschnitte und Satz der Drucksachen (Kit: papier_druck.js, sb_ki.PDF_JS)
            return os.path.join(HIER, teil)
        if teil == '_werkbank' or teil.startswith('_werkbank/') or teil.startswith('pruefung'):
            return os.path.join(HIER, '__nicht__')
        eigen = os.path.join(HIER, teil)
        if teil and teil != 'assets' and not teil.startswith('assets/') and os.path.exists(eigen):
            return eigen
        return os.path.join(WEB, teil)

    def _weiter(self):
        teile = self.path.split('/')
        ref = urllib.parse.urlparse(self.headers.get('Referer') or '').path.split('/')
        ref_port = WERKZEUG_PORT.get(ref[2]) if len(ref) > 2 and ref[1] == '_werkzeuge' else None
        if len(teile) >= 3 and teile[1] == '_werkzeuge' and teile[2] in WERKZEUG_PORT:
            port = WERKZEUG_PORT[teile[2]]
        elif self.path.startswith('/assets/oberflaeche/'):   # das gemeinsame Kleid der Werkzeuge liegt an der Wurzel jedes Werkzeug-Servers
            port = ref_port or 9081
        elif self.path.startswith(('/stamm/', '/werkzeuge/')):   # Stammdaten und Teile des Schaufensters liegen nur bei ihm
            port = 9082
        elif self.path.startswith('/api/'):   # Schnittstellen an der Wurzel: an das Werkzeug, von dessen Seite die Anfrage kommt; ohne Herkunft fragt nur das Schaufenster so
            port = ref_port or 9082
        else:
            return False
        laenge = int(self.headers.get('Content-Length') or 0)
        daten = self.rfile.read(laenge) if laenge else None
        ziel = f'http://127.0.0.1:{port}'
        kopf = {k: v for k, v in self.headers.items() if k.lower() not in ('host', 'connection', 'accept-encoding', 'content-length')}
        for k in list(kopf):   # das Werkzeug sieht sich selbst als Herkunft (es prüft Origin und Referer bei Anfragen, die etwas schreiben)
            if k.lower() == 'origin':
                kopf[k] = ziel
            elif k.lower() == 'referer':
                kopf[k] = ziel + urllib.parse.urlparse(kopf[k]).path
        req = urllib.request.Request(ziel + self.path, data=daten, method=self.command, headers=kopf)
        try:
            r = urllib.request.urlopen(req, timeout=300)
        except urllib.error.HTTPError as e:
            r = e
        except Exception:
            self.send_error(502); return True
        inhalt = r.read()
        self.send_response(r.status if hasattr(r, 'status') else r.code)
        for k, v in r.headers.items():
            if k.lower() in ('x-frame-options', 'content-length', 'transfer-encoding', 'connection', 'date', 'server'):
                continue
            if k.lower() == 'content-security-policy':
                v = ';'.join(x for x in v.split(';') if 'frame-ancestors' not in x).strip() or None
                if not v:
                    continue
            self.send_header(k, v)
        self.send_header('Content-Length', str(len(inhalt)))
        super().end_headers()
        if self.command != 'HEAD':
            self.wfile.write(inhalt)
        return True

    def do_GET(self):
        if not self._weiter():
            super().do_GET()

    def do_HEAD(self):
        if not self._weiter():
            super().do_HEAD()

    def do_PUT(self):
        if not self._weiter():
            self.send_error(405)

    do_DELETE = do_PATCH = do_PUT

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, *a):
        pass

    def do_POST(self):   # Messung der Website (falls eingebaut) nimmt die Vorschau an und speichert nichts
        if self._weiter():
            return
        self.rfile.read(min(int(self.headers.get('Content-Length') or 0), 13000))
        self.send_response(204); self.end_headers()


class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    S(('127.0.0.1', PORT), H).serve_forever()
