#!/usr/bin/env python3
"""Culinarium Hannover · «So läuft ein Abend» in 15 edlen Fassungen, direkt in der echten Startseite, 26.10.2026.
Robert: «15 versionen luxuriös elegant und edel wie für ein luxushotel» und «direkt in der seite auswählbar, nicht in so dummen rahmen».
Baut ablauf-wahl-seite.html: die echte Startseite, der Teil «So läuft ein Abend» umschaltbar (Leiste unten, Pfeiltasten, ?ablauf=Nummer).
Fassung 0 ist der heutige Stand. Nur transform und opacity, nativer Scroll.
Aufruf: python3 website/bau.py && python3 website/ablauf_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION

HIER = bau.HIER

# Die vier Schritte: Etikett, Titel, Satz, kurzer Satz
S = [
    ('Der Empfang', 'Ankommen', 'Zum Ankommen gibt es einen Aperitif. Die Tafel ist gedeckt, die Kerzen brennen.', 'Ein Aperitif, die Kerzen brennen.'),
    ('Aus der Küche', 'Drei Gänge', 'Aus der Küche kommen drei Gänge, Teller für Teller für die ganze Tafel. Das Menü wechselt mit jedem Abend.', 'Teller für Teller für die ganze Tafel.'),
    ('Von der Bar', 'Fünf Drinks', 'Zu den Gängen kommen fünf Signature Drinks von Momo, gemacht für genau dieses Essen.', 'Von Momo, gemacht für dieses Essen.'),
    ('Am Tisch', 'Tasting und Schulung', 'Momo erklärt jeden Drink am Tisch, damit man die Aromen nicht nur schmeckt, sondern auch versteht.', 'Jeder Drink wird am Tisch erklärt.'),
]
EINL = 'Wer zum ersten Mal kommt, weiss nicht, was ihn erwartet. Ungefähr so: ankommen, anstossen, essen, probieren, zuhören, und am Ende mit Leuten am Tisch sitzen, die man vorher nicht kannte.'
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8h12M9 3l5 5-5 5"/></svg>'
PZ = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M14 8H2M7 3L2 8l5 5"/></svg>'


def b(k, cls='', pos=None, w=1000):
    """Foto in voller Grösse; sichtbar von Anfang an (Master 4)."""
    return '<div class="ae-b %s"><img src="assets/bild/%s-%d.webp?v=%s" alt="" loading="lazy" decoding="async"%s></div>' % (
        cls, k, w, VERSION, ' style="object-position:%s"' % pos if pos else '')


def lab(t, cls=''):
    return '<span class="ae-lab %s">%s</span>' % (cls, E(t))


def kopf(cls='mitte', titel='So läuft ein Abend.', satz=EINL):
    return ('<div class="ae-kopf %s">%s<span class="ae-strich"></span><h2 class="ae-t ae-h">%s</h2><p class="ae-sz">%s</p></div>'
            % (cls, lab('Der Abend'), E(titel), E(satz)))


def txt(i, lang=True, cls=''):
    l, t, s, k = S[i]
    return '<div class="ae-txt %s">%s<span class="ae-strich"></span><h3 class="ae-t">%s</h3><p class="ae-sz">%s</p></div>' % (cls, lab(l), E(t), E(s if lang else k))


F = []  # (Name, Inhalt)

# 1 Doppelseite: je Schritt eine Seite wie im Bildband, die Seiten wechseln von links nach rechts
W1 = [('g2', 'tafelleer'), ('r09', 'm8'), ('m7', 'd3'), ('kerze2', 'schaum')]
F.append(('Doppelseite', kopf() + '<div class="ae-dp">' + ''.join(
    '<div class="ae-dp-s">%s<div class="ae-dp-r">%s%s</div></div>' % (b(g, 'ae-dp-g'), b(k), txt(i)) for i, (g, k) in enumerate(W1)) + '</div>'))

# 2 Arkaden: vier hohe Bögen mit feiner Innenlinie
F.append(('Arkaden', kopf() + '<div class="ae-ak auf">' + ''.join(
    '<div class="ae-ak-st">%s%s</div>' % (b(k, 'ae-ak-b'), txt(i, False, 'mitte')) for i, k in enumerate(['g2', 'r09', 'm7', 'kerze2'])) + '</div>'))

# 3 Vier Paneele: Bildbahnen über die volle Breite, Überfahren zieht die Goldlinie auf
F.append(('Vier Paneele', kopf() + '<div class="ae-pn">' + ''.join(
    '<div class="ae-pn-p">%s<div class="ae-pn-dim"></div>%s<div class="ae-pn-u"><h3 class="ae-t">%s</h3><span class="ae-pn-l"></span><p class="ae-sz">%s</p></div></div>'
    % (b(k), lab(S[i][0], 'ae-pn-o'), E(S[i][1]), E(S[i][2])) for i, k in enumerate(['tafelleer', 'anrichten', 'm7', 'kerze2'])) + '</div>'))

# 4 Die Einladung: breites Bild der Tafel, darauf eine Karte in Elfenbein
F.append(('Die Einladung', '<div class="ae-ei auf">%s<div class="ae-ei-k"><p class="ae-ei-kopf">%s</p><h2 class="ae-t ae-h ae-ei-h">So läuft ein Abend.</h2><div class="ae-ei-r">%s</div></div></div>' % (
    b('tafelleer', 'ae-ei-b', '50% 58%', 1600), lab('Ein Abend im Culinarium'),
    ''.join('<div><h3 class="ae-t">%s</h3><p>%s</p></div>' % (E(t), E(s)) for _l, t, s, _k in S))))

# 5 Galerie: ein Bild über die ganze Breite, langsames Überblenden, dunkle Tafel mit dem Schritt
G5 = [('tafelleer', '50% 60%', 1600), ('pass4', '50% 50%', 1600), ('m1', '50% 55%', 1600), ('t09', '50% 45%', 1000)]
F.append(('Galerie', kopf() + '<div class="ae-ga" data-ae-galerie><div class="ae-ga-bild">%s</div><div class="ae-ga-t">%s</div><div class="ae-ga-st"><span class="ae-ga-lauf"><i></i></span><button class="ae-pf" data-r="-1" aria-label="Zurück">%s</button><button class="ae-pf" data-r="1" aria-label="Weiter">%s</button></div></div>' % (
    ''.join('<img%s src="assets/bild/%s-%d.webp?v=%s" alt="" loading="lazy" style="object-position:%s">' % (' class="an"' if i == 0 else '', k, w, VERSION, p) for i, (k, p, w) in enumerate(G5)),
    ''.join('<div%s>%s</div>' % (' class="an"' if i == 0 else '', txt(i)) for i in range(4)), PZ, PF)))

# 6 Triptychon: Mitte gross, Nachbarn klein und gedämpft
W6 = ['g2', 'r09', 'm7', 'kerze2']
F.append(('Triptychon', kopf() + '<div class="ae-tp" data-ae-trip><div class="ae-tp-spur">%s</div><button class="ae-pf ae-tp-z" data-r="-1" aria-label="Zurück">%s</button><button class="ae-pf ae-tp-v" data-r="1" aria-label="Weiter">%s</button></div>' % (
    ''.join('<div class="ae-tp-st">%s%s</div>' % (b(W6[j]), txt(j, False, 'mitte')) for j in (3, 0, 1, 2, 3, 0)), PZ, PF)))

# 7 Übereinander: Vollbilder, das nächste gleitet über das stehende
W7 = [('tablett', None), ('r09', None), ('m7', None), ('kerze2', '50% 40%')]
F.append(('Übereinander', kopf() + '<div class="ae-ub">' + ''.join(
    '<div class="ae-ub-p">%s%s</div>' % (b(k, '', p, 1000), txt(i, True, 'mitte ae-ub-t')) for i, (k, p) in enumerate(W7)) + '</div>'))

# 8 Medaillons: ovale Bilder mit doppelter Fassung
F.append(('Medaillons', kopf() + '<div class="ae-md auf">' + ''.join(
    '<div>%s%s</div>' % (b(k, 'ae-md-o'), txt(i, False, 'mitte')) for i, k in enumerate(['g2', 'roq1', 'glas', 'momo'])) + '</div>'))

# 9 Die Liste: Schritte gross zwischen Haarlinien, Bild in voller Höhe daneben
F.append(('Die Liste', '<div class="ae-ls" data-ae-liste><div class="ae-ls-l">%s<span class="ae-strich"></span><h2 class="ae-t ae-h">So läuft ein Abend.</h2><div class="ae-ls-z">%s</div><p class="ae-sz ae-ls-s">%s</p></div><div class="ae-ls-bild">%s</div></div>' % (
    lab('Der Abend'),
    ''.join('<button type="button"%s data-i="%d">%s<span class="ae-t">%s</span></button>' % (' class="an"' if i == 0 else '', i, lab(l), E(t)) for i, (l, t, _s, _k) in enumerate(S)),
    E(S[0][2]), ''.join('<img%s src="assets/bild/%s-1000.webp?v=%s" alt="" loading="lazy">' % (' class="an"' if i == 0 else '', k, VERSION) for i, k in enumerate(['tablett', 'r09', 'd3', 'kerze2'])))))

# 10 Bild und Detail: grosses Bild, kleines Detail greift über die Ecke und läuft leicht gegen
W10 = [('tafelleer', 'g2'), ('anrichten', 'r09'), ('m7', 'g1'), ('kerze2', 'schaum')]
F.append(('Bild und Detail', kopf() + '<div class="ae-bd">' + ''.join(
    '<div class="ae-bd-z">%s%s%s</div>' % (b(g, 'ae-bd-g'), b(k, 'ae-bd-k'), txt(i)) for i, (g, k) in enumerate(W10)) + '</div>'))

# 11 Promenade: seitwärts durch vier grosse Hochformate, Goldlinie zeigt den Weg
F.append(('Promenade', '<div class="ae-pr-w"><div class="ae-pr" data-ae-prom><div class="ae-pr-i">%s<span class="ae-strich"></span><h2 class="ae-t ae-h">So läuft ein Abend.</h2><p class="ae-sz">Wer zum ersten Mal kommt, weiss nicht, was ihn erwartet. Ungefähr so.</p></div>%s</div><div class="ae-pr-f"><i></i></div><div class="ae-pr-st"><button class="ae-pf" data-r="-1" aria-label="Zurück">%s</button><button class="ae-pf" data-r="1" aria-label="Weiter">%s</button></div></div>' % (
    lab('Der Abend'), ''.join('<div class="ae-pr-k">%s%s</div>' % (b(k), txt(i, False)) for i, k in enumerate(['g2', 'r09', 'm7', 'kerze2'])), PZ, PF)))

# 12 Passepartout: vier Fotos in Elfenbein-Rahmen, gehängt wie in einer Galerie
F.append(('Passepartout', kopf() + '<div class="ae-pp">' + ''.join(
    '<div><div class="ae-pp-r">%s</div>%s</div>' % (b(k), txt(i, False, 'mitte')) for i, k in enumerate(['g2', 'r01', 'glas', 'momo'])) + '</div>'))

# 13 Geteilt: links steht der Schritt, rechts ziehen seine Bilder vorbei
W13 = [('tafelleer', 'g2'), ('r09', 'anrichten'), ('m7', 'd3'), ('kerze2', 'schaum')]
F.append(('Geteilt', kopf() + '<div class="ae-gt" data-ae-geteilt><div class="ae-gt-l"><div class="ae-gt-st">%s</div></div><div class="ae-gt-r">%s</div></div>' % (
    ''.join('<div%s>%s</div>' % (' class="an"' if i == 0 else '', txt(i)) for i in range(4)),
    ''.join('<div class="ae-gt-g" data-i="%d">%s%s</div>' % (i, b(g), b(k, 'schmal')) for i, (g, k) in enumerate(W13)))))

# 14 Register: Reiter mit gleitender Goldlinie, grosses Bild, Text und Detail
W14 = [('tafelleer', 'g2'), ('anrichten', 'r09'), ('m1', 'm7'), ('kerze2', 'schaum')]
F.append(('Register', kopf() + '<div class="ae-rg" data-ae-reg><div class="ae-rg-r">%s<span class="ae-rg-s"></span></div><div class="ae-rg-k"><div class="ae-rg-b">%s</div><div class="ae-rg-re"><div class="ae-rg-t">%s</div><div class="ae-rg-d">%s</div></div></div></div>' % (
    ''.join('<button type="button"%s data-i="%d"><span class="ae-t">%s</span></button>' % (' class="an"' if i == 0 else '', i, E(t)) for i, (_l, t, _s, _k) in enumerate(S)),
    ''.join('<img%s src="assets/bild/%s-1000.webp?v=%s" alt="" loading="lazy">' % (' class="an"' if i == 0 else '', g, VERSION) for i, (g, _k) in enumerate(W14)),
    ''.join('<div%s>%s</div>' % (' class="an"' if i == 0 else '', txt(i)) for i in range(4)),
    ''.join('<img%s src="assets/bild/%s-1000.webp?v=%s" alt="" loading="lazy">' % (' class="an"' if i == 0 else '', k, VERSION) for i, (_g, k) in enumerate(W14)))))

# 15 Die Kolumne: wie ein Artikel im Reisemagazin, Initiale in Gold
ko = '<div class="ae-ko"><div class="ae-ko-kopf">%s<span class="ae-strich"></span><h2 class="ae-t ae-h">So läuft ein Abend.</h2><p class="ae-sz ae-ko-ini">%s</p></div>' % (lab('Der Abend'), E(EINL))
for i, bild in enumerate([b('tafelleer', 'ae-ko-b', '50% 60%', 1600), b('pass4', 'ae-ko-b', None, 1600), '<div class="ae-ko-paar">%s%s</div>' % (b('m7'), b('d3')), b('kerze2', 'ae-ko-b', '50% 38%')]):
    ko += bild + txt(i, True, 'mitte ae-ko-t')
F.append(('Die Kolumne', ko + '</div>'))


def main():
    seite = open(os.path.join(HIER, 'index.html')).read()
    m = re.search(r'(<section class="vab v-ablauf[^"]*"[^>]*id="ablauf"[^>]*>)(<div class="vi h-ablauf">.*?)(<p class="ueber[^>]*>.*?</p></section>)', seite, re.S)
    assert m, 'Teil «So läuft ein Abend» in index.html nicht gefunden (erst bau.py laufen lassen)'
    kopf_tag = m.group(1).replace('class="vab v-ablauf', 'class="vab v-ablauf wahl', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv ae ae-%02d" data-n="%d" hidden>%s</div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>So läuft ein Abend</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: vier Karten'] + [n for n, _x in F]
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["ablauf"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/ablauf-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, VERSION)
    seite = seite.replace('<title>', '<title>Ablauf wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/ablauf-wahl.css?v=%s">\n</head>' % (VERSION, VERSION), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'ablauf-wahl-seite.html'), 'w').write(seite)
    print('Seite ablauf-wahl-seite.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
