#!/usr/bin/env python3
"""Baustein in der Werkbank Culinarium (Werkbank-Chat 28.10.2026), über das Schäfli kopiert; die Herkunft steht darunter wie in der Vorlage.
Werkbank Landgasthof Ruedihus, Abschnittsköpfe (12.10.2026, Stand der Werkbank des Grand Beau-Rivage, Master 5b):
Zahl und Strich fallen weg, über jeder Überschrift steht das Medaillon des Hauses in Gold, Überschrift und Einleitung mittig, darunter Luft.

Das Kit setzt  <p class="kap"><b>02</b><i></i><span>Mitgebracht</span></p>.  setz() macht daraus
<p class="kap kap--z"><svg class="kap__z"><use href="#hz"/></svg><span>Mitgebracht</span></p>  (#hz liegt oben in der Seite)
und legt einmal den Goldverlauf #rhgold (auf Holz) und #rhgold-t (auf Papier, eine Stufe tiefer) in die Seite.
Eigen fürs Ruedihus: das Medaillon ist hochkant, das Wort darunter steht in der Titelschrift des Hauses (keine gesperrten Versalien),
die Überschrift in Gelasio fett bleibt kleiner als beim Grand Beau-Rivage, weil die Schrift breiter läuft.
Eingehängt in haus.py: CSS am Dateiende, anwenden() in nach_bau()."""
import os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
import haus as _H
VB = _H.ZEICHEN[0]   # assets/logo/zeichen.svg

CSS = '''
/* ---------- Abschnittsköpfe mittig, Medaillon des Hauses in Gold darüber, ohne Zahl (kopf_mitte.py, 12.10.2026) ---------- */
.kap--z{flex-direction:column;justify-content:center;gap:clamp(14px,1.4vw,22px);text-align:center;margin-bottom:clamp(16px,1.8vw,28px)}
.kap__z{display:block;width:clamp(50px,5.9vw,92px);height:auto;flex:none;color:#ef7649;fill:currentColor}
.fl--papier .kap__z,.fl--creme .kap__z,.fl--weiss .kap__z{color:#b15736;fill:currentColor}
.kap--z span{font-family:var(--serif);font-weight:700;font-size:clamp(1rem,1.1vw,1.14rem);letter-spacing:.01em}
.kap.kap--z~.zt.zt{font-size:clamp(2.1rem,5.5vw,5.9rem);line-height:1.04}
.kopfzeile{display:block;text-align:center;margin-bottom:clamp(54px,6.4vw,104px)}
.kopfzeile .zt .z>span,.kap--z~.zt .z>span{margin-inline:auto}
.kap--z~.zt{text-align:center}
.kopfzeile .lauf{max-width:60ch;margin:clamp(18px,2.1vw,32px) auto 0;padding-bottom:0}
.fl>.in>.kopfzeile:first-child{padding-top:clamp(8px,1.4vw,24px)}
/* Abschnitte mit Text- und Bildspalte (Unterlagen): der Kopf steht mittig über beiden Spalten */
@media(min-width:1000px){
  .karten{row-gap:0;align-items:start}
  .karten>div:first-child{display:contents}
  .karten>div:first-child>.kap,.karten>div:first-child>.zt{grid-column:1/-1}
  .karten>div:first-child>.zt{margin-bottom:clamp(54px,6.4vw,104px)}
  .karten>div:first-child>.lauf{margin-top:0!important;align-self:end;grid-column:1;grid-row:3}
  .karten>div:first-child>.kn-reihe{align-self:start;grid-column:1;grid-row:4}
  .karten>div:nth-child(2){grid-column:2;grid-row:3/span 2;align-self:center}
}
@media(max-width:999px){.karten>div:first-child{text-align:center}.karten>div:first-child>.lauf{margin-inline:auto}.karten>div:first-child>.kn-reihe{justify-content:center}}
/* Material und Schluss: alles mittig unter der Überschrift */
.schluss .in{text-align:center}
.schluss .lauf{margin-inline:auto}
.schluss .gruss-u,.schluss .kn-reihe{justify-content:center}
'''

GOLD = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" id="rhgold-def"><defs>'
        '<linearGradient id="rhgold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d49a"/><stop offset=".3" stop-color="#dcae66"/>'
        '<stop offset=".52" stop-color="#b78f51"/><stop offset=".66" stop-color="#946a31"/><stop offset=".84" stop-color="#c98f4b"/><stop offset="1" stop-color="#e6c084"/></linearGradient>'
        '<linearGradient id="rhgold-t" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b98443"/><stop offset=".34" stop-color="#9a672b"/>'
        '<stop offset=".56" stop-color="#7d4f27"/><stop offset=".7" stop-color="#6a401c"/><stop offset=".86" stop-color="#93622c"/><stop offset="1" stop-color="#a9763a"/></linearGradient>'
        '</defs></svg>')
KAP = re.compile(r'<p class="kap"([^>]*)><b>[^<]*</b><i></i><span>')
ZEICHEN = f'<svg class="kap__z" viewBox="{VB}" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>'


def setz(t):
    """Zahl und Strich aus jeder Kapitelzeile, das Medaillon davor. Mehrfach anwendbar."""
    if 'id="hz"' not in t:
        return t
    t = KAP.sub(lambda m: f'<p class="kap kap--z"{m.group(1)}>{ZEICHEN}<span>', t)
    if 'id="rhgold-def"' not in t:
        t = t.replace('<div class="gang-linie"', GOLD + '\n<div class="gang-linie"', 1)
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
