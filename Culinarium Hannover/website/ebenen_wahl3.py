#!/usr/bin/env python3
"""Culinarium Hannover · Abschnitt «Abend und Haus», 15 Abwandlungen von «Über Eck», 26.10.2026.
Robert: «mach von 2 nochmal 15 Variationen» (Nummer 2 aus ebenen-wahl-2.html).
Baut ebenen-wahl-3.html. Oben als 00 die Ausgangsfassung, darunter 15 Abwandlungen: immer zwei Bilder mit schräger Naht
in Kerzenfarbe, anders sind Winkel, Richtung, Rahmen, Lage von Titel und Text, Zahl der Bilder und der bewegte Moment.
Nur transform und opacity bewegen sich, die wandernde Kante ist ein schräg gestelltes Feld (skewX), kein animierter Ausschnitt.
Aufruf: python3 website/ebenen_wahl3.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ebenen_wahl2 import ABEND, HAUS, blk, titel, KOPF_CSS, META, BILD, E, HIER


def fig(k, cls='', w=1000, pos=None, cd='none', cm='none'):
    """Foto mit Ausschnitt am Bildschirm (cd) und am Handy (cm)."""
    stufen = sorted(META[k]['stufen'])
    s = next((x for x in stufen if x >= w), stufen[-1])
    _q, p, alt = BILD[k]
    return ('<figure class="ph %s" style="--cd:%s;--cm:%s"><img src="assets/bild/%s-%d.webp" alt="%s" loading="lazy" decoding="async" style="object-position:%s"></figure>'
            % (cls, cd, cm, k, s, E(alt), pos or p))


def poly(spec):
    """('v', oben, unten) Naht von oben nach unten in Prozent der Breite; ('h', links, rechts) quer in Prozent der Höhe."""
    o, a, b = spec
    if o == 'v':
        return ('polygon(0 0,%s%% 0,%s%% 100%%,0 100%%)' % (a, b), 'polygon(%s%% 0,100%% 0,100%% 100%%,%s%% 100%%)' % (a, b), (a, 0, b, 100))
    return ('polygon(0 0,100%% 0,100%% %s%%,0 %s%%)' % (b, a), 'polygon(0 %s%%,100%% %s%%,100%% 100%%,0 100%%)' % (a, b), (0, a, 100, b))


def naht(linien, cls):
    return ('<svg class="naht %s" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">%s</svg>'
            % (cls, ''.join('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % l for l in linien)))


def sx(cls, L, R, d, m, innen='', lc='', rc='', linie=True, p=True):
    """Rahmen mit zwei Bildern und schräger Naht. L, R = (Bild, Lage, Breite)."""
    dl, dr, ld = poly(d)
    ml, mr, lm = poly(m)
    return ('<div class="sx %s"%s>%s%s%s%s</div>' % (
        cls, ' data-p' if p else '',
        fig(L[0], 'l ' + lc, L[2], L[1], dl, ml), fig(R[0], 'r ' + rc, R[2], R[1], dr, mr),
        (naht([ld], 'd') + naht([lm], 'm')) if linie else '', innen))


def tafel():
    return '<div class="tafel">%s</div>' % titel()


def unter():
    return '<div class="unter">%s%s</div>' % (blk(ABEND), blk(HAUS))


def tuer(k, pos, w=1000, gc=''):
    """Schräges Feld für die wandernde Kante: das Feld schert und wandert, das Bild darin hält gegen und bleibt stehen."""
    return '<div class="tuer"><div class="tuer-in">%s</div></div>' % fig(k, gc, w, pos)


F = []   # (Nr, Name, Satz, Bewegung · Handy, HTML, CSS)

F.append(('00', 'Über Eck (Ausgang)', 'Die gewählte Nummer 2 zum Vergleich: links die Tafel, rechts die Hausecke, die Naht steil, der Titel auf einer Tafel quer darüber, die Texte in den Ecken auf dem Bild.',
'Bewegung: beide Bilder ziehen von 110 auf 100 Prozent · Handy: Kante quer',
sx('w00', ('t08', '34% 45%', 1000), ('ecke', '62% 50%', 1600), ('v', 58, 42), ('h', 58, 42),
   tafel() + blk(ABEND, 'o lu') + blk(HAUS, 'o ro'), 'g gu', 'g go'),
'''.w00{margin:0 var(--rand);height:min(94svh,880px);min-height:640px}
.w00>.ph img{transform:scale(calc(1.1 - .1 * var(--p,1)))}'''))

F.append(('01', 'Steil, Text darunter', 'Die Naht fast senkrecht, das Bild frei von Text. Der Titel sitzt auf der Naht, Abend und Haus stehen darunter, jeder unter seiner Hälfte. Die Fotos bleiben ganz zu sehen.',
'Bewegung: beide Bilder ziehen von 110 auf 100 Prozent · Handy: Kante quer, Texte untereinander',
sx('w01', ('t08', '40% 45%', 1000), ('ecke', '60% 50%', 1600), ('v', 53, 47), ('h', 54, 46), tafel()) + unter(),
'''.w01{margin:0 var(--rand);aspect-ratio:16/8.2}
.w01>.ph img{transform:scale(calc(1.1 - .1 * var(--p,1)))}
@media (max-width:860px){.w01{aspect-ratio:4/5}}'''))

F.append(('02', 'Flach', 'Die Naht liegt fast waagerecht: oben die gedeckte Tafel, unten die Fenster der Bar. Man liest von oben nach unten, vom Abend ins Haus.',
'Bewegung: die beiden Bilder wandern gegeneinander seitwärts · Handy: Kante etwas flacher',
sx('w02', ('tafelleer', '50% 52%', 1600), ('fassade', '50% 50%', 1600), ('h', 64, 36), ('h', 56, 44),
   tafel() + blk(ABEND, 'o lo') + blk(HAUS, 'o ru'), 'g go', 'g gu'),
'''.w02{margin:0 var(--rand);height:min(96svh,900px);min-height:640px}
.w02>.ph img{transform:scale(1.07) translateX(calc((var(--p,.5) - .5) * -50px))}
.w02>.r img{transform:scale(1.07) translateX(calc((var(--p,.5) - .5) * 50px))}'''))

F.append(('03', 'Gegenläufig', 'Die Naht kippt in die andere Richtung. Der Abend beginnt oben links, das Haus endet unten rechts, so läuft der Blick einmal quer durch den Rahmen.',
'Bewegung: die Bar rechts steigt beim Scrollen leicht herauf · Handy: Kante quer, andere Neigung',
sx('w03', ('t01', '40% 42%', 1600), ('barnacht', '55% 50%', 1000), ('v', 40, 62), ('h', 40, 60),
   tafel() + blk(ABEND, 'o lo') + blk(HAUS, 'o ru'), 'g go', 'g gu'),
'''.w03{margin:0 var(--rand);height:min(94svh,880px);min-height:640px}
.w03>.r img{transform:scale(1.08) translateY(calc((var(--p,.5) - .5) * -60px))}'''))

F.append(('04', 'Randlos', 'Ohne Rahmen von Kante zu Kante, so hoch wie der Bildschirm. Der Titel steht oben frei auf dem Bild, beide Texte unten auf einem gemeinsamen dunklen Grund.',
'Bewegung: beide Bilder ziehen von 110 auf 100 Prozent · Handy: Titel auf einer Tafel in der Mitte',
sx('w04', ('anstossen', '40% 40%', 1600), ('theke', '60% 34%', 1000), ('v', 60, 40), ('h', 56, 44),
   '<i class="schleier"></i><div class="oben">%s</div>' % titel() + blk(ABEND, 'o lu') + blk(HAUS, 'o ru'), 'g', 'g'),
'''.w04{height:100svh;min-height:660px;border-radius:0!important}
.w04>.ph img{transform:scale(calc(1.1 - .1 * var(--p,1)))}
.w04 .schleier{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(14,12,16,.72) 0%,rgba(14,12,16,0) 30%,rgba(14,12,16,0) 52%,rgba(14,12,16,.92) 100%)}
.w04 .oben{position:absolute;z-index:3;top:clamp(36px,8vh,80px);left:0;right:0;text-align:center;padding:0 var(--rand)}
.w04 .o.lu{left:var(--rand)}.w04 .o.ru{right:var(--rand)}
@media (max-width:860px){div.w04{height:1260px}.w04 .schleier{display:none}.w04 .oben{top:50%;transform:translateY(-50%);left:20px;right:20px;background:var(--nacht);padding:16px 18px;border-radius:var(--r)}}'''))

F.append(('05', 'Die Kante wandert', 'Beim Hereinscrollen gehört der Rahmen zuerst fast ganz dem Abend. Dann wandert die Naht nach links und das Haus nimmt mehr Platz ein, der Titel reist auf der Naht mit.',
'Bewegung: die Naht wandert mit dem Scrollen von rechts nach links (schräges Feld, nur transform) · Handy: feste Kante quer',
'<div class="sx w05 tuerrahmen" data-p>%s%s%s<div class="trag">%s</div>%s%s</div>' % (
    fig('t08', 'l g gu', 1000, '40% 45%', 'none', poly(('h', 56, 44))[0]), tuer('ecke', '62% 50%', 1600, 'g gu'),
    fig('ecke', 'r g nurhandy', 1600, '62% 50%', 'none', poly(('h', 56, 44))[1]), tafel(),
    blk(ABEND, 'o lu'), blk(HAUS, 'o ru')),
'''.w05{margin:0 var(--rand);height:min(94svh,860px);min-height:620px;--f:calc(.12 - .26 * var(--p,1))}
.w05 .o.ru{max-width:300px}'''))

F.append(('06', 'Keil in der Mitte', 'Zwei Nähte statt einer: dazwischen ein Keil mit zwei Gläsern beim Anstossen, darauf der Titel. Links der Abend, rechts das Haus, in der Mitte das, was beide verbindet.',
'Bewegung: das Bild im Keil zieht von 112 auf 100 Prozent · Handy: drei Bänder quer übereinander',
'<div class="sx w06" data-p>%s%s%s%s%s%s%s%s</div>' % (
    fig('t08', 'l g go', 1000, '38% 45%', 'polygon(0 0,44% 0,32% 100%,0 100%)', 'polygon(0 0,100% 0,100% 30%,0 38%)'),
    fig('glaeser', 'mi', 1600, '50% 45%', 'polygon(44% 0,68% 0,56% 100%,32% 100%)', 'polygon(0 38%,100% 30%,100% 62%,0 70%)'),
    fig('theke', 'r g gu', 1000, '66% 34%', 'polygon(68% 0,100% 0,100% 100%,56% 100%)', 'polygon(0 70%,100% 62%,100% 100%,0 100%)'),
    naht([(44, 0, 32, 100), (68, 0, 56, 100)], 'd'), naht([(0, 38, 100, 30), (0, 70, 100, 62)], 'm'),
    tafel(), blk(ABEND, 'o lo'), blk(HAUS, 'o ru')),
'''.w06{margin:0 var(--rand);height:min(94svh,880px);min-height:640px}
.w06 .mi img{transform:scale(calc(1.12 - .12 * var(--p,1)))}
@media (max-width:860px){div.w06{height:1400px}}'''))

F.append(('07', 'Die Schärpe', 'Die Naht wird zu einem breiten dunklen Band, schräg über den ganzen Rahmen, mit zwei Linien in Kerzenfarbe. Der Titel läuft auf dem Band entlang wie auf einer Schärpe.',
'Bewegung: das Band gleitet beim Hereinscrollen entlang seiner Richtung · Handy: Band mit zweizeiligem Titel',
sx('w07', ('tafelleer', '50% 55%', 1600), ('fassade', '50% 50%', 1600), ('h', 64, 36), ('h', 53, 47),
   '<div class="band">%s</div>' % titel() + blk(ABEND, 'o lo') + blk(HAUS, 'o ru'), 'g go', 'g gu', linie=False),
'''.w07{margin:0 var(--rand);height:min(96svh,900px);--wink:-9.44deg}
.w07 .band{position:absolute;z-index:3;left:-20%;right:-20%;top:50%;display:grid;place-items:center;padding:clamp(18px,2vw,30px) 0;background:var(--nacht);
border-top:1.6px solid var(--kerze);border-bottom:1.6px solid var(--kerze);transform:translateY(-50%) rotate(var(--wink)) translateX(calc((1 - var(--p,1)) * -9%))}
.w07 .band .ti{white-space:nowrap;font-size:clamp(28px,3.4vw,56px)}
.w07 .band br{display:none}
@media (max-width:860px){.w07 .band{left:-10%;right:-10%}
.w07 .band .ti{white-space:normal;text-align:center;padding:0 14%}.w07 .band br{display:inline}}'''))

F.append(('08', 'Text links, Ecke rechts', 'Der Text steht als ein Block links: Titel, Abend, Haus. Rechts ein hohes Bild mit der schrägen Naht, beschriftet nur mit «Der Abend» und «Das Haus» in den Ecken.',
'Bewegung: beide Bilder ziehen von 110 auf 100 Prozent · Handy: Bild oben, Text darunter',
'<div class="w08"><div class="text">%s<div class="zwei">%s%s</div></div>%s</div>' % (
    titel(), blk(ABEND), blk(HAUS),
    sx('w08b', ('t12', '40% 42%', 1600), ('ecke', '64% 50%', 1600), ('v', 62, 38), ('h', 56, 44),
       '<p class="mono marke lu">Der Abend</p><p class="mono marke ro">Das Haus</p>', 'g gu', 'g go')),
'''.w08{display:grid;grid-template-columns:minmax(0,.86fr) minmax(0,1.14fr);gap:clamp(28px,4.4vw,80px);align-items:center;padding:0 var(--rand)}
.w08 .text{display:flex;flex-direction:column;gap:34px}
.w08 .zwei{display:grid;gap:30px}.w08 .zwei .blk+.blk{padding-top:30px;border-top:1px solid var(--linie)}
.w08b{aspect-ratio:4/4.7}
.w08b>.ph img{transform:scale(calc(1.1 - .1 * var(--p,1)))}
.w08b .marke{position:absolute;z-index:3;color:var(--weiss)}
.w08b .marke.lu{left:22px;bottom:22px}.w08b .marke.ro{right:22px;top:22px}
@media (max-width:860px){.w08{grid-template-columns:1fr}.w08b{order:-1;aspect-ratio:4/5}.w08b .marke.lu{top:20px;bottom:auto}.w08b .marke.ro{bottom:20px;top:auto}}'''))

F.append(('09', 'Im Plakatrahmen', 'Der Schnitt sitzt auf einem warmweissen Blatt wie auf den Plakaten des Hauses: oben die Kopfzeile mit Haus und Adresse, unten Titel und beide Texte in dunkler Schrift.',
'Bewegung: beide Bilder ziehen von 110 auf 100 Prozent · Handy: Blatt schmal, Texte untereinander',
'<div class="w09"><div class="blatt"><div class="kz"><span>Walk on the Wild Side</span><span>Haasemannstraße 13 · Linden</span></div>%s<div class="fuss">%s<div class="zwei">%s%s</div></div></div></div>' % (
    sx('w09b', ('t08', '40% 45%', 1000), ('ecke', '62% 50%', 1600), ('v', 57, 43), ('h', 55, 45)),
    titel(), blk(ABEND, kn='dunkel'), blk(HAUS, kn='dunkel leer')),
'''.w09{max-width:1220px;margin:0 auto;padding:0 var(--rand)}
.w09 .blatt{background:var(--weiss);color:var(--nacht);padding:clamp(14px,1.8vw,26px);border-radius:4px;box-shadow:0 40px 80px -40px rgba(0,0,0,.9)}
.w09 .kz{display:flex;justify-content:space-between;gap:16px;font:400 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;padding:2px 2px 14px}
.w09b{aspect-ratio:16/8.4;border-radius:2px!important}
.w09b>.ph img{transform:scale(calc(1.1 - .1 * var(--p,1)))}
.w09 .fuss{padding:clamp(28px,4vw,52px) clamp(6px,2vw,30px) clamp(16px,2vw,24px);display:flex;flex-direction:column;align-items:center;gap:clamp(26px,3.4vw,44px);text-align:center}
.w09 .zwei{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,72px);text-align:left;width:100%}
.w09 .tx{color:rgba(22,21,26,.74)}.w09 .mono{color:rgba(22,21,26,.62)}.w09 .mono.e{color:#B15736}
.w09 .knopf.leer{background:transparent;color:var(--nacht);box-shadow:inset 0 0 0 1px rgba(22,21,26,.3)}
@media (max-width:860px){.w09b{aspect-ratio:4/5}.w09 .zwei{grid-template-columns:1fr;gap:30px}.w09 .kz{flex-direction:column;gap:8px}}'''))

F.append(('10', 'Hochformat in der Mitte', 'Ein einziges hohes Bild in der Mitte, schräg geteilt. Der Abend lehnt links daran, das Haus rechts, so sitzt jeder Text an seiner Hälfte.',
'Bewegung: beide Bilder ziehen von 110 auf 100 Prozent · Handy: Bild oben, Texte darunter',
'<div class="w10"><div class="kopf">%s</div><div class="reihe">%s%s%s</div></div>' % (
    titel(), blk(ABEND, 'rb'), sx('w10b', ('t01', '30% 42%', 1600), ('theke', '70% 34%', 1000), ('v', 64, 36), ('v', 62, 38)), blk(HAUS)),
'''.w10 .reihe{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,3.4vw,60px);align-items:center;padding:0 var(--rand)}
.w10b{aspect-ratio:3/4.3}
.w10b>.ph img{transform:scale(calc(1.1 - .1 * var(--p,1)))}
.w10 .rb{align-items:flex-end;text-align:right}
@media (max-width:860px){.w10 .reihe{grid-template-columns:1fr;gap:34px}.w10b{order:-1;aspect-ratio:4/5.2}.w10 .rb{align-items:flex-start;text-align:left}}'''))

F.append(('11', 'Mehrere Bilder je Seite', 'Jede Hälfte zeigt drei Bilder statt einem: links Tafel, Gläser und Kerzen, rechts Hausecke, Theke und Schild. Die schräge Naht schneidet durch beide Gruppen, die Texte stehen darunter.',
'Bewegung: die beiden Gruppen rücken beim Hereinscrollen an der Naht zusammen · Handy: Kante quer, Gruppen oben und unten',
'<div class="sx w11" data-p><div class="gr l" style="--cd:%s;--cm:%s">%s%s%s</div><div class="gr r" style="--cd:%s;--cm:%s">%s%s%s</div>%s%s%s</div>%s' % (
    poly(('v', 57, 43))[0], poly(('h', 53, 47))[0], fig('t01', 'g1', 1600, '50% 42%'), fig('glaeser', 'g2'), fig('kerze2', 'g3'),
    poly(('v', 57, 43))[1], poly(('h', 53, 47))[1], fig('ecke', 'g1', 1600, '60% 50%'), fig('theke', 'g2', 1000, '50% 32%'), fig('schildnacht', 'g3'),
    naht([(57, 0, 43, 100)], 'd'), naht([(0, 53, 100, 47)], 'm'), tafel(), unter()),
'''.w11{margin:0 var(--rand);height:min(90svh,840px);min-height:600px;background:var(--bg)!important}
.w11 .gr{position:absolute;inset:0;display:grid;gap:6px;clip-path:var(--cd)}
.w11 .gr .ph{border-radius:0}
.w11 .gr.l{grid-template-columns:32fr 26fr 42fr;grid-template-rows:1fr 1fr;grid-template-areas:"a b ." "a c .";transform:translateX(calc((1 - var(--p,1)) * -26px))}
.w11 .gr.r{grid-template-columns:42fr 26fr 32fr;grid-template-rows:1fr 1fr;grid-template-areas:". b a" ". c a";transform:translateX(calc((1 - var(--p,1)) * 26px))}
.w11 .g1{grid-area:a}.w11 .g2{grid-area:b}.w11 .g3{grid-area:c}
@media (max-width:860px){div.w11{height:980px}.w11 .gr{clip-path:var(--cm)}
.w11 .gr.l{grid-template-columns:1fr 1fr;grid-template-rows:34fr 21fr 45fr;grid-template-areas:"a a" "b c" ". .";transform:translateY(calc((1 - var(--p,1)) * -20px))}
.w11 .gr.r{grid-template-columns:1fr 1fr;grid-template-rows:45fr 21fr 34fr;grid-template-areas:". ." "b c" "a a";transform:translateY(calc((1 - var(--p,1)) * 20px))}}'''))

F.append(('12', 'Zeigen schiebt die Kante', 'Wer auf eine Hälfte zeigt, gibt ihr mehr Raum: die Naht weicht zur anderen Seite, der Titel reist mit. Der Rahmen antwortet auf die Maus, ohne dass etwas springt.',
'Bewegung: die Naht weicht beim Zeigen zur Seite (schräges Feld, nur transform) · Handy: Antippen einer Hälfte, sonst feste Kante quer',
'<div class="sx w12 tuerrahmen" data-zu="">%s%s%s<div class="trag">%s</div>%s%s</div>' % (
    fig('t01', 'l g gu', 1600, '40% 42%', 'none', poly(('h', 56, 44))[0]), tuer('theke', '62% 34%', 1000, 'g gu'),
    fig('theke', 'r g nurhandy', 1000, '62% 34%', 'none', poly(('h', 56, 44))[1]), tafel(),
    blk(ABEND, 'o lu'), blk(HAUS, 'o ru')),
'''.w12{margin:0 var(--rand);height:min(94svh,860px);min-height:620px;--f:0}
.w12[data-zu="l"]{--f:.15}.w12[data-zu="r"]{--f:-.15}
.w12 .tuer,.w12 .tuer-in,.w12 .trag{transition:transform 1s var(--k)}
.w12 .o.ru{max-width:320px}'''))

F.append(('13', 'Die Naht zeichnet sich', 'Erst stehen die beiden Bilder nebeneinander, dann zieht sich die Linie in Kerzenfarbe beim Scrollen von oben nach unten durch den Rahmen, als würde jemand den Schnitt mit dem Stift ziehen.',
'Bewegung: die Linie wächst mit dem Scrollen (scale) · Handy: Linie quer, wächst von links',
sx('w13', ('t08', '36% 45%', 1000), ('fassade', '60% 50%', 1600), ('v', 58, 42), ('h', 53, 47),
   '<i class="strich"></i>' + tafel() + blk(ABEND, 'o lu') + blk(HAUS, 'o ro'), 'g gu', 'g go', linie=False),
'''.w13{margin:0 var(--rand);height:min(94svh,880px);--wink:15.88deg;--lang:104%}
.w13 .strich{position:absolute;z-index:2;left:58%;top:0;width:2px;margin-left:-1px;height:var(--lang);background:var(--kerze);transform-origin:50% 0;
transform:rotate(var(--wink)) scaleY(clamp(.12,calc(var(--p,1) * 1.5),1))}
@media (max-width:860px){.w13 .strich{left:0;top:53%;width:var(--lang);height:2px;margin:-1px 0 0;transform-origin:0 50%;
transform:rotate(var(--wink)) scaleX(clamp(.12,calc(var(--p,1) * 1.5),1))}}'''))

F.append(('14', 'Zwei Scherben', 'Die beiden Hälften berühren sich nicht: zwischen ihnen bleibt ein schmaler schräger Spalt, durch den der Grund der Seite scheint. Beim Scrollen gleiten sie in die gleiche Höhe.',
'Bewegung: die Scherben gleiten gegeneinander in die gleiche Höhe · Handy: Spalt quer',
'<div class="kopf">%s</div>' % titel() + '<div class="sx w14" data-p>%s%s%s%s</div>' % (
    fig('t01', 'l g gu', 1600, '38% 42%', 'polygon(0 0,55% 0,44% 100%,0 100%)', 'polygon(0 0,100% 0,100% 50%,0 57%)'),
    fig('ecke', 'r g go', 1600, '64% 50%', 'polygon(59% 0,100% 0,100% 100%,48% 100%)', 'polygon(0 62%,100% 55%,100% 100%,0 100%)'),
    blk(ABEND, 'o lu'), blk(HAUS, 'o ro')),
'''.w14{margin:0 var(--rand);height:min(88svh,820px);min-height:600px;background:none!important;overflow:visible!important}
.w14>.l{transform:translateY(calc((1 - var(--p,1)) * -46px))}
.w14>.r{transform:translateY(calc((1 - var(--p,1)) * 46px))}
@media (max-width:860px){.w14{height:1240px}.w14>.l{transform:translateX(calc((1 - var(--p,1)) * -26px))}.w14>.r{transform:translateX(calc((1 - var(--p,1)) * 26px))}}'''))

F.append(('15', 'Titel quer drüber', 'Ohne Tafel: der Titel steht gross und frei über beiden Bildern, die Naht läuft hinter ihm durch. Die beiden Zeilen schieben sich beim Hereinscrollen von links und rechts zusammen. Die Texte stehen darunter.',
'Bewegung: die zwei Titelzeilen gleiten von beiden Seiten an ihren Platz · Handy: Titel kleiner, Kante quer',
sx('w15', ('anstossen', '42% 40%', 1600), ('ecke', '62% 50%', 1600), ('v', 56, 44), ('h', 54, 46),
   '<i class="schleier"></i><h2 class="ti riesig"><span>Culinarium im</span><span>Walk on the Wild Side.</span></h2>') + unter(),
'''.w15{margin:0 var(--rand);height:min(86svh,800px);min-height:560px}
.w15 .schleier{position:absolute;inset:0;z-index:1;background:radial-gradient(ellipse 70% 60% at 50% 50%,rgba(14,12,16,.62),rgba(14,12,16,.25))}
.w15 .riesig{position:absolute;z-index:3;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;font-size:clamp(46px,7.4vw,124px);line-height:.98;padding:0 var(--rand)}
.w15 .riesig span{display:block}
.w15 .riesig span:first-child{transform:translateX(calc((1 - var(--p,1)) * -80px))}
.w15 .riesig span:last-child{transform:translateX(calc((1 - var(--p,1)) * 80px))}
@media (max-width:860px){.w15{height:auto;aspect-ratio:4/5.4;min-height:0}.w15 .riesig{font-size:clamp(38px,11vw,52px)}}'''))


CSS = '''/* Gemeinsam: Rahmen mit schräger Naht */
.sx{position:relative;overflow:hidden;border-radius:var(--r);background:var(--nacht3)}
.sx>.ph{position:absolute;inset:0;border-radius:0;clip-path:var(--cd)}
.sx .ph.g::after{content:"";position:absolute;inset:0;pointer-events:none}
.sx .ph.gu::after{background:linear-gradient(0deg,rgba(14,12,16,.9),rgba(14,12,16,0) 58%)}
.sx .ph.go::after{background:linear-gradient(180deg,rgba(14,12,16,.9),rgba(14,12,16,0) 58%)}
.sx .naht{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none}
.sx .naht line{stroke:var(--kerze);stroke-width:1.6;vector-effect:non-scaling-stroke}
.sx .naht.m,.sx .nurhandy{display:none}
.sx .tafel{position:absolute;z-index:3;left:50%;top:50%;transform:translate(-50%,-50%);background:var(--nacht);padding:22px 30px 24px;border-radius:var(--r);text-align:center;width:max-content;max-width:88%}
.sx .o{position:absolute;z-index:3;max-width:400px;--in:clamp(22px,3.4vw,56px)}
.sx .o.lu{left:var(--in);bottom:var(--in)}.sx .o.lo{left:var(--in);top:var(--in)}
.sx .o.ru{right:var(--in);bottom:var(--in)}.sx .o.ro{right:var(--in);top:var(--in)}
.sx .o .tx{font-size:16.5px;max-width:38ch}
.unter{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,96px);padding:clamp(30px,5vh,52px) var(--rand) 0;max-width:1240px;margin:0 auto}
/* Wandernde Kante: das Feld schert und wandert um --f (Anteil der Breite), das Bild darin hält genau dagegen */
.tuerrahmen>.l{clip-path:none}
.tuer{position:absolute;top:0;bottom:0;left:50%;width:200%;z-index:1;overflow:hidden;transform-origin:0 50%;transform:translateX(calc(var(--f) * 50%)) skewX(-11deg)}
.tuer::after{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;margin-left:-1px;background:var(--kerze);z-index:2}
.tuer-in{position:absolute;top:0;bottom:0;left:-25%;width:50%;transform-origin:50% 50%;transform:skewX(11deg) translateX(calc(var(--f) * -100%))}
.tuer-in .ph{position:absolute;inset:0;border-radius:0}
.trag{position:absolute;inset:0;z-index:3;pointer-events:none;transform:translateX(calc(var(--f) * 100%))}
.trag .tafel{pointer-events:auto;top:36%}
@media (max-width:860px){
div.sx{height:1240px;min-height:0}
.sx>.ph{clip-path:var(--cm)}
.sx .naht.d{display:none}.sx .naht.m{display:block}
.sx .ph.l.g::after{background:linear-gradient(180deg,rgba(14,12,16,.92),rgba(14,12,16,.15) 50%)}
.sx .ph.r.g::after{background:linear-gradient(0deg,rgba(14,12,16,.92),rgba(14,12,16,.15) 50%)}
.sx .o.lu,.sx .o.lo{top:22px;bottom:auto;left:20px;right:20px}
.sx .o.ru,.sx .o.ro{bottom:22px;top:auto;left:20px;right:20px;max-width:none}
.sx .tafel{padding:16px 18px}
.unter{grid-template-columns:1fr;gap:34px}
.tuerrahmen>.l{clip-path:var(--cm)}.tuer{display:none}.trag{transform:none}.sx .nurhandy{display:block}
div.w01,div.w08b,div.w09b,div.w10b,div.w15{height:auto}}'''

JS = r'''(function () {
  // Scroll-Fortschritt je Fassung als --p (0 bis 1); nur transform und opacity hängen daran
  var els = [].slice.call(document.querySelectorAll('[data-p]'));
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function lauf() {
    var vh = innerHeight;
    els.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var p = still ? 1 : Math.min(1, Math.max(0, (vh - r.top) / (vh * .55 + r.height * .45)));
      el.style.setProperty('--p', p.toFixed(4));
    });
  }
  var t = false;
  addEventListener('scroll', function () { if (!t) { t = true; requestAnimationFrame(function () { t = false; lauf(); }); } }, { passive: true });
  addEventListener('resize', lauf); lauf();

  // 07 und 13: Winkel (und Länge) der Naht aus der wirklichen Grösse des Rahmens
  function winkel() {
    var mob = innerWidth <= 860, g = 180 / Math.PI;
    var b7 = document.querySelector('.w07').getBoundingClientRect();
    document.querySelector('.w07').style.setProperty('--wink', (-Math.atan((mob ? .06 : .28) * b7.height / b7.width) * g).toFixed(3) + 'deg');
    var e13 = document.querySelector('.w13'), b = e13.getBoundingClientRect(), dx, dy;
    if (mob) { dx = b.width; dy = .06 * b.height; e13.style.setProperty('--wink', (-Math.atan(dy / dx) * g).toFixed(3) + 'deg'); e13.style.setProperty('--lang', (Math.hypot(dx, dy) / b.width * 100).toFixed(3) + '%'); }
    else { dx = .16 * b.width; dy = b.height; e13.style.setProperty('--wink', (Math.atan(dx / dy) * g).toFixed(3) + 'deg'); e13.style.setProperty('--lang', (Math.hypot(dx, dy) / b.height * 100).toFixed(3) + '%'); }
  }
  addEventListener('resize', winkel); winkel();

  // 12: Zeigen auf eine Hälfte gibt ihr mehr Raum; Antippen ebenso
  var v12 = document.querySelector('.w12');
  function seite(e) { var r = v12.getBoundingClientRect(); return (e.clientX - r.left) / r.width < .5 ? 'l' : 'r'; }
  v12.addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse') v12.dataset.zu = seite(e); });
  v12.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') v12.dataset.zu = ''; });
  v12.addEventListener('click', function (e) { if (!e.target.closest('a')) v12.dataset.zu = seite(e); });

  // Leiste unten: aktuelle Fassung, blättern (Pfeiltasten, ?f=Nummer)
  var fk = [].slice.call(document.querySelectorAll('.fk')), akt = 0, wl = document.querySelector('[data-wl]');
  function zeige() { wl.innerHTML = '<em>' + fk[akt].dataset.nr + ' / 15</em>' + fk[akt].dataset.name; }
  function welche() {
    var y = innerHeight * .4, n = 0;
    fk.forEach(function (f, i) { if (f.getBoundingClientRect().top < y) n = i; });
    if (n !== akt) { akt = n; zeige(); }
  }
  function geh(n) { n = Math.min(fk.length - 1, Math.max(0, n)); scrollTo({ top: fk[n].getBoundingClientRect().top + scrollY - 10, behavior: 'smooth' }); }
  addEventListener('scroll', welche, { passive: true });
  document.querySelectorAll('[data-schritt]').forEach(function (b) { b.addEventListener('click', function () { geh(akt + +b.dataset.schritt); }); });
  addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') geh(akt + 1); else if (e.key === 'ArrowLeft') geh(akt - 1); });
  var q = new URLSearchParams(location.search).get('f');
  if (q !== null) setTimeout(function () { var f = document.getElementById('f' + (+q)); f && scrollTo({ top: f.getBoundingClientRect().top + scrollY - 10 }); }, 60);
  zeige();
})();'''


def main():
    teile = []
    for nr, name, satz, m, html, _css in F:
        teile.append('<!-- ============ %s ============ -->\n<section class="fk" id="f%d" data-nr="%s" data-name="%s"><b>%s</b><h2>%s</h2><p>%s</p><p class="m">%s</p></section>\n%s'
                     % (nr, int(nr), nr, E(name), nr, E(name), E(satz), E(m), html))
    s = '''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Culinarium · Über Eck · 15 Abwandlungen</title>
<meta name="robots" content="noindex">
<style>
/* Culinarium · Abschnitt «Abend und Haus», 15 Abwandlungen von «Über Eck», 26.10.2026. Gebaut von ebenen_wahl3.py.
   Nur Wahlseite. Bewegung nur transform und opacity, nichts startet unsichtbar. */
%s
%s
%s
</style>
</head>
<body>
<header class="wk">
  <p class="mono e">Culinarium · Startseite · Abschnitt unter dem Auftakt</p>
  <h1>Über Eck: 15 Abwandlungen</h1>
  <p>Ganz oben als 00 die Nummer 2 aus der letzten Runde. Darunter 15 Abwandlungen: immer zwei Bilder mit schräger Naht in Kerzenfarbe, anders sind Winkel, Richtung, Rahmen, wo Titel und Text stehen, wie viele Bilder und was sich bewegt. Unten in der Leiste oder mit den Pfeiltasten blätterst du weiter.</p>
</header>
%s
<nav class="wl" aria-label="Fassungen"><button type="button" data-schritt="-1" aria-label="Vorige Fassung">&#8592;</button><span data-wl></span><button type="button" data-schritt="1" aria-label="Nächste Fassung">&#8594;</button></nav>
<script>
%s
</script>
</body>
</html>
''' % (KOPF_CSS, CSS, '\n'.join('/* %s %s */\n%s' % (f[0], f[1], f[5]) for f in F) + '\n/* Text auf dem Bild braucht Höhe */\n.w00,.w02,.w03,.w05,.w06,.w07,.w12,.w13,.w14{min-height:780px}', '\n\n'.join(teile), JS)
    ziel = os.path.join(HIER, 'ebenen-wahl-3.html')
    open(ziel, 'w', encoding='utf-8').write(s)
    print(ziel, len(F) - 1, 'Abwandlungen und die Ausgangsfassung')


if __name__ == '__main__':
    main()
