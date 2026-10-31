#!/usr/bin/env python3
"""Dirty Chicken · Abschnitt «Wie Dirty Chicken von sich spricht» (die Sätze in Berliner Schnauze) in 15 Fassungen zur Wahl (28.10.2026).
Robert: «15 alternative Visualisierungsmöglichkeiten». Heute: vier Sätze als Zitatwand in zwei Spalten (varianten.py › ZITATWAND, dc-zitate).
Material: die fünf echten Beiträge von @dirtychicken.hannover (Juni 2026, _quelle/dirty-chicken/ig/beitraege.md) mit ihren Bildern:
Burger DZId0KMoAtq, Drink DZIo4FHIqRR, Mannschaft DZIjZWNCGZT, Plakat zum Opening-Reel DZPYEOJIfVb, Tisch DZiug6EoMRr, dazu das Zeichen.
Jede Fassung ein anderes Gerüst, ein eigener bewegter Moment, nur transform und opacity, nichts überlappt, Gesichter unberührt.
Nicht noch einmal (schon in Essen- und Nacht-Wahl gezeigt): Feed, Bon, Stories, Liste mit Mausbild, Doppelseite, Kachelwand, Bahnen, Lichterkette.
Baut dirty-chicken-zitate-wahl.html (Hero, Fenster, Essen, Nacht, erstes Pop-up wie auf der echten Seite, dann der Teil umschaltbar; ?zitate=Nummer, 0 = heute).
Aufruf: python3 website/dc_zitate_wahl.py"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, foto, zl, sw
import varianten
import dc_essen
import dc_nacht

HIER = bau.HIER
KICK = 'In Berliner Schnauze'
TITEL = ('Wie Dirty Chicken', 'von sich spricht.')
TEXT = 'So wie Dirty Chicken auf Instagram schreibt: kurz, herzlich, ein bisschen Strasse. Fünf Sätze aus dem Juni 2026.'

# (Satz, Hochdeutsch, Datum, Bild, Beitrag)
Z = [
    ('Dit is keen Burger. Dit Ding is ’ne Ansage.', 'Das ist kein Burger. Das Ding ist eine Ansage.', '3. Juni 2026', 'dc_burger', 'DZId0KMoAtq'),
    ('Dirty Food &amp; Dirty Drinks. Jenau meen Ding wa.', 'Dirty Food &amp; Dirty Drinks. Genau mein Ding, was.', '3. Juni 2026', 'dc_drink', 'DZIo4FHIqRR'),
    ('Wenn aus Freunden und Kollegen Familie wird. Dann haste allet richtig jemacht!', 'Wenn aus Freunden und Kollegen Familie wird. Dann hast du alles richtig gemacht!', '3. Juni 2026', 'dc_team', 'DZIjZWNCGZT'),
    ('Opening 2026! Wat ne Sause.', 'Opening 2026! Was für ein Fest.', '6. Juni 2026', 'dc_plakat', 'DZPYEOJIfVb'),
    ('Dit ist wahre Liebe!', 'Das ist wahre Liebe!', '13. Juni 2026', 'dc_tisch', 'DZiug6EoMRr'),
]
IG = 'https://www.instagram.com/p/%s/'


def q(s):
    return '„%s“' % s


def ek(text, i=0):
    return '<p class="ek sw auf" style="--i:%d"><span>%s</span></p>' % (i, text)


def et(zeilen, cls='', i0=0):
    return zl(zeilen, 'h2', ('et ' + cls).strip(), i0)


def ex(text, i=2, cls=''):
    return sw(text, 'p', ('ex ' + cls).strip(), i)


def kopf(kick=KICK, titel=TITEL, text=TEXT, cls=''):
    return '<div class="vk nx-kopf %s">%s%s%s</div>' % (cls, ek(kick), et(list(titel)), ex(text) if text else '')


def sec(n, ton, inner, cls=''):
    return '<section class="vab dc-ab ess zts%02d %s" data-ton="%s">%s</section>' % (n, cls, ton, inner)


def d_zeichen(cls=''):
    return bau.zeichen_haus('dc', cls)


def datum(d, cls=''):
    return '<span class="mono zt-datum %s">%s</span>' % (cls, d)


F = []

# 1 Die Buchstabentafel: die Sätze stecken als weisse Buchstaben in einer schwarzen Filztafel wie im Café; die Buchstaben fallen Zeile für Zeile in ihre Rillen
def tafel_zeilen():
    out = []
    i = 0
    for s, _h, d, _k, _p in Z:
        text = re.sub('&amp;', '&', s).upper()
        for wort_zeile in zeilenbrechen(text, 22):
            spans = []
            for ch in wort_zeile:
                if ch == ' ':
                    spans.append('<i></i>')
                else:
                    spans.append('<b style="--i:%d">%s</b>' % (i, E(ch)))
                    i += 1
            out.append('<div class="zt1-z">%s</div>' % ''.join(spans))
        out.append('<div class="zt1-z zt1-d"><em>%s</em></div>' % d)
    return ''.join(out)


def zeilenbrechen(text, n):
    zeilen, akt = [], ''
    for w in text.split(' '):
        if akt and len(akt) + 1 + len(w) > n:
            zeilen.append(akt); akt = w
        else:
            akt = (akt + ' ' + w).strip()
    if akt:
        zeilen.append(akt)
    return zeilen


F.append(('Die Buchstabentafel', 'Die Sätze stecken als weisse Buchstaben in einer schwarzen Filztafel wie im Café; beim Ankommen fallen die Buchstaben Zeile für Zeile in ihre Rillen. Daneben Titel und das Foto vom Tisch.', sec(1, 'warm', '''<div class="vi zt1"><div class="zt1-tafel auf" aria-label="Die Sätze von Dirty Chicken auf einer Buchstabentafel">%s</div>
<div class="zt1-rechts">%s<div class="zt1-bild auf">%s</div></div></div>''' % (
    tafel_zeilen(), kopf(), foto('dc_tisch', '', '(max-width:860px) 100vw, 34vw', auf=False)))))

# 2 Die Leuchtschrift: eine Laufschrift aus Leuchtpunkten wie über dem Imbiss, die Sätze laufen in Kerzenfarbe von rechts nach links; darunter die fünf Bilder mit Datum
def lauf_text():
    return ' &nbsp;·&nbsp; '.join(re.sub('&amp;', '&amp;', s) for s, _h, _d, _k, _p in Z) + ' &nbsp;·&nbsp; '
F.append(('Die Leuchtschrift', 'Eine Laufschrift aus Leuchtpunkten wie über einem Imbiss: die fünf Sätze ziehen in Kerzenfarbe von rechts nach links über die ganze Breite. Darunter die fünf Beiträge als Bilder mit Datum.', sec(2, 'nacht', '''<div class="vi">%s</div>
<div class="zt2-kasten" aria-label="Laufschrift mit den Sätzen von Dirty Chicken"><div class="zt2-lauf"><p>%s</p><p aria-hidden="true">%s</p></div></div>
<div class="vi zt2-reihe auf">%s</div>''' % (
    kopf(cls='mitte'), lauf_text(), lauf_text(),
    ''.join('<figure class="zt2-b" style="--i:%d">%s<figcaption>%s<span>%s</span></figcaption></figure>' % (i, foto(k, '', '(max-width:860px) 50vw, 18vw', auf=False, pos='50% 40%'), datum(d), q(s)) for i, (s, _h, d, k, _p) in enumerate(Z))))))

# 3 Die Übersetzung: jeder Satz ist ein Knopf; antippen schiebt die Berliner Fassung nach oben hinaus und holt das Hochdeutsche von unten herein, nichts springt
F.append(('Die Übersetzung', 'Jeder Satz ist ein Knopf: Antippen schiebt die Berliner Fassung nach oben hinaus und holt das Hochdeutsche von unten herein. Noch einmal antippen, und die Schnauze ist zurück. Links Titel und die Mannschaft.', sec(3, 'warm', '''<div class="vi zt3"><div class="zt3-links">%s<div class="zt3-bild auf">%s</div></div>
<div class="zt3-liste auf">%s</div></div>''' % (
    kopf(text='Antippen übersetzt. Für alle, die nicht aus Berlin sind.'), foto('dc_team2', '', '(max-width:860px) 100vw, 30vw', auf=False, pos='50% 40%'),
    ''.join('<button type="button" class="zt3-z" style="--i:%d" aria-label="%s, antippen für Hochdeutsch"><span class="zt3-schlitz"><span class="zt3-b">%s</span><span class="zt3-h">%s</span></span><span class="zt3-u">%s<em>Berlinerisch</em><em>Hochdeutsch</em></span></button>' % (
        i, E(re.sub('&amp;', '&', s)), q(s), q(h), datum(d)) for i, (s, h, d, _k, _p) in enumerate(Z))))))

# 4 Das Wörterbuch: die Berliner Wörter aus den Sätzen als Einträge wie in einem kleinen Wörterbuch, mit Bedeutung, dem Satz, in dem sie stehen, und dem Bild dazu
W = [('Dit', 'das', 'Dit is keen Burger.', 'dc_burger'), ('keen', 'kein', 'Dit Ding is ’ne Ansage.', 'dc_burger'), ('jenau', 'genau', 'Jenau meen Ding wa.', 'dc_drink'),
     ('wa', 'nicht wahr; steht am Satzende', 'Jenau meen Ding wa.', 'dc_drink'), ('haste', 'hast du', 'Dann haste allet richtig jemacht!', 'dc_team'),
     ('allet', 'alles', 'Dann haste allet richtig jemacht!', 'dc_team2'), ('Sause', 'ein Fest, das länger geht', 'Opening 2026! Wat ne Sause.', 'dc_plakat')]
F.append(('Das Wörterbuch', 'Die Berliner Wörter aus den Sätzen als Einträge in einem kleinen Wörterbuch auf hellem Grund: das Wort gross, daneben die Bedeutung, der Satz, in dem es steht, und das Bild des Beitrags.', sec(4, 'hell', '<div class="vi">%s<div class="zt4-buch">%s</div></div>' % (
    kopf(kick='Kleines Wörterbuch', titel=('Dit, keen,', 'jenau, wa.'), text='Sieben Wörter, die auf Instagram öfter fallen. Für alle, die nicht aus Berlin sind.'),
    ''.join('<div class="zt4-e sw auf" style="--i:%d"><b>%s</b><div class="zt4-t"><p class="zt4-bed">%s</p><p class="zt4-satz">%s</p></div><div class="zt4-b">%s</div></div>' % (
        i % 4, w, b, q(s), foto(k, '', '(max-width:860px) 30vw, 10vw', auf=False, pos='50% 40%')) for i, (w, b, s, k) in enumerate(W))))))

# 5 Die Stempel: die Sätze als violette Stempel auf hellem Papier, jeder leicht schräg und beim Ankommen aufgedrückt; am Ende das Zeichen als runder Stempel
ST = [(-5, 'gross'), (3, ''), (-2, 'breit'), (4, ''), (-6, 'gross')]
F.append(('Die Stempel', 'Die Sätze als violette Stempel auf hellem Papier, jeder leicht schräg, in Versalien mit Rahmen und Datum; beim Ankommen werden sie nacheinander aufgedrückt. Zum Schluss das Zeichen als runder Stempel.', sec(5, 'hell', '<div class="vi">%s<div class="zt5-papier auf">%s<div class="zt5-rund" style="--i:5"><span class="zt5-ring">%s</span></div></div></div>' % (
    kopf(kick='Abgestempelt', titel=('Schwarz auf', 'weiss. Na ja, lila.')),
    ''.join('<div class="zt5-s %s" style="--i:%d;--r:%ddeg"><span class="zt5-text">%s</span><span class="zt5-d mono">%s</span></div>' % (cls, i, r, re.sub('&amp;', '&amp;', s).upper(), d) for i, ((s, _h, d, _k, _p), (r, cls)) in enumerate(zip(Z, ST))),
    d_zeichen('zt5-z')))))

# 6 Die Nachrichten: die Beiträge als Unterhaltung, wie Nachrichten von @dirtychicken.hannover: erst das Bild, dann der Satz, dazu das Datum; jede Nachricht kommt von links herein
def nachricht(i, s, d, k):
    return '''<div class="zt6-n" style="--i:%d"><div class="zt6-kopf">%s<b>dirtychicken.hannover</b>%s</div>
<div class="zt6-bild">%s</div><p class="zt6-text">%s</p></div>''' % (i, d_zeichen('zt6-z'), datum(d), foto(k, '', '(max-width:860px) 80vw, 26vw', auf=False, pos='50% 40%'), s)
F.append(('Die Nachrichten', 'Die Beiträge als Unterhaltung, wie Nachrichten von @dirtychicken.hannover: erst das Bild, dann der Satz, dazu das Datum. Jede Nachricht kommt von links herein, eine nach der anderen. Links der Titel.', sec(6, 'nacht', '<div class="vi zt6"><div class="zt6-links">%s</div><div class="zt6-faden auf">%s</div></div>' % (
    kopf(text='Fünf Beiträge, Juni 2026. Jeder klingt, als stünde jemand neben dir am Tresen.'), ''.join(nachricht(i, s, d, k) for i, (s, _h, d, k, _p) in enumerate(Z))))))

# 7 Die Titelseite: die Sätze als Schlagzeilen einer Boulevardzeitung, schwarze Versalien auf hellem Papier, ein Satz riesig, die Mannschaft als Aufmacherfoto, die anderen als Unterzeilen
F.append(('Die Titelseite', 'Die Sätze als Schlagzeilen einer Boulevardzeitung: Zeitungskopf in Violett, ein Satz riesig in schwarzen Versalien, die Mannschaft als Aufmacherfoto mit Bildzeile, die übrigen Sätze als Unterzeilen in der rechten Spalte.', sec(7, 'hell', '''<div class="vi zt7"><div class="zt7-kopfzeile sw auf" style="--i:0"><span class="mono">Hannover · Juni 2026</span><b>Dirty Chicken</b><span class="mono">Pop-up · Sandwiches &amp; More</span></div>
<h3 class="zt7-schlag zl auf" aria-label="%s"><span class="z"><span style="--i:1">Dit is keen</span></span><span class="z"><span style="--i:2">Burger.</span></span></h3>
<p class="zt7-unter sw auf" style="--i:3">Dit Ding is ’ne Ansage. Chicken-Sandwiches, Chunks mit Spicy Glaze, Dirty Drinks von der Bar und Musik, nur an einzelnen Tagen.</p>
<div class="zt7-unten"><figure class="zt7-foto auf">%s<figcaption>%s<span>%s</span></figcaption></figure>
<div class="zt7-spalte">%s</div></div></div>''' % (
    E('Dit is keen Burger.'), foto('dc_team', '', '(max-width:860px) 100vw, 60vw', auf=False, pos='50% 40%'), datum(Z[2][2]), q(Z[2][0]),
    ''.join('<div class="zt7-m sw auf" style="--i:%d">%s<b>%s</b></div>' % (i + 4, datum(d), q(s)) for i, (s, _h, d, _k, _p) in enumerate([Z[1], Z[3], Z[4]]))))))

# 8 Satz für Satz: links bleibt das Bild stehen und tauscht, rechts ziehen die Sätze vorbei; der Satz in der Mitte des Schirms bestimmt das Bild
F.append(('Satz für Satz', 'Links bleibt das Bild stehen, rechts ziehen die Sätze gross vorbei; welcher Satz in der Mitte des Schirms steht, bestimmt das Bild links, das sich von unten heraufschiebt. Nichts springt.', sec(8, 'warm', '''<div class="vi">%s</div>
<div class="vi zt8"><div class="zt8-bilder"><div class="zt8-box auf" data-wahl="0">%s</div></div>
<div class="zt8-saetze">%s</div></div>''' % (
    kopf(),
    ''.join('<div class="zt8-b" data-s="%d">%s</div>' % (i, foto(k, '', '(max-width:860px) 100vw, 40vw', auf=False, pos='50% 40%')) for i, (_s, _h, _d, k, _p) in enumerate(Z)),
    ''.join('<div class="zt8-s" data-s="%d"><p class="zt8-q zl auf" aria-label="%s">%s</p>%s</div>' % (i, E(re.sub('&amp;', '&', s)), ''.join('<span class="z"><span style="--i:%d">%s</span></span>' % (j, z) for j, z in enumerate(zeilenbrechen(q(s), 24))), datum(d)) for i, (s, _h, d, _k, _p) in enumerate(Z))))))

# 9 Die Untertitel: ein Bild wie im Kino mit schwarzen Balken, der Satz steht als Untertitel darunter; Pfeile schieben das nächste Bild samt Untertitel herein
F.append(('Die Untertitel', 'Ein Bild wie im Kino zwischen schwarzen Balken, der Satz steht als Untertitel darunter. Die Pfeile schieben das nächste Bild samt Untertitel seitwärts herein, Datum und Zähler laufen mit.', sec(9, 'nacht', '''<div class="vi">%s</div>
<div class="zt9-kino auf" data-akt="0"><div class="zt9-spur">%s</div>
<div class="zt9-ut"><div class="zt9-ut-spur">%s</div></div>
<div class="zt9-steuer"><button type="button" class="zt9-k" data-r="-1" aria-label="Voriger Satz">%s</button><span class="mono" data-zt9-nr>1 / %d</span><button type="button" class="zt9-k" data-r="1" aria-label="Nächster Satz">%s</button></div></div>''' % (
    kopf(cls='mitte'),
    ''.join('<div class="zt9-b">%s</div>' % foto(k, '', '(max-width:860px) 100vw, 70vw', auf=False, pos='50% 45%') for _s, _h, _d, k, _p in Z),
    ''.join('<div class="zt9-u"><p>%s</p>%s</div>' % (q(s), datum(d)) for s, _h, d, _k, _p in Z),
    bau.PFEIL.replace('<svg', '<svg class="zt9-pf-l"'), len(Z), bau.PFEIL))))

# 10 Die Fahnen: fünf helle Fahnen hängen an einer Stange, die Sätze laufen von oben nach unten; oben das Bild des Beitrags, unten das Datum; beim Ankommen pendeln sie aus
F.append(('Die Fahnen', 'Fünf helle Fahnen hängen an einer Stange, die Sätze laufen von oben nach unten wie auf einem Banner; oben das Bild des Beitrags, unten das Datum. Beim Ankommen pendeln die Fahnen aus und bleiben hängen.', sec(10, 'dc', '''<div class="vi">%s</div>
<div class="zt10-stange auf"><div class="zt10-reihe">%s</div></div>''' % (
    kopf(cls='mitte'),
    ''.join('<div class="zt10-f" style="--i:%d">%s<p class="zt10-t">%s</p>%s</div>' % (i, foto(k, '', '(max-width:860px) 40vw, 16vw', auf=False, pos='50% 40%'), q(s), datum(d)) for i, (s, _h, d, k, _p) in enumerate(Z))))))

# 11 Die Ansage: nur Schrift. Die fünf Sätze riesig in Versalien über die ganze Breite, abwechselnd gefüllt und als Umriss, die Zeilen kommen aus dem Schlitz
def ansage_zeile(i, s, d):
    zeilen = zeilenbrechen(re.sub('&amp;', '&', s).upper(), 20)
    return '<div class="zt11-s %s"><p class="zl auf" aria-label="%s">%s</p>%s</div>' % ('um' if i % 2 else 'voll', E(re.sub('&amp;', '&', s)), ''.join('<span class="z"><span style="--i:%d">%s</span></span>' % (j, E(z)) for j, z in enumerate(zeilen)), datum(d))
F.append(('Die Ansage', 'Nur Schrift: die fünf Sätze riesig in Versalien über die ganze Breite, abwechselnd gefüllt und als Umrisslinie, jede Zeile kommt aus dem Schlitz. Kein Bild, die Schnauze trägt den ganzen Teil.', sec(11, 'nacht', '<div class="vi">%s</div><div class="zt11-wand">%s</div>' % (
    kopf(text=''), ''.join(ansage_zeile(i, s, d) for i, (s, _h, d, _k, _p) in enumerate(Z))))))

# 12 Das Rad: die fünf Sätze laufen auf einem grossen Kreis um das Bild vom Tisch; das Rad dreht sich mit dem Scrollen, der Satz oben ist gerade dran
def rad_svg():
    # zwei Ringe in einer Drehgruppe: aussen drei Sätze, innen die zwei übrigen; Schriftgrösse aus dem Umfang (Fraunces etwa 0,5 em je Zeichen)
    def ring(rid, r, saetze):
        pfad = 'M 500,%d a %d,%d 0 1,1 0,%d a %d,%d 0 1,1 0,-%d' % (500 - r, r, r, 2 * r, r, r, 2 * r)
        text = ''.join('<tspan>%s</tspan><tspan class="zt12-punkt"> · </tspan>' % q(s) for s in saetze)
        n = sum(len(re.sub('&amp;', '&', s)) + 5 for s in saetze)
        u = int(2 * math.pi * r)
        fs = min(44, int(u / (n * .5)))
        return ('<path id="%s" d="%s"/>' % (rid, pfad),
                '<text class="zt12-text" style="font-size:%dpx"><textPath href="#%s" textLength="%d" lengthAdjust="spacing">%s</textPath></text>' % (fs, rid, u - 8, text))
    pa, ta = ring('zt12-a', 462, [Z[0][0], Z[1][0], Z[3][0]])
    pi, ti = ring('zt12-i', 336, [Z[2][0], Z[4][0]])
    return '<svg class="zt12-rad" viewBox="0 0 1000 1000" aria-hidden="true"><defs>%s%s</defs>%s%s</svg>' % (pa, pi, ta, ti)
F.append(('Das Rad', 'Die fünf Sätze laufen auf einem grossen Kreis um das Bild vom Tisch. Das Rad dreht sich mit dem Scrollen, in der Mitte steht das Bild still. Daneben Titel und die Sätze zum Lesen.', sec(12, 'warm', '''<div class="vi zt12"><div class="zt12-links">%s<div class="zt12-liste">%s</div></div>
<div class="zt12-buehne auf"><div class="zt12-dreh">%s</div><div class="zt12-mitte">%s</div></div></div>''' % (
    kopf(), ''.join('<p class="zt12-s sw auf" style="--i:%d">%s %s</p>' % (i + 3, q(s), datum(d)) for i, (s, _h, d, _k, _p) in enumerate(Z)),
    rad_svg(), foto('dc_tisch', '', '(max-width:860px) 60vw, 24vw', auf=False, ratio=False)))))

# 13 Die Streifen: fünf Bildstreifen über die ganze Breite, jeder nur einen Streifen hoch, der Satz steht mittig darauf; die Streifen kommen abwechselnd von links und rechts
F.append(('Die Streifen', 'Fünf Bildstreifen über die ganze Breite, jeder nur einen Streifen hoch, der Satz steht gross mittig darauf, das Datum am Rand. Die Streifen kommen abwechselnd von links und rechts herein.', sec(13, 'nacht', '<div class="vi">%s</div><div class="zt13-streifen auf">%s</div>' % (
    kopf(cls='mitte'), ''.join('<div class="zt13-s %s" style="--i:%d">%s<div class="zt13-text"><p>%s</p>%s</div></div>' % ('l' if i % 2 == 0 else 'r', i, foto(k, '', '100vw', auf=False, pos='50% 45%', extra='style="--weg:0px"'), q(s), datum(d)) for i, (s, _h, d, k, _p) in enumerate(Z))))))

# 14 Lauter: jeder Satz wird beim Heraufscrollen grösser, als würde jemand lauter sprechen, bis er die ganze Breite füllt; daneben das Bild klein
F.append(('Lauter', 'Jeder Satz wächst beim Heraufscrollen, als würde jemand lauter sprechen, bis er die ganze Breite füllt; danach macht er dem nächsten Platz. Neben jedem Satz das Bild des Beitrags, klein.', sec(14, 'dc', '<div class="vi">%s</div><div class="vi zt14-folge">%s</div>' % (
    kopf(), ''.join('<div class="zt14-s"><div class="zt14-bild auf">%s</div><div class="zt14-q"><p>%s</p>%s</div></div>' % (foto(k, '', '(max-width:860px) 40vw, 14vw', auf=False, pos='50% 40%'), q(s), datum(d)) for s, _h, d, k, _p in Z)))))

# 15 Die Bierdeckel: die Sätze auf runden Bierdeckeln, die auf dem dunklen Tisch liegen, leicht verdreht; dazwischen das Glas rund; die Deckel landen nacheinander
BD = [(-7, 'dc_burger'), (4, None), (-3, 'dc_drink'), (6, None), (-5, None), (2, 'dc_tisch')]
def bierdeckel():
    out, zi = [], 0
    for i, (r, k) in enumerate(BD):
        if k:
            out.append('<div class="zt15-rund zt15-foto" style="--i:%d;--r:%ddeg">%s</div>' % (i, r, foto(k, '', '(max-width:860px) 44vw, 20vw', auf=False, pos='50% 45%')))
        else:
            s, _h, d, _k, _p = Z[zi]; zi += 1
            out.append('<div class="zt15-rund zt15-deckel %s" style="--i:%d;--r:%ddeg"><span class="zt15-ring"></span><p>%s</p>%s</div>' % ('lang' if len(s) > 50 else '', i, r, q(s), datum(d)))
    for s, _h, d, _k, _p in Z[zi:]:
        i += 1
        out.append('<div class="zt15-rund zt15-deckel %s" style="--i:%d;--r:%ddeg"><span class="zt15-ring"></span><p>%s</p>%s</div>' % ('lang' if len(s) > 50 else '', i, (-4, 5)[i % 2], q(s), datum(d)))
    return ''.join(out)
F.append(('Die Bierdeckel', 'Die Sätze auf runden Bierdeckeln, die auf dem dunklen Tisch liegen, jeder leicht verdreht, mit Ring und Datum; dazwischen Burger, Drink und Tisch als runde Bilder. Die Deckel landen nacheinander auf dem Tisch.', sec(15, 'warm', '<div class="vi">%s</div><div class="vi zt15-tisch auf">%s</div>' % (
    kopf(kick='Vom Tresen', titel=('Steht auf', 'dem Deckel.'), text='Was Dirty Chicken schreibt, passt auf einen Bierdeckel. Fünf Sätze, Juni 2026.'), bierdeckel()))))


def main():
    # Rahmen ist die echte dirty-chicken.html im heutigen Stand (zitate_rahmen.py, Robert 28.10.2026: «die aktuellen Formate der Website»)
    import zitate_rahmen
    kb = zitate_rahmen.seite('dirty-chicken-zitate-wahl.html', 'zitate', 'Zitate', F, 'dc-zitate-wahl.css', 'dc-zitate-wahl.js', 'Zitate wählen · Dirty Chicken')
    json.dump([{'nr': i, 'name': n, 'satz': s_} for i, (n, s_, _h) in enumerate(F, 1)], open(os.path.join(HIER, '_sicherung', 'zitate-fassungen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Seite dirty-chicken-zitate-wahl.html', kb, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
