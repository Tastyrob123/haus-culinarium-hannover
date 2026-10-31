#!/usr/bin/env python3
"""Culinarium Hannover · «Was auf den Tisch kommt» (Seite Der Abend), zweite Runde: 20 Fassungen, direkt in der echten Seite, 27.10.2026.
Robert: «20 alternative Visualisierungen … so richtig geil, dass es abholt und Bock macht», dazu: «mit mehr Bildern, mehr Wow und luxuriös».
Keine wiederholt eine der 15 aus menue_wahl.py. Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll;
Hereinkommendes ist von Anfang an sichtbar. Gold auf Schwarz, Kerzenlicht, grosse Fotos.
Baut menue-wahl-2.html (Leiste unten, Pfeiltasten, ?tisch=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/menue_wahl2.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, zl, marke
from menue_wahl import META, TITEL, SATZ, ZEILE, FUSS, T, bild, titel, unter, karte

HIER = bau.HIER
MIT = 'A UNiQUE EXPERiENCE BY MOMO X RUDI'


def url(k, w=1600):
    st = [s for s in META[k]['stufen'] if s <= w] or META[k]['stufen'][:1]
    return 'assets/bild/%s-%d.webp?v=%s' % (k, st[-1], VERSION)


def teil(t, cls='mx-teil'):
    return '<div class="%s"><h3 class="mx-n">%s</h3><p class="mx-u">%s</p></div>' % (cls, E(t[0]), unter(t))


def teile(cls='mx-teile'):
    return '<div class="%s">%s</div>' % (cls, ''.join(teil(t) for t in T))


def fuss():
    return '<p class="mx-fuss">%s</p>' % E(FUSS)


F = []  # (Name, Inhalt)

# 1 Vier Säulen: vier hohe Bildsäulen im Kerzenlicht, versetzt gehängt, jede gleitet beim Scrollen in eigenem Tempo
S01 = [(T[0], 'toast', 'glaeser', '0px', .05), (T[1], 'beete', 'anrichten', '96px', -.04), (T[2], 'g1', 'momo', '28px', .07), (T[3], 'klaeren', 'schaum', '128px', -.02)]
F.append(('Vier Säulen', '<div class="mx01">%s<div class="mx01-reihe">%s</div>%s</div>' % (
    titel('reihe'),
    ''.join('<figure class="mx01-s" data-mx-par="%s" style="--o:%s"><div class="mx01-b">%s</div><figcaption><h3 class="mx-n">%s</h3><p class="mx-u">%s</p></figcaption><div class="mx01-b2">%s</div></figure>' % (
        sp, o, bild(a, 1000), E(t[0]), unter(t), bild(b, 640)) for t, a, b, o, sp in S01),
    fuss())))

# 2 Die Glocke hebt sich: der Teller unter einer dunklen Glocke auf dem Platzteller, beim Scrollen hebt sie sich
F.append(('Die Glocke hebt sich', '<div class="mx02"><div class="mx02-l">%s</div>'
          '<div class="mx02-buehne" data-mx-glocke><span class="mx02-platz"></span><figure class="mx02-teller">%s</figure>'
          '<div class="mx02-glocke"><i class="mx02-knauf"></i></div></div><div class="mx02-r">%s%s</div></div>'
          '<div class="mx02-band">%s</div>' % (
              titel(), bild('r02', 1000), teile(), fuss(),
              ''.join('<figure class="auf" style="--i:%d">%s</figure>' % (i, bild(k, 640)) for i, k in enumerate(['beeteglas', 'r09', 'g2', 'hok1', 'kerze1'])))))

# 3 Im Wort: «Tisch» riesig, die Buchstaben sind aus dem Foto vom Anstossen geschnitten; darunter die vier Teile mit Bildern
F.append(('Im Wort', '<div class="mx03"><h2 class="mx03-h" aria-label="Was auf den Tisch kommt."><span class="mx03-vor">Was auf den</span>'
          '<span class="mx03-wort" style="background-image:url(%s)">Tisch</span><span class="mx03-nach">kommt.</span></h2>'
          '<div class="mx03-unten"><div class="mx03-l"><p class="sw auf">%s</p>%s</div><div class="mx03-vier">%s</div></div></div>' % (
              url('anstossen', 2400), SATZ, fuss(),
              ''.join('<figure class="mx03-f auf" style="--i:%d"><div class="mx03-b">%s</div><figcaption><h3 class="mx-n">%s</h3><p class="mx-u">%s</p></figcaption></figure>' % (
                  i, bild(k, 640), E(t[0]), unter(t)) for i, (t, k) in enumerate(zip(T, ['glaeser', 'beete', 'g1', 'klaeren']))))))

# 4 Salonhängung: eine dunkle Wand voller gerahmter Bilder mit Passepartout, mittendrin die Karte als Hauptwerk; beim Ankommen rücken die Rahmen gerade
SALON = [('anstossen', '1 / 1 / 7 / 5', -2.4, 'Aperitif', 'zum Ankommen'), ('beete', '1 / 9 / 6 / 13', 1.8, 'Drei Gänge', 'von Rudi'),
         ('rudi', '7 / 1 / 11 / 5', 1.4, '', ''), ('momo', '6 / 9 / 10 / 11', -1.6, '', ''), ('g1', '6 / 11 / 10 / 13', 2.2, 'Fünf Drinks', 'Momos Signature Drinks'),
         ('glaeser', '11 / 1 / 15 / 3', -1.2, '', ''), ('hok1', '11 / 3 / 15 / 5', 1.6, '', ''), ('klaeren', '10 / 9 / 15 / 13', -1.8, 'Tasting und Schulung', 'Fatwashing, Milkwashing, Klärung mit Enzymen')]
F.append(('Salonhängung', '<div class="mx04 mx-voll"><div class="mx04-wand">%s<div class="mx04-titel">%s</div><div class="mx04-karte auf" style="--r:.6deg">%s</div><p class="mx04-schild">%s</p></div></div>' % (
    ''.join('<figure class="mx04-r auf" style="grid-area:%s;--r:%sdeg;--i:%d"><div class="mx04-b">%s</div>%s</figure>' % (
        ga, r, i % 5, bild(k, 1000), ('<figcaption><b>%s</b><span>%s</span></figcaption>' % (E(n), E(u))) if n else '') for i, (k, ga, r, n, u) in enumerate(SALON)),
    zl(TITEL, 'h2', 'mw-h'), karte(), E(FUSS))))

# 5 Der runde Tisch: Teller und Gläser als Runde um einen Platzteller mit der Marke; die Runde dreht sich beim Scrollen
RUND = [('r02', 'teller'), ('g1', 'glas'), ('lauch', 'teller'), ('d2', 'glas'), ('r09', 'teller'), ('g4', 'glas'), ('r01', 'teller'), ('glas', 'glas')]
F.append(('Der runde Tisch', '<div class="mx05"><div class="mx05-tisch"><div class="mx05-ring" data-mx-dreh>%s</div>'
          '<div class="mx05-mitte"><div class="mx05-marke">%s</div><p>%s</p></div></div><div class="mx05-r">%s%s%s</div></div>' % (
              ''.join('<figure class="mx05-p %s" style="--a:%ddeg">%s</figure>' % (c, i * 45, bild(k, 640)) for i, (k, c) in enumerate(RUND)),
              marke('wm'), MIT, titel(), teile(), fuss())))

# 6 Untertitel: Breitbild wie im Kino, der Abend in vier Szenen, darunter der Satz als Untertitel; läuft von selbst, Kapitel antippbar
UT = [('anstossen', '50% 34%', 'Zum Ankommen gibt es einen Aperitif.'), ('lauch', '50% 50%', 'Rudi kocht drei Gänge, zuletzt Aubergine, Kokos, Limette und Sesam.'),
      ('d3', '50% 38%', 'Momo stellt zu jedem Gang einen eigenen Drink dazu.'), ('schaum', '50% 42%', 'Im Tasting zeigt er Fatwashing, Milkwashing und die Klärung mit Enzymen.')]
F.append(('Untertitel', '<div class="mx06" data-mx-tabs data-mx-auto="5600"><div class="mx06-kopf">%s</div><div class="mx06-kino mx-voll"><div class="mx06-leinwand">%s</div></div>'
          '<div class="mx06-unter">%s</div><div class="mx06-kap">%s</div></div>' % (
              titel('reihe'),
              ''.join('<figure class="mx06-b%s" data-a="%d">%s</figure>' % (' an' if i == 0 else '', i, bild(k, 2400, pos=p)) for i, (k, p, _s) in enumerate(UT)),
              ''.join('<p class="mx06-ut%s" data-a="%d">%s</p>' % (' an' if i == 0 else '', i, E(s)) for i, (_k, _p, s) in enumerate(UT)),
              ''.join('<button type="button" class="%s" data-q="%d">%s</button>' % ('an' if i == 0 else '', i, E(t[0])) for i, t in enumerate(T)))))

# 7 Gold auf Schwarz: eine schwarze Lederkarte mit Goldprägung, die sich beim Ankommen aufschlägt; links das Foto, rechts das Menü in Gold
F.append(('Gold auf Schwarz', '<div class="mx07">%s<div class="mx07-buch"><div class="mx07-seite l"></div>'
          '<div class="mx07-seite r"><div class="mx07-gold"><div class="mx07-marke">%s</div><p class="mx07-mit">%s</p>%s<p class="mx07-fuss">%s</p></div></div>'
          '<div class="mx07-deckel auf"><div class="mx07-vorn"><div class="mx07-marke">%s</div><p class="mx07-mit">Der Abend</p></div><div class="mx07-hinten">%s</div></div></div>'
          '<div class="mx07-band">%s</div></div>' % (
              titel('mw-mi'), marke('wm'), MIT,
              ''.join('<div class="mx07-g"><h3>%s</h3><p>%s</p></div>' % (E(t[0]), unter(t)) for t in T), E(FUSS), marke('wm'), bild('anstossen', 1600, pos='50% 40%'),
              ''.join('<figure class="auf" style="--i:%d">%s</figure>' % (i, bild(k, 1000)) for i, k in enumerate(['beete', 'g2', 'kerze1', 'tarte'])))))

# 8 Die Wand des Abends: ein grosses Bild vom Anstossen, das langsam näher kommt, drumherum der Abend Kante an Kante; Titel und Karte als Felder in der Wand
WAND = [('hero', 'anstossen', '1 / 1 / 6 / 8'), ('titel', '', '1 / 8 / 4 / 13'), ('b', 'momo', '4 / 8 / 7 / 10'), ('b', 'g1', '4 / 10 / 7 / 13'),
        ('b', 'beete', '6 / 1 / 9 / 4'), ('b', 'rudi', '6 / 4 / 9 / 8'), ('karte', '', '7 / 8 / 10 / 13'), ('b', 'klaeren', '9 / 1 / 12 / 5'),
        ('b', 'hok1', '9 / 5 / 12 / 8'), ('b', 'g4', '10 / 8 / 12 / 10'), ('b', 'tarte', '10 / 10 / 12 / 13')]


def wandfeld(a, k, ga):
    if a == 'hero':
        return '<figure class="mx08-f hero" style="grid-area:%s" data-mx-zoom>%s</figure>' % (ga, bild(k, 2400, pos='50% 38%'))
    if a == 'titel':
        return '<div class="mx08-f titel" style="grid-area:%s">%s</div>' % (ga, titel())
    if a == 'karte':
        return '<div class="mx08-f papier" style="grid-area:%s"><p class="mw-mit">%s</p>%s</div>' % (ga, MIT, teile('mx08-teile'))
    return '<figure class="mx08-f" style="grid-area:%s">%s</figure>' % (ga, bild(k, 1000))


F.append(('Die Wand des Abends', '<div class="mx08"><div class="mx08-wand">%s</div>%s</div>' % (''.join(wandfeld(*w) for w in WAND), fuss())))

# 9 Gegenläufig: links Rudis Küche, rechts Momos Bar, die beiden Bildsäulen laufen beim Scrollen gegeneinander; in der Mitte der Text
KUE = ['rudi', 'anrichten', 'beete', 'pass3', 'r09', 'lauch', 'roq1']
BAR = ['momo', 'g1', 'd3', 'g2', 'schaum', 'klaeren', 'g4']
F.append(('Gegenläufig', '<div class="mx09" data-mx-gegen><div class="mx09-sp l"><div class="mx09-lauf">%s</div><p class="mx09-et">Rudis Küche</p></div>'
          '<div class="mx09-mitte">%s%s%s</div><div class="mx09-sp r"><div class="mx09-lauf">%s</div><p class="mx09-et">Momos Bar</p></div></div>' % (
              ''.join('<figure>%s</figure>' % bild(k, 640) for k in KUE), titel('mw-mi'), teile(), fuss(),
              ''.join('<figure>%s</figure>' % bild(k, 640) for k in BAR))))

# 10 Laufband: oben ziehen die Teller nach links, unten die Drinks nach rechts, dazwischen der Titel in einer Zeile
TEL = ['r02', 'beete', 'lauch', 'tarte', 'r09', 'hok1', 'roq1', 'baiser', 'r07', 'r01']
GLA = ['g1', 'glaeser', 'd2', 'g4', 'schaum', 'g2', 'coupe', 'd1', 'g3', 'glas']
F.append(('Laufband', '<div class="mx10"><div class="mx10-band mx-voll" data-mx-lauf="-1"><div class="mx10-spur">%s</div></div>'
          '<h2 class="mx10-h zl auf" aria-label="Was auf den Tisch kommt."><span class="z"><span style="--i:0">Was auf den Tisch kommt.</span></span></h2>'
          '<div class="mx10-band mx-voll" data-mx-lauf="1"><div class="mx10-spur">%s</div></div>'
          '<div class="mx10-unten"><div><p class="sw auf">%s</p>%s</div>%s</div></div>' % (
              ''.join('<figure>%s</figure>' % bild(k, 640) for k in TEL), ''.join('<figure>%s</figure>' % bild(k, 640) for k in GLA), SATZ, fuss(), teile())))

# 11 Der Bogen: ein schmaler Bogen im Dunkeln, durch den man die gedeckte Tafel sieht; beim Scrollen öffnet er sich, bis man drin sitzt
F.append(('Der Bogen', '<div class="mx11 mx-voll" data-mx-bogen><div class="mx11-kleb"><figure class="mx11-bild">%s</figure><span class="mx11-tor"></span>'
          '<div class="mx11-t">%s</div></div></div><div class="mx11-unten">%s</div><div class="mx11-satz"><p class="sw auf">%s</p>%s</div>' % (
              bild('tafelleer', 1600, pos='50% 50%'), zl(TITEL, 'h2', 'mw-h'),
              ''.join('<figure class="mx11-f auf" style="--i:%d"><div class="mx11-b">%s</div><figcaption><h3 class="mx-n">%s</h3><p class="mx-u">%s</p></figcaption></figure>' % (
                  i, bild(k, 1000), E(t[0]), unter(t)) for i, (t, k) in enumerate(zip(T, ['glaeser', 'r09', 'g1', 'klaeren']))),
              SATZ, fuss())))

# 12 Mit der Kerze: die Tafel liegt im Dunkeln, ein Lichtkegel folgt der Maus (am Handy wandert er) und findet die vier Teile des Abends
KERZE = [(T[0], '7%', '9%'), (T[1], '6%', '70%'), (T[2], '56%', '15%'), (T[3], '50%', '77%')]
F.append(('Mit der Kerze', '<div class="mx12"><div class="mx12-l">%s<p class="mx12-tipp">Mit der Kerze über den Tisch fahren.</p>%s</div>'
          '<div class="mx12-buehne" data-mx-kerze>%s%s<div class="mx12-dunkel"></div></div></div>' % (
              titel(), fuss(), bild('t01', 1600, pos='50% 50%'),
              ''.join('<div class="mx12-et" style="left:%s;top:%s"><h3 class="mx-n">%s</h3><p class="mx-u">%s</p></div>' % (x, y, E(t[0]), unter(t)) for t, x, y in KERZE))))

# 13 Titelseite: der Abend als Titelseite eines Magazins, daneben die aufgeschlagene Doppelseite mit Bildern und Zitat
F.append(('Titelseite', '<div class="mx13"><figure class="mx13-cover auf">%s<div class="mx13-kopf"><div class="mx13-marke">%s</div><p>%s</p></div>'
          '<div class="mx13-zeilen"><p class="mx13-kl">Diesmal am Tisch</p>%s</div><p class="mx13-ort">Walk on the Wild Side · Linden</p></figure>'
          '<div class="mx13-heft"><div class="mx13-text">%s<blockquote class="mx13-zitat">«%s»</blockquote></div>'
          '<div class="mx13-bilder"><figure class="a">%s<figcaption>Rudi am Tisch</figcaption></figure><figure class="b">%s<figcaption>Rote Bete mit Schaum</figcaption></figure>'
          '<figure class="c">%s<figcaption>Klärung durch den Filter</figcaption></figure></div></div></div>' % (
              bild('g1', 1600, pos='50% 62%'), marke('wm'), MIT,
              ''.join('<p class="mx13-z"><b>%s</b> %s</p>' % (a, b) for a, b in [('Ein Aperitif', 'zum Ankommen'), ('Drei Gänge', 'von Rudi'), ('Fünf Drinks', 'von Momo'), ('Fatwashing, Milkwashing, Enzyme', 'im Tasting')]),
              titel(), E(FUSS), bild('rudi', 1000), bild('beete', 1000), bild('klaeren', 1000))))

# 14 Bögen und Teller: drei Gänge als runde Teller, fünf Drinks als hohe Bögen, Aperitif und Tasting als Medaillons
F.append(('Bögen und Teller', '<div class="mx14"><div class="mx14-oben">%s<div class="mx14-gaenge"><div class="mx14-teller">%s</div>%s</div></div>'
          '<div class="mx14-boegen">%s</div>%s<div class="mx14-unten">%s</div></div>' % (
              titel(), ''.join('<figure class="auf" style="--i:%d">%s</figure>' % (i, bild(k, 1000)) for i, k in enumerate(['r02', 'roq1', 'r09'])), teil(T[1], 'mx-teil mx14-cap'),
              ''.join('<figure class="mx14-bo auf" style="--i:%d">%s</figure>' % (i, bild(k, 1000)) for i, k in enumerate(['g1', 'g2', 'g4', 'd2', 'glas'])),
              teil(T[2], 'mx-teil mx14-cap mi'),
              ''.join('<div class="mx14-med"><figure class="%s">%s</figure>%s</div>' % (c, bild(k, 640), teil(t)) for t, k, c in [(T[0], 'glaeser', 'rund'), (T[3], 'klaeren', 'bogen')]) + fuss())))

# 15 Die lange Tafel: die Seite hält an und der Abend zieht seitwärts vorbei, Gang für Gang, Glas für Glas, wie an einer langen Tafel entlang
TAFEL = [('kap', 0), ('b', 'glaeser', 'h'), ('b', 'toast', 'h'), ('kap', 1), ('b', 'beete', 'h'), ('b', 'r09', 'h'), ('b', 'lauch', 'q'), ('b', 'roq1', 'h'),
         ('kap', 2), ('b', 'g1', 'h'), ('b', 'd3', 'h'), ('b', 'g4', 'h'), ('b', 'g2', 'h'), ('kap', 3), ('b', 'klaeren', 'h'), ('b', 'schaum', 'h'), ('b', 'kerze1', 'h')]


def tafelteil(x):
    if x[0] == 'kap':
        t = T[x[1]]
        return '<div class="mx15-kap"><h3>%s</h3><p class="mx-u">%s</p></div>' % (E(t[0]), unter(t))
    return '<figure class="mx15-f %s">%s</figure>' % (x[2], bild(x[1], 1000))


F.append(('Die lange Tafel', '<div class="mx15 mx-voll" data-mx-quer><div class="mx15-kleb"><div class="mx15-spur"><div class="mx15-start">%s</div>%s'
          '<div class="mx15-ende"><p class="mx15-fuss">%s</p></div></div></div></div>' % (titel(), ''.join(tafelteil(x) for x in TAFEL), E(FUSS))))

# 16 Die Namen tragen Bilder: vier Namen gross wie Plakatschrift; wer darüberfährt, dem folgt das Foto dazu
S16 = [(T[0], 'toast'), (T[1], 'r09'), (T[2], 'g1'), (T[3], 'klaeren')]
F.append(('Die Namen tragen Bilder', '<div class="mx16" data-mx-folge><div class="mx16-kopf">%s</div><div class="mx16-liste">%s</div><div class="mx16-schwebe">%s</div>%s</div>' % (
    titel('reihe'),
    ''.join('<div class="mx16-z" data-i="%d"><h3>%s</h3><p class="mx-u">%s</p><figure class="mx16-mobil">%s</figure></div>' % (i, E(t[0]), unter(t), bild(k, 1000)) for i, (t, k) in enumerate(S16)),
    ''.join('<figure data-i="%d">%s</figure>' % (i, bild(k, 1000)) for i, (_t, k) in enumerate(S16)), fuss())))

# 17 Triptychon: drei Bogentafeln wie ein Altarbild, Rudi und Momo als Flügel, die sich beim Ankommen öffnen; darunter die Predella mit den vier Teilen
F.append(('Triptychon', '<div class="mx17">%s<div class="mx17-altar"><figure class="mx17-fl l auf">%s<figcaption>Rudi · Küche</figcaption></figure>'
          '<figure class="mx17-mitte">%s</figure><figure class="mx17-fl r auf">%s<figcaption>Momo · Bar</figcaption></figure></div>'
          '<div class="mx17-predella">%s</div>%s</div>' % (
              titel('mw-mi'), bild('rudi', 1000), bild('anstossen', 1600, pos='50% 40%'), bild('momo', 1000, pos='50% 30%'),
              ''.join('<div class="mx17-p"><figure>%s</figure><h3>%s</h3><p>%s</p></div>' % (bild(k, 640), E(t[0]), unter(t)) for t, k in zip(T, ['glaeser', 'beete', 'g1', 'klaeren'])),
              fuss())))

# 18 Die Kamera fährt: ein Foto vom gedeckten Tisch, jeder Teil des Abends fährt an seine Stelle im Bild heran
KAM = [('Der ganze Tisch', 'so sieht es aus, wenn du dich setzt', '.5,.5,1'), (T[0][0], unter(T[0]), '.18,.36,2.6'), (T[1][0], unter(T[1]), '.68,.66,2.1'),
       (T[2][0], unter(T[2]), '.5,.37,2.4'), (T[3][0], unter(T[3]), '.63,.5,2.8')]
F.append(('Die Kamera fährt', '<div class="mx18" data-mx-kamera><div class="mx18-l">%s<div class="mx18-k">%s</div>%s</div><figure class="mx18-bild">%s</figure></div>' % (
    titel(),
    ''.join('<button type="button" class="%s" data-z="%s"><b>%s</b><span>%s</span></button>' % ('an' if i == 0 else '', z, E(n), u if i else E(u)) for i, (n, u, z) in enumerate(KAM)),
    fuss(), bild('kartglas', 1600))))

# 19 Die Einladung: vor der dunklen Tafel ein Umschlag in Pflaume und Gold, beim Scrollen zieht die Karte des Abends heraus
F.append(('Die Einladung', '<div class="mx19 mx-voll" data-mx-brief><figure class="mx19-grund">%s</figure><div class="mx19-in">%s'
          '<div class="mx19-buehne"><figure class="mx19-foto l auf">%s</figure><div class="mx19-brief"><span class="mx19-hinten"></span>'
          '<div class="mx19-karte">%s</div><span class="mx19-vorn"><i>%s</i></span></div><figure class="mx19-foto r auf">%s</figure></div></div></div>' % (
              bild('tafelleer', 1600), titel('mw-mi'), bild('glaeser', 1000), karte(), MIT, bild('g1', 1000))))

# 20 Lamellen: ein grosses Bild aus senkrechten Lamellen; wer einen Teil wählt, dem drehen sich die Lamellen Stück für Stück zum nächsten Bild
LAM = [('toast', T[0]), ('r09', T[1]), ('g1', T[2]), ('klaeren', T[3])]
N20 = 9
F.append(('Lamellen', '<div class="mx20" data-mx-lamellen data-bilder=\'%s\'><div class="mx20-l">%s<div class="mx20-k">%s</div>%s</div>'
          '<div class="mx20-buehne" style="--n:%d">%s</div></div>' % (
              json.dumps([url(k, 1600) for k, _t in LAM]), titel(),
              ''.join('<button type="button" class="%s" data-l="%d"><b>%s</b><span>%s</span></button>' % ('an' if i == 0 else '', i, E(t[0]), unter(t)) for i, (_k, t) in enumerate(LAM)),
              fuss(), N20,
              ''.join('<div class="mx20-s" style="--i:%d;--x:%.4f%%"><i class="v" style="background-image:url(%s)"></i><i class="h"></i></div>' % (
                  i, i * 100 / (N20 - 1), url('toast', 1600)) for i in range(N20)))))


def main():
    seite = open(os.path.join(HIER, 'abend.html')).read()
    m = re.search(r'(<section class="menuekarte"[^>]*>)(\s*<div class="mk-raster">.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Was auf den Tisch kommt» in abend.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="menuekarte"', 'id="tisch" data-name="Was auf den Tisch kommt" class="menuekarte wahl"', 1)
    teile_ = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile_ += ['<div class="wv mkw mxw mx-f%02d" data-n="%d" hidden><div class="mw-in">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Was auf den Tisch kommt</b><span data-nr></span></div>' + ''.join(teile_) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Karte auf Foto, Text und zwei Bilder'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('menue-wahl.css', 'menue-wahl-2.css', 'menue-wahl-2.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["tisch"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/menue-wahl-2.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Was auf den Tisch kommt wählen (2) · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/menue-wahl.css?v=%s">\n'
                          '<link rel="stylesheet" href="assets/menue-wahl-2.css?v=%s">\n</head>' % (VERSION, v, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'menue-wahl-2.html'), 'w').write(seite)
    print('Seite menue-wahl-2.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
