#!/usr/bin/env python3
"""Culinarium Hannover · Hero von «Das Haus» (bar.html) in 15 Fassungen, 27.10.2026.
Robert: «Gib mir 15 visuelle Alternative Darstellungsmöglichkeiten für diesen Hero.» Heute: drei Bilder nebeneinander, Titel darüber (Fassung 0).
Jede Fassung füllt den ersten Bildschirm, trägt die Bar (Nacht, Schild, Theke, Negroni, Konzerte, ohne Karte) und hat einen bewegten Moment,
nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut bar-kopf-wahl.html (Leiste unten, Pfeiltasten, ?kopf=Nummer).
Aufruf: python3 website/bau.py && python3 website/bar_kopf_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, zl, sw

HIER = bau.HIER
bau.META.update(bau.bilder())

TEXT = 'Der Gastgeber von Culinarium: eine Nachbarschafts-Mixology-Bar in Linden, Haasemannstraße 13. Drinks, Events, private Veranstaltungen und Tastings.'
INFO = 'Donnerstag 19 bis 1 Uhr · Freitag und Samstag 19 bis 2 Uhr'
WS = ['Walk on', 'the Wild Side.']


def bild(k, sizes='100vw', pos=None, cls=''):
    q, p, alt = bau.BILD[k]
    m = bau.META[k]
    return '<img%s src="assets/bild/%s-%d.webp?v=%s" srcset="%s" sizes="%s" alt="%s" decoding="async" style="object-position:%s">' % (
        ' class="%s"' % cls if cls else '', k, m['stufen'][0], VERSION, bau.srcset(k), sizes, E(alt), pos or p)


def gross_url(k):
    return 'assets/bild/%s-%d.webp?v=%s' % (k, bau.META[k]['stufen'][-1], VERSION)


def titel(cls='gross', zeilen=WS):
    return zl(zeilen, 'h1', cls)


def text(i=1):
    return sw(TEXT, i=i) + '<p class="bk-info sw auf" style="--i:%d">%s</p>' % (i + 1, INFO)


def held(nr, inner, extra=''):
    return '<div class="bk bk%02d"%s>%s</div>' % (nr, extra, inner)


F = []

# 1 Leuchtschrift: die Rückwand der Bar im Dunkeln, der Titel ist eine Neonröhre wie das Negroni darüber; sie flackert an
F.append(('Leuchtschrift', held(1, '<figure class="bk-bild bk01-bild">%s</figure>'
    '<div class="bk01-neon auf" aria-label="Walk on the Wild Side."><h1 class="bk01-aus" aria-hidden="true">Walk on<br>the Wild Side.</h1><p class="bk01-an" aria-hidden="true">Walk on<br>the Wild Side.</p></div>'
    '<div class="bk-text unten-mitte">%s</div>' % (bild('barneg', pos='50% 40%'), text()))))

# 2 Der Ausleger: die Fenster der Bar bei Nacht, davor hängt das Schild am Arm und pendelt aus
F.append(('Der Ausleger', held(2, '<figure class="bk-bild">%s</figure><div class="bk-grund links"></div>'
    '<div class="bk02-arm" aria-hidden="true"></div><div class="bk02-schild auf"><span class="bk02-ketten" aria-hidden="true"></span>%s</div>'
    '<div class="bk-text links-unten">%s</div>' % (bild('barnacht', pos='50% 50%'), titel('bk02-titel'), text()))))

# 3 Tag und Nacht: die Hausecke mit den Schildern am Tag; beim Scrollen wird es Nacht und die Schilder leuchten
F.append(('Tag und Nacht', held(3, '<figure class="bk-bild">%s</figure><figure class="bk-bild bk03-nacht" data-zieh="nacht">%s</figure>'
    '<div class="bk-grund unten"></div><p class="bk03-uhr" aria-hidden="true"><span class="t">Linden, am Tag</span><span class="n" data-zieh="nachtwort">ab 19 Uhr</span></p>'
    '<div class="bk-text unten-links">%s%s</div>' % (bild('schildtag', pos='50% 38%'), bild('schildnacht', pos='50% 45%'), titel(), text()))))

# 4 Durchs Fenster: von der Strasse auf die beleuchteten Fenster; beim Scrollen geht man hinein und steht an der Theke
F.append(('Durchs Fenster', held(4, '<figure class="bk-bild bk04-innen" data-zieh="innen">%s</figure><figure class="bk-bild bk04-aussen" data-zieh="fenster">%s</figure>'
    '<div class="bk-grund links"></div><div class="bk-text links">%s%s</div>' % (bild('theke', pos='50% 35%'), bild('fassade', pos='50% 50%'), titel(), text()))))

# 5 Wortband: hinter dem Titel laufen die Abende der Bar in Zeilen gegenläufig durchs Bild, davor steht der Name
BAND = [['Mixology ohne Karte', 'Konzerte am Donnerstag', 'SESSION Sip & Sounds'],
        ['Gastschichten', 'Tastings', 'Private Feiern', 'Haasemannstraße 13'],
        ['Negroni', 'Anniversary Night', 'Silvester-Frühshoppen', 'DJs an den Decks']]
F.append(('Wortband', held(5, '<figure class="bk-bild bk05-bild">%s</figure><div class="bk05-baender" aria-hidden="true">%s</div>'
    '<div class="bk-text mitte">%s%s</div>' % (bild('momo', pos='50% 35%'), ''.join(
        '<div class="bk05-z%s"><span>%s</span><span>%s</span></div>' % (' rueck' if i % 2 else '', ' · '.join(z * 2) + ' · ', ' · '.join(z * 2) + ' · ')
        for i, z in enumerate(BAND)), titel(), text()))))

# 6 Bühne: wie ein Konzertplakat, links die Schrift, rechts der Abend auf der kleinen Bühne in voller Höhe
F.append(('Bühne', held(6, '<div class="bk06-plakat"><p class="bk06-tag auf">Donnerstag · Konzert · ab 19 Uhr</p>%s%s</div>'
    '<figure class="bk06-bild bk-setzt auf">%s</figure>' % (titel(), text(), bild('ws14', '(max-width:860px) 100vw, 50vw', pos='45% 50%')))))

# 7 Abzüge: Fotos aus der Bar liegen wie Abzüge auf dem dunklen Tresen und landen nacheinander, der Name in der Mitte
ABZ = [('ws03', '-7deg', '6%', '14%'), ('ws12', '5deg', '74%', '12%'), ('ws15', '-4deg', '2%', '56%'), ('ws35', '8deg', '80%', '58%'),
       ('ws00', '3deg', '22%', '8%'), ('lachen', '-6deg', '60%', '64%'), ('ws07', '-3deg', '57%', '6%'), ('d3', '6deg', '24%', '62%')]
F.append(('Abzüge', held(7, '<div class="bk07-tisch auf">%s</div><div class="bk-text mitte schmal">%s%s</div>' % (
    ''.join('<figure class="bk07-a" style="--r:%s;left:%s;top:%s;--i:%d">%s</figure>' % (r, x, y, i, bild(k, '240px')) for i, (k, r, x, y) in enumerate(ABZ)),
    titel(), text()))))

# 8 Name voller Bar: «Wild Side» riesig, in den Buchstaben die Rückwand der Bar; beim Scrollen kommt der Name näher
F.append(('Name voller Bar', held(8, '<p class="bk08-klein zl auf" aria-hidden="true"><span class="z"><span>Walk on the</span></span></p>'
    '<p class="bk08-wort" data-zieh="wort" aria-hidden="true" style="background-image:url(%s)">Wild<br>Side.</p><h1 class="vh">Walk on the Wild Side.</h1>'
    '<div class="bk-text rechts-unten">%s</div>' % (gross_url('theke'), text()))))

# 9 Mosaik: Theke, Schild, Gläser, Konzert, Gäste dicht in ungleichen Grössen; der Name hat sein eigenes Feld, nicht im Bild
MOS = [('barneg', 'grid-column:1/3;grid-row:1/5', '50% 40%'), ('ws03', 'grid-column:3;grid-row:1/3', '50% 50%'), ('schildnah', 'grid-column:4;grid-row:1/2', '50% 45%'),
       ('ws14', 'grid-column:5/7;grid-row:1/3', '50% 50%'), ('kanister', 'grid-column:4;grid-row:2/3', '50% 50%'),
       ('lachen', 'grid-column:3;grid-row:3/5', '50% 35%'), ('ws12', 'grid-column:6;grid-row:3/5', '50% 40%')]
F.append(('Mosaik', held(9, '<div class="bk09-gitter">%s<div class="bk09-feld" style="grid-column:4/6;grid-row:3/5">%s%s</div></div>' % (
    ''.join('<figure class="bk09-k bk-setzt auf" style="%s;--i:%d">%s</figure>' % (g, i, bild(k, '(max-width:860px) 50vw, 34vw', pos=p)) for i, (k, g, p) in enumerate(MOS)),
    titel('mittel'), text()))))

# 10 Hinter der Theke: links der Name, rechts zwei Spalten mit den Leuten hinter der Theke, eine steigt, eine sinkt
SP1 = ['ws20', 'theke', 'ws11', 'bar', 'ws05']
SP2 = ['w3', 'ws10', 'momo', 'theke2', 'ws12']
F.append(('Hinter der Theke', held(10, '<div class="bk10-text">%s%s</div><div class="bk10-spalten" aria-hidden="true">%s</div>' % (
    titel(), text(), ''.join('<div class="bk10-s%s"><div class="bk10-zug">%s</div></div>' % (' rueck' if j else '', ''.join(
        '<figure>%s</figure>' % bild(k, '(max-width:860px) 50vw, 24vw') for k in sp * 2)) for j, sp in enumerate((SP1, SP2)))))))

# 11 Drei Seiten der Bar: unten drei Worte, Zeigen oder Tippen tauscht das grosse Bild an derselben Stelle
SEITEN = [('Ohne Karte', 'Du erzählst, was du magst, und bekommst deinen Drink.', 'momo', '50% 35%'),
          ('Konzerte', 'Donnerstags spielt jemand auf der kleinen Bühne.', 'ws14', '50% 45%'),
          ('SESSION', 'Sip & Sounds, DJs an den Decks bis eins.', 'barneg', '50% 45%')]
F.append(('Drei Seiten der Bar', held(11, '%s<div class="bk-grund unten stark"></div><div class="bk11-oben">%s%s</div><div class="bk11-wahl">%s</div>' % (
    ''.join('<figure class="bk-bild bk11-b%s" data-seite="%d">%s</figure>' % (' an' if i == 0 else '', i, bild(k, pos=p)) for i, (_w, _s, k, p) in enumerate(SEITEN)),
    titel(), text(), ''.join('<button type="button" data-seite="%d"%s><b>%s</b><span>%s</span></button>' % (i, ' class="an"' if i == 0 else '', w, s)
                             for i, (w, s, _k, _p) in enumerate(SEITEN))))))

# 12 Ohne Karte: zuerst der Satz der Bar auf der Nacht, darunter das Bild vom Abseihen, das beim Scrollen hochkommt
F.append(('Ohne Karte', held(12, '<div class="bk12-oben">%s<p class="bk12-satz zl auf" aria-label="Eine Karte gibt es hier nicht. Erzähl, was du magst.">'
    '<span class="z"><span style="--i:1">Eine Karte gibt es hier nicht.</span></span><span class="z"><span style="--i:2">Erzähl, was du magst.</span></span></p>%s</div>'
    '<figure class="bk12-bild" data-zieh="hoch">%s</figure>' % (titel('bk12-titel', ['Walk on the Wild Side.']), text(3), bild('d3', pos='50% 62%')))))

# 13 Das Türschild: links die Hausecke mit den Schildern in voller Höhe, rechts die Zeiten wie ein Schild an der Tür
F.append(('Das Türschild', held(13, '<figure class="bk13-bild" data-zieh="drift">%s</figure><div class="bk13-rechts">%s%s'
    '<div class="bk13-schild sw auf" style="--i:3"><p class="bk13-kopf">Geöffnet</p><dl><dt>Donnerstag</dt><dd>19 – 1 Uhr</dd><dt>Freitag</dt><dd>19 – 2 Uhr</dd><dt>Samstag</dt><dd>19 – 2 Uhr</dd></dl>'
    '<p class="bk13-fuss">Haasemannstraße 13 · Linden</p></div></div>' % (bild('schildtag', '(max-width:860px) 100vw, 55vw', pos='50% 40%'), titel(), sw(TEXT, i=1)))))

# 14 Den Tresen entlang: über dem Namen ein Band aus Bildern der Theke; beim Scrollen geht man den Tresen entlang
TRESEN = ['ws01', 'theke', 'kanister', 'barneg', 'bar', 'flaschen', 'theke2', 'ws13', 'ws00']
F.append(('Den Tresen entlang', held(14, '<div class="bk14-band" data-zieh="band" aria-hidden="true">%s</div><div class="bk14-unten">%s<div>%s</div></div>' % (
    ''.join('<figure>%s</figure>' % bild(k, '(max-width:860px) 50vw, 24vw') for k in TRESEN), titel(), text()))))

# 15 Mittelsäule: in der Mitte Momo beim Shaken in voller Höhe, der Name links und rechts daneben; das Bild steigt beim Scrollen
F.append(('Mittelsäule', held(15, '<p class="bk15-l zl auf" aria-hidden="true"><span class="z"><span>Walk on</span></span></p>'
    '<figure class="bk15-bild" data-zieh="saeule">%s</figure><p class="bk15-r zl auf" aria-hidden="true"><span class="z"><span style="--i:1">the Wild</span></span><span class="z"><span style="--i:2">Side.</span></span></p>'
    '<h1 class="vh">Walk on the Wild Side.</h1><div class="bk15-text">%s</div>' % (bild('momo', '(max-width:860px) 70vw, 34vw', pos='50% 30%'), text()))))


def main():
    seite = open(os.path.join(HIER, 'bar.html')).read()
    m = re.search(r'<section class="vab bar-ab v-bar-kopf[^"]*"[^>]*>(.*?)</section>', seite, re.S)
    assert m, 'Kopf in bar.html nicht gefunden (erst bau.py laufen lassen)'
    alt = re.search(r'<section ([^>]*)>', m.group(0)).group(1)
    teile = ['<div class="wv bk-heute" data-n="0"><section %s>%s</section></div>' % (alt, m.group(1))]
    teile += ['<div class="wv bkv" data-n="%d" hidden>%s</div>' % (i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = '<section class="bkw wahl" data-ton="strasse" id="kopf" data-name="Hero">' + '<div class="wahl-marke"><b>Hero</b><span data-nr></span></div>' + ''.join(teile) + '</section>'
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Mosaik mit Tafel (eingebaut)'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('bar-kopf-wahl.css', 'bar-kopf-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["kopf"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/bar-kopf-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Hero «Das Haus» wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/bar-kopf-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'bar-kopf-wahl.html'), 'w').write(seite)
    print('Seite bar-kopf-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
