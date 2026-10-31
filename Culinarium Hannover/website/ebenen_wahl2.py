#!/usr/bin/env python3
"""Culinarium Hannover · Abschnitt «Abend und Haus» (unter dem Auftakt), 15 weitere Fassungen, 26.10.2026.
Robert: «15 visuelle alternative Darstellungsmöglichkeiten für den Abschnitt» (heute: «Flankiert» aus ebenen-wahl.html).
Baut ebenen-wahl-2.html. Keine Fassung wiederholt eine der 15 aus ebenen-wahl.html.
Inhalt in jeder Fassung gleich (Titel, Der Abend, Das Haus, zwei Knöpfe); anders ist nur die Anordnung.
Je Fassung ein eigener bewegter Moment, nur transform und opacity, nichts startet unsichtbar, nativer Scroll.
Aufruf: python3 website/ebenen_wahl2.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, BILD

HIER = bau.HIER
META = json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json')))

PFEIL = ('<i><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" '
         'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i>')

ABEND = dict(etikett='Der Abend', titel='Culinarium',
             satz='Ein Menü mit fünf passenden Drinks an einer langen Tafel für vierzehn Gäste, an einzelnen Wochenenden.',
             info='Freitag ab 19:00 · Samstag ab 17:00 · zuletzt 89,00 EUR', kn=('Der Abend', 'abend.html', ''))
HAUS = dict(etikett='Das Haus', titel='Walk on the Wild Side',
            satz='Culinarium findet im Walk on the Wild Side statt, einer Mixology-Bar ohne Karte in Linden, Haasemannstraße 13.',
            info='Bar: Donnerstag bis Samstag ab 19 Uhr', kn=('Das Haus', 'bar.html', 'leise'))


def knopf(t, href, cls=''):
    return '<a class="knopf %s" href="%s"><span>%s</span>%s</a>' % (cls, href, E(t), PFEIL)


def ph(k, cls='', w=1000, pos=None, laden='lazy'):
    """Foto in der kleinsten Stufe, die mindestens w breit ist."""
    stufen = sorted(META[k]['stufen'])
    s = next((x for x in stufen if x >= w), stufen[-1])
    _q, p, alt = BILD[k]
    return ('<figure class="ph %s"><img src="assets/bild/%s-%d.webp" alt="%s" loading="%s" decoding="async" style="object-position:%s"></figure>'
            % (cls, k, s, E(alt), laden, pos or p))


def blk(d, cls='', etikett=None, titel=True, kn=None):
    t, href, kc = d['kn']
    return ('<div class="blk %s"><p class="mono e">%s</p>%s<p class="tx">%s</p><p class="mono">%s</p>%s</div>'
            % (cls, E(etikett or d['etikett']), '<h3 class="ti h3">%s</h3>' % E(d['titel']) if titel else '',
               E(d['satz']), E(d['info']), knopf(t, href, kc if kn is None else kn)))


def titel(cls='h2'):
    return '<h2 class="ti %s">Culinarium im<br>Walk on the Wild Side.</h2>' % cls


# ------------------------------------------------------------------ die 15 Fassungen
F = []   # (Name, Satz, Bewegung · Handy, HTML, CSS)

F.append(('Die Empore', 'Zwei Stockwerke übereinander: oben die Tafel auf der Empore, unten die Theke. Der Titel steht auf dem Boden dazwischen, so liest man das Haus von oben nach unten.',
'Bewegung: das obere Bild wandert beim Scrollen leicht gegen die Seite · Handy: Bild und Text je Stockwerk untereinander',
'''<div class="v01" data-p>
<div class="stock oben">%s%s</div>
<div class="boden"><i></i>%s<i></i></div>
<div class="stock unten">%s%s</div></div>''' % (
    ph('t01', w=1600, pos='50% 46%'), blk(ABEND, etikett='Oben · die Tafel auf der Empore'), titel(),
    ph('theke', pos='50% 34%'), blk(HAUS, etikett='Unten · die Theke')),
'''.v01{margin:0 var(--rand)}
.v01 .stock{position:relative;height:clamp(440px,66vh,660px);border-radius:var(--r);overflow:hidden}
.v01 .stock>.ph{position:absolute;inset:-7% 0;border-radius:0}
.v01 .oben>.ph img{transform:translateY(calc((var(--p,.5) - .5) * -70px))}
.v01 .stock::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,12,16,.86),rgba(14,12,16,.5) 34%,rgba(14,12,16,0) 64%)}
.v01 .unten::after{background:linear-gradient(270deg,rgba(14,12,16,.86),rgba(14,12,16,.5) 34%,rgba(14,12,16,0) 64%)}
.v01 .stock .blk{position:absolute;z-index:2;bottom:clamp(24px,5vh,52px);left:clamp(22px,3.6vw,60px);max-width:430px}
.v01 .unten .blk{left:auto;right:clamp(22px,3.6vw,60px)}
.v01 .boden{display:flex;align-items:center;gap:clamp(18px,3vw,44px);padding:clamp(26px,4.4vh,44px) 0;text-align:center}
.v01 .boden i{flex:1;height:1px;background:var(--linie)}
@media (max-width:860px){.v01 .stock{height:auto}.v01 .stock>.ph{position:relative;inset:auto;height:54vh;border-radius:var(--r)}.v01 .stock::after{display:none}
.v01 .stock .blk{position:relative;inset:auto;padding:22px 2px 0;max-width:none}.v01 .boden i{display:none}.v01 .boden{justify-content:center}}'''))

F.append(('Über Eck', 'Das Haus steht an einer Ecke in Linden, also teilt eine schräge Kante den Rahmen: links die Tafel, rechts die Hausecke. Eine Linie in Kerzenfarbe läuft die Naht entlang, der Titel sitzt quer darauf.',
'Bewegung: beide Bilder ziehen beim Hereinscrollen von 110 auf 100 Prozent · Handy: die Kante liegt quer, Abend oben, Haus unten',
'''<div class="v02" data-p>%s%s
<svg class="naht d" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><line x1="58" y1="0" x2="42" y2="100"/></svg>
<svg class="naht m" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><line x1="0" y1="58" x2="100" y2="42"/></svg>
<div class="tafel">%s</div>%s%s</div>''' % (
    ph('t08', 'l', pos='34% 45%'), ph('ecke', 'r', w=1600, pos='62% 50%'), titel(),
    blk(ABEND, 'abend'), blk(HAUS, 'haus')),
'''.v02{position:relative;margin:0 var(--rand);height:min(94svh,880px);min-height:640px;border-radius:var(--r);overflow:hidden;background:var(--nacht3)}
.v02>.ph{position:absolute;inset:0;border-radius:0}
.v02>.ph img{transform:scale(calc(1.1 - .1 * var(--p,1)))}
.v02 .l{clip-path:polygon(0 0,58% 0,42% 100%,0 100%)}
.v02 .r{clip-path:polygon(58% 0,100% 0,100% 100%,42% 100%)}
.v02>.ph::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(14,12,16,.9),rgba(14,12,16,0) 58%)}
.v02 .r::after{background:linear-gradient(180deg,rgba(14,12,16,.9),rgba(14,12,16,0) 58%)}
.v02 .naht{position:absolute;inset:0;width:100%;height:100%;z-index:2}
.v02 .naht line{stroke:var(--kerze);stroke-width:1.6;vector-effect:non-scaling-stroke}
.v02 .naht.m{display:none}
.v02 .tafel{position:absolute;z-index:3;left:50%;top:50%;transform:translate(-50%,-50%);background:var(--nacht);padding:22px 30px 24px;border-radius:var(--r);text-align:center;width:max-content;max-width:88%}
.v02 .blk{position:absolute;z-index:3;max-width:400px}
.v02 .abend{left:clamp(22px,3.4vw,56px);bottom:clamp(24px,4.6vh,48px)}
.v02 .haus{right:clamp(22px,3.4vw,56px);top:clamp(24px,4.6vh,48px)}
@media (max-width:860px){.v02{height:1240px;min-height:0}.v02 .l{clip-path:polygon(0 0,100% 0,100% 42%,0 58%)}.v02 .r{clip-path:polygon(0 58%,100% 42%,100% 100%,0 100%)}
.v02 .l::after{background:linear-gradient(180deg,rgba(14,12,16,.92),rgba(14,12,16,.2) 50%)}.v02 .r::after{background:linear-gradient(0deg,rgba(14,12,16,.92),rgba(14,12,16,.2) 50%)}
.v02 .naht.d{display:none}.v02 .naht.m{display:block}.v02 .abend{top:22px;bottom:auto;left:20px;right:20px}.v02 .haus{bottom:22px;top:auto;left:20px;right:20px}.v02 .tafel{padding:16px 18px}}'''))

F.append(('Zwei Abzüge', 'Zwei Abzüge liegen auf dem Tisch, einer vom Abend, einer vom Haus, mit Bildzeile wie von Hand. Daneben der Text als ein Block. Beim Hereinscrollen schieben sie sich auseinander, als hätte jemand sie hingelegt.',
'Bewegung: die Abzüge fächern auf (Drehung und Weg) · Handy: Abzüge oben, Text darunter',
'''<div class="v03" data-p><div class="text">%s<div class="zwei">%s%s</div></div>
<div class="tisch"><div class="abzug a1">%s<p>Der Abend · an der Tafel</p></div><div class="abzug a2">%s<p>Das Haus · Haasemannstraße 13</p></div></div></div>''' % (
    titel(), blk(ABEND), blk(HAUS), ph('t12', pos='50% 42%'), ph('theke', pos='50% 36%')),
'''.v03{display:grid;grid-template-columns:minmax(0,.86fr) minmax(0,1.14fr);gap:clamp(28px,4.4vw,80px);align-items:center;padding:0 var(--rand)}
.v03 .text{display:flex;flex-direction:column;gap:34px}
.v03 .zwei{display:grid;gap:30px}
.v03 .zwei .blk+.blk{padding-top:30px;border-top:1px solid var(--linie)}
.v03 .tisch{position:relative;aspect-ratio:1/1.05}
.v03 .abzug{position:absolute;width:60%;background:var(--weiss);padding:12px 12px 0;border-radius:3px;box-shadow:0 34px 70px -26px rgba(0,0,0,.85)}
.v03 .abzug .ph{aspect-ratio:4/5;border-radius:1px}
.v03 .abzug p{font:400 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:rgba(22,21,26,.7);padding:16px 2px 18px}
.v03 .a1{left:2%;top:2%;transform:translateX(calc(16% * (1 - var(--p,1)))) rotate(calc(-1deg - 4deg * var(--p,1)))}
.v03 .a2{right:2%;top:16%;transform:translateX(calc(-16% * (1 - var(--p,1)))) rotate(calc(1deg + 4deg * var(--p,1)))}
@media (max-width:860px){.v03{grid-template-columns:1fr}.v03 .tisch{order:-1;aspect-ratio:1/1.12}.v03 .abzug{width:64%}}'''))

F.append(('Erst der Abend, dann das Haus', 'Links steht ein Bild, rechts scrollt der Text: zuerst der Abend mit der Tafel. Kommt der zweite Teil, tauscht das Bild an derselben Stelle zur Theke. Man liest die beiden nacheinander, nicht gegeneinander.',
'Bewegung: Bild tauscht beim Scrollen an derselben Stelle (Deckkraft) · Handy: jedes Bild steht über seinem Text, nichts klebt',
'''<div class="v04" data-p="sticky"><div class="buehne"><div class="st">%s%s</div></div>
<div class="spalte"><div class="schritt">%s%s%s</div><div class="schritt">%s%s</div></div></div>''' % (
    ph('tafelleer', 'a', w=1600), ph('theke', 'b', pos='50% 36%'),
    titel(), ph('tafelleer', 'nurhandy'), blk(ABEND), ph('theke', 'nurhandy', pos='50% 36%'), blk(HAUS)),
'''.v04{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(28px,4.4vw,80px);padding:0 var(--rand)}
.v04 .st{position:sticky;top:6svh;height:88svh}
.v04 .st .ph{position:absolute;inset:0}
.v04 .st .b{opacity:clamp(0,(var(--p,0) - .42) * 6,1)}
.v04 .schritt{min-height:88svh;display:flex;flex-direction:column;justify-content:center;gap:34px}
.v04 .nurhandy{display:none}
@media (max-width:860px){.v04{grid-template-columns:1fr}.v04 .buehne{display:none}.v04 .nurhandy{display:block;aspect-ratio:4/5}.v04 .schritt{min-height:0;gap:22px;padding-bottom:34px}}'''))

F.append(('Kino', 'Ein Breitbild wie im Kino, randlos von Kante zu Kante. Oben im schwarzen Balken der Titel, unten wie Untertitel die beiden Texte, Abend und Haus, durch einen Strich getrennt.',
'Bewegung: das Breitbild fährt beim Scrollen langsam zurück (Zoom 112 auf 100) · Handy: Bild 16 zu 10, Texte untereinander',
'''<div class="v05" data-p><div class="ob">%s</div>%s<div class="ut">%s<i class="strich"></i>%s</div></div>''' % (
    titel(), ph('anstossen', 'leinwand', w=2400, pos='50% 52%'), blk(ABEND, 'mitte'), blk(HAUS, 'mitte')),
'''.v05{background:#0C0B0E;padding:clamp(40px,7vh,72px) 0}
.v05 .ob{text-align:center;padding:0 var(--rand) clamp(28px,4.4vh,46px)}
.v05 .leinwand{aspect-ratio:2.39/1;border-radius:0}
.v05 .leinwand img{transform:scale(calc(1.12 - .12 * var(--p,1)))}
.v05 .ut{display:grid;grid-template-columns:1fr 1px 1fr;gap:clamp(24px,4vw,72px);padding:clamp(32px,5vh,56px) var(--rand) 0;max-width:1240px;margin:0 auto}
.v05 .strich{background:var(--linie)}
@media (max-width:860px){.v05 .leinwand{aspect-ratio:16/10}.v05 .ut{grid-template-columns:1fr;gap:30px}.v05 .strich{height:1px}}'''))

F.append(('Wand um den Titel', 'Viele Bilder dicht an dicht, der Titel mitten in der Wand. Links die Bilder vom Abend mit seinem Text, rechts die Bilder aus der Bar mit ihrem. Kaum Leerraum, man sieht alles auf einmal.',
'Bewegung: die Wand rückt beim Hereinscrollen zusammen (jedes Bild ein Stück zur Mitte) · Handy: zwei Spalten, Texte über volle Breite',
'''<div class="v06" data-p><div class="wand">
%s%s%s<div class="tt">%s</div>%s%s%s%s
<div class="ab">%s</div><div class="hs">%s</div></div></div>''' % (
    ph('t01', 'p1', pos='50% 40%'), ph('glaeser', 'p2'), ph('kerze2', 'p5'), titel(), ph('theke', 'p3', pos='50% 32%'),
    ph('schildnacht', 'p4'), ph('flaschen', 'p6'), ph('anstossen', 'p7', pos='50% 40%') + ph('bar', 'p8'),
    blk(ABEND), blk(HAUS)),
'''.v06{padding:0 var(--rand);overflow-x:clip}
.v06 .wand{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));grid-template-rows:clamp(170px,17vw,250px) clamp(170px,17vw,250px) auto;gap:8px;
grid-template-areas:"p1 p2 tt tt p3 p4" "p1 p5 tt tt p6 p4" "ab ab p7 p8 hs hs"}
.v06 .ph{transform:translate(calc(var(--dx,0px) * (1 - var(--p,1))),calc(var(--dy,0px) * (1 - var(--p,1))))}
.v06 .p1{grid-area:p1;--dx:-46px}.v06 .p2{grid-area:p2;--dx:-26px;--dy:-20px}.v06 .p5{grid-area:p5;--dx:-26px;--dy:20px}.v06 .p3{grid-area:p3;--dx:26px;--dy:-20px}
.v06 .p4{grid-area:p4;--dx:46px}.v06 .p6{grid-area:p6;--dx:26px;--dy:20px}.v06 .p7{grid-area:p7;--dy:40px;min-height:250px}.v06 .p8{grid-area:p8;--dy:40px;min-height:250px}
.v06 .tt{grid-area:tt;display:grid;place-items:center;text-align:center;padding:20px}
.v06 .ab{grid-area:ab;padding:26px 26px 26px 4px;align-self:center}.v06 .hs{grid-area:hs;padding:26px 4px 26px 26px;align-self:center}
@media (max-width:860px){.v06 .wand{grid-template-columns:1fr 1fr;grid-template-rows:none;grid-template-areas:"tt tt" "p1 p5" "p2 p7" "ab ab" "p3 p4" "p6 p8" "hs hs"}
.v06 .ph{aspect-ratio:4/5;min-height:0!important}.v06 .tt{padding:10px 0 22px}.v06 .ab,.v06 .hs{padding:22px 2px 30px}}'''))

F.append(('Vorder- und Rückseite', 'Eine grosse Karte: vorn der Abend, hinten das Haus. Antippen dreht sie um. Unter der Karte steht, was auf der Rückseite wartet, damit niemand etwas verpasst.',
'Bewegung: die Karte dreht sich um ihre senkrechte Achse (rotateY) · Handy: Bild oben, Text unten, Drehen bleibt',
'''<div class="v07" data-seite="vorn"><div class="kopf">%s</div><div class="karte"><div class="dreh">
<div class="seite vorn">%s<div class="innen">%s<button type="button" class="wende" data-wende>Umdrehen: das Haus</button></div></div>
<div class="seite hinten">%s<div class="innen">%s<button type="button" class="wende" data-wende>Umdrehen: der Abend</button></div></div>
</div></div><p class="mono hinweis">Vorn der Abend, hinten das Haus, Haasemannstraße 13</p></div>''' % (
    titel(), ph('t01', w=1600, pos='50% 42%'), blk(ABEND), ph('ws00', pos='50% 50%'), blk(HAUS, kn='')),
'''.v07 .karte{perspective:2000px;max-width:1240px;margin:0 auto;padding:0 var(--rand)}
.v07 .dreh{display:grid;transform-style:preserve-3d;-webkit-transform-style:preserve-3d;transition:transform 1.1s var(--k)}
.v07[data-seite="hinten"] .dreh{transform:rotateY(180deg)}
.v07 .seite{grid-area:1/1;display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);border-radius:calc(var(--r) + 6px);overflow:hidden;background:var(--nacht);backface-visibility:hidden;-webkit-backface-visibility:hidden;box-shadow:0 40px 80px -40px rgba(0,0,0,.9)}
.v07 .hinten{transform:rotateY(180deg);background:var(--schiefer)}
.v07 .seite{transition:opacity 0s .5s}
.v07 .hinten,.v07[data-seite="hinten"] .vorn{opacity:0;pointer-events:none}
.v07[data-seite="hinten"] .hinten{opacity:1;pointer-events:auto}
.v07 .seite .ph{border-radius:0;min-height:min(70vh,600px)}
.v07 .innen{display:flex;flex-direction:column;justify-content:center;gap:30px;padding:clamp(28px,4vw,60px)}
.v07 .wende{all:unset;cursor:pointer;align-self:flex-start;font:400 12.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--kerze);padding:6px 0;border-bottom:1px solid currentColor}
.v07 .hinweis{text-align:center;margin-top:22px}
@media (max-width:860px){.v07 .seite{grid-template-columns:1fr}.v07 .seite .ph{min-height:0;aspect-ratio:4/4.2}.v07 .innen{padding:24px 20px 28px}}'''))

F.append(('Hinauf zur Tafel', 'Drei Bilder steigen an wie eine Treppe: das Schild an der Strasse klein, die Theke mittel, die Tafel oben gross. Der Titel sitzt in der freien Ecke. So steht der Weg des Gastes schon im Bild, bevor man liest.',
'Bewegung: die Stufen steigen beim Hereinscrollen unterschiedlich weit herauf · Handy: Tafel gross oben, Theke und Schild nebeneinander darunter',
'''<div class="v08" data-p><div class="ecke">%s<p class="tx">Von der Strasse an die Theke, von der Theke an die lange Tafel.</p></div>
<div class="stufe s1">%s<p class="mono">Die Strasse</p></div>
<div class="stufe s2">%s<p class="mono">Die Theke</p></div>
<div class="stufe s3">%s<p class="mono">Die Tafel</p></div>
<div class="t2">%s</div><div class="t3">%s</div></div>''' % (
    titel(), ph('schildnacht'), ph('theke', pos='50% 36%'), ph('tafelleer', w=1600), blk(HAUS, etikett='Das Haus'), blk(ABEND)),
'''.v08{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:clamp(14px,1.8vw,30px);row-gap:28px;padding:0 var(--rand);align-items:end}
.v08 .ecke{grid-column:1/4;grid-row:1;align-self:start;display:flex;flex-direction:column;gap:16px}
.v08 .ecke .h2{font-size:clamp(30px,3.2vw,54px)}
.v08 .ecke .tx{font-size:16px}
.v08 .stufe{display:flex;flex-direction:column;gap:12px;transform:translateY(calc((1 - var(--p,1)) * var(--h)))}
.v08 .s1 .ph{aspect-ratio:1/1}.v08 .s2 .ph{aspect-ratio:4/5}.v08 .s3 .ph{aspect-ratio:4/5.6}
.v08 .s1{grid-column:1/4;grid-row:2;--h:24px}
.v08 .s2{grid-column:4/8;grid-row:1/3;--h:60px}
.v08 .s3{grid-column:8/13;grid-row:1/3;--h:100px}
.v08 .t2{grid-column:4/8;grid-row:3;align-self:start}.v08 .t3{grid-column:8/13;grid-row:3;align-self:start}
@media (max-width:860px){.v08{grid-template-columns:1fr 1fr;row-gap:20px}.v08 .ecke{grid-column:1/3;grid-row:auto}.v08 .s3{grid-column:1/3;grid-row:auto}
.v08 .t3{grid-column:1/3;grid-row:auto;padding-bottom:16px}.v08 .s2{grid-column:1;grid-row:auto}.v08 .s1{grid-column:2;grid-row:auto}.v08 .t2{grid-column:1/3;grid-row:auto}}'''))

F.append(('Umgekehrt', 'Das Gegenteil von heute: ein grosses Hochformat in der Mitte, die Texte rechts und links daran, jeder mit einem kleinen Bild darüber. Der Abend lehnt links am Bild, das Haus rechts.',
'Bewegung: das Mittelbild zieht beim Hereinscrollen von 114 auf 100 Prozent · Handy: grosses Bild oben, die beiden Seiten untereinander',
'''<div class="v09" data-p><div class="kopf">%s</div><div class="reihe">
<div class="seite links">%s%s</div>%s<div class="seite rechts">%s%s</div></div></div>''' % (
    titel(), ph('glaeser', 'klein'), blk(ABEND, 'rechtsb'), ph('anstossen', 'gross', w=1600, pos='50% 40%'),
    ph('schildnacht', 'klein'), blk(HAUS)),
'''.v09 .reihe{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr) minmax(0,1fr);gap:clamp(24px,3.4vw,60px);align-items:center;padding:0 var(--rand)}
.v09 .gross{aspect-ratio:4/5.2}
.v09 .gross img{transform:scale(calc(1.14 - .14 * var(--p,1)))}
.v09 .seite{display:flex;flex-direction:column;gap:26px}
.v09 .klein{aspect-ratio:4/3}
.v09 .links{align-items:flex-end}.v09 .links .klein{width:100%}
.v09 .rechtsb{align-items:flex-end;text-align:right}
@media (max-width:860px){.v09 .reihe{grid-template-columns:1fr;gap:34px}.v09 .gross{order:-1}.v09 .links,.v09 .rechtsb{align-items:flex-start;text-align:left}.v09 .seite{gap:18px}}'''))

F.append(('Aufgeschoben', 'Zwei Blätter wie zwei Schubladen: Zuerst liegt der Abend offen, vom Haus sieht man nur die Kante mit seinem Namen. Beim Scrollen schiebt sich das Haus darüber.',
'Bewegung: das zweite Blatt schiebt sich seitwärts herein (Weg), seine Kante ist von Anfang an da · Handy: beide Blätter untereinander, nichts klebt',
'''<div class="v10" data-p="sticky"><div class="st">
<div class="blatt b1">%s<div class="innen">%s%s</div></div>
<div class="blatt b2"><div class="zunge"><span>Das Haus · Walk on the Wild Side</span></div><div class="innen">%s</div>%s</div>
</div></div>''' % (ph('t12', w=1600, pos='50% 42%'), titel(), blk(ABEND), blk(HAUS), ph('theke', pos='50% 36%')),
'''.v10{height:230vh;margin:0 var(--rand)}
.v10 .st{position:sticky;top:6svh;height:88svh;overflow:hidden;border-radius:var(--r)}
.v10 .blatt{position:absolute;inset:0;display:grid;border-radius:var(--r);overflow:hidden}
.v10 .b1{grid-template-columns:minmax(0,1.05fr) minmax(0,1fr) 9%;background:var(--nacht)}
.v10 .b2{grid-template-columns:9% minmax(0,1fr) minmax(0,1.05fr);background:var(--schiefer);box-shadow:-34px 0 70px -24px rgba(0,0,0,.8);
transform:translateX(calc(91% * (1 - clamp(0,(var(--p,0) - .12) / .56,1))))}
.v10 .blatt .ph{border-radius:0}
.v10 .innen{display:flex;flex-direction:column;justify-content:center;gap:30px;padding:clamp(28px,3.6vw,60px)}
.v10 .zunge{display:grid;place-items:center;border-right:1px solid var(--linie)}
.v10 .zunge span{writing-mode:vertical-rl;transform:rotate(180deg);font:400 12.5px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--weiss);white-space:nowrap}
@media (max-width:860px){.v10{height:auto}.v10 .st{position:relative;top:0;height:auto;overflow:visible;display:grid;gap:14px}.v10 .blatt{position:relative;grid-template-columns:1fr!important;transform:none!important;box-shadow:none}
.v10 .blatt .ph{aspect-ratio:4/4.4}.v10 .zunge{display:none}.v10 .b2 .ph{order:-1}.v10 .innen{padding:24px 20px 28px}}'''))

F.append(('Zwei Untersetzer', 'Zwei runde Bilder wie Untersetzer auf dem Tresen: links der Abend, rechts die Bar. Beim Hereinscrollen rücken sie zusammen, bis sie sich berühren, wie zwei Gläser beim Anstossen.',
'Bewegung: die beiden Kreise rücken zusammen (Weg) · Handy: Kreise etwas kleiner, Texte untereinander',
'''<div class="v11" data-p><div class="kopf">%s</div><div class="paar"><div class="kreis k1">%s</div><div class="kreis k2">%s</div></div>
<div class="texte">%s%s</div></div>''' % (titel(), ph('t08', pos='50% 42%'), ph('theke', pos='50% 34%'), blk(ABEND, 'mitte'), blk(HAUS, 'mitte')),
'''.v11{overflow-x:clip}
.v11 .paar{display:flex;justify-content:center;padding:0 var(--rand)}
.v11 .kreis{width:min(40vw,560px);aspect-ratio:1}
.v11 .kreis .ph{height:100%;border-radius:50%;box-shadow:0 0 0 1px rgba(239,118,73,.5),0 40px 80px -40px rgba(0,0,0,.9)}
.v11 .k1{transform:translateX(calc(3% + 70px * (var(--p,1) - 1)))}
.v11 .k2{transform:translateX(calc(-3% - 70px * (var(--p,1) - 1)))}
.v11 .texte{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,96px);max-width:1080px;margin:clamp(30px,5vh,56px) auto 0;padding:0 var(--rand)}
@media (max-width:860px){.v11 .kreis{width:48vw}.v11 .texte{grid-template-columns:1fr;gap:34px}}'''))

F.append(('Buchrücken', 'Der Titel steht senkrecht am linken Rand wie auf einem Buchrücken. Daneben ein Breitbild von den Leuten vor der Bar und darunter die beiden Texte nebeneinander.',
'Bewegung: der senkrechte Titel wandert beim Scrollen langsam gegen die Seite · Handy: Titel waagerecht oben',
'''<div class="v12" data-p>%s<div class="inhalt">%s<div class="zwei">%s%s</div></div></div>''' % (
    titel('ruecken'), ph('trio2', 'breit', w=1600, pos='50% 45%'), blk(ABEND), blk(HAUS)),
'''.v12{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(24px,3.4vw,64px);padding:0 var(--rand)}
.v12 .ruecken{writing-mode:vertical-rl;transform:rotate(180deg) translateY(calc((var(--p,.5) - .5) * 70px));font-size:clamp(46px,5.6vw,92px);line-height:.98;white-space:nowrap;align-self:center}
.v12 .inhalt{display:flex;flex-direction:column;gap:clamp(26px,4vh,44px)}
.v12 .breit{aspect-ratio:16/9.4}
.v12 .zwei{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,3.6vw,64px)}
.v12 .zwei .blk+.blk{padding-left:clamp(24px,3.6vw,64px);border-left:1px solid var(--linie)}
@media (max-width:860px){.v12{grid-template-columns:1fr}.v12 .ruecken{writing-mode:horizontal-tb;transform:none;white-space:normal;font-size:clamp(34px,9vw,44px)}
.v12 .zwei{grid-template-columns:1fr}.v12 .zwei .blk+.blk{padding-left:0;border-left:0;padding-top:28px;border-top:1px solid var(--linie)}}'''))

F.append(('Ein Abend als Band', 'Ein Band zum Seitwärts-Ziehen: vorn der Titel mit dem Abend, dann Bilder von der Tafel, in der Mitte das Haus als eigene Karte, dann Bilder aus der Bar. Unten zeigt ein Strich, wie weit man ist.',
'Bewegung: der Laufbalken folgt dem Band · Handy: Wischen mit dem Finger, Karten fast bildschirmbreit',
'''<div class="v13"><div class="band" tabindex="0" aria-label="Bilder vom Abend und aus der Bar">
<div class="karte">%s%s</div>%s%s%s%s<div class="karte k2">%s</div>%s%s%s%s</div>
<div class="fuss"><div class="lauf"><i></i></div><button type="button" data-band="-1" aria-label="Zurück"><svg viewBox="0 0 24 24"><path d="M19 12H6M11 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button><button type="button" data-band="1" aria-label="Weiter"><svg viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button></div></div>''' % (
    titel(), blk(ABEND), ph('t01', pos='50% 40%'), ph('glaeser'), ph('anstossen', pos='50% 40%'), ph('kerze2'),
    blk(HAUS), ph('theke', pos='50% 34%'), ph('flaschen'), ph('schildnacht'), ph('barnacht')),
'''.v13 .band{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x proximity;padding:0 var(--rand);scroll-padding:0 var(--rand);scrollbar-width:none;overscroll-behavior-x:contain}
.v13 .band::-webkit-scrollbar{display:none}
.v13 .band>*{flex:0 0 auto;height:min(74svh,660px);scroll-snap-align:start}
.v13 .band>.ph{aspect-ratio:4/5.2}
.v13 .karte{width:min(420px,82vw);display:flex;flex-direction:column;justify-content:flex-end;gap:30px;padding:0 28px 6px 0}
.v13 .k2{padding-left:28px;border-left:1px solid var(--linie);margin-left:18px}
.v13 .fuss{display:flex;align-items:center;gap:8px;margin:22px var(--rand) 0}
.v13 .lauf{flex:1;height:2px;background:var(--linie);position:relative;overflow:hidden;margin-right:14px}
.v13 .lauf i{position:absolute;inset:0;background:var(--kerze);transform-origin:0 50%;transform:scaleX(var(--b,.2))}
.v13 .fuss button{all:unset;cursor:pointer;width:46px;height:46px;border-radius:50%;display:grid;place-items:center;box-shadow:inset 0 0 0 1px var(--linie)}
.v13 .fuss svg{width:19px;height:19px}
@media (max-width:860px){.v13 .band>*{height:66svh}.v13 .karte{width:84vw}.v13 .fuss button{display:none}}'''))

F.append(('Das Bild wächst', 'Oben der Titel und die beiden Texte nebeneinander, als ruhiger Block. Darunter ein Bild vom Anstossen an der Tafel, das beim Scrollen von schmal auf volle Breite aufgeht.',
'Bewegung: das Bild wächst mit dem Scrollen von 62 auf 100 Prozent (scale) · Handy: Hochformat, wächst von 80 auf 100',
'''<div class="v14" data-p><div class="oben"><div class="kopf">%s</div><div class="zwei">%s%s</div></div><div class="rahmen">%s</div></div>''' % (
    titel(), blk(ABEND, 'mitte'), blk(HAUS, 'mitte'), ph('tafelleer', w=1600, pos='50% 56%')),
'''.v14 .zwei{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,96px);max-width:1080px;margin:0 auto;padding:0 var(--rand)}
.v14 .rahmen{margin-top:clamp(36px,6vh,64px);padding:0 var(--rand)}
.v14 .rahmen .ph{aspect-ratio:2.1/1;transform-origin:50% 0;transform:scale(calc(.62 + .38 * var(--p,1)))}
@media (max-width:860px){.v14 .zwei{grid-template-columns:1fr;gap:34px}.v14 .rahmen .ph{aspect-ratio:4/4.6;transform:scale(calc(.8 + .2 * var(--p,1)))}}'''))

F.append(('Schachbrett', 'Vier gleich grosse Felder ohne Fuge: Bild, Text, Text, Bild. Der Abend auf Warmweiss neben der Tafel, das Haus auf Schiefer neben der Theke. Die zwei Farben sind die Farben der Plakate.',
'Bewegung: die Bilder wandern in ihren Feldern leicht gegenläufig · Handy: Bild, Text, Bild, Text',
'''<div class="v15" data-p><div class="feld f1">%s</div><div class="feld text hell">%s%s</div><div class="feld text schiefer">%s</div><div class="feld f4">%s</div></div>''' % (
    ph('t01', w=1600, pos='50% 42%'), titel(), blk(ABEND, kn='dunkel'), blk(HAUS), ph('theke', pos='50% 34%')),
'''.v15{display:grid;grid-template-columns:1fr 1fr;margin:0 var(--rand);border-radius:var(--r);overflow:hidden}
.v15 .feld{position:relative;overflow:hidden;min-height:clamp(420px,46vw,640px)}
.v15 .feld>.ph{position:absolute;inset:-7% 0;border-radius:0}
.v15 .f1>.ph img{transform:translateY(calc((var(--p,.5) - .5) * -60px))}
.v15 .f4>.ph img{transform:translateY(calc((var(--p,.5) - .5) * 60px))}
.v15 .text{display:flex;flex-direction:column;justify-content:center;gap:30px;padding:clamp(28px,5vw,84px)}
.v15 .hell{background:var(--weiss);color:var(--nacht)}
.v15 .hell .tx{color:rgba(22,21,26,.74)}.v15 .hell .mono{color:rgba(22,21,26,.6)}
.v15 .schiefer{background:var(--schiefer)}
@media (max-width:860px){.v15{grid-template-columns:1fr}.v15 .feld.f1,.v15 .feld.f4{min-height:62vh}.v15 .text{min-height:0;padding:30px 22px 34px}.v15 .f4{order:3}.v15 .schiefer{order:4}}'''))


# ------------------------------------------------------------------ Seite
KOPF_CSS = '''@font-face{font-family:"Fraunces";src:url(assets/schrift/fraunces-soft.woff2) format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:"Urbanist";src:url(assets/schrift/urbanist.woff2) format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:"DM Mono";src:url(assets/schrift/dmmono.woff2) format("woff2");font-weight:400;font-display:swap}
:root{--nacht:#16151A;--nacht3:#2A2831;--schiefer:#3A3845;--weiss:#FAF4F4;--kerze:#EF7649;--bg:#222028;--fg2:rgba(250,244,244,.74);--linie:rgba(250,244,244,.18);
--titel:"Fraunces",Georgia,serif;--text:"Urbanist",system-ui,sans-serif;--mono:"DM Mono",ui-monospace,monospace;--rand:clamp(16px,4.4vw,72px);--r:10px;--k:cubic-bezier(.22,.68,.26,1)}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;overflow-x:clip}
body{margin:0;background:var(--bg);color:var(--weiss);font:400 17px/1.55 var(--text);-webkit-font-smoothing:antialiased;overflow-x:clip;padding-bottom:90px}
img{display:block;max-width:100%}
a{color:inherit}
h1,h2,h3,p{margin:0}
.ti{font-family:var(--titel);font-weight:340;line-height:1;letter-spacing:-.014em;font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 144}
.h2{font-size:clamp(36px,4.4vw,72px);line-height:1}
.h3{font-size:clamp(26px,2.3vw,38px);line-height:1.04}
.tx{color:var(--fg2);font-size:18px;line-height:1.55;max-width:42ch}
.mono{font-family:var(--mono);font-size:12.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--fg2)}
.mono.e{color:var(--kerze)}
.blk{display:flex;flex-direction:column;gap:14px;align-items:flex-start}
.blk.mitte{align-items:center;text-align:center}
.ph{position:relative;margin:0;overflow:hidden;border-radius:var(--r);background:var(--nacht3)}
.ph img{width:100%;height:100%;object-fit:cover}
.knopf{display:inline-flex;align-items:center;gap:18px;height:58px;padding:0 8px 0 28px;border-radius:999px;background:var(--weiss);color:var(--nacht);font:600 14px/1 var(--text);letter-spacing:.16em;text-transform:uppercase;text-decoration:none;box-shadow:0 16px 32px -16px rgba(0,0,0,.65),inset 0 1px 0 rgba(255,255,255,.85);transition:transform .45s var(--k);margin-top:8px}
.knopf i{display:grid;place-items:center;width:42px;height:42px;border-radius:50%;background:var(--kerze);color:#fff}
.knopf svg{width:19px;height:19px}
.knopf:hover{transform:translateY(-2px)}
.knopf.leise{background:transparent;color:var(--weiss);box-shadow:inset 0 0 0 1px var(--linie)}
.knopf.leise i{background:transparent;box-shadow:inset 0 0 0 1px var(--linie)}
.knopf.dunkel{background:var(--nacht);color:var(--weiss);box-shadow:none}
.kopf{padding:0 var(--rand) clamp(30px,4.6vh,52px);text-align:center}
/* Wahlseite */
.wk{padding:56px var(--rand) 20px;max-width:1100px}
.wk h1{font:340 clamp(30px,3.4vw,50px)/1.05 var(--titel);font-variation-settings:"SOFT" 100,"opsz" 144;margin:14px 0}
.wk p{color:var(--fg2);max-width:70ch}
.fk{display:grid;grid-template-columns:auto 1fr;gap:6px 22px;padding:84px var(--rand) 30px;border-top:1px solid rgba(250,244,244,.1);margin-top:56px}
.fk b{font:400 13px/1.6 var(--mono);color:var(--kerze);letter-spacing:.08em;grid-row:span 3}
.fk h2{font:340 clamp(24px,2.2vw,32px)/1.1 var(--titel);font-variation-settings:"SOFT" 100,"opsz" 96}
.fk p{color:var(--fg2);max-width:80ch;font-size:15.5px}
.fk p.m{font-family:var(--mono);font-size:12px;letter-spacing:.06em;color:rgba(250,244,244,.5);text-transform:uppercase}
.wl{position:fixed;z-index:50;left:50%;bottom:14px;transform:translateX(-50%);display:flex;align-items:center;gap:6px;padding:6px;border-radius:14px;background:#16151A;box-shadow:0 10px 30px -10px rgba(0,0,0,.8),inset 0 0 0 1px rgba(250,244,244,.12);font:400 12.5px/1 var(--mono);letter-spacing:.05em;max-width:calc(100vw - 24px)}
.wl button{all:unset;cursor:pointer;width:34px;height:34px;display:grid;place-items:center;border-radius:9px;color:var(--weiss)}
.wl button:hover{background:rgba(250,244,244,.08)}
.wl span{padding:0 10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wl em{font-style:normal;color:var(--kerze);margin-right:8px}
@media (prefers-reduced-motion:reduce){.v07 .dreh{transition:none}}'''

JS = r'''(function () {
  // Scroll-Fortschritt je Fassung als --p (0 bis 1); nur transform und opacity hängen daran
  var els = [].slice.call(document.querySelectorAll('[data-p]'));
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function lauf() {
    var vh = innerHeight;
    els.forEach(function (el) {
      var r = el.getBoundingClientRect(), p;
      if (el.dataset.p === 'sticky') p = -r.top / Math.max(1, r.height - vh);
      else p = (vh - r.top) / (vh * .55 + r.height * .45);
      p = Math.min(1, Math.max(0, p));
      if (still && el.dataset.p !== 'sticky') p = 1;
      el.style.setProperty('--p', p.toFixed(4));
    });
  }
  var t = false;
  addEventListener('scroll', function () { if (!t) { t = true; requestAnimationFrame(function () { t = false; lauf(); }); } }, { passive: true });
  addEventListener('resize', lauf); lauf();

  // 07: Karte wenden
  var v7 = document.querySelector('.v07');
  v7.querySelectorAll('[data-wende]').forEach(function (b) {
    b.addEventListener('click', function () { v7.dataset.seite = v7.dataset.seite === 'vorn' ? 'hinten' : 'vorn'; });
  });

  // 13: Band, Laufbalken und Pfeile
  var band = document.querySelector('.v13 .band'), lb = document.querySelector('.v13 .lauf');
  function balken() { lb.style.setProperty('--b', ((band.scrollLeft + band.clientWidth) / band.scrollWidth).toFixed(4)); }
  band.addEventListener('scroll', balken, { passive: true }); addEventListener('resize', balken); balken();
  document.querySelectorAll('[data-band]').forEach(function (b) {
    b.addEventListener('click', function () { band.scrollBy({ left: +b.dataset.band * band.clientWidth * .7, behavior: 'smooth' }); });
  });

  // Leiste unten: aktuelle Fassung, blättern (Pfeiltasten, ?f=Nummer)
  var fk = [].slice.call(document.querySelectorAll('.fk')), akt = 0, wl = document.querySelector('[data-wl]');
  function zeige() { wl.innerHTML = '<em>' + String(akt + 1).padStart(2, '0') + ' / ' + fk.length + '</em>' + fk[akt].dataset.name; }
  function welche() {
    var y = innerHeight * .4, n = 0;
    fk.forEach(function (f, i) { if (f.getBoundingClientRect().top < y) n = i; });
    if (n !== akt) { akt = n; zeige(); }
  }
  function geh(n) { n = Math.min(fk.length - 1, Math.max(0, n)); scrollTo({ top: fk[n].getBoundingClientRect().top + scrollY - 10, behavior: 'smooth' }); }
  addEventListener('scroll', welche, { passive: true });
  document.querySelectorAll('[data-schritt]').forEach(function (b) { b.addEventListener('click', function () { geh(akt + +b.dataset.schritt); }); });
  addEventListener('keydown', function (e) {
    if (e.target.closest && e.target.closest('.band')) return;
    if (e.key === 'ArrowRight') geh(akt + 1); else if (e.key === 'ArrowLeft') geh(akt - 1);
  });
  var q = +new URLSearchParams(location.search).get('f');
  if (q) setTimeout(function () { fk[q - 1] && scrollTo({ top: fk[q - 1].getBoundingClientRect().top + scrollY - 10 }); }, 60);
  zeige();
})();'''


def main():
    teile = []
    for i, (name, satz, m, html, _css) in enumerate(F, 1):
        teile.append('<!-- ============ %02d ============ -->\n<section class="fk" id="f%d" data-name="%s"><b>%02d</b><h2>%s</h2><p>%s</p><p class="m">%s</p></section>\n%s'
                     % (i, i, E(name), i, E(name), E(satz), E(m), html))
    s = '''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Culinarium · Abend und Haus · 15 weitere Fassungen</title>
<meta name="robots" content="noindex">
<style>
/* Culinarium · Abschnitt «Abend und Haus» (unter dem Auftakt), 15 weitere Fassungen, 26.10.2026. Gebaut von ebenen_wahl2.py.
   Nur Wahlseite. Bewegung nur transform und opacity, nichts startet unsichtbar. */
%s
%s
</style>
</head>
<body>
<header class="wk">
  <p class="mono e">Culinarium · Startseite · Abschnitt unter dem Auftakt</p>
  <h1>Abend und Haus: 15 weitere Fassungen</h1>
  <p>Gleicher Inhalt in jeder Fassung: der Titel, der Abend mit Zeiten und Preis, das Haus mit Adresse und Barzeiten, zwei Knöpfe. Anders ist nur, wie Bild und Text stehen und was sich bewegt. Keine wiederholt eine Fassung aus der ersten Runde. Unten in der Leiste oder mit den Pfeiltasten blätterst du weiter.</p>
</header>
%s
<nav class="wl" aria-label="Fassungen"><button type="button" data-schritt="-1" aria-label="Vorige Fassung">&#8592;</button><span data-wl></span><button type="button" data-schritt="1" aria-label="Nächste Fassung">&#8594;</button></nav>
<script>
%s
</script>
</body>
</html>
''' % (KOPF_CSS, '\n'.join('/* %02d %s */\n%s' % (i, f[0], f[4]) for i, f in enumerate(F, 1)), '\n\n'.join(teile), JS)
    ziel = os.path.join(HIER, 'ebenen-wahl-2.html')
    open(ziel, 'w', encoding='utf-8').write(s)
    print(ziel, len(F), 'Fassungen')


if __name__ == '__main__':
    main()
