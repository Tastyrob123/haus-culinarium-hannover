#!/usr/bin/env python3
"""Culinarium Hannover · Hero der Seite Dirty Chicken in 15 Fassungen (27.10.2026).
Robert: «Denk dran, es ist ein Hero, der muss richtig geil sein, der muss richtig Spaß machen, der muss richtig Bock machen, dass man da hingeht.»
Alle Fotos aus _quelle/dirty-chicken (Rudis neun Aufnahmen vom 27.10. und Instagram), beide Filme, das D als Zeichen.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll.
Baut dirty-chicken-wahl.html (Leiste unten, Pfeiltasten, ?kopf=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/dc_wahl.py"""
import json, os, re, sys
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, zl, sw, knopf, PFEIL

HIER, PROJ = bau.HIER, bau.PROJ
DC = '_quelle/dirty-chicken/'
IG = 'https://www.instagram.com/dirtychicken.hannover/'
SATZ = '„Dirty Chicken. Sandwiches &amp; More.“ Ein Pop-up aus der Familie des Walk on the Wild Side, dem Haus von Culinarium. Die nächsten Termine stehen auf Instagram.'

FOTO = {  # Schlüssel: (Quelle, Bildausschnitt, alt)
    'tisch': (DC + 'vom-kunden-2026-10-27/84678.jpg', '50% 50%', 'Ein Tisch voller Dirty Chicken von oben'),
    'drinks': (DC + 'vom-kunden-2026-10-27/84683.jpg', '50% 45%', 'Drinks, Pommes und Chicken auf dem Tisch'),
    'burger': (DC + 'vom-kunden-2026-10-27/84673.jpg', '50% 55%', 'Ein Chicken-Sandwich im Papier'),
    'sosse': (DC + 'vom-kunden-2026-10-27/84676.jpg', '50% 60%', 'Grüne Sauce kommt auf die Chicken Chunks'),
    'glas': (DC + 'vom-kunden-2026-10-27/84612.jpg', '50% 50%', 'Ein klarer Drink neben dem Chicken'),
    'bar': (DC + 'vom-kunden-2026-10-27/84611.jpg', '50% 50%', 'Ein Drink und Chicken an der Theke'),
    'salat': (DC + 'vom-kunden-2026-10-27/84607.jpg', '50% 50%', 'Krautsalat, Pommes und ein Longdrink'),
    'karte': (DC + 'vom-kunden-2026-10-27/84626.jpg', '50% 50%', 'Die Karte von Dirty Chicken'),
    'team': (DC + 'vom-kunden-2026-10-27/84558.jpg', '50% 40%', 'Die Mannschaft von Dirty Chicken hinter der Theke'),
    'igburger': (DC + 'ig/2026-06-03_dirtychicken.hannover_DZId0KMoAtq-1.jpg', '50% 50%', 'Ein Dirty-Chicken-Burger mit dem Zeichen auf dem Brötchen'),
    'igdrink': (DC + 'ig/2026-06-03_dirtychicken.hannover_DZIo4FHIqRR-1.jpg', '50% 50%', 'Chicken Chunks und ein Drink'),
    'igtisch': (DC + 'ig/2026-06-13_dirtychicken.hannover_DZiug6EoMRr-1.jpg', '50% 50%', 'Ein Tisch voller Dirty Chicken'),
    'igteam': (DC + 'ig/2026-06-03_dirtychicken.hannover_DZIjZWNCGZT-1.jpg', '50% 40%', 'Die Mannschaft an der Theke'),
}
STUFEN = (800, 1400, 2200)


def fotos_machen():
    for k, (q, _p, _a) in FOTO.items():
        qp = os.path.join(PROJ, q)
        im = None
        for b in STUFEN:
            z = os.path.join(HIER, 'assets/bild/dw_%s-%d.webp' % (k, b))
            if os.path.exists(z) and os.path.getmtime(z) > os.path.getmtime(qp):
                continue
            if im is None:
                im = ImageOps.exif_transpose(Image.open(qp)).convert('RGB')
            if im.width < b * .9 and b != STUFEN[0]:
                continue
            x = im.resize((b, round(im.height * b / im.width)), Image.LANCZOS) if im.width > b else im
            x.save(z, 'WEBP', quality=80, method=6)
            print('Foto', k, b)


def img(k, sizes='100vw', pos=None, cls=''):
    q, p, alt = FOTO[k]
    st = [b for b in STUFEN if os.path.exists(os.path.join(HIER, 'assets/bild/dw_%s-%d.webp' % (k, b)))]
    return '<img%s src="assets/bild/dw_%s-800.webp?v=%s" srcset="%s" sizes="%s" alt="%s" style="object-position:%s" loading="lazy" decoding="async">' % (
        ' class="%s"' % cls if cls else '', k, VERSION, ', '.join('assets/bild/dw_%s-%d.webp?v=%s %dw' % (k, b, VERSION, b) for b in st),
        sizes, E(alt), pos or p)


def titel(cls='', zeilen=('Dirty', 'Chicken.')):
    return zl(list(zeilen), 'h1', ('dh-t ' + cls).strip())


def satz(i=2, cls=''):
    return sw(SATZ, i=i, cls=('dh-satz ' + cls).strip())


def ig_knopf(cls='violett'):
    return '<div class="knoepfe sw auf" style="--i:3">%s</div>' % knopf('Instagram @dirtychicken.hannover', IG, cls)


def text(cls='', zeilen=('Dirty', 'Chicken.')):
    return '<div class="dh-text %s">%s%s%s</div>' % (cls, titel(zeilen=zeilen), satz(), ig_knopf())


def film(name, cls=''):
    return '<video class="%s" muted playsinline loop preload="none" poster="assets/film/%s.webp?v=%s" data-src="assets/film/%s.mp4?v=%s" aria-label="%s"></video>' % (
        cls, name, VERSION, name, VERSION, 'Opening 2026 bei Dirty Chicken' if name == 'opening' else 'Die Mannschaft von Dirty Chicken')


def d_pfade():
    """Das D von Dirty Chicken (nachgezogen) als Pfade mit seiner Verschiebung."""
    s = open(os.path.join(HIER, 'assets/zeichen/haus.svg')).read()
    m = re.search(r'<symbol id="dc"[^>]*><g transform="([^"]+)">(.*?)</g></symbol>', s, re.S)
    return m.group(1), m.group(2)


def held(cls, inner, ton=''):
    return '<div class="dh %s"%s>%s</div>' % (cls, ' data-ton="%s"' % ton if ton else '', inner)


F = []  # (Name, Inhalt)

# 1 Die Platte: der volle Tisch von oben dreht sich langsam wie eine Schallplatte; Titel unten links
F.append(('Die Platte', held('d01', '<figure class="d01-platte" aria-hidden="true">%s</figure><div class="dh-grund unten"></div>%s' % (
    img('tisch', '150vmax'), text('unten-links')))))

# 2 Der Biss: das Sandwich füllt den Schirm, die Kamera kommt aus der Kruste heraus und zeigt das ganze Ding
F.append(('Der Biss', held('d02', '<figure class="dh-voll d02-zoom auf">%s</figure><div class="dh-grund unten stark"></div>'
                        '<p class="d02-zitat sw auf" style="--i:1">„Dit is keen Burger.<br>Dit Ding is ’ne Ansage.“</p>%s' % (
                            img('burger', '100vw', '50% 58%'), text('unten-mitte')))))

# 3 Die Ansage: zwei Wortzeilen mit Bildern in der Zeile laufen gegenläufig, dazwischen steht der Name still
R1 = [('Dirty Food', 'igburger'), ('Dirty Drinks', 'glas'), ('Live Music', 'team'), ('Sandwiches &amp; More', 'sosse')]
R2 = [('Chicken Chunks', 'igdrink'), ('Spicy Glaze', 'drinks'), ('Pickled Onions', 'salat'), ('Wat ne Sause', 'igteam')]


def reihe(r):
    eins = ''.join('<span class="d03-w">%s</span><span class="d03-b">%s</span>' % (w, img(k, '22vw')) for w, k in r)
    return '<div class="d03-lauf">%s%s</div>' % (eins, eins)


F.append(('Die Ansage', held('d03 tap', '<div class="d03-r r1" aria-hidden="true">%s</div>%s<div class="d03-r r2" aria-hidden="true">%s</div>'
                         '<div class="d03-fuss">%s%s</div>' % (reihe(R1), titel(zeilen=('Dirty Chicken.',)), reihe(R2), satz(), ig_knopf()), 'dc')))

# 4 Durch das D: die violette Fläche ist zu, nur durch das D sieht man den Tisch; beim Scrollen fällt man hinein
DG, DP = d_pfade()
F.append(('Durch das D', held('d04', '<div class="d04-kleb"><figure class="dh-voll">%s</figure>'
                          '<div class="d04-zoom" data-zieh="d"><svg class="d04-deck" viewBox="214 197 652 712" aria-hidden="true">'
                          '<defs><mask id="d04m" maskUnits="userSpaceOnUse" x="-30000" y="-30000" width="60000" height="60000">'
                          '<rect x="-30000" y="-30000" width="60000" height="60000" fill="#fff"/><g transform="%s" fill="#000">%s</g></mask></defs>'
                          '<rect x="-30000" y="-30000" width="60000" height="60000" fill="#8953A9" mask="url(#d04m)"/></svg>'
                          '<h1 class="d04-titel zl auf" aria-label="Dirty Chicken."><span class="z l"><span style="--i:0">Dirty</span></span><span class="z r"><span style="--i:1">Chicken.</span></span></h1>'
                          '<div class="d04-unten">%s%s</div></div><p class="d04-tipp mono">Scroll hinein</p></div>' % (
                              img('drinks', '100vw', '50% 50%'), DG, DP, satz(), ig_knopf()))))

# 5 Die Bildspur: wo die Maus fährt, landen Fotos auf dem Tisch; sieben liegen schon da
SPUR = ['burger', 'glas', 'sosse', 'team', 'igdrink', 'tisch', 'salat', 'igburger', 'bar', 'drinks', 'igtisch', 'karte', 'igteam']
LIEGT = [('burger', 6, 18, -9), ('glas', 74, 12, 7), ('sosse', 84, 54, -5), ('team', 9, 60, 6), ('igdrink', 62, 70, -8), ('tisch', 30, 74, 4), ('igburger', 44, 8, -3)]
F.append(('Die Bildspur', held('d05 tap', '<div class="d05-spur" aria-hidden="true">%s</div><div class="d05-vorrat" hidden>%s</div><div class="d05-mitte">%s%s%s</div>'
                           '<p class="d05-tipp mono">Fahr mit der Maus über den Tisch</p>' % (
                               ''.join('<figure class="d05-k" style="left:%d%%;top:%d%%;--d:%ddeg">%s</figure>' % (x, y, d, img(k, '18vw')) for k, x, y, d in LIEGT),
                               ''.join(img(k, '18vw') for k in SPUR), titel(), satz(), ig_knopf()), 'dc')))

# 6 Der Bon: aus dem Drucker an der Theke läuft der Bon, daneben die Bar bei Nacht
BON = '''<div class="d06-bon auf" aria-label="Bon von Dirty Chicken"><div class="d06-papier">
<p class="d06-kopf">DIRTY CHICKEN</p><p class="d06-mitte">Sandwiches &amp; More<br>Pop-up · Walk on the Wild Side</p><hr>
<p><b>1×</b> Chicken Chunks<br><span>Spicy Glaze</span></p>
<p><b>1×</b> Sandwich<br><span>Paprika Honey Mayo</span><br><span>Pickled Onions</span></p>
<p><b>1×</b> Krautsalat</p><p><b>2×</b> Dirty Drinks</p><hr>
<p class="d06-summe"><b>Summe</b><b>wahre Liebe</b></p><hr>
<p class="d06-mitte">Nächster Termin auf Instagram<br>@dirtychicken.hannover</p>
<p class="d06-mitte d06-gruss">Dit is keen Burger.<br>Dit Ding is ’ne Ansage.</p></div></div>'''
F.append(('Der Bon', held('d06', '<figure class="dh-voll">%s</figure><div class="dh-grund links"></div><div class="d06-schlitz" aria-hidden="true"></div>%s%s' % (
    img('bar', '100vw', '50% 50%'), BON, text('unten-rechts')))))

# 7 Hingeknallt: sechs Teller und Gläser landen von oben auf dem violetten Tisch, nacheinander
KNALL = [('burger', 3, 13, 24, -8), ('igdrink', 74, 10, 20, 6), ('sosse', 84, 52, 15, -4), ('glas', 2, 60, 16, 7), ('igtisch', 64, 76, 17, -6), ('salat', 18, 80, 14, 5)]
F.append(('Hingeknallt', held('d07 tap', '%s<div class="d07-mitte">%s%s%s</div>' % (
    ''.join('<figure class="d07-k auf" style="left:%d%%;top:%d%%;width:%dvw;--d:%ddeg;--i:%d">%s</figure>' % (x, y, w, d, i, img(k, '%dvw' % w)) for i, (k, x, y, w, d) in enumerate(KNALL)),
    titel(), satz(), ig_knopf()), 'dc')))

# 8 Familie: die Mannschaft hinter der Theke über den ganzen Schirm, Rudis Satz dazu; beim Scrollen geht man auf sie zu
F.append(('Familie', held('d08', '<figure class="dh-voll d08-bild" data-zieh="hinein">%s</figure><div class="dh-grund unten stark"></div>'
                      '<blockquote class="d08-zitat sw auf" style="--i:1"><p>„Wenn aus Freunden und Kollegen Familie wird. Dann haste allet richtig jemacht!“</p></blockquote>%s' % (
                          img('team', '100vw', '50% 38%'), text('unten-links')))))

# 9 Food &amp; Drinks: Sandwich und Glas kommen von beiden Seiten und stossen in der Mitte an
F.append(('Food &amp; Drinks', held('d09', '<figure class="d09-h l auf">%s<figcaption>Dirty Food</figcaption></figure><figure class="d09-h r auf">%s<figcaption>Dirty Drinks</figcaption></figure>'
                                '<div class="d09-und auf" aria-hidden="true">&amp;</div><div class="dh-grund unten stark"></div>%s' % (
                                    img('burger', '50vw', '50% 55%'), img('glas', '50vw', '45% 50%'), text('unten-mitte')), 'dc')))

# 10 Der Automat: vier Bildsäulen laufen gegeneinander wie Walzen, in der Mitte steht das violette Schild
SAEULEN = [['burger', 'igdrink', 'team', 'salat', 'karte'], ['tisch', 'glas', 'igburger', 'sosse', 'igteam'],
           ['drinks', 'bar', 'igtisch', 'burger', 'glas'], ['sosse', 'igteam', 'salat', 'igdrink', 'tisch']]
F.append(('Der Automat', held('d10', '<div class="d10-saeulen" aria-hidden="true">%s</div><div class="d10-schild tap">%s%s%s</div>' % (
    ''.join('<div class="d10-s s%d"><div class="d10-zug">%s</div></div>' % (i, ''.join('<figure>%s</figure>' % img(k, '25vw') for k in s * 2)) for i, s in enumerate(SAEULEN)),
    titel(), satz(), ig_knopf()), 'dc')))

# 11 Die Durchreiche: eine Öffnung in der violetten Wand, dahinter läuft der Film der Mannschaft
F.append(('Die Durchreiche', held('d11 tap', '%s<div class="d11-luke"><div class="d11-film">%s</div></div><div class="d11-brett" aria-hidden="true"></div><div class="d11-unten">%s%s</div>' % (
    titel(zeilen=('Dirty Chicken.',)), film('familie', 'film-hier'), satz(), ig_knopf()), 'dc')))

# 12 Leuchtschrift: die Bar bei Nacht, das D und der Name gehen als Leuchtschrift an
F.append(('Leuchtschrift', held('d12', '<figure class="dh-voll d12-bild">%s</figure><div class="d12-neon auf"><svg class="d12-d" viewBox="214 197 652 712" aria-hidden="true"><g transform="%s">%s</g></svg>%s</div>'
                            '<div class="d12-unten">%s%s</div>' % (img('bar', '100vw', '50% 60%'), DG, DP, titel(zeilen=('Dirty Chicken.',)), satz(), ig_knopf()))))

# 13 Stories: drei Hochformate wie auf Instagram, in der Mitte läuft der Opening-Film mit Laufbalken
F.append(('Stories', held('d13 tap', '<div class="d13-text">%s%s%s</div><div class="d13-stapel">'
                      '<figure class="d13-k l auf">%s</figure>'
                      '<figure class="d13-k m auf"><div class="d13-balken"><i></i></div><p class="d13-wer"><svg viewBox="214 197 652 712" aria-hidden="true"><use href="assets/zeichen/haus.svg?v=%s#dc"/></svg>dirtychicken.hannover<span>Opening 2026</span></p>%s</figure>'
                      '<figure class="d13-k r auf">%s</figure></div>' % (
                          titel(), satz(), ig_knopf(), img('sosse', '22vw'), VERSION, film('opening', 'film-hier'), img('igburger', '22vw')), 'dc')))

# 14 Ausgepackt: das violette Papier reisst auf wie die Tüte um das Sandwich, dahinter die grüne Sauce
F.append(('Ausgepackt', held('d14', '<figure class="dh-voll">%s</figure><div class="d14-papier o auf tap">%s</div><div class="d14-papier u auf tap">%s%s</div>' % (
    img('sosse', '100vw', '50% 62%'), titel(zeilen=('Dirty Chicken.',)), satz(), ig_knopf()))))

# 15 Das Wort: DIRTY über die ganze Breite, durch die Buchstaben zieht der Tisch vorbei; darunter Chicken.
ZUG = ['burger', 'igdrink', 'team', 'sosse', 'glas', 'tisch', 'salat', 'igburger']
F.append(('Das Wort', held('d15', '<svg class="d15-wort" viewBox="0 0 1600 470" aria-hidden="true"><defs><clipPath id="d15c"><text x="800" y="420" text-anchor="middle">DIRTY</text></clipPath></defs>'
                       '<g clip-path="url(#d15c)"><rect width="1600" height="470" fill="#8953A9"/><g class="d15-zug">%s</g></g></svg>'
                       '<div class="d15-unten"><h1 class="dh-t zl auf" aria-label="Dirty Chicken."><span class="z"><span style="--i:0">Chicken.</span></span></h1><div>%s%s</div></div>' % (
                           ''.join('<image href="assets/bild/dw_%s-800.webp?v=%s" x="%d" y="0" width="400" height="470" preserveAspectRatio="xMidYMid slice"/>' % (k, VERSION, i * 400)
                                   for i, k in enumerate(ZUG * 2)), satz(), ig_knopf()))))


def main():
    fotos_machen()
    seite = open(os.path.join(HIER, 'dirty-chicken.html')).read()
    m = re.search(r'<section class="vab dc-ab bar-ab v-dc-kopf[^"]*"[^>]*>.*?</section>', seite, re.S)
    assert m, 'Kopf in dirty-chicken.html nicht gefunden'
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(0)]
    teile += ['<div class="wv dwv" data-n="%d" hidden>%s</div>' % (i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = '<section class="dw wahl" data-ton="dc" id="kopf" data-name="Hero"><div class="wahl-marke"><b>Hero</b><span data-nr></span></div>' + ''.join(teile) + '</section>'
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: zwei Bilder, Titel darüber'] + [re.sub('&amp;', '&', n) for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('dc-wahl.css', 'dc-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["kopf"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/dc-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Hero Dirty Chicken wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/dc-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'dirty-chicken-wahl.html'), 'w').write(seite)
    print('Seite dirty-chicken-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
