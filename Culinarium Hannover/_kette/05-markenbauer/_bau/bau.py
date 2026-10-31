#!/usr/bin/env python3
"""Culinarium Hannover · Station 05 Markenbauer · 26.10.2026.
Robert 26.10.2026: «baue das Design-Buch nochmal auf höchstem Standard mit den ganzen Farben und Co., wie wir das auch für die Luxushotels
gemacht haben» · zum Haus: «richtig cool, bisschen urban, modern, funky, Style Kitchen … Tasty Rob Style x Rudi und sein Team».

Dieser Teil hält die Inhalte (Farben mit Fundstelle, Abendfarben, Farbwelten, Schriften, Ton, eigene Welt), baut Tapeten, farben.svg,
farben.css, die Probe (marke/probe.html) und marke.json. Das Markenbuch selbst baut bau2.py (Bauart Le Livre des Grand Beau-Rivage,
wie Monte-Moro). Alle Farben aus _bau/messung.json (messen.py), Zeichen aus zeichen.py, Schriftwahl aus match.py / match_zeile.py.
   python3 bau.py && python3 bau2.py"""
import html, json, os, re

H = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(H)                      # _kette/05-markenbauer
M = os.path.join(P, 'marke')
e = html.escape
MS = json.load(open(os.path.join(H, 'messung.json')))
PL = {p['abend']: p for p in MS['plakate']}
FO = {f['name']: f for f in MS['fotos']}


# ---------------------------------------------------------------- Rechnen mit Farben
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def hx(c): return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)
def mix(a, b, t): return hx([x + (y - x) * t for x, y in zip(rgb(a), rgb(b))])


def lum(h):
    def k(c):
        c /= 255; return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = rgb(h); return .2126 * k(r) + .7152 * k(g) + .0722 * k(b)


def kontrast(a, b):
    la, lb = lum(a), lum(b); return (max(la, lb) + .05) / (min(la, lb) + .05)


def bis(c, ziel, gegen, mind=4.5):
    """c schrittweise Richtung ziel mischen, bis der Kontrast gegen «gegen» reicht (gerechnet, nicht gemessen)."""
    t = 0.0
    while kontrast(mix(c, ziel, t), gegen) < mind and t < 1: t += .02
    return mix(c, ziel, min(t, 1))


def fs(f, was):
    b = f['box']
    return '%s · %s, Ausschnitt x %d–%d, y %d–%d (von %d × %d)' % (was, f['datei'], b[0], b[2], b[1], b[3], f['groesse'][0], f['groesse'][1])


# ---------------------------------------------------------------- Farben, gemessen
WW = PL['2026-09']['band']['hex']        # Warmweiss, Modus = Median auf fünf von sechs Plakaten
SV = PL['2026-09']['tinte']['hex']                                          # Schiefer-Violett, auf allen sechs Plakaten gleich
RG = MS['rahmen']['hex']
FARBEN = [
    dict(gruppe='haus', name='Warmweiss', hex=WW, rolle='flaeche-hell', belegt='Logo, Drucksache', foto='plakat-2026-09',
         fundstelle=fs(PL['2026-09']['band'], 'Band unter dem Bild, Plakat Mondfrau'), auch='Auf allen sechs Plakaten seit 11/2024 derselbe Ton (Modus und Median; März 2026 #F9F5F4). Leicht rosé.'),
    dict(gruppe='haus', name='Schiefer-Violett', hex=SV, rolle='schrift', belegt='Logo, Drucksache', foto='plakat-2026-03',
         fundstelle=fs(PL['2026-09']['tinte'], 'Wortmarke CULINARIUM, Plakat Mondfrau'), auch='Auf allen sechs Plakaten exakt gleich; ebenso die Zeile A UNiQUE EXPERiENCE und das Profilbild.'),
    dict(gruppe='haus', name='Rahmengrau', hex=RG, rolle='linie', belegt='Drucksache', foto='plakat-2026-03',
         fundstelle=fs(MS['rahmen'], 'die doppelte Linie um Wortmarke und Zeile, Plakat Panther mit Eisbecher; nur Grau ohne Farbstich'), auch='Median ' + MS['rahmen']['median'] + '. Im Kundenprofil «geschätzt #B0B0B0», hier gemessen.'),
]
ABENDE = [  # (Schlüssel, Name, Abend, Motiv, Bild)
    ('eisblau', 'Eisblau', '2024-11', 'Ski', 'plakat-2024-11', '29./30.11.2024'),
    ('orange', 'Orange', '2025-02', 'Panther auf dem Thron', 'plakat-2025-02', '21./22.02.2025'),
    ('gruen', 'Grasgrün', '2025-06', 'Gärtnerin', 'plakat-2025-06', '13./14.06.2025'),
    ('nachtblau', 'Nachtblau', '2025-11', 'Kürbis', 'plakat-2025-11', '14./15.11.2025'),
    ('ochsenblut', 'Ochsenblut', '2026-03', 'Panther mit Eisbecher', 'plakat-2026-03', '27./28.03.2026'),
    ('sepia', 'Sepia', '2026-09', 'Mondfrau', 'plakat-2026-09', '25./26.09.2026'),
]
KP = {'eisblau': '#B8E9FC', 'orange': '#ED7748', 'gruen': '#99B456', 'nachtblau': '#15354A', 'ochsenblut': '#881301', 'sepia': '#553827'}   # Kundenprofil Blatt 5
for k, n, a, mo, bild, dat in ABENDE:
    p = PL[a]['bild']
    FARBEN.append(dict(gruppe='abend', name=n, hex=p['hex'], rolle='akzent', belegt='Drucksache', foto=bild, abend=k,
                       fundstelle=fs(p, 'häufigster Ton der Illustration, Plakat %s (%s)' % (mo, dat)),
                       auch='Median %s; im Kundenprofil %s (andere Rechnung, gleiche Farbe).' % (p['median'], KP[k])))
FOTO_ROLLEN = [  # (Messname, Anzeigename, Rolle, Bild, Zusatz)
    ('Putz', 'Putz', 'flaeche-hell', 'putz', ''),
    ('Flur', 'Flurorange', 'akzent', 'flur', 'Liegt nah am Orange des Plakats vom Februar 2025.'),
    ('Kerze', 'Kerzenlicht', 'akzent', 'kerzen', 'Nur Wachs im Licht, überstrahlte Pixel ausgenommen.'),
    ('Honig', 'Honig', 'akzent', 'ballons', ''),
    ('Schiefertisch', 'Schiefertisch', 'flaeche-dunkel', 'glas-dunkel', ''),
    ('Barnacht', 'Barnacht', 'flaeche-dunkel', 'glas-dunkel', ''),
    ('Ziegel', 'Klinker', 'flaeche-dunkel', 'ecke', 'Liegt nah am Schiefer-Violett der Wortmarke.'),
    ('Campari', 'Campari', 'punkt', 'anstossen', 'Hier der Median: der Drink ist ein Verlauf, der häufigste Ton (#8B1424) ist nur sein dunkelster Teil.'),
]
for mn, n, r, bild, zus in FOTO_ROLLEN:
    f = FO[mn]; hexw = f['median'] if mn == 'Campari' else f['hex']
    FARBEN.append(dict(gruppe='foto', name=n, hex=hexw, rolle=r, belegt='Foto', foto=bild,
                       fundstelle=fs(f, f['was']), auch=('Median ' + f['median'] if mn != 'Campari' else 'Modus ' + f['hex']) + ('. ' + zus if zus else '')))
F = {f['name']: f['hex'] for f in FARBEN}

# ---------------------------------------------------------------- Farbwelten (abgeleitete Töne sind gerechnet)
NACHT_A = mix(SV, '#000000', .42)


def abend_toene(c, nacht=NACHT_A):
    return dict(gold=bis(c, '#FFFFFF', nacht, 4.5), gold_h=mix(bis(c, '#FFFFFF', nacht, 4.5), '#FFFFFF', .35), gold_h2=mix(c, '#FFFFFF', .72),
                gold_t=bis(c, '#000000', WW, 3.0), taupe=bis(c, '#000000', WW, 3.0), akzent=bis(c, '#000000', WW, 4.5), taupe_tief=bis(c, '#000000', WW, 4.5))


ABEND_TOENE = {k: abend_toene(F[n]) for k, n, *_ in ABENDE}
ABEND_DEFAULT = 'orange'
LICHT = dict(weiss=mix(WW, '#FFFFFF', .55), papier=WW, tinte=SV, rahmen=RG, rot=F['Campari'])
WELTEN = {
    'a': dict(name='Plakat', titel=['Schiefer', 'und Abendfarbe.'],
              satz='Das Schiefer-Violett der Wortmarke, abgedunkelt, trägt die dunklen Flächen; das Warmweiss des Plakatbands die hellen. '
                   'Betont wird mit der Farbe des Abends: jedes Plakat hat seine eigene, die Seite nimmt die des nächsten Abends. Solange kein Termin steht, Orange vom Februar 2025, dasselbe Orange wie im Flur der Bar.',
              css=dict(LICHT, creme=mix(WW, RG, .16), sand=mix(WW, RG, .45), marine=NACHT_A, d0=mix(SV, '#000000', .62), d1=mix(SV, '#000000', .52),
                       d2=mix(SV, '#000000', .34), d3=mix(SV, '#000000', .24), blau=SV, aare=mix(SV, '#FFFFFF', .12), aare_h=mix(SV, '#FFFFFF', .55),
                       **ABEND_TOENE[ABEND_DEFAULT]),
              knopf='Schiefer', akzent='Abendfarbe'),
    'b': dict(name='Kerzenlicht', titel=['Barnacht', 'und Kerze.'],
              satz='Die dunkle Tischplatte unter Rudis Tellern trägt die dunklen Flächen, Klinker und Barnacht geben die Tiefe. Betont wird mit dem Licht der Kerzen auf der Tafel und dem Honig der Glasballons an der Bar. '
                   'Warmweiss und die Schrift in Schiefer-Violett bleiben vom Plakat. Campari nur als Punkt.',
              css=dict(LICHT, creme=mix(WW, F['Putz'], .22), sand=mix(WW, F['Putz'], .5), marine=F['Schiefertisch'], d0=F['Barnacht'], d1=mix(F['Schiefertisch'], F['Barnacht'], .5),
                       d2=mix(F['Schiefertisch'], F['Klinker'], .25), d3=mix(F['Schiefertisch'], F['Klinker'], .4), blau=mix(F['Schiefertisch'], F['Klinker'], .62), aare=F['Klinker'],
                       aare_h=mix(F['Klinker'], '#FFFFFF', .5), gold=F['Kerzenlicht'], gold_h=mix(F['Kerzenlicht'], '#FFFFFF', .4), gold_h2=mix(F['Kerzenlicht'], '#FFFFFF', .72),
                       gold_t=F['Honig'], taupe=mix(F['Honig'], F['Kerzenlicht'], .25), akzent=bis(F['Honig'], '#000000', WW, 4.5), taupe_tief=bis(F['Honig'], '#000000', WW, 4.5)),
              knopf='Kerzenlicht', akzent='Kerzenlicht und Honig'),
}
VARS = ['weiss', 'papier', 'creme', 'sand', 'marine', 'd0', 'd1', 'd2', 'd3', 'blau', 'aare', 'aare_h', 'tinte', 'gold', 'gold_h', 'gold_h2', 'gold_t', 'taupe', 'akzent', 'taupe_tief', 'rot', 'rahmen']


def css_vars(d): return ';'.join('--%s:%s' % (k.replace('_', '-'), d[k]) for k in VARS if k in d)


def farben_css(pre=''):
    """Variablen beider Welten + sechs Abendfarben, je Abend nur die Betonung. Dazu die Tapeten."""
    s = '/* Culinarium Hannover · Farben und Farbwelten · Markenbuch Station 05 · 26.10.2026 · jede Farbe mit Fundstelle in marke.json */\n'
    s += ':root,[data-welt="a"]{%s;--tap-d:url(%szeichen/tapete-dunkel-a.svg);--tap-h:url(%szeichen/tapete-hell-a.svg)}\n' % (css_vars(WELTEN['a']['css']), pre, pre)
    for k, *_ in ABENDE:
        t = ABEND_TOENE[k]
        s += ':root:not([data-welt="b"])[data-abend="%s"],[data-welt="a"][data-abend="%s"]{%s}\n' % (k, k, ';'.join('--%s:%s' % (x.replace('_', '-'), t[x]) for x in t))
    s += '[data-welt="b"]{%s;--tap-d:url(%szeichen/tapete-dunkel-b.svg);--tap-h:url(%szeichen/tapete-hell-b.svg)}\n' % (css_vars(WELTEN['b']['css']), pre, pre)
    s += '/* Hausfarben */\n:root{' + ';'.join('--f-%s:%s' % (re.sub(r'[^a-z]+', '-', f['name'].lower().replace('ü', 'ue').replace('ä', 'ae')).strip('-'), f['hex']) for f in FARBEN) + '}\n'
    return s


# ---------------------------------------------------------------- Zeichen (aus zeichen.py, Original-Pixel des Plakats, potrace)
def lies(n): return open(os.path.join(M, 'zeichen', n), encoding='utf-8').read()


def teile(n):
    t = lies(n)
    return re.search(r'viewBox="([^"]+)"', t).group(1), re.search(r'<svg[^>]*>(.*)</svg>', t, re.S).group(1)


CVB, CIN = teile('c.svg'); XVB, XIN = teile('x.svg'); WVB, WIN = teile('wortmarke.svg'); ZVB, ZIN = teile('zeile.svg'); MVB, MIN = teile('wortmarke-mit-zeile.svg')


def sym_defs():
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            f'<symbol id="c" viewBox="{CVB}">{CIN}</symbol><symbol id="x" viewBox="{XVB}">{XIN}</symbol>'
            f'<symbol id="wortmarke" viewBox="{WVB}">{WIN}</symbol><symbol id="zeile" viewBox="{ZVB}">{ZIN}</symbol>'
            f'<symbol id="marke" viewBox="{MVB}">{MIN}</symbol></defs></svg>')


def eingebettet(vb, innen, x, y, h, farbe, deck):
    v = [float(a) for a in vb.split()]; w = h * v[2] / v[3]
    return f'<svg x="{x - w / 2:.2f}" y="{y - h / 2:.2f}" width="{w:.2f}" height="{h:.2f}" viewBox="{vb}" fill="{farbe}" fill-opacity="{deck}">{innen}</svg>'


# ---------------------------------------------------------------- Tapete: die doppelte Linie der Plakate als Gitter, das x an jeder Kreuzung, das C im Feld
def tapete(farbe, a_linie, a_zeichen, a_c):
    S = 224
    lin = (f'<g stroke="{farbe}" stroke-opacity="{a_linie}" stroke-width="1" fill="none">'
           f'<path d="M0 .5H{S}M0 4.5H{S}M.5 0V{S}M4.5 0V{S}"/></g>')
    xs = ''.join(eingebettet(XVB, XIN, x, y, 9, farbe, a_zeichen) for x, y in ((2.5, 2.5),))
    c = eingebettet(CVB, CIN, S / 2 + 2.5, S / 2 + 2.5, 24, farbe, a_c)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">{lin}{xs}{c}</svg>'


def schreib_tapeten():
    for k, w in WELTEN.items():
        c = w['css']
        gold = c['gold'] if k == 'b' else WELTEN['a']['css']['aare_h']
        open(os.path.join(M, 'zeichen', f'tapete-dunkel-{k}.svg'), 'w').write(tapete(gold, .07, .14, .09))
        open(os.path.join(M, 'zeichen', f'tapete-hell-{k}.svg'), 'w').write(tapete(SV, .04, .09, .05))


# ---------------------------------------------------------------- Zeichen-Dateien in den Hausfarben
def schreib_zeichen():
    for name, (vb, innen) in {'c': (CVB, CIN), 'x': (XVB, XIN), 'wortmarke': (WVB, WIN), 'zeile': (ZVB, ZIN), 'wortmarke-mit-zeile': (MVB, MIN)}.items():
        for fn, farbe in (('schiefer', SV), ('warmweiss', WW)):
            open(os.path.join(M, 'zeichen', f'{name}-{fn}.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="{farbe}">{innen}</svg>')
    # Zeichen im Browser: das C in Schiefer auf Warmweiss, quadratisch
    v = [float(a) for a in CVB.split()]; s = max(v[2], v[3]) * 1.34
    open(os.path.join(M, 'zeichen', 'icon.svg'), 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s:.0f} {s:.0f}"><rect width="100%" height="100%" rx="{s * .22:.0f}" fill="{WW}"/>'
        f'<svg x="{(s - v[2]) / 2:.0f}" y="{(s - v[3]) / 2:.0f}" width="{v[2]:.0f}" height="{v[3]:.0f}" viewBox="{CVB}" fill="{SV}">{CIN}</svg></svg>')


# ---------------------------------------------------------------- farben.svg (Farbkarten zum Mitnehmen)
def farben_svg():
    W, rh = 1200, 120
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="DM Mono, Menlo, monospace">' % (W, rh * len(FARBEN) + 40, W, rh * len(FARBEN) + 40),
           f'<rect width="100%" height="100%" fill="{WW}"/>']
    for i, f in enumerate(FARBEN):
        y = 20 + i * rh
        out.append(f'<rect x="20" y="{y}" width="200" height="{rh - 16}" rx="12" fill="{f["hex"]}"/>')
        for j, t in enumerate([mix(f['hex'], '#000000', .5), mix(f['hex'], '#000000', .25), f['hex'], mix(f['hex'], '#FFFFFF', .45), mix(f['hex'], '#FFFFFF', .8)]):
            out.append(f'<rect x="{240 + j * 112}" y="{y}" width="104" height="{rh - 50}" rx="8" fill="{t}"/><text x="{240 + j * 112}" y="{y + rh - 28}" font-size="12" fill="{SV}">{t}</text>')
        out.append(f'<text x="830" y="{y + 30}" font-size="19" fill="{SV}">{e(f["name"])}</text><text x="830" y="{y + 56}" font-size="14" fill="{SV}">{f["hex"]} · {e(f["belegt"])}</text>')
    out.append('</svg>')
    open(os.path.join(M, 'farben.svg'), 'w').write('\n'.join(out))


# ---------------------------------------------------------------- Schriften
SCHRIFTEN = [
    dict(rolle='titel', name='Fraunces Soft', schnitt='600 bis 900, Weichheit 100, «Wonky» an, optische Grösse 144', datei='marke/schriften/Fraunces-Soft-600_900.woff2',
         quelle='Google Fonts (github.com/google/fonts, ofl/fraunces), 26.10.2026, als feste Instanz gerechnet (_bau, fontTools)', lizenz='SIL Open Font License 1.1 (marke/schriften/OFL-fraunces.txt)',
         wofuer='Titel, Zutatenzeilen, grosse Zahlen'),
    dict(rolle='etikett', name='Urbanist', schnitt='700 bis 900, Versalien, das i klein, gesperrt', datei='marke/schriften/Urbanist-400_900.woff2',
         quelle='Google Fonts (ofl/urbanist), 26.10.2026', lizenz='SIL Open Font License 1.1 (marke/schriften/OFL-urbanist.txt)', wofuer='Kapitelzeilen, Bildzeilen, Knöpfe, das Band'),
    dict(rolle='lauf', name='Instrument Sans', schnitt='400 und 600', datei='marke/schriften/InstrumentSans-normal-400_600.woff2',
         quelle='Werkbank-Kit (Google Fonts), über Späher 02', lizenz='SIL Open Font License 1.1', wofuer='alles, was gelesen wird'),
    dict(rolle='mono', name='DM Mono', schnitt='400', datei='marke/schriften/DMMono-normal-400.woff2', quelle='Werkbank-Kit (Google Fonts), über Späher 02',
         lizenz='SIL Open Font License 1.1', wofuer='Zeiten, Preise, Plätze: gesetzt wie ein Bon aus der Küche'),
]
MATCH = json.load(open(os.path.join(H, 'match.json'))); MZ = json.load(open(os.path.join(H, 'match_zeile.json')))


def deck(liste, name): return next(x for x in liste if x['name'] == name)


SCHRIFTWAHL = [  # neben die Wortmarke gelegt (Master 2.2): (Name, CSS-Klasse, Urteil, Satz)
    ('Fraunces Soft 900', 'f-ti', 'gewählt', 'Eine Antiqua der 70er mit weichen, tropfenförmigen Enden wie in der Wortmarke; fett, aber nicht stumpf. Deckung %.2f. Liegt schon in der Website.' % deck(MATCH['wort'], 'Fraunces 900 Soft')['deckung']),
    ('Gravitas One', 'f-gr', 'zweite Wahl', 'Die einzige freie Schrift, die so breit läuft wie CULINARIUM und dünne Diagonalen gegen dicke Stämme setzt (Breite %.2f). Mit Füsschen, ohne Tropfen.' % deck(MATCH['wort'], 'Gravitas One')['breite']),
    ('Bagel Fat One', 'f-ba', 'nicht', 'Höchste Deckung (%.2f), aber rund und weich wie ein Spielzeug; das Haus ist scharf geschnitten.' % deck(MATCH['wort'], 'Bagel Fat One')['deckung']),
    ('Dela Gothic One', 'f-de', 'nicht', 'Fett und breit wie ein Plakat (Deckung %.2f), aber eine Groteske. Titel in Groteske wirken bei uns nie fertig.' % deck(MATCH['wort'], 'Dela Gothic One')['deckung']),
]
ZEILENWAHL = [
    ('Urbanist 900', 'gewählt', 'Deckung %.2f bei %.2f em Sperrung; geometrisch wie die Zeile, ohne Kugelenden. Liegt schon in der Website.' % (deck(MZ, 'Urbanist 900')['deckung'], deck(MZ, 'Urbanist 900')['sperrung_em'])),
    ('Fredoka 700 schmal', 'nicht', 'Höchste Deckung (%.2f), aber durchweg gerundet; die Zeile des Hauses hat gerade Enden.' % deck(MZ, 'Fredoka 700 schmal')['deckung']),
    ('Lexend 800', 'möglich', 'Deckung %.2f; ruhiger, etwas schmaler.' % deck(MZ, 'Lexend 800')['deckung']),
]

# ---------------------------------------------------------------- Ton und eigene Welt
TON = dict(
    charakter=[
        'Zwei teilen einen Abend: Rudi kocht ein Drei-Gänge-Menü, Momo mixt fünf Signature Drinks dazu und erklärt jeden selbst, mit Fatwashing, Milkwashing und Klärung durch Enzyme.',
        'Der Ort ist eine Bar in Linden, das Walk on the Wild Side in der Haasemannstraße 13: draussen Klinker, Schilder und Graffiti, drinnen Kerzen, Kupferlicht und eine lange Tafel. Ein Freitag um 19 Uhr, ein Samstag um 17 Uhr, zuletzt «AUSGEBUCHT!».',
        'Jeder Abend kündigt sich mit einem eigenen Plakat an, Pin-up oder Art déco in einer eigenen Farbe, darunter immer dasselbe warmweisse Band mit CULINARIUM. Der Ton ist herzlich, im Du, mit einer Knappheit, die stimmt.'],
    eigene_worte=['A UNiQUE EXPERiENCE BY MOMO X RUDI', 'geht in die nächste Runde', 'Signature Drinks', 'Cocktail Tasting', 'dazugehörige Schulung',
                  'Momo wird persönlich jeden Drink für dich erklären', 'nur 14 Plätze pro Abend', 'AUSGEBUCHT!', 'Vorverkauf', 'Walk on the Wild Side',
                  'AUBERGINE / KOKOS / LIMETTE / SESAM', 'Food Pairing'],
    nicht=['Geschmacksexplosionen (steht in jeder Ankündigung, bleibt dort)', 'kulinarische Reise', 'unvergesslich', 'Genuss pur', 'ein Fest für die Sinne', 'Geheimtipp',
           'Emojis aus den Beiträgen', '«Hasemannstrasse» (richtig: Haasemannstraße)', 'Sie-Ansprache', '«vegetarisch» als Merkmal der Marke (Rudi 26.10.2026: nicht mehr rein vegetarisch)', 'Fakten der Bar als Fakten von Culinarium (Falstaff, Google-Noten)'],
    quellen=['_quelle/extern/ig/beitraege.md (Beiträge 2023–2026)', '_quelle/extern/ig-team/beitraege.md (Rudi)', '_kette/03-sammler/fakten.json', '_kette/02-spaeher/befund.md', '_quelle/recherche/Kundenprofil.md Blatt 5'])

EIGENE_WELT = dict(
    satz=['Culinarium ist die Welt eines Abends in einer Bar: eine lange Tafel bei Kerzenlicht, ein Tresen voller Flaschen und Glasballons, zwei Leute, die kochen und mixen und dabei erzählen, vierzehn Gäste, die zusammen anstossen.',
          'Die Marke ist ein Plakat-System: oben jedes Mal ein neues Bild in einer neuen Farbe, unten immer das Band mit der Wortmarke. Daraus kommt die Ordnung der Seite: das Bild wechselt, das Band bleibt, die Farbe gehört dem nächsten Abend.',
          'Urban ist es von aussen, Klinker, Schilder, Graffiti an der Ecke in Linden; warm von innen, Kupfer, Kerze, dunkler Tisch. Die Seite spielt beides: dunkle Flächen wie die Bar, warmweisse Bänder wie das Plakat, und Bilder, die paarweise ankommen wie Teller und Glas.'],
    unterschied_zu={
        'Grand Beau-Rivage': 'Belle Époque, Portier, Ballsaal, Marine und Gold, Medaillon-Tapete; hier eine Bar in Linden, Schiefer-Violett, Abendfarbe statt Gold, die Tapete aus der doppelten Plakatlinie.',
        'Carlton-Europe': 'Vintage-Hotel mit Dachterrasse, Kissen, Weinkeller, Türflügel im Auftakt; hier kein Hotel, ein Abend an einer Tafel, zwei Bilder, die sich treffen statt aufgehen.',
        'Hotel Seiler au Lac · Waldhotel Doldenhorn · Landgasthof Ruedihus · Berghotel Gasterntal': 'See, Wald, Berg und Weg; hier Stadt, Klinker und Kerzenlicht, keine Landschaft.',
        'Zurbriggen (vier Häuser)': 'Berg, Schnee, Lärche, Grat als Naht; hier die doppelte Linie des Plakats als einzige Linie.',
        'Taverne zum Schäfli · Wirtschaft am Schlössli': 'Riegelhaus und Hafen, Wappen und Zeiger, Petrona und Open Sans; hier eine Display-Antiqua der 70er und eine Zeile mit kleinem i.',
        'Salt & Silver': 'Hamburger Taco-Bar mit Reise-Erzählung und Vorhang; hier kein Vorhang, die Wechselfarbe des Abends und Zutatenzeilen in Rudis Schreibweise.',
        'Tasty Grand Hotel': 'erfundenes Hotel; hier ein echtes Paar aus Küche und Bar mit eigenen Fotos.'})

DARSTELLUNG = 'Das Band unter dem Bild: wie auf jedem Plakat sitzt unter dem Foto ein warmweisses Band mit doppelter Linie, darin Name, Datum oder Zeile in der Etikettschrift. Keine Schrift auf dem Foto, kein Schild darüber. Dazu die Abendfarbe: die Betonung der ganzen Seite wechselt mit dem Plakat des nächsten Abends.'
BEWEGUNG = 'Anstossen: zwei Bilder steigen getrennt von unten herauf, das zweite eine Achtelsekunde später, und treffen sich an der Naht mit einem gemeinsamen, einzigen Puls, wie zwei Gläser. Nur transform, nichts kommt von der Seite.'


# ---------------------------------------------------------------- Probe: ein Stück der künftigen Seite
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'


def ki(t):
    """Etiketten des Hauses: Versalien, das i klein (wie A UNiQUE EXPERiENCE)."""
    return '<span class="kw">' + e(t.upper()).replace('I', '<span class="ki">i</span>') + '</span>'


def knopf(text, href, kl='', neu=False):
    z = ' target="_blank" rel="noopener"' if neu else ''
    return f'<a class="kn {kl}" href="{href}"{z}><span>{ki(text)}</span><i>{PF}</i></a>'


PROBE_CSS = r'''
@font-face{font-family:'Fraunces Soft';font-style:normal;font-weight:400 900;font-display:swap;src:url('schriften/Fraunces-Soft-600_900.woff2') format('woff2')}
@font-face{font-family:'Urbanist';font-style:normal;font-weight:400 900;font-display:swap;src:url('schriften/Urbanist-400_900.woff2') format('woff2')}
@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:400 600;font-display:swap;src:url('schriften/InstrumentSans-normal-400_600.woff2') format('woff2')}
@font-face{font-family:'DM Mono';font-style:normal;font-weight:400;font-display:swap;src:url('schriften/DMMono-normal-400.woff2') format('woff2')}
@font-face{font-family:'Titel Ersatz';src:local('Georgia');size-adjust:92%}
:root{--titel:'Fraunces Soft','Titel Ersatz',Georgia,serif;--etikett:'Urbanist','Arial Black',Arial,sans-serif;--sans:'Instrument Sans',system-ui,sans-serif;--mono:'DM Mono',ui-monospace,Menlo,monospace;
  --e1:cubic-bezier(.16,1,.3,1);--rand:clamp(16px,4.4vw,72px);--rund:clamp(22px,2.6vw,36px)}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;background:var(--marine);overflow-x:clip}
body{margin:0;font:400 17.5px/1.62 var(--sans);color:var(--tinte);background:var(--marine);-webkit-font-smoothing:antialiased;overflow-x:clip;font-synthesis:none}
img{display:block;max-width:100%}
a{color:inherit;text-decoration:none}
.ki{text-transform:none}
.in{max-width:1440px;margin:0 auto;padding:0 var(--rand)}
.dunkel{background-color:var(--marine);background-image:var(--tap-d);background-size:224px;color:var(--weiss)}
.hell{background-color:var(--papier);background-image:var(--tap-h);background-size:224px;color:var(--tinte)}
/* Etikett: Versalien, das i klein, gesperrt */
.et{font:800 clamp(.72rem,.82vw,.84rem)/1.2 var(--etikett);letter-spacing:.16em;text-transform:uppercase}
/* Knopf: Pille mit Tiefe, runder Knauf mit Pfeil, Glanzstreif, gibt nach */
.kn{position:relative;display:inline-flex;align-items:center;gap:18px;height:56px;padding:0 6px 0 28px;border-radius:28px;overflow:hidden;isolation:isolate;
  font:800 12px/1 var(--etikett);letter-spacing:.16em;text-transform:uppercase;color:var(--weiss);
  background:linear-gradient(180deg,var(--aare),var(--blau) 55%,var(--d1));
  box-shadow:inset 0 1px 0 rgba(255,255,255,.22),inset 0 -2px 0 rgba(0,0,0,.35),0 22px 34px -20px rgba(0,0,0,.65);transition:transform .5s var(--e1)}
.kn::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.28) 50%,transparent 70%);transform:translateX(-120%)}
.kn:hover{transform:translateY(-2px)}.kn:hover::after{transform:translateX(120%);transition:transform .9s var(--e1)}.kn:active{transform:translateY(1px) scale(.985)}
.kn i{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,var(--gold-h),var(--gold) 60%,var(--gold-t));color:var(--d0);box-shadow:inset 0 1px 0 rgba(255,255,255,.6),0 6px 12px -6px rgba(0,0,0,.6)}
.kn i svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:1.6}
.kn--hell{color:var(--tinte);background:linear-gradient(180deg,var(--weiss),var(--papier) 55%,var(--creme));box-shadow:inset 0 1px 0 #fff,inset 0 -2px 0 rgba(0,0,0,.08),0 22px 34px -20px rgba(0,0,0,.55)}
.kn--hell i{background:linear-gradient(180deg,var(--aare),var(--blau) 60%,var(--d1));color:var(--gold)}
/* Auftritt: deckend von unten, satt an den Platz (Master 4); ausgelöst am Rand */
.js [data-a]{opacity:0;transform:translate3d(0,46px,0);transition:opacity .7s var(--e1),transform 1.3s var(--e1);transition-delay:calc(var(--i,0)*.11s)}
.js [data-a].da{opacity:1;transform:none}
/* Anstossen: zwei Bilder steigen getrennt herauf, das zweite eine Achtelsekunde später, ein gemeinsamer Puls an der Naht */
.paar{display:grid;grid-template-columns:1fr 1fr;gap:0}
.paar figure{margin:0;position:relative;overflow:hidden}
.paar img{width:100%;height:100%;object-fit:cover}
.js .paar figure{transform:translate3d(0,64px,0);transition:transform 1.35s var(--e1)}
.js .paar figure:nth-child(2){transition-delay:.125s}
.js .paar.da figure{transform:none}
.js .paar.da{animation:stoss .62s var(--e1) 1.18s 1 both}
@keyframes stoss{0%{transform:scale(1)}38%{transform:scale(1.012)}100%{transform:scale(1)}}
.paar figure img{transform:scale(1.1);transition:transform 2.2s var(--e1)}
.paar.da figure img{transform:none}
/* Das Band: warmweiss, doppelte Linie oben und unten, wie unter jedem Plakat */
.band{position:relative;background:var(--papier);color:var(--tinte);border-top:1px solid var(--rahmen);border-bottom:1px solid var(--rahmen);box-shadow:inset 0 3px 0 var(--papier),inset 0 4px 0 var(--rahmen),inset 0 -3px 0 var(--papier),inset 0 -4px 0 var(--rahmen)}
.band__in{display:grid;grid-template-columns:minmax(0,1.2fr) auto;align-items:center;gap:clamp(18px,3vw,48px);padding:clamp(22px,2.6vw,36px) var(--rand);max-width:1440px;margin:0 auto}
.band__w{width:min(100%,640px);color:var(--tinte)}
.band__z{width:min(100%,520px);color:var(--tinte);margin-top:clamp(10px,1.1vw,16px)}
.band__r{display:flex;flex-direction:column;align-items:flex-end;gap:14px;text-align:right}
.band__r .et{color:var(--akzent)}
.auftakt{position:relative;background:var(--marine)}
.auftakt .paar{height:min(82svh,880px)}
.auftakt .paar figure:first-child img{object-position:50% 30%}
.auftakt .paar figure:last-child img{object-position:50% 25%}
.naht{position:absolute;left:50%;top:0;bottom:0;width:0;z-index:2;pointer-events:none}
.naht svg{position:absolute;left:50%;top:50%;width:clamp(30px,3vw,46px);height:auto;transform:translate(-50%,-50%);color:var(--gold);opacity:0;transition:opacity .6s ease 1.25s}
.paar.da~.naht svg,.da .naht svg{opacity:1}
/* Momos Kapitel: Zutatenzeile */
.zt{padding:clamp(90px,10vw,160px) 0}
.zt__g{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:clamp(28px,4.4vw,72px);align-items:center}
.zt h2{font:700 clamp(2.1rem,4.6vw,4.9rem)/.98 var(--titel);margin:18px 0 26px;letter-spacing:-.01em;color:var(--weiss);text-transform:uppercase}
.zt h2 .sl{color:var(--gold);font-weight:600;padding:0 .08em}
.zt p.l{max-width:46ch;color:color-mix(in srgb,var(--weiss) 86%,transparent);margin:0 0 30px}
.zt .et{color:var(--gold)}
.zt blockquote{margin:0 0 34px;padding-left:22px;border-left:2px solid var(--gold);font:600 clamp(1.15rem,1.6vw,1.45rem)/1.3 var(--titel);color:var(--weiss);max-width:30ch}
.zt blockquote small{display:block;margin-top:10px;font:800 11px/1.2 var(--etikett);letter-spacing:.16em;text-transform:uppercase;color:var(--gold-h)}
.zt .paar{border-radius:var(--rund);overflow:hidden;aspect-ratio:5/4;box-shadow:0 50px 80px -50px rgba(0,0,0,.85)}
.unterband{display:flex;justify-content:space-between;gap:16px;padding:14px 20px;background:var(--papier);color:var(--tinte);border-top:1px solid var(--rahmen);box-shadow:inset 0 3px 0 var(--papier),inset 0 4px 0 var(--rahmen)}
.unterband .et{color:var(--tinte)}
.unterband .et b{font-weight:800;color:var(--akzent)}
/* Rudis Kapitel: der Teller in vier Wörtern, der Bon */
.gang{padding:clamp(90px,10vw,160px) 0;border-radius:var(--rund) var(--rund) 0 0;margin-top:calc(var(--rund)*-1);position:relative}
.gang__w{font:800 clamp(2.4rem,7.2vw,7.4rem)/.92 var(--titel);letter-spacing:-.015em;text-transform:uppercase;margin:16px 0 clamp(36px,4vw,60px);color:var(--tinte);text-wrap:balance}
.gang__w .sl{color:var(--taupe);font-weight:600}
.gang .et{color:var(--akzent)}
.gang__g{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr);gap:clamp(24px,3.6vw,60px);align-items:end}
.gang__b{margin:0;border-radius:var(--rund);overflow:hidden;box-shadow:0 50px 80px -50px rgba(40,30,40,.6)}
.gang__b img{width:100%;aspect-ratio:3/2;object-fit:cover}
.bon{position:relative;background:#fff;color:#1e1d22;padding:28px 26px 30px;border-radius:6px;font:400 13.5px/1.75 var(--mono);box-shadow:0 2px 0 rgba(0,0,0,.04),0 40px 60px -36px rgba(40,30,40,.55);transform:rotate(0deg)}
.bon__k{display:flex;flex-direction:column;align-items:center;gap:8px;padding-bottom:16px;margin-bottom:14px;border-bottom:1px dashed #b9b4b4}
.bon__k svg{width:78%;color:var(--tinte)}
.bon dl{display:grid;grid-template-columns:auto 1fr;gap:2px 16px;margin:0}
.bon dt{text-transform:uppercase;letter-spacing:.08em;color:#6b6770}
.bon dd{margin:0;text-align:right}
.bon .summe{margin-top:14px;padding-top:12px;border-top:1px dashed #b9b4b4;display:flex;justify-content:space-between;font-size:15px}
.bon .stand{margin-top:14px;font-size:11px;line-height:1.5;color:#6b6770;text-align:center}
.bon .kn{margin-top:22px;width:100%;justify-content:space-between}
/* die Abendfarbe zum Umschalten */
.abend{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:clamp(40px,4vw,60px)}
.abend .et{color:var(--tinte);margin-right:8px}
.abend button{all:unset;cursor:pointer;display:flex;align-items:center;gap:10px;padding:6px 14px 6px 6px;border-radius:30px;background:#fff;box-shadow:inset 0 0 0 1px rgba(0,0,0,.07),0 10px 18px -12px rgba(0,0,0,.4);font:800 11px/1 var(--etikett);letter-spacing:.14em;text-transform:uppercase}
.abend button img{width:30px;height:30px;border-radius:50%;object-fit:cover}
.abend button[aria-pressed=true]{box-shadow:inset 0 0 0 2px var(--akzent),0 10px 18px -12px rgba(0,0,0,.4)}
.abend button:focus-visible{outline:2px solid var(--akzent);outline-offset:3px}
.pfuss{padding:46px var(--rand) 56px;text-align:center;font-size:13.5px;color:color-mix(in srgb,var(--weiss) 70%,transparent)}
.welt-wahl{position:fixed;right:14px;top:14px;z-index:9;display:flex;gap:6px;padding:6px;border-radius:30px;background:var(--d0);box-shadow:0 14px 30px -14px rgba(0,0,0,.6),inset 0 0 0 1px color-mix(in srgb,var(--gold) 40%,transparent)}
.welt-wahl a{padding:11px 16px;border-radius:24px;font:800 11px/1 var(--etikett);letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.82)}
.welt-wahl a[aria-current=true]{color:var(--d0);background:linear-gradient(180deg,var(--gold-h),var(--gold))}
.aufnahme .welt-wahl{display:none}
@media (max-width:900px){.zt__g,.gang__g{grid-template-columns:1fr}.band__in{grid-template-columns:1fr}.band__r{align-items:flex-start;text-align:left}.auftakt .paar{height:62svh}}
@media (max-width:520px){.welt-wahl{left:14px;right:14px;justify-content:center}.bon{font-size:12.5px}}
@media (prefers-reduced-motion:reduce){.js [data-a],.js .paar figure,.paar figure img{opacity:1;transform:none;transition:none}.js .paar.da{animation:none}}
'''

PROBE_JS = r'''<script>
(function(){var q=new URLSearchParams(location.search),w=q.get('welt'),a=q.get('abend'),b=document.body;
if(w==='b')b.setAttribute('data-welt','b');if(a)b.setAttribute('data-abend',a);
document.querySelectorAll('.welt-wahl a').forEach(function(x){x.setAttribute('aria-current',String((w||'a')===x.dataset.w))});
document.querySelectorAll('[data-abend-knopf]').forEach(function(k){k.setAttribute('aria-pressed',String((b.getAttribute('data-abend')||'%(abend)s')===k.dataset.abendKnopf));
 k.addEventListener('click',function(){b.setAttribute('data-abend',k.dataset.abendKnopf);document.querySelectorAll('[data-abend-knopf]').forEach(function(o){o.setAttribute('aria-pressed',String(o===k))})})});
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('da');io.unobserve(x.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:0});
document.querySelectorAll('[data-a],.paar').forEach(function(el){io.observe(el)});})();
</script>'''


def probe():
    abend_k = ''.join(f'<button type="button" data-abend-knopf="{k}"><img src="bilder/{bild}.jpg" alt="">{ki(n)}</button>' for k, n, a, mo, bild, dat in ABENDE)
    body = f'''{sym_defs()}
<nav class="welt-wahl" aria-label="Farbwelt"><a href="?welt=a" data-w="a">A · Plakat</a><a href="?welt=b" data-w="b">B · Kerzenlicht</a></nav>
<header class="auftakt" aria-label="Probe: Auftakt">
  <div class="paar" role="img" aria-label="Zwei Bilder Wand an Wand: am Tresen wird geschüttelt, am Tisch der Gäste wird erzählt">
    <figure><img src="bilder/tresen.jpg" alt="" decoding="async"></figure>
    <figure><img src="bilder/tafel-koch.jpg" alt="" decoding="async"></figure>
  </div>
</header>
<section class="band" aria-label="Das Band">
  <div class="band__in">
    <div data-a><h1 style="margin:0"><svg class="band__w" viewBox="{WVB}" fill="currentColor" role="img" aria-label="Culinarium"><use href="#wortmarke"/></svg></h1>
      <svg class="band__z" viewBox="{ZVB}" fill="currentColor" role="img" aria-label="A unique experience by Momo x Rudi"><use href="#zeile"/></svg></div>
    <div class="band__r" data-a style="--i:1"><p class="et" style="margin:0">{ki('Haasemannstraße 13 · Hannover-Linden')}</p>
      {knopf('Platz anfragen', 'https://www.instagram.com/culinarium_hannover/', neu=True)}</div>
  </div>
</section>
<section class="zt dunkel" aria-label="Probe: Momos Kapitel"><div class="in zt__g">
  <div data-a><p class="et">{ki('Das Glas · Signature Drinks')}</p>
    <h2>Fatwashing<span class="sl">/</span> Milkwashing<span class="sl">/</span> Enzyme</h2>
    <p class="l">Zu jedem Gang ein Drink, fünf an einem Abend, mit einem Cocktail Tasting und einer dazugehörigen Schulung.</p>
    <blockquote>«Momo wird persönlich jeden Drink für dich erklären.»<small>{ki('Aus jeder Ankündigung seit 2024')}</small></blockquote>
    {knopf('Den nächsten Abend sehen', '#gang')}</div>
  <div data-a style="--i:1"><div class="paar" style="aspect-ratio:5/4"><figure><img src="bilder/giessen.jpg" alt="Ein Drink wird am Tresen eingegossen" loading="lazy" decoding="async" style="object-position:55% 40%"></figure><figure><img src="bilder/schaum.jpg" alt="Schaum aus dem Siphon auf einem Drink" loading="lazy" decoding="async"></figure></div>
    <div class="unterband"><span class="et">{ki('Am Tresen')}</span><span class="et"><b>{ki('Momo x Rudi')}</b></span></div></div>
</div></section>
<section class="gang hell" id="gang" aria-label="Probe: Rudis Kapitel"><div class="in">
  <p class="et" data-a>{ki('Der Teller · Rudi, Oktober 2026')}</p>
  <h2 class="gang__w" data-a style="--i:1">Aubergine<span class="sl"> / </span>Kokos<span class="sl"> / </span>Limette<span class="sl"> / </span>Sesam</h2>
  <div class="gang__g">
    <div data-a><figure class="gang__b"><img src="bilder/pass.jpg" alt="Angerichtete Teller in Reihe" loading="lazy" decoding="async"></figure><div class="unterband" style="border-radius:0 0 14px 14px;margin:-14px 14px 0;position:relative"><span class="et">{ki('Am Pass')}</span><span class="et"><b>{ki('Angerichtet')}</b></span></div></div>
    <aside class="bon" data-a style="--i:1" aria-label="Der Abend in Kürze">
      <div class="bon__k"><svg viewBox="{WVB}" fill="currentColor" aria-hidden="true"><use href="#wortmarke"/></svg><span>WALK ON THE WILD SIDE</span></div>
      <dl><dt>Freitag</dt><dd>19:00</dd><dt>Samstag</dt><dd>17:00</dd><dt>Menü</dt><dd>3 Gänge</dd><dt>Drinks</dt><dd>5 Signature Drinks</dd><dt>Plätze</dt><dd>14</dd></dl>
      <div class="summe"><span>PRO PERSON</span><span>89,00 EUR</span></div>
      <p class="stand">Stand der Abende im März und September 2026 · der nächste Termin ist nicht angekündigt</p>
      {knopf('Auf die Liste', 'https://www.instagram.com/culinarium_hannover/', 'kn--hell', neu=True)}
    </aside>
  </div>
  <div class="abend" data-a><span class="et">{ki('Die Abendfarbe')}</span>{abend_k}</div>
</div></section>
<footer class="pfuss dunkel"><p>Probe der Designidentität · Markenbuch Culinarium Hannover, Station 05 · Entwurf von Tasty Studios, nicht die offizielle Seite · Fotos aus Rudis Dateien, Plakate vom Konto @culinarium_hannover · Fakten aus den Beiträgen 2024–2026 · Wortmarke ist Platzhalter, das Original schickt Rudi nach · Knöpfe führen zum Instagram-Profil, dem heutigen Buchungsweg</p></footer>
'''
    s = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
         '<meta name="robots" content="noindex,nofollow"><title>Probe · Culinarium Hannover</title>'
         '<meta name="description" content="Ein Stück der künftigen Seite in Titelschrift, Farbwelt, Knopf, Tapete und Rudis Fotos.">'
         '<link rel="icon" href="zeichen/icon.svg" type="image/svg+xml"><link rel="preload" href="bilder/tresen.jpg" as="image"><link rel="preload" href="bilder/tafel-koch.jpg" as="image">'
         f'<style>{farben_css()}{PROBE_CSS}</style><script>document.documentElement.classList.add("js")</script></head>'
         f'<body data-abend="{ABEND_DEFAULT}">{body}{PROBE_JS.replace("%(abend)s", ABEND_DEFAULT)}</body></html>')
    open(os.path.join(M, 'probe.html'), 'w', encoding='utf-8').write(s)


# ---------------------------------------------------------------- marke.json
def marke_json():
    d = dict(
        farben=[dict(name=f['name'], hex=f['hex'], rolle=f['rolle'], belegt=f['belegt'], fundstelle=f['fundstelle'], auch=f['auch'],
                     foto='marke/bilder/%s.jpg' % f['foto'] if f.get('foto') else None, **({'abend': f['abend']} if f.get('abend') else {})) for f in FARBEN],
        abendfarben=[dict(kennung=k, name=n, plakat=dat, motiv=mo, hex=F[n], toene=ABEND_TOENE[k], bild='marke/bilder/%s.jpg' % bild) for k, n, a, mo, bild, dat in ABENDE],
        abendfarbe_vorgabe=dict(kennung=ABEND_DEFAULT, grund='nächster Termin nicht angekündigt (Profil 25.10.2026); Orange vom Februar 2025 liegt nah am gemessenen Flur der Bar'),
        farbwelten=[dict(kennung=k, name=w['name'], satz=w['satz'], flaechen=[w['css'][x] for x in ('marine', 'd2', 'blau', 'papier', 'creme')],
                         akzent=w['akzent'], betonung=w['css']['gold'], betonung_auf_hell=w['css']['akzent'], schrift=w['css']['tinte'], linie=RG, punkt=w['css']['rot'],
                         css=w['css'], tapete=['marke/zeichen/tapete-dunkel-%s.svg' % k, 'marke/zeichen/tapete-hell-%s.svg' % k], probe='marke/probe.html?welt=%s' % k) for k, w in WELTEN.items()],
        farbwelt_gewaehlt=dict(k='a', name=WELTEN['a']['name'], wort='Robert 26.10.2026: «a» (weitergegeben von der Sitzung «Culinarium · Rudis Dateien aus Mail und Drive holen»)'),
        farbwelt_verworfen=dict(k='b', name=WELTEN['b']['name'], wo='marke/markenbuch.html#welten'),
        abendfarbe_gewaehlt=None,
        schriften=SCHRIFTEN,
        schriftwahl=dict(titel=[dict(name=n, urteil=u, satz=s) for n, c, u, s in SCHRIFTWAHL], zeile=[dict(name=n, urteil=u, satz=s) for n, u, s in ZEILENWAHL],
                         messung='_bau/match.json, _bau/match_zeile.json (Deckung Buchstabe für Buchstabe gegen die Original-Pixel des Plakats)'),
        wortmarke=dict(status='platzhalter', platzhalter_grund='Rudi am 26.10.2026 (über die Sitzung «Culinarium Hannover Recherche»): Die Wortmarke aus dem Instagram-Profilbild und den Plakaten ist nicht sein Logo, er schickt das echte nach. Bis dahin Platzhalter; Zeichen, Titelschrift und Logo-Regeln werden mit dem Original neu geprüft.',
                       datei='marke/zeichen/wortmarke.svg', art='svg', mit_zeile='marke/zeichen/wortmarke-mit-zeile.svg', zeile='marke/zeichen/zeile.svg',
                       original='_quelle/logo/culinarium-profilbild-1080.jpg (Profilbild 1080 × 1080) und _quelle/logo/nachgezogen/wortmarke-und-zeile-aus-plakat-2026-09.png (Plakat 2014 px)',
                       vektor='Zug der Original-Pixel aus dem Plakat mit potrace (_bau/zeichen.py), Deckung gegen das Original %s (Wortmarke) und %s (Zeile); keine Datei des Gestalters' %
                              (json.load(open(os.path.join(H, 'zeichen.json')))['wortmarke']['deckung'], json.load(open(os.path.join(H, 'zeichen.json')))['zeile']['deckung']),
                       abgeleitete_titelschrift='Fraunces Soft 600–900 (Antiqua der 70er, tropfenförmige Enden); vorläufig, abgeleitet vom Platzhalter, mit dem Original neu prüfen', schrift_der_wortmarke='nicht belegt; Kundenprofil nennt Gazpacho, Brasika, Moret, Hatton als verwandt (nur visuell)'),
        zeichen=['marke/zeichen/c.svg', 'marke/zeichen/x.svg', 'marke/zeichen/icon.svg'],
        zeichen_satz='Vorläufig, aus dem Platzhalter: Das C ist der erste Buchstabe der Wortmarke, freigestellt; das x kommt aus «MOMO X RUDI» in der Zeile. Beide unverändert aus dem Zug der Original-Pixel.',
        tapete=dict(was='Gitter aus der doppelten Linie der Plakate, Rapport 176 px, an jeder Kreuzung das x, in jedem Feld das C, Ton in Ton',
                    dateien=['marke/zeichen/tapete-dunkel-a.svg', 'marke/zeichen/tapete-hell-a.svg', 'marke/zeichen/tapete-dunkel-b.svg', 'marke/zeichen/tapete-hell-b.svg']),
        knopf=dict(form='Pille 56 px, Etikettschrift Urbanist 800 in Versalien mit kleinem i, rechts runder Knauf mit Pfeil in der Betonungsfarbe',
                   tiefe='Verlauf in drei Stufen, Lichtkante oben, dunkle Kante unten, weicher Schatten; Glanzstreif beim Überfahren, hebt sich 2 px, gibt beim Drücken nach'),
        band=dict(was='Warmweisses Band mit doppelter Linie oben und unten, wie unter jedem Plakat; trägt Wortmarke, Zeile, Datum, Namen, Bildzeilen',
                  nie='kein gerahmtes Schild auf einem Foto, keine Plakette, keine Einkerbung'),
        darstellungsidee=DARSTELLUNG, bewegungsidee=BEWEGUNG,
        merkmale_nicht=['vegetarisch (Rudi 26.10.2026: Culinarium ist nicht mehr rein vegetarisch)'],
        ton=TON, welt='grand', eigene_welt=EIGENE_WELT, familie_machart=None,
        bilder='marke/bilder/herkunft.json (nur Rudis Dateien und die Plakate des eigenen Kontos)',
        seiten=dict(markenbuch='marke/markenbuch.html', probe='marke/probe.html', logo_richtig_falsch='marke/logo-richtig-falsch/index.html'),
        stand='26.10.2026; Farbwelt A «Plakat» gewählt (Robert 26.10.2026), Abendfarbe nicht gewählt, Vorgabe Orange')
    json.dump(d, open(os.path.join(P, 'marke.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    schreib_zeichen(); schreib_tapeten(); farben_svg()
    open(os.path.join(M, 'farben.css'), 'w').write(farben_css())
    probe(); marke_json()
    for k, w in WELTEN.items():
        c = w['css']; print(k, w['name'], 'Schrift/Papier %.1f' % kontrast(c['tinte'], c['papier']), 'Betonung/Nacht %.1f' % kontrast(c['gold'], c['marine']), 'Akzent/Papier %.1f' % kontrast(c['akzent'], c['papier']))
    for k, t in ABEND_TOENE.items(): print('  Abend', k, t['gold'], t['akzent'])
    print('gebaut: probe.html, farben.css, farben.svg, Tapeten, Zeichen, marke.json')
