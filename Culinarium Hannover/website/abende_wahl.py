#!/usr/bin/env python3
"""Culinarium Hannover · «Alle Abende» (abende.html, Teil mit den Jahren) in 15 Fassungen, 27.10.2026.
Robert: «15 visuelle Alternativen … nicht dass das alles so ein Stapel wird, sondern dass alles seinen Raum hat, luxuriös, elegant und edel».
Keine Fassung wiederholt eine der Runden zu Plakaten und Chronik (plakate_wahl.py, chronik_wahl.py, chronik_wahl2.py).
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut abende-wahl.html (Leiste unten, Pfeiltasten, ?jahre=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/abende_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, marke

HIER = bau.HIER
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
ZAHL = {1: 'Ein Abend', 2: 'Zwei Abende', 3: 'Drei Abende', 4: 'Vier Abende', 5: 'Fünf Abende'}

# Alle Abende, neuestes zuerst; der Abend im September 2023 ohne Plakat bekommt die Wortmarke
A = []
for jahr, datum, notiz, preis, pid, mit in bau.ABENDE[::-1]:
    A.append(dict(k=('p_' + pid) if pid else None, jahr=jahr, datum=datum, lang='%s %s' % (datum, jahr), preis=preis, notiz=notiz,
                  mit=mit.replace('BY ', 'by ').replace('MOMO', 'Momo').replace('RUDI', 'Rudi').replace('CHRISTOPH', 'Christoph').replace(' X ', ' x '),
                  akz=bau.akzent('p_' + pid) if pid else '#B15736', id=pid or 'ohne-%s' % jahr))
JAHRE = ['2026', '2025', '2024', '2023']
JA = {j: [a for a in A if a['jahr'] == j] for j in JAHRE}


def bild(a, w=640, cls=''):
    if not a['k']:
        return '<div class="aw-ohne %s">%s</div>' % (cls, marke('wm'))
    return '<img class="%s" src="assets/bild/%s-%d.webp?v=%s" alt="Plakat Culinarium, %s" loading="lazy" decoding="async">' % (
        cls, a['k'], w, VERSION, E(a['lang']))


def mono(a):
    return E(a['preis']) + (' · ' + E(a['notiz']) if a['notiz'] else '')


def info(a, cls='', jahr=True):
    return '<div class="aw-info %s"><p class="aw-datum">%s</p><p class="aw-mono">%s</p><p class="aw-mit">%s</p></div>' % (
        cls, E(a['lang'] if jahr else a['datum']), mono(a), E(a['mit']))


def mit_jahr(j):
    m = sorted({a['mit'] for a in JA[j]}, key=lambda x: -len(x))
    return ' · '.join(E(x) for x in m)


F = []  # (Name, Inhalt)

# 1 Der Ausstellungsraum: je Abend eine Wand, das Plakat gross, daneben der Wandtext wie im Museum; Seiten im Wechsel
F.append(('Der Ausstellungsraum', '<div class="aw01">%s</div>' % ''.join(
    '<article class="aw01-w" id="x1-%s"><figure class="aw01-p auf">%s</figure><div class="aw01-t auf"><span class="aw-jahrklein">%s</span>%s</div></article>' % (
        a['id'], bild(a, 1000), a['jahr'], info(a, 'gross')) for a in A)))

# 2 Das Passepartout: jedes Plakat gerahmt mit breitem Rand, darunter ein graviertes Schild; drei je Reihe, viel Luft
def pp():
    out = []
    for j in JAHRE:
        out.append('<div class="aw02-jahr"><span>%s</span></div>' % j)
        out += ['<figure class="aw02-r auf" style="--i:%d"><div class="aw02-rahmen"><div class="aw02-matte">%s</div></div><figcaption class="aw02-schild">%s</figcaption></figure>' % (
            i, bild(a), info(a)) for i, a in enumerate(JA[j])]
    return ''.join(out)


F.append(('Das Passepartout', '<div class="aw02">%s</div>' % pp()))

# 3 Die Weinkarte: links steht das Plakat gross, rechts die Abende wie auf einer Weinkarte, nach Jahrgang; Zeile zeigt Plakat
def karte():
    out = []
    i = 0
    for j in JAHRE:
        z = []
        for a in JA[j]:
            z.append('<button type="button" class="aw03-z%s" data-q="%d"><span class="aw03-mob">%s</span><span class="aw03-l"><b>%s</b><i></i><em>%s</em></span><span class="aw03-u">%s%s</span></button>' % (
                ' an' if i == 0 else '', i, bild(a), E(a['datum']), E(a['preis']), E(a['mit']), (' · ' + E(a['notiz'])) if a['notiz'] else ''))
            i += 1
        out.append('<div class="aw03-jg"><p class="aw03-jahr"><span>Jahrgang</span>%s</p>%s</div>' % (j, ''.join(z)))
    return ''.join(out)


F.append(('Die Weinkarte', '<div class="aw03" data-aw><div class="aw03-bild"><div class="aw03-rahmen auf">%s</div><p class="aw03-unter" aria-live="polite">%s</p></div><div class="aw03-liste">%s</div></div>' % (
    ''.join('<span class="aw03-b%s" data-a="%d">%s</span>' % (' an' if i == 0 else '', i, bild(a, 1000)) for i, a in enumerate(A)),
    ''.join('<span class="aw03-a%s" data-a="%d">%s</span>' % (' an' if i == 0 else '', i, E(a['lang'])) for i, a in enumerate(A)),
    karte())))

# 4 Die Menükarten: jedes Plakat mit seiner gedruckten Karte daneben, zwei je Reihe
F.append(('Die Menükarten', '<div class="aw04">%s</div>' % ''.join(
    '<article class="aw04-k auf" style="--i:%d;--akz:%s"><figure class="aw04-p">%s</figure><div class="aw04-karte"><span class="aw04-kopf">Culinarium · %s</span><span class="aw04-orn"></span>'
    '<p class="aw04-d">%s</p><p class="aw04-satz">Ein Abend an der Tafel</p><span class="aw04-orn"></span><p class="aw-mono">%s</p><p class="aw-mit">%s</p></div></article>' % (
        i % 2, a['akz'], bild(a), a['jahr'], E(a['datum']), mono(a), E(a['mit'])) for i, a in enumerate(A))))

# 5 Der rote Faden: eine Linie in Kerze läuft mit dem Scrollen nach unten, die Abende links und rechts davon
def faden():
    out, vor, s = [], None, 0
    for a in A:
        if a['jahr'] != vor:
            out.append('<p class="aw05-jahr"><span>%s</span></p>' % a['jahr'])
            vor = a['jahr']
        out.append('<article class="aw05-a %s auf"><figure class="aw05-p">%s</figure>%s</article>' % ('l' if s % 2 == 0 else 'r', bild(a), info(a, '', False)))
        s += 1
    return ''.join(out)


F.append(('Der rote Faden', '<div class="aw05" data-aw-faden><span class="aw05-linie"><i></i></span>%s</div>' % faden()))

# 6 Die Bühne: jeder Abend bekommt seine eigene Bühne in der Farbe seines Plakats
F.append(('Die Bühne', '<div class="aw06 aw-voll">%s</div>' % ''.join(
    '<article class="aw06-b" style="--akz:%s"><p class="aw06-jahr">%s</p><figure class="aw06-p auf">%s</figure>%s</article>' % (
        a['akz'], a['jahr'], bild(a, 1000), info(a, 'mitte', False)) for a in A)))

# 7 Die Nischen: ein dunkler Saal, jedes Plakat in einer gewölbten Nische mit eigenem Licht
def nischen():
    out = []
    for j in JAHRE:
        out.append('<p class="aw07-jahr"><span>%s</span></p>' % j)
        out += ['<figure class="aw07-n auf" style="--i:%d"><div class="aw07-bogen"><span class="aw07-licht"></span><div class="aw07-p">%s</div></div><figcaption>%s</figcaption></figure>' % (
            i, bild(a), info(a, 'mitte', False)) for i, a in enumerate(JA[j])]
    return ''.join(out)


F.append(('Die Nischen', '<div class="aw07 aw-voll"><div class="aw07-saal">%s</div></div>' % nischen()))

# 8 Das Buch der Abende: je Jahr eine Doppelseite, links das Jahr, rechts seine Plakate
F.append(('Das Buch der Abende', '<div class="aw08">%s</div>' % ''.join(
    '<div class="aw08-dop"><div class="aw08-links"><p class="aw08-jahr">%s</p><p class="aw08-zahl">%s</p><p class="aw-mit">%s</p></div>'
    '<div class="aw08-rechts auf"><div class="aw08-raster n%d">%s</div></div></div>' % (
        j, ZAHL[len(JA[j])], mit_jahr(j), len(JA[j]), ''.join('<figure class="aw08-p">%s%s</figure>' % (bild(a), info(a, '', False)) for a in JA[j])) for j in JAHRE)))

# 9 Die Vitrinen: je Jahr eine Vitrine, die Plakate stehen auf einem Glasboden und spiegeln sich
F.append(('Die Vitrinen', '<div class="aw09">%s</div>' % ''.join(
    '<div class="aw09-v"><div class="aw09-glas"><div class="aw09-reihe n%d">%s</div></div><div class="aw09-sockel"><span class="aw09-jahr">%s</span><span class="aw-mit">%s</span></div></div>' % (
        len(JA[j]), ''.join('<figure class="aw09-p auf" style="--i:%d"><div class="aw09-bild">%s<span class="aw09-spiegel" aria-hidden="true">%s</span></div><figcaption>%s</figcaption></figure>' % (
            i, bild(a), bild(a), info(a, 'mitte', False)) for i, a in enumerate(JA[j])), j, mit_jahr(j)) for j in JAHRE)))

# 10 Die Jahresreihen: je Jahr eine Reihe zum Wischen, das Jahr bleibt links stehen
F.append(('Die Jahresreihen', '<div class="aw10">%s</div>' % ''.join(
    '<div class="aw10-r"><div class="aw10-kopf"><p class="aw10-jahr">%s</p><p class="aw10-zahl">%s</p><span class="aw10-pfeile"><button type="button" data-reihe="-1" aria-label="Zurück">‹</button><button type="button" data-reihe="1" aria-label="Weiter">›</button></span></div>'
    '<div class="aw10-band auf">%s</div></div>' % (
        j, ZAHL[len(JA[j])], ''.join('<figure class="aw10-p">%s%s</figure>' % (bild(a, 1000), info(a, '', False)) for a in JA[j])) for j in JAHRE)))

# 11 Die Einladungen: jedes Plakat als Karte, die aus ihrem Umschlag in der Farbe des Abends steigt
F.append(('Die Einladungen', '<div class="aw11">%s</div>' % ''.join(
    '<figure class="aw11-e auf" style="--i:%d;--akz:%s"><div class="aw11-umschlag"><span class="aw11-hinten"></span><div class="aw11-karte">%s</div><span class="aw11-vorn"></span></div><figcaption>%s</figcaption></figure>' % (
        i % 3, a['akz'], bild(a), info(a)) for i, a in enumerate(A))))

# 12 Die Bildstrecke: wie eine Strecke im Magazin, gross und klein im Wechsel, versetzt, mit viel Weiss
STRECKE = [(0, 7, 0), (8, 4, 22), (2, 4, 0), (7, 6, 10), (0, 5, 6), (6, 6, 0), (1, 6, 0), (8, 4, 16), (3, 5, 0), (9, 4, 8), (0, 6, 0), (7, 5, 14), (2, 5, 0), (8, 4, 4)]
F.append(('Die Bildstrecke', '<div class="aw12">%s</div>' % ''.join(
    '<figure class="aw12-p auf" style="--c:%d;--w:%d;--m:%d">%s%s<figcaption>%s</figcaption></figure>' % (
        c + 1, w, m, '<span class="aw12-jahr">%s</span>' % a['jahr'] if i == 0 or A[i - 1]['jahr'] != a['jahr'] else '', bild(a, 1000 if w >= 6 else 640), info(a, '', False))
    for i, (a, (c, w, m)) in enumerate(zip(A, STRECKE)))))

# 13 Die Kapitel: jedes Jahr beginnt mit einem dunklen Titelblatt, danach seine Plakate gross zu zweit
F.append(('Die Kapitel', '<div class="aw13 aw-voll">%s</div>' % ''.join(
    '<div class="aw13-k"><div class="aw13-titel"><p class="aw13-jahr auf"><span>%s</span></p><p class="aw13-zeile">%s · %s</p></div><div class="aw13-raster">%s</div></div>' % (
        j, ZAHL[len(JA[j])], mit_jahr(j), ''.join('<figure class="aw13-p auf" style="--i:%d">%s%s</figure>' % (i % 2, bild(a, 1000), info(a, '', False)) for i, a in enumerate(JA[j]))) for j in JAHRE)))

# 14 Der Planschrank: Plakate liegen flach in den Schubladen eines Planschranks, eine je Jahr; aufziehen zeigt sie
F.append(('Der Planschrank', '<div class="aw14">%s</div>' % ''.join(
    '<div class="aw14-lade%s"><button type="button" class="aw14-front" data-lade aria-expanded="%s"><span class="aw14-halter"><b>%s</b><em>%s</em></span><span class="aw14-griff"></span><span class="aw14-mit">%s</span></button>'
    '<div class="aw14-innen"%s><div class="aw14-boden n%d">%s</div></div></div>' % (
        ' offen' if n == 0 else '', 'true' if n == 0 else 'false', j, ZAHL[len(JA[j])], mit_jahr(j), '' if n == 0 else ' hidden', len(JA[j]),
        ''.join('<figure class="aw14-p auf" style="--i:%d">%s%s</figure>' % (i, bild(a), info(a, '', False)) for i, a in enumerate(JA[j]))) for n, j in enumerate(JAHRE))))

def tage(d):
    """«Fr 25. und Sa 26. September» › «25./26. September», «Sa 21. Oktober» › «21. Oktober»."""
    m = re.match(r'\w+ (\d+)\. und \w+ (\d+)\. (\w+)', d)
    return '%s./%s. %s' % m.groups() if m else re.sub(r'^\w+ ', '', d)


# 15 Eins nach dem anderen: ein Plakat gross auf der Staffelei, daneben alle Daten zum Antippen
def daten():
    out, i = [], 0
    for j in JAHRE:
        z = []
        for a in JA[j]:
            z.append('<button type="button" class="aw15-d%s" data-q="%d">%s</button>' % (' an' if i == 0 else '', i, E(tage(a['datum']))))
            i += 1
        out.append('<div class="aw15-j"><span>%s</span>%s</div>' % (j, ''.join(z)))
    return ''.join(out)


F.append(('Eins nach dem anderen', '<div class="aw15" data-aw><div class="aw15-buehne auf">%s</div><div class="aw15-r"><div class="aw15-text">%s</div>'
          '<div class="aw15-schritte"><button type="button" data-schritt="-1" aria-label="Voriger Abend">‹</button><button type="button" data-schritt="1" aria-label="Nächster Abend">›</button></div><div class="aw15-daten">%s</div></div></div>' % (
              ''.join('<span class="aw15-b%s" data-a="%d">%s</span>' % (' an' if i == 0 else '', i, bild(a, 1000)) for i, a in enumerate(A)),
              ''.join('<div class="aw15-a%s" data-a="%d"><span class="aw-jahrklein">%s</span>%s</div>' % (' an' if i == 0 else '', i, a['jahr'], info(a, 'gross', False)) for i, a in enumerate(A)),
              daten())))


def main():
    seite = open(os.path.join(HIER, 'abende.html')).read()
    m = re.search(r'(<section class="jahre" data-ton="hell">)(<div class="alle-karten.*?)(<p class="jahre-hinweis.*?</section>)', seite, re.S)
    assert m, 'Teil «Jahre» in abende.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = '<section class="jahre wahl" data-ton="hell" id="jahre" data-name="Alle Abende">'
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv awv aw-f%02d" data-n="%d" hidden>%s</div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Alle Abende</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: fünf je Reihe, Jahr als Kachel'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('abende-wahl.css', 'abende-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["jahre"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/abende-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Alle Abende wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/abende-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'abende-wahl.html'), 'w').write(seite)
    print('Seite abende-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
