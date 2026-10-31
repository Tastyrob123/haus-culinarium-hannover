#!/usr/bin/env python3
"""Werkbank-Kit, gemeinsamer Kern für alle Häuser.

Das Kit baut zu einer fertigen Website das ganze Werkbank-Paket (Master «Website-Bau», Abschnitt 5a):
Werkbank, Unterlagen, Drucksachen, Etiketten (oder ihr Gegenstück), Feed, Material.
Vorbild und Herkunft: `Carlton-Europe Interlaken/_werkbank/`. Hier ist dasselbe so gebaut, dass es je Haus nur
noch eine Datei mit Inhalt braucht: `<Projekt>/_werkbank/haus.py` (+ `papier.py`, `satz_daten.py`, `feed_daten.py`).

Aufruf jedes Werkzeugs:  python3 ~/Desktop/Website-Projekte/_Werkbank-Kit/<werkzeug>.py "<Projektordner>"
Reihenfolge:             alles.sh "<Projektordner>"   (nennt jeden Schritt)

Die Website des Hauses wird nie angefasst. Alles Eigene liegt in werkbank/, unterlagen/, drucksachen/,
<etiketten>/, feed/, material/ und _werkbank/."""
import base64, colorsys, datetime, html, io, json, os, re, sys
from PIL import Image

KIT = os.path.dirname(os.path.abspath(__file__))


def _projekt():
    for a in sys.argv[1:]:
        if os.path.isdir(a) and os.path.exists(os.path.join(a, '_werkbank', 'haus.py')):
            return os.path.abspath(a)
    if os.environ.get('HAUS'):
        return os.path.abspath(os.environ['HAUS'])
    if os.path.exists(os.path.join(os.getcwd(), '_werkbank', 'haus.py')):
        return os.getcwd()
    raise SystemExit('Projektordner fehlt: python3 <werkzeug>.py "<Projektordner>"')


ROOT = _projekt()
W = os.path.join(ROOT, '_werkbank')
sys.path.insert(0, W)
import haus as H  # noqa: E402

e = html.escape
STAND = datetime.date.today().strftime('%d.%m.%Y')
BASE = f'http://127.0.0.1:{H.PORT}/'
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
LI = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg>'
RE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>'
ZAHL = {1: 'Ein', 2: 'Zwei', 3: 'Drei', 4: 'Vier', 5: 'Fünf', 6: 'Sechs', 7: 'Sieben', 8: 'Acht', 9: 'Neun', 10: 'Zehn', 11: 'Elf', 12: 'Zwölf',
        13: 'Dreizehn', 14: 'Vierzehn', 15: 'Fünfzehn', 16: 'Sechzehn', 17: 'Siebzehn', 18: 'Achtzehn', 19: 'Neunzehn', 20: 'Zwanzig', 30: 'Dreissig'}
zahl = lambda n: ZAHL.get(n, str(n))


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('ü', 'ue').replace('ä', 'ae').replace('ö', 'oe').replace('ß', 'ss')).strip('-')


def lies(name, ersatz=None):
    p = os.path.join(W, name)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else ersatz


def schreib(pfad, text):
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    open(pfad, 'w', encoding='utf-8').write(text)


# ------------------------------------------------------------------ Zeichen des Hauses
# H.ZEICHEN = (viewBox, innen)   kleines Zeichen (Leiste, Trenner)      H.WORT = (viewBox, innen) Schriftzug / Wortmarke
def zeichen(kl=''):
    vb, innen = H.ZEICHEN
    return f'<svg{f" class={chr(34)}{kl}{chr(34)}" if kl else ""} viewBox="{vb}" aria-hidden="true" fill="currentColor">{innen}</svg>'


def wortmarke(kl=''):
    vb, innen = H.WORT
    return f'<svg{f" class={chr(34)}{kl}{chr(34)}" if kl else ""} viewBox="{vb}" role="img" aria-label="{e(H.NAME)}" fill="currentColor">{innen}</svg>'


from hilfen import svg_innen  # noqa: E402,F401


# ------------------------------------------------------------------ Bilder
def webp(quelle, ziel, breite, q=78, dunkel=None, schnitt=None, lage=(.5, .5)):
    """Schreibt ein WebP und gibt (b, h) zurück. schnitt = Seitenverhältnis b/h, lage = Bildmitte 0..1."""
    im = quelle if isinstance(quelle, Image.Image) else Image.open(quelle)
    if im.mode not in ('RGB', 'RGBA'):
        im = im.convert('RGB')
    if schnitt:
        w, h = im.size
        if w / h > schnitt:
            nw = round(h * schnitt); x0 = round(max(0, min(w - nw, w * lage[0] - nw / 2))); im = im.crop((x0, 0, x0 + nw, h))
        else:
            nh = round(w / schnitt); y0 = round(max(0, min(h - nh, h * lage[1] - nh / 2))); im = im.crop((0, y0, w, y0 + nh))
    if im.width > breite:
        im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
    if dunkel:  # das Dunkel steckt im Bild, damit nichts Durchscheinendes darüber liegen muss
        f, anteil = dunkel
        r, g, b = (int(H.FARBEN['nacht'][i:i + 2], 16) for i in (1, 3, 5))
        im = Image.blend(im.convert('RGB'), Image.new('RGB', im.size, (r, g, b)), f)
        if anteil:
            oben = Image.new('RGB', im.size, (r, g, b)); mask = Image.new('L', im.size, 0); px = mask.load()
            for y in range(im.height):
                t = max(0, (y / im.height - (1 - anteil - .25)) / (anteil + .25))
                v = int(255 * min(1, t) ** 1.4 * .86)
                for x in range(im.width):
                    px[x, y] = v
            im = Image.composite(oben, im, mask)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    im.save(ziel, 'WEBP', quality=q, method=5)
    # kleines echtes Abbild (40 px, um 1 KB) als Hintergrund hinter dem Foto: nie ein dunkler Kasten, bis das Foto da ist (Robert 10.10.2026)
    # Freigestellte Bilder (Aufkleber, Objekte) bekommen kein Abbild: es wäre ein dunkles Rechteck um die Form (Robert 12.10.2026, Kofferaufkleber)
    if im.mode == 'RGBA' and im.getchannel('A').getextrema()[0] < 255:
        VORAB.pop(os.path.splitext(os.path.basename(ziel))[0], None)
        FREI.add(os.path.splitext(os.path.basename(ziel))[0])
        return im.size
    k = im.convert('RGB').resize((40, max(1, round(im.height * 40 / im.width))), Image.LANCZOS)
    b = io.BytesIO(); k.save(b, 'WEBP', quality=42, method=6)
    VORAB[os.path.splitext(os.path.basename(ziel))[0]] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    return im.size


VORAB = {}
FREI = set()   # freigestellte Bilder: Schatten folgt der Form, nicht dem Rechteck


def qr_svg(url, farbe=None, label='QR-Code zur Zimmermappe'):
    """QR-Code als SVG in der Tinte des Hauses, ohne Rand (Karte zur Zimmermappe)."""
    import qrcode, qrcode.image.svg
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    t = img.to_string(encoding='unicode')
    t = re.sub(r'<\?xml[^>]*>', '', t).strip()
    t = re.sub(r'<svg ', f'<svg role="img" aria-label="{e(label)}" ', t, count=1)
    return re.sub(r'<path ', f'<path fill="{farbe or H.FARBEN["tinte"]}" ', t, count=1)


def hausbild(key):
    """Ein Foto der Website des Hauses (assets/img), grösste Fassung. Schlüssel dürfen auch volle Pfade sein."""
    if os.path.isabs(key) and os.path.exists(key):
        return key
    A = os.path.join(ROOT, 'assets', 'img')
    for n in (key + '-l.webp', key + '.webp', key + '-m.webp', key + '-s.webp', key):
        if os.path.exists(os.path.join(A, n)):
            return os.path.join(A, n)
    q = os.path.join(ROOT, key)
    if os.path.exists(q):
        return q
    raise FileNotFoundError(key)


# ------------------------------------------------------------------ Farben und Schriften: die Gestaltung des Carlton auf das Haus umrechnen
_CE = dict(nacht='#06142b', navy='#0b1f40', gold='#dcc68f', papier='#f4ecdc')   # Bezugsfarben der Vorlage


def _hls(hexa):
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return colorsys.rgb_to_hls(r, g, b)


def _um(r, g, b):
    """Eine Farbe der Vorlage → Farbe des Hauses. Blau-Familie → dunkle Töne, Creme → Papier, Gold/Messing → Betonung."""
    F = H.FARBEN
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    grad = h * 360
    if s < .09 or l > .985 or l < .012:
        return r, g, b
    if 195 <= grad <= 248:
        zh, zl, zs = _hls(F['navy']); qh, ql, qs = _hls(_CE['navy'])
        nh, nl, ns = zh, min(.97, l * zl / ql), min(1, s * zs / qs)
        if l < .12:      # die tiefsten Töne richten sich nach der Nacht des Hauses
            th, tl, ts = _hls(F['nacht']); uh, ul, us = _hls(_CE['nacht'])
            nl, ns = l * tl / ul, min(1, s * ts / us)
    elif 24 <= grad <= 62:
        if l >= .8:
            zh, zl, zs = _hls(F['papier']); qh, ql, qs = _hls(_CE['papier'])
            nh, ns = zh, min(1, s * zs / max(qs, .01))
            nl = 1 - (1 - l) * (1 - zl) / (1 - ql)
        else:
            zh, zl, zs = _hls(F['gold']); qh, ql, qs = _hls(_CE['gold'])
            nh, nl, ns = zh, min(.95, l * zl / ql), min(1, s * zs / qs)
    else:
        return r, g, b
    nr, ng, nb = colorsys.hls_to_rgb(nh, max(0, min(1, nl)), max(0, min(1, ns)))
    return round(nr * 255), round(ng * 255), round(nb * 255)


def faerbe(css):
    def hexf(m):
        x = m.group(1)
        if len(x) == 3:
            x = ''.join(c * 2 for c in x)
        if len(x) != 6:
            return m.group(0)
        r, g, b = (int(x[i:i + 2], 16) for i in (0, 2, 4))
        return '#%02x%02x%02x' % _um(r, g, b)
    css = re.sub(r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b', hexf, css)
    css = re.sub(r'(rgba?)\((\d+),(\d+),(\d+)', lambda m: '%s(%d,%d,%d' % ((m.group(1),) + _um(int(m.group(2)), int(m.group(3)), int(m.group(4)))), css)
    return css


def schriften_css(pfad='fonts/'):
    """@font-face der Werkbank. H.SCHRIFT = dict(titel=(Familie, Datei, Gewicht-Angabe), sans=…, mono=…, ersatz=…)"""
    t = H.SCHRIFT['titel']
    return (f"@font-face{{font-family:'{t[0]}';font-style:normal;font-weight:400 700;font-display:swap;src:url('{pfad}{t[1]}') format('woff2')}}\n"
            f"@font-face{{font-family:'Instrument Sans';font-style:normal;font-weight:400 600;font-display:swap;src:url('{pfad}InstrumentSans-normal-400_600.woff2') format('woff2')}}\n"
            f"@font-face{{font-family:'DM Mono';font-style:normal;font-weight:400;font-display:swap;src:url('{pfad}DMMono-normal-400.woff2') format('woff2')}}\n"
            f"@font-face{{font-family:'Titel Ersatz';src:{H.SCHRIFT.get('ersatz', 'local(Georgia)')}}}\n"
            "@font-face{font-family:'Sans Ersatz';src:local('Arial');size-adjust:99%}\n")


def druckschrift_css(pfad='../fonts/'):
    """Feste TrueType-Schnitte für alles, was gedruckt oder als Bild gerendert wird (schriften.py legt sie nach _werkbank/fonts)."""
    alle = list(H.DRUCKSCHRIFT) + [('Instrument Sans', 400, 'InstrumentSans-Regular.ttf'), ('Instrument Sans', 500, 'InstrumentSans-Medium.ttf'), ('Instrument Sans', 600, 'InstrumentSans-SemiBold.ttf'), ('DM Mono', 400, 'DMMono-Regular.ttf')]
    return ''.join(f"@font-face{{font-family:'{fam}';font-style:{'italic' if str(g).endswith('i') else 'normal'};font-weight:{str(g).rstrip('i')};src:url('{pfad}{d}') format('truetype')}}\n" for fam, g, d in alle)


def wurzel_css():
    F = H.FARBEN
    t = H.SCHRIFT['titel']
    return (':root{\n'
            f"  --nacht:{F['nacht']}; --tief:{F['tief']}; --navy:{F['navy']}; --blau:{F['blau']}; --papier:{F['papier']}; --creme:{F['creme']}; --weiss:{F['weiss']}; --gold:{F['gold']}; --messing:{F['messing']}; --taupe:{F['taupe']}; --tinte:{F['tinte']}; --punkt:{F.get('punkt', F['gold'])}; --rot:{F.get('rot', F.get('punkt', F['gold']))};\n"
            f"  --serif:'{t[0]}','Titel Ersatz',{H.SCHRIFT.get('titel_folge', 'Georgia,serif')};\n"
            "  --sans:'Instrument Sans','Sans Ersatz',system-ui,-apple-system,'Segoe UI',sans-serif;\n"
            "  --mono:'DM Mono',ui-monospace,'SF Mono',Menlo,monospace;\n"
            "  --e1:cubic-bezier(.16,1,.3,1); --e2:cubic-bezier(.32,.72,0,1); --e3:cubic-bezier(.34,1.3,.5,1);\n"
            "  --rand:clamp(20px,4.6vw,76px); --max:1480px; --abschnitt:clamp(92px,10.6vw,172px); --rund:clamp(26px,3.4vw,52px);\n"
            f"  --muster:{'url(muster.webp)' if getattr(H, 'MUSTER_BILD', None) else H.MUSTER}; --musterb:{H.MUSTER_B};\n"
            '}\n')


def gestaltung():
    """werkbank.css + seiten.css des Kits, umgerechnet auf Farben, Schriften und Muster des Hauses → werkbank/."""
    ziel = os.path.join(ROOT, 'werkbank')
    os.makedirs(os.path.join(ziel, 'fonts'), exist_ok=True)
    css = open(os.path.join(KIT, 'werkbank.css'), encoding='utf-8').read()
    kopf_ende = css.index('*,*::before,*::after{box-sizing:border-box}')
    rest = css[kopf_ende:]
    rest = rest.replace('url(../assets/img/tapete-navy.webp)', 'var(--muster)').replace('/1100px auto', '/var(--musterb) auto').replace('background-size:1100px auto', 'background-size:var(--musterb) auto')
    rest = faerbe(rest)
    if getattr(H, 'MUSTER_BILD', None):   # das Muster als Bildkachel (billiger beim Scrollen als ein verwickelter Pfad); im Druck bleibt es Vektor
        import shutil as _sh
        _sh.copy2(os.path.join(ROOT, H.MUSTER_BILD), os.path.join(ziel, 'muster.webp'))
        if getattr(H, 'MUSTER_DAEMPFUNG', None):   # Tapete leiser: das Ornament rückt zur Grundfarbe hin (Robert 11.10.2026, Grand Beau-Rivage)
            from PIL import Image as _I
            import numpy as _np
            _m = _I.open(os.path.join(ziel, 'muster.webp'))
            if _m.mode in ('RGBA', 'LA'):   # durchsichtige Kachel: nur die Deckkraft des Ornaments senken
                _a = _np.asarray(_m.convert('RGBA'), _np.float32).copy(); _a[..., 3] *= H.MUSTER_DAEMPFUNG
                _I.fromarray(_a.astype(_np.uint8), 'RGBA').save(os.path.join(ziel, 'muster.webp'), 'WEBP', quality=90)
            else:
                _a = _np.asarray(_m.convert('RGB'), _np.float32); _g = _np.median(_a.reshape(-1, 3), axis=0)
                _I.fromarray(_np.clip(_g + (_a - _g) * H.MUSTER_DAEMPFUNG, 0, 255).astype(_np.uint8)).save(os.path.join(ziel, 'muster.webp'), 'WEBP', quality=88)
    kopf = f'/* Werkbank {H.NAME}. Aufbau aus dem Werkbank-Kit (Vorlage Carlton-Europe), Farben, Schrift, Muster und Auftakt vom Haus.\n   Bewegt wird nur über transform und opacity, der Scroll bleibt nativ. */\n'
    schreib(os.path.join(ziel, 'werkbank.css'), kopf + schriften_css() + wurzel_css() + rest + '\n/* ---------- Eigenes des Hauses ---------- */\n' + getattr(H, 'CSS', ''))
    s = open(os.path.join(KIT, 'seiten.css'), encoding='utf-8').read()
    s = s.replace('url(../assets/img/tapete-navy.webp)', 'var(--muster)').replace('/1100px auto', '/var(--musterb) auto')
    schreib(os.path.join(ziel, 'seiten.css'), faerbe(s) + getattr(H, 'CSS_SEITEN', ''))
    js = open(os.path.join(KIT, 'werkbank.js'), encoding='utf-8').read().replace("'carlton-europe / '", "'" + H.KURZ + " / '")
    schreib(os.path.join(ziel, 'werkbank.js'), js)
    import shutil
    for f in {H.SCHRIFT['titel'][1], 'InstrumentSans-normal-400_600.woff2', 'DMMono-normal-400.woff2'} | set(getattr(H, 'SCHRIFT_MEHR', [])):
        q = os.path.join(ROOT, 'assets', 'fonts', f)
        if os.path.exists(q):
            shutil.copy2(q, os.path.join(ziel, 'fonts', f))
        else:
            print('  Schrift fehlt:', f)


# ------------------------------------------------------------------ Bausteine der Seiten
# ------------------------------------------------------------------ Reihenfolge der Abschnitte: je Haus eigen (H.REIHENFOLGE), die Kapitelnummern folgen daraus
STANDARD_FOLGE = ['brief', 'mitgebracht', 'lauf', 'vergleich', 'ideen', 'gefuege', 'seiten', 'unterlagen', 'handschrift', 'feed', 'papier', 'material', 'dazu', 'schluss']


def folge():
    f = list(getattr(H, 'REIHENFOLGE', STANDARD_FOLGE))
    if getattr(H, 'STUDIO', None) and 'studio' not in f:   # das Studio (Kontrollpanel) kommt nach der Handschrift, sobald das Haus eines hat
        f.insert(f.index('handschrift') + 1 if 'handschrift' in f else len(f) - 2, 'studio')
    # seit 10.10.2026 (Robert, Carlton-Europe) gehören zu jeder Werkbank: «Für Ihre Gäste» nach den Seiten, «Rezeption im Chat» nach dem Studio, «Geprüft» vor dem Schluss
    if getattr(H, 'GAESTE', None) and 'gaeste' not in f:
        f.insert(f.index('seiten') + 1 if 'seiten' in f else len(f) - 2, 'gaeste')
    if getattr(H, 'REZEPTION', None) and 'rezeption' not in f:
        nach = 'studio' if 'studio' in f else ('handschrift' if 'handschrift' in f else None)
        f.insert(f.index(nach) + 1 if nach else len(f) - 2, 'rezeption')
    if getattr(H, 'MAILS', None) and 'mails' not in f:   # seit 11.10.2026 (Robert, Grand Beau-Rivage): die Mails an die Gäste als eigener Bereich, nach der Rezeption
        nach = next((x for x in ('rezeption', 'gaeste', 'seiten') if x in f), None)
        f.insert(f.index(nach) + 1 if nach else len(f) - 2, 'mails')
    if getattr(H, 'GEPRUEFT', None) and 'geprueft' not in f:
        f.insert(f.index('schluss') if 'schluss' in f else len(f), 'geprueft')
    for x in getattr(H, 'EIGENE', []):   # eigene Abschnitte eines Hauses, ganz in haus.py gebaut (Grand Beau-Rivage 12.10.2026: Mehrwert, zwei Häuser, Angebot)
        if x['key'] not in f:
            f.insert(f.index(x['nach']) + 1 if x['nach'] in f else (f.index('schluss') if 'schluss' in f else len(f)), x['key'])
    return f


def nr(abschnitt):
    """Kapitelnummer eines Abschnitts in der Werkbank dieses Hauses (das Laufband zählt nicht mit)."""
    f = [x for x in folge() if x != 'lauf']
    return f.index(abschnitt) + 1 if abschnitt in f else 0


def kn(text, href, klasse='', neu=False):
    return f'<a class="kn {klasse}" href="{href}"{" target=\"_blank\" rel=\"noopener\"" if neu else ""}>{text}<i>{PF}</i></a>'


def titel(zeilen, stufe='h2', klasse='t2', mehr=''):
    """Grosse Zeilen, jede fährt aus ihrer eigenen Maske hoch. Die letzte steht in der Zweitfarbe."""
    innen = ''.join(f'<span class="z"><span>{f"<em>{z}</em>" if i == len(zeilen) - 1 and len(zeilen) > 1 else z}</span></span>' for i, z in enumerate(zeilen))
    return f'<{stufe} class="{klasse} zt"{mehr}>{innen}</{stufe}>'


def kap(nr, name, mehr=''):
    return f'<p class="kap" data-a="auf"{mehr}><b>{nr:02d}</b><i></i><span>{name}</span></p>'


def kopf(nr, name, zeilen, text):
    return (f'<div class="kopfzeile"><div>{kap(nr, name)}{titel(zeilen)}</div>'
            f'<div class="lauf"><p data-a="worte">{text}</p></div></div>')


def sprite():
    vb, innen = H.ZEICHEN
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><g id="hz">{innen}</g></defs></svg>'


HZ = f'<svg class="hz" viewBox="{H.ZEICHEN[0]}" aria-hidden="true" fill="currentColor"><use href="#hz"/></svg>'


def v(datei):
    return int(os.path.getmtime(os.path.join(ROOT, 'werkbank', datei))) if os.path.exists(os.path.join(ROOT, 'werkbank', datei)) else 0


def rahmen(titel_, beschr, name, haupt, fuss_satz=None):
    """Rahmen der Unterseiten (Unterlagen, Drucksachen, Etiketten, Material)."""
    fuss_satz = fuss_satz or f'Das sind Ideen von Robert Reff, Tasty Studios, und keine offiziellen Drucksachen des Hauses. Fotos, Zeichen und Texte gehören {H.RECHTE}'
    return f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel_)} · {e(H.NAME)}</title>
<meta name="description" content="{e(beschr)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{H.FARBEN['nacht']}">
<link rel="preload" href="../werkbank/fonts/{H.SCHRIFT['titel'][1]}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../werkbank/werkbank.css?v={v('werkbank.css')}">
<link rel="stylesheet" href="../werkbank/seiten.css?v={v('seiten.css')}">
</head>
<body class="haus-{H.KURZ}">
{sprite()}
<div class="gang-linie" aria-hidden="true"></div>
<header class="leiste leiste--sofort"><div class="insel">
  <a class="insel__m" href="../werkbank/index.html">{HZ}{f"<b>{e(H.LEISTE)}</b>" if H.LEISTE else ""}<span>{e(name)}</span></a>
  <a class="glanz" href="../werkbank/index.html">Zur Werkbank{PF}</a>
</div></header>
<main>
{haupt}
</main>
<footer class="fuss fuss--kurz"><div class="in">
  <div><b>{e(name)} zum Entwurf</b><p>{fuss_satz}</p></div>
  <div class="r mono"><a href="mailto:robert@tasty-studios.de">robert@tasty-studios.de</a><span>Stand {STAND}</span></div>
</div></footer>
<script src="../werkbank/werkbank.js?v={v('werkbank.js')}"></script>
</body>
</html>
'''


if __name__ == '__main__':
    # Plan für die Node-Werkzeuge (Aufnahmen, Druck): _werkbank/plan.json
    plan = {'port': H.PORT, 'base': BASE, 'kurz': H.KURZ, 'seiten': [[s[0], s[1], s[2]] for s in H.SEITEN], 'wahl': getattr(H, 'WAHL', 'main > section'),
            'start_ms': getattr(H, 'START_MS', 5200), 'heute': getattr(H, 'HEUTE_URL', ''), 'etiketten_ordner': H.ETIKETTEN['ordner'],
            'name': H.NAME, 'gold': H.FARBEN['gold'], 'punkt': H.FARBEN.get('punkt', H.FARBEN['gold']), 'tinte': H.FARBEN['tinte'],
            'chat_frage': getattr(H, 'CHAT_FRAGE', 'Bis wann gibt es etwas zu essen?'), 'chat_frage_h': getattr(H, 'CHAT_FRAGE_H', 'Kann ich meinen Hund mitbringen?'), 'mappe': os.path.exists(os.path.join(ROOT, 'mappe.html'))}
    if getattr(H, 'STELLEN', None): plan['stellen'] = H.STELLEN   # feste Halte der Ansichten je Seite (ansicht.js), z. B. damit der Fuss mit drauf ist (Familie Maeder, 17.10.2026)
    json.dump(plan, open(os.path.join(W, 'plan.json'), 'w'), ensure_ascii=False, indent=1)
    gestaltung()
    print('Plan und Gestaltung geschrieben für', H.NAME)
