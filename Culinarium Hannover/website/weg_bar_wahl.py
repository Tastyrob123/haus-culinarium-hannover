#!/usr/bin/env python3
"""Culinarium Hannover · Der Weg, die Bilderwand mit der Karte «Die Bar» in 20 Fassungen, direkt in der echten Weg-Seite, 27.10.2026.
Robert: «Kannst du mir bitte 20 visuelle Alternativen geben, wie man diesen Abschnitt darstellen könnte?» (Bildschirmfotos: vier Bilder um die Karte).
Titel «So findest du hin.», Satz und Angaben darüber bleiben Pixel für Pixel; getauscht wird nur die Wand darunter.
Keine Gegenstände aus weg-wahl.html und weg-wahl-2.html wieder (Bon, Tafel, Aufsteller, Tür, Leine, Postkarte, Vorhang, Klingel, Orgelpfeifen …):
hier geht es um Anordnung von Bild und Karte. Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll.
Baut weg-bar-wahl.html (Leiste unten, Pfeiltasten, ?weg=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/weg_bar_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION
from weg_wahl import bild, BAR, TEL, META

HIER = bau.HIER
F = []


def fo(k, cls='', sizes='(max-width:860px) 50vw, 30vw', pos=None, unter=''):
    return '<figure class="foto %s" style="--lq:url(%s)">%s%s</figure>' % (cls, META[k]['lq'], bild(k, sizes, pos), unter)


def tel():
    return '<a href="%s">%s</a>' % TEL


def gaenge():
    return ''.join('<div class="fk-gang"><p>%s %s</p></div>' % (t, z) for t, z in BAR)


def karte(cls=''):
    """Die Karte wie heute: Die Bar, Walk on the Wild Side, drei Abende, Telefon."""
    return ('<div class="fw-karte zb-k %s"><p class="fk-zitat">Die Bar</p><p class="fk-wer">Walk on the Wild Side</p>%s'
            '<p class="fk-fuss">%s</p></div>' % (cls, gaenge(), tel()))


def quer(cls=''):
    """Dieselbe Karte liegend: Name und Telefon links, die drei Abende rechts."""
    return ('<div class="fw-karte zb-kq %s"><div class="zb-kq-name"><p class="fk-zitat">Die Bar</p><p class="fk-wer">Walk on the Wild Side</p>'
            '<p class="fk-fuss">%s</p></div><div class="zb-kq-zeiten">%s</div></div>' % (cls, tel(), gaenge()))


def lauf(art, f, inner, cls=''):
    return '<div class="%s" data-wb="%s" data-f="%s">%s</div>' % (cls, art, f, inner)


WEG = ['ecke', 'schildnacht', 'fensterdraussen', 'barlicht', 'flur', 'schildnah']

# 1 Das Band: sechs Bilder Kante an Kante über die ganze Breite, die Karte hängt unten mittig hinein; das Band wandert quer
F.append(('Das Band', '<div class="zb zb01 auf"><div class="zb01-band zb-voll">%s</div><div class="zb01-k">%s</div></div>' % (
    lauf('quer', -90, ''.join(fo(k, '', '(max-width:860px) 40vw, 20vw') for k in WEG), 'zb01-lauf'), karte())))

# 2 Auf der Naht: vier hohe Bilder ohne Fuge, die Karte liegt genau auf der Naht in der Mitte und steigt beim Scrollen
F.append(('Auf der Naht', '<div class="zb zb02 auf"><div class="zb02-reihe">%s</div><div class="zb02-mitte">%s</div></div>' % (
    ''.join(fo(k, '', '(max-width:860px) 50vw, 25vw') for k in ('ecke', 'schildnacht', 'fensterdraussen', 'flur')),
    lauf('drift', -80, karte(), 'zb02-k'))))

# 3 Ein grosses Bild: das Schild bei Nacht über die ganze Breite, die Karte steht rechts im Bild; das Bild kommt näher
F.append(('Ein grosses Bild', '<div class="zb zb03 auf"><div class="zb03-bild">%s<div class="zb03-k">%s</div></div></div>' % (
    lauf('zoom', .12, fo('schildnacht', '', '100vw', '50% 34%'), 'zb03-zoom'), karte())))

# 4 Angedockt: die Fenster der Bar am Abend über die ganze Breite, die Karte dockt an der Unterkante an, links und rechts je ein Bild
F.append(('Angedockt', '<div class="zb zb04 auf"><div class="zb04-gross zb-voll">%s</div><div class="zb04-unten">%s<div class="zb04-k">%s</div>%s</div></div>' % (
    lauf('drift', 110, fo('fassade', '', '100vw', '50% 45%'), 'zb04-lauf'),
    fo('ecke', 'zb04-a', '(max-width:860px) 50vw, 33vw'), karte(), fo('flur', 'zb04-b', '(max-width:860px) 50vw, 33vw'))))

# 5 Näher ran: vier Bilder unten bündig, jedes grösser als das davor, von der Ecke bis zur offenen Tür; die Karte steht über den kleinen
F.append(('Näher ran', '<div class="zb zb05 auf"><div class="zb05-k">%s</div>%s</div>' % (
    karte(), ''.join('<div class="zb05-b zb05-%d">%s</div>' % (i, lauf('zoom', .1, fo(k, '', '(max-width:860px) 50vw, %dvw' % w), 'zb05-zoom') if i == 4 else fo(k, '', '(max-width:860px) 50vw, %dvw' % w))
                     for i, (k, w) in enumerate((('ecke', 16), ('schildnacht', 22), ('fensterdraussen', 28), ('flur', 38)), 1)))))

# 6 Das Querband: oben und unten eine Reihe Bilder, dazwischen die Karte als helles Band über die ganze Breite; die Reihen laufen gegeneinander
TAGE = ''.join('<div><p class="zb06-tag">%s</p><p class="zb06-zeit">%s</p></div>' % (t, z) for t, z in BAR)
F.append(('Das Querband', '<div class="zb zb06 auf zb-voll">%s<div class="zb06-band"><div><p class="zb06-name">Die Bar</p><p class="fk-wer">Walk on the Wild Side</p></div>'
          '<div class="zb06-tage">%s</div><p class="zb06-tel">%s</p></div>%s</div>' % (
              lauf('quer', -70, ''.join(fo(k, '', '(max-width:860px) 40vw, 20vw', '50% 40%') for k in ('ecke', 'schildnacht', 'fassade', 'barlicht', 'schildnah', 'fensterdraussen')), 'zb06-reihe'),
              TAGE, tel(),
              lauf('quer', 70, ''.join(fo(k, '', '(max-width:860px) 40vw, 20vw', '50% 45%') for k in ('flur', 'ws00', 'barneg', 'kerze3', 'bar', 'barnacht')), 'zb06-reihe'))))

# 7 Wörter und Bilder: die Öffnungszeiten riesig gesetzt, zwischen Tag und Uhrzeit steckt ein Bild in der Zeile
F.append(('Wörter und Bilder', '<div class="zb zb07 auf"><p class="fk-wer zb07-kopf">Die Bar · Walk on the Wild Side</p>%s<p class="zb07-tel">%s</p></div>' % (
    ''.join('<div class="zb07-z"><span>%s</span><span class="zb07-b">%s</span><span>%s</span></div>' % (
        t, lauf('zoom', .18, fo(k, '', '(max-width:860px) 40vw, 24vw', '50% 40%'), 'zb07-zoom'), z) for (t, z), k in zip(BAR, ('schildnacht', 'barlicht', 'flur'))), tel())))

# 8 Drei Abende, drei Bilder: je Abend ein grosses Bild, Tag und Uhrzeit stehen gross darauf; das mittlere steigt
F.append(('Drei Abende, drei Bilder', '<div class="zb zb08 auf"><div class="zb08-reihe">%s</div><div class="zb08-fuss"><p class="zb08-name">Die Bar</p>'
          '<p class="fk-wer">Walk on the Wild Side</p><p class="zb08-tel">%s</p></div></div>' % (
              ''.join(('<div class="zb08-t">%s</div>' if i != 1 else lauf('drift', -90, '%s', 'zb08-t')) % (
                  fo(k, '', '(max-width:860px) 100vw, 33vw', '50% 40%') + '<div class="zb08-text"><p class="zb08-tag">%s</p><p class="zb08-zeit">%s</p></div>' % (t, z))
                  for i, ((t, z), k) in enumerate(zip(BAR, ('barlicht', 'ws00', 'schildnacht')))), tel())))

# 9 Der Dreiklang: Karte links über die volle Höhe, in der Mitte gross der Flur, rechts zwei Bilder übereinander
F.append(('Der Dreiklang', '<div class="zb zb09 auf">%s<div class="zb09-m">%s</div>%s%s</div>' % (
    karte('zb09-k'), lauf('zoom', .1, fo('flur', '', '(max-width:860px) 100vw, 46vw'), 'zb09-zoom'),
    fo('schildnacht', 'zb09-a'), fo('ecke', 'zb09-b'))))

# 10 Bild im Bild: die Hausecke gross, das Schild kleiner darüber versetzt, die Karte an der anderen Ecke; das kleine Bild schwebt
F.append(('Bild im Bild', '<div class="zb zb10 auf"><div class="zb10-gross">%s</div>%s<div class="zb10-k">%s</div></div>' % (
    fo('ecke', '', '(max-width:860px) 100vw, 58vw'), lauf('drift', -130, fo('schildnacht', '', '(max-width:860px) 60vw, 30vw'), 'zb10-klein'), karte())))

# 11 Die Torbögen: fünf Bögen nebeneinander, im mittleren steht die Karte; der mittlere Bogen steigt
F.append(('Die Torbögen', '<div class="zb zb11 auf">%s%s%s</div>' % (
    ''.join('<div class="zb11-bogen zb11-%d">%s</div>' % (i, fo(k, '', '(max-width:860px) 50vw, 20vw')) for i, k in enumerate(('ecke', 'schildnacht'), 1)),
    lauf('drift', -70, karte('zb11-k'), 'zb11-mitte'),
    ''.join('<div class="zb11-bogen zb11-%d">%s</div>' % (i, fo(k, '', '(max-width:860px) 50vw, 20vw')) for i, k in enumerate(('fensterdraussen', 'flur'), 3)))))

# 12 Der Bilderrahmen: zehn Bilder rahmen die Karte ein; oben und unten rücken die Reihen beim Scrollen an die Karte heran
F.append(('Der Bilderrahmen', '<div class="zb zb12 auf">%s<div class="zb12-mitte">%s%s%s</div>%s</div>' % (
    lauf('drift', 70, ''.join(fo(k, '', '(max-width:860px) 25vw, 25vw') for k in ('ecke', 'schildnacht', 'fassade', 'schildnah')), 'zb12-reihe'),
    fo('fensterdraussen', '', '(max-width:860px) 25vw, 25vw'), quer('zb12-k'), fo('barlicht', '', '(max-width:860px) 25vw, 25vw'),
    lauf('drift', -70, ''.join(fo(k, '', '(max-width:860px) 25vw, 25vw') for k in ('flur', 'ws00', 'barneg', 'kerze3')), 'zb12-reihe'))))

# 13 Das Mauerwerk: Bilder im Ziegelverband wie die Klinker der Fassade, die Karte ist ein langer Stein; die Reihen schieben sich gegeneinander
F.append(('Das Mauerwerk', '<div class="zb zb13 auf">%s%s%s</div>' % (
    lauf('quer', -50, ''.join(fo(k, 'zb13-s') for k in ('ecke', 'schildnacht', 'fassade', 'schildnah', 'barnacht')), 'zb13-reihe'),
    lauf('quer', 50, fo('fensterdraussen', 'zb13-s h') + fo('barlicht', 'zb13-s') + quer('zb13-s zb13-k') + fo('flur', 'zb13-s') + fo('kerze3', 'zb13-s h'), 'zb13-reihe b'),
    lauf('quer', -50, ''.join(fo(k, 'zb13-s') for k in ('ws00', 'barneg', 'bar', 'schildtag', 'theke')), 'zb13-reihe'))))

# 14 Schrift dahinter: «Wild Side» riesig hinter drei Bildern und der Karte; die Schrift zieht beim Scrollen durch
F.append(('Schrift dahinter', '<div class="zb zb14 auf"><div class="zb14-schrift zb-voll" aria-hidden="true">%s</div>%s<div class="zb14-k">%s</div></div>' % (
    lauf('quer', -220, '<p>Wild Side</p>', 'zb14-lauf'),
    ''.join('<div class="zb14-f zb14-%s">%s</div>' % (c, fo(k)) for c, k in (('a', 'schildnacht'), ('b', 'ecke'), ('c', 'flur'))), karte())))

# 15 Die Jalousie: die Hausecke in acht Streifen, die versetzt stehen und sich in der Mitte des Bildschirms zu einem Bild fügen
STREIFEN = ''.join('<div class="zb15-s" style="--o:%dpx"><div class="zb15-in" style="--i:%d">%s</div></div>' % (o, i, bild('schildtag', '(max-width:860px) 100vw, 64vw', '50% 42%'))
                   for i, o in enumerate((-70, 50, -30, 80, -60, 30, -90, 60)))
F.append(('Die Jalousie', '<div class="zb zb15 auf"><div class="zb15-k">%s</div><div class="zb15-bild" data-wb-jal>%s</div></div>' % (karte(), STREIFEN)))

# 16 Die Karte bleibt stehen: links steht die Karte fest, rechts ziehen vier hohe Bilder in zwei Spalten vorbei
F.append(('Die Karte bleibt stehen', '<div class="zb zb16 auf"><div class="zb16-l">%s</div><div class="zb16-r"><div>%s%s</div><div>%s%s</div></div></div>' % (
    karte(), fo('ecke', 'hoch', '(max-width:860px) 50vw, 32vw'), fo('fensterdraussen', '', '(max-width:860px) 50vw, 32vw'),
    fo('schildnacht', '', '(max-width:860px) 50vw, 32vw'), fo('flur', 'hoch', '(max-width:860px) 50vw, 32vw'))))

# 17 Die Überblendung: ein grosses Bild bleibt stehen und blendet beim Scrollen über vier Stationen bis zur Bar, die Karte daneben
ST = [('ecke', 'An der Ecke Rampenstraße'), ('schildnacht', 'Am Schild an der Hausecke'), ('flur', 'Durch den Flur'), ('ws00', 'In der Bar')]
F.append(('Die Überblendung', '<div class="zb zb17 auf" data-wb-blende><div class="zb17-buehne"><div class="zb17-bilder">%s</div>%s</div></div>' % (
    ''.join(fo(k, 'zb17-f', '(max-width:860px) 50vw, 64vw', None, '<figcaption>%s</figcaption>' % E(t)) for k, t in ST), karte('zb17-k'))))

# 18 Der Flur: vier Bilder hängen an den Wänden eines Gangs, am Ende des Gangs steht die Karte; beim Scrollen geht man hinein
F.append(('Der Flur', '<div class="zb zb18 auf"><div class="zb18-raum">%s</div><div class="zb18-handy">%s<div class="zb18-hb">%s%s</div></div></div>' % (
    lauf('tief', 320, '<div class="zb18-wand l">%s%s</div><div class="zb18-wand r">%s%s</div><div class="zb18-ende">%s</div>' % (
        fo('ecke', '', '30vw'), fo('schildnacht', '', '30vw'), fo('flur', '', '30vw'), fo('fensterdraussen', '', '30vw'), karte('zb18-k')), 'zb18-tief'),
    karte(), fo('schildnacht', '', '50vw'), fo('flur', '', '50vw'))))

# 19 Der Aushang: die Karte gross über die halbe Breite, «Die Bar» und die Zeiten in grosser Schrift, rechts vier Bilder
F.append(('Der Aushang', '<div class="zb zb19 auf">%s%s</div>' % (
    karte('zb19-k'), lauf('drift', -70, ''.join(fo(k, '', '(max-width:860px) 50vw, 25vw') for k in ('ecke', 'schildnacht', 'fensterdraussen', 'flur')), 'zb19-r'))))

# 20 Die Mittelachse: in der Mitte hoch der Flur, links die Tage, rechts die Uhrzeiten, darüber gross «Die Bar»
F.append(('Die Mittelachse', '<div class="zb zb20 auf"><p class="fk-wer">Walk on the Wild Side</p><p class="zb20-titel">Die Bar</p>'
          '<div class="zb20-achse"><div class="zb20-l">%s</div>%s<div class="zb20-r">%s</div></div><p class="zb20-tel">%s</p></div>' % (
              ''.join('<p>%s</p>' % t for t, _z in BAR), lauf('zoom', .12, fo('flur', '', '(max-width:860px) 60vw, 28vw'), 'zb20-bild'),
              ''.join('<p>%s</p>' % z for _t, z in BAR), tel())))


def main():
    seite = open(os.path.join(HIER, 'weg.html'), encoding='utf-8').read()
    m = re.search(r'(<section class="vab bar-ab v-weg-abends[^"]*"[^>]*>)(.*?)(</section>)', seite, re.S)
    assert m, '«So findest du hin» in weg.html nicht gefunden'
    innen = m.group(2)
    w = innen.index('<div class="fw flaeche')
    assert innen.endswith('</div>')
    vorn = innen[:w]
    kopf_tag = m.group(1).replace('class="vab ', 'id="weg" data-name="Die Bar" class="wahl vab ', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % innen]
    teile += ['<div class="wv" data-n="%d" hidden>%s%s</div></div>' % (i, vorn, wand) for i, (_n, wand) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Die Bar</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: vier Bilder um die Karte'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('weg-bar-wahl.css', 'weg-bar-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["weg"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/weg-bar-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
    seite = seite.replace('<title>', '<title>Bar-Karte wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/weg-bar-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'weg-bar-wahl.html'), 'w', encoding='utf-8').write(seite)
    print('Seite weg-bar-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
