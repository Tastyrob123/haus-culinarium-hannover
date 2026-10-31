#!/usr/bin/env python3
"""Baustein in der Werkbank Culinarium (Werkbank-Chat 28.10.2026), über das Schäfli kopiert; die Herkunft steht darunter wie in der Vorlage.
Werkbank Landgasthof Ruedihus, Auftakt: die drei Abzüge als Kacheln im Raum statt Polaroids (12.10.2026, Master 5b, Punkt 1).

Bildschirm und Handy bleiben, wie das Kit sie setzt. Die drei Abzüge (.abzug--1, --2, --3) werden Kacheln:
Foto mit runden Ecken wie die Zimmer-Kacheln der Ruedihus-Seite, warme Lichtkante oben, tiefer Schatten im Holzton, leicht im Raum gedreht,
Neigung zum Zeiger, kein Anheben. Eingehängt in haus.py: CSS am Dateiende, anwenden() in nach_bau()."""
import os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)

CSS = '''
/* ---------- Auftakt: Kacheln statt Polaroids (auftakt_kacheln.py, 12.10.2026) ---------- */
.stapel{container-type:inline-size}
.stapel .tel{z-index:3}
.akz{margin:0;perspective:800px;z-index:2;--f:1;--rad:clamp(12px,2.9cqw,22px)}
.akz__b{display:block;position:relative;aspect-ratio:var(--f);overflow:hidden;border-radius:var(--rad);background:#2a180a;
  box-shadow:0 0 0 1px rgba(243,205,148,.2),0 3px 0 #120904,0 40px 56px -26px rgba(8,4,1,.85),0 14px 22px -12px rgba(8,4,1,.6);
  transform:translateZ(0) rotateX(var(--rx,0deg)) rotateY(calc(var(--by,0deg) + var(--ry,0deg)));transition:transform .8s var(--e2)}
.akz.kipp .akz__b{transition:transform .2s ease-out}
.akz__b>img{display:block;width:100%;height:100%;aspect-ratio:auto;object-fit:cover}
.akz__b::after{content:'';position:absolute;inset:0;border-radius:inherit;pointer-events:none;box-shadow:inset 0 1px 0 rgba(255,236,200,.34),inset 0 0 0 1px rgba(243,205,148,.2)}
.stapel .akz--a{left:-6%;top:-8%;width:30%;--f:3/2;--r:-3deg;--r0:-12deg;--by:10deg}
.stapel .akz--b{right:4.5%;top:-9%;width:18%;--f:4/5;--r:3deg;--r0:12deg;--by:-10deg}
.stapel .akz--c{left:31%;bottom:1%;width:23%;--f:5/4;--r:2deg;--r0:9deg;--by:8deg}
@media(max-width:560px){.stapel .akz--c{display:none}}
@media(min-width:1001px){.stapel{margin-top:clamp(64px,6.2vw,96px)}}   /* Robert 29.10.2026: «im Hero sind die Bilder oben an der Leiste zu nah»: die ganze Gruppe rückt tiefer, mindestens 48 px Luft unter der Leiste */
'''

JS = '''<script id="auftakt-kacheln">
/* Kacheln im Auftakt neigen sich zum Zeiger (nur transform); nach jedem Scrollen 300 ms Ruhe, kein Anheben */
(function(){
  if(!matchMedia('(hover:hover) and (pointer:fine)').matches||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  var ruhe=0;addEventListener('scroll',function(){ruhe=Date.now()+300;},{passive:true});
  [].forEach.call(document.querySelectorAll('.akz'),function(k){
    var b=k.querySelector('.akz__b'),t=0;
    k.addEventListener('pointermove',function(e){
      if(Date.now()<ruhe||t)return;
      t=requestAnimationFrame(function(){t=0;var r=k.getBoundingClientRect();
        k.classList.add('kipp');
        b.style.setProperty('--ry',(((e.clientX-r.left)/r.width-.5)*9).toFixed(2)+'deg');
        b.style.setProperty('--rx',((.5-(e.clientY-r.top)/r.height)*9).toFixed(2)+'deg');});
    });
    k.addEventListener('pointerleave',function(){k.classList.remove('kipp');b.style.setProperty('--ry','0deg');b.style.setProperty('--rx','0deg');});
  });
})();
</script>
'''

PLATZ = {'1': ('a', 6), '3': ('b', 7), '2': ('c', 8)}   # Abzug des Kits → Platz der Kachel, Reihenfolge des Hereinkommens
ABZUG = re.compile(r'<div class="abzug abzug--([123])" data-a="schweb" data-drift="([^"]+)">(<img[^>]*>)<span>[^<]*</span></div>')


def setz(t):
    """Macht in der gebauten Werkbank aus den drei Abzügen des Auftakts Kacheln und hängt das Neige-Skript an. Mehrfach anwendbar."""
    a = t.find('<div class="stapel"')
    if a < 0:
        return t
    e = t.find('<div class="tel"', a)
    kopf, block, rest = t[:a], t[a:e], t[e:]

    def kachel(m):
        platz, i = PLATZ[m.group(1)]
        return (f'<figure class="akz akz--{platz}" data-a="schweb" data-drift="{m.group(2)}" style="--i:{i}">'
                f'<span class="akz__b">{m.group(3)}</span></figure>')
    t = kopf + ABZUG.sub(kachel, block) + rest
    if 'class="akz ' in t and 'id="auftakt-kacheln"' not in t:
        t = re.sub(r'(<script src="werkbank\.js)', lambda m: JS + m.group(1), t, count=1)
    return t


def anwenden(pfad):
    if not os.path.exists(pfad) or os.path.getsize(pfad) == 0:
        return False
    alt = open(pfad, encoding='utf-8').read()
    neu = setz(alt)
    if neu != alt:
        tmp = pfad + f'.{os.getpid()}.tmp'
        open(tmp, 'w', encoding='utf-8').write(neu)
        os.replace(tmp, pfad)
    return neu != alt
