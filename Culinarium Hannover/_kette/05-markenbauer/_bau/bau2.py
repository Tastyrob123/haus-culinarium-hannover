#!/usr/bin/env python3
"""Station 05 · Markenbauer · Culinarium Hannover, 26.10.2026.

Baut das Markenbuch nach dem Muster von Le Livre des Grand Beau-Rivage, wie die Markenbücher der Luxushäuser (Monte-Moro, Castell Son Claret):
dieselbe Bauart und Bewegung (Vorlage _vorlage/gbr-markenbuch.py, gbr-marke.css, gbr-marke.js), übersetzt auf Wortmarke, C, x, Plakatband,
Farben, Schriften und Fotos dieses Hauses. Inhalte aus bau.py. Farben der Vorlage werden zu Variablen, damit Farbwelt A/B und die sechs
Abendfarben die ganze Seite umfärben (nur ein Attribut am body).
   python3 bau2.py      → marke/markenbuch.html, marke/marke.css, marke/marke.js, marke/logo-richtig-falsch/index.html
Geräte: Laptop aus Blender (geraet/laptop.png + laptop.json, Render des Grand Beau-Rivage über Monte-Moro), Bildschirm geraet/schirm/*.png
aus geraet/schirme.js; Handy aus Blender (geraet/handy_render.py), sonst ein gezeichneter Rahmen."""
import html, json, os, re, sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import bau as B  # noqa: E402

M = B.M
V = os.path.join(H, '_vorlage')
e = html.escape
F = B.F
ki = B.ki
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
PU = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v10M3.5 7.5 8 12l4.5-4.5M3 14h10"/></svg>'
A = B.WELTEN['a']['css']

# ---------------------------------------------------------------- Farben in Gruppen
GRUPPEN = [
    ('haus', 'Vom Plakat', 'Die drei Farben, die auf jedem Plakat stehen: das Band, die Schrift der Wortmarke, die doppelte Linie. Sie bleiben in jeder Farbwelt.', [
        ('warmweiss', 'Warmweiss', F['Warmweiss'], 'helle Fläche, das Band'),
        ('schiefer', 'Schiefer-Violett', F['Schiefer-Violett'], 'Schrift, Wortmarke, dunkle Fläche in A'),
        ('rahmen', 'Rahmengrau', F['Rahmengrau'], 'die doppelte Linie')]),
    ('abend', 'Die Abendfarben', 'Jedes Plakat hat seine eigene Farbe. Die Seite nimmt die des nächsten Abends als Betonung.', [
        (k, n, F[n], 'Plakat ' + dat) for k, n, a, mo, bild, dat in B.ABENDE]),
    ('bar', 'Aus der Bar', 'Gemessen an Rudis Fotos: Wand, Licht, Tisch und Klinker. Daraus die Welt B und die Tiefe der dunklen Flächen.', [
        ('putz', 'Putz', F['Putz'], 'warme helle Fläche in B'),
        ('flur', 'Flurorange', F['Flurorange'], 'nah am Orange des Plakats'),
        ('kerze', 'Kerzenlicht', F['Kerzenlicht'], 'Betonung auf Dunkel in B'),
        ('honig', 'Honig', F['Honig'], 'Betonung auf Hell in B'),
        ('schiefertisch', 'Schiefertisch', F['Schiefertisch'], 'dunkle Fläche in B'),
        ('barnacht', 'Barnacht', F['Barnacht'], 'tiefster Ton'),
        ('klinker', 'Klinker', F['Klinker'], 'Kanten und Platten in B'),
        ('campari', 'Campari', F['Campari'], 'nur als Punkt')]),
]
FK = {k: (n, h) for _, _, _, l in GRUPPEN for k, n, h, _ in l}
HERKUNFT = [
    ('plakat-2026-09', 'Das Band unter jedem Plakat', 'Plakat Mondfrau, September 2026: oben das Bild, unten das warmweisse Band mit doppelter Linie und der Wortmarke in Schiefer-Violett. Auf allen sechs Plakaten seit 2024 dieselben Töne.', ['warmweiss', 'schiefer', 'rahmen'], '50% 50%'),
    ('flur', 'Der Flur zur Bar', 'Orange gestrichen, eine Hängelampe. Das Orange liegt nah am Plakat vom Februar 2025; darum ist Orange die Abendfarbe, solange kein Termin steht.', ['flur', 'orange'], '50% 40%'),
    ('kerzen', 'Kerzen auf der Tafel', 'Das Licht der Abende. Daraus die Betonung der Welt B, auf dunkler Fläche hell und warm.', ['kerze'], '40% 70%'),
    ('ballons', 'Glasballons an der Bar', 'Sirup in Glas, Zapfhähne aus Metall. Der Honig ist die Betonung der Welt B auf hellem Grund.', ['honig'], '40% 50%'),
    ('glas-dunkel', 'Der dunkle Tisch', 'Glas auf Tischplatte, dahinter Dunkel. Tischplatte und Dunkel sind die Flächen der Welt B.', ['schiefertisch', 'barnacht'], '50% 50%'),
    ('ecke', 'Die Ecke Haasemannstraße', 'Klinker, die Schilder WILD SIDE, Bänder und Graffiti. Der Klinker liegt nah am Schiefer-Violett der Wortmarke.', ['klinker'], '50% 30%'),
]
WELT_NAMEN = {'a': 'Plakat', 'b': 'Kerzenlicht'}


def foto(key):
    p = os.path.join(M, 'bilder', key + '.jpg')
    if not os.path.exists(p): raise FileNotFoundError(key)
    return 'bilder/' + key + '.jpg'


rgb, lum, kontrast = B.rgb, B.lum, B.kontrast


def streifen(key, n=5):
    from PIL import Image
    im = Image.open(os.path.join(M, 'bilder', key + '.jpg')).convert('RGB'); im.thumbnail((360, 360))
    q = im.quantize(n, method=Image.Quantize.MEDIANCUT); pal = q.getpalette()[:n * 3]; ges = im.size[0] * im.size[1]
    t = [(c / ges, '#%02x%02x%02x' % tuple(pal[i * 3:i * 3 + 3])) for c, i in q.getcolors()]
    t.sort(key=lambda x: -lum(x[1])); return t


# ---------------------------------------------------------------- Bausteine
def zeichen(kl='', titel=''):
    lab = f' role="img" aria-label="{e(titel)}"' if titel else ' aria-hidden="true"'
    return f'<svg class="{kl}" viewBox="{B.CVB}" fill="currentColor"{lab}><use href="#c"/></svg>'


def xz(kl=''):
    return f'<svg class="{kl}" viewBox="{B.XVB}" fill="currentColor" aria-hidden="true"><use href="#x"/></svg>'


def wort(kl=''):
    return f'<svg class="{kl}" viewBox="{B.WVB}" fill="currentColor" role="img" aria-label="Culinarium"><use href="#wortmarke"/></svg>'


def zeile(kl=''):
    return f'<svg class="{kl}" viewBox="{B.ZVB}" fill="currentColor" role="img" aria-label="A unique experience by Momo x Rudi"><use href="#zeile"/></svg>'


def marke(kl=''):
    return f'<svg class="{kl}" viewBox="{B.MVB}" fill="currentColor" role="img" aria-label="Culinarium, a unique experience by Momo x Rudi"><use href="#marke"/></svg>'


def kn(text, href, kl='', neu=False, laden=False):
    zus = (' target="_blank" rel="noopener"' if neu else '') + (' download' if laden else '')
    return f'<a class="kn {kl}" href="{href}"{zus}>{ki(text)}<i>{PU if laden else PF}</i></a>'


def zeilen(liste):
    return ''.join(f'<span class="z"><span>{"<em>" + x + "</em>" if i == len(liste) - 1 and len(liste) > 1 else x}</span></span>' for i, x in enumerate(liste))


def kopf(kap, titel, lead):
    return f'''<header class="mk" data-r="kopf">
      <div><p class="mk__kap"><b>{ki(kap)}</b><i></i></p>
      <h2 class="mk__t">{zeilen(titel)}</h2></div>
      <p class="mk__lead">{lead}</p>
    </header>'''


def kachel(key, name, label, text, i, lage='50% 50%'):
    return f'''<article class="k3 k3--karte" data-r="feder" style="--i:{i}">
        <div class="k3__b"><img src="{foto(key)}" alt="{e(name)}" loading="lazy" decoding="async" style="object-position:{lage}"></div>
        <div class="k3__n"><small>{ki(label)}</small><b>{e(name)}</b><p>{text}</p></div>
      </article>'''


def chip(k):
    n, h = FK[k]
    return f'<span class="mini"><i style="background:{h}"></i>{e(n)}</span>'


def geraet(welt, i=0):
    L = json.load(open(os.path.join(M, 'geraet', 'laptop.json')))
    x, y, w, h = L['schirm']
    handy = os.path.exists(os.path.join(M, 'geraet', f'handy-{welt}.png'))
    tel = (f'<img class="ger__tel" src="geraet/handy-{welt}.png" alt="Die Probe am Handy, Farbwelt {welt.upper()}" loading="lazy" decoding="async">' if handy
           else f'<span class="ger__tel ger__tel--css"><img src="geraet/schirm/handy-{welt}.png" alt="Die Probe am Handy, Farbwelt {welt.upper()}" loading="lazy" decoding="async"></span>')
    return f'''<div class="ger" data-r="feder" style="--i:{i}">
      <div class="ger__laptop"><img class="ger__inhalt" src="geraet/schirm/laptop-{welt}.png" alt="Die Probe am Rechner, Farbwelt {welt.upper()}" loading="lazy" decoding="async" style="left:{x * 100:.3f}%;top:{y * 100:.3f}%;width:{w * 100:.3f}%;height:{h * 100:.3f}%"><img class="ger__huelle" src="geraet/laptop.png" alt="" width="{L['groesse'][0]}" height="{L['groesse'][1]}" loading="lazy" decoding="async"></div>
      {tel}
    </div>'''


# ---------------------------------------------------------------- CSS: die Vorlage des Rivage, Farben als Variablen
VORLAGE_HEX = {
    '#1b2033': 'marine', '#151a2b': 'd1', '#181c2d': 'd1', '#20263c': 'd2', '#232a43': 'd2', '#262c45': 'd3', '#171b2b': 'd1', '#141827': 'd0', '#1a1d28': 'tinte',
    '#323a58': 'aare', '#3f4767': 'aare', '#2c334d': 'blau',
    '#cdaa5c': 'gold', '#e6d2a2': 'gold', '#c9a764': 'gold', '#dcc189': 'gold', '#fbf0cf': 'gold-h2', '#f3e3b6': 'gold-h', '#ead39c': 'gold-h', '#fff7e2': 'gold-h2', '#9c7b43': 'gold-t',
    '#f9f1e1': 'papier', '#fdf5e8': 'weiss', '#eee2cc': 'creme', '#c8ba9e': 'sand', '#fdf9f1': 'weiss', '#e8dcc3': 'creme', '#e7dcc6': 'creme', '#efe4cf': 'creme', '#f7f0e3': 'papier', '#e2d2b5': 'sand',
    '#b0934f': 'taupe', '#967d40': 'akzent', '#826c35': 'taupe-tief', '#6d5a2c': 'taupe-tief', '#7a1f2b': 'rot'}
VORLAGE_RGBA = {(26, 29, 40): 'tinte', (253, 249, 241): 'weiss', (230, 210, 162): 'gold', (130, 108, 53): 'taupe-tief', (8, 9, 15): 'd0', (7, 8, 12): 'd0', (14, 17, 28): 'd0',
                (27, 32, 51): 'marine', (255, 250, 236): 'weiss', (255, 244, 222): 'weiss', (240, 227, 194): 'creme', (150, 166, 214): 'aare-h', (78, 64, 44): 'taupe-tief',
                (70, 52, 26): 'taupe-tief', (61, 42, 16): 'taupe-tief', (101, 85, 52): 'taupe-tief', (210, 191, 152): 'sand'}


def css():
    s = open(os.path.join(V, 'gbr-marke.css'), encoding='utf-8').read()
    kopf_alt = s[:s.index('@property')]
    fonts = ("@font-face{font-family:'Fraunces Soft';font-style:normal;font-weight:400 900;font-display:swap;src:url('schriften/Fraunces-Soft-600_900.woff2') format('woff2')}\n"
             "@font-face{font-family:'Urbanist';font-style:normal;font-weight:400 900;font-display:swap;src:url('schriften/Urbanist-400_900.woff2') format('woff2')}\n"
             "@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:400 600;font-display:swap;src:url('schriften/InstrumentSans-normal-400_600.woff2') format('woff2')}\n"
             "@font-face{font-family:'DM Mono';font-style:normal;font-weight:400;font-display:swap;src:url('schriften/DMMono-normal-400.woff2') format('woff2')}\n"
             "@font-face{font-family:'Titel Ersatz';src:local('Georgia');size-adjust:92%}\n")
    s = s.replace(kopf_alt, '/* Markenbuch Culinarium Hannover · Station 05 · Tasty Studios · 26.10.2026. Bauart und Bewegung wie Le Livre des Grand Beau-Rivage\n'
                            '   (Vorlage _vorlage/gbr-marke.css), wie die Markenbücher der Luxushäuser; Farben als Variablen aus farben.css (Welt A/B, sechs Abendfarben),\n'
                            '   Schriften, Zeichen und Tapete dieses Hauses. Nur transform und opacity, nativer Scroll. */\n\n' + fonts)
    root_alt = re.search(r':root\{.*?\n\}', s, re.S).group(0)
    root_neu = (B.farben_css() +
                ':root{\n  --linie:color-mix(in srgb,var(--tinte) 16%,transparent); --linie-d:color-mix(in srgb,var(--gold) 24%,transparent);\n'
                "  --serif:'Fraunces Soft','Titel Ersatz',Georgia,serif;\n  --caps:'Urbanist','Arial Black',Arial,sans-serif;\n"
                "  --sans:'Instrument Sans',system-ui,-apple-system,'Segoe UI',sans-serif;\n  --mono:'DM Mono',ui-monospace,'SF Mono',Menlo,monospace;\n"
                "  --e1:cubic-bezier(.16,1,.3,1); --e2:cubic-bezier(.32,.72,0,1); --e3:cubic-bezier(.19,1,.22,1);\n"
                "  --feder:cubic-bezier(.28,1.42,.42,1); --landen:cubic-bezier(.2,1.12,.3,1);\n"
                "  --rand:clamp(18px,5vw,96px); --max:1440px; --ab:clamp(110px,11.5vw,190px); --rund:clamp(28px,3.6vw,56px); --r:clamp(20px,2vw,28px);\n  --start:0s;\n}")
    s = s.replace(root_alt, root_neu)
    s = s.replace('url(../../assets/img/tapete-dunkel.webp)', 'var(--tap-d)').replace('url(../../assets/img/tapete-hell.webp)', 'var(--tap-h)').replace('340px auto', '224px auto')
    teile = s.split(root_neu)
    def hexv(m):
        k = VORLAGE_HEX.get(m.group(0).lower()); return f'var(--{k})' if k else m.group(0)
    def rgbav(m):
        k = VORLAGE_RGBA.get((int(m.group(1)), int(m.group(2)), int(m.group(3))))
        if not k: return m.group(0)
        return f'color-mix(in srgb,var(--{k}) {float(m.group(4)) * 100:.0f}%,transparent)'
    teile[1] = re.sub(r'rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)', rgbav, re.sub(r'#[0-9a-fA-F]{6}\b', hexv, teile[1]))
    s = root_neu.join(teile)
    s += r'''
/* ---------- Culinarium: Etiketten in Versalien mit kleinem i, kräftig wie die Zeile der Plakate ---------- */
html{font-synthesis:none}
.ki{text-transform:none}
.mk__kap,.titel__kap,.titel__ort,.leiste__k,.k3__n small,.lock__o,.her__wird>span,.r5,.prunk__z small{font-weight:800;letter-spacing:.17em}
.mk__kap b{font-weight:800}
.leiste__m b{font-weight:900;letter-spacing:.2em}
.kn{font-family:var(--caps);font-weight:800;letter-spacing:.15em}
.mk__t,h3,.k3__n b,.fenster__s,.fenster__u,.fa__n b,.anteil__b b,.fk__n,.f-a,.r1,.r2,.r3,.r4,.prunk__z b,.bau .bau__t,.pa figcaption,.laden b,.index a,.gr__s,.mini{font-weight:600}
.mk__t{font-weight:700;letter-spacing:-.018em;line-height:.96}
.mk__t em{font-weight:600}
/* ---------- Das Band statt Einkerbung (Robert 18.10.2026: keine Einkerbungen): warmweiss mit doppelter Linie, wie unter jedem Plakat ---------- */
.kerbe.kerbe{position:absolute;left:0;right:0;top:auto;bottom:0;z-index:3;max-width:none;transform:none;margin:0;border-radius:0;
  padding:clamp(11px,1vw,14px) clamp(14px,1.4vw,20px) clamp(10px,.9vw,12px);background:var(--papier);color:var(--tinte);
  box-shadow:inset 0 1px 0 var(--rahmen),inset 0 4px 0 var(--papier),inset 0 5px 0 var(--rahmen);
  font:800 clamp(.66rem,.74vw,.76rem)/1.2 var(--caps);letter-spacing:.16em;text-transform:uppercase;text-align:left;white-space:normal;text-shadow:none}
.kerbe.kerbe::before,.kerbe.kerbe::after{display:none;content:none}
.lock .kerbe.kerbe,.tap__f .kerbe.kerbe,.welt__tafel .kerbe.kerbe{text-align:center}
/* ---------- das Band als Baustein ---------- */
.band{position:relative;background:var(--papier);color:var(--tinte);box-shadow:inset 0 1px 0 var(--rahmen),inset 0 4px 0 var(--papier),inset 0 5px 0 var(--rahmen),inset 0 -1px 0 var(--rahmen),inset 0 -4px 0 var(--papier),inset 0 -5px 0 var(--rahmen)}
.band--gross{display:flex;flex-direction:column;align-items:center;gap:clamp(12px,1.2vw,18px);padding:clamp(26px,2.8vw,44px) clamp(20px,3vw,60px);border-radius:var(--r);box-shadow:inset 0 1px 0 var(--rahmen),inset 0 4px 0 var(--papier),inset 0 5px 0 var(--rahmen),inset 0 -1px 0 var(--rahmen),inset 0 -4px 0 var(--papier),inset 0 -5px 0 var(--rahmen),0 40px 60px -44px rgba(0,0,0,.6)}
.lock--papier{padding-left:0;padding-right:0}
.hinweis{display:flex;flex-wrap:wrap;align-items:center;gap:10px 22px;padding:16px clamp(18px,2vw,28px);margin-bottom:clamp(26px,3vw,44px);border-radius:var(--r);font-size:.98rem;color:var(--tinte)}
.hinweis>span:first-child{font:900 11.5px/1 var(--caps);letter-spacing:.17em;color:var(--rot)}
.titel__ph{margin-top:14px;font:800 11px/1.3 var(--caps);letter-spacing:.16em;text-transform:uppercase;color:color-mix(in srgb,var(--weiss) 70%,transparent)}
.band--voll{width:100%;margin:0;border-radius:0;box-shadow:inset 0 1px 0 var(--rahmen),inset 0 4px 0 var(--papier),inset 0 5px 0 var(--rahmen),inset 0 -1px 0 var(--rahmen),inset 0 -4px 0 var(--papier),inset 0 -5px 0 var(--rahmen)}
.band--gross svg.w{width:min(560px,100%);height:auto;color:var(--tinte)}
.band--gross svg.zl{width:min(460px,90%);height:auto;color:var(--tinte)}
/* Titelblatt: Wortmarke in Warmweiss, darunter die Zeile */
.titel__w{color:var(--papier)}
.titel__zl{display:block;width:min(720px,80vw);margin:clamp(18px,2vw,30px) auto 0;color:var(--gold)}
.titel__z svg{color:var(--gold)}
/* ---------- Fenster: kein Textschatten (wird an den Zeilenkanten abgeschnitten, Robert 26.10.2026: «da sieht man noch Schatten hinter dem Text»), dafür ein weicher Hof ohne Kante hinter dem ganzen Block ---------- */
.fenster__s,.fenster__u{text-shadow:none}
.fenster__t::before{content:'';position:absolute;left:50%;top:50%;width:min(1100px,96vw);height:190%;transform:translate(-50%,-50%);z-index:-1;pointer-events:none;
  background:radial-gradient(closest-side,color-mix(in srgb,var(--d0) 62%,transparent) 0%,color-mix(in srgb,var(--d0) 38%,transparent) 45%,transparent 100%)}
/* ---------- Welten, Geräte, Zeichen (wie Monte-Moro) ---------- */
.welt__tafel{min-height:clamp(240px,22vw,320px)}
.welten{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(22px,3vw,52px)}
.welt{display:flex;flex-direction:column;gap:18px}
.welt__k{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap}
.welt__k h3{font-size:clamp(1.7rem,2.4vw,2.5rem);line-height:1.05}
.welt__k h3 em{font-style:normal;color:var(--akzent)}
.welt__b{display:flex;gap:8px}
.welt__b i{width:34px;height:34px;border-radius:10px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.welt p{font-size:1rem;line-height:1.66;color:color-mix(in srgb,var(--tinte) 84%,transparent);max-width:52ch}
.ger{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 24%;align-items:end;gap:0}
.ger__laptop{position:relative;width:100%}
.ger__huelle{position:relative;z-index:2;width:100%;height:auto;display:block}
.ger__inhalt{position:absolute;z-index:1;object-fit:cover;object-position:50% 0;border-radius:1.8% 1.8% 0 0}
.ger__tel{position:relative;z-index:3;width:138%;margin-left:-38%;margin-bottom:-6%;height:auto;filter:drop-shadow(0 26px 22px rgba(20,16,24,.32))}
.ger__tel--css{display:block;width:30%;margin-left:-6%;margin-bottom:6%;padding:5px;border-radius:26px;background:#0b0c10;box-shadow:0 30px 40px -24px rgba(0,0,0,.6),inset 0 0 0 1px rgba(255,255,255,.08)}
.ger__tel--css img{width:100%;border-radius:21px}
.reihe5{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(14px,1.6vw,24px);margin-top:clamp(16px,1.8vw,28px)}
.zei{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;text-align:center;gap:14px;padding:clamp(22px,2.4vw,34px) 16px;border-radius:var(--r);background:var(--weiss);box-shadow:inset 0 0 0 1px var(--linie),0 30px 40px -32px rgba(20,16,24,.4)}
.zei svg,.zei img{height:clamp(54px,5.4vw,78px);width:auto;max-width:100%;color:var(--tinte)}
.zei b{font-family:var(--serif);font-weight:600;font-size:1.2rem;line-height:1.15}
.zei small{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;line-height:1.4;color:color-mix(in srgb,var(--tinte) 62%,transparent)}
.regeln--4{grid-template-columns:repeat(4,minmax(0,1fr))}
.regel--f .regel__f{position:relative}
.regel--f .regel__f::before{content:'';position:absolute;inset:0;border-radius:14px;box-shadow:inset 0 0 0 1.5px var(--rot);pointer-events:none;z-index:2}
.regel--f .regel__f::after{content:'';position:absolute;right:10px;top:10px;width:26px;height:26px;z-index:3;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'><circle cx='15' cy='15' r='15' fill='%23D44032'/><path d='M10 10l10 10M20 10L10 20' stroke='white' stroke-width='2.4' stroke-linecap='round'/></svg>") center/contain no-repeat}
.lf{width:100%;min-height:170px;display:flex;align-items:center;justify-content:center;gap:16px;border-radius:14px;overflow:hidden}
.lf svg,.lf img{height:auto}
.satz3 ul{display:grid;gap:9px} .satz3 li{position:relative;padding-left:20px;font-size:.98rem;line-height:1.5;color:color-mix(in srgb,var(--tinte) 80%,transparent)}
.satz3 li::before{content:'';position:absolute;left:0;top:.7em;width:9px;height:1.5px;background:var(--akzent)}
.satz3 .nicht li::before{background:var(--rot)}
.unter{display:grid;gap:0;border-top:1px solid var(--linie-d)}
.unter li{display:grid;grid-template-columns:minmax(150px,300px) 1fr;gap:20px;padding:18px 0;border-bottom:1px solid var(--linie-d);opacity:0;transform:translate3d(0,22px,0);transition:opacity 1s var(--e2),transform 1.3s var(--e1);transition-delay:calc(var(--i,0)*90ms)}
.da .unter li,.unter.da li{opacity:1;transform:none}
.unter b{font-family:var(--serif);font-weight:600;font-size:1.25rem;line-height:1.15} .unter span{color:color-mix(in srgb,var(--weiss) 82%,transparent);font-size:.98rem;line-height:1.55}
.wahl{display:grid;gap:0;margin-top:clamp(36px,4vw,64px);border-radius:var(--r);overflow:hidden;background:var(--weiss);box-shadow:inset 0 0 0 1px var(--linie),0 40px 60px -44px rgba(20,16,24,.5)}
.wahl__z{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(18px,3vw,48px);align-items:center;padding:clamp(18px,2vw,28px) clamp(20px,2.6vw,40px);border-bottom:1px solid var(--linie)}
.wahl__z:last-child{border-bottom:0}
.wahl__z--logo{background:var(--papier)}
.wahl__p{font-size:clamp(2.2rem,4.2vw,4.2rem);line-height:1;color:var(--tinte);white-space:nowrap;overflow:hidden}
.wahl__p svg{height:clamp(44px,4.6vw,74px);width:auto;max-width:100%}
.wahl__n{display:flex;flex-direction:column;gap:6px}
.wahl__n b{font-family:var(--mono);font-weight:400;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--tinte)}
.wahl__n em{font-style:normal;font-family:var(--caps);font-weight:800;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--akzent)}
.wahl__n span{font-size:.98rem;line-height:1.5;color:color-mix(in srgb,var(--tinte) 80%,transparent)}
.wahl__z--gewaehlt{box-shadow:inset 4px 0 0 var(--gold)}
.f-ti{font-family:'Fraunces Soft','Titel Ersatz',serif;font-weight:900} .f-gr{font-family:'Gravitas One',serif} .f-ba{font-family:'Bagel Fat One',sans-serif} .f-de{font-family:'Dela Gothic One',sans-serif}
.f-et{font-family:var(--caps);font-weight:900;letter-spacing:.1em;text-transform:uppercase}
.f-c{font-family:var(--caps);font-weight:800;letter-spacing:.12em}
.welt--nicht{opacity:.62}
.welt--gewaehlt .welt__k h3::after{content:'Gewählt';margin-left:14px;padding:5px 12px 4px;border-radius:999px;vertical-align:.35em;font:800 11px/1 var(--caps);letter-spacing:.14em;text-transform:uppercase;color:var(--weiss);background:var(--blau)}
.tap__f--hell{background:var(--papier) var(--tap-h) 50% 0/224px auto;box-shadow:inset 0 0 0 clamp(14px,1.8vw,24px) var(--sand),inset 0 0 0 calc(clamp(14px,1.8vw,24px) + 1px) color-mix(in srgb,var(--tinte) 14%,transparent),0 36px 48px -30px rgba(20,16,24,.5)}
.lock--marine .lock__w{color:var(--papier)}
.lock--quer .lock__z{width:clamp(54px,5vw,80px);color:var(--tinte)}
.lock--quer .lock__wq{width:clamp(200px,20vw,300px);height:auto;color:var(--tinte)}
.lock--groessen>div{flex-direction:row;justify-content:center;align-items:flex-end;gap:clamp(22px,3vw,52px)}
/* ---------- Die Abendfarben: sechs Plakate, ein Klick färbt das Markenbuch ---------- */
.abende{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:clamp(12px,1.4vw,20px)}
.ab-k{position:relative;display:flex;flex-direction:column;border-radius:var(--r);overflow:hidden;background:var(--papier);color:var(--tinte);text-align:left;box-shadow:0 34px 50px -36px rgba(0,0,0,.7);transition:transform .9s var(--e1)}
.ab-k:hover{transform:translateY(-4px)}
.ab-k img{width:100%;aspect-ratio:1;object-fit:cover}
.ab-k__f{height:46px;background:var(--c)}
.ab-k__n{padding:14px 16px 16px;display:flex;flex-direction:column;gap:4px}
.ab-k__n b{font-family:var(--serif);font-weight:600;font-size:1.25rem;line-height:1.1}
.ab-k__n small{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;color:color-mix(in srgb,var(--tinte) 64%,transparent)}
.ab-k[aria-pressed=true]{box-shadow:0 0 0 3px var(--gold),0 34px 50px -36px rgba(0,0,0,.7)}
.ab-k[aria-pressed=true] .ab-k__n small::after{content:' · Betonung jetzt';color:var(--akzent)}
.ab-k:focus-visible{outline:2px solid var(--gold);outline-offset:4px}
.ab-h{margin-top:clamp(22px,2.4vw,34px);text-align:center;font:800 11px/1.4 var(--caps);letter-spacing:.16em;text-transform:uppercase;color:var(--gold-h)}
/* ---------- der Bon und die Zutatenzeile als Bausteine ---------- */
.bon{background:#fff;color:#1e1d22;padding:22px 22px 24px;border-radius:6px;font:400 13px/1.75 var(--mono);box-shadow:0 40px 60px -36px rgba(0,0,0,.6);width:min(320px,100%)}
.bon__k{display:flex;flex-direction:column;align-items:center;gap:6px;padding-bottom:12px;margin-bottom:10px;border-bottom:1px dashed #b9b4b4}
.bon__k svg{width:80%;color:var(--tinte)}
.bon dl{display:grid;grid-template-columns:auto 1fr;gap:0 16px;margin:0}.bon dt{text-transform:uppercase;letter-spacing:.08em;color:#6b6770}.bon dd{margin:0;text-align:right}
.bon .summe{margin-top:10px;padding-top:10px;border-top:1px dashed #b9b4b4;display:flex;justify-content:space-between}
.bau .zutat,.zutat{font-family:var(--serif);font-weight:800;font-size:clamp(1.9rem,3.2vw,3rem)!important;line-height:.98;letter-spacing:-.012em;text-transform:uppercase;color:var(--weiss);text-align:left;margin-top:16px}
.zutat .sl{color:var(--gold);font-weight:600}
@media (max-width:1100px){.abende{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:1000px){.welten{grid-template-columns:1fr}.reihe5{grid-template-columns:repeat(2,minmax(0,1fr))}.regeln--4{grid-template-columns:repeat(2,minmax(0,1fr))}.wahl__z{grid-template-columns:1fr}}
@media (max-width:620px){.anteil .mk__kap span{display:none}.regeln--4{grid-template-columns:1fr}.unter li{grid-template-columns:1fr;gap:6px}.ger{grid-template-columns:minmax(0,1fr) 30%}.wahl__p{font-size:2.2rem}.abende{grid-template-columns:repeat(2,minmax(0,1fr))}.titel__ort{flex-wrap:wrap;justify-content:center;letter-spacing:.2em;row-gap:10px}}
'''
    open(os.path.join(M, 'marke.css'), 'w', encoding='utf-8').write(s)
    js = open(os.path.join(V, 'gbr-marke.js'), encoding='utf-8').read().replace('Markenbuch Grand Beau-Rivage', 'Markenbuch Culinarium Hannover')
    js += '''
/* Farbwelt A/B und Abendfarbe im Markenbuch umschalten: nur Attribute am body, die Farben kommen aus dem CSS */
(function(){var q=new URLSearchParams(location.search),b=document.body,w=q.get('welt'),a=q.get('abend');
if(w==='b')b.setAttribute('data-welt','b');if(a)b.setAttribute('data-abend',a);
function zeig(){var wb=b.getAttribute('data-welt')==='b',ab=b.getAttribute('data-abend');
 document.querySelectorAll('[data-welt-knopf]').forEach(function(k){k.classList.toggle('kn--linie',(k.getAttribute('data-welt-knopf')==='b')!==wb)});
 document.querySelectorAll('[data-abend-knopf]').forEach(function(k){k.setAttribute('aria-pressed',String(!wb&&k.getAttribute('data-abend-knopf')===ab))})}
document.querySelectorAll('[data-welt-knopf]').forEach(function(k){k.addEventListener('click',function(ev){ev.preventDefault();if(k.getAttribute('data-welt-knopf')==='b')b.setAttribute('data-welt','b');else b.removeAttribute('data-welt');zeig()})});
document.querySelectorAll('[data-abend-knopf]').forEach(function(k){k.addEventListener('click',function(){b.removeAttribute('data-welt');b.setAttribute('data-abend',k.getAttribute('data-abend-knopf'));zeig()})});
zeig()})();
'''
    open(os.path.join(M, 'marke.js'), 'w', encoding='utf-8').write(js)


# ---------------------------------------------------------------- Logo richtig und falsch
def logo_karten(pre=''):
    WW, SV, NA = F['Warmweiss'], F['Schiefer-Violett'], A['marine']
    def wm(farbe, st=''): return f'<svg viewBox="{B.WVB}" style="fill:{farbe};{st}" aria-hidden="true"><use href="#wortmarke"/></svg>'
    def mz(farbe, st=''): return f'<svg viewBox="{B.MVB}" style="fill:{farbe};{st}" aria-hidden="true"><use href="#marke"/></svg>'
    def cz(farbe, st=''): return f'<svg viewBox="{B.CVB}" style="fill:{farbe};{st}" aria-hidden="true"><use href="#c"/></svg>'
    band = f'background:{WW};box-shadow:inset 0 1px 0 {F["Rahmengrau"]},inset 0 4px 0 {WW},inset 0 5px 0 {F["Rahmengrau"]},inset 0 -1px 0 {F["Rahmengrau"]},inset 0 -4px 0 {WW},inset 0 -5px 0 {F["Rahmengrau"]}'
    richtig = [
        ('Auf dem Band', f'<div class="lf" style="{band};flex-direction:column;gap:10px">{mz(SV, "width:74%")}</div>', 'Die Hauptform: Wortmarke und Zeile in Schiefer-Violett auf Warmweiss, darüber und darunter die doppelte Linie. So steht sie auf jedem Plakat.'),
        ('Warmweiss auf Dunkel', f'<div class="lf tapete" style="background-color:{NA}">{mz(WW, "width:74%")}</div>', 'Auf dunkler Fläche in Warmweiss, Form unverändert, aus dem Zug der Original-Pixel.'),
        ('Die Wortmarke allein', f'<div class="lf" style="background:{WW}">{wm(SV, "width:76%")}</div>', 'Ohne Zeile, wo wenig Platz ist: in der Leiste, auf Etiketten, im Fuss.'),
        ('Das C allein', f'<div class="lf" style="background:{A["creme"]}">{cz(SV, "height:110px;width:auto")}</div>', 'Der erste Buchstabe ist das Zeichen: Leiste, Tapete, Zeichen im Browser, Stempel.'),
        ('Mindestgrösse', f'<div class="lf" style="background:{WW};flex-direction:column;gap:16px">{wm(SV, "width:120px")}<span class="mono" style="font-size:10px;color:{A["akzent"]};letter-spacing:.12em">120 PX · MIT ZEILE 220 PX</span></div>', 'Die Wortmarke allein ab 120 Pixel Breite, mit Zeile ab 220 Pixel; darunter ist die Zeile nicht mehr lesbar. Kleiner steht nur das C.'),
        ('Schutzraum', f'<div class="lf" style="background:{WW}"><div style="position:relative;padding:7%;outline:1px dashed {A["akzent"]};width:86%">{wm(SV, "width:100%")}</div></div>', 'Rundum so viel Luft wie das U in CULINARIUM breit ist. Die doppelte Linie des Bandes zählt nicht als Störung.'),
        ('Unter dem Foto', f'<div class="lf" style="background:url({pre}{foto("tafel-kerzen")}) 50% 40%/cover;flex-direction:column;justify-content:flex-end;padding:0;align-items:stretch"><div style="{band};padding:14px 18%">{wm(SV, "width:100%")}</div></div>', 'Wie auf dem Plakat: das Foto oben, das Band darunter. Die Wortmarke steht auf dem Band, nicht im Bild.'),
        ('In der Abendfarbe', f'<div class="lf" style="background:{F["Orange"]}">{wm(WW, "width:76%")}</div>', 'Auf einer vollen Abendfarbe darf die Wortmarke Warmweiss stehen, wenn der Kontrast reicht (Orange, Ochsenblut, Nachtblau, Sepia).'),
    ]
    falsch = [
        ('Gestreckt', f'<div class="lf" style="background:{WW}">{wm(SV, "width:60%;transform:scaleY(1.6)")}</div>', 'Die Proportion bleibt. Nie höher oder schmaler gezogen.'),
        ('Umgefärbt', f'<div class="lf" style="background:{WW}">{wm("#2aa198", "width:76%")}</div>', 'Nur Schiefer-Violett oder Warmweiss. Keine Abendfarbe als Schrift auf Hell, kein Verlauf.'),
        ('Mit Schatten und Glanz', f'<div class="lf" style="background:{NA}">{wm(WW, "width:76%;filter:drop-shadow(0 6px 10px rgba(0,0,0,.9)) drop-shadow(0 0 18px rgba(239,118,73,.9))")}</div>', 'Kein Schatten, kein Leuchten, kein Neon. Die Wortmarke liegt flach.'),
        ('Neu gesetzt', f'<div class="lf" style="background:{WW};font-family:var(--serif);font-weight:900;font-size:clamp(26px,2.6vw,40px);color:{SV}">CULINARIUM</div>', 'Der Name wird nie in der Titelschrift nachgeschrieben, auch nicht in Fraunces. Die Wortmarke ist eine Datei.'),
        ('Auf dem Foto', f'<div class="lf" style="background:url({pre}{foto("kerzen")}) 50% 50%/cover">{wm(WW, "width:76%")}</div>', 'Kerzen, Gesichter, Flaschen hinter den Buchstaben: unlesbar. Die Wortmarke gehört auf das Band.'),
        ('Als Schild über dem Bild', f'<div class="lf" style="background:url({pre}{foto("tresen")}) 50% 30%/cover"><div style="background:{WW};outline:2px solid {SV};outline-offset:-8px;padding:18px 22px;width:70%">{wm(SV, "width:100%")}</div></div>', 'Kein gerahmtes Schild, keine Plakette mitten im Foto. Das Band liegt unter dem Bild, über die ganze Breite.'),
        ('Zeile getrennt', f'<div class="lf" style="background:{WW};flex-direction:column;align-items:flex-start;padding:0 12%">{zeile_s(SV, "width:46%")}{wm(SV, "width:80%;margin-left:14%")}</div>', 'Die Zeile steht unter der Wortmarke, linksbündig wie im Profilbild oder auf ganzer Breite wie im Plakat; nie darüber, nie versetzt.'),
        ('Zu klein', f'<div class="lf" style="background:{WW}">{mz(SV, "width:110px")}</div>', 'Mit Zeile unter 220 Pixel ist «A UNiQUE EXPERiENCE» nicht mehr lesbar. Dann nur die Wortmarke.'),
    ]
    def karten(liste, kl):
        return ''.join(f'<div class="regel {kl}" data-r="feder" style="--i:{i % 4}"><div class="regel__f">{b}</div><h3>{e(t)}</h3><p>{e(s)}</p></div>' for i, (t, b, s) in enumerate(liste))
    return karten(richtig, 'regel--r'), karten(falsch, 'regel--f')


def zeile_s(farbe, st=''): return f'<svg viewBox="{B.ZVB}" style="fill:{farbe};{st}" aria-hidden="true"><use href="#zeile"/></svg>'


# ---------------------------------------------------------------- die Seite
def seite():
    alle = [(k, n, h, r) for _, _, _, l in GRUPPEN for k, n, h, r in l]
    n_f = len(alle)
    TD, TH = F['Schiefer-Violett'], F['Warmweiss']
    faecher = ''.join(f'''<button class="fa" type="button" data-hex="{h}" style="--c:{h};--t:{TD if lum(h) > .3 else TH};--j:{j};--w:{(j - (n_f - 1) / 2) * 4.2:.1f}deg" aria-label="{e(n)} {h.upper()} kopieren">
          <span class="fa__n"><b>{e(n)}</b><small>{h.upper()}</small></span><span class="fa__ok">kopiert</span>
        </button>''' for j, (k, n, h, r) in enumerate(alle))
    gruppen_html = ''
    for gk, gname, gsatz, liste in GRUPPEN:
        karten = ''.join(f'''<button class="fk" type="button" data-r="feder" data-hex="{h}" style="--i:{i % 4};--c:{h};--t:{TD if lum(h) > .3 else TH}" aria-label="{e(n)} {h.upper()} kopieren">
            <span class="fk__f"><span class="fk__hex">{h.upper()}</span><span class="fk__ok">kopiert</span></span>
            <span class="fk__n">{e(n)}</span>
            <span class="fk__r">{e(r)}</span>
            <span class="fk__w"><span>HEX</span>{h.upper()}<span>RGB</span>{' · '.join(map(str, rgb(h)))}</span>
          </button>''' for i, (k, n, h, r) in enumerate(liste))
        gruppen_html += f'''<div class="gr gr--{gk}" data-g>
        <div class="gr__k" data-r style="--i:0"><p class="mk__kap"><b>{ki(gname)}</b><i></i></p><p class="gr__s">{e(gsatz)}</p></div>
        <div class="gr__l gr__l--{min(len(liste), 4)}">{karten}</div>
      </div>'''
    anteile = [('Warmweiss', 52, F['Warmweiss'], TD), ('Dunkle Fläche', 34, A['marine'], F['Warmweiss']), ('Schrift', 9, TD, F['Warmweiss']), ('Abendfarbe', 5, F['Orange'], A['d0'])]
    anteil_html = ''.join(f'<span style="--p:{p};--j:{j};background:{c};color:{t}"><b><span data-zahl="{p}">0</span> %</b><small>{e(n)}</small></span>' for j, (n, p, c, t) in enumerate(anteile))
    WW, SV = F['Warmweiss'], F['Schiefer-Violett']
    paare = [('Schiefer auf Warmweiss', SV, WW, 'Lesetext'), ('Warmweiss auf Nacht A', WW, A['marine'], 'Lesetext auf Dunkel'),
             ('Orange hell auf Nacht A', B.ABEND_TOENE['orange']['gold'], A['marine'], 'Betonung auf Dunkel'), ('Orange tief auf Warmweiss', B.ABEND_TOENE['orange']['akzent'], WW, 'Betonung auf Hell'),
             ('Kerzenlicht auf Schiefertisch', F['Kerzenlicht'], F['Schiefertisch'], 'Betonung in B'), ('Honig tief auf Warmweiss', B.WELTEN['b']['css']['akzent'], WW, 'Betonung auf Hell in B'),
             ('Orange auf Warmweiss', F['Orange'], WW, 'nur grosse Zeilen'), ('Rahmengrau auf Warmweiss', F['Rahmengrau'], WW, 'nur die Linie')]

    def urteil(r):
        if r >= 7: return 'Sehr gut, auch für langen Text'
        if r >= 4.5: return 'Gut für Lesetext'
        if r >= 3: return 'Nur für grosse Zeilen'
        return 'Nur Linie, nie Schrift'
    kontrast_html = ''
    for i, (t, a, b, w) in enumerate(paare):
        r = kontrast(a, b)
        kontrast_html += f'''<li class="ko" data-r="feder" style="--i:{i % 3};--g:{b};--s:{a}">
          <span class="ko__p"><span>Aa</span><small>Momo x Rudi.</small></span>
          <span class="ko__n"><b>{e(t)}</b><small>{e(w)}</small></span>
          <span class="ko__z"><b><span data-zahl="{r:.1f}" data-komma>0</span></b><small>zu 1</small></span>
          <em class="ko__u">{urteil(r)}</em>
        </li>'''
    herkunft_html = ''
    for i, (key, t, x, toene, lage) in enumerate(HERKUNFT):
        st = streifen(key)
        st_html = ''.join(f'<i style="flex:{max(a, .06):.3f};background:{h};--j:{j}"></i>' for j, (a, h) in enumerate(st))
        werte = ' · '.join(h.upper() for _, h in st)
        wird = f'<p class="her__wird"><span>{ki("Daraus")}</span>{"".join(chip(k) for k in toene)}</p>'
        herkunft_html += f'''<article class="her k3" data-r="feder" style="--i:{i % 3}">
        <div class="k3__b her__b"><img src="{foto(key)}" alt="{e(t)}" loading="lazy" decoding="async" style="object-position:{lage}"><span class="kerbe">{ki(t)}</span></div>
        <div class="her__st" aria-label="Gemessene Töne: {werte}">{st_html}</div>
        <p class="her__m">aus dem Foto gemessen · {werte}</p>
        <p class="her__x">{e(x)}</p>
        {wird}
      </article>'''
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyzäöüß<br>0123456789 · 89,00 EUR · 30449'
    schriften = [
        ('a', 'Grosse Zeilen', 'Fraunces Soft', '600 bis 900, weich, gross und klein, Zutatenzeilen in Versalien', 'Titel, Zutatenzeilen, grosse Zahlen; aus der Wortmarke abgeleitet', 'Aa', 'Aubergine / Kokos / Limette / Sesam', ALPHA),
        ('c', 'Etiketten', 'Urbanist', '800 und 900, Versalien, das i klein, gesperrt', 'Kapitelzeilen, Bildzeilen, Knöpfe, das Band; aus der Zeile der Plakate', 'Aa', 'A UNiQUE EXPERiENCE BY MOMO X RUDi', ALPHA.replace('IJ', 'iJ')),
        ('s', 'Lesetext', 'Instrument Sans', 'Regular 400 und Semibold 600', 'alles, was gelesen wird', 'Aa', 'Momo wird persönlich jeden Drink für dich erklären.', ALPHA),
        ('m', 'Der Bon', 'DM Mono', 'Regular 400', 'Zeiten, Plätze, Preise, gesetzt wie ein Bon aus der Küche', 'Aa', 'FR 19:00 · SA 17:00 · 14 PLÄTZE', ALPHA),
    ]

    def rollen(text):
        return ''.join(f'<span class="ro" style="--k:{i}" data-c="{e(c)}">{e(c)}</span>' if c != ' ' else ' ' for i, c in enumerate(text))
    schrift_html = ''.join(f'''<article class="sch" data-g>
        <div class="sch__k" data-r style="--i:0"><p class="mk__kap"><b>{ki(r)}</b><i></i></p><h3 class="sch__n f-{c}">{e(n)}</h3><dl><dt>Schnitt</dt><dd>{e(s)}</dd><dt>Wofür</dt><dd>{e(w)}</dd></dl></div>
        <div class="sch__aa f-{c}" data-r="maske" aria-hidden="true"><span class="z"><span>{aa}</span></span></div>
        <div class="sch__r" data-r style="--i:2"><p class="sch__satz f-{c}" aria-label="{e(probe)}">{rollen(probe)}</p><p class="sch__abc f-{c}">{abc}</p></div>
      </article>''' for c, r, n, s, w, aa, probe, abc in schriften)
    wahl_html = (f'<div class="wahl__z wahl__z--logo" data-r style="--i:0"><span class="wahl__p">{wort()}</span><span class="wahl__n"><b>Die Wortmarke</b><em>{ki("Platzhalter")}</em><span>Aus Profilbild und Plakaten; nach Rudi nicht sein Logo, das Original kommt nach. Breite Display-Schrift der 70er, dicke Stämme, dünne Diagonalen, tropfenförmige Enden. Welche Schrift es ist, ist nicht belegt; verwandt nach dem Kundenprofil Gazpacho, Brasika, Moret, Hatton, alle kostenpflichtig.</span></span></div>'
                 + ''.join(f'<div class="wahl__z{" wahl__z--gewaehlt" if u == "gewählt" else ""}" data-r style="--i:{i + 1}"><span class="wahl__p {c}">CULINARIUM</span><span class="wahl__n"><b>{e(n)}</b><em>{ki(u)}</em><span>{e(s)}</span></span></div>' for i, (n, c, u, s) in enumerate(B.SCHRIFTWAHL)))
    zwahl_html = (f'<div class="wahl__z wahl__z--logo" data-r style="--i:0"><span class="wahl__p">{zeile()}</span><span class="wahl__n"><b>Die Zeile</b><em>{ki("Platzhalter")}</em><span>Geometrische Groteske, sehr kräftig, gesperrt, in Versalien mit kleinem i.</span></span></div>'
                  + ''.join(f'<div class="wahl__z{" wahl__z--gewaehlt" if u == "gewählt" else ""}" data-r style="--i:{i + 1}"><span class="wahl__p f-et" style="font-size:clamp(1rem,1.7vw,1.6rem);letter-spacing:.14em">{ki("A unique experience")}</span><span class="wahl__n"><b>{e(n)}</b><em>{ki(u)}</em><span>{e(s)}</span></span></div>' for i, (n, u, s) in enumerate(B.ZEILENWAHL[:1])))
    rang = [('Titel gross', 'Fraunces Soft 800 · 96 px', 'r1', 'Momo x Rudi.'), ('Zutatenzeile', 'Fraunces Soft 800 · Versalien · 64 px', 'r2', 'AUBERGINE / KOKOS'),
            ('Zwischentitel', 'Fraunces Soft 600 · 36 px', 'r3', 'Vierzehn an einem Tisch.'), ('Kleiner Titel', 'Fraunces Soft 600 · 22 px', 'r4', 'Fatwashing, Milkwashing, Enzyme'),
            ('Etikett', 'Urbanist 800 · 12 px · gesperrt · kleines i', 'r5', 'WALK ON THE WiLD SiDE · HANNOVER-LiNDEN'), ('Lesetext', 'Instrument Sans · 18 px · Zeilenabstand 1,62', 'r6', 'Zusätzlich begleiten dich 5 von Momos Signature Drinks, kreativ kreiert passend zum Essen, mit unserem Cocktail Tasting und einer dazugehörigen Schulung.'),
            ('Der Bon', 'DM Mono · 13 px', 'r7', 'BEGiNN FREiTAG 19:00 · SAMSTAG 17:00')]
    rang_html = ''.join(f'<li data-r="maske"><span class="rang__m"><b>{e(a)}</b>{e(b)}</span><span class="{c}"><span class="z"><span>{e(s).replace("i", "<span class=ki>i</span>") if c == "r5" else e(s)}</span></span></span></li>' for a, b, c, s in rang)
    bilder = [('pass', 'Am Pass', 'b1', '50% 50%'), ('anstossen2', 'Anstossen über der Tafel', 'b2', '50% 40%'), ('glas-hell', 'Ein heller Drink', 'b3', '50% 60%'),
              ('team', 'Vor dem Negroni', 'b4', '40% 50%'), ('tafel-kerzen', 'Die lange Tafel', 'b5', '50% 50%'), ('schild-nacht', 'Wild Side bei Nacht', 'b6', '50% 40%'), ('teller-gold', 'Teller mit Goldrand', 'b7', '50% 50%')]
    bilder_html = ''.join(f'<figure class="bi {c} k3" data-r="feder" style="--i:{i % 3}"><div class="k3__b"><img src="{foto(k)}" alt="{e(t)}" loading="lazy" decoding="async" style="object-position:{l}"><figcaption class="kerbe">{ki(t)}</figcaption></div></figure>' for i, (k, t, c, l) in enumerate(bilder))
    nein = [('zerr', 'Nicht verzerren'), ('dreh', 'Nicht drehen'), ('farbe', 'Nicht umfärben'), ('schatten', 'Keine Schatten')]
    nein_html = ''.join(f'<figure class="nein nein--{c}"><div>{zeichen()}<i></i></div><figcaption>{e(t)}</figcaption></figure>' for c, t in nein)
    richtig_html, falsch_html = logo_karten()
    unterschiede = ''.join(f'<li style="--i:{i}"><b>{e(k)}</b><span>{e(v)}</span></li>' for i, (k, v) in enumerate(B.EIGENE_WELT['unterschied_zu'].items()))
    T = B.TON
    abende_html = ''.join(f'''<button class="ab-k" type="button" data-r="feder" data-abend-knopf="{k}" style="--i:{j % 6};--c:{F[n]}" aria-pressed="false">
        <img src="{foto(bild)}" alt="Plakat {e(mo)}, {dat}" loading="lazy" decoding="async"><span class="ab-k__f"></span>
        <span class="ab-k__n"><b>{e(n)}</b><small>{F[n]} · {dat}</small></span></button>''' for j, (k, n, a, mo, bild, dat) in enumerate(B.ABENDE))

    def welt_block(k, w, i):
        c = w['css']
        geraet_html = geraet(k, i) if os.path.exists(os.path.join(M, 'geraet', 'schirm', f'laptop-{k}.png')) else ''
        return f'''<div class="welt {'welt--gewaehlt' if k == 'a' else 'welt--nicht'}">
        <div class="welt__k"><h3>{k.upper()} · <em>{e(w['name'])}</em></h3><div class="welt__b">{''.join(f'<i style="background:{c[x]}"></i>' for x in ('papier', 'creme', 'marine', 'blau', 'gold', 'akzent'))}</div></div>
        <p>{e(w['satz'])}</p>
        <figure class="lock lock--marine welt__tafel" data-r="flug" style="--i:{i};--fx:{'-10vw' if i == 0 else '10vw'};--fy:22vh;--fw:{'-5deg' if i == 0 else '5deg'};background-color:{c['marine']};background-image:url(zeichen/tapete-dunkel-{k}.svg);background-size:224px;color:{c['papier']}"><div>{marke('lock__w')}<p class="lock__o" style="color:{c['gold']}">{ki('Haasemannstraße 13 · Welt ' + k.upper())}</p></div><figcaption class="kerbe">{ki('Fläche ' + w['name'] + ' · Betonung ' + w['akzent'])}</figcaption></figure>
        {geraet_html}
        <div class="knr">{kn(f'Probe {k.upper()} öffnen', f'probe.html?welt={k}', neu=True)}<a class="kn {"kn--linie" if k == "b" else ""}" href="?welt={k}" data-welt-knopf="{k}">{ki(f"Markenbuch in {k.upper()}")}<i>{PF}</i></a></div>
      </div>'''
    KAPITEL = [('haltung', 'Haltung'), ('zeichen', 'Zeichen'), ('farben', 'Farben'), ('abende', 'Abendfarben'), ('welten', 'Welten'), ('herkunft', 'Herkunft'), ('schrift', 'Schrift'),
               ('tapete', 'Tapete'), ('bilder', 'Bilder'), ('bausteine', 'Bausteine'), ('logo', 'Logo'), ('welt', 'Eigene Welt'), ('mitnehmen', 'Mitnehmen')]
    index_html = ''.join(f'<a href="#{k}" data-r style="--i:{i}"><span>{e(n)}</span></a>' for i, (k, n) in enumerate(KAPITEL))
    nav_html = ''.join(f'<a href="#{k}">{ki(n)}</a>' for k, n in KAPITEL[:10])
    v_css = int(os.path.getmtime(os.path.join(M, 'marke.css'))); v_js = int(os.path.getmtime(os.path.join(M, 'marke.js')))
    offen_satz = 'Gewählt am 26.10.2026: Farbwelt A «Plakat». Zur Wahl: die Abendfarbe des nächsten Abends, bis dahin Orange. Die Wortmarke ist ein Platzhalter, bis Rudis Original da ist. Offen: die Rechte an den Plakat-Illustrationen und an den Fotos, wer auf welchem Foto zu sehen ist.'
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Markenbuch · Culinarium Hannover</title>
<meta name="description" content="Wortmarke und Zeichen, Farben und ihre Herkunft, die sechs Abendfarben, Schriften, Tapete, Bilder und Bausteine für die erste Website von Culinarium. Entwurf von Tasty Studios, Oktober 2026.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{A['marine']}">
<link rel="icon" href="zeichen/icon.svg" type="image/svg+xml">
<link rel="preload" href="schriften/Fraunces-Soft-600_900.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="schriften/Urbanist-400_900.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="marke.css?v={v_css}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body data-abend="{B.ABEND_DEFAULT}">
{B.sym_defs()}

<nav class="leiste" aria-label="Markenbuch">
  <a class="leiste__m" href="#oben">{zeichen()}<span><b>{ki('Markenbuch')}</b><small>Station 05 · Culinarium Hannover</small></span></a>
  <div class="leiste__k">{nav_html}</div>
  <a class="glanz" href="probe.html" target="_blank" rel="noopener">{ki('Die Probe')}{PF}</a>
</nav>

<main>
<section class="titel tapete" id="oben">
  <div class="titel__in">
    <p class="titel__kap" data-r="hero" style="--i:0"><i></i><b>{ki('Markenbuch · Oktober 2026')}</b><i></i></p>
    <div class="titel__z" data-r="zeichen">{zeichen('', 'Das C')}</div>
    <h1 class="titel__w" data-r="maske"><span class="z"><span>{wort()}</span></span></h1>
    <span class="titel__zl" data-r="hero" style="--i:1">{zeile()}</span>
    <p class="titel__ph" data-r="hero" style="--i:1">{ki("Wortmarke: Platzhalter · das Original schickt Rudi nach")}</p>
    <p class="titel__ort" data-r="hero" style="--i:2"><span style="white-space:nowrap">{ki('Walk on the Wild Side')}</span> <span class="raute"></span> {ki('Haasemannstraße 13')} <span class="raute"></span> {ki('Hannover-Linden')}</p>
    <p class="titel__lead" data-r="hero" style="--i:3">Alles, was Culinarium erkennbar macht, an einem Ort: die Wortmarke, das C und das x, das Band der Plakate, die Farben und woher sie kommen, die Farbe jedes Abends, die Schriften, die Tapete, die Bilder und die Bausteine der neuen Website. Damit jedes neue Stück, ob Plakat, Seite oder Bon, aussieht wie aus einem Guss.</p>
    <div class="knr knr--mitte" data-r="hero" style="--i:4">{kn('Lesen', '#haltung')}{kn('Die Probe', 'probe.html', 'kn--linie', neu=True)}</div>
  </div>
  <nav class="index" aria-label="Inhalt" data-g>{index_html}</nav>
  <span class="titel__runter" aria-hidden="true"><i></i></span>
</section>

<section class="ab blatt papier tapete-h" id="haltung">
  <div class="in">
    {kopf('Haltung', ['Momo', 'x Rudi.'], 'So steht es unter jedem Plakat: «A UNiQUE EXPERiENCE BY MOMO X RUDI». Einer kocht, einer mixt und erklärt, vierzehn sitzen an einer langen Tafel in einer Bar in Linden. Die Gestaltung ist urban von aussen und warm von innen: dunkle Flächen wie die Bar, warmweisse Bänder wie das Plakat, und eine Farbe, die mit jedem Abend wechselt.')}
    <div class="drei" data-g>
      {kachel('tresen', 'Das Glas.', 'Am Tresen', 'Fünf Signature Drinks an einem Abend, jeder erklärt. Fatwashing, Milkwashing, Klärung durch Enzyme stehen in jeder Ankündigung.', 0, '50% 30%')}
      {kachel('pass', 'Der Teller.', 'Am Pass', 'Drei Gänge zu fünf Drinks. Rudi schreibt seine Teller in vier Wörtern: AUBERGINE / KOKOS / LIMETTE / SESAM.', 1, '50% 50%')}
      {kachel('anstossen2', 'Die Tafel.', 'Vierzehn Plätze', 'Ein Freitag um 19 Uhr, ein Samstag um 17 Uhr. Zuletzt stand auf dem Plakat: «AUSGEBUCHT!»', 2, '50% 40%')}
    </div>
  </div>
</section>

<section class="fenster" aria-label="Der Durchbruch in der Wand">
  <div class="fenster__f">
    <div class="fenster__b"><img src="{foto('putz')}" alt="Durchbruch in der Wand der Bar, dahinter ein Tisch mit Kerze" decoding="async"></div>
    <div class="fenster__t"><p class="fenster__s"><span class="z"><span>Walk on</span></span><span class="z"><span><em>the wild side.</em></span></span></p><p class="fenster__u">Der Kopf jedes Plakats, der Name der Bar.</p></div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="zeichen">
  <div class="in">
    {kopf('Zeichen und Name', ['Ein Name,', 'vorerst ein Platzhalter.'], 'Rudi sagt am 26. Oktober 2026: Die Wortmarke aus dem Instagram-Profilbild und den Plakaten ist nicht sein Logo, das echte schickt er nach. Alles in diesem Kapitel ist deshalb Platzhalter: CULINARIUM in einer breiten Display-Schrift der 70er, darunter die Zeile «A UNiQUE EXPERiENCE BY MOMO X RUDI», aus den Original-Pixeln des grössten Plakats als Vektor gezogen. Kommt das Original, werden Wortmarke, C, Titelschrift und Logo-Regeln daran neu geprüft.')}
    <div class="band hinweis" data-r><span>{ki('Platzhalter')}</span><span>Wortmarke aus Profilbild und Plakaten · das Original schickt Rudi nach</span></div>
    <div class="lockups" data-g>
      <figure class="lock lock--marine tapete" data-r="flug" style="--i:0;--fx:-14vw;--fy:22vh;--fw:-6deg"><div>{marke('lock__w')}<p class="lock__o">{ki('Hauptform auf Dunkel')}</p></div><figcaption class="kerbe">{ki('Warmweiss auf Schiefer')}</figcaption></figure>
      <figure class="lock lock--papier" data-r="flug" style="--i:1;--fx:14vw;--fy:22vh;--fw:6deg"><div style="width:100%;align-self:stretch;display:flex;align-items:center"><div class="band band--gross band--voll">{wort('w')}{zeile('zl')}</div></div><figcaption class="kerbe">{ki('Auf dem Band, wie auf jedem Plakat')}</figcaption></figure>
      <figure class="lock lock--quer" data-r="flug" style="--i:2;--fx:-12vw;--fy:30vh;--fw:5deg"><div>{zeichen('lock__z')}<span class="lock__strich"></span>{wort('lock__wq')}</div><figcaption class="kerbe">{ki('Querform für Leiste und Bon')}</figcaption></figure>
      <figure class="lock lock--groessen tapete" data-r="flug" style="--i:3;--fx:12vw;--fy:30vh;--fw:-5deg"><div style="color:var(--gold)">{zeichen('g1')}{zeichen('g2')}{zeichen('g3')}{zeichen('g4')}</div><figcaption class="kerbe">{ki('Das C: Leiste, Stempel, Zeichen im Browser')}</figcaption></figure>
    </div>
    <div class="reihe5" data-g>
      <div class="zei" data-r="feder" style="--i:0">{zeichen('', 'Das C')}<b>Das C</b><small>erster Buchstabe der Wortmarke · unverändert</small></div>
      <div class="zei" data-r="feder" style="--i:1">{xz()}<b>Das x</b><small>aus «MOMO X RUDI» · verbindet zwei</small></div>
      <div class="zei" data-r="feder" style="--i:2"><span class="band" style="display:block;width:100%;height:clamp(54px,5.4vw,78px)"></span><b>Das Band</b><small>Warmweiss, doppelte Linie · unter jedem Bild</small></div>
      <div class="zei" data-r="feder" style="--i:3"><img src="{foto('plakat-2026-03')}" alt="Plakat vom März 2026 mit Band und Wortmarke" style="border-radius:8px"><b>Auf dem Plakat</b><small>@culinarium_hannover · März 2026</small></div>
    </div>
    <div class="regeln" data-g>
      <div class="regel" data-r="feder" style="--i:0">
        <div class="regel__f"><svg class="schutz" viewBox="-60 -60 {float(B.CVB.split()[2]) + 120:.0f} {float(B.CVB.split()[3]) + 120:.0f}" aria-hidden="true">
          <rect x="-50" y="-50" width="{float(B.CVB.split()[2]) + 100:.0f}" height="{float(B.CVB.split()[3]) + 100:.0f}" rx="8" fill="none" stroke="currentColor" stroke-width="4" stroke-dasharray="16 12"/>
          <g fill="currentColor"><use href="#c" width="{float(B.CVB.split()[2]):.0f}" height="{float(B.CVB.split()[3]):.0f}"/></g>
        </svg></div>
        <h3>Schutzraum</h3><p>Rund um das C bleibt ein Drittel seiner Höhe frei. Kein Text, kein Bildrand, keine Linie ragt hinein.</p>
      </div>
      <div class="regel" data-r="feder" style="--i:1">
        <div class="regel__f klein"><span>{zeichen()}<small>16 px</small></span><span>{zeichen()}<small>24 px</small></span><span>{zeichen()}<small>8 mm</small></span></div>
        <h3>Kleinste Grösse</h3><p>Das C allein ab 16 Pixel Höhe, im Druck ab 8 Millimeter. Die Wortmarke allein ab 120 Pixel Breite, mit Zeile ab 220 Pixel.</p>
      </div>
      <div class="regel regel--breit" data-r="feder" style="--i:2">
        <div class="regel__f neine">{nein_html}</div>
        <h3>Was das Zeichen nicht darf</h3><p>Es steht gerade, in Schiefer-Violett, Warmweiss oder der Betonungsfarbe, ohne Schatten und ohne Kreis darum. Auf Fotos nie; dafür gibt es das Band.</p>
      </div>
    </div>
  </div>
</section>

<section class="ab blatt papier" id="farben">
  <div class="in">
    {kopf('Farben', ['Siebzehn Töne,', 'jeder mit Fundstelle.'], 'Drei Farben stehen auf jedem Plakat und bleiben immer: Warmweiss, Schiefer-Violett, Rahmengrau. Dazu die sechs Abendfarben der Plakate seit November 2024 und acht Töne aus Rudis Fotos der Bar. Gemessen ist jeweils der häufigste Ton einer Fläche, zur Gegenprobe der Median; beide stehen im Paket. Ein Klick auf eine Farbe kopiert ihren Wert.')}
    <div class="faecher" data-r="faecher"><div class="faecher__in">{faecher}</div><p class="faecher__h">Über den Fächer fahren, ein Klick kopiert den Farbwert.</p></div>
    <div class="anteil" data-r="anteil"><p class="mk__kap"><b>{ki('Mengenverhältnis')}</b><i></i><span>Richtwert für eine Seite oder ein Plakat</span></p><div class="anteil__b">{anteil_html}</div></div>
    {gruppen_html}
    <div class="kontrast">
      <div class="kontrast__k" data-r><p class="mk__kap"><b>{ki('Lesbarkeit')}</b><i></i></p><h3>Welche Farbe auf welcher stehen darf.</h3><p>Gerechnet nach dem internationalen Standard für Lesbarkeit im Netz (WCAG 2.1). Ab 4,5 zu 1 ist Lesetext gut lesbar, ab 3 zu 1 grosse Zeilen. Jede Abendfarbe hat dafür einen hellen Ton für dunkle Flächen und einen tiefen für helle, gerechnet, nicht gemessen.</p></div>
      <ul class="kontrast__l" data-g>{kontrast_html}</ul>
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="abende">
  <div class="in">
    {kopf('Die Abendfarben', ['Jeder Abend', 'hat seine Farbe.'], 'Seit November 2024 hat jedes Plakat eine eigene Farbe: Eisblau zum Ski, Orange zum Panther, Grasgrün zur Gärtnerin, Nachtblau zum Kürbis, Ochsenblut zum Eisbecher, Sepia zur Mondfrau. Die neue Seite übernimmt das: Ihre Betonung ist die Farbe des nächsten Abends. Ein Klick auf ein Plakat färbt dieses Markenbuch um, Welt A.')}
    <div class="abende" data-g>{abende_html}</div>
    <p class="ab-h">{ki('Solange kein Termin steht: Orange, wie im Flur der Bar')}</p>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="welten">
  <div class="in">
    {kopf('Die Farbwelt', ['Gewählt:', 'das Plakat.'], 'Robert hat am 26. Oktober 2026 Welt A gewählt: «a». Welt B bleibt hier zum Nachlesen. Beide Welten teilen Warmweiss, Schiefer-Violett, die doppelte Linie, das C und die Schriften. Sie unterscheiden sich dort, wo die Seite dunkel wird und womit sie betont. A nimmt das Plakat: Schiefer als dunkle Fläche, die Abendfarbe als Betonung. B nimmt die Bar: die dunkle Tischplatte als Fläche, das Kerzenlicht als Betonung. Die Probe läuft in beiden Welten als eigene Seite, zum Scrollen. Die Abendfarbe ist nicht gewählt; bis zum nächsten Termin gilt Orange als Vorgabe.')}
    <div class="welten" data-g>
      {welt_block('a', B.WELTEN['a'], 0)}
      {welt_block('b', B.WELTEN['b'], 1)}
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="herkunft">
  <div class="in">
    {kopf('Herkunft', ['Woher die Farben', 'kommen.'], 'Aus dem Plakat und aus Rudis Fotos der Bar: das Band, der Flur, die Kerzen, die Glasballons, der dunkle Tisch, die Ecke draussen. Unter jedem Bild der Streifen, der beim Bau dieser Seite aus dem Foto gemessen wurde, darunter die Töne, die daraus geworden sind.')}
    <div class="hers" data-g>{herkunft_html}</div>
  </div>
</section>

<section class="ab blatt papier" id="schrift">
  <div class="in">
    {kopf('Schrift', ['Aus Wortmarke', 'und Zeile.'], 'Die Titel nehmen die Haltung der Wortmarke auf: Fraunces Soft, eine Antiqua der 70er mit weichen Tropfen an den Enden. Die Etiketten nehmen die Zeile auf: Urbanist, kräftig, gesperrt, in Versalien und mit kleinem i wie in «UNiQUE». Instrument Sans hält lange Texte lesbar, DM Mono setzt Zeiten und Preise wie einen Bon aus der Küche. Alle sind frei lizenziert und liegen als Dateien bei der Website.')}
    <div class="schs">{schrift_html}</div>
    <div class="rang">
      <div class="rang__k" data-r><p class="mk__kap"><b>{ki('Neben der Wortmarke')}</b><i></i></p><h3>Achtzehn freie Schriften, gemessen.</h3><p>Jede Schrift wurde mit CULINARIUM gesetzt und Buchstabe für Buchstabe auf die Original-Pixel des Plakats gelegt. Keine freie Schrift trifft die Wortmarke; hier die vier, über die zu entscheiden war.</p></div>
      <div><div class="wahl" data-g>{wahl_html}</div>
      <div class="wahl" data-g style="margin-top:clamp(18px,2vw,28px)">{zwahl_html}</div></div>
    </div>
    <div class="rang">
      <div class="rang__k" data-r><p class="mk__kap"><b>{ki('Rangordnung')}</b><i></i></p><h3>Sieben Stufen, mehr braucht die Seite nicht.</h3><p>Grössen der neuen Website auf einem Rechner mit 1440 Pixel Breite. Auf dem Handy werden die Titel kleiner, der Lesetext bleibt.</p></div>
      <ul class="rang__l">{rang_html}</ul>
    </div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="tapete">
  <div class="in">
    {kopf('Tapete', ['Die doppelte Linie', 'als Gitter.'], 'Das Muster kommt vom Plakat: die doppelte Linie um Wortmarke und Zeile, zu einem Gitter gelegt, an jeder Kreuzung das x, in jedem Feld das C. Zart und Ton in Ton, auf dunklen Flächen in der Betonung, auf hellen in Schiefer-Violett, immer im Wechsel mit glatten Flächen.')}
    <div class="tap" data-g>
      <figure class="tap__f tap__f--dunkel" data-r="feder" style="--i:0"><span class="streif"></span><figcaption class="kerbe">{ki('Auf Dunkel')}</figcaption></figure>
      <figure class="tap__f tap__f--hell" data-r="feder" style="--i:1"><span class="streif"></span><figcaption class="kerbe">{ki('Auf Warmweiss')}</figcaption></figure>
    </div>
    <div class="prunk" data-r="prunk">
      <div class="prunk__z" style="--i:0"><b><span data-zahl="224">0</span></b><i></i><small>Pixel Rapport am Bildschirm</small></div>
      <div class="prunk__z" style="--i:1"><b><span data-zahl="5">0</span></b><i></i><small>Prozent Deckkraft der Linie auf Hell</small></div>
      <div class="prunk__z" style="--i:2"><b><span>1 : 1</span></b><i></i><small>im Wechsel mit glatten Flächen</small></div>
    </div>
  </div>
</section>

<section class="ab blatt papier" id="bilder">
  <div class="in">
    {kopf('Bilder', ['Kerzenlicht', 'und Kupfer.'], 'Gezeigt wird, was ein Gast an so einem Abend sieht: der Pass mit den Tellern, das Anstossen, die Gläser, die Leute an der Bar, die gedeckte Tafel, das Schild in der Nacht. Alle Fotos stammen aus Rudis Dateien. Wer sie gemacht hat und wer darauf zu sehen ist, ist noch nicht belegt; Namen stehen deshalb nirgends im Bild.')}
    <div class="collage" data-g>{bilder_html}</div>
    <div class="satz3" data-g>
      <div data-r style="--i:0"><h3>Nur Rudis Fotos.</h3><p>Dazu die Plakate des eigenen Kontos. Keine Bilder von Gästen aus Instagram, keine der Bar ohne ihre Freigabe, keine erzeugten Bilder.</p></div>
      <div data-r style="--i:1"><h3>Warm bleibt warm.</h3><p>Das Licht der Abende ist orange und kupfern. Es wird nicht kalt gezogen; nur Schärfe und Helligkeit werden angeglichen.</p></div>
      <div data-r style="--i:2"><h3>Das Band statt Schrift im Bild.</h3><p>Wie auf dem Plakat sitzt unter jedem Foto ein schmales warmweisses Band mit doppelter Linie. Darin steht, was zu sehen ist.</p></div>
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="bausteine">
  <div class="in">
    {kopf('Bausteine', ['Knopf, Band,', 'Bon und Zeile.'], 'Die kleinen Teile, die überall wiederkehren. Der Knopf hat Tiefe und einen runden Knauf in der Betonung und gibt nach, wenn man ihn drückt. Das Band trägt Namen und Daten. Der Bon setzt Zeiten und Preise. Die Zutatenzeile macht aus vier Wörtern eine Überschrift. Probieren Sie es gern aus.')}
    <div class="baus" data-g>
      <div class="bau" data-r="feder" style="--i:0"><div class="bau__f knr knr--mitte">{kn('Platz anfragen', '#bausteine')}{kn('Zur Warteliste', '#bausteine', 'kn--linie')}</div><h3>Knöpfe</h3><p>Etikettschrift in Versalien mit kleinem i. Der Knauf trägt die Farbe des Abends. Der Knopf sagt, was passiert.</p></div>
      <div class="bau" data-r="feder" style="--i:1"><div class="bau__f"><div class="band" style="width:100%;padding:18px 22px;display:flex;justify-content:space-between;gap:16px;font:800 11.5px/1.3 var(--caps);letter-spacing:.16em;text-transform:uppercase"><span>{ki('Am Tresen')}</span><span style="color:var(--akzent)">{ki('Momo x Rudi')}</span></div></div><h3>Das Band</h3><p>Warmweiss, oben und unten die doppelte Linie. Es liegt unter dem Bild über die ganze Breite und trägt, was sonst ein Schild wäre. Nie gerahmt, nie auf dem Foto.</p></div>
      <div class="bau" data-r="feder" style="--i:0"><div class="bau__f" style="justify-content:center"><div class="bon"><div class="bon__k">{wort()}<span>WALK ON THE WILD SIDE</span></div><dl><dt>Freitag</dt><dd>19:00</dd><dt>Samstag</dt><dd>17:00</dd><dt>Plätze</dt><dd>14</dd></dl><div class="summe"><span>PRO PERSON</span><span>89,00 EUR</span></div></div></div><h3>Der Bon</h3><p>Zeiten, Plätze und Preis stehen wie auf einem Bon aus der Küche, in DM Mono auf weissem Papier. Stand: Abende im März und September 2026.</p></div>
      <div class="bau" data-r="feder" style="--i:1"><div class="bau__f bau__f--titel" data-r="maske"><p class="mk__kap"><b>{ki('Rudi · Oktober 2026')}</b><i></i></p><p class="bau__t zutat"><span class="z"><span>Aubergine<span class="sl"> / </span>Kokos</span></span><span class="z"><span><span class="sl">/ </span>Limette<span class="sl"> / </span>Sesam</span></span></p></div><h3>Die Zutatenzeile</h3><p>So schreibt Rudi seine Teller. Die Zeile wird zur Überschrift, Zeile für Zeile aus dem Schlitz, die Schrägstriche in der Betonung. Momos Techniken bekommen dieselbe Form.</p></div>
    </div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="logo">
  <div class="in">
    {kopf('Logo richtig und falsch', ['Eingesetzt,', 'nie verändert.'], 'Die Regeln gelten vorerst für den Platzhalter aus Profilbild und Plakaten; mit Rudis Original werden sie neu gezeichnet. Wortmarke, Zeile und C sind Dateien. Sie werden eingesetzt, nie nachgezeichnet, nie verändert. Acht Dinge, die gehen, und acht, die nicht gehen.')}
    <p class="mk__kap" data-r><b>{ki('Richtig')}</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px;margin-bottom:clamp(40px,4vw,64px)">{richtig_html}</div>
    <p class="mk__kap" data-r><b>{ki('Falsch')}</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px">{falsch_html}</div>
    <div class="knr knr--mitte" data-r style="margin-top:clamp(36px,4vw,56px)">{kn('Logo-Regeln als eigene Seite', 'logo-richtig-falsch/index.html', 'kn--linie', neu=True)}</div>
  </div>
</section>

<section class="ab blatt papier" id="welt">
  <div class="in">
    {kopf('Die eigene Welt', ['Was nur', 'Culinarium ist.'], ' '.join(e(x) for x in B.EIGENE_WELT['satz']))}
    <div class="satz3" data-g style="margin-top:0;padding-top:0;border-top:0">
      <div data-r style="--i:0"><h3>Charakter</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in T['charakter'])}</ul></div>
      <div data-r style="--i:1"><h3>Worte des Hauses</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in T['eigene_worte'])}</ul></div>
      <div data-r style="--i:2"><h3>Nicht</h3><ul class="nicht">{''.join(f'<li>{e(x)}</li>' for x in T['nicht'])}</ul></div>
    </div>
    <div class="satz3" data-g>
      <div data-r style="--i:0"><h3>Darstellung, neu.</h3><p>{e(B.DARSTELLUNG)}</p></div>
      <div data-r style="--i:1"><h3>Bewegung, neu.</h3><p>{e(B.BEWEGUNG)}</p></div>
      <div data-r style="--i:2"><h3>Die Probe.</h3><p>Auftakt als Paar mit dem Band darunter, Momos Kapitel als Zutatenzeile, Rudis Kapitel mit Bon und Abendfarbe. {kn('Ansehen', 'probe.html', neu=True)}</p></div>
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="unterschied">
  <div class="in">
    {kopf('Projekt Nummer 10', ['Womit es sich von jedem', 'bisherigen Haus unterscheidet.'], 'Jedes Haus bekommt eine eigene Welt, kein Haus bekommt das System. Vor dieser Station wurden die Konzepte und Markenbücher der bisherigen Häuser gelesen; hier steht je Haus, was Culinarium anders macht. Culinarium ist das erste Haus ohne Zimmer und ohne eigenes Restaurant, eine Reihe von Abenden.')}
    <ul class="unter" data-g>{unterschiede}</ul>
  </div>
</section>

<section class="ab blatt marine tapete schluss" id="mitnehmen">
  <div class="in">
    {kopf('Zum Mitnehmen', ['Alles für das', 'nächste Plakat.'], 'Wortmarke, Zeile und C als Vektor (Platzhalter, bis Rudis Original da ist), die Farben als fertige Datei, die Tapeten und die Schriften. Wer ein neues Plakat, einen Bon oder eine Seite gestaltet, findet hier alles dafür.')}
    <ul class="laden" data-g>
      <li data-r style="--i:0"><span><b>Wortmarke mit Zeile</b><small>Platzhalter · SVG, Schiefer-Violett</small></span>{kn('Laden', 'zeichen/wortmarke-mit-zeile-schiefer.svg', laden=True)}</li>
      <li data-r style="--i:1"><span><b>Wortmarke hell</b><small>Platzhalter · SVG, Warmweiss</small></span>{kn('Laden', 'zeichen/wortmarke-mit-zeile-warmweiss.svg', laden=True)}</li>
      <li data-r style="--i:2"><span><b>Das C</b><small>Platzhalter · SVG, Zeichen</small></span>{kn('Laden', 'zeichen/c-schiefer.svg', laden=True)}</li>
      <li data-r style="--i:3"><span><b>Das x</b><small>SVG</small></span>{kn('Laden', 'zeichen/x-schiefer.svg', laden=True)}</li>
      <li data-r style="--i:4"><span><b>Farben</b><small>beide Welten und sechs Abende als CSS-Datei</small></span>{kn('Laden', 'farben.css', laden=True)}</li>
      <li data-r style="--i:5"><span><b>Farbkarten</b><small>alle siebzehn Töne, SVG</small></span>{kn('Laden', 'farben.svg', laden=True)}</li>
      <li data-r style="--i:6"><span><b>Fraunces Soft</b><small>600 bis 900, WOFF2, Lizenz OFL</small></span>{kn('Laden', 'schriften/Fraunces-Soft-600_900.woff2', laden=True)}</li>
      <li data-r style="--i:7"><span><b>Urbanist</b><small>400 bis 900, WOFF2, Lizenz OFL</small></span>{kn('Laden', 'schriften/Urbanist-400_900.woff2', laden=True)}</li>
    </ul>
    <div class="ende" data-r="ende">
      <span class="strich strich--gross">{zeichen()}</span>
      <p class="ende__w">{wort()}</p>
      <p class="ende__s">Markenbuch Culinarium Hannover · Station 05 der Kette · Entwurf von Tasty Studios, Oktober 2026. {offen_satz}</p>
      <div class="knr knr--mitte">{kn('Die Probe', 'probe.html', neu=True)}{kn('Logo richtig und falsch', 'logo-richtig-falsch/index.html', 'kn--linie', neu=True)}</div>
    </div>
  </div>
</section>
</main>
<script src="marke.js?v={v_js}" defer></script>
</body>
</html>
'''


def logo_seite():
    richtig_html, falsch_html = logo_karten('../')
    v_css = int(os.path.getmtime(os.path.join(M, 'marke.css'))); v_js = int(os.path.getmtime(os.path.join(M, 'marke.js')))
    s = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Logo richtig und falsch · Culinarium Hannover</title><meta name="robots" content="noindex, nofollow">
<link rel="icon" href="../zeichen/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../marke.css?v={v_css}"><script>document.documentElement.classList.add('js')</script></head>
<body data-abend="{B.ABEND_DEFAULT}">{B.sym_defs()}
<nav class="leiste" aria-label="Markenbuch"><a class="leiste__m" href="../markenbuch.html">{zeichen()}<span><b>{ki('Markenbuch')}</b><small>Logo richtig und falsch</small></span></a><div class="leiste__k"></div><a class="glanz" href="../markenbuch.html#logo">{ki('Zum Markenbuch')}{PF}</a></nav>
<main>
<section class="ab creme tapete-h" id="logo" style="padding-top:clamp(60px,7vw,110px)">
  <div class="in">
    {kopf('Logo richtig und falsch', ['Eingesetzt,', 'nie verändert.'], 'Vorerst für den Platzhalter: Wortmarke, Zeile und C sind aus den Pixeln des Plakats gezogen (Deckung 99,6 und 98,5 Prozent); nach Rudi ist das nicht sein Logo, das Original kommt nach. Sie werden eingesetzt, nie nachgezeichnet, nie verändert. Eine Datei des Gestalters fehlt noch.')}
    <p class="mk__kap" data-r><b>{ki('Richtig')}</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px;margin-bottom:clamp(40px,4vw,64px)">{richtig_html}</div>
    <p class="mk__kap" data-r><b>{ki('Falsch')}</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px">{falsch_html}</div>
  </div>
</section>
</main>
<script src="../marke.js?v={v_js}" defer></script></body></html>'''
    s = s.replace('url(zeichen/', 'url(../zeichen/')
    open(os.path.join(M, 'logo-richtig-falsch', 'index.html'), 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    css()
    t = open(os.path.join(M, 'marke.css'), encoding='utf-8').read()
    # die Tapeten-Pfade im CSS gelten relativ zu marke/, in logo-richtig-falsch/ eine Ebene tiefer: dort über eigene Variablen
    open(os.path.join(M, 'markenbuch.html'), 'w', encoding='utf-8').write(seite())
    logo_seite()
    print('gebaut: markenbuch.html, marke.css, marke.js, logo-richtig-falsch/')
