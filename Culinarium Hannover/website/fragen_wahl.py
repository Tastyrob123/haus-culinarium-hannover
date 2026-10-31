#!/usr/bin/env python3
"""Culinarium Hannover · «Gut zu wissen» in 15 Fassungen, direkt in der echten Startseite, 27.10.2026.
Robert: «15 alternative visuelle darstellungsformen des abschnittes». Heute: Foto links mit Titel, rechts sieben aufklappbare Karten mit Nummern.
Jede Fassung eine eigene Anordnung aus der Welt des Abends (Karte am Platz, Tafel, Plakat, Ticket, Theke, Teller), ohne Nummern-Liste und ohne Pillen.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut fragen-wahl.html (Leiste unten, Pfeiltasten, ?fragen=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/fragen_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, knopf

HIER = bau.HIER

# Frage, kurze Antwort, Antwort, Bild, Stichwort
Q = [
    ('Wie komme ich an einen Platz?', 'Im Vorverkauf.',
     'Tickets gibt es bisher nur im Vorverkauf. Sobald der nächste Abend feststeht, erfahren es die zuerst, die auf der Warteliste stehen.',
     'kerze3', 'Platz'),
    ('Was kostet ein Abend?', '89 Euro.',
     'Zuletzt 89,00 EUR am 25. und 26. September 2026, für den ganzen Abend: drei Gänge, fünf Drinks, Tasting und Schulung.',
     'roq1', 'Preis'),
    ('Wann geht es los?', 'Fr 19, Sa 17 Uhr.',
     'Freitags ab 19 Uhr, samstags ab 17 Uhr. Culinarium gibt es an einzelnen Wochenenden, meist ein Freitag und der Samstag danach.',
     'fassade', 'Beginn'),
    ('Wie viele sind dabei?', 'Vierzehn.',
     'Vierzehn Gäste an einer langen Tafel. Wer zu zweit kommt, sitzt mit anderen am Tisch.',
     'tafelleer', 'Tafel'),
    ('Was gibt es zu essen?', 'Jedes Mal etwas anderes.',
     'Das Menü wechselt mit jedem Abend. Was genau kommt, steht auf der Karte an deinem Platz.',
     'service', 'Menü'),
    ('Kann ich ein Ticket zurückgeben?', 'Leider nein.',
     '„Da die Plätze begrenzt sind, bitten wir um Verständnis, dass Tickets nicht rückerstattet werden können.“',
     'karte', 'Tickets'),
    ('Wo ist das?', 'In Linden.',
     'Im Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover-Linden.',
     'schildtag', 'Ort'),
]
POS = {'p_DbYnkdkjrNy': '50% 50%', 'roq1': '50% 50%', 'fassade': '50% 50%', 'tafelleer': '50% 55%', 'service': '50% 40%',
       'karte': '50% 50%', 'schildtag': '50% 40%', 't03': '50% 40%', 'kerze1': '50% 40%', 'glaeser': '50% 45%', 'kerze2': '50% 40%'}
KNOPF = knopf('Der Abend', 'abend.html')
X = '<i class="fw-x" aria-hidden="true">×</i>'


def bild(b, w=1000, cls='', alt=''):
    return '<img class="%s" src="assets/bild/%s-%d.webp?v=%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        cls, b, w, VERSION, E(alt), POS.get(b, '50% 50%'))


def titel(cls='', satz='Was Gäste vor ihrem ersten Abend wissen wollen.', zwei=False):
    """Überschrift wie überall: rollt aus dem Schlitz; zwei=True setzt «wissen.» in Kerze."""
    h = ('<span class="z"><span style="--i:0">Gut zu</span></span> <span class="z"><span style="--i:1"><em>wissen.</em></span></span>' if zwei
         else '<span class="z"><span style="--i:0">Gut zu wissen.</span></span>')
    return '<div class="fw-tk %s"><h2 class="zl auf titel" aria-label="Gut zu wissen.">%s</h2>%s</div>' % (
        cls, h, '<p class="sw auf fw-satz" style="--i:2">%s</p>' % E(satz) if satz else '')


def wahl(i, inner, tag='button', cls=''):
    """Auslöser für Frage i (Klick zeigt Antwort i)."""
    return '<%s type="button" class="%s%s" data-q="%d">%s</%s>' % (tag, cls, ' an' if i == 0 else '', i, inner, tag)


F = []  # (Name, Inhalt)

# 1 Bild zur Frage: grosses Foto links, das mit jeder Frage wechselt; rechts die Fragen als grosse Zeilen ohne Nummern
F.append(('Bild zur Frage', '<div class="fw-01" data-fw>'
          '<div class="fw-01-bild auf">%s<div class="fw-01-titel">%s</div></div>'
          '<div class="fw-01-r"><div class="fw-01-liste">%s</div><div class="sw auf">%s</div></div></div>' % (
              ''.join('<figure class="fw-01-f%s" data-a="%d">%s</figure>' % (' an' if i == 0 else '', i, bild(q[3], 1600 if q[3] in ('roq1', 'fassade', 'tafelleer', 'service', 'schildtag') else 1000)) for i, q in enumerate(Q)),
              titel(), ''.join('<div class="fw-01-z%s" data-a="%d">%s<p>%s</p></div>' % (
                  ' an' if i == 0 else '', i, wahl(i, '<span>%s</span><i aria-hidden="true"></i>' % E(q[0])), E(q[2])) for i, q in enumerate(Q)), KNOPF)))

# 2 Die Karte am Platz: die gedruckte Karte liegt auf der Tafel, die Fragen stehen darauf wie Gänge
F.append(('Die Karte am Platz', '<div class="fw-02"><div class="fw-02-tisch">%s</div>'
          '<article class="fw-02-karte auf"><p class="fw-02-kopf">Culinarium <span>×</span> Gut zu wissen</p>'
          '<h2 class="fw-02-h">Bevor du kommst</h2><div class="fw-02-gaenge">%s</div>'
          '<p class="fw-02-fuss">Walk on the Wild Side · Haasemannstraße 13 · Hannover-Linden</p></article>'
          '<div class="fw-02-k sw auf">%s</div></div>' % (
              bild('tafelleer', 1600), ''.join('<div class="fw-02-g"><h3>%s</h3><p>%s</p></div>' % (E(q[0]), E(q[2])) for q in Q), KNOPF)))

# 3 Kurz gesagt: jede Antwort in einem Wort, gross gesetzt; darunter klein die ganze Antwort
F.append(('Kurz gesagt', '<div class="fw-03">%s<div class="fw-03-raster">%s</div><div class="sw auf fw-03-k">%s</div></div>' % (
    titel('links', 'Die Antwort zuerst, die Einzelheiten darunter.'),
    ''.join('<div class="fw-03-z"><p class="fw-03-f">%s</p><p class="zl auf fw-03-w"><span class="z"><span style="--i:%d">%s</span></span></p><p class="fw-03-a">%s</p></div>' % (
        E(q[0]), i, E(q[1]), E(q[2])) for i, q in enumerate(Q)), KNOPF)))

# 4 Am Tisch gefragt: die Fragen kommen von Gästen, Momo antwortet; wechselnd links und rechts wie ein Gespräch an der Tafel
F.append(('Am Tisch gefragt', '<div class="fw-04"><div class="fw-04-l">%s<figure class="fw-04-bild auf">%s<figcaption>Momo erklärt am Tisch.</figcaption></figure></div>'
          '<div class="fw-04-gespraech">%s<div class="sw auf">%s</div></div></div>' % (
              titel('links', 'Was am Tisch am häufigsten gefragt wird, und was Momo dann sagt.'), bild('kerze1', 1000),
              ''.join('<div class="fw-04-paar auf" style="--i:%d"><p class="fw-04-gast">%s</p><p class="fw-04-momo"><b>Momo</b>%s</p></div>' % (
                  i, E(q[0]), E(q[2])) for i, q in enumerate(Q)), KNOPF)))

# 5 Das Plakat: der Teil als Plakat des Abends, die Antworten als Plakatzeilen, daneben das echte Plakat
F.append(('Das Plakat', '<div class="fw-05"><div class="fw-05-plakat auf"><p class="fw-05-oben">Culinarium <span>×</span> Walk on the Wild Side</p>'
          '<h2 class="fw-05-h">Gut zu<br>wissen.</h2><div class="fw-05-fakten">%s</div>'
          '<p class="fw-05-klein">Tickets nur im Vorverkauf · nicht rückerstattbar · Menü wechselt jeden Abend · zuerst erfährt es die Warteliste</p></div>'
          '<div class="fw-05-r"><figure class="fw-05-echt auf">%s<figcaption>Das Plakat zum letzten Abend</figcaption></figure><dl class="fw-05-liste">%s</dl><div class="sw auf">%s</div></div></div>' % (
              ''.join('<p><span>%s</span><b>%s</b></p>' % (a, b) for a, b in [('Freitag', 'ab 19'), ('Samstag', 'ab 17'), ('Plätze', '14'), ('Preis', '89 €')]),
              bild('p_DbYnkdkjrNy', 1000), ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (E(q[0]), E(q[2])) for q in Q), KNOPF)))

# 6 Fotoband: sieben hohe Fotos nebeneinander, die Frage unten drauf; antippen dreht das Foto um, hinten steht die Antwort
F.append(('Fotoband', '<div class="fw-06">%s<div class="fw-06-band" data-fw-dreh>%s</div><div class="sw auf fw-06-k">%s</div></div>' % (
    titel('mitte', 'Antippen, und das Bild dreht sich um.'),
    ''.join('<button type="button" class="fw-06-k1 auf" style="--i:%d" aria-label="%s"><span class="fw-06-vorn">%s<b>%s</b></span><span class="fw-06-hinten"><b>%s</b><span>%s</span></span></button>' % (
        i, E(q[0]), bild(q[3], 640), E(q[0]), E(q[1]), E(q[2])) for i, q in enumerate(Q)), KNOPF)))

# 7 Die Tafel von oben: die lange Tafel mit vierzehn Plätzen, auf sieben Tellern liegt je eine Frage; ein Teller antippen, die Antwort steht auf der Tischmitte
def tafel():
    stuehle = ''.join('<span class="fw-07-s" style="--x:%d;--o:%d"></span>' % (i % 7, i // 7) for i in range(14))
    teller = ''.join('<button type="button" class="fw-07-t%s" data-q="%d" style="--x:%d;--o:%d"><span>%s</span></button>' % (
        ' an' if i == 0 else '', i, i, i % 2, E(q[4])) for i, q in enumerate(Q))
    mitte = ''.join('<div class="fw-07-a%s" data-a="%d"><h3>%s</h3><p>%s</p></div>' % (' an' if i == 0 else '', i, E(q[0]), E(q[2])) for i, q in enumerate(Q))
    return '<div class="fw-07-tafel auf" data-fw>%s<div class="fw-07-platte">%s<div class="fw-07-mitte">%s</div><span class="fw-07-kerze k1"></span><span class="fw-07-kerze k2"></span><span class="fw-07-kerze k3"></span></div></div>' % (stuehle, teller, mitte)


F.append(('Die Tafel von oben', '<div class="fw-07">%s%s<div class="sw auf fw-07-k">%s</div></div>' % (
    titel('mitte', 'Vierzehn Plätze, sieben Fragen. Einen Teller antippen.'), tafel(), KNOPF)))

# 8 Die Kreidetafel: an der Wand der Bar hängt die Tafel, Fragen und Antworten stehen darauf wie die Drinks des Abends
F.append(('Die Kreidetafel', '<div class="fw-08"><div class="fw-08-tafel auf"><span class="fw-08-haken" aria-hidden="true"></span>'
          '<h2 class="fw-08-h">Gut zu wissen</h2><p class="fw-08-unter">heute an der Tafel</p><div class="fw-08-spalten">%s</div></div>'
          '<div class="fw-08-r"><figure class="fw-08-bild auf">%s</figure><div class="sw auf">%s</div></div></div>' % (
              ''.join('<div class="fw-08-z"><h3>%s</h3><p>%s</p></div>' % (E(q[0]), E(q[2])) for q in Q), bild('theke', 1000), KNOPF)))

# 9 Das Ticket: links der Abschnitt mit den Fragen, rechts der Hauptteil mit Antwort und Bild; eine Frage antippen, und der Hauptteil wird neu gedruckt
F.append(('Das Ticket', '<div class="fw-09">%s<div class="fw-09-ticket auf" data-fw><div class="fw-09-stub"><p class="fw-09-k">Culinarium · Einlass</p>%s</div>'
          '<div class="fw-09-haupt">%s</div></div><div class="sw auf fw-09-kn">%s</div></div>' % (
              titel('mitte', ''),
              ''.join(wahl(i, E(q[0]), cls='fw-09-q') for i, q in enumerate(Q)),
              ''.join('<div class="fw-09-a%s" data-a="%d"><div class="fw-09-text"><p class="fw-09-k">%s</p><h3>%s</h3><p>%s</p><p class="fw-09-ort">Haasemannstraße 13 · Hannover-Linden</p></div><div class="fw-09-bild">%s</div></div>' % (
                  ' an' if i == 0 else '', i, E(q[4]), E(q[1]), E(q[2]), bild(q[3], 1000)) for i, q in enumerate(Q)), KNOPF)))

# 10 Der Kartenstapel: sieben Karten mit Foto liegen übereinander; antippen legt die oberste nach hinten
F.append(('Der Kartenstapel', '<div class="fw-10"><div class="fw-10-l">%s<p class="fw-10-hinweis">Karte antippen für die nächste Frage.</p><div class="sw auf">%s</div></div>'
          '<div class="fw-10-stapel auf" data-fw-stapel>%s</div></div>' % (
              titel('links', 'Sieben Fragen, sieben Karten.', True), KNOPF,
              ''.join('<button type="button" class="fw-10-karte" style="--p:%d" aria-label="%s">%s<span class="fw-10-text"><b>%s</b><span>%s</span></span></button>' % (
                  i, E(q[0]), bild(q[3], 1000), E(q[0]), E(q[2])) for i, q in enumerate(Q)))))

# 11 Die Zeitung: ein heller Teil wie eine Zeitungsseite, die Frage als fetter Einstieg, die Antwort läuft weiter; ein Foto mit Bildzeile
F.append(('Die Zeitung', '<div class="fw-11"><div class="fw-11-kopf"><p>Culinarium · Ausgabe Herbst 2026</p><p>Hannover-Linden</p></div><span class="fw-11-linie auf"></span>'
          '<h2 class="zl auf fw-11-h" aria-label="Gut zu wissen."><span class="z"><span style="--i:0">Gut zu wissen.</span></span></h2>'
          '<div class="fw-11-spalten"><figure class="fw-11-bild">%s<figcaption>Vierzehn Gäste an einer Tafel, hier im September.</figcaption></figure>%s</div><div class="fw-11-k">%s</div></div>' % (
              bild('t03', 1000), ''.join('<p class="fw-11-p"><b>%s</b> %s</p>' % (E(q[0]), E(q[2])) for q in Q), knopf('Der Abend', 'abend.html', 'hell'))))

# 12 Die Einladung: ein Brief auf hellem Papier, der alles in ganzen Sätzen sagt; die Fragen stehen als Randnotizen daneben
BRIEF = [
    (2, 'Du kommst an einem Freitag ab 19 Uhr oder an einem Samstag ab 17 Uhr. Culinarium gibt es an einzelnen Wochenenden.'),
    (6, 'Wir sind im Walk on the Wild Side, Haasemannstraße 13, in Hannover-Linden.'),
    (3, 'Du sitzt mit dreizehn anderen an einer langen Tafel. Wer zu zweit kommt, lernt also neue Leute kennen.'),
    (4, 'Was es zu essen gibt, steht auf der Karte an deinem Platz. Das Menü wechselt mit jedem Abend.'),
    (1, 'Zuletzt hat der ganze Abend 89 Euro gekostet: drei Gänge, fünf Drinks, Tasting und Schulung.'),
    (0, 'Plätze gibt es nur im Vorverkauf. Wer auf der Warteliste steht, erfährt den nächsten Abend zuerst.'),
    (5, 'Und weil die Plätze so knapp sind, können wir Tickets leider nicht zurücknehmen.'),
]
F.append(('Die Einladung', '<div class="fw-12"><div class="fw-12-l">%s<figure class="fw-12-bild auf">%s</figure></div><div class="fw-12-umschlag"><article class="fw-12-brief auf">'
          '<p class="fw-12-anrede">Liebe Gäste,</p>%s<p class="fw-12-gruss">Bis bald an der Tafel<br><span>Momo, Rudi und Derya</span></p></article></div></div>' % (
              titel('links', 'Alles, was du wissen musst, in einem Brief.', True) + '<div class="sw auf fw-12-k">%s</div>' % KNOPF, bild('glaeser', 1000),
              ''.join('<div class="fw-12-absatz"><span class="fw-12-rand">%s</span><p>%s</p></div>' % (E(Q[n][0]), E(t)) for n, t in BRIEF))))

# 13 Der Drehteller: die Fragen stehen im Kreis um einen Teller; eine antippen, der Teller dreht sie nach oben und die Antwort steht links
F.append(('Der Drehteller', '<div class="fw-13" data-fw data-fw-dreh-teller><div class="fw-13-l">%s<div class="fw-13-mitte">%s</div><div class="sw auf">%s</div></div>'
          '<div class="fw-13-buehne auf"><div class="fw-13-rad">%s<div class="fw-13-teller">%s</div></div></div></div>' % (
              titel('links', 'Eine Frage antippen, der Teller dreht sie zu dir.', True),
              ''.join('<div class="fw-13-a%s" data-a="%d"><b>%s</b><p>%s</p></div>' % (' an' if i == 0 else '', i, E(q[1]), E(q[2])) for i, q in enumerate(Q)), KNOPF,
              ''.join('<button type="button" class="fw-13-q%s" data-q="%d" style="--w:%d"><span>%s</span></button>' % (' an' if i == 0 else '', i, i, E(q[0])) for i, q in enumerate(Q)),
              bild('roq1', 1000))))

# 14 Der Satz: alle Fragen in einem fortlaufenden Satz, getrennt durch das × der Plakate; die gewählte Antwort steht gross darunter
F.append(('Der Satz', '<div class="fw-14" data-fw><p class="fw-14-k1">Gut zu wissen</p><p class="fw-14-satz auf">%s</p><div class="fw-14-antwort">%s</div>'
          '<div class="fw-14-unten"><div class="fw-14-bilder">%s</div><div class="sw auf">%s</div></div></div>' % (
              X.join(wahl(i, E(q[0]), cls='fw-14-q') for i, q in enumerate(Q)),
              ''.join('<div class="fw-14-a%s" data-a="%d"><p>%s</p></div>' % (' an' if i == 0 else '', i, E(q[2])) for i, q in enumerate(Q)),
              ''.join('<figure class="fw-14-b%s" data-a="%d">%s</figure>' % (' an' if i == 0 else '', i, bild(q[3], 640)) for i, q in enumerate(Q)), KNOPF)))

# 15 Die Pinnwand: an der Wand neben der Bar hängen Zettel und Abzüge, jeder Zettel eine Frage mit Antwort; beim Hinscrollen landen sie nacheinander
ZETTEL = [(0, -2.5), (1, 1.8), (2, -1.2), (3, 2.4), (4, -2), (5, 1.4), (6, -1.6)]
F.append(('Die Pinnwand', '<div class="fw-15">%s<div class="fw-15-wand">%s%s</div><div class="sw auf fw-15-k">%s</div></div>' % (
    titel('mitte', 'Was an der Wand neben der Bar hängt.'),
    ''.join('<div class="fw-15-zettel z%d auf" style="--r:%.1fdeg;--i:%d"><span class="fw-15-band"></span><h3>%s</h3><p>%s</p></div>' % (
        i, r, i, E(Q[i][0]), E(Q[i][2])) for i, r in ZETTEL),
    ''.join('<figure class="fw-15-abzug a%d auf" style="--r:%.1fdeg;--i:%d">%s</figure>' % (n, r, 7 + n, bild(b, 640)) for n, (b, r) in enumerate([('kerze2', 3), ('schildtag', -3.5)])),
    KNOPF)))


def main():
    seite = open(os.path.join(HIER, 'index.html')).read()
    m = re.search(r'(<section class="vab v-fragen[^"]*"[^>]*id="fragen"[^>]*>)(<div class="vi h-fragen">.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Gut zu wissen» in index.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab v-fragen', 'data-name="Gut zu wissen" class="vab v-fragen wahl', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv gzw fw-f%02d" data-n="%d" hidden><div class="vi">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Gut zu wissen</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Foto und Karten zum Aufklappen'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('fragen-wahl.css', 'fragen-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["fragen"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/fragen-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Gut zu wissen wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/fragen-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'fragen-wahl.html'), 'w').write(seite)
    print('Seite fragen-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
