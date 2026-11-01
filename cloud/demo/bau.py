#!/usr/bin/env python3
"""Baut aus einer Aufnahme (proxy.py) eine Demo ohne Server.
Aufruf: python3 bau.py <aufnahme-ordner> <start-weg> <ausgabe-ordner> [links.json]
start-weg z. B. _werkzeuge/maison/index.html"""
import sys, os, json, re, hashlib, shutil, posixpath

AUF, START, AUS = sys.argv[1], sys.argv[2].lstrip('/'), sys.argv[3]
LINKS = json.load(open(sys.argv[4])) if len(sys.argv) > 4 and os.path.exists(sys.argv[4]) else {}
HIER = os.path.dirname(os.path.abspath(__file__))
# Schlüssel, Passwörter, Zugänge: nie in eine Demo (Culinarium 1.11.: online/schluessel.txt)
GEHEIM = re.compile(r'schl(ue|ü)ssel|secret|token|passw|credential|zugang|\.env$|\.pem$|\.key$|api[-_]?key', re.I)
STATISCH = {'css', 'js', 'mjs', 'woff2', 'woff', 'ttf', 'otf', 'webp', 'jpg', 'jpeg', 'png', 'svg', 'gif', 'ico', 'pdf', 'mp4', 'webm', 'json', 'html', 'htm', 'txt', 'xml', 'wasm', 'map', 'avif', 'mp3', 'csv', 'md'}

def U(f):
    """Oberste Ordner mit «_» vorn sind im Artifact reserviert: «_werkzeuge» → «uwerkzeuge»."""
    return 'u' + f[1:] if f.startswith('_') else f


shutil.rmtree(AUS, ignore_errors=True)
os.makedirs(os.path.join(AUS, 'demo', 'd'), exist_ok=True)

karte, post, dateien = {}, {}, {}
for zeile in open(os.path.join(AUF, 'log.jsonl'), encoding='utf-8'):
    try:
        e = json.loads(zeile)
    except Exception:
        continue
    p = e['p'].lstrip('/')
    pn, _, q = p.partition('?')
    if e['m'] in ('GET', 'HEAD'):
        if e['st'] != 200 or e['m'] == 'HEAD':
            continue
        if pn == '' or pn.endswith('/'):
            pn += 'index.html'
        letzt = pn.rsplit('/', 1)[-1]
        ext = letzt.rsplit('.', 1)[-1].lower() if '.' in letzt else ''
        ct = e['ct'] or ''
        if ext in STATISCH and not (q and ext in ('json', 'html') and 'api/' in pn) and not ('json' in ct and ext != 'json'):
            f = U(pn)
        else:
            art = 'html' if 'html' in ct else 'json' if 'json' in ct else 'js' if 'javascript' in ct else 'css' if 'css' in ct else 'svg' if 'svg' in ct else \
                'webp' if 'webp' in ct else 'png' if 'png' in ct else 'jpg' if 'jpeg' in ct else 'pdf' if 'pdf' in ct else 'woff2' if 'woff2' in ct else 'txt'
            f = 'demo/d/' + hashlib.sha1(p.encode()).hexdigest()[:14] + '.' + art
        if GEHEIM.search(pn):
            continue
        dateien[f] = e['k']
        karte[p] = f
        if pn not in karte or not q:
            karte[pn] = f
    else:
        f = 'demo/d/' + hashlib.sha1((e['m'] + p + e['k']).encode()).hexdigest()[:14] + '.json'
        dateien[f] = e['k']
        post[e['m'] + ' ' + pn] = {'f': f, 'ct': e['ct'] or 'application/json', 'st': e['st']}

for f, k in dateien.items():
    ziel = os.path.join(AUS, f)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    shutil.copyfile(os.path.join(AUF, 'k', k), ziel)

# Zusatz: ganze Ordner von der Platte (Bilder, die die Aufnahme nicht erreicht hat). Arg 5: "ordner=webweg,ordner2=webweg2"
GRENZE = int(os.environ.get('DEMO_MAX_DATEIEN', '480'))
if len(sys.argv) > 5 and sys.argv[5]:
    for paar in sys.argv[5].split(','):
        ordner, _, web = paar.partition('=')
        for d, uds, fs in os.walk(ordner):
            uds[:] = [u for u in uds if not u.startswith(('_', '.')) and u not in ('pruefung', 'aufnahmen', 'sicherung', 'node_modules', 'lieferung', 'test')]
            for x in sorted(fs):
                if len(dateien) >= GRENZE:
                    break
                if x.endswith(('.py', '.pyc', '.md', '.sh', '.log', '.bak', '.ase')) or '.' not in x or GEHEIM.search(x) or '.vor-' in x or os.path.getsize(os.path.join(d, x)) > 8e6:
                    continue
                w = posixpath.join(web.strip('/'), os.path.relpath(os.path.join(d, x), ordner).replace(os.sep, '/'))
                f = U(w)
                if f in dateien:
                    continue
                ziel = os.path.join(AUS, f)
                os.makedirs(os.path.dirname(ziel), exist_ok=True)
                shutil.copyfile(os.path.join(d, x), ziel)
                dateien[f] = None
                karte.setdefault(w, f)

# Nachziehen: Anfragen, die der Server nicht beantwortet hat (403/404), aber auf der Platte liegen.
# Umgebung DEMO_NACHZIEHEN="webweg-anfang=ordner,…" z. B. "assets/schrift/=website/assets/schrift/"
for paar in filter(None, os.environ.get('DEMO_NACHZIEHEN', '').split(',')):
    vorn, _, ordner = paar.partition('=')
    for zeile in open(os.path.join(AUF, 'log.jsonl'), encoding='utf-8'):
        try:
            e = json.loads(zeile)
        except Exception:
            continue
        p = e['p'].lstrip('/')
        pn = p.partition('?')[0]
        if e['m'] != 'GET' or e['st'] < 400 or not pn.startswith(vorn) or pn in karte or GEHEIM.search(pn):
            continue
        quelle = os.path.join(ordner, pn[len(vorn):])
        if not os.path.isfile(quelle):
            continue
        f = U(pn)
        ziel = os.path.join(AUS, f)
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        shutil.copyfile(quelle, ziel)
        dateien[f] = None
        karte[pn] = f
        karte[p] = f

open(os.path.join(AUS, 'demo', 'ok.json'), 'w').write('{"ok":true,"demo":true}')
open(os.path.join(AUS, 'demo', 'karte.js'), 'w', encoding='utf-8').write(
    'window.__DEMO_KARTE=' + json.dumps(karte, ensure_ascii=False) + ';\nwindow.__DEMO_POST=' + json.dumps(post, ensure_ascii=False) +
    ';\nwindow.__DEMO_LINKS=' + json.dumps(LINKS) + ';\n')
shutil.copyfile(os.path.join(HIER, 'shim.js'), os.path.join(AUS, 'demo', 'shim.js'))


def rel(von, weg):
    """Weg «/x/y» relativ zur Datei «von» machen."""
    pfad, _, rest = weg.lstrip('/').partition('?')
    hash_ = ''
    if '#' in pfad:
        pfad, _, h = pfad.partition('#'); hash_ = '#' + h
    if pfad == '' or pfad.endswith('/'):
        pfad += 'index.html'
    f = karte.get(weg.lstrip('/')) or karte.get(pfad) or U(pfad)
    r = posixpath.relpath(f, posixpath.dirname(von) or '.')
    return r + hash_


def biege_html(von, t):
    t = re.sub(r'(\s(?:src|href|action|poster|data-src)=)(["\'])(/(?!/)[^"\']*)\2', lambda m: m.group(1) + m.group(2) + rel(von, m.group(3)) + m.group(2), t)
    t = re.sub(r'url\((["\']?)(/(?!/)[^)"\']+)\1\)', lambda m: 'url(' + m.group(1) + rel(von, m.group(2)) + m.group(1) + ')', t)
    for port, url in LINKS.items():
        t = re.sub(r'https?://(?:127\.0\.0\.1|localhost):' + port + r'[^"\'\s<>)]*', url, t)
    vor = posixpath.relpath('demo', posixpath.dirname(von) or '.')
    kopf = f'<script src="{vor}/karte.js"></script><script src="{vor}/shim.js"></script>'
    m = re.search(r'<head[^>]*>', t, re.I)
    if m:
        t = t[:m.end()] + kopf + t[m.end():]
    else:
        t = kopf + t
    return t


def eingebettet(weg):
    """Kleine Datei als data:-Adresse (url() in CSS-Variablen löst der Browser dort auf, wo die Variable benutzt wird)."""
    import base64, mimetypes
    pn = weg.lstrip('/').partition('?')[0].partition('#')[0]
    f = karte.get(pn) or U(pn)
    p = os.path.join(AUS, f)
    if not os.path.isfile(p) or os.path.getsize(p) > 300e3:
        return None
    return 'data:' + (mimetypes.guess_type(pn)[0] or 'application/octet-stream') + ';base64,' + base64.b64encode(open(p, 'rb').read()).decode()


def biege_css(von, t):
    t = re.sub(r'--[\w-]+\s*:[^;{}]*url\([^;{}]*', lambda m: re.sub(r'url\((["\']?)(/(?!/)[^)"\']+)\1\)', lambda u: 'url(' + u.group(1) + (eingebettet(u.group(2)) or rel(von, u.group(2))) + u.group(1) + ')', m.group(0)), t)
    t = re.sub(r'url\((["\']?)(/(?!/)[^)"\']+)\1\)', lambda m: 'url(' + m.group(1) + rel(von, m.group(2)) + m.group(1) + ')', t)
    t = re.sub(r'@import\s+(["\'])(/(?!/)[^"\']+)\1', lambda m: '@import ' + m.group(1) + rel(von, m.group(2)) + m.group(1), t)
    return t


for f in list(dateien):
    p = os.path.join(AUS, f)
    if f.endswith(('.html', '.htm')):
        t = open(p, encoding='utf-8', errors='replace').read()
        if '<' in t[:2000]:
            open(p, 'w', encoding='utf-8').write(biege_html(f, t))
    elif f.endswith('.css'):
        t = biege_css(f, open(p, encoding='utf-8', errors='replace').read())
        open(p, 'w', encoding='utf-8').write(t)

start = karte.get(START) or U(START)
titel = os.environ.get('DEMO_TITEL', '')
if not titel:
    try:
        m = re.search(r'<title>([^<]+)</title>', open(os.path.join(AUS, start), encoding='utf-8', errors='replace').read())
        titel = (m.group(1).split('·')[0].strip() + ' · Demo') if m else 'Demo'
    except Exception:
        titel = 'Demo'
open(os.path.join(AUS, 'index.html'), 'w', encoding='utf-8').write(
    '<title>' + titel + '</title><meta name="claude:viewport-fit-sides" content="cover">'
    '<style>:root{--bg:#130e0d;--fg:#f2e9dc;color-scheme:dark}body{background:var(--bg);color:var(--fg);font-family:Georgia,serif;min-height:100vh;display:grid;place-items:center;'
    'padding-block:40px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}a{color:#d8b264}</style>'
    f'<p><a href="{start}">Demo öffnen</a></p><script>try{{location.replace({json.dumps(start)})}}catch(e){{}}</script>')

n = sum(len(fs) for _, _, fs in os.walk(AUS))
gr = sum(os.path.getsize(os.path.join(d, x)) for d, _, fs in os.walk(AUS) for x in fs)
gross = [os.path.relpath(os.path.join(d, x), AUS) for d, _, fs in os.walk(AUS) for x in fs if os.path.getsize(os.path.join(d, x)) > 14.5e6]
print(json.dumps({'dateien': n, 'mb': round(gr / 1e6, 1), 'start': start, 'karte': len(karte), 'post': len(post), 'zu_gross': gross}))
