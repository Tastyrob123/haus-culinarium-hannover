#!/usr/bin/env python3
"""L’Imprimerie · Culinarium Hannover: legt die Marke des Hauses für das Studio an (nichts abgetippt, alles aus dem Projekt gelesen).
   python3 bau.py   → haeuser/culinarium/ (marke.json, schriften, tapete, bilder, mini, kopf, mail) + api/_daten/culinarium.json
                      (das Wissen dazu baut _qa/wissen_bau.py → api/_daten/culinarium-wissen.txt)
Quellen (alle im Projekt des Hauses, nur gelesen):
  Farben      website/assets/culinarium.css :root und [data-ton] (Farbwelt A «Plakat», Robert 26.10.2026 «a»): Nacht, Strasse, Schiefer als dunkle Flächen,
              Warmweiss der Plakate als helle, Kerze als Licht, Linie und kleine Zeilen. Dieselben Werte wie Website und Werkzeug-Oberfläche (kleid/culinarium.css).
  Schriften   website/assets/schrift/*.woff2 (wie verbaut): Fraunces mit weichen Enden (SOFT 100) für Titel, Urbanist 600 für die Zeilen der Plakate
              («A UNiQUE EXPERiENCE BY MOMO X RUDI», wie .tb-t-zeile/.fk-zeile der Website), Instrument Sans für Lesetext, DM Mono für Zahlen und Daten.
              Aus den variablen Schriften je benutzte Stärke als feste TrueType-Schnitte (fontTools), damit PDF und Bildschirm dieselbe Schrift tragen
              und das PDF keine Type-3-Schriften enthält (Fehlerbuch 10a, La Carte Schäfli 21.10.2026). Nie fett, nie kursiv; Urbanist 600 nur in Plakatzeilen.
  Zeichen     das «C» der Wortmarke (_werkzeuge/oberflaeche/kleid/culinarium-zeichen.svg, Chat «culinarium-maison», aus dem Vektor der Website), Pfade unverändert.
  Wortmarke   Rudis Original-Logo (_quelle/logo/original/culinarium-logo-original.svg, Pfad #wm, 28.10.2026) als zweites Zeichen (el.z = 2), Farbe Schiefer
              wie auf den Plakaten. Nur für die Plakate je Abend und Stücke, die die ganze Wortmarke tragen.
  Tapete      website/assets/zeichen/tapete-dunkel.svg und tapete-hell.svg: feines Raster mit dem «C», Ton in Ton
  Fotos       website/assets/bild/<key>-<grösste Breite>.webp, Beschreibung aus dem Bildregister BILD in website/bau.py (als Daten gelesen, nie importiert:
              der Import baut die Website). Die geschärften Fassungen des Chats «culinarium-bilder» kommen über dieses Register nach. Nie: Plakate fremder
              Abende der Bar (Session, Silvester-Frühshoppen …), das Logo von Dirty Chicken als Foto, die zusammengesetzte Plakatwand.
  Plakate     je Abend aus bau.ABENDE die Illustration der Vorderseite, aus dem Instagram-Bild des Plakats ausgeschnitten (_quelle/extern/ig/<datum>_<ID>-1.jpg,
              Bildfeld innerhalb des warmweissen Rands, oberhalb des Kastens mit der Wortmarke). Akzentfarbe je Abend wie die Website (website/bau.py akzent()).
Die Schlüssel der Farben (navy, papier, creme, weiss, gold, taupe, messing …) sind die Rollen, die der Kern des Studios kennt; die Werte und Namen sind
die des Culinarium (navy = Nacht, blau = Schiefer, gold = Kerze hell, messing = Kerze, taupe = Kerze tief, tanne = Schiefer als Titel auf Hell)."""
import ast, glob, json, os, re, shutil, subprocess, sys
from PIL import Image, ImageOps
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '_qa'))
import kopfzone   # Kopfzonen-Prüfung der Plakat-Motive (Gegenstände unter der Kopfzeile, Kontrast 4,5:1)

Image.MAX_IMAGE_PIXELS = None
HIER = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HIER))          # Culinarium Hannover
WEB = os.path.join(PROJ, 'website')
Z = os.path.join(HIER, 'haeuser', 'culinarium')

ROLLEN = ['Eigene Fotos', 'Plakat-Motive', 'Plakate', 'Der Abend & die Tafel', 'Teller & Küche', 'Drinks & Bar', 'Die Leute', 'Linden & das Haus', 'Dirty Chicken']


def gruppe(key):
    k = key
    if k.startswith(('pl_', 'p_')) or k in ('pop23', 'pl23'):
        return 'Plakate'
    if k.startswith(('dc_', 'dn_')):
        return 'Dirty Chicken'
    if k in ('schildnacht', 'barnacht', 'schildtag', 'ecke', 'fassade', 'flur', 'barlicht', 'schildnah', 'fensterdraussen', 'loch'):
        return 'Linden & das Haus'
    if k in ('momo', 'rudi', 'trio', 'trio2', 'team_alle', 'kopf_momo', 'kopf_derya', 'kopf_rudi', 'momo_hoch', 'kueche', 'service') or re.fullmatch(r'w\d', k):
        return 'Die Leute'
    if k in ('glas', 'tablett', 'kerze1', 'theke', 'theke2', 'bar', 'klaeren', 'glaeser', 'beeteglas', 'kanister', 'schaum', 'schaumglas', 'glasnacht', 'flaschen',
             'barneg', 'lachen', 'm3', 'm7') or re.fullmatch(r'(g|d)\d', k) or k.startswith('ws'):
        return 'Drinks & Bar'
    if k in ('tafelleer', 'toast', 'kerze2', 'kerze3', 'anstossen', 'karte', 'kartglas') or re.fullmatch(r't\d\d', k):
        return 'Der Abend & die Tafel'
    return 'Teller & Küche'


# Fotos, die die Drucksachen nicht zeigen dürfen (Grund steht dabei)
RAUS = {
    'plakatwand': 'zusammengesetzte Wand aus allen Plakaten (Website), kein Foto',
    'dc_zeichen': 'Logo von Dirty Chicken, kein Foto',
    'ws43': 'Abend «Wild Side x Rudi in Love», nicht Culinarium', 'ws44': 'Karte eines anderen Abends der Bar', 'ws45': 'Karte eines anderen Abends der Bar',
}
# Plakate anderer Abende der Bar (Session Sip & Sounds, Silvester-Frühshoppen, Tanz in den Mai …) gehören nicht in die Drucksachen des Culinarium
PLAKAT_BAR = re.compile(r'^Plakat (?!Culinarium)')
# Ansichten des Studios: Foto im Kopf (1200 px, haeuser/culinarium/kopf/), siehe buehne.js FOTO
KOPF = ['fassade', 'barnacht', 'tafelleer', 'anstossen', 'kerze2', 'pass', 'kueche', 'lauch', 'glas', 'theke', 'trio2', 'schildnacht', 'kartglas', 'loch', 'klaeren', 'flur', 'barneg']
ERSATZ = 'fassade'


def website_daten():
    """BILD, ABENDE, ZEILEN aus website/bau.py als Daten (ast), ohne den Bau der Website auszulösen (Master Abschnitt 9)."""
    src = open(os.path.join(WEB, 'bau.py'), encoding='utf-8').read()
    env = {'os': os}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and all(isinstance(x, ast.Name) for x in n.targets) and n.targets[0].id in ('V', 'D', 'IG', 'DC', 'WS', 'VERSION', 'BILD', 'ABENDE', 'ZEILEN'):
            exec(compile(ast.Module([n], []), 'bau.py', 'exec'), env)
    return env


def akzent(datei):
    """Akzentfarbe eines Plakats, gleiches Verfahren wie website/bau.py akzent(): gesättigtster häufiger Ton der Illustration."""
    im = Image.open(datei).convert('RGB')
    w, h = im.size
    x = im.crop((int(w * .06), int(h * .06), int(w * .94), int(h * .68))).resize((120, 120))
    q = x.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:24]
    best, bs = (58, 56, 69), -1
    for n, i in sorted(q.getcolors(), reverse=True):
        r, g, b = pal[i * 3:i * 3 + 3]
        mx, mn = max(r, g, b), min(r, g, b)
        sc = (mx - mn) / (mx or 1) * (n ** .5) * (1 if 50 < mx < 245 else .3)
        if sc > bs:
            bs, best = sc, (r, g, b)
    return '#%02x%02x%02x' % best


def akzent_motiv(datei, ersatz='#ef7649'):
    """Akzentfarbe eines Motivs für Linie und Zeile des Plakats: kräftigster Ton, der auf Nacht und auf Warmweiss trägt (nicht zu dunkel, nicht zu hell)."""
    im = Image.open(datei).convert('RGB').resize((160, 120))
    q = im.quantize(colors=12, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:36]
    best, bs = None, -1
    for n, i in q.getcolors():
        r, g, b = pal[i * 3:i * 3 + 3]
        mx, mn = max(r, g, b), min(r, g, b)
        sat = (mx - mn) / (mx or 1)
        if mx < 120 or mx > 248 or sat < .35:
            continue
        sc = sat * (n ** .5)
        if sc > bs:
            bs, best = sc, (r, g, b)
    return '#%02x%02x%02x' % best if best else ersatz


def helligkeit(datei):
    """Mittlere Helligkeit (0–1) oben (Zeile «WALK ON THE WILD SIDE» vorn) und unten links (Daten der Rückseite): danach Schriftfarbe und Schleier."""
    im = Image.open(datei).convert('L'); w, h = im.size
    oben = im.crop((int(w * .15), 0, int(w * .85), int(h * .18))).resize((64, 16))
    unten = im.crop((0, int(h * .45), int(w * .6), h)).resize((64, 48))
    m = lambda x: sum(x.get_flattened_data() if hasattr(x, "get_flattened_data") else x.getdata()) / (x.width * x.height * 255)
    return round(m(oben), 3), round(m(unten), 3)


def helligkeit_rueck(datei):
    """Helligkeit der Rückseite dort, wo die Schrift steht (oben links «WALK / ON THE / WILD SIDE», unten Daten, Gänge und Drinks): über 0,55 dunkle Schrift."""
    im = Image.open(datei).convert('L'); w, h = im.size
    teile = [im.crop((0, 0, int(w * .45), int(h * .3))), im.crop((0, int(h * .7), w, h))]
    return round(sum(sum(x.resize((48, 32)).getdata()) / (48 * 32 * 255) for x in teile) / 2, 3)


def rueckfarbe(datei):
    """Ruhiger Grund der Rückseite in der Farbwelt der Illustration (statt eines Bildes): die häufigste kräftige Farbe des Bildes, so weit abgedunkelt,
    dass warmweisse Schrift mindestens 7:1 Kontrast hat (wie auf den echten Rückseiten: weisse Versalien auf satter, dunkler Fläche)."""
    im = Image.open(datei).convert('RGB').resize((120, 90))
    q = im.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:24]; zaehl = sorted(q.getcolors(), reverse=True)
    def satt(rgb):
        mx, mn = max(rgb), min(rgb); return (mx - mn) / (mx or 1)
    farben = [tuple(pal[i * 3:i * 3 + 3]) for _, i in zaehl]
    wahl = next((f for f in farben if satt(f) > .25 and max(f) > 40), farben[0])
    def lum(c):
        c = [x / 255 for x in c]; c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
        return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
    f = list(wahl)
    while (0.911 + .05) / (lum(f) + .05) < 7 and max(f) > 8:
        f = [int(x * .9) for x in f]
    return '#%02x%02x%02x' % tuple(f)


def illustration(datei):
    """Bildfeld der Vorderseite: innerhalb des warmweissen Rands, oberhalb des Kastens mit der Wortmarke. Alle Plakate seit 2023 haben denselben
    Aufbau (gemessen an DFqbLG2s_dc: x 4,0–96,5 %, y 2,6–74,5 %); feste Anteile, weil Schnee oder ein weisser Boden im Bild sonst als Rand gelten."""
    im = ImageOps.exif_transpose(Image.open(datei)).convert('RGB')
    w, h = im.size
    return im.crop((round(w * .0415), round(h * .0275), round(w * .9635), round(h * .7435)))


def potrace_pfade(svg):
    """potrace-SVG (transform translate/scale, Befehle m M c l z, relativ) → Pfade als absolute Befehle in Einheiten der Seite (y nach unten);
    Umlaufrichtung bleibt (beide Achsen gleich gespiegelt), PDF (pdf-lib, nonzero) und Bildschirm füllen gleich. Wie bau.py der Taverne zum Schäfli."""
    tr = re.search(r'translate\(([-\d.]+),([-\d.]+)\)\s*scale\(([-\d.]+),([-\d.]+)\)', svg)
    tx, ty, sx, sy = (float(x) for x in tr.groups()) if tr else (0, 0, 1, 1)
    alle = []
    for d in re.findall(r'\sd="([^"]+)"', svg):
        tok = re.findall(r'[MmCcLlZz]|-?\d*\.?\d+', d)
        i, cmd, x, y, sx0, sy0, teile = 0, None, 0.0, 0.0, 0.0, 0.0, []
        while i < len(tok):
            t = tok[i]
            if re.match(r'[A-Za-z]', t):
                cmd = t; i += 1
                if cmd in 'Zz':
                    teile.append(('Z',)); x, y = sx0, sy0
                continue
            n = {'M': 2, 'm': 2, 'L': 2, 'l': 2, 'C': 6, 'c': 6}[cmd]
            v = [float(q) for q in tok[i:i + n]]; i += n
            rel = cmd.islower()
            if cmd in 'Mm':
                x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1]); sx0, sy0 = x, y
                teile.append(('M', x, y)); cmd = 'l' if rel else 'L'
            elif cmd in 'Ll':
                x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1]); teile.append(('L', x, y))
            else:
                q = [(x + v[k], y + v[k + 1]) if rel else (v[k], v[k + 1]) for k in (0, 2, 4)]
                teile.append(('C', *q[0], *q[1], *q[2])); x, y = q[2]
        neu = []
        for t in teile:
            if t[0] == 'Z':
                neu.append(t); continue
            q = []
            for k in range(1, len(t), 2):
                q += [tx + sx * t[k], ty + sy * t[k + 1]]
            neu.append((t[0], *q))
        alle.append(neu)
    return alle


def als_d(teile_liste):
    f = lambda v: f'{v:.2f}'
    return [''.join('Z' if t[0] == 'Z' else t[0] + ' '.join(f(v) for v in t[1:]) for t in p) for p in teile_liste]


TOK = re.compile(r'[MCLZmclzHhVv]|-?\d*\.?\d+(?:e-?\d+)?')


def pfad_teile(d):
    """Pfad mit absoluten Befehlen M, L, C, Z (so stehen Logo und Zeichen) → Liste von Befehlen."""
    tok = TOK.findall(d)
    i, cmd, teile = 0, None, []
    while i < len(tok):
        t = tok[i]
        if t.isalpha():
            cmd = t; i += 1
            if cmd in 'Zz':
                teile.append(('Z',))
            continue
        n = {'M': 2, 'L': 2, 'C': 6}[cmd]
        v = [float(q) for q in tok[i:i + n]]; i += n
        teile.append((cmd, *v))
        if cmd == 'M':
            cmd = 'L'
    return teile


def zeichen_aus(pfade_d, hoehe=140, box=None):
    """Zeichen aus absoluten Pfaden, Höhe 140 Einheiten, Nullpunkt oben links (Rahmen = box oder aus den Punkten)."""
    alle = [pfad_teile(d) for d in pfade_d]
    pts = [(t[k], t[k + 1]) for p in alle for t in p if t[0] != 'Z' for k in range(1, len(t), 2)]
    x0, y0, x1, y1 = box or (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
    k = hoehe / (y1 - y0)
    f = lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')
    aus = []
    for p in alle:
        s = []
        for t in p:
            if t[0] == 'Z':
                s.append('Z'); continue
            s.append(t[0] + ' '.join(f((t[j] - x0) * k) if j % 2 == 1 else f((t[j] - y0) * k) for j in range(1, len(t))))
        aus.append(''.join(s))
    return aus, [0, 0, round((x1 - x0) * k, 2), hoehe]


def tapete(quelle, farbe, deckung_linie, deckung_c, ziel, breite=448):
    """Kachel der Website-Tapete (224 px Rapport): feines Raster als Linie, das «C» klein, eigene Farbe und Deckkraft, WebP mit Alpha."""
    s = open(os.path.join(WEB, 'assets/zeichen', quelle), encoding='utf-8').read()
    s, n1 = re.subn(r'stroke="#[0-9A-Fa-f]{6}" stroke-opacity="[\d.]+"', f'stroke="{farbe}" stroke-opacity="{deckung_linie}"', s, count=1)
    s, n2 = re.subn(r'fill="#[0-9A-Fa-f]{6}" fill-opacity="[\d.]+"', f'fill="{farbe}" fill-opacity="{deckung_c}"', s, count=1)
    if n1 != 1 or n2 != 1:
        raise SystemExit('Tapete: Aufbau des SVG unbekannt (' + quelle + ')')
    tmp_svg, tmp_png = ziel + '.svg', ziel + '.png'
    open(tmp_svg, 'w', encoding='utf-8').write(s)
    env = dict(os.environ, NODE_PATH=os.path.expanduser('~/Aussen-Pruefung/node_modules'))
    subprocess.run(['node', os.path.join(HIER, '_qa', 'svg_png.js'), tmp_svg, tmp_png, str(breite)], check=True, env=env)
    Image.open(tmp_png).save(ziel, 'WEBP', lossless=True)
    os.remove(tmp_svg); os.remove(tmp_png)


def schnitt(quelle, ziel, achsen, familie):
    """Fester TrueType-Schnitt aus der Schrift der Website (OFL), damit PDF (pdf-lib) und Bildschirm dieselben Formen tragen."""
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    q = os.path.join(WEB, 'assets', 'schrift', quelle)
    if os.path.exists(ziel) and os.path.getmtime(ziel) >= os.path.getmtime(q) and os.path.getmtime(ziel) >= os.path.getmtime(__file__):
        return
    f = TTFont(q)
    if 'fvar' in f:
        da = {a.axisTag for a in f['fvar'].axes}
        instancer.instantiateVariableFont(f, {k: v for k, v in achsen.items() if k in da}, inplace=True)
    f.flavor = None
    for r in f['name'].names:
        if r.nameID in (1, 4, 16):
            r.string = familie
        elif r.nameID == 6:
            r.string = familie.replace(' ', '-')
        elif r.nameID in (2, 17):
            r.string = 'Regular'
    f.save(ziel)


def bildschirm_woff2(S):
    """Am Bildschirm woff2 als Teilmenge Latein samt Umlauten, «», € und Satzzeichen, alle Layout-Merkmale und Kerning (29.10.2026: Start der Werkstatt);
    das PDF bettet weiter die vollen TTF ein (druck.js), satz.js lädt woff2 vor TTF."""
    from fontTools import subset
    from fontTools.ttLib import TTFont
    U = list(range(0x20, 0x7f)) + list(range(0xa0, 0x250)) + list(range(0x2000, 0x2070)) + [0x20ac, 0x2122, 0x2190, 0x2192, 0x2212, 0x2116, 0xfb01, 0xfb02]
    GROSS = [c for c in range(0x20, 0x61)] + list(range(0x7b, 0x7f)) + [0xa0, 0xab, 0xb7, 0xbb] + list(range(0xc0, 0xdf)) + [0x1e9e] + list(range(0x2010, 0x2027)) + [0x20ac]
    for f in sorted(glob.glob(os.path.join(S, '*.ttf'))):
        o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['*']; o.name_IDs = ['*']; o.notdef_outline = True; o.hinting = True; o.legacy_kern = True
        uu = GROSS if os.path.basename(f).startswith('Anton') else U   # Kopfzeile wie Rudi steht immer in Versalien: nur die Grossbuchstaben (30.10.2026, 31 → rund 9 KB); satz.js holt für alles andere die TTF (unicode-range)
        ft = TTFont(f); u = subset.Subsetter(o); u.populate(unicodes=uu); u.subset(ft); ft.flavor = 'woff2'; ft.save(f[:-4] + '.woff2')


def culinarium():
    for u in ('schriften', 'bilder', 'mini', 'kopf', 'mail'):
        os.makedirs(os.path.join(Z, u), exist_ok=True)

    css = open(os.path.join(WEB, 'assets/culinarium.css'), encoding='utf-8').read()
    wurzel = css[css.index(':root{'):css.index('}', css.index(':root{'))]
    V = {k: v.lower() for k, v in re.findall(r'--([a-z0-9-]+):(#[0-9a-fA-F]{6})', wurzel)}
    TON = {t: dict(re.findall(r'--(bg|fg|fg2):(#[0-9A-Fa-f]{6})', b)) for t, b in re.findall(r'\[data-ton=(\w+)\]\{([^}]*)\}', css)}
    F = dict(navy=V['nacht'], nacht=V['nacht-tief'], blau=V['schiefer'], tinte=TON['hell']['fg'].lower(), papier='#f3ecea', creme='#e9e0de', weiss=V['weiss'],
             gold=V['kerze-hell'], taupe=V['kerze-tief'], messing=V['kerze'], tanne=V['schiefer'], kander=V['kerze'], laden=TON['strasse']['bg'].lower(), dc=V['dc'],
             leise=TON['hell']['fg2'].lower())
    # papier/creme: Raum und Fläche der Werkzeug-Oberfläche (kleid/culinarium.css --wo-papier, --wo-papier2, Chat «culinarium-maison»), aus dem Warmweiss abgeleitet
    kl = open(os.path.join(PROJ, '_werkzeuge', 'oberflaeche', 'kleid', 'culinarium.css'), encoding='utf-8').read()
    wo = {k: v.lower() for k, v in re.findall(r'--wo-([a-z0-9]+):(#[0-9a-fA-F]{6})', kl)}
    F['papier'], F['creme'] = wo.get('papier', F['papier']), wo.get('papier2', F['creme'])
    N = dict(navy='Nacht', nacht='Nacht tief', blau='Schiefer', tinte='Tinte', papier='Plakatpapier', creme='Plakatpapier tief', weiss='Warmweiss', gold='Kerze hell',
             taupe='Kerze tief', messing='Kerze', tanne='Schiefer', kander='Kerze', laden='Strasse', dc='Dirty Chicken', leise='Tinte leise')

    zd = open(os.path.join(PROJ, '_werkzeuge', 'oberflaeche', 'kleid', 'culinarium-zeichen.svg'), encoding='utf-8').read()
    pfade, vb = zeichen_aus(re.findall(r'\sd="([^"]+)"', zd))
    lg = open(os.path.join(PROJ, '_quelle', 'logo', 'original', 'culinarium-logo-original.svg'), encoding='utf-8').read()
    wmb = [float(x) for x in re.search(r'data-wm="([^"]+)"', lg).group(1).split()]
    pfade2, vb2 = zeichen_aus([re.search(r'id="wm"[^>]*\sd="([^"]+)"', lg).group(1)], 140, (wmb[0], wmb[1], wmb[0] + wmb[2], wmb[1] + wmb[3]))
    logo_farbe = re.search(r'id="wm" fill="(#[0-9A-Fa-f]{6})"', lg).group(1).lower()
    # Zeichen von Dirty Chicken (das D mit Hühnerfuss, potrace aus dem Profilbild, _quelle/dirty-chicken/logo/; nur für Stücke im Ton «dc»)
    pfade3, vb3 = zeichen_aus(als_d(potrace_pfade(open(os.path.join(PROJ, '_quelle', 'dirty-chicken', 'logo', 'dirtychicken-zeichen-nachgezogen.svg'), encoding='utf-8').read())))

    S = os.path.join(Z, 'schriften')
    schnitt('fraunces-soft.woff2', os.path.join(S, 'Fraunces-340.ttf'), dict(wght=340, SOFT=100, WONK=1, opsz=144), 'Fraunces 340')
    schnitt('fraunces-soft.woff2', os.path.join(S, 'Fraunces-Zeile-360.ttf'), dict(wght=360, SOFT=100, WONK=0, opsz=72), 'Fraunces Zeile 360')
    schnitt('instrument.woff2', os.path.join(S, 'InstrumentSans-400.ttf'), dict(wght=400), 'Instrument Sans 400')
    schnitt('instrument.woff2', os.path.join(S, 'InstrumentSans-500.ttf'), dict(wght=500), 'Instrument Sans 500')
    schnitt('dmmono.woff2', os.path.join(S, 'DMMono-400.ttf'), {}, 'DM Mono 400')
    schnitt('urbanist.woff2', os.path.join(S, 'Urbanist-600.ttf'), dict(wght=600), 'Urbanist 600')
    schnitt('urbanist.woff2', os.path.join(S, 'Urbanist-800.ttf'), dict(wght=800), 'Urbanist 800')   # Rückseite der Plakate: fette, runde Versalien wie dort
    SCHRIFTEN = {
        'titel': ('Fraunces 340', 'Fraunces-340.ttf', 'Titel, Fraunces mit weichen Enden 340 wie die Website (SOFT 100, opsz 144)'),
        'kapitale': ('Fraunces Zeile 360', 'Fraunces-Zeile-360.ttf', 'Rudis Zeilen in Versalien mit Schrägstrich («LAUCH / BLUMENKOHL / CHIPOTLE»)'),
        'text': ('Instrument Sans', 'InstrumentSans-400.ttf', 'Lesetext wie die Website'),
        'kursiv': ('Instrument Sans 500', 'InstrumentSans-500.ttf', 'Betont (die Website setzt nie kursiv, Betonung über Stärke und Farbe)'),
        'mono': ('DM Mono', 'DMMono-400.ttf', 'Zahlen, Daten, Zeiten'),
        'plakat': ('Urbanist 600', 'Urbanist-600.ttf', 'Zeilen der Plakate («A UNiQUE EXPERiENCE BY MOMO X RUDI») wie die Website'),
        'plakatfett': ('Urbanist 800', 'Urbanist-800.ttf', 'Rückseite der Plakate: «WALK / ON THE / WILD SIDE», Daten, Gänge und Drinks, fett und rund wie auf den echten Rückseiten'),
        # Kopfzeile wie Rudi sie malt (Robert 29.10.2026): Anton aus dem google/fonts-Repo (OFL), liegt schon in schriften/ (Anton-400.ttf, Anton-OFL.txt)
        'kopf': ('Anton', 'Anton-400.ttf', 'Kopfzeile «WALK ON THE WILD SIDE» wie Rudi sie malt: sehr fett, schmal, Versalien, farbig aus dem Motiv (Anton, SIL Open Font License 1.1)'),
    }

    bildschirm_woff2(S)

    # Tapete: Raster mit dem «C». Website dunkel 7 % / 14 %, im Druck kräftiger (feine Linien verschwinden auf Papier), in der Oberfläche leiser.
    tapete('tapete-dunkel.svg', F['gold'], .14, .2, os.path.join(Z, 'tapete-dunkel.webp'))
    tapete('tapete-hell.svg', F['blau'], .09, .14, os.path.join(Z, 'tapete-hell.webp'))
    tapete('tapete-dunkel.svg', F['gold'], .08, .13, os.path.join(Z, 'tapete-ui-dunkel.webp'))
    tapete('tapete-hell.svg', F['blau'], .05, .08, os.path.join(Z, 'tapete-ui-hell.webp'))
    t = Image.open(os.path.join(Z, 'tapete-dunkel.webp')).convert('RGBA'); g = Image.new('RGBA', t.size, F['navy']); g.alpha_composite(t)
    g.convert('RGB').save(os.path.join(Z, 'mail', '_tapete.jpg'), 'JPEG', quality=86)

    # Fotos aus dem Bildregister der Website
    W = website_daten()
    meta = json.load(open(os.path.join(WEB, 'assets', 'bild', 'meta.json'), encoding='utf-8'))
    beschr = {k: v[2] for k, v in W['BILD'].items()}
    for j, d, z_, p, pid, mit in W['ABENDE']:
        if pid:
            beschr['p_' + pid] = 'Plakat Culinarium, %s %s' % (d, j)
    LIVRE = os.path.join(PROJ, '_werkzeuge', 'livre')
    LJ = os.path.join(LIVRE, 'livre.json')
    LV = {}
    if os.path.exists(LJ):
        lj = json.load(open(LJ, encoding='utf-8'))
        if 'Culinarium' in str(lj.get('haus') or ''):
            LV = {f['k']: f for f in lj.get('fotos', [])}
    bilder, neu, raus = [], 0, []

    def ablegen(key, q, alt, gr, quelle=None):
        nonlocal neu
        ziel, mini = os.path.join(Z, 'bilder', key + '.webp'), os.path.join(Z, 'mini', key + '.webp')
        im = q if isinstance(q, Image.Image) else Image.open(q)
        w, h = im.size
        stand = getattr(q, 'stand', None) or (None if isinstance(q, Image.Image) else os.path.getmtime(q))   # Quelle neuer als die Ablage → neu ablegen
        alt_da = os.path.exists(ziel) and Image.open(ziel).size == (w, h) and (stand is None or os.path.getmtime(ziel) >= stand)
        if not alt_da:
            if isinstance(q, Image.Image):
                q.save(ziel, 'WEBP', quality=90, method=5)
            else:
                shutil.copy2(q, ziel)
            neu += 1
            for x in (mini, os.path.join(Z, 'mail', key + '.jpg'), os.path.join(Z, 'kopf', key + '.webp')):
                if os.path.exists(x): os.remove(x)
        rgb = im.convert('RGB')
        if not os.path.exists(mini):
            k = rgb.copy(); k.thumbnail((520, 520), Image.LANCZOS); k.save(mini, 'WEBP', quality=74, method=5)
        mail = os.path.join(Z, 'mail', key + '.jpg')
        if not os.path.exists(mail):
            k = rgb.copy(); k.thumbnail((1200, 1200), Image.LANCZOS); k.save(mail, 'JPEG', quality=76, optimize=True, progressive=True)
        if key in KOPF and not os.path.exists(os.path.join(Z, 'kopf', key + '.webp')):
            k = rgb.copy(); k.thumbnail((1200, 1200), Image.LANCZOS); k.save(os.path.join(Z, 'kopf', key + '.webp'), 'WEBP', quality=78, method=5)
        b = dict(key=key, alt=alt, w=w, h=h, gruppe=gr)
        if quelle:
            b['quelle'] = quelle
        bilder.append(b)

    for key in list(beschr):
        alt = beschr[key]
        if key in RAUS or PLAKAT_BAR.match(alt) or key not in meta:
            raus.append(key); continue
        q = os.path.join(WEB, 'assets', 'bild', '%s-%d.webp' % (key, max(meta[key]['stufen'])))
        if key in LV and LV[key].get('fl') and os.path.exists(os.path.normpath(os.path.join(LIVRE, LV[key]['fl']))):
            q = os.path.normpath(os.path.join(LIVRE, LV[key]['fl']))   # kennt das Hausbuch das Foto, gilt dessen Datei (Master F80)
        if not os.path.exists(q):
            raus.append(key); continue
        ablegen(key, q, alt, gruppe(key))

    # Plakate je Abend: Illustration der Vorderseite (für das Plakat im Rahmen des Hauses) und Akzentfarbe
    abende = []
    for j, d, zusatz, preis, pid, mit in W['ABENDE']:
        a = dict(jahr=j, daten=d, zusatz=zusatz, mit=mit, plakat=pid)
        if pid:
            f = [x for x in os.listdir(os.path.join(PROJ, W['IG'])) if pid in x and x.endswith('-1.jpg')][0]
            q = os.path.join(PROJ, W['IG'], f)
            ablegen('pl_' + pid, illustration(q), 'Illustration des Plakats, %s %s' % (d, j), 'Plakat-Motive')   # Rudis Illustration: im Fotofach unter «Plakat-Motive», zum Tauschen im Editor
            ablegen('po_' + pid, q, 'Plakat vom %s %s, ganz' % (d, j), 'Plakate')   # das ganze Plakat fürs Archiv, nichts angeschnitten
            r = q.replace('-1.jpg', '-2.jpg')
            if os.path.exists(r):
                ablegen('pr_' + pid, r, 'Rückseite des Plakats vom %s %s, ganz' % (d, j), 'Plakate')
            a['akzent'] = akzent(q)
            a['illustration'] = 'pl_' + pid
        abende.append(a)

    # Plakat-Motive: nur Rudis echte Plakat-Illustrationen seit 2023 (Roberts Entscheid 28.10.2026: «KI-Erzeugung aus der Plakatwerkstatt raus. Die Werkstatt
    # arbeitet mit Rudis echten Plakat-Illustrationen und dem Editor»). Je Illustration: Schlagworte für die Filter, ob «WALK ON THE WILD SIDE» schon im Bild
    # steht (dann keine zweite Kopfzeile), ob die Kopfzone für eine gesetzte Kopfzeile frei ist, und die Farbe des ruhigen Grunds der Rückseite.
    motive = []
    PI = os.path.join(HIER, '_qa', 'plakat-illustrationen.json')
    OHNE_SCHRIFT = {'CyT32RTMB4d', 'C56bJeds8PF', 'DCCf-ikoaGs', 'DPwlqcfiKcA', 'DbYnkdkjrNy'}   # Illustrationen ohne «WALK ON THE WILD SIDE» im Bild
    ak = {a['plakat']: a.get('akzent') for a in abende if a.get('plakat')}
    for m in json.load(open(PI, encoding='utf-8')).get('plakate', []):
        q = os.path.join(Z, 'bilder', 'pl_' + m['id'] + '.webp')
        if not os.path.exists(q):
            continue
        ho, hu = helligkeit(q); k = kopfzone.pruefe(q); schrift = m['id'] not in OHNE_SCHRIFT
        motive.append(dict(key='pl_' + m['id'], titel=m['titel'], quelle='plakat', schrift=schrift, schlagworte=m['schlagworte'], akzent=ak.get(m['id']),
                           hell_oben=ho, hell_unten=hu, kopf_frei=bool(k['frei']) and not schrift, kopf_farbe=k['farbe'] or 'weiss', rueck_farbe=rueckfarbe(q),
                           ganz='po_' + m['id'], kopf_box=kopfzone.kopfzeile_box(q) if schrift else None,   # Lage der gemalten Kopfzeile (Druckprüfung 29.10.)
                           ganz_kopf_box=kopfzone.kopfzeile_box(os.path.join(Z, 'bilder', 'po_' + m['id'] + '.webp')) if os.path.exists(os.path.join(Z, 'bilder', 'po_' + m['id'] + '.webp')) else None))
    json.dump(motive, open(os.path.join(Z, 'motive.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    da = {b['key'] for b in bilder}
    for u in ('bilder', 'mini', 'kopf'):
        for f in os.listdir(os.path.join(Z, u)):
            if f.endswith('.webp') and f[:-5] not in da and not f.startswith(('ki_', 'kir_', 'ab_', 'abr_')): os.remove(os.path.join(Z, u, f))   # neu erzeugte Motive des Servers (api/plakat.py) bleiben
    bilder.sort(key=lambda b: (ROLLEN.index(b['gruppe']), b['key']))

    marke = dict(
        key='culinarium', name='Culinarium', voll='Culinarium Hannover', ort='Hannover-Linden', artikel='das',
        zeile='A UNiQUE EXPERiENCE BY MOMO X RUDI', satz='Ein Menü mit fünf passenden Drinks an einer Tafel, an einzelnen Wochenenden.',
        adr='Walk on the Wild Side · Haasemannstraße 13 · 30449 Hannover', tel='Instagram @culinarium_hannover', mail='', web='instagram.com/culinarium_hannover',
        # keine Telefonnummer und keine Mailadresse für das Culinarium (fakten.json: «offen»); Kontakt per Instagram-Nachricht wie in den Beiträgen
        farben=F, farbnamen=N,
        toene=dict(
            dunkel=dict(grund='navy', tapete='dunkel', titel='weiss', text='papier', mono='gold', linie='messing', zeichen='messing', schild='papier', schild_text='navy'),
            hell=dict(grund='weiss', tapete=None, titel='tanne', text='tinte', mono='taupe', linie='messing', zeichen='tanne', schild='navy', schild_text='weiss'),
            creme=dict(grund='papier', tapete='hell', titel='tanne', text='tinte', mono='taupe', linie='messing', zeichen='tanne', schild='navy', schild_text='weiss'),
            # Dirty Chicken: nur in eigenen Stücken, Violett der Website (--dc), Schrift und Zeichen hell (website [data-ton=dc] fg #FFF7EF)
            dc=dict(grund='dc', tapete=None, titel='weiss', text='weiss', mono='weiss', linie='weiss', zeichen='weiss', schild='weiss', schild_text='dc'),
        ),
        schriften={k: dict(familie=f, datei=d, wofuer=w) for k, (f, d, w) in SCHRIFTEN.items()},
        tapete=dict(dunkel='tapete-dunkel.webp', hell='tapete-hell.webp', rapport_mm=24),
        zeichen=dict(vb=vb, pfade=pfade, verh=vb[3] / vb[2], name='Das «C» der Wortmarke'),
        zeichen2=dict(vb=vb2, pfade=pfade2, verh=vb2[3] / vb2[2], name='Die Wortmarke CULINARIUM (Rudis Original)',
                      farben=dict(grund=F['weiss'], zeichen=logo_farbe, text=logo_farbe, hell=F['gold'])),
        zeichen3=dict(vb=vb3, pfade=pfade3, verh=vb3[3] / vb3[2], name='Das D mit Hühnerfuss (Dirty Chicken, nachgezogen)'),
        abende=abende,
        betriebe=[('Culinarium', 'Ein Menü mit fünf Signature Drinks an einer Tafel, wenige Plätze, an einzelnen Wochenenden'),
                  ('Walk on the Wild Side', 'Die Bar in Linden, in der die Abende stattfinden'),
                  ('Dirty Chicken', 'Pop-up aus derselben Familie, eigene Farbe Violett')],
        regeln=['Anrede «du», herzlich, knapp, ein bisschen Strasse, wie das Haus schreibt. Nie Werbesprache, nie Ausrufezeichen im Titel.',
                'Jeder Satz wertet auf: Sorgfalt, Handarbeit, der einzelne Gast. Zahlen nur als Exklusivität («nur 14 Plätze»), nie als Menge.',
                'Rudis Gänge so schreiben, wie er sie schreibt: Versalien mit Schrägstrich («LAUCH / BLUMENKOHL / CHIPOTLE»), nie übersetzen oder glätten.',
                'Jeder Abend hat sein Plakat: Illustration oben, darunter die Wortmarke CULINARIUM im Kasten und das Band «A UNiQUE EXPERiENCE BY MOMO X RUDI», '
                'eine Akzentfarbe je Abend. Rückseite: Daten in der Form «27 / 11 / 26», Uhrzeit, «3 GÄNGE MENÜ», «5 SiGNATURE DRiNKS».',
                'Dunkle Flächen in Nacht, immer mit dem feinen Raster. Kerze nur für Linien, Zeichen und kleine Zeilen.',
                'Titel in Fraunces mit weichen Enden, nie fett, nie kursiv. Zahlen und Daten in DM Mono.',
                'Preise nur, wo das Haus sie nennt (Preis je Abend aus den Terminen); sonst keine.',
                'Das Culinarium findet in der Bar Walk on the Wild Side statt (Haasemannstraße 13, Linden). Dirty Chicken ist ein Pop-up aus derselben Familie '
                'und kommt nur in eigenen Stücken vor, dort in Violett. Kein Hotel, keine Zimmer.'],
        bilder=bilder,
        raus=sorted(set(raus)),
        ersatz=ERSATZ,
        doppelt={},
    )
    for b in marke.get('bilder', []):   # Farbe und Schatten der Kopfzeile wie Rudi je Bild (kopfzone.rudi_kopf, 29.10.2026)
        q = os.path.join(Z, 'bilder', b['key'] + '.webp')
        if os.path.exists(q): r = kopfzone.rudi_kopf(q); b['kopf_rudi'] = dict(farbe=r['farbe'], schatten=r['schatten'])
    json.dump(marke, open(os.path.join(Z, 'marke.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    json.dump({}, open(os.path.join(Z, 'druck.json'), 'w'))   # gedruckt wird die grösste Fassung der Website (I03), Originale liegen in _quelle/

    D = os.path.join(HIER, 'api', '_daten')
    os.makedirs(D, exist_ok=True)
    ki = {k: v for k, v in marke.items() if k not in ('zeichen', 'zeichen2', 'zeichen3', 'bilder')}
    ki['bilder'] = [f"{b['key']} | {'quer' if b['w'] > b['h'] * 1.1 else 'hoch' if b['h'] > b['w'] * 1.1 else 'quadratisch'} | {b['alt']}" for b in bilder]
    json.dump(ki, open(os.path.join(D, 'culinarium.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('culinarium:', len(bilder), 'Fotos,', neu, 'neu,', len(raus), 'nicht übernommen,', sum(1 for a in abende if a.get('plakat')), 'Plakate,',
          len(os.listdir(os.path.join(Z, 'kopf'))), 'Köpfe · Hausbuch', 'gelesen' if LV else 'noch nicht (eigene Kopie)')


if __name__ == '__main__':
    culinarium()
