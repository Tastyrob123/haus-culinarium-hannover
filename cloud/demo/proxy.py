#!/usr/bin/env python3
"""Aufnahme-Proxy: lauscht auf PORT_AUS, reicht an PORT_EIN weiter und schreibt jede Anfrage samt Antwort in ein Verzeichnis.
Aufruf: python3 proxy.py 9381 9281 /pfad/zu/aufnahme"""
import sys, os, json, hashlib, http.server, socketserver, urllib.request, urllib.error, threading

AUS, EIN, ZIEL = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
os.makedirs(os.path.join(ZIEL, 'k'), exist_ok=True)
LOCK = threading.Lock()


class H(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *a):
        pass

    def _weiter(self):
        n = int(self.headers.get('Content-Length') or 0)
        body = self.rfile.read(n) if n else b''
        url = f'http://127.0.0.1:{EIN}{self.path}'
        hdr = {k: v for k, v in self.headers.items() if k.lower() not in ('host', 'accept-encoding', 'connection', 'content-length')}
        req = urllib.request.Request(url, data=body if self.command not in ('GET', 'HEAD') else None, headers=hdr, method=self.command)
        try:
            r = urllib.request.urlopen(req, timeout=120)
            st, rh, rb = r.status, dict(r.headers.items()), r.read()
        except urllib.error.HTTPError as e:
            st, rh, rb = e.code, dict(e.headers.items()), e.read()
        except Exception as e:
            st, rh, rb = 502, {'Content-Type': 'text/plain'}, str(e).encode()
        h = hashlib.sha1(rb).hexdigest()[:16]
        with LOCK:
            p = os.path.join(ZIEL, 'k', h)
            if not os.path.exists(p):
                open(p, 'wb').write(rb)
            with open(os.path.join(ZIEL, 'log.jsonl'), 'a') as f:
                f.write(json.dumps({'m': self.command, 'p': self.path, 'st': st, 'ct': rh.get('Content-Type', ''), 'k': h,
                                    'rb': body.decode('utf-8', 'replace')[:4000]}, ensure_ascii=False) + '\n')
        self.send_response(st)
        for k, v in rh.items():
            if k.lower() in ('content-length', 'transfer-encoding', 'connection', 'content-encoding'):
                continue
            self.send_header(k, v)
        self.send_header('Content-Length', str(len(rb)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(rb)

    do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = do_HEAD = _weiter


class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


S(('127.0.0.1', AUS), H).serve_forever()
