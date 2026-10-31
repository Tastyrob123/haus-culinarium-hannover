#!/usr/bin/env python3
"""Culinarium Hannover · Kopf von «Alle Abende» (abende.html) in 15 Fassungen, zweite Runde 27.10.2026.
Robert zur ersten Runde (lauter Plakate, Stand *.vor-fotos-2026-10-27): «Es macht jetzt überhaupt keinen Sinn, ein Hero zu bauen, wo schon wieder Poster sind.
Wir haben so viele Bilder von dem Restaurant, von den Abenden, von der Atmosphäre.» Deshalb hier nur Rudis Fotos der Abende, kein Plakat;
die Plakate zeigt die Seite darunter (Vitrinen) und am Schluss.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut abende-kopf-wahl.html (Leiste unten, Pfeiltasten, ?kopf=Nummer); Fassung 0 ist der heutige Stand.
Dritte Runde: jede Fassung ist ein Hero über den ganzen ersten Bildschirm (Robert: «Es muss ein Hero sein … Und nicht ein Abschnitt»).
Aufruf: python3 website/bau.py && python3 website/kopf_wahl.py"""
import json, os, re, sys
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, zl, sw

Image.MAX_IMAGE_PIXELS = None
HIER, PROJ = bau.HIER, bau.PROJ
SATZ = 'Seit dem ersten Pop-up im Mai 2023 und den ersten Culinarium-Plakaten im September 2023. Jeder Abend mit seinem Plakat, so wie er angekündigt wurde.'

# Rudis Fotos der Abende (_quelle/vom-kunden/drive), Beschreibung für alt
FOTO = {
    '5376': 'Am Tisch wird bei Kerzen angestossen',
    '4574': 'Gäste stossen an einem Tisch der Bar an',
    '3887': 'Durch den Flur in die Bar',
    '5022': 'Gäste klatschen an der Tafel bei Kerzenlicht',
    '3858': 'Ein Drink wird bei Kerzenlicht erklärt',
    '3855': 'An der Bar wird erklärt, vorn brennen Kerzen',
    '3901': 'Die lange Tafel voller Gäste',
    '3842': 'Kerzen, Flaschen und Gläser auf der Tafel',
    '4108': 'Ein Drink mit Schaum bei Kerzenlicht',
    '4972': 'Die lange Tafel mit Kerzen, gedeckt',
    '3916': 'Kerze und Drink an der Tafel',
    '36913': 'Gäste an der Tafel unter den Lampen',
    '4004': 'Im schmalen Raum wird an der Tafel erklärt',
    '5062': 'Gläser vor dem Negroni-Schriftzug',
    '4568': 'An der Bar wird ein Drink geschüttelt',
    '3986': 'Abend in der Bar unter der bemalten Decke',
    '5005': 'An der Tafel wird angestossen',
    '3859': 'Blick durch die Tür auf die Tafel',
    '64066': 'Der Koch erklärt den Teller, Gäste fotografieren',
    '37016': 'Im Service an der Tafel',
    '5409': 'Ein Drink im Stielglas',
    '5037': 'Ein Teller wird an den Tisch gebracht',
    '4026': 'Zwei Gläser stossen an',
    '3831': 'Zwei Gäste lachen an der Bar',
    '4024': 'Am Tisch wird angestossen',
    '4093': 'Die Bar von aussen bei Nacht',
}
QUELLE = {n: next(p for p in ('_quelle/vom-kunden/drive/%s.jpg' % n, '_quelle/vom-kunden/%s.jpg' % n, '_quelle/vom-kunden/drive-arw-vorschau/%s.jpg' % n)
                  if os.path.exists(os.path.join(PROJ, p))) for n in FOTO}
STUFEN = (800, 1400, 2200)


def fotos_machen():
    for n, q in QUELLE.items():
        qp = os.path.join(PROJ, q)
        im = None
        for b in STUFEN:
            z = os.path.join(HIER, 'assets/bild/kf_%s-%d.webp' % (n, b))
            if os.path.exists(z) and os.path.getmtime(z) > os.path.getmtime(qp):
                continue
            if im is None:
                im = ImageOps.exif_transpose(Image.open(qp)).convert('RGB')
            if im.width < b * .9 and b != STUFEN[0]:
                continue
            x = im.resize((b, round(im.height * b / im.width)), Image.LANCZOS) if im.width > b else im
            x.save(z, 'WEBP', quality=80, method=6)
            print('Foto', n, b)


def foto(n, sizes='50vw', cls='', pos='50% 50%', eager=False):
    st = [b for b in STUFEN if os.path.exists(os.path.join(HIER, 'assets/bild/kf_%s-%d.webp' % (n, b)))]
    return '<img class="%s" src="assets/bild/kf_%s-800.webp?v=%s" srcset="%s" sizes="%s" alt="%s" style="object-position:%s"%s decoding="async">' % (
        cls, n, VERSION, ', '.join('assets/bild/kf_%s-%d.webp?v=%s %dw' % (n, b, VERSION, b) for b in st), sizes, E(FOTO[n]), pos,
        ' fetchpriority="high"' if eager else ' loading="lazy"')


def titel(cls='gross'):
    return zl(['Alle Abende.'], 'h1', cls)


def satz(i=1, cls=''):
    return sw(SATZ, i=i, cls=cls)


F = []  # (Name, Inhalt)
# Dritte Runde (Robert 27.10.2026: «Es muss ein Hero sein, ein Hero. Und nicht ein Abschnitt.»):
# jede Fassung füllt den ersten Bildschirm randlos, das Bild trägt die Stimmung, der Titel liegt im Bild. Stand davor *.vor-hero-2026-10-27.


def held(cls, inner):
    return '<div class="kh %s">%s</div>' % (cls, inner)


def text(cls='', i=1):
    return '<div class="kh-text %s">%s%s</div>' % (cls, titel(), satz(i))


# 1 Randvoll: ein Bild über den ganzen Schirm, Anstossen bei Kerzen; es setzt sich beim Laden aus der Nähe in den Rahmen
F.append(('Randvoll', held('kh01', '<figure class="kh-bild kh-setzt auf">%s</figure><div class="kh-grund unten"></div>%s' % (
    foto('5376', '100vw', pos='50% 42%', eager=True), text('unten-links')))))

# 2 Überblende: fünf Momente eines Abends lösen einander über den ganzen Schirm ab, jeder kommt aus der Nähe
UEBER = [('3858', '50% 45%'), ('5022', '50% 45%'), ('3901', '50% 50%'), ('4108', '50% 50%'), ('3986', '50% 45%')]
F.append(('Überblende', held('kh02', '<div class="kh02-bilder">%s</div><div class="kh-grund mitte"></div>%s' % (
    ''.join('<figure class="kh-bild kh02-b%s">%s</figure>' % (' an' if i == 0 else '', foto(n, '100vw', pos=p, eager=i < 2)) for i, (n, p) in enumerate(UEBER)),
    text('mitte')))))

# 3 Geteilt: zwei Bilder Kante an Kante über die ganze Höhe, links das Glas, rechts die Tafel; der Titel steht über der Naht
F.append(('Geteilt', held('kh03', '<figure class="kh03-h l auf">%s</figure><figure class="kh03-h r auf">%s</figure><div class="kh-grund mitte"></div>%s' % (
    foto('4108', '50vw', pos='50% 50%', eager=True), foto('3901', '50vw', pos='50% 50%', eager=True), text('mitte')))))

# 4 Drei Bahnen: Ankommen, Anstossen, Bleiben als drei randlose Bahnen über die ganze Höhe; der Titel liegt unten über allen dreien
F.append(('Drei Bahnen', held('kh04', '%s<div class="kh-grund unten"></div>%s' % (
    ''.join('<figure class="kh04-b kh-setzt auf" style="--i:%d">%s<figcaption>%s</figcaption></figure>' % (i, foto(n, '34vw', pos=p, eager=True), w)
            for i, (n, p, w) in enumerate([('3887', '50% 50%', 'Ankommen'), ('5376', '50% 40%', 'Anstossen'), ('5022', '50% 45%', 'Bleiben')])),
    text('unten-links')))))

# 5 Das Licht geht an: der Raum liegt im Dunkeln, nach dem Laden gehen die Kerzen an
F.append(('Das Licht geht an', held('kh05', '<figure class="kh-bild kh05-bild auf"><span class="kh05-dunkel">%s</span><span class="kh05-hell">%s</span></figure><div class="kh-grund mitte"></div>%s' % (
    foto('3855', '100vw', pos='50% 50%', eager=True), foto('3855', '100vw', pos='50% 50%', eager=True), text('mitte')))))

# 6 Das Kinobild: der Schirm ist schwarz, in der Mitte ein Breitbild wie im Kino, das langsam schwenkt; der Titel steht im unteren Balken
F.append(('Das Kinobild', held('kh06', '<figure class="kh06-bild auf">%s</figure><div class="kh06-balken">%s%s</div>' % (
    foto('3986', '100vw', pos='50% 50%', eager=True), titel(), satz()))))

# 7 Davor: hinten die Bar im Dunkeln über den ganzen Schirm, davor der Titel riesig und vorne ein Bild vom Shaken, das beim Scrollen schneller steigt
F.append(('Davor', held('kh07', '<figure class="kh-bild kh07-hinten">%s</figure><p class="kh07-wort zl auf" aria-hidden="true"><span class="z"><span>Alle Abende.</span></span></p>'
                        '<figure class="kh07-vorn" data-zieh="vor">%s</figure><div class="kh07-text"><h1 class="vh">Alle Abende.</h1>%s</div>' % (
                            foto('5062', '100vw', pos='50% 50%', eager=True), foto('4568', '(max-width:860px) 60vw, 26vw', pos='50% 35%', eager=True), satz()))))

# 8 Hinein: der Flur zur Bar über den ganzen Schirm; beim Scrollen geht man auf die Tür zu
F.append(('Hinein', held('kh08', '<figure class="kh-bild kh08-bild" data-zieh="hinein">%s</figure><div class="kh-grund links"></div>%s' % (
    foto('3887', '100vw', pos='50% 55%', eager=True), text('links')))))

# 9 Der grosse Titel: Anstossen am Tisch der Bar über den ganzen Schirm, der Titel riesig in der Mitte; das Bild bleibt beim Scrollen zurück
F.append(('Der grosse Titel', held('kh09', '<figure class="kh-bild" data-zieh="zurueck">%s</figure><div class="kh-grund voll"></div>%s' % (
    foto('4574', '100vw', pos='50% 38%', eager=True), text('mitte riesig')))))

# 10 Die Lamellen: ein Bild über den ganzen Schirm in fünf senkrechten Streifen, die versetzt hereinkommen und sich schliessen
F.append(('Die Lamellen', held('kh10', '<figure class="kh10-bild auf" role="img" aria-label="%s">%s</figure><div class="kh-grund unten"></div>%s' % (
    E(FOTO['3859']), ''.join('<span class="kh10-l" style="--i:%d">%s</span>' % (i, foto('3859', '100vw', pos='50% 50%', eager=True)) for i in range(5)),
    text('unten-links')))))

# 11 Die Bildwand: acht Bilder vom Abend Kante an Kante über den ganzen Schirm, darüber der Titel
WAND = [('3858', '50% 40%'), ('4108', '50% 50%'), ('5376', '50% 40%'), ('3842', '50% 50%'), ('4004', '50% 50%'), ('5022', '50% 45%'), ('3916', '50% 55%'), ('3986', '50% 45%')]
F.append(('Die Bildwand', held('kh11', '<div class="kh11-wand">%s</div><div class="kh-grund voll stark"></div>%s' % (
    ''.join('<figure class="kh11-k kh-setzt auf" style="--i:%d">%s</figure>' % (i, foto(n, '(max-width:860px) 50vw, 25vw', pos=p, eager=True)) for i, (n, p) in enumerate(WAND)),
    text('mitte')))))

# 12 Es wird weit: das Bild steht zuerst als grosses Fenster in der Nacht, der Titel darauf; beim Scrollen wächst es bis an die Ränder
F.append(('Es wird weit', held('kh12', '<figure class="kh12-bild" data-zieh="weit">%s<div class="kh-grund mitte"></div></figure>%s' % (
    foto('5005', '100vw', pos='50% 42%', eager=True), text('mitte')))))

# 13 Senkrecht: der schmale Raum mit der Tafel über den ganzen Schirm, der Titel läuft senkrecht an der linken Kante hinauf
F.append(('Senkrecht', held('kh13', '<figure class="kh-bild kh-setzt auf">%s</figure><div class="kh-grund links"></div><h1 class="kh13-titel zl auf" aria-label="Alle Abende."><span class="z"><span>Alle Abende.</span></span></h1><div class="kh13-satz">%s</div>' % (
    foto('4004', '100vw', pos='50% 45%', eager=True), satz()))))

# 14 Die Kante: oben die Nacht mit «Alle», darunter die Bar von aussen bis an den unteren Rand, «Abende.» liegt im Bild
F.append(('Die Kante', held('kh14', '<div class="kh14-oben"><h1 class="kh14-titel zl auf" aria-label="Alle Abende."><span class="z"><span style="--i:0">Alle</span></span></h1>%s</div>'
                        '<figure class="kh14-bild" data-zieh="innen">%s<div class="kh-grund oben"></div><p class="kh14-zwei zl auf" aria-hidden="true"><span class="z"><span style="--i:1">Abende.</span></span></p></figure>' % (
                            satz(), foto('4093', '100vw', pos='50% 60%', eager=True)))))

# 15 Der Filmstreifen: hohe Bilder vom Abend Kante an Kante über die ganze Höhe, sie ziehen langsam seitwärts; der Titel steht still darüber
STREIFEN = [('3887', '50% 50%'), ('4108', '50% 50%'), ('5376', '50% 40%'), ('3842', '50% 50%'), ('64066', '50% 40%'), ('5022', '50% 45%'), ('3859', '50% 50%'), ('4004', '50% 50%')]
F.append(('Der Filmstreifen', held('kh15', '<div class="kh15-zug" aria-hidden="true">%s</div><div class="kh-grund voll"></div>%s' % (
    ''.join('<figure class="kh15-k">%s</figure>' % foto(n, '(max-width:860px) 60vw, 34vw', pos=p, eager=True) for n, p in STREIFEN * 2),
    text('mitte')))))


def main():
    fotos_machen()
    seite = open(os.path.join(HIER, 'abende.html')).read()
    m = re.search(r'<section class="seitenkopf plakatkopf" data-ton="schiefer">(.*?)</section>', seite, re.S)
    assert m, 'Kopf in abende.html nicht gefunden (erst bau.py laufen lassen)'
    teile = ['<div class="wv seitenkopf plakatkopf" data-n="0">%s</div>' % m.group(1)]
    teile += ['<div class="wv kwv kh-f%02d" data-n="%d" hidden>%s</div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = '<section class="kw wahl" data-ton="schiefer" id="kopf" data-name="Kopf">' + '<div class="wahl-marke"><b>Kopf</b><span data-nr></span></div>' + ''.join(teile) + '</section>'
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Titel, sechs Plakate in einer Reihe'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('kopf-wahl.css', 'kopf-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["kopf"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/kopf-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Kopf «Alle Abende» wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/kopf-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'abende-kopf-wahl.html'), 'w').write(seite)
    print('Seite abende-kopf-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
