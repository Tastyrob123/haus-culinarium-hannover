#!/usr/bin/env python3
"""Culinarium Hannover · Übergang Kopf → Fenster auf abende.html, dritte Runde: Fassungen 16 bis 45, 27.10.2026.
Robert zu Runde zwei (1–15): «Alles scheiße … Bitte 30 weitere Versionen.» Vorgaben: keine Abwandlung der ersten 15,
keine Fuge, Linie oder Kante anders gezeichnet; Fotos, Bewegung, Typografie aus der Welt des Hauses, der Kopf endet anders,
Kapitel fangen anders an. Weiter: keine Unschärfe, kein Verlauf ins Dunkle, Bewegung nur über transform (und opacity),
nichts fliegt von der Seite herein. Fassung 0 ist der heutige Stand.
Baut abende-uebergang-wahl3.html aus abende.html: Leiste unten, Pfeiltasten ← →, ?ue=Nummer.
Aufruf: python3 website/bau.py && python3 website/uebergang_abende_wahl3.py"""
import json, os
import bau
import abende_info as AI

HIER = os.path.dirname(os.path.abspath(__file__))
E = bau.E
V = bau.VERSION
CREME, NACHT = '#F4EEE8', '#0F0E13'


def img(k, gr=1000, cls='', pos='50% 50%'):
    return '<img class="%s" src="assets/bild/%s-%d.webp?v=%s" alt="%s" loading="lazy" decoding="async" style="object-position:%s">' % (
        cls, k, gr, V, E(bau.BILD[k][2]), pos)


# Nummer, Name, Gruppe ('zeig' = Kopf steht, darunter liegt das Fenster; 'steh' = Kopf steht ohne Fenster dahinter; '' = Kapitel dazwischen)
F = [
    (16, 'Hochrollen: die beiden Hälften rollen nacheinander nach oben weg, darunter liegt das Fenster', 'zeig'),
    (17, 'Die Schere: links geht hoch, rechts geht runter, dazwischen öffnet sich das Fenster', 'zeig'),
    (18, 'Kacheln heben ab: der Kopf zerfällt in acht Kacheln, die einzeln nach oben fliegen', 'zeig'),
    (19, 'Umblättern: der Kopf klappt nach oben weg wie eine Seite der Karte', 'zeig'),
    (20, 'Der Fächer: die Hälften kippen nach aussen und fallen weg', 'zeig'),
    (21, 'Hineinzoomen: man fährt in die Tafel hinein, dann hebt sich der Kopf', 'zeig'),
    (22, 'Zurücktreten: der Kopf wird kleiner und geht nach oben, das Fenster steht schon dahinter', 'zeig'),
    (23, 'Der Titel bleibt: die Bilder gehen, «Alle Abende.» bleibt stehen und wird zur Überschrift des Fensters', 'zeig'),
    (24, 'Der Satz als Kapitel: der Satz aus dem Kopf bekommt eine eigene helle Seite, Wort für Wort', ''),
    (25, 'Vierzehn: die Zahl der Abende zählt beim Scrollen hoch', ''),
    (26, 'Die Uhrzeit: Freitag 19:00, Samstag 17:00, gross wie auf einem Plakat', ''),
    (27, 'A UNiQUE EXPERiENCE: die Zeile von den Plakaten, gross und in Bewegung', ''),
    (28, 'Die Speisenfolge: die Gänge der ersten Karte leuchten beim Scrollen nacheinander auf', ''),
    (29, 'Die Fotowand: vier Bilder der Abende Kante an Kante, sie schweben nacheinander herauf', ''),
    (30, 'Das Panorama: der Pass mit den Tellern über die ganze Breite, die Kamera fährt zurück', ''),
    (31, 'Nacht und Tag: das Schild der Bar abends und am Tag, die Naht des Kopfs läuft weiter', ''),
    (32, 'Der Kontaktbogen: zwölf Bilder der Abende wie auf einem Kontaktabzug, mit Nummern', ''),
    (33, 'Die Hälften werden Bilder: die zwei Kopfbilder werden klein und rahmen den Titel', 'steh'),
    (34, 'Die Menükarte: die echte Karte des ersten Abends steht auf der Naht und richtet sich auf', ''),
    (35, 'Der Spalt: die Naht des Kopfs öffnet sich im Fenster von der Mitte aus', ''),
    (36, 'Gegenläufig: zwei Spalten mit Bildern der Abende laufen beim Scrollen gegeneinander', ''),
    (37, 'Das Kalenderblatt: beim Scrollen blättert der Kalender durch alle vierzehn Termine', ''),
    (38, 'Die Namen der Drinks: Momos Drinks von den Karten schweben in verschiedenen Tempi', ''),
    (39, 'By Momo x Rudi: die beiden, Bild an Bild, mit ihren Namen darunter', ''),
    (40, 'Das Zitat: ein Satz von Culinarium selbst, gross gesetzt', ''),
    (41, 'Der erste Abend: 20.05.2023 gross über der Bar', ''),
    (42, 'Der Teller: ein Teller von oben liegt auf der Naht und dreht sich beim Scrollen', ''),
    (43, 'Bild in der Schrift: «Abende» in riesigen Buchstaben, gefüllt mit einem Bild der Tafel', ''),
    (44, 'Die Leuchtschrift: das Negroni-Schild der Bar geht ruhig an', ''),
    (45, 'Aufstehen: drei Bilder liegen flach wie auf dem Tisch und stellen sich beim Scrollen auf', ''),
]

# ---------------------------------------------------------------- Inhalte der Kapitel
SATZ = 'Jeder Abend seit dem ersten Pop-up im Mai 2023. Darunter alle Plakate, so wie sie angekündigt wurden.'
woerter = ''.join('<span class="w" style="--i:%d"><span>%s</span></span> ' % (i, E(w)) for i, w in enumerate(SATZ.split()))

k1 = AI.KARTEN['CxNkFWTIvL2']
gaenge_erste = [g for g, _, _ in k1['gaenge']]  # Amuse Bouche, Apéritif, Vorspeise, Hauptgang, Dessert

drinks = []
for k in ('CxNkFWTIvL2', 'ohne-2023', 'CzMcqNcMCqG', 'C56bJeds8PF'):
    for _, _, d in AI.KARTEN[k]['gaenge']:
        n = d.split(' · ')[0].strip()
        if n and '|' not in n and n not in drinks:
            drinks.append(n)
drinks = drinks[:14]

kal = ''.join('<div class="u3-blatt" style="--i:%d;z-index:%d"><b>%s</b><p class="t">%s</p><p class="j">%s</p></div>' % (
    i, 40 - i, 'Culinarium', E(d), j) for i, (j, d, z, p, pid, mit) in enumerate(bau.ABENDE))

ZITAT = ('„2023 mit einem zauberhaften Abschluss .. mit tollen Menschen, mit leckerem Essen und mit wunderbar kreativen Drinks“', 'Culinarium auf Instagram, 9. Januar 2024')

KACHELN = ''.join('<div class="u3-ka" style="--c:%d;--r:%d;--d:%.2f;--ox:%d%%"><div>%s</div></div>' % (
    c, r, d, -(c % 2) * 100, img('schaumglas' if c < 2 else 't08', 1000).replace('loading="lazy"', 'loading="eager"')) for (c, r, d) in [(0, 0, .0), (1, 0, .22), (2, 0, .08), (3, 0, .3), (0, 1, .16), (1, 1, .04), (2, 1, .26), (3, 1, .12)])

KARTE = '<div class="u3-mk">%s<p class="u3-mk-m">Menü</p>%s</div>' % (bau.marke('wm'), ''.join(
    '<div class="u3-mk-g"><p class="n">%s</p><p class="t">%s</p></div>' % (E(g), E(t or d.split(' · ')[0])) for g, t, d in k1['gaenge']))

X = {
    24: '<section class="u3-x x24 hell" data-p><p class="u3-satz">%s</p></section>' % woerter,
    25: '<section class="u3-x x25 hell" data-p><p class="u3-zahl">0</p><p class="u3-unter">Abende seit September 2023</p></section>',
    26: '<section class="u3-x x26" data-p><div><p class="u3-tag">Freitag</p><p class="u3-uhr"><span>19:00</span></p></div><div><p class="u3-tag">Samstag</p><p class="u3-uhr"><span>17:00</span></p></div></section>',
    27: '<section class="u3-x x27" data-p><p class="a">A UNiQUE</p><p class="b">EXPERiENCE</p><p class="c">BY MOMO X RUDI</p></section>',
    28: '<section class="u3-x x28 hell" data-p><p class="u3-k mono">Die erste Karte, September 2023</p><ol>%s</ol></section>' % ''.join('<li>%s</li>' % E(g) for g in gaenge_erste),
    29: '<section class="u3-x x29" data-p>%s</section>' % ''.join('<figure style="--i:%d">%s</figure>' % (i, img(k)) for i, k in enumerate(['t01', 'toast', 'lachen', 't13'])),
    30: '<section class="u3-x x30" data-p><figure>%s</figure></section>' % img('pass', 1600),
    31: '<section class="u3-x x31" data-p><figure class="l">%s<figcaption>Abends</figcaption></figure><figure class="r">%s<figcaption>Am Tag</figcaption></figure></section>' % (img('schildnacht'), img('schildtag', 1600)),
    32: '<section class="u3-x x32" data-p>%s</section>' % ''.join('<figure style="--i:%d">%s<figcaption>%02d</figcaption></figure>' % (i, img(k, 640), i + 1) for i, k in enumerate(['t05', 't09', 'r01', 't10', 'g1', 't12', 'anstossen', 'r04', 't14', 'kerze1', 'r08', 't06'])),
    34: '<div class="u3-x x34" data-p>%s</div>' % KARTE,
    36: '<section class="u3-x x36" data-p><div class="sp l">%s</div><div class="sp r">%s</div></section>' % (
        ''.join('<figure>%s</figure>' % img(k) for k in ['t05', 't09', 't10', 't12', 'kerze2']), ''.join('<figure>%s</figure>' % img(k) for k in ['t14', 't06', 't07', 'service', 'anstossen'])),
    37: '<section class="u3-x x37 hell" data-p><div class="u3-kal">%s</div><p class="u3-unter">Vierzehn Abende, September 2023 bis September 2026</p></section>' % kal,
    38: '<section class="u3-x x38" data-p>%s</section>' % ''.join('<p style="--x:%d%%;--y:%d%%;--s:%.2f;--g:%d">%s</p>' % (
        x, y, s, g, E(n)) for n, (x, y, s, g) in zip(drinks, [(8, 8, 1.2, 40), (54, 4, .9, -30), (30, 22, 1.5, 70), (70, 26, 1, 20), (6, 40, .95, -50), (46, 44, 1.3, 55), (78, 50, .9, -25),
                                                               (18, 62, 1.1, 30), (56, 66, 1.4, -60), (34, 80, .9, 45), (74, 82, 1.2, -35), (4, 88, 1, 25), (44, 92, 1, -20), (84, 12, .85, 60)])),
    39: '<section class="u3-x x39 hell" data-p><p class="u3-by">By Momo <em>x</em> Rudi.</p><div class="u3-zwei"><figure>%s<figcaption><b>Momo</b><span>mixt die Drinks</span></figcaption></figure><figure>%s<figcaption><b>Rudi</b><span>kocht die Gänge</span></figcaption></figure></div></section>' % (
        img('momo', 1600, pos='50% 25%'), img('rudi', 1600, pos='50% 25%')),
    40: '<section class="u3-x x40 hell" data-p><blockquote><p>%s</p><cite>%s</cite></blockquote></section>' % (E(ZITAT[0]), E(ZITAT[1])),
    41: '<section class="u3-x x41" data-p><figure>%s</figure><div class="u3-erst"><p class="d"><span>20.05.2023</span></p><p class="s">Das erste Pop-up, mit Momo.</p></div></section>' % img('barlicht', 1000, pos='50% 60%'),
    42: '<div class="u3-x x42" data-p><div class="u3-teller">%s</div></div>' % img('r02', 1000),
    43: '<section class="u3-x x43 hell" data-p><p class="u3-fuell" style="background-image:url(assets/bild/t03-1600.webp?v=%s)">Abende</p></section>' % V,
    44: '<section class="u3-x x44" data-p><figure>%s</figure></section>' % img('barneg', 1600),
    45: '<section class="u3-x x45" data-p>%s</section>' % ''.join('<figure style="--i:%d">%s</figure>' % (i, img(k)) for i, k in enumerate(['r01', 'g1', 'r04'])),
}

EINSATZ = ''.join(X.values())

CSS = '''
/* Übergang Kopf → Fenster, dritte Runde (nur Wahlseite) */
.u3-x{display:none;position:relative}
body[class*="u3-"] .kopf-geteilt::after,body[class*="u3-"] .kopf-geteilt::before,body[class*="u3-"] #fenster-abende::before,body[class*="u3-"] #fenster-abende::after{content:none}
.kopf-geteilt{position:relative}
.u3-x.hell{background:%(c)s;color:#232129}
.u3-x:not(.hell){background:%(n)s;color:#FAF4F4}
.u3-x img{display:block;width:100%%;height:100%%;object-fit:cover}

/* ===== Kopf steht (zeig: Fenster liegt darunter; steh: ohne Fenster) ===== */
body.u3-pin .u3-buehne{height:220vh;position:relative}
body.u3-pin .kopf-geteilt{position:sticky;top:0;z-index:3}
body.u3-zeig .kopf-geteilt{background:transparent}
body.u3-zeig #fenster-abende{margin-top:-220vh;height:calc(220vh + min(66vh,640px))!important;z-index:1}
body.u3-pin .kg-h{transition:none!important}
body.u3-pin .kg-grund,body.u3-pin .kg-text{will-change:transform,opacity}
/* 16 Hochrollen */
body.u3-16 .kg-h.l{transform:translateY(calc(clamp(0,var(--k)/.7,1) * -118%%))!important}
body.u3-16 .kg-h.r{transform:translateY(calc(clamp(0,(var(--k) - .25)/.7,1) * -118%%))!important}
body.u3-16 .kg-grund,body.u3-16 .kg-text{opacity:calc(1 - var(--k)*2.4)}
body.u3-16 .kg-text{transform:translate(-50%%,calc(-42%% - var(--k)*40vh))}
/* 17 Schere */
body.u3-17 .kg-h.l{transform:translateY(calc(var(--k) * -118%%))!important}
body.u3-17 .kg-h.r{transform:translateY(calc(var(--k) * 118%%))!important}
body.u3-17 .kg-grund,body.u3-17 .kg-text{opacity:calc(1 - var(--k)*2.4)}
/* 18 Kacheln */
.u3-kacheln{display:none}
body.u3-18 .kg-h,body.u3-18 .kg-grund{visibility:hidden}
body.u3-18 .u3-kacheln{display:block;position:absolute;inset:0;z-index:0}
.u3-ka{position:absolute;left:calc(var(--c)*25%%);top:calc(var(--r)*50%%);width:25%%;height:50%%;overflow:hidden;transform:translateY(calc(clamp(0,(var(--k) - var(--d))/.5,1) * -230%%))}
.u3-ka>div{position:absolute;left:var(--ox);top:calc(var(--r) * -100%%);width:200%%;height:200%%}
.u3-ka img{display:block;width:100%%;height:100%%;object-fit:cover}
body.u3-18 .kg-text{opacity:calc(1 - var(--k)*2.4)}
/* 19 Umblättern */
body.u3-19 .u3-buehne{perspective:1800px}
body.u3-19 .kopf-geteilt{transform-origin:50%% 0;transform:rotateX(calc(var(--k) * 96deg));backface-visibility:hidden}
/* 20 Fächer */
body.u3-20 .kopf-geteilt{overflow:visible}
body.u3-20 .u3-buehne{overflow-x:clip}
body.u3-20 .kg-h.l{transform-origin:0 100%%;transform:translateY(calc(var(--k)*70%%)) rotate(calc(var(--k) * -24deg))!important}
body.u3-20 .kg-h.r{transform-origin:100%% 100%%;transform:translateY(calc(var(--k)*70%%)) rotate(calc(var(--k) * 24deg))!important}
body.u3-20 .kg-grund,body.u3-20 .kg-text{opacity:calc(1 - var(--k)*2.4)}
/* 21 Hineinzoomen */
body.u3-21 .kopf-geteilt{transform:translateY(calc(clamp(0,(var(--k) - .55)/.45,1) * -102%%))}
body.u3-21 .kg-h.l{transform-origin:100%% 55%%;transform:scale(calc(1 + min(var(--k),.55)*1.3))!important}
body.u3-21 .kg-h.r{transform-origin:0 55%%;transform:scale(calc(1 + min(var(--k),.55)*1.3))!important}
body.u3-21 .kg-grund,body.u3-21 .kg-text{opacity:calc(1 - var(--k)*3)}
/* 22 Zurücktreten */
body.u3-22 .kopf-geteilt{transform:translateY(calc(clamp(0,(var(--k) - .6)/.4,1) * -112%%)) scale(calc(1 - clamp(0,var(--k)/.6,1) * .24))}
body.u3-22 .kopf-geteilt.zu{clip-path:inset(0 round 26px);-webkit-clip-path:inset(0 round 26px)}
/* 23 Der Titel bleibt */
body.u3-23 .kg-h,body.u3-23 .kg-grund{transform:translateY(calc(var(--k) * -118%%))!important}
body.u3-23 .kg-text .sw{opacity:calc(1 - var(--k)*4)}
body.u3-23 .kg-text{transform:translate(-50%%,-42%%) scale(calc(1 - var(--k)*.22))}
body.u3-23 #fenster-abende .fenster-satz{visibility:hidden}
/* 33 Die Hälften werden Bilder */
body.u3-33 .kg-grund{opacity:calc(1 - var(--k)*2)}
body.u3-33 .kg-h.l{transform:translateX(calc(var(--k) * -6vw)) scale(calc(1 - var(--k)*.56))!important}
body.u3-33 .kg-h.r{transform:translateX(calc(var(--k) * 6vw)) scale(calc(1 - var(--k)*.56))!important}
body.u3-33 .kopf-geteilt.zu .kg-h{clip-path:inset(6%% 0 round 18px);-webkit-clip-path:inset(6%% 0 round 18px)}

/* ===== Kapitel dazwischen ===== */
body.u3-24 .x24,body.u3-25 .x25,body.u3-26 .x26,body.u3-27 .x27,body.u3-28 .x28,body.u3-29 .x29,body.u3-30 .x30,body.u3-31 .x31,body.u3-32 .x32,body.u3-34 .x34,
body.u3-36 .x36,body.u3-37 .x37,body.u3-38 .x38,body.u3-39 .x39,body.u3-40 .x40,body.u3-41 .x41,body.u3-42 .x42,body.u3-43 .x43,body.u3-44 .x44,body.u3-45 .x45{display:block}
/* 24 Satz */
body.u3-24 .kg-text .sw{display:none}
.x24{padding:clamp(90px,16vh,170px) var(--rand)}
.u3-satz{max-width:24ch;margin:0 auto;text-align:center;font:330 clamp(34px,4.4vw,66px)/1.12 var(--titel);letter-spacing:-.015em;font-variation-settings:"SOFT" 100,"opsz" 144}
.u3-satz .w{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.08em}
.u3-satz .w>span{display:inline-block;transform:translateY(110%%);transition:transform 1.1s var(--k) calc(var(--i)*.06s)}
.x24.da .u3-satz .w>span{transform:none}
/* 25 Vierzehn */
.x25{padding:clamp(60px,10vh,110px) var(--rand) clamp(70px,12vh,130px);text-align:center}
.u3-zahl{font:250 clamp(200px,30vw,440px)/.85 var(--titel);letter-spacing:-.04em;color:#232129;font-variation-settings:"SOFT" 100,"opsz" 144;font-variant-numeric:tabular-nums}
.u3-unter{margin-top:18px;font:500 12px/1 var(--mono);letter-spacing:.24em;text-transform:uppercase;color:#B15736}
/* 26 Uhrzeit */
.x26{display:none;padding:clamp(80px,14vh,150px) var(--rand)}
body.u3-26 .x26{display:grid;grid-template-columns:1fr 1fr;gap:4vw;text-align:center}
.u3-tag{font:500 12px/1 var(--mono);letter-spacing:.26em;text-transform:uppercase;color:var(--kerze-hell,#F5A689)}
.u3-uhr{overflow:hidden;margin-top:14px}
.u3-uhr span{display:block;font:250 clamp(110px,15vw,240px)/.9 var(--titel);letter-spacing:-.04em;font-variation-settings:"SOFT" 100,"opsz" 144;transform:translateY(105%%);transition:transform 1.4s var(--k)}
.x26 div+div .u3-uhr span{transition-delay:.18s}
.x26.da .u3-uhr span{transform:none}
/* 27 A UNiQUE EXPERiENCE */
.x27{padding:clamp(70px,12vh,130px) 0;overflow:hidden;text-align:center}
.x27 p{font:800 clamp(64px,11vw,190px)/.92 var(--etikett);letter-spacing:-.01em;white-space:nowrap}
.x27 .a{transform:translateY(calc((var(--p) - .5) * 26vh))}
.x27 .b{color:var(--kerze);transform:translateY(calc((var(--p) - .5) * 6vh))}
.x27 .c{transform:translateY(calc((var(--p) - .5) * -18vh));font-size:clamp(40px,6.4vw,110px)}
/* 28 Speisenfolge */
.x28{padding:clamp(80px,14vh,150px) var(--rand);text-align:center}
.x28 .u3-k{font:500 11px/1 var(--mono);letter-spacing:.24em;text-transform:uppercase;color:#B15736;margin-bottom:28px}
.x28 ol{list-style:none;margin:0;padding:0}
.x28 li{font:300 clamp(40px,5.4vw,86px)/1.1 var(--titel);letter-spacing:.02em;text-transform:uppercase;font-variation-settings:"SOFT" 100,"opsz" 144;opacity:.14;transition:opacity .8s ease}
.x28 li+li::before{content:"";display:block;width:2px;height:clamp(22px,3.6vh,36px);background:#232129;margin:12px auto;opacity:.5}
.x28 li.an{opacity:1}
/* 29 Fotowand */
body.u3-29 .x29{display:grid;grid-template-columns:repeat(4,1fr);gap:0;background:%(n)s}
.x29 figure{margin:0;aspect-ratio:4/5;overflow:hidden;transform:translateY(90px);transition:transform 1.5s var(--k) calc(var(--i)*.14s)}
.x29 figure img{transform:scale(1.14);transition:transform 2.6s var(--k2) calc(var(--i)*.14s)}
.x29.da figure,.x29.da figure img{transform:none}
/* 30 Panorama */
.x30 figure{margin:0;height:min(64vh,620px);overflow:hidden}
.x30 img{transform:scale(calc(1.32 - var(--q)*.32))}
/* 31 Nacht und Tag */
body.u3-31 .x31{display:grid;grid-template-columns:1fr 1fr;height:min(88vh,820px);overflow:hidden}
.x31 figure{margin:0;position:relative;overflow:hidden}
.x31 figure img{height:116%%}
.x31 .l img{transform:translateY(calc((var(--p) - .5) * -14%%))}
.x31 .r img{transform:translateY(calc((var(--p) - .5) * 14%%))}
.x31 figcaption{position:absolute;left:24px;bottom:22px;font:500 11px/1 var(--mono);letter-spacing:.24em;text-transform:uppercase;color:#FAF4F4;text-shadow:0 1px 10px rgba(0,0,0,.6)}
/* 32 Kontaktbogen */
body.u3-32 .x32{display:grid;grid-template-columns:repeat(6,1fr);gap:clamp(8px,1vw,14px);padding:clamp(40px,7vh,70px) var(--rand);background:#16151A}
.x32 figure{margin:0;transform:translateY(60px);opacity:0;transition:transform 1.2s var(--k) calc(var(--i)*.07s),opacity .6s ease calc(var(--i)*.07s)}
.x32 figure img{aspect-ratio:4/5;height:auto}
.x32 figcaption{margin-top:7px;font:500 10px/1 var(--mono);letter-spacing:.2em;color:var(--kerze)}
.x32.da figure{transform:none;opacity:1}
/* 34 Menükarte auf der Naht */
.x34{height:0;z-index:6;perspective:1400px}
.u3-mk{position:absolute;left:50%%;top:0;width:min(400px,78vw);background:#FBF8F4;color:#232129;border-radius:6px;padding:30px 30px 26px;text-align:center;
  transform-origin:50%% 100%%;transform:translate(-50%%,-50%%) rotateX(calc((1 - var(--q)) * 58deg));box-shadow:0 40px 60px -36px rgba(0,0,0,.7)}
.u3-mk .marke{width:78%%;height:auto;aspect-ratio:4650/564;color:#232129}
.u3-mk-m{font:600 10px/1 var(--etikett);letter-spacing:.26em;text-transform:uppercase;margin:8px 0 14px;padding-bottom:12px;border-bottom:1.5px solid #232129}
.u3-mk-g{padding:7px 0}.u3-mk-g .n{font:500 15px/1.1 var(--text);letter-spacing:.08em;text-transform:uppercase}
.u3-mk-g .t{margin-top:4px;font:400 11px/1.4 var(--text);color:#6A6570}
/* 35 Der Spalt */
.u3-spalt{display:none}
body.u3-35 .u3-spalt{display:block;position:absolute;inset:0;z-index:4;pointer-events:none;overflow:hidden}
.u3-spalt i{position:absolute;top:0;bottom:0;width:50.5%%;background:%(n)s}
.u3-spalt i:first-child{left:0;transform:translateX(calc(var(--q) * -101%%))}
.u3-spalt i:last-child{right:0;transform:translateX(calc(var(--q) * 101%%))}
/* 36 Gegenläufig */
body.u3-36 .x36{display:grid;grid-template-columns:1fr 1fr;height:min(110vh,1000px);overflow:hidden}
.x36 .sp{display:flex;flex-direction:column}
.x36 figure{margin:0;aspect-ratio:4/5;overflow:hidden;flex:none}
.x36 .l{transform:translateY(calc(var(--p) * -60%%))}
.x36 .r{transform:translateY(calc(-60%% + var(--p) * 60%%))}
/* 37 Kalenderblatt */
.x37{padding:clamp(80px,13vh,140px) var(--rand);text-align:center}
.u3-kal{position:relative;width:min(380px,80vw);aspect-ratio:4/4.4;margin:0 auto;perspective:1200px}
.u3-blatt{position:absolute;inset:0;background:#FBF8F4;border-radius:10px;box-shadow:0 30px 50px -34px rgba(35,33,41,.6),inset 0 0 0 1px rgba(35,33,41,.08);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:24px;
  transform-origin:50%% 0;transition:transform .7s var(--k),opacity .2s ease;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.u3-blatt b{position:absolute;top:0;left:0;right:0;padding:12px;border-radius:10px 10px 0 0;background:var(--kerze);color:#1A1218;font:600 11px/1 var(--etikett);letter-spacing:.24em;text-transform:uppercase}
.u3-blatt .t{font:300 clamp(26px,2.6vw,36px)/1.15 var(--titel);color:#232129;max-width:12ch}
.u3-blatt .j{font:250 clamp(70px,7vw,110px)/.9 var(--titel);color:#232129;letter-spacing:-.03em}
.u3-blatt.weg{transform:rotateX(-112deg);opacity:0;transition:transform .7s var(--k),opacity .25s ease .3s}
.x37 .u3-unter{margin-top:34px}
/* 38 Drinks */
body.u3-38 .x38{height:min(120vh,1080px);overflow:hidden}
.x38 p{position:absolute;left:var(--x);top:var(--y);font:italic 300 calc(clamp(26px,2.8vw,44px) * var(--s))/1 var(--titel);white-space:nowrap;color:#FAF4F4;
  transform:translateY(calc((var(--p) - .5) * var(--g) * 1vh))}
.x38 p:nth-child(3n){color:var(--kerze-hell,#F5A689)}
/* 39 Momo und Rudi */
.x39{padding:clamp(60px,10vh,110px) 0 0}
.u3-by{text-align:center;font:300 clamp(48px,6.4vw,104px)/1 var(--titel);letter-spacing:-.02em;margin-bottom:clamp(34px,5vh,56px)}
.u3-by em{font-style:normal;color:var(--kerze)}
.u3-zwei{display:grid;grid-template-columns:1fr 1fr}
.x39 figure{margin:0;position:relative;height:min(92vh,860px);overflow:hidden}
.x39 figure img{transform:scale(1.12);transition:transform 2.6s var(--k2)}
.x39.da figure img{transform:none}
.x39 figcaption{position:absolute;left:0;right:0;bottom:0;padding:26px 28px;display:flex;align-items:baseline;gap:14px;background:%(c)s}
.x39 figcaption b{font:300 clamp(30px,3vw,46px)/1 var(--titel)}
.x39 figcaption span{font:500 11px/1 var(--mono);letter-spacing:.2em;text-transform:uppercase;color:#B15736}
/* 40 Zitat */
.x40{padding:clamp(90px,15vh,170px) var(--rand)}
.x40 blockquote{margin:0 auto;max-width:26ch;text-align:center;transform:translateY(60px);opacity:0;transition:transform 1.5s var(--k),opacity .9s ease}
.x40.da blockquote{transform:none;opacity:1}
.x40 p{font:italic 300 clamp(32px,3.8vw,58px)/1.18 var(--titel);letter-spacing:-.01em}
.x40 cite{display:block;margin-top:30px;font:500 11px/1 var(--mono);font-style:normal;letter-spacing:.22em;text-transform:uppercase;color:#B15736}
/* 41 Der erste Abend */
.x41{height:min(90vh,840px);overflow:hidden}
.x41 figure{position:absolute;inset:0;margin:0}
.u3-erst{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:clamp(50px,9vh,90px);text-align:center}
.u3-erst .d{overflow:hidden}
.u3-erst .d span{display:block;font:250 clamp(84px,13vw,220px)/.9 var(--titel);letter-spacing:-.04em;color:#FAF4F4;text-shadow:0 2px 50px rgba(0,0,0,.55);transform:translateY(105%%);transition:transform 1.5s var(--k)}
.u3-erst .s{margin-top:16px;font:400 18px/1.4 var(--text);color:#FAF4F4;text-shadow:0 1px 18px rgba(0,0,0,.7);opacity:0;transition:opacity 1s ease .5s}
.x41.da .u3-erst .d span{transform:none}.x41.da .u3-erst .s{opacity:1}
/* 42 Teller */
.x42{height:0;z-index:6}
.u3-teller{position:absolute;left:50%%;top:0;width:min(400px,46vw);aspect-ratio:1;border-radius:50%%;overflow:hidden;transform:translate(-50%%,-50%%) rotate(calc(var(--q) * 140deg))}
.u3-teller img{transform:scale(1.5)}
/* 43 Bild in der Schrift */
.x43{padding:clamp(40px,6vh,70px) 0;overflow:hidden}
.u3-fuell{text-align:center;font:700 clamp(150px,25vw,420px)/.86 var(--titel);letter-spacing:-.05em;font-variation-settings:"SOFT" 0,"opsz" 144;background-size:cover;background-position:50%% 50%%;
  -webkit-background-clip:text;background-clip:text;color:transparent;transform:translateY(calc((var(--p) - .5) * -16vh))}
/* 44 Leuchtschrift */
.x44 figure{margin:0;height:min(84vh,780px);overflow:hidden;opacity:.06}
.x44 figure{transition:opacity 2.4s ease .2s}
.x44.da figure{opacity:1}
/* 45 Aufstehen */
body.u3-45 .x45{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(10px,1.2vw,16px);padding:clamp(70px,12vh,130px) var(--rand);perspective:1400px}
.x45 figure{margin:0;aspect-ratio:4/5;overflow:hidden;border-radius:var(--r);transform-origin:50%% 100%%;transform:rotateX(calc(clamp(0,1 - (var(--q) - var(--i)*.08)*1.25,1) * 78deg))}
@media (max-width:860px){
  body.u3-29 .x29{grid-template-columns:1fr 1fr}
  body.u3-32 .x32{grid-template-columns:repeat(3,1fr)}
  body.u3-26 .x26{grid-template-columns:1fr;gap:40px}
  .x41 .u3-erst .d span{font-size:19vw}
  body.u3-45 .x45{grid-template-columns:1fr 1fr 1fr;gap:6px}
  body.u3-zeig #fenster-abende{height:calc(220vh + 54svh)!important}
}

''' % {'c': CREME, 'n': NACHT}

PIN = [n for n, _, g in F if g]
ZEIG = [n for n, _, g in F if g == 'zeig']

LEISTE = r'''<script>
/* Übergang wählen (?ue=N): ← → oder Klick wechseln; 0 = heute, dann 16 bis 45 */
(function () {
  var L = %s, PIN = %s, ZEIG = %s, b = document.body, f = document.getElementById('fenster-abende'), bu = document.querySelector('.u3-buehne'), kopf = document.querySelector('.kopf-geteilt');
  var NR = L.map(function (x) { return x[0]; });
  var s = parseInt(new URLSearchParams(location.search).get('ue'), 10), n = NR.indexOf(s); if (n < 0) n = 1;
  var t = document.createElement('div');
  t.style.cssText = 'position:fixed;left:50%%;bottom:18px;transform:translateX(-50%%);z-index:300;background:#16151A;color:#FAF4F4;border:1px solid rgba(239,118,73,.6);border-radius:999px;padding:8px 10px;font:500 13px/1 Urbanist,sans-serif;letter-spacing:.06em;display:flex;gap:14px;align-items:center;white-space:nowrap;max-width:calc(100vw - 24px);overflow:hidden';
  var k = 'background:none;border:0;color:#F5A689;font:400 22px/1 Urbanist,sans-serif;cursor:pointer;padding:2px 10px';
  t.innerHTML = '<button type="button" style="' + k + '" data-s="-1" aria-label="Voriger Übergang">‹</button><span data-i style="overflow:hidden;text-overflow:ellipsis"></span><button type="button" style="' + k + '" data-s="1" aria-label="Nächster Übergang">›</button>';
  b.appendChild(t);
  var aktiv = [];
  function zeig(i) {
    n = (i + L.length) %% L.length; var nr = NR[n];
    b.className = b.className.replace(/\bu3-\S+/g, '').trim();
    if (nr) { b.classList.add('u3-' + nr); if (PIN.indexOf(nr) >= 0) b.classList.add('u3-pin'); if (ZEIG.indexOf(nr) >= 0) b.classList.add('u3-zeig'); }
    t.querySelector('[data-i]').innerHTML = '<span style="color:#F5A689">' + (nr || 0) + '</span>&nbsp;&nbsp;' + L[n][1];
    history.replaceState(null, '', '?ue=' + nr);
    [].forEach.call(document.querySelectorAll('.u3-x.da'), function (x) { x.classList.remove('da'); });
    aktiv = [].filter.call(document.querySelectorAll('[data-p]'), function (x) { return x.offsetParent !== null || getComputedStyle(x).display !== 'none'; });
    if (nr === 35) aktiv.push(f);
    rechnen(); setTimeout(hin, 60);
  }
  function c(x) { return Math.min(1, Math.max(0, x)); }
  function rechnen() {
    var vh = innerHeight;
    if (b.classList.contains('u3-pin')) {
      var r = bu.getBoundingClientRect(), kk = c(-r.top / (r.height - vh));
      bu.style.setProperty('--k', kk.toFixed(4)); kopf.classList.toggle('zu', kk > .01);
    }
    aktiv.forEach(function (el) {
      var r = el.getBoundingClientRect(), h = r.height, p = c((vh - r.top) / (vh + h)), q = c((vh - r.top) / (vh / 2 + h / 2));
      el.style.setProperty('--p', p.toFixed(4)); el.style.setProperty('--q', q.toFixed(4));
      if (r.top < vh * .82 && r.bottom > 0) el.classList.add('da');
      if (el.classList.contains('x25')) el.querySelector('.u3-zahl').textContent = Math.round(c((q - .15) / .7) * 14);
      if (el.classList.contains('x28')) [].forEach.call(el.querySelectorAll('li'), function (li, j) { li.classList.toggle('an', q > .25 + j * .14); });
      if (el.classList.contains('x37')) [].forEach.call(el.querySelectorAll('.u3-blatt'), function (bl, j, all) { bl.classList.toggle('weg', j < all.length - 1 && p > .18 + j * (.6 / (all.length - 1))); });
    });
  }
  addEventListener('scroll', function () { requestAnimationFrame(rechnen); }, { passive: true });
  addEventListener('resize', rechnen);
  t.addEventListener('click', function (e) { var x = e.target.closest('[data-s]'); if (x) zeig(n + +x.dataset.s); });
  addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); zeig(n + 1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); zeig(n - 1); } });
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  /* Stehende Köpfe starten oben, alle anderen mit der Naht in der Bildmitte */
  function hin() {
    if (b.classList.contains('u3-pin')) { scrollTo(0, 0); return; }
    var x = document.querySelector('.u3-x[data-p]:not([style*="none"])'), z = [].filter.call(document.querySelectorAll('.u3-x'), function (e) { return getComputedStyle(e).display !== 'none'; })[0];
    scrollTo(0, (z || f).getBoundingClientRect().top + scrollY - innerHeight * .5);
  }
  zeig(n);
  addEventListener('load', function () { setTimeout(hin, 150); setTimeout(function () { hin(); rechnen(); }, 900); });
})();
</script>
''' % (json.dumps([[0, 'Heute: unscharf ins Dunkle, orange Linie']] + [[nr, nm] for nr, nm, _ in F], ensure_ascii=False), json.dumps(PIN), json.dumps(ZEIG))

h = open(os.path.join(HIER, 'abende.html'), encoding='utf-8').read()
assert '<section class="kopf-geteilt"' in h and '<section class="fenster" id="fenster-abende"' in h, 'Kopf oder Fenster fehlt in abende.html (erst bau.py laufen lassen)'
h = h.replace('<title>', '<title>Übergang wählen (16–45) · ', 1)
h = h.replace('</head>', '<style>%s</style>\n</head>' % CSS, 1)
h = h.replace('<section class="kopf-geteilt"', '<div class="u3-buehne"><section class="kopf-geteilt"', 1)
h = h.replace('<div class="kg-grund" aria-hidden="true"></div>', '<div class="u3-kacheln" aria-hidden="true">%s</div><div class="kg-grund" aria-hidden="true"></div>' % KACHELN, 1)
i = h.index('<section class="fenster" id="fenster-abende"')
h = h[:i] + '</div>' + EINSATZ + h[i:]
j = h.index('>', h.index('<section class="fenster" id="fenster-abende"')) + 1
h = h[:j] + '<div class="u3-spalt" aria-hidden="true"><i></i><i></i></div>' + h[j:]
h = h.replace('</body>', LEISTE + '</body>', 1)
open(os.path.join(HIER, 'abende-uebergang-wahl3.html'), 'w', encoding='utf-8').write(h)
print('abende-uebergang-wahl3.html: Fassungen 16–45 + heute')
