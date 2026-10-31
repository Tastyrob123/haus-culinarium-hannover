#!/usr/bin/env python3
"""Dirty Chicken · die Seite nach Hero und Fenster, neu als eine Geschichte (Robert 27.10.2026 abends:
«Das Dirty Chicken ist im Fokus, das ist der Star … das Einzige, was bleibt, ist der Hero und das erste Fenster»).

Erzählt in der Reihenfolge, in der das Pop-up von sich selbst spricht (Plakat: Dirty Food, Dirty Drinks & Live Music):
  1 Drei Worte     · feststehende Bühne, drei Bilder und drei Worte wechseln beim Scrollen (die Ansage, in drei Worten)
  2 Die Karte      · helle Fläche wie die Karte auf dem Tisch; die Teller kommen von oben auf den Tisch
  3 Dirty Drinks   · dunkel wie die Bar; zwei Gläser stossen an der Naht an
  4 Opening 2026   · violett mit Tapete; der Film unbeschnitten in der Mitte, die Sätze in Berliner Schnauze schweben drum herum
  5 Familie        · Film der Mannschaft und der Satz «Wenn aus Freunden und Kollegen Familie wird»
  6 Das nächste Mal· Band wie am Hero, das Zeichen, Instagram, und die zwei Türen zurück ins Haus
Jeder Teil endet mit einem Satz, der in den nächsten führt (Charakterblatt, Drehbuch).
Fakten: _quelle/dirty-chicken/ig/beitraege.md, Plakat DZPYEOJIfVb, Karte 84626 (Chicken Chunks · Spicy Glaze; Sandwich · Paprika Honey Mayo · Pickled Onions).
Aussehen: assets/dirty-chicken.css, Bewegung: assets/dirty-chicken.js (nur transform, nativer Scroll)."""
import bau
from bau import E, foto, zl, sw, knopf

IG = 'https://www.instagram.com/dirtychicken.hannover/'


def film(n, cls='', label=''):
    return ('<figure class="film %s" style="--lq:url(assets/film/%s.webp);aspect-ratio:%s"><video muted playsinline preload="none" poster="assets/film/%s.webp?v=%s" data-src="assets/film/%s.mp4?v=%s" aria-label="%s"></video>'
            '<button class="film-nochmal" type="button" aria-label="Film noch einmal abspielen">Noch einmal</button></figure>') % (
        cls, n, '1/1' if n == 'familie' else '9/16', n, bau.VERSION, n, bau.VERSION, E(label))


def kicker(text, i=0):
    return sw('<span>%s</span>' % text, 'p', 'dcn-k', i)


def etikett(text):
    return '<span class="dcn-etikett">%s</span>' % text


def abschnitt(k, ton, inner, lauf=''):
    return '<section class="vab dc-ab bar-ab dcn dcn-%s" id="%s" data-ton="%s" data-lauf="%s">%s</section>' % (k, k, ton, lauf, inner)


def fuss_svg():
    return '<svg class="am-fuss" viewBox="-20 -32 40 68" aria-hidden="true"><path d="M0 34 L0 4 M0 4 L-14 -22 M0 4 L2 -28 M0 4 L18 -18"/></svg>'


# ------------------------------------------------------------------ 1 Drei Worte
DREI = [
    ('dn_sosse', '50% 55%', ['Dirty', 'Food.'],
     'Fried Chicken, das kracht: Chunks mit Spicy Glaze und grüner Sauce, das Sandwich mit Paprika-Honig-Mayo und eingelegten Zwiebeln. Dazu Pommes und Krautsalat, alles auf dem Blechteller.'),
    ('dn_glas', '50% 50%', ['Dirty', 'Drinks.'],
     'Die Drinks kommen von der Bar: Die Leute vom Walk on the Wild Side stehen hinter dem Tresen und mixen, was zum Chicken passt. Beim ersten Mal mit Gastschicht von Martin Bauermann, Beluga Vodka Berlin.'),
    ('dn_team', '50% 42%', ['Live-', 'Musik.'],
     'Ein Pop-up ist kein Mittagstisch, sondern ein Fest: ein Nachmittag und ein Abend lang, mit Musik, mit der ganzen Mannschaft, danach Aftershow.'),
]


def drei():
    bilder = ''.join('<div class="dr-bild" data-s="%d">%s</div>' % (i, foto(b, '', '100vw', auf=False, pos=pos)) for i, (b, pos, _t, _x) in enumerate(DREI))
    worte = ''.join('<h2 class="dr-wort" data-s="%d" aria-label="%s"><span class="z"><span>%s</span></span><span class="z"><span>%s</span></span></h2>' % (
        i, E(' '.join(t)), t[0], t[1]) for i, (_b, _p, t, _x) in enumerate(DREI))
    texte = ''.join('<p class="dr-text" data-s="%d">%s</p>' % (i, x) for i, (_b, _p, _t, x) in enumerate(DREI))
    zaehler = ''.join('<span class="dr-nr" data-s="%d">0%d</span>' % (i, i + 1) for i in range(len(DREI)))
    punkte = ''.join('<i data-s="%d"></i>' % i for i in range(len(DREI)))
    return '''<div class="dr-lauf"><div class="dr-buehne" data-schritt="0">
  <div class="dr-bilder">%s</div><div class="dr-hof"></div>
  <div class="dr-schild">
    <p class="dcn-k"><span>Die Ansage, in drei Worten</span><b class="dr-zaehler">%s<span class="dr-von">/ 03</span></b></p>
    <div class="dr-worte">%s</div>
    <div class="dr-texte">%s</div>
    <div class="dr-punkte" aria-hidden="true">%s</div>
  </div>
</div></div>''' % (bilder, zaehler, worte, texte, punkte)


# ------------------------------------------------------------------ 2 Die Karte
KARTE = [('Chicken Chunks', 'Spicy Glaze, grüne Sauce'),
         ('Sandwich', 'Paprika Honey Mayo, Pickled Onions'),
         ('Pommes &amp; Krautsalat', 'kommen immer mit')]


def karte():
    zeilen = ''.join('<div class="ka-gericht sw auf" style="--i:%d"><span class="ka-nr mono">0%d</span><div><b>%s</b><span>%s</span></div></div>' % (
        2 + i, i + 1, n, z) for i, (n, z) in enumerate(KARTE))
    blatt = '''<div class="ka-blatt auf">
    <div class="ka-kopf"><span class="ka-d">%s</span><p class="ka-marke zl auf"><span class="z"><span style="--i:0">Dirty Chicken</span></span></p><p class="dcn-k sw auf" style="--i:1"><span>Sandwiches &amp; More</span></p></div>
    <div class="ka-liste">%s</div>
    <p class="ka-fuss sw auf" style="--i:5">Dirty Food &amp; Dirty Drinks</p>
  </div>''' % (bau.zeichen_haus('dc', 'ka-zeichen'), zeilen)
    def teller(k, sizes, text, cls, pos=None):
        return '<div class="ka-teller %s">%s%s</div>' % (cls, foto(k, '', sizes, auf=False, pos=pos), etikett(text))
    return '''<div class="vi ka">
  <div class="ka-oben"><div class="vk"><h2 class="zl auf dcn-titel" aria-label="Was auf den Tisch kommt."><span class="z"><span style="--i:0">Was auf den</span></span><span class="z"><span style="--i:1">Tisch kommt.</span></span></h2>%s</div></div>
  <div class="ka-tisch auf">%s%s%s%s%s</div>
  %s
</div>''' % (sw('So sah die Karte beim Pop-up aus: zwei Sachen, die wir können, und das, was immer dazukommt. Kein Burger, ’ne Ansage.', 'p', 'vtext dcn-text', 1),
             blatt,
             teller('dn_sosse', '(max-width:860px) 50vw, 33vw', 'Chicken Chunks · Spicy Glaze', 'ka-t1', '50% 55%'),
             teller('dn_burger', '(max-width:860px) 50vw, 33vw', 'Sandwich · Paprika Honey Mayo', 'ka-t2', '50% 55%'),
             teller('dn_tisch', '(max-width:860px) 100vw, 58vw', 'Alles auf einmal', 'ka-t3', '50% 50%'),
             teller('dn_salat', '(max-width:860px) 100vw, 42vw', 'Pommes &amp; Krautsalat', 'ka-t4', '50% 50%'),
             sw('Und zum Chicken: Dirty Drinks.', 'p', 'ueber dcn-ueber', 0))


# ------------------------------------------------------------------ 3 Dirty Drinks
def drinks():
    paar = '<div class="paar auf dri-paar">%s%s</div>' % (foto('dn_glas', '', '(max-width:860px) 50vw, 30vw', auf=False), foto('dc_drink', '', '(max-width:860px) 50vw, 30vw', auf=False))
    text = '''<div class="vk dri-text">%s%s%s<div class="sw auf knoepfe" style="--i:3">%s</div></div>''' % (
        kicker('Dirty Drinks', 0),
        zl(['Vom Tresen,', 'nicht vom Fass.'], 'h2', 'dcn-titel'),
        sw('Hinter dem Tresen stehen die Leute vom Walk on the Wild Side, der Bar in Linden, aus der Dirty Chicken kommt. Mixology ohne Karte: Du sagst, worauf du Lust hast, und es passt zum Chicken. Klar, kalt, mit ein paar Tropfen Öl auf der Oberfläche, oder lang und rot mit Eis.', 'p', 'vtext dcn-text', 2),
        knopf('Das Haus', 'bar.html', 'leise'))
    unten = '<div class="dri-unten auf"><div class="dri-u1">%s%s</div><div class="dri-u2">%s%s</div></div>' % (
        foto('dn_drinks', '', '(max-width:860px) 100vw, 58vw', auf=False, pos='50% 45%'), etikett('Drinks, Pommes, Chunks'),
        foto('dn_bar', '', '(max-width:860px) 100vw, 40vw', auf=False), etikett('An der Theke'))
    return '''<div class="vi dri"><div class="dri-oben">%s%s</div>%s%s</div>''' % (
        paar, text, unten, sw('Und dann ging das Licht an: Opening 2026.', 'p', 'ueber dcn-ueber', 0))


# ------------------------------------------------------------------ 4 Opening 2026
POP = [('Wann', '30. Mai 2026, 14 bis 22 Uhr'), ('Wo', 'AM:PM Café im Tiedthof, Goseriede&nbsp;4'), ('Was', 'Dirty Food, Dirty Drinks &amp;&nbsp;Live&nbsp;Music'),
       ('Gastschicht', 'Martin Bauermann, Beluga Vodka&nbsp;Berlin'), ('Danach', 'Aftershow im NATE'), ('Mit dabei', 'AM:PM, Walk on the Wild Side, Beluga,&nbsp;NATE')]
ZITATE = [('Wat ne Sause.', 'Opening, Juni 2026'), ('Jenau meen Ding wa.', 'Juni 2026'), ('Dit ist wahre Liebe!', 'Juni 2026')]


def opening():
    dl = '<dl class="vz op-vz sw auf" style="--i:3">%s</dl>' % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % z for z in POP)
    links = '<div class="op-text vk">%s%s%s%s</div>' % (
        kicker('Das erste Pop-up', 0),
        zl(['Opening', '2026.'], 'h2', 'dcn-titel'),
        sw('„Opening 2026! Wat ne Sause.“ Ein Nachmittag und ein Abend im Tiedthof, mit der Bar als Gastgeber, Live-Musik und Aftershow. Der Film ist von diesem Tag.', 'p', 'vtext dcn-text', 2),
        dl)
    def zitat(i, t, wer, g):
        return '<blockquote class="op-q" style="--g0:%s"><p class="zl auf" aria-label="%s"><span class="z"><span style="--i:%d">%s</span></span></p><cite class="mono sw auf" style="--i:%d">@dirtychicken.hannover · %s</cite></blockquote>' % (
            g, E(t), i, '„%s“' % t, i + 1, wer)
    rechts = '<div class="op-rechts">%s<div class="op-plakat auf" style="--g0:.5">%s%s</div>%s</div>' % (
        zitat(0, *ZITATE[0], '-.9'),
        foto('dc_plakat', '', '(max-width:860px) 60vw, 24vw', auf=False), etikett('Das Plakat'),
        zitat(2, *ZITATE[1], '1.1'))
    mitte = '<div class="op-film auf">%s%s</div>' % (film('opening', 'op-f', 'Opening 2026 bei Dirty Chicken, der Film vom Tag'), zitat(4, *ZITATE[2], '-.6'))
    return '<div class="vi op"><div class="op-raster">%s%s%s</div>%s</div>' % (
        links, mitte, rechts, sw('Und die, die das alles getragen haben: die Familie.', 'p', 'ueber dcn-ueber', 0))


# ------------------------------------------------------------------ 5 Familie
def familie():
    oben = '<div class="fa-oben"><div class="fa-film auf">%s%s</div><div class="vk fa-text">%s%s%s</div></div>' % (
        film('familie', 'fa-f', 'Die Mannschaft hinter der Theke'), etikett('Die Mannschaft, 10 Sekunden'),
        kicker('Die Familie', 0),
        zl(['Wenn aus Freunden', 'und Kollegen', 'Familie wird.'], 'h2', 'dcn-titel fa-titel'),
        sw('„Dann haste allet richtig jemacht!“ Die Leute hinter Dirty Chicken sind dieselben wie hinter dem Tresen der Bar und an der langen Tafel von Culinarium: eine Mannschaft, drei Abende, die man nicht verwechselt.', 'p', 'vtext dcn-text', 4))
    paar = '<div class="paar auf fa-paar">%s%s</div>' % (foto('dc_team', '', '(max-width:860px) 50vw, 45vw', auf=False, pos='50% 40%'), foto('dc_team2', '', '(max-width:860px) 50vw, 45vw', auf=False, pos='50% 40%'))
    return '<div class="vi fa">%s%s%s</div>' % (oben, paar, sw('Bleibt die Frage: Wann wieder?', 'p', 'ueber dcn-ueber', 0))


# ------------------------------------------------------------------ 6 Das nächste Mal
BAND = ['Fried Chicken', 'Sandwiches &amp; More', 'Chicken Chunks mit Spicy Glaze', 'Dirty Food &amp; Dirty Drinks', 'Pommes &amp; Krautsalat', 'Live-Musik', 'Nur an einzelnen Tagen']


def naechstes():
    eins = ''.join('<span>%s</span>%s' % (w, fuss_svg()) for w in BAND)
    band = '<div class="am-band dcn-band" aria-hidden="true"><div class="am-band-zug"><p>%s</p><p>%s</p></div></div>' % (eins, eins)
    mitte = '''<div class="na-mitte auf">
    <div class="na-zeichen">%s</div>
    <div class="vk mitte na-text">%s%s%s<div class="sw auf knoepfe" style="--i:3"><a class="knopf violett" href="%s" target="_blank" rel="noopener" aria-label="Dirty Chicken auf Instagram"><span>@d<em class="ki">i</em>rtych<em class="ki">i</em>cken.hannover</span><i>%s</i></a></div></div>
  </div>''' % (bau.zeichen_haus('dc', 'na-d'), kicker('Das nächste Pop-up', 0),
               zl(['Wann wieder?'], 'h2', 'dcn-titel na-titel'),
               sw('Wann und wo es Dirty Chicken als Nächstes gibt, steht zuerst auf Instagram. Dort gehen auch die Plätze weg, bevor jemand fragt.', 'p', 'vtext dcn-text', 2),
               IG, bau.PFEIL)
    def tuer(k, pos, etik, name, satz, kn, i):
        return '<a class="na-tuer auf" href="%s" style="--i:%d">%s<div class="na-tuer-text"><p class="dcn-k"><span>%s</span></p><p class="na-tuer-name">%s</p><p class="na-tuer-satz">%s</p><span class="na-tuer-kn"><span>%s</span><i>%s</i></span></div></a>' % (
            kn[1], i, foto(k, '', '(max-width:860px) 100vw, 44vw', auf=False, pos=pos), etik, name, satz, kn[0], bau.PFEIL)
    tueren = '<div class="na-tueren"><p class="na-haus zl auf"><span class="z"><span style="--i:0">Aus demselben Haus.</span></span></p><div class="na-tuer-reihe">%s%s</div></div>' % (
        tuer('tafelleer', '50% 58%', 'Die Abende', 'Culinarium', 'Ein Menü mit fünf passenden Drinks an einer langen Tafel für vierzehn Gäste, an einzelnen Wochenenden.', ('Zu Culinarium', 'index.html'), 1),
        tuer('theke', '50% 40%', 'Das Haus', 'Walk on the Wild Side', 'Die Bar in Linden, Haasemannstraße 13: Mixology ohne Karte, Donnerstag bis Samstag ab 19 Uhr.', ('Das Haus', 'bar.html'), 2))
    return '%s<div class="vi na">%s%s</div>' % (band, mitte, tueren)


def seite():
    """Alle Teile nach Hero und Fenster, in der Reihenfolge der Geschichte."""
    return ''.join([
        abschnitt('drei', 'nacht', drei(), 'Drei Worte'),
        abschnitt('karte', 'hell', karte(), 'Die Karte'),
        abschnitt('drinks', 'nacht', drinks(), 'Dirty Drinks'),
        abschnitt('opening', 'dc', opening(), 'Opening 2026'),
        abschnitt('familie', 'warm', familie(), 'Familie'),
        abschnitt('naechstes', 'dc', naechstes(), 'Wann wieder'),
    ])


def einbinden(h):
    """Eigenes CSS und JS nur für diese Seite, hinter den gemeinsamen Dateien."""
    h = h.replace('<link rel="stylesheet" href="assets/culinarium.css?v=%s">' % bau.VERSION,
                  '<link rel="stylesheet" href="assets/culinarium.css?v=%s">\n<link rel="stylesheet" href="assets/dirty-chicken.css?v=%s">' % (bau.VERSION, bau.VERSION), 1)
    h = h.replace('<script src="assets/culinarium.js?v=%s" defer></script>' % bau.VERSION,
                  '<script src="assets/culinarium.js?v=%s" defer></script>\n<script src="assets/dirty-chicken.js?v=%s" defer></script>' % (bau.VERSION, bau.VERSION), 1)
    return h
