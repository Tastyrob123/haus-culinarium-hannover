#!/usr/bin/env python3
"""Culinarium Hannover · «Seit 2023.» in 15 Fassungen, direkt in der echten Startseite, 27.10.2026.
Robert: «gib 15 visualisierungsmöglichkeiten für den abschnitt alternativ». Heute: Titel mittig, fünf Bildkarten mit Jahreszahl, Monat und Satz.
Jede Fassung eine eigene Anordnung aus der Welt des Hauses (Plakate, Preise, Bonspiess, Messbecher, Abzüge, Rudis Zeilen), ohne Nummern-Liste und ohne Pillen.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut chronik-wahl.html (Leiste unten, Pfeiltasten, ?chronik=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/chronik_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, knopf

HIER = bau.HIER

# Jahr, Wann, Satz, Bild, Stichwort, Rudis Zeile (Fakten wie im heutigen Teil)
M = [
    ('2023', 'Mai', 'Das erste Pop-up mit Momo im Walk on the Wild Side.', 'pop23', 'Pop-up', 'POP-UP / MOMO / WILD SIDE'),
    ('2023', 'Herbst', 'Die ersten Abende unter dem Namen Culinarium, „by Momo x Christoph“, jeder mit eigenem Plakat.', 'pl23', 'Culinarium', 'CULINARIUM / ERSTES PLAKAT'),
    ('2024', 'Frühjahr', 'Rudi kommt in die Küche. Seitdem heisst es „by Momo x Rudi“.', 'kueche', 'Rudi', 'RUDI / IN DER KÜCHE'),
    ('2025', 'Februar', 'Vierzehn Plätze an einer Tafel, freitags ab 19 Uhr, samstags ab 17 Uhr.', 't08', 'Die Tafel', 'VIERZEHN PLÄTZE / EINE TAFEL'),
    ('2026', 'September', 'Der Abend ist ausgebucht, bevor er beginnt.', 'kerze1', 'Ausgebucht', 'AUSGEBUCHT'),
]
ABENDE = bau.ABENDE  # (Jahr, Datum, Zusatz, Preis, Plakat-ID, Zeile)
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
POS = {'kueche': '50% 40%', 't08': '50% 40%', 'kerze1': '50% 40%', 't01': '50% 40%', 't03': '50% 40%', 'tafelleer': '50% 55%',
       'anstossen': '50% 40%', 'momo': '50% 38%', 'theke': '50% 45%', 'lachen': '50% 35%', 'kerze2': '50% 40%', 'service': '50% 40%'}
KNOPF = knopf('Alle Abende ansehen', 'abende.html')
SATZ = 'Aus einem Pop-up an der Bar sind ausgebuchte Abende geworden.'


def bild(b, w=1000, cls='', alt=''):
    return '<img class="%s" src="assets/bild/%s-%d.webp?v=%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        cls, b, w, VERSION, E(alt), POS.get(b, '50% 50%'))


def plakat(pid, w=640):
    return bild('p_' + pid, w, 'ch-pl', 'Plakat Culinarium')


def titel(cls='', satz=SATZ):
    """Überschrift wie überall: rollt aus dem Schlitz."""
    return '<div class="ch-tk %s"><h2 class="zl auf titel" aria-label="Seit 2023."><span class="z"><span style="--i:0">Seit 2023.</span></span></h2>%s</div>' % (
        cls, '<p class="sw auf ch-satz" style="--i:2">%s</p>' % E(satz) if satz else '')


def monat(datum):
    return next(i for i, m in enumerate(MONATE) if m in datum)


def preis(p):
    return p.replace(',00 EUR', ' €')


F = []  # (Name, Inhalt)

# 1 Das mitlaufende Jahr: links bleibt die Jahreszahl stehen und rollt weiter, rechts ziehen die fünf Momente mit grossem Foto vorbei
F.append(('Das mitlaufende Jahr', '<div class="ch-01" data-ch-lauf><div class="ch-01-l"><div class="ch-01-fest">%s<div class="ch-01-fenster" aria-hidden="true"><div class="ch-01-rolle">%s</div></div>'
          '<p class="ch-01-wann mono" aria-hidden="true">%s</p><div class="sw auf">%s</div></div></div><div class="ch-01-r">%s</div></div>' % (
              titel('links'), ''.join('<span>%s</span>' % m[0] for m in M), ''.join('<span>%s</span>' % E(m[1]) for m in M), KNOPF,
              ''.join('<article class="ch-01-m" data-m="%d"><figure class="ch-01-bild">%s</figure><p class="ch-01-j">%s</p><p class="mono ch-w">%s %s</p><p class="ch-01-s">%s</p></article>' % (
                  i, bild(m[3], 1000), m[0], E(m[1]), m[0], E(m[2])) for i, m in enumerate(M)))))

# 2 Jahreszahlen als Schalter: oben die fünf Momente als grosse Zahlen, darunter eine Bühne; antippen wechselt Foto und Satz
F.append(('Jahreszahlen als Schalter', '<div class="ch-02" data-ch>%s<div class="ch-02-zahlen">%s</div><div class="ch-02-buehne auf">%s</div><div class="sw auf ch-02-k">%s</div></div>' % (
    titel('mitte'),
    ''.join('<button type="button" class="ch-02-z%s" data-q="%d"><b>%s</b><span class="mono">%s</span></button>' % (' an' if i == 0 else '', i, m[0], E(m[1])) for i, m in enumerate(M)),
    ''.join('<figure class="ch-02-f%s" data-a="%d">%s<figcaption><span class="mono">%s %s</span><p>%s</p></figcaption></figure>' % (
        ' an' if i == 0 else '', i, bild(m[3], 1600 if m[3] == 'kueche' else 1000), E(m[1]), m[0], E(m[2])) for i, m in enumerate(M)), KNOPF)))

# 3 Der Preis als Treppe: vier Jahre, vier Preise, jede Stufe ein Stück höher und ein Foto obendrauf
STUFEN = [('2023', '59 €', 'Die ersten Abende by Momo x Christoph.', 'pl23'),
          ('2024', '69 €', 'Rudi kommt in die Küche.', 'kueche'),
          ('2025', '79 €', 'Vierzehn Plätze an einer Tafel.', 't08'),
          ('2026', '89 €', 'Ausgebucht, bevor es losgeht.', 'kerze1')]
F.append(('Der Preis als Treppe', '<div class="ch-03">%s<div class="ch-03-treppe">%s</div><div class="sw auf ch-03-k">%s</div></div>' % (
    titel('links', 'Mit jedem Jahr ein Stück mehr Abend. Der Preis steigt mit, die Plätze bleiben knapp.'),
    ''.join('<div class="ch-03-s auf" style="--i:%d;--h:%d"><figure>%s</figure><div class="ch-03-block"><p class="ch-03-p">%s</p><p class="mono ch-w">%s</p><p class="ch-03-t">%s</p></div></div>' % (
        i, i, bild(b, 640), p, j, E(t)) for i, (j, p, t, b) in enumerate(STUFEN)), KNOPF)))

# 4 Der Name auf dem Plakat: die Zeile «by Momo x …» wie auf den Plakaten, Christoph wird durchgestrichen, Rudi kommt dazu
NAMEN = [('Herbst 2023', 'BY MOMO <i>X</i> <s>CHRISTOPH<u></u></s>', 'CxNkFWTIvL2', 'Die ersten Abende heissen Culinarium.'),
         ('April 2024', 'BY MOMO', 'C56bJeds8PF', 'Ein Abend steht Momo allein auf dem Plakat.'),
         ('Seit Juli 2024', 'BY MOMO <i>X</i> <em>RUDI</em>', 'C8cgYVSouVT', 'Rudi kommt in die Küche, und bleibt.')]
F.append(('Der Name auf dem Plakat', '<div class="ch-04">%s<div class="ch-04-zeilen">%s</div><p class="ch-04-rest sw auf"><span class="mono">Mai 2023</span> Das erste Pop-up. '
          '<span class="mono">Februar 2025</span> Vierzehn Plätze an einer Tafel. <span class="mono">September 2026</span> Ausgebucht, bevor es beginnt.</p><div class="sw auf">%s</div></div>' % (
              titel('links', 'Wer kocht, steht auf dem Plakat. Drei Zeilen erzählen die Geschichte.'),
              ''.join('<div class="ch-04-z auf" style="--i:%d"><p class="mono ch-w">%s</p><p class="ch-04-name">%s</p><figure class="ch-04-pl">%s</figure><p class="ch-04-s">%s</p></div>' % (
                  i, w, n, plakat(pid), E(s)) for i, (w, n, pid, s) in enumerate(NAMEN)), KNOPF)))


# 5 Die Leine: alle Plakate hängen nach Datum an einer Leine quer durch vier Jahre, mit Klammern; darunter die Jahre mit ihrem Moment
def leine():
    los, ende = 2023 + 4 / 12, 2026 + 9 / 12
    lage = lambda a: (int(a[0]) + monat(a[1]) / 12 - los) / (ende - los)
    pl = ''.join('<figure class="ch-05-p" style="--x:%.4f;--r:%.1fdeg;--i:%d">%s<span class="ch-05-kl" aria-hidden="true"></span><figcaption class="mono">%s</figcaption></figure>' % (
        lage(a), (-3, 2.5, -1.5, 3, -2.5, 1.5)[n % 6], n, plakat(a[4]), E(a[1].split(' und ')[0] + ' ' + a[0][2:])) for n, a in enumerate(a for a in ABENDE if a[4]))
    pl = '<figure class="ch-05-p ch-05-erst" style="--x:0;--r:2deg;--i:0">%s<span class="ch-05-kl" aria-hidden="true"></span><figcaption class="mono">Mai 23</figcaption></figure>' % bild('pop23', 640, 'ch-pl') + pl
    jahre = ''.join('<div class="ch-05-j" style="--x:%.4f"><b>%s</b><p>%s</p></div>' % (
        max(0, (int(j) - los) / (ende - los)), j, E(t)) for j, t in [('2023', 'Pop-up, dann Culinarium'), ('2024', 'Rudi kommt'), ('2025', 'Vierzehn Plätze'), ('2026', 'Ausgebucht')])
    return '<div class="ch-05-band auf"><div class="ch-05-feld"><span class="ch-05-schnur" aria-hidden="true"></span>%s<div class="ch-05-jahre">%s</div></div></div>' % (pl, jahre)


F.append(('Die Leine', '<div class="ch-05">%s%s<div class="sw auf ch-05-k">%s</div></div>' % (
    titel('mitte', 'Jedes Plakat an seinem Tag aufgehängt, vom ersten Pop-up bis zum letzten Abend.'), leine(), KNOPF)))


# 6 Der Wandkalender: vier Jahre nebeneinander, zwölf Monate untereinander; jeder Abend ist angestrichen, antippen zeigt sein Plakat gross
def kalender():
    spalten, bühne, n = [], [], 0
    abende = [('2023', 'Sa 20. Mai', 'das erste Pop-up', '', None, '')] + [a for a in ABENDE]
    for j in ('2023', '2024', '2025', '2026'):
        zeilen = []
        for mi, mn in enumerate(MONATE):
            hier = [a for a in abende if a[0] == j and monat(a[1]) == mi]
            if hier:
                knoepfe = ''
                for a in hier:
                    knoepfe += '<button type="button" class="ch-06-t1%s" data-q="%d">%s</button>' % (' an' if n == 0 else '', n, E(a[1].split(' und ')[0]))
                    b = bild('p_' + a[4], 1000, '', 'Plakat') if a[4] else bild('pop23', 1000, '', 'Plakat Pop-up')
                    bühne.append('<div class="ch-06-a%s" data-a="%d"><figure>%s</figure><p class="mono ch-w">%s %s</p><p class="ch-06-t">%s</p></div>' % (
                        ' an' if n == 0 else '', n, b, E(a[1]), j, E(' · '.join(x for x in (a[2], preis(a[3])) if x) or 'Culinarium')))
                    n += 1
                zeilen.append('<span class="ch-06-m da-ab"><span class="mono">%s</span>%s</span>' % (mn[:3], knoepfe))
            else:
                zeilen.append('<span class="ch-06-m"><span class="mono">%s</span></span>' % mn[:3])
        spalten.append('<div class="ch-06-sp"><p class="ch-06-j">%s</p>%s</div>' % (j, ''.join(zeilen)))
    return '<div class="ch-06-wand auf" data-ch><div class="ch-06-kal">%s</div><div class="ch-06-buehne">%s</div></div>' % (''.join(spalten), ''.join(bühne))


F.append(('Der Wandkalender', '<div class="ch-06">%s%s<div class="sw auf">%s</div></div>' % (
    titel('links', 'Vom Pop-up bis heute ist jeder Abend angestrichen. Einen Tag antippen.'), kalender(), KNOPF)))

# 7 Die Abzüge: fünf Fotos mit weissem Rand liegen auf dem dunklen Tresen, beschriftet von Hand; sie landen nacheinander
LAGE7 = [(-4, 0), (3, 1), (-2, 2), (4, 3), (-3, 4)]
F.append(('Die Abzüge', '<div class="ch-07">%s<div class="ch-07-tresen">%s</div><div class="sw auf ch-07-k">%s</div></div>' % (
    titel('mitte'),
    ''.join('<figure class="ch-07-a a%d auf" style="--r:%ddeg;--i:%d"><div class="ch-07-f">%s</div><figcaption><span class="ch-07-hand">%s %s</span><span>%s</span></figcaption></figure>' % (
        i, r, i, bild(M[i][3], 640), E(M[i][1]), M[i][0], E(M[i][2])) for r, i in LAGE7), KNOPF)))

# 8 Der Kontaktbogen: zwölf Bilder wie auf einem Filmbogen, fünf davon mit Fettstift eingekreist und beschriftet
BOGEN = ['pop23', 'schildnacht', 'pl23', 'momo', 'theke', 'kueche', 'pass', 't08', 'lachen', 'glaeser', 'kerze1', 'anstossen']
KREIS = {'pop23': 0, 'pl23': 1, 'kueche': 2, 't08': 3, 'kerze1': 4}
F.append(('Der Kontaktbogen', '<div class="ch-08"><div class="ch-08-l">%s<div class="sw auf">%s</div></div><div class="ch-08-bogen auf">%s</div></div>' % (
    titel('links', 'Vier Jahre auf einem Bogen. Eingekreist ist, was den Abend verändert hat.'), KNOPF,
    ''.join('<figure class="ch-08-f%s" style="--i:%d">%s<span class="ch-08-nr mono">%dA</span>%s</figure>' % (
        ' kreis' if b in KREIS else '', n, bild(b, 640), n + 14,
        '<span class="ch-08-ring" aria-hidden="true"></span><figcaption>%s %s · %s</figcaption>' % (E(M[KREIS[b]][1]), M[KREIS[b]][0], E(M[KREIS[b]][4])) if b in KREIS else '')
        for n, b in enumerate(BOGEN)))))

# 9 Rudis Zeilen: jeder Moment in Versalien mit Schrägstrichen, wie Rudi seine Teller schreibt; das Foto schaut seitlich herein
F.append(('Rudis Zeilen', '<div class="ch-09">%s<div class="ch-09-zeilen">%s</div><div class="sw auf ch-09-k">%s</div></div>' % (
    titel('mitte', 'So schreibt Rudi seine Teller. So schreiben wir seine Geschichte.'),
    ''.join('<div class="ch-09-z %s"><figure class="ch-09-b auf">%s</figure><div class="ch-09-t"><p class="mono ch-w">%s %s</p><h3 class="zl auf"><span class="z"><span>%s</span></span></h3><p class="ch-09-s">%s</p></div></div>' % (
        'rechts' if i % 2 else 'links', bild(m[3], 640), E(m[1]), m[0], m[5].replace(' / ', ' <i>/</i> '), E(m[2])) for i, m in enumerate(M)), KNOPF)))

# 10 Der Bonspiess: an der Bar steckt auf dem Spiess ein Bon je Moment; antippen holt seinen Abend als Foto nach vorn
F.append(('Der Bonspiess', '<div class="ch-10" data-ch><div class="ch-10-l">%s<div class="ch-10-spiess"><span class="ch-10-stab" aria-hidden="true"></span>%s<span class="ch-10-fuss" aria-hidden="true"></span></div></div>'
          '<div class="ch-10-r"><div class="ch-10-buehne auf">%s</div><div class="sw auf">%s</div></div></div>' % (
              titel('links', 'Was an der Bar auf dem Spiess landet, ist erledigt. Fünf Bons, vier Jahre.'),
              ''.join('<button type="button" class="ch-10-bon auf%s" data-q="%d" style="--i:%d;--r:%.1fdeg"><span class="ch-10-kopf">Walk on the Wild Side<br>Haasemannstr. 13</span>'
                      '<span class="ch-10-z"><span>%s %s</span><span>#%03d</span></span><b>%s</b><span class="ch-10-s">%s</span><span class="ch-10-z"><span>Culinarium</span><span>✕</span></span></button>' % (
                          ' an' if i == 4 else '', i, 4 - i, (-2.5, 1.8, -1, 2.2, -1.6)[i], E(m[1][:3].upper()), m[0], i + 1, E(m[4]), E(m[2])) for i, m in reversed(list(enumerate(M)))),
              ''.join('<figure class="ch-10-f%s" data-a="%d">%s<figcaption class="mono">%s %s</figcaption></figure>' % (' an' if i == 4 else '', i, bild(m[3], 1000), E(m[1]), m[0]) for i, m in enumerate(M)), KNOPF)))

# 11 Es wird grösser: fünf Bilder auf einer Grundlinie, jedes grösser als das davor, vom kleinen Pop-up zum vollen Abend
F.append(('Es wird grösser', '<div class="ch-11">%s<div class="ch-11-reihe">%s</div><div class="sw auf ch-11-k">%s</div></div>' % (
    titel('links'),
    ''.join('<figure class="ch-11-b auf" style="--i:%d;--g:%d"><div class="ch-11-f">%s</div><figcaption><b>%s</b><span class="mono">%s</span><span class="ch-11-s">%s</span></figcaption></figure>' % (
        i, i, bild(m[3], 1000), m[0], E(m[1]), E(m[2])) for i, m in enumerate(M)), KNOPF)))

# 12 Der Messbecher: ein Jigger von der Bar mit fünf Strichen; beim Scrollen füllt er sich, und jeder Strich hat sein Bild
F.append(('Der Messbecher', '<div class="ch-12" data-ch-becher><div class="ch-12-l">%s<div class="ch-12-bilder">%s</div><div class="sw auf">%s</div></div>'
          '<div class="ch-12-r"><div class="ch-12-becher"><div class="ch-12-glas"><span class="ch-12-fuell" aria-hidden="true"></span>%s</div></div></div></div>' % (
              titel('links', 'Gemessen wie an der Bar: Strich für Strich voller.'),
              ''.join('<figure class="ch-12-f%s" data-m="%d">%s</figure>' % (' an' if i == 0 else '', i, bild(m[3], 1000)) for i, m in enumerate(M)), KNOPF,
              ''.join('<div class="ch-12-strich%s" data-m="%d" style="--y:%d"><span class="ch-12-l1"></span><p><b>%s %s</b>%s</p></div>' % (
                  ' an' if i == 0 else '', i, i, E(m[1]), m[0], E(m[2])) for i, m in enumerate(M)))))

# 13 Der Erzählsatz: die Geschichte in einem grossen Absatz, die Fotos stehen mitten im Text wie Wörter
INL = lambda b: '<span class="ch-13-i auf">%s</span>' % bild(b, 640)
F.append(('Der Erzählsatz', '<div class="ch-13"><p class="ch-13-k mono">Seit 2023</p><p class="ch-13-text">Im Mai 2023 stellt Momo %s zum ersten Mal ein Pop-up in die Bar. '
          'Im Herbst heisst es Culinarium %s und jeder Abend bekommt sein eigenes Plakat. 2024 kommt Rudi %s in die Küche, '
          'seitdem steht „by Momo x Rudi“ darauf. Seit Februar 2025 sitzen vierzehn Gäste %s an einer Tafel, '
          'und heute ist der Abend ausgebucht %s bevor er beginnt.</p><div class="sw auf ch-13-kn">%s</div></div>' % (
              INL('pop23'), INL('pl23'), INL('kueche'), INL('t08'), INL('kerze1'), KNOPF)))

# 14 Das Querband: fünf hohe Fotos zum Wischen, die Jahreszahl gross im Bild, der Satz darunter
F.append(('Das Querband', '<div class="ch-14"><div class="ch-14-kopf">%s<div class="ch-14-pfeile"><button type="button" data-ch-band="-1" aria-label="Zurück">‹</button><button type="button" data-ch-band="1" aria-label="Weiter">›</button></div></div>'
          '<div class="ch-14-band auf">%s</div><div class="sw auf ch-14-k">%s</div></div>' % (
              titel('links'),
              ''.join('<figure class="ch-14-b"><div class="ch-14-f">%s<b>%s</b></div><figcaption><span class="mono">%s</span><p>%s</p></figcaption></figure>' % (
                  bild(m[3], 1000), m[0], E(m[1]), E(m[2])) for m in M), KNOPF)))

# 15 Damals und heute: das Pop-up 2023 und ein ausgebuchter Abend 2026 übereinander; der Griff schiebt die Zeit
F.append(('Damals und heute', '<div class="ch-15">%s<div class="ch-15-feld auf" data-ch-schieber style="--p:50">'
          '<figure class="ch-15-heute">%s<figcaption><span class="mono">2026</span>Ausgebucht, bevor es beginnt.</figcaption></figure>'
          '<div class="ch-15-clip"><div class="ch-15-innen"><figure class="ch-15-damals">%s<figcaption><span class="mono">Mai 2023</span>Das erste Pop-up an der Bar.</figcaption></figure></div></div>'
          '<div class="ch-15-griff" aria-hidden="true"><span>‹ ›</span></div><input type="range" min="0" max="100" value="50" aria-label="Zwischen 2023 und 2026 schieben"></div>'
          '<div class="ch-15-dazwischen">%s</div><div class="sw auf ch-15-k">%s</div></div>' % (
              titel('mitte', 'Schieb den Griff: links das erste Pop-up, rechts ein Abend heute.'), bild('anstossen', 1600), bild('pop23', 1000),
              ''.join('<p><span class="mono">%s %s</span>%s</p>' % (E(m[1]), m[0], E(m[2])) for m in M[1:4]), KNOPF)))


def main():
    seite = open(os.path.join(HIER, 'index.html')).read()
    m = re.search(r'(<section class="vab v-chronik[^"]*"[^>]*id="chronik"[^>]*>)(<div class="vi h-chronik">.*?)(<p class="ueber[^>]*>[^<]*</p></section>)', seite, re.S)
    assert m, 'Teil «Seit 2023» in index.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab v-chronik', 'data-name="Seit 2023" class="vab v-chronik wahl', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv chw ch-f%02d" data-n="%d" hidden><div class="vi">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Seit 2023</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: fünf Bildkarten mit Jahreszahl'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('chronik-wahl.css', 'chronik-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["chronik"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/chronik-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Seit 2023 wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/chronik-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'chronik-wahl.html'), 'w').write(seite)
    print('Seite chronik-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
