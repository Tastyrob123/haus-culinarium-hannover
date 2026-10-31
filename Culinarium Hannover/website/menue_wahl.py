#!/usr/bin/env python3
"""Culinarium Hannover · «Was auf den Tisch kommt» (Seite Der Abend) in 15 Fassungen, direkt in der echten Seite, 27.10.2026.
Robert: «gib mir 15 visuelle darstellungsmöglichkeiten um diese abschnitte alternativ darzustellen». Heute: Karte schräg auf Foto links, rechts Titel, Satz, zwei Fotos.
Gezogen mit der Entwurfs-Maschine (essen), jede Fassung mit `pruefen` gegen alle Häuser durch (höchstens 24 % gleich).
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut menue-wahl.html (Leiste unten, Pfeiltasten, ?tisch=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/bau.py && python3 website/menue_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, zl, marke

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json')))

TITEL = ['Was auf den', 'Tisch kommt.']
SATZ = ('Das Menü ändert sich mit jedem Abend. Rudi kocht drei Gänge, Momo stellt zu jedem einen eigenen Drink dazu, '
        'zum Ankommen gibt es einen Aperitif. Was genau auf den Tisch kommt, steht auf der Karte an deinem Platz.')
ZEILE = 'AUBERGINE / KOKOS / LIMETTE / SESAM'
FUSS = 'Momo erklärt jeden Drink persönlich.'
# Teil, Unterzeile, Bild, Glas oder Detail dazu (Beitrag DbYnkdkjrNy, Aperitif C56bJeds8PF, Rudis Zeile De1pn9ttMoX)
T = [
    ('Aperitif', 'zum Ankommen', 'toast', 'glaeser'),
    ('Drei Gänge', 'von Rudi, zuletzt zum Beispiel', 'beete', 'roq1'),
    ('Fünf Drinks', 'Momos Signature Drinks, passend zum Essen', 'g1', 'beeteglas'),
    ('Tasting und Schulung', 'Fatwashing, Milkwashing, Klärung mit Enzymen', 'klaeren', 'schaum'),
]


def bild(k, w=1000, cls='', pos='50% 50%', alt=None):
    st = [s for s in META[k]['stufen'] if s <= w] or META[k]['stufen'][:1]
    return '<img class="%s" src="assets/bild/%s-%d.webp?v=%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        cls, k, st[-1], VERSION, E(alt if alt is not None else bau.BILD[k][2]), pos)


def titel(cls='', satz=True, i=0):
    return '<div class="mw-tk %s">%s%s</div>' % (cls, zl(TITEL, 'h2', 'mw-h'), '<p class="sw auf mw-satz" style="--i:2">%s</p>' % SATZ if satz else '')


def unter(t):
    """Unterzeile eines Teils; bei den Gängen mit Rudis Zeile."""
    return E(t[1]) + ('<span class="mw-zeile">%s</span>' % ZEILE if t[0] == 'Drei Gänge' else '')


def karte(cls=''):
    """Die gedruckte Karte des Abends, wie heute."""
    return ('<div class="mw-karte %s"><div class="mw-rahmen"><div class="mw-marke">%s</div><p class="mw-mit">A UNiQUE EXPERiENCE BY MOMO X RUDI</p>%s'
            '<p class="mw-kfuss">%s</p></div></div>') % (
        cls, marke('wm'), ''.join('<div class="mw-gang" data-g="%d"><h3>%s</h3><p>%s</p></div>' % (i, E(t[0]), unter(t)) for i, t in enumerate(T)), E(FUSS))


X = '<i class="mw-x" aria-hidden="true">×</i>'
F = []  # (Name, Inhalt)

# 1 Fotos im Satz: der Abend als ein grosser Satz, kleine Fotos sitzen zwischen den Wörtern und öffnen sich; darunter Karte am Tisch und Text
F.append(('Fotos im Satz', '<div class="mw01"><p class="mw01-satz">Zum Ankommen ein Aperitif <span class="mw01-f auf" style="--i:0">%s</span> '
          'dann drei Gänge <span class="mw01-f auf" style="--i:1">%s</span> aus Rudis Küche, zu jedem ein eigener Drink <span class="mw01-f auf" style="--i:2">%s</span> '
          'von Momo, und er erklärt dir, wie er gemacht ist <span class="mw01-f auf" style="--i:3">%s</span></p>'
          '<div class="mw01-unten"><figure class="mw01-gross auf">%s</figure>%s<figure class="mw01-gross b auf">%s</figure></div></div>' % (
              bild('glaeser', 640), bild('roq1', 640), bild('g1', 640), bild('klaeren', 640), bild('kartglas', 1000), titel('mw01-t'), bild('anstossen', 1000))))

# 2 Teller und Glas: vier Teile antippen, rechts wendet sich das Paar (Teller | Glas), Naht in Kerze
F.append(('Teller und Glas', '<div class="mw02" data-mw><div class="mw02-l">%s<div class="mw02-namen">%s</div></div><div class="mw02-paare auf">%s</div></div>' % (
    titel(),
    ''.join('<button type="button" class="mw02-n%s" data-q="%d"><b>%s</b><span>%s</span></button>' % (' an' if i == 0 else '', i, E(t[0]), unter(t)) for i, t in enumerate(T)),
    ''.join('<div class="mw02-paar%s" data-a="%d"><figure class="mw02-a">%s</figure><figure class="mw02-b">%s</figure></div>' % (
        ' an' if i == 0 else '', i, bild(t[2], 1000), bild(t[3], 1000)) for i, t in enumerate(T)))))

# 3 Dein Platz: der gedeckte Platz von oben, Glas, Teller, Karte und Drink landen nacheinander; antippen erklärt
PLATZ = [('Aperitif', 'glaeser', 'p-ap', 0), ('Drei Gänge', 'r10', 'p-te', 1), ('Fünf Drinks', 'g1', 'p-gl', 2), ('Tasting und Schulung', 'klaeren', 'p-ta', 3)]
F.append(('Dein Platz', '<div class="mw03" data-mw><div class="mw03-tisch auf">%s<div class="mw03-karte-o" style="--i:4">%s</div><span class="mw03-besteck b1"></span><span class="mw03-besteck b2"></span></div>'
          '<div class="mw03-r">%s<div class="mw03-text">%s</div></div></div>' % (
              ''.join('<button type="button" class="mw03-o %s%s" data-q="%d" style="--i:%d"><span class="mw03-rund">%s</span><span class="mw03-et">%s</span></button>' % (
                  c, ' an' if n == 0 else '', n, n, bild(k, 640), E(name)) for name, k, c, n in PLATZ),
              karte('klein'), titel(),
              ''.join('<div class="mw03-a%s" data-a="%d"><h3>%s</h3><p>%s</p></div>' % (' an' if i == 0 else '', i, E(t[0]), unter(t)) for i, t in enumerate(T)))))

# 4 Der Bon: ein Abend als Kassenbon, der aus dem Schlitz gedruckt wird; daneben Text und das Anstossen
BON = [('1', 'Aperitif', 'zum Ankommen'), ('3', 'Gänge', 'aus der Küche'), ('', ZEILE, ''), ('5', 'Drinks', 'Momos Signature'),
       ('1', 'Tasting und Schulung', ''), ('', 'Fatwashing, Milkwashing, Klärung mit Enzymen', '')]
F.append(('Der Bon', '<div class="mw04"><div class="mw04-l">%s<figure class="mw04-klein auf">%s</figure></div>'
          '<div class="mw04-drucker"><span class="mw04-schlitz"></span><div class="mw04-bon auf"><div class="mw04-marke">%s</div>'
          '<p class="mw04-c">Walk on the Wild Side<br>Haasemannstraße 13 · Linden</p><p class="mw04-strich"></p>%s<p class="mw04-strich"></p>'
          '<p class="mw04-z"><span>Erklärt</span><b>jeder Drink</b></p><p class="mw04-z"><span>Plätze</span><b>14</b></p>'
          '<p class="mw04-z summe"><span>Summe, zuletzt</span><b>89,00 EUR</b></p><p class="mw04-strich"></p><p class="mw04-c">Danke und bis zum nächsten Abend</p></div></div>'
          '<figure class="mw04-gross auf">%s</figure></div>' % (
              titel(), bild('t03', 1000), marke('wm'),
              ''.join('<p class="mw04-z%s"><span>%s%s</span><b>%s</b></p>' % (' fein' if not a else '', ('%s× ' % a) if a else '', E(b), E(c)) for a, b, c in BON),
              bild('anstossen', 1600))))

# 5 Vorne die Küche, hinten die Bar: die Karte hat zwei Seiten, ein Schalter wendet sie; dahinter wechselt das Foto
SEITE = [('Auf dem Teller', [('Drei Gänge', 'von Rudi, zuletzt zum Beispiel<span class="mw-zeile">%s</span>' % ZEILE), ('Am Pass angerichtet', 'und an den Tisch gebracht')], 'service'),
         ('Im Glas', [('Aperitif', 'zum Ankommen'), ('Fünf Drinks', 'Momos Signature Drinks, passend zum Essen'), ('Tasting und Schulung', 'Fatwashing, Milkwashing, Klärung mit Enzymen')], 'bar')]
F.append(('Zwei Seiten der Karte', '<div class="mw05" data-mw><div class="mw05-buehne auf">%s<div class="mw05-schalter">%s</div>'
          '<div class="mw05-wende" data-mw-wende>%s</div></div><div class="mw05-text">%s</div></div>' % (
              ''.join('<figure class="mw05-grund%s" data-a="%d">%s</figure>' % (' an' if i == 0 else '', i, bild(s[2], 1600)) for i, s in enumerate(SEITE)),
              ''.join('<button type="button" class="%s" data-q="%d">%s</button>' % ('an' if i == 0 else '', i, E(s[0])) for i, s in enumerate(SEITE)),
              ''.join('<div class="mw05-s s%d"><div class="mw-rahmen"><div class="mw-marke">%s</div><p class="mw-mit">A UNiQUE EXPERiENCE BY MOMO X RUDI</p><p class="mw05-kopf">%s</p>%s<p class="mw-kfuss">%s</p></div></div>' % (
                  i, marke('wm'), E(s[0]), ''.join('<div class="mw-gang"><h3>%s</h3><p>%s</p></div>' % (E(a), b) for a, b in s[1]),
                  'Rudi kocht drei Gänge.' if i == 0 else E(FUSS)) for i, s in enumerate(SEITE)),
              titel('mw-mi'))))

# 6 Durchs Glas: derselbe Teller, einmal direkt, einmal durch das Glas gesehen; mit dem Griff hin und her ziehen
F.append(('Durchs Glas', '<div class="mw06"><div class="mw06-l"><p class="mw06-frage zl auf" aria-label="Erst der Teller oder erst das Glas?"><span class="z"><span style="--i:0">Erst der Teller</span></span><span class="z"><span style="--i:1">oder erst das Glas?</span></span></p>'
          '%s<p class="mw06-teile">%s</p></div>'
          '<div class="mw06-buehne auf" data-mw-zieh style="--x:50">%s<div class="mw06-oben"><div>%s</div></div><span class="mw06-griff"><i></i></span>'
          '<span class="mw06-et l">Teller</span><span class="mw06-et r">Durchs Glas</span><input type="range" min="4" max="96" value="50" aria-label="Zwischen Teller und Glas ziehen"></div></div>' % (
              titel(), X.join('<span>%s</span>' % E(t[0]) for t in T), bild('roq1', 1600), bild('roq2', 1600))))

# 7 Rahmen aus Bildern: die Karte in der Mitte, rundum Fotos Kante an Kante, die sich beim Ankommen um sie schliessen
RAHMEN = ['m3', 'g2', 'm1', 'hok1', 'g3', 'm2', 'r02', 'beeteglas', 'm4', 'g4', 'r07', 'm5', 'schaum', 'd2', 'm8', 'coupe', 'r08', 'g5', 'm7', 'kanister']
POS7 = [(c, r) for r in range(4) for c in range(6) if not (r in (1, 2) and c in (2, 3))]
F.append(('Rahmen aus Bildern', '<div class="mw07"><div class="mw07-rahmen auf">%s<div class="mw07-mitte">%s</div></div><div class="mw07-t">%s</div></div>' % (
    ''.join('<figure class="mw07-f" style="--dx:%d;--dy:%d;--i:%d">%s</figure>' % (
        (-1 if c < 2 else 1 if c > 3 else 0), (-1 if r == 0 else 1 if r == 3 else 0), n % 7, bild(k, 640)) for n, (k, (c, r)) in enumerate(zip(RAHMEN, POS7))),
    karte(), titel('mw-mi'))))

# 8 Der Abend in einer Reihe: Glas, Teller, Glas im Takt des Menüs, seitwärts zum Durchblättern
REIHE = [('glas', 'glaeser', 'Aperitif', 'zum Ankommen'), ('teller', 'beete', 'Gang', ''), ('glas', 'beeteglas', 'Drink', 'dazu'),
         ('teller', 'roq1', 'Gang', ''), ('glas', 'g1', 'Drink', 'dazu'), ('teller', 'hok1', 'Gang', ''), ('glas', 'g2', 'Drink', 'dazu'),
         ('breit', 'klaeren', 'Tasting und Schulung', 'Fatwashing, Milkwashing, Klärung mit Enzymen')]
F.append(('Der Abend in einer Reihe', '<div class="mw08"><div class="mw08-kopf">%s<div class="mw08-pfeile"><button type="button" data-mw-band="-1" aria-label="Zurück">‹</button><button type="button" data-mw-band="1" aria-label="Weiter">›</button></div></div>'
          '<div class="mw08-band">%s</div><p class="mw08-fuss">%s</p></div>' % (
              titel(),
              ''.join('<figure class="mw08-e %s auf" style="--i:%d"><div class="mw08-b">%s</div><figcaption><b>%s</b>%s</figcaption></figure>' % (
                  a, n, bild(k, 1000), E(b), ('<span>%s</span>' % E(c)) if c else '') for n, (a, k, b, c) in enumerate(REIHE)),
              E(FUSS))))

# 9 Die Karte bleibt stehen: links angeheftet die Karte, deren Zeile aufleuchtet; rechts je Teil ein grosses Foto
F.append(('Die Karte bleibt stehen', '<div class="mw09" data-mw-buehne><div class="mw09-l">%s</div><div class="mw09-r">%s%s</div></div>' % (
    karte('steht'), titel(),
    ''.join('<figure class="mw09-f auf" data-g="%d">%s<figcaption><b>%s</b><span>%s</span></figcaption></figure>' % (
        i, bild(t[3] if i == 1 else t[2], 1600), E(t[0]), unter(t)) for i, t in enumerate(T)))))

# 10 Küche, Bar, Tisch: wer was auf den Tisch bringt, drei Orte als grosse Fotos, gross und klein im Wechsel
ORTE = [('Die Küche', 'Drei Gänge, zuletzt zum Beispiel<span class="mw-zeile">%s</span>' % ZEILE, 'kueche', 'mw-gr'),
        ('Die Bar', 'Ein Aperitif zum Ankommen und fünf von Momos Signature Drinks.', 'bar', 'mw-kl'),
        ('Am Tisch', 'Tasting und Schulung: Fatwashing, Milkwashing, Klärung mit Enzymen. %s' % E(FUSS), 'kerze1', 'mw-gr')]
F.append(('Küche, Bar, Tisch', '<div class="mw10">%s<div class="mw10-orte">%s</div></div>' % (
    titel('mw-mi'),
    ''.join('<figure class="mw10-o %s"><div class="mw10-b auf" style="--i:%d">%s</div><figcaption><b>%s</b><span>%s</span></figcaption></figure>' % (
        g, i, bild(k, 1600), E(n), s) for i, (n, s, k, g) in enumerate(ORTE)))))

# 11 Blatt auf Blatt: jeder Teil ein randloses Foto mit Karte darauf, das nächste Blatt schiebt sich beim Scrollen darüber
F.append(('Blatt auf Blatt', '<div class="mw11">%s<div class="mw11-stapel">%s</div></div>' % (
    titel('mw-mi'),
    ''.join('<section class="mw11-blatt" style="--i:%d">%s<div class="mw11-tafel"><p class="mw11-k">Culinarium%s%s</p><h3>%s</h3><p>%s</p></div></section>' % (
        i, bild(k, 1600), X, 'Der Abend', E(t[0]), unter(t)) for i, (t, k) in enumerate(zip(T, ['anstossen', 'service', 'g1', 'klaeren']))))))

# 12 Zahlen als Wörter: ein Aperitif, drei Gänge, fünf Drinks, drei Techniken; in jeder Zeile ein Bildfenster, das gegenläufig wandert
WORT = [('Ein Aperitif', 'zum Ankommen', 'glaeser'), ('Drei Gänge', 'von Rudi, zuletzt zum Beispiel<span class="mw-zeile">%s</span>' % ZEILE, 'roq1'),
        ('Fünf Drinks', 'Momos Signature Drinks, passend zum Essen', 'g1'), ('Drei Techniken', 'Fatwashing, Milkwashing, Klärung mit Enzymen, im Tasting erklärt', 'klaeren')]
F.append(('Zahlen als Wörter', '<div class="mw12"><p class="mw12-kick">Was auf den Tisch kommt</p>%s<div class="mw12-schluss">%s</div></div>' % (
    ''.join('<div class="mw12-z %s"><p class="mw12-w zl auf" aria-label="%s"><span class="z"><span style="--i:0">%s</span></span></p><figure class="mw12-fen" data-mw-drift>%s</figure><p class="mw12-u">%s</p></div>' % (
        'r' if i % 2 else 'l', E(w), E(w), bild(k, 1000), s) for i, (w, s, k) in enumerate(WORT)),
    '<p class="sw auf">%s</p><p class="mw12-fuss">%s</p>' % (SATZ, E(FUSS)))))

# 13 Der Tisch danach: Abzüge liegen um die Karte, beim Ankommen fächern sie vom Stapel auf
ABZ = [('toast', 'Aperitif', -7, -30, -26), ('beete', 'Drei Gänge', 5, 4, -34), ('g1', 'Fünf Drinks', -4, 30, -20), ('klaeren', 'Tasting', 6, -32, 22),
       ('roq1', 'Teller und Glas', -3, 30, 24), ('kerze2', 'Momo erklärt', 3, 2, 34)]
F.append(('Der Tisch danach', '<div class="mw13"><div class="mw13-tisch auf">%s%s</div><div class="mw13-r">%s<p class="mw13-fuss">%s</p></div></div>' % (
    ''.join('<figure class="mw13-a" style="--r:%ddeg;--x:%d;--y:%d;--i:%d">%s<figcaption>%s</figcaption></figure>' % (r, x, y, n, bild(k, 640), E(c)) for n, (k, c, r, x, y) in enumerate(ABZ)),
    karte('mw-mi'), titel(), E(FUSS))))

# 14 Karte zerlegt: die vier Teile der Karte als Papierfelder, im Schachbrett mit ihren Fotos
FELD = [('b', 'glaeser'), ('t', 0), ('b', 'beete'), ('t', 1), ('t', 2), ('b', 'g1'), ('t', 3), ('b', 'klaeren')]
F.append(('Karte zerlegt', '<div class="mw14">%s<div class="mw14-brett">%s</div></div>' % (
    titel('reihe'),
    ''.join(('<figure class="mw14-b"><div class="auf" style="--i:%d">%s</div></figure>' % (n, bild(v, 1000))) if a == 'b' else
            '<div class="mw14-t"><p class="mw-mit">A UNiQUE EXPERiENCE BY MOMO X RUDI</p><h3>%s</h3><p>%s</p></div>' % (E(T[v][0]), unter(T[v]))
            for n, (a, v) in enumerate(FELD)))))

# 15 Ein Satz über dem Abend: randloses Foto, das beim Scrollen zurückzoomt, darauf ein Satz; darunter die Karte als eine Zeile
F.append(('Ein Satz über dem Abend', '<div class="mw15"><div class="mw15-buehne"><figure class="mw15-f" data-mw-zoom>%s</figure>'
          '<p class="mw15-satz zl auf" aria-label="Was genau kommt, steht auf der Karte an deinem Platz."><span class="z"><span style="--i:0">Was genau kommt, steht</span></span><span class="z"><span style="--i:1">auf der Karte an deinem Platz.</span></span></p></div>'
          '<div class="mw15-unten">%s<div class="mw15-zeile">%s</div></div></div>' % (
              bild('kerze2', 1600), titel('reihe'),
              ''.join('<div class="mw15-t"><h3>%s</h3><p>%s</p></div>' % (E(t[0]), unter(t)) for t in T))))


def main():
    seite = open(os.path.join(HIER, 'abend.html')).read()
    m = re.search(r'(<section class="menuekarte"[^>]*>)(\s*<div class="mk-raster">.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Was auf den Tisch kommt» in abend.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="menuekarte"', 'id="tisch" data-name="Was auf den Tisch kommt" class="menuekarte wahl"', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv mkw mw-f%02d" data-n="%d" hidden><div class="mw-in">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Was auf den Tisch kommt</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Karte auf Foto, Text und zwei Bilder'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('menue-wahl.css', 'menue-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["tisch"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/menue-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Was auf den Tisch kommt wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/menue-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'menue-wahl.html'), 'w').write(seite)
    print('Seite menue-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
