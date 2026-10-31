#!/usr/bin/env python3
"""Culinarium Hannover · «Jeder Abend hat sein Plakat» in 15 Fassungen, direkt in der echten Startseite, 27.10.2026.
Robert: «gib 15 visualisierungsmöglichkeiten für den abschnitt alternativ». Heute: grosses neuestes Plakat links, rechts Titel und vier kleine auf einem Brett.
Jede Fassung eine eigene Anordnung aus der Welt der Plakate (Wand, Heft, Regal, Litfasssäule, Leine, Tafel), ohne Nummern-Liste und ohne Pillen.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut plakate-wahl.html (Leiste unten, Pfeiltasten, ?plakate=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/plakate_wahl.py"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, knopf

HIER = bau.HIER
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
KURZ = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']

# Plakate, neuestes zuerst: (Schlüssel, Datum lang, Monat 0–11, Jahr, Preis, Notiz, Akzent)
P = []
for jahr, datum, notiz, preis, pid, _by in [a for a in bau.ABENDE if a[4]][::-1]:
    mo = next(i for i, m in enumerate(MONATE) if m in datum)
    P.append(dict(k='p_' + pid, lang='%s %s' % (datum, jahr), mo=mo, jahr=jahr, preis=preis, notiz=notiz,
                  kurz='%s %s' % (KURZ[mo], jahr), akz=bau.akzent('p_' + pid)))
N = len(P)
JAHRE = sorted({p['jahr'] for p in P}, reverse=True)
SATZ = 'Seit September 2023 bekommt jeder Culinarium-Abend ein eigenes Plakat. Zusammen sehen sie aus wie die Ausgaben eines Magazins.'
KNOPF = knopf('Alle Abende ansehen', 'abende.html')


def hell(hx):
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return .2126 * r + .7152 * g + .0722 * b > .55


def bild(p, w=640, cls=''):
    return '<img class="%s" src="assets/bild/%s-%d.webp?v=%s" alt="Plakat Culinarium, %s" loading="lazy" decoding="async">' % (
        cls, p['k'], w, VERSION, E(p['lang']))


def titel(cls='', satz=SATZ, mit_knopf=True, zwei=True):
    """Überschrift wie überall: rollt aus dem Schlitz; zwei Zeilen, «Plakat.» in Kerze."""
    h = ('<span class="z"><span style="--i:0">Jeder Abend</span></span> <span class="z"><span style="--i:1">hat sein <em>Plakat.</em></span></span>' if zwei
         else '<span class="z"><span style="--i:0">Jeder Abend hat sein <em>Plakat.</em></span></span>')
    return '<div class="pk-tk %s"><h2 class="zl auf titel" aria-label="Jeder Abend hat sein Plakat.">%s</h2>%s%s</div>' % (
        cls, h, '<p class="sw auf pk-satz" style="--i:2">%s</p>' % E(satz) if satz else '',
        '<div class="sw auf pk-kn" style="--i:3">%s</div>' % KNOPF if mit_knopf else '')


def zeile(p, cls='pk-z'):
    """Datum und Preis unter einem Plakat."""
    return '<span class="%s"><b>%s</b><em>%s</em></span>' % (cls, E(p['lang']), E(p['preis']))


def an(i, n=0):
    return ' an' if i == n else ''


F = []  # (Name, Inhalt)

# 1 Die Plakatwand: alle dreizehn übereinander geklebt wie an einer Wand in Linden, das neueste oben drauf
WAND = [(0, 3, -3), (19, 0, 2), (57, 2, -2), (76, 5, 3), (2, 33, 2), (74, 35, -3), (0, 64, -1), (19, 60, 3), (55, 62, -2), (76, 65, 2), (25, 30, -4), (60, 28, 3)]
F.append(('Die Plakatwand', '<div class="pk-01"><div class="pk-01-l">%s</div><div class="pk-01-wand">%s<figure class="pk-01-p gross auf" style="--x:33;--y:17;--w:34;--r:-1;--i:13">%s</figure></div></div>' % (
    titel('links') + '<p class="pk-01-oben"><span class="mono">Ganz oben</span>%s</p>' % zeile(P[0]),
    ''.join('<figure class="pk-01-p auf" style="--x:%d;--y:%d;--w:24;--r:%d;--i:%d">%s</figure>' % (x, y, r, i, bild(P[i + 1])) for i, (x, y, r) in enumerate(WAND)),
    bild(P[0], 1000))))

# 2 Das Zeitband: alle Plakate in einer Reihe zum Wischen, darüber die Jahre auf einer Linie
def band():
    out, vor = [], None
    for i, p in enumerate(P):
        jahr = '<span class="pk-02-jahr">%s</span>' % p['jahr'] if p['jahr'] != vor else ''
        vor = p['jahr']
        out.append('<figure class="pk-02-p%s">%s%s<figcaption>%s</figcaption></figure>' % (' neu' if i == 0 else '', jahr, bild(P[i], 1000 if i == 0 else 640), zeile(p)))
    return ''.join(out)


F.append(('Das Zeitband', '<div class="pk-02"><div class="pk-02-kopf">%s<div class="pk-02-r"><p class="sw auf pk-satz">%s</p><div class="pk-02-kn sw auf">%s<span class="pk-pfeile"><button type="button" data-band="-1" aria-label="Zurück">‹</button><button type="button" data-band="1" aria-label="Weiter">›</button></span></div></div></div>'
          '<div class="pk-02-linie auf"></div><div class="vband pk-02-band">%s</div></div>' % (titel('', '', False), E(SATZ), KNOPF, band())))

# 3 Der Stapel: die Plakate liegen aufeinander wie Hefte; antippen legt das oberste nach hinten
F.append(('Der Stapel', '<div class="pk-03"><div class="pk-03-stapel auf" data-pk-stapel>%s</div><div class="pk-03-r">%s<div class="pk-03-jetzt" aria-live="polite"><span class="mono">Obenauf</span><b data-pk-lang>%s</b><em data-pk-preis>%s</em></div><p class="pk-hinweis">Plakat antippen, das nächste kommt nach oben.</p></div></div>' % (
    ''.join('<button type="button" class="pk-03-p" style="--p:%d" data-lang="%s" data-preis="%s" aria-label="Nächstes Plakat">%s</button>' % (
        i, E(p['lang']), E(p['preis']), bild(p, 1000)) for i, p in enumerate(P)),
    titel('links'), E(P[0]['lang']), E(P[0]['preis']))))

# 4 Das Heft: links das Titelblatt gross, rechts das Inhaltsverzeichnis aller Ausgaben; eine Zeile antippen wechselt das Titelblatt
F.append(('Das Heft', '<div class="pk-04" data-pk><figure class="pk-04-cover auf">%s</figure><div class="pk-04-r">%s<p class="pk-04-k mono">In diesem Heft</p><div class="pk-04-inhalt">%s</div><div class="sw auf">%s</div></div></div>' % (
    ''.join('<span class="pk-04-b%s" data-a="%d">%s</span>' % (an(i), i, bild(p, 1000)) for i, p in enumerate(P)),
    titel('links', SATZ, False),
    ''.join('<button type="button" class="pk-04-z%s" data-q="%d"><span>%s</span><em>%s</em></button>' % (an(i), i, E(p['lang']), E(p['preis'])) for i, p in enumerate(P)), KNOPF)))

# 5 Der Zeitschriftenständer: drei Fächer aus Holz, die Plakate stecken darin, auf der Kante steht das Datum
FAECHER = [P[0:5], P[5:9], P[9:13]]
F.append(('Der Zeitschriftenständer', '<div class="pk-05">%s<div class="pk-05-staender">%s</div></div>' % (
    titel('mitte'),
    ''.join('<div class="pk-05-fach auf" style="--i:%d"><div class="pk-05-reihe">%s</div><span class="pk-05-kante"></span></div>' % (
        f, ''.join('<figure class="pk-05-p">%s<figcaption>%s</figcaption></figure>' % (bild(p), E(p['kurz'])) for p in reihe)) for f, reihe in enumerate(FAECHER)))))

# 6 Jahrgänge: je Jahr eine Reihe, die Jahreszahl gross davor, wie die Jahrgänge eines Magazins im Archiv
F.append(('Jahrgänge', '<div class="pk-06">%s<div class="pk-06-jahre">%s</div></div>' % (
    titel('links'),
    ''.join('<div class="pk-06-jg auf" style="--i:%d"><p class="pk-06-zahl">%s<span>%d %s</span></p><div class="pk-06-reihe">%s</div></div>' % (
        j, jahr, len([p for p in P if p['jahr'] == jahr]), 'Abende' if len([p for p in P if p['jahr'] == jahr]) > 1 else 'Abend',
        ''.join('<figure class="pk-06-p">%s<figcaption>%s</figcaption></figure>' % (bild(p), zeile(p)) for p in P if p['jahr'] == jahr))
        for j, jahr in enumerate(JAHRE)))))

# 7 Der Fächer: alle Plakate aufgefächert wie Karten in der Hand; eins antippen holt es nach vorn
ALT = P[::-1]  # links das älteste
F.append(('Der Fächer', '<div class="pk-07" data-pk>%s<div class="pk-07-buehne"><div class="pk-07-faecher auf">%s</div></div><div class="pk-07-unten"><div class="pk-07-zeilen" aria-live="polite">%s</div><div class="sw auf">%s</div></div></div>' % (
    titel('mitte', SATZ, False),
    ''.join('<button type="button" class="pk-07-p%s" data-q="%d" style="--w:%d;--z:%d" aria-label="%s">%s</button>' % (
        an(i, N - 1), i, i - (N - 1) // 2, i, E(p['lang']), bild(p, 1000 if i == N - 1 else 640)) for i, p in enumerate(ALT)),
    ''.join('<p class="pk-07-a%s" data-a="%d">%s</p>' % (an(i, N - 1), i, zeile(p, 'pk-z gross')) for i, p in enumerate(ALT)), KNOPF)))

# 8 Die Farbe des Abends: ein Plakat gross, die ganze Fläche nimmt seine Farbe an; unten die Abende zum Wählen
F.append(('Die Farbe des Abends', '<div class="pk-08" data-pk><div class="pk-08-flaeche auf">%s<div class="pk-08-innen"><figure class="pk-08-plakat">%s</figure><div class="pk-08-r">%s<div class="pk-08-jetzt">%s</div></div></div><div class="pk-08-wahl">%s</div></div></div>' % (
    ''.join('<span class="pk-08-farbe%s" data-a="%d" style="--akz:%s"></span>' % (an(i), i, p['akz']) for i, p in enumerate(P)),
    ''.join('<span class="pk-08-b%s" data-a="%d">%s</span>' % (an(i), i, bild(p, 1000)) for i, p in enumerate(P)),
    titel('links'),
    ''.join('<p class="pk-08-a%s" data-a="%d">%s</p>' % (an(i), i, zeile(p, 'pk-z gross')) for i, p in enumerate(P)),
    ''.join('<button type="button" class="pk-08-q%s" data-q="%d" style="--akz:%s">%s</button>' % (an(i), i, p['akz'], E(p['kurz'])) for i, p in enumerate(P)))))

# 9 Der Wandkalender: vier Jahre, zwölf Monate; wo ein Abend war, hängt sein Plakat. Antippen zeigt es gross
def kalender():
    nach = {(p['jahr'], p['mo']): i for i, p in enumerate(P)}
    kopf = '<div class="pk-09-zeile kopf"><span></span>%s</div>' % ''.join('<span>%s</span>' % m[0] for m in MONATE)
    reihen = []
    for jahr in JAHRE:
        zellen = []
        for mo in range(12):
            i = nach.get((jahr, mo))
            zellen.append('<button type="button" class="pk-09-zelle voll%s" data-q="%d" aria-label="%s">%s</button>' % (an(i), i, E(P[i]['lang']), bild(P[i]))
                          if i is not None else '<span class="pk-09-zelle"></span>')
        reihen.append('<div class="pk-09-zeile"><span class="pk-09-jahr">%s</span>%s</div>' % (jahr, ''.join(zellen)))
    return kopf + ''.join(reihen)


F.append(('Der Wandkalender', '<div class="pk-09" data-pk><figure class="pk-09-gross auf">%s<figcaption>%s</figcaption></figure><div class="pk-09-r">%s<div class="pk-09-kal auf">%s</div></div></div>' % (
    ''.join('<span class="pk-09-b%s" data-a="%d">%s</span>' % (an(i), i, bild(p, 1000)) for i, p in enumerate(P)),
    ''.join('<span class="pk-09-a%s" data-a="%d">%s</span>' % (an(i), i, zeile(p)) for i, p in enumerate(P)),
    titel('links'), kalender())))

# 10 Die Litfasssäule: die Plakate in zwei Reihen rund um eine Säule geklebt (das neueste zweimal, damit die Säule voll ist); beim Scrollen dreht sie sich weiter
F.append(('Die Litfasssäule', '<div class="pk-10">%s<div class="pk-10-buehne auf" data-pk-saeule><div class="pk-10-skala"><span class="pk-10-hut"></span><div class="pk-10-ring">%s</div><span class="pk-10-fuss"></span></div></div></div>' % (
    titel('links'),
    ''.join('<figure class="pk-10-p" style="--n:%d;--e:%d">%s</figure>' % (i % 7, i // 7, bild(p)) for i, p in enumerate(P + P[:1])))))

# 11 Durchblättern: der Teil bleibt stehen, beim Scrollen blättern die Ausgaben von der neuesten zur ersten
F.append(('Durchblättern', '<div class="pk-11" data-pk-blaettern style="--n:%d"><div class="pk-11-buehne"><figure class="pk-11-plakat">%s</figure><div class="pk-11-r">%s<div class="pk-11-jetzt">%s</div><div class="pk-11-lauf"><span class="pk-11-strich"></span><span class="mono pk-11-von"><span>%s</span><span>September 2023</span></span></div></div></div></div>' % (
    N, ''.join('<span class="pk-11-b%s" data-a="%d">%s</span>' % (an(i), i, bild(p, 1000)) for i, p in enumerate(P)),
    titel('links'),
    ''.join('<p class="pk-11-a%s" data-a="%d">%s</p>' % (an(i), i, zeile(p, 'pk-z gross')) for i, p in enumerate(P)), MONATE[P[0]['mo']] + ' ' + P[0]['jahr'])))

# 12 Die Rücken im Regal: die Ausgaben stehen im Regal, man sieht nur die Rücken in ihrer Farbe; einen antippen zieht das Heft heraus
F.append(('Die Rücken im Regal', '<div class="pk-12" data-pk><figure class="pk-12-cover auf">%s<figcaption>%s</figcaption></figure><div class="pk-12-r">%s<div class="pk-12-regal auf">%s<span class="pk-12-brett"></span></div></div></div>' % (
    ''.join('<span class="pk-12-b%s" data-a="%d">%s</span>' % (an(i), i, bild(p, 1000)) for i, p in enumerate(P)),
    ''.join('<span class="pk-12-a%s" data-a="%d">%s</span>' % (an(i), i, zeile(p)) for i, p in enumerate(P)),
    titel('links'),
    ''.join('<button type="button" class="pk-12-ruecken%s%s" data-q="%d" style="--akz:%s;--h:%d" aria-label="%s"><span class="pk-12-wm">Culinarium</span><span class="pk-12-d">%s</span></button>' % (
        an(i), ' dunkel' if hell(p['akz']) else '', i, p['akz'], [100, 94, 97, 92, 99, 95, 100, 93, 96, 98, 94, 100, 95][i], E(p['lang']), E(p['kurz'])) for i, p in enumerate(P)))))

# 13 Die Leine: die Plakate hängen mit Klammern an zwei Leinen quer durch den Raum
def leine(teil, start):
    n = len(teil)
    out = []
    for j, p in enumerate(teil):
        t = (j + .5) / n
        out.append('<figure class="pk-13-p" style="--t:%.4f;--y:%.1f;--r:%.2f;--s:%d;--i:%d"><span class="pk-13-klammer"></span>%s<figcaption>%s</figcaption></figure>' % (
            t, 10 + 160 * t * (1 - t), 5 * (1 - 2 * t), 1 if (start + j) % 2 else -1, j, bild(p), E(p['kurz'])))
    return '<div class="pk-13-leine auf"><svg viewBox="0 0 1000 100" preserveAspectRatio="none" aria-hidden="true"><path d="M0,10 Q500,170 1000,10"/></svg>%s</div>' % ''.join(out)


F.append(('Die Leine', '<div class="pk-13">%s%s%s</div>' % (titel('mitte'), leine(P[:7], 0), leine(P[7:], 7))))

# 14 Die Salonhängung: gerahmt und dicht an dicht wie in einem alten Salon, das neueste in der Mitte am grössten
SALON = [(38, 9, 24), (21, 5, 14), (65, 5, 14), (5, 10, 13), (82, 10, 13), (21, 22, 14), (65, 22, 14), (38, 36, 11), (51, 36, 11), (5, 27, 13), (82, 27, 13), (21, 39, 14), (65, 39, 14)]
F.append(('Die Salonhängung', '<div class="pk-14">%s<div class="pk-14-wand">%s</div><p class="pk-14-schild">Ganz in der Mitte: %s</p></div>' % (
    titel('mitte'),
    ''.join('<figure class="pk-14-rahmen auf%s" style="--x:%d;--y:%d;--w:%d;--i:%d">%s</figure>' % (' mitte' if i == 0 else '', x, y, w, i, bild(P[i], 1000 if i == 0 else 640))
            for i, (x, y, w) in enumerate(SALON)), E(P[0]['lang']))))

# 15 Die Untersetzer: auf der langen Tafel liegen die Plakate wie Bierdeckel verstreut
DECKEL = [(42, 30, 22, -6), (8, 52, 16, 9), (24, 18, 15, -12), (66, 16, 16, 7), (80, 46, 15, -4), (62, 58, 17, 14), (30, 64, 15, -9), (6, 14, 14, 4), (86, 8, 13, -10), (48, 74, 14, 5), (14, 80, 13, -3), (74, 80, 14, 11), (90, 70, 12, -7)]
F.append(('Die Untersetzer', '<div class="pk-15"><div class="pk-15-tisch auf"><img class="pk-15-foto" src="assets/bild/tafelleer-1600.webp?v=%s" alt="" loading="lazy" decoding="async">'
          '<div class="pk-15-kopf">%s</div><div class="pk-15-ebene"><div class="pk-15-platte">%s</div></div></div></div>' % (
              VERSION, titel('links'),
              ''.join('<figure class="pk-15-d" style="--x:%d;--y:%d;--w:%d;--r:%d;--i:%d">%s</figure>' % (x, y, w, r, i, bild(P[i], 1000 if i == 0 else 640))
                      for i, (x, y, w, r) in enumerate(DECKEL)))))


def main():
    seite = open(os.path.join(HIER, 'index.html')).read()
    m = re.search(r'(<section class="vab v-plakate[^"]*"[^>]*id="plakate"[^>]*>)(<div class="vi gr">.*?)(<p class="ueber.*?</section>)', seite, re.S)
    assert m, 'Teil «Die Plakate» in index.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab v-plakate', 'data-name="Die Plakate" class="vab v-plakate wahl', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv plw pk-f%02d" data-n="%d" hidden><div class="vi">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Die Plakate</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: neuestes gross, vier auf dem Brett'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('plakate-wahl.css', 'plakate-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["plakate"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/plakate-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Plakate wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/plakate-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'plakate-wahl.html'), 'w').write(seite)
    print('Seite plakate-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
