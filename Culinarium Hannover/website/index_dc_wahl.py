#!/usr/bin/env python3
"""Startseite · Bildwand im Abschnitt Dirty Chicken in 15 Fassungen zur Wahl (28.10.2026 morgens).
Robert: «die Sticker und Logo + Überschrift finde ich schon super, geht nur um den Bereich darunter mit den Bildern.»
Kopf (Zeichen, Kicker, Titel, Text, Knopf) und die drei Sticker bleiben; nur die Fläche darunter wechselt. Alle Dirty-Chicken-Fotos, beide Filme (nie beschnitten),
das D als Form. Jede Fassung ein anderes Gerüst, ein bewegter Moment, nur transform und opacity, nie zwei Fotos übereinander, Gesichter unberührt.
Baut index-dc-wahl.html aus der echten index.html (?dcwand=Nummer, 0 = heute). Aufruf: python3 website/index_dc_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, foto, zl, sw
import varianten

HIER = bau.HIER
bau.META.update(bau.bilder())


def film(n, cls=''):
    """filmw: eigener Abspieler der Wahlseite, lädt nur die gezeigte Fassung (Film nie beschnitten)."""
    return ('<figure class="filmw %s" style="--lq:url(assets/film/%s.webp);aspect-ratio:%s"><video muted playsinline loop preload="none" poster="assets/film/%s.webp?v=%s" data-film="assets/film/%s.mp4?v=%s" aria-label="%s"></video></figure>') % (
        cls, n, '1/1' if n == 'familie' else '9/16', n, VERSION, n, VERSION, 'Die Mannschaft hinter der Theke' if n == 'familie' else 'Opening 2026 bei Dirty Chicken')


def f(k, sizes='(max-width:860px) 50vw, 24vw', pos=None):
    return foto(k, '', sizes, auf=False, pos=pos)


def d_pfade():
    s = open(os.path.join(HIER, 'assets/zeichen/haus.svg')).read()
    m = re.search(r'<symbol id="dc"[^>]*><g transform="([^"]+)">(.*?)</g></symbol>', s, re.S)
    return m.group(1), m.group(2)


def srcbild(k, w=1000):
    st = [x for x in bau.META[k]['stufen'] if x <= w]
    return 'assets/bild/%s-%d.webp?v=%s' % (k, max(st) if st else bau.META[k]['stufen'][0], VERSION)


def fuss_svg(cls=''):
    return '<svg class="%s" viewBox="-20 -32 40 68" aria-hidden="true"><path d="M0 34 L0 4 M0 4 L-14 -22 M0 4 L2 -28 M0 4 L18 -18"/></svg>' % cls


F = []

# 1 Das D aus Bildern: das Zeichen als Form, innen zwölf Fotos als Kacheln; daneben der Film
DG, DP = d_pfade()
KACHELN = ['dc_burger', 'dn_glas', 'dc_team', 'dn_tisch', 'dn_sosse', 'dc_drink', 'dn_bar', 'dc_tisch', 'dn_karte', 'dn_team', 'dn_drinks', 'dc_team2']
def d_kacheln():
    # Fläche des D: viewBox 214 197 652 712 → 3 Spalten à 217, 4 Zeilen à 178
    out = []
    for i, k in enumerate(KACHELN):
        c, r = i % 3, i // 3
        out.append('<image class="sdc1-k" style="--i:%d" href="%s" x="%d" y="%d" width="219" height="180" preserveAspectRatio="xMidYMid slice"/>' % (i, srcbild(k, 640), 214 + c * 217, 197 + r * 178))
    return ''.join(out)
F.append(('Das D aus Bildern', 'Das Zeichen selbst als grosse Form, innen zwölf Fotos als Kacheln, die sich beim Ankommen setzen; daneben der Film.', '''<div class="sdc sdc1 auf">
<svg class="sdc1-d" viewBox="214 197 652 712" aria-label="Das D von Dirty Chicken aus Fotos"><defs><mask id="sdc1m" maskUnits="userSpaceOnUse" x="214" y="197" width="652" height="712"><rect x="214" y="197" width="652" height="712" fill="#000"/><g transform="%s" fill="#fff">%s</g></mask></defs><g mask="url(#sdc1m)"><rect x="214" y="197" width="652" height="712" fill="#3B1F4D"/>%s</g></svg>
<div class="sdc1-film">%s</div></div>''' % (DG, DP, d_kacheln(), film('opening', 'sdc1-f'))))

# 2 Der Sticker-Bogen: ein heller Stickerbogen, die Fotos als ausgestanzte Sticker mit weissem Rand
STICKER = [('dc_burger', -4), ('dn_glas', 3), ('dc_team', -2), ('film', 2), ('dn_tisch', 4), ('dc_drink', -3), ('dn_bar', 2), ('dc_plakat', -2)]
F.append(('Der Sticker-Bogen', 'Ein heller Stickerbogen wie beim Sticker oben: die Fotos als ausgestanzte Sticker mit weissem Rand, jeder leicht gedreht, keiner über dem anderen; sie lösen sich beim Ankommen vom Bogen.', '<div class="sdc sdc2 auf"><div class="sdc2-bogen">%s</div></div>' % ''.join(
    '<div class="sdc2-s" style="--r:%ddeg;--i:%d">%s</div>' % (r, i, film('opening', 'sdc2-f') if k == 'film' else f(k, pos='50% 40%')) for i, (k, r) in enumerate(STICKER))))

# 3 Der Comic: Panels mit schwarzen Stegen, Sprechblasen in Berliner Schnauze
COMIC = [('dc_burger', 'w', '„Dit is keen Burger.“'), ('dn_sosse', '', ''), ('film', 'h2', '„Wat ne Sause.“'), ('dc_drink', '', '„Jenau meen Ding wa.“'), ('dn_team', '', ''), ('dc_tisch', '', '„Dit ist wahre Liebe!“')]
F.append(('Der Comic', 'Die Fotos als Comic-Panels mit schwarzen Stegen, dazu Sprechblasen mit den echten Zeilen in Berliner Schnauze; der Film ist das hohe Panel.', '<div class="sdc sdc3 auf"><div class="sdc3-seite">%s</div></div>' % ''.join(
    '<div class="sdc3-p %s" style="--i:%d">%s%s</div>' % (c, i, film('opening', 'sdc3-f') if k == 'film' else f(k, '(max-width:860px) 50vw, 30vw', '50% 40%'), ('<span class="sdc3-b">%s</span>' % t) if t else '')
    for i, (k, c, t) in enumerate(COMIC))))

# 4 Die Fussspur: Hühnerfüsse laufen im Zickzack über die Fläche, an jedem Knick ein Foto
SPUR = [('dc_burger', 'o'), ('dn_glas', 'u'), ('film', 'o'), ('dc_team', 'u'), ('dn_tisch', 'o')]
F.append(('Die Fussspur', 'Hühnerfüsse laufen im Zickzack über die Fläche, Schritt für Schritt; an jedem Knick steht ein Foto, der Film mittendrin.', '<div class="sdc sdc4 auf"><div class="sdc4-weg">%s%s</div></div>' % (
    ''.join('<i class="sdc4-f" style="--i:%d;--x:%d%%;--y:%d%%;--r:%ddeg">%s</i>' % (i, 4 + i * 8, 50 + (14 if i % 2 else -14), (-20 if i % 2 else 20), fuss_svg()) for i in range(12)),
    ''.join('<div class="sdc4-b %s" style="--i:%d">%s</div>' % (c, i, film('opening', 'sdc4-film') if k == 'film' else f(k, pos='50% 40%')) for i, (k, c) in enumerate(SPUR)))))

# 5 Das Regal: die Fotos stehen auf einem Brett, verschieden hoch, der Film in der Mitte am höchsten
REGAL = [('dn_glas', 'h2'), ('dc_burger', 'h1'), ('dn_bar', 'h3'), ('film', 'h4'), ('dc_team', 'h1'), ('dn_tisch', 'h3'), ('dc_drink', 'h2')]
F.append(('Das Regal', 'Die Fotos stehen wie Flaschen auf einem Brett, verschieden hoch, der Film in der Mitte am höchsten; sie werden nacheinander abgestellt.', '<div class="sdc sdc5 auf"><div class="sdc5-brett">%s</div><i class="sdc5-kante"></i></div>' % ''.join(
    '<div class="sdc5-b %s" style="--i:%d">%s</div>' % (c, i, film('opening', 'sdc5-f') if k == 'film' else f(k, pos='50% 40%')) for i, (k, c) in enumerate(REGAL))))

# 6 Der Kontaktbogen: Negativstreifen mit Bildnummern, ein Bild mit Fettstift eingekreist
KONTAKT = ['dc_burger', 'dn_sosse', 'dc_drink', 'dn_glas', 'dc_team', 'dn_tisch', 'dn_bar', 'dc_tisch', 'dn_karte', 'dn_team']
F.append(('Der Kontaktbogen', 'Ein Kontaktbogen wie vom Fotografen: zwei Negativstreifen mit Bildnummern, die Fotos als Abzüge, eins mit Fettstift eingekreist; am Ende der Film.', '<div class="sdc sdc6 auf"><div class="sdc6-bogen"><div class="sdc6-streifen">%s</div><div class="sdc6-streifen">%s%s</div></div></div>' % (
    ''.join('<div class="sdc6-b%s" style="--i:%d"><span class="mono">%02dA</span>%s</div>' % (' kreis' if i == 2 else '', i, i + 1, f(k, '(max-width:860px) 40vw, 18vw', '50% 40%')) for i, k in enumerate(KONTAKT[:5])),
    ''.join('<div class="sdc6-b" style="--i:%d"><span class="mono">%02dA</span>%s</div>' % (i + 5, i + 6, f(k, '(max-width:860px) 40vw, 18vw', '50% 40%')) for i, k in enumerate(KONTAKT[5:9])),
    '<div class="sdc6-b sdc6-film" style="--i:9"><span class="mono">10A</span>%s</div>' % film('opening', 'sdc6-f'))))

# 7 Das Profil: das Instagram-Profil als Raster, neun Quadrate, der quadratische Film der Mannschaft mittendrin
PROFIL = ['dc_burger', 'dc_drink', 'dc_tisch', 'dn_glas', 'film', 'dn_bar', 'dc_team', 'dn_karte', 'dn_salat']
F.append(('Das Profil', 'Das Instagram-Profil als Raster: Kopf mit Zeichen und Namen, darunter neun Quadrate, der quadratische Film der Mannschaft mittendrin.', '''<div class="sdc sdc7 auf"><div class="sdc7-kopf"><span class="sdc7-d">%s</span><div><b>dirtychicken.hannover</b><span>Sandwiches &amp; More · Pop-up aus dem Walk on the Wild Side</span></div><a class="sdc7-folgen" href="https://www.instagram.com/dirtychicken.hannover/" target="_blank" rel="noopener">Folgen</a></div>
<div class="sdc7-raster">%s</div></div>''' % (bau.zeichen_haus('dc', 'sdc7-dz'), ''.join(
    '<div class="sdc7-q" style="--i:%d">%s</div>' % (i, film('familie', 'sdc7-f') if k == 'film' else f(k, '(max-width:860px) 33vw, 15vw', '50% 40%')) for i, k in enumerate(PROFIL)))))

# 8 Die Taschenlampe: eine dunkle Bildwand, der Lichtkegel folgt der Maus; am Handy wandert er von selbst
LAMPE = ['dc_burger', 'dn_glas', 'dc_team', 'dn_tisch', 'dn_sosse', 'dc_drink', 'dn_bar', 'dc_tisch']
F.append(('Die Taschenlampe', 'Eine dunkle Bildwand, nur ein Lichtkegel zeigt die Fotos: Er folgt der Maus, am Handy wandert er von selbst über die Wand.', '<div class="sdc sdc8 auf"><div class="sdc8-wand">%s<div class="sdc8-licht" aria-hidden="true"></div></div></div>' % ''.join(
    '<div class="sdc8-b">%s</div>' % f(k, '(max-width:860px) 50vw, 25vw', '50% 40%') for k in LAMPE)))

# 9 Aufräumen: die Fotos liegen verstreut und gedreht, beim Ankommen rücken sie in ein sauberes Raster
AUF = [('dc_burger', -9, 26, 14), ('dn_glas', 7, -18, -10), ('film', -4, 10, 22), ('dc_team', 11, -30, 8), ('dn_tisch', -7, 22, -16), ('dc_drink', 5, -12, 18)]
F.append(('Aufräumen', 'Die Fotos liegen verstreut und schief auf dem Tisch; beim Ankommen rücken sie mit einem Federn in ein sauberes Raster.', '<div class="sdc sdc9 auf"><div class="sdc9-raster">%s</div></div>' % ''.join(
    '<div class="sdc9-b" style="--i:%d;--r:%ddeg;--x:%dpx;--y:%dpx">%s</div>' % (i, r, x, y, film('opening', 'sdc9-f') if k == 'film' else f(k, '(max-width:860px) 50vw, 30vw', '50% 40%')) for i, (k, r, x, y) in enumerate(AUF))))

# 10 Die Jalousie: ein grosses Bild hinter Lamellen, die nacheinander zur Seite fahren; daneben der Film
F.append(('Die Jalousie', 'Ein grosses Bild vom vollen Tisch liegt hinter violetten Lamellen, die beim Ankommen nacheinander zur Seite fahren; daneben der Film.', '<div class="sdc sdc10 auf"><div class="sdc10-bild">%s<div class="sdc10-lamellen" aria-hidden="true">%s</div></div><div class="sdc10-film">%s</div></div>' % (
    f('dn_tisch', '(max-width:860px) 100vw, 60vw', '50% 50%'), ''.join('<i style="--i:%d"></i>' % i for i in range(8)), film('opening', 'sdc10-f'))))

# 11 Der Diaprojektor: ein grosser Rahmen, die Dias wechseln von selbst, darunter die kleinen Bilder zum Anwählen
DIAS = ['dc_burger', 'dn_sosse', 'dc_drink', 'dn_tisch', 'dc_team', 'dn_glas', 'dn_bar']
F.append(('Der Diaprojektor', 'Ein grosser Rahmen wie beim Diaabend: alle paar Sekunden schiebt das nächste Bild herein, darunter die kleinen Bilder zum Anwählen; der Film läuft daneben.', '''<div class="sdc sdc11 auf" data-akt="0"><div class="sdc11-rahmen">%s</div><div class="sdc11-film">%s</div>
<div class="sdc11-leiste">%s</div></div>''' % (
    ''.join('<div class="sdc11-d" data-s="%d">%s</div>' % (i, f(k, '(max-width:860px) 100vw, 66vw', '50% 45%')) for i, k in enumerate(DIAS)), film('opening', 'sdc11-f'),
    ''.join('<button type="button" class="sdc11-k%s" data-s="%d" aria-label="Bild %d"><img src="%s" alt="" loading="lazy" decoding="async"></button>' % (' an' if i == 0 else '', i, i + 1, srcbild(k, 640)) for i, k in enumerate(DIAS)))))

# 12 Das Band: ein breites Band zum Blättern mit Laufbalken, jedes Bild mit seiner Zeile
BAND = [('dc_burger', 'Dit is keen Burger.'), ('dn_sosse', 'Grüne Sauce drauf.'), ('film', 'Opening 2026.'), ('dn_glas', 'Dirty Drinks.'), ('dc_team', 'Die Mannschaft.'), ('dn_tisch', 'Alles auf einmal.'), ('dc_plakat', 'Das Plakat.'), ('dn_bar', 'An der Theke.')]
F.append(('Das Band', 'Ein breites Band zum seitwärts Blättern, jedes Bild mit seiner Zeile, ein Laufbalken zeigt, wo man ist; der Film blättert mit.', '''<div class="sdc sdc12 auf"><div class="sdc12-band">%s</div><div class="sdc12-fuss"><div class="sdc12-lauf"><i></i></div><div class="sdc12-pfeile"><button type="button" data-sdc12="-1" aria-label="Zurück">‹</button><button type="button" data-sdc12="1" aria-label="Weiter">›</button></div></div></div>''' % ''.join(
    '<div class="sdc12-k">%s<p class="sdc12-z">%s</p></div>' % (film('opening', 'sdc12-f') if k == 'film' else f(k, '(max-width:860px) 80vw, 34vw', '50% 40%'), t) for k, t in BAND)))

# 13 Die Wand gleitet: sechs Felder, jedes Foto gleitet beim Scrollen in eigenem Tempo im Rahmen
GLEIT = [('dc_burger', '1'), ('film', '0'), ('dn_tisch', '-1'), ('dn_glas', '-1'), ('dc_team', '1'), ('dc_drink', '0')]
F.append(('Die Wand gleitet', 'Sechs Felder Wand an Wand, der Film in der Mitte; beim Scrollen gleitet jedes Foto in seinem Rahmen in eigenem Tempo, mal mit, mal gegen den Strom.', '<div class="sdc sdc13 auf"><div class="sdc13-wand">%s</div></div>' % ''.join(
    '<div class="sdc13-f" style="--g0:%s">%s</div>' % (g, film('opening', 'sdc13-film') if k == 'film' else f(k, '(max-width:860px) 50vw, 30vw', '50% 40%')) for k, g in GLEIT)))

# 14 Die Bons am Pass: eine Schiene wie am Küchenpass, die Fotos hängen daran wie Bestellzettel mit Abriss
PASS = ['dc_burger', 'dn_sosse', 'film', 'dc_drink', 'dn_glas', 'dc_team']
F.append(('Die Bons am Pass', 'Eine Metallschiene wie am Küchenpass, die Fotos hängen daran mit Klammer wie Bestellzettel, oben abgerissen; beim Ankommen pendeln sie kurz aus.', '<div class="sdc sdc14 auf"><i class="sdc14-schiene"></i><div class="sdc14-zettel">%s</div></div>' % ''.join(
    '<div class="sdc14-z" style="--i:%d"><i class="sdc14-klammer"></i>%s</div>' % (i, film('opening', 'sdc14-f') if k == 'film' else f(k, pos='50% 40%')) for i, k in enumerate(PASS))))

# 15 Die Theke: eine Reihe läuft von selbst wie Teller über den Tresen, jedes Bild mit Zeile; Maus drauf hält an
THEKE = [('dc_burger', 'Sandwich'), ('dn_sosse', 'Chicken Chunks'), ('dn_glas', 'Dirty Drinks'), ('film', 'Opening 2026'), ('dc_team', 'Die Mannschaft'), ('dn_tisch', 'Alles auf einmal'), ('dn_bar', 'An der Theke'), ('dc_plakat', 'Das Plakat')]
def theke():
    return ''.join('<div class="sdc15-t">%s<span class="mono">%s</span></div>' % (film('opening', 'sdc15-f') if k == 'film' else f(k, '(max-width:860px) 60vw, 24vw', '50% 40%'), t) for k, t in THEKE)
F.append(('Die Theke', 'Eine Reihe läuft von selbst über die Fläche wie Teller über den Tresen, jedes Bild mit seiner Zeile; Maus drauf hält sie an.', '<div class="sdc sdc15 auf"><div class="sdc15-zug">%s%s</div></div>' % (theke(), theke())))


# ================================================================== Zweite Runde (Robert 28.10.2026: «gib nochmal 15 versionen für die wand»), Nummern 16 bis 30

# 16 Ein Bild: ein einziges Foto, so breit wie die Fläche, sonst nichts
F.append(('Ein Bild', 'Ein einziges Foto, so breit wie die Fläche, breit wie eine Leinwand, darunter eine Zeile; sonst nichts. Gross schlägt viel.', '<div class="sdc sdc16 auf">%s<p class="mono sdc16-z">Alles auf einmal · Pop-up im Tiedthof, Juni 2026</p></div>' % f('dn_tisch', '100vw', '50% 52%')))

# 17 Zwei Filme: beide Filme nebeneinander, unbeschnitten, dazu zwei Fotos
F.append(('Zwei Filme', 'Beide Filme nebeneinander, unbeschnitten und beide laufen: das Opening hoch, die Mannschaft quadratisch; rechts zwei Fotos übereinander.', '<div class="sdc sdc17 auf">%s%s<div class="sdc17-col">%s%s</div></div>' % (
    film('opening', 'o'), film('familie', 'q'), f('dc_burger', '(max-width:860px) 50vw, 30vw', '50% 50%'), f('dn_glas', '(max-width:860px) 50vw, 30vw', '50% 50%'))))

# 18 Das Karussell: acht runde Fotos drehen langsam um den Film in der Mitte, bleiben dabei aufrecht
KAR = ['dc_burger', 'dn_glas', 'dc_team', 'dn_tisch', 'dn_sosse', 'dc_drink', 'dn_bar', 'dc_tisch']
F.append(('Das Karussell', 'Acht runde Fotos drehen langsam um den Film in der Mitte und bleiben dabei aufrecht, wie Teller auf einem Drehteller.', '<div class="sdc sdc18 auf"><div class="sdc18-ring">%s</div><div class="sdc18-mitte">%s</div></div>' % (
    ''.join('<div class="sdc18-arm" style="--a:%ddeg"><div class="sdc18-b">%s</div></div>' % (i * 45, f(k, '(max-width:860px) 30vw, 12vw', '50% 40%')) for i, k in enumerate(KAR)), film('opening', 'sdc18-f'))))

# 19 Die Pyramide: drei unten, zwei in der Mitte, der Film oben
F.append(('Die Pyramide', 'Drei Fotos unten, zwei in der Mitte, der Film ganz oben: eine Pyramide, die sich von unten nach oben aufbaut.', '<div class="sdc sdc19 auf"><div class="sdc19-r r3">%s</div><div class="sdc19-r r2">%s</div><div class="sdc19-r r1">%s</div></div>' % (
    ''.join('<div class="sdc19-b" style="--i:%d">%s</div>' % (i, f(k, pos='50% 40%')) for i, k in enumerate(['dc_burger', 'dn_tisch', 'dc_team'])),
    ''.join('<div class="sdc19-b" style="--i:%d">%s</div>' % (i + 3, f(k, pos='50% 40%')) for i, k in enumerate(['dn_glas', 'dc_drink'])),
    '<div class="sdc19-b" style="--i:5">%s</div>' % film('opening', 'sdc19-f'))))

# 20 Das Kreuz: der Film in der Mitte, oben, unten, links und rechts je ein Foto; die Ecken bleiben Tapete
F.append(('Das Kreuz', 'Der Film in der Mitte, darüber, darunter, links und rechts je ein Foto; die Ecken bleiben Tapete, so hat jedes Bild Luft.', '<div class="sdc sdc20 auf"><div class="sdc20-o">%s</div><div class="sdc20-l">%s</div><div class="sdc20-m">%s</div><div class="sdc20-r">%s</div><div class="sdc20-u">%s</div></div>' % (
    f('dn_team', '(max-width:860px) 100vw, 30vw', '50% 42%'), f('dn_glas', '(max-width:860px) 50vw, 24vw'), film('opening', 'sdc20-f'), f('dc_burger', '(max-width:860px) 50vw, 24vw'), f('dn_tisch', '(max-width:860px) 100vw, 30vw'))))

# 21 Der Bogen: sieben Fotos stehen auf einem Bogen wie Karten in der Hand, jedes leicht gedreht, keines über dem anderen
BOG = ['dn_glas', 'dc_burger', 'dn_bar', 'film', 'dc_team', 'dn_tisch', 'dc_drink']
F.append(('Der Bogen', 'Sieben Fotos stehen auf einem Bogen wie Karten in der Hand, jedes leicht mitgedreht, keines über dem anderen; der Film in der Mitte oben.', '<div class="sdc sdc21 auf"><div class="sdc21-bogen">%s</div></div>' % ''.join(
    '<div class="sdc21-b" style="--a:%ddeg;--i:%d">%s</div>' % (-39 + i * 13, i, film('opening', 'sdc21-f') if k == 'film' else f(k, '(max-width:860px) 40vw, 14vw', '50% 40%')) for i, k in enumerate(BOG))))

# 22 Das Daumenkino: die Standbilder des Films blättern schnell wie ein Daumenkino, daneben drei Fotos
F.append(('Das Daumenkino', 'Die acht Standbilder des Films blättern schnell durch wie ein Daumenkino, sobald man davor steht; daneben drei Fotos.', '<div class="sdc sdc22 auf"><div class="sdc22-kino" data-s="0">%s</div><div class="sdc22-fotos">%s%s%s</div></div>' % (
    ''.join('<figure class="sdc22-bl" data-s="%d"><img src="assets/film/opening-still-%d.webp?v=%s" alt="" loading="eager" decoding="async"></figure>' % (i, t, VERSION) for i, t in enumerate([1, 5, 9, 13, 17, 21, 25, 29])),
    f('dc_burger', '(max-width:860px) 50vw, 30vw'), f('dn_tisch', '(max-width:860px) 50vw, 30vw'), f('dc_team', '(max-width:860px) 100vw, 60vw', '50% 40%'))))

# 23 Blinklicht: acht Kacheln wie Leuchtkästen einer Bar, die ab und zu kurz flackern
BLINK = ['dc_burger', 'dn_glas', 'dc_team', 'dn_sosse', 'dc_drink', 'dn_tisch', 'dn_bar', 'dc_tisch']
F.append(('Blinklicht', 'Acht Kacheln wie die Leuchtkästen einer Bar, jede flackert ab und zu kurz, nie zwei zugleich; das Licht geht nie ganz aus.', '<div class="sdc sdc23 auf"><div class="sdc23-wand">%s</div></div>' % ''.join(
    '<div class="sdc23-k" style="--t:%.1fs;--d:%.1fs">%s<i></i></div>' % (7 + (i * 3) % 5, (i * 1.7) % 6, f(k, '(max-width:860px) 50vw, 24vw', '50% 40%')) for i, k in enumerate(BLINK))))

# 24 Der Tausch: acht Kacheln, alle drei Sekunden tauschen zwei ihren Platz
TAUSCH = ['dc_burger', 'dn_glas', 'film', 'dn_tisch', 'dc_team', 'dn_sosse', 'dc_drink', 'dn_bar']
F.append(('Der Tausch', 'Acht Kacheln in zwei Reihen; alle drei Sekunden tauschen zwei von ihnen den Platz, sie gleiten aneinander vorbei. Nichts springt.', '<div class="sdc sdc24 auf"><div class="sdc24-raster">%s</div></div>' % ''.join(
    '<div class="sdc24-k" data-i="%d">%s</div>' % (i, film('opening', 'sdc24-f') if k == 'film' else f(k, '(max-width:860px) 50vw, 24vw', '50% 40%')) for i, k in enumerate(TAUSCH))))

# 25 Die Lupe: ein grosses Bild, wo die Maus steht, zeigt ein Kreis das zweite Bild darunter
F.append(('Die Lupe', 'Ein grosses Bild der Mannschaft; wo die Maus hinfährt, zeigt ein Kreis das Bild darunter, den vollen Tisch. Am Handy wandert der Kreis von selbst.', '<div class="sdc sdc25 auf"><div class="sdc25-buehne"><div class="sdc25-a">%s</div><div class="sdc25-b">%s</div></div><div class="sdc25-film">%s</div></div>' % (
    f('dn_team', '(max-width:860px) 100vw, 70vw', '50% 42%'), f('dn_tisch', '(max-width:860px) 100vw, 70vw', '50% 50%'), film('opening', 'sdc25-f'))))

# 26 Mauerwerk: drei Spalten, jedes Foto in seinem eigenen Format, nichts beschnitten
MAUER = ['dc_burger', 'dn_glas', 'film', 'dn_team', 'dc_drink', 'dn_tisch', 'dc_team', 'dn_bar', 'dc_plakat']
F.append(('Mauerwerk', 'Drei Spalten wie gemauert: jedes Foto in seinem eigenen Format, hoch, quer, quadratisch, nichts beschnitten; der Film sitzt mittendrin.', '<div class="sdc sdc26 auf"><div class="sdc26-mauer">%s</div></div>' % ''.join(
    '<div class="sdc26-s" style="--i:%d">%s</div>' % (i, film('opening', 'sdc26-f') if k == 'film' else foto(k, '', '(max-width:860px) 50vw, 30vw', auf=False, ratio=True)) for i, k in enumerate(MAUER))))

# 27 Der Zug: eine Reihe hoher Fotos, die beim Scrollen seitwärts zieht
ZUG = ['dc_burger', 'dn_sosse', 'film', 'dn_glas', 'dc_team', 'dn_tisch', 'dn_bar', 'dc_tisch', 'dc_plakat']
F.append(('Der Zug', 'Eine Reihe hoher Fotos, breiter als der Schirm, die beim Scrollen seitwärts durchzieht; der Film fährt mit.', '<div class="sdc sdc27 auf"><div class="sdc27-zug">%s</div></div>' % ''.join(
    '<div class="sdc27-w">%s</div>' % (film('opening', 'sdc27-f') if k == 'film' else f(k, '(max-width:860px) 60vw, 22vw', '50% 40%')) for k in ZUG)))

# 28 Die Kreise: fünf runde Fotos in verschiedenen Grössen, der Film als hohe Pille
KREISE = [('dc_burger', 'g'), ('dn_glas', 'm'), ('film', ''), ('dc_team', 'g'), ('dn_tisch', 'm'), ('dc_drink', 'k')]
F.append(('Die Kreise', 'Fünf runde Fotos in drei Grössen, versetzt auf und ab wie Blasen, der Film als hohe Pille dazwischen.', '<div class="sdc sdc28 auf"><div class="sdc28-reihe">%s</div></div>' % ''.join(
    '<div class="sdc28-b %s" style="--i:%d">%s</div>' % (c, i, film('opening', 'sdc28-f') if k == 'film' else f(k, '(max-width:860px) 40vw, 18vw', '50% 40%')) for i, (k, c) in enumerate(KREISE))))

# 29 Näher ran: ein grosses Foto, das beim Scrollen langsam näher kommt, daneben der Film
F.append(('Näher ran', 'Ein grosses Foto vom Tisch mit den Drinks, das beim Scrollen langsam näher kommt, als würde man sich an den Tisch setzen; daneben der Film.', '<div class="sdc sdc29 auf"><div class="sdc29-rahmen"><div class="sdc29-zoom">%s</div></div><div class="sdc29-film">%s</div></div>' % (
    f('dn_drinks', '(max-width:860px) 100vw, 66vw', '50% 45%'), film('opening', 'sdc29-f'))))

# 30 Die Galerie: sechs Abzüge mit hellem Passepartout, Zeile darunter, wie an einer Galeriewand
GAL = [('dc_burger', 'Sandwich'), ('dn_glas', 'Dirty Drinks'), ('film', 'Opening 2026'), ('dc_team', 'Die Mannschaft'), ('dn_sosse', 'Chicken Chunks'), ('dn_tisch', 'Alles auf einmal')]
F.append(('Die Galerie', 'Sechs Abzüge mit hellem Passepartout und Zeile darunter, wie an einer Galeriewand gehängt; der Film hängt als Hochformat dazwischen.', '<div class="sdc sdc30 auf"><div class="sdc30-wand">%s</div></div>' % ''.join(
    '<div class="sdc30-r" style="--i:%d">%s<span class="mono">%s</span></div>' % (i, film('opening', 'sdc30-f') if k == 'film' else f(k, '(max-width:860px) 50vw, 16vw', '50% 40%'), t) for i, (k, t) in enumerate(GAL))))


def main():
    h = open(os.path.join(HIER, 'index.html'), encoding='utf-8').read()
    m = re.search(r'(<section class="vab v-dirty-chicken[^"]*"[^>]*>.*?)(<div class="fw flaeche auf".*?)(<div class="stk stk-satz")', h, re.S)
    assert m, 'Bildwand im Dirty-Chicken-Teil nicht gefunden'
    alt = m.group(2)
    teile = ['<div class="wv" data-n="0">%s</div>' % alt]
    teile += ['<div class="wv" data-n="%d" hidden>%s</div>' % (i, x) for i, (_n, _s, x) in enumerate(F, 1)]
    neu = '<div class="dw wahl" id="dcwand" data-name="Bildwand"><div class="wahl-marke"><b>Bildwand</b><span data-nr></span></div>%s</div>' % ''.join(teile)
    h = h[:m.start(2)] + neu + h[m.end(2):]
    namen = ['Heute: Burger, Drink, Film, Tisch, Team'] + [re.sub('&amp;', '&', n) for n, _s, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('index-dc-wahl.css', 'index-dc-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["dcwand"],daumen:%s};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/index-dc-wahl.js?v=%s" defer></script>''' % (
        json.dumps(namen, ensure_ascii=False), 'true' if os.path.exists(os.path.join(HIER, 'assets/daumen/dcwand-1.jpg')) else 'false', VERSION, v)
    h = h.replace('<title>', '<title>Bildwand Dirty Chicken wählen · ', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/index-dc-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    h = h.replace('</body>', leiste + '\n</body>', 1)
    for fk in varianten.FILMLQ:
        h = h.replace('--lq:url(assets/film/%s.webp)' % fk, '--lq:url(%s)' % varianten.FILMLQ[fk])
    open(os.path.join(HIER, 'index-dc-wahl.html'), 'w', encoding='utf-8').write(h)
    json.dump([{'nr': i, 'name': n, 'satz': s_} for i, (n, s_, _x) in enumerate(F, 1)], open(os.path.join(HIER, '_sicherung', 'dcwand-fassungen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Seite index-dc-wahl.html', len(h) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
