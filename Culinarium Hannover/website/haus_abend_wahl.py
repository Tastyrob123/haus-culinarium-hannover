#!/usr/bin/env python3
"""Culinarium Hannover · Abschnitt «Abend und Haus» (unter dem Auftakt, heute «Flankiert»), 15 neue Fassungen, 26.10.2026.
Robert: «15 alternative visuelle Darstellungsmöglichkeiten» (Bildschirmfoto von «Flankiert», 20:06).
Baut haus-abend-wahl.html. Keine Fassung wiederholt eine der 30 aus ebenen-wahl.html und ebenen-wahl-2.html.
Inhalt in jeder Fassung gleich (Titel, Der Abend, Das Haus, zwei Knöpfe); anders sind Anordnung, Bild und bewegter Moment.
Bewegung nur transform und opacity, nichts startet unsichtbar, nativer Scroll.
Aufruf: python3 website/haus_abend_wahl.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E
from ebenen_wahl2 import ph, blk, knopf, titel, ABEND, HAUS, KOPF_CSS

HIER = bau.HIER


def paar(cls=''):
    """Abend und Haus als ein geschlossener Block nebeneinander."""
    return '<div class="paar2 %s">%s%s</div>' % (cls, blk(ABEND), blk(HAUS))


F = []   # (Name, Satz, Bewegung · Handy, HTML, CSS)

# 01 ---------------------------------------------------------------
F.append(('Die Tür zur Tafel', 'Das ganze Bild ist die Bar. Mitten darin steht ein hoher Bogen wie eine offene Tür, und durch ihn sieht man die gedeckte Tafel. Der Abend steht im Bogen, das Haus davor in der Bar.',
'Bewegung: das Bild im Bogen wandert beim Scrollen leicht gegen die Bar, als ginge man darauf zu · Handy: Bar oben mit Titel, Bogen darunter in voller Breite',
'''<div class="w01" data-p>%s
<div class="links">%s%s</div>
<div class="bogen">%s%s</div></div>''' % (
    ph('ws13', 'grund', w=1000, laden='eager'), titel(), blk(HAUS),
    ph('kerze3', 'innen', w=1000, pos='50% 45%', laden='eager'), blk(ABEND)),
'''.w01{position:relative;margin:0 var(--rand);min-height:clamp(560px,88vh,860px);border-radius:var(--r);overflow:hidden;display:grid;grid-template-columns:1fr minmax(300px,36%);gap:clamp(24px,4vw,64px);padding:clamp(28px,5vw,72px)}
.w01>.grund{position:absolute;inset:0;border-radius:0}
.w01>.grund::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,12,16,.9),rgba(14,12,16,.62) 46%,rgba(14,12,16,.35))}
.w01 .links{position:relative;z-index:1;display:flex;flex-direction:column;justify-content:space-between;gap:40px;padding:8px 0}
.w01 .bogen{position:relative;z-index:1;border-radius:999px 999px 14px 14px;overflow:hidden;box-shadow:0 0 0 1px rgba(239,118,73,.55),0 30px 80px -30px rgba(0,0,0,.9);display:flex;align-items:flex-end;min-height:440px}
.w01 .bogen>.ph{position:absolute;inset:-9% 0;border-radius:0}
.w01 .bogen>.ph img{transform:translateY(calc((var(--p,.5) - .5) * -80px)) scale(1.04)}
.w01 .bogen::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(14,12,16,.96),rgba(14,12,16,.82) 44%,rgba(14,12,16,.2) 72%,rgba(14,12,16,0) 86%)}
.w01 .bogen .blk{position:relative;z-index:2;padding:0 clamp(20px,2.4vw,34px) clamp(22px,2.6vw,36px)}
@media (max-width:860px){.w01{grid-template-columns:1fr;padding:26px 20px}.w01 .bogen{min-height:62vh}}'''))

# 02 ---------------------------------------------------------------
F.append(('Leuchtschrift', 'Die Rückwand der Bar mit dem Negroni-Schriftzug füllt den Rahmen. Der Titel leuchtet davor wie eine zweite Leuchtschrift in Kerzenfarbe. Unten auf dem Tresen stehen der Abend und das Haus nebeneinander.',
'Bewegung: die Schrift geht einmal flackernd an, wenn der Teil ins Bild kommt (Deckkraft von 55 auf 100 Prozent) · Handy: Schrift kleiner, Texte untereinander',
'''<div class="w02" data-an>%s<h2 class="ti neon">Culinarium im<br>Walk on the Wild Side.</h2>%s</div>''' % (
    ph('barneg', 'grund', w=1600, pos='50% 30%'), paar()),
'''.w02{position:relative;margin:0 var(--rand);min-height:clamp(600px,92vh,900px);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;align-items:center;padding:clamp(48px,9vh,96px) clamp(22px,4vw,64px) clamp(28px,4vw,56px)}
.w02>.grund{position:absolute;inset:0;border-radius:0}
.w02>.grund::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,12,16,.55),rgba(14,12,16,.35) 40%,rgba(14,12,16,.94) 76%)}
.w02 .neon{position:relative;z-index:1;text-align:center;font-size:clamp(46px,6.4vw,104px);color:#FFE3D2;text-shadow:0 0 6px rgba(255,180,140,.9),0 0 22px rgba(239,118,73,.85),0 0 60px rgba(239,118,73,.55);opacity:.55}
.w02.an .neon{animation:flacker 1.6s steps(1,end) forwards}
@keyframes flacker{0%{opacity:.55}12%{opacity:1}18%{opacity:.6}26%{opacity:1}34%{opacity:.75}42%,100%{opacity:1}}
.w02 .paar2{position:relative;z-index:1;width:100%}
@media (max-width:860px){.w02{min-height:0;gap:60vh}.w02 .neon{font-size:44px}}
@media (prefers-reduced-motion:reduce){.w02 .neon{opacity:1;animation:none}}'''))

# 03 ---------------------------------------------------------------
F.append(('Filmstreifen', 'Oben Titel und die beiden Texte als ein ruhiger Block. Darunter läuft ein Filmstreifen mit Lochrand durch das Bild: Strasse, Flur, Theke, Tafel, Teller, Anstossen, ein Abend als Negativ-Rolle.',
'Bewegung: der Streifen zieht beim Scrollen langsam nach links · Handy: Streifen zum Wischen, Bilder etwas kleiner',
'''<div class="w03" data-p><div class="kopf">%s%s</div>
<div class="rolle"><div class="streifen">%s</div></div></div>''' % (
    titel(), paar(),
    ''.join('<div class="bild">%s<span class="mono">CULINARIUM %02dA</span></div>' % (ph(k, w=1000), i)
            for i, k in enumerate(('barnacht', 'flur', 'theke', 't01', 'roq1', 'toast', 'kerze2'), 1))),
'''.w03 .kopf{display:flex;flex-direction:column;align-items:center;gap:clamp(30px,4.6vh,48px);padding:0 var(--rand) clamp(40px,6vh,64px);text-align:center}
.w03 .kopf .blk{text-align:left}
.w03 .rolle{overflow:hidden}
.w03 .streifen{display:flex;gap:14px;width:max-content;background:#0B0A0D;padding:38px 14px;
background-image:repeating-linear-gradient(90deg,transparent 0 14px,rgba(250,244,244,.82) 14px 28px,transparent 28px 40px),repeating-linear-gradient(90deg,transparent 0 14px,rgba(250,244,244,.82) 14px 28px,transparent 28px 40px);
background-size:40px 12px,40px 12px;background-position:0 13px,0 calc(100% - 13px);background-repeat:repeat-x;
transform:translateX(calc(var(--p,0) * -38%))}
.w03 .bild{position:relative}
.w03 .bild .ph{width:clamp(260px,28vw,420px);aspect-ratio:4/5;border-radius:3px}
.w03 .bild .mono{position:absolute;left:4px;top:-30px;font-size:10.5px;color:#E8A06F;letter-spacing:.14em}
.w03 .paar2{text-align:left}
@media (max-width:860px){.w03 .rolle{overflow-x:auto;scroll-snap-type:x mandatory}.w03 .streifen{transform:none}.w03 .bild{scroll-snap-align:center}.w03 .bild .ph{width:72vw}}'''))

# 04 ---------------------------------------------------------------
F.append(('An der Leine', 'Über die ganze Breite hängt eine Leine, an ihr mit Holzklammern vier grosse Abzüge: zwei vom Abend, zwei aus der Bar. Darunter Titel und Text als ein Block. Wirkt wie die Wand hinter der Theke, nicht wie eine Website.',
'Bewegung: die Abzüge schwingen beim Scrollen leicht aus (Drehung um die Klammer) · Handy: zwei Abzüge je Leine, zwei Leinen übereinander',
'''<div class="w04" data-p><div class="leine"><i class="schnur"></i>%s</div><div class="unter">%s%s</div></div>''' % (
    ''.join('<div class="abzug" style="--d:%s">%s<b></b></div>' % (d, ph(k, w=640 if i else 1000))
            for i, (k, d) in enumerate((('t09', '-2.4deg'), ('theke2', '1.8deg'), ('anstossen', '-1.2deg'), ('ws05', '2.6deg')))),
    titel(), paar()),
'''.w04{padding:0 var(--rand)}
.w04 .leine{position:relative;display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(14px,2vw,30px);padding-top:30px}
.w04 .schnur{position:absolute;left:-4vw;right:-4vw;top:30px;height:1px;background:rgba(250,244,244,.45)}
.w04 .abzug{position:relative;padding:12px 12px 46px;background:#F3ECE6;border-radius:2px;box-shadow:0 26px 50px -24px rgba(0,0,0,.9);transform-origin:50% -18px;transform:rotate(calc(var(--d) + (var(--p,.5) - .5) * 5deg))}
.w04 .abzug:nth-child(odd){transform:rotate(calc(var(--d) - (var(--p,.5) - .5) * 5deg))}
.w04 .abzug .ph{aspect-ratio:4/5;border-radius:1px}
.w04 .abzug b{position:absolute;left:50%;top:-22px;width:14px;height:40px;margin-left:-7px;border-radius:3px;background:linear-gradient(90deg,#A27650,#C49A6C 50%,#A27650)}
.w04 .unter{display:flex;flex-direction:column;align-items:center;gap:40px;padding-top:clamp(48px,7vh,72px);text-align:center}
.w04 .unter .paar2{text-align:left}
@media (max-width:860px){.w04 .leine{grid-template-columns:1fr 1fr;row-gap:56px}.w04 .schnur{display:none}}'''))

# 05 ---------------------------------------------------------------
F.append(('Mit Sternchen', 'Der Abend gross: ein randloses Bild der Tafel, der Abend darauf. Am Titel hängt ein Sternchen in Kerzenfarbe, und unten folgt die Fussnote: das Haus, mit eigenem Bild, wie eine Anmerkung, die man gern liest. Die Rangfolge steht in der Typografie.',
'Bewegung: das Sternchen dreht sich beim Scrollen langsam einmal · Handy: Bild, Abend, dann die Fussnote untereinander',
'''<div class="w05" data-p><h2 class="ti h2 kopf">Culinarium im Walk on the Wild Side<span class="stern">*</span></h2>
<div class="gross">%s%s</div>
<div class="fuss"><span class="stern gross-stern">*</span>%s%s</div></div>''' % (
    ph('tafelleer', w=1600, pos='50% 48%'), blk(ABEND),
    blk(HAUS), ph('theke', 'klein', w=1000, pos='50% 32%')),
'''.w05{padding:0 var(--rand)}
.w05 .kopf{text-align:center;padding-bottom:clamp(28px,4vh,44px)}
.w05 .stern{display:inline-block;color:var(--kerze);font-size:.8em;vertical-align:.5em;margin-left:.06em;transform:rotate(calc(var(--p,0) * 180deg))}
.w05 .gross{position:relative;height:clamp(460px,74vh,760px);border-radius:var(--r);overflow:hidden;display:flex;align-items:flex-end}
.w05 .gross>.ph{position:absolute;inset:0;border-radius:0}
.w05 .gross::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(14,12,16,.9),rgba(14,12,16,.3) 46%,rgba(14,12,16,0) 70%),linear-gradient(90deg,rgba(14,12,16,.82),rgba(14,12,16,.4) 40%,rgba(14,12,16,0) 62%)}
.w05 .gross .blk{position:relative;z-index:1;padding:0 clamp(22px,3.6vw,60px) clamp(24px,4vh,48px);max-width:560px}
.w05 .fuss{display:grid;grid-template-columns:auto 1fr minmax(260px,40%);gap:clamp(18px,3vw,48px);align-items:center;margin-top:clamp(28px,4vh,40px);padding-top:clamp(28px,4vh,40px);border-top:1px solid var(--linie)}
.w05 .gross-stern{font:340 clamp(80px,9vw,140px)/.6 var(--titel);vertical-align:0;margin:0;align-self:start}
.w05 .fuss .klein{aspect-ratio:16/10}
@media (max-width:860px){.w05 .fuss{grid-template-columns:auto 1fr}.w05 .fuss .klein{grid-column:1/-1}.w05 .gross{height:auto;flex-direction:column}.w05 .gross>.ph{position:relative;height:56vh;width:100%}.w05 .gross::after{display:none}.w05 .gross .blk{padding:22px 0 0}}'''))

# 06 ---------------------------------------------------------------
F.append(('Fächer', 'Sechs Abzüge liegen erst als Stapel in der Mitte. Beim Scrollen fächern sie sich auf wie ein Blatt Karten in der Hand: drei vom Abend, drei aus der Bar. Darunter Titel und die beiden Texte.',
'Bewegung: der Stapel fächert beim Scrollen auf (nur Drehung) · Handy: kleinerer Fächer, Texte untereinander',
'''<div class="w06" data-p><div class="hand">%s</div><div class="unter">%s%s</div></div>''' % (
    ''.join('<div class="karte" style="--k:%s">%s</div>' % (k, ph(b, w=640, pos=p))
            for k, (b, p) in zip((-2.5, -1.5, -.5, .5, 1.5, 2.5),
                                (('ws00', None), ('theke', '50% 30%'), ('barnacht', None), ('toast', None), ('roq1', None), ('t01', None)))),
    titel(), paar()),
'''.w06{padding:0 var(--rand)}
.w06 .hand{position:relative;height:clamp(480px,70vh,660px);display:flex;justify-content:center;align-items:flex-end;overflow:hidden;padding-bottom:6px}
.w06 .karte{position:absolute;bottom:0;width:clamp(220px,22vw,330px);aspect-ratio:4/5.4;transform-origin:50% 135%;transform:rotate(calc(var(--k) * (2deg + var(--p,0) * 9deg)));box-shadow:0 30px 60px -26px rgba(0,0,0,.95);border-radius:var(--r)}
.w06 .karte .ph{width:100%;height:100%;box-shadow:inset 0 0 0 1px rgba(250,244,244,.14)}
.w06 .unter{display:flex;flex-direction:column;align-items:center;gap:40px;padding-top:clamp(40px,6vh,64px);text-align:center}
.w06 .unter .paar2{text-align:left}
@media (max-width:860px){.w06 .hand{height:60vh}.w06 .karte{width:44vw;transform:rotate(calc(var(--k) * (2deg + var(--p,0) * 6deg)))}}'''))

# 07 ---------------------------------------------------------------
F.append(('Ein Abend in sechs Bildern', 'Links ein grosses Bild, das von selbst weiterblendet: die Strasse, die Tür, die Theke, die Tafel, der Teller, das Anstossen. Rechts daneben, fest stehend, Titel und die beiden Texte. In zwanzig Sekunden sieht man den ganzen Abend.',
'Bewegung: Überblenden alle 3,5 Sekunden mit langsamem Zoom, eine feine Linie zeigt den Lauf · Handy: Bild oben, Text darunter',
'''<div class="w07"><div class="schau" data-schau>%s<i class="lauf"></i></div><div class="text">%s%s%s</div></div>''' % (
    ''.join(ph(k, 'an' if i == 0 else '', w=1000, pos=p) for i, (k, p) in enumerate(
        (('schildnacht', None), ('flur', None), ('theke', '50% 30%'), ('tafelleer', None), ('lauch', None), ('anstossen', '50% 38%')))),
    titel(), blk(ABEND), blk(HAUS)),
'''.w07{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:clamp(24px,4vw,64px);padding:0 var(--rand);align-items:center}
.w07 .schau{position:relative;height:clamp(540px,86vh,860px);border-radius:var(--r);overflow:hidden;background:var(--nacht3)}
.w07 .schau .ph{position:absolute;inset:0;border-radius:0;opacity:0;transition:opacity 1.2s ease}
.w07 .schau .ph img{transform:scale(1.08);transition:transform 4.8s linear}
.w07 .schau .ph.an{opacity:1}
.w07 .schau .ph.an img{transform:scale(1)}
.w07 .lauf{position:absolute;left:0;right:0;bottom:0;height:3px;background:var(--kerze);transform-origin:0 50%;transform:scaleX(var(--l,0));transition:transform .6s var(--k)}
.w07 .text{display:flex;flex-direction:column;gap:clamp(22px,3.6vh,44px)}
@media (max-width:860px){.w07{grid-template-columns:1fr}.w07 .schau{height:64vh}}
@media (prefers-reduced-motion:reduce){.w07 .schau .ph img{transition:none;transform:none}}'''))

# 08 ---------------------------------------------------------------
F.append(('Hinter den Bildern', 'Der Titel steht riesig über die ganze Breite, und zwei grosse Bilder stehen davor, eines tiefer, eines höher. Die Schrift schaut zwischen und über den Bildern hervor. Unter jedem Bild sein Text.',
'Bewegung: die Schrift wandert langsamer als die Bilder, so entsteht Tiefe · Handy: Schrift oben, Bilder mit Text untereinander',
'''<div class="w08" data-p><h2 class="ti riese" aria-label="Culinarium im Walk on the Wild Side."><span>Culinarium im</span><span>Walk on the Wild Side.</span></h2>
<div class="vorn"><div class="sp a">%s%s</div><div class="sp b">%s%s</div></div></div>''' % (
    ph('t02', w=1000), blk(ABEND), ph('ws28', w=1000), blk(HAUS)),
'''.w08{position:relative;padding:0 var(--rand)}
.w08 .riese{position:absolute;left:var(--rand);right:var(--rand);top:0;font-size:clamp(60px,10.6vw,190px);line-height:.92;letter-spacing:-.03em;color:rgba(250,244,244,.92);display:flex;flex-direction:column;transform:translateY(calc((var(--p,.5) - .5) * 50px))}
.w08 .riese span:last-child{align-self:flex-end;text-align:right;color:var(--kerze)}
.w08 .vorn{position:relative;z-index:1;display:grid;grid-template-columns:1fr 1fr;gap:clamp(30px,8vw,140px);padding:calc(min(10.6vw,190px) * 1.62) clamp(0px,5vw,90px) 0}
.w08 .sp{display:flex;flex-direction:column;gap:26px}
.w08 .sp .ph{aspect-ratio:4/5;box-shadow:0 40px 80px -40px rgba(0,0,0,.95)}
.w08 .sp.a{margin-top:clamp(140px,16vw,280px)}
@media (max-width:860px){.w08 .riese{position:relative;left:auto;right:auto;font-size:15vw;transform:none}.w08 .vorn{grid-template-columns:1fr;padding:30px 0 0}.w08 .sp.a{margin-top:0}}'''))

# 09 ---------------------------------------------------------------
F.append(('Magazinseite', 'Eine aufgeschlagene Doppelseite: links ein Hochformat randlos bis zum Falz, rechts gesetzt wie im Heft, mit Kopfzeile, Titel, grossem Anfangsbuchstaben beim Abend und dem Haus darunter mit eigenem Querformat.',
'Bewegung: das linke Bild zoomt beim Hereinscrollen von 108 auf 100 Prozent · Handy: Bild oben, Seite darunter',
'''<div class="w09" data-p><div class="li">%s</div><div class="re"><p class="mono kz"><span>Culinarium</span><span>Linden</span></p>%s
<div class="abend"><p class="tx init">%s</p><p class="mono">%s</p>%s</div>
<div class="haus">%s%s</div></div></div>''' % (
    ph('t05', w=1000), titel('h2'), E(ABEND['satz']), E(ABEND['info']), knopf(*ABEND['kn'][:2]),
    ph('theke2', w=1000), blk(HAUS)),
'''.w09{display:grid;grid-template-columns:1fr 1fr;margin:0 var(--rand);background:#1C1A21;border-radius:var(--r);overflow:hidden;box-shadow:0 40px 90px -40px rgba(0,0,0,.9)}
.w09 .li{position:relative;min-height:clamp(620px,96vh,940px);overflow:hidden}
.w09 .li .ph{position:absolute;inset:0;border-radius:0}
.w09 .li .ph img{transform:scale(calc(1.08 - var(--p,0) * .08))}
.w09 .li::after{content:"";position:absolute;top:0;bottom:0;right:0;width:60px;background:linear-gradient(90deg,rgba(0,0,0,0),rgba(0,0,0,.4))}
.w09 .re{position:relative;display:flex;flex-direction:column;gap:clamp(22px,3.4vh,34px);padding:clamp(28px,4vw,64px)}
.w09 .re::before{content:"";position:absolute;top:0;bottom:0;left:0;width:50px;background:linear-gradient(90deg,rgba(0,0,0,.35),rgba(0,0,0,0))}
.w09 .kz{display:flex;justify-content:space-between;border-bottom:1px solid var(--linie);padding-bottom:12px}
.w09 .abend{display:flex;flex-direction:column;gap:14px;align-items:flex-start}
.w09 .init::first-letter{float:left;font:340 4.4em/.82 var(--titel);color:var(--kerze);margin:.06em .1em 0 0}
.w09 .haus{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1fr);gap:22px;align-items:start;border-top:1px solid var(--linie);padding-top:clamp(22px,3.4vh,34px)}
.w09 .haus .ph{aspect-ratio:4/5}
.w09 .haus .tx{font-size:16px}
@media (max-width:860px){.w09{grid-template-columns:1fr}.w09 .li{min-height:60vh}.w09 .haus{grid-template-columns:1fr}}'''))

# 10 ---------------------------------------------------------------
F.append(('Schaufensterschrift', 'Wir stehen draussen in Linden und schauen durchs Fenster in die Bar. Auf der Scheibe steht der Titel wie von Hand in Blattgold geschrieben, darunter die Hausnummer. Unter dem Fenster der Abend und das Haus.',
'Bewegung: das Bild hinter der Scheibe zieht beim Hereinscrollen von 110 auf 100 Prozent, die Schrift bleibt auf dem Glas · Handy: Fenster hochkant, Texte darunter',
'''<div class="w10" data-p><div class="scheibe">%s<div class="gold"><h2 class="ti">Culinarium im<br>Walk on the Wild Side.</h2><p>Haasemannstraße · 13</p></div><i class="rahmen"></i></div>%s</div>''' % (
    ph('fensterdraussen', w=1000), paar()),
'''.w10{padding:0 var(--rand)}
.w10 .scheibe{position:relative;max-width:1180px;margin:0 auto;height:clamp(520px,84vh,820px);border-radius:4px;overflow:hidden;display:grid;place-items:center}
.w10 .scheibe>.ph{position:absolute;inset:0;border-radius:0}
.w10 .scheibe>.ph img{transform:scale(calc(1.1 - var(--p,0) * .1))}
.w10 .scheibe::after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% 42%,rgba(14,12,16,.25),rgba(14,12,16,.72) 80%)}
.w10 .rahmen{position:absolute;inset:0;z-index:2;border:clamp(10px,1.4vw,18px) solid #121015;box-shadow:inset 0 0 0 1px rgba(250,244,244,.1)}
.w10 .gold{position:relative;z-index:1;text-align:center;padding:0 6vw}
.w10 .gold .ti{font-size:clamp(46px,6vw,96px);font-weight:420;letter-spacing:.005em;background:linear-gradient(180deg,#FFE7B0 0%,#E3A94F 38%,#A8692A 58%,#F2C77A 78%,#C88A3C 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 0 rgba(30,18,8,.9))}
.w10 .gold p{margin-top:20px;font:400 13px/1 var(--mono);letter-spacing:.32em;text-transform:uppercase;color:#E8BC74}
.w10 .paar2{margin-top:clamp(36px,5vh,56px)}
@media (max-width:860px){.w10 .scheibe{height:74vh}.w10 .gold .ti{font-size:40px}}'''))

# 11 ---------------------------------------------------------------
F.append(('Eintrittskarte', 'Der Abschnitt ist eine grosse Eintrittskarte für den Abend: links das Bild der Tafel, in der Mitte der Abend mit Tag, Uhrzeit und Preis, an der Perforation der Abriss für das Haus mit Adresse und Barzeiten.',
'Bewegung: die Karte legt sich beim Hereinscrollen gerade (−3° auf 0°), der Abriss bleibt eine Spur versetzt · Handy: Bild oben, Abend, Abriss unten quer',
'''<div class="w11" data-p><div class="kopf">%s</div><div class="karte"><div class="bild">%s</div><div class="mitte">%s</div><div class="abriss">%s%s</div></div></div>''' % (
    titel(), ph('t06', w=1000, pos='50% 42%'), blk(ABEND, kn='dunkel'), ph('theke', 'mini', w=640, pos='50% 30%'), blk(HAUS, kn='dunkel')),
'''.w11{padding:0 var(--rand)}
.w11 .kopf{text-align:center;padding-bottom:clamp(30px,5vh,52px)}
.w11 .karte{--loch:radial-gradient(circle at 0 0,transparent 16px,#000 16.5px);display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1.2fr) minmax(0,.95fr);max-width:1240px;margin:0 auto;background:var(--weiss);color:var(--nacht);border-radius:14px;overflow:hidden;transform:rotate(calc(-3deg + var(--p,0) * 3deg));box-shadow:0 40px 90px -40px rgba(0,0,0,.95)}
.w11 .bild .ph{height:100%;min-height:440px;border-radius:0}
.w11 .mitte,.w11 .abriss{padding:clamp(26px,3vw,48px)}
.w11 .abriss{position:relative;border-left:2px dashed rgba(22,21,26,.3);background:#F1E9E5;transform:translateX(calc((1 - var(--p,0)) * 14px))}
.w11 .abriss::before,.w11 .abriss::after{content:"";position:absolute;left:-17px;width:32px;height:32px;border-radius:50%;background:var(--bg)}
.w11 .abriss::before{top:-16px}.w11 .abriss::after{bottom:-16px}
.w11 .mini{aspect-ratio:16/10;margin-bottom:18px}
.w11 .tx{color:rgba(22,21,26,.78)}.w11 .mono{color:rgba(22,21,26,.6)}.w11 .mono.e{color:#B9541F}
.w11 .h3{color:var(--nacht)}
@media (max-width:860px){.w11 .karte{grid-template-columns:1fr}.w11 .bild .ph{min-height:44vh}.w11 .abriss{border-left:0;border-top:2px dashed rgba(22,21,26,.3)}.w11 .abriss::before{left:-16px;top:-17px}.w11 .abriss::after{left:auto;right:-16px;top:-17px;bottom:auto}}'''))

# 12 ---------------------------------------------------------------
F.append(('Titel bleibt stehen', 'Links stehen Titel, Abend und Haus fest, während rechts eine lange Spalte grosser Bilder vorbeizieht: erst die Bar von aussen, dann die Theke, dann die Tafel und die Teller. Man liest in Ruhe, die Bilder erzählen dazu.',
'Bewegung: nur der native Scroll, die linke Spalte bleibt stehen · Handy: Text oben, die Bilder als Reihe zum Wischen darunter',
'''<div class="w12"><div class="fest">%s%s%s</div><div class="spalte">%s</div></div>''' % (
    titel(), blk(ABEND), blk(HAUS),
    ''.join(ph(k, c, w=1000, pos=p) for k, c, p in (
        ('barlicht', 'breit', None), ('lachen', 'halb', '50% 35%'), ('theke', 'halb r', '50% 30%'),
        ('t03', 'breit', None), ('beete', 'halb', None), ('glaeser', 'halb r', None)))),
'''.w12{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:clamp(28px,5vw,80px);padding:0 var(--rand)}
.w12 .fest{position:sticky;top:clamp(40px,10vh,110px);align-self:start;display:flex;flex-direction:column;gap:clamp(28px,4.4vh,44px)}
.w12 .spalte{display:grid;grid-template-columns:1fr 1fr;gap:clamp(12px,1.4vw,20px)}
.w12 .breit{grid-column:1/-1;aspect-ratio:4/3}
.w12 .halb{aspect-ratio:4/5}
.w12 .halb.r{margin-top:clamp(40px,8vh,90px)}
@media (max-width:860px){.w12{grid-template-columns:1fr}.w12 .fest{position:static}.w12 .spalte{display:flex;overflow-x:auto;gap:12px;scroll-snap-type:x mandatory}.w12 .spalte .ph{flex:0 0 78vw;aspect-ratio:4/5;margin:0;scroll-snap-align:center}}'''))

# 13 ---------------------------------------------------------------
F.append(('Panorama', 'Ein einziges breites Bildband ohne Fugen, so lang wie der Weg des Gastes: von der Strasse über den Flur und die Theke bis an die Tafel. Darüber Titel und Text als Block, das Band läuft beim Scrollen am Auge vorbei.',
'Bewegung: das Band wandert beim Scrollen um eine Bildschirmbreite nach links · Handy: Band zum Wischen',
'''<div class="w13" data-p><div class="kopf">%s%s</div><div class="fahrt"><div class="band">%s</div></div></div>''' % (
    titel(), paar(),
    ''.join(ph(k, w=1000, pos=p) for k, p in (('ecke', None), ('barnacht', None), ('flur', None), ('theke', '50% 30%'), ('kerze3', None), ('tafelleer', None), ('anstossen', '50% 38%')))),
'''.w13 .kopf{display:flex;flex-direction:column;align-items:center;gap:clamp(30px,4.6vh,48px);padding:0 var(--rand) clamp(36px,5vh,56px);text-align:center}
.w13 .kopf .paar2{text-align:left}
.w13 .fahrt{overflow:hidden}
.w13 .band{display:flex;width:max-content;transform:translateX(calc(var(--rand) - var(--p,0) * 100vw))}
.w13 .band .ph{width:clamp(300px,34vw,520px);height:clamp(420px,66vh,660px);border-radius:0}
.w13 .band .ph:first-child{border-radius:var(--r) 0 0 var(--r)}.w13 .band .ph:last-child{border-radius:0 var(--r) var(--r) 0}
@media (max-width:860px){.w13 .fahrt{overflow-x:auto}.w13 .band{transform:none}.w13 .band .ph{width:78vw;height:58vh}}'''))

# 14 ---------------------------------------------------------------
F.append(('Kerzenschein', 'Ein grosses Bild von der Tafel liegt im Dunkeln. Wo die Maus ist, brennt eine Kerze und macht einen Kreis warm und hell, so sucht man die Gesichter selbst. Am Handy wandert das Licht von allein. Daneben Titel und Text.',
'Bewegung: der Lichtkreis folgt der Maus (nur Weg), am Handy langsamer Rundgang · Handy: Bild oben, Text darunter',
'''<div class="w14"><div class="dunkel" data-licht>%s<i class="licht"></i></div><div class="text">%s%s%s</div></div>''' % (
    ph('t01', w=1000), titel(), blk(ABEND), blk(HAUS)),
'''.w14{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:clamp(24px,4vw,64px);padding:0 var(--rand);align-items:center}
.w14 .dunkel{position:relative;height:clamp(540px,86vh,860px);border-radius:var(--r);overflow:hidden;cursor:none}
.w14 .dunkel>.ph{position:absolute;inset:0;border-radius:0}
.w14 .licht{position:absolute;left:-150%;top:-150%;width:300%;height:300%;pointer-events:none;
background:radial-gradient(circle at 50% 50%,rgba(255,170,90,.1) 0,rgba(14,12,16,0) 5%,rgba(14,12,16,.8) 12%,rgba(14,12,16,.9) 24%);
transform:translate(var(--x,50%),var(--y,45%));transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.w14 .text{display:flex;flex-direction:column;gap:clamp(28px,4.6vh,48px)}
@media (max-width:860px){.w14{grid-template-columns:1fr}.w14 .dunkel{height:64vh}}'''))

# 15 ---------------------------------------------------------------
F.append(('Schräge Bahn', 'Eine Bahn grosser Bilder liegt quer durch den Abschnitt, von links unten nach rechts oben, wie eine Theke im Anschnitt. Darüber Titel und die beiden Texte als ein Block, die Bahn zieht beim Scrollen an ihnen vorbei.',
'Bewegung: die Bahn gleitet beim Scrollen entlang ihrer eigenen Schräge · Handy: Bahn flacher, Bilder kleiner',
'''<div class="w15" data-p><div class="kopf">%s%s</div><div class="schraeg"><div class="bahn">%s</div></div></div>''' % (
    titel(), paar(),
    ''.join(ph(k, w=640, pos=p) for k, p in (('ws00', None), ('t07', None), ('theke', '50% 30%'), ('g1', None), ('t04', None), ('ws03', None), ('hok1', None), ('t08', None), ('barnacht', None)))),
'''.w15{overflow:hidden;padding-bottom:40px}
.w15 .kopf{display:flex;flex-direction:column;align-items:center;gap:clamp(30px,4.6vh,48px);padding:0 var(--rand);text-align:center;position:relative;z-index:1}
.w15 .kopf .paar2{text-align:left}
.w15 .schraeg{transform:rotate(-7deg);margin:clamp(70px,10vh,110px) -10vw clamp(50px,7vh,80px)}
.w15 .bahn{display:flex;gap:16px;width:max-content;transform:translateX(calc(-6vw - var(--p,0) * 60vw))}
.w15 .bahn .ph{width:clamp(220px,22vw,340px);aspect-ratio:4/5;flex:none}
@media (max-width:860px){.w15 .schraeg{transform:rotate(-4deg)}.w15 .bahn .ph{width:46vw}}'''))


# ------------------------------------------------------------------ Seite
EIGEN_CSS = '''.paar2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,64px);max-width:1040px;width:100%;margin:0 auto}
@media (max-width:860px){.paar2{grid-template-columns:1fr;gap:34px}}'''

JS = r'''(function () {
  // Scroll-Fortschritt je Fassung als --p (0 bis 1); nur transform und opacity hängen daran
  var els = [].slice.call(document.querySelectorAll('[data-p]'));
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function lauf() {
    var vh = innerHeight;
    els.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var p = Math.min(1, Math.max(0, (vh - r.top) / (vh * .55 + r.height * .45)));
      el.style.setProperty('--p', (still ? 1 : p).toFixed(4));
    });
  }
  var t = false;
  addEventListener('scroll', function () { if (!t) { t = true; requestAnimationFrame(function () { t = false; lauf(); }); } }, { passive: true });
  addEventListener('resize', lauf); lauf();

  // 02: Leuchtschrift geht an, sobald sie im Bild ist
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('an'); io.unobserve(e.target); } });
  }, { threshold: .35 });
  document.querySelectorAll('[data-an]').forEach(function (el) { io.observe(el); });

  // 07: sechs Bilder blenden weiter, nur solange sichtbar
  var s = document.querySelector('[data-schau]'), bs = [].slice.call(s.querySelectorAll('.ph')), n = 0, sicht = false;
  new IntersectionObserver(function (es) { sicht = es[0].isIntersecting; }).observe(s);
  function schritt() { s.style.setProperty('--l', ((n + 1) / bs.length).toFixed(3)); }
  schritt();
  if (!still) setInterval(function () {
    if (!sicht) return;
    bs[n].classList.remove('an'); n = (n + 1) % bs.length; bs[n].classList.add('an'); schritt();
  }, 3500);

  // 14: Kerzenschein folgt der Maus, sonst eigener Rundgang
  var d = document.querySelector('[data-licht]'), maus = false, w = 0;
  function setz(x, y) { d.style.setProperty('--x', x + 'px'); d.style.setProperty('--y', y + 'px'); }
  d.addEventListener('pointermove', function (e) { if (e.pointerType !== 'mouse') return; maus = true; var r = d.getBoundingClientRect(); setz(e.clientX - r.left, e.clientY - r.top); });
  d.addEventListener('pointerleave', function () { maus = false; });
  setz(d.clientWidth * .5, d.clientHeight * .45);
  if (!still) setInterval(function () {
    if (maus) return; w += .9;
    setz(d.clientWidth * (.5 + Math.cos(w) * .28), d.clientHeight * (.48 + Math.sin(w * 1.3) * .22));
  }, 1600);

  // Leiste unten: aktuelle Fassung, blättern (Pfeiltasten, ?f=Nummer)
  var fk = [].slice.call(document.querySelectorAll('.fk')), akt = 0, wl = document.querySelector('[data-wl]');
  function zeige() { wl.innerHTML = '<em>' + String(akt + 1).padStart(2, '0') + ' / ' + fk.length + '</em>' + fk[akt].dataset.name; }
  function welche() {
    var y = innerHeight * .4, k = 0;
    fk.forEach(function (f, i) { if (f.getBoundingClientRect().top < y) k = i; });
    if (k !== akt) { akt = k; zeige(); }
  }
  function geh(k) { k = Math.min(fk.length - 1, Math.max(0, k)); scrollTo({ top: fk[k].getBoundingClientRect().top + scrollY - 10, behavior: 'smooth' }); }
  addEventListener('scroll', welche, { passive: true });
  document.querySelectorAll('[data-schritt]').forEach(function (b) { b.addEventListener('click', function () { geh(akt + +b.dataset.schritt); }); });
  addEventListener('keydown', function (e) {
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
<title>Culinarium · Abend und Haus · 15 neue Fassungen</title>
<meta name="robots" content="noindex">
<style>
/* Culinarium · Abschnitt «Abend und Haus» (unter dem Auftakt), 15 neue Fassungen, 26.10.2026. Gebaut von haus_abend_wahl.py.
   Nur Wahlseite. Bewegung nur transform und opacity, nichts startet unsichtbar. */
%s
%s
%s
</style>
</head>
<body>
<header class="wk">
  <p class="mono e">Culinarium · Startseite · Abschnitt unter dem Auftakt</p>
  <h1>Abend und Haus: 15 neue Fassungen</h1>
  <p>Gleicher Inhalt in jeder Fassung: der Titel, der Abend mit Zeiten und Preis, das Haus mit Adresse und Barzeiten, zwei Knöpfe. Anders sind Anordnung, Bild und der eine bewegte Moment. Keine wiederholt eine der 30 Fassungen aus den ersten beiden Runden. Unten in der Leiste oder mit den Pfeiltasten blätterst du weiter.</p>
</header>
%s
<nav class="wl" aria-label="Fassungen"><button type="button" data-schritt="-1" aria-label="Vorige Fassung">&#8592;</button><span data-wl></span><button type="button" data-schritt="1" aria-label="Nächste Fassung">&#8594;</button></nav>
<script>
%s
</script>
</body>
</html>
''' % (KOPF_CSS, EIGEN_CSS, '\n'.join('/* %02d %s */\n%s' % (i, f[0], f[4]) for i, f in enumerate(F, 1)), '\n\n'.join(teile), JS)
    ziel = os.path.join(HIER, 'haus-abend-wahl.html')
    open(ziel, 'w', encoding='utf-8').write(s)
    print(ziel, len(F), 'Fassungen')


if __name__ == '__main__':
    main()
