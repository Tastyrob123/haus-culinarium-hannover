#!/usr/bin/env python3
"""Le Livre · Culinarium Hannover · Prüfung der Dateien und Downloads ohne Browser (Master Werkzeug-Bau L02, L03, L04, L06, L10). Nur lesen,
schreibt nur pruefung/ergebnisse/. Vorlage: dateien_pruef.py der Taverne zum Schäfli (dort nur gelesen), Teil A neu für Culinarium (28.10.2026).
  A  jede Datei gegen ihre Quelle: Farben (livre.json, CSS, JSON, ASE) gegen website/assets/culinarium.css und die Abendfarben (marke.json); Schriften Byte für
     Byte die der Website, TTF lesbar, Lizenzen dabei; Wortmarke, Zeile, beides zusammen Pfad für Pfad Rudis Original (nur die Farbe gewechselt, nur Schiefer
     und Warmweiss), auch im Markenbuch; Rudis PDF, Dirty Chicken, Tapeten und das Profilbild Byte für Byte die Originale; jede PNG gefüllt in ihrer Farbe;
     ZIP = alle Einzeldateien.
  B  jedes Foto in allen vier Grössen (wie «Laden», ohne Server): Masse, JPEG, Name, Druck in der Grösse von Rudis Original, Ausschnitt wirkt; Herkunft.
  C  Probe-Antwort ohne Claude: Prüfung läuft durch, kein Schlüssel wird gelesen, keine Anfrage nach aussen.
   python3 _werkzeuge/livre/pruefung/dateien_pruef.py"""
import builtins, hashlib, io, json, os, re, struct, sys, time, zipfile
from PIL import Image, ImageOps
HIER = os.path.dirname(os.path.abspath(__file__))
LIV = os.path.dirname(HIER)
PROJ = os.path.dirname(os.path.dirname(LIV))
WEB = os.path.join(PROJ, 'website')
MARKE = os.path.join(PROJ, '_kette', '05-markenbauer')
sys.path.insert(0, LIV)
os.environ.pop('LIVRE_KI', None); os.environ.pop('ANTHROPIC_API_KEY', None)
import livre as LV  # noqa: E402
L = json.load(open(os.path.join(LIV, 'livre.json'), encoding='utf-8'))
Q = json.load(open(os.path.join(LIV, '_quellen.json'), encoding='utf-8'))
DAT = os.path.join(LIV, 'dateien')
S_ = 'culinarium-hannover-'
erg = []
def z(nr, t, ok, m=''): erg.append(dict(nr=nr, t=t, ok=bool(ok), m=str(m)[:400])); print(('✓' if ok else '✗'), nr, t, '·', str(m)[:220])
sha = lambda p: hashlib.sha1(open(p, 'rb').read()).hexdigest()
rgb = lambda h: tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))

# ---------------------------------------------------------------- A Farben
css = open(os.path.join(WEB, 'assets', 'culinarium.css'), encoding='utf-8').read().upper()
MJ = json.load(open(os.path.join(MARKE, 'marke.json'), encoding='utf-8'))
abend = {'abend-' + x['kennung']: x['hex'].upper() for x in MJ['abendfarben']}
p = []
for f in L['farben']:
    if f['g'] == 'abende':
        if abend.get(f['k']) != f['h']: p.append(f"Abendfarbe {f['k']} {f['h']} ≠ marke.json {abend.get(f['k'])}")
    elif f['h'] not in css: p.append(f"{f['n']} {f['h']} nicht in culinarium.css")
    if tuple(f['rgb']) != rgb(f['h']): p.append('RGB ' + f['k'])
cssd = open(os.path.join(DAT, S_ + 'farben.css'), encoding='utf-8').read().lower()
jsond = json.load(open(os.path.join(DAT, S_ + 'farben.json'), encoding='utf-8'))
ase = open(os.path.join(DAT, S_ + 'farben.ase'), 'rb').read()
p += ['CSS ohne ' + f['k'] for f in L['farben'] if f"--{f['k']}:{f['h'].lower()}" not in cssd]
if [x['hex'].upper() for x in jsond] != [f['h'] for f in L['farben']]: p.append('JSON weicht ab')
i, gelesen = 12, []
while i < len(ase):
    typ, laenge = struct.unpack('>HI', ase[i:i + 6]); body = ase[i + 6:i + 6 + laenge]; i += 6 + laenge
    nl = struct.unpack('>H', body[:2])[0]; r, g, b = struct.unpack('>fff', body[2 + nl * 2 + 4:2 + nl * 2 + 16])
    gelesen.append('#%02X%02X%02X' % (round(r * 255), round(g * 255), round(b * 255)))
if gelesen != [f['h'] for f in L['farben']]: p.append('ASE weicht ab')
z('A1', f"{len(L['farben'])} Farben = culinarium.css bzw. Plakate (marke.json); CSS, JSON, ASE gleich", not p, '; '.join(p) or ' '.join(f['h'] for f in L['farben']))
# ---------------------------------------------------------------- A Schriften
from fontTools.ttLib import TTFont
p = []
with zipfile.ZipFile(os.path.join(DAT, S_ + 'schriften.zip')) as zf:
    for s_ in L['schriften']:
        if zf.read('web/' + s_['d']) != open(os.path.join(WEB, 'assets', 'schrift', s_['d']), 'rb').read(): p.append('ungleich ' + s_['d'])
        t = TTFont(io.BytesIO(zf.read('programme/' + s_['d'].replace('.woff2', '.ttf'))))
        if s_['n'].split()[0].lower() not in t['name'].getDebugName(1).lower(): p.append('TTF-Name ' + t['name'].getDebugName(1))
        if s_['d'] not in css.lower(): p.append('nicht in culinarium.css ' + s_['d'])
    for l in ('lizenz/OFL-fraunces.txt', 'lizenz/OFL-urbanist.txt'):
        if l not in zf.namelist(): p.append('fehlt ' + l)
z('A2', 'Schriften Byte für Byte die der Website, TTF lesbar, Lizenzen dabei', not p, '; '.join(p) or ', '.join(s_['n'] for s_ in L['schriften']))
# ---------------------------------------------------------------- A Wortmarke: Rudis Original, Pfad für Pfad
og = open(os.path.join(PROJ, '_quelle', 'logo', 'original', 'culinarium-logo-original.svg'), encoding='utf-8').read()
WM = re.search(r'<path id="wm"[^>]* d="([^"]+)"', og).group(1); ZL = re.search(r'<path id="zeile"[^>]* d="([^"]+)"', og).group(1)
SOLL = {'logo': WM + ZL, 'wortmarke': WM, 'zeile': ZL}
FARBE = {'original': '#383944', 'schiefer': '#3A3845', 'weiss': '#FAF4F4'}
D = {g['k']: g for g in L['dateien']}
p = []
for g in ('logo', 'wortmarke', 'zeile'):
    for v in D[g]['var']:
        t = open(os.path.join(DAT, v['dateien'][0]), encoding='utf-8').read()
        m = re.search(r'<path fill="(#[0-9A-Fa-f]{6})" d="([^"]+)"', t)
        if not m or m.group(2) != SOLL[g]: p.append(f'{g}-{v["k"]} Pfad ≠ Original')
        if not m or m.group(1).upper() != FARBE.get(v['k'], '?'): p.append(f'{g}-{v["k"]} Farbe {m and m.group(1)}')
bz = os.path.join(LIV, 'buch', 'zeichen')
for n in os.listdir(bz):
    mm = re.match(r'(wortmarke-mit-zeile|wortmarke|zeile)(-[a-z]+)?\.svg$', n)
    if mm:
        pf = re.search(r' d="([^"]+)"', open(os.path.join(bz, n), encoding='utf-8').read()).group(1)
        if pf != SOLL[{'wortmarke-mit-zeile': 'logo', 'wortmarke': 'wortmarke', 'zeile': 'zeile'}[mm.group(1)]]: p.append('Markenbuch ' + n)
buch = open(os.path.join(LIV, 'buch.html'), encoding='utf-8').read()
for k, soll in (('wortmarke', WM), ('zeile', ZL), ('marke', WM + ZL)):
    m = re.search(r'<symbol id="%s" viewBox="[^"]+"><path d="([^"]+)"/></symbol>' % k, buch)
    if not m or m.group(1) != soll: p.append('Markenbuch Symbol ' + k)
z('A3', 'Wortmarke, Zeile und beides zusammen Pfad für Pfad Rudis Original, nur in Original, Schiefer, Warmweiss; ebenso im Markenbuch', not p, '; '.join(p))
# ---------------------------------------------------------------- A Originale Byte für Byte
OQ = os.path.join(PROJ, '_quelle')
paare = [(S_ + 'logo-original-rudi.pdf', os.path.join(OQ, 'logo', 'original', 'culinarium-logo-original-rudi-2026-10-28.pdf')),
         (S_ + 'dc-logo.png', os.path.join(OQ, 'dirty-chicken', 'logo', 'original', 'dirtychicken-logo-lila-1440.png')),
         (S_ + 'dc-logo.pdf', os.path.join(OQ, 'dirty-chicken', 'logo', 'original', 'dirtychicken-logo-lila-original-rudi-2026-10-28.pdf')),
         (S_ + 'dc-d.png', os.path.join(OQ, 'dirty-chicken', 'logo', 'original', 'dirtychicken-d-lila-original.png')),
         (S_ + 'dc-d.pdf', os.path.join(OQ, 'dirty-chicken', 'logo', 'original', 'dirtychicken-d-lila-original-rudi-2026-10-28.pdf')),
         (S_ + 'instagram-profilbild.jpg', os.path.join(OQ, 'logo', 'culinarium-profilbild-1080.jpg')),
         (S_ + 'tapete-dunkel.svg', os.path.join(WEB, 'assets', 'zeichen', 'tapete-dunkel.svg')),
         (S_ + 'tapete-hell.svg', os.path.join(WEB, 'assets', 'zeichen', 'tapete-hell.svg')),
         (S_ + 'tapete-dc.svg', os.path.join(WEB, 'assets', 'zeichen', 'tapete-dc.svg'))]
p = [a for a, b in paare if sha(os.path.join(DAT, a)) != sha(b)]
z('A4', 'Rudis PDF, Dirty Chicken (Logo und D), Profilbild und Tapeten Byte für Byte die Originale (nie umgefärbt)', not p, '; '.join(p) or f'{len(paare)} Dateien')
# ---------------------------------------------------------------- A PNG gefüllt, in ihrer Farbe
p = []
for g in ('logo', 'wortmarke', 'zeile'):
    for v in D[g]['var']:
        im = Image.open(os.path.join(DAT, v['dateien'][1])).convert('RGBA')
        px = [q[:3] for q in im.getdata() if q[3] > 250]
        if len(px) < 1000: p.append(f'{g}-{v["k"]} fast leer'); continue
        soll = rgb(FARBE[v['k']]); mitte = tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3))
        if max(abs(a - b) for a, b in zip(mitte, soll)) > 3: p.append(f'{g}-{v["k"]} Farbe {mitte} ≠ {soll}')
z('A6', 'Jede PNG der Wortmarke gefüllt, deckende Bildpunkte in der angegebenen Farbe', not p, '; '.join(p))
with zipfile.ZipFile(os.path.join(DAT, S_ + 'marke.zip')) as zf:
    fehlt = sorted(set(os.listdir(DAT)) - {S_ + 'marke.zip'} - set(zf.namelist()))
    anders = [n for n in zf.namelist() if hashlib.sha1(zf.read(n)).hexdigest() != sha(os.path.join(DAT, n))]
z('A7', 'ZIP «Alle Dateien» = alle Einzeldateien, Byte für Byte', not fehlt and not anders, ' '.join(fehlt + anders) or f'{len(os.listdir(DAT)) - 1} Dateien')

# ---------------------------------------------------------------- B Fotos in vier Grössen
t0 = time.time(); p = []
for f in L['fotos']:
    for g in ('instagram', 'story', 'web', 'druck'):
        try:
            d, typ, name = LV.bild(f['k'], g, .5, .5)
        except Exception as e:  # noqa: BLE001
            p.append(f"{f['k']} {g}: {e}"); continue
        im = Image.open(io.BytesIO(d))
        if im.format != 'JPEG' or typ != 'image/jpeg' or not name.startswith(S_): p.append(f"{f['k']} {g} Format/Name {name}"); continue
        if ('-mit-ki-veraendert-' in name) != (f['art'] == 'ki'): p.append(f"{f['k']} KI-Kennzeichen")
        if g == 'instagram' and im.size != (1080, 1350): p.append(f"{f['k']} instagram {im.size}")
        if g == 'story' and im.size != (1080, 1920): p.append(f"{f['k']} story {im.size}")
        if g == 'web' and max(im.size) > 2000: p.append(f"{f['k']} web {im.size}")
        if g == 'druck':
            q = Q[f['k']]; o = ImageOps.exif_transpose(Image.open(os.path.join(os.path.dirname(PROJ), q['druck'])))
            w, h = o.size
            if q['ausschnitt']:
                a = q['ausschnitt']; w, h = int(a[2] * w) - int(a[0] * w), int(a[3] * h) - int(a[1] * h)
            if abs(im.size[0] - w) > 2 or abs(im.size[1] - h) > 2 or 'websitegroesse' in name: p.append(f"{f['k']} druck {im.size} ≠ {w}×{h}")
z('B1', f"Alle {len(L['fotos'])} Fotos in vier Grössen: Masse, JPEG, Name, KI-Kennzeichen, Druck = Original (mit Ausschnitt)", not p, '; '.join(p[:8]) or f'{len(L["fotos"]) * 4} Dateien in {time.time() - t0:.0f} s')
a, _, _ = LV.bild('pass4', 'instagram', 0, 0); b, _, _ = LV.bild('pass4', 'instagram', 1, 1)
z('B2', 'Ausschnitt wirkt (links/rechts verschieden)', a != b)
fremd = [f['k'] for f in L['fotos'] if f['art'] == 'fremd' or f['q'].startswith('offen')]
z('B3', 'Herkunft: jedes Foto mit Satz, nichts «offen»; fremde Rechte genau die Fotos der Bar Walk on the Wild Side', all(f['q'] for f in L['fotos']) and not any(f['q'].startswith('offen') for f in L['fotos'])
  and all(k.startswith('ws') for k in fremd) and all(f['art'] == 'fremd' for f in L['fotos'] if f['k'].startswith('ws')), f"{len(fremd)} fremd (Bar), {sum(1 for f in L['fotos'] if f['art'] == 'haus')} von Culinarium")
z('B4', 'Vorher-Bilder: eines je nachgeschärftem Foto, gleiche Grösse wie das Foto der Website',
  all(os.path.exists(os.path.join(LIV, 'original', f['k'] + '.webp')) and Image.open(os.path.join(LIV, 'original', f['k'] + '.webp')).size == Image.open(os.path.join(WEB, f['fl'][6:])).size
      for f in L['fotos'] if f['vn']), f"{sum(1 for f in L['fotos'] if f['vn'])} mit Vorher")

# ---------------------------------------------------------------- C Probe ohne Claude
gelesen, raus = [], []
_open = builtins.open
def wache_open(f, *a, **k):
    if 'API Key' in str(f): gelesen.append(str(f))
    return _open(f, *a, **k)
import urllib.request as UR
_url = UR.urlopen
UR.urlopen = lambda *a, **k: raus.append(a) or (_ for _ in ()).throw(OSError('gesperrt'))
builtins.open = wache_open
try:
    import base64
    d = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(LIV, 'beispiel', 'entwurf.png'), 'rb').read()).decode()
    j = LV.pruefen(dict(name='probe.png', typ='image/png', daten=d, sprache='de'))
finally:
    builtins.open = _open; UR.urlopen = _url
z('C1', 'Probe ohne Claude: läuft durch, Farben gemessen, als Probe beschriftet, kein Schlüssel gelesen, keine Anfrage nach aussen',
  j.get('probe') and j['messung']['toene'] and not gelesen and not raus and all('Probe' in x['titel'] or x['bereich'] == 'farben' for x in j['ki']['punkte']), f"{len(j['messung']['toene'])} Töne")

fs = sum(1 for e in erg if not e['ok'])
os.makedirs(os.path.join(HIER, 'ergebnisse'), exist_ok=True)
json.dump(erg, open(os.path.join(HIER, 'ergebnisse', 'dateien.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{len(erg) - fs} von {len(erg)} ok')
