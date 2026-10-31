#!/usr/bin/env python3
"""Culinarium Hannover · Übergang Kopf → Fenster auf abende.html in 15 Fassungen, zweite Runde, 27.10.2026.
Robert: «dieser Übergang … ist absoluter Bullshit, dieses Unscharfe vom Hero. Ins Fenster übergehende, was zur Hölle.
Ich will bitte 15 Möglichkeiten haben, diesen Übergang zu gestalten und selber entscheiden.»
Regeln für jede Fassung: kein Weichzeichner, keine Unschärfe, kein Verlauf ins Dunkle; jede Fassung eine eigene Idee;
Bewegung nur über transform und opacity. Fassung 0 ist der heutige Stand.
Baut abende-uebergang-wahl2.html aus abende.html: Leiste unten, Pfeiltasten ← →, ?ue=Nummer.
Aufruf: python3 website/bau.py && python3 website/uebergang_abende_wahl2.py"""
import json, os, random
import bau

HIER = os.path.dirname(os.path.abspath(__file__))
CREME = '#F4EEE8'
NACHT = '#0F0E13'

N = [
    'Heute: unscharf ins Dunkle, orange Linie',
    'Der Schnitt: Kante an Kante, ohne alles',
    'Die Fuge: ein schmaler heller Streifen trennt Kopf und Fenster',
    'Die Jahre: ein helles Band mit den vier Jahren und ihren Abenden',
    'Die Karte darüber: das Fenster legt sich mit runden Ecken über den Kopf',
    'Der Stapel: der Kopf bleibt stehen, das Fenster fährt darüber',
    'Die Papierkante: ein Streifen gerissenes Papier liegt auf der Naht',
    'Die Schräge: der Kopf endet in einer schrägen Kante',
    'Der Versatz: die linke Hälfte endet früher als die rechte',
    'Der Bogen: das Fenster öffnet sich oben als flacher Bogen',
    'Die Wortmarke: Culinarium steht gross über der Naht',
    'Das Laufband: alle Abende laufen als Zeile über ein dunkles Band',
    'Das Passepartout: das Fenster sitzt in einem hellen Rahmen',
    'Der Knauf: ein runder Knopf auf der Naht führt zu den Plakaten',
    'Die Kerzenlinie: eine klare orange Linie vom Titel ins Fenster',
    'Der Kartenrand: ein dunkles Band mit Doppellinie wie auf der Menükarte',
]

# Gerissene Papierkante: feste Zacken (Saat), damit sie bei jedem Bau gleich aussieht
random.seed(27)
oben = ' '.join('L%d %.1f' % (x, random.uniform(0, 12)) for x in range(0, 1001, 18))
unten = ' '.join('L%d %.1f' % (x, random.uniform(48, 60)) for x in range(1000, -1, -18))
PAPIER = '<svg viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 6 %s L1000 54 %s Z" fill="%s"/></svg>' % (oben, unten, CREME)

ZAHL = {'2023': 'Fünf Abende', '2024': 'Vier Abende', '2025': 'Drei Abende', '2026': 'Zwei Abende'}
JAHRE = ''.join('<div><b>%s</b><span>%s</span></div>' % (j, ZAHL[j]) for j in ('2023', '2024', '2025', '2026'))

import abende_info as _AI
lauf = []
for j, d, z, p, pid, mit in reversed(bau.ABENDE):
    m = (_AI.INFO.get(pid or 'ohne-%s' % j) or {}).get('motto')
    lauf.append('<span>%s %s%s</span>' % (bau.E(d), j, (' <em>%s</em>' % bau.E(m)) if m else ''))
LAUF = '<i>·</i>'.join(lauf)

EINSATZ = '''<div class="u2-zw" aria-hidden="true">
<div class="u2-fuge"></div>
<div class="u2-jahre">%s</div>
<div class="u2-papier">%s</div>
<div class="u2-marke">%s</div>
<div class="u2-lauf"><div class="u2-lauf-zug"><p>%s<i>·</i></p><p>%s<i>·</i></p></div></div>
<div class="u2-knauf"><a href="#plakate" tabindex="-1">%s</a></div>
<div class="u2-rand"><span></span><i>•••</i><span></span></div>
</div>
''' % (JAHRE, PAPIER, bau.marke('wm'), LAUF, LAUF, bau.PFEIL)

CSS = '''
/* Übergang Kopf → Fenster, zweite Runde (nur Wahlseite) */
.u2-zw>div{display:none}
/* ab Fassung 1: heutige Verläufe und Linien aus */
body[class*="u2-"] .kopf-geteilt::after,body[class*="u2-"] .kopf-geteilt::before,body[class*="u2-"] #fenster-abende::before,body[class*="u2-"] #fenster-abende::after{content:none}
.kopf-geteilt{position:relative}
.u2-zw{position:relative;z-index:6}
/* 2 Fuge */
body.u2-2 .u2-fuge{display:block;height:clamp(10px,1vw,14px);background:%(c)s}
/* 3 Die Jahre */
body.u2-3 .u2-jahre{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));background:%(c)s;color:#232129;padding:clamp(26px,4vh,40px) var(--rand)}
.u2-jahre div{display:flex;flex-direction:column;align-items:center;gap:8px;border-left:1px solid rgba(35,33,41,.18)}
.u2-jahre div:first-child{border-left:0}
.u2-jahre b{font:300 clamp(40px,4.6vw,72px)/.9 var(--titel);letter-spacing:-.02em;font-variation-settings:"SOFT" 100,"opsz" 144;color:#232129}
.u2-jahre span{font:500 11px/1 var(--mono);letter-spacing:.2em;text-transform:uppercase;color:#B15736}
/* 4 Karte darüber */
body.u2-4 .kopf-geteilt{z-index:1}
body.u2-4 #fenster-abende{z-index:2;margin-top:-10vh;clip-path:inset(0 round 30px 30px 0 0);-webkit-clip-path:inset(0 round 30px 30px 0 0)}
/* 5 Stapel */
body.u2-5 .kopf-geteilt{position:sticky;top:0;z-index:0}
body.u2-5 .kopf-geteilt~section,body.u2-5 .kopf-geteilt~footer{position:relative;z-index:1}
/* 6 Papierkante */
body.u2-6 .u2-papier{display:block;height:0}
.u2-papier svg{position:absolute;left:0;width:100%%;height:clamp(34px,4.4vw,56px);top:0;transform:translateY(-50%%);display:block}
/* 7 Schräge */
body.u2-7 .kopf-geteilt{z-index:2;clip-path:polygon(0 0,100%% 0,100%% 82%%,0 100%%);-webkit-clip-path:polygon(0 0,100%% 0,100%% 82%%,0 100%%)}
body.u2-7 #fenster-abende{z-index:1;margin-top:-18vh}
/* 8 Versatz */
body.u2-8 .kopf-geteilt{z-index:2;clip-path:polygon(0 0,100%% 0,100%% 100%%,50%% 100%%,50%% 86%%,0 86%%);-webkit-clip-path:polygon(0 0,100%% 0,100%% 100%%,50%% 100%%,50%% 86%%,0 86%%)}
body.u2-8 #fenster-abende{z-index:1;margin-top:-14vh}
/* 9 Bogen */
body.u2-9 .kopf-geteilt{z-index:1}
body.u2-9 #fenster-abende{z-index:2;margin-top:-13vh;clip-path:inset(0 round 50%% 50%% 0 0 / 13vh 13vh 0 0);-webkit-clip-path:inset(0 round 50%% 50%% 0 0 / 13vh 13vh 0 0)}
/* 10 Wortmarke über der Naht */
body.u2-10 .u2-marke{display:flex;justify-content:center;align-items:flex-start;height:0}
.u2-marke .marke{width:min(860px,82vw);height:auto;aspect-ratio:4650/564;flex:none;color:var(--kerze);transform:translateY(-50%%)}
/* 11 Laufband */
body.u2-11 .u2-lauf{display:block;background:%(n)s;border-top:1px solid rgba(250,244,244,.12);border-bottom:1px solid rgba(250,244,244,.12);overflow:hidden;padding:20px 0}
.u2-lauf-zug{display:flex;width:max-content;animation:u2-lauf 70s linear infinite}
.u2-lauf-zug p{display:flex;align-items:baseline;white-space:nowrap;font:400 clamp(20px,2vw,28px)/1 var(--titel);color:#FAF4F4}
.u2-lauf-zug span{padding:0 22px}.u2-lauf-zug em{font-style:italic;color:var(--kerze-hell,#F5A689);margin-left:10px}
.u2-lauf-zug i{font-style:normal;color:var(--kerze)}
@keyframes u2-lauf{to{transform:translateX(-50%%)}}
@media (prefers-reduced-motion:reduce){.u2-lauf-zug{animation:none}}
/* 12 Passepartout */
body.u2-12 #fenster-abende::after{content:"";position:absolute;inset:0;width:auto;height:auto;margin:0;background:none;z-index:3;pointer-events:none;border:clamp(14px,2.2vw,30px) solid %(c)s}
body.u2-12 #fenster-abende::before{content:"";position:absolute;inset:clamp(14px,2.2vw,30px);width:auto;height:auto;margin:0;background:none;z-index:3;pointer-events:none;border-radius:18px;box-shadow:0 0 0 20px %(c)s}
body.u2-12 #fenster-abende{background:%(c)s}
/* 13 Knauf */
body.u2-13 .u2-knauf{display:flex;justify-content:center;align-items:flex-start;height:0}
.u2-knauf a{flex:none;display:grid;place-items:center;width:clamp(76px,7vw,96px);aspect-ratio:1;border-radius:50%%;background:%(c)s;color:#1A1218;transform:translateY(-50%%);box-shadow:inset 0 -6px 0 rgba(35,33,41,.12),0 0 0 6px rgba(244,238,232,.22);transition:transform .5s var(--feder)}
.u2-knauf a svg{width:30px;height:30px;transform:rotate(90deg)}
.u2-knauf a:hover{transform:translateY(-46%%)}
/* 14 Kerzenlinie */
body.u2-14 .kopf-geteilt::before{content:"";position:absolute;left:50%%;bottom:0;width:2px;margin-left:-1px;height:16vh;z-index:2;background:var(--kerze)}
body.u2-14 #fenster-abende::after{content:"";position:absolute;left:50%%;top:0;width:2px;margin-left:-1px;height:16vh;z-index:2;background:var(--kerze)}
/* 15 Kartenrand */
body.u2-15 .u2-rand{display:flex;align-items:center;gap:22px;background:%(n)s;padding:clamp(28px,4.5vh,44px) var(--rand)}
.u2-rand span{flex:1;height:5px;border-top:1px solid rgba(250,244,244,.55);border-bottom:1px solid rgba(250,244,244,.55)}
.u2-rand i{font-style:normal;color:var(--kerze);letter-spacing:.4em;font-size:18px;padding-left:.4em}
@media (max-width:860px){body.u2-3 .u2-jahre{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:22px}.u2-jahre div:nth-child(3){border-left:0}
  body.u2-4 #fenster-abende,body.u2-9 #fenster-abende{margin-top:-7svh}body.u2-9 #fenster-abende{clip-path:inset(0 round 50%% 50%% 0 0 / 7svh 7svh 0 0);-webkit-clip-path:inset(0 round 50%% 50%% 0 0 / 7svh 7svh 0 0)}}
''' % {'c': CREME, 'n': NACHT}

LEISTE = r'''<script>
/* Übergang wählen (?ue=N): ← → oder Klick wechseln; 0 = heute */
(function () {
  var N = %s, b = document.body, f = document.getElementById('fenster-abende');
  var n = parseInt(new URLSearchParams(location.search).get('ue'), 10); if (!(n >= 0 && n < N.length)) n = 1;
  var t = document.createElement('div');
  t.style.cssText = 'position:fixed;left:50%%;bottom:18px;transform:translateX(-50%%);z-index:300;background:#16151A;color:#FAF4F4;border:1px solid rgba(239,118,73,.6);border-radius:999px;padding:8px 10px;font:500 13px/1 Urbanist,sans-serif;letter-spacing:.06em;display:flex;gap:14px;align-items:center;white-space:nowrap;max-width:calc(100vw - 24px);overflow:hidden';
  var k = 'background:none;border:0;color:#F5A689;font:400 22px/1 Urbanist,sans-serif;cursor:pointer;padding:2px 10px';
  t.innerHTML = '<button type="button" style="' + k + '" data-s="-1" aria-label="Voriger Übergang">‹</button><span data-i style="overflow:hidden;text-overflow:ellipsis"></span><button type="button" style="' + k + '" data-s="1" aria-label="Nächster Übergang">›</button>';
  b.appendChild(t);
  function zeig(i) {
    n = (i + N.length) %% N.length;
    for (var j = 1; j < N.length; j++) b.classList.toggle('u2-' + j, j === n);
    t.querySelector('[data-i]').innerHTML = '<span style="color:#F5A689">' + n + ' / ' + (N.length - 1) + '</span>&nbsp;&nbsp;' + N[n];
    history.replaceState(null, '', '?ue=' + n);
  }
  t.addEventListener('click', function (e) { var x = e.target.closest('[data-s]'); if (x) zeig(n + +x.dataset.s); });
  addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); zeig(n + 1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); zeig(n - 1); } });
  document.addEventListener('click', function (e) { var a = e.target.closest('.u2-knauf a'); if (a) { e.preventDefault(); var j = document.querySelector('.jahre'); scrollTo({ top: j.getBoundingClientRect().top + scrollY - 70, behavior: 'smooth' }); } });
  zeig(n);
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  /* Naht in die Bildmitte, damit man den Übergang sofort sieht */
  function hin() { scrollTo(0, f.getBoundingClientRect().top + scrollY - innerHeight * .5); }
  addEventListener('load', function () { setTimeout(hin, 150); setTimeout(hin, 900); });
})();
</script>
''' % json.dumps(N, ensure_ascii=False)

h = open(os.path.join(HIER, 'abende.html'), encoding='utf-8').read()
assert '<section class="kopf-geteilt"' in h and 'id="fenster-abende"' in h, 'Kopf oder Fenster fehlt in abende.html (erst bau.py laufen lassen)'
h = h.replace('<title>', '<title>Übergang wählen · ', 1)
h = h.replace('</head>', '<style>%s</style>\n</head>' % CSS, 1)
h = h.replace('<section class="fenster" id="fenster-abende"', EINSATZ + '<section class="fenster" id="fenster-abende"', 1)
h = h.replace('</body>', LEISTE + '</body>', 1)
open(os.path.join(HIER, 'abende-uebergang-wahl2.html'), 'w', encoding='utf-8').write(h)
print('abende-uebergang-wahl2.html: %d Fassungen + heute' % (len(N) - 1))
