#!/usr/bin/env python3
"""Dirty Chicken · Abschnitt nach dem Essen («Dirty Food, Dirty Drinks»: Glas, Film, Mannschaft) in 15 Fassungen zur Wahl (27.10.2026, 23:20).
Robert: «15 verschiedene Visualisierungsmöglichkeiten … das muss jetzt richtig überborden, richtig geil, richtig krass … damit das richtig sexy im Kopf bleibt.»
Der Teil erzählt die Nacht des Pop-ups: Dirty Drinks von der Bar, Live-Musik, die Mannschaft, Opening 2026. Material: Glas mit Öltropfen (84612), Theke (84611),
Drinks von oben (84683), Mannschaft im AM:PM (84558), beide Teamfotos von Instagram, das Plakat, Tisch (DZiug6EoMRr, 84678), Karte (84626), Sauce (84676),
der Opening-Film (9:16, 33 s, nie beschnitten), der Film der Mannschaft (1:1) und acht Standbilder aus dem Opening-Film (assets/film/opening-still-*.webp).
Nicht noch einmal: die Bilder des Essen-Teils (DZIo4FHIqRR, 84673, 84607). Jede Fassung ein anderes Gerüst, ein eigener bewegter Moment, nur transform und opacity,
nie zwei Fotos übereinander, Gesichter unberührt. Baut dirty-chicken-nacht-wahl.html (Hero, Fenster, Essen wie auf der echten Seite, dann der Teil umschaltbar; ?nacht=Nummer, 0 = heute).
Aufruf: python3 website/dc_nacht_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, foto, zl, sw
import varianten
import dc_essen

HIER = bau.HIER
KICK = 'Dirty Drinks &amp; Live-Musik'
TEXT = 'Die Drinks kommen von der Bar, die Musik vom Pop-up, und am Ende steht die ganze Mannschaft hinter dem Tresen. Opening 2026: „Wat ne Sause.“'
STILLS = [1, 5, 9, 13, 17, 21, 25, 29]


def ek(text, i=0):
    return '<p class="ek sw auf" style="--i:%d"><span>%s</span></p>' % (i, text)


def et(zeilen, cls='', i0=0):
    return zl(zeilen, 'h2', ('et ' + cls).strip(), i0)


def ex(text, i=2, cls=''):
    return sw(text, 'p', ('ex ' + cls).strip(), i)


def film(n, cls=''):
    # filmw statt film: der gemeinsame Abspieler würde sonst alle 17 Filme der Wahlseite auf einmal laden; dc-nacht-wahl.js spielt nur die gezeigte Fassung
    return ('<figure class="filmw %s" style="--lq:url(assets/film/%s.webp);aspect-ratio:%s"><video muted playsinline loop preload="none" poster="assets/film/%s.webp?v=%s" data-film="assets/film/%s.mp4?v=%s" aria-label="%s"></video>'
            '</figure>') % (
        cls, n, '1/1' if n == 'familie' else '9/16', n, VERSION, n, VERSION, 'Die Mannschaft hinter der Theke' if n == 'familie' else 'Opening 2026 bei Dirty Chicken')


def still(t, cls=''):
    return '<figure class="nx-still %s"><img src="assets/film/opening-still-%d.webp?v=%s" alt="Standbild aus dem Film vom Opening" loading="eager" decoding="async"></figure>' % (cls, t, VERSION)


def d_zeichen(cls=''):
    return bau.zeichen_haus('dc', cls)


def kopf(kick=KICK, titel=('Jenau meen', 'Ding wa.'), text=TEXT, cls=''):
    return '<div class="vk nx-kopf %s">%s%s%s</div>' % (cls, ek(kick), et(list(titel)), ex(text))


def sec(n, ton, inner, cls=''):
    return '<section class="vab dc-ab ess nxs%02d %s" data-ton="%s">%s</section>' % (n, cls, ton, inner)


F = []

# 1 Die Bahnen: drei Bildbahnen laufen gegenläufig über die ganze Breite, der Film fährt in der mittleren mit
BAHNEN = [['dn_glas', 'dn_team', 'dc_tisch', 'dn_karte', 'dn_sosse', 'dn_tisch'], ['dc_team', 'film:opening', 'dn_drinks', 'dc_plakat', 'dn_bar', 'dc_team2']]
def bahn(ks, i):
    # jede Bahn zweimal die sechs Stücke je Kopie, damit die Schleife auch auf breiten Schirmen keine Lücke lässt (Kopie breiter als der Schirm)
    eins = ''.join(film('opening', 'nx1-f') if k == 'film:opening' else foto(k, '', '(max-width:860px) 60vw, 28vw', auf=False, ratio=True) for k in ks * 2)
    return '<div class="nx1-bahn b%d" aria-hidden="%s"><div class="nx1-zug">%s%s</div></div>' % (i, 'false' if i == 1 else 'true', eins, eins)
F.append(('Die Bahnen', 'Zwei Bildbahnen laufen gegenläufig über die ganze Breite, der Film fährt in der unteren mit; oben der Titel.', sec(1, 'dc', '<div class="vi">%s</div><div class="nx1-bahnen">%s</div>' % (
    kopf(), ''.join(bahn(ks, i) for i, ks in enumerate(BAHNEN))))))

# 2 Der Filmstreifen: acht Standbilder als Filmstreifen, der mit dem Scrollen seitwärts zieht; darunter der Film selbst
F.append(('Der Filmstreifen', 'Acht Standbilder aus dem Opening-Film als Filmstreifen mit Perforation, der beim Scrollen seitwärts zieht; darunter läuft der Film selbst.', sec(2, 'nacht', '''<div class="vi">%s</div>
<div class="nx2-streifen"><div class="nx2-spur">%s</div></div>
<div class="vi nx2-unten"><div class="nx2-film auf">%s</div><div class="vk">%s%s</div></div>''' % (
    kopf(titel=('Der Film', 'vom Tag.')), ''.join(still(t) for t in STILLS), film('opening', 'nx2-f'), ek('33 Sekunden, Juni 2026', 0),
    ex('„Opening 2026! Wat ne Sause.“ Der Film ist von diesem Tag: die Drinks, die Leute, das Chicken. Gedreht im AM:PM Café im Tiedthof.', 1)))))

# 3 Das zweite Fenster: die Theke steht als Fenster, die Seite zieht darüber; danach Film und Mannschaft
F.append(('Das zweite Fenster', 'Die dunkle Theke mit Glas und Chicken steht als Fenster, die Seite zieht darüber, ein Satz darauf; danach Film und Mannschaft nebeneinander.', '''<section class="fenster" id="fenster-nacht" aria-label="Dirty Drinks">
  <div class="fenster-schicht">%s<div class="fenster-hof"></div><p class="fenster-satz zl"><span class="z"><span style="--i:0">Dirty Drinks.</span></span><span class="z"><span style="--i:1">Jenau meen Ding wa.</span></span></p></div>
</section>''' % foto('dn_bar', '', '100vw', auf=False, pos='50% 50%') + sec(3, 'nacht', '''<div class="vi nx3"><div class="nx3-film auf">%s</div><div class="nx3-rechts"><div class="nx3-bild auf">%s</div>%s</div></div>''' % (
    film('opening', 'nx3-f'), foto('dn_team', '', '(max-width:860px) 100vw, 56vw', auf=False, pos='50% 42%'), kopf(titel=('Live-Musik.',))))))

# 4 Der Equalizer: neun hohe Bildstreifen tanzen wie ein Equalizer, der Film ist der Bass in der Mitte
EQ = ['dn_glas', 'dn_bar', 'dc_tisch', 'dn_team', 'film:opening', 'dc_team2', 'dn_drinks', 'dc_plakat', 'dn_tisch']
F.append(('Der Equalizer', 'Neun hohe Bildstreifen wippen in eigenem Takt wie ein Equalizer, der Film steht als Bass in der Mitte und läuft.', sec(4, 'dc', '<div class="vi">%s</div><div class="nx4-eq auf">%s</div>' % (
    kopf(titel=('Live-', 'Musik.')), ''.join(
        '<div class="nx4-s s%d" style="--t:%.2fs;--d:%.2fs">%s</div>' % (i, 1.1 + (i * 7 % 5) * .18, (i * 3 % 7) * .13, film('opening', 'nx4-f') if k == 'film:opening' else foto(k, '', '(max-width:860px) 30vw, 11vw', auf=False))
        for i, k in enumerate(EQ))))))

# 5 Stories: fünf Hochformate wie auf Instagram, die mittlere spielt den Film; antippen holt eine Karte in die Mitte
STORIES = [('dc_plakat', 'Das Plakat'), ('dn_glas', 'Dirty Drinks'), ('film', 'Opening 2026'), ('dn_team', 'Die Mannschaft'), ('dc_team2', 'Wat ne Sause')]
def story(i, k, t):
    kopfz = '<div class="nx5-kopf"><i class="nx5-balken"></i><p class="nx5-wer">%s<span>dirtychicken.hannover</span><b>%s</b></p></div>' % (d_zeichen('nx5-d'), t)
    inner = film('opening', 'nx5-f') if k == 'film' else foto(k, '', '(max-width:860px) 70vw, 22vw', auf=False, pos='50% 40%')
    return '<button type="button" class="nx5-k" data-i="%d" aria-label="%s">%s%s</button>' % (i, E(t), inner, kopfz)
F.append(('Stories', 'Fünf Hochformate wie Instagram-Stories nebeneinander, die mittlere spielt den Film; antippen holt eine andere Karte in die Mitte, nichts springt.', sec(5, 'nacht', '<div class="vi">%s</div><div class="nx5-buehne auf" data-akt="2"><div class="nx5-spur">%s</div></div>' % (
    kopf(cls='mitte'), ''.join(story(i, k, t) for i, (k, t) in enumerate(STORIES))))))

# 6 Durch die Buchstaben: DRINKS über die ganze Breite, durch die Buchstaben zieht der Tisch mit den Drinks; daneben der Film
F.append(('Durch die Buchstaben', 'Das Wort DRINKS über die ganze Breite, durch die Buchstaben zieht beim Scrollen der Tisch mit den Drinks; darunter Live-Musik mit dem Film.', sec(6, 'nacht', '''<div class="vi">%s</div>
<div class="nx6-wort auf"><svg viewBox="0 0 1600 420" aria-hidden="true"><defs><clipPath id="nx6c"><text x="800" y="392" text-anchor="middle">DRINKS</text></clipPath></defs>
<g clip-path="url(#nx6c)"><rect width="1600" height="420" fill="#3B1F4D"/><image class="nx6-bild" href="assets/bild/dn_drinks-1600.webp?v=%s" x="0" y="-200" width="1600" height="2130" preserveAspectRatio="xMidYMid slice"/></g></svg></div>
<div class="vi nx6-unten"><div class="vk"><h3 class="zl auf nx6-t" aria-label="&amp; Live-Musik."><span class="z"><span style="--i:0">&amp; Live-Musik.</span></span></h3>%s</div><div class="nx6-film auf">%s</div></div>''' % (
    kopf(titel=('Dirty',), text=''), VERSION, ex(TEXT, 1), film('opening', 'nx6-f')))))

# 7 Die Liste: Zeilen der Nacht, das Bild folgt der Maus über der Zeile (eigener Effekt aus dem Fundus); am Handy tauscht ein Bild oben
LISTE = [('Dirty Drinks', 'von der Bar, ohne Karte', 'dn_glas'), ('Live-Musik', 'den ganzen Abend', 'dn_team'), ('Gastschicht', 'Martin Bauermann, Beluga Vodka Berlin', 'dn_bar'),
         ('Aftershow', 'im NATE', 'dc_team2'), ('Die Mannschaft', 'hinter dem Tresen', 'dc_team'), ('Das Plakat', '30. Mai 2026, AM:PM', 'dc_plakat')]
F.append(('Die Liste', 'Die Nacht als Zeilen; wo die Maus über eine Zeile fährt, folgt ihr das Bild dazu (eigener Effekt aus deinem Fundus). Am Handy tippst du, das Bild oben tauscht.', sec(7, 'warm', '''<div class="vi nx7"><div class="nx7-links">%s<div class="nx7-film auf">%s</div></div>
<div class="nx7-rechts"><div class="nx7-handy auf" data-wahl="0">%s</div><ul class="hr-list nx7-liste" data-hover-reveal>%s</ul></div></div>''' % (
    kopf(titel=('Eine', 'Nacht.')), film('familie', 'nx7-f'),
    ''.join('<div class="nx7-hb" data-s="%d">%s</div>' % (i, foto(k, '', '100vw', auf=False, pos='50% 40%')) for i, (_n, _s, k) in enumerate(LISTE)),
    ''.join('<li class="hr-item nx7-z" data-hr-src="assets/bild/%s-%d.webp?v=%s" data-s="%d"><a href="#nacht" class="nx7-a"><b>%s</b><span>%s</span></a></li>' % (k, max(w for w in bau.META[k]['stufen'] if w <= 1000), VERSION, i, n, s) for i, (n, s, k) in enumerate(LISTE))))))

# 8 Die Lichterkette: runde Bilder hängen wie Glühbirnen an einer Schnur und schaukeln; darunter der Film gross
KETTE = [('dn_glas', 6, 0), ('dn_bar', 20, 14), ('dc_tisch', 34, 24), ('dn_karte', 50, 28), ('dn_drinks', 66, 24), ('dc_plakat', 80, 14), ('dn_tisch', 94, 0)]
F.append(('Die Lichterkette', 'Runde Bilder hängen wie Glühbirnen an einer durchhängenden Schnur und schaukeln leicht; darunter der Film gross und der Text.', sec(8, 'nacht', '''<div class="vi">%s</div>
<div class="nx8-kette auf"><svg class="nx8-schnur" viewBox="0 0 1600 160" preserveAspectRatio="none" aria-hidden="true"><path d="M0 20 Q800 180 1600 20" fill="none" stroke="rgba(255,247,239,.5)" stroke-width="2"/></svg>%s</div>
<div class="vi nx8-unten"><div class="nx8-film auf">%s</div><div class="vk">%s%s</div></div>''' % (
    kopf(titel=('Die Nacht', 'geht an.'), text='', cls='mitte'),
    ''.join('<div class="nx8-b" style="--x:%d%%;--y:%dpx;--t:%.1fs;--i:%d">%s</div>' % (x, y, 3.2 + i * .35, i, foto(k, '', '(max-width:860px) 26vw, 11vw', auf=False)) for i, (k, x, y) in enumerate(KETTE)),
    film('opening', 'nx8-f'), ek(KICK, 0), ex(TEXT, 1)))))

# 9 Der Vorhang: ein violetter Vorhang geht auf und gibt die Bühne frei: Film in der Mitte, die Mannschaft links und rechts
F.append(('Der Vorhang', 'Ein violetter Vorhang mit Tapete geht beim Ankommen auf und gibt die Bühne frei: der Film in der Mitte, links und rechts die Mannschaft.', sec(9, 'nacht', '''<div class="nx9-buehne auf"><div class="nx9-hinten"><div class="nx9-h l">%s</div><div class="nx9-h m">%s</div><div class="nx9-h r">%s</div></div>
<div class="nx9-v l" aria-hidden="true"></div><div class="nx9-v r" aria-hidden="true"></div></div><div class="vi nx9-unten">%s</div>''' % (
    foto('dn_team', '', '(max-width:860px) 50vw, 34vw', auf=False, pos='50% 42%'), film('opening', 'nx9-f'), foto('dc_team2', '', '(max-width:860px) 50vw, 34vw', auf=False, pos='50% 40%'),
    kopf(titel=('Bühne frei.',))))))

# 10 Blitzlicht: Partyfotos tauchen eins nach dem anderen mit Blitz auf, leicht gedreht, keins über dem anderen
BLITZ = [('dn_team', -2.5), ('dn_glas', 2), ('dc_team', -1.5), ('film', 1), ('dn_bar', 2.5), ('dc_tisch', -2), ('dc_plakat', 1.5), ('dc_team2', -1)]
F.append(('Blitzlicht', 'Acht Partyfotos tauchen eins nach dem anderen auf wie geblitzt, jedes leicht gedreht, keins über dem anderen; der Film der Mannschaft ist eins davon.', sec(10, 'nacht', '<div class="vi">%s<div class="nx10-wand auf">%s</div></div>' % (
    kopf(titel=('Wat ne', 'Sause.')), ''.join('<div class="nx10-f" style="--i:%d;--r:%.1fdeg">%s</div>' % (i, r, film('familie', 'nx10-film') if k == 'film' else foto(k, '', '(max-width:860px) 50vw, 24vw', auf=False, pos='50% 40%'))
                                                for i, (k, r) in enumerate(BLITZ))))))

# 11 Der Ablauf: Nachmittag, Abend, Nacht, Danach als Stationen auf einer Linie, jede mit Bild oder Film
ABLAUF = [('Nachmittag', 'Ab 14 Uhr: die Chunks kommen raus, Sauce drauf.', 'dn_sosse'), ('Abend', 'Dirty Drinks von der Bar, Gastschicht Martin Bauermann, Beluga Vodka Berlin.', 'dn_glas'),
          ('Nacht', 'Live-Musik, bis 22 Uhr. Der Film ist von diesem Tag.', 'film'), ('Danach', 'Aftershow im NATE. Wenn aus Freunden und Kollegen Familie wird.', 'dc_team2')]
F.append(('Der Ablauf', 'Der Tag des Pop-ups als Linie mit vier Stationen: Nachmittag, Abend, Nacht, Danach, jede mit Bild oder Film und einem Satz.', sec(11, 'warm', '<div class="vi">%s<div class="nx11-linie auf">%s</div></div>' % (
    kopf(titel=('Ein Tag,', 'eine Nacht.')), ''.join('<div class="nx11-st" style="--i:%d"><h3 class="zl auf" aria-label="%s"><span class="z"><span style="--i:%d">%s</span></span></h3><div class="nx11-b">%s</div>%s</div>' % (
        i, E(n), i, n, film('opening', 'nx11-f') if k == 'film' else foto(k, '', '(max-width:860px) 100vw, 22vw', auf=False), ex(s, i + 1)) for i, (n, s, k) in enumerate(ABLAUF))))))

# 12 Die Doppelseite: eine Magazin-Doppelseite, links das grosse Foto, rechts Schlagzeile, Text in Spalten und der Film als Kasten
F.append(('Die Doppelseite', 'Eine helle Magazin-Doppelseite: links die Mannschaft als ganzseitiges Foto, rechts Schlagzeile, Text in zwei Spalten und der Film als Kasten mit Bildzeile.', sec(12, 'hell', '''<div class="vi nx12"><div class="nx12-seite l auf">%s<span class="nx12-nr mono">14</span></div>
<div class="nx12-seite r"><p class="nx12-dach mono sw auf" style="--i:0">Dirty Chicken · Opening 2026 · AM:PM Café im Tiedthof</p>%s
<div class="nx12-spalten"><p class="sw auf" style="--i:2">%s</p><p class="sw auf" style="--i:3">Dit is keen Burger, dit Ding is ’ne Ansage: Fried Chicken, das kracht, dazu Dirty Drinks und Live-Musik, einen Nachmittag und einen Abend lang. Danach Aftershow im NATE.</p></div>
<div class="nx12-kasten auf">%s<p class="nx12-bz">Der Film vom Tag, 33 Sekunden. <span class="mono">@dirtychicken.hannover</span></p></div><span class="nx12-nr mono r">15</span></div></div>''' % (
    foto('dn_team', '', '(max-width:860px) 100vw, 50vw', auf=False, pos='50% 42%'), et(['Wat ne', 'Sause.'], 'nx12-t', 1), TEXT, film('opening', 'nx12-f')))))

# 13 Die Kachelwand: die grüne Fliesenwand der Bar als Raster, Kacheln sind Fotos, Farbe oder Wörter, der Film ist zwei Kacheln hoch
KACHELN = [('f', 'dn_glas'), ('w', 'DIRTY'), ('f', 'dn_team'), ('film', ''), ('f', 'dc_tisch'), ('w', 'DRINKS'),
           ('w', 'LIVE'), ('f', 'dn_bar'), ('f', 'dc_team'), ('k', ''), ('f', 'dn_drinks'), ('f', 'dc_plakat'),
           ('f', 'dn_karte'), ('k', ''), ('w', 'MUSIK'), ('f', 'dc_team2'), ('f', 'dn_tisch'), ('w', 'SAUSE')]
def kachel(i, art, v):
    if art == 'film':
        return '<div class="nx13-k film2" style="--i:%d">%s</div>' % (i, film('opening', 'nx13-f'))
    if art == 'f':
        return '<div class="nx13-k" style="--i:%d">%s</div>' % (i, foto(v, '', '(max-width:860px) 33vw, 16vw', auf=False, pos='50% 40%'))
    if art == 'w':
        return '<div class="nx13-k wort" style="--i:%d"><span>%s</span></div>' % (i, v)
    return '<div class="nx13-k farbe" style="--i:%d"></div>' % i
F.append(('Die Kachelwand', 'Die grüne Fliesenwand der Bar als Raster: Kacheln sind Fotos, Farbe oder ein Wort, der Film ist zwei Kacheln hoch; die Wand setzt sich Kachel für Kachel.', sec(13, 'nacht', '<div class="vi">%s<div class="nx13-wand auf">%s</div></div>' % (
    kopf(titel=('Hinter', 'der Theke.')), ''.join(kachel(i, a, v) for i, (a, v) in enumerate(KACHELN))))))

# 14 Prost: zwei Gläser kommen beim Scrollen von links und rechts aufeinander zu und stossen an der Naht an; darunter der Film
F.append(('Prost', 'Zwei Gläser kommen beim Scrollen von links und rechts aufeinander zu und stossen in der Mitte an, erst dann steht das Paar; darunter Film und Text.', sec(14, 'dc', '''<div class="vi">%s</div>
<div class="nx14-paar"><div class="nx14-g l">%s</div><div class="nx14-g r">%s</div></div>
<div class="vi nx14-unten"><div class="nx14-film auf">%s</div><div class="vk">%s%s</div></div>''' % (
    kopf(titel=('Prost.',), text='', cls='mitte'), foto('dn_glas', '', '(max-width:860px) 50vw, 44vw', auf=False), foto('dn_bar', '', '(max-width:860px) 50vw, 44vw', auf=False),
    film('opening', 'nx14-f'), ek(KICK, 0), ex(TEXT, 1)))))

# 15 Der Rahmen: der Film in der Mitte, zehn Fotos schliessen sich beim Ankommen als Rahmen um ihn
RAHMEN = {'o': ['dn_glas', 'dn_team', 'dc_tisch', 'dn_karte'], 'u': ['dn_bar', 'dc_team', 'dn_drinks', 'dc_plakat'], 'l': ['dn_tisch'], 'r': ['dc_team2']}
F.append(('Der Rahmen', 'Der Film steht in der Mitte, zehn Fotos kommen von oben, unten, links und rechts herein und schliessen sich als Rahmen um ihn.', sec(15, 'nacht', '''<div class="vi">%s</div>
<div class="nx15-rahmen auf"><div class="nx15-reihe o">%s</div><div class="nx15-mitte"><div class="nx15-seite l">%s</div><div class="nx15-film">%s</div><div class="nx15-seite r">%s</div></div><div class="nx15-reihe u">%s</div></div>''' % (
    kopf(cls='mitte'),
    ''.join('<div class="nx15-b" style="--i:%d">%s</div>' % (i, foto(k, '', '(max-width:860px) 50vw, 22vw', auf=False, pos='50% 40%')) for i, k in enumerate(RAHMEN['o'])),
    foto(RAHMEN['l'][0], '', '(max-width:860px) 50vw, 22vw', auf=False), film('opening', 'nx15-f'), foto(RAHMEN['r'][0], '', '(max-width:860px) 50vw, 22vw', auf=False, pos='50% 40%'),
    ''.join('<div class="nx15-b" style="--i:%d">%s</div>' % (i, foto(k, '', '(max-width:860px) 50vw, 22vw', auf=False, pos='50% 40%')) for i, k in enumerate(RAHMEN['u']))))))


def main():
    s = [bau.kopf('Nacht wählen · Dirty Chicken', 'Dirty Chicken: der Abschnitt nach dem Essen in 15 Fassungen zur Wahl.', 'dirty-chicken.html', 'dc')]
    k, n, c = varianten.DCSEITE[0]
    s.append(varianten.abschnitt(k, n, c, idn=False).replace('class="vab ', 'class="vab dc-ab bar-ab ', 1))
    s.append('''<section class="fenster" id="fenster-dc" aria-label="Die Ansage">
  <div class="fenster-schicht">%s<div class="fenster-hof"></div><p class="fenster-satz zl"><span class="z"><span style="--i:0">Dit is keen Burger.</span></span><span class="z"><span style="--i:1">Dit Ding is ’ne Ansage.</span></span></p></div>
</section>''' % foto('dn_burger', '', '100vw', auf=False, pos='50% 55%'))
    s.append(dc_essen.essen())
    k, n, c = varianten.DCSEITE[1]
    heute = varianten.abschnitt(k, n, c, idn=False).replace('class="vab ', 'class="vab dc-ab bar-ab ', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % heute]
    teile += ['<div class="wv" data-n="%d" hidden>%s</div>' % (i, h) for i, (_n, _s, h) in enumerate(F, 1)]
    s.append('<section class="dw wahl" data-ton="nacht" id="nacht" data-name="Nacht"><div class="wahl-marke"><b>Nacht</b><span data-nr></span></div>%s</section>' % ''.join(teile))
    s.append(bau.fuss())
    h = ''.join(s)
    namen = ['Heute: Glas, Film, Mannschaft'] + [re.sub('&amp;', '&', n) for n, _s, _h in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('dc-nacht-wahl.css', 'dc-nacht-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["nacht"],daumen:%s};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/dc-nacht-wahl.js?v=%s" defer></script>
<script type="module">import { initHoverReveal } from './assets/hr.js?v=%s'; if (matchMedia('(hover:hover)').matches) initHoverReveal(null, { width: 380, ratio: 1.25, ease: .16, tilt: 8 });</script>''' % (
        json.dumps(namen, ensure_ascii=False), 'true' if os.path.exists(os.path.join(HIER, 'assets/daumen/nacht-1.jpg')) else 'false', VERSION, v, VERSION)
    h = h.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/hr.css?v=%s">\n<link rel="stylesheet" href="assets/dc-nacht-wahl.css?v=%s">\n</head>' % (VERSION, VERSION, v), 1)
    h = h.replace('</body>', leiste + '\n</body>', 1)
    for fk in varianten.FILMLQ:
        h = h.replace('--lq:url(assets/film/%s.webp)' % fk, '--lq:url(%s)' % varianten.FILMLQ[fk])
    open(os.path.join(HIER, 'dirty-chicken-nacht-wahl.html'), 'w', encoding='utf-8').write(h)
    json.dump([{'nr': i, 'name': n, 'satz': s_} for i, (n, s_, _h) in enumerate(F, 1)], open(os.path.join(HIER, '_sicherung', 'nacht-fassungen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Seite dirty-chicken-nacht-wahl.html', len(h) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
