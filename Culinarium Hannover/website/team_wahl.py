#!/usr/bin/env python3
"""Culinarium Hannover · «Drei Leute, ein Haus.» in 15 Fassungen, direkt in der echten Teamseite, 27.10.2026.
Robert: «15 verschiedene visuelle Alternativen … ohne dass wir so krass ins Detail gehen über diese ganzen Leute … Sonst gehen wir auf die 3 notfalls».
Der Abspann mit Rollen und Namen ist abgelehnt (Stand: varianten.py.abspann-abgelehnt-2026-10-27). Jede Fassung zeigt die Mannschaft hinter den drei
nur im Bild: Gruppenfoto (dc_team, dn_team), Hände, Pass, Service, Theke, Film. Keine Namen ausser Derya, Momo und Rudi.
Ein bewegter Moment je Fassung, nur transform und opacity, nativer Scroll; Hereinkommendes ist von Anfang an sichtbar.
Baut team-wahl.html (Leiste unten, Pfeiltasten, ?team=Nummer); Fassung 0 ist der heutige Stand.
Aufruf: python3 website/varianten.py && python3 website/team_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, VERSION

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets/bild/meta.json')))

# Rund, Hochformat, Rolle, Name, Satz (Satz wie auf der Seite heute, gekürzt)
P = [('kopf_derya', 'w3', 'Führt die Bar', 'Derya Ivkin', 'Führt das Walk on the Wild Side seit dem Reopening im November 2023.'),
     ('kopf_momo', 'momo_hoch', 'Mixt die Drinks', 'Momo', 'Mixt die fünf Drinks eines Abends und erklärt jeden selbst.'),
     ('kopf_rudi', 'w4', 'Kocht die Gänge', 'Rudi Napieraj', 'Kocht seit 2024 die drei Gänge an der langen Tafel.')]
POS = {'w3': '50% 30%', 'momo_hoch': '50% 25%', 'w4': '50% 30%', 'dn_team': '50% 52%', 'dc_team': '50% 45%', 'trio2': '50% 40%',
       'pass2': '50% 12%', 'w2': '50% 25%', 'theke': '50% 35%', 'kueche': '50% 30%', 'w6': '50% 30%', 'service': '50% 35%'}
# Gesichter im Gruppenfoto dc_team (x %, y %), am Bild abgelesen 27.10.2026: Derya mit Brille, Momo mit Bart, Rudi mit Mütze
GESICHT = [(83, 39), (75.5, 36.5), (65, 40)]
SATZ = 'Drei, die man kennt. Und eine ganze Mannschaft, die mit anpackt.'
HAENDE = ['m7', 'klaeren', 'm2', 'pass3', 'm8', 'm6']
ARBEIT = ['pass2', 'w2', 'theke', 'kueche', 'w6', 'm7']


def bild(k, w=1000, cls='', alt='', pos=None):
    st = [s for s in META[k]['stufen'] if s <= w] or META[k]['stufen'][:1]
    return '<img class="%s" src="assets/bild/%s-%d.webp?v=%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        cls, k, st[-1], VERSION, E(alt or bau.BILD[k][2]), pos or POS.get(k, '50% 50%'))


def kopf(satz=SATZ, cls='mitte', titel=('Drei Leute,', 'ein Haus.')):
    return '<div class="vk %s">%s%s</div>' % (cls, bau.zl(list(titel), 'h2', 'titel'), bau.sw(E(satz), 'p', 'vtext', 1) if satz else '')


def rund(k, cls='tw-rund'):
    return '<span class="%s">%s</span>' % (cls, bild(k, 640))


def mini(i, cls='tw-mini'):
    """Kleine Visitenkarte: rundes Bild, Rolle, Name."""
    r, _h, was, name, _s = P[i]
    return '<div class="%s sw auf" style="--i:%d">%s<p class="mono">%s</p><h3>%s</h3></div>' % (cls, i, rund(r), E(was), E(name))


def karte(i, cls='kp sw auf'):
    r, _h, was, name, satz = P[i]
    return '<article class="%s" style="--i:%d"><div class="kp-bild">%s</div><p class="kp-was mono">%s</p><h3 class="kp-name">%s</h3><p class="kp-text">%s</p></article>' % (
        cls, i, bild(r, 640), E(was), E(name), E(satz))


F = []  # (Name, Inhalt)

# 1 Vor der Mannschaft: die ganze Mannschaft breit an der Theke, die drei Karten stehen vorn an der Bildkante wie vor dem Tresen
F.append(('Vor der Mannschaft', '<div class="tw-01">%s<figure class="tw-01-bild auf">%s</figure><div class="tw-01-reihe">%s</div></div>' % (
    kopf(), bild('dn_team', 1600), ''.join(mini(i, 'tw-mini tw-01-k') for i in range(3)))))

# 2 Drei Leute | ein Haus: der Titel wörtlich als Bildpaar, links die drei vor der Bar, rechts die Mannschaft; Naht in Kerze, die Bilder stossen an
F.append(('Drei Leute, ein Haus', '<div class="tw-02"><div class="tw-02-paar">'
          '<figure class="tw-02-l auf">%s<figcaption><span class="zl auf"><span class="z"><span>Drei Leute,</span></span></span><small>Derya, Momo und Rudi</small></figcaption></figure>'
          '<figure class="tw-02-r auf">%s<figcaption><span class="zl auf"><span class="z"><span style="--i:1">ein Haus.</span></span></span><small>und alle, die mit anpacken</small></figcaption></figure>'
          '</div></div>' % (bild('trio2', 1600), bild('dc_team', 1000))))

# 3 Zoom zurück: das Gruppenfoto beginnt ganz nah bei den drei und zieht beim Scrollen auf, bis die ganze Mannschaft im Bild steht
ox, oy = GESICHT[1]
F.append(('Zoom zurück', '<div class="tw-03">%s<figure class="tw-03-bild auf" data-tw-zoom style="--ox:%.1f%%;--oy:%.1f%%">%s</figure></div>' % (
    '<div class="tw-03-l">%s<div class="tw-03-liste">%s</div></div>' % (kopf(cls='', satz='Erst die drei. Dann alle, die dazugehören.'), ''.join(mini(i, 'tw-mini tw-zeile') for i in range(3))),
    ox, oy, bild('dc_team', 1000))))

# 4 Licht an: im Gruppenfoto brennt zuerst nur über den drei Gesichtern Licht, dann geht es für die ganze Mannschaft an
loecher = ', '.join('radial-gradient(circle at %.1f%% %.1f%%, transparent 0 4.6%%, #000 7.6%%)' % g for g in GESICHT)
F.append(('Licht an', '<div class="tw-04">%s<figure class="tw-04-bild auf">%s<span class="tw-04-dunkel" style="-webkit-mask-image:%s;mask-image:%s"></span></figure>'
          '<div class="tw-04-namen">%s</div></div>' % (
              kopf(satz='Erst brennt das Licht über den dreien, dann für alle.'), bild('dc_team', 1000), loecher, loecher,
              ''.join('<p class="sw auf" style="--i:%d"><span class="mono">%s</span>%s</p>' % (i, E(p[2]), E(p[3])) for i, p in enumerate(P)))))

# 5 Gesichter und Hände: oben die drei Gesichter, darunter ein Band aus Händen bei der Arbeit, ohne Gesicht, ohne Namen
F.append(('Gesichter und Hände', '<div class="tw-05">%s<div class="tw-05-reihe">%s</div><div class="tw-05-band auf">%s</div></div>' % (
    kopf(satz='', titel=('Drei Gesichter,', 'viele Hände.')), ''.join(mini(i, 'tw-mini tw-gross') for i in range(3)),
    ''.join('<figure style="--i:%d">%s</figure>' % (n, bild(k, 640)) for n, k in enumerate(HAENDE)))))

# 6 Filmstreifen: ein Streifen mit Perforation, vorn die drei Köpfe, dahinter Bild für Bild die Mannschaft; der Streifen läuft beim Scrollen weiter
F.append(('Filmstreifen', '<div class="tw-06">%s<div class="tw-06-streifen auf" data-tw-lauf><div class="tw-06-bahn">%s%s</div></div></div>' % (
    kopf(),
    ''.join('<figure class="tw-06-k">%s<figcaption>%s</figcaption></figure>' % (bild(p[0], 640), E(p[3])) for p in P),
    ''.join('<figure class="tw-06-k">%s</figure>' % bild(k, 640) for k in ['dc_team'] + ARBEIT))))

# 7 Das Plakat: wie die Plakate der Abende, die drei Namen gross mit dem x, darunter klein die Mannschaft; das Gruppenfoto ist das Motiv
F.append(('Das Plakat', '<div class="tw-07"><div class="tw-07-plakat auf"><p class="tw-07-oben">A unique experience by</p>'
          '<h2 class="tw-07-h">Derya <i>×</i> Momo <i>×</i> Rudi</h2><figure>%s</figure>'
          '<p class="tw-07-unten">und die ganze Mannschaft des Walk on the Wild Side</p></div>'
          '<div class="tw-07-r">%s<div class="tw-07-liste">%s</div></div></div>' % (
              bild('dc_team', 1000), kopf(cls='', satz='Auf dem Plakat stehen drei Namen. Am Abend stehen alle da.'),
              ''.join(mini(i, 'tw-mini tw-zeile') for i in range(3)))))

# 8 Mittendrin: eine Wand aus Bildern der Mannschaft bei der Arbeit, drei Felder davon sind die drei, in Kerze gerahmt
WAND = ['pass2', 'kopf_derya', 'w2', 'theke', 'm7', 'kopf_momo', 'kueche', 'w6', 'klaeren', 'kopf_rudi', 'm2', 'service']
F.append(('Mittendrin', '<div class="tw-08">%s<div class="tw-08-wand auf">%s</div><p class="tw-08-satz sw auf">%s</p></div>' % (
    kopf(satz=''), ''.join('<figure class="%s">%s</figure>' % ('tw-08-ich' if k.startswith('kopf_') else '', bild(k, 640)) for k in WAND),
    'In Kerze gerahmt: Derya, Momo und Rudi. Drumherum alle, die mit anpacken.')))

# 9 Umdrehen: die drei Karten wie heute; antippen dreht die Karte um, hinten die Leute, mit denen sie arbeiten, nur im Bild
HINTEN = [('theke', 'Mit ihr an der Theke.'), ('klaeren', 'Mit ihm an der Bar.'), ('pass2', 'Mit ihm am Pass.')]
F.append(('Umdrehen', '<div class="tw-09">%s<div class="kp-reihe tw-09-reihe">%s</div><p class="tw-09-hinweis mono sw auf">Karte antippen, und sie dreht sich um.</p></div>' % (
    kopf(), ''.join('<button type="button" class="tw-09-k auf" style="--i:%d" data-tw-um><span class="tw-09-vorn">%s</span><span class="tw-09-hinten">%s<b>%s</b></span></button>' % (
        i, '<span class="kp"><span class="kp-bild">%s</span><span class="kp-was mono">%s</span><span class="kp-name">%s</span><span class="kp-text">%s</span></span>' % (
            bild(P[i][0], 640), E(P[i][2]), E(P[i][3]), E(P[i][4])), bild(HINTEN[i][0], 640), E(HINTEN[i][1])) for i in range(3)))))

# 10 Fächer: hinter jeder Karte zwei Fotos aus ihrem Teil des Hauses, die beim Hinscrollen auffächern
FAECHER = [('theke', 'w5'), ('klaeren', 'bar'), ('pass2', 'kueche')]
F.append(('Fächer', '<div class="tw-10">%s<div class="tw-10-reihe">%s</div></div>' % (
    kopf(), ''.join('<div class="tw-10-platz auf" style="--i:%d"><figure class="tw-10-f a">%s</figure><figure class="tw-10-f b">%s</figure>%s</div>' % (
        i, bild(a, 640), bild(b, 640), karte(i)) for i, (a, b) in enumerate(FAECHER)))))

# 11 Laufband: die drei gross und rund, dahinter läuft quer über die Seite, was die Mannschaft tut
LAUF = ' · '.join(['Theke', 'Küche', 'Service', 'Tafel', 'Pass', 'Bar', 'Spülküche', 'Musik'] * 2)
F.append(('Laufband', '<div class="tw-11">%s<div class="tw-11-buehne"><p class="tw-11-lauf" aria-hidden="true"><span>%s ·&#160;</span><span>%s ·&#160;</span></p>'
          '<div class="tw-11-reihe">%s</div></div></div>' % (kopf(), LAUF, LAUF, ''.join(mini(i, 'tw-mini tw-riesig') for i in range(3)))))

# 12 Der Film: die Mannschaft im eigenen Film (Dirty Chicken, 10,7 s, läuft ohne Ton), daneben die drei
F.append(('Der Film', '<div class="tw-12"><figure class="tw-12-film auf"><video src="assets/film/familie.mp4?v=%s" poster="assets/film/familie.webp?v=%s" muted playsinline loop autoplay preload="metadata"></video></figure>'
          '<div class="tw-12-r">%s<div class="tw-12-liste">%s</div></div></div>' % (
              VERSION, VERSION, kopf(cls='', satz='„Wenn aus Freunden und Kollegen Familie wird.“ So nennt die Mannschaft ihren eigenen Film.'),
              ''.join(mini(i, 'tw-mini tw-zeile') for i in range(3)))))

# 13 Durchwischen: ein Band zum Wischen, zuerst die drei im Hochformat, dann die Mannschaft bei der Arbeit, nur mit einem Wort zum Ort
WISCH = [('pass2', 'Am Pass'), ('w2', 'Im Service'), ('theke', 'An der Theke'), ('kueche', 'In der Küche'), ('w6', 'An der Tafel'), ('dc_team', 'Alle zusammen')]
F.append(('Durchwischen', '<div class="tw-13">%s<div class="tw-13-band auf">%s%s</div><p class="tw-13-hinweis mono sw auf">Zur Seite wischen</p></div>' % (
    kopf(),
    ''.join('<figure class="tw-13-k ich">%s<figcaption><span class="mono">%s</span>%s</figcaption></figure>' % (bild(p[1], 1000), E(p[2]), E(p[3])) for p in P),
    ''.join('<figure class="tw-13-k">%s<figcaption><span class="mono">%s</span></figcaption></figure>' % (bild(k, 1000), E(w)) for k, w in WISCH))))

# 14 Triptychon und Streifen: die drei als hohe Bilder nebeneinander, darunter ein schmaler Streifen mit der ganzen Mannschaft
F.append(('Triptychon und Streifen', '<div class="tw-14">%s<div class="tw-14-drei">%s</div><figure class="tw-14-streifen auf">%s</figure><p class="tw-14-satz sw auf">Und alle, die mit anpacken.</p></div>' % (
    kopf(satz=''), ''.join('<figure class="auf" style="--i:%d">%s<figcaption><span class="mono">%s</span>%s</figcaption></figure>' % (i, bild(p[1], 1000), E(p[2]), E(p[3])) for i, p in enumerate(P)),
    bild('dn_team', 1600, pos='50% 47%'))))

# 15 Markiert: das Gruppenfoto gross, drei Ringe in Kerze um die drei; die Namen daneben, wer darüberfährt, sieht den Ring
F.append(('Markiert', '<div class="tw-15" data-tw-ringe><figure class="tw-15-bild auf">%s%s</figure><div class="tw-15-r">%s<div class="tw-15-liste">%s</div></div></div>' % (
    bild('dc_team', 1000), ''.join('<span class="tw-15-ring" data-r="%d" style="left:%.1f%%;top:%.1f%%;--i:%d"></span>' % (i, x, y, i) for i, (x, y) in enumerate(GESICHT)),
    kopf(cls='', satz='Drei davon kennst du von hier. Die anderen triffst du am Abend.'),
    ''.join('<div class="tw-15-name sw auf" data-r="%d" style="--i:%d"><span class="mono">%s</span><b>%s</b></div>' % (i, i, E(p[2]), E(p[3])) for i, p in enumerate(P)))))


def main():
    seite = open(os.path.join(HIER, 'leute.html')).read()
    m = re.search(r'(<section class="vab[^"]*v-lt-koepfe[^"]*"[^>]*>)(.*?)(</section>)', seite, re.S)
    assert m, 'Teil «Die Leute» in leute.html nicht gefunden (erst varianten.py laufen lassen)'
    kopf_tag = m.group(1).replace('<section class="', '<section id="team" data-name="Die Leute" class="wahl ', 1)
    teile = ['<div class="wv" data-n="0">%s</div>' % m.group(2)]
    teile += ['<div class="wv tw tw-f%02d" data-n="%d" hidden><div class="vi">%s</div></div>' % (i, i, inner) for i, (_n, inner) in enumerate(F, 1)]
    neu = kopf_tag + '<div class="wahl-marke"><b>Die Leute</b><span data-nr></span></div>' + ''.join(teile) + m.group(3)
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: drei Karten'] + [n for n, _x in F]
    v = VERSION + 'r%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('team-wahl.css', 'team-wahl.js'))
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["team"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
<script src="assets/team-wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION, v)
    seite = seite.replace('<title>', '<title>Die Leute wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<link rel="stylesheet" href="assets/team-wahl.css?v=%s">\n</head>' % (VERSION, v), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'team-wahl.html'), 'w').write(seite)
    print('Seite team-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
