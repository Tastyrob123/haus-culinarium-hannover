#!/usr/bin/env python3
"""Culinarium Hannover · «Seit 2023.» zweite Runde: 15 weitere Fassungen, direkt in der echten Startseite, 27.10.2026.
Robert: «gib nochmal 15». Keine der ersten Runde (chronik_wahl.py) wiederholt: Tafel, Gläser, Stapel, Buch, Story, Bilderwand, Anzeigetafel, Tickets, Teller, Vollbild, Abspann, zwei Linien.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut chronik-wahl-2.html (Leiste unten, Pfeiltasten, ?chronik=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/chronik_wahl2.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION
from chronik_wahl import M, ABENDE, KNOPF, bild, titel, plakat

HIER = bau.HIER
F = []  # (Name, Inhalt)
JAHRE = [('2023', 'Mai'), ('2023', 'Herbst'), ('2024', 'Frühjahr'), ('2025', 'Februar'), ('2026', 'September')]


def wo(m):
    return '%s %s' % (E(m[1]), m[0])


# 1 Die Tafel von oben: die lange Tafel, an fünf Plätzen steht je ein Teller mit einem Moment, die Tischkarte daneben erzählt ihn
F.append(('Die Tafel von oben', '<div class="cz-01">%s<div class="cz-01-tafel auf"><div class="cz-01-platte">%s</div></div><div class="sw auf cz-k">%s</div></div>' % (
    titel('mitte', 'Fünf Plätze an der langen Tafel, an jedem ein Stück Geschichte.'),
    ''.join('<div class="cz-01-platz %s" style="--x:%d;--i:%d"><figure class="cz-01-teller">%s</figure><div class="cz-01-karte"><p class="mono ch-w">%s</p><p>%s</p></div></div>' % (
        'oben' if i % 2 == 0 else 'unten', i, i, bild(m[3], 640), wo(m), E(m[2])) for i, m in enumerate(M)), KNOPF)))

# 2 Fünf Gläser auf dem Tresen: fünf von Momos Drinks nebeneinander abgestellt, unter jedem ein Bierdeckel mit dem Jahr; antippen erzählt
GLAS = ['g1', 'g3', 'g2', 'g4', 'g5']
F.append(('Fünf Gläser auf dem Tresen', '<div class="cz-02" data-ch>%s<div class="cz-02-tresen">%s</div><div class="cz-02-satz" aria-live="polite">%s</div><div class="sw auf cz-k">%s</div></div>' % (
    titel('mitte', 'Für jedes Jahr ein Glas. Einen Deckel antippen.'),
    ''.join('<button type="button" class="cz-02-g auf%s" data-q="%d" style="--i:%d"><figure>%s</figure><span class="cz-02-deckel"><b>%s</b><span>%s</span></span></button>' % (
        ' an' if i == 0 else '', i, i, bild(g, 640), m[0], E(m[1])) for i, (m, g) in enumerate(zip(M, GLAS))),
    ''.join('<p class="cz-02-a%s" data-a="%d"><span class="mono ch-w">%s</span>%s</p>' % (' an' if i == 0 else '', i, wo(m), E(m[2])) for i, m in enumerate(M)), KNOPF)))

# 3 Der Stapel beim Scrollen: jeder Moment eine grosse Karte, die oben stehen bleibt; die nächste schiebt sich darüber
F.append(('Der Stapel beim Scrollen', '<div class="cz-03">%s<div class="cz-03-stapel">%s</div><div class="sw auf cz-k">%s</div></div>' % (
    titel('mitte'),
    ''.join('<article class="cz-03-karte" style="--i:%d"><figure>%s</figure><div class="cz-03-text"><p class="cz-03-j">%s</p><p class="mono ch-w">%s</p><p class="cz-03-s">%s</p></div></article>' % (
        i, bild(m[3], 1600 if m[3] == 'kueche' else 1000), m[0], E(m[1]), E(m[2])) for i, m in enumerate(M)), KNOPF)))

# 4 In Zahlen: ein grosses Gruppenbild, daneben vier Zahlen, die alles sagen
ZAHLEN = [('1', 'Pop-up im Mai 2023, mit dem alles anfing'), ('14', 'Ausgaben Culinarium seit September 2023'),
          ('13', 'Plakate, jedes für seinen Abend gestaltet'), ('14', 'Plätze an einer Tafel, jedes Mal')]
F.append(('In Zahlen', '<div class="cz-04"><figure class="cz-04-bild auf">%s</figure><div class="cz-04-r">%s<div class="cz-04-zahlen">%s</div><div class="sw auf">%s</div></div></div>' % (
    bild('trio2', 1600), titel('links', 'Vier Jahre, in vier Zahlen.'),
    ''.join('<div class="cz-04-z"><p class="zl auf cz-04-n"><span class="z"><span style="--i:%d">%s</span></span></p><p class="cz-04-t">%s</p></div>' % (i, n, E(t)) for i, (n, t) in enumerate(ZAHLEN)), KNOPF)))

# 5 Das Buch zum Blättern: eine aufgeschlagene Doppelseite, links das Foto, rechts der Eintrag; die Seite blättert um
F.append(('Das Buch zum Blättern', '<div class="cz-05" data-cz-buch>%s<div class="cz-05-buch auf">%s<button type="button" class="cz-05-weiter" aria-label="Umblättern">Umblättern ›</button></div><div class="sw auf cz-k">%s</div></div>' % (
    titel('mitte', 'Das Gästebuch des Abends, eine Seite je Moment.'),
    ''.join('<div class="cz-05-seite%s" data-s="%d"><figure class="cz-05-l">%s</figure><div class="cz-05-r"><p class="cz-05-kopf mono">Culinarium · Seite %d</p><p class="cz-05-hand">%s</p><p class="cz-05-s">%s</p></div></div>' % (
        ' an' if i == 0 else '', i, bild(m[3], 1000), i + 1, wo(m), E(m[2])) for i, m in enumerate(M)), KNOPF)))

# 6 Wie eine Story: ein hohes Bild, oben fünf Striche, die sich füllen; es läuft von selbst, antippen geht weiter
F.append(('Wie eine Story', '<div class="cz-06"><div class="cz-06-l">%s<div class="sw auf">%s</div></div><div class="cz-06-story auf" data-cz-story>'
          '<div class="cz-06-striche">%s</div>%s<button type="button" class="cz-06-zur" aria-label="Zurück"></button><button type="button" class="cz-06-vor" aria-label="Weiter"></button></div></div>' % (
              titel('links', 'Vier Jahre in fünf Bildern, so wie Culinarium sie auf Instagram erzählt.'), KNOPF,
              ''.join('<span><i></i></span>' for _m in M),
              ''.join('<figure class="cz-06-f%s" data-s="%d">%s<figcaption><span class="mono">%s</span><p>%s</p></figcaption></figure>' % (
                  ' an' if i == 0 else '', i, bild(m[3], 1000), wo(m), E(m[2])) for i, m in enumerate(M)))))

# 7 Die Bilderwand im Flur: gerahmte Fotos in verschiedenen Grössen, eng gehängt; unter fünf davon ein Messingschild
WAND = [('pop23', 0, 0, 26, 34), ('t03', 28, 0, 18, 46), ('pl23', 48, 4, 22, 30), ('lachen', 72, 0, 28, 38),
        ('kueche', 0, 40, 22, 44), ('theke', 24, 52, 20, 36), ('t08', 48, 40, 24, 48), ('kerze1', 74, 44, 26, 44)]
SCHILD = {'pop23': 0, 'pl23': 1, 'kueche': 2, 't08': 3, 'kerze1': 4}
F.append(('Die Bilderwand im Flur', '<div class="cz-07"><div class="cz-07-l">%s<div class="sw auf">%s</div></div><div class="cz-07-wand">%s</div></div>' % (
    titel('links', 'Wie im Flur einer alten Wohnung: eng gehängt, jedes Bild mit Schild.'), KNOPF,
    ''.join('<figure class="cz-07-r auf" style="left:%d%%;top:%d%%;width:%d%%;height:%d%%;--i:%d"><div class="cz-07-f">%s</div>%s</figure>' % (
        x, y, w, h, n, bild(b, 640), '<figcaption><b>%s</b>%s</figcaption>' % (wo(M[SCHILD[b]]), E(M[SCHILD[b]][4])) if b in SCHILD else '')
        for n, (b, x, y, w, h) in enumerate(WAND)))))

# 8 Die Zahl hinter dem Bild: je Moment eine Reihe, die Jahreszahl riesig und hohl dahinter, das Foto davor; die Zahl wandert langsamer
F.append(('Die Zahl hinter dem Bild', '<div class="cz-08">%s%s<div class="sw auf cz-k">%s</div></div>' % (
    titel('mitte'),
    ''.join('<div class="cz-08-reihe %s"><p class="cz-08-zahl" data-cz-par aria-hidden="true">%s</p><figure class="cz-08-bild auf">%s</figure><div class="cz-08-t"><p class="mono ch-w">%s</p><p>%s</p></div></div>' % (
        'rechts' if i % 2 else 'links', m[0], bild(m[3], 1000), wo(m), E(m[2])) for i, m in enumerate(M)), KNOPF)))

# 9 Die Kreidetafel: an der Wand der Bar, wo sonst die Drinks stehen, steht die Geschichte; daneben ein Foto vom Tresen
F.append(('Die Kreidetafel', '<div class="cz-09"><div class="cz-09-tafel auf"><p class="cz-09-h">Seit 2023</p><p class="cz-09-u">heute an der Tafel</p>%s</div>'
          '<div class="cz-09-r"><figure class="cz-09-bild auf">%s</figure><p class="cz-09-satz">Aus einem Pop-up an der Bar sind ausgebuchte Abende geworden.</p><div class="sw auf">%s</div></div></div>' % (
              ''.join('<div class="cz-09-z"><span>%s</span><i></i><b>%s</b></div><p class="cz-09-s">%s</p>' % (wo(m), E(m[4]), E(m[2])) for m in M), bild('theke2', 1000), KNOPF)))


# 10 Die Anzeigetafel: wie am Bahnhof, Buchstaben auf Klappen; beim Hinscrollen klappen die Zeilen nacheinander um
def klappen(t, w, i):
    t = t.upper().ljust(w)[:w]
    return ''.join('<span style="--d:%d">%s</span>' % (i * 6 + n, E(c) if c != ' ' else '&nbsp;') for n, c in enumerate(t))


ANZ = [('MAI 23', 'POP-UP MOMO', 'WILD SIDE'), ('HERBST 23', 'CULINARIUM', 'MOMO X CHRISTOPH'), ('2024', 'RUDI KOCHT', 'MOMO X RUDI'),
       ('FEB 25', 'EINE TAFEL', '14 PLÄTZE'), ('SEPT 26', 'AUSGEBUCHT', 'BIS BALD')]
F.append(('Die Anzeigetafel', '<div class="cz-10">%s<div class="cz-10-tafel auf"><div class="cz-10-kopf mono"><span>Wann</span><span>Was</span><span>Mit</span></div>%s</div><p class="cz-10-unter">%s</p><div class="sw auf cz-k">%s</div></div>' % (
    titel('mitte', 'Abfahrt Haasemannstraße 13: wohin der Abend seit 2023 gefahren ist.'),
    ''.join('<div class="cz-10-z">%s</div>' % ''.join('<span class="cz-10-f">%s</span>' % klappen(t, w, i) for t, w in zip(z, (9, 11, 16))) for i, z in enumerate(ANZ)),
    'Haasemannstraße 13 · Hannover-Linden', KNOPF)))

# 11 Die Tickets in der Hand: fünf Eintrittskarten, aufgefächert wie Spielkarten; antippen zieht eine heraus und erzählt
F.append(('Die Tickets in der Hand', '<div class="cz-11" data-ch><div class="cz-11-l">%s<div class="cz-11-satz" aria-live="polite">%s</div><div class="sw auf">%s</div></div>'
          '<div class="cz-11-faecher auf">%s</div></div>' % (
              titel('links', 'Fünf Eintrittskarten, aufgefächert. Eine ziehen.'),
              ''.join('<p class="cz-11-a%s" data-a="%d"><span class="mono ch-w">%s</span>%s</p>' % (' an' if i == 4 else '', i, wo(m), E(m[2])) for i, m in enumerate(M)), KNOPF,
              ''.join('<button type="button" class="cz-11-t%s" data-q="%d" style="--w:%d"><figure>%s</figure><span class="cz-11-text"><span class="mono">Culinarium · Einlass</span><b>%s</b><span>%s</span></span></button>' % (
                  ' an' if i == 4 else '', i, i - 2, bild(m[3], 640), m[0], E(m[4])) for i, m in enumerate(M)))))

# 12 Der Teller als Uhr: in der Mitte ein Teller von Rudi, am Rand die fünf Momente wie Stunden; antippen dreht den Moment nach oben
F.append(('Der Teller als Uhr', '<div class="cz-12" data-ch data-cz-uhr><div class="cz-12-l">%s<div class="cz-12-mitte">%s</div><div class="sw auf">%s</div></div>'
          '<div class="cz-12-buehne auf"><div class="cz-12-rad">%s<figure class="cz-12-teller">%s</figure></div></div></div>' % (
              titel('links', 'Einen Moment am Rand antippen, der Teller dreht ihn nach oben.'),
              ''.join('<div class="cz-12-a%s" data-a="%d"><figure>%s</figure><p class="mono ch-w">%s</p><p class="cz-12-s">%s</p></div>' % (
                  ' an' if i == 0 else '', i, bild(m[3], 640), wo(m), E(m[2])) for i, m in enumerate(M)), KNOPF,
              ''.join('<button type="button" class="cz-12-q%s" data-q="%d" style="--w:%d"><span><b>%s</b>%s</span></button>' % (
                  ' an' if i == 0 else '', i, i, m[0], E(m[4])) for i, m in enumerate(M)),
              bild('roq1', 1000))))

# 13 Kapitel im Vollbild: der Teil wird zur Bühne über die ganze Breite; beim Scrollen blendet ein Foto ins nächste, die Jahreszahl wechselt
F.append(('Kapitel im Vollbild', '<div class="cz-13" data-cz-kapitel><div class="cz-13-fest"><div class="cz-13-bilder">%s</div><div class="cz-13-text">%s<div class="cz-13-st">%s</div></div></div>'
          '<div class="cz-13-marken">%s</div><div class="sw auf cz-k">%s</div></div>' % (
              ''.join('<figure class="cz-13-f%s" data-m="%d">%s</figure>' % (' an' if i == 0 else '', i, bild(m[3], 1600 if m[3] == 'kueche' else 1000)) for i, m in enumerate(M)),
              titel('links', ''),
              ''.join('<div class="cz-13-s%s" data-m="%d"><p class="cz-13-j">%s</p><p class="mono ch-w">%s</p><p>%s</p></div>' % (
                  ' an' if i == 0 else '', i, m[0], E(m[1]), E(m[2])) for i, m in enumerate(M)),
              ''.join('<span data-m="%d"></span>' % i for i in range(len(M))), KNOPF)))

# 14 Der Abspann: wie am Ende eines Films, zwei Spalten mittig gesetzt; links wann, rechts was und mit wem
ABSPANN = [('Mai 2023', 'Das erste Pop-up', 'Momo'), ('Herbst 2023', 'Die ersten Abende als Culinarium', 'Momo x Christoph'),
           ('2024', 'Rudi kommt in die Küche', 'Momo x Rudi'), ('Februar 2025', 'Vierzehn Plätze an einer Tafel', 'freitags ab 19, samstags ab 17 Uhr'),
           ('September 2026', 'Ausgebucht, bevor es beginnt', 'Fr 25. und Sa 26.')]
F.append(('Der Abspann', '<div class="cz-14"><figure class="cz-14-hinten">%s</figure><div class="cz-14-rolle" data-cz-par>'
          '<p class="cz-14-titel">Culinarium</p><p class="cz-14-unter">seit 2023 im Walk on the Wild Side</p>%s'
          '<div class="cz-14-z gross"><span>Drinks</span><b>Momo</b></div><div class="cz-14-z gross"><span>Küche</span><b>Rudi</b></div><div class="cz-14-z gross"><span>Bar</span><b>Derya</b></div>'
          '<div class="cz-14-z"><span>Ort</span><b>Haasemannstraße 13, Hannover-Linden</b></div><div class="sw auf cz-14-k">%s</div></div></div>' % (
              bild('barnacht', 1000),
              ''.join('<div class="cz-14-z"><span>%s</span><b>%s<em>%s</em></b></div>' % (E(a), E(b), E(c)) for a, b, c in ABSPANN), KNOPF)))

# 15 Zwei Linien, ein x: Momos Linie läuft seit 2023 durch, Christophs endet, Rudis kommt 2024 dazu; wo sie zusammenlaufen, steht das x
F.append(('Zwei Linien, ein x', '<div class="cz-15">%s<div class="cz-15-feld auf"><svg class="cz-15-svg" viewBox="0 0 1200 360" preserveAspectRatio="none" aria-hidden="true">'
          '<path class="cz-15-momo" d="M0 180 H1200"/><path class="cz-15-chr" d="M220 70 C330 70 340 175 420 178 M420 182 C470 182 500 110 560 70"/>'
          '<path class="cz-15-rudi" d="M560 300 C650 300 660 185 760 182 H1200"/></svg>'
          '<div class="cz-15-kopf k1"><figure>%s</figure><b>Momo</b><span>seit Mai 2023</span></div>'
          '<div class="cz-15-kopf k2"><b>Christoph</b><span>Herbst 2023 bis Januar 2024</span></div>'
          '<div class="cz-15-kopf k3"><figure>%s</figure><b>Rudi</b><span>seit 2024</span></div><p class="cz-15-x">x</p>'
          '<div class="cz-15-jahre">%s</div></div><div class="cz-15-momente">%s</div><div class="sw auf cz-k">%s</div></div>' % (
              titel('mitte', 'Momo ist von Anfang an da. Rudi kommt dazu, und seitdem heisst es Momo x Rudi.'),
              bild('kopf_momo', 640), bild('kopf_rudi', 640),
              ''.join('<span style="--x:%d">%s</span>' % (x, j) for x, j in [(0, '2023'), (36, '2024'), (66, '2025'), (93, '2026')]),
              ''.join('<div class="cz-15-m"><figure>%s</figure><p class="mono ch-w">%s</p><p>%s</p></div>' % (bild(m[3], 640), wo(m), E(m[2])) for m in M), KNOPF)))


def main():
    seite = open(os.path.join(HIER, 'index.html')).read()
    m = re.search(r'(<section class="vab v-chronik[^"]*"[^>]*id="chronik"[^>]*>)(<div class="vi h-chronik">.*?)(<p class="ueber[^>]*>[^<]*</p></section>)', seite, re.S)
    assert m, 'Teil «Seit 2023» in index.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab v-chronik', 'data-name="Seit 2023 · Runde 2" class="vab v-chronik wahl', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv chw ch2 cz-f%02d" data-n="%d" hidden><div class="vi">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Seit 2023 · Runde 2</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: fünf Bildkarten mit Jahreszahl'] + [n for n, _x in F]
    css = ('chronik-wahl.css', 'chronik-wahl-2.css', 'chronik-wahl.js', 'chronik-wahl-2.js')
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in css)
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["chronik"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/chronik-wahl.js?v=%s" defer></script>
<script src="assets/chronik-wahl-2.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v, v)
    seite = seite.replace('<title>', '<title>Seit 2023 wählen, Runde 2 · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/chronik-wahl.css?v=%s">\n<link rel="stylesheet" href="assets/chronik-wahl-2.css?v=%s">\n</head>' % (VERSION, v, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'chronik-wahl-2.html'), 'w').write(seite)
    print('Seite chronik-wahl-2.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
