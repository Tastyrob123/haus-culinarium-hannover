#!/usr/bin/env python3
"""Culinarium Hannover · 15 neue Auftakte, 26.10.2026.
Robert: «15 Variationsmöglichkeiten für richtig geilen Hero» (heute steht Fassung 4 «Anstossen»).
Baut auftakt-wahl.html: die echte Startseite, oben die 15 Auftakte zum Durchklicken (Pfeile unten, Pfeiltasten, ?f=Nummer).
Jede Fassung hat ein eigenes Gerüst und genau einen eigenen bewegten Moment; nur transform und opacity, nativer Scroll.
Aufruf: python3 website/bau.py && python3 website/auftakt_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, knopf, marke, BILD, VERSION, AUFTAKT_TEXT

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json')))


def b(k, cls='', sizes='50vw', pos=None, i=None):
    """Foto ohne den Auftritt der Seite: jede Fassung bewegt ihre Bilder selbst. Abbild als Grund, geladen beim Zeigen."""
    m = META[k]
    q, p, alt = BILD[k]
    srcset = ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (k, w, VERSION, w) for w in m['stufen'])
    return ('<figure class="vb %s" style="--lq:url(%s)%s"><img data-srcset="%s" data-sizes="%s" alt="%s" decoding="async" style="object-position:%s"></figure>'
            % (cls, m['lq'], '' if i is None else ';--i:%d' % i, srcset, sizes, E(alt), pos or p))


def lockup(cls=''):
    """Wortmarke und Zeile «A UNiQUE EXPERiENCE BY MOMO X RUDI», zeilenweise aus dem Schlitz."""
    return ('<div class="at-marke zl auf %s"><div class="at-wm"><span class="z"><span style="--i:0">%s</span></span></div>'
            '<div class="at-zeile"><span class="z"><span style="--i:1">%s</span></span></div></div>' % (cls, marke('wm'), marke('zeile')))


def text(cls='', satz=AUFTAKT_TEXT):
    return ('<div class="vx-text %s"><p class="vx-satz sw auf" style="--i:2">%s</p><div class="sw auf" style="--i:3">%s</div></div>'
            % (cls, satz, knopf('Zum nächsten Abend', '#bisbald')))


def rz(z):
    return E(z).replace(' / ', '&#160;<i>/</i> ')


def wm_pfad():
    s = open(os.path.join(HIER, 'assets', 'zeichen', 'marke.svg')).read()
    m = re.search(r'<symbol id="wm"[^>]*><path transform="([^"]+)"[^>]*d="([^"]+)"', s)
    return m.group(1), m.group(2)


# ------------------------------------------------------------------ die 15 Fassungen
F = []   # (Name, Hinweis zum Ausprobieren, Klasse, Inhalt)

# 1 Durchs Wort: die Fläche ist zu, nur durch die Buchstaben sieht man den Abend; Scrollen fährt durch das I in den Raum
tr, d = wm_pfad()
F.append(('Durchs Wort', 'scrollen', 'v-wort', '''<div class="vw-buehne">%s
<svg class="vw-deckel" viewBox="0 0 4650 564" aria-hidden="true"><path transform="%s" fill="#16151A" fill-rule="evenodd" d="M-600000 6005640H646500V-600000H-600000Z %s"/></svg>
<div class="vw-zeile zl auf"><span class="z"><span style="--i:1">%s</span></span></div>%s</div>''' % (
    b('anstossen', 'vw-foto', '100vw', '50% 42%'), tr, ' '.join(d.split()), marke('zeile'), text())))

# 2 Fünf Gläser: «5 von Momos Signature Drinks», abgestellt von links auf die Tresenkante
F.append(('Fünf Gläser', 'ansehen', 'v-glaeser', '''%s<div class="vg-reihe">%s</div><div class="vg-kante"></div>
<div class="vg-fuss"><p class="vg-zahl sw auf" style="--i:1">5 Drinks · 3 Gänge · 14 Plätze</p>%s</div>''' % (
    lockup(), ''.join(b(k, '', '(max-width:860px) 40vw, 20vw', i=i) for i, k in enumerate(('g1', 'd3', 'g4', 'g3', 'g5'))), text())))

# 3 Was zum Abend gehört: vier Zeilen erklären das Culinarium, Zeigen tauscht das Bild an derselben Stelle
LISTE = [('Fünf Drinks', 'von Momo', 'g1'), ('Drei Gänge', 'aus der Küche', 'lauch'), ('Eine Tafel', 'auf der Empore', 'tafelleer'), ('Vierzehn Plätze', 'pro Abend', 't03')]
F.append(('Was zum Abend gehört', 'Zeilen zeigen', 'v-liste', '''<div class="vl-links">%s<ul class="vl-zeilen">%s</ul>%s</div>
<div class="vl-bild">%s</div>''' % (
    lockup(), ''.join('<li class="sw auf%s" style="--i:%d" data-n="%d"><b>%s</b><span>%s</span></li>' % (' an' if i == 0 else '', i + 1, i, t, u) for i, (t, u, _k) in enumerate(LISTE)),
    text('statisch', 'Food-Pairing-Abende im Walk on the Wild Side in Linden, an einzelnen Wochenenden im Jahr.'),
    ''.join(b(k, 'an' if i == 0 else '', '(max-width:860px) 100vw, 54vw') for i, (_t, _u, k) in enumerate(LISTE)))))

# 4 Das Plakat: jeder Abend hat sein Plakat, also ist der Auftakt das Plakat des nächsten Abends
F.append(('Das Plakat', 'ansehen', 'v-plakat hell', '''<div class="vp-blatt">
<div class="vp-kopf"><span>Walk on the Wild Side</span><span>Haasemannstraße 13 · Linden</span></div>
%s
<div class="vp-mitte"><div class="vp-spalte"><p class="vp-gross sw auf" style="--i:2">Ein Menü, fünf passende Drinks, eine lange Tafel.</p>%s</div>
%s
<dl class="vp-daten sw auf" style="--i:3"><div><dt>Nächster Abend</dt><dd>Termin folgt</dd></div><div><dt>Plätze</dt><dd>14</dd></div><div><dt>Beginn</dt><dd>Fr 19:00 · Sa 17:00</dd></div><div><dt>Zuletzt</dt><dd>25. + 26.09.2026, ausgebucht</dd></div></dl></div></div>''' % (
    lockup(), '<div class="sw auf" style="--i:3">' + knopf('Auf die Warteliste', 'abend.html#warteliste', 'hell') + '</div>', b('glas', 'vp-bild', '(max-width:860px) 70vw, 30vw', '50% 40%'))))

# 5 Kerzenlicht: der Raum liegt im Dunkeln, die Maus trägt die Kerze
F.append(('Kerzenlicht', 'Maus bewegen', 'v-licht', '''%s<div class="vk-licht"><div class="vk-innen">%s</div></div>%s%s''' % (
    b('kerze1', 'vk-dunkel', '100vw', '50% 55%'), b('kerze1', 'vk-hell', '100vw', '50% 55%'), lockup('mitte'), text())))

# 6 Die lange Tafel: acht Abende als ein Band, das langsam am Tisch entlang treibt
TAFEL = ['t01', 't04', 't09', 't02', 't12', 't05', 't08', 't13']
band = ''.join(b(k, '', '(max-width:860px) 46vw, 22vw') for k in TAFEL)
F.append(('Die lange Tafel', 'ansehen', 'v-tafel', '''<div class="vt-oben">%s<p class="vt-zahl sw auf" style="--i:2"><b>14</b>Plätze an einem Tisch</p></div>
<div class="vt-band"><div class="vt-lauf">%s%s</div></div>%s''' % (lockup(), band, band.replace('<img ', '<img aria-hidden="true" '), text('unten'))))

# 7 Das x: Glas x Teller, wie das x auf den Plakaten, die Naht schräg durchs Bild
F.append(('Das x', 'ansehen', 'v-x', '''<div class="vx-l">%s</div><div class="vx-r">%s</div><svg class="vx-naht" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><line x1="62" y1="0" x2="40" y2="100"/></svg>
<span class="vx-kreuz" aria-hidden="true">×</span><p class="vx-eck vx-eck1">Fünf Drinks<br>von Momo</p><p class="vx-eck vx-eck2">Drei Gänge<br>von Rudi</p>%s%s''' % (
    b('g4', '', '60vw', '50% 45%'), b('r09', '', '60vw', '50% 50%'), lockup('oben'), text())))

# 8 Ebenen: Name zwischen den Bildern, die Ebenen folgen der Maus mit eigener Tiefe
F.append(('Ebenen', 'Maus bewegen', 'v-ebenen', '''<div class="ve-e" data-t="-.4">%s%s</div>%s<div class="ve-e" data-t="1">%s%s</div>%s''' % (
    b('tafelleer', 've-a', '40vw', '50% 40%'), b('theke', 've-b', '36vw', '50% 35%'), lockup('mitte'),
    b('g1', 've-c', '20vw'), b('roq1', 've-d', '22vw'), text())))

# 9 Der Stapel: Abzüge vom Abend landen auf dem Tisch, Antippen legt den nächsten oben drauf
STAPEL = ['anstossen', 'lauch', 'glaeser', 'kerze2', 'spag', 't12']
F.append(('Der Stapel', 'Stapel antippen', 'v-stapel', '''<div class="vs-links">%s%s</div>
<button class="vs-stapel" type="button" aria-label="Nächstes Foto">%s</button>''' % (
    lockup(), text('statisch'), ''.join(b(k, '', '(max-width:860px) 70vw, 30vw', i=i) for i, k in enumerate(STAPEL)))))

# 10 Laufband: die Wörter des Abends laufen gegenläufig hinter dem Glas
REIHEN = ['FATWASHING / MILKWASHING / ENZYME / ', 'LAUCH / BLUMENKOHL / CHIPOTLE / ', 'HOKKAIDO / KÜRBISKERNÖL / HASELNUSS / ']
F.append(('Laufband', 'ansehen', 'v-band', '''<div class="vb-feld"><div class="vb-reihen" aria-hidden="true">%s</div>%s%s</div>
<div class="vb-fuss">%s</div>''' % (
    ''.join('<div class="vb-reihe r%d"><span>%s</span><span>%s</span></div>' % (i, rz(r) * 2, rz(r) * 2) for i, r in enumerate(REIHEN)),
    b('anstossen', 'vb-bild', '(max-width:860px) 70vw, 30vw', '50% 40%'), lockup(), text())))

# 11 Draussen / Drinnen: draussen Linden bei Tag, drinnen Kerzen; die Naht lässt sich ziehen
F.append(('Draussen, drinnen', 'Naht ziehen', 'v-tuer', '''%s<div class="vd-drinnen"><div class="vd-innen">%s</div></div>
<div class="vd-griff" aria-hidden="true"><span></span></div>
<p class="vd-wort vd-w1">Drinnen</p><p class="vd-wort vd-w2">Draussen</p>%s%s''' % (
    b('ecke', 'vd-draussen', '100vw', '50% 40%'), b('kerze3', '', '100vw', '50% 50%'), lockup('mitte'), text())))

# 12 Ein Satz: der Satz erklärt den Abend, die Bilder stehen mitten in den Zeilen
def ib(k, pos='50% 50%'):
    return '<span class="vi-b">%s</span>' % b(k, '', '14vw', pos).replace('<figure', '<span').replace('</figure>', '</span>')
ZEILEN12 = ['Fünf Drinks %s' % ib('g4'), 'zu drei Gängen %s' % ib('lauch'), 'an einer Tafel %s' % ib('tafelleer', '50% 60%'), 'für vierzehn %s Gäste.' % ib('t12', '50% 35%')]
F.append(('Ein Satz', 'ansehen', 'v-satz hell', '''<div class="vi-kopf zl auf"><span class="z"><span style="--i:0">%s</span></span></div>
<h1 class="vi-gross zl auf">%s</h1><div class="vi-fuss"><p class="sw auf" style="--i:5">Culinarium: Food-Pairing-Abende im Walk on the Wild Side, Hannover-Linden.</p><div class="sw auf" style="--i:6">%s</div></div>''' % (
    marke('wm'), ''.join('<span class="z"><span style="--i:%d">%s</span></span>' % (i + 1, z) for i, z in enumerate(ZEILEN12)), knopf('Zum nächsten Abend', '#bisbald', 'hell'))))

# 13 Die Karte: die Menükarte liegt auf dem Tisch, mit Rudis Zeilen im Wortlaut der Beiträge
F.append(('Die Karte', 'ansehen', 'v-karte', '''%s<div class="vc-hof"></div>
<div class="vc-links"><h1 class="vc-titel zl auf"><span class="z"><span style="--i:0">Dein Platz</span></span><span class="z"><span style="--i:1">an der Tafel.</span></span></h1>%s</div>
<div class="vc-karte"><div class="vc-wm">%s</div><div class="vc-zeile">%s</div><p class="vc-klein">Aus Rudis Karten</p>
<ul>%s</ul><p class="vc-klein">Dazu fünf Drinks von Momo</p><p class="vc-fuss"><span>14 Plätze</span><span>Linden</span></p></div>''' % (
    b('tafelleer', 'vc-foto', '100vw', '50% 62%'), text('statisch'), marke('wm'), marke('zeile'),
    ''.join('<li>%s</li>' % rz(' '.join(z).replace('/ ', '/ ')) for z, _b, _i in bau.ZEILEN[:3]))))

# 14 Randlos: ein Bild, randlos; der Name steht kantenbündig unten, Scrollen zoomt zurück
F.append(('Randlos', 'scrollen', 'v-randlos', '''<div class="vr-rahmen">%s</div><div class="vr-hof"></div>
<div class="vr-oben">%s<div class="sw auf" style="--i:3">%s</div></div><div class="vr-name zl auf"><span class="z"><span style="--i:0">%s</span></span></div>''' % (
    b('t12', 'vr-foto', '100vw', '50% 40%'), '<p class="vx-satz sw auf" style="--i:2">%s</p>' % AUFTAKT_TEXT, knopf('Zum nächsten Abend', '#bisbald'), marke('wm'))))

# 15 Pairing: links steigen die Gläser, rechts sinken die Teller, in der Mitte das x
GL = ['g1', 'g3', 'd3', 'g5', 'glas', 'g4']
TE = ['r09', 'roq1', 'hok1', 'spag', 'r02', 'lauch']
def saeule(ks):
    s = ''.join(b(k, '', '(max-width:860px) 30vw, 22vw') for k in ks)
    return s + s.replace('<img ', '<img aria-hidden="true" ')
F.append(('Pairing', 'ansehen', 'v-pairing', '''<div class="vq-s vq-l"><div class="vq-lauf">%s</div></div><div class="vq-s vq-r"><div class="vq-lauf">%s</div></div>
<div class="vq-mitte">%s<p class="vq-x zl auf"><span class="z"><span style="--i:1">Glas <i>×</i> Teller</span></span></p>%s</div>''' % (
    saeule(GL), saeule(TE), lockup(), text('statisch'))))


def auftakte():
    out = ['<div class="fassung %s" data-nr="%d" data-name="%s"%s>%s</div>' % (cls, i, E(n), '' if i == 1 else ' hidden', inner)
           for i, (n, _h, cls, inner) in enumerate(F, 1)]
    return '<section class="auftakt vx" data-ton="nacht" id="auftakt" aria-label="Culinarium">%s</section>' % ''.join(out)


def main():
    seite = open(os.path.join(HIER, 'index.html')).read()
    seite, n = re.subn(r'<section class="auftakt".*?</section>', lambda _m: auftakte(), seite, count=1, flags=re.S)
    assert n == 1, 'Auftakt in index.html nicht gefunden (erst bau.py laufen lassen)'
    seite = re.sub(r'<div class="fassungen".*?</div>\s*', '', seite, flags=re.S)
    liste = json.dumps([[i, '%s <em>%s</em>' % (E(nm), E(h))] for i, (nm, h, _c, _x) in enumerate(F, 1)], ensure_ascii=False)
    leiste = ('<div class="fassungen" id="fassungen" data-liste="%s"><button class="fz-zurueck" type="button" aria-label="Vorige Fassung">‹</button>'
              '<span class="fz-name"></span><button class="fz-vor" type="button" aria-label="Nächste Fassung">›</button></div>') % E(liste)
    seite = seite.replace('<title>', '<title>Auftakt wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/auftakt-wahl.css?v=%s">\n</head>' % VERSION, 1)
    seite = seite.replace('</body>', '%s\n<script src="assets/auftakt-wahl.js?v=%s" defer></script>\n</body>' % (leiste, VERSION), 1)
    open(os.path.join(HIER, 'auftakt-wahl.html'), 'w').write(seite)
    print('Seite auftakt-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen')


if __name__ == '__main__':
    main()
