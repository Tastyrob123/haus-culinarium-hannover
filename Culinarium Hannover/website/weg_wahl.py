#!/usr/bin/env python3
"""Culinarium Hannover · Der Weg «So findest du hin.» in 15 Fassungen, direkt in der echten Weg-Seite, 27.10.2026.
Robert: «Gib mir 15 verschiedene visuelle Darstellungsmöglichkeiten für diesen Bereich.» Heute: Titel, Angaben in zwei Spalten,
darunter vier Fotos um die Karte «Die Bar» mit den Öffnungszeiten.
Jede Fassung eine eigene Anordnung aus der Welt des Hauses (Tischkarte, Leuchtschild, Streichholzbriefchen, Plakat, Abzüge,
Stadtplan, Fensterschrift, das x aus MOMO X RUDI …), gezogen mit der Entwurfs-Maschine (anreise), ohne Nummern-Liste und ohne Pillen.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Angaben nur aus varianten.py (WEG_DATEN, KARTE_BAR); «Ecke Rampenstraße» steht auf dem Strassenschild im Foto ecke.
Baut weg-wahl.html (Leiste unten, Pfeiltasten, ?weg=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/weg_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, PFEIL

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets/bild/meta.json')))
MAPS = 'https://www.google.com/maps/search/?api=1&query=Walk+on+the+Wild+Side+Haasemannstra%C3%9Fe+13+30449+Hannover'
TEL = ('tel:+491633909578', '+49 163 3909578')
SATZ = 'Die Bar liegt an der Hausecke, am Schild mit Walk on the Wild Side erkennst du sie.'
BAR = [('Donnerstag', '19 bis 1 Uhr'), ('Freitag', '19 bis 2 Uhr'), ('Samstag', '19 bis 2 Uhr')]


def bild(k, sizes='50vw', pos=None):
    st = META[k]['stufen']
    p, alt = bau.BILD[k][1], bau.BILD[k][2]
    s = ', '.join('assets/bild/%s-%d.webp?v=%s %dw' % (k, w, VERSION, w) for w in st)
    return '<img src="assets/bild/%s-%d.webp?v=%s" srcset="%s" sizes="%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        k, st[min(1, len(st) - 1)], VERSION, s, sizes, E(alt), pos or p)


def fig(k, cls='', sizes='50vw', i=0, pos=None, extra=''):
    return '<figure class="%s auf" style="--i:%d"%s>%s</figure>' % (cls, i, extra, bild(k, sizes, pos))


def titel(zeilen=('So findest du hin.',), cls=''):
    return bau.zl(list(zeilen), 'h2', 'wg-t ' + cls)


def satz(t=SATZ, i=1, cls=''):
    return bau.sw(E(t), 'p', 'wg-satz ' + cls, i)


def knopf(t='In Google Maps öffnen', cls=''):
    return bau.knopf(t, MAPS, cls)


def tel(cls='wg-tel'):
    return '<a class="%s" href="%s">%s</a>' % (cls, TEL[0], TEL[1])


TEILE = {
    'adresse': ('Adresse', 'Walk on the Wild Side<br>Haasemannstraße 13<br>30449 Hannover'),
    'plus': ('Plus Code', '9PC7+49 Hannover'),
    'cul': ('Culinarium', 'Freitag ab 19:00<br>Samstag ab 17:00'),
    'bar': ('Die Bar', '<br>'.join('%s %s' % (t, z) for t, z in BAR)),
    'tel': ('Telefon', '<a href="%s">%s</a>' % TEL),
}


def daten(teile=('adresse', 'plus', 'cul', 'bar'), cls=''):
    return '<dl class="wg-d %s">%s</dl>' % (cls, ''.join(
        '<div><dt class="mono">%s</dt><dd>%s</dd></div>' % TEILE[k] for k in teile))


F = []

# 1 Die Tischkarte: der Weg als gedruckte Karte am Platz, in Rudis Zeilen SCHILD / ECKE / FLUR, liegt schräg auf dem Foto vom gedeckten Tisch
GAENGE = [('Schild', 'Schwarz mit gelbem Rand, oben an der Hausecke. Abends leuchtet es.'),
          ('Ecke', 'Haasemannstraße 13, Ecke Rampenstraße, mitten in Linden.'),
          ('Flur', 'Durch die Tür und den Flur entlang, dahinter brennen die Kerzen.')]
F.append(('Die Tischkarte', '<div class="vi wg01">%s<div class="wg01-karte auf" style="--i:1"><p class="wg-et">Der Weg · Walk on the Wild Side</p>%s%s'
          '<div class="wg01-fuss"><span>Culinarium Freitag ab 19 · Samstag ab 17</span>%s</div></div>%s</div>' % (
              fig('karte', 'wg01-b', '(max-width:860px) 100vw, 70vw', 0, '50% 55%'),
              titel(cls='wg01-z'),
              ''.join('<div class="wg01-g"><b>%s</b><span>%s</span></div>' % g for g in GAENGE),
              tel(), '<div class="wg01-unter">%s%s</div>' % (daten(('adresse', 'plus', 'bar')), knopf()))))

# 2 Das Leuchtschild: das Schild der Bar nachgebaut, statt WILD SIDE steht die Adresse darauf; es hängt am Arm und geht an
F.append(('Das Leuchtschild', '<div class="vi wg02"><div class="wg02-l">%s%s%s<div class="wg-tat">%s%s</div></div>'
          '<div class="wg02-r"><div class="wg02-haken auf"><i class="wg02-arm"></i><div class="wg02-schild"><span class="wg02-klein">Walk on the</span>'
          '<span class="wg02-gross">Haase&shy;mann<br>straße<br>13</span><i class="wg02-licht"></i></div></div>%s</div></div>' % (
              titel(), satz(), daten(('adresse', 'cul', 'bar')), knopf(), tel(),
              fig('schildnacht', 'wg02-echt', '(max-width:860px) 40vw, 18vw', 2))))

# 3 Wann die Tür offen ist: die Nacht von 17 bis 3 Uhr als Leiste, je Tag die Bar und Culinarium; die Balken ziehen sich auf
STUNDEN = [17, 19, 21, 23, 1, 3]


def balken(von, bis, cls, offen=False):
    l = (von - 17) * 10
    b = ((bis if bis > 12 else bis + 24) - von) * 10 if bis else 46
    return '<i class="wg03-%s%s" style="left:%d%%;width:%d%%"></i>' % (cls, ' offen' if offen else '', l, b)


ZEILEN = [('Do', balken(19, 1, 'bar'), ''), ('Fr', balken(19, 2, 'bar'), balken(19, None, 'cul', True)),
          ('Sa', balken(19, 2, 'bar'), balken(17, None, 'cul', True))]
F.append(('Wann die Tür offen ist', '<div class="vi wg03"><div class="wg03-l">%s%s%s<div class="wg-tat">%s%s</div></div>'
          '<div class="wg03-r"><div class="wg03-plan auf" style="--i:1"><div class="wg03-skala"><span></span>%s</div>%s'
          '<p class="wg03-leg"><span class="b">Die Bar</span><span class="c">Culinarium, Ende offen</span></p></div>'
          '<div class="wg03-band">%s%s%s</div></div></div>' % (
              titel(), satz('Donnerstags bis samstags ist die Tür ab 19 Uhr offen. Culinarium beginnt freitags um 19, samstags schon um 17 Uhr.'),
              daten(('adresse', 'plus'), 'eng'), knopf(), tel(),
              ''.join('<b>%02d</b>' % h for h in STUNDEN),
              ''.join('<div class="wg03-z"><span>%s</span><div class="wg03-spur">%s%s</div></div>' % z for z in ZEILEN),
              fig('barlicht', '', '(max-width:860px) 33vw, 18vw', 2), fig('schildnacht', '', '(max-width:860px) 33vw, 18vw', 3),
              fig('kerze3', '', '(max-width:860px) 33vw, 18vw', 4))))

# 4 Tag und Nacht: zwei Bilder derselben Ecke, ein Schalter tauscht sie an Ort und Stelle
def paar(tag, nacht, cls, sizes):
    return '<figure class="wg04-f %s auf">%s%s</figure>' % (cls, bild(tag, sizes).replace('<img ', '<img class="wg04-tag" ', 1),
                                                          bild(nacht, sizes).replace('<img ', '<img class="wg04-nacht" ', 1))


F.append(('Tag und Nacht', '<div class="vi wg04" data-zeit="nacht"><div class="wg04-bilder">%s%s</div><div class="wg04-text">%s'
          '<div class="wg04-schalter" role="group" aria-label="Tageszeit"><button type="button" data-wg-zeit="tag" aria-pressed="false">Tagsüber</button>'
          '<i></i><button type="button" data-wg-zeit="nacht" aria-pressed="true">Abends</button></div>'
          '<p class="wg-satz wg04-s tag">Tagsüber erkennst du die Bar an den zwei Schildern an der Hausecke, Ecke Rampenstraße.</p>'
          '<p class="wg-satz wg04-s nacht">Abends leuchtet das Schild über der Ecke, und durch die Fenster siehst du schon die Theke.</p>%s%s</div></div>' % (
              paar('schildtag', 'schildnacht', 'a', '(max-width:860px) 50vw, 30vw'), paar('ecke', 'barlicht', 'b', '(max-width:860px) 50vw, 30vw'),
              titel(), daten(('adresse', 'cul', 'bar'), 'eng'), '<div class="wg-tat">%s%s</div>' % (knopf(), tel()))))

# 5 Schrift auf der Scheibe: die Adresse wie Blattgold aufs Fenster gemalt; beim Scrollen geht drinnen das Licht an
F.append(('Schrift auf der Scheibe', '<div class="vi wg05"><figure class="wg05-f auf">%s<i class="wg05-licht" data-wg-lauf="licht"></i>'
          '<p class="wg05-gold" aria-hidden="true"><span>Bar · Culinarium</span><b>Haasemannstraße 13</b><span>Linden</span></p></figure>'
          '<div class="wg05-unter"><div>%s%s</div>%s<div class="wg-tat">%s%s</div></div></div>' % (
              bild('barnacht', '(max-width:860px) 100vw, 90vw', '50% 62%'), titel(), satz(), daten(('adresse', 'cul', 'bar'), 'eng'), knopf(), tel())))

# 6 Das Streichholzbriefchen: vorn Name und Adresse, beim Ankommen klappt der Deckel auf, innen Hölzer und Öffnungszeiten
HOELZER = ''.join('<i style="--h:%d"></i>' % h for h in (0, 3, 1, 4, 2, 0, 3, 1, 2, 4))
F.append(('Das Streichholzbriefchen', '<div class="vi wg06">%s<div class="wg06-mitte"><div class="wg06-buch auf" style="--i:1">'
          '<div class="wg06-innen"><div class="wg06-hoelzer">%s</div><div class="wg06-reib"></div><div class="wg06-zeiten">%s</div></div>'
          '<div class="wg06-deckel"><div class="wg06-vorn"><span class="wg06-klein">Walk on the</span><b>Wild Side</b><span class="wg06-adr">Haasemannstraße 13 · Linden</span></div>'
          '<div class="wg06-hinten"><span class="wg06-klein">Culinarium</span><b>Fr ab 19<br>Sa ab 17</b>%s</div></div></div>'
          '<button type="button" class="wg06-knopf" data-wg-klappe>Auf- und zuklappen</button></div><div class="wg06-text">%s%s%s<div class="wg-tat">%s</div></div></div>' % (
              fig('loch', 'wg06-b', '(max-width:860px) 100vw, 34vw', 0), HOELZER,
              ''.join('<p><span>%s</span>%s</p>' % (t, z) for t, z in BAR), tel('wg06-tel'),
              titel(), satz(), daten(('adresse', 'plus'), 'eng'), knopf())))

# 7 Das Plakat zum Weg: wie die Plakate der Abende, warmweiss mit Linie in Kerze; Plakat und Nachtbild stossen an der Naht an
F.append(('Das Plakat zum Weg', '<div class="vi wg07"><div class="wg07-paar"><div class="wg07-plakat auf"><p class="wg07-kopf">Culinarium <em>×</em> Walk on the Wild Side</p>'
          '<p class="wg07-t">So findest<br>du hin.</p><figure>%s</figure><p class="wg07-adr">Haasemannstraße 13<br>30449 Hannover-Linden</p><i class="wg07-linie"></i>'
          '<p class="wg07-zeit">Culinarium Fr ab 19 · Sa ab 17</p><p class="wg07-bar">Die Bar: Do 19 bis 1 · Fr und Sa 19 bis 2</p></div>%s</div>'
          '<div class="wg07-unter">%s<div class="wg-tat">%s%s</div></div></div>' % (
              bild('ecke', '(max-width:860px) 60vw, 24vw', '50% 60%'),
              fig('schildnacht', 'wg07-foto', '(max-width:860px) 100vw, 36vw', 1), satz(i=0), knopf(), tel())))

# 8 Der Stadtplan im Strich: die Ecke als Skizze, drei Punkte antippen, das Foto daneben tauscht an derselben Stelle
ORTE = [('schild', 'Das Schild', 'schildtag', 'An der Hausecke hängen die zwei Schilder, schwarz mit gelbem Rand.', (61, 46)),
        ('ecke', 'Von der Rampenstraße', 'ecke', 'Aus der Rampenstraße siehst du die Ecke mit den Schildern schon von weitem.', (61, 14)),
        ('fenster', 'Die Fenster', 'barnacht', 'Abends leuchten die Fenster der Bar zur Haasemannstraße hin.', (42, 36))]
PLAN = ('<svg class="wg08-svg" viewBox="0 0 400 400" aria-hidden="true">'
        '<path class="blk" d="M24 24h196v130H24zM268 24h108v130H268zM24 214h196v162H24zM268 214h108v162H268z"/>'
        '<path class="str" d="M0 184h400M244 0v400"/><path class="haus" d="M150 104h70v50h-70z"/>'
        '<text x="34" y="200">Haasemannstraße</text><text x="256" y="236" transform="rotate(90 256 236)">Rampenstraße</text>'
        '<text class="kl" x="34" y="56">Linden-Mitte</text></svg>')
F.append(('Der Stadtplan im Strich', '<div class="vi wg08" data-ort="schild"><div class="wg08-l">%s%s<div class="wg08-plan auf" style="--i:1">%s%s</div>'
          '<p class="wg08-hin mono">Skizze, nicht massstäblich</p></div><div class="wg08-r"><figure class="wg08-f auf" style="--i:2">%s</figure>%s%s'
          '<div class="wg-tat">%s%s</div></div></div>' % (
              titel(), satz('Tippe auf einen Punkt, und du siehst, was du dort siehst.'), PLAN,
              ''.join('<button type="button" class="wg08-p" data-wg-ort="%s" style="left:%d%%;top:%d%%" aria-pressed="%s"><i></i><span>%s</span></button>' % (
                  k, x, y, 'true' if k == 'schild' else 'false', n) for k, n, _b, _s, (x, y) in ORTE),
              ''.join(bild(b, '(max-width:860px) 100vw, 40vw').replace('<img ', '<img data-ort-bild="%s" ' % k, 1) for k, _n, b, _s, _p in ORTE),
              ''.join('<p class="wg-satz wg08-s" data-ort-satz="%s">%s</p>' % (k, s) for k, _n, _b, s, _p in ORTE),
              daten(('adresse', 'cul', 'bar'), 'eng'), knopf(), tel())))

# 9 Heranzoomen: der Plus Code gross, daneben drei Rahmen ineinander (Ecke, Schild, Flur); beim Scrollen kommst du näher
F.append(('Heranzoomen', '<div class="vi wg09"><div class="wg09-l"><p class="wg09-code auf">9PC7+49</p>%s%s%s<div class="wg-tat">%s%s</div></div>'
          '<div class="wg09-r auf" style="--i:1"><figure class="wg09-a">%s<figure class="wg09-b" data-wg-lauf="zoom" data-f=".22">%s'
          '<figure class="wg09-c" data-wg-lauf="zoom" data-f=".3">%s</figure></figure></figure>'
          '<p class="wg09-wo mono"><span>Linden-Mitte</span><span>Haasemannstraße 13</span><span>Durch den Flur</span></p></div></div>' % (
              titel(), satz('Der Plus Code führt dich in Google Maps bis vor die Tür. Dort hängt das Schild, und hinter dem Flur liegt die Bar.'),
              daten(('adresse', 'cul', 'bar'), 'eng'), knopf(), tel(),
              bild('ecke', '(max-width:860px) 100vw, 46vw'), bild('schildnacht', '(max-width:860px) 60vw, 26vw'), bild('flur', '(max-width:860px) 40vw, 16vw'))))

# 10 Der Filmstreifen: sechs Hochformate vom Schild bis zur Tafel, seitwärts zum Blättern, jedes mit seinem Halt
HALTE = [('schildtag', 'Am Schild', 'Zwei Schilder an der Hausecke.'), ('ecke', 'Ecke Rampenstraße', 'Haasemannstraße 13, Linden-Mitte.'),
         ('schildnacht', 'Abends', 'Dann leuchtet das Schild.'), ('fensterdraussen', 'Am Fenster', 'Wer draussen sitzt, sitzt schon fast drin.'),
         ('flur', 'Durch den Flur', 'Die Tür, der Flur, das warme Licht.'), ('kerze3', 'An der Tafel', 'Hier beginnt der Abend.')]
F.append(('Der Filmstreifen', '<div class="wg10"><div class="vi wg10-kopf"><div>%s%s</div><div class="wg10-pf"><button type="button" data-wg-band="-1" aria-label="Zurück">‹</button>'
          '<button type="button" data-wg-band="1" aria-label="Weiter">›</button></div></div><div class="wg10-band" tabindex="0">%s</div>'
          '<div class="vi wg10-unter">%s<div class="wg-tat">%s%s</div></div></div>' % (
              titel(), satz(), ''.join('<div class="wg10-halt auf" style="--i:%d"><figure>%s</figure><p class="mono">%s</p><p class="wg10-s">%s</p></div>' % (
                  i, bild(k, '(max-width:860px) 72vw, 26vw'), n, s) for i, (k, n, s) in enumerate(HALTE)),
              daten(), knopf(), tel())))

# 11 Kühl und warm: links draussen bei Tag, rechts drinnen bei Kerzen, die Naht in Kerzenfarbe; die Bilder wandern gegeneinander
F.append(('Kühl und warm', '<div class="wg11"><div class="vi wg11-kopf">%s%s</div><div class="wg11-paar">'
          '<figure class="wg11-f auf"><div data-wg-lauf="drift" data-f="-50">%s</div></figure><i class="wg11-naht"></i>'
          '<figure class="wg11-f auf" style="--i:1"><div data-wg-lauf="drift" data-f="50">%s</div></figure></div>'
          '<div class="vi wg11-unter"><div><p class="wg11-wo">Draussen</p><p class="wg11-s">Das Schild an der Hausecke, Ecke Rampenstraße.</p>%s%s</div>'
          '<div><p class="wg11-wo">Drinnen</p><p class="wg11-s">Theke, Kerzen und an einzelnen Wochenenden die lange Tafel.</p>%s%s</div></div></div>' % (
              titel(), satz('Draussen ist Linden, drinnen brennen die Kerzen. Dazwischen liegt nur die Tür.'),
              bild('ecke', '(max-width:860px) 50vw, 50vw', '50% 40%'), bild('kerze3', '(max-width:860px) 50vw, 50vw'),
              daten(('adresse', 'plus'), 'eng'), knopf(), daten(('cul', 'bar'), 'eng'), tel())))

# 12 Der Stapel Abzüge: fünf Fotos mit weissem Rand übereinander, antippen legt das oberste nach hinten
ABZUEGE = [('schildnacht', 'Das Schild an der Ecke', -3), ('ecke', 'Ecke Rampenstraße', 4), ('barlicht', 'Abends leuchten die Fenster', -1),
           ('flur', 'Durch den Flur', 3), ('kerze3', 'Und dann die Tafel', -4)]
F.append(('Der Stapel Abzüge', '<div class="vi wg12"><div class="wg12-l">%s%s%s<div class="wg-tat">%s%s</div></div>'
          '<div class="wg12-r"><button type="button" class="wg12-stapel auf" data-wg-stapel aria-label="Nächstes Foto">%s</button>'
          '<p class="wg12-hin mono">Antippen für das nächste Foto</p></div></div>' % (
              titel(), satz(), daten(('adresse', 'plus', 'cul', 'bar'), 'eng zwei'), knopf(), tel(),
              ''.join('<span class="wg12-a" style="--r:%ddeg;z-index:%d">%s<em>%s</em></span>' % (r, len(ABZUEGE) - i, bild(k, '(max-width:860px) 80vw, 32vw'), t)
                      for i, (k, t, r) in enumerate(ABZUEGE)))))

# 13 Das Schachbrett: Bild und Angabe wechseln sich ab, gleich gross, drei Farben des Hauses
FELD = lambda cls, i, inner: '<div class="wg13-t %s auf" style="--i:%d">%s</div>' % (cls, i, inner)
F.append(('Das Schachbrett', '<div class="vi wg13"><div class="wg13-kopf">%s%s</div><div class="wg13-brett">%s%s%s%s%s%s</div>'
          '<div class="wg13-unter">%s</div></div>' % (
              titel(cls='mitte'), satz(cls='mitte'),
              fig('schildnacht', 'wg13-b', '(max-width:860px) 50vw, 30vw', 0),
              FELD('hell', 1, '<p class="mono">Adresse</p><p class="wg13-gross">Haasemann&shy;straße 13</p><p>30449 Hannover-Linden<br>Plus Code 9PC7+49</p>'),
              fig('ecke', 'wg13-b', '(max-width:860px) 50vw, 30vw', 2),
              FELD('kerze', 3, '<p class="mono">Die Bar</p>%s' % ''.join('<p class="wg13-z"><span>%s</span>%s</p>' % b for b in BAR)),
              fig('flur', 'wg13-b', '(max-width:860px) 50vw, 30vw', 4),
              FELD('schiefer', 5, '<p class="mono">Culinarium</p><p class="wg13-gross">Fr ab 19<br>Sa ab 17</p>%s' % tel()),
              knopf())))

# 14 Ruf an: die Frage an den Gast, die Nummer riesig, rundherum vier Bilder vom Weg verstreut
F.append(('Ruf an', '<div class="vi wg14">%s%s%s%s<div class="wg14-mitte"><p class="wg14-frage sw auf">Du stehst an der Ecke und findest die Tür nicht?</p>'
          '%s<a class="wg14-nr" href="%s">%s</a>%s</div>%s</div>' % (
              fig('schildtag', 'wg14-b a', '(max-width:860px) 40vw, 18vw', 0), fig('fensterdraussen', 'wg14-b b', '(max-width:860px) 40vw, 14vw', 1),
              fig('flur', 'wg14-b c', '(max-width:860px) 40vw, 15vw', 2), fig('barlicht', 'wg14-b d', '(max-width:860px) 40vw, 19vw', 3),
              '<p class="wg14-ruf sw auf" style="--i:1">Ruf in der Bar an:</p>', TEL[0],
              bau.zl(['+49 163', '3909578'], 'span', 'wg14-z'), satz('Haasemannstraße 13, Ecke Rampenstraße. Das Schild hängt an der Hausecke.', 2, 'mitte'),
              '<div class="wg14-unter">%s%s</div>' % (daten(), knopf()))))

# 15 Das Laufband: ein Band in der Titelschrift läuft quer, getrennt vom x aus MOMO X RUDI, darunter die Fotoreihe ohne Lücke
LAUF = ' <i>×</i> '.join(['Haasemannstraße 13', 'Linden-Mitte', 'Donnerstag bis Samstag ab 19 Uhr', 'Culinarium freitags ab 19, samstags ab 17', 'Am Schild an der Ecke']) + ' <i>×</i> '
F.append(('Das Laufband', '<div class="wg15"><div class="vi wg15-kopf">%s%s<div class="wg-tat">%s%s</div></div>'
          '<div class="wg15-lauf" aria-hidden="true"><p class="wg15-spur"><span>%s</span><span>%s</span></p></div>'
          '<div class="wg15-reihe">%s%s%s%s%s</div><div class="vi">%s</div></div>' % (
              titel(cls='mitte'), satz(cls='mitte'), knopf(), tel(), LAUF, LAUF,
              fig('schildtag', 'w2', '(max-width:860px) 50vw, 26vw', 0), fig('ecke', 'w1', '(max-width:860px) 50vw, 14vw', 1),
              fig('fensterdraussen', 'w15', '(max-width:860px) 50vw, 20vw', 2), fig('flur', 'w1', '(max-width:860px) 50vw, 14vw', 3),
              fig('schildnacht', 'w2', '(max-width:860px) 50vw, 26vw', 4), daten(cls='vier'))))


def main():
    seite = open(os.path.join(HIER, 'weg.html'), encoding='utf-8').read()
    m = re.search(r'(<section class="vab bar-ab v-weg-abends[^"]*"[^>]*>)(.*?)(</section>)', seite, re.S)
    assert m, '«So findest du hin» in weg.html nicht gefunden (erst varianten.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab ', 'id="weg" data-name="So findest du hin" class="wahl vab ', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv wg wg-f%02d" data-n="%d" hidden>%s</div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Der Weg</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Angaben, vier Bilder um die Karte'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('weg-wahl.css', 'weg-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["weg"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/weg-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
    seite = seite.replace('<title>', '<title>Weg wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/weg-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'weg-wahl.html'), 'w', encoding='utf-8').write(seite)
    print('Seite weg-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
