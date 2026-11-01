#!/usr/bin/env python3
"""Werkbank Culinarium: bewegt wird nur über transform und opacity (Regel 55, Roberts Kriterium 37; Abnahme-Tor 30.10.2026, Bewegungsmessung:
«Animiert auch color, background-color, background-image, box-shadow, stroke-dashoffset»).
- Übergänge in den Stilblättern der Werkbank: Einträge für Farbe, Hintergrund, Schatten, Rahmen, Strich, Füllung, Abstände und eigene Werte
  (--gp) fallen weg; der neue Zustand steht sofort, transform/opacity/visibility bleiben.
- Glanzkante («Zur Website» in der Leiste): statt eines gemalten Verlaufs, der jedes Bild neu gezeichnet wird, dreht sich ein Verlauf
  hinter dem Knopf (transform), der Knopf deckt ihn bis auf die Kante ab.
- Die Karte «Die Übergabe.» (karte.html) kommt wie die Werkbank herein: Kopf und Gänge steigen gestaffelt auf (nur am Bildschirm, nie im PDF).
Läuft in haus.nach_bau vor text_mitte, wiederholbar.   python3 _werkbank/nur_bewegung.py [<website/_werkbank>]"""
import glob, os, re, sys

ERLAUBT = ('transform', 'opacity', 'visibility', 'translate', 'scale', 'rotate', 'none')
GLANZ = ('/* nur-bewegung */.glanz{animation:none!important;border:0!important;background:none!important;transition:transform .5s var(--e2)!important}'
         '.glanz::before{content:"";position:absolute;z-index:-2;left:50%;top:50%;width:260px;height:260px;margin:-130px 0 0 -130px;'
         'background:conic-gradient(transparent,var(--gold) 6%,#ffffff 12%,var(--taupe) 18%,transparent 24%);animation:glanzdreh 4s linear infinite;will-change:transform}'
         '.glanz::after{content:"";position:absolute;z-index:-1;inset:1px;border-radius:inherit;background:linear-gradient(180deg,#423e4c,#23212a)}'
         '@keyframes glanzdreh{to{transform:rotate(1turn)}}'
         '@media (prefers-reduced-motion:reduce){.glanz::before{animation:none}}')
KARTE = ('<style id="nur-bewegung">@media screen{html.bew .mn-kopf>*,html.bew .mn-gang,html.bew .mn-l li,html.bew .sag-orn{opacity:0;transform:translateY(22px);'
         'transition:opacity .9s cubic-bezier(.16,1,.3,1),transform 1.1s cubic-bezier(.16,1,.3,1);transition-delay:calc(var(--bi,0)*70ms)}'
         'html.bew .hoch{opacity:1!important;transform:none!important}}'
         '@media (prefers-reduced-motion:reduce){html.bew .mn-kopf>*,html.bew .mn-gang,html.bew .mn-l li,html.bew .sag-orn{opacity:1;transform:none;transition:none}}</style>'
         '<script id="nur-bewegung-js">(function(){if(matchMedia("print").matches||!("IntersectionObserver" in window))return;var d=document.documentElement;d.classList.add("bew");'
         'var z=[].slice.call(document.querySelectorAll(".mn-kopf>*,.mn-gang,.mn-l li,.sag-orn")),n=0;'
         'var io=new IntersectionObserver(function(es){n=0;es.forEach(function(e){if(e.isIntersecting){e.target.style.setProperty("--bi",n++);e.target.classList.add("hoch");io.unobserve(e.target)}})},{rootMargin:"0px 0px -6% 0px"});'
         'z.forEach(function(e){io.observe(e)});addEventListener("beforeprint",function(){z.forEach(function(e){e.classList.add("hoch")})})})();</script>')


def teile(wert):
    """Kommagetrennte Einträge, Klammern (cubic-bezier, var) bleiben ganz."""
    aus, tiefe, s = [], 0, ''
    for c in wert:
        tiefe += (c == '(') - (c == ')')
        if c == ',' and tiefe == 0:
            aus.append(s); s = ''
        else:
            s += c
    return aus + [s]


def uebergang(m):
    wert, rest = m.group(2), m.group(3)
    bleibt = [t for t in teile(wert) if t.strip().split()[:1] and t.strip().split()[0] in ERLAUBT]
    return m.group(1) + (','.join(bleibt) if bleibt else 'none') + rest


def anwenden(root):
    n = 0
    for f in glob.glob(os.path.join(root, 'werkbank', '*.css')):
        if '.vor-' in f:
            continue
        s = open(f, encoding='utf-8').read()
        neu = re.sub(r'(transition:)([^;}!]+)(!important|)', lambda m: uebergang(m), s)
        if os.path.basename(f) == 'werkbank.css':
            neu = re.sub(r'/\* nur-bewegung \*/.*\Z', '', neu, flags=re.S).rstrip() + '\n' + GLANZ + '\n'
        if neu != s:
            open(f, 'w', encoding='utf-8').write(neu); n += 1
    k = os.path.join(root, 'werkbank', 'karte.html')
    if os.path.exists(k):
        s = open(k, encoding='utf-8').read()
        s = re.sub(r'<style id="nur-bewegung">.*?</style><script id="nur-bewegung-js">.*?</script>', '', s, flags=re.S)
        i = s.rfind('</body>')
        if i > 0:
            open(k, 'w', encoding='utf-8').write(s[:i] + KARTE + s[i:]); n += 1
    return n


if __name__ == '__main__':
    print('nur-bewegung:', anwenden(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Dateien')
