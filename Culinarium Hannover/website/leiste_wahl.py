#!/usr/bin/env python3
"""Culinarium Hannover · 15 Fassungen der Leiste im Auftakt, 26.10.2026.
Robert: «GIB MIR 15 visuelle darstellungsmöglichketen der leiste im Hero».
Baut leiste-wahl.html: alle 15 untereinander, jede über dem Auftaktfoto, oben «Heute» zum Vergleich.
Knopf «Handy» zeigt dieselben Leisten in 390 px Breite.
Aufruf: python3 website/leiste_wahl.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bau import E, NAV, VERSION

HIER = os.path.dirname(os.path.abspath(__file__))
WM = '<svg class="marke" viewBox="0 0 4650 564" role="img" aria-label="Culinarium"><use href="assets/zeichen/marke.svg?v=%s#wm"/></svg>' % VERSION
MENUE = '<button class="lb-menue" type="button"><i></i><span>Menü</span></button>'


def links(paare=NAV, fmt='%s'):
    return ''.join('<a href="#">%s</a>' % (fmt % E(t)) for h, t in paare)


def marke():
    return '<a class="lb-marke" href="#">%s</a>' % WM


def standard(knopf='<a class="lb-knopf" href="#"><span>Warteliste</span></a>'):
    return '%s<nav class="lb-nav">%s</nav>%s%s' % (marke(), links(), knopf, MENUE)


# ------------------------------------------------------------------ die Fassungen: (Name, Satz, Klasse, Leiste)
F = [('Heute', 'So steht sie jetzt: dunkler Balken, volle Breite, oranger Knopf.', 'v0', standard())]

F.append(('Glas', 'Die Leiste wird durchsichtig, das Foto läuft verschwommen darunter weiter.', 'v1', standard()))

F.append(('Frei', 'Kein Balken mehr. Schrift steht direkt im Bild, oben ein weicher Schatten; der Knopf nur als Umriss.',
          'v2', standard()))

F.append(('Kapsel', 'Eine schwebende, abgerundete Leiste mit Abstand zum Rand, mittig über dem Foto.', 'v3', standard()))

F.append(('Zwei Inseln', 'Marke links und Seiten rechts als zwei getrennte Glasinseln; dazwischen bleibt das Foto frei.',
          'v4', '%s<div class="insel"><nav class="lb-nav">%s</nav><a class="lb-knopf" href="#"><span>Warteliste</span></a></div>%s'
          % (marke(), links(), MENUE)))

F.append(('Mittelachse', 'Marke in der Mitte, die Seiten links und rechts davon verteilt, wie über einer Tafel.',
          'v5', '<nav class="lb-nav links">%s</nav>%s<nav class="lb-nav rechts">%s<a class="lb-knopf" href="#"><span>Warteliste</span></a></nav>%s'
          % (links(NAV[:3]), marke(), links(NAV[3:]), MENUE)))

F.append(('Zwei Stockwerke', 'Darüber eine feine Zeile mit Ort und nächstem Abend, darunter die eigentliche Leiste.',
          'v6', '<div class="ober"><span>Walk on the Wild Side · Haasemannstraße 13 · Hannover-Linden</span>'
          '<span><b></b>Nächster Abend: Termin folgt · 14 Plätze</span></div><div class="unter">%s</div>' % standard()))

F.append(('Kerzenstrich', 'Offen über dem Foto, unten ein feiner oranger Strich; Warteliste als Wort mit Pfeil statt Knopf.',
          'v7', standard('<a class="lb-knopf" href="#"><span>Warteliste</span><i>→</i></a>')))

F.append(('Etikett', 'Nummerierte Seiten in Schreibmaschinenschrift, eckiger Knopf, wie ein Speisekarten-Kopf.',
          'v8', '%s<nav class="lb-nav">%s</nav><a class="lb-knopf" href="#"><span>Warteliste</span></a>%s'
          % (marke(), ''.join('<a href="#"><b>%02d</b>%s</a>' % (i + 1, E(t)) for i, (h, t) in enumerate(NAV)), MENUE)))

F.append(('Seitlich', 'Die Leiste steht senkrecht links neben dem Foto; Seiten untereinander, Knopf unten.',
          'v9', '%s<nav class="lb-nav">%s</nav><a class="lb-knopf" href="#"><span>Warteliste</span></a>%s' % (marke(), links(), MENUE)))

F.append(('Unten', 'Die Leiste liegt am unteren Rand des Fotos und rückt erst beim Scrollen nach oben fest.', 'v10', standard()))

F.append(('Nur Marke', 'Nichts als Marke, Warteliste und Menü. Die Seiten öffnen sich erst über das Menü.',
          'v11', '%s<a class="lb-knopf" href="#"><span>Warteliste</span></a><button class="lb-menue immer" type="button"><i></i><span>Menü</span></button>' % marke()))

F.append(('Papier', 'Eine helle, schwebende Karte über dem dunklen Foto, wie eine Menükarte auf dem Tisch.', 'v12', standard()))

F.append(('Ticket', 'Rechts ein orangener Abriss mit Lochrand: Warteliste mit Platzzahl, wie eine Eintrittskarte.',
          'v13', '%s<nav class="lb-nav">%s</nav><a class="lb-knopf" href="#"><small>14 Plätze · Termin folgt</small><span>Warteliste</span></a>%s'
          % (marke(), links(), MENUE)))

F.append(('Serifen', 'Die Seiten in der Titelschrift, mit Punkten getrennt; Warteliste als unterstrichener Satz.',
          'v14', standard('<a class="lb-knopf" href="#"><span>Auf die Warteliste</span></a>')))

F.append(('Kerzenfläche', 'Die ganze Leiste in Kerzenorange, Schrift dunkel, Knopf dunkel. Laut und unverwechselbar.', 'v15', standard()))


def fassung(n, name, satz, cls, leiste):
    nr = 'Heute' if n == 0 else '%02d' % n
    return '''<section class="fa" id="f%d">
  <div class="fa-kopf"><span class="fa-nr">%s</span><h2>%s</h2><p>%s</p></div>
  <div class="held %s"><header class="lb">%s</header>
    <p class="held-satz">Drei Gänge.<br>Fünf Drinks.<br>Vierzehn Plätze.</p></div>
</section>''' % (n, nr, E(name), E(satz), cls, leiste)


CSS = r'''
@font-face{font-family:"Fraunces";src:url(assets/schrift/fraunces-soft.woff2) format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:"Urbanist";src:url(assets/schrift/urbanist.woff2) format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:"Instrument Sans";src:url(assets/schrift/instrument.woff2) format("woff2");font-weight:400 600;font-display:swap}
@font-face{font-family:"DM Mono";src:url(assets/schrift/dmmono.woff2) format("woff2");font-weight:400;font-display:swap}
:root{--nacht:#16151A;--nacht-tief:#0F0E13;--weiss:#FAF4F4;--kerze:#EF7649;--kerze-hell:#F5A689;--kerze-tief:#B15736;--dc:#8953A9;
  --titel:"Fraunces",Georgia,serif;--text:"Instrument Sans",system-ui,sans-serif;--etikett:"Urbanist",system-ui,sans-serif;--mono:"DM Mono",ui-monospace,monospace;
  --rand:clamp(16px,3vw,40px);--glas:rgba(22,21,26,.55)}
*{box-sizing:border-box;margin:0}
html{background:var(--nacht-tief);color:var(--weiss);font:400 16px/1.5 var(--text);-webkit-font-smoothing:antialiased}
body{padding:0 var(--rand) 120px;max-width:1500px;margin:0 auto}
a{color:inherit;text-decoration:none}
button{font:inherit;color:inherit;cursor:pointer}

.kopf{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:20px;padding:56px 0 28px;border-bottom:1px solid rgba(250,244,244,.12)}
.kopf h1{font-family:var(--titel);font-weight:340;font-size:clamp(34px,4vw,56px);line-height:1;font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 144}
.kopf p{margin-top:10px;color:rgba(250,244,244,.7);max-width:620px}
.schalter{display:flex;border:1px solid rgba(250,244,244,.2);border-radius:999px;padding:4px}
.schalter button{border:0;background:none;padding:8px 18px;border-radius:999px;font:500 14px/1 var(--etikett);letter-spacing:.03em;color:rgba(250,244,244,.7)}
.schalter button[aria-pressed=true]{background:var(--weiss);color:var(--nacht)}
.sprung{display:flex;flex-wrap:wrap;gap:6px;padding:18px 0 8px}
.sprung a{font:400 12px/1 var(--mono);padding:8px 10px;border:1px solid rgba(250,244,244,.16);border-radius:6px;color:rgba(250,244,244,.75)}
.sprung a:hover{border-color:var(--kerze);color:var(--weiss)}

.fa{padding-top:56px}
.fa-kopf{display:grid;grid-template-columns:auto 1fr;column-gap:16px;align-items:baseline;margin-bottom:16px}
.fa-nr{font:400 13px/1 var(--mono);color:var(--kerze);letter-spacing:.06em}
.fa-kopf h2{font-family:var(--titel);font-weight:340;font-size:30px;line-height:1.1;font-variation-settings:"SOFT" 100,"opsz" 72}
.fa-kopf p{grid-column:2;color:rgba(250,244,244,.68);font-size:15px;margin-top:4px;max-width:720px}
#f0 .fa-nr{color:rgba(250,244,244,.5)}

/* Auftakt-Ausschnitt */
.held{position:relative;container-type:inline-size;height:clamp(380px,36vw,500px);border-radius:10px;overflow:hidden;margin:0 auto;
  background:#222 url(assets/bild/anstossen-1600.webp?v=VERSION) 50% 42%/cover;transition:max-width .5s cubic-bezier(.22,.68,.26,1)}
.held::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(15,14,19,.72),rgba(15,14,19,0) 55%);pointer-events:none}
.held-satz{position:absolute;z-index:1;left:32px;bottom:28px;font-family:var(--titel);font-weight:340;font-size:clamp(28px,3.4vw,46px);line-height:1;
  letter-spacing:-.012em;font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 144}
body.handy .held{max-width:390px;height:700px}
body.handy .held-satz{left:20px;font-size:34px}

/* Grundleiste */
.lb{position:absolute;z-index:3;inset:0 0 auto;height:64px;display:flex;align-items:center;gap:28px;padding:0 32px;color:var(--weiss)}
.lb-marke{display:block;line-height:0;color:inherit}
.lb .marke{height:17px;width:auto;fill:currentColor}
.lb-nav{display:flex;gap:26px;margin-left:auto}
.lb-nav a{font:500 14px/1 var(--etikett);letter-spacing:.04em;color:rgba(250,244,244,.8);padding:8px 0;position:relative;white-space:nowrap;transition:color .2s}
.lb-nav a:hover{color:var(--weiss)}
.lb-knopf{display:inline-flex;align-items:center;gap:8px;height:38px;padding:0 18px;border-radius:999px;background:var(--kerze);color:#fff;
  font:500 14px/1 var(--etikett);letter-spacing:.03em;white-space:nowrap;box-shadow:inset 0 1px 0 rgba(255,255,255,.3),0 8px 18px -10px rgba(207,114,51,.9);transition:background .2s,color .2s}
.lb-knopf:hover{background:#F1875F}
.lb-menue{display:none;align-items:center;gap:10px;margin-left:auto;height:38px;padding:0 16px;border-radius:999px;border:1px solid rgba(250,244,244,.28);background:transparent;font:500 14px/1 var(--etikett)}
.lb-menue i{width:16px;height:7px;border-top:1.5px solid currentColor;border-bottom:1.5px solid currentColor}
@container (max-width:900px){
  .lb{padding:0 20px;gap:12px}
  .lb-nav,.lb .lb-knopf{display:none}
  .lb-menue{display:inline-flex}
}

/* 0 Heute */
.v0 .lb{background:var(--nacht);border-bottom:1px solid rgba(250,244,244,.08)}

/* 1 Glas */
.v1 .lb{background:rgba(22,21,26,.34);-webkit-backdrop-filter:blur(16px) saturate(1.3);backdrop-filter:blur(16px) saturate(1.3);border-bottom:1px solid rgba(250,244,244,.14)}

/* 2 Frei */
.v2 .lb{height:84px;align-items:flex-start;padding-top:24px}
.v2::before{content:"";position:absolute;z-index:2;inset:0 0 auto;height:170px;background:linear-gradient(180deg,rgba(15,14,19,.78),rgba(15,14,19,0));pointer-events:none}
.v2 .lb-nav a{text-shadow:0 1px 12px rgba(0,0,0,.4)}
.v2 .lb-knopf{background:transparent;box-shadow:inset 0 0 0 1px rgba(250,244,244,.55);margin-top:-9px}
.v2 .lb-knopf:hover{background:var(--kerze);box-shadow:none}
.v2 .lb-menue{margin-top:-9px}

/* 3 Kapsel */
.v3 .lb{top:18px;left:50%;right:auto;transform:translateX(-50%);width:min(1080px,calc(100% - 48px));height:58px;padding:0 9px 0 26px;border-radius:999px;
  background:rgba(22,21,26,.6);-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);border:1px solid rgba(250,244,244,.14);box-shadow:0 20px 40px -24px rgba(0,0,0,.6)}
.v3 .lb-knopf{height:40px}
@container (max-width:900px){.v3 .lb{width:calc(100% - 24px);top:12px;padding:0 8px 0 20px}}

/* 4 Zwei Inseln */
.v4 .lb{top:18px;height:56px;padding:0 24px}
.v4 .lb-marke{height:52px;display:flex;align-items:center;padding:0 22px;border-radius:999px;background:var(--glas);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border:1px solid rgba(250,244,244,.13)}
.v4 .insel{margin-left:auto;display:flex;align-items:center;gap:22px;height:52px;padding:0 7px 0 24px;border-radius:999px;background:var(--glas);
  -webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border:1px solid rgba(250,244,244,.13)}
.v4 .lb-nav{gap:22px}
@container (max-width:900px){.v4 .insel{display:none}.v4 .lb{padding:0 12px}.v4 .lb-menue{height:52px;background:var(--glas);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px)}}

/* 5 Mittelachse */
.v5 .lb{display:grid;grid-template-columns:1fr auto 1fr;height:88px;background:linear-gradient(180deg,rgba(15,14,19,.75),rgba(15,14,19,0))}
.v5 .lb-nav{margin:0;gap:28px;align-items:center}
.v5 .lb-nav.rechts{justify-content:flex-end}
.v5 .lb .marke{height:22px}
.v5 .lb-knopf{height:34px;padding:0 14px;margin-left:4px}
@container (max-width:900px){.v5 .lb{display:flex}.v5 .lb-nav{display:none}}

/* 6 Zwei Stockwerke */
.v6 .lb{display:block;height:auto;padding:0}
.v6 .ober{display:flex;justify-content:space-between;gap:20px;height:32px;align-items:center;padding:0 32px;background:var(--nacht-tief);
  font:400 11px/1 var(--mono);letter-spacing:.07em;text-transform:uppercase;color:rgba(250,244,244,.62)}
.v6 .ober b{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--kerze);margin-right:9px;vertical-align:1px;box-shadow:0 0 0 4px rgba(239,118,73,.18)}
.v6 .unter{display:flex;align-items:center;gap:28px;height:62px;padding:0 32px;background:rgba(22,21,26,.5);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-bottom:1px solid rgba(250,244,244,.1)}
@container (max-width:900px){.v6 .ober span:first-child{display:none}.v6 .ober,.v6 .unter{padding:0 20px}.v6 .ober{justify-content:flex-start}}

/* 7 Kerzenstrich */
.v7 .lb{height:72px;background:linear-gradient(180deg,rgba(15,14,19,.6),rgba(15,14,19,.15));border-bottom:1px solid var(--kerze)}
.v7 .lb-nav a::after{content:"";position:absolute;left:50%;bottom:-6px;width:5px;height:5px;margin-left:-2.5px;border-radius:50%;background:var(--kerze);opacity:0;transform:translateY(4px);transition:.25s}
.v7 .lb-nav a:hover::after{opacity:1;transform:none}
.v7 .lb-knopf{background:none;box-shadow:none;padding:0;color:var(--kerze-hell);font-weight:600}
.v7 .lb-knopf i{font-style:normal;transition:transform .25s}
.v7 .lb-knopf:hover{background:none;color:var(--kerze)}
.v7 .lb-knopf:hover i{transform:translateX(4px)}

/* 8 Etikett */
.v8 .lb{background:var(--nacht);height:60px;border-bottom:1px solid rgba(250,244,244,.1)}
.v8 .lb-nav{gap:22px}
.v8 .lb-nav a{font:400 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:rgba(250,244,244,.72)}
.v8 .lb-nav b{font-weight:400;color:var(--kerze);margin-right:7px}
.v8 .lb-knopf{border-radius:3px;height:34px;font:400 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;box-shadow:none}

/* 9 Seitlich */
.v9 .lb{inset:0 auto 0 0;width:230px;height:auto;flex-direction:column;align-items:flex-start;gap:0;padding:30px 28px;
  background:rgba(15,14,19,.66);-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);border-right:1px solid rgba(250,244,244,.1)}
.v9 .lb .marke{height:15px}
.v9 .lb-nav{flex-direction:column;gap:2px;margin:auto 0}
.v9 .lb-nav a{font-family:var(--titel);font-weight:340;font-size:21px;letter-spacing:0;font-variation-settings:"SOFT" 100,"opsz" 48;padding:6px 0}
.v9 .lb-nav a:hover{color:var(--kerze-hell)}
.v9 .held-satz,.v9 .held-satz{left:262px}
@container (max-width:900px){
  .v9 .lb{inset:0 0 auto;width:auto;height:64px;flex-direction:row;align-items:center;padding:0 20px;border-right:0}
  .v9 .held-satz{left:20px}}
.v9 .lb-menue{margin-left:auto}

/* 10 Unten */
.v10 .lb{inset:auto 0 0;height:68px;background:rgba(15,14,19,.55);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border-top:1px solid rgba(250,244,244,.12)}
.v10 .held-satz{bottom:100px}
.v10::after{background:linear-gradient(0deg,rgba(15,14,19,.6),rgba(15,14,19,0) 60%)}

/* 11 Nur Marke */
.v11 .lb{height:92px;gap:12px;background:linear-gradient(180deg,rgba(15,14,19,.7),rgba(15,14,19,0))}
.v11 .lb .marke{height:24px}
.v11 .lb-knopf{margin-left:auto}
.v11 .lb-menue.immer{display:inline-flex;margin-left:0;height:38px;background:rgba(250,244,244,.1);border-color:rgba(250,244,244,.3);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
@container (max-width:900px){.v11 .lb-knopf{display:inline-flex}.v11 .lb .marke{height:17px}.v11 .lb{height:70px}}

/* 12 Papier */
.v12 .lb{top:16px;left:24px;right:24px;height:60px;border-radius:10px;background:#FAF4F4;color:#26242D;padding:0 10px 0 24px;box-shadow:0 22px 44px -22px rgba(0,0,0,.7)}
.v12 .lb-nav a{color:rgba(38,36,45,.72)}
.v12 .lb-nav a:hover{color:#26242D}
.v12 .lb-knopf{border-radius:7px;box-shadow:none}
.v12 .lb-menue{border-color:rgba(38,36,45,.25)}
@container (max-width:900px){.v12 .lb{left:12px;right:12px;top:12px}}

/* 13 Ticket */
.v13 .lb{background:var(--nacht);padding-right:0;height:66px;border-bottom:1px solid rgba(250,244,244,.08)}
.v13 .lb-knopf{height:100%;border-radius:0;flex-direction:column;justify-content:center;align-items:flex-start;gap:5px;padding:0 30px 0 34px;box-shadow:none;
  -webkit-mask:radial-gradient(circle 7px at 0 0,#0000 98%,#000) top/100% 51% no-repeat,radial-gradient(circle 7px at 0 100%,#0000 98%,#000) bottom/100% 51% no-repeat;
  mask:radial-gradient(circle 7px at 0 0,#0000 98%,#000) top/100% 51% no-repeat,radial-gradient(circle 7px at 0 100%,#0000 98%,#000) bottom/100% 51% no-repeat;position:relative}
.v13 .lb-knopf::before{content:"";position:absolute;left:0;top:11px;bottom:11px;border-left:2px dashed rgba(22,21,26,.45)}
.v13 .lb-knopf small{font:400 10.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:rgba(22,21,26,.72)}
.v13 .lb-knopf span{font:600 15px/1 var(--etikett);letter-spacing:.03em;color:var(--nacht)}
@container (max-width:900px){.v13 .lb{padding-right:20px}}

/* 14 Serifen */
.v14 .lb{height:84px;background:linear-gradient(180deg,rgba(15,14,19,.72),rgba(15,14,19,0))}
.v14 .lb-nav{gap:0}
.v14 .lb-nav a{font-family:var(--titel);font-weight:340;font-size:18px;letter-spacing:0;font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 36}
.v14 .lb-nav a+a::before{content:"·";position:absolute;left:-2px;color:var(--kerze);transform:translateX(-50%)}
.v14 .lb-nav a+a{margin-left:26px}
.v14 .lb-knopf{background:none;box-shadow:none;padding:0;height:auto;font-family:var(--titel);font-weight:340;font-size:18px;letter-spacing:0;font-style:italic;
  font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 36;border-bottom:1px solid var(--kerze);border-radius:0;padding-bottom:3px;margin-left:10px}
.v14 .lb-knopf:hover{background:none;color:var(--kerze-hell)}

/* 15 Kerzenfläche */
.v15 .lb{background:var(--kerze);color:var(--nacht)}
.v15 .lb-nav a{color:rgba(22,21,26,.78);font-weight:600}
.v15 .lb-nav a:hover{color:var(--nacht)}
.v15 .lb-knopf{background:var(--nacht);color:var(--weiss);box-shadow:none}
.v15 .lb-knopf:hover{background:#2A2833}
.v15 .lb-menue{border-color:rgba(22,21,26,.35)}
'''.replace('VERSION', VERSION)

JS = '''document.querySelectorAll('.schalter button').forEach(function(b){b.addEventListener('click',function(){
  document.querySelectorAll('.schalter button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
  document.body.classList.toggle('handy',b.dataset.w==='handy')})});
document.querySelectorAll('.held a[href="#"],.held button').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault()})});'''


def seite():
    sprung = ''.join('<a href="#f%d">%s</a>' % (n, 'Heute' if n == 0 else '%02d %s' % (n, E(f[0]))) for n, f in enumerate(F))
    return '''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Leiste · 15 Fassungen</title>
<style>%s</style>
</head>
<body>
<div class="kopf"><div><h1>Die Leiste im Auftakt</h1><p>15 Fassungen über dem Auftaktfoto, oben die heutige zum Vergleich. Mit der Maus über die Seiten fahren; «Handy» zeigt alle in Telefonbreite.</p></div>
<div class="schalter"><button type="button" aria-pressed="true" data-w="breit">Bildschirm</button><button type="button" aria-pressed="false" data-w="handy">Handy</button></div></div>
<nav class="sprung">%s</nav>
%s
<script>%s</script>
</body>
</html>
''' % (CSS, sprung, '\n'.join(fassung(n, *f) for n, f in enumerate(F)), JS)


if __name__ == '__main__':
    ziel = os.path.join(HIER, 'leiste-wahl.html')
    open(ziel, 'w').write(seite())
    print(ziel, len(F) - 1, 'Fassungen')
