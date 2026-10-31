#!/usr/bin/env python3
"""Baustein in der Werkbank Culinarium (Werkbank-Chat 28.10.2026), über das Schäfli kopiert; die Herkunft steht darunter wie in der Vorlage.
Werkbank Landgasthof Ruedihus, «Geprüft» im Stil der Ruedihus-Seite (12.10.2026, Master 5b Punkt 21).

Eigen fürs Ruedihus: der Prüfbericht liegt da wie ein Schpiszettel des Hauses. Ein helles Blatt mit dem Medaillon, vier Zeilen wie vier Gänge
(Name, ein Satz, rechts statt des Preises der Haken), unten Ort, Datum und Unterschriftszeile, über der Ecke der Stempel im Rot der Geranien.
Daneben drei echte Fotos des Hauses als Kacheln mit Einkerbung wie die Zimmer auf der Website. Darunter, was offen bleibt, und der Weg zur Prüfbericht-Seite.
Eingehängt in haus.py: geprueft_abschnitt = geprueft_blatt.abschnitt(globals()) (Haken des Kits), CSS am Dateiende."""
import datetime

import haus as _H
VB = _H.ZEICHEN[0]
MONATE = 'Januar Februar März April Mai Juni Juli August September Oktober November Dezember'.split()


def abschnitt(h):
    def bau(k):
        e, bild, KP = k['e'], k['bild'], k['kap']
        TRIO, PUNKTE = h['GEPRUEFT_TRIO'], h['GEPRUEFT_PUNKTE']
        heute = h.get('PRUEFDATUM') or datetime.date.today()   # Tag der Prüfung, fest in haus.py
        datum = f'{heute.day}. {MONATE[heute.month - 1]} {heute.year}'
        stempel = ('<svg class="gb-st gb-st--eck" viewBox="0 0 260 110" aria-hidden="true"><rect x="4" y="4" width="252" height="102" rx="10" fill="none" stroke="currentColor" stroke-width="4"/>'
                   '<rect x="14" y="14" width="232" height="82" rx="5" fill="none" stroke="currentColor" stroke-width="1.4"/>'
                   '<path d="M34 56l14 14 30-32" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
                   f'<text x="98" y="52" font-family="DM Mono,monospace" font-size="17" letter-spacing="3" fill="currentColor">GEPRÜFT</text>'
                   f'<text x="98" y="76" font-family="DM Mono,monospace" font-size="11" letter-spacing="1.6" fill="currentColor">{e(datum.upper())}</text></svg>')
        haken = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7"/></svg>'
        zeichen = f'<svg viewBox="{VB}" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>'
        fotos = ''.join(f'<figure class="gb-f" data-a="auf" style="--i:{i}"><div class="gb-f__b">{bild(f"gt-{i}", n)}</div><figcaption>{e(n)}</figcaption></figure>'
                        for i, (*_, n) in enumerate(TRIO))
        punkte = ''.join(f'<li data-a="auf" style="--i:{i}">' + (f'<span class="gb-pb">{bild(f"gp-{i}", ti)}</span>' if f'gp-{i}' in k['m'] else '') + f'<div><h3>{e(ti)}</h3><p>{e(x)}</p></div><i class="gb-ok">{haken}</i></li>' for i, (ti, x) in enumerate(PUNKTE))
        return f"""
<section class="fl {h['FLAECHE'].get('geprueft', 'fl--navy tapete')} blatt gb" id="geprueft">
  <div class="in">
    <div class="kopfzeile"><div><p class="kap" data-a="auf"><b>00</b><i></i><span>{e(KP['name'])}</span></p>{k['titel'](KP['zeilen'])}</div><div class="lauf"><p data-a="worte">{KP['text']}</p></div></div>
    <div class="gb-b">
      <article class="gb-blatt" data-a="heben">
        <header><span class="gb-z">{zeichen}</span><h3>Prüfbericht</h3><p>Alles auf einen Blick · {e(h['NAME'])}</p></header>
        <ol class="gb-l">{punkte}</ol>
        <footer><span>Hamburg, {datum}</span><span>Robert Reff · Tasty Studios</span></footer>
        {stempel}
      </article>
      <div class="gb-fotos">{fotos}</div>
    </div>
    <div class="gb-fuss" data-a="auf"><p>{e(h.get('GEPRUEFT_OFFEN', ''))}</p>{k['kn']('Den ganzen Prüfbericht lesen', 'geprueft/index.html', neu=True)}</div>
  </div>
</section>"""
    return bau


CSS = '''
/* Schlössli 20.10.2026 (Robert: «in allen Tools Bilder dazu»): jeder Punkt des Prüfblatts mit seinem Bild */
.gb-l li{display:flex;align-items:center;gap:clamp(12px,1.4vw,20px)}.gb-l li>div{flex:1}
/* Schäfli 21.10.2026: am Handy lag das Bild über dem Text (390 px, Safari und Chrome): Bild links in eigener Spalte, Text und Haken rechts darunter */
@media(max-width:640px){.gb-l li{display:grid!important;grid-template-columns:64px minmax(0,1fr)!important;column-gap:14px!important;row-gap:10px;align-items:start!important}.gb-l li>.gb-pb{position:static!important;width:64px;grid-column:1;grid-row:1/span 2;margin:4px 0 0}.gb-l li>div{grid-column:2;min-width:0}.gb-l li>.gb-ok{position:static!important;grid-column:2;grid-row:2}}
.gb-pb{flex:none;display:block;width:clamp(72px,7vw,104px);aspect-ratio:4/3;border-radius:10px;overflow:hidden;box-shadow:0 10px 16px -12px rgba(4,16,35,.5)}.gb-pb img{display:block;width:100%;height:100%;object-fit:cover}
/* Schäfli (wie Schlössli): Stempel eckig (keine Siegel, Tasty-Sprache E), Bildname unter dem Foto (keine Einkerbung) */
.gb-st--eck{width:clamp(150px,13vw,200px)!important;height:auto!important;aspect-ratio:260/110}
.gb-f>figcaption{position:static!important;margin-top:10px;padding:0!important;background:none!important;border-radius:0!important;font-family:var(--mono)!important;font-weight:400!important;font-size:11px!important;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)!important}
.gb-f>figcaption::before,.gb-f>figcaption::after{display:none!important}
.gb-f{display:flex;flex-direction:column}.gb-f>.gb-f__b{flex:1}
/* ---------- Geprüft: der Prüfbericht als Blatt wie ein Schpiszettel, daneben drei Fotos mit Einkerbung (geprueft_blatt.py, 12.10.2026) ---------- */
.gb-b{display:grid;gap:clamp(20px,2.6vw,44px);align-items:stretch}
@media(min-width:1000px){.gb-b{grid-template-columns:minmax(0,1.42fr) minmax(0,.58fr)}}
.gb-blatt{position:relative;border-radius:clamp(20px,2vw,30px);padding:clamp(28px,3.6vw,60px) clamp(22px,3.6vw,60px) clamp(22px,2.6vw,40px);background:var(--weiss);color:var(--tinte);
  box-shadow:inset 0 1px 0 #fffdf7,0 0 0 1px rgba(125,79,39,.3),0 50px 70px -46px rgba(0,0,0,.95)}
.gb-blatt::before{content:'';position:absolute;inset:clamp(9px,1vw,14px);border:1px solid rgba(183,143,81,.6);border-radius:clamp(13px,1.3vw,20px);pointer-events:none}
.gb [data-a="heben"]{opacity:1;transform:translate3d(0,120px,0) scale(.974);transform-origin:50% 100%;transition:transform 2.2s cubic-bezier(.16,1,.3,1)}
.gb [data-a="heben"].da{transform:none}
.gb-blatt header{text-align:center;padding-bottom:clamp(18px,2vw,30px);border-bottom:1px solid rgba(125,79,39,.3)}
.gb-z{display:block;width:clamp(40px,3.8vw,58px);margin:0 auto clamp(10px,1.2vw,16px);color:#8a5a22}
.gb-z svg{display:block;width:100%;height:auto;fill:#b15736}
.gb-blatt header h3{margin:0;font-family:var(--serif);font-weight:700;font-size:clamp(1.9rem,3vw,3rem);line-height:1.05}
.gb-blatt header p{margin:8px 0 0;font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--taupe)}
.gb-l{list-style:none;margin:0;padding:0}
.gb-l li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:clamp(14px,2vw,34px);align-items:center;padding:clamp(16px,1.8vw,26px) 0;border-bottom:1px dotted rgba(125,79,39,.5)}
.gb-l li:has(>.gb-pb){grid-template-columns:auto minmax(0,1fr) auto}   /* Gestaltung 28.10.2026: mit Bild drei Spalten, der Haken bleibt rechts auf einer Linie statt unter dem Bild */
.gb-l:has(.gb-pb) li:not(:has(>.gb-pb))>div{padding-left:calc(clamp(72px,7vw,104px) + clamp(14px,2vw,34px))}   /* ohne Bild: Text auf derselben Linie wie die Zeilen mit Bild */
@media(max-width:640px){.gb-l:has(.gb-pb) li:not(:has(>.gb-pb))>div{padding-left:0}}
.gb-l h3{margin:0 0 6px;font-family:var(--serif);font-weight:700;font-size:clamp(1.3rem,1.7vw,1.7rem);line-height:1.14}
.gb-l p{margin:0;max-width:62ch;font-size:clamp(.98rem,1.04vw,1.06rem);line-height:1.56;color:rgba(42,26,14,.82)}
.gb-ok{flex:none;width:clamp(40px,3.4vw,52px);aspect-ratio:1;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,#5a3a20 0%,#321f10 52%,#170d06 100%);box-shadow:inset 0 1px 0 rgba(255,236,200,.3),0 12px 16px -10px rgba(42,26,14,.6)}
.gb-ok svg{width:48%;height:48%;fill:none;stroke:#f3cd94;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:26;stroke-dashoffset:26;transition:stroke-dashoffset .9s var(--e1) calc(.5s + var(--i)*160ms)}
.gb-l li.da .gb-ok svg{stroke-dashoffset:0}
.gb-blatt footer{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 20px;margin-top:clamp(16px,1.8vw,26px);padding-right:clamp(90px,10vw,150px);font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--taupe)}
.gb-st{position:absolute;right:clamp(-14px,-1vw,-6px);bottom:clamp(-18px,-1.4vw,-8px);width:clamp(104px,10.4vw,156px);height:auto;color:#a8260f;transform:rotate(-13deg);opacity:.9;pointer-events:none}
.gb-fotos{display:grid;gap:clamp(12px,1.4vw,20px)}
@media(max-width:999px){.gb-fotos{grid-template-columns:repeat(3,minmax(0,1fr))}}
.gb-f{margin:0;min-height:0}
.gb-f__b{position:relative;height:100%;min-height:clamp(120px,13vw,190px);border-radius:clamp(16px,1.6vw,24px);overflow:hidden;background:#2a180a;box-shadow:0 0 0 1px rgba(201,133,67,.3),0 30px 40px -28px rgba(0,0,0,.9)}
.gb-f__b img{position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:cover;transition:transform 2.2s cubic-bezier(.16,1,.3,1)}
@media(hover:hover){.gb-f:hover img{transform:scale(1.06);transition-duration:2.8s}}
.gb-f figcaption{position:absolute;left:0;bottom:0;padding:8px 16px 7px 14px;border-radius:0 16px 0 0;background:var(--navy);font-family:var(--serif);font-weight:700;font-size:clamp(.9rem,1vw,1.04rem);line-height:1.2;color:#fbf5ea}
.gb-f figcaption::before,.gb-f figcaption::after{content:'';position:absolute;width:16px;height:16px;background:radial-gradient(circle at 100% 0,transparent 15.5px,var(--navy) 16px)}
.gb-f figcaption::before{left:0;top:-16px}.gb-f figcaption::after{right:-16px;bottom:0}
.gb-fuss{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:18px clamp(24px,3vw,48px);margin-top:clamp(34px,4vw,60px);text-align:center}
.gb-fuss p{margin:0;max-width:64ch;font-size:clamp(1rem,1.06vw,1.08rem);line-height:1.6;color:rgba(251,245,234,.84)}
@media(max-width:640px){.gb-fotos{grid-template-columns:1fr 1fr}.gb-f:last-child{grid-column:1/-1}.gb-f__b{min-height:150px}.gb-blatt footer{padding-right:0;padding-bottom:70px}}
@media (prefers-reduced-motion:reduce){.gb [data-a="heben"]{transform:none;transition:none}.gb-ok svg{stroke-dashoffset:0;transition:none}.gb-f__b img{transition:none;transform:none!important}}
'''
