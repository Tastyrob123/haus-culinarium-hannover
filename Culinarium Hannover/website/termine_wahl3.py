#!/usr/bin/env python3
"""Culinarium Hannover · «Wann und wie viel» dritte Runde, 8 Fassungen, direkt in der echten Seite, 27.10.2026.
Robert zur zweiten Runde: «alle scheiße. passt nicht zum stil der seite». Darum hier nur Bausteine, die die Seite schon hat:
Kopf wie «Was auf den Tisch kommt» (Titel und Textblock nebeneinander), Fotos mit Goldstrich und Bildzeile (Säulen),
Papierkarte mit Doppelrahmen, 14 Platz-Punkten und Preiszeile (Platz buchen), Tischkarte (Warteliste), Mittelfeld zwischen Bildern (Auftakt),
Knopf mit Knauf. Bewegung: das Hochschweben der Fotos der Seite, dazu Anstossen (Charakterblatt 7). Text nie mitten in eine Bildwand.
Nur belegte Fakten: freitags ab 19:00, samstags ab 17:00, 14 Plätze, zuletzt 89 € am 25. und 26.09.2026 ausgebucht, Storno wörtlich (DbYnkdkjrNy, DVjkofijp6R).
Baut termine-wahl-3.html (Leiste unten, Pfeiltasten, ?termine=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/termine_wahl3.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import zl, sw, foto, marke, knopf

HIER = bau.HIER
bau.META.update(json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json'))))  # sonst erst in bau.main()
VERSION = bau.VERSION

TITEL = ['Wann und', 'wie viel.']
STORNO = '„Da die Plätze begrenzt sind, bitten wir um Verständnis, dass Tickets nicht rückerstattet werden können.“'
TEXT = ('Culinarium findet an einzelnen Wochenenden statt, freitags ab 19:00 und samstags ab 17:00. '
        'Der Preis gilt für den ganzen Abend, Essen und Drinks. Der nächste Termin steht noch nicht fest.')
TICKETS = 'Tickets gibt es bisher nur im Vorverkauf. ' + STORNO
ZUL = 'Zuletzt am 25. und 26. September 2026, ausgebucht.'
EUR = '89,00 EUR'


def kopf(text=TEXT, cls=''):
    """Kopf wie «Was auf den Tisch kommt»: Titel und Textblock nebeneinander, unten bündig."""
    return '<div class="t3-kopf %s">%s%s</div>' % (cls, zl(TITEL, 'h2', 'gross'), sw(text, 'p', '', 1))


def punkte(cls=''):
    return '<div class="t3-punkte %s" aria-hidden="true">%s</div>' % (cls, ''.join('<i style="--i:%d"></i>' % n for n in range(14)))


def preis(label='Pro Person'):
    return '<p class="t3-preis"><span>%s</span><b>%s</b></p>' % (label, EUR)


def zeile(k, wert, rest=''):
    return '<p class="t3-zeile"><span>%s</span><b>%s</b>%s</p>' % (k, wert, ('<em>%s</em>' % rest) if rest else '')


def buchen():
    return knopf('Platz buchen', '#termine-buchen')


F = []  # (Name, Inhalt)

# 1 Vier Bilder, vier Zeilen: wie «Was auf den Tisch kommt», aber in einer geraden Reihe; jedes Foto trägt eine Angabe als Bildzeile
VIER = [('Freitags ab 19:00', 'Der Abend beginnt um sieben.', 'anstossen', '50% 55%'),
        ('Samstags ab 17:00', 'Zwei Stunden früher.', 't14', '50% 40%'),
        ('14 Plätze', 'An einer langen Tafel.', 'tafelleer', '50% 35%'),
        ('89,00 EUR', 'Pro Person, Essen und Drinks.', 'kartglas', '50% 55%')]
F.append(('Vier Bilder, vier Zeilen', '<div class="t3-in">%s<div class="t3a-reihe">%s</div><p class="t3-fuss">%s %s</p></div>' % (
    kopf(),
    ''.join('<div class="t3a-s">%s<div class="t3-bz"><h3>%s</h3><p>%s</p></div></div>' % (
        foto(k, 't3a-b', '(max-width:860px) 46vw, 22vw', pos=p, extra='style="--d:%.2fs"' % (n * .12)), h, t) for n, (h, t, k, p) in enumerate(VIER)),
    ZUL, TICKETS)))

# 2 Die Karte des Abends: ein Bildpaar und daneben die Papierkarte aus «Platz buchen», gross, mit allem, was der Gast wissen muss
F.append(('Die Karte des Abends', '<div class="t3-in"><div class="t3b">'
          '<div class="t3b-bilder">%s%s</div>'
          '<div class="t3b-rechts">%s%s'
          '<div class="t3-karte auf" style="--i:2"><p class="t3-kick">Ein Abend bei Culinarium</p>'
          '<div class="t3-tage"><p><b>Freitag</b><span>ab 19:00</span></p><p><b>Samstag</b><span>ab 17:00</span></p></div>'
          '%s<p class="t3-frei">14 Plätze an einer Tafel</p>%s<p class="t3-klein">%s</p>%s</div></div></div></div>' % (
              foto('kerze3', 't3b-f1', '(max-width:860px) 50vw, 26vw', pos='50% 50%'),
              foto('t14', 't3b-f2', '(max-width:860px) 50vw, 26vw', pos='50% 40%', extra='style="--d:.18s"'),
              zl(TITEL, 'h2', 'gross'), sw(TEXT, 'p', 't3b-text', 1), punkte(), preis(), ZUL, buchen())))

# 3 Das Paar: Freitag und Samstag als zwei Hochformate an einer Naht, sie stossen an; der Textblock steht geschlossen daneben
F.append(('Das Paar', '<div class="t3-in"><div class="t3c">'
          '<div class="t3c-paar"><div class="t3c-h">%s<div class="t3-bz"><h3>Freitag</h3><p>ab 19:00</p></div></div>'
          '<div class="t3c-h">%s<div class="t3-bz"><h3>Samstag</h3><p>ab 17:00</p></div></div></div>'
          '<div class="t3c-block">%s%s<div class="t3c-platz sw auf" style="--i:2">%s<p class="t3-frei">14 Plätze an einer Tafel</p>%s<p class="t3-klein">%s</p></div>%s</div>'
          '</div></div>' % (
              foto('anstossen', 't3c-f', '(max-width:860px) 50vw, 30vw', pos='50% 55%'),
              foto('t05', 't3c-f', '(max-width:860px) 50vw, 30vw', pos='50% 45%', extra='style="--d:.22s"'),
              zl(TITEL, 'h2', 'gross'), sw(TEXT, 'p', 't3c-text', 1), punkte(), preis(), ZUL, sw(TICKETS, 'p', 't3-klein t3c-storno', 3))))

# 4 Die Mitte: wie der Auftakt der Seite, ein dunkles Feld zwischen Bildern; links und rechts je zwei Fotos ohne Lücke
F.append(('Die Mitte', '<div class="t3d">'
          '<div class="t3d-seite">%s%s</div>'
          '<div class="t3d-mitte"><p class="t3-kick">Wann und wie viel</p>%s'
          '<div class="t3d-tage"><p><span>Freitags ab</span><b>19:00</b></p><p><span>Samstags ab</span><b>17:00</b></p></div>'
          '%s<p class="t3-frei">14 Plätze an einer Tafel</p>%s<p class="t3-klein">%s</p></div>'
          '<div class="t3d-seite">%s%s</div></div>' % (
              foto('t12', 't3d-b', '(max-width:860px) 50vw, 30vw', pos='50% 40%'), foto('t01', 't3d-b', '(max-width:860px) 50vw, 30vw', pos='50% 50%', extra='style="--d:.1s"'),
              zl(['Ein Abend,', 'eine Tafel.'], 'h2', 'gross'), punkte(), preis(), ZUL,
              foto('tafelleer', 't3d-b', '(max-width:860px) 50vw, 30vw', pos='50% 30%', extra='style="--d:.16s"'), foto('karte', 't3d-b', '(max-width:860px) 50vw, 30vw', pos='50% 55%', extra='style="--d:.24s"'))))

# 5 Die Tischkarte: das Tafelfoto wie heute, randlos; statt der vier grossen Zahlen liegt die Tischkarte der Seite darauf, daneben der Textblock
F.append(('Die Tischkarte', '<div class="t3e"><div class="t3e-bild">%s</div><div class="t3e-hof"></div><div class="t3e-in">'
          '<div class="tischkarte t3e-karte auf"><div class="tk-marke">%s</div><p class="tk-zeile">A UNiQUE EXPERiENCE BY MOMO X RUDI</p>'
          '<div class="t3e-tage"><p><span>Freitags ab</span><b>19:00</b></p><p><span>Samstags ab</span><b>17:00</b></p></div>'
          '<p class="tk-mehr"><span>14 Plätze an einer Tafel</span><span>%s pro Person</span></p><p class="tk-ort">%s</p></div>'
          '<div class="t3e-text">%s%s%s</div></div></div>' % (
              foto('tafelleer', '', '100vw', auf=False), marke('wm'), EUR, ZUL,
              zl(TITEL, 'h2', 'gross'), sw(TEXT, 'p', '', 1), sw(TICKETS, 'p', 't3-klein', 2))))

# 6 Vierzehn Plätze: drei Fotos als Band, darunter die vierzehn Punkte aus «Platz buchen» über die ganze Breite, darunter die Angaben als Bildzeilen
F.append(('Vierzehn Plätze', '<div class="t3-in">%s<div class="t3f-band">%s%s%s</div>%s'
          '<div class="t3f-zeilen sw auf" style="--i:2"><div class="t3-bz"><h3>Freitags ab 19:00</h3><p>Samstags ab 17:00</p></div>'
          '<div class="t3-bz"><h3>14 Plätze</h3><p>an einer Tafel, mehr gibt es nicht</p></div>'
          '<div class="t3-bz"><h3>89,00 EUR</h3><p>pro Person, Essen und Drinks</p></div>'
          '<div class="t3-bz"><h3>Ausgebucht</h3><p>zuletzt am 25. und 26. September 2026</p></div></div><p class="t3-fuss">%s</p></div>' % (
              kopf(), foto('t09', 't3f-b', '(max-width:860px) 100vw, 33vw', pos='50% 50%'),
              foto('tafelleer', 't3f-b', '(max-width:860px) 100vw, 33vw', pos='50% 32%', extra='style="--d:.12s"'),
              foto('t02', 't3f-b', '(max-width:860px) 100vw, 33vw', pos='50% 50%', extra='style="--d:.24s"'),
              punkte('breit staffel auf'), TICKETS)))

# 7 Bild und Liste: drei Fotos übereinander gelegt wie bei «Dein Platz an der Tafel», daneben der Block mit einer Liste wie die Preiszeile der Karten
F.append(('Bild und Liste', '<div class="t3-in"><div class="t3g">'
          '<div class="t3g-fotos">%s%s%s</div>'
          '<div class="t3g-block">%s%s<div class="t3g-liste sw auf" style="--i:2">%s%s%s%s%s</div>%s<div class="sw auf" style="--i:4">%s</div></div></div></div>' % (
              foto('anstossen', 'f1', '(max-width:860px) 60vw, 26vw', pos='50% 55%'), foto('tafelleer', 'f2', '(max-width:860px) 60vw, 24vw', pos='50% 32%', extra='style="--d:.12s"'),
              foto('kartglas', 'f3', '(max-width:860px) 60vw, 22vw', pos='50% 55%', extra='style="--d:.24s"'),
              zl(TITEL, 'h2', 'gross'), sw('Culinarium findet an einzelnen Wochenenden statt. Der nächste Termin steht noch nicht fest.', 'p', 't3g-text', 1),
              zeile('Freitags', 'ab 19:00'), zeile('Samstags', 'ab 17:00'), zeile('Plätze', '14', 'an einer Tafel'),
              zeile('Pro Person', EUR, 'Essen und Drinks'), zeile('Zuletzt', '25. + 26.09.2026', 'ausgebucht'),
              sw(TICKETS, 'p', 't3-klein', 3), buchen())))

# 8 Zwei Abende im Bild: zwei grosse Fotos nebeneinander, in jedes ist unten eine schmale Papierkarte gesteckt, Freitag und Samstag
F.append(('Zwei Abende im Bild', '<div class="t3-in">%s<div class="t3h">'
          '<div class="t3h-s">%s<div class="t3-karte klein auf" style="--i:1"><div class="t3-tage eins"><p><b>Freitag</b><span>ab 19:00</span></p></div>%s%s</div></div>'
          '<div class="t3h-s">%s<div class="t3-karte klein auf" style="--i:3"><div class="t3-tage eins"><p><b>Samstag</b><span>ab 17:00</span></p></div>%s%s</div></div>'
          '</div><p class="t3-fuss">14 Plätze an einer Tafel. %s %s</p></div>' % (
              kopf(), foto('kerze3', 't3h-b', '(max-width:860px) 100vw, 48vw', pos='50% 50%'), punkte(), preis(),
              foto('t14', 't3h-b', '(max-width:860px) 100vw, 48vw', pos='50% 40%', extra='style="--d:.2s"'), punkte(), preis(), ZUL, TICKETS)))


def main():
    seite = open(os.path.join(HIER, 'abend.html')).read()
    m = re.search(r'(<section class="termine"[^>]*>)(\s*<div class="te-buehne">.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Wann und wie viel» in abend.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="termine"', 'id="termine" data-name="Wann und wie viel" class="termine wahl"', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv t3w t3-f%02d" data-n="%d" hidden>%s</div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Wann und wie viel</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Tafelfoto, vier Zahlen in einer Reihe'] + [n for n, _x in F]
    v = VERSION + 'r%d' % os.path.getmtime(os.path.join(HIER, 'assets', 'termine-wahl-3.css'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["termine"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION)
    seite = seite.replace('<title>', '<title>Wann und wie viel wählen, Runde 3 · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/termine-wahl-3.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'termine-wahl-3.html'), 'w').write(seite)
    print('Seite termine-wahl-3.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
