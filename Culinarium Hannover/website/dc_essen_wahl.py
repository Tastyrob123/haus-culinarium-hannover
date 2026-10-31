#!/usr/bin/env python3
"""Dirty Chicken · erster Abschnitt nach dem Fenster («Dit is keen Burger») in 20 Fassungen zur Wahl (27.10.2026 abends).
Robert: «Wir müssen Abschnitt für Abschnitt gehen und du musst mir Vorschläge geben … 20 Alternativen, und ich entscheide.»
Jede Fassung ein anderes Gerüst (Entwurfs-Maschine, Bereich Essen, mit Abstand zu Culinarium, Bar und allen anderen Häusern),
gebunden an die Gegenstände des Pop-ups: Blechteller, Papier, Bon, Karte, Sauce, Instagram, Film, Tapete, das D.
Nie zwei Fotos übereinander, nie dasselbe Foto zweimal in einer Fassung, Gesichter unberührt, ein bewegter Moment je Blick, nur transform und opacity.
Baut dirty-chicken-essen-wahl.html: Hero und Fenster wie auf der echten Seite, dann der Abschnitt umschaltbar (Leiste unten, Pfeiltasten, ?essen=Nummer),
Fassung 0 = heutiger Stand (die abgelehnte Bühne «Drei Worte»). Aufruf: python3 website/dc_essen_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, foto, zl, sw
import varianten
import dc_neu

HIER = bau.HIER
GERICHTE = [('Chicken Chunks', 'Spicy Glaze, grüne Sauce'), ('Sandwich', 'Paprika-Honig-Mayo, eingelegte Zwiebeln'), ('Pommes &amp; Krautsalat', 'kommen immer mit')]
SATZ = 'Fried Chicken, das kracht: zwei Sachen, die wir können, und das, was immer dazukommt. Kein Burger, ’ne Ansage.'
IG = 'https://www.instagram.com/dirtychicken.hannover/'


def ek(text, i=0):
    return '<p class="ek sw auf" style="--i:%d"><span>%s</span></p>' % (i, text)


def et(zeilen, cls='', i0=0):
    return zl(zeilen, 'h2', ('et ' + cls).strip(), i0)


def ex(text, i=2, cls=''):
    return sw(text, 'p', ('ex ' + cls).strip(), i)


def ez(i0=2, cls=''):
    return '<div class="ezl %s">%s</div>' % (cls, ''.join(
        '<div class="ez sw auf" style="--i:%d"><b>%s</b><span>%s</span></div>' % (i0 + i, n, s) for i, (n, s) in enumerate(GERICHTE)))


def film(n, cls=''):
    return ('<figure class="film %s" style="--lq:url(assets/film/%s.webp);aspect-ratio:%s"><video muted playsinline preload="none" poster="assets/film/%s.webp?v=%s" data-src="assets/film/%s.mp4?v=%s" aria-label="%s"></video>'
            '<button class="film-nochmal" type="button" aria-label="Film noch einmal abspielen">Noch einmal</button></figure>') % (
        cls, n, '1/1' if n == 'familie' else '9/16', n, VERSION, n, VERSION, 'Die Mannschaft hinter der Theke' if n == 'familie' else 'Opening 2026 bei Dirty Chicken')


def d_zeichen(cls=''):
    return bau.zeichen_haus('dc', cls)


def sec(n, ton, inner, cls=''):
    return '<section class="vab dc-ab ess es%02d %s" data-ton="%s">%s</section>' % (n, cls, ton, inner)


F = []  # (Name, Satz für Robert, HTML)

# 1 Die Teller: vier ovale Blechteller werden von rechts serviert, jeder mit seinem Namen
TELLER = [('dn_sosse', '50% 55%', 'Chicken Chunks', 'Spicy Glaze, grüne Sauce'), ('dn_burger', '50% 55%', 'Sandwich', 'Paprika-Honig-Mayo, eingelegte Zwiebeln'),
          ('dn_salat', '50% 50%', 'Pommes &amp; Krautsalat', 'kommen immer mit'), ('dn_drinks', '50% 45%', 'Dirty Drinks', 'von der Bar, dazu')]
teller = ''.join('<figure class="e01-t" style="--i:%d">%s<figcaption><b>%s</b><span>%s</span></figcaption></figure>' % (
    i, foto(k, '', '(max-width:860px) 50vw, 24vw', auf=False, pos=p), n, su) for i, (k, p, n, su) in enumerate(TELLER))
F.append(('Die Teller', 'Vier Blechteller, oval wie die echten, kommen von rechts auf den Tisch; unter jedem sein Name.', sec(1, 'nacht', '<div class="vi"><div class="vk e01-kopf">%s%s%s</div><div class="e01-reihe auf">%s</div></div>' % (
    ek('Dirty Food'), et(['Was auf den', 'Tisch kommt.']), ex(SATZ), teller))))

# 2 Die Tüte: das Sandwich füllt den Schirm, die Karte steht auf dem Papier der Tüte
F.append(('Die Tüte', 'Das Sandwich randlos über den ganzen Schirm, die Karte steht auf dem Kraftpapier der Tüte, die von unten hochkommt.', sec(2, 'nacht', '''<div class="e02-buehne auf">%s<div class="e02-hof"></div>
<div class="e02-tuete"><div class="e02-d">%s</div>%s%s%s%s</div></div>''' % (
    foto('dn_burger', 'e02-bild', '100vw', auf=False, pos='62% 55%'), d_zeichen('e02-dz'), ek('Dirty Food'), et(['Im Papier.']), ez(2), ex('Kein Burger, ’ne Ansage.', 5)))))

# 3 Der Bon: die Bestellung druckt sich Zeile für Zeile, daneben die Sauce
BON = ''.join('<p class="e03-z sw auf" style="--i:%d">%s</p>' % (i, z) for i, z in enumerate([
    '<b class="e03-kopf">DIRTY CHICKEN</b>', 'Sandwiches &amp; More · Pop-up', '<hr>',
    '<b>1×</b>Chicken Chunks<span>Spicy Glaze, grüne Sauce</span>', '<b>1×</b>Sandwich<span>Paprika-Honig-Mayo, eingelegte Zwiebeln</span>',
    '<b>1×</b>Pommes &amp; Krautsalat', '<b>2×</b>Dirty Drinks', '<hr>', '<b>Summe</b><b class="e03-r">wahre Liebe</b>', '<hr>', 'Dit is keen Burger.<br>Dit Ding is ’ne Ansage.']))
F.append(('Der Bon', 'Die Bestellung läuft wie aus dem Drucker an der Theke, Zeile für Zeile; links die Sauce, die auf die Chunks kommt.', sec(3, 'nacht', '''<div class="vi e03">
<div class="e03-bild auf">%s</div>
<div class="e03-rechts"><div class="vk">%s%s%s</div><div class="e03-bon auf"><div class="e03-papier">%s</div></div></div></div>''' % (
    foto('dn_sosse', '', '(max-width:860px) 100vw, 52vw', auf=False, pos='50% 55%'), ek('Die Bestellung'), et(['Einmal', 'alles.']), ex(SATZ), BON))))

# 4 Chunks oder Sandwich?: ein Bild, zwei Worte; tippen tauscht das Bild an derselben Stelle
F.append(('Chunks oder Sandwich?', 'Ein grosses Bild, daneben zwei grosse Worte; wer eins antippt, bekommt sein Bild an derselben Stelle. Nichts springt.', sec(4, 'warm', '''<div class="vi e04" data-wahl="0">
<div class="e04-buehne auf"><div class="e04-b" data-s="0">%s</div><div class="e04-b" data-s="1">%s</div></div>
<div class="e04-text">%s<div class="e04-worte">
<button type="button" class="e04-w an" data-s="0" aria-pressed="true"><b class="zl auf"><span class="z"><span style="--i:1">Chunks.</span></span></b><span class="sw auf" style="--i:2">Spicy Glaze, grüne Sauce</span></button>
<button type="button" class="e04-w" data-s="1" aria-pressed="false"><b class="zl auf"><span class="z"><span style="--i:2">Sandwich.</span></span></b><span class="sw auf" style="--i:3">Paprika-Honig-Mayo, eingelegte Zwiebeln</span></button></div>
%s</div></div>''' % (foto('dn_sosse', '', '(max-width:860px) 100vw, 56vw', auf=False, pos='50% 55%'), foto('dn_burger', '', '(max-width:860px) 100vw, 56vw', auf=False, pos='50% 55%'),
                     ek('Chunks oder Sandwich?'), ex('Dazu Pommes und Krautsalat, immer. Tipp auf eins von beiden.', 4)))))

# 5 Der Feed: drei Posts von Instagram mit ihren Zeilen, so wie Dirty Chicken selbst spricht
POSTS = [('dc_burger', 'Dit is keen Burger. Dit Ding is ’ne Ansage.'), ('dc_drink', 'Dirty Food &amp; Dirty Drinks. Jenau meen Ding wa.'), ('dc_tisch', 'Dit ist wahre Liebe!')]
F.append(('Der Feed', 'Drei Posts von Instagram nebeneinander, darunter ihre Zeilen in Berliner Schnauze; so spricht das Pop-up von sich selbst.', sec(5, 'nacht', '''<div class="vi">
<div class="vk e05-kopf">%s%s%s</div>
<div class="e05-reihe auf">%s</div></div>''' % (ek('So steht es auf Instagram'), et(['Dirty Food.']), ex(SATZ), ''.join(
    '<figure class="e05-p" style="--d:%.2fs">%s<figcaption><p class="e05-q">„%s“</p><span class="mono">@dirtychicken.hannover · Juni 2026</span></figcaption></figure>' % (i * .14, foto(k, '', '(max-width:860px) 100vw, 30vw', auf=False), q)
    for i, (k, q) in enumerate(POSTS))))))

# 6 Zwei Worte: Chunks und Sandwich, je ein Schirm mit einem Wort und einem Bild
def e06_s(wort, sub, k, pos, rechts=False):
    w = '<div class="e06-wort"><h2 class="zl auf e06-w" aria-label="%s"><span class="z"><span style="--i:0">%s</span></span></h2>%s</div>' % (E(wort), wort, ex(sub, 1))
    b = '<div class="e06-bild">%s</div>' % foto(k, '', '(max-width:860px) 100vw, 50vw', auf=False, pos=pos)
    return '<div class="e06-s auf%s">%s</div>' % (' r' if rechts else '', (b + w) if rechts else (w + b))
F.append(('Zwei Worte', 'Chunks und Sandwich bekommen je einen ganzen Schirm: ein Wort, ein Bild, sonst nichts. Danach ein Satz zu Pommes und Krautsalat.', sec(6, 'nacht', '%s%s<p class="e06-dazu zl auf" aria-label="Dazu Pommes und Krautsalat."><span class="z"><span style="--i:0">Dazu Pommes &amp; Krautsalat.</span></span></p>' % (
    e06_s('Chunks.', 'Spicy Glaze, grüne Sauce, Pickles. Fried Chicken, das kracht.', 'dn_sosse', '50% 55%'),
    e06_s('Sandwich.', 'Paprika-Honig-Mayo, eingelegte Zwiebeln, weiches Brötchen, im Papier.', 'dn_burger', '50% 55%', True)))))

# 7 Keen Burger: drei Zahlen zählen hoch, jede mit ihrem Wort und Bild
def e07_z(i, zahl, wort, satz, k):
    return '<div class="e07-z auf" style="--i:%d"><b class="e07-n" data-zahl="%d">%d</b><div class="e07-t"><h2 class="zl auf" aria-label="%s"><span class="z"><span style="--i:0">%s</span></span></h2>%s</div><div class="e07-b">%s</div></div>' % (
        i, zahl, zahl, E(wort), wort, ex(satz, 1), foto(k, '', '(max-width:860px) 100vw, 24vw', auf=False))
F.append(('Keen Burger', 'Drei Zahlen zählen hoch: 0 Burger, 2 Sachen, 1 Sauce. Jede Zahl mit ihrem Wort und ihrem Bild.', sec(7, 'dc', '<div class="vi e07">%s%s%s</div>' % (
    e07_z(0, 0, 'Burger.', 'Dit is keen Burger. Dit Ding is ’ne Ansage.', 'dc_burger'),
    e07_z(1, 2, 'Sachen.', 'Chicken Chunks mit Spicy Glaze. Sandwich mit Paprika-Honig-Mayo und eingelegten Zwiebeln.', 'dn_tisch'),
    e07_z(2, 1, 'Sauce.', 'Grün, auf die Chunks, bis es tropft. Dazu Pommes und Krautsalat.', 'dn_sosse')))))

# 8 Der Film: der Film vom Tag unbeschnitten links, rechts die Karte
F.append(('Der Film', 'Der Film vom Opening steht unbeschnitten links, rechts die drei Sachen als grosse Zeilen.', sec(8, 'nacht', '''<div class="vi e08">
<div class="e08-film auf">%s</div><div class="vk e08-text">%s%s%s%s</div></div>''' % (
    film('opening', 'e08-f'), ek('Dirty Food'), et(['So sah', 'es aus.']), ez(2), ex('Kein Burger, ’ne Ansage.', 5)))))

# 9 Tisch von oben: ein einziges grosses Foto, das beim Scrollen langsam näher kommt
F.append(('Tisch von oben', 'Ein einziges Foto, der volle Tisch von oben, so breit wie die Seite; beim Scrollen kommt er langsam näher. Darunter die Karte als Block.', sec(9, 'warm', '''<div class="vi e09">
<div class="e09-rahmen auf"><div class="e09-zoom">%s</div></div>
<div class="e09-unten"><div class="vk">%s%s</div>%s</div></div>''' % (
    foto('dn_tisch', '', '100vw', auf=False, pos='50% 50%'), ek('Dirty Food'), et(['Alles auf', 'einmal.']), ez(2)))))

# 10 Schachbrett: Bildfeld und Textfeld wechseln, gleich gross
def e10_f(k, pos, wort, satz, i):
    return '<div class="e10-f bild">%s</div><div class="e10-f text"><div class="vk">%s<h2 class="zl auf" aria-label="%s"><span class="z"><span style="--i:1">%s</span></span></h2>%s</div></div>' % (
        foto(k, '', '(max-width:860px) 100vw, 50vw', auf=False, pos=pos), ek(['Eins', 'Zwei'][i]), E(wort), wort, ex(satz, 2))
F.append(('Schachbrett', 'Vier gleich grosse Felder: Bild, Text, Text, Bild. Die Textfelder sind violett mit Tapete.', sec(10, 'nacht', '<div class="e10 auf">%s%s</div>' % (
    e10_f('dn_sosse', '50% 55%', 'Chicken Chunks.', 'Spicy Glaze, grüne Sauce, Pickles. Fried Chicken, das kracht.', 0),
    e10_f('dn_burger', '50% 55%', 'Sandwich.', 'Paprika-Honig-Mayo, eingelegte Zwiebeln, weiches Brötchen. Dazu Pommes und Krautsalat.', 1)))))

# 11 Die Luke: ein ovales Fenster in der violetten Wand, dahinter gleitet der Tisch
F.append(('Die Luke', 'Die violette Wand hat ein ovales Fenster wie ein Blechteller; dahinter gleitet der volle Tisch beim Scrollen vorbei. Links die Karte.', sec(11, 'dc', '''<div class="vi e11">
<div class="vk e11-text">%s%s%s</div>
<div class="e11-luke auf"><div class="e11-glas">%s</div></div></div>''' % (
    ek('Dirty Food'), et(['Was auf den', 'Tisch kommt.']), ez(2), foto('dn_tisch', '', '(max-width:860px) 100vw, 60vw', auf=False, pos='50% 50%')))))

# 12 Zickzack: drei Einträge versetzt links und rechts, jeder mit eigenem Abstand
def e12_r(k, pos, wort, satz, rechts, klein=False):
    b = '<div class="e12-bild%s">%s</div>' % (' klein' if klein else '', foto(k, '', '(max-width:860px) 100vw, 52vw', auf=False, pos=pos))
    t = '<div class="vk e12-text"><h2 class="zl auf" aria-label="%s"><span class="z"><span style="--i:0">%s</span></span></h2>%s</div>' % (E(wort), wort, ex(satz, 1))
    return '<div class="e12-r auf%s">%s</div>' % (' r' if rechts else '', (t + b) if rechts else (b + t))
F.append(('Zickzack', 'Chunks, Sandwich, Pommes und Krautsalat wechseln versetzt links und rechts, jedes Bild hoch, jeder Text ein Block daneben.', sec(12, 'nacht', '<div class="vi">%s%s%s%s</div>' % (
    '<div class="vk e12-kopf">%s%s</div>' % (ek('Dirty Food'), et(['Drei Sachen.'])),
    e12_r('dn_sosse', '50% 55%', 'Chicken Chunks.', 'Spicy Glaze, grüne Sauce, Pickles.', False),
    e12_r('dn_burger', '50% 55%', 'Sandwich.', 'Paprika-Honig-Mayo, eingelegte Zwiebeln, weiches Brötchen.', True),
    e12_r('dn_salat', '50% 50%', 'Pommes &amp; Krautsalat.', 'Kommen immer mit.', False, True)))))

# 13 Die Hand: die Sauce randlos mit einem Satz, darunter das Paar Sandwich und Beilagen
F.append(('Die Hand', 'Die Hand mit der Sauce über den ganzen Schirm, darauf ein Satz; darunter stossen Sandwich und Beilagen als Paar an.', sec(13, 'nacht', '''<div class="e13-oben auf">%s<div class="e13-hof"></div>
<p class="e13-satz zl auf" aria-label="Grüne Sauce drauf, bis es tropft."><span class="z"><span style="--i:0">Grüne Sauce drauf,</span></span><span class="z"><span style="--i:1">bis es tropft.</span></span></p></div>
<div class="vi e13-unten"><div class="vk">%s%s%s</div><div class="paar auf e13-paar">%s%s</div></div>''' % (
    foto('dn_sosse', 'e13-bild', '100vw', auf=False, pos='50% 62%'), ek('Dirty Food'), et(['Zwei Sachen.']), ez(2),
    foto('dn_burger', '', '(max-width:860px) 50vw, 30vw', auf=False, pos='50% 55%'), foto('dn_salat', '', '(max-width:860px) 50vw, 30vw', auf=False)))))

# 14 Die Karte lag da: das Foto der echten Karte, daneben ihre Zeilen gross
F.append(('Die Karte lag da', 'Das Foto der echten Karte vom Tisch, daneben ihre drei Zeilen gross gesetzt.', sec(14, 'warm', '''<div class="vi e14">
<div class="e14-bild auf">%s</div><div class="vk e14-text">%s%s%s%s</div></div>''' % (
    foto('dn_karte', '', '(max-width:860px) 100vw, 48vw', auf=False, pos='50% 50%'), ek('So lag sie auf dem Tisch'), et(['Die Karte.']), ez(2, 'ez-gross'), ex('Zwei Sachen, die wir können, und das, was immer dazukommt.', 5)))))

# 15 Die Wand: eine dichte Wand aus neun Bildern, die nacheinander hell werden
WAND = [('dn_sosse', 'g', '50% 55%'), ('dn_burger', 'g', '50% 55%'), ('dn_salat', 'm', '50% 50%'), ('dc_drink', 'm', '50% 50%'),
        ('dc_tisch', 'm', '50% 50%'), ('dn_bar', 'm', '50% 50%'), ('dn_glas', 's', '50% 50%'), ('dc_burger', 's', '50% 50%')]
F.append(('Die Wand', 'Acht Bilder dicht an dicht in ungleichen Grössen; beim Ankommen gehen sie nacheinander an wie Lichter.', sec(15, 'nacht', '''<div class="vi">
<div class="vk e15-kopf">%s%s%s</div>
<div class="e15-wand auf">%s</div></div>''' % (ek('Dirty Food'), et(['Alles, was auf', 'den Tisch kam.']), ex(SATZ), ''.join(
    '<div class="e15-w %s" style="--i:%d">%s</div>' % (c, i, foto(k, '', '(max-width:860px) 50vw, 33vw', auf=False, pos=p)) for i, (k, c, p) in enumerate(WAND))))))

# 16 Der Satz: ein Satz über die ganze Breite, kleine Fotos sitzen zwischen den Wörtern
def e16_i(k, pos):
    """Kleines Foto im Satz: ein span statt figure, damit der Absatz nicht aufbricht (figure schliesst ein p)."""
    m = bau.META[k]
    return '<span class="e16-i" style="--lq:url(%s)"><img data-srcset="%s" data-sizes="12vw" alt="%s" decoding="async" style="object-position:%s"></span>' % (
        m['lq'], bau.srcset(k), E(bau.BILD[k][2]), pos)
F.append(('Der Satz', 'Die ganze Karte als ein Satz über die volle Breite, zwischen den Wörtern sitzen kleine Fotos der Sachen.', sec(16, 'dc', '''<div class="vi e16">%s
<p class="e16-satz sw auf" style="--i:1">Chicken Chunks %s mit Spicy Glaze und grüner Sauce, das Sandwich %s mit Paprika-Honig-Mayo und eingelegten Zwiebeln, dazu Pommes %s und Krautsalat %s. Kein Burger, ’ne Ansage.</p></div>''' % (
    ek('Dirty Food'), e16_i('dn_sosse', '50% 55%'), e16_i('dn_burger', '50% 55%'), e16_i('dn_salat', '50% 50%'), e16_i('dn_tisch', '50% 50%')))))

# 17 Zwei Steckbriefe: je ein hohes Bild, darunter die Angaben als Liste
def e17_s(k, pos, wort, zeilen):
    return '<div class="e17-s auf">%s<h3 class="zl auf" aria-label="%s"><span class="z"><span style="--i:1">%s</span></span></h3><dl class="vz sw auf" style="--i:2">%s</dl></div>' % (
        foto(k, '', '(max-width:860px) 100vw, 46vw', auf=False, pos=pos), E(wort), wort, ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % z for z in zeilen))
F.append(('Zwei Steckbriefe', 'Chunks und Sandwich nebeneinander, je ein hohes Bild und darunter die Angaben als Liste: Glasur, Sauce, dazu.', sec(17, 'warm', '''<div class="vi e17">
<div class="vk e17-kopf">%s%s</div>
<div class="e17-reihe">%s%s</div></div>''' % (ek('Dirty Food'), et(['Zwei Sachen.']),
    e17_s('dn_sosse', '50% 55%', 'Chicken Chunks.', [('Glasur', 'Spicy Glaze'), ('Sauce', 'grün, drüber'), ('Dazu', 'Pickles, Pommes, Krautsalat')]),
    e17_s('dn_burger', '50% 55%', 'Sandwich.', [('Mayo', 'Paprika-Honig'), ('Zwiebeln', 'eingelegt'), ('Brötchen', 'weich, im Papier')])))))

# 18 Dirty Food, gross: zwei Zeilen Versalien laufen gegenläufig hinter einem Bild
def e18_lauf(woerter, cls):
    eins = ' · '.join(woerter) + ' · '
    return '<div class="e18-lauf %s" aria-hidden="true"><p>%s</p><p>%s</p></div>' % (cls, eins, eins)
F.append(('Dirty Food, gross', 'Zwei Zeilen Versalien in Umrisslinie laufen gegenläufig hinter einem Bild vorbei: Dirty Food, Dirty Drinks, Chicken Chunks, Spicy Glaze.', sec(18, 'nacht', '''<div class="e18">%s%s
<div class="vi e18-mitte auf"><div class="e18-bild">%s</div><div class="vk">%s%s%s</div></div></div>''' % (
    e18_lauf(['DIRTY FOOD', 'DIRTY DRINKS', 'SANDWICHES &amp; MORE'], 'a'), e18_lauf(['CHICKEN CHUNKS', 'SPICY GLAZE', 'PICKLED ONIONS'], 'b'),
    foto('dc_drink', '', '(max-width:860px) 100vw, 44vw', auf=False), ek('Dirty Food'), et(['Dirty', 'Food.']), ez(2)))))

# 19 Stillleben: ein Bild in der Mitte, viel Ruhe, ein Satz darunter
F.append(('Stillleben', 'Ein einziges Bild in der Mitte, Glas und Teller auf der Theke, viel Ruhe drum herum; darunter ein Satz und die Karte in einer Zeile.', sec(19, 'warm', '''<div class="vi e19">%s
<div class="e19-bild auf">%s</div>
<p class="e19-satz zl auf" aria-label="Ein Glas, ein Teller, ein Abend."><span class="z"><span style="--i:0">Ein Glas, ein Teller,</span></span><span class="z"><span style="--i:1">ein Abend.</span></span></p>
<p class="e19-zeile sw auf" style="--i:2">Chicken Chunks · Spicy Glaze &nbsp;/&nbsp; Sandwich · Paprika-Honig-Mayo &nbsp;/&nbsp; Pommes &amp; Krautsalat</p></div>''' % (
    ek('Stillleben', 0), foto('dn_bar', '', '(max-width:860px) 100vw, 44vw', auf=False, pos='50% 50%')))))

# 20 Der Leuchtkasten: die Tafel über der Theke, leuchtet violett, darunter die Theke
F.append(('Der Leuchtkasten', 'Die Karte als Leuchttafel über der Theke: dunkler Kasten mit violettem Schein, je Zeile ein kleines Bild; darunter die Theke.', sec(20, 'nacht', '''<div class="vi e20">
<div class="vk e20-kopf">%s%s</div>
<div class="e20-kasten auf">%s</div>
<div class="e20-theke auf">%s</div></div>''' % (ek('Über der Theke'), et(['Die Tafel.']), ''.join(
    '<div class="e20-r sw auf" style="--i:%d"><div class="e20-b">%s</div><b>%s</b><span>%s</span></div>' % (i, foto(k, '', '(max-width:860px) 30vw, 12vw', auf=False, pos=p), n, s)
    for i, (k, p, (n, s)) in enumerate(zip(['dn_sosse', 'dn_burger', 'dn_salat'], ['50% 55%', '50% 55%', '50% 50%'], GERICHTE))),
    foto('dn_bar', '', '100vw', auf=False, pos='50% 45%')))))


def main():
    s = [bau.kopf('Essen wählen · Dirty Chicken', 'Dirty Chicken: erster Abschnitt nach dem Fenster in 20 Fassungen zur Wahl.', 'dirty-chicken.html', 'dc')]
    k, n, c = varianten.DCSEITE[0]
    s.append(varianten.abschnitt(k, n, c, idn=False).replace('class="vab ', 'class="vab dc-ab bar-ab ', 1))
    s.append('''<section class="fenster" id="fenster-dc" aria-label="Die Ansage">
  <div class="fenster-schicht">%s<div class="fenster-hof"></div><p class="fenster-satz zl"><span class="z"><span style="--i:0">Dit is keen Burger.</span></span><span class="z"><span style="--i:1">Dit Ding is ’ne Ansage.</span></span></p></div>
</section>''' % foto('dn_burger', '', '100vw', auf=False, pos='50% 55%'))
    heute = '<section class="vab dc-ab dcn dcn-drei" data-ton="nacht">%s</section>' % dc_neu.drei()
    teile = ['<div class="wv" data-n="0">%s</div>' % heute]
    teile += ['<div class="wv" data-n="%d" hidden>%s</div>' % (i, h) for i, (_n, _s, h) in enumerate(F, 1)]
    s.append('<section class="dw wahl" data-ton="nacht" id="essen" data-name="Essen"><div class="wahl-marke"><b>Essen</b><span data-nr></span></div>%s</section>' % ''.join(teile))
    s.append(bau.fuss())
    h = ''.join(s)
    namen = ['Heute: Drei Worte (abgelehnt)'] + [re.sub('&amp;', '&', n) for n, _s, _h in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('dc-essen-wahl.css', 'dc-essen-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["essen"],daumen:%s};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/dirty-chicken.js?v=%s" defer></script>
<script src="assets/dc-essen-wahl.js?v=%s" defer></script>''' % (
        json.dumps(namen, ensure_ascii=False), 'true' if os.path.exists(os.path.join(HIER, 'assets/daumen/essen-1.jpg')) else 'false', VERSION, VERSION, v)
    h = h.replace('</head>', '<link rel="stylesheet" href="assets/dirty-chicken.css?v=%s">\n<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/dc-essen-wahl.css?v=%s">\n</head>' % (VERSION, VERSION, v), 1)
    h = h.replace('</body>', leiste + '\n</body>', 1)
    for fk in varianten.FILMLQ:
        h = h.replace('--lq:url(assets/film/%s.webp)' % fk, '--lq:url(%s)' % varianten.FILMLQ[fk])
    open(os.path.join(HIER, 'dirty-chicken-essen-wahl.html'), 'w', encoding='utf-8').write(h)
    json.dump([{'nr': i, 'name': n, 'satz': s_} for i, (n, s_, _h) in enumerate(F, 1)], open(os.path.join(HIER, '_sicherung', 'essen-fassungen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Seite dirty-chicken-essen-wahl.html', len(h) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
