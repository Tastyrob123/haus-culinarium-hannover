#!/usr/bin/env python3
"""Culinarium Hannover · Der Weg, die Wand mit der Karte «Die Bar» in 20 weiteren Fassungen, direkt in der echten Weg-Seite, 27.10.2026.
Robert: «Keiner davon gefällt mir. Kannst du bitte alle nochmal neu machen?» Die 20 aus weg-bar-wahl.html (Band, Naht, Dreiklang, Torbögen,
Mauerwerk, Flur, Aushang …) waren reine Anordnungen von Bild und Karte; hier steht jede Fassung als Gegenstand mit Tiefe und Material aus der Bar
(Regal, Theke, Platten, Flaschen, Säule, Bullaugen …), so wie die gewählten Teile Mosaik, Vitrinen, Ticket und Automat.
Titel, Satz und Angaben darüber bleiben Pixel für Pixel. Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll.
Baut weg-bar-wahl-2.html (Leiste unten, Pfeiltasten, ?weg=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/weg_bar_wahl2.py"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION
from weg_wahl import bild, BAR, TEL, META
from weg_bar_wahl import fo, tel, karte, quer, lauf

HIER = bau.HIER
F = []
KURZ = [('Donnerstag', '19 bis 1 Uhr'), ('Freitag', '19 bis 2 Uhr'), ('Samstag', '19 bis 2 Uhr')]


def kopf(cls=''):
    """Name als geschlossener Block: Die Bar, Walk on the Wild Side, Telefon."""
    return '<div class="zc-kopf %s"><p class="zc-name">Die Bar</p><p class="fk-wer">Walk on the Wild Side</p><p class="zc-tel">%s</p></div>' % (cls, tel())


def src(k, w=1000):
    st = META[k]['stufen']
    w = max(x for x in st if x <= w) if any(x <= w for x in st) else st[0]
    return 'assets/bild/%s-%d.webp?v=%s' % (k, w, VERSION)


# 1 Das Regal: drei Bretter an der dunklen Wand, auf jedem stehen gerahmte Bilder, vorn am Brett ein Messingschild mit Tag und Uhrzeit
BRETTER = [(('ecke', 78), ('schildnacht', 100), ('fassade', 86), ('barlicht', 70)),
           (('flur', 96), ('ws00', 74), ('barneg', 88), ('kerze3', 100)),
           (('bar', 82), ('schaumglas', 100), ('glasnacht', 76), ('theke', 92))]
F.append(('Das Regal', '<div class="zb zc01 auf">%s%s</div>' % (kopf('mitte'), ''.join(
    '<div class="zc01-fach">%s<div class="zc01-brett"><p class="zc01-schild"><b>%s</b> %s</p></div></div>' % (
        lauf('drift', (-40, 30, -50)[i], ''.join('<div class="zc01-rahmen" style="--h:%d%%">%s</div>' % (h, fo(k, '', '(max-width:860px) 25vw, 16vw')) for k, h in reihe), 'zc01-reihe'),
        t, z) for i, (reihe, (t, z)) in enumerate(zip(BRETTER, KURZ))))))

# 2 Die spiegelnde Theke: Bilder und Karte stehen auf schwarz glänzendem Holz und spiegeln sich darin; sie steigen, das Spiegelbild sinkt
STAND = [('ecke', 74), ('schildnacht', 92), None, ('flur', 96), ('barlicht', 70)]
def stand(spiegel=False):
    return ''.join(('<div class="zc02-i" style="--h:%d%%">%s</div>' % (h, fo(k, '', '(max-width:860px) 30vw, 18vw')) if s else
                    '<div class="zc02-i zc02-k">%s</div>' % karte()) for s in STAND for (k, h) in [s or ('', 100)])
F.append(('Die spiegelnde Theke', '<div class="zb zc02 auf">%s<div class="zc02-spiegel" aria-hidden="true" inert>%s</div></div>' % (
    lauf('drift', -50, stand(), 'zc02-reihe'), lauf('drift', 50, '<div class="zc02-umkehr">%s</div>' % stand(True), 'zc02-sl'))))

# 3 Die Plattenkiste: Plattenhüllen aus Fotos stehen in der Holzkiste, eine Hülle ist herausgezogen und trägt die Angaben; sie wird beim Scrollen weiter herausgezogen
HUELLEN = [('ws09', -7), ('barneg', 4), ('schildnacht', -3), ('flur', 5), ('ws00', -5), ('bar', 3)]
F.append(('Die Plattenkiste', '<div class="zb zc03 auf"><div class="zc03-kiste">%s%s<div class="zc03-front"><span>Walk on the Wild Side</span></div></div></div>' % (
    ''.join('<div class="zc03-h" style="--x:%d;--r:%ddeg">%s</div>' % (i, r, fo(k, '', '(max-width:860px) 30vw, 18vw')) for i, (k, r) in enumerate(HUELLEN)),
    lauf('drift', -110, '<div class="zc03-raus">%s</div>' % karte(), 'zc03-zug'))))

# 4 Die Platte: eine Schallplatte liegt halb aus der Hülle (Konzert in der Bar), auf dem Etikett das Schild, die Abende stehen rund in der Rille; sie dreht sich beim Scrollen
RUND = '  ·  '.join('%s %s' % tz for tz in KURZ) + '  ·  '
F.append(('Die Platte', '<div class="zb zc04 auf"><div class="zc04-bild"><div class="zc04-huelle">%s</div>%s</div>%s</div>' % (
    fo('ws09', '', '(max-width:860px) 80vw, 40vw'),
    lauf('dreh', 140, '<div class="zc04-platte"><div class="zc04-etikett">%s</div><svg class="zc04-rund" viewBox="0 0 400 400" aria-hidden="true"><defs><path id="zc04p" d="M200,200 m-148,0 a148,148 0 1,1 296,0 a148,148 0 1,1 -296,0"/></defs>'
         '<text><textPath href="#zc04p">%s</textPath></text></svg></div>' % (fo('schildnacht', '', '20vw', '50% 30%'), E(RUND)), 'zc04-dreh'),
    karte('zc04-k'))))

# 5 Der Fächer: sieben Bilder wie ein Blatt Karten aufgefächert, vorn steht die Karte; der Fächer geht beim Scrollen weiter auf
FAECHER = [('ecke', -39), ('schildnacht', -26), ('fassade', -13), ('flur', 13), ('barlicht', 26), ('ws00', 39)]
F.append(('Der Fächer', '<div class="zb zc05 auf"><div class="zc05-f" data-wb="faecher">%s</div><div class="zc05-k">%s</div></div>' % (
    ''.join('<div class="zc05-b" style="--a:%d">%s</div>' % (a, fo(k, '', '(max-width:860px) 40vw, 18vw')) for k, a in FAECHER), karte())))

# 6 Die Aufkleber: Bilder als Sticker mit weissem Rand auf der Stahltür, die Abende auf einem grossen runden Sticker in Kerzenfarbe, der sich beim Scrollen dreht
STICKER = [('schildnacht', 2, 4, 22, 46, -7), ('ecke', 24, 30, 20, 50, 5), ('flur', 66, 2, 17, 44, 8), ('ws00', 76, 46, 22, 46, -4), ('barlicht', 4, 56, 18, 38, 9), ('schildnah', 48, 64, 16, 32, -10)]
F.append(('Die Aufkleber', '<div class="zb zc06 auf">%s%s</div>' % (
    ''.join('<div class="zc06-s" style="left:%d%%;top:%d%%;width:%d%%;height:%d%%;--r:%ddeg">%s</div>' % (x, y, w, h, r, fo(k, '', '(max-width:860px) 50vw, 22vw')) for k, x, y, w, h, r in STICKER),
    lauf('dreh', 18, '<div class="zc06-rund"><p class="zc06-name">Die Bar</p><p class="zc06-wer">Walk on the Wild Side</p>%s<p class="zc06-tel">%s</p></div>' % (
        ''.join('<p class="zc06-z"><b>%s</b> %s</p>' % tz for tz in KURZ), tel()), 'zc06-dreh'))))

# 7 Die Litfasssäule: acht Bilder rund um eine Säule, die sich beim Scrollen dreht; daneben die Karte
SAEULE = ['ecke', 'schildnacht', 'fassade', 'flur', 'barlicht', 'ws00', 'barneg', 'schildnah']
F.append(('Die Litfasssäule', '<div class="zb zc07 auf"><div class="zc07-buehne"><i class="zc07-kappe"></i><div class="zc07-ring" data-wb="saeule" data-f="200">%s</div><i class="zc07-fuss"></i></div>%s</div>' % (
    ''.join('<div class="zc07-p" style="--i:%d">%s</div>' % (i, fo(k, '', '(max-width:860px) 40vw, 16vw')) for i, k in enumerate(SAEULE)), karte('zc07-k'))))

# 8 Der Riss: die Schilder an der Hausecke, mitten durchgerissen; im Riss steht die Karte, die beiden Hälften gehen beim Scrollen auseinander
def zacken(seite):
    pk = []
    for j in range(13):
        y = j * 100 / 12
        x = (100 - (6 if j % 2 else 0)) if seite == 'l' else (6 if j % 2 else 0)
        pk.append('%.1f%% %.2f%%' % (x, y))
    return 'polygon(0 0,%s,0 100%%)' % ','.join(pk) if seite == 'l' else 'polygon(%s,100%% 100%%,100%% 0)' % ','.join(pk)
F.append(('Der Riss', '<div class="zb zc08 auf">%s%s<div class="zc08-k">%s</div></div>' % (
    lauf('quer', -90, '<div class="zc08-h" style="clip-path:%s">%s</div>' % (zacken('l'), fo('schildtag', '', '100vw', '50% 40%')), 'zc08-l'),
    lauf('quer', 90, '<div class="zc08-h" style="clip-path:%s">%s</div>' % (zacken('r'), fo('schildtag', '', '100vw', '50% 40%')), 'zc08-r'),
    karte())))

# 9 Die Flügel: wie ein Klappaltar; in der Mitte die Karte, links und rechts je ein Flügel mit zwei Bildern, die beim Scrollen ganz aufgehen
F.append(('Die Flügel', '<div class="zb zc09 auf" data-wb="fluegel"><div class="zc09-f l">%s%s</div>%s<div class="zc09-f r">%s%s</div></div>' % (
    fo('ecke', '', '(max-width:860px) 50vw, 30vw'), fo('schildnacht', '', '(max-width:860px) 50vw, 30vw'), karte('zc09-k'),
    fo('flur', '', '(max-width:860px) 50vw, 30vw'), fo('barlicht', '', '(max-width:860px) 50vw, 30vw'))))

# 10 Bilder in der Schrift: «Die Bar» riesig, die Buchstaben sind mit dem Bild der Bar bei Nacht gefüllt; darunter gross die drei Abende
F.append(('Bilder in der Schrift', '<div class="zb zc10 auf">%s<p class="fk-wer zc10-wer">Walk on the Wild Side</p><div class="zc10-tage">%s</div><p class="zc-tel">%s</p></div>' % (
    lauf('drift', -60, '<p class="zc10-wort" style="background-image:url(%s)">Die Bar</p>' % src('flur'), 'zc10-lauf'),
    ''.join('<div><p class="zc10-tag">%s</p><p class="zc10-zeit">%s</p></div>' % tz for tz in KURZ), tel())))

# 11 Die Fallblattanzeige: die Abende auf einer Anzeige wie am Bahnhof, die Blätter fallen beim Ankommen herunter; daneben zwei Bilder
ZEILEN = [('WALK ON THE WILD SIDE', 'kopf'), ('DONNERSTAG 19:00-01:00', ''), ('FREITAG    19:00-02:00', ''), ('SAMSTAG    19:00-02:00', '')]
n = [0]
def blatt(z):
    out = []
    for ch in z.ljust(22):
        n[0] += 1
        out.append('<span class="zc11-c" style="--i:%d">%s</span>' % (n[0] % 40, '&nbsp;' if ch == ' ' else E(ch)))
    return ''.join(out)
F.append(('Die Fallblattanzeige', '<div class="zb zc11 auf"><div class="zc11-l"><div class="zc11-tafel" aria-label="Die Bar, Walk on the Wild Side: %s">%s</div>'
          '<p class="zc-tel">Die Bar · %s</p></div><div class="zc11-r">%s%s</div></div>' % (
              E(', '.join('%s %s' % tz for tz in KURZ)), ''.join('<div class="zc11-z %s" aria-hidden="true">%s</div>' % (c, blatt(z)) for z, c in ZEILEN), tel(),
              fo('schildnacht', '', '(max-width:860px) 50vw, 30vw'), fo('barlicht', '', '(max-width:860px) 50vw, 30vw'))))

# 12 Die Wendekarten: drei hohe Karten, vorn ein Bild, hinten der Abend; sie drehen sich nacheinander um, sobald sie in die Mitte kommen
F.append(('Die Wendekarten', '<div class="zb zc12 auf"><div class="zc12-reihe" data-wb="wenden">%s</div>%s</div>' % (
    ''.join('<div class="zc12-k" style="--o:%d"><div class="zc12-in"><div class="zc12-vorn">%s<p class="zc12-tagv">%s</p></div>'
            '<div class="zc12-hinten"><p class="fk-wer">Die Bar</p><p class="zc12-tag">%s</p><p class="zc12-zeit">%s</p></div></div></div>' % (
                i, fo(k, '', '(max-width:860px) 100vw, 33vw'), t, t, z) for i, ((t, z), k) in enumerate(zip(KURZ, ('barlicht', 'ws00', 'schildnacht')))),
    kopf('zeile'))))

# 13 Die Salonhängung: eine dichte Wand mit Bildern in Gold-, Schwarz- und Passepartout-Rahmen, die Karte hängt mittendrin; schief gehängt, beim Scrollen gerade
HAENGUNG = [('ecke', 1, 1, 3, 4, 'gold', -2), ('schildnacht', 4, 1, 2, 3, 'schwarz', 2), ('barlicht', 1, 5, 3, 4, 'pp', 1.5), ('flur', 4, 4, 2, 5, 'gold', -1.5),
            ('kerze3', 6, 7, 3, 2, 'schwarz', -2.5), ('fensterdraussen', 9, 1, 2, 4, 'schwarz', -2), ('schildnah', 11, 1, 2, 3, 'gold', 2.5), ('barneg', 9, 5, 4, 4, 'pp', -1),
            ('ws00', 11, 4, 2, 1, 'gold', 1)]
F.append(('Die Salonhängung', '<div class="zb zc13 auf" data-wb="gerade">%s<div class="zc13-r pp zc13-kr" style="grid-column:6/9;grid-row:1/7;--r:1.2">%s</div></div>' % (
    ''.join('<div class="zc13-r %s" style="grid-column:%d/span %d;grid-row:%d/span %d;--r:%s">%s</div>' % (art, c, w, r, h, rot, fo(k, '', '(max-width:860px) 50vw, 25vw'))
            for k, c, r, w, h, art, rot in HAENGUNG), karte())))

# 14 Die Rundsicht: die Bilder stehen innen in einem Rund wie ein Panorama, vorn die Karte; das Rund dreht sich beim Scrollen
RUNDSICHT = ['fassade', 'ecke', 'schildnacht', 'fensterdraussen', 'flur', 'barlicht', 'ws00', 'barneg', 'schildnah']
F.append(('Die Rundsicht', '<div class="zb zc14 auf"><div class="zc14-raum"><div class="zc14-ring" data-wb="rund" data-f="40">%s</div></div><div class="zc14-k">%s</div></div>' % (
    ''.join('<div class="zc14-p" style="--i:%d">%s</div>' % (i - 4, fo(k, '', '(max-width:860px) 40vw, 20vw')) for i, k in enumerate(RUNDSICHT)), karte())))

# 15 Die Doppelbelichtung: das Schild bei Nacht und der Flur übereinander belichtet; die zweite Aufnahme zieht beim Scrollen quer, daneben die Karte
F.append(('Die Doppelbelichtung', '<div class="zb zc15 auf"><div class="zc15-bild">%s%s</div>%s</div>' % (
    fo('schildnacht', 'zc15-a', '(max-width:860px) 100vw, 64vw', '50% 32%'),
    lauf('quer', 220, fo('flur', '', '(max-width:860px) 100vw, 70vw', '50% 50%'), 'zc15-b'), karte('zc15-k'))))

# 16 Die Flaschen: fünf Flaschen in einer Reihe, jede mit einem Bild gefüllt; die grosse in der Mitte trägt das Etikett mit den Abenden
FLASCHEN = [('ecke', 'rund', 62), ('schildnacht', 'eckig', 78), (None, 'gross', 100), ('flur', 'hoch', 86), ('barlicht', 'bauch', 58)]
F.append(('Die Flaschen', '<div class="zb zc16 auf">%s</div>' % lauf('drift', -50, ''.join(
    ('<div class="zc16-f %s" style="--h:%d%%">%s</div>' % (form, h, fo(k, '', '(max-width:860px) 30vw, 18vw')) if k else
     '<div class="zc16-f %s" style="--h:%d%%">%s<div class="zc16-etikett"><p class="zc16-name">Die Bar</p><p class="fk-wer">Walk on the Wild Side</p>%s<p class="zc-tel">%s</p></div></div>' % (
         form, h, fo('barneg', '', '(max-width:860px) 50vw, 26vw'), ''.join('<p class="zc16-z"><b>%s</b> %s</p>' % tz for tz in KURZ), tel()))
    for k, form, h in FLASCHEN), 'zc16-reihe')))

# 17 Das Daumenkino: der Weg als Block zum Durchblättern; beim Scrollen klappt Blatt um Blatt nach oben, von der Ecke bis zur Karte
BLAETTER = [('ecke', 'An der Ecke Rampenstraße'), ('schildnacht', 'Am Schild an der Hausecke'), ('fensterdraussen', 'Durchs Fenster'), ('flur', 'Durch den Flur'), ('ws00', 'In der Bar')]
F.append(('Das Daumenkino', '<div class="zb zc17 auf" data-wb-blaettern><div class="zc17-buehne"><div class="zc17-block">%s<div class="zc17-b zc17-letzt" style="z-index:1">%s</div></div></div></div>' % (
    ''.join('<div class="zc17-b" style="z-index:%d">%s</div>' % (10 - i, fo(k, '', '(max-width:860px) 100vw, 60vw', None, '<figcaption>%s</figcaption>' % E(t))) for i, (k, t) in enumerate(BLAETTER)),
    quer('zc17-k'))))

# 18 Das Rautenmuster: Bilder als Rauten im Harlekin-Muster über die ganze Breite, in der Mitte eine grosse helle Raute mit den Angaben
RAUTEN, BILDER = [], ['ecke', 'schildnacht', 'fassade', 'flur', 'barlicht', 'ws00', 'barneg', 'schildnah', 'kerze3', 'bar', 'fensterdraussen', 'glasnacht', 'theke', 'barnacht']
z = 0
for r in range(6):
    for c in range(-1, 7):
        x = c * 100 / 6 + (r % 2) * 100 / 12 - 100 / 12
        y = r * 100 / 6 - 100 / 6
        RAUTEN.append('<div class="zc18-r" style="left:%.3f%%;top:%.3f%%">%s</div>' % (x, y, fo(BILDER[z % len(BILDER)], '', '(max-width:860px) 34vw, 17vw')))
        z += 1
F.append(('Das Rautenmuster', '<div class="zb zc18 auf"><div class="zc18-feld">%s</div><div class="zc18-gross"><div class="zc18-text"><p class="zc-name">Die Bar</p><p class="fk-wer">Walk on the Wild Side</p>%s<p class="zc-tel">%s</p></div></div>%s</div>' % (
    lauf('quer', 70, ''.join(RAUTEN), 'zc18-lauf'), ''.join('<p class="zc18-z">%s %s</p>' % tz for tz in KURZ), tel(), karte('zc18-handy'))))

# 19 Das Leporello: sechs Felder im Zickzack gefaltet wie ein Faltblatt, das erste ist die Karte; beim Scrollen faltet es sich glatt auseinander
F.append(('Das Leporello', '<div class="zb zc19 auf"><div class="zc19-band" data-wb="leporello">%s%s</div></div>' % (
    '<div class="zc19-p zc19-erst" style="--s:1">%s</div>' % karte(),
    ''.join('<div class="zc19-p" style="--s:%d">%s</div>' % (-1 if i % 2 == 0 else 1, fo(k, '', '(max-width:860px) 50vw, 17vw')) for i, k in enumerate(('ecke', 'schildnacht', 'fensterdraussen', 'flur', 'ws00'))))))

# 20 Die Bullaugen: drei runde Fenster mit Messingring in der dunklen Wand, unter jedem ein Messingschild mit dem Abend; darüber der Name
F.append(('Die Bullaugen', '<div class="zb zc20 auf">%s<div class="zc20-reihe">%s</div></div>' % (
    kopf('mitte'), ''.join('<div class="zc20-auge"><div class="zc20-ring"><div class="zc20-glas">%s</div></div><p class="zc20-schild"><b>%s</b>%s</p></div>' % (
        lauf('zoom', .16, fo(k, '', '(max-width:860px) 70vw, 28vw'), 'zc20-zoom'), t, z) for (t, z), k in zip(KURZ, ('schildnacht', 'flur', 'ws00'))))))


def main():
    seite = open(os.path.join(HIER, 'weg.html'), encoding='utf-8').read()
    m = re.search(r'(<section class="vab bar-ab v-weg-abends[^"]*"[^>]*>)(.*?)(</section>)', seite, re.S)
    assert m, '«So findest du hin» in weg.html nicht gefunden'
    innen = m.group(2)
    vorn = innen[:innen.index('<div class="fw flaeche')]
    kopf_tag = m.group(1).replace('class="vab ', 'id="weg" data-name="Die Bar" class="wahl vab ', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % innen]
    teile += ['<div class="wv" data-n="%d" hidden>%s%s</div></div>' % (i, vorn, wand) for i, (_n, wand) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Die Bar</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: vier Bilder um die Karte'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('weg-bar-wahl.css', 'weg-bar-wahl-2.css', 'weg-bar-wahl.js', 'weg-bar-wahl-2.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["weg"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/weg-bar-wahl.js?v=%s" defer></script>
<script src="assets/weg-bar-wahl-2.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v, v)
    seite = seite.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
    seite = seite.replace('<title>', '<title>Bar-Karte wählen 2 · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/weg-bar-wahl.css?v=%s">\n'
                          '<link rel="stylesheet" href="assets/weg-bar-wahl-2.css?v=%s">\n</head>' % (VERSION, v, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'weg-bar-wahl-2.html'), 'w', encoding='utf-8').write(seite)
    print('Seite weg-bar-wahl-2.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
