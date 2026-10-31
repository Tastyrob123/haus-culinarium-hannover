#!/usr/bin/env python3
"""Culinarium Hannover · Team-Seite, «Wie es kam.» zweite Runde, 10 Fassungen, direkt in der echten Seite, 27.10.2026.
Robert: «Kannst du mir bitte visuelle Alternativen für diesen Abschnitt geben? Wie man das alternativ darstellen könnte.»
Heute: Titel mittig, sechs Bildkarten im Raster 3 × 2. Keine der 45 Fassungen aus chronik_wahl.py, chronik_wahl2.py und kam_wahl.py
wiederholt sich. Diesmal ohne Gegenstands-Spiel: jede Fassung ist eine andere Anordnung im Vokabular der Seite (Fraunces gross,
Bildwand mit Fuge, Daten in Kerze), dicht mit Fotos (Memory: Varianten dicht in echter Seite).
Fotos: keines, das sonst auf leute.html steht, keine Köpfe der drei (w3, momo_hoch, Gruppenfotos), keine Gesichter hervorgehoben.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut kam-wahl-2.html (Leiste unten, Pfeiltasten, ?kam=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/kam_wahl2.py (liest das fertige leute.html)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION

HIER = bau.HIER

# Wann (wie heute), Monat, Jahr, Satz (wie heute), Bilder je Moment
S = [
    ('Oktober 2017', 'Oktober', '2017', 'Das Walk on the Wild Side öffnet in der ehemaligen Fußballkneipe Linden Journal.',
     ['schildnacht', 'ecke', 'barnacht', 'fassade', 'schildtag', 'flur']),
    ('Mai 2023', 'Mai', '2023', 'Das erste Pop-up mit Momo.', ['pop23', 'ws12', 'd3', 'schaum', 'g1']),
    ('Herbst 2023', 'Herbst', '2023', 'Die ersten Abende unter dem Namen Culinarium, „by Momo x Christoph“.',
     ['pl23', 'p_CyT32RTMB4d', 'p_CzMcqNcMCqG', 'karte', 'kartglas']),
    ('November 2023', 'November', '2023', 'Reopening der Bar unter Derya Ivkin. Mixology ohne Karte.',
     ['ws00', 'ws01', 'barneg', 'flaschen', 'kanister', 'ws29']),
    ('2024', '', '2024', 'Rudi kommt in die Küche von Culinarium, „by Momo x Rudi“.', ['kueche', 'pass2', 'pass3', 'w7', 'pass', 'm2']),
    ('2026', 'September', '2026', 'Der September-Abend ist ausgebucht, Dirty Chicken feiert Opening.',
     ['kerze1', 'kerze2', 'p_DbYnkdkjrNy', 'dc_zeichen', 't01', 'anstossen']),
]
POS = {'pop23': '22% 40%', 'kueche': '50% 40%', 'kerze1': '50% 40%', 'kerze2': '50% 45%', 'ecke': '50% 40%', 'schildtag': '50% 30%',
       'pass2': '50% 30%', 'pl23': '50% 60%', 'p_CyT32RTMB4d': '50% 70%', 'p_CzMcqNcMCqG': '50% 70%', 'p_DbYnkdkjrNy': '50% 70%',
       'flur': '50% 55%', 'ws01': '50% 40%', 'anstossen': '50% 40%', 't01': '50% 40%'}
SATZ = 'Von der Bar in einer alten Fußballkneipe bis zum ausgebuchten Abend an der langen Tafel.'
GROESSEN = {}


def bild(b, w=1000, alt=None):
    if not GROESSEN:
        for f in os.listdir(os.path.join(HIER, 'assets', 'bild')):
            m = re.match(r'(.+)-(\d+)\.webp$', f)
            if m:
                GROESSEN.setdefault(m.group(1), set()).add(int(m.group(2)))
    w = max([g for g in GROESSEN.get(b, {640}) if g <= w] or [640])
    alt = bau.BILD[b][2] if alt is None and b in bau.BILD else (alt or '')
    return '<img src="assets/bild/%s-%d.webp?v=%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        b, w, VERSION, E(alt), POS.get(b, '50% 50%'))


def fig(b, cls='', w=1000, extra=''):
    if b.startswith('p_') or b in ('pl23', 'pop23'):
        cls = (cls + ' k2-plakat' + (' dunkel' if b == 'pop23' else '')).strip()  # Plakate ganz zeigen, nie die Schrift anschneiden
    return '<figure%s%s>%s</figure>' % (' class="%s"' % cls if cls else '', extra, bild(b, w))


def kopf(cls='mitte', satz=SATZ):
    """Überschrift wie heute: rollt aus dem Schlitz."""
    return '<div class="vk %s">%s%s</div>' % (cls, bau.zl(['Wie es kam.'], 'h2', 'titel'), bau.sw(E(satz), 'p', 'vtext', 1) if satz else '')


def text(i, cls='k2-tx'):
    """Datum mit Kerzenlinie und Satz, wie unter den Karten heute."""
    return '<div class="%s"><h3 class="k2-datum">%s</h3><p class="k2-satz">%s</p></div>' % (cls, E(S[i][0]), E(S[i][3]))


F = []  # (Name, Ton, Inhalt)

# 1 Drei Bilder je Moment: dasselbe Raster wie heute, aber jeder Moment ist eine kleine Bildwand aus drei Fotos mit Fuge
F.append(('Drei Bilder je Moment', 'hell', '<div class="k2-01">%s<div class="k2-01-raster">%s</div></div>' % (kopf(), ''.join(
    '<article class="k2-01-m auf" style="--i:%d"><div class="k2-wand k2-01-w">%s%s%s</div>%s</article>' % (
        i, fig(s[4][0], 'a'), fig(s[4][1], 'b', 640), fig(s[4][2], 'c', 640), text(i)) for i, s in enumerate(S)))))

# 2 Eine Wand, sechs Spalten: eine geschlossene Wand über die volle Breite, jede Spalte ein Moment mit zwei Fotos;
#   die Spalten steigen versetzt in den Rahmen, darunter die sechs Daten genau unter ihrer Spalte
F.append(('Eine Wand, sechs Spalten', 'hell', '<div class="k2-02">%s<div class="k2-wand k2-02-w auf k2-ohne">%s</div><div class="k2-02-texte">%s</div></div>' % (
    kopf(), ''.join('<div class="k2-02-s" style="--i:%d">%s%s</div>' % (i, fig(s[4][0]), fig(s[4][1], w=640)) for i, s in enumerate(S)),
    ''.join(text(i) for i in range(6)))))

# 3 Im Wechsel: je Moment eine Zeile, links ein grosses Foto, ein zweites greift über die Kante; die Jahreszahl gross daneben;
#   die Seiten wechseln, das kleine Foto wandert beim Scrollen langsamer
WECHSEL = {2: ['kartglas', 'pl23']}  # das Plakat ins kleine Feld, gross ein Foto vom Abend
F.append(('Im Wechsel', 'hell', '<div class="k2-03">%s%s</div>' % (kopf(), ''.join(
    '<article class="k2-03-z%s"><div class="k2-03-bilder">%s%s</div><div class="k2-03-text"><p class="k2-mono">%s</p><h3 class="k2-jahr">%s</h3><p class="k2-satz gross">%s</p></div></article>' % (
        ' rechts' if i % 2 else '', fig(WECHSEL.get(i, s[4])[0], 'k2-03-gross auf', 1600), fig(WECHSEL.get(i, s[4])[1], 'k2-03-klein', 640, ' data-k2-p'),
        E(s[1]) or '&#160;', s[2], E(s[3])) for i, s in enumerate(S)))))

# 4 Drei Stränge: die Geschichte nach den drei Fäden des Hauses, Die Bar, Die Abende, Die Tafel; je Strang eine Bildwand aus fünf Fotos
STR = [('Die Bar.', [0, 3], ['schildnacht', 'ecke', 'ws00', 'ws01', 'barneg']),
       ('Die Abende.', [1, 2], ['ws12', 'pop23', 'pl23', 'karte', 'p_CyT32RTMB4d']),
       ('Die Tafel.', [4, 5], ['kueche', 'pass3', 'kerze1', 'kerze2', 'dc_zeichen'])]
F.append(('Drei Stränge', 'hell', '<div class="k2-04">%s%s</div>' % (kopf(), ''.join(
    '<div class="k2-04-strang%s"><div class="k2-04-l"><h3 class="k2-04-name">%s</h3>%s</div><div class="k2-wand k2-04-w auf">%s</div></div>' % (
        ' rechts' if n % 2 else '', E(name), ''.join(text(i) for i in ids),
        fig(b[0], 'a', 1600) + ''.join(fig(x, w=640) for x in b[1:])) for n, (name, ids, b) in enumerate(STR)))))

# 5 Gegenläufig: zwei Bildreihen über die volle Breite, oben die Bar, unten die Abende; beim Scrollen laufen sie gegeneinander
OBEN = ['schildnacht', 'ecke', 'barnacht', 'pop23', 'ws12', 'ws00', 'ws01', 'barneg', 'flaschen']
UNTEN = ['pl23', 'p_CyT32RTMB4d', 'karte', 'kueche', 'pass2', 'pass3', 'kerze1', 'kerze2', 'p_DbYnkdkjrNy']
F.append(('Gegenläufig', 'hell', '<div class="k2-05" data-k2-p><div class="k2-innen">%s</div>%s%s<div class="k2-innen"><div class="k2-05-texte">%s</div></div></div>' % (
    kopf(), '<div class="k2-05-reihe o"><div class="k2-05-bahn">%s</div></div>' % ''.join(fig(b, w=640) for b in OBEN),
    '<div class="k2-05-reihe u"><div class="k2-05-bahn">%s</div></div>' % ''.join(fig(b, w=640) for b in UNTEN),
    ''.join(text(i) for i in range(6)))))

# 6 Leporello: sechs Blätter, aneinander gefaltet wie ein Faltblatt; beim Hinscrollen faltet es sich flach auf
F.append(('Leporello', 'hell', '<div class="k2-06">%s<div class="k2-06-falz" data-k2-p>%s</div></div>' % (kopf(), ''.join(
    '<article class="k2-06-blatt" style="--i:%d">%s%s</article>' % (i, fig(s[4][0]), text(i)) for i, s in enumerate(S)))))

# 7 Mosaik nach Gewicht: die Grösse sagt, wie viel ein Moment wiegt; der Anfang hoch, der ausgebuchte Abend über drei Felder;
#   die Fotos ziehen beim Hereinkommen in ihren Rahmen
def kachel(i, platz, bilder, cls=''):
    inhalt = fig(bilder[0], 'k2-07-b', 1600) if len(bilder) == 1 else '<div class="k2-wand k2-07-mehr">%s</div>' % ''.join(
        fig(b, 'k2-07-b', 1000) for b in bilder)
    return '<article class="k2-07-k auf%s" style="%s">%s%s</article>' % (cls, platz, inhalt, text(i))


F.append(('Mosaik nach Gewicht', 'hell', '<div class="k2-07">%s<div class="k2-07-raster">%s</div></div>' % (kopf(), ''.join([
    kachel(0, 'grid-column:1/3;grid-row:1/3;--i:0', ['schildnacht'], ' hoch'),
    kachel(1, 'grid-column:3;grid-row:1;--i:1', ['pop23']),
    kachel(2, 'grid-column:4;grid-row:1;--i:2', ['pl23']),
    kachel(3, 'grid-column:3/5;grid-row:2;--i:3', ['ws00', 'ws01']),
    kachel(4, 'grid-column:1;grid-row:3;--i:4', ['kueche']),
    kachel(5, 'grid-column:2/5;grid-row:3;--i:5', ['kerze1', 'kerze2', 'dc_zeichen'], ' breit')]))))

# 8 Grosse Daten, Bildstreifen: je Moment eine Zeile, die Jahreszahl riesig links, rechts ein Streifen aus vier Fotos,
#   der beim Scrollen ein Stück weiterzieht
F.append(('Grosse Daten, Bildstreifen', 'hell', '<div class="k2-08">%s%s</div>' % (kopf(), ''.join(
    '<article class="k2-08-z"><div class="k2-08-l"><p class="k2-mono">%s</p><h3 class="k2-jahr">%s</h3><p class="k2-satz">%s</p></div>'
    '<div class="k2-08-r" data-k2-p><div class="k2-wand k2-08-w">%s</div></div></article>' % (
        E(s[1]) or '&#160;', s[2], E(s[3]), ''.join(fig(b, w=640) for b in s[4][:4])) for s in S))))

# 9 Drei Spalten, drei Tempi: je Spalte zwei Momente, Bilder in verschiedenen Formaten; die Spalten laufen beim Scrollen verschieden schnell
SP = [[0, 3], [1, 4], [2, 5]]
FORM = {0: '4/5', 1: '1/1', 2: '1/1', 3: '4/5', 4: '3/4', 5: '4/5'}
ZWISCHEN = {0: 'fassade', 1: 'd3', 2: 'kartglas', 3: 'kanister', 4: 'w7', 5: 't01'}
F.append(('Drei Spalten, drei Tempi', 'hell', '<div class="k2-09" data-k2-p>%s<div class="k2-09-spalten">%s</div></div>' % (kopf(), ''.join(
    '<div class="k2-09-sp" style="--t:%d">%s</div>' % (n, ''.join(
        '<article class="k2-09-m"><div class="k2-wand k2-09-w" style="aspect-ratio:%s">%s%s</div>%s</article>' % (
            FORM[i], fig(S[i][4][0], 'a'), fig(ZWISCHEN[i], 'b', 640), text(i)) for i in ids)) for n, ids in enumerate(SP)))))

# 10 Von heute aus: zuerst der ausgebuchte Abend gross, dann zurück bis zur Bar von 2017, fünf Momente in einer Reihe
F.append(('Von heute aus', 'hell', '<div class="k2-10">%s<div class="k2-10-heute"><div class="k2-wand k2-10-w auf">%s</div>'
          '<div class="k2-10-t"><p class="k2-mono">%s</p><h3 class="k2-jahr">%s</h3><p class="k2-satz gross">%s</p></div></div>'
          '<p class="k2-10-zurueck k2-mono">Und so fing es an</p><div class="k2-10-reihe staffel auf">%s</div></div>' % (
              kopf(), fig('kerze1', 'a', 1600) + fig('kerze2', w=640) + fig('p_DbYnkdkjrNy', w=640) + fig('anstossen', w=640) + fig('dc_zeichen', w=640),
              E(S[5][1]), S[5][2], E(S[5][3]),
              ''.join('<article class="k2-10-m" style="--i:%d">%s%s</article>' % (n, fig(S[i][4][0]), text(i)) for n, i in enumerate([4, 3, 2, 1, 0])))))


def pruefen():
    """Jedes Foto nur einmal je Fassung und nie eins, das sonst auf der Seite steht."""
    seite = open(os.path.join(HIER, 'leute.html')).read()
    i = seite.find('v-lt-chronik'); a = seite.rfind('<section', 0, i); b = seite.find('</section>', i)
    aussen = set(re.findall(r'assets/bild/([A-Za-z0-9_\-]+?)-\d+\.webp', seite[:a] + seite[b:]))
    for n, (name, _t, inner) in enumerate(F, 1):
        k = re.findall(r'assets/bild/([A-Za-z0-9_\-]+?)-\d+\.webp', inner)
        doppelt = {x for x in k if k.count(x) > 1}
        assert not doppelt, 'Fassung %d %s: doppelt %s' % (n, name, doppelt)
        assert not (set(k) & aussen), 'Fassung %d %s: steht schon auf der Seite %s' % (n, name, set(k) & aussen)


def main():
    pruefen()
    seite = open(os.path.join(HIER, 'leute.html')).read()
    m = re.search(r'(<section class="vab bar-ab v-lt-chronik[^"]*"[^>]*>)(<div class="vi h-ablauf">.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Wie es kam» in leute.html nicht gefunden'
    kopf_tag = m.group(1).replace('class="vab', 'id="kam" data-name="Wie es kam" class="vab wahl', 1)
    teile = ['<div class="wv" data-n="0" data-ton="hell">%s</div>' % m.group(2)]
    teile += ['<div class="wv k2 k2-f%02d" data-n="%d" data-ton="%s" hidden><div class="vi">%s</div></div>' % (i, i, ton, inner) for i, (_n, ton, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Wie es kam</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: sechs Bildkarten im Raster'] + [n for n, _t, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('kam-wahl-2.css', 'kam-wahl-2.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["kam"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/kam-wahl-2.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Wie es kam wählen (Runde 2) · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/kam-wahl-2.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'kam-wahl-2.html'), 'w').write(seite)
    print('Seite kam-wahl-2.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
