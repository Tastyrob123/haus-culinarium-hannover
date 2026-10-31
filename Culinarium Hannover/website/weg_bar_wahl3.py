#!/usr/bin/env python3
"""Culinarium Hannover · Der Weg, «Die Bar» mit den Öffnungszeiten in 15 weiteren Fassungen, direkt in der echten Weg-Seite, 28.10.2026.
Robert: «15 alternative visualisierungsmögligkeiten» (Bildschirmfoto: vier Bilder um die cremefarbene Karte, 08:37). Runde 1 (weg-bar-wahl.html, Anordnungen)
hatte er abgelehnt; aus Runde 2 (weg-bar-wahl-2.html, Gegenstände) kam um 08:50 in einem anderen Chat «6» (Die Aufkleber) in die Seite, das ist hier Fassung 0. Hier gibt es keine Karte mehr: Die Zeiten selbst werden zur Form (die Woche,
der Zeitstrahl von 19 bis 2, jede Stunde ein Bild, die Bühne, die Wand, die auseinandergeht …), jede Fassung dicht mit sechs bis zwanzig Fotos,
im Vokabular des Hauses (Bildwand mit Fuge, Fraunces, Kerze), ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll.
Fotos aus Hero (schildnacht) und Schluss (barlicht) der Weg-Seite und aus dem Fuss (theke, tafelleer) kommen nicht vor (je Seite jedes Foto nur einmal).
Titel «So findest du hin.», Satz und Angaben darüber bleiben Pixel für Pixel; getauscht wird nur die Wand darunter.
Baut weg-bar-wahl-3.html (Leiste unten, Pfeiltasten, ?weg=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/weg_bar_wahl3.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION
from weg_wahl import bild, BAR, TEL, META
from weg_bar_wahl import fo, tel, lauf

HIER = bau.HIER
F = []
TAGE = [('Donnerstag', '19 bis 1 Uhr'), ('Freitag', '19 bis 2 Uhr'), ('Samstag', '19 bis 2 Uhr')]


def src(k, w=1000):
    st = META[k]['stufen']
    w = max(x for x in st if x <= w) if any(x <= w for x in st) else st[0]
    return 'assets/bild/%s-%d.webp?v=%s' % (k, w, VERSION)


def name(cls='', zeile=False):
    """Die Bar · Walk on the Wild Side · Telefon, als Block oder als eine Zeile."""
    return ('<div class="zd-name %s%s"><p class="zd-gross">Die Bar</p><p class="zd-wer">Walk on the Wild Side</p><p class="zd-tel">%s</p></div>'
            % ('zeile ' if zeile else '', cls, tel()))


def tage(cls=''):
    """Die drei Abende als Zeilen: Tag gross, Uhrzeit darunter."""
    return '<div class="zd-tage %s">%s</div>' % (cls, ''.join('<div class="zd-tag"><p class="zd-t">%s</p><p class="zd-z">%s</p></div>' % tz for tz in TAGE))


def fw(ks, cls='', sizes='(max-width:860px) 50vw, 30vw', pos=None, extra=None):
    """Bildwand mit Fuge wie auf der Seite; extra = Liste zusätzlicher Felder (html) am Ende."""
    inner = ''.join('<div class="fw-f" style="--i:%d">%s</div>' % (i, fo(k, '', sizes, pos)) for i, k in enumerate(ks))
    return '<div class="fw zd-fw %s">%s%s</div>' % (cls, inner, ''.join(extra or []))


# 1 Die Woche: sieben Tage nebeneinander, Montag bis Mittwoch und Sonntag dunkel, Donnerstag bis Samstag voller Bilder; heute ist markiert
WOCHE = [('Mo', 'Montag'), ('Di', 'Dienstag'), ('Mi', 'Mittwoch'), ('Do', 'Donnerstag'), ('Fr', 'Freitag'), ('Sa', 'Samstag'), ('So', 'Sonntag')]
WOCHE_BILDER = {'Do': ('ecke', 'flur'), 'Fr': ('fensterdraussen', 'bar'), 'Sa': ('barnacht', 'ws28')}
def wochentag(i, kurz, lang):
    if kurz in WOCHE_BILDER:
        a, b = WOCHE_BILDER[kurz]
        zeit = dict(TAGE)[lang]
        return ('<div class="zd01-t offen" data-tag="%d" style="--i:%d"><div class="zd01-b">%s<i class="zd01-v"></i></div><div class="zd01-b">%s<i class="zd01-v"></i></div>'
                '<div class="zd01-text"><p class="zd01-lang">%s</p><p class="zd01-zeit">%s</p></div><p class="zd01-heute">Heute</p></div>') % (
            i + 1, i, fo(a, '', '(max-width:860px) 50vw, 18vw', '50% 40%'), fo(b, '', '(max-width:860px) 50vw, 18vw', '50% 45%'), lang, zeit)
    return '<div class="zd01-t zu" data-tag="%d"><p class="zd01-kurz">%s</p><p class="zd01-lang">%s</p><p class="zd01-zu">geschlossen</p><p class="zd01-heute">Heute</p></div>' % (i + 1, kurz, lang)
F.append(('Die Woche', '<div class="zb zd01 auf" data-zd-woche>%s<div class="zd01-tage">%s</div></div>' % (
    name('zd01-kopf', True), ''.join(wochentag(i, k, l) for i, (k, l) in enumerate(WOCHE)))))

# 2 Von 19 bis 2: der Abend als Linie, Stunde für Stunde ein Bild über oder unter der Linie; die Linie füllt sich beim Scrollen
STUNDEN = [('19', 'flur', 'Die Tür geht auf'), ('20', 'ws00', ''), ('21', 'bar', ''), ('22', 'ws12', ''), ('23', 'ws28', ''), ('0', 'ws09', ''), ('1', 'ws14', 'Donnerstag Schluss'), ('2', 'barnacht', 'Freitag und Samstag Schluss')]
F.append(('Von 19 bis 2', '<div class="zb zd02 auf">%s<div class="zd02-strahl"><div class="zd02-linie"><i class="zd02-fuell" data-zd="fuell"></i></div>%s</div></div>' % (
    name('zd02-kopf', True), ''.join(
        '<div class="zd02-st %s" style="--i:%d"><div class="zd02-b">%s</div><p class="zd02-uhr"><b>%s Uhr</b>%s</p></div>' % (
            'o' if i % 2 == 0 else 'u', i, fo(k, '', '(max-width:860px) 25vw, 12vw', '50% 40%'), u, ('<span>%s</span>' % t) if t else '')
        for i, (u, k, t) in enumerate(STUNDEN)))))

# 3 Drei Abende: links die drei Abende als Knöpfe, rechts eine Wand aus drei Bildern, die beim Antippen an derselben Stelle tauscht
ABENDE = [('ecke', 'flur', 'ws00'), ('fensterdraussen', 'bar', 'ws12'), ('barnacht', 'ws28', 'ws09')]
F.append(('Drei Abende', '<div class="zb zd03 auf" data-zd-tap><div class="zd03-l">%s<div class="zd03-knoepfe">%s</div></div><div class="zd03-r">%s</div></div>' % (
    name(), ''.join('<button type="button" class="zd03-k%s" data-i="%d" aria-pressed="%s"><b>%s</b><span>%s</span></button>' % (' an' if i == 0 else '', i, 'true' if i == 0 else 'false', t, z) for i, (t, z) in enumerate(TAGE)),
    ''.join('<div class="zd03-wand%s" data-i="%d"%s>%s</div>' % (' an' if i == 0 else '', i, '' if i == 0 else ' aria-hidden="true"', fw(ks, 'zd03-fw', '(max-width:860px) 100vw, 40vw')) for i, ks in enumerate(ABENDE)))))

# 4 Die Wand geht auf: neun Bilder als Wand; beim Scrollen rücken die obere und die untere Reihe auseinander, in den Spalten stehen Name und Zeiten
WAND = [['ecke', 'schildtag', 'fensterdraussen'], ['flur', 'barneg', 'bar'], ['ws00', 'ws28', 'barnacht']]
F.append(('Die Wand geht auf', '<div class="zb zd04 auf" data-zd="wand"><p class="zd04-z o"><span class="zd-gross">Die Bar</span><span class="zd-wer">Walk on the Wild Side</span><span class="zd-tel">%s</span></p>'
          '<p class="zd04-z u">%s</p><div class="zd04-wand">%s</div></div>' % (
              tel(), ''.join('<span><b>%s</b> %s</span>' % tz for tz in TAGE),
              ''.join('<div class="zd04-reihe r%d">%s</div>' % (r, ''.join(fo(k, '', '(max-width:860px) 33vw, 30vw', '50% 40%') for k in ks)) for r, ks in enumerate(WAND)))))

# 5 Ab 19 Uhr: die Ansage riesig, die Wand aus acht Bildern beginnt schon unter dem Satz, darunter die drei Abende in einer Zeile
F.append(('Ab 19 Uhr', '<div class="zb zd05 auf"><p class="zd-wer zd05-wer">Die Bar · Walk on the Wild Side</p>%s%s<div class="zd05-fuss">%s<p class="zd-tel">%s</p></div></div>' % (
    bau.zl(['Ab 19 Uhr.'], 'h3', 'zd05-gross'),
    fw(['schildtag', 'fensterdraussen', 'flur', 'bar', 'ws00', 'ws12', 'ws28', 'barnacht'], 'zd05-wand', '(max-width:860px) 50vw, 24vw', '50% 40%'),
    tage('reihe'), tel())))

# 6 Blatt für Blatt: der Weg in vier Blättern, jedes eine Wand aus drei Bildern mit Zeile; beim Scrollen legt sich Blatt über Blatt, das letzte trägt die Zeiten
BLAETTER = [('Ecke Rampenstraße', ['ecke', 'schildtag', 'fensterdraussen']), ('Die Tür', ['flur', 'loch', 'kerze3']), ('An der Theke', ['bar', 'ws12', 'barneg']), ('Bis in die Nacht', ['ws28', 'ws09', 'barnacht'])]
F.append(('Blatt für Blatt', '<div class="zb zd06">%s<div class="zd06-blatt zd06-ende auf" style="--n:4"><div class="zd06-platte">%s%s</div></div></div>' % (
    ''.join('<div class="zd06-blatt auf" style="--n:%d"><p class="zd06-zeile"><span class="mono">%d / 4</span>%s</p>%s</div>' % (
        i, i + 1, t, fw(ks, 'zd06-fw', '(max-width:860px) 100vw, 44vw', '50% 40%')) for i, (t, ks) in enumerate(BLAETTER)),
    name('mitte'), tage('reihe'))))

# 7 Drei Streifen: je Abend ein Streifen über die ganze Breite, links die Zeiten auf dunkler Tafel, rechts drei Bilder; die Streifen gleiten gegenläufig
F.append(('Drei Streifen', '<div class="zb zd07 auf zb-voll">%s</div>' % ''.join(
    '<div class="zd07-reihe"><div class="zd07-tafel"><p class="zd-wer">%s</p><p class="zd07-tag">%s</p><p class="zd07-zeit">%s</p></div>%s</div>' % (
        'Die Bar' if i == 0 else ('Walk on the Wild Side' if i == 1 else 'Haasemannstraße 13'), t, z,
        lauf('quer', (-60, 60, -60)[i], ''.join(fo(k, '', '(max-width:860px) 40vw, 26vw', '50% 40%') for k in ks), 'zd07-bilder'))
    for i, ((t, z), ks) in enumerate(zip(TAGE, ABENDE)))))

# 8 Verstreut: Name und Zeiten in der Mitte, acht Bilder frei darum verteilt, verschieden gross, jedes wandert in eigenem Tempo
STREU = [('ecke', 0, 2, 24, -70), ('schildtag', 25, 0, 18, 40), ('fensterdraussen', 58, 0, 19, -50), ('barnacht', 78, 4, 22, 60),
         ('flur', 2, 54, 18, 50), ('bar', 21, 58, 22, -40), ('ws00', 60, 52, 17, 70), ('ws28', 78, 50, 22, -60)]
F.append(('Verstreut', '<div class="zb zd08 auf"><div class="zd08-mitte">%s%s</div>%s</div>' % (
    name('mitte'), tage('mitte'),
    ''.join('<div class="zd08-b" style="left:%d%%;top:%d%%;width:%d%%">%s</div>' % (x, y, w, lauf('drift', f, fo(k, '', '(max-width:860px) 50vw, 20vw', '50% 40%'), 'zd08-lauf')) for k, x, y, w, f in STREU))))

# 9 Jede Stunde ein Bild: je Abend eine Reihe, je Stunde ein Feld mit Bild; Donnerstag endet um 1, Freitag und Samstag um 2
STUNDEN_BILDER = [['ecke', 'schildtag', 'fensterdraussen', 'flur', 'ws00', 'bar'], ['schildnah', 'fassade', 'barneg', 'ws12', 'ws28', 'ws05', 'ws10'], ['barnacht', 'kerze3', 'flaschen', 'ws33', 'ws09', 'ws14', 'ws20']]
UHREN = ['19', '20', '21', '22', '23', '0', '1', '2']
F.append(('Jede Stunde ein Bild', '<div class="zb zd09 auf">%s<div class="zd09-skala"><span></span>%s</div>%s</div>' % (
    name('zd09-kopf', True), ''.join('<b>%s</b>' % u for u in UHREN),
    ''.join('<div class="zd09-reihe"><p class="zd09-tag">%s</p><div class="zd09-felder">%s%s</div><p class="zd09-ende">bis %s</p></div>' % (
        t, ''.join('<div class="zd09-f" style="--i:%d">%s</div>' % (j, fo(k, '', '(max-width:860px) 12vw, 9vw', '50% 40%')) for j, k in enumerate(ks)),
        '<div class="zd09-f leer"></div>' if len(ks) < 7 else '', z.split(' bis ')[1]) for (t, z), ks in zip(TAGE, STUNDEN_BILDER)))))

# 10 Das Band zum Blättern: die Zeiten als erstes Feld, dann acht Bilder in einer Reihe, die man seitwärts zieht; Pfeile blättern
BAND = ['ecke', 'schildtag', 'fensterdraussen', 'flur', 'bar', 'ws00', 'ws28', 'barnacht']
F.append(('Das Band zum Blättern', '<div class="zb zd10 auf"><div class="zd10-kopf">%s<div class="zd10-pfeile"><button type="button" data-band="-1" aria-label="Zurück">‹</button><button type="button" data-band="1" aria-label="Weiter">›</button></div></div>'
          '<div class="vband zd10-band"><div class="zd10-erst">%s</div>%s</div></div>' % (
              name('', True), tage(), ''.join('<div class="zd10-b" style="--i:%d">%s</div>' % (i, fo(k, '', '(max-width:860px) 70vw, 28vw', '50% 40%')) for i, k in enumerate(BAND)))))

# 11 Die Lichter gehen an: eine dichte Wand aus zehn Nachtbildern, die nacheinander hell werden; in der Mitte die Zeiten auf dunklem Glas
LICHTER = ['ecke', 'schildtag', 'fensterdraussen', 'barnacht', 'flur', 'bar', 'ws00', 'ws12', 'ws28', 'barneg']
LICHT_FOLGE = [3, 7, 1, 9, 0, 5, 8, 2, 6, 4]
def licht(i, k):
    return '<div class="fw-f zd11-f" style="--i:%d">%s<i class="zd11-v"></i></div>' % (LICHT_FOLGE[i], fo(k, '', '(max-width:860px) 50vw, 24vw', '50% 40%'))
F.append(('Die Lichter gehen an', '<div class="zb zd11 auf"><div class="fw zd-fw zd11-wand">%s<div class="zd11-mitte">%s%s</div>%s</div></div>' % (
    ''.join(licht(i, k) for i, k in enumerate(LICHTER[:5])), name('mitte'), tage('reihe'), ''.join(licht(i + 5, k) for i, k in enumerate(LICHTER[5:])))))

# 12 Draussen, drinnen: links vier Bilder von der Strasse, rechts vier aus der Bar, dazwischen die Naht mit den Zeiten senkrecht; die Hälften gleiten gegeneinander
F.append(('Draussen, drinnen', '<div class="zb zd12 auf"><div class="zd12-h l">%s<span class="fl-etikett">Draussen</span></div><div class="zd12-naht">%s<p class="zd12-senk">%s</p><p class="zd-tel">%s</p></div><div class="zd12-h r">%s<span class="fl-etikett">Drinnen</span></div></div>' % (
    lauf('drift', 50, fw(['ecke', 'schildtag', 'fensterdraussen', 'barnacht'], 'zd12-fw', '(max-width:860px) 50vw, 22vw', '50% 40%'), 'zd12-lauf'),
    '<p class="zd-gross">Die Bar</p><p class="zd-wer">Walk on the Wild Side</p>', ' · '.join('%s %s' % tz for tz in TAGE), tel(),
    lauf('drift', -50, fw(['flur', 'bar', 'ws00', 'barneg'], 'zd12-fw', '(max-width:860px) 50vw, 22vw', '50% 40%'), 'zd12-lauf'))))

# 13 Das Fenster: die Fenster der Bar am Abend stehen, die Seite zieht darüber; auf dem Bild die Ansage gross, darunter die Zeiten in einer Zeile
F.append(('Das Fenster', '''<section class="fenster zd13" aria-label="Die Bar am Abend">
  <div class="fenster-schicht">%s<div class="fenster-hof"></div><p class="fenster-satz zl"><span class="z"><span style="--i:0">Donnerstag bis Samstag,</span></span><span class="z"><span style="--i:1">ab 19 Uhr.</span></span></p>
  <p class="zd13-zeile">Die Bar · Walk on the Wild Side · Donnerstag bis 1 Uhr · Freitag und Samstag bis 2 Uhr · %s</p></div>
</section>''' % (fo('fassade', '', '100vw', '50% 50%'), tel())))

# 14 Die Zeilen: die drei Abende als grosse Zeilen; wo die Maus über eine Zeile fährt, folgt ihr ein Bild (eigener Baustein aus dem Fundus); darunter fünf Bilder
ZEILEN = [('Donnerstag', '19 bis 1 Uhr', 'ecke'), ('Freitag', '19 bis 2 Uhr', 'fensterdraussen'), ('Samstag', '19 bis 2 Uhr', 'barnacht'), ('Haasemannstraße 13', TEL[1], 'flur')]
F.append(('Die Zeilen', '<div class="zb zd14 auf"><div class="zd14-kopf"><p class="zd-gross">Die Bar</p><p class="zd-wer">Walk on the Wild Side</p></div><ul class="hr-list zd14-liste" data-hover-reveal>%s</ul>%s</div>' % (
    ''.join('<li class="hr-item zd14-z" data-hr-src="%s"><a href="%s"><b>%s</b><span>%s</span></a></li>' % (src(k), TEL[0] if t.startswith('Haase') else '#weg', t, z) for t, z, k in ZEILEN),
    fw(['bar', 'ws00', 'ws12', 'ws28', 'ws09'], 'zd14-wand', '(max-width:860px) 50vw, 20vw', '50% 40%'))))

# 15 Die Bühne: die Wand bleibt stehen, beim Scrollen hat erst der Donnerstag, dann der Freitag, dann der Samstag die Bühne, je vier Bilder
BUEHNE = [['ecke', 'flur', 'ws00', 'kerze3'], ['fensterdraussen', 'bar', 'ws12', 'barneg'], ['barnacht', 'ws28', 'ws09', 'flaschen']]
F.append(('Die Bühne', '<div class="zb zd15" data-zd="buehne"><div class="zd15-fest"><div class="zd15-l"><p class="zd-wer">Die Bar · Walk on the Wild Side</p>%s<p class="zd-tel">%s</p></div><div class="zd15-r auf">%s</div></div></div>' % (
    ''.join('<div class="zd15-tag%s" data-i="%d"><p class="zd15-t">%s</p><p class="zd15-z">%s</p></div>' % (' an' if i == 0 else '', i, t, z) for i, (t, z) in enumerate(TAGE)), tel(),
    ''.join('<div class="zd15-wand%s" data-i="%d">%s</div>' % (' an' if i == 0 else '', i, fw(ks, 'zd15-fw', '(max-width:860px) 50vw, 26vw', '50% 40%')) for i, ks in enumerate(BUEHNE)))))


def main():
    seite = open(os.path.join(HIER, 'weg.html'), encoding='utf-8').read()
    m = re.search(r'(<section class="vab bar-ab v-weg-abends[^"]*"[^>]*>)(.*?)(</section>)', seite, re.S)
    assert m, '«So findest du hin» in weg.html nicht gefunden'
    innen = m.group(2)
    # die Wand beginnt nach den Angaben: heute «Die Aufkleber» (akl, Robert «6» am 28.10.2026), davor die Bildwand mit Karte (fw flaeche)
    w = innen.find('<div class="akl')
    if w < 0:
        w = innen.find('<div class="fw flaeche')
    assert w > 0, 'Wand in «So findest du hin» nicht gefunden'
    vorn = innen[:w]
    kopf_tag = m.group(1).replace('class="vab ', 'id="weg" data-name="Die Bar" class="wahl vab ', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % innen]
    teile += ['<div class="wv" data-n="%d" hidden>%s%s</div></div>' % (i, vorn, wand) for i, (_n, wand) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Die Bar</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: die Aufkleber'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('weg-bar-wahl.css', 'weg-bar-wahl-3.css', 'weg-bar-wahl.js', 'weg-bar-wahl-3.js'))
    daumen = os.path.exists(os.path.join(HIER, 'assets/daumen/weg-1.jpg'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["weg"],daumen:%s};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/weg-bar-wahl.js?v=%s" defer></script>
<script src="assets/weg-bar-wahl-3.js?v=%s" defer></script>
<script type="module">import { initHoverReveal } from './assets/hr.js?v=%s'; if (matchMedia('(hover:hover)').matches) initHoverReveal(null, { width: 360, ratio: 1.3, ease: .16, tilt: 8 });</script>''' % (
        json.dumps(namen, ensure_ascii=False), 'true' if daumen else 'false', VERSION, v, v, VERSION)
    seite = seite.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
    seite = seite.replace('<title>', '<title>Bar-Zeiten wählen 3 · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/hr.css?v=%s">\n<link rel="stylesheet" href="assets/weg-bar-wahl.css?v=%s">\n'
                          '<link rel="stylesheet" href="assets/weg-bar-wahl-3.css?v=%s">\n</head>' % (VERSION, VERSION, v, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'weg-bar-wahl-3.html'), 'w', encoding='utf-8').write(seite)
    json.dump([{'nr': i, 'name': n} for i, (n, _h) in enumerate(F, 1)], open(os.path.join(HIER, '_sicherung', 'weg-bar-3-fassungen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Seite weg-bar-wahl-3.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
