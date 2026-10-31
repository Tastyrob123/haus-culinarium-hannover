#!/usr/bin/env python3
"""Culinarium Hannover · Team-Seite, «Wie es kam.» in 15 Fassungen, direkt in der echten Seite, 27.10.2026.
Robert: «Gib mir 15 verschiedene visuelle Darstellungsmöglichkeiten für diesen Abschnitt.» Heute: Titel mittig, sechs Bildkarten im Raster.
Keine der 30 Fassungen aus chronik_wahl.py und chronik_wahl2.py wiederholt sich; jede Anordnung kommt aus der Welt des Hauses
(Linden Journal, das Loch in der Wand, Tresen, Karte, Kerzen, Fassade, Fussballkneipe), ohne Nummern-Liste und ohne Pillen.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut kam-wahl.html (Leiste unten, Pfeiltasten, ?kam=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/kam_wahl.py (liest das fertige leute.html)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION

HIER = bau.HIER

# Wann, Jahr, Satz, Bild, Wort, Rudis Zeile, Schlagzeile, Seite (Fakten wie im heutigen Teil)
S = [
    ('Oktober', '2017', 'Das Walk on the Wild Side öffnet in der ehemaligen Fußballkneipe Linden Journal.', 'schildnacht', 'Die Bar',
     'LINDEN JOURNAL / FUSSBALLKNEIPE / BAR', 'Aus der Fußballkneipe wird eine Bar', 'bar'),
    ('Mai', '2023', 'Das erste Pop-up mit Momo.', 'pop23', 'Das Pop-up',
     'MOMO / POP-UP / ERSTER ABEND', 'Momo lädt zum ersten Pop-up', 'abend'),
    ('Herbst', '2023', 'Die ersten Abende unter dem Namen Culinarium, „by Momo x Christoph“.', 'pl23', 'Der Name',
     'CULINARIUM / MOMO X CHRISTOPH', 'Die Abende bekommen einen Namen', 'abend'),
    ('November', '2023', 'Reopening der Bar unter Derya Ivkin. Mixology ohne Karte.', 'ws00', 'Die Theke',
     'DERYA / REOPENING / OHNE KARTE', 'Die Bar öffnet neu, mit Derya', 'bar'),
    ('', '2024', 'Rudi kommt in die Küche von Culinarium, „by Momo x Rudi“.', 'kueche', 'Die Küche',
     'RUDI / KÜCHE / MOMO X RUDI', 'Rudi kommt in die Küche', 'abend'),
    ('September', '2026', 'Der September-Abend ist ausgebucht, Dirty Chicken feiert Opening.', 'kerze1', 'Ausgebucht',
     'AUSGEBUCHT / DIRTY CHICKEN', 'Ausgebucht, bevor es beginnt', 'abend'),
]
POS = {'kueche': '50% 40%', 'kerze1': '50% 40%', 'anstossen': '50% 38%', 'tafelleer': '50% 55%', 'kopf_momo': '50% 40%',
       'kopf_derya': '50% 40%', 'kopf_rudi': '50% 40%', 'trio2': '50% 45%'}
SATZ = 'Von der Bar in einer alten Fußballkneipe bis zum ausgebuchten Abend an der langen Tafel.'
GROESSEN = {}


def wann(s):
    return ('%s %s' % (s[0], s[1])).strip()


def bild(b, w=1000, cls='', alt=None):
    if not GROESSEN:
        for f in os.listdir(os.path.join(HIER, 'assets', 'bild')):
            m = re.match(r'(.+)-(\d+)\.webp$', f)
            if m:
                GROESSEN.setdefault(m.group(1), set()).add(int(m.group(2)))
    w = max([g for g in GROESSEN.get(b, {640}) if g <= w] or [640])
    alt = bau.BILD[b][2] if alt is None and b in bau.BILD else (alt or '')
    return '<img class="%s" src="assets/bild/%s-%d.webp?v=%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        cls, b, w, VERSION, E(alt), POS.get(b, '50% 50%'))


def titel(cls='mitte', satz=SATZ):
    """Überschrift wie überall: rollt aus dem Schlitz."""
    return '<div class="kw-tk %s"><h2 class="zl auf titel" aria-label="Wie es kam."><span class="z"><span style="--i:0">Wie es kam.</span></span></h2>%s</div>' % (
        cls, '<p class="sw auf kw-satz" style="--i:1">%s</p>' % E(satz) if satz else '')


def zeile(z):
    return z.replace(' / ', ' <i>/</i> ')


F = []  # (Name, Ton, Inhalt)

# 1 Die Titelseite: das Haus hiess einmal Linden Journal, also erscheint die Geschichte als Zeitung; die Abendmeldung oben, der Rest in Spalten
aufm = S[5]
F.append(('Die Titelseite', 'hell', '<div class="kw-01"><div class="kw-01-blatt auf"><header class="kw-01-kopf"><p class="mono">Haasemannstraße 13 · Hannover-Linden</p>'
          '<h2 class="kw-01-name" aria-label="Wie es kam.">Linden Journal</h2><p class="mono">Ausgabe 2017 bis 2026</p><span class="kw-01-linie" aria-hidden="true"></span></header>'
          '<article class="kw-01-auf"><figure>%s</figure><div><p class="mono kw-w">%s</p><h3>%s</h3><p>%s</p><p class="kw-01-unter">%s</p></div></article>'
          '<div class="kw-01-spalten">%s</div></div></div>' % (
              bild('anstossen', 1600), wann(aufm), E(aufm[6]), E(aufm[2]), E(SATZ),
              ''.join('<article class="kw-01-m"><figure>%s</figure><p class="mono kw-w">%s</p><h3>%s</h3><p>%s</p></article>' % (
                  bild(s[3], 640), wann(s), E(s[6]), E(s[2])) for s in S[:5]))))

# 2 Durch die Wand: das Loch in der Wand der Bar als einziges Fenster; die Daten daneben schalten, was man hindurch sieht
F.append(('Durch die Wand', 'nacht', '<div class="kw-02" data-kw>%s<div class="kw-02-buehne"><div class="kw-02-wand auf"><div class="kw-02-loch">%s</div></div>'
          '<div class="kw-02-daten">%s<div class="kw-02-texte">%s</div></div></div></div>' % (
              titel('links', 'Durch das Loch in der Wand der Bar, sechs Mal zu einer anderen Zeit.'),
              ''.join('<figure class="kw-02-f%s" data-a="%d">%s</figure>' % (' an' if i == 0 else '', i, bild(s[3], 1000)) for i, s in enumerate(S)),
              ''.join('<button type="button" class="kw-02-d%s" data-q="%d"><span class="mono">%s</span><b>%s</b></button>' % (
                  ' an' if i == 0 else '', i, E(s[0] or 'Jahr'), s[1]) for i, s in enumerate(S)),
              ''.join('<p class="kw-02-t%s" data-a="%d">%s</p>' % (' an' if i == 0 else '', i, E(s[2])) for i, s in enumerate(S)))))

# 3 Der lange Tresen: beim Hinunterscrollen fährt der Tresen seitlich vorbei; auf ihm stehen die sechs Momente, die Daten sind ins Holz geschrieben
F.append(('Der lange Tresen', 'nacht', '<div class="kw-03-handy">%s</div><div class="kw-03" data-kw-tresen><div class="kw-03-halt"><div class="kw-03-spur">'
          '<div class="kw-03-anfang">%s</div>%s<div class="kw-03-ende"><p class="kw-03-heute">Und der nächste Abend kommt.</p></div></div>'
          '<div class="kw-03-holz" aria-hidden="true"></div></div></div>' % (
              titel('links', 'Neun Jahre an einem Tresen entlang. Wisch weiter, er fährt vorbei.'), titel('links', 'Neun Jahre an einem Tresen entlang. Scroll weiter, er fährt vorbei.'),
              ''.join('<figure class="kw-03-m"><div class="kw-03-b">%s</div><figcaption><span class="mono kw-w">%s</span><p>%s</p></figcaption></figure>' % (
                  bild(s[3], 1000), wann(s), E(s[2])) for s in S))))

# 4 Zwei Seiten der Theke: links die Bar, rechts die Abende; die Mittellinie zieht sich beim Scrollen und trägt die Jahre
F.append(('Zwei Seiten der Theke', 'hell', '<div class="kw-04">%s<div class="kw-04-koepfe"><p><b>Die Bar</b><span class="mono">Walk on the Wild Side</span></p><p><b>Die Abende</b><span class="mono">Culinarium</span></p></div>'
          '<div class="kw-04-feld" data-kw-p="linie"><span class="kw-04-linie" aria-hidden="true"></span>%s</div></div>' % (
              titel(),
              ''.join('<div class="kw-04-z %s"><p class="kw-04-j mono">%s</p><article class="kw-04-k auf"><figure>%s</figure><p class="mono kw-w"><span class="kw-04-seite">%s · </span>%s</p><p class="kw-04-s">%s</p></article></div>' % (
                  s[7], s[1], bild(s[3], 1000), 'Die Bar' if s[7] == 'bar' else 'Die Abende', wann(s), E(s[2])) for s in S))))

# 5 Die Karte des Abends: die Geschichte als gedruckte Menükarte in sechs Gängen, in Rudis Zeilen; das Foto daneben wechselt mit dem Gang
F.append(('Die Karte des Abends', 'hell', '<div class="kw-05" data-kw-karte><div class="kw-05-bild"><div class="kw-05-rahmen">%s</div></div>'
          '<div class="kw-05-karte auf"><p class="mono kw-05-oben">Culinarium · by Momo x Rudi</p><h2 class="kw-05-titel">Wie es kam.</h2><p class="kw-05-unter">Sechs Gänge, 2017 bis 2026</p>%s'
          '<p class="mono kw-05-fuss">Haasemannstraße 13 · Linden</p></div></div>' % (
              ''.join('<figure class="kw-05-f%s" data-m="%d">%s</figure>' % (' an' if i == 0 else '', i, bild(s[3], 1000)) for i, s in enumerate(S)),
              ''.join('<div class="kw-05-gang%s" data-m="%d"><figure class="kw-05-klein">%s</figure><p class="kw-05-z">%s</p><p class="kw-05-s"><span class="mono">%s</span> %s</p></div>' % (
                  ' an' if i == 0 else '', i, bild(s[3], 640), zeile(s[5]), wann(s), E(s[2])) for i, s in enumerate(S)))))

# 6 Bilder in den Zahlen: vier Jahre, riesig gesetzt; das Foto des Jahres steckt in den Ziffern, die Zahl gleitet beim Scrollen
JAHRE = [('2017', 'schildnacht', [S[0]]), ('2023', 'theke', S[1:4]), ('2024', 'kueche', [S[4]]), ('2026', 'kerze1', [S[5]])]
F.append(('Bilder in den Zahlen', 'hell', '<div class="kw-06">%s%s</div>' % (titel(), ''.join(
    '<div class="kw-06-r%s" data-kw-p><p class="kw-06-zahl" style="background-image:url(assets/bild/%s-1000.webp?v=%s)" aria-hidden="true">%s</p><div class="kw-06-t">%s</div></div>' % (
        ' rechts' if n % 2 else '', b, VERSION, j,
        ''.join('<p><span class="mono kw-w">%s</span>%s</p>' % (wann(s), E(s[2])) for s in ms)) for n, (j, b, ms) in enumerate(JAHRE)))))

# 7 Die Reportage: ein grosses Aufmacherbild, dann die Geschichte als Text mit Randdaten, einem Zitat und zwei Bildern dazwischen
F.append(('Die Reportage', 'hell', '<div class="kw-07"><figure class="kw-07-auf" data-kw-p><div class="kw-07-auf-i">%s</div></figure>'
          '<div class="kw-07-kopf">%s</div><div class="kw-07-text">'
          '<div class="kw-07-a"><p class="mono kw-07-rand">Oktober 2017</p><p class="kw-07-erst">In Linden, in der ehemaligen Fußballkneipe Linden Journal, öffnet das Walk on the Wild Side. Eine Bar an der Haasemannstraße 13, und für die nächsten Jahre bleibt sie genau das.</p></div>'
          '<div class="kw-07-a"><p class="mono kw-07-rand">Mai 2023</p><p>Momo stellt zum ersten Mal ein Pop-up an die Bar. Im Herbst bekommen die Abende einen Namen: Culinarium, „by Momo x Christoph“.</p></div>'
          '<div class="kw-07-zwei"><figure>%s</figure><figure>%s</figure></div>'
          '<div class="kw-07-a"><p class="mono kw-07-rand">November 2023</p><p>Die Bar öffnet neu, unter Derya Ivkin. Eine Karte gibt es seitdem nicht: Wer an die Theke kommt, bekommt einen Drink nach seinem Geschmack.</p></div>'
          '<blockquote class="kw-07-zitat"><p>„Wenn aus Freunden und Kollegen Familie wird.“</p><cite class="mono">Dirty Chicken, Juni 2026</cite></blockquote>'
          '<div class="kw-07-a"><p class="mono kw-07-rand">2024</p><p>Rudi kommt in die Küche. Seitdem steht auf jedem Plakat „by Momo x Rudi“.</p></div>'
          '<figure class="kw-07-breit">%s</figure>'
          '<div class="kw-07-a"><p class="mono kw-07-rand">September 2026</p><p>Der Abend ist ausgebucht, bevor er beginnt. Und Rudis zweite Küche, Dirty Chicken, feiert Opening.</p></div>'
          '</div></div>' % (bild('tafelleer', 1600), titel('links'), bild('pop23', 640), bild('pl23', 640), bild('kueche', 1600))))

# 8 Postkarten aus Linden: sechs Karten liegen auf dem Tisch, vorn das Foto; antippen dreht die Karte um, hinten steht der Moment
F.append(('Postkarten aus Linden', 'hell', '<div class="kw-08">%s<div class="kw-08-tisch">%s</div></div>' % (
    titel('mitte', 'Sechs Karten aus Linden. Dreh sie um, hinten steht, was passiert ist.'),
    ''.join('<button type="button" class="kw-08-karte auf" style="--i:%d;--r:%.1fdeg" data-kw-dreh aria-label="Karte %s umdrehen"><span class="kw-08-innen">'
            '<span class="kw-08-vorn">%s<span class="kw-08-gruss">Gruss aus Linden · %s</span></span>'
            '<span class="kw-08-hinten"><span class="kw-08-marke"><b>%s</b><span>Linden</span></span><span class="kw-08-text"><span class="mono kw-w">%s</span>%s</span>'
            '<span class="kw-08-an">Walk on the Wild Side<br>Haasemannstraße 13<br>Hannover-Linden</span></span></span></button>' % (
                i, (-2.2, 1.6, -1.1, 2.4, -1.8, 1.2)[i], wann(s), bild(s[3], 640), s[1], s[1], wann(s), E(s[2])) for i, s in enumerate(S)))))

# 9 Das Diamagazin: oben die Leinwand, darunter die Dias im Magazin; antippen hebt das Dia heraus und wirft es auf die Leinwand
F.append(('Das Diamagazin', 'nacht', '<div class="kw-09" data-kw>%s<div class="kw-09-leinwand auf">%s</div><div class="kw-09-magazin">%s</div></div>' % (
    titel('mitte', 'Ein Diaabend in der Bar. Tipp ein Dia an, es kommt auf die Leinwand.'),
    ''.join('<figure class="kw-09-f%s" data-a="%d">%s<figcaption><span class="mono kw-w">%s</span><p>%s</p></figcaption></figure>' % (
        ' an' if i == 0 else '', i, bild(s[3], 1000), wann(s), E(s[2])) for i, s in enumerate(S)),
    ''.join('<button type="button" class="kw-09-dia%s" data-q="%d"><span class="kw-09-rahmen"><span class="kw-09-schrift mono">%s</span>%s</span></button>' % (
        ' an' if i == 0 else '', i, E((s[0][:3] + ' ' if s[0] else '') + s[1]), bild(s[3], 640)) for i, s in enumerate(S)))))

# 10 Das Sammelalbum: für die alte Fussballkneipe ein Album mit Bildern zum Einkleben; die Leute als Bilder, darunter der Moment
KLEB = [('schildnacht', 'Die Bar'), ('kopf_momo', 'Momo'), ('pl23', 'Culinarium'), ('kopf_derya', 'Derya Ivkin'), ('kopf_rudi', 'Rudi'), ('kerze1', 'Ausgebucht')]
F.append(('Das Sammelalbum', 'hell', '<div class="kw-10">%s<div class="kw-10-seite"><p class="kw-10-kopf mono">Saison 2017 bis 2026 · Haasemannstraße 13</p><div class="kw-10-felder">%s</div></div></div>' % (
    titel('mitte', 'Früher hingen hier Fußballbilder. Heute klebt die Geschichte des Hauses im Album.'),
    ''.join('<div class="kw-10-feld"><figure class="kw-10-bild auf" style="--i:%d;--r:%.1fdeg">%s<figcaption><b>%s</b><span class="mono">%s</span></figcaption></figure><p class="kw-10-s">%s</p></div>' % (
        i, (-1.6, 1.2, -.8, 1.8, -1.3, .9)[i], bild(k[0], 640), E(k[1]), wann(s), E(s[2])) for i, (s, k) in enumerate(zip(S, KLEB))))))

# 11 Der Fotoautomat: zwei Streifen aus dem Automaten, je drei Bilder; daneben steht, was auf ihnen passiert; die Streifen gleiten verschieden schnell
F.append(('Der Fotoautomat', 'nacht', '<div class="kw-11">%s<div class="kw-11-paare">%s</div></div>' % (
    titel('mitte'), ''.join(
        '<div class="kw-11-paar%s" data-kw-p><div class="kw-11-streifen" style="--r:%.1fdeg">%s</div><div class="kw-11-text">%s</div></div>' % (
            ' rechts' if n else '', (-2.4, 2)[n], ''.join('<figure>%s</figure>' % bild(s[3], 640) for s in teil),
            ''.join('<p><span class="mono kw-w">%s</span>%s</p>' % (wann(s), E(s[2])) for s in teil)) for n, teil in enumerate((S[:3], S[3:]))))))

# 12 Die grossen Wörter: sechs Wörter über die ganze Breite; wer darüberfährt, dem folgt das Foto zum Wort
F.append(('Die grossen Wörter', 'hell', '<div class="kw-12" data-kw-woerter>%s<div class="kw-12-liste">%s</div><div class="kw-12-folger" aria-hidden="true">%s</div></div>' % (
    titel('links', 'Fahr über ein Wort, und das Bild dazu kommt mit.'),
    ''.join('<div class="kw-12-z" data-m="%d"><span class="mono kw-w">%s</span><p class="kw-12-wort">%s.</p><p class="kw-12-s">%s</p><figure class="kw-12-handy">%s</figure></div>' % (
        i, wann(s), E(s[4]), E(s[2]), bild(s[3], 640)) for i, s in enumerate(S)),
    ''.join('<figure data-m="%d">%s</figure>' % (i, bild(s[3], 640, alt='')) for i, s in enumerate(S)))))

# 13 Das Massband: ein durchgehendes Bildband, jedes Bild so breit, wie die Zeit lang war; darunter das Massband mit den Monaten
MONATE = [67, 4, 2, 8, 26, 6]  # Okt 2017 bis Mai 2023, bis Herbst, bis Nov, bis 2024, bis Sep 2026, bis heute
F.append(('Das Massband', 'hell', '<div class="kw-13">%s<div class="kw-13-roll"><div class="kw-13-innen"><div class="kw-13-band auf" data-kw-p>%s</div><div class="kw-13-mass" aria-hidden="true">%s</div><div class="kw-13-texte">%s</div></div></div></div>' % (
    titel('links', 'Jedes Bild ist so breit, wie die Zeit dauerte. Sechs Jahre Bar, dann ging es schnell.'),
    ''.join('<figure style="--w:%.2f">%s</figure>' % (max(m, 9) ** .62, bild(s[3], 1000)) for s, m in zip(S, MONATE)),
    ''.join('<span style="--w:%.2f"><b>%s</b></span>' % (max(m, 9) ** .62, s[1] if s[1] != S[i - 1][1] or i == 0 else '') for i, (s, m) in enumerate(zip(S, MONATE))),
    ''.join('<p style="--w:%.2f"><span class="mono kw-w">%s</span>%s</p>' % (max(m, 9) ** .62, wann(s), E(s[2])) for s, m in zip(S, MONATE)))))

# 14 Eine Kerze mehr: oben stehen sechs Kerzen; mit jedem Moment, an dem du vorbeiscrollst, brennt eine mehr
F.append(('Eine Kerze mehr', 'nacht', '<div class="kw-14" data-kw-kerzen><div class="kw-14-halt"><div class="kw-14-kopf">%s</div><div class="kw-14-reihe" aria-hidden="true">%s</div></div><div class="kw-14-liste">%s</div></div>' % (
    titel('mitte', 'Mit jedem Schritt brennt eine Kerze mehr auf der Tafel.'),
    ''.join('<span class="kw-14-k" data-m="%d" style="--h:%d"><i class="kw-14-flamme"></i><i class="kw-14-schein"></i><span class="kw-14-wachs"></span><b class="mono">%s</b></span>' % (
        i, (62, 80, 54, 72, 88, 66)[i], s[1]) for i, s in enumerate(S)),
    ''.join('<article class="kw-14-m%s" data-m="%d"><figure>%s</figure><div><p class="mono kw-w">%s</p><p class="kw-14-s">%s</p></div></article>' % (
        ' rechts' if i % 2 else '', i, bild(s[3], 1000), wann(s), E(s[2])) for i, s in enumerate(S)))))

# 15 Die Fassade bei Nacht: das Haus an der Haasemannstrasse mit sechs Fenstern; beim Scrollen geht hinter jedem Fenster das Licht an
F.append(('Die Fassade bei Nacht', 'nacht', '<div class="kw-15">%s<div class="kw-15-haus auf" data-kw-p><p class="kw-15-schild mono">Walk on the Wild Side</p><div class="kw-15-fenster">%s</div>'
          '<div class="kw-15-strasse mono">Haasemannstraße 13</div></div></div>' % (
              titel('mitte', 'Scroll hinunter, und hinter jedem Fenster geht ein Licht an.'),
              ''.join('<figure class="kw-15-f" style="--i:%d"><div class="kw-15-glas">%s<span class="kw-15-dunkel" aria-hidden="true"></span></div><figcaption><span class="mono kw-w">%s</span><p>%s</p></figcaption></figure>' % (
                  i, bild(s[3], 640), wann(s), E(s[2])) for i, s in enumerate(S)))))


def main():
    seite = open(os.path.join(HIER, 'leute.html')).read()
    m = re.search(r'(<section class="vab bar-ab v-lt-chronik[^"]*"[^>]*>)(<div class="vi h-ablauf">.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Wie es kam» in leute.html nicht gefunden'
    kopf_tag = m.group(1).replace('class="vab', 'id="kam" data-name="Wie es kam" class="vab wahl', 1)
    teile = ['<div class="wv" data-n="0" data-ton="hell">%s</div>' % m.group(2)]
    teile += ['<div class="wv kw kw-f%02d" data-n="%d" data-ton="%s" hidden><div class="vi">%s</div></div>' % (i, i, ton, inner) for i, (_n, ton, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Wie es kam</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: sechs Bildkarten im Raster'] + [n for n, _t, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('kam-wahl.css', 'kam-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["kam"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/kam-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Wie es kam wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/kam-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'kam-wahl.html'), 'w').write(seite)
    print('Seite kam-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
