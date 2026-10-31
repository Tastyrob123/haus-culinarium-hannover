#!/usr/bin/env python3
"""La Maison (Zentrale) des Culinarium Hannover (28.10.2026, Chat «culinarium-maison»).
Funktion, Bedienung und Technik wie La Maison der Taverne zum Schäfli und der anderen Häuser (Master Werkzeug-Bau 4.1, M01 bis M27,
R03, R04, R18, R19); Kleid und Empfang eigen für dieses Haus.

  python3 _werkzeuge/maison/bau.py      baut beide Fassungen aus einem Lauf (M13):
      _werkzeuge/maison/index.html …       lokal, über server.py (http://127.0.0.1:9081/_werkzeuge/maison/)
      _werkzeuge/maison/online/…           online-Fassung (nichts wird hochgeladen; Wege ohne localhost)

Empfang «Die Plakatwand»: Jeder Abend des Culinarium kündigt sich mit einem eigenen Plakat an (marke.json → eigene_welt). Links die Bühne
wie ein Schaufenster der Bar, in Ruhe die Fenster der Bar am Abend, beim Darüberfahren die echte Vorschau des Werkzeugs (M23); rechts die sechs
Werkzeuge als Plakate an der Wand: oben ein Foto aus den Abenden, unten das Band mit Name, was es tut, Stand. Das «x» von «Momo x Rudi»
als einziges Ornament, das «C» der Wortmarke als Zeichen.

Was ein Werkzeug liefert (Bildschirm, Knopf-Namen), nimmt der Bau erst, wenn es im Revier des Werkzeugs liegt (_werkzeuge/<werkzeug>/index.html)
und sein Bildschirm unter roh/ liegt (aufgenommen mit schirme.js). Bis dahin: Satz ohne Zahl, Tafel ohne Knopf-Namen, lokal ein
beschrifteter Platzhalter, online die Ruhe-Ansicht. Kundendaten (Name, Adresse, Fotos) nur aus der Website und der Sammlung gelesen, nie abgetippt."""
import ast, glob, hashlib, html, json, os, re, runpy, shutil, sys

e = html.escape
HIER = os.path.dirname(os.path.abspath(__file__))
WZ = os.path.dirname(HIER)                             # _werkzeuge/
ROOT = os.path.dirname(WZ)                             # Projektordner des Hauses
WEB = os.path.join(ROOT, 'website')
KETTE = os.path.join(ROOT, '_kette')
QUELLE = os.path.join(HIER, 'quelle')
ROH = os.path.join(HIER, 'roh')
PORT = 9081                                             # Prüfserver von La Maison (server.py)
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'


# ---------------------------------------------------------------- Hauswerte, gelesen aus der Sammlung (fakten.json) und website/bau.py (nie importiert: ast)
FAKTEN = json.load(open(os.path.join(KETTE, '03-sammler', 'fakten.json'), encoding='utf-8'))
_adr = re.fullmatch(r'(?P<bar>[^,]+), (?P<strasse>[^,]+), (?P<plz>\d{5}) (?P<ort>[^ (]+)(?: \((?P<teil>[^)]+)\))?', FAKTEN['adresse']['wert'])
if not _adr:
    raise SystemExit('fakten.json: Adresse nicht lesbar')
NAME = 'Culinarium'                                        # Name der Marke (Wortmarke CULINARIUM, marke.json)
BAR, STRASSE, PLZ_ORT, ORT = _adr['bar'], _adr['strasse'], _adr['plz'] + ' ' + _adr['ort'], _adr['ort'] + '-Linden'
if 'Linden' not in (_adr['teil'] or ''):
    ORT = _adr['ort']


def _bild_register():
    """BILD aus website/bau.py: Schlüssel → alt, pos (zweiter und dritter Wert jedes Eintrags, ohne den Pfad auszuwerten)."""
    baum = ast.parse(open(os.path.join(WEB, 'bau.py'), encoding='utf-8').read())
    for k in baum.body:
        if isinstance(k, ast.Assign) and len(k.targets) == 1 and getattr(k.targets[0], 'id', '') == 'BILD':
            return {ast.literal_eval(kk): dict(pos=ast.literal_eval(v.elts[1]), alt=ast.literal_eval(v.elts[2]))
                    for kk, v in zip(k.value.keys, k.value.values) if isinstance(v, ast.Tuple) and len(v.elts) >= 3}
    raise SystemExit('website/bau.py: BILD nicht gefunden')


BILDER_W = _bild_register()
MARKE = json.load(open(os.path.join(KETTE, '05-markenbauer', 'marke.json'), encoding='utf-8'))
ABENDFARBEN = [f for f in MARKE.get('abendfarben') or [] if re.fullmatch(r'#[0-9A-Fa-f]{6}', f.get('hex', '')) and re.fullmatch(r'#[0-9A-Fa-f]{6}', (f.get('toene') or {}).get('akzent', ''))]
if not ABENDFARBEN:
    raise SystemExit('marke.json: keine Abendfarben')


def svg_innen(pfad):
    s = open(pfad, encoding='utf-8').read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    innen = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    innen = re.sub(r'<!--.*?-->', '', innen, flags=re.S).replace('fill="#000"', '')
    return vb, re.sub(r'\s+', ' ', innen).strip()


ZEICHEN_DATEI = os.path.join(WZ, 'oberflaeche', 'kleid', 'culinarium-zeichen.svg')
LAMM_VB, LAMM = svg_innen(ZEICHEN_DATEI)       # das «C» der Wortmarke (Zeichen des Hauses; Name LAMM nur, weil der Bau der Vorlage so heisst)


# ---------------------------------------------------------------- Werkzeuge des Hauses
# Reihe wie in allen Häusern (Taste 1 bis 6 gleich).
REIHE = ['bureau', 'carte', 'imprimerie', 'reception', 'livre', 'registre']
TEIL = {'bureau': 'website', 'carte': 'karten', 'imprimerie': 'druck', 'reception': 'gaeste', 'livre': 'marke', 'registre': 'besuche'}
PORTS = {'bureau': 9082, 'carte': 9083, 'reception': 9084, 'livre': 9085, 'registre': 9086, 'imprimerie': 9087}   # AUFTRAG-GEMEINSAM.md


def welt_namen():
    t = open(os.path.expanduser('~/Desktop/Website-Projekte/_Werkzeuge/stamm/welt.js'), encoding='utf-8').read()
    return {teil: (land, tut) for teil, land, tut in re.findall(r"(\w+): \{ grand: '[^']+', land: '([^']+)', tut: '([^']+)' \}", t)}


WN = welt_namen()
# Namen der Werkzeuge: EINE Stelle für alle sieben Werkzeuge ist _werkzeuge/oberflaeche/kleid/culinarium.js (WO_HAUS.namen). Hier nur gelesen.
def haus_namen():
    t = open(os.path.join(WZ, 'oberflaeche', 'kleid', 'culinarium.js'), encoding='utf-8').read()
    m = re.search(r"namen:\s*\{([^}]*)\}", t)
    return dict(re.findall(r"(\w+):\s*'([^']+)'", m.group(1))) if m else {}


NAMEN = haus_namen()
ZENTRALE = NAMEN.get('zentrale') or WN['zentrale'][0]
ROLLE = {'bureau': 'Website pflegen', 'carte': 'Menü und Drinks je Abend', 'imprimerie': 'Plakate und Drucksachen', 'reception': 'Team hinter dem Gäste-Chat',
         'livre': 'Marke zum Arbeiten', 'registre': 'Besuche der Website'}   # Culinarium: ohne Preislisten, Zimmer oder Säle (die hat das Haus nicht)
W = {k: dict(name=NAMEN.get(TEIL[k]) or WN[TEIL[k]][0], rolle=ROLLE[k]) for k in REIHE}
ROLLE_K = {'bureau': 'Website', 'carte': 'Karten', 'imprimerie': 'Drucksachen', 'reception': 'Gäste', 'livre': 'Marke', 'registre': 'Besuche'}   # kurze Zeile im Gefach
KURZ = {'bureau': 'Die Website, Seite für Seite', 'carte': 'Menü und Drinks je Abend', 'imprimerie': 'Plakate, druckfertig', 'reception': 'Fragen der Gäste',
        'livre': 'Fotos, Wortmarke, Farben', 'registre': 'Besuche ohne Namen'}
# Satz je Saal: was das Werkzeug für dieses Haus tut (nur, was die Website hat: Abende, Plakate, Menü mit Drinks, Warteliste, Bar, Dirty Chicken)
SATZ = {
    'bureau': 'Die Website zum Anfassen: Texte, Fotos, die nächsten Abende und Hinweise für Gäste, Seite für Seite und ohne Programmierer.',
    'carte': 'Das Menü jedes Abends mit seinen Drinks: jeder Gang mit dem Drink, den Momo dazu stellt. Daraus entstehen die Karte am Platz und die PDF.',
    'imprimerie': 'Für jeden Abend sein eigenes Plakat, dazu Karten und Beiträge, in der Plakatsprache des Culinarium und ohne Grafikprogramm.',
    'reception': 'Was Gäste zu den Abenden wissen wollen, zu Plätzen, Unverträglichkeiten und dem Weg in die Bar, mit einem Antwortentwurf. Dazu ein Chat, der aus deinen Seiten antwortet.',
    'livre': 'Die Marke des Culinarium zum Arbeiten, für dich und für jede Agentur: Fotos der Abende, Wortmarke, Farben und Schriften.',
    'registre': 'Wer deine Website besucht: woher die Gäste kommen, welche Abende sie sich ansehen und wie oft es weiter zum Platz geht.',
}


def geliefert(k):
    """Ein Werkzeug gilt als da, wenn sein Revier eine Oberfläche hat (_werkzeuge/<werkzeug>/index.html)."""
    return os.path.exists(os.path.join(WZ, k, 'index.html'))


# Stand-Weg je Werkzeug (Form fest, Master 4.1 «Stand-Wege»): steht in stand_wege.json (aus dem Werkzeug gelesen). Lokal holt der Prüfserver
# von La Maison sie über /_weiter/<werkzeug>/… (ein Browser liest nicht quer über Ports); online nur, wenn das Werkzeug online einen Weg hat.
def stand_wege():
    try:
        return json.load(open(os.path.join(HIER, 'stand_wege.json'), encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def wege(online):
    sw = stand_wege()
    aus = {}
    for k in REIHE:
        d = sw.get(k) or {}
        if online:
            auf = d.get('online') or '../werkbank/index.html#werkzeuge'
            stand = d.get('stand_online') or ''
        else:
            auf = (d.get('adresse') or f'http://127.0.0.1:{PORTS[k]}/_werkzeuge/{k}/') if geliefert(k) else ''
            stand = [f'/_weiter/{k}/' + x.lstrip('/') for x in ([d['stand']] if isinstance(d.get('stand'), str) else d.get('stand') or [])] if geliefert(k) else []
        aus[k] = dict(auf=auf, stand=stand, anl=(d.get('anleitung_online') if online else d.get('anleitung')) or '')
    return aus


# ---------------------------------------------------------------- Bilder
BILDER = {}
FEHLT = []


def pos_y(k):
    """Senkrechte Lage des Motivs aus «pos» des Bildregisters (z. B. '50% 60%' → 0,6)."""
    try:
        return float(BILDER_W[k]['pos'].split()[1].rstrip('%')) / 100
    except (KeyError, IndexError, ValueError):
        return .5


def webp(ziel, name, quelle, breit, klein=None, qual=82, crop=None):
    """Bild nach img/<name>.webp (und -s.webp), nur neu, wenn die Quelle neuer ist."""
    from PIL import Image
    os.makedirs(os.path.join(ziel, 'img'), exist_ok=True)
    z = os.path.join(ziel, 'img', name + '.webp')
    im = Image.open(quelle).convert('RGB')
    if crop:
        im = im.crop(crop)
    w = min(breit, im.width); h = round(im.height * w / im.width)
    if not os.path.exists(z) or os.path.getmtime(z) < max(os.path.getmtime(quelle), os.path.getmtime(__file__)):
        (im.resize((w, h), Image.LANCZOS) if w != im.width else im).save(z, quality=qual, method=6)
        if klein:
            kw = min(klein, w)
            im.resize((kw, round(im.height * kw / im.width)), Image.LANCZOS).save(os.path.join(ziel, 'img', name + '-s.webp'), quality=78, method=6)
    BILDER[name] = (w, h)


def web_bild(k, gross=(2400, 1600, 1000, 640)):
    for w in gross:
        q = os.path.join(WEB, 'assets', 'bild', f'{k}-{w}.webp')
        if os.path.exists(q):
            return q
    m = sorted(glob.glob(os.path.join(WEB, 'assets', 'bild', f'{k}-[0-9]*.webp')), key=lambda p: -int(re.search(r'-(\d+)\.webp$', p).group(1)))
    if m:
        return m[0]
    raise SystemExit('Foto fehlt in der Website: ' + k)


# Ruhe-Ansicht: die Fenster der Bar am Abend (wie das Startbild der Werkzeuge), hochkant genug für die Bühne neben zwei Reihen Plakaten (5 : 4)
RUHE = 'fassade'


def ruhe_crop():
    from PIL import Image
    w, h = Image.open(web_bild(RUHE)).size
    ch = min(h, round(w * 4 / 5)); cw = round(ch * 5 / 4)
    x0 = (w - cw) // 2; y0 = round((h - ch) * pos_y(RUHE))
    return (x0, y0, x0 + cw, y0 + ch)


# Foto des Hauses je Werkzeug (Plakat im Empfang), aus den Bildern der Website, 4 : 3 geschnitten
RAUM = {'bureau': 'ecke', 'carte': 'lauch', 'imprimerie': 'pl23', 'reception': 'kerze2', 'livre': 'theke', 'registre': 'flur'}
RAUM_G = (800, 600)
# Fotos aus dem Bereich «Fotos» des Markenbuchs für dessen Saal (nur Fotos des Hauses, keine Menschen angeschnitten, nichts vom Schwesterhaus)
ARCHIV = ['tafelleer', 'g1', 'pass', 'anstossen', 'kanister', 'roq1']
SCHIRME = {'bureau': ['bureau', 'bureau-2'], 'carte': ['carte'], 'imprimerie': ['imprimerie'], 'reception': ['reception'],
           'livre': ['livre-fotos', 'livre-marke'], 'registre': ['registre', 'registre-herkunft']}


# Empfang wie die Zentrale des Grand Beau-Rivage (Robert 29.10.2026: «kannst du das machen wie beim Rivage?»): fünf hohe Fenster, je Werkzeug ein Foto
# des Abends über die ganze Höhe, Die Besucherliste als Zahlenzeile unter dem Titel. Je Foto: Lage am Desktop (hohe Säule) und am Handy (flaches Band),
# so gewählt, dass das Motiv steht (Fenster der Bar, Rudi am Tisch, die gedeckte Tafel in der Mitte unter dem Titel, Anstossen an der Tafel, Momo vor der Bar; Momo mit dem Shaker vor den Flaschen war gedrosselt zu schwer).
FENSTER = {'bureau': ('barlicht', '50% 50%', '50% 74%'), 'carte': ('rudi', '50% 40%', '50% 24%'), 'imprimerie': ('tafelleer', '50% 50%', '50% 52%'),
           'reception': ('anstossen', '42% 50%', '50% 30%'), 'livre': ('momo_hoch', '50% 50%', '50% 20%')}
FARBE = {}   # Platzhalter in der Motivfarbe statt Schwarz (Fund Oberchef 29.10.2026)


def bilder(ziel):
    BILDER.clear(); FEHLT.clear()
    from PIL import Image
    webp(ziel, 'ruhe', web_bild(RUHE), 1800, 1000, 80, ruhe_crop())
    for k, (f, pos, pos_h) in FENSTER.items():
        q = web_bild(f); w, h = Image.open(q).size
        px, py = (float(x.rstrip('%')) / 100 for x in pos.split()); hy = float(pos_h.split()[1].rstrip('%')) / 100
        # Fenster am Desktop: nur der sichtbare Streifen (Breite : Höhe = 0,36 wie ein Fenster bei 1440 × 900 bis 1920 × 1080), 600 und 900 px breit (Oberchef 29.10.2026)
        cw = min(w, round(h * .36)); x0 = round((w - cw) * px)
        for b in (600, 900):
            webp(ziel, f'fenster-{k}-{b}', q, b, None, 72, (x0, 0, x0 + cw, h))
        # am Handy ein flaches Band (2,6 : 1) an der Stelle, wo das Motiv steht
        bh = min(h, round(w / 2.6)); y0 = round((h - bh) * hy)
        webp(ziel, f'fenster-{k}-band', q, 800, None, 74, (0, y0, w, y0 + bh))
        FARBE[k] = '#%02x%02x%02x' % Image.open(q).convert('RGB').resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    for k in REIHE:
        for n in SCHIRME[k]:
            q = next((os.path.join(ROH, n + x) for x in ('.png', '.jpg', '.webp') if os.path.exists(os.path.join(ROH, n + x))), '')
            if not geliefert(k) or not q:
                FEHLT.append(n)
                continue
            webp(ziel, 'schirm-' + n, q, 2400, 1200, 84)
    from PIL import Image
    for k, rk in RAUM.items():
        q = web_bild(rk, (1600, 1000, 2400, 640))
        for name, (bw, bh) in ((f'raum-{k}', RAUM_G), (f'raum-{k}-s', (480, 360))):
            z = os.path.join(ziel, 'img', name + '.webp')
            if not os.path.exists(z) or os.path.getmtime(z) < max(os.path.getmtime(q), os.path.getmtime(__file__)):
                im = Image.open(q).convert('RGB')
                if k == 'imprimerie':   # Plakate nie anschneiden (Oberchef/Robert 28.10.2026): das ganze Plakat mit Innenrand und weichem Schatten auf hellem Grund
                    from PIL import ImageFilter
                    rand = round(bh * .09); ph = bh - 2 * rand; im = im.resize((round(im.width * ph / im.height), ph), Image.LANCZOS)
                    grund = Image.new('RGB', (bw, bh), (243, 236, 234)); x = (bw - im.width) // 2
                    sch = Image.new('L', (bw, bh), 0); sch.paste(150, (x + 4, rand + round(bh * .03), x + im.width - 4, rand + ph + round(bh * .03)))
                    grund.paste((120, 105, 108), (0, 0), sch.filter(ImageFilter.GaussianBlur(round(bh * .035))))
                    grund.paste(im, (x, rand)); grund.save(z, quality=82, method=6)
                    continue
                sk = max(bw / im.width, bh / im.height)
                im = im.resize((round(im.width * sk), round(im.height * sk)), Image.LANCZOS)
                x = (im.width - bw) // 2; y = min(max(0, round(im.height * pos_y(rk) - bh * .5)), im.height - bh)
                im.crop((x, y, x + bw, y + bh)).save(z, quality=80, method=6)
    # Stücke der Säle: Karten (roh/karten/*.png aus den PDF von La Carte), Drucksachen (roh/druck/*.png), Fotos aus dem Markenbuch
    if geliefert('imprimerie'):
        for q in sorted(glob.glob(os.path.join(ROH, 'druck', '*.png'))):
            webp(ziel, 'druck-' + os.path.basename(q)[:-4], q, 1000, None, 84)
    if geliefert('carte'):
        for q in sorted(glob.glob(os.path.join(ROH, 'karten', '*.png'))):
            webp(ziel, 'karte-' + os.path.basename(q)[:-4], q, 1000, None, 84)
    if geliefert('livre'):
        for k in ARCHIV:
            webp(ziel, 'archiv-' + k, web_bild(k, (1000, 1600, 640)), 900, None, 80)
    for n in ('reception-chat',):
        q = os.path.join(ROH, n + '.png')
        if os.path.exists(q) and geliefert('reception'):
            webp(ziel, 'schirm-' + n, q, 2400, 1200, 84)
    # Tapeten der Website als gerechnetes Bild (quelle/tapete.js, doppelte Dichte): ein SVG-Muster kostete am Handy beim ersten Scrollen ein Bild über 33 ms
    for art, svg in (('dunkel', 'tapete-dunkel.svg'), ('hell', 'tapete-hell.svg')):
        q = os.path.join(QUELLE, f'tapete-{art}@2x.png')
        if not os.path.exists(q) or os.path.getmtime(q) < os.path.getmtime(os.path.join(WEB, 'assets', 'zeichen', svg)):
            raise SystemExit('Tapete der Website ist neuer: node _werkzeuge/maison/quelle/tapete.js')
        Image.open(q).save(os.path.join(ziel, 'img', f'tapete-{art}.webp'), lossless=True, method=6)
    os.makedirs(os.path.join(ziel, 'schrift'), exist_ok=True)
    for f in ('fraunces-soft.woff2', 'instrument.woff2', 'urbanist.woff2', 'dmmono.woff2'):
        shutil.copyfile(os.path.join(WEB, 'assets', 'schrift', f), os.path.join(ziel, 'schrift', f))


# ---------------------------------------------------------------- Bausteine
I = {
    'stift': '<svg viewBox="0 0 24 24"><path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13.5 6.5 4 4"/></svg>',
    'uhr': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="M12 7.5V12l3 2"/></svg>',
    'waage': '<svg viewBox="0 0 24 24"><path d="M12 4v16M7 20h10M5 8h14"/><path d="m5 8-2.5 6a2.5 2.5 0 0 0 5 0zM19 8l-2.5 6a2.5 2.5 0 0 0 5 0z"/></svg>',
    'liste': '<svg viewBox="0 0 24 24"><path d="M9 7h11M9 12h11M9 17h11"/><path d="M4.5 7h.5M4.5 12h.5M4.5 17h.5"/></svg>',
    'pdf': '<svg viewBox="0 0 24 24"><path d="M6 3.5h8l4 4v13H6z"/><path d="M14 3.5v4h4M9 13h6M9 16.5h4"/></svg>',
    'zurueck': '<svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 1 0 2.4-5.7"/><path d="M4 4v4.5h4.5"/></svg>',
    'satz': '<svg viewBox="0 0 24 24"><path d="M4 6h16M4 11h16M4 16h9"/><path d="m17 15 3 3-3 3"/></svg>',
    'fuenf': '<svg viewBox="0 0 24 24"><rect x="3.5" y="5" width="7" height="9" rx="1"/><rect x="13.5" y="5" width="7" height="9" rx="1"/><path d="M6 18h12"/></svg>',
    'druck': '<svg viewBox="0 0 24 24"><path d="M7 8V3.5h10V8"/><rect x="3.5" y="8" width="17" height="8" rx="1.5"/><path d="M7 13.5h10v7H7z"/></svg>',
    'blase': '<svg viewBox="0 0 24 24"><path d="M4 5.5h16v11H10l-4 3.5v-3.5H4z"/></svg>',
    'eingang': '<svg viewBox="0 0 24 24"><path d="M4 13.5 6.5 5h11l2.5 8.5V19H4z"/><path d="M4 13.5h5a3 3 0 0 0 6 0h5"/></svg>',
    'foto': '<svg viewBox="0 0 24 24"><rect x="3.5" y="5.5" width="17" height="13" rx="1.5"/><path d="m3.5 16 5-5 4 4 3-3 5 5"/><circle cx="15.5" cy="9.5" r="1.5"/></svg>',
    'datei': '<svg viewBox="0 0 24 24"><path d="M3.5 7.5h6l2 2h9v9h-17z"/></svg>',
    'farbe': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle cx="9" cy="9.5" r="1.3"/><circle cx="14.5" cy="8.5" r="1.3"/><circle cx="16" cy="13.5" r="1.3"/><path d="M11 20a2.5 2.5 0 0 1 0-5"/></svg>',
    'karte': '<svg viewBox="0 0 24 24"><path d="M4 20V6l5-2 6 2 5-2v14l-5 2-6-2z"/><path d="M9 4v14M15 6v14"/></svg>',
}

UI = []   # Knopf-Namen aus den Tafeln: (werkzeug, name), gegen den Code des Werkzeugs geprüft (knoepfe())


def ui(t, k=''):
    def merk(m):
        UI.append((k, m.group(1)))
        return f'<span class="m-ui">{m.group(1)}</span>'
    return re.sub(r'«([^»]+)»', merk, t)


# Tafeln «So geht’s». ALLG ohne Knopf-Namen, solange das Werkzeug nicht vorliegt. HAUS (tafeln.json) mit den echten Knopf-Namen («…»),
# erst nach der Lieferung aus dem Code des Werkzeugs gelesen und beim Bau dagegen geprüft.
TAFEL_ALLG = {
    'bureau': [('stift', 'Text oder Foto ändern', 'Den Bereich wählen, in der Vorschau auf den Text oder das Foto klicken und ändern.'),
               ('uhr', 'Die nächsten Abende', 'Datum, Uhrzeit und freie Plätze eines Abends stehen an einer Stelle. Einmal ändern, jede Seite der Website folgt.'),
               ('waage', 'Erst Entwurf, dann online', 'Gespeichert ist erst ein Entwurf. Vorher und nachher nebeneinander ansehen, dann veröffentlichen.')],
    'carte': [('stift', 'Einen Gang ändern', 'Den Abend wählen, den Gang anklicken und seine Zeile überschreiben. Daneben steht sofort die Karte, wie sie am Platz liegt.'),
              ('liste', 'Den Drink dazu', 'Zu jedem Gang gehört sein Drink. Name und Zutaten stehen gleich daneben, so bleibt das Paar zusammen.'),
              ('pdf', 'Die Karte drucken', 'Vorab eine Probe ansehen, dann veröffentlichen: die PDF wird neu gesetzt, die Website zeigt das neue Menü.')],
    'imprimerie': [('satz', 'Den Abend beschreiben', 'Unter «Abend beschreiben» Thema, Konzept, Gastkoch und Wochenende eintragen, drei, vier oder fünf Vorschläge wählen und «Vorschläge anlegen».'),
                   ('fuenf', 'Neue Plakate, eigene Ideen', 'Jeder Vorschlag ist ein ganz neues Plakat im Stil von Rudis Plakaten, mit eigener Bildidee, vorn und hinten. Den passenden mit «Diesen bearbeiten» öffnen und im Editor fertig machen. Rudis Illustrationen liegen unter «Plakat-Motive».'),
                   ('druck', 'Drucken', 'Druckfertig als PDF speichern, für die Druckerei oder als Beitrag.')],
    'reception': [('blase', 'Gäste fragen im Chat', 'Auf jeder Seite der Website können Gäste fragen. Der Chat antwortet aus deinen Seiten, zu Abenden, Plätzen und dem Weg in die Bar.'),
                  ('eingang', 'Anfragen beantworten', 'Ein Platz an der Tafel, eine Unverträglichkeit, ein Abend für eine Gruppe: jede Anfrage steht im Eingang, mit einem Entwurf für deine Antwort. Verschickt wird nur, was du selbst schickst.'),
                  ('liste', 'Lücken schliessen', 'Wusste der Chat etwas nicht, steht die Frage in einer eigenen Liste. Einmal nachtragen, ab dann antwortet er selbst.')],
    'livre': [('foto', 'Ein Foto holen', 'Ein Foto anklicken und die Grösse wählen: für Instagram, die Website oder den Druck.'),
              ('datei', 'Wortmarke weitergeben', 'Wortmarke, Farben und Schriften liegen als Dateien bereit, für Agentur oder Druckerei.'),
              ('farbe', 'Einen Entwurf prüfen', 'Plakat oder Flyer einer Agentur hineinziehen. Es sagt Punkt für Punkt, was zum Culinarium passt.')],
    'registre': [('karte', 'Woher die Gäste kommen', 'Länder und Orte der Besuche, ohne Cookies und nie mit Namen.'),
                 ('liste', 'Was sie sich ansehen', 'Welche Abende und Seiten gefragt sind, und wie lange die Gäste bleiben.'),
                 ('uhr', 'Weiter zum Platz', 'Wie oft ein Besuch zum Platz führt: gebucht oder auf der Warteliste.')],
}


def tafel_zeilen(k):
    try:
        h = json.load(open(os.path.join(HIER, 'tafeln.json'), encoding='utf-8'))
    except (OSError, ValueError):
        h = {}
    z = h.get(k) if geliefert(k) and h.get(k) else TAFEL_ALLG[k]
    nm = {TEIL[x]: W[x]['name'] for x in REIHE}      # Namen anderer Werkzeuge nur aus der einen Stelle ({karten} → «die Tafel» im Satz)
    return [(s, t, re.sub(r'\{(\w+)\}', lambda m: (nm[m.group(1)][0].lower() + nm[m.group(1)][1:]) if m.group(1) in nm else m.group(0), x)) for s, t, x in z]


def tafel(k, i=0, extra=''):
    z = ''.join(f'<div class="m-tafel__z"><i>{I[s]}</i><p><b>{e(t)}</b>{ui(e(x, quote=False), k)}</p></div>' for s, t, x in tafel_zeilen(k))
    return f'<div class="m-tafel" data-r style="--i:{i}"><p class="m-tafel__kopf"><span>So geht’s</span></p>{z}{extra}</div>'


class Bau:
    online = False


WM_VB = '0 0 364.78 40.36'
WM = re.search(r'<symbol id="wm"[^>]*>(.*?)</symbol>', open(os.path.join(WEB, 'assets', 'zeichen', 'marke.svg'), encoding='utf-8').read(), re.S).group(1)
# Stufen des Wegs zur Buchung im Saal von Le Registre: Namen wie im Besucherbuch des Hauses (Fehlerbuch 10a, Stube Schäfli), sobald es vorliegt
# (registre/stufen.json); bis dahin die Wege der Website (Abend ansehen → Platz buchen oder Warteliste → Platz bestätigt).
try:
    STUFE = json.load(open(os.path.join(WZ, 'registre', 'stufen.json'), encoding='utf-8'))['maison']
except (OSError, ValueError, KeyError):
    STUFE = ['«Der Abend» geöffnet', 'Platz gebucht oder auf der Warteliste', 'dabei', 'zählt das Team am Abend, nicht die Website']   # Le Registre 28.10.2026


def wortmarke(c):
    return f'<svg class="{c}" viewBox="{WM_VB}" aria-label="Culinarium" role="img">{WM}</svg>'


def lamm(c):
    return f'<svg class="{c}" viewBox="{LAMM_VB}" fill="currentColor" aria-hidden="true">{LAMM}</svg>'


def schirm(n, k, leiste, alt, i=0, sizes='(max-width:1000px) 92vw, 60vw'):
    leiste = leiste.removeprefix(f'{ZENTRALE} · ')   # Abnahme-Tor 30.10.2026 (K2): man steht schon im Tresen; Werkzeug · Bereich passt bei jeder Breite ganz in die Leiste
    name = 'schirm-' + n
    if name not in BILDER:
        if Bau.online:
            return ''
        return (f'<figure class="m-schirm m-schirm--platz" data-r="schweb" style="--i:{i}" data-platz="{e(n)}"><div class="m-schirm__leiste" aria-hidden="true"><span>{e(leiste)}</span></div>'
                f'<div class="m-platz">{lamm("")}<b>Bildschirm folgt</b><p>{e(W[k]["name"])} wird gerade gebaut. Sobald es vorliegt, steht hier sein echter Bildschirm.</p>'
                f'<small>Platzhalter, nur lokal</small></div></figure>')
    b = BILDER[name]
    return (f'<figure class="m-schirm" data-r="schweb" style="--i:{i}"><div class="m-schirm__leiste" aria-hidden="true"><span>{e(leiste)}</span></div>'
            f'<img src="img/{name}.webp" srcset="img/{name}-s.webp 1200w, img/{name}.webp {b[0]}w" sizes="{sizes}" width="{b[0]}" height="{b[1]}" alt="{e(alt)}" loading="lazy" decoding="async"></figure>')


def stueck_bild(name, alt, cls='', i=0):
    if name not in BILDER:
        return ''
    w, h = BILDER[name]
    return f'<figure class="m-stueck {cls}" data-r="schweb" style="--i:{i}"><img src="img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}" loading="lazy" decoding="async"></figure>'


def stuecke(k):
    """Weitere echte Bilder je Saal (Fehlerbuch 10a: die Säle der anderen Häuser haben mehr Bilder als nur einen Bildschirm)."""
    if k == 'bureau':
        t = schirm('bureau-2', 'bureau', f'{ZENTRALE} · {W["bureau"]["name"]} · Startseite', 'Eine Seite offen: links die Stellen, rechts die Startseite der Website', 1, '(max-width:1000px) 92vw, 40vw')
        return f'<div class="m-stuecke m-stuecke--eins">{t}</div>' if 'schirm-bureau-2' in BILDER else ''
    if k in ('carte', 'imprimerie'):
        vor = 'karte-' if k == 'carte' else 'druck-'
        n = sorted(b for b in BILDER if b.startswith(vor))[:3]
        art = ['m-stueck--blatt', 'm-stueck--quer', 'm-stueck--blatt']
        try:   # Namen der Stücke aus der Lieferung des Werkzeugs (roh/karten/namen.json aus /api/status von La Carte, roh/druck/namen.json), nichts erfunden
            alt = json.load(open(os.path.join(ROH, 'karten' if k == 'carte' else 'druck', 'namen.json'), encoding='utf-8'))
        except (OSError, ValueError):
            alt = {}
        t = ''.join(stueck_bild(b, W[k]['name'] + ': ' + alt.get(b[len(vor):], b[len(vor):].replace('-', ' ')), 'm-stueck--quer' if BILDER[b][0] > BILDER[b][1] else 'm-stueck--blatt', i + 1) for i, b in enumerate(n))
        return f'<div class="m-stuecke m-stuecke--karten">{t}</div>' if t else ''
    if k == 'registre':   # Abnahme-Tor 30.10.2026 (K4): sonst steht links nur ein Bildschirm neben der langen rechten Spalte
        t = schirm('registre-herkunft', 'registre', f'{W["registre"]["name"]} · Herkunft', W['registre']['name'] + ' mit Beispielwerten: woher die Gäste kommen', 1, '(max-width:1000px) 92vw, 40vw')
        return f'<div class="m-stuecke m-stuecke--eins">{t}</div>' if 'schirm-registre-herkunft' in BILDER else ''
    if k == 'reception':
        t = schirm('reception-chat', 'reception', f'{ZENTRALE} · {W["reception"]["name"]} · Chat ausprobieren', 'Chat ausprobieren: so fragt ein Gast, mit Beispielfragen', 1, '(max-width:1000px) 92vw, 40vw')
        return f'<div class="m-stuecke m-stuecke--eins">{t}</div>' if 'schirm-reception-chat' in BILDER else ''
    if k == 'livre':
        t = ''.join(stueck_bild('archiv-' + n, BILDER_W[n]['alt'], 'm-stueck--foto', i + 1) for i, n in enumerate(ARCHIV))
        return f'<div class="m-stuecke m-stuecke--fotos">{t}</div>' if t else ''
    return ''


def knopf(t, href, cls='', neu=False):
    if not href:
        return f'<span class="m-hinweis">{e(t.replace("öffnen", "folgt"))}, sobald es vorliegt.</span>'
    z = ' target="_blank" rel="noopener"' if neu else ''
    return f'<a class="knopf {cls}" href="{e(href)}"{z}>{e(t)}<i>{PF}</i></a>'


def saal_kopf(k, nr):
    teile = W[k]['name'].split(' ', 1)
    titel = f'<em>{e(teile[0])}</em> {e(teile[1])}' if len(teile) == 2 else e(teile[0])
    return (f'<header class="m-saal__kopf">{lamm("m-saal__z")}<p class="m-saal__nr" data-r style="--i:0">N° {nr + 1} von 6 · {e(W[k]["rolle"])}</p>'
            f'<h2 class="m-saal__titel" data-r style="--i:1">{titel}</h2><p class="m-saal__satz" data-r style="--i:2">{e(SATZ[k])}</p></header>'
            f'<div class="m-saal__linie" aria-hidden="true"><i></i></div>')


def farben():
    """Farben des Hauses für den Saal der Marke: aus livre.json des Werkzeugs (nur nach der Lieferung), sonst keine (nichts erfunden)."""
    if not geliefert('livre'):
        return []
    try:
        f = json.load(open(os.path.join(WZ, 'livre', 'livre.json'), encoding='utf-8')).get('farben') or []
        return [(x['n'], x['h'].lower()) for x in f if re.fullmatch(r'#[0-9a-fA-F]{6}', x.get('h', '')) and x.get('n') and x.get('g') not in ('heute', 'abende', 'dc')][:12]   # Hausfarben ohne Plakatfarben und Dirty-Chicken-Violett (Le Livre 28.10.2026)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return []


# ---------------------------------------------------------------- Seite
# Demo-Check 21.10.2026 (wie am Schlössli): Gastgeber, Hausbuch und Besucherbuch verlinken «Die Stube» über ihren eigenen Server
# (9064/9065/9066 …/_werkzeuge/maison/). Dort fehlen die Stand-Wege (/_weiter/…), die Stube stand ohne Zahlen. Lokal geht sie deshalb immer auf ihren Server,
# und zwar unter 127.0.0.1 (die Werkstatt verlinkt localhost:9061, sonst wäre der Merker «Zur Werkbank» in einem anderen Speicher).
ZUR_STUBE = (f'<script>if(/^(127\\.0\\.0\\.1|localhost)$/.test(location.hostname)&&(location.port!=="{PORT}"||location.hostname!=="127.0.0.1"))'
             f'location.replace("http://127.0.0.1:{PORT}"+location.pathname+location.search+location.hash)</script>\n')


def seite(online, v):
    Bau.online = online
    UI.clear()
    A = wege(online)
    auf = {k: A[k]['auf'] for k in REIHE}
    web = '/index.html' if online else '/index.html'      # lokal liefert server.py die Website in der Wurzel aus

    rb = BILDER['ruhe']
    vorschau = (f'<img class="hz-bild hz-bild--ruhe an" data-vorschau="ruhe" src="img/ruhe.webp" srcset="img/ruhe-s.webp 1000w, img/ruhe.webp {rb[0]}w" '
                f'sizes="(max-width:1000px) 100vw, 46vw" width="{rb[0]}" height="{rb[1]}" alt="{e(BILDER_W[RUHE]["alt"])}" decoding="async" fetchpriority="high">')
    unter = f'<span data-vorschau="ruhe" class="an">{e(NAME)} · {e(STRASSE)}</span>'
    for i, k in enumerate(REIHE):
        n = 'schirm-' + SCHIRME[k][0]
        if n in BILDER:
            vorschau += (f'<img class="hz-bild hz-bild--schirm" data-vorschau="{i}" src="img/{n}.webp" srcset="img/{n}-s.webp 1200w, img/{n}.webp {BILDER[n][0]}w" '
                         f'sizes="(max-width:1000px) 100vw, 46vw" width="{BILDER[n][0]}" height="{BILDER[n][1]}" alt="Vorschau: {e(W[k]["name"])}" decoding="async" loading="lazy">')
            unter += f'<span data-vorschau="{i}">Vorschau · {e(W[k]["name"])}</span>'
        elif not online:
            vorschau += (f'<div class="hz-platz" data-vorschau="{i}" data-platz="{e(k)}"><div>{lamm("m-saal__z")}<b>{e(W[k]["name"])}</b>'
                         f'Die Vorschau folgt, sobald das Werkzeug vorliegt.<small>Platzhalter, nur lokal</small></div></div>')
            unter += f'<span data-vorschau="{i}">{e(W[k]["name"])} · Vorschau folgt</span>'
    insel = ''.join(f'<a class="m-insel__p" href="#{k}"><span class="rl">{e(W[k]["name"])}</span></a>' for k in REIHE)
    band = ''.join(f'<li>{e(t)}</li><li class="p" aria-hidden="true"></li>' for t in [W[k]['name'] for k in REIHE] + [NAME, 'Momo x Rudi', BAR, STRASSE, ORT])

    fb = farben()
    farbreihe = (f'<ul class="m-farben" aria-label="Die Farben des Hauses" style="--n:{len(fb)}">' +
                 ''.join(f'<li data-r style="--i:{min(i, 4)};--c:{hx}"><i></i><b>{e(nm)}</b><span>{hx.upper()}</span></li>' for i, (nm, hx) in enumerate(fb)) + '</ul>') if fb else ''

    def zwei(a, b):
        return f'<div class="m-schirme{" m-schirme--zwei" if b else ""}">{a}{b}</div>'

    saele = f'''
<section class="m-saal tapete" id="bureau">
  <div class="innen">
  {saal_kopf('bureau', 0)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('bureau', 'bureau', f'{ZENTRALE} · {W["bureau"]["name"]} · Übersicht', W['bureau']['name'] + ': die Übersicht mit allen Bereichen der Website', 0), '')}{stuecke('bureau')}</div>
    <div>
      {tafel('bureau', 1)}
      <div class="m-tafel m-tafel--stand" data-r style="--i:2;margin-top:18px">
        <div class="m-zahlen"><div class="m-zahl"><b data-zahl="bereiche">–</b><span>Bereiche</span></div><div class="m-zahl"><b data-zahl="seiten">–</b><span>Seiten</span></div></div>
        <p class="m-tafel__stand" data-stand="bureau">&nbsp;</p>
        {knopf(W['bureau']['name'] + ' öffnen', auf['bureau'], 'knopf--dunkel')}
      </div>
    </div>
  </div>
  </div>
</section>

<section class="m-saal dunkel" id="carte">
  <div class="innen">
  {saal_kopf('carte', 1)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('carte', 'carte', f'{ZENTRALE} · {W["carte"]["name"]}', W['carte']['name'] + ': links die Gerichte, rechts die Karte, wie sie gedruckt wird', 0), '')}{stuecke('carte')}</div>
    <div>
      {tafel('carte', 1)}
      <div data-r style="--i:2;margin-top:22px">
        <div class="m-zahlen"><div class="m-zahl"><b data-zahl="karten">–</b><span>Karten</span></div><div class="m-zahl"><b data-zahl="entwurf">–</b><span>Offene Entwürfe</span></div></div>
        <p style="margin-top:22px">{knopf(W['carte']['name'] + ' öffnen', auf['carte'])}</p>
      </div>
    </div>
  </div>
  </div>
</section>

<section class="m-saal papier" id="imprimerie">
  <div class="innen">
  {saal_kopf('imprimerie', 2)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('imprimerie', 'imprimerie', f'{ZENTRALE} · {W["imprimerie"]["name"]}', W['imprimerie']['name'] + ': die Übersicht mit den Vorlagen des Hauses', 0), '')}{stuecke('imprimerie')}</div>
    <div>
      {tafel('imprimerie', 1)}
      <div data-r style="--i:2;margin-top:22px">{knopf(W['imprimerie']['name'] + ' öffnen', auf['imprimerie'], 'knopf--dunkel', neu=True)}<p class="m-hinweis" data-stand="imprimerie-kurz">&nbsp;</p></div>
    </div>
  </div>
  </div>
</section>

<section class="m-saal dunkel" id="reception">
  <div class="innen">
  {saal_kopf('reception', 3)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('reception', 'reception', f'{ZENTRALE} · {W["reception"]["name"]} · Eingang', W['reception']['name'] + ': Eingang mit den Anfragen und was Gäste gefragt haben', 0), '')}{stuecke('reception')}</div>
    <div>
      {tafel('reception', 1, '<p class="m-tafel__stand" data-stand="reception">&nbsp;</p>')}
      <p data-r style="--i:2;margin-top:22px">{knopf(W['reception']['name'] + ' öffnen', auf['reception'])}</p>
    </div>
  </div>
  </div>
</section>

<section class="m-saal tapete" id="livre">
  <div class="innen">
  {saal_kopf('livre', 4)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('livre-fotos', 'livre', f'{ZENTRALE} · {W["livre"]["name"]} · Fotos', W['livre']['name'] + ': die Fotos des Hauses', 0), schirm('livre-marke', 'livre', f'{ZENTRALE} · {W["livre"]["name"]} · Logo & Dateien', W['livre']['name'] + ': Wortmarke und Farben als Dateien', 1, '(max-width:1000px) 92vw, 30vw') if 'schirm-livre-marke' in BILDER else '')}{stuecke('livre')}</div>
    <div>
      {tafel('livre', 1)}
      <div data-r style="--i:2;margin-top:22px">{knopf(W['livre']['name'] + ' öffnen', auf['livre'], 'knopf--dunkel')}<p class="m-hinweis" data-stand="livre">&nbsp;</p></div>
    </div>
  </div>
  {farbreihe}
  </div>
</section>

<section class="m-saal papier" id="registre">
  <div class="innen">
  {saal_kopf('registre', 5)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('registre', 'registre', f'{ZENTRALE} · {W["registre"]["name"]} · Beispielwerte', W['registre']['name'] + ' mit Beispielwerten: Besuche je Tag, Herkunft und die meistbesuchten Seiten', 0), '')}{stuecke('registre')}</div>
    <div>
      {tafel('registre', 1)}
      <div class="m-tafel" data-r style="--i:2;margin-top:18px">
        <div class="m-zahlen"><div class="m-zahl"><b data-zahl="reg-besuche">–</b><span>Besuche</span></div><div class="m-zahl"><b data-zahl="reg-seiten">–</b><span>Seiten angesehen</span></div><div class="m-zahl"><b data-zahl="reg-laender">–</b><span>Länder</span></div></div>
        <p class="m-hinweis" data-stand="besuche">&nbsp;</p>
        {knopf(W['registre']['name'] + ' öffnen', auf['registre'], 'knopf--dunkel')}
        <p class="m-hinweis">Gezählt ohne Cookies, nie mit Namen.</p>
      </div>
    </div>
  </div>
  <ol class="m-weg" data-r style="--n:4;margin-top:clamp(36px,4vw,56px)">
    <li style="--i:0"><b data-wg="besuche">–</b><span>Besuche</span><small data-wg="besuche-satz">auf der Website</small></li>
    <li style="--i:1"><b data-wg="fenster">–</b><span>{e(STUFE[0])}</span><small data-wg="fenster-satz">&nbsp;</small></li>
    <li style="--i:2"><b data-wg="weiter">–</b><span>{e(STUFE[1])}</span><small data-wg="weiter-satz">&nbsp;</small></li>
    <li style="--i:3"><b aria-hidden="true">{lamm("m-weg__z")}</b><span>{e(STUFE[2])}</span><small>{e(STUFE[3])}</small></li>
  </ol>
  </div>
</section>'''

    anl = [(W[k]['name'], A[k]['anl']) for k in REIHE if A[k]['anl']]
    anleitungen = ''.join(f'<a href="{e(h)}" target="_blank" rel="noopener">{e(n)}, Schritt für Schritt</a>' for n, h in anl) or \
        '<span class="m-fuss__leer">Die Anleitungen kommen mit den Werkzeugen.</span>'
    reg_auf = auf['registre']
    pw = '' if online or not geliefert('bureau') else ((stand_wege().get('bureau') or {}).get('pruefung') or '')
    pruef = knopf('Prüfung öffnen', pw, 'knopf--klein') + ' ' if pw else ''   # R04: Prüfung des Bureau, nur lokal (online nur «Neu laden»)

    # Kennzahlen im Textfluss (nicht flex): Zahl und Wort stehen so auf einer Grundlinie; getrennt mit «·» wie auf der Website (Kopf 29.10.2026)
    pkt = '<span class="rw-pkt" aria-hidden="true">·</span>'
    zeile_heute = (f'<p class="m-zeile"><span>Heute</span> <span><b data-stand="registre-heute">–</b>Besuche</span>{pkt}<span><b data-stand="registre-buchung">–</b>zum Platz</span>{pkt}'
                   + (f'<a href="{e(reg_auf)}">{e(W["registre"]["name"])} öffnen</a>' if reg_auf else f'<span>{e(W["registre"]["name"])} folgt</span>') + '</p>')
    hilfe = '<p class="m-hilfe">Ein Klick oder die Taste <kbd>1</kbd> bis <kbd>6</kbd> öffnet das Werkzeug. Darunter stellt sich jedes einzeln vor.</p>'
    rahmen = f'<figure class="hz-rahmen">{vorschau}<figcaption class="hz-unter" aria-live="polite">{unter}</figcaption></figure>'
    zt = ZENTRALE.split(' ', 1)
    titel = f'{e(zt[0])} <em>{e(zt[1])}</em>' if len(zt) == 2 else e(zt[0])
    # Kopf (neu 29.10.2026, Robert: «der header sieht scheiße aus»; M22 sinngemäss, kompakt wie bisher): links eine Zeile Wortmarke · Bar · Ort, darunter
    # «Der Tresen» als Hauptsache; rechts ein Block Datum, Gruss, Kennzahlen, dessen letzte Zeile auf der Grundlinie des Titels steht. Keine «x»-Zierden,
    # die Linie schlicht; «Beispiel» leise in der Datumszeile, nicht in den Zahlen.
    kopf = (f'<div class="rw-kopf"><div class="rw-kopf__l"><p class="rw-kopf__ort">{wortmarke("rw-kopf__wm")}{pkt}<span>{e(BAR)}</span>{pkt}<span>{e(ORT)}</span></p><h1 class="rw-titel">{titel}</h1></div>'
            f'<div class="rw-kopf__r"><p class="rw-datum"><span id="datum">&nbsp;</span><span class="rw-kopf__bsp" hidden>{pkt}Besuchszahlen als Beispiel</span></p>'
            f'<p class="rw-gruss"><span id="gruss">Guten Tag.</span> Womit fangen wir heute an?</p>{zeile_heute}</div></div>'
            f'<div class="rw-linie" aria-hidden="true"></div>')

    # Jedes Plakat der Wand trägt eine Abendfarbe aus den echten Plakaten (marke.json → abendfarben, gemessen), in der Reihenfolge der Abende
    def gefach(i, k):
        rk = RAUM[k]
        af = ABENDFARBEN[i % len(ABENDFARBEN)]
        return (f'<li class="hz-z rw-g" style="--i:{i};--pk:{af["hex"]};--pa:{af["toene"]["akzent"]}" data-abend="{e(af["name"])}"><a href="{e(auf[k] or "#" + k)}" data-taste="{i + 1}">'
                f'<span class="rw-b"><img src="img/raum-{k}.webp" srcset="img/raum-{k}-s.webp 480w, img/raum-{k}.webp {RAUM_G[0]}w" sizes="(max-width:700px) 46vw, (max-width:1000px) 30vw, 16vw" '
                f'width="{RAUM_G[0]}" height="{RAUM_G[1]}" alt="{e(BILDER_W[rk]["alt"])}" decoding="async"></span>'
                f'<span class="rw-t"><small class="rw-nr">N° {i + 1} · {e(ROLLE_K[k])}</small><b class="rw-name">{e(W[k]["name"])}</b>'
                f'<span class="rw-stand" data-stand="{k}-kurz">{e(KURZ[k])}</span></span><span class="hz-ring" aria-hidden="true">{PF}</span></a></li>')

    def fenster(i, k):
        f, pos, pos_h = FENSTER[k]; b = BILDER['fenster-' + k + '-900']
        return (f'<li class="hz-z"><a class="m-f5__k" style="--i:{i};--pos:{pos};--pos-h:{pos_h};--farbe:{FARBE[k]}" href="{e(auf[k] or "#" + k)}" data-taste="{i + 1}">'
                f'<picture><source media="(max-width:800px)" srcset="img/fenster-{k}-band.webp {BILDER["fenster-" + k + "-band"][0]}w" sizes="100vw">'
                f'<img src="img/fenster-{k}-900.webp" srcset="img/fenster-{k}-600.webp 600w, img/fenster-{k}-900.webp 900w" sizes="20vw" '
                f'width="{b[0]}" height="{b[1]}" alt="{e(BILDER_W[f]["alt"])}" decoding="async" fetchpriority="high" onload="this.classList.add(\'da\')"></picture>'
                f'<span class="m-f5__t"><span class="m-f5__w">{e(ROLLE_K[k])}</span><b>{e(W[k]["name"])}</b><small data-stand="{k}-kurz">{e(KURZ[k])}</small>'
                f'<i class="m-f5__p" aria-hidden="true">{PF}</i></span></a></li>')

    # Empfang wie beim Grand Beau-Rivage: die Fenster, darüber in der Mitte der Kopf (Wortmarke · Bar · Ort, «Der Tresen» gross, Gruss, Datum) und die
    # Zahlenzeile der Besucherliste (Taste 6). Keine «x», getrennt mit «·»; «Beispiel» leise in der Datumszeile.
    reg = auf['registre']
    zeile = (f'<p class="m-f5__zeile"><span>Heute</span><b data-stand="registre-heute">–</b>Besuche{pkt}<b data-stand="registre-buchung">–</b>zum Platz{pkt}'
             + (f'<span class="hz-z"><a href="{e(reg)}" data-taste="6">{e(W["registre"]["name"])} öffnen{PF}</a></span>' if reg else f'<span class="hz-z"><a href="#registre" data-taste="6">{e(W["registre"]["name"])}{PF}</a></span>') + '</p>')
    empfang = (f'<section class="m-empfang m-f5" id="oben">'
               f'<nav class="m-f5__reihe" aria-label="Alle Werkzeuge"><ol class="hz-tafel">{"".join(fenster(i, k) for i, k in enumerate(REIHE[:5]))}</ol></nav>'
               f'<div class="m-f5__oben"><p class="m-f5__ort">{wortmarke("m-f5__wm")}{pkt}<span>{e(BAR)}</span>{pkt}<span>{e(ORT)}</span></p>'
               f'<h1 class="m-f5__titel">{e(ZENTRALE)}</h1>'
               f'<p class="m-f5__gruss"><span id="gruss">Guten Tag.</span> Womit fangen wir heute an?</p>'
               f'<p class="m-f5__datum"><span id="datum">&nbsp;</span><span class="rw-kopf__bsp" hidden>{pkt}Besuchszahlen als Beispiel</span></p>'
               f'{zeile}</div></section>')

    vorladen = '\n'.join(f'<link rel="preload" as="image" href="img/fenster-{k}-900.webp" imagesrcset="img/fenster-{k}-600.webp 600w, img/fenster-{k}-900.webp 900w" '
                         f'imagesizes="20vw" media="(min-width:801px)" fetchpriority="high">\n'
                         f'<link rel="preload" as="image" href="img/fenster-{k}-band.webp" media="(max-width:800px)" fetchpriority="high">' for k in REIHE[:5])
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
{'' if online else ZUR_STUBE}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(ZENTRALE)} · {e(NAME)}</title>
<meta name="description" content="Alle Werkzeuge des {e(NAME)} an einem Ort: {', '.join(W[k]['name'] for k in REIHE)}.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#16151A">
<link rel="icon" href="img/zeichen.svg" type="image/svg+xml">
<link rel="stylesheet" href="maison.css?v={v['maison.css']}">
{vorladen}
<script src="fehler.js?v={v['fehler.js']}"></script>
</head>
<body class="ma">
<div class="m-tuer" id="tuer" role="alert" hidden><p class="m-tuer__t">{e(ZENTRALE)} startet nicht.</p><p id="tuer-t">&nbsp;</p>{pruef}<a class="knopf knopf--klein" href="">Neu laden<i>{PF}</i></a></div>

<header class="m-oben">
  <a class="knopf knopf--klein m-oben__ecke m-oben__ecke--l" href="#fuss">Anleitungen<i>{PF}</i></a>
  <nav class="m-insel" aria-label="Werkzeuge">
    <a class="m-ecke" href="#oben"><span class="m-ecke__ring">{lamm("m-ecke__z")}</span><span class="m-ecke__t"><b>{e(ZENTRALE)}</b><small>Alle Werkzeuge · {e(NAME)}</small></span></a>
    <span class="m-insel__wege">{insel}</span>
  </nav>
  <a class="knopf knopf--klein m-oben__ecke" href="{web}" target="_blank" rel="noopener">Website ansehen<i>{PF}</i></a>
</header>

<main>
{empfang}

<div class="m-band" data-laufband aria-hidden="true"><ul>{band}{band}</ul></div>
{saele}
</main>

<footer class="m-fuss tapete" id="fuss">
  <div class="m-fuss__platte" data-r>
    <div class="m-fuss__marke">{wortmarke("m-fuss__wm")}<b>Momo x Rudi</b></div>
    <div class="m-fuss__spalte"><p class="m-fuss__k">Die Abende</p><p>{e(NAME)} in der Bar <span class="m-nb">{e(BAR)}</span></p><p>{e(STRASSE)}, <span class="m-nb">{e(PLZ_ORT)}</span></p><a href="{web}" target="_blank" rel="noopener">Website ansehen</a></div>
    <div class="m-fuss__spalte"><p class="m-fuss__k">Anleitungen</p>{anleitungen}</div>
    <div class="m-fuss__spalte"><p class="m-fuss__k">Fragen</p><p>Robert Reff · Tasty Studios</p><p>robert@tasty-studios.de</p></div>
  </div>
</footer>

<script type="application/json" id="maison-wege">{json.dumps({k: A[k]['stand'] for k in REIHE})}</script>
<script type="application/json" id="maison-beispiel">{json.dumps([k for k in REIHE if (stand_wege().get(k) or {}).get('beispiel')])}</script>
<script src="maison.js?v={v['maison.js']}"></script>
<script src="zur-werkbank.js?v={v['zur-werkbank.js']}" defer data-zw></script>
<script src="rundgang.js?v={v['rundgang.js']}" defer data-werkzeug="maison"></script>
</body>
</html>
'''


def knoepfe():
    """Jeder «Knopf-Name» aus den Tafeln muss im Code des Werkzeugs vorkommen (M20). Ordner aus stand_wege.json → code, sonst _werkzeuge/<werkzeug>."""
    fehlt = []
    sw = stand_wege()
    for k, n in sorted(set(UI)):
        code = (sw.get(k) or {}).get('code') or [os.path.join(WZ, k)]
        n = html.unescape(n)
        gefunden = False
        for o in code:
            for wurzel, _, dateien in os.walk(os.path.expanduser(o)):
                if any(t in wurzel for t in ('/online', '/pruefung', '/node_modules', '/_qa', '/_sicherung')):
                    continue
                for d in dateien:
                    if d.endswith(('.js', '.html', '.py')):
                        try:
                            if n.lower() in open(os.path.join(wurzel, d), encoding='utf-8', errors='ignore').read().lower():
                                gefunden = True; break
                        except OSError:
                            pass
                if gefunden:
                    break
            if gefunden:
                break
        if not gefunden:
            fehlt.append(f'{W[k]["name"]}: «{n}»')
    return fehlt


FEHLER_JS = r'''document.documentElement.classList.add('js');   /* Bewegung nur mit Skript; als Datei statt eingebettet (Sicherheitsregel online) */
/* Fehlermelder (R03), vor allem anderen: Skriptfehler in den Browser (culinarium_werkzeuge_fehler) und an den Server-Teil (studio/api/fehler, wenn es ihn gibt).
   Netzfehler nie melden, höchstens 20 je Seite, eigener Fehlschlag wird nicht erneut gemeldet. */
(function(){var zahl=0;function merk(t){t=String(t);window.MAISON_FEHLER=t;if(++zahl>20||/Load failed|access control|abort|NetworkError|Failed to fetch/i.test(t))return;
try{var a=JSON.parse(localStorage.getItem('culinarium_werkzeuge_fehler')||'[]');a.unshift({zeit:new Date().toISOString(),art:'maison',text:('Zentrale: '+t).slice(0,400),ort:location.pathname});localStorage.setItem('culinarium_werkzeuge_fehler',JSON.stringify(a.slice(0,30)))}catch(e){}
try{fetch('/studio/api/fehler',{method:'POST',headers:{'Content-Type':'application/json','X-Studio':'1'},body:JSON.stringify({text:('Zentrale · '+t).slice(0,600)}),keepalive:true}).catch(function(){})}catch(e){}}
window.addEventListener('error',function(e){if(e.target&&e.target.tagName==='SCRIPT'){window.MAISON_FEHLER='Die Datei '+e.target.getAttribute('src').split('?')[0]+' liess sich nicht laden.';return}merk((e.message||'Fehler')+' · '+(e.filename||'').split('/').pop()+':'+(e.lineno||''))},true);
window.addEventListener('unhandledrejection',function(e){merk('Versprechen: '+((e.reason&&e.reason.message)||e.reason))});
/* Startfehler-Tür (R04): ist maison.js beim Laden nicht durchgelaufen, sagt die Seite es und zeigt alles ohne Bewegung. Wache nach 12 s. */
function tuer(){if(window.MAISON_BEREIT)return;var t=document.getElementById('tuer');if(!t||!t.hidden)return;
document.documentElement.classList.remove('js');document.getElementById('tuer-t').textContent=window.MAISON_FEHLER||'Das Programm der Seite ist nicht durchgelaufen.';t.hidden=false}
window.addEventListener('load',tuer);setTimeout(tuer,12000);})();
'''


def rundgang():
    s = open(os.path.join(QUELLE, 'rundgang-vorlage.js'), encoding='utf-8').read()
    a = s.index('  var GAENGE = {'); b = s.index('\n  };', a) + 4
    namen = ', '.join(W[k]['name'] for k in REIHE)
    gang = f'''  var GAENGE = {{
    maison: {{ name: '{ZENTRALE}', schritte: [
      {{ ziel: ['.m-f5__titel', '#oben'], oben: true, titel: 'Das ist {ZENTRALE}',
        text: 'Der Eingang zu allen Werkzeugen des Culinarium. Von hier aus pflegst du Website, Menüs mit Drinks, Plakate, den Chat und die Marke selbst.' }},
      {{ ziel: ['.hz-z:first-child a', '.hz-tafel'], titel: 'Ein Fenster je Werkzeug',
        text: '{namen}. Darunter steht, was dort gerade ansteht.' }},
      {{ ziel: ['.m-f5__zeile'], titel: 'Heute auf der Website',
        text: 'Wer heute auf der Website war und wer von dort weiter zur Reservierung ging. Ein Klick öffnet die ganze Liste.' }},
      {{ ziel: ['.m-insel', '.m-oben'], oben: true, titel: 'Immer erreichbar',
        text: 'Ein Klick auf diese Leiste bringt dich von überall zurück zu den Werkzeugen. Aus jedem Werkzeug kommst du hierher zurück.' }},
      {{ ziel: ['#bureau .m-saal__kopf', '#bureau'], titel: 'Jedes Werkzeug stellt sich vor',
        text: 'Weiter unten zeigt jedes Werkzeug, was es für das Culinarium tut, mit Bildern aus dem Werkzeug selbst.' }}
    ] }}
  }};'''
    s = s[:a] + gang + s[b:]
    s = s.replace("'rundgang-bg-'", "'rundgang-culinarium-'")
    s = s.replace('font:600 26px/1.1 "Barlow Semi","Arial Narrow",sans-serif', 'font:340 27px/1.12 Fraunces,Georgia,serif')
    s = s.replace('font:600 18px/1 "Barlow Semi","Arial Narrow",sans-serif', 'font:340 18px/1 Fraunces,Georgia,serif')
    s = s.replace('"Barlow Semi","Arial Narrow",sans-serif', 'Fraunces,Georgia,serif')
    for alt, neu in (('#2c3136', '#1C1B21'), ('#485056', '#3A3845'), ('#1d2224', '#16151A'), ('#7c8386', '#8a8592'), ('#e9ecec', '#FAF4F4'),
                     ('#d6bb96', '#F5A689'), ('#b7a27a', '#EF7649'), ('#e3cd98', '#F5A689'), ('227,205,152', '245,166,137'), ('#f7e9c6', '#FBD9CB'),
                     ('#b99a5c', '#EF7649'), ('#fffdf9', '#FFFCFB'), ('#f7f1e5', '#FAF4F4'), ('#f4ecdc', '#FAF4F4'), ('210,191,152', '245,166,137'),
                     ('130,108,53', '177,87,54'), ('10,12,22', '15,14,19'), ('10,13,26', '15,14,19'), ('26,29,40', '22,21,26'), ('27,32,51', '22,21,26')):
        s = s.replace(alt, neu)
    s = re.sub(r'^/\*[^\n]*\*/\n', '', s, count=1)
    if re.search(r'Barlow|Cormorant|Cinzel|Gasterntal|Fenster ist|#2c3136|#485056', s):
        raise SystemExit('rundgang.js: Angabe der Vorlage übrig')
    return f'/* Rundgang (R18, M11): Kopie des Werkzeugs der Häuser, Gang für {ZENTRALE} des {NAME}; gebaut von _werkzeuge/maison/bau.py */\n' + s


def zur_werkbank():
    s = open(os.path.join(QUELLE, 'zur-werkbank-vorlage.js'), encoding='utf-8').read()
    s = re.sub(r'^/\*[^\n]*Gasterntal[^\n]*\*/\n', '', s)
    if "var SCHL = 'bg-wb';" not in s:
        raise SystemExit('zur-werkbank.js: Schlüssel nicht gefunden')
    s = s.replace("var SCHL = 'bg-wb';", "var SCHL = 'culinarium-wb';").replace('«bg-wb»', '«culinarium-wb»')
    s = s.replace('linear-gradient(180deg,#485056,#1d2224)', 'linear-gradient(180deg,#3A3845,#16151A)')
    return f'/* «Zur Werkbank» (R19) · {ZENTRALE} des {NAME}: Kopie des Bausteins der Häuser, Schlüssel des Hauses «culinarium-wb». Gebaut von bau.py. */\n' + s


def ohne_fremde(t):
    """Angaben anderer Häuser gehen nicht in die Ausgabe (F29)."""
    m = re.search(r'.{0,40}(?:Rivage|\bgbr\b|Carlton|Interlaken|Doldenhorn|Ruedihus|Gasterntal|Kandersteg|Selden|Schlössli|Bottighofen|gastronovi|Hafen|Seehimmel|Barlow|Cormorant|Cinzel|\bbg-wb\b|schloessli|Sch(?:ä|ae)fli|Wigoltingen|Kuchler|Maeder|Zurbriggen|Zenchef|Petrona|Riegel|Lamm).{0,40}', t, re.I | re.S)
    if m:
        raise SystemExit('Angabe eines anderen Hauses in der Ausgabe: ' + m.group(0))
    return t


def baue():
    teile = {
        'maison.css': open(os.path.join(QUELLE, 'maison.css'), encoding='utf-8').read(),
        'maison.js': open(os.path.join(QUELLE, 'maison.js'), encoding='utf-8').read(),
        'rundgang.js': rundgang(),
        'fehler.js': FEHLER_JS,
        'zur-werkbank.js': zur_werkbank(),
    }
    v = {n: hashlib.sha1(t.encode()).hexdigest()[:10] for n, t in teile.items()}   # M20: Fassung aus dem Inhalt
    for online in (False, True):
        ziel = os.path.join(HIER, 'online') if online else HIER
        os.makedirs(ziel, exist_ok=True)
        bilder(ziel)
        open(os.path.join(ziel, 'img', 'zeichen.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{LAMM_VB}"><rect x="-3" y="-3" width="46" height="48" rx="10" fill="#16151A"/>{LAMM.replace("<path ", "<path fill=\'#EF7649\' ")}</svg>')
        for n, t in teile.items():
            open(os.path.join(ziel, n), 'w', encoding='utf-8').write(ohne_fremde(t) if n != 'zur-werkbank.js' else t)
        s = ohne_fremde(seite(online, v))
        if online and re.search(r'localhost|127\.0\.0\.1|data-platz|/_weiter/', s):
            raise SystemExit('Online-Fassung enthält localhost oder Platzhalter')
        open(os.path.join(ziel, 'index.html'), 'w', encoding='utf-8').write(s)
    fk = knoepfe()
    os.makedirs(os.path.join(HIER, 'pruefung'), exist_ok=True)
    json.dump({k: dict(teil=TEIL[k], da=geliefert(k), adresse=wege(False)[k]['auf']) for k in REIHE},
              open(os.path.join(HIER, 'pruefung', 'adressen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{ZENTRALE} gebaut: _werkzeuge/maison/index.html + online/index.html · {len([b for b in BILDER if b.startswith("schirm")])} Bildschirme')
    print('  vorliegend:', ', '.join(f'{W[k]["name"]} {"ja" if geliefert(k) else "–"}' for k in REIHE))
    if FEHLT:
        print('  noch ohne Bildschirm:', ', '.join(FEHLT))
    if fk:
        print('  Knopf-Namen nicht im Code gefunden:', '; '.join(fk))


if __name__ == '__main__':
    baue()
