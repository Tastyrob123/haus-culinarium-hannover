#!/usr/bin/env python3
"""Baustein in der Werkbank Culinarium (Werkbank-Chat 28.10.2026), über das Schäfli kopiert; die Herkunft steht darunter wie in der Vorlage.
Werkbank Landgasthof Ruedihus: die freigestellten Objekte für den Fuss «Alles auf einen Blick» (12.10.2026, Master 5b Punkt 23).

Eigen fürs Ruedihus: nichts ist erzeugt. Jedes Objekt ist aus den eigenen Stücken des Hauses gelegt, so wie sie in der Werkbank schon vorkommen:
die Geräte (Gehäuse aus Blender, übernommen) mit den echten Bildschirmen, die neu gesetzten Karten, Anhänger, Banderole, Zündholz-Etiketten,
Ansichtskarten, Untersetzer und das Prüfblatt mit dem Stempel. Der Schatten folgt der Form und steckt im Bild (Kit schatten.py).
python3 _werkbank/objekte_bau.py  → _werkbank/objekte/<weg>.png (1000 × 1000, durchsichtig); nach_bau() legt sie als WebP nach werkbank/eigen/."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
G, AN, AUS = os.path.join(W, 'geraete'), os.path.join(W, 'ansichten'), os.path.join(W, 'objekte')
sys.path.insert(0, os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit'))
import schatten  # noqa: E402

N = 1000
DUNKEL = (12, 11, 15)   # Schatten in der Nacht der Bar (#16151A, dunkler)


def offen(p):
    return Image.open(p if os.path.isabs(p) else os.path.join(ROOT, p)).convert('RGBA')


def decke(im, b, h, oben=True):
    """Bild auf b × h füllen (oben bündig oder mittig beschnitten)."""
    f = max(b / im.width, h / im.height)
    im = im.resize((max(b, round(im.width * f)), max(h, round(im.height * f))), Image.LANCZOS)
    x, y = (im.width - b) // 2, 0 if oben else (im.height - h) // 2
    return im.crop((x, y, x + b, y + h))


def laptop(schirm):
    L = json.load(open(os.path.join(G, 'laptop.json')))
    g = offen(os.path.join(G, 'laptop-geraet.png'))
    x, y, b, h = (round(v * (g.width if i % 2 == 0 else g.height)) for i, v in enumerate(L['schirm']))
    grund = Image.new('RGBA', g.size, (0, 0, 0, 0))
    grund.paste(decke(offen(schirm), b, h), (x, y))
    grund.alpha_composite(g)
    return grund


def handy(schirm):
    L = json.load(open(os.path.join(G, 'handy.json')))
    g = offen(os.path.join(G, 'handy-geraet.png'))       # bringt seinen Schatten schon mit
    x, y, b, h = (round(v * (g.width if i % 2 == 0 else g.height)) for i, v in enumerate(L['schirm']))
    s = decke(offen(schirm), b, h)
    m = Image.new('L', (b, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, b - 1, h - 1], radius=round(b * .1), fill=255)
    grund = Image.new('RGBA', g.size, (0, 0, 0, 0))
    grund.paste(s, (x, y), m)
    grund.alpha_composite(g)
    gx, gy, gb, gh = (v for v in L['gehaeuse'])
    return grund.crop((round(gx * g.width) - 6, round(gy * g.height) - 6, round((gx + gb) * g.width) + 6, round((gy + gh) * g.height) + 6))


def blatt(pfad, radius=0):
    im = offen(pfad)
    if radius:
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=radius, fill=255)
        im.putalpha(m)
    return im


def lege(stuecke, name):
    """stuecke: (Bild, Breite in px, Mitte x, Mitte y, Drehung, Schatten ja/nein). Später Genanntes liegt oben."""
    bild = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    for im, breite, cx, cy, grad, sch in stuecke:
        im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
        if grad:
            im = im.rotate(grad, expand=True, resample=Image.BICUBIC)
        if sch:
            im = schatten.backe(im, rand=.1, tiefe=.03, weich=.03, staerke=.6, farbe=DUNKEL)
        bild.alpha_composite(im, (round(cx - im.width / 2), round(cy - im.height / 2)))
    os.makedirs(AUS, exist_ok=True)
    bild.save(os.path.join(AUS, name + '.png'))
    return name


def pruefblatt():
    """Kleines Blatt «Prüfbericht» mit vier Zeilen und dem Stempel in Orange, gezeichnet (keine Schrift ausser den Linien)."""
    b, h = 560, 760
    im = Image.new('RGBA', (b, h), (250, 244, 244, 255)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([14, 14, b - 15, h - 15], radius=14, outline=(177, 173, 172, 255), width=2)
    d.rounded_rectangle([b / 2 - 90, 96, b / 2 + 90, 116], radius=8, fill=(58, 56, 69, 255))
    d.line([70, 160, b - 70, 160], fill=(58, 56, 69, 150), width=2)
    for i in range(4):
        y = 214 + i * 104
        d.rounded_rectangle([70, y, 250, y + 14], radius=6, fill=(58, 56, 69, 255))
        d.rounded_rectangle([70, y + 30, 380, y + 38], radius=4, fill=(58, 56, 69, 110)); d.rounded_rectangle([70, y + 48, 330, y + 56], radius=4, fill=(58, 56, 69, 110))
        d.rounded_rectangle([b - 122, y - 4, b - 70, y + 48], radius=12, fill=(22, 21, 26, 255))
        d.line([b - 108, y + 23, b - 98, y + 33, b - 84, y + 13], fill=(239, 118, 73, 255), width=5, joint='curve')
        d.line([70, y + 78, b - 70, y + 78], fill=(58, 56, 69, 80), width=1)
    m = Image.new('L', (b, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, b - 1, h - 1], radius=24, fill=255); im.putalpha(m)
    S = 4; r = 150
    st = Image.new('RGBA', (r * 2 * S, r * 2 * S), (0, 0, 0, 0)); ds = ImageDraw.Draw(st); rot = (239, 118, 73, 235)
    ds.ellipse([8 * S, 8 * S, (2 * r - 8) * S, (2 * r - 8) * S], outline=rot, width=7 * S)
    ds.ellipse([56 * S, 56 * S, (2 * r - 56) * S, (2 * r - 56) * S], outline=rot, width=3 * S)
    for k in range(40):   # gestrichelter Kranz, wo beim echten Stempel die Schrift läuft
        import math
        a0, a1 = math.radians(k * 9), math.radians(k * 9 + 5)
        ds.arc([30 * S, 30 * S, (2 * r - 30) * S, (2 * r - 30) * S], start=math.degrees(a0), end=math.degrees(a1), fill=rot, width=9 * S)
    ds.line([(r - 40) * S, (r + 2) * S, (r - 12) * S, (r + 30) * S, (r + 44) * S, (r - 32) * S], fill=rot, width=13 * S, joint='curve')
    st = st.resize((r * 2, r * 2), Image.LANCZOS)
    return im, st


def main():
    """Culinarium: Website und Gäste im Laptop, Werkzeuge im Laptop (Aufnahmen ansichten/Werkzeuge, sb_werkzeuge.js), Karten, Drucksachen, Untersetzer,
    Befund, Prüfblatt. Jedes Stück nur, wenn seine Bilder da sind (Lieferungen der Werkzeug-Chats kommen nach)."""
    R, H_, GA = os.path.join(AN, 'Rechner'), os.path.join(AN, 'Handy'), os.path.join(AN, 'Gaeste')
    D, U_, UN = 'drucksachen/img/', 'untersetzer/img/', 'unterlagen/img/'
    lap = lambda s: schatten.backe(laptop(s), rand=.06, tiefe=.02, weich=.03, staerke=.55, farbe=DUNKEL)
    liste = lambda o, pre='': sorted(f for f in os.listdir(os.path.join(ROOT, o)) if f.startswith(pre) and f.endswith('.webp') and not f.endswith('-r.webp')) if os.path.isdir(os.path.join(ROOT, o)) else []
    fertig = [lege([(lap(os.path.join(R, 'Startseite.jpg')), 980, 500, 520, 0, False)], 'website')]
    if os.path.exists(os.path.join(GA, 'buchen.jpg')):
        fertig.append(lege([(lap(os.path.join(GA, 'buchen.jpg')), 980, 500, 520, 0, False)], 'gaeste'))
    un = [f for f in liste('unterlagen/img', 'n-') if f.endswith('-01.webp')]
    if un:
        orte = {1: [(520, 500, 500, -2)], 2: [(360, 290, 500, -3), (360, 710, 500, 2)]}.get(len(un[:3]), [(300, 170, 500, -3), (300, 500, 500, 2), (300, 830, 500, -2)])   # nebeneinander, mittig, nichts überdeckt (Robert 29.10.2026)
        fertig.append(lege([(blatt(UN + f), b, x, y, r, True) for f, (b, x, y, r) in zip(un[:3], orte)], 'unterlagen'))
    dr = liste('drucksachen/img')
    if len(dr) >= 3:
        wahl = [f for f in ('karte.webp', 'ausgebucht.webp', 'dc-flyer.webp') if f in dr] or dr[:3]   # hell, dunkel, farbig: drei Stücke nebeneinander (Robert 29.10.2026)
        fertig.append(lege([(blatt(D + f), 300, x, 500, r, True) for f, (x, r) in zip(wahl, ((170, -3), (500, 2), (830, -2)))], 'drucksachen'))
    us = liste('untersetzer/img', 'u')
    if len(us) >= 4:
        fertig.append(lege([(blatt(U_ + us[0]), 400, 285, 285, -4, True), (blatt(U_ + us[1]), 400, 715, 285, 3, True), (blatt(U_ + us[2]), 400, 285, 715, 2, True),
                            (blatt(U_ + us[3]), 400, 715, 715, -3, True)], 'etiketten'))   # zwei mal zwei mit Abstand
        if len(dr) >= 2:
            fertig.append(lege([(blatt(D + dr[-1]), 300, 170, 500, -3, True), (blatt(U_ + us[-1]), 260, 500, 520, 0, True), (blatt(D + dr[-2]), 300, 830, 500, 2, True)], 'material'))   # nebeneinander
    if os.path.exists(os.path.join(ROOT, 'feed', 'feed.json')) and os.path.exists(os.path.join(AN, 'Strom', 'feed-rechner.jpg')):
        fertig.append(lege([(lap(os.path.join(AN, 'Strom', 'feed-rechner.jpg')), 980, 500, 520, 0, False)], 'feed'))
    WH = lambda n: os.path.join(AN, 'Werkzeuge-Handy', n + '.jpg')

    def mit_leiste(n):
        im = offen(WH(n)); o = round(im.height * .056)
        neu = Image.new('RGBA', im.size, im.getpixel((4, 4)))
        neu.paste(im.crop((0, 0, im.width, im.height - o)), (0, o))
        p = os.path.join(AN, 'Werkzeuge-Handy', '_' + n + '.png'); neu.save(p)
        return p
    for name in ('maison', 'bureau', 'carte', 'reception', 'livre', 'registre', 'imprimerie'):
        wr = os.path.join(AN, 'Werkzeuge', name + '.jpg')
        if os.path.exists(wr):
            fertig.append(lege([(lap(wr), 980, 500, 520, 0, False)], name))
    mb = os.path.join(AN, 'Strom', 'markenbuch-rechner.jpg')   # bis Le Livre liefert: das Markenbuch der Station 05
    if not os.path.exists(os.path.join(AN, 'Werkzeuge', 'livre.jpg')) and os.path.exists(mb):
        fertig.append(lege([(lap(mb), 980, 500, 520, 0, False)], 'livre'))
    an = os.path.join(AN, 'Strom', 'analyse-rechner.jpg')
    if os.path.exists(an):
        fertig.append(lege([(lap(an), 980, 500, 520, 0, False)], 'analyse-h'))
    # Robert 20.10.2026 zum Wegweiser: «da bitte mit PCs und so arbeiten», dann «Da überall mit PCs arbeiten»: jedes Gerät im Wegweiser ist ein Laptop, kein Handy
    gp_ = os.path.join(AN, 'Strom', 'geprueft-rechner.jpg')
    if os.path.exists(gp_):
        fertig.append(lege([(lap(gp_), 980, 500, 520, 0, False)], 'geprueft'))
    else:
        b, st = pruefblatt()
        fertig.append(lege([(b, 520, 500, 500, -5, True)], 'geprueft'))
    ah = os.path.join(AN, 'Strom', 'angebot-rechner.jpg')
    if os.path.exists(ah):
        fertig.append(lege([(lap(ah), 980, 500, 520, 0, False)], 'vorschlag'))
    print('Objekte:', ', '.join(fertig))


if __name__ == '__main__':
    main()
