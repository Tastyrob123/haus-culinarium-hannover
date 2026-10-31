#!/usr/bin/env python3
"""Le Livre · Culinarium Hannover · Sicherheit des Servers (Vorlage Schäfli, dort nur gelesen) (FUNKTIONEN.md Zeile 89, Master L12), gegen den laufenden Prüfserver oder die Online-Probe.
   python3 _werkzeuge/livre/pruefung/sicherheit.py [basis]        basis = http://127.0.0.1:9085 (lokal, Weg /_werkzeuge/livre/api/) oder mit «online» (Weg /werkzeuge/livre/api/)
Prüft: fremder Host 421, fremde Herkunft 403 (Origin und Sec-Fetch-Site), zu gross 413, kein JSON 415, kaputtes JSON 400, zu viele Prüfungen 429 mit Retry-After,
gesperrte Pfade 404, erlaubte Wege 200. Danach ist die Prüfung eine Minute gesperrt (Grenze), deshalb als letzter Lauf."""
import http.client, json, os, sys, urllib.parse

BASIS = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:9085').rstrip('/')
ONLINE = 'online' in sys.argv[2:]
API = '/werkzeuge/livre/api/' if ONLINE else '/_werkzeuge/livre/api/'
u = urllib.parse.urlparse(BASIS)
erg = []
def z(t, ok, m=''): erg.append(dict(t=t, ok=bool(ok), m=str(m))); print(('✓' if ok else '✗'), t, '·', m)


def frage(methode, pfad, kopf=None, koerper=b'', host=None):
    c = http.client.HTTPConnection(u.hostname, u.port, timeout=30)
    k = {'Host': host or u.netloc}
    k.update(kopf or {})
    c.putrequest(methode, pfad, skip_host=True, skip_accept_encoding=True)
    for a, b in k.items():
        c.putheader(a, b)
    c.endheaders()
    if koerper:
        try:
            c.send(koerper)
        except (BrokenPipeError, ConnectionResetError):
            pass
    try:
        r = c.getresponse(); d = r.read(); return r.status, dict(r.getheaders()), d
    except (ConnectionResetError, http.client.RemoteDisconnected):
        return 0, {}, b''


j = lambda d: json.dumps(d).encode()
if not ONLINE:
    s, _, d = frage('GET', API + 'stand', host='boese.example:9085'); z('Fremder Host → 421', s == 421, s)
s, _, d = frage('POST', API + 'pruefen', {'Content-Type': 'application/json', 'Origin': 'https://boese.example', 'Content-Length': '2'}, b'{}'); z('Fremde Herkunft (Origin) → 403', s == 403, s)
s, _, d = frage('POST', API + 'pruefen', {'Content-Type': 'application/json', 'Sec-Fetch-Site': 'cross-site', 'Content-Length': '2'}, b'{}'); z('Fremde Herkunft (Sec-Fetch-Site) → 403', s == 403, s)
s, _, d = frage('POST', API + 'fehler', {'Content-Type': 'application/json', 'Content-Length': str(9000)}, b'x' * 9000); z('Fehlerbericht über 8 KB → 413', s == 413, s)
gross = 46 * 1024 * 1024 if not ONLINE else 4_500_000
s, _, d = frage('POST', API + 'pruefen', {'Content-Type': 'application/json', 'Content-Length': str(gross)}, b''); z(f'Prüfung über {gross // 1048576} MB → 413', s == 413, s)
s, _, d = frage('POST', API + 'pruefen', {'Content-Type': 'text/plain', 'Content-Length': '2'}, b'{}'); z('Kein JSON → 415', s == 415, s)
s, _, d = frage('POST', API + 'pruefen', {'Content-Type': 'application/json', 'Content-Length': '5'}, b'{kapu'); z('Kaputtes JSON → 400 mit Stichwort', s == 400 and b'EINGABE' in d, (s, d[:60]))
s, _, d = frage('POST', API + 'pruefen', {'Content-Type': 'application/json', 'Content-Length': '2'}, b'{}'); z('Leere Prüfung → 400 «DATEI · Keine Datei angekommen»', s == 400 and 'DATEI' in d.decode(), (s, d.decode()[:60]))
s, _, d = frage('GET', API + 'bild?k=gibt-es-nicht&f=web'); z('Unbekanntes Foto → 400 «BILD · …»', s == 400 and 'BILD' in d.decode(), (s, d.decode()[:60]))
s, _, d = frage('GET', API + 'bild?k=pass4&f=riesig'); z('Unbekannte Grösse → 400 «FORMAT · …»', s == 400 and 'FORMAT' in d.decode(), s)
s, _, d = frage('GET', API + 'nichts'); z('Unbekannter Weg → 400/404 mit Stichwort', s in (400, 404) and 'WEG' in d.decode(), s)
if not ONLINE:
    gesperrt = ['/_werkzeuge/livre/livre.py', '/_werkzeuge/livre/server.py', '/_werkzeuge/livre/_quellen.json', '/_werkzeuge/livre/_register-vor-schaerfen.json', '/_werkzeuge/livre/LIEFERUNG.md', '/_werkzeuge/livre/FUNKTIONEN.md',
                '/_werkzeuge/livre/_qa/fehler.jsonl', '/_werkzeuge/livre/pruefung/funktionen.js', '/_werkzeuge/livre/online/livre_online.py', '/_werkzeuge/livre/bau.py', '/_werkzeuge/livre/pruefung/bedienen.js',
                '/bau.py', '/abende_info.py', '/_qa/', '/_sicherung/', '/_zuschnitt/plakatwand.jpg', '/_werkbank/serve.py', '/_alt/', '/.git/config', '/_werkzeuge/reception/server.py', '/_werkzeuge/carte/serve.py', '/_werkzeuge/livre/../../bau.py',
                '/%2e%2e/%2e%2e/etc/passwd', '/_werkzeuge/livre/%2e%2e/%2e%2e/bau.py']
    offen = [p for p in gesperrt if frage('GET', p)[0] not in (404, 400)]
    z(f'Gesperrte Pfade ({len(gesperrt)}) → 404', not offen, offen or 'alle 404')
    erlaubt = ['/_werkzeuge/livre/', '/_werkzeuge/livre/livre.json', '/marke/livre.json', '/_werkzeuge/livre/buch.html', '/_werkzeuge/livre/dateien/culinarium-hannover-marke.zip', '/index.html', '/assets/bild/pass4-1600.webp', '/assets/oberflaeche/kleid/culinarium.js', '/_werkzeuge/livre/anleitung.html']
    zu = [p for p in erlaubt if frage('GET', p)[0] != 200]
    z(f'Erlaubte Wege ({len(erlaubt)}) → 200', not zu, zu or 'alle 200')
    s, k, _ = frage('GET', '/_werkzeuge/livre/')
    z('Sicherheitskopfzeilen (nosniff, SAMEORIGIN, Referrer)', k.get('X-Content-Type-Options') == 'nosniff' and k.get('X-Frame-Options') == 'SAMEORIGIN' and k.get('Referrer-Policy'), {a: k.get(a) for a in ('X-Content-Type-Options', 'X-Frame-Options')})
# Grenze: Prüfungen je Minute (lokal 20, online 8 je 10 Minuten); die Grenze zählt vor allen anderen Prüfungen, darum genügen Anfragen ohne Inhalt
codes = [frage('POST', API + 'pruefen', {'Content-Type': 'text/plain', 'Content-Length': '0'})[0] for _ in range(22)]
s, k, d = frage('POST', API + 'pruefen', {'Content-Type': 'text/plain', 'Content-Length': '0'})
z('Zu viele Prüfungen → 429 mit Retry-After', s == 429 and int(k.get('Retry-After', 0)) > 0 and 429 in codes, f'{codes.count(415)}× 415, dann {codes.count(429) + 1}× 429, Retry-After {k.get("Retry-After")}')
os.makedirs(os.path.join(os.path.dirname(__file__), 'ergebnisse'), exist_ok=True)
json.dump(erg, open(os.path.join(os.path.dirname(__file__), 'ergebnisse', 'sicherheit-' + ('online' if ONLINE else 'lokal') + '.json'), 'w'), ensure_ascii=False, indent=1)
print(f"Summe: {sum(e['ok'] for e in erg)}/{len(erg)}")
sys.exit(0 if all(e['ok'] for e in erg) else 1)
