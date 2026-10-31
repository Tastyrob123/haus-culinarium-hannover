#!/usr/bin/env python3
"""Culinarium Hannover · «So läuft ein Abend» in 15 Fassungen nach der Machart des Grand Beau-Rivage, direkt in der echten Startseite, 26.10.2026.
Robert nach vier abgelehnten Runden: «zu brav, kein Wow», Vorbild Grand Beau-Rivage. Dazu bleibt: passt zur Seite, alles auf einen Blick,
ein Teil, ein Bildschirm (Briefing 4.3), grosse Bilder dicht (Design-DNA «Dicht heisst edel»), keine Kicker-Zeile, keine Ziffernliste.
Machart vom Rivage: grosse Kacheln mit weichem Schatten, Namen in der Einkerbung, zweifarbige Überschrift aus dem Schlitz,
Fotowand mit Karte, Bildgruppe mit Tausch, Bilder steigen von unten und federn einmal. Farben und Schrift von Culinarium.
Baut ablauf-wahl-seite.html (Leiste unten, Pfeiltasten, ?ablauf=Nummer); Fassung 0 ist der heutige Stand.
Frühere Runden: _alt/ablauf_wahl.edel-2026-10-26.py, _alt/ablauf_wahl.kompakt-2026-10-26.py.
Aufruf: python3 website/bau.py && python3 website/ablauf_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION, knopf

HIER = bau.HIER

# Etikett (klein), Titel, Satz
S = [
    ('Zum Ankommen', 'Aperitif', 'Die Tafel ist gedeckt, die Kerzen brennen.'),
    ('Aus der Küche', 'Drei Gänge', 'Teller für Teller für die ganze Tafel.'),
    ('Von der Bar', 'Fünf Drinks', 'Von Momo, gemacht für genau dieses Essen.'),
    ('Am Tisch', 'Tasting und Schulung', 'Momo erklärt, was im Glas ist.'),
]
BILD = ['g2', 'r09', 'm7', 'kerze2']
POS = {'kerze2': '50% 35%', 'tafelleer': '50% 60%', 'momo': '50% 30%'}


def kopf(cls='', satz='Wer zum ersten Mal kommt, weiss nicht, was ihn erwartet. Ungefähr so:'):
    """Überschrift der Seite: rollt zeilenweise aus dem Schlitz, zweiter Teil in Kerze (wie «Zimmer & Suiten.» beim Rivage)."""
    return ('<div class="vk mitte kb-vk %s"><h2 class="zl auf titel eins" aria-label="So läuft ein Abend."><span class="z"><span style="--i:0">So läuft</span></span> '
            '<span class="z"><span style="--i:1"><em>ein Abend.</em></span></span></h2>%s</div>'
            % (cls, '<p class="sw auf vtext" style="--i:2">%s</p>' % E(satz) if satz else ''))


def bild(b, w=1000):
    pos = POS.get(b)
    return '<img src="assets/bild/%s-%d.webp?v=%s" alt="" loading="lazy" decoding="async"%s>' % (b, w, VERSION, ' style="object-position:%s"' % pos if pos else '')


def k(b, i=None, cls='', d=0, kerbe=True, satz=True, name=None, w=1000):
    """Kachel wie beim Rivage: randlos, rund, weicher Schatten; Name in der Einkerbung unten links."""
    cap = ''
    if kerbe and i is not None:
        cap = '<figcaption class="kb-kerbe"><b>%s</b>%s</figcaption>' % (E(name or S[i][1]), '<small>%s</small>' % E(S[i][2]) if satz else '')
    return '<figure class="foto kb-k %s" style="--d:%.2fs">%s%s</figure>' % (cls, d, bild(b, w), cap)


F = []  # (Name, Inhalt)

# 1 Einkerbung: vier grosse Kacheln dicht nebeneinander, Name und Satz in der ausgeschnittenen Ecke, steigen gestaffelt und federn
F.append(('Einkerbung', kopf() + '<div class="kb-01">%s</div>' % ''.join(k(BILD[i], i, d=i * .12) for i in range(4))))

# 2 Fotowand mit Karte (Rivage «Hochzeit»): Kacheln um eine dunkle Karte mit dem Ablauf und Punktlinien
LISTE = [('Aperitif', 'zum Ankommen'), ('Gänge', 'drei'), ('Signature Drinks', 'fünf'), ('Tasting', 'am Tisch')]
F.append(('Fotowand mit Karte', '<div class="kb-02">%s%s%s<div class="kb-02-karte"><h2 class="zl auf titel eins" aria-label="So läuft ein Abend."><span class="z"><span style="--i:0">So läuft</span></span> <span class="z"><span style="--i:1"><em>ein Abend.</em></span></span></h2><p class="kb-02-satz">Wer zum ersten Mal kommt, weiss nicht, was ihn erwartet. Ungefähr so:</p><dl class="kb-liste">%s</dl></div>%s%s</div>' % (
    k('g2', 0, 'a', 0, satz=False), k('r09', 1, 'b', .1, satz=False), k('m7', 2, 'c', .2, satz=False),
    ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (E(a), E(b)) for a, b in LISTE),
    k('tafelleer', None, 'd', .3, kerbe=False), k('kerze2', 3, 'e', .4, satz=False))))

# 3 3D-Kacheln (Rivage «Zimmer & Suiten»): vier grosse Kacheln, Name mittig darunter, feine Versalzeile, neigen sich leicht zur Maus
DETAIL = ['Die Tafel ist gedeckt', 'Teller für Teller', 'Von Momo', 'Am Tisch erklärt']
F.append(('3D-Kacheln', kopf() + '<div class="kb-03" data-kb-neigen>%s</div>' % ''.join(
    '<div class="kb-03-z">%s<h3 class="kb-name">%s</h3><p class="kb-zeile">%s</p></div>' % (k(BILD[i], None, d=i * .12, kerbe=False), E(S[i][1]), E(DETAIL[i])) for i in range(4))))

# 4 Am Fluss (Rivage «Restaurant»): grosses Bild mit Einkerbung und drei kleine darunter, rechts Titel, Satz und vier Karten
KARTE = [('Zum Ankommen', 'Aperitif'), ('Aus der Küche', '3 Gänge'), ('Von der Bar', '5 Drinks'), ('Am Tisch', 'Tasting')]
F.append(('Am Fluss', '<div class="kb-04"><div class="kb-04-l">%s<div class="kb-04-klein">%s%s%s</div></div><div class="kb-04-r">%s<div class="kb-04-karten">%s</div><div class="sw auf kb-04-kn" style="--i:4">%s</div></div></div>' % (
    k('tafelleer', 0, 'gross', 0, satz=False, name='An der langen Tafel', w=1600), k('g2', None, '', .12, kerbe=False), k('r09', None, '', .2, kerbe=False), k('m7', None, '', .28, kerbe=False),
    kopf('links', 'Vierzehn Gäste an einer Tafel. Erst ein Aperitif, dann drei Gänge aus der Küche und fünf Drinks von Momo, die er am Tisch erklärt.'),
    ''.join('<div class="sw auf" style="--i:%d"><span>%s</span><b>%s</b></div>' % (i + 2, E(a), E(b)) for i, (a, b) in enumerate(KARTE)), knopf('Der Abend', 'abend.html'))))

# 5 Kino: ein Bild über die ganze Breite, das langsam heranfährt und in das nächste übergeht; die vier Schritte stehen darunter, eine Linie läuft mit
KINO = [('tablett', '50% 55%', 1000), ('pass4', '50% 50%', 1600), ('m1', '50% 55%', 1600), ('t09', '50% 45%', 1000)]
F.append(('Kino', kopf(satz='') + '<div class="kb-05" data-kb-kino><div class="kb-05-bild">%s</div><div class="kb-05-r">%s</div></div>' % (
    ''.join('<img%s src="assets/bild/%s-%d.webp?v=%s" alt="" loading="lazy" style="object-position:%s">' % (' class="an"' if i == 0 else '', b, w, VERSION, p) for i, (b, p, w) in enumerate(KINO)),
    ''.join('<button type="button"%s data-i="%d"><span class="kb-05-l"><i></i></span><b>%s</b><small>%s</small></button>' % (' class="an"' if i == 0 else '', i, E(S[i][1]), E(S[i][2])) for i in range(4)))))

# 6 Abzüge auf der Bühne: die Tafel gross in der Mitte, vier Abzüge landen nacheinander von unten auf ihren Rändern
F.append(('Abzüge auf der Bühne', kopf() + '<div class="kb-06">%s%s</div>' % (
    k('t02', None, 'mitte', 0, kerbe=False), ''.join('<figure class="kb-abzug a%d" style="--d:%.2fs"><div class="kb-abzug-b">%s</div><figcaption>%s</figcaption></figure>' % (
        i, .5 + i * .22, bild(BILD[i], 640), E(S[i][1])) for i in range(4)))))

# 7 Auffächern: die vier Kacheln kommen als Stapel und legen sich auseinander in ihre Reihe
F.append(('Auffächern', kopf() + '<div class="kb-07">%s</div>' % ''.join(k(BILD[i], i, 'f%d' % i, 0) for i in range(4))))

# 8 Anstossen: zwei Paare, Glas und Teller, kommen von beiden Seiten und stossen an der Naht an
F.append(('Anstossen', kopf() + '<div class="kb-08"><div class="kb-08-p">%s%s</div><div class="kb-08-p">%s%s</div></div>' % (
    k(BILD[0], 0, 'l', 0), k(BILD[1], 1, 'r', .1), k(BILD[2], 2, 'l', .2), k(BILD[3], 3, 'r', .3))))

# 9 Ziegelverband: vier Bilder im Verband, breit und schmal im Wechsel, links der Titel
F.append(('Ziegelverband', '<div class="kb-09">%s<div class="kb-09-r">%s%s%s%s</div></div>' % (
    kopf('links'), k('tafelleer', 0, 'br', 0, w=1600), k('r09', 1, 'sm', .1), k('m7', 2, 'sm', .2), k('kerze2', 3, 'br', .3))))

# 10 Satz an der Naht: vier Bilder Wand an Wand, an ihrer unteren Kante läuft der Ablauf als Satz durch (Laufband, Briefing 6.9)
NAHT = 'Zur Begrüssung ein Aperitif <i>×</i> drei Gänge aus der Küche <i>×</i> fünf Drinks von Momo <i>×</i> Tasting und Schulung am Tisch <i>×</i> '
F.append(('Satz an der Naht', kopf() + '<div class="kb-10"><div class="kb-10-r">%s</div><div class="kb-10-band" aria-label="Aperitif, drei Gänge, fünf Drinks, Tasting und Schulung"><div class="kb-10-zug"><span>%s</span><span aria-hidden="true">%s</span></div></div></div>' % (
    ''.join(k(BILD[i], i, '', i * .1, satz=False) for i in range(4)), NAHT * 2, NAHT * 2)))

# 11 Der Fächer: vier Karten wie eine aufgefächerte Menükarte, leicht übereinander, Name auf hellem Rand
F.append(('Der Fächer', kopf() + '<div class="kb-11">%s</div>' % ''.join(
    '<figure class="kb-blatt b%d" style="--d:%.2fs"><div class="kb-blatt-b">%s</div><figcaption><b>%s</b><small>%s</small></figcaption></figure>' % (
        i, i * .1, bild(BILD[i]), E(S[i][1]), E(S[i][2])) for i in range(4))))

# 12 Bildgruppe mit Tausch (Rivage-Baustein 6.5): ein grosses Bild mit Einkerbung, drei quer daneben; ein Klick holt ein kleines an die grosse Stelle
F.append(('Bildgruppe mit Tausch', '<div class="kb-12" data-kb-gruppe><div class="kb-12-l">%s</div><div class="kb-12-r">%s</div></div>' % (
    kopf('links', 'Ein Aperitif, drei Gänge, fünf Drinks und am Ende ein Tasting. Ein Bild antippen, und es kommt nach vorn.'),
    ''.join('<button type="button" class="kb-12-p" data-platz="%d" data-i="%d" aria-label="%s">%s</button>' % (i, i, E(S[i][1]), k(BILD[i], i, '', i * .1)) for i in range(4)))))

# 13 Lichter an: die vier Kacheln liegen im Dunkeln und gehen nacheinander an wie Kerzen auf der Tafel
F.append(('Lichter an', kopf() + '<div class="kb-13">%s</div>' % ''.join(
    '<div class="kb-13-z" style="--l:%.2fs">%s<span class="kb-13-dunkel"></span></div>' % (.5 + i * .5, k(BILD[i], i, '', 0)) for i in range(4))))

# 14 Die gebogene Wand: vier hohe Kacheln stehen im Bogen um den Betrachter, wie Plätze um die Tafel
F.append(('Die gebogene Wand', kopf() + '<div class="kb-14">%s</div>' % ''.join(
    '<div class="kb-14-z w%d">%s</div>' % (i, k(BILD[i], i, '', i * .1)) for i in range(4))))

# 15 Löcher in der Wand: die Wand der Bar mit vier Öffnungen, dahinter der Abend; die Bilder gleiten beim Scrollen hinter den Öffnungen
F.append(('Löcher in der Wand', kopf() + '<div class="kb-15">%s</div>' % ''.join(
    '<div class="kb-15-z"><div class="kb-15-loch l%d">%s</div><h3 class="kb-name">%s</h3><p class="kb-zeile">%s</p></div>' % (
        i, bild(BILD[i]), E(S[i][1]), E(S[i][2])) for i in range(4))))


def main():
    seite = open(os.path.join(HIER, 'index.html')).read()
    m = re.search(r'(<section class="vab v-ablauf[^"]*"[^>]*id="ablauf"[^>]*>)(<div class="vi h-ablauf">.*?)(<p class="ueber[^>]*>.*?</p></section>)', seite, re.S)
    assert m, 'Teil «So läuft ein Abend» in index.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab v-ablauf', 'data-name="So läuft ein Abend" class="vab v-ablauf wahl', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    # .auf: die Fotos steigen wie überall auf der Seite von unten in ihren Platz (Seiten-CSS .foto / .da)
    teile += ['<div class="wv kb kb-f%02d" data-n="%d" hidden><div class="auf kb-buehne">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>So läuft ein Abend</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Treppe aus vier Karten'] + [n for n, _x in F]
    v = VERSION + 'r%d' % os.path.getmtime(os.path.join(HIER, 'assets', 'ablauf-wahl.css'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["ablauf"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/ablauf-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Ablauf wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/ablauf-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'ablauf-wahl-seite.html'), 'w').write(seite)
    print('Seite ablauf-wahl-seite.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
