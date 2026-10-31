#!/usr/bin/env python3
"""Le Livre (Marke) · Culinarium Hannover: baut die Marke zum Arbeiten aus der Website und dem Markenbuch der Station 05 (Farbwelt A «Plakat»,
Robert 26.10.2026: «a»). Nachbau von Le Livre der Taverne zum Schäfli (jüngstes Vorbild, dort nur gelesen). Die Website wird nie angefasst und nie
importiert (Falle 9): gelesen werden BILD in website/bau.py (register.py, per ast), website/assets/bild/meta.json, website/assets/culinarium.css,
assets/zeichen/, assets/schrift/, _quelle/logo/original/ (Rudis Logo, 28.10.2026), _quelle/dirty-chicken/logo/original/, _quelle/**/herkunft.json,
_kette/05-markenbauer/marke.json und marke/. Geschrieben wird nur in diesen Ordner.

   python3 _werkzeuge/livre/bau.py   → livre.json, dateien/, original/, _quellen.json (nur lokal), listen/, beispiel/, buch.html, buch/, index.html

Farben = die Werte der Website heute (culinarium.css); jede wird dort gesucht, der Bau bricht ab, wenn eine fehlt. Herkunft je Foto: haus (Rudis
Dateien, Instagram von Culinarium, Rudi und Momo, Dirty Chicken), fremd (Instagram der Bar Walk on the Wild Side: die Bar gehört nicht zu Culinarium,
Freigabe offen), ki (mit KI verändert). Geschärfte Fotos (Chat culinarium-bilder, Pfad _quelle/ki/geschaerft/) zeigen «Vorher»: die Quelle aus
_register-vor-schaerfen.json (Stand des Registers vor dem Schärfen, 28.10.2026)."""
import base64, hashlib, html, io, json, os, re, shutil, struct, subprocess, sys, time, zipfile
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFile, ImageFont

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))              # …/Culinarium Hannover
ROOT = os.path.join(PROJEKT, 'website')                        # die Website, nur gelesen; ausgeliefert unter / (server.py)
PROJEKTE = os.path.dirname(PROJEKT)
QUELLE = os.path.join(PROJEKT, '_quelle')
MARKE = os.path.join(PROJEKT, '_kette', '05-markenbauer')
BILDER = os.path.join(ROOT, 'assets', 'bild')
CSS = os.path.join(ROOT, 'assets', 'culinarium.css')
FONTS = os.path.join(ROOT, 'assets', 'schrift')
ZEICHEN = os.path.join(ROOT, 'assets', 'zeichen')
LOGO = os.path.join(QUELLE, 'logo', 'original')
DC_LOGO = os.path.join(QUELLE, 'dirty-chicken', 'logo', 'original')
DAT = os.path.join(HIER, 'dateien')
ORIG = os.path.join(HIER, 'original')
e = html.escape
HAUS = 'Culinarium Hannover'
STAND = time.strftime('%d.%m.%Y')
SCHLUESSEL = 'culinarium-hannover'
MJ = json.load(open(os.path.join(MARKE, 'marke.json'), encoding='utf-8'))
NODE = dict(os.environ, NODE_PATH=os.path.expanduser('~/Aussen-Pruefung/node_modules'))
KLEID = os.path.join(PROJEKT, '_werkzeuge', 'oberflaeche', 'kleid', 'culinarium.js')
PLATZHALTER = {'zentrale': 'La Maison', 'website': 'Le Bureau', 'karten': 'La Carte', 'gaeste': 'La Réception', 'marke': 'Le Livre', 'besuche': 'Le Registre', 'druck': 'L’Imprimerie'}   # nur falls das Kleid fehlt; gilt ist kleid/culinarium.js
sys.path.insert(0, HIER)
import register  # noqa: E402


def namen_aus_kleid():
    """Sichtbare Namen der Werkzeuge: eine Stelle für alle, WO_HAUS.namen im gemeinsamen Kleid (gehört dem Chat culinarium-maison)."""
    if not os.path.exists(KLEID):
        print('Hinweis: Kleid fehlt noch, Arbeitsnamen als Platzhalter:', KLEID)
        return dict(PLATZHALTER)
    m = re.search(r'namen:\s*\{([^}]*)\}', open(KLEID, encoding='utf-8').read())
    if not m:
        return dict(PLATZHALTER)
    return dict(PLATZHALTER, **dict(re.findall(r"(\w+):\s*['\"]([^'\"]+)['\"]", m.group(1))))


NAMEN = namen_aus_kleid()
NAME = NAMEN['marke']


def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- Farben: so wie culinarium.css sie trägt (Farbwelt A «Plakat», Abendfarbe Orange)
# (Schlüssel, Name, Wert der Website, Rolle, Gruppe)
FARBEN = [
    ('nacht', 'Nacht', '#16151A', 'Grund der dunklen Flächen: die Bar bei Nacht', 'nacht'),
    ('nacht-tief', 'Nacht tief', '#0F0E13', 'die tiefste Fläche, unter Bildern und im Fuss', 'nacht'),
    ('strasse', 'Strasse', '#1C1B21', 'dunkle Fläche beim Ankommen, draussen kühl', 'nacht'),
    ('bar', 'Bar', '#222028', 'dunkle Fläche drinnen, einen Ton wärmer', 'nacht'),
    ('tafel', 'Tafel', '#26252E', 'dunkle Fläche an der Tafel im Kerzenlicht', 'nacht'),
    ('schiefer', 'Schiefer', '#3A3845', 'die Farbe der Wortmarke auf jedem Plakat: Schrift auf Warmweiss und Flächen', 'nacht'),
    ('weiss', 'Warmweiss', '#FAF4F4', 'Grund der hellen Flächen und Schrift auf Dunkel: das Band unter jedem Plakat', 'hell'),
    ('tinte', 'Tinte', '#2A2833', 'Lesetext auf Warmweiss, nie reines Schwarz', 'hell'),
    ('leise', 'Leise', '#5B5763', 'zweite Zeile auf Warmweiss', 'hell'),
    ('kerze', 'Kerze', '#EF7649', 'die Farbe des Abends: Schrägstrich in Rudis Zeilen, Knauf, Linien auf Dunkel', 'kerze'),
    ('kerze-hell', 'Kerze hell', '#F5A689', 'leise Betonung auf Dunkel', 'kerze'),
    ('kerze-tief', 'Kerze tief', '#B15736', 'Betonung auf Warmweiss, wo Kerze zu hell steht', 'kerze'),
    ('dc', 'Dirty-Chicken-Violett', '#8953A9', 'nur für Dirty Chicken, Rudis zweite Küche: Flächen und Tapete', 'dc'),
    ('dc-hell', 'Dirty-Chicken-Hell', '#FFF7EF', 'Schrift auf Violett', 'dc'),
]
GRUPPEN = [('nacht', 'Nacht und Schiefer', 'Die dunklen Flächen, so wie die Bar am Abend: draussen kühl, drinnen mit jedem Schritt wärmer. Schiefer ist die Farbe der Wortmarke.'),
           ('hell', 'Warmweiss', 'Das Warmweiss des Bandes, das unter jedem Plakat liegt. Darauf wird gelesen, in Tinte, nie in reinem Schwarz.'),
           ('kerze', 'Kerze', 'Das Licht des Abends: Orange vom Plakat im Februar 2025, nah am Licht im Flur der Bar. Es betont, es schreibt nie den Lesetext.'),
           ('dc', 'Dirty Chicken', 'Das Violett aus dem Logo von Dirty Chicken. Es gehört nur dorthin, nie zu den Abenden von Culinarium.'),
           ('abende', 'Die Farben der Abende', 'Jeder Abend hat sein Plakat und seine eigene Farbe. Gemessen an der Illustration, je Plakat ein Ton.')]


def css_text():
    return open(CSS, encoding='utf-8').read()


def farben_liste():
    s = css_text().upper(); aus = []
    for k, n, h, r, g in FARBEN:
        if h.upper() not in s:
            raise SystemExit(f'Farbe {n} {h} steht nicht in culinarium.css, erst klären')
        woher = 'Wert der Website (culinarium.css)'
        fa = next(w for w in MJ['farbwelten'] if w['kennung'] == 'a')
        if h.upper() in [x.upper() for x in list(fa['css'].values()) + fa['flaechen']]:
            woher = 'Farbwelt «Plakat» der Hausregeln, unverändert auf der Website'
        aus.append((k, n, h, r, g, woher))
    for a in MJ['abendfarben']:                                   # Plakat-Farben: gemessen an den Plakaten (Markenbuch), nicht auf der Website als Fläche
        aus.append(('abend-' + a['kennung'], a['name'], a['hex'], f'Plakat {a["plakat"]}, {a["motiv"]}', 'abende', f'gemessen am Plakat {a["plakat"]}'))
    return aus


# ---------------------------------------------------------------- Bildarchiv
REG, ABENDE = register.lesen()
META = json.load(open(os.path.join(BILDER, 'meta.json'), encoding='utf-8'))
VOR_SCHAERFEN = json.load(open(os.path.join(HIER, '_register-vor-schaerfen.json'), encoding='utf-8'))['quelle']
BEREICH = {
    'ort': ['fassade', 'schildnacht', 'barnacht', 'schildtag', 'ecke', 'flur', 'fensterdraussen', 'loch', 'schildnah', 'barlicht', 'barneg', 'flaschen', 'kanister', 'theke', 'theke2'],
    'tafel': ['tafelleer', 'toast', 'kerze1', 'kerze2', 'kerze3', 'anstossen', 'glaeser', 'lachen', 'karte', 'kartglas', 'service', 'rudi']
             + ['t%02d' % i for i in range(1, 15)],
    'teller': ['tarte', 'lauch', 'roq1', 'roq2', 'hok1', 'hok2', 'spag', 'beete', 'baiser', 'm4', 'm5'] + ['r%02d' % i for i in range(1, 12)],
    'drinks': ['momo', 'glas', 'tablett', 'g1', 'g2', 'g3', 'g4', 'g5', 'd1', 'd2', 'd3', 'klaeren', 'schaum', 'schaumglas', 'coupe', 'glasnacht', 'bar', 'm3', 'm7', 'beeteglas'],
    'pass': ['anrichten', 'm1', 'm2', 'm6', 'm8', 'kueche', 'pass', 'pass2', 'pass3', 'pass4', 'w7'],
    'team': ['trio', 'trio2', 'team_alle', 'kopf_momo', 'kopf_derya', 'kopf_rudi', 'momo_hoch', 'w1', 'w2', 'w3', 'w4', 'w5', 'w6'],
}
BEREICHE = ['ort', 'tafel', 'teller', 'drinks', 'pass', 'team', 'plakate', 'abende', 'dc', 'wildside']
B_VON = {k: b for b, ks in BEREICH.items() for k in ks}


def bereich(k):
    if k in B_VON:
        return B_VON[k]
    if k.startswith('ws'):
        return 'wildside'
    if k.startswith(('dc_', 'dn_')):
        return 'dc'
    if k.startswith('p_') or k in ('pop23', 'pl23', 'plakatwand'):
        return 'plakate'
    if k.startswith(('ab_', 'abr_')):
        return 'abende'
    return None


# Mit KI hochgerechnet (Vermerk im Register, website/bau.py Zeile «Hero Team»): Vorlage für «Vorher»
HOCHGERECHNET = {'team_alle': ('_quelle/dirty-chicken/ig/2026-06-03_dirtychicken.hannover_DZIjZWNCGZT-2.jpg',
                               'Mit KI auf 4K geschärft. Die KI verändert Gesichter leicht; für Druck und Werbung das Original beim Fotografen anfragen')}
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']


def datum(s):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', s or '')
    return f'{int(m.group(3))}. {MONATE[int(m.group(2)) - 1]} {m.group(1)}' if m else ''


def hk(rel):
    """Eintrag aus der herkunft.json im Ordner der Quelle (oder darüber); Schlüssel = Weg ab dem Ordner oder Dateiname."""
    p = os.path.join(PROJEKT, rel); d = os.path.dirname(p)
    while d.startswith(QUELLE):
        f = os.path.join(d, 'herkunft.json')
        if os.path.exists(f):
            try:
                j = json.load(open(f, encoding='utf-8'))
            except ValueError:
                j = {}
            for key in (os.path.relpath(p, d), os.path.basename(p)):
                if isinstance(j, dict) and isinstance(j.get(key), dict):
                    return j[key]
            if isinstance(j, dict) and isinstance(j.get('dateien'), dict) and isinstance(j['dateien'].get(os.path.basename(p)), dict):
                return j['dateien'][os.path.basename(p)]
        d = os.path.dirname(d)
    return {}


def beitrag(rel):
    """(Datum, Adresse) eines Instagram-Bildes aus dem Dateinamen JJJJ-MM-TT_konto_KENNUNG-n.jpg."""
    b = os.path.basename(rel)
    m = re.match(r'(\d{4}-\d{2}-\d{2})_[A-Za-z0-9_.]+?_([A-Za-z0-9_-]{9,12})-\d+\.\w+$', b)
    return (datum(m.group(1)), f'https://www.instagram.com/p/{m.group(2)}/') if m else (datum(b[:10]), '')


def herkunft(k, rel):
    """(art, Quelle als Satz, Adresse) für die Quelle rel (relativ zum Projektordner)."""
    h = hk(rel)
    if k in HOCHGERECHNET:
        d, u = beitrag(HOCHGERECHNET[k][0])
        return 'haus', f'Instagram von Dirty Chicken (@dirtychicken.hannover), Beitrag vom {d}. {HOCHGERECHNET[k][1]}', u
    if rel.startswith('_quelle/vom-kunden/'):
        return 'haus', 'Foto von Rudi, aus seinen Dateien für Culinarium (Oktober 2026)', ''
    if rel.startswith('website/_zuschnitt/plakatwand'):
        return 'haus', 'Alle Plakate von Culinarium, für die Website nebeneinander an eine dunkle Wand gesetzt (keine eigene Aufnahme)', ''
    if rel.startswith('website/_zuschnitt/'):
        return 'haus', 'Ausschnitt aus einem Foto von Rudi (das Team vor der Bar), für die Website zugeschnitten', ''
    if rel.startswith('_quelle/extern/ig/'):
        d, u = beitrag(rel)
        plakat = k.startswith('p_')
        return 'haus', f'Instagram von Culinarium (@culinarium_hannover), Beitrag vom {d}' , h.get('adresse') or u
    if rel.startswith(('_quelle/extern/ig-highlights/', '_quelle/extern/ig-zuschnitt-2/')):
        hh = hk('_quelle/extern/ig-highlights/' + os.path.basename(rel)) if 'zuschnitt' in rel else h
        d = datum(os.path.basename(rel))
        if '_culinarium_hannover_' in rel:
            dd, u = beitrag(rel)
            return 'haus', f'Instagram von Culinarium (@culinarium_hannover), Beitrag vom {dd}, für die Website ohne Schrift zugeschnitten', u
        return 'haus', f'Instagram von Culinarium, Story vom {d}' + (', für die Website ohne Namen und Schrift zugeschnitten' if 'zuschnitt' in rel else ''), hh.get('adresse', '')
    if rel.startswith('_quelle/extern/ig-team/'):
        d, u = beitrag(rel)
        wer = 'Rudi (@rudi__san)' if '_rudi__san_' in rel else 'Momo (@momo012027)' if '_momo012027_' in rel else 'dem Team'
        return 'haus', f'Instagram von {wer}, Beitrag vom {d}', u
    if rel.startswith('_quelle/dirty-chicken/vom-kunden'):
        return 'haus', 'Foto von Rudi für Dirty Chicken (27. Oktober 2026)', ''
    if rel.startswith('_quelle/dirty-chicken/logo/'):
        return 'haus', 'Logo von Dirty Chicken, Original von Rudi (28. Oktober 2026)', ''
    if rel.startswith('_quelle/dirty-chicken/ig/'):
        d, u = beitrag(rel)
        foto = ', Foto von @focusonbiz_hannover' if 'focusonbiz' in (h.get('text') or '') else ''
        return 'haus', f'Instagram von Dirty Chicken (@dirtychicken.hannover), Beitrag vom {d}{foto}', h.get('adresse') or u
    if rel.startswith('_quelle/walk-on-the-wild-side/'):
        d, u = beitrag(rel)
        return 'fremd', (f'Instagram der Bar Walk on the Wild Side (@walkonthewildside_hannover), Beitrag vom {d}. Die Bar ist der Ort der Abende, '
                         'gehört aber nicht zu Culinarium'), h.get('adresse') or u
    return 'fremd', 'offen: Herkunft nicht in den Unterlagen', ''


def geschaerft(rel):
    return '/ki/geschaerft/' in rel or '/hochgerechnet/' in rel


def dateien_von(k):
    """(gross, mittel, klein) in website/assets/bild als Weg von der Seite des Werkzeugs aus; klein die kleinste Stufe, mittel höchstens 1600."""
    st = META[k]['stufen']
    gr = max(st); kl = min(st); mi = max([b for b in st if b <= 1600] or [kl])
    if not os.path.exists(os.path.join(BILDER, f'{k}-{gr}.webp')):
        return None, None, None
    return (f'../../assets/bild/{k}-{gr}.webp', f'../../assets/bild/{k}-{mi}.webp', f'../../assets/bild/{k}-{kl}.webp')


def signatur(pfad):
    im = Image.open(pfad).convert('L').resize((17, 16), Image.LANCZOS)
    a = np.asarray(im, np.int16)
    return (a[:, 1:] > a[:, :-1]).flatten()


def katalog():
    aus, quellen, zusammen, gesehen = [], {}, {}, {}
    for k, (rel, _pos, alt) in REG.items():
        if k not in META:
            print('nicht auf der Website gebaut:', k); continue
        if rel in gesehen:                                         # Fehlerbuch 10a 19.10.2026: doppelte Einträge zusammenführen
            zusammen[k] = gesehen[rel]; continue
        gesehen[rel] = k
        fl, fm, fs = dateien_von(k)
        p = os.path.join(PROJEKT, rel)
        if not fl or not os.path.exists(p):
            print('nicht im Archiv:', k); continue
        vor = None
        if geschaerft(rel):
            vor = HOCHGERECHNET[k][0] if k in HOCHGERECHNET else VOR_SCHAERFEN.get(k)
            if vor == rel:
                vor = None
        art, q, u = herkunft(k, vor if (vor and k not in HOCHGERECHNET) else rel)
        if vor and k not in HOCHGERECHNET:
            q += '. Licht und Schärfe mit KI nachgeschärft'
        with Image.open(p) as im0:
            w, h = ImageOps.exif_transpose(im0).size
        f = 'hoch' if h > w * 1.04 else 'quer' if w > h * 1.04 else 'quadrat'
        b = bereich(k)
        if b is None:
            raise SystemExit(f'Foto {k} hat keinen Bereich, erst in BEREICH eintragen')
        aus.append(dict(k=k, t={'de': alt}, b=b, s='jahr', f=f, w=w, h=h, art=art, q=q, u=u, ue=bool(vor), alt=False, vn=False, fl=fl, fm=fm, fs=fs))
        quellen[k] = dict(druck=p, ausschnitt=None, original=os.path.join(PROJEKT, vor) if vor else None)
    # gleiche Fotos unter verschiedenen Quellen (Bildvergleich, Abstand der Signaturen unter 0,08): ein Eintrag
    sigs = {d['k']: signatur(os.path.join(ROOT, d['fs'][6:])) for d in aus}
    weg = set()
    for i, a in enumerate(aus):
        for b in aus[i + 1:]:
            if b['k'] in weg or a['k'] in weg:
                continue
            if np.mean(sigs[a['k']] != sigs[b['k']]) < .08 and a['art'] == b['art'] and a['f'] == b['f']:
                weg.add(b['k']); zusammen[b['k']] = a['k']
    aus = [d for d in aus if d['k'] not in weg]
    for d in aus:
        doppelt = [x for x, z in zusammen.items() if z == d['k']]
        if doppelt:
            d['q'] += '. Auf der Website auch unter ' + ', '.join(f'«{x}»' for x in doppelt)
    for x in weg:
        quellen.pop(x, None)
    return aus, quellen, zusammen


def originale(aus, quellen):
    """Das unveränderte Ausgangsbild der nachgeschärften Fotos, auf die Grösse der Website gerechnet (original/<k>.webp), gleicher Ausschnitt."""
    if os.path.isdir(ORIG):
        shutil.rmtree(ORIG)
    os.makedirs(ORIG)
    n = 0
    for d in aus:
        o = quellen[d['k']]['original']
        if not (d['ue'] and o and os.path.exists(o)):
            continue
        with Image.open(os.path.join(ROOT, d['fl'][6:])) as nach:
            groesse = nach.size
        im = ImageOps.exif_transpose(Image.open(o)).convert('RGB')
        w, h = im.size; z = groesse[0] / groesse[1]
        if abs(w / h - z) > .005:
            if w / h > z:
                nw = round(h * z); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
            else:
                nh = round(w / z); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im.resize(groesse, Image.LANCZOS).save(os.path.join(ORIG, d['k'] + '.webp'), 'WEBP', quality=80, method=5)
        d['vn'] = True
        n += 1
    return n


# ---------------------------------------------------------------- Zeichnen mit Chromium (SVG → PNG, unsichtbar, ein Lauf, eigener Prozess)
def svg_png(paare):
    """paare: [(svg, png, breite)]; jedes SVG in der gewünschten Breite auf durchsichtigem Grund (SVG als data:-Adresse, Falle 9)."""
    js = os.path.join(HIER, '_svg_png.js')
    open(js, 'w').write('''const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 1 });
  for (const [svg, png, w, h] of JSON.parse(process.argv[2])) {
    await p.setViewportSize({ width: w, height: h });
    const d = 'data:image/svg+xml;base64,' + require('fs').readFileSync(svg).toString('base64');
    await p.setContent(`<html><body style="margin:0;background:transparent"><img src="${d}" style="display:block;width:${w}px;height:${h}px"></body></html>`);
    await p.waitForFunction(() => document.images[0].complete && document.images[0].naturalWidth > 0);
    await p.screenshot({ path: png, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } }); }
  await b.close(); })();''')
    liste = []
    for svg, png, breite in paare:
        s = open(svg, encoding='utf-8').read()
        vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
        liste.append([svg, png, breite, round(breite * vb[3] / vb[2])])
    subprocess.run(['node', js, json.dumps(liste)], check=True, env=NODE, timeout=240, cwd=HIER)
    os.remove(js)


def logo_pfade():
    """Rudis Original (aus dem PDF gelöst, Pfade unverändert): Wortmarke, Zeile und ihre Rahmen."""
    s = open(os.path.join(LOGO, 'culinarium-logo-original.svg'), encoding='utf-8').read()
    d = {k: re.search(r'<path id="%s"[^>]* d="([^"]+)"' % k, s).group(1) for k in ('wm', 'zeile')}
    vb = {'wmz': re.search(r'viewBox="([^"]+)"', s).group(1), 'wm': re.search(r'data-wm="([^"]+)"', s).group(1), 'zeile': re.search(r'data-zeile="([^"]+)"', s).group(1)}
    farbe = re.search(r'<path id="wm" fill="(#[0-9A-Fa-f]{6})"', s).group(1)
    return d, vb, farbe


def ase(farben):
    def block(name, r, g, b):
        n = (name + '\0').encode('utf-16-be')
        body = struct.pack('>H', len(name) + 1) + n + b'RGB ' + struct.pack('>fff', r / 255, g / 255, b / 255) + struct.pack('>H', 2)
        return struct.pack('>HI', 1, len(body)) + body
    bl = b''.join(block(n, *rgb(h)) for n, h in farben)
    return b'ASEF' + struct.pack('>HHI', 1, 0, len(farben)) + bl


def wert(name):
    """Ein einfacher Textwert aus website/bau.py, gelesen ohne die Datei auszuführen."""
    import ast
    for n in ast.parse(open(os.path.join(ROOT, 'bau.py'), encoding='utf-8').read()).body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return ast.literal_eval(n.value)
    raise SystemExit(f'{name} fehlt in website/bau.py')


def zeile_rudi():
    import ast
    for n in ast.parse(open(os.path.join(ROOT, 'bau.py'), encoding='utf-8').read()).body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ZEILEN' for t in n.targets):
            return ' '.join(ast.literal_eval(n.value)[0][0])
    raise SystemExit('ZEILEN fehlt in website/bau.py')


SCHRIFTEN = [
    ('t', 'Fraunces', 'fraunces-soft.woff2', 'Titel und Rudis Zeilen', '340 für Titel, 300 für Rudis Zeilen in Versalien, weiche Enden (SOFT 100); nie fett, nie kursiv', zeile_rudi(), 300),
    ('e', 'Urbanist', 'urbanist.woff2', 'Etiketten und Knöpfe', '600 bis 700, Versalien, 0,12 em gesperrt', 'A UNiQUE EXPERiENCE', 700),
    ('s', 'Instrument Sans', 'instrument.woff2', 'Lesetext', '400, 17 px, Zeilenabstand 1,62', next(w for w in MJ['ton']['eigene_worte'] if w.startswith('Momo wird')) + '.', 400),
    ('m', 'DM Mono', 'dmmono.woff2', 'Zeiten, Daten, Preise', '400, Versalien, 13 px, 0,06 em gesperrt', 'Haasemannstraße 13 · 30449 Hannover', 400),
]
LIZENZ = {'Fraunces': 'OFL-fraunces.txt', 'Urbanist': 'OFL-urbanist.txt'}


def dateien(fa):
    if os.path.isdir(DAT):
        shutil.rmtree(DAT)
    os.makedirs(DAT)
    F = {k: h for k, n, h, r, g, w in fa}
    liste, render = [], []
    d, vb, farbe_orig = logo_pfade()
    # Rudis Logo: das Original unverändert (Farbe #383944 wie im PDF), dazu einfarbig in Schiefer und Warmweiss, wie das Markenbuch es erlaubt («Umgefärbt»: nur diese zwei). Einfarbiger Vektor: umfärben erlaubt
    # (Falle 9 Schäfli betrifft nur Logos mit farbigem Zeichen); jede Datei wird als Tafel angesehen (pruefung/dateien_pruef.py).
    def svg(name, box, pfad, farbe, titel):
        open(os.path.join(DAT, name), 'w', encoding='utf-8').write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}"><title>{e(titel)}</title><path fill="{farbe}" d="{pfad}"/></svg>\n')
    for gruppe, box, pfad, wort, breite in (('logo', vb['wmz'], d['wm'] + d['zeile'], 'Culinarium · A UNiQUE EXPERiENCE', 2400),
                                            ('wortmarke', vb['wm'], d['wm'], 'Culinarium', 2400),
                                            ('zeile', vb['zeile'], d['zeile'], 'A UNiQUE EXPERiENCE', 1800)):
        var = []
        farben = (('original', farbe_orig, 'hell'),) if gruppe == 'logo' else ()
        for k, farbe, grund in farben + (('schiefer', F['schiefer'], 'hell'), ('weiss', F['weiss'], 'dunkel')):
            s = f'{SCHLUESSEL}-{gruppe}-{k}.svg'; p = s[:-4] + '.png'
            svg(s, box, pfad, farbe, wort)
            render.append((os.path.join(DAT, s), os.path.join(DAT, p), breite))
            var.append(dict(k=k, grund=grund, dateien=[s, p]))
        if gruppe == 'logo':                                        # Rudis PDF dazu, Byte für Byte
            n = f'{SCHLUESSEL}-logo-original-rudi.pdf'
            shutil.copyfile(os.path.join(LOGO, 'culinarium-logo-original-rudi-2026-10-28.pdf'), os.path.join(DAT, n))
            var[0]['dateien'].append(n)
        liste.append(dict(k=gruppe, var=var))
    # Dirty Chicken: Rudis Originale (PNG aus dem PDF, Original-Pixel, und die PDF), nie umgefärbt, nie nachgezeichnet
    var = []
    for k, png, pdf in (('dc-logo', 'dirtychicken-logo-lila-1440.png', 'dirtychicken-logo-lila-original-rudi-2026-10-28.pdf'),
                        ('dc-d', 'dirtychicken-d-lila-original.png', 'dirtychicken-d-lila-original-rudi-2026-10-28.pdf')):
        n = f'{SCHLUESSEL}-{k}.png'; m = f'{SCHLUESSEL}-{k}.pdf'
        shutil.copyfile(os.path.join(DC_LOGO, png), os.path.join(DAT, n)); shutil.copyfile(os.path.join(DC_LOGO, pdf), os.path.join(DAT, m))
        var.append(dict(k=k, grund='dc' if k == 'dc-logo' else 'hell', dateien=[n, m], px=list(Image.open(os.path.join(DAT, n)).size)))   # das D ist violett auf durchsichtigem Grund
    liste.append(dict(k='dc', var=var))
    # Tapeten der Website: Gitter aus der doppelten Linie der Plakate, das C in jedem Feld, Ton in Ton; dazu die Tapete von Dirty Chicken
    var = []
    for k, grund, quelle, farbe in (('dunkel', 'dunkel', 'tapete-dunkel.svg', F['nacht']), ('hell', 'hell', 'tapete-hell.svg', F['weiss']), ('dc', 'dc', 'tapete-dc.svg', F['dc'])):
        s = f'{SCHLUESSEL}-tapete-{k}.svg'; p = s[:-4] + '.png'; w = s[:-4] + '.webp'
        shutil.copyfile(os.path.join(ZEICHEN, quelle), os.path.join(DAT, s))
        t_ = open(os.path.join(DAT, s), encoding='utf-8').read()   # Tor 3, 30.10.2026: das Zeichen des Hauses ist das C, das x an den Kreuzungen fällt weg
        open(os.path.join(DAT, s), 'w', encoding='utf-8').write(re.sub(r'<svg [^>]*viewBox="0 0 224 228"[^>]*>.*?</svg>', '', t_, flags=re.S))
        vbw = re.search(r'viewBox="([^"]+)"', open(os.path.join(DAT, s), encoding='utf-8').read()).group(1).split()
        render.append((os.path.join(DAT, s), os.path.join(DAT, p), int(float(vbw[2]))))
        var.append(dict(k=k, grund=grund, dateien=[p, s, w], farbe=farbe))
    liste.append(dict(k='tapete', var=var))
    # So zeigt sich Culinarium heute auf Instagram: das Profilbild, unverändert, zum Nachschlagen
    n = f'{SCHLUESSEL}-instagram-profilbild.jpg'
    shutil.copyfile(os.path.join(QUELLE, 'logo', 'culinarium-profilbild-1080.jpg'), os.path.join(DAT, n))
    liste.append(dict(k='website', var=[dict(k='heute', grund='hell', dateien=[n], px=list(Image.open(os.path.join(DAT, n)).size))]))
    svg_png(render)
    for g in liste:
        for v in g['var']:
            png = next((x for x in v['dateien'] if x.endswith('.png')), None)
            if png and 'px' not in v:
                v['px'] = list(Image.open(os.path.join(DAT, png)).size)
    for v in next(g for g in liste if g['k'] == 'tapete')['var']:
        Image.open(os.path.join(DAT, v['dateien'][0])).save(os.path.join(DAT, v['dateien'][2]), 'WEBP', lossless=True)
    # Farben als Datei: CSS, JSON und ASE
    css = ':root{\n' + ''.join(f'  --{k}:{h}; /* {n}: {r} */\n' for k, n, h, r, g, w in fa) + '}\n'
    open(os.path.join(DAT, f'{SCHLUESSEL}-farben.css'), 'w', encoding='utf-8').write(f'/* {HAUS} · Farben der Marke ({STAND}), Werte der Website und der Plakate */\n' + css)
    json.dump([dict(name=n, hex=h, rgb=list(rgb(h)), rolle=r, gruppe=g, woher=w) for k, n, h, r, g, w in fa], open(os.path.join(DAT, f'{SCHLUESSEL}-farben.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(DAT, f'{SCHLUESSEL}-farben.ase'), 'wb').write(ase([(n, h) for k, n, h, r, g, w in fa]))
    liste.append(dict(k='farben', var=[dict(k='alle', grund='hell', dateien=[f'{SCHLUESSEL}-farben.css', f'{SCHLUESSEL}-farben.json', f'{SCHLUESSEL}-farben.ase'])]))
    # Schriften: die Dateien der Website, dazu als ZIP mit TTF und Lizenz
    from fontTools.ttLib import TTFont
    with zipfile.ZipFile(os.path.join(DAT, f'{SCHLUESSEL}-schriften.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for s_ in SCHRIFTEN:
            z.write(os.path.join(FONTS, s_[2]), 'web/' + s_[2])
            f = TTFont(os.path.join(FONTS, s_[2])); f.flavor = None
            b = io.BytesIO(); f.save(b); z.writestr('programme/' + s_[2].replace('.woff2', '.ttf'), b.getvalue())
        for fam, l in LIZENZ.items():
            z.write(os.path.join(MARKE, 'marke', 'schriften', l), 'lizenz/' + l)
        z.writestr('LIESMICH.txt', f'''{HAUS} · Schriften der Marke ({STAND})

Fraunces mit weichen Enden (SOFT 100): Titel 340, Rudis Zeilen in Versalien 300. Nie fett, nie kursiv.
Urbanist 600 bis 700: Etiketten und Knöpfe in Versalien, 0,12 em gesperrt.
Instrument Sans 400: Lesetext, 17 px, Zeilenabstand 1,62.
DM Mono 400: Zeiten, Daten und Preise in Versalien.

Alle stehen unter der SIL Open Font License 1.1 (frei für Druck, Website und Programme, auch gewerblich; nicht als Schrift allein verkaufen).
web/        die Dateien der Website
programme/  dieselben Schriften als TTF zum Installieren
lizenz/     Lizenztexte
''')
    liste.append(dict(k='schriften', var=[dict(k='alle', grund='hell', dateien=[f'{SCHLUESSEL}-schriften.zip'])]))
    alle = sorted(n_ for n_ in os.listdir(DAT) if not n_.endswith('-marke.zip'))   # erst die Liste, dann das ZIP (sonst packt es sich selbst ein)
    with zipfile.ZipFile(os.path.join(DAT, f'{SCHLUESSEL}-marke.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for n_ in alle:
            z.write(os.path.join(DAT, n_), n_)
    return liste


# ---------------------------------------------------------------- Beispiel für die Markenprüfung
def beispiel(F):
    """Ein eigens gezeichneter Entwurf, wie ihn eine Agentur schicken könnte: ein guter Instagram-Beitrag mit einem Foto von Rudi und der Wortmarke,
    aber in einer fremden Schrift (Baskerville), mit Gold und reinem Schwarz statt Nacht und Kerze, und dem Wort «Sie». Geprüft mit der Prüfung selbst ohne
    Claude (LIVRE_KI=0); die Farben bleiben gemessen, Schrift, Zeichen, Bild und Ton bekommen Beispiel-Urteile zu genau diesem Entwurf, beschriftet."""
    os.environ['LIVRE_KI'] = '0'
    import livre as LV
    LV._livre.cache_clear()
    zb = os.path.join(HIER, 'beispiel')
    if os.path.isdir(zb):
        shutil.rmtree(zb)
    os.makedirs(zb)
    W, H = 1080, 1350
    GOLD, SCHWARZ = (0xC9, 0xA2, 0x4A), (0, 0, 0)
    im = Image.new('RGB', (W, H), SCHWARZ)
    k = 'anstossen'
    foto = Image.open(os.path.join(BILDER, f'{k}-{max(META[k]["stufen"])}.webp')).convert('RGB')
    sk = max(W / foto.width, 880 / foto.height); foto = foto.resize((round(foto.width * sk), round(foto.height * sk)), Image.LANCZOS)
    y0 = round((foto.height - 880) * .4)
    im.paste(foto.crop(((foto.width - W) // 2, y0, (foto.width - W) // 2 + W, y0 + 880)), (0, 0))
    dr = ImageDraw.Draw(im)
    try:
        titel = ImageFont.truetype('/System/Library/Fonts/Supplemental/Baskerville.ttc', 78)
        lese = ImageFont.truetype('/System/Library/Fonts/Supplemental/Baskerville.ttc', 34)
        knopf = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 26)
    except OSError:
        titel = lese = knopf = ImageFont.load_default()
    dr.text((72, 930), 'Ein Abend mit Momo x Rudi', font=titel, fill=(255, 255, 255))
    dr.text((72, 1046), 'Drei Gänge und fünf Drinks an einer Tafel.', font=lese, fill=(225, 225, 225))
    dr.text((72, 1092), 'Haasemannstraße 13 · Hannover-Linden', font=lese, fill=(225, 225, 225))
    dr.rectangle((72, 1190, 492, 1262), fill=GOLD)
    dr.text((104, 1212), 'SICHERN SIE IHREN PLATZ', font=knopf, fill=SCHWARZ)
    logo = Image.open(os.path.join(DAT, f'{SCHLUESSEL}-logo-weiss.png')).convert('RGBA'); logo.thumbnail((360, 120), Image.LANCZOS)
    dunkel = Image.new('RGBA', (W, 240), (0, 0, 0, 0)); dd = ImageDraw.Draw(dunkel)
    for i in range(240):
        dd.line((0, i, W, i), fill=(0, 0, 0, int(130 * (1 - i / 240))))
    im.paste(dunkel, (0, 0), dunkel); im.paste(logo, (64, 56), logo)
    im.save(os.path.join(zb, 'entwurf.png'), optimize=True)
    b = io.BytesIO(); im.save(b, 'PNG')
    j = LV.pruefen(dict(name='Beispiel-Entwurf «Ein Abend mit Momo x Rudi», Instagram-Beitrag', typ='image/png', daten='data:image/png;base64,' + base64.b64encode(b.getvalue()).decode(), sprache='de'))
    j['beispiel'] = True
    kk = j.setdefault('ki', {})
    farb = [x for x in kk.get('punkte', []) if x.get('bereich') == 'farben']
    for x in farb:
        x['text'] = x['text'].replace('Gemessen ohne KI: ', 'Gemessen: ')
    kk['punkte'] = farb + [
        dict(bereich='farben', urteil='achten', titel='Gold und reines Schwarz', text=f'Der Knopf trägt ein Gold, die Fläche reines Schwarz. Bei Culinarium tragen Nacht {F["nacht"]} und Schiefer {F["schiefer"]} die dunklen Flächen, betont wird mit Kerze {F["kerze"]}, der Farbe des Abends.'),
        dict(bereich='schrift', urteil='passt_nicht', titel='Titel in Baskerville', text='Der Titel steht in einer klassischen Antiqua. Culinarium setzt Titel in Fraunces mit weichen Enden, leicht, nie fett; Etiketten und Knöpfe in Urbanist, Versalien, gesperrt.'),
        dict(bereich='zeichen', urteil='passt', titel='Die Wortmarke steht richtig', text='Rudis Wortmarke mit der Zeile «A UNiQUE EXPERiENCE» steht in Warmweiss auf dunklem Grund, ungedreht und mit Luft rundherum.'),
        dict(bereich='bild', urteil='passt', titel='Das Foto zeigt einen Abend', text='Anstossen über der Tafel bei Kerzenlicht: ein Foto von Rudi aus dem Bildarchiv, genau das, was ein Gast an einem Abend erlebt.'),
        dict(bereich='ton', urteil='achten', titel='Du statt Sie', text='Culinarium spricht seine Gäste mit Du an, herzlich und knapp. «Sichern Sie Ihren Platz» klingt nach Verkauf; die Abende kündigen sich mit «nur 14 Plätze pro Abend» an.'),
    ]
    kk['gesamt'] = ('Ein guter Entwurf: Foto, Wortmarke und Satz passen zu einem Abend bei Culinarium. Schrift, Gold und Schwarz kommen nicht aus der Marke; '
                    'mit Fraunces, Nacht und Kerze wird daraus ein Beitrag, der aussieht wie die Website.')
    kk['ton'] = [dict(stelle='SICHERN SIE IHREN PLATZ', vorschlag='Platz anfragen')]
    j['probe'] = False
    json.dump(j, open(os.path.join(zb, 'pruefung.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    return j


# Bilder zu den Farbgruppen (Fehlerbuch 10a, 20.10.2026: ein Foto je Gruppe, nie wiederholt; Farbfeld ganz). Abendfarben: je Farbe ihr Plakat.
GRUPPE_BILD = {'nacht': ('buch/bilder/schild-nacht.jpg', 'Das Schild der Bar in der Nacht. Daraus kommen die dunklen Flächen.'),
               'hell': ('listen/farbe-hell.webp', 'So steht Warmweiss mit Tinte auf der Website.'),
               'kerze': ('buch/bilder/flur.jpg', 'Der Flur zur Bar im Licht der Hängelampe. So nah liegt Kerze am Licht des Hauses.'),
               'dc': ('listen/farbe-dc.webp', 'Das Logo von Dirty Chicken, Rudis Original. Daraus kommt das Violett.')}


def listen_bilder():
    z = os.path.join(HIER, 'listen')
    if os.path.isdir(z):
        shutil.rmtree(z)
    os.makedirs(z)
    seiten = [os.path.join(ROOT, n) for n in ('index.html', 'abend.html', 'abende.html', 'leute.html') if os.path.exists(os.path.join(ROOT, n))]
    r = subprocess.run(['node', os.path.join(HIER, 'listen_bilder.js'), z] + seiten, env=NODE, timeout=420, capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode:
        raise SystemExit('listen_bilder.js: ' + r.stderr[-600:])
    Image.open(os.path.join(DC_LOGO, 'dirtychicken-logo-lila-1440.png')).convert('RGB').save(os.path.join(z, 'farbe-dc.png'))
    for n in os.listdir(z):
        im = Image.open(os.path.join(z, n)).convert('RGB'); im.thumbnail((1200, 800), Image.LANCZOS)
        im.save(os.path.join(z, n[:-4] + '.webp'), 'WEBP', quality=84, method=5); os.remove(os.path.join(z, n))


def main():
    t0 = time.time()
    fa = farben_liste()
    F = {k: h for k, n, h, r, g, w in fa}
    aus, quellen, zusammen = katalog()
    n_orig = originale(aus, quellen)
    liste = dateien(fa)
    groessen = {f: os.path.getsize(os.path.join(DAT, f)) for f in sorted(os.listdir(DAT))}
    abend_bild = {'abend-' + a['kennung']: 'buch/bilder/' + os.path.basename(a['bild']) for a in MJ['abendfarben']}
    daten = dict(haus=HAUS, ort='Hannover-Linden', fotos=aus, dateien=liste,
                 farben=[dict(k=k, n=n, h=h.upper(), rgb=list(rgb(h)), r=r, g=g, woher=w, **({'b': abend_bild[k]} if k in abend_bild else {})) for k, n, h, r, g, w in fa],
                 gruppen=[dict(k=k, n=n, s=s) for k, n, s in GRUPPEN], glanz=[], groessen=groessen,
                 bereiche=[b for b in BEREICHE if any(f['b'] == b for f in aus)],
                 schriften=[dict(k=k, n=fam, d=d, r=r, e=ein, p=p, w=w) for k, fam, d, r, ein, p, w in SCHRIFTEN],
                 namen=NAMEN, zusammen=zusammen,
                 ton=dict(eigene_worte=MJ['ton']['eigene_worte'], nicht=MJ['ton']['nicht']),
                 stand=dict(fotos=len(aus), haus=sum(1 for x in aus if x['art'] == 'haus'), frei=sum(1 for x in aus if x['art'] == 'frei'),
                            ki=sum(1 for x in aus if x['art'] == 'ki'), fremd=sum(1 for x in aus if x['art'] == 'fremd'), partner=0,
                            ue=sum(1 for x in aus if x['ue']), vn=n_orig, original=sum(1 for v in quellen.values() if v['druck'] and os.path.exists(v['druck'])),
                            dateien=len(groessen), datum=STAND))
    json.dump(daten, open(os.path.join(HIER, 'livre.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump({k: dict(druck=v['druck'] and os.path.relpath(v['druck'], PROJEKTE), ausschnitt=v['ausschnitt'],
                       original=v['original'] and os.path.relpath(v['original'], PROJEKTE)) for k, v in quellen.items()},
              open(os.path.join(HIER, '_quellen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    import buch
    buch.aus_station5(os.path.join(MARKE, 'marke'), ROOT, daten)
    beispiel(F)
    listen_bilder()
    for g in daten['gruppen']:
        if g['k'] in GRUPPE_BILD:
            g['bild'], g['bild_t'] = GRUPPE_BILD[g['k']]
    for s_ in daten['schriften']:
        s_['bild'] = f'listen/schrift-{s_["k"]}.webp'
    for f_ in [*GRUPPE_BILD.values()] + [(x['bild'], '') for x in daten['schriften']] + [(b, '') for b in abend_bild.values()]:
        if not os.path.exists(os.path.join(HIER, f_[0])):
            raise SystemExit('Bild fehlt: ' + f_[0])
    json.dump(daten, open(os.path.join(HIER, 'livre.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    seite(F)
    st = daten['stand']
    print(f'livre.json: {len(aus)} Fotos ({st["haus"]} Haus, {st["ki"]} KI, {st["fremd"]} fremde Rechte, {st["ue"]} nachgeschärft, '
          f'{n_orig} mit Vorher, {st["original"]} mit Original) · {len(zusammen)} doppelte zusammengeführt · {len(groessen)} Dateien · {time.time() - t0:.0f} s')


def v_von(*namen):
    h = hashlib.sha1()
    for n in namen:
        p = os.path.join(HIER, n)
        h.update(open(p, 'rb').read() if os.path.exists(p) else b'-')
    return h.hexdigest()[:10]


def seite(F):
    v = v_von('livre.json'); vc = v_von('livre.css'); vj = v_von('livre.js')
    open(os.path.join(HIER, 'index.html'), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{NAME} · Culinarium Hannover</title>
<meta name="description" content="{NAME}, die Marke von Culinarium Hannover zum Arbeiten: Bildarchiv mit fertigen Grössen, Rudis Wortmarke, Dirty Chicken, Tapeten und Farben als Dateien, Markenprüfung für Entwürfe, Hausregeln.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['nacht']}">
<link rel="icon" href="/assets/oberflaeche/kleid/culinarium-zeichen.svg" type="image/svg+xml">
<script src="/assets/oberflaeche/kleid/culinarium.js?v={v_von('../oberflaeche/kleid/culinarium.js')}"></script>
<link rel="preload" href="../../assets/schrift/fraunces-soft.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../../assets/schrift/instrument.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../../assets/schrift/dmmono.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="livre.json?v={v}" as="fetch" crossorigin>
<link rel="stylesheet" href="/assets/oberflaeche/grund.css?v={v_von('../oberflaeche/grund.css')}">
<link rel="stylesheet" href="/assets/oberflaeche/rahmen-buehne.css?v={v_von('../oberflaeche/rahmen-buehne.css')}">
<link rel="stylesheet" href="/assets/oberflaeche/kleid/culinarium.css?v={v_von('../oberflaeche/kleid/culinarium.css')}">
<link rel="stylesheet" href="livre.css?v={vc}">
</head>
<body class="li wo-app">
<header class="wo-kopf" id="kopf"></header>
<aside class="wo-rand" id="rand" aria-label="{NAME}"></aside>
<main class="wo-raum" id="haupt"><div id="ansicht"></div></main>
<footer class="wo-leiste" id="leiste" aria-live="polite"></footer>
<div class="fenster" id="fenster" hidden></div>
<div class="meldung" id="meldung" aria-live="polite"></div>
<noscript><p class="li-noscript">{NAME} braucht JavaScript.</p></noscript>
<script src="start.js?v={v_von('start.js')}" data-v="{vj}"></script>
<script src="/assets/oberflaeche/oberflaeche.js?v={v_von('../oberflaeche/oberflaeche.js')}"></script>
<script src="livre.js?v={vj}"></script>
</body>
</html>
''')


if __name__ == '__main__':
    main()
