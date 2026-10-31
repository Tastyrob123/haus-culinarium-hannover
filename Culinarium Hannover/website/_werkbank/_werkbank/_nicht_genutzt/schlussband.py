#!/usr/bin/env python3
"""Werkbank Landgasthof Ruedihus: Laufband zwischen dem Schluss und dem Fuss «Alles auf einen Blick» (12.10.2026, Master 5b Punkt 23).

Eigen fürs Ruedihus: über das Band laufen die Produkte aus der Karte des Hauses mit ihrer Herkunft, im Wortlaut des Lauftexts der Ruedihus-Seite
(gelesen aus der gebauten Seite, damit die Wörter nur an einer Stelle stehen). Das Band läuft nur, solange es im Bild ist; bewegt wird nur transform.
Eingehängt in haus.py: CSS am Dateiende, anwenden() in nach_bau(). Mehrfach anwendbar."""
import os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
VB = '0 0 1044 1398'

CSS = '''
/* ---------- Laufband zwischen Schluss und Fuss (schlussband.py, 12.10.2026) ---------- */
.lb{position:relative;z-index:3;overflow:hidden;background:var(--tief);color:rgba(243,205,148,.8)}
.lb::before,.lb::after{content:'';position:absolute;left:0;right:0;height:1px;z-index:1;pointer-events:none;background:linear-gradient(90deg,transparent,rgba(201,133,67,.42) 14%,rgba(201,133,67,.42) 86%,transparent)}
.lb::before{top:0}.lb::after{bottom:0}
.lb__z{display:flex;align-items:center;width:max-content;margin:0;padding:0;list-style:none;animation:lbzug 90s linear infinite;animation-play-state:paused}
.lb.laeuft .lb__z{animation-play-state:running;will-change:transform}
.lb li{flex:none;display:flex;align-items:center;height:56px;margin:0;padding:0 30px;font-family:var(--serif);font-weight:700;font-size:clamp(.92rem,1.02vw,1.06rem);line-height:1;letter-spacing:.02em;white-space:nowrap}
.lb li.lb__m{padding:0 4px;color:rgba(201,133,67,.7)}
.lb__m svg{display:block;width:auto;height:20px}
@keyframes lbzug{to{transform:translate3d(-50%,0,0)}}
@media(max-width:860px){.lb li{height:48px;padding:0 20px}.lb__m svg{height:16px}}
@media(prefers-reduced-motion:reduce){.lb__z{animation:none}}
'''

JS = ('<script id="lb-js">(function(){var b=document.querySelector(\'.lb\');'
      'if(!b||!(\'IntersectionObserver\' in window)||matchMedia(\'(prefers-reduced-motion: reduce)\').matches)return;'
      'new IntersectionObserver(function(E){b.classList.toggle(\'laeuft\',E[0].isIntersecting)},{rootMargin:\'80px 0px\'}).observe(b)})();</script>')
VORGABE = ['Kandersteger Hobelkäse aus dem Ueschinental', 'Forelle aus dem Blausee', 'Walliser Trockenfleisch', 'Spiezer Riesling', 'Greyerzer Nydle', 'Zuger Kirsch', 'Aargauer Rüebli', 'Mauler aus Môtiers']


def worte():
    """Die Produkte mit ihrer Herkunft, wie sie im Lauftext der gebauten Ruedihus-Seite stehen."""
    for seite in ('essen.html', 'index.html'):
        try:
            t = open(os.path.join(ROOT, seite), encoding='utf-8').read()
        except OSError:
            continue
        for m in re.finditer(r'<div class="laufband__zug">(.*?)</div>', t, flags=re.S):
            w = re.findall(r'<span>(.*?)</span>', m.group(1))
            if w and 'Hobelkäse' in w[0]:
                return w
    return VORGABE


def band():
    z = f'<li class="lb__m" aria-hidden="true"><svg viewBox="{VB}" fill="currentColor"><use href="#hz"/></svg></li>'
    w = worte()
    satz = lambda versteckt: ''.join(f'<li{" aria-hidden=" + chr(34) + "true" + chr(34) if versteckt else ""}><span>{x}</span></li>{z}' for x in w)
    return (f'<div class="lb" aria-label="Aus der Karte des Hauses: woher die Produkte kommen"><ul class="lb__z">{satz(False)}{satz(True)}</ul></div>\n{JS}\n')


def setz(t):
    t = re.sub(r'<div class="lb".*?</div>\n<script id="lb-js">.*?</script>\n', '', t, flags=re.S)
    i = t.find('<footer class="fuss">')
    return t if i < 0 else t[:i] + band() + t[i:]


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
