#!/usr/bin/env python3
"""Dirty Chicken · «Wie Dirty Chicken von sich spricht», zweite Runde: 15 weitere Fassungen (Robert 28.10.2026: «nochmal 15»).
Erste Runde: dirty-chicken-zitate-wahl.html (dc_zitate_wahl.py). Hier nichts davon noch einmal: keine Buchstabentafel, Leuchtschrift, Übersetzung,
Wörterbuch, Stempel, Nachrichten, Titelseite, Satz für Satz, Untertitel, Fahnen, Ansage, Rad, Streifen, Lauter, Bierdeckel.
Dieselben fünf echten Sätze von @dirtychicken.hannover (Juni 2026) mit ihren Bildern. Jede Fassung ein eigener Gegenstand aus der Welt des Pop-ups
(Einschlagpapier, Spiess im Sandwich, Sterne vom Plakat, Platte für die Live-Musik, Fotoautomat, Abreisskalender, Hühnerfuss),
ein eigener bewegter Moment, nur transform und opacity, keine Fotos übereinander, Gesichter unberührt.
Baut dirty-chicken-zitate-wahl-2.html (?zitate2=Nummer, 0 = heute).
Aufruf: python3 website/dc_zitate_wahl_2.py"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, foto, zl, sw
import varianten
import dc_essen
import dc_nacht
from dc_zitate_wahl import Z, q, ek, et, ex, kopf, datum, d_zeichen, zeilenbrechen

HIER = bau.HIER


def sec(n, ton, inner, cls=''):
    return '<section class="vab dc-ab ess zus%02d %s" data-ton="%s">%s</section>' % (n, cls, ton, inner)


def roh(s):
    return re.sub('&amp;', '&', s)


F = []

# 1 Das Essen spricht: fünf Bilder als Mosaik, aus jedem kommt eine Sprechblase mit dem Satz des Beitrags
ESSEN = [('dc_burger', 'grid-column:1;grid-row:1/3', 'b-u-r', '50% 50%'), ('dc_drink', 'grid-column:2;grid-row:1', 'b-u-l', '50% 50%'),
         ('dc_team', 'grid-column:2;grid-row:2', 'b-o-l', '50% 40%'), ('dc_plakat', 'grid-column:3;grid-row:1', 'b-u-l', '50% 40%'), ('dc_tisch', 'grid-column:3;grid-row:2', 'b-u-r', '50% 50%')]
F.append(('Das Essen spricht', 'Fünf Bilder als Mosaik Kante an Kante, und aus jedem kommt eine Sprechblase mit seinem Satz: der Burger sagt «Dit is keen Burger», der Tisch sagt «Dit ist wahre Liebe». Die Blasen springen nacheinander auf.', sec(1, 'nacht', '<div class="vi">%s<div class="zu1-wand auf">%s</div></div>' % (
    kopf(text='Wer hier redet? Dit Essen. So stand es im Juni 2026 auf Instagram.'),
    ''.join('<div class="zu1-f" style="%s">%s<div class="zu1-blase %s" style="--i:%d"><p>%s</p>%s</div></div>' % (
        st, foto(k, '', '(max-width:860px) 100vw, 34vw', auf=False, pos=pos, extra='style="--weg:0px"'), b, i, q(s), datum(d))
        for i, ((k, st, b, pos), (s, _h, d, _k, _p)) in enumerate(zip(ESSEN, Z)))))))

# 2 Die Neonschrift: die Sätze als Leuchtröhren an der grünen Fliesenwand der Bar; beim Ankommen gehen sie nacheinander an
NEON = [('n-gross n-lila', 4), ('n-weiss', 0), ('n-kerze', 1), ('n-weiss', 2), ('n-lila', 3)]
F.append(('Die Neonschrift', 'Die Sätze als Leuchtröhren an der grünen Fliesenwand der Bar. Erst sieht man die kalten Röhren, dann gehen sie nacheinander an, «Dit ist wahre Liebe!» gross in Lila.', sec(2, 'nacht', '''<div class="vi">%s</div>
<div class="zu2-wand auf"><div class="zu2-innen">%s</div></div>''' % (
    kopf(cls='mitte'),
    ''.join('<div class="zu2-s %s" style="--i:%d"><p class="zu2-r" aria-hidden="true">%s</p><p class="zu2-l">%s</p>%s</div>' % (c, j, roh(Z[i][0]), roh(Z[i][0]), datum(Z[i][2])) for j, (c, i) in enumerate(NEON))))))

# 3 Die Schallplatte: das Plakat ist die Hülle, die Platte zieht beim Scrollen heraus und dreht sich; daneben Seite A und Seite B mit den Sätzen
F.append(('Die Schallplatte', 'Live-Musik gehört dazu: Das Plakat ist die Plattenhülle, die Platte mit dem Zeichen auf dem Etikett zieht beim Scrollen heraus und dreht sich. Daneben Seite A und Seite B, die Sätze als Titel.', sec(3, 'warm', '''<div class="vi zu3"><div class="zu3-spieler auf"><div class="zu3-platte"><div class="zu3-rillen"></div><div class="zu3-etikett">%s<span>Dirty Chicken<br>Opening 2026</span></div></div><div class="zu3-huelle">%s</div></div>
<div class="zu3-rechts">%s<div class="zu3-seite"><p class="zu3-s-kopf">Seite A</p>%s</div><div class="zu3-seite"><p class="zu3-s-kopf">Seite B</p>%s</div></div></div>''' % (
    d_zeichen('zu3-z'), foto('dc_plakat', '', '(max-width:860px) 80vw, 38vw', auf=False, extra='style="--weg:0px"'),
    kopf(kick='Dirty Food, Dirty Drinks &amp; Live-Musik', text=''),
    ''.join('<div class="zu3-t sw auf" style="--i:%d"><b>%s</b>%s</div>' % (i + 2, roh(s), datum(d)) for i, (s, _h, d, _k, _p) in enumerate(Z[:3])),
    ''.join('<div class="zu3-t sw auf" style="--i:%d"><b>%s</b>%s</div>' % (i + 5, roh(s), datum(d)) for i, (s, _h, d, _k, _p) in enumerate(Z[3:]))))))

# 4 Die Spiesse: in jedem Bild steckt ein Fähnchen auf einem Holzspiess, wie im Sandwich; der Satz steht auf dem Fähnchen
# Mannschaft: das Fähnchen steckt unten im Tresen, nie über den Köpfen
SP = [('dc_burger', '58%', '-6deg', '5%'), ('dc_drink', '62%', '5deg', '5%'), ('dc_team', '97%', '-3deg', '64%'), ('dc_plakat', '70%', '4deg', '5%'), ('dc_tisch', '56%', '-5deg', '5%')]
F.append(('Die Spiesse', 'In jedem Bild steckt ein Holzspiess mit Fähnchen, wie er im Sandwich steckt, und auf dem Fähnchen steht der Satz. Beim Ankommen werden die Spiesse von oben hineingesteckt.', sec(4, 'warm', '<div class="vi">%s<div class="zu4-reihe auf">%s</div></div>' % (
    kopf(),
    ''.join('<div class="zu4-f" style="--i:%d;--y:%s;--r:%s;--o:%s">%s<div class="zu4-spiess"><div class="zu4-fahne"><p>%s</p>%s</div><i></i></div></div>' % (
        i, y, r, o, foto(k, '', '(max-width:860px) 80vw, 19vw', auf=False, pos='50% 40%', extra='style="--weg:0px"'), q(s), datum(d)) for i, ((k, y, r, o), (s, _h, d, _k, _p)) in enumerate(zip(SP, Z)))))))

# 5 Die Sterne: die Sätze in den Zackensternen vom Pop-up-Plakat, in der Schrift des Plakats; in der Mitte das Plakat selbst
def stern(n=16, ri=.82):
    pkt = []
    for i in range(n * 2):
        r = 50 if i % 2 == 0 else 50 * ri
        a = math.pi * i / n - math.pi / 2
        pkt.append('%.2f,%.2f' % (50 + r * math.cos(a), 50 + r * math.sin(a)))
    return '<svg class="zu5-form" viewBox="0 0 100 100" aria-hidden="true" preserveAspectRatio="none"><polygon points="%s"/></svg>' % ' '.join(pkt)
STERNE = [(0, 'm', -8), (1, 'm', 6), (2, 'g', -4), (3, 'k', 10), (4, 'k', -12)]
def stern_html(j, i, gr, r):
    s, _h, d, _k, _p = Z[i]
    return '<div class="zu5-st %s" style="--i:%d;--r:%ddeg">%s<div class="zu5-t"><p>%s</p>%s</div></div>' % (gr, j, r, stern(), roh(s), datum(d))
F.append(('Die Sterne', 'Die Sätze stehen in den Zackensternen vom Pop-up-Plakat, in Versalien wie dort «POP» und «UP»; in der Mitte das Plakat selbst. Die Sterne drehen sich beim Ankommen in ihre Lage.', sec(5, 'dc', '<div class="vi">%s<div class="zu5-feld auf">%s<div class="zu5-plakat">%s</div>%s</div></div>' % (
    kopf(cls='mitte'), ''.join(stern_html(j, i, g, r) for j, (i, g, r) in enumerate(STERNE[:2])), foto('dc_plakat', '', '(max-width:860px) 70vw, 26vw', auf=False, extra='style="--weg:0px"'),
    ''.join(stern_html(j + 2, i, g, r) for j, (i, g, r) in enumerate(STERNE[2:]))))))

# 6 Die Tonspur: jeder Satz als Tonspur über die ganze Breite; beim Scrollen läuft der Abspielkopf und die Wörter darunter leuchten mit
def welle(seed, n=84):
    return ''.join('<i style="--h:%.2f"></i>' % (.18 + .82 * abs(math.sin(seed * 1.7 + k * .37) * math.cos(seed + k * .11 + math.sin(k * .9)))) for k in range(n))
def spur(i, s, d, k):
    woerter = roh(s).split(' ')
    return '''<div class="zu6-spur"><div class="zu6-kopf"><div class="zu6-bild">%s</div><b>dirtychicken.hannover</b>%s</div>
<div class="zu6-welle" aria-hidden="true">%s<span class="zu6-kopfl"></span></div><p class="zu6-text" aria-label="%s">%s</p></div>''' % (
        foto(k, '', '64px', auf=False, pos='50% 40%', extra='style="--weg:0px"'), datum(d), welle(i + 1), E(roh(s)), ' '.join('<span>%s</span>' % E(w) for w in woerter))
F.append(('Die Tonspur', 'Wie Dirty Chicken spricht, als Tonspur: Jeder Satz hat seine Welle über die ganze Breite. Beim Scrollen läuft der Abspielkopf durch, die Welle färbt sich und die Wörter darunter leuchten mit, wie beim Mitsingen.', sec(6, 'nacht', '<div class="vi">%s<div class="zu6-spuren">%s</div></div>' % (
    kopf(), ''.join(spur(i, s, d, k) for i, (s, _h, d, k, _p) in enumerate(Z))))))

# 7 Die Postkarten: vorne das Bild, hinten der Satz mit Briefmarke und Poststempel; beim Ankommen drehen sie sich um, antippen dreht zurück
def karte(i, s, d, k):
    tag = d.split('.')[0] + '.6.26'
    return '''<button type="button" class="zu7-k" style="--i:%d" aria-label="Postkarte umdrehen"><span class="zu7-innen"><span class="zu7-v">%s<em>Grüsse vom Pop-up</em></span>
<span class="zu7-r"><span class="zu7-text"><b>%s</b><span class="zu7-gruss">Euer Dirty Chicken</span></span><span class="zu7-rand"><span class="zu7-marke">%s</span><span class="zu7-stempel"><span>Hannover</span><b>%s</b></span><span class="zu7-linie"></span><span class="zu7-linie"></span><span class="zu7-linie"></span></span></span></span></button>''' % (
        i, foto(k, '', '(max-width:860px) 90vw, 30vw', auf=False, pos='50% 45%', extra='style="--weg:0px"'), q(s), d_zeichen('zu7-z'), tag)
F.append(('Die Postkarten', 'Fünf Postkarten vom Pop-up: vorne das Bild, hinten der Satz mit Briefmarke und Poststempel. Beim Ankommen drehen sie sich eine nach der anderen um, antippen dreht sie wieder auf das Bild.', sec(7, 'hell', '<div class="vi">%s<div class="zu7-tisch auf">%s</div></div>' % (
    kopf(kick='Post aus Hannover', titel=('Grüsse vom', 'Pop-up.'), text='Fünf Sätze, so wie sie im Juni 2026 auf Instagram standen. Antippen dreht die Karte.'),
    ''.join(karte(i, s, d, k) for i, (s, _h, d, k, _p) in enumerate(Z))))))

# 8 Ein Wort je Satz: aus jedem Satz das eine Wort riesig über die ganze Breite, darunter der ganze Satz klein, daneben das Bild
WORT = [('Ansage.', 'dc_burger'), ('Ding.', 'dc_drink'), ('Familie.', 'dc_team'), ('Sause.', 'dc_plakat'), ('Liebe.', 'dc_tisch')]
F.append(('Ein Wort je Satz', 'Aus jedem Satz das eine Wort, das ihn trägt, riesig über die ganze Breite: Ansage, Ding, Familie, Sause, Liebe. Darunter der ganze Satz, daneben das Bild, abwechselnd links und rechts.', sec(8, 'nacht', '<div class="vi">%s</div><div class="vi zu8-folge">%s</div>' % (
    kopf(text='Fünf Sätze, fünf Wörter. Mehr braucht Dirty Chicken nicht.'),
    ''.join('<div class="zu8-e %s"><h3 class="zu8-w zl auf" aria-label="%s"><span class="z"><span style="--i:0">%s</span></span></h3><div class="zu8-unten"><div class="zu8-bild auf">%s</div><div class="zu8-satz sw auf" style="--i:2"><p>%s</p>%s</div></div></div>' % (
        'r' if i % 2 else 'l', E(w), w, foto(k, '', '(max-width:860px) 60vw, 26vw', auf=False, pos='50% 40%'), q(s), datum(d)) for i, ((w, k), (s, _h, d, _k, _p)) in enumerate(zip(WORT, Z)))))))

# 9 Die Drucke: jeder Satz als Druck im Stil eines Clubs, wie auf dem Rücken eines Shirts: Bogen mit dem Namen, Zeichen, Satz, Ort und Jahr
TH = ['d-creme', 'd-lila', 'd-nacht', 'd-kerze', 'd-pflaume']
def druck(i, s, d):
    return '''<div class="zu9-d %s" style="--i:%d"><svg class="zu9-bogen" viewBox="0 0 300 92" aria-hidden="true"><defs><path id="zu9-b%d" d="M 30 88 A 124 124 0 0 1 270 88"/></defs><text><textPath href="#zu9-b%d" startOffset="50%%" text-anchor="middle">DIRTY CHICKEN</textPath></text></svg>
%s<p class="zu9-satz">%s</p><p class="zu9-fuss"><i></i>Hannover · %s<i></i></p></div>''' % (TH[i], i, i, i, d_zeichen('zu9-z'), roh(s), d.replace(' 2026', ' ’26'))
F.append(('Die Drucke', 'Jeder Satz als Druck im Stil eines Clubs, wie auf dem Rücken eines Shirts: oben im Bogen DIRTY CHICKEN, darunter das Zeichen, der Satz, Ort und Datum. Fünf Drucke in fünf Farben der Marke, sie werden nacheinander aufs Papier gepresst.', sec(9, 'warm', '<div class="vi">%s<div class="zu9-tisch auf">%s</div></div>' % (
    kopf(kick='Zum Mitnehmen', titel=('Gedruckt,', 'nicht gesagt.'), text='So würden die Sätze auf dem Shirt aussehen. Fünf Sätze, fünf Drucke.'),
    ''.join(druck(i, s, d) for i, (s, _h, d, _k, _p) in enumerate(Z))))))

# 10 Das Einschlagpapier: der Burger liegt eingeschlagen, beim Scrollen gehen die beiden Seiten des bedruckten Papiers auf; auf dem Papier die Sätze
def papier(saetze, seite):
    return '<div class="zu10-p %s"><div class="zu10-druck">%s<p class="zu10-zeile">Sandwiches &amp; More · Hannover</p>%s</div></div>' % (
        seite, d_zeichen('zu10-z'), ''.join('<div class="zu10-s"><p>%s</p>%s</div>' % (roh(s).upper(), datum(d)) for s, d in saetze))
F.append(('Das Einschlagpapier', 'Der Burger liegt eingeschlagen in bedrucktem Papier. Beim Scrollen gehen die beiden Seiten auf und geben ihn frei; auf dem Papier stehen die Sätze, so wie eine Marke ihr Papier bedruckt.', sec(10, 'nacht', '<div class="vi">%s</div><div class="vi zu10 auf"><div class="zu10-bild">%s</div>%s%s</div>' % (
    kopf(cls='mitte', text='Auspacken. Erst das Papier, dann die Ansage.'), foto('dn_burger', '', '(max-width:860px) 100vw, 34vw', auf=False, pos='50% 55%', extra='style="--weg:0px"'),
    papier([(Z[0][0], Z[0][2]), (Z[2][0], Z[2][2])], 'l'), papier([(Z[1][0], Z[1][2]), (Z[3][0], Z[3][2]), (Z[4][0], Z[4][2])], 'r')))))

# 11 Der Fotoautomat: je Satz ein Streifen aus dem Fotoautomaten mit zwei Bildern, der Satz unten im weissen Rand; die Streifen fahren aus dem Schlitz
STREIF = [['dc_burger', 'dn_sosse'], ['dc_drink', 'dn_glas'], ['dc_team', 'dc_team2'], ['dc_plakat', 'dn_bar'], ['dc_tisch', 'dn_salat']]
F.append(('Der Fotoautomat', 'Wie aus dem Fotoautomaten: je Satz ein Streifen mit zwei Bildern, der Satz steht unten im weissen Rand, darunter das Datum. Beim Ankommen fahren die Streifen nacheinander aus dem Schlitz.', sec(11, 'warm', '''<div class="vi">%s<div class="zu11-automat auf"><div class="zu11-schlitz"><span>Foto · Automat</span></div><div class="zu11-reihe">%s</div></div></div>''' % (
    kopf(),
    ''.join('<div class="zu11-st" style="--i:%d">%s<div class="zu11-rand"><p>%s</p>%s</div></div>' % (
        i, ''.join('<div class="zu11-b">%s</div>' % foto(k, '', '(max-width:860px) 40vw, 16vw', auf=False, pos='50% 45%', extra='style="--weg:0px"') for k in ks), q(s), datum(d))
        for i, (ks, (s, _h, d, _k, _p)) in enumerate(zip(STREIF, Z)))))))

# 12 Die Lautschrift: jedes Wort steht über seiner Aussprache, Wort für Wort, wie in einem Sprachführer für Berliner Schnauze
IPA = [
    [('Dit', 'dɪt'), ('is', 'ɪs'), ('keen', 'keːn'), ('Burger.', 'ˈbœːɐ̯ɡɐ'), ('Dit', 'dɪt'), ('Ding', 'dɪŋ'), ('is', 'ɪs'), ('’ne', 'nə'), ('Ansage.', 'ˈanzaːjə')],
    [('Dirty', 'ˈdœːɐ̯tiː'), ('Food', 'fuːt'), ('&amp;', 'ʊn'), ('Dirty', 'ˈdœːɐ̯tiː'), ('Drinks.', 'dʁɪŋks'), ('Jenau', 'jəˈnaʊ̯'), ('meen', 'meːn'), ('Ding', 'dɪŋ'), ('wa.', 'va')],
    [('Wenn', 'vɛn'), ('aus', 'aʊ̯s'), ('Freunden', 'ˈfʁɔɪ̯ndn̩'), ('und', 'ʊn'), ('Kollegen', 'kɔˈleːjn̩'), ('Familie', 'faˈmiːli̯ə'), ('wird.', 'vɪʁt'), ('Dann', 'dan'), ('haste', 'ˈhastə'), ('allet', 'ˈalət'), ('richtig', 'ˈʁɪçtɪç'), ('jemacht!', 'jəˈmaxt')],
    [('Opening', 'ˈoːpənɪŋ'), ('2026!', 'ˈtsvantsɪç ˈzɛksʊntˌtsvantsɪç'), ('Wat', 'vat'), ('ne', 'nə'), ('Sause.', 'ˈzaʊ̯zə')],
    [('Dit', 'dɪt'), ('ist', 'ɪst'), ('wahre', 'ˈvaːʁə'), ('Liebe!', 'ˈliːbə')],
]
def laut(i, paare, d, k):
    return '<div class="zu12-e"><div class="zu12-bild auf">%s</div><div class="zu12-zeile">%s</div>%s</div>' % (
        foto(k, '', '120px', auf=False, pos='50% 40%', extra='style="--weg:0px"'),
        ''.join('<span class="zu12-w"><b>%s</b><span class="zu12-ipa"><span class="zu12-in auf" style="--i:%d">[%s]</span></span></span>' % (w, j, a) for j, (w, a) in enumerate(paare)), datum(d))
F.append(('Die Lautschrift', 'Wie ein Sprachführer für Berliner Schnauze: Jedes Wort steht über seiner Aussprache, Wort für Wort. Man sieht, warum «Ansage» hier «Ansaje» heisst. Die Lautschrift fährt Wort für Wort unter die Wörter.', sec(12, 'hell', '<div class="vi">%s<div class="zu12-liste">%s</div><p class="zu12-notiz sw auf" style="--i:1">In Berlin wird das g zwischen zwei Vokalen zum j: Ansaje, Kolleejen, jemacht.</p></div>' % (
    kopf(kick='Sprachführer', titel=('So spricht', 'man dit aus.'), text='Fünf Sätze von Dirty Chicken, Wort für Wort mit Lautschrift. Für alle, die nicht aus Berlin sind.'),
    ''.join(laut(i, p, Z[i][2], Z[i][3]) for i, p in enumerate(IPA))))))

# 13 Der Abreisskalender: ein Block mit dem Juni 2026, jedes Blatt ein Tag mit seinem Satz; antippen reisst das Blatt ab, das Bild daneben wechselt
TAGE = {'3. Juni 2026': ('Mittwoch', '3'), '6. Juni 2026': ('Samstag', '6'), '13. Juni 2026': ('Samstag', '13')}
def blatt(i, s, d):
    wt, tag = TAGE[d]
    return '<div class="zu13-blatt" data-s="%d" style="--z:%d"><p class="zu13-wt mono">%s</p><p class="zu13-tag">%s</p><p class="zu13-satz">%s</p><p class="zu13-fuss mono">@dirtychicken.hannover</p></div>' % (i, 10 - i, wt, tag, q(s))
F.append(('Der Abreisskalender', 'Ein Abreisskalender für den Juni 2026: Jedes Blatt ist ein Tag mit dem Satz, den Dirty Chicken an diesem Tag geschrieben hat. Antippen reisst das Blatt ab, das Bild daneben wechselt mit.', sec(13, 'warm', '''<div class="vi zu13"><div class="zu13-links">%s<div class="zu13-block auf" data-akt="0" role="button" tabindex="0" aria-label="Blatt abreissen"><div class="zu13-kopf"><i></i><span>Juni 2026</span><i></i></div><div class="zu13-stapel">%s</div></div>
<p class="zu13-hinweis mono">Antippen reisst das Blatt ab</p></div><div class="zu13-bilder"><div class="zu13-box auf" data-wahl="0">%s</div></div></div>''' % (
    kopf(kick='Juni 2026', titel=('Ein Satz', 'am Tag.'), text=''), ''.join(blatt(i, s, d) for i, (s, _h, d, _k, _p) in enumerate(Z)),
    ''.join('<div class="zu13-b" data-s="%d">%s</div>' % (i, foto(k, '', '(max-width:860px) 100vw, 40vw', auf=False, pos='50% 40%', extra='style="--weg:0px"')) for i, (_s, _h, _d, k, _p) in enumerate(Z))))))

# 14 Die Spur: Hühnerfüsse laufen in einer Spur die Seite hinunter, von Satz zu Satz; an jedem Halt Bild und Satz, abwechselnd links und rechts
FUSS = '<svg class="zu14-fuss" viewBox="-3 -3 30 38" aria-hidden="true"><path d="M12 26V14M12 14L3 3M12 14V0M12 14L21 3M12 26l-4 6"/></svg>'
def tritte(n=7):
    return ''.join('<span class="zu14-t %s" style="--j:%d">%s</span>' % ('a' if k % 2 else 'b', k, FUSS) for k in range(n))
F.append(('Die Spur', 'Das Zeichen von Dirty Chicken ist ein Hühnerfuss, also läuft eine Spur aus Hühnerfüssen die Seite hinunter, von Satz zu Satz. An jedem Halt das Bild und der Satz, abwechselnd links und rechts; die Tritte setzen nacheinander auf.', sec(14, 'dc', '<div class="vi">%s</div><div class="vi zu14">%s</div>' % (
    kopf(cls='mitte', text='Immer der Spur nach. Fünf Sätze aus dem Juni 2026.'),
    ''.join('<div class="zu14-e %s"><div class="zu14-inhalt"><div class="zu14-bild auf">%s</div><div class="zu14-satz sw auf" style="--i:1"><p>%s</p>%s</div></div><div class="zu14-weg auf">%s</div></div>' % (
        'r' if i % 2 else 'l', foto(k, '', '(max-width:860px) 70vw, 28vw', auf=False, pos='50% 40%'), q(s), datum(d), tritte()) for i, (s, _h, d, k, _p) in enumerate(Z))))))

# 15 Das Herz: die fünf Sätze füllen als Text ein Herz, in der Mitte das Zeichen; «Dit ist wahre Liebe!» als Unterschrift
def herzform():
    # Herz aus vier Kurven (viewBox 0..100), daraus links und rechts die Aussenflächen für shape-outside
    kurven = [((50, 22), (50, 22), (41, 3), (24, 3)), ((24, 3), (8, 3), (0, 16), (0, 30)), ((0, 30), (0, 52), (28, 70), (50, 98))]
    def b(p, t):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
        u = 1 - t
        return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3, u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)
    pkt = []
    for k in kurven:
        pkt += [b(k, t / 12) for t in range(13)]
    # Kante von oben Mitte über den linken Bogen bis zur Spitze; rechts gespiegelt
    kante = pkt
    l = ['0% 0%', '100% 0%'] + ['%.1f%% %.1f%%' % (min(100, x * 2), y) for x, y in kante] + ['100% 100%', '0% 100%']
    r = ['100% 0%', '0% 0%'] + ['%.1f%% %.1f%%' % (max(0, (100 - x) * 2 - 100), y) for x, y in kante] + ['0% 100%', '100% 100%']
    pfad = 'M50,22 C50,22 41,3 24,3 C8,3 0,16 0,30 C0,52 28,70 50,98 C72,70 100,52 100,30 C100,16 92,3 76,3 C59,3 50,22 50,22 Z'
    return 'polygon(%s)' % ', '.join(l), 'polygon(%s)' % ', '.join(r), pfad
HL, HR, HP = herzform()
F.append(('Das Herz', 'Die fünf Sätze füllen als Text ein Herz, gesetzt in der Titelschrift; die Kontur des Herzens ist nur eine feine Linie. Darunter steht gross «Dit ist wahre Liebe!» als Unterschrift. Das Herz schlägt beim Ankommen einmal.', sec(15, 'nacht', '''<div class="vi zu15"><div class="zu15-links">%s</div>
<div class="zu15-herz auf"><svg class="zu15-linie" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="%s"/></svg>
<div class="zu15-text"><span class="zu15-fl" style="shape-outside:%s"></span><span class="zu15-fr" style="shape-outside:%s"></span><p>%s</p></div></div></div>''' % (
    kopf(text='Fünf Sätze aus dem Juni 2026, gesetzt in ein Herz. Der letzte sagt, worum es geht.'), HP, HL, HR,
    ' '.join('%s <span class="zu15-d">%s</span>' % (roh(s), d.replace(' 2026', '')) for s, _h, d, _k, _p in Z)))))


def main():
    # Rahmen ist die echte dirty-chicken.html im heutigen Stand (zitate_rahmen.py, Robert 28.10.2026: «die aktuellen Formate der Website»)
    import zitate_rahmen
    kb = zitate_rahmen.seite('dirty-chicken-zitate-wahl-2.html', 'zitate2', 'Zitate 2', F, 'dc-zitate-wahl-2.css', 'dc-zitate-wahl-2.js', 'Zitate wählen, Runde 2 · Dirty Chicken')
    json.dump([{'nr': i, 'name': n, 'satz': s_} for i, (n, s_, _h) in enumerate(F, 1)], open(os.path.join(HIER, '_sicherung', 'zitate2-fassungen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Seite dirty-chicken-zitate-wahl-2.html', kb, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
