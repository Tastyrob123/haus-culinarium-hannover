#!/usr/bin/env python3
"""Culinarium Hannover · «Wann und wie viel» zweite Runde, 12 neue Fassungen, direkt in der echten Seite, 27.10.2026.
Robert: die erste Runde (termine-wahl.html, Ticket, Plakat, Uhr, Kalender, Anzeigetafel …) gefällt nicht, «bitte gib mir weitere».
Diesmal keine Gegenstände, sondern ruhige Anordnungen: Typografie, Bildschnitt, Raster, Scroll. Keine Säulen (stehen schon bei «Was auf den Tisch kommt»).
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Nur belegte Fakten: freitags ab 19:00, samstags ab 17:00, 14 Plätze, zuletzt 89 € am 25. und 26.09.2026 ausgebucht, Storno wörtlich (DbYnkdkjrNy, DVjkofijp6R).
Baut termine-wahl-2.html (Leiste unten, Pfeiltasten, ?termine=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/termine_wahl2.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, zl, marke

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json')))

TITEL = ['Wann und', 'wie viel.']
STORNO = '„Da die Plätze begrenzt sind, bitten wir um Verständnis, dass Tickets nicht rückerstattet werden können.“'
SATZ = ('Culinarium findet an einzelnen Wochenenden statt, der Preis gilt für den ganzen Abend, Essen und Drinks. '
        'Der nächste Termin steht noch nicht fest. Tickets gibt es bisher nur im Vorverkauf. ' + STORNO)
ZUL = 'zuletzt, 25. und 26. September 2026, ausgebucht'
EUR = '89&#160;€'


def bild(k, w=1000, cls='', pos='50% 50%', alt=None):
    st = [s for s in META[k]['stufen'] if s <= w] or META[k]['stufen'][:1]
    return '<img class="%s" src="assets/bild/%s-%d.webp?v=%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        cls, k, st[-1], VERSION, E(alt if alt is not None else bau.BILD[k][2]), pos)


def satz(cls='', i=2):
    return '<p class="sw auf tx-satz %s" style="--i:%d">%s</p>' % (cls, i, SATZ)


def titel(cls=''):
    return zl(TITEL, 'h2', ('tx-h ' + cls).strip())


F = []  # (Name, Inhalt)

# 1 Die Bildlegende: ein grosses Foto wie im Museum, die Angaben stehen klein daneben wie auf dem Schild an der Wand; das Foto zieht beim Scrollen langsam auf
F.append(('Die Bildlegende', '<div class="tx01"><figure class="tx01-f" data-tx-zoom>%s</figure><div class="tx01-r">%s'
          '<div class="tx01-schild auf" style="--i:1"><p class="tx01-tage"><span>Freitags ab <b>19:00</b></span><span>Samstags ab <b>17:00</b></span></p>'
          '<p class="tx01-z">14 Plätze an einer Tafel</p><p class="tx01-z">%s für den ganzen Abend, Essen und Drinks</p><p class="tx01-z leise">%s</p></div>%s</div></div>' % (
              bild('anstossen', 1600, pos='50% 45%'), titel(), EUR, ZUL, satz())))

# 2 Das Bild bleibt stehen: links die Tafel, angeheftet; rechts ziehen die vier Angaben riesig untereinander vorbei
ZAHLEN2 = [('19:00', 'freitags ab'), ('17:00', 'samstags ab'), ('14', 'Plätze an einer Tafel'), (EUR, ZUL)]
F.append(('Das Bild bleibt stehen', '<div class="tx02"><div class="tx02-l"><figure class="tx02-f">%s</figure></div><div class="tx02-r">%s%s<div class="tx02-liste">%s</div></div></div>' % (
    bild('kerze2', 1600, pos='50% 55%'), titel(), satz(),
    ''.join('<div class="tx02-z auf" style="--i:%d"><b>%s</b><span>%s</span></div>' % (n, z, t) for n, (z, t) in enumerate(ZAHLEN2)))))

# 3 Vier Bildschirme: die Bühne steht still, beim Scrollen tauscht sie Satz und Foto, ein Bildschirm je Angabe
BUEHNE3 = [('Freitags', 'ab 19:00.', 'anstossen', '50% 62%'), ('Samstags', 'ab 17:00.', 'toast', '50% 40%'), ('Vierzehn Plätze', 'an einer Tafel.', 'tafelleer', '50% 30%'), ('89&#160;€', 'für den ganzen Abend.', 'kartglas', '50% 55%')]
F.append(('Vier Bildschirme', '<div class="tx03" data-tx-buehne style="--n:%d"><div class="tx03-steh"><div class="tx03-bilder">%s</div>'
          '<div class="tx03-kopf"><p class="tx-kick">Wann und wie viel</p><p class="tx03-lauf"><i></i></p></div><div class="tx03-saetze">%s</div>'
          '<p class="tx03-fuss">%s</p></div></div><div class="tx03-nach">%s</div>' % (
              len(BUEHNE3),
              ''.join('<figure class="tx03-f%s" data-s="%d">%s</figure>' % (' an' if n == 0 else '', n, bild(k, 1600, pos=po)) for n, (_a, _b, k, po) in enumerate(BUEHNE3)),
              ''.join('<p class="tx03-s%s" data-s="%d"><b>%s</b> %s</p>' % (' an' if n == 0 else '', n, a, b) for n, (a, b, _k, _p) in enumerate(BUEHNE3)),
              'Essen und Drinks, %s' % ZUL, satz())))

# 4 Bilder in der Zeile: vier Zeilen über die ganze Breite, in jeder sitzt ein kleines Foto mitten im Satz
def inl(k, pos='50% 50%'):
    return '<span class="tx04-b">%s</span>' % bild(k, 640, pos=pos, alt='')


ZEILEN4 = ['Freitags %s ab 19:00' % inl('kerze2', '50% 40%'), 'samstags ab 17:00 %s' % inl('toast', '50% 30%'),
           '%s 14 an einer Tafel' % inl('tafelleer', '50% 60%'), '89&#160;€ %s der ganze Abend' % inl('kartglas', '50% 60%')]
F.append(('Bilder in der Zeile', '<div class="tx04"><p class="tx-kick">Wann und wie viel</p><p class="tx04-zeilen zl auf" aria-label="Freitags ab 19:00, samstags ab 17:00, 14 an einer Tafel, 89 Euro der ganze Abend">%s</p>'
          '<div class="tx04-fuss"><p class="tx04-zul">Essen und Drinks inbegriffen, %s.</p>%s</div></div>' % (
              ''.join('<span class="z"><span style="--i:%d">%s</span></span>' % (n, z) for n, z in enumerate(ZEILEN4)), ZUL, satz())))

# 5 Die Woche: sieben Spalten, Montag bis Donnerstag und Sonntag nur ein Strich, Freitag und Samstag breit, mit Foto und Uhrzeit
WOCHE = [('Mo', ''), ('Di', ''), ('Mi', ''), ('Do', ''), ('Fr', ('19:00', 'kerze2')), ('Sa', ('17:00', 'toast')), ('So', '')]
F.append(('Die Woche', '<div class="tx05"><div class="tx05-kopf">%s%s</div><div class="tx05-woche">%s</div>'
          '<div class="tx05-fuss"><p><b>14</b> Plätze an einer Tafel</p><p><b>%s</b> Essen und Drinks, %s</p></div></div>' % (
              titel(), satz(),
              ''.join(('<div class="tx05-tag ab auf eigen" style="--i:%d"><figure>%s</figure><p><span>%s</span><b>ab %s</b></p></div>' % (n, bild(v[1], 1000), {'Fr': 'Freitag', 'Sa': 'Samstag'}[t], v[0]))
                      if v else '<div class="tx05-tag"><span>%s</span></div>' % t for n, (t, v) in enumerate(WOCHE)),
              EUR, ZUL)))

# 6 Die Einladung: mittig gesetzt wie eine Einladungskarte, die Zahlen ausgeschrieben; zwei Fotos rahmen links und rechts und wandern gegenläufig
F.append(('Die Einladung', '<div class="tx06"><figure class="tx06-f l" data-tx-drift="-1">%s</figure><figure class="tx06-f r" data-tx-drift="1">%s</figure>'
          '<div class="tx06-mitte"><div class="tx06-marke">%s</div><p class="tx-kick">Wann und wie viel</p>'
          '<p class="tx06-text zl auf" aria-label="Freitags ab sieben, samstags ab fünf, an einer Tafel für vierzehn, für neunundachtzig Euro, Essen und Drinks.">'
          '<span class="z"><span style="--i:0">freitags ab sieben,</span></span><span class="z"><span style="--i:1">samstags ab fünf,</span></span>'
          '<span class="z"><span style="--i:2">an einer Tafel für vierzehn,</span></span><span class="z"><span style="--i:3">für neunundachtzig Euro,</span></span>'
          '<span class="z"><span style="--i:4"><em>Essen und Drinks.</em></span></span></p>'
          '<p class="tx06-ziffern">Fr 19:00 · Sa 17:00 · 14 Plätze · %s</p><p class="tx06-zul">%s</p>%s</div></div>' % (
              bild('kerze3', 1000, pos='60% 50%'), bild('glaeser', 1000, pos='50% 50%'), marke('wm'), EUR, ZUL, satz('tx06-s'))))

# 7 Die Leinwand: das Foto im Kinoformat über die ganze Breite, die Kamera fährt beim Scrollen die Tafel entlang; darunter die Angaben als Untertitel
F.append(('Die Leinwand', '<div class="tx07"><div class="tx07-oben"><p class="tx-kick">Culinarium · Walk on the Wild Side · Linden</p><p class="tx-kick">Freitag, Samstag</p></div>'
          '<figure class="tx07-f" data-tx-fahrt>%s</figure>'
          '<p class="tx07-ut zl auf" aria-label="Freitags ab 19:00, samstags ab 17:00. Vierzehn Plätze an einer Tafel, 89 Euro für den ganzen Abend.">'
          '<span class="z"><span style="--i:0">Freitags ab 19:00, samstags ab 17:00.</span></span><span class="z"><span style="--i:1">Vierzehn Plätze an einer Tafel, %s für den ganzen Abend.</span></span></p>'
          '<div class="tx07-unten">%s<div><p class="tx07-zul">Essen und Drinks inbegriffen, %s.</p>%s</div></div></div>' % (
              bild('t08', 1600, pos='50% 50%'), EUR, titel(), ZUL, satz())))

# 8 Der Stapel: vier Karten, jede bleibt oben hängen, die nächste schiebt sich darüber, bis alle vier aufeinander liegen
STAPEL = [('Freitag', '19:00', 'ab sieben Uhr abends', 'kerze2', 'hell'), ('Samstag', '17:00', 'zwei Stunden früher', 'toast', 'dunkel'),
          ('Plätze', '14', 'an einer langen Tafel', 'tafelleer', 'kerze'), ('Preis', EUR, 'Essen und Drinks, ' + ZUL, 'kartglas', 'hell')]
F.append(('Der Stapel', '<div class="tx08"><div class="tx08-kopf">%s%s</div><div class="tx08-stapel">%s</div></div>' % (
    titel(), satz(),
    ''.join('<div class="tx08-k %s" style="--i:%d"><figure>%s</figure><div class="tx08-t"><p class="tx08-was">%s</p><b>%s</b><p class="tx08-wie">%s</p></div></div>' % (
        ton, n, bild(k, 1000), was, z, wie) for n, (was, z, wie, k, ton) in enumerate(STAPEL)))))

# 9 Die lange Tafel: das Foto als langer, flacher Streifen wie die Tafel selbst; die Angaben hängen an feinen Strichen darüber und darunter
F.append(('Die lange Tafel', '<div class="tx09"><div class="tx09-kopf">%s%s</div><div class="tx09-zug auf eigen">'
          '<div class="tx09-reihe o"><p class="tx09-a" style="--i:0"><b>19:00</b><span>freitags ab</span></p><p class="tx09-a" style="--i:2"><b>14</b><span>Plätze an einer Tafel</span></p></div>'
          '<figure class="tx09-f">%s</figure>'
          '<div class="tx09-reihe u"><p class="tx09-a" style="--i:1"><b>17:00</b><span>samstags ab</span></p><p class="tx09-a" style="--i:3"><b>%s</b><span>%s</span></p></div></div></div>' % (
              titel(), satz(), bild('tafelleer', 1600, pos='50% 28%'), EUR, ZUL)))

# 10 Drei Fragen: was der Gast wissen will, links leise gefragt, rechts gross beantwortet
FRAGEN = [('Wann?', 'Freitags ab 19:00,<br>samstags ab 17:00.'), ('Für wie viele?', 'Vierzehn,<br>an einer Tafel.'), ('Was kostet es?', 'Zuletzt %s,<br>Essen und Drinks.' % EUR)]
F.append(('Drei Fragen', '<div class="tx10"><div class="tx10-kopf"><div>%s%s</div><figure class="tx10-f">%s</figure></div><div class="tx10-liste">%s</div><p class="tx10-zul">%s.</p></div>' % (
    titel(), satz(), bild('kerze1', 1000, pos='50% 45%'),
    ''.join('<div class="tx10-p"><p class="tx10-q">%s</p><p class="tx10-a zl auf" aria-label="%s"><span class="z"><span style="--i:0">%s</span></span></p></div>' % (
        q, re.sub('<[^>]+>', ' ', a).replace('&#160;', ' '), a.replace('<br>', '</span></span><span class="z"><span style="--i:1">')) for q, a in FRAGEN),
    ZUL[0].upper() + ZUL[1:])))

# 11 Randnotizen: der Abschnitt als ruhiger Lesetext wie in einem Magazin, die Zahlen stehen gross am Rand neben ihrem Absatz
ABS11 = [('19:00', 'Culinarium findet an einzelnen Wochenenden statt. Freitags beginnt der Abend um sieben,'),
         ('17:00', 'samstags schon um fünf, zwei Stunden früher. Der nächste Termin steht noch nicht fest.'),
         ('14', 'Alle sitzen an einer langen Tafel, vierzehn Gäste, mehr Plätze gibt es nicht. Tickets gibt es bisher nur im Vorverkauf.'),
         (EUR, 'Der Preis gilt für den ganzen Abend, Essen und Drinks. Zuletzt waren es 89 Euro, am 25. und 26. September 2026 war ausgebucht.')]
F.append(('Randnotizen', '<div class="tx11"><div class="tx11-kopf">%s</div><div class="tx11-text">%s<blockquote class="tx11-zitat">%s</blockquote></div>'
          '<figure class="tx11-f">%s</figure></div>' % (
              titel(), ''.join('<div class="tx11-abs auf" style="--i:%d"><b>%s</b><p>%s</p></div>' % (n, z, t) for n, (z, t) in enumerate(ABS11)),
              STORNO, bild('karte', 1000, pos='50% 50%'))))

# 12 Samstag noch hell: zwei Hälften über die ganze Breite, Samstag beginnt um fünf bei Tageslicht auf hellem Grund, Freitag um sieben im Kerzenlicht
F.append(('Samstag noch hell', '<div class="tx12"><div class="tx12-paar"><div class="tx12-h sa auf eigen"><figure>%s</figure><p><span>Samstags ab</span><b>17:00</b></p></div>'
          '<div class="tx12-h fr auf eigen"><figure>%s</figure><p><span>Freitags ab</span><b>19:00</b></p></div></div>'
          '<div class="tx12-fuss">%s<div><p class="tx12-zeile"><span><b>14</b> Plätze an einer Tafel</span><span><b>%s</b> Essen und Drinks, %s</span></p>%s</div></div></div>' % (
              bild('t14', 1000, pos='50% 40%'), bild('kerze2', 1000, pos='50% 50%'), titel(), EUR, ZUL, satz())))


def main():
    seite = open(os.path.join(HIER, 'abend.html')).read()
    m = re.search(r'(<section class="termine"[^>]*>)(\s*<div class="te-buehne">.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Wann und wie viel» in abend.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="termine"', 'id="termine" data-name="Wann und wie viel" class="termine wahl"', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv tex tx-f%02d" data-n="%d" hidden><div class="tx-in">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Wann und wie viel</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Tafelfoto, vier Zahlen in einer Reihe'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('termine-wahl-2.css', 'termine-wahl-2.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["termine"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/termine-wahl-2.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Wann und wie viel wählen, Runde 2 · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/termine-wahl-2.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'termine-wahl-2.html'), 'w').write(seite)
    print('Seite termine-wahl-2.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
