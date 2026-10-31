#!/usr/bin/env python3
"""Dirty Chicken · Abschnitt «Das erste Pop-up» (Wann, Wo, Was, Gastschicht, Danach, Mit dabei) in 15 Fassungen zur Wahl (28.10.2026, 08:40).
Robert: «15 alternative Visualisierungsmöglichkeiten» zum heutigen Steckbrief (Zeichen links, Tabelle rechts).
Die Fakten bleiben wörtlich wie heute. Jede Fassung ein anderes Gerüst aus der Entwurfs-Maschine (Billett, Rechnung, Grosse Zahl, Plakatwand, Tafel, Weg,
Einladung, Ablauf, Drei Scheiben, Namen als Liste, Glaskarte, Kalender, Leiste zum Aufklappen, Zahlen als Wörter, Senkrecht), ein eigener bewegter Moment,
nur transform und opacity, Gesichter unberührt. Bilder: nur das Zeichen, dc_burger, dn_sosse und Standbilder aus dem Opening-Film (nicht die Bilder von Essen und Nacht).
Baut dirty-chicken-popup-wahl.html (Hero, Fenster, Essen, Nacht wie auf der echten Seite, dann der Teil umschaltbar; ?pop=Nummer, 0 = heute).
Aufruf: python3 website/dc_pop_wahl.py"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, foto, zl, sw
import varianten
import dc_essen
import dc_nacht

HIER = bau.HIER
KICK = 'Das erste Pop-up · 30. Mai 2026'
TEXT = 'Ein Nachmittag und Abend im Tiedthof, mit Gastschicht an der Bar und Musik.'
FAKTEN = [('Wann', '30. Mai 2026, 14 bis 22 Uhr'), ('Wo', 'AM:PM Café im Tiedthof, Goseriede 4'), ('Was', 'Dirty Food, Dirty Drinks &amp; Live Music'),
          ('Gastschicht', 'Martin Bauermann, Beluga Vodka Berlin'), ('Danach', 'Aftershow im NATE'), ('Mit dabei', 'AM:PM, Walk on the Wild Side, Beluga, NATE')]


def ek(text, i=0):
    return '<p class="ek sw auf" style="--i:%d"><span>%s</span></p>' % (i, text)


def et(zeilen, cls='', i0=0):
    return zl(zeilen, 'h2', ('et ' + cls).strip(), i0)


def ex(text, i=2, cls=''):
    return sw(text, 'p', ('ex ' + cls).strip(), i)


def still(t, cls='', pos='50% 50%'):
    return '<figure class="pp-still %s"><img src="assets/film/opening-still-%d.webp?v=%s" alt="Standbild aus dem Film vom Opening" loading="lazy" decoding="async" style="object-position:%s"></figure>' % (cls, t, VERSION, pos)


def d_zeichen(cls=''):
    return bau.zeichen_haus('dc', cls)


def kopf(kick=KICK, titel=('Das erste', 'Pop-up.'), text=TEXT, cls='', i0=0):
    return '<div class="vk pp-kopf %s">%s%s%s</div>' % (cls, ek(kick, i0), et(list(titel), '', i0), ex(text, i0 + 2) if text else '')


def vz(fakten=FAKTEN, cls='', i=3):
    return '<dl class="pp-vz sw auf %s" style="--i:%d">%s</dl>' % (cls, i, ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in fakten))


def sec(n, ton, inner, cls=''):
    return '<section class="vab dc-ab ess pps%02d %s" data-ton="%s">%s</section>' % (n, cls, ton, inner)


def stern(zacken=24, r1=50, r2=38):
    return ','.join('%.1f%% %.1f%%' % (50 + (r1 if i % 2 == 0 else r2) * math.cos(math.pi * i / zacken - math.pi / 2), 50 + (r1 if i % 2 == 0 else r2) * math.sin(math.pi * i / zacken - math.pi / 2)) for i in range(zacken * 2))


FUSS = '<svg class="pp-fuss" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 58V92M50 58 22 22M50 58 50 12M50 58 78 22" fill="none" stroke="currentColor" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'

F = []

# 1 Das Ticket: die Angaben als Eintrittskarte auf Creme, rechts der Abriss mit dem Datum; der Abriss knickt beim Ankommen leicht ab
F.append(('Das Ticket', 'Die Angaben als Eintrittskarte auf Creme, rechts der Abriss mit Datum und Uhrzeit an einer Perforation; beim Ankommen knickt der Abriss leicht ab.', sec(1, 'nacht', '''<div class="vi"><div class="pp1-ticket pp-hell auf">
<div class="pp1-haupt"><div class="pp1-kopf"><span class="mono">Dirty Chicken · Pop-up · No. 001</span>%s</div>%s%s%s</div>
<div class="pp1-abriss" aria-hidden="true"><span class="pp1-datum">30. Mai</span><span class="mono">14 bis 22 Uhr</span><span class="mono pp1-ort">AM:PM Café im Tiedthof</span></div>
</div></div>''' % (d_zeichen('pp1-z'), et(['Das erste', 'Pop-up.']), ex(TEXT, 1), vz(i=2)))))

# 2 Der Kassenbon: der Abend als Bon vom AM:PM, Zeile für Zeile in Schreibmaschinenschrift; der Bon rollt beim Ankommen aus dem Schlitz
BON = [('AM:PM CAFÉ · TIEDTHOF', ''), ('GOSERIEDE 4 · HANNOVER', ''), ('30.05.2026', '14:00–22:00'), ('—', ''),
       ('1  NACHMITTAG', 'AB 14:00'), ('1  ABEND', 'BIS 22:00'), ('   DIRTY FOOD', ''), ('   DIRTY DRINKS', ''), ('   LIVE MUSIC', ''),
       ('1  GASTSCHICHT', 'M. BAUERMANN'), ('   BELUGA VODKA BERLIN', ''), ('1  AFTERSHOW', 'NATE'), ('—', ''),
       ('SUMME', 'WAT NE SAUSE'), ('—', ''), ('MIT DABEI', ''), ('AM:PM · WALK ON THE WILD SIDE', ''), ('BELUGA · NATE', ''), ('DANKE. BIS ZUM NÄCHSTEN MAL.', '')]
F.append(('Der Kassenbon', 'Der Abend als Kassenbon vom AM:PM, Zeile für Zeile in Schreibmaschinenschrift bis zur Summe «Wat ne Sause»; der Bon rollt beim Ankommen aus dem Schlitz.', sec(2, 'warm', '''<div class="vi pp2"><div class="pp2-links">%s</div>
<div class="pp2-rechts auf"><div class="pp2-schlitz"></div><div class="pp2-bon pp-hell" aria-label="Der Abend als Kassenbon">%s</div></div></div>''' % (
    kopf(), ''.join('<p class="pp2-strich"></p>' if a == '—' else '<p><span>%s</span><span>%s</span></p>' % (a, b) for a, b in BON)))))

# 3 Das Datum: «30. Mai» riesig über die ganze Breite, darunter die Angaben in einer Reihe; das Datum driftet beim Scrollen leicht gegen die Seite
F.append(('Das Datum', 'Das Datum riesig über die ganze Breite auf Violett, darunter die Angaben in einer Reihe nebeneinander; beim Scrollen driftet das Datum leicht gegen die Seite.', sec(3, 'dc', '''<div class="vi">%s
<h2 class="pp3-datum zl auf" aria-label="30. Mai 2026"><span class="z"><span style="--i:0">30. Mai</span></span></h2>
<div class="pp3-reihe sw auf" style="--i:1">%s</div>%s</div>''' % (
    ek('Das erste Pop-up'),
    ''.join('<div><span class="mono">%s</span><b>%s</b></div>' % (k, v) for k, v in [('Wann', '14 bis 22 Uhr')] + FAKTEN[1:]),
    ex(TEXT, 2, 'pp3-text')))))

# 4 Das eigene Plakat: die Angaben als Plakat im Stil des echten (Violett, Creme, zwei Sterne «POP» «UP»), mit Klebeband an der Wand; hängt schief und richtet sich
F.append(('Das eigene Plakat', 'Die Angaben als Plakat im Stil des echten Dirty-Chicken-Plakats: Violett, Creme, zwei Sterne «POP» und «UP», mit Klebeband an die Wand geklebt; es hängt schief und richtet sich beim Ankommen.', sec(4, 'nacht', '''<div class="vi pp4"><div class="pp4-wand"><div class="pp4-plakat auf" style="--stern:polygon(%s)">
<i class="pp4-tape l"></i><i class="pp4-tape r"></i>
<p class="pp4-oben">AM:PM · Walk on the Wild Side · Beluga · NATE</p>
<p class="pp4-name">%s<span>Dirty Chicken</span></p>
<div class="pp4-sterne"><span class="pp4-stern">POP</span><span class="pp4-stern b">UP</span></div>
<p class="pp4-gross">Dirty Food<br>Dirty Drinks<br>&amp; Live Music</p>
<p class="pp4-gast">Martin Bauermann <small>Gastschicht · Beluga Vodka Berlin</small></p>
<p class="pp4-unten"><b>30. Mai</b><span>14 bis 22 Uhr · AM:PM Café im Tiedthof · Goseriede 4<br>Aftershow im NATE</span><b>AM:PM</b></p>
</div></div><div class="pp4-rechts">%s%s</div></div>''' % (stern(), d_zeichen('pp4-z'), kopf(), vz()))))

# 5 Die Anzeigetafel: die sechs Zeilen auf einer Fallblatt-Anzeige wie am Bahnhof, jeder Buchstabe ein Blatt; die Zeilen klappen beim Ankommen nacheinander um
def flaps(text):
    return ''.join('<i>%s</i>' % (E(ch) if ch != ' ' else '&nbsp;') for ch in text)
F.append(('Die Anzeigetafel', 'Die sechs Zeilen auf einer Fallblatt-Anzeige wie am Bahnhof, jeder Buchstabe ein eigenes Blatt in Versalien; beim Ankommen klappen die Zeilen nacheinander um.', sec(5, 'nacht', '''<div class="vi">%s
<div class="pp5-tafel auf">%s</div></div>''' % (
    kopf(text=TEXT), ''.join('<div class="pp5-z" style="--i:%d"><span class="mono">%s</span><span class="pp5-flaps">%s</span></div>' % (
        i, k, flaps(re.sub('&amp;', '&', v).upper())) for i, (k, v) in enumerate(FAKTEN))))))

# 6 Die Hühnerspur: sechs Fussabdrücke des Huhns laufen quer über die Fläche, an jedem steht eine Angabe; die Abdrücke stempeln sich nacheinander auf
SPUR = [(0, 0, -14), (17, 44, 12), (34, 2, -10), (51, 46, 14), (68, 4, -12), (85, 48, 10)]
F.append(('Die Hühnerspur', 'Sechs Fussabdrücke des Huhns aus dem Zeichen laufen im Zickzack quer über das Violett, an jedem Abdruck steht eine Angabe; die Abdrücke stempeln sich nacheinander auf.', sec(6, 'dc', '''<div class="vi">%s
<div class="pp6-weg auf">%s</div></div>''' % (
    kopf(cls='mitte'), ''.join('<div class="pp6-st" style="--x:%d%%;--y:%d%%;--w:%ddeg;--i:%d">%s<span class="mono">%s</span><b>%s</b></div>' % (
        x, y, w, i, FUSS, k, v) for i, ((x, y, w), (k, v)) in enumerate(zip(SPUR, FAKTEN)))))))

# 7 Die Einladung: eine gedruckte Einladungskarte auf Creme mit Doppelrahmen, alles mittig gesetzt; das Zeichen stempelt sich unten rechts auf
F.append(('Die Einladung', 'Eine gedruckte Einladungskarte auf Creme mit Doppelrahmen, alles mittig gesetzt wie auf einer Einladung; zum Schluss stempelt sich das Zeichen unten rechts auf die Karte.', sec(7, 'warm', '''<div class="vi"><div class="pp7-karte pp-hell auf">
<p class="mono pp7-lad sw auf" style="--i:0">Dirty Chicken lädt ein</p>%s%s
<div class="pp7-zeilen sw auf" style="--i:2">%s</div>
<p class="pp7-dabei sw auf" style="--i:3"><span class="mono">Mit dabei</span>AM:PM · Walk on the Wild Side · Beluga · NATE</p>
<div class="pp7-stempel" aria-hidden="true">%s</div>
</div></div>''' % (et(['Das erste', 'Pop-up.'], 'pp7-t'), ex(TEXT, 1, 'pp7-x'),
                   ''.join('<p><span class="mono">%s</span><b>%s</b></p>' % (k, v) for k, v in FAKTEN[:5]), d_zeichen('pp7-z')))))

# 8 Der Stundenplan: eine Zeitleiste von 14 bis 22 Uhr, darüber die drei Bänder Essen, Drinks, Musik, hinter 22 Uhr die Aftershow; eine Marke wandert mit dem Scrollen
BAENDER = [('Dirty Food', 'Fried Chicken, Sandwiches &amp; More'), ('Dirty Drinks', 'Gastschicht Martin Bauermann, Beluga Vodka Berlin'), ('Live Music', 'den ganzen Abend')]
F.append(('Der Stundenplan', 'Eine Zeitleiste von 14 bis 22 Uhr, darüber die Bänder Dirty Food, Dirty Drinks und Live Music, hinter 22 Uhr die Aftershow im NATE; eine violette Marke wandert mit dem Scrollen über die Stunden.', sec(8, 'nacht', '''<div class="vi">%s
<div class="pp8-plan auf">
<div class="pp8-baender">%s</div>
<div class="pp8-linie"><div class="pp8-stunden">%s</div><div class="pp8-danach"><span class="mono">Danach</span><b>Aftershow im NATE</b></div><i class="pp8-marke"></i></div>
</div>
<div class="pp8-unten sw auf" style="--i:2"><div><span class="mono">Wo</span><b>AM:PM Café im Tiedthof, Goseriede 4</b></div><div><span class="mono">Mit dabei</span><b>AM:PM, Walk on the Wild Side, Beluga, NATE</b></div></div></div>''' % (
    kopf(), ''.join('<div class="pp8-band" style="--i:%d"><b>%s</b><span>%s</span></div>' % (i, a, b) for i, (a, b) in enumerate(BAENDER)),
    ''.join('<span><i></i><em class="mono">%d</em></span>' % h for h in range(14, 23))))))

# 9 Drei Türen: Tiedthof, Bar, NATE als drei hohe Felder mit Standbild, Name und Angaben; die Felder werden nacheinander hell
TUEREN = [('Im Tiedthof', 13, '50% 30%', [('Wo', 'AM:PM Café, Goseriede 4'), ('Wann', '30. Mai 2026, 14 bis 22 Uhr'), ('Was', 'Dirty Food &amp; Live Music')]),
          ('An der Bar', 25, '50% 50%', [('Was', 'Dirty Drinks'), ('Gastschicht', 'Martin Bauermann'), ('Von', 'Beluga Vodka Berlin')]),
          ('Danach', 21, '50% 40%', [('Was', 'Aftershow'), ('Wo', 'im NATE'), ('Wann', 'nach 22 Uhr')])]
F.append(('Drei Türen', 'Der Abend in drei hohen Feldern nebeneinander: der Tiedthof, die Bar, das NATE, jedes mit Standbild aus dem Film, Name und Angaben; die Felder werden nacheinander hell.', sec(9, 'nacht', '''<div class="vi">%s
<div class="pp9-reihe auf">%s</div>
<p class="pp9-dabei sw auf" style="--i:4"><span class="mono">Mit dabei</span>AM:PM, Walk on the Wild Side, Beluga, NATE</p></div>''' % (
    kopf(), ''.join('<div class="pp9-t" style="--i:%d"><div class="pp9-bild">%s<i class="pp9-dunkel"></i></div><h3>%s</h3><dl class="pp-vz klein">%s</dl></div>' % (
        i, still(t, 'pp9-s', pos), n, ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in zz)) for i, (n, t, pos, zz) in enumerate(TUEREN))))))

# 10 Vier Namen: «Mit dabei» als grosse Liste (AM:PM, Walk on the Wild Side, Beluga, NATE) mit ihrer Rolle; Zeigen oder Tippen tauscht das Bild rechts
NAMEN = [('AM:PM', 'Café im Tiedthof, Goseriede 4 · der Ort', ('foto', 'dc_burger')), ('Walk on the Wild Side', 'die Bar in Linden · das Haus', ('foto', 'theke')),
         ('Beluga', 'Gastschicht Martin Bauermann · Vodka aus Berlin', ('still', 25)), ('NATE', 'die Aftershow · danach', ('still', 21))]
F.append(('Vier Namen', 'Oben in einer Zeile Datum, Uhrzeit und Was; darunter «Mit dabei» als grosse Liste der vier Namen mit ihrer Rolle; Zeigen oder Tippen auf einen Namen tauscht das Bild rechts an derselben Stelle.', sec(10, 'warm', '''<div class="vi pp10"><div class="pp10-links">%s
<p class="pp10-zeile sw auf" style="--i:1">30. Mai 2026, 14 bis 22 Uhr · Dirty Food, Dirty Drinks &amp; Live Music · danach Aftershow im NATE</p>
<p class="ek sw auf" style="--i:2"><span>Mit dabei</span></p>
<div class="pp10-liste sw auf" style="--i:3">%s</div></div>
<div class="pp10-wahl auf" data-wahl="0">%s</div></div>''' % (
    et(['Das erste', 'Pop-up.']),
    ''.join('<button type="button" class="pp10-n%s" data-s="%d"><b>%s</b><span>%s</span></button>' % (' an' if i == 0 else '', i, n, r) for i, (n, r, _b) in enumerate(NAMEN)),
    ''.join('<div class="pp10-b" data-s="%d">%s</div>' % (i, foto(b[1], '', '(max-width:860px) 100vw, 40vw', auf=False, pos='50% 40%') if b[0] == 'foto' else still(b[1], 'pp10-s'))
            for i, (_n, _r, b) in enumerate(NAMEN))))))

# 11 Der Tischaufsteller: ein grosses Tischfoto über die ganze Breite, darauf eine dunkle Karte mit den Angaben wie ein Aufsteller auf dem Tisch; das Foto fährt in den Rahmen, die Karte steigt
F.append(('Der Tischaufsteller', 'Das Tischfoto mit der Sauce läuft über die ganze Breite, darauf steht eine dunkle Karte mit den Angaben wie ein Aufsteller auf dem Tisch; das Foto fährt in den Rahmen, die Karte steigt leicht.', sec(11, 'nacht', '''<div class="pp11">%s<div class="pp11-hof"></div>
<div class="pp11-karte auf">%s%s</div></div>''' % (foto('dn_sosse', 'pp11-f', '100vw', auf=True, pos='50% 62%'), kopf(), vz()), 'pp11-ab')))

# 12 Das Kalenderblatt: ein Abreisskalender mit dem 30. riesig, Samstag und Uhrzeit, dahinter die abgerissenen Blätter; sie fächern beim Ankommen auf
F.append(('Das Kalenderblatt', 'Ein Abreisskalender auf Violett: das Blatt mit dem 30. riesig, Samstag, 14 bis 22 Uhr, dahinter zwei schon abgerissene Blätter; sie fächern beim Ankommen auf. Rechts die übrigen Angaben.', sec(12, 'dc', '''<div class="vi pp12"><div class="pp12-stapel auf">
<div class="pp12-blatt h2 pp-hell"></div><div class="pp12-blatt h1 pp-hell"></div>
<div class="pp12-blatt vorn pp-hell"><span class="pp12-monat">Mai 2026</span><b class="pp12-tag">30</b><span class="pp12-wtag">Samstag</span><span class="mono">14 bis 22 Uhr</span></div>
</div><div class="pp12-rechts">%s%s</div></div>''' % (kopf(), vz(FAKTEN[1:])))))

# 13 Die Leiste zum Aufklappen: Wann, Wo, Was, Gastschicht, Danach, Mit dabei als Leiste aus grossen Wörtern; Antippen holt die Antwort riesig auf die Bühne darunter
F.append(('Die Leiste', 'Wann, Wo, Was, Gastschicht, Danach und Mit dabei als Leiste aus grossen Wörtern; Antippen holt die Antwort riesig auf die Bühne darunter, die vorige schiebt sich weg, nichts springt.', sec(13, 'nacht', '''<div class="vi">%s
<div class="pp13-leiste sw auf" style="--i:1" role="tablist">%s</div>
<div class="pp13-buehne auf" data-wahl="0">%s</div></div>''' % (
    kopf(), ''.join('<button type="button" class="pp13-k%s" data-s="%d" role="tab" aria-selected="%s">%s</button>' % (' an' if i == 0 else '', i, 'true' if i == 0 else 'false', k) for i, (k, _v) in enumerate(FAKTEN)),
    ''.join('<div class="pp13-a" data-s="%d"><p>%s</p></div>' % (i, v) for i, (_k, v) in enumerate(FAKTEN))))))

# 14 Zahlen als Wörter: Ein Nachmittag, Ein Abend, Eine Gastschicht, Eine Aftershow als grosse Zeilen, rechts jeweils die Angabe dazu; die Zeilen kommen nacheinander aus dem Schlitz
WOERTER = [('Ein Nachmittag.', 'Ab 14 Uhr im AM:PM Café im Tiedthof, Goseriede 4.'), ('Ein Abend.', 'Bis 22 Uhr: Dirty Food, Dirty Drinks &amp; Live Music.'),
           ('Eine Gastschicht.', 'Martin Bauermann, Beluga Vodka Berlin, an der Bar.'), ('Eine Aftershow.', 'Danach im NATE.')]
F.append(('Zahlen als Wörter', 'Ein Nachmittag, ein Abend, eine Gastschicht, eine Aftershow: vier grosse Zeilen untereinander, rechts jeweils die Angabe dazu; die Zeilen kommen nacheinander aus dem Schlitz.', sec(14, 'warm', '''<div class="vi">%s
<div class="pp14-zeilen">%s</div>
<p class="pp14-dabei sw auf" style="--i:5"><span class="mono">Mit dabei</span>AM:PM, Walk on the Wild Side, Beluga, NATE</p></div>''' % (
    ek(KICK), ''.join('<div class="pp14-z">%s%s</div>' % (zl([w], 'h3', 'pp14-w', i), sw(s, 'p', 'pp14-s', i + 1)) for i, (w, s) in enumerate(WOERTER))))))

# 15 Senkrecht: der Titel läuft senkrecht am linken Rand, in der Mitte ein hohes Standbild, rechts die Angaben rechtsbündig
F.append(('Senkrecht', 'Der Titel läuft senkrecht am linken Rand von unten nach oben, in der Mitte ein hohes Standbild aus dem Film, rechts die Angaben rechtsbündig untereinander.', sec(15, 'nacht', '''<div class="vi pp15">
<h2 class="pp15-senk zl auf" aria-label="Das erste Pop-up."><span class="z"><span style="--i:0">Das erste Pop-up.</span></span></h2>
<div class="pp15-bild auf">%s</div>
<div class="pp15-rechts">%s%s%s</div></div>''' % (still(5, 'pp15-s'), ek(KICK), ex(TEXT, 1), vz(cls='rechts')))))


def main():
    s = [bau.kopf('Pop-up wählen · Dirty Chicken', 'Dirty Chicken: der Abschnitt «Das erste Pop-up» in 15 Fassungen zur Wahl.', 'dirty-chicken.html', 'dc')]
    k, n, c = varianten.DCSEITE[0]
    s.append(varianten.abschnitt(k, n, c, idn=False).replace('class="vab ', 'class="vab dc-ab bar-ab ', 1))
    s.append('''<section class="fenster" id="fenster-dc" aria-label="Die Ansage">
  <div class="fenster-schicht">%s<div class="fenster-hof"></div><p class="fenster-satz zl"><span class="z"><span style="--i:0">Dit is keen Burger.</span></span><span class="z"><span style="--i:1">Dit Ding is ’ne Ansage.</span></span></p></div>
</section>''' % foto('dn_burger', '', '100vw', auf=False, pos='50% 55%'))
    s.append(dc_essen.essen())
    s.append(dc_nacht.nacht())
    k, n, c = [x for x in varianten.DCSEITE if x[0] == 'dc-pop'][0]
    heute = varianten.abschnitt(k, n, c, idn=False).replace('class="vab ', 'class="vab dc-ab bar-ab ', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % heute]
    teile += ['<div class="wv" data-n="%d" hidden>%s</div>' % (i, h) for i, (_n, _s, h) in enumerate(F, 1)]
    s.append('<section class="dw wahl" data-ton="nacht" id="pop" data-name="Pop-up"><div class="wahl-marke"><b>Pop-up</b><span data-nr></span></div>%s</section>' % ''.join(teile))
    s.append(bau.fuss())
    h = ''.join(s)
    namen = ['Heute: Zeichen und Tabelle'] + [re.sub('&amp;', '&', n) for n, _s, _h in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('dc-pop-wahl.css', 'dc-pop-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["pop"],daumen:%s};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/dc-pop-wahl.js?v=%s" defer></script>''' % (
        json.dumps(namen, ensure_ascii=False), 'true' if os.path.exists(os.path.join(HIER, 'assets/daumen/pop-1.jpg')) else 'false', VERSION, v)
    h = h.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/dc-pop-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    h = h.replace('</body>', leiste + '\n</body>', 1)
    for fk in varianten.FILMLQ:
        h = h.replace('--lq:url(assets/film/%s.webp)' % fk, '--lq:url(%s)' % varianten.FILMLQ[fk])
    open(os.path.join(HIER, 'dirty-chicken-popup-wahl.html'), 'w', encoding='utf-8').write(h)
    json.dump([{'nr': i, 'name': n, 'satz': s_} for i, (n, s_, _h) in enumerate(F, 1)], open(os.path.join(HIER, '_sicherung', 'pop-fassungen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Seite dirty-chicken-popup-wahl.html', len(h) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
