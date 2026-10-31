#!/usr/bin/env python3
"""Culinarium Hannover · Der Weg «So findest du hin.» in 20 weiteren Fassungen, direkt in der echten Weg-Seite, 27.10.2026.
Robert: «Vergiss, was ich gesagt habe. Mach bitte nochmal 20 neue Versionen.» Die 15 aus weg-wahl.html (weg_wahl.py) kommen hier nicht wieder vor:
keine Tischkarte, kein Leuchtschild, keine Zeitleiste, kein Tag-Nacht-Schalter, keine Fensterschrift, kein Briefchen, kein Plakat, keine Skizze,
kein Zoom, kein Filmstreifen, kein Kühl und warm, kein Stapel, kein Schachbrett, kein Ruf an, kein Laufband.
Gegenstände aus der Bar und vom Weg dorthin: Bon am Pass, Tafel von oben, Aufsteller, Tür, Hausnummer, Leine, Bierdeckel, Postkarte, Uhr, Stempel,
Kerze, Garderobenmarke, die echte Karte (OpenStreetMap, Koordinaten 52.37026, 9.71346 laut Nominatim, passt zum Plus Code 9PC7+49), Vorhang,
Klingelleiste, Fensterfront, Magazinseite, Orgelpfeifen. Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll.
Baut weg-wahl-2.html (Leiste unten, Pfeiltasten, ?weg=Nummer); Fassung 0 ist der heutige Stand. Gemeinsame Teile aus weg_wahl.py.
Aufruf: python3 website/weg_wahl2.py"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION
from weg_wahl import bild, fig, titel, satz, knopf, tel, daten, BAR, TEL, MAPS, SATZ

HIER = bau.HIER
LAT, LON = 52.37026, 9.71346
OSM = 'https://www.openstreetmap.org/export/embed.html?bbox=%.5f,%.5f,%.5f,%.5f&layer=mapnik&marker=%.5f,%.5f' % (
    LON - .006, LAT - .0032, LON + .006, LAT + .0032, LAT, LON)
F = []

# 1 Der Bon am Pass: der Weg als Küchenbon, der an der Schiene hängt; er rutscht beim Ankommen ein Stück herunter
ZACKEN = 'polygon(0 0,100%% 0,100%% calc(100%% - 10px),%s,0 calc(100%% - 10px))' % ','.join(
    '%.2f%% %s' % (100 - k * 100 / 24, '100%' if k % 2 else 'calc(100% - 10px)') for k in range(1, 24))
BON = [('Walk on the Wild Side', ''), ('Haasemannstr. 13', ''), ('30449 Hannover', ''), None,
       ('Tisch', 'Tafel'), ('Plätze', '14'), None,
       ('Do', '19:00 – 01:00'), ('Fr', '19:00 – 02:00'), ('Sa', '19:00 – 02:00'), None,
       ('Culinarium Fr', 'ab 19:00'), ('Culinarium Sa', 'ab 17:00'), None,
       ('Plus Code', '9PC7+49'), ('Tel', '0163 3909578')]
F.append(('Der Bon am Pass', '<div class="vi wh01"><div class="wh01-l">%s%s<div class="wg-tat">%s</div></div>'
          '<div class="wh01-m"><i class="wh01-schiene"></i><div class="wh01-bon auf" style="clip-path:%s">%s<p class="wh01-ende">*** bis gleich ***</p></div></div>%s</div>' % (
              titel(), satz(), knopf(), ZACKEN,
              ''.join('<p class="wh01-strich"></p>' if z is None else '<p><span>%s</span><b>%s</b></p>' % (E(z[0]), E(z[1])) for z in BON),
              fig('theke', 'wh01-b', '(max-width:860px) 100vw, 34vw', 1))))

# 2 Die Tafel von oben: die lange Tafel mit vierzehn Gedecken, an vier Plätzen stehen Tischkarten mit den Angaben; die Kerzen flackern
GEDECK = lambda: ''.join('<i class="wh02-teller"></i>' for _ in range(7))
KARTEN = [('Adresse', 'Haasemannstraße 13<br>30449 Hannover'), ('Plus Code', '9PC7+49'),
          ('Culinarium', 'Fr ab 19 · Sa ab 17'), ('Die Bar', 'Do bis Sa ab 19')]
F.append(('Die Tafel von oben', '<div class="vi wh02"><div class="wh02-kopf">%s%s</div><div class="wh02-raum auf">%s'
          '<div class="wh02-tisch"><div class="wh02-reihe">%s</div><div class="wh02-kerzen">%s</div><div class="wh02-reihe">%s</div>'
          '<div class="wh02-karten">%s</div></div></div><div class="wh02-unter"><div class="wg-tat">%s%s</div></div></div>' % (
              titel(cls='mitte'), satz('Vierzehn Plätze an einer langen Tafel, mitten in der Bar. So kommst du hin.', cls='mitte'),
              fig('tafelleer', 'wh02-b', '(max-width:860px) 100vw, 30vw'), GEDECK(),
              ''.join('<i style="--i:%d"></i>' % i for i in range(5)), GEDECK(),
              ''.join('<div class="wh02-karte" style="--k:%d"><p class="mono">%s</p><p>%s</p></div>' % (i, t, z) for i, (t, z) in enumerate(KARTEN)),
              knopf(), tel())))

# 3 Der Aufsteller: eine Kreidetafel steht vor der Hausecke; die Linie unter der Adresse zieht sich wie mit Kreide
F.append(('Der Aufsteller', '<div class="vi wh03">%s<div class="wh03-tafel auf" style="--i:1"><div class="wh03-schiefer">'
          '<p class="wh03-klein">Walk on the Wild Side</p><p class="wh03-gross">Haasemann&shy;straße 13</p><i class="wh03-kreide"></i>'
          '<p class="wh03-z">Bar: Donnerstag bis Samstag ab 19</p><p class="wh03-z">Culinarium: Freitag ab 19, Samstag ab 17</p>'
          '<p class="wh03-klein">Am Schild an der Ecke</p></div><i class="wh03-bein a"></i><i class="wh03-bein b"></i></div>'
          '<div class="wh03-text">%s%s%s<div class="wg-tat">%s%s</div></div></div>' % (
              fig('ecke', 'wh03-b', '(max-width:860px) 100vw, 56vw', 0, '50% 55%'), titel(), satz(), daten(('adresse', 'plus'), 'eng'), knopf(), tel())))

# 4 Die Tür geht auf: eine dunkle Tür mit der 13, beim Ankommen schwingt sie auf und dahinter liegt der Flur
F.append(('Die Tür geht auf', '<div class="vi wh04"><div class="wh04-text">%s%s%s<div class="wg-tat">%s%s</div></div>'
          '<div class="wh04-r"><div class="wh04-rahmen auf">%s<div class="wh04-tuer"><span class="wh04-nr">13</span><i class="wh04-griff"></i>'
          '<span class="wh04-schild">Walk on the Wild Side</span></div></div><button type="button" class="wh04-knopf" data-wh-tuer>Tür auf und zu</button></div></div>' % (
              titel(), satz('Haasemannstraße 13, an der Hausecke. Hinter der Tür geht es den Flur entlang, dort brennen schon die Kerzen.'),
              daten(('adresse', 'cul', 'bar'), 'eng'), knopf(), tel(), bild('flur', '(max-width:860px) 80vw, 30vw'))))

# 5 Die Hausnummer: eine riesige 13, in der das Nachtfoto der Bar liegt; daneben alles, was man wissen muss
F.append(('Die Hausnummer', '<div class="vi wh05"><div class="wh05-zahl auf" role="img" aria-label="13" style="background-image:url(assets/bild/barlicht-1000.webp?v=%s)">13</div>'
          '<div class="wh05-text"><p class="wh05-str">Haasemannstraße</p>%s%s%s<div class="wg-tat">%s%s</div></div></div>' % (
              VERSION, titel(), satz(), daten(('plus', 'cul', 'bar', 'tel'), 'eng'), knopf(), tel())))

# 6 Die Leine: fünf Fotos vom Weg an Holzklammern auf einer Leine quer durch den Raum; sie schwingen beim Ankommen aus
LEINE = [('schildtag', 'Das Schild', -3), ('ecke', 'Ecke Rampenstraße', 2), ('fensterdraussen', 'Am Fenster', -2), ('flur', 'Der Flur', 3), ('kerze3', 'Die Tafel', -1)]
F.append(('Die Leine', '<div class="wh06"><div class="vi wh06-kopf">%s%s</div><div class="wh06-leine"><svg class="wh06-schnur" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true">'
          '<path d="M0 6 Q500 70 1000 6"/></svg>%s</div><div class="vi wh06-unter">%s<div class="wg-tat">%s%s</div></div></div>' % (
              titel(), satz(), ''.join('<div class="wh06-f auf" style="--i:%d;--r:%ddeg;--y:%dpx"><i class="wh06-klammer"></i><figure>%s</figure><p class="mono">%s</p></div>' % (
                  i, r, [4, 22, 30, 22, 4][i], bild(k, '(max-width:860px) 40vw, 18vw'), t) for i, (k, t, r) in enumerate(LEINE)),
              daten(cls='vier'), knopf(), tel())))

# 7 Der Bierdeckel: ein runder Deckel mit der Adresse im Kreis liegt auf dem Tresenfoto und dreht sich beim Scrollen
RING = 'Walk on the Wild Side · Haasemannstraße 13 · Linden-Mitte · 30449 Hannover · '
F.append(('Der Bierdeckel', '<div class="vi wh07"><div class="wh07-l">%s<div class="wh07-deckel" data-wg-lauf="dreh" data-f="120"><svg viewBox="0 0 300 300" aria-hidden="true">'
          '<defs><path id="wh07-ring" d="M150,150 m-112,0 a112,112 0 1,1 224,0 a112,112 0 1,1 -224,0"/></defs><circle cx="150" cy="150" r="146" class="rand"/>'
          '<circle cx="150" cy="150" r="96" class="innen"/><text><textPath href="#wh07-ring">%s</textPath></text></svg>'
          '<p class="wh07-mitte"><b>13</b><span>Do bis Sa<br>ab 19 Uhr</span></p></div></div><div class="wh07-r">%s%s%s<div class="wg-tat">%s%s</div></div></div>' % (
              fig('bar', 'wh07-b', '(max-width:860px) 100vw, 46vw'), E(RING.upper()), titel(), satz(), daten(('adresse', 'plus', 'cul', 'bar'), 'eng'), knopf(), tel())))

# 8 Ein Satz mit Bildern: die Wegbeschreibung als ein grosser Satz in der Titelschrift, kleine Fotos stehen mitten im Text
KLEIN = lambda k: '<span class="wh08-bild auf">%s</span>' % bild(k, '160px')
F.append(('Ein Satz mit Bildern', '<div class="vi wh08"><p class="wg-et wh08-et">So findest du hin</p><p class="wh08-satz sw auf">'
          'Geh in Linden zur Haasemannstraße 13 %s Ecke Rampenstraße. Such das Schild %s mit dem gelben Rand, geh durch die Tür und den Flur %s entlang. '
          'Dann siehst du die Kerzen %s und bist da.</p><div class="wh08-unter">%s<div class="wg-tat">%s%s</div></div></div>' % (
              KLEIN('ecke'), KLEIN('schildnacht'), KLEIN('flur'), KLEIN('kerze3'), daten(cls='vier'), knopf(), tel())))

# 9 Der Wegweiser: ein Pfosten mit vier Brettern, die in verschiedene Richtungen zeigen; sie schwingen beim Ankommen ein
BRETTER = [('rechts hell', 'Walk on the Wild Side', 'Haasemannstraße 13 · Linden'), ('links kerze', 'Culinarium', 'Freitag ab 19 · Samstag ab 17'),
           ('rechts schiefer', 'Die Bar', 'Donnerstag bis Samstag ab 19 Uhr')]
F.append(('Der Wegweiser', '<div class="vi wh09">%s<div class="wh09-pfosten"><i class="wh09-stab"></i>%s'
          '<a class="wh09-brett rechts dunkel auf" style="--i:3;--r:2deg" href="%s"><b>In Google Maps öffnen</b><span>Plus Code 9PC7+49</span></a></div>'
          '<div class="wh09-text">%s%s%s</div></div>' % (
              fig('schildtag', 'wh09-b', '(max-width:860px) 100vw, 30vw'),
              ''.join('<div class="wh09-brett %s auf" style="--i:%d;--r:%ddeg"><b>%s</b><span>%s</span></div>' % (c, i, [-2, 3, -3][i], t, z) for i, (c, t, z) in enumerate(BRETTER)),
              MAPS, titel(), satz(), tel())))

# 10 Die Postkarte: Vorderseite mit dem Nachtfoto, die Rückseite schiebt sich darunter hervor, mit Anschrift, Marke und Stempel
F.append(('Die Postkarte', '<div class="vi wh10"><div class="wh10-text">%s%s<div class="wg-tat">%s%s</div></div><div class="wh10-karten">'
          '<div class="wh10-hinten auf" style="--i:1"><div class="wh10-gruss"><p>Komm vorbei! Die Bar liegt an der Hausecke, Ecke Rampenstraße. Am Schild mit dem gelben Rand erkennst du sie.</p>'
          '<p class="wh10-zeit">Bar Do bis Sa ab 19 · Culinarium Fr ab 19, Sa ab 17</p></div><div class="wh10-an"><span class="wh10-marke">×</span><span class="wh10-poststempel">Linden<br>30449</span>'
          '<p>Walk on the Wild Side</p><p>Haasemannstraße 13</p><p>30449 Hannover</p></div></div>'
          '<figure class="wh10-vorn auf">%s<span>Grüsse aus Linden</span></figure></div></div>' % (
              titel(), satz(), knopf(), tel(), bild('schildnacht', '(max-width:860px) 80vw, 34vw', '50% 35%'))))

# 11 Die Uhr: ein Zifferblatt über 24 Stunden, je Tag ein Ring für die Bar, Punkte, wo Culinarium beginnt; der Zeiger läuft auf 19 Uhr


def pkt(r, h):
    a = math.radians(h / 24 * 360 - 90)
    return 200 + r * math.cos(a), 200 + r * math.sin(a)


def bogen(r, h1, h2):
    (x1, y1), (x2, y2) = pkt(r, h1), pkt(r, h2)
    return 'M%.1f %.1fA%d %d 0 %d 1 %.1f %.1f' % (x1, y1, r, r, 1 if h2 - h1 > 12 else 0, x2, y2)


RINGE = [('Do', 158, 19, 25, None), ('Fr', 136, 19, 26, 19), ('Sa', 114, 19, 26, 17)]
UHR = ('<svg class="wh11-uhr" viewBox="0 0 400 400" role="img" aria-label="Öffnungszeiten als Zifferblatt">'
       '<circle cx="200" cy="200" r="186" class="blatt"/>%s%s%s%s<g class="wh11-zeiger"><line x1="200" y1="200" x2="200" y2="70"/></g><circle cx="200" cy="200" r="5" class="mitte"/></svg>') % (
    ''.join('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="strich"/>' % (pkt(176, h) + pkt(186 if h % 3 else 168, h)) for h in range(24)),
    ''.join('<text x="%.1f" y="%.1f">%02d</text>' % (pkt(196 - 0, h)[0], pkt(196, h)[1] + 4, h) for h in range(0, 24, 3)),
    ''.join('<path d="%s" class="ring"/><text class="tag" x="%.1f" y="%.1f">%s</text>' % (bogen(r, a, b), pkt(r, b + .8)[0], pkt(r, b + .8)[1] + 5, t) for t, r, a, b, _c in RINGE),
    ''.join('<circle cx="%.1f" cy="%.1f" r="7" class="cul"/>' % pkt(r, c) for _t, r, _a, _b, c in RINGE if c))
F.append(('Die Uhr', '<div class="vi wh11"><div class="wh11-l auf">%s<p class="wh11-leg"><span class="b">Die Bar</span><span class="c">Culinarium beginnt</span></p></div>'
          '<div class="wh11-r">%s%s%s<div class="wg-tat">%s%s</div></div></div>' % (
              UHR, titel(), satz('Donnerstags bis samstags öffnet die Bar um 19 Uhr. Culinarium beginnt freitags um 19, samstags schon um 17 Uhr.'),
              daten(('adresse', 'plus'), 'eng'), knopf(), tel())))

# 12 Der Stempel: ein Einlassstempel in Kerzenfarbe auf warmweissem Papier, er drückt sich beim Ankommen auf
F.append(('Der Stempel', '<div class="vi wh12">%s<div class="wh12-papier"><div class="wh12-stempel auf"><p class="wh12-ring">Walk on the Wild Side</p>'
          '<p class="wh12-gross">Haasemannstr. 13</p><p class="wh12-ring">Linden · Do bis Sa ab 19</p></div>'
          '<div class="wh12-text">%s%s%s<div class="wg-tat">%s%s</div></div></div></div>' % (
              fig('lachen', 'wh12-b', '(max-width:860px) 100vw, 34vw'), titel(), satz(), daten(('adresse', 'plus', 'cul', 'bar'), 'eng'), knopf(), tel())))

# 13 Bei Kerzenlicht: alles in einer Spalte um ein Kerzenfoto, ein warmer Schein dahinter atmet leise
F.append(('Bei Kerzenlicht', '<div class="vi wh13"><i class="wh13-schein" aria-hidden="true"></i>%s%s%s%s<div class="wg-tat">%s%s</div></div>' % (
    fig('ws00', 'wh13-b', '(max-width:860px) 60vw, 22vw'), titel(cls='mitte'), satz(cls='mitte'), daten(cls='vier'), knopf(), tel())))

# 14 Die Garderobenmarke: eine Messingmarke mit der 13 hängt am Haken und pendelt aus
F.append(('Die Garderobenmarke', '<div class="vi wh14"><div class="wh14-l">%s%s%s<div class="wg-tat">%s%s</div></div>'
          '<div class="wh14-m"><i class="wh14-haken"></i><div class="wh14-marke auf"><i class="wh14-loch"></i><span class="wh14-klein">Walk on the Wild Side</span>'
          '<b>13</b><span class="wh14-klein">Haasemannstraße</span></div></div>%s</div>' % (
              titel(), satz(), daten(('adresse', 'plus', 'cul', 'bar'), 'eng'), knopf(), tel(), fig('barneg', 'wh14-b', '(max-width:860px) 100vw, 30vw', 1))))

# 15 Die echte Karte: OpenStreetMap mit der Nadel an der Haasemannstraße 13, daneben das Schild in echt
F.append(('Die echte Karte', '<div class="vi wh15"><figure class="wh15-karte auf"><iframe title="Karte: Walk on the Wild Side, Haasemannstraße 13" src="%s"></iframe></figure>'
          '<div class="wh15-r">%s%s%s<div class="wg-tat">%s%s</div>%s</div></div>' % (
              E(OSM), titel(), satz(), daten(('adresse', 'plus', 'cul', 'bar'), 'eng'), knopf('Route in Google Maps'), tel(),
              fig('schildnacht', 'wh15-b', '(max-width:860px) 40vw, 12vw', 2))))

# 16 Der Vorhang: ein schwerer Vorhang in Schiefer geht auf, dahinter der Blick durch die Tür auf die Tafel; die Angaben stehen an der Bühnenkante
F.append(('Der Vorhang', '<div class="vi wh16"><div class="wh16-kopf">%s%s</div><div class="wh16-buehne auf">%s<i class="wh16-v l"></i><i class="wh16-v r"></i></div>'
          '<div class="wh16-kante">%s<div class="wg-tat">%s%s</div></div></div>' % (
              titel(cls='mitte'), satz(cls='mitte'), bild('kerze3', '(max-width:860px) 100vw, 80vw', '50% 45%'), daten(cls='vier'), knopf(), tel())))

# 17 Die Klingelleiste: drei Namensschilder mit Knopf; wer drückt, sieht rechts Foto und Angaben dazu
KLINGEL = [('bar', 'Walk on the Wild Side', 'Die Bar', 'barlicht', 'Haasemannstraße 13, an der Hausecke. Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr.'),
           ('cul', 'Culinarium', 'An der langen Tafel', 'kerze3', 'Freitag ab 19 Uhr, Samstag ab 17 Uhr. Vierzehn Plätze, nur an einzelnen Wochenenden.'),
           ('weg', 'Der Weg', 'Ecke Rampenstraße', 'schildtag', 'Plus Code 9PC7+49. Zwei Schilder an der Hausecke, schwarz mit gelbem Rand.')]
F.append(('Die Klingelleiste', '<div class="vi wh17" data-klingel="bar"><div class="wh17-l">%s%s<div class="wh17-platte auf" role="group" aria-label="Klingeln">%s</div>'
          '<div class="wg-tat">%s%s</div></div><div class="wh17-r auf" style="--i:1">%s</div></div>' % (
              titel(), satz('Drück auf eine Klingel.'),
              ''.join('<button type="button" class="wh17-zeile" data-wh-klingel="%s" aria-pressed="%s"><span class="wh17-name"><b>%s</b><em>%s</em></span><i></i></button>' % (
                  k, 'true' if k == 'bar' else 'false', n, u) for k, n, u, _b, _s in KLINGEL), knopf(), tel(),
              ''.join('<div class="wh17-anzeige" data-anzeige="%s"><figure>%s</figure><p>%s</p></div>' % (k, bild(b, '(max-width:860px) 100vw, 40vw'), s) for k, _n, _u, b, s in KLINGEL))))

# 18 Die Fensterfront: drei hohe Scheiben mit dunklen Sprossen wie die Fenster der Bar, auf der Fensterbank die Angaben; die Scheiben werden nacheinander hell
F.append(('Die Fensterfront', '<div class="vi wh18"><div class="wh18-kopf">%s%s</div><div class="wh18-front auf">%s</div>'
          '<div class="wh18-bank">%s</div><div class="wg-tat">%s%s</div></div>' % (
              titel(), satz(),
              ''.join('<figure class="wh18-s" style="--i:%d">%s<i class="wh18-dunkel"></i></figure>' % (i, bild(k, '(max-width:860px) 33vw, 30vw', p)) for i, (k, p) in enumerate(
                  [('fassade', '50% 50%'), ('barlicht', '50% 55%'), ('fensterdraussen', '50% 50%')])),
              daten(('adresse', 'cul', 'bar')), knopf(), tel())))

# 19 Die Magazinseite: wie eine Seite im Stadtmagazin, mit Dachzeile, Initiale, Spalten, grossem Bild und einem Kasten «Auf einen Blick»
F.append(('Die Magazinseite', '<div class="vi wh19"><p class="wg-et wh19-dach">Ausgehen in Linden</p>%s<div class="wh19-seite">'
          '<div class="wh19-spalten"><p class="wh19-erst">Die Bar liegt an der Hausecke der Haasemannstraße, dort, wo die Rampenstraße abgeht. Von weitem siehst du zwei Schilder, schwarz mit gelbem Rand, darauf Walk on the Wild Side.</p>'
          '<p>Abends leuchtet das Schild über der Ecke, und durch die grossen Fenster siehst du schon die Theke. Geh durch die Tür und den Flur entlang, dann bist du drin.</p>'
          '<blockquote class="wh19-zitat">Am Schild mit dem gelben Rand erkennst du sie.</blockquote>'
          '<p>Die Bar hat donnerstags bis samstags ab 19 Uhr geöffnet. An einzelnen Wochenenden steht dort die lange Tafel von Culinarium, freitags ab 19, samstags ab 17 Uhr.</p></div>'
          '<figure class="wh19-b auf">%s<figcaption class="mono">Das Schild an der Hausecke</figcaption></figure>'
          '<aside class="wh19-kasten auf" style="--i:1"><p class="wg-et">Auf einen Blick</p>%s<div class="wg-tat">%s%s</div></aside></div></div>' % (
              titel(), bild('schildtag', '(max-width:860px) 100vw, 40vw'), daten(('adresse', 'plus', 'cul', 'bar')), knopf(), tel())))

# 20 Die Orgelpfeifen: vier gleich breite Säulen, jede beginnt auf anderer Höhe, darunter je eine Angabe; beim Scrollen wandern sie verschieden schnell
PFEIFEN = [('schildtag', 'adresse', 0, -30), ('ecke', 'plus', 150, 40), ('flur', 'cul', 70, -50), ('kerze3', 'bar', 210, 30)]
F.append(('Die Orgelpfeifen', '<div class="vi wh20"><div class="wh20-text">%s%s<div class="wg-tat">%s%s</div></div><div class="wh20-pfeifen">%s</div></div>' % (
    titel(), satz(), knopf(), tel(),
    ''.join('<div class="wh20-p" style="--y:%dpx"><div data-wg-lauf="drift" data-f="%d"><figure class="auf" style="--i:%d">%s</figure>%s</div></div>' % (
        y, f, i, bild(k, '(max-width:860px) 50vw, 20vw'), daten((d,), 'eins')) for i, (k, d, y, f) in enumerate(PFEIFEN)))))


def main():
    seite = open(os.path.join(HIER, 'weg.html'), encoding='utf-8').read()
    m = re.search(r'(<section class="vab bar-ab v-weg-abends[^"]*"[^>]*>)(.*?)(</section>)', seite, re.S)
    assert m, '«So findest du hin» in weg.html nicht gefunden (erst varianten.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab ', 'id="weg" data-name="So findest du hin" class="wahl vab ', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv wg wh wh-f%02d" data-n="%d" hidden>%s</div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Der Weg</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Angaben, vier Bilder um die Karte'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('weg-wahl.css', 'weg-wahl.js', 'weg-wahl-2.css', 'weg-wahl-2.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["weg"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/weg-wahl.js?v=%s" defer></script>
<script src="assets/weg-wahl-2.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v, v)
    seite = seite.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
    seite = seite.replace('<title>', '<title>Weg wählen 2 · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/weg-wahl.css?v=%s">\n'
                          '<link rel="stylesheet" href="assets/weg-wahl-2.css?v=%s">\n</head>' % (VERSION, v, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'weg-wahl-2.html'), 'w', encoding='utf-8').write(seite)
    print('Seite weg-wahl-2.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
