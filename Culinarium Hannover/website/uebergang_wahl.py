#!/usr/bin/env python3
"""Culinarium Hannover · Seite «Das Haus» (bar.html), Übergang zwischen Hero «Mosaik» und «Dein Drink», 15 Fassungen, 27.10.2026.
Robert: «entferne das Fenster wieder … Wir müssen da irgendeinen Übergang finden» (nach Hero folgt sofort die Fotoreihe von «Dein Drink»).
Baut uebergang-wahl.html aus bar.html: zwischen den beiden Abschnitten ein umschaltbarer Block (0 = ohne Übergang, heute).
Kein Fenster, kein Foto, das auf der Seite schon vorkommt. Zwei Fassungen (6, 10) ziehen Inhalt aus «Dein Drink» nach oben,
statt ihn zu wiederholen. Aufruf: python3 website/uebergang_wahl.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, foto, zl, sw

HIER = bau.HIER
bau.META.update(json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json'))))   # nur lesen

TECH = (('Fatwashing', 'Die Spirituose nimmt den Geschmack eines Fetts an.'),
        ('Milkwashing', 'Milch bindet die Trübstoffe, der Drink wird klar und weich.'),
        ('Enzyme', 'Enzyme lösen die Trübung aus Fruchtsaft, der Geschmack bleibt.'))


def satz(zeilen, cls='ub-satz'):
    return zl(zeilen, 'p', cls)


def band(n, ton, inner, cls=''):
    return '<section class="ub ub%d %s" data-ton="%s" aria-label="Übergang">%s</section>' % (n, cls, ton, inner)


LAUF = ' · '.join(('Ohne Karte', 'Dein Drink', 'Fatwashing', 'Milkwashing', 'Enzyme', 'Haasemannstraße 13', 'Linden')) + ' · '

F = [
    ('Laufschrift', lambda n: band(n, 'strasse', '<div class="ub-lauf" aria-hidden="true"><div>%s</div></div>' % ('<span>%s</span>' % E(LAUF)) * 4)),
    ('Ein Satz gross', lambda n: band(n, 'warm', satz(['Erzähl an der Theke,', 'was du magst.']))),
    ('Zeichen der Bar', lambda n: band(n, 'warm', '<div class="ub-zeichen auf"><i></i>%s<i></i></div><p class="ub-mono sw auf" style="--i:1">Haasemannstraße 13 · Linden</p>' % bau.zeichen_haus('ws', 'ub-ws'))),
    ('Heller Streifen', lambda n: band(n, 'hell', satz(['Hier gibt es keine Karte.']) + sw('Nur die Theke, Derya und Momo.', 'p', 'ub-klein', 1))),
    ('Linie hinab', lambda n: band(n, 'warm', '<div class="ub-linie auf"><i></i></div><p class="ub-mono sw auf" style="--i:1">Ohne Karte</p>')),
    ('Titel zuerst', lambda n: band(n, 'warm', '<div class="fwk">%s<div class="fwk-r"><div>%s</div></div></div>' % (
        '<div class="fwk-l">%s</div>' % zl(['Dein Drink,', 'nach deinem Geschmack.'], 'h2', 'fwk-titel'),
        sw('Eine Getränkekarte gibt es im Walk on the Wild Side nicht. Wer an die Theke kommt, erzählt, was er mag, und bekommt seinen eigenen Drink. Seit dem Reopening am 9. November 2023 führt Derya Ivkin die Bar, Momo steht mit ihr hinter der Theke.', 'p', 'fwk-text', 1)), 'ub-links')),
    ('Gespräch (Beispiel)', lambda n: band(n, 'warm', '<div class="ub-gespraech"><p class="ub-frage sw auf">«Was trinkst du gern?»</p><p class="ub-antwort sw auf" style="--i:1">«Was Frisches, nicht zu süss.»</p></div>')),
    ('Schild mit Satz', lambda n: band(n, 'warm', '<div class="ub-schild"><div class="ub-sb auf">%s</div>%s</div>' % (
        foto('schildnacht', '', '(max-width:860px) 40vw, 14vw', auf=False, pos='50% 40%'), satz(['Unter dem Schild', 'wartet die Theke.'], 'ub-satz ub-satz-l')))),
    ('Kerzenschein', lambda n: band(n, 'warm', satz(['Drinnen brennen', 'schon die Kerzen.']), 'ub-glut')),
    ('Techniken als Brücke', lambda n: band(n, 'warm', '<div class="ub-tech sw auf">%s</div>' % ''.join(
        '<div><p class="ub-v">%s</p><p class="ub-klein">%s</p></div>' % (E(a.upper()), E(b)) for a, b in TECH))),
    ('Draussen und drinnen', lambda n: band(n, 'warm', '<div class="ub-split"><div><p class="ub-mono">Draussen</p>%s</div><div><p class="ub-mono">Drinnen</p>%s</div></div>' % (
        satz(['Haasemannstraße 13,', 'Linden.'], 'ub-satz ub-satz-m'), satz(['Kerzen, Theke,', 'dein Drink.'], 'ub-satz ub-satz-m')), 'ub-voll')),
    ('Kicker auf Linie', lambda n: band(n, 'warm', '<div class="ub-kicker sw auf"><i></i><span>Ohne Karte</span><i></i></div>')),
    ('Null Karten', lambda n: band(n, 'warm', '<div class="ub-null"><p class="ub-zahl zl auf"><span class="z"><span>0</span></span></p><div class="sw auf" style="--i:1"><p class="ub-mono">Getränkekarten</p><p class="ub-satz ub-satz-m">Dafür ein Drink,<br>der nur dir gehört.</p></div></div>')),
    ('Derya und Momo', lambda n: band(n, 'warm', '<div class="ub-zwei">%s%s<p class="ub-satz ub-satz-m sw auf" style="--i:2">Hinter der Theke:<br>Derya Ivkin und Momo.</p></div>' % (
        '<div class="ub-kopf auf">%s</div>' % foto('kopf_derya', '', '120px', auf=False), '<div class="ub-kopf auf" style="--i:1">%s</div>' % foto('kopf_momo', '', '120px', auf=False)))),
    ('Tresenkante', lambda n: band(n, 'warm', satz(['Setz dich an die Theke.']) + '<i class="ub-holz" aria-hidden="true"></i>', 'ub-voll')),
]

CSS = '''/* Übergang Hero → «Dein Drink» (uebergang_wahl.py). Nur für die Wahlseite. */
.ub{padding:clamp(48px,8vh,96px) var(--rand) 0;text-align:center;background:var(--bg);color:var(--fg)}
.ub[data-ton=hell]{padding-bottom:clamp(48px,8vh,96px);margin-top:clamp(40px,6vh,72px)}
.ub-satz{font:340 clamp(40px,5vw,88px)/1 var(--titel);letter-spacing:-.02em;font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 144;margin:0 auto}
.ub-satz .z{display:block}
.ub-satz-m{font-size:clamp(30px,3.2vw,54px)}
.ub-satz-l{text-align:left;margin:0}
.ub-mono{font:500 11px/1.4 var(--etikett);letter-spacing:.18em;text-transform:uppercase;color:var(--kerze-hell);margin:14px 0 0}
[data-ton=hell] .ub-mono{color:var(--kerze-tief)}
.ub-klein{color:var(--fg2);font-size:clamp(15px,1.2vw,17px);line-height:1.6;margin:16px auto 0;max-width:40ch}
.ub-lauf{overflow:hidden;margin:0 calc(-1 * var(--rand));padding:20px 0;border-block:1px solid var(--linie)}
.ub-lauf>div{display:flex;width:max-content;animation:ublauf 60s linear infinite}
.ub-lauf span{font:340 clamp(28px,2.8vw,46px)/1 var(--titel);font-variation-settings:"SOFT" 100,"opsz" 96;white-space:pre;color:var(--fg)}
@keyframes ublauf{to{transform:translateX(-50%)}}
html.ruhig .ub-lauf>div{animation:none}
.ub-zeichen{display:flex;align-items:center;gap:clamp(18px,3vw,44px);max-width:900px;margin:0 auto}
.ub-zeichen i{flex:1;height:1px;background:var(--linie)}
.ub-ws{width:clamp(56px,5vw,80px);height:auto;color:var(--kerze-hell)}
.ub-linie i{display:block;width:1px;height:clamp(110px,16vh,170px);margin:0 auto;background:var(--kerze);transform-origin:top;transform:scaleY(.2);transition:transform 1.6s cubic-bezier(.22,.68,.26,1)}
.ub-linie.da i{transform:none}
html.ruhig .ub-linie i{transform:none}
.ub-links{text-align:left}
.ub-links .fwk{margin-bottom:0}
body:has(#uebergang>.wv[data-n="6"]:not([hidden])) .v-bar-karte .wr-k>.fwk-titel,
body:has(#uebergang>.wv[data-n="6"]:not([hidden])) .v-bar-karte .wr-k>.fwk-text{display:none}
body:has(#uebergang>.wv[data-n="10"]:not([hidden])) .v-bar-karte .wr-k>div:has(>.vt){display:none}
.ub-gespraech{max-width:980px;margin:0 auto;display:grid;gap:10px}
.ub-gespraech p{margin:0;font:340 clamp(32px,3.8vw,64px)/1.05 var(--titel);font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 144}
.ub-frage{text-align:left;color:var(--kerze-hell)}
.ub-antwort{text-align:right}
.ub-schild{display:flex;align-items:center;justify-content:center;gap:clamp(24px,4vw,64px)}
.ub-sb{width:clamp(130px,13vw,200px);aspect-ratio:4/5;overflow:hidden;border-radius:4px;flex:none}
.ub-sb .foto{height:100%;width:100%;border-radius:0}
.ub-glut{background:radial-gradient(ellipse 60% 70% at 50% 70%,rgba(239,118,73,.22),rgba(239,118,73,0) 70%),linear-gradient(180deg,#1C1B21,#222028);padding-bottom:clamp(20px,3vh,36px)}
.ub-tech{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(18px,3vw,56px);max-width:1200px;margin:0 auto}
.ub-tech>div{padding-top:18px;border-top:1px solid var(--kerze)}
.ub-v{margin:0;font:340 clamp(22px,2.2vw,36px)/1 var(--titel);letter-spacing:.04em;font-variation-settings:"SOFT" 100,"opsz" 72}
.ub-split{display:grid;grid-template-columns:1fr 1fr;max-width:var(--max);margin:0 auto}
.ub-split>div{padding:clamp(32px,5vh,56px) clamp(20px,3vw,48px);display:flex;flex-direction:column-reverse;gap:12px;align-items:center}
.ub-split>div:first-child{background:#18171C}
.ub-split>div:last-child{background:radial-gradient(ellipse at 50% 80%,rgba(239,118,73,.2),rgba(239,118,73,0) 70%),#26232A}
.ub-kicker{display:flex;align-items:center;gap:20px;max-width:var(--max);margin:0 auto}
.ub-kicker i{flex:1;height:1px;background:var(--kerze);opacity:.55}
.ub-kicker span{font:500 12px/1 var(--etikett);letter-spacing:.24em;text-transform:uppercase;color:var(--kerze-hell)}
.ub-null{display:flex;align-items:center;justify-content:center;gap:clamp(20px,3vw,48px);text-align:left}
.ub-zahl{margin:0;font:300 clamp(120px,14vw,220px)/.8 var(--titel);color:var(--kerze-hell);font-variation-settings:"SOFT" 100,"opsz" 144}
.ub-null .ub-mono{margin:0 0 10px}
.ub-zwei{display:flex;align-items:center;justify-content:center;gap:clamp(12px,1.6vw,20px);width:max-content;max-width:100%;margin:0 auto}
.ub-kopf{width:clamp(76px,7vw,110px);aspect-ratio:1;border-radius:50%;overflow:hidden;flex:none}
.ub-kopf .foto{width:100%;height:100%;border-radius:0}
.ub-zwei .ub-satz{text-align:left;margin-left:clamp(10px,2vw,30px)}
.ub-holz{display:block;height:20px;margin:clamp(22px,3vh,32px) calc(-1 * var(--rand)) 0;background:linear-gradient(180deg,#6A4430,#2A1B13);box-shadow:inset 0 2px 0 var(--kerze)}
.ub-voll{padding-left:0;padding-right:0}.ub-voll .ub-holz{margin-left:0;margin-right:0}
@media (max-width:860px){
  .ub-tech,.ub-split{grid-template-columns:1fr}
  .ub-schild,.ub-null,.ub-zwei{flex-direction:column;text-align:center}
  .ub-satz-l,.ub-zwei .ub-satz{text-align:center;margin:0}
  .ub-antwort{text-align:left}
}'''


def main():
    s = open(os.path.join(HIER, 'bar.html'), encoding='utf-8').read()
    i = s.index('v-bar-karte')
    a = s.rindex('<section', 0, i)
    teile = ['<div class="wv" data-n="0"></div>']
    for n, (_name, mach) in enumerate(F, 1):
        teile.append('<div class="wv" data-n="%d" hidden>%s</div>' % (n, mach(n)))
    block = '<div class="wahl" id="uebergang" data-name="Übergang"><div class="wahl-marke"><b>Übergang</b><span data-nr>Fassung 0 · Ohne</span></div>%s</div>' % ''.join(teile)
    s = s[:a] + block + s[a:]
    s = s.replace('<title>', '<title>Auswahl · Übergang · ', 1)
    s = s.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<style>\n%s\n</style>\n</head>' % (bau.VERSION, CSS), 1)
    namen = ['Ohne'] + [n for n, _ in F]
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["uebergang"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), bau.VERSION)
    s = s.replace('</body>', leiste + '</body>', 1)
    ziel = os.path.join(HIER, 'uebergang-wahl.html')
    open(ziel, 'w', encoding='utf-8').write(s)
    print(ziel, len(F), 'Fassungen')


if __name__ == '__main__':
    main()
