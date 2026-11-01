#!/usr/bin/env python3
"""Baut die Werkbank als statischen Ordner für ein Artifact (höchstens 511 Dateien).
Aufruf: python3 werkbank.py <werkbank-ordner> <wege.json> <ausgabe> [links.json]
wege.json: Liste der Wege (relativ zum Werkbank-Ordner), z. B. aus einem Durchlauf aller Werkbank-Seiten bei 1440 und 390.
- gleiche Dateien (gleicher Inhalt) nur einmal, Verweise zeigen auf die eine
- Bildgrößen-Reihen (x-1200/x-1800/x-2400.webp) nur eine Größe
- http://127.0.0.1:908x-Verweise → Demo-Adressen aus links.json ({"9081": "...", "website": "..."})"""
import sys, os, json, re, hashlib, shutil, posixpath, collections
from urllib.parse import unquote, quote

QUELLE, WEGE, AUS = sys.argv[1], sys.argv[2], sys.argv[3]
LINKS = json.load(open(sys.argv[4])) if len(sys.argv) > 4 and os.path.exists(sys.argv[4]) else {}
GROESSE = 1800

wege = [w for w in json.load(open(WEGE)) if os.path.isfile(os.path.join(QUELLE, w)) and os.path.getsize(os.path.join(QUELLE, w)) < 14.5e6]
umleiten = {}

# Bildgrößen-Reihen: nur eine Größe behalten (die nächste an GROESSE)
reihe = collections.defaultdict(list)
for w in wege:
    m = re.match(r'(.*)-(\d{3,4})\.(webp|jpg|avif)$', w)
    if m:
        reihe[(m.group(1), m.group(3))].append((int(m.group(2)), w))
for l in reihe.values():
    if len(l) > 1:
        bleibt = min(l, key=lambda x: abs(x[0] - GROESSE))[1]
        for _, w in l:
            if w != bleibt:
                umleiten[w] = bleibt

# gleicher Inhalt: eine Datei
nach_hash = collections.defaultdict(list)
for w in wege:
    if w in umleiten:
        continue
    nach_hash[hashlib.sha1(open(os.path.join(QUELLE, w), 'rb').read()).hexdigest()].append(w)
for l in nach_hash.values():
    if len(l) > 1:
        bleibt = sorted(l, key=lambda w: (bool(re.search(r'[:*?"<>|\\]', w)), not w.startswith('material/'), len(w)))[0]   # «:» u. ä. nimmt das Artifact nicht   # Material-Namen sind die lesbaren Dateinamen
        for w in l:
            if w != bleibt:
                umleiten[w] = bleibt

behalten = [w for w in wege if w not in umleiten]
shutil.rmtree(AUS, ignore_errors=True)
for w in behalten:
    z = os.path.join(AUS, w)
    os.makedirs(os.path.dirname(z), exist_ok=True)
    shutil.copyfile(os.path.join(QUELLE, w), z)

menge = set(behalten)
fehlend = collections.Counter()


def neu(von, ref):
    if not ref or re.match(r'^(#|[a-z][a-z0-9+.-]*:|//)', ref, re.I):
        return None
    pfad, rest = re.match(r'^([^?#]*)(.*)$', ref).group(1, 2)
    if not pfad:
        return None
    ziel = posixpath.normpath(unquote(pfad).lstrip('/') if pfad.startswith('/') else posixpath.join(posixpath.dirname(von), unquote(pfad)))
    if ziel.endswith('/') or os.path.isdir(os.path.join(QUELLE, ziel)):
        ziel = ziel.rstrip('/') + '/index.html'
    ziel2 = umleiten.get(ziel, ziel)
    if ziel2 not in menge:
        if LINKS.get('website') and re.fullmatch(r'/?(\.\./)*[\w-]+\.html', pfad) and not os.path.exists(os.path.join(QUELLE, ziel)):
            return LINKS['website'].rstrip('/') + '/' + ziel.rsplit('/', 1)[-1] + rest
        if os.path.splitext(ziel)[1]:
            fehlend[ziel] += 1
        return None
    if ziel2 == ziel and not pfad.startswith('/'):
        return None
    return quote(posixpath.relpath(ziel2, posixpath.dirname(von) or '.'), safe='/-_.~') + rest


def eingebettet(von, ref):
    """url() in CSS-Variablen löst der Browser dort auf, wo die Variable benutzt wird: kleine Dateien deshalb als data:-Adresse."""
    import base64, mimetypes
    if re.match(r'^(data:|[a-z]+:|//)', ref, re.I):
        return None
    pfad = ref.split('?')[0].split('#')[0]
    ziel = posixpath.normpath(pfad.lstrip('/') if pfad.startswith('/') else posixpath.join(posixpath.dirname(von), unquote(pfad)))
    ziel = umleiten.get(ziel, ziel)
    p = os.path.join(QUELLE, ziel)
    if not os.path.isfile(p) or os.path.getsize(p) > 300e3:
        return None
    return 'data:' + (mimetypes.guess_type(p)[0] or 'application/octet-stream') + ';base64,' + base64.b64encode(open(p, 'rb').read()).decode()


def ersetze_attr(von, t):
    t = re.sub(r'--[\w-]+\s*:[^;{}]*url\([^;{}]*', lambda m: re.sub(r'url\((["\']?)([^)"\']+)\1\)', lambda u: 'url(' + u.group(1) + (eingebettet(von, u.group(2)) or u.group(2)) + u.group(1) + ')', m.group(0)), t)
    def eins(m):
        n = neu(von, m.group(3))
        return m.group(1) + m.group(2) + (n if n is not None else m.group(3)) + m.group(2)
    t = re.sub(r'(\s(?:src|href|data|poster|data-src|data-href|data-pdf|data-bild)=)(["\'])([^"\']*)\2', eins, t)

    def satz(m):
        teile = []
        for s in m.group(3).split(','):
            s = s.strip()
            if not s:
                continue
            u, _, w = s.partition(' ')
            n = neu(von, u)
            teile.append(((n if n is not None else u) + (' ' + w if w else '')))
        return m.group(1) + m.group(2) + ', '.join(teile) + m.group(2)
    t = re.sub(r'(\ssrcset=)(["\'])([^"\']*)\2', satz, t)
    t = re.sub(r'url\((["\']?)([^)"\']+)\1\)', lambda m: 'url(' + m.group(1) + (neu(von, m.group(2)) or m.group(2)) + m.group(1) + ')', t)
    return t


def ersetze_links(t):
    for port, url in LINKS.items():
        if port.isdigit():
            t = re.sub(r'https?://(?:127\.0\.0\.1|localhost):' + port + r'[^"\'\s<>)]*', url, t)
    return t


for w in behalten:
    p = os.path.join(AUS, w)
    if w.endswith(('.html', '.htm', '.css', '.js', '.json')):
        t = open(p, encoding='utf-8', errors='replace').read()
        if not w.endswith(('.js', '.json')):
            t = ersetze_attr(w, t)
        t = ersetze_links(t)
        if w.endswith(('.html', '.htm')):
            # Links zu Werkzeug-Demos (claude.ai) in neuem Fenster
            t = re.sub(r'<a\s([^>]*href="https://claude\.ai/[^"]*")(?![^>]*target=)', r'<a target="_blank" rel="noopener" \1', t)
        open(p, 'w', encoding='utf-8').write(t)

start = 'werkbank/index.html'
open(os.path.join(AUS, 'index.html'), 'w', encoding='utf-8').write(
    '<title>Werkbank Culinarium</title><style>:root{--bg:#130e0d;--fg:#f2e9dc;color-scheme:dark}body{background:var(--bg);color:var(--fg);font-family:Georgia,serif;min-height:100vh;display:grid;place-items:center;padding:40px 16px}a{color:#d8b264}</style>'
    f'<p><a href="{start}">Werkbank öffnen</a></p><script>try{{location.replace({json.dumps(start)})}}catch(e){{}}</script>')

n = sum(len(fs) for _, _, fs in os.walk(AUS))
gr = sum(os.path.getsize(os.path.join(d, x)) for d, _, fs in os.walk(AUS) for x in fs)
print(json.dumps({'dateien': n, 'mb': round(gr / 1e6, 1), 'umgeleitet': len(umleiten), 'fehlend': fehlend.most_common(40)}, ensure_ascii=False))
