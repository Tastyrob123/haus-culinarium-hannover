#!/usr/bin/env python3
"""Werkbank Culinarium (Vorlage Schäfli, dort Schlössli und Ruedihus), Kapitel «Ihre Werkzeuge»: «Einmal ändern, überall richtig.» als Bühne mit echten Aufnahmen (Werkbank-Chat 17.10.2026;
Aufbau, Bewegung und Skript aus dh_strom.py des Waldhotel Doldenhorn, dort aus strom_buehne.py des Carlton-Europe, nur gelesen und kopiert). Links die
Aufnahme des Werkzeugs mit Siegel, rechts je Ziel eine Bildkachel, goldene Wege dazwischen, ein Licht fliegt darüber. Inhalt nur aus echten Aufnahmen:
den Lieferungen der Werkzeug-Chats, den Seitenaufnahmen der Werkbank
(ansichten/Rechner, Handy, Chat) und ansichten/Strom (rh_aufnahmen.js). Eine Szene erscheint erst, wenn alle ihre Bilder da sind."""
import html, json, os
from PIL import Image

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
HAUS = 'Culinarium'
WZB = lambda r: os.path.join(W, 'ansichten', 'Werkzeuge', r)   # Aufnahmen der gelieferten Werkzeuge (sb_werkzeuge.js)
AN = lambda r: os.path.join(W, 'ansichten', r)
UN = lambda r: os.path.join(ROOT, 'unterlagen', 'img', r)
DR = lambda r: os.path.join(ROOT, 'drucksachen', 'img', r)

# Werkzeug, Rolle, Aufnahme (Datei, Ausschnitt oder None), Stücke [(Bild, Ausschnitt, Titel, Satz)]. Nur echte Aufnahmen; eine Szene erscheint erst, wenn alle Bilder da sind.
import rh_werkzeuge as _WK
_N = _WK.NAMEN
SZENEN = [
    (_N['bureau'], 'Website', (WZB('bureau.jpg'), None), [
        (WZB('bureau-2.jpg'), None, 'Einen Abend eintragen',
         'Tag, Beginn, Preis und Plätze an einer Stelle; jeder Abend bekommt sein Plakat. Ebenso ein neuer Satz oder ein Foto.'),
        (AN('Gaeste/buchen.jpg'), None, 'Auf der Website',
         'Auf «Der Abend» stehen die nächsten Abende mit ihrem Plakat. Bis zum Veröffentlichen sieht nur ihr die Änderung.'),
        (AN('Gaeste/buchen-h.jpg'), None, 'Am Handy',
         'Das Handy zeigt danach dieselben Abende, ohne dass jemand sie ein zweites Mal schreibt.')]),
    (_N['carte'], 'Karten', (WZB('carte.jpg'), None), [
        (WZB('carte-2.jpg'), None, 'Teller und Drink je Gang',
         'Links die Liste, rechts sofort die Karte am Platz, so wie sie gedruckt wird.'),
        (UN('n-abend-2025-02-21-01.webp'), None, 'Auf dem Tisch',
         'Daraus wird das Blatt am Platz, als PDF in A4 für die Druckerei oder den eigenen Drucker.')]),
    (_N['livre'], 'Marke', (WZB('livre.jpg'), None), [
        (WZB('livre-2.jpg'), None, 'Die Fotos der Abende',
         'Jedes Foto von Tafel, Bar, Tellern und Drinks groß ansehen und in der passenden Größe laden.'),
        (AN('Rechner/Alle Abende 2.jpg'), None, 'Die Plakate',
         'Dieselben Farben und Plakate kennt auch das Werkzeug für Drucksachen, darum sieht jedes Blatt nach Culinarium aus.')]),
    (_N['imprimerie'], 'Plakate und Papier', (WZB('imprimerie.jpg'), None), [
        (os.path.join(ROOT, 'assets', 'bild', 'ill_DbYnkdkjrNy-1300.webp'), None, 'Den Abend beschreiben',   # Bild bis zu neuen Plakaten im gemalten Stil: Rudis Illustration und Plakat (September 2026)
         'Thema, Konzept, Gastkoch und Wochenende genügen; die Werkstatt malt dafür drei bis fünf neue Plakate im Stil eurer bisherigen, vorn und hinten.'),
        (os.path.join(ROOT, 'assets', 'bild', 'p_DbYnkdkjrNy-1600.webp'), None, 'Das Plakat des Abends',
         'Ihr wählt eins und setzt im Editor Texte, Datum und Farbe, vorn und hinten, druckfertig.')]),
    (_N['reception'], 'Gäste', (WZB('reception.jpg'), None), [
        (WZB('reception-2.jpg'), None, 'Jede Anfrage nach ihrer Art',
         'Warteliste, Plätze am Abend, eine eigene Feier und Nachrichten kommen hier an, jede mit einem Brief als Entwurf.'),
        (AN('Gaeste/warteliste.jpg'), None, 'Woher sie kommen',
         'Etwa vom Ticket auf der Seite «Der Abend», auf dem sich ein Gast für den nächsten Termin einträgt.')]),
    (_N['registre'], 'Besuche', (WZB('registre.jpg'), None), [
        (WZB('registre-2.jpg'), None, 'Woher und wohin',
         'Woher die Gäste kommen und welche Seiten sie ansehen, ohne Cookies gezählt. Im Entwurf sind die Zahlen erfunden.'),
        (AN('Rechner/Startseite 4.jpg'), None, 'Was gefragt ist',
         'Welche Stelle am häufigsten offen ist, zeigt, wonach eure Gäste suchen.')]),
]
FEDER = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.1-4.4L15.9 4.8a1.9 1.9 0 0 1 2.7 0l.6.6a1.9 1.9 0 0 1 0 2.7L8.4 18.9z"/><path d="M14.2 6.5l3.3 3.3"/><path d="M12.5 20H20"/></svg>'
HAKEN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5.5 12.6l4.1 4.1L18.5 7.6"/></svg>'
_ZVB = __import__('re').search(r'viewBox="([^"]+)"', open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', '..', '_werkzeuge', 'oberflaeche', 'kleid', 'culinarium-zeichen.svg'), encoding='utf-8').read()).group(1)   # viewBox des «C» (29.10.)
ZEICHEN = f'<svg class="fbs__zeichen" viewBox="{_ZVB}" aria-hidden="true"><use href="#hz"/></svg>'


def _schnitt(q, box, f):
    im = Image.open(q).convert('RGB')
    w, h = im.size
    if box:
        im = im.crop((round(box[0] * w), round(box[1] * h), round(box[2] * w), round(box[3] * h)))
        w, h = im.size
    if w / h > f:
        nw = round(h * f); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        im = im.crop((0, 0, w, round(w / f)))
    return im


def szenen():
    return [s for s in SZENEN if os.path.exists(s[2][0]) and all(os.path.exists(x[0]) for x in s[3])]


def bilder(webp):
    m = {}
    for i, (name, rolle, (q, box), st) in enumerate(szenen()):
        m[f'fb-{i}'] = webp(_schnitt(q, box, 16 / 10), f'fb-{i}', 1200, 82)
        for j, (b, bx, *_t) in enumerate(st):
            m[f'fb-{i}-{j}'] = webp(_schnitt(b, bx, 4 / 3), f'fb-{i}-{j}', 640, 80)
    return m


def _img(m, n):
    w, h = m[n]
    return f'<img src="img/{n}.webp" width="{w}" height="{h}" alt="" loading="lazy" decoding="async">'


def html_(k, saetze):
    m, S = k['m'], szenen()
    if not S:
        return ''
    pf = '<button type="button" aria-label="Vorige"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg></button><button type="button" aria-label="Nächste"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg></button>'
    wahl = '<div class="fb__reiter">' + ''.join(f'<button type="button" class="fb__w" aria-pressed="false"><small>{e(r)}</small><span>{e(n)}</span></button>' for n, r, _q, _s in S) + f'</div><div class="fb__pf">{pf}</div>'
    szenen_html = ''
    for i, (name, rolle, _q, st) in enumerate(S):
        li = ''.join(f'<li class="fbz" style="--k:{j}"><div class="fbz__b"><figure class="fbk">{_img(m, f"fb-{i}-{j}")}<i class="fbk__glanz"></i></figure>'
                     f'<i class="fbz__hof"></i><span class="fbz__ok">{HAKEN}</span></div><div class="fbz__t"><b class="fbz__n">{e(t)}</b><p class="fbz__s">{e(s)}</p></div></li>'
                     for j, (_b, _bx, t, s) in enumerate(st))
        was = saetze.get(name, '')
        szenen_html += (f'<li class="fbs fbs--{len(st)}" style="--n:{len(st)}"><div class="fbs__q"><div class="fbs__b"><figure class="fbk fbk--q">{_img(m, f"fb-{i}")}</figure>'
                        f'<span class="fbs__siegel" aria-hidden="true">{FEDER}<i></i></span></div>'
                        f'<div class="fbs__t"><div class="fbs__k">{ZEICHEN}<div><b>{e(name)}</b><small>{HAUS}</small></div></div>'
                        + (f'<span>{e(was)}</span>' if was else '') + f'</div></div><ol class="fbs__z">{li}</ol></li>')
    funken = '<li class="fb__funke" aria-hidden="true"></li>' * max(len(s[3]) for s in S)
    return (f'<div class="wz-strom fb"><h3 class="wz-strom__t" data-a="auf">Einmal ändern, <em>überall richtig.</em></h3><div class="fb__wahl">{wahl}</div>'
            f'<ul class="fb__raum"><li class="fb__netzli" aria-hidden="true" style="display:contents"><svg class="fb__netz"></svg></li>{funken}{szenen_html}</ul></div>{JS}')


CSS = '''
/* ---------- Einmal ändern, überall richtig: Fluss, Fassung 2: Bühne mit Bildkacheln, Bögen und Licht (strom_fluss.py, 12.10.2026) ---------- */
.fb{--fg:#dcc68f;--fd:cubic-bezier(.28,1.42,.42,1);--sm:clamp(54px,4.7vw,70px);--rad:clamp(14px,1.5vw,22px)}
.fb .wz-strom__t{margin-bottom:clamp(20px,2.2vw,32px);font-size:clamp(1.9rem,3.1vw,3.2rem);text-wrap:balance}
.fb__wahl{display:none}
.fb>.fb__raum{position:relative;max-width:1280px;margin:0 auto;padding:0;list-style:none;display:grid;gap:0}
.fb__netz,.fb__funke{display:none}
.fbs{position:relative;display:grid;grid-template-columns:minmax(0,43fr) minmax(0,11fr) minmax(0,46fr);align-items:center;padding:clamp(30px,3.4vw,52px) 0}
.fbs+.fbs{border-top:1px solid rgba(220,198,143,.22)}
.fbs__q{grid-column:1;min-width:0}
.fbs__b{position:relative;transform:perspective(1500px) rotateY(5deg);transform-origin:0 50%}
[dir=rtl] .fbs__b{transform:perspective(1500px) rotateY(-5deg);transform-origin:100% 50%}
.fbk{position:relative;margin:0;aspect-ratio:4/3;overflow:hidden;border-radius:var(--rad);background:#141826;box-shadow:0 36px 46px -28px rgba(0,0,0,.92),0 0 0 1px rgba(220,198,143,.16)}
.fbk--q{aspect-ratio:16/10}
.fbk img{display:block;width:100%;height:100%;object-fit:cover}
.fbk::after{content:'';position:absolute;inset:0;border-radius:inherit;pointer-events:none;box-shadow:inset 0 1px 0 rgba(255,255,255,.26),inset 0 0 0 1px rgba(230,210,162,.2)}
.fbk__glanz{position:absolute;top:-20%;bottom:-20%;left:0;width:38%;pointer-events:none;background:linear-gradient(100deg,transparent,rgba(255,250,235,.55) 48%,transparent);transform:translateX(-150%) skewX(-12deg)}
.fbs__siegel{position:absolute;z-index:2;inset-inline-end:calc(var(--sm)/-2);top:50%;width:var(--sm);height:var(--sm);margin-top:calc(var(--sm)/-2);border-radius:50%;display:grid;place-items:center;
  background:linear-gradient(180deg,#fdf6e6 0%,#e4d1a8 100%);box-shadow:inset 0 1px 0 rgba(255,255,255,.95),inset 0 -1px 0 rgba(110,88,44,.42),0 0 0 1px rgba(226,206,156,.95),0 20px 26px -12px rgba(0,0,0,.9)}
.fbs__siegel svg{width:42%;height:42%;fill:none;stroke:var(--tinte);stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.fbs__siegel::after{content:'';position:absolute;inset:-8px;border-radius:50%;border:1px solid rgba(220,198,143,.45);pointer-events:none}
.fbs__siegel i{position:absolute;inset:-1px;border-radius:50%;border:1px solid var(--fg);opacity:0;pointer-events:none}
.fbs__t{display:flex;flex-direction:column;margin-top:clamp(20px,2.2vw,32px)}
.fbs__k{display:flex;align-items:center;gap:clamp(14px,1.5vw,22px)}
.fbs__zeichen{flex:none;width:clamp(52px,4.8vw,70px);height:auto;fill:currentColor;color:#ef7649}
.fbs__t b{display:block;font:400 clamp(1.2rem,1.9vw,1.8rem)/1.1 var(--serif);letter-spacing:.2em;text-transform:uppercase;
  background:linear-gradient(180deg,#fbf0cf 0%,#ead39c 34%,#c9a764 52%,#9c7b43 62%,#dcc189 80%,#f3e3b6 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 1px 0 rgba(0,0,0,.6))}
.fbs__k small{display:block;margin-top:8px;font-family:var(--mono);font-size:clamp(.66rem,.82vw,.8rem);letter-spacing:.3em;text-transform:uppercase;color:rgba(251,246,234,.72)}
.fbs__t span{margin-top:clamp(14px,1.5vw,20px);max-width:34em;font-size:clamp(1rem,1.12vw,1.1rem);line-height:1.5;color:rgba(251,246,234,.86);text-wrap:pretty}
.fbs__z{grid-column:3;list-style:none;margin:0;padding:0;display:grid;gap:clamp(16px,1.9vw,28px);min-width:0}
.fbz{--kb:41%;display:grid;grid-template-columns:minmax(0,var(--kb)) minmax(0,1fr);align-items:center;gap:clamp(16px,1.8vw,28px)}
/* Robert 12.10.2026 ~18:43 «geordneter und gerader, mit den Linien»: die drei Kacheln stehen in einer Flucht (kein Versatz der mittleren), die Wege sind ein Stamm mit rechtwinkligen, gerundeten Abzweigen statt freier Bögen */
.fbz__b{position:relative;transform:perspective(1200px) rotateY(-6deg);transform-origin:100% 50%}
[dir=rtl] .fbz__b{transform:perspective(1200px) rotateY(6deg);transform-origin:0 50%}
.fbz__b::before{content:'';position:absolute;inset-inline-start:-17px;top:calc(50% - 4px);width:7px;height:7px;border-top:1.2px solid var(--fg);border-inline-end:1.2px solid var(--fg);transform:rotate(45deg)}
[dir=rtl] .fbz__b::before{transform:rotate(-45deg)}
.fbz__hof{position:absolute;inset:-2px;border-radius:calc(var(--rad) + 2px);pointer-events:none;box-shadow:0 0 0 1.5px rgba(226,206,156,.95),0 0 36px 2px rgba(220,198,143,.3)}
.fbz__ok{position:absolute;z-index:2;inset-inline-end:-10px;top:-10px;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;
  background:linear-gradient(180deg,#fdf6e6 0%,#e4d1a8 100%);box-shadow:inset 0 1px 0 rgba(255,255,255,.95),0 0 0 1px rgba(226,206,156,.95),0 8px 12px -5px rgba(0,0,0,.85)}
.fbz__ok svg{width:58%;height:58%;fill:none;stroke:var(--tinte);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
.fbz__t{min-width:0}
.fbz__n{display:block;font-family:var(--serif);font-size:clamp(1.22rem,1.6vw,1.6rem);line-height:1.15;color:#fbf6ea;text-wrap:balance}
.fbz__s{margin:8px 0 0;font-size:clamp(.9rem,.98vw,.99rem);line-height:1.5;color:rgba(251,246,234,.8);text-wrap:pretty}

/* --- Bühne (nur mit Skript: .fb-lebt): eine Szene zur Zeit --- */
.fb.fb-lebt .fb__wahl{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:14px clamp(18px,2.4vw,34px);margin:clamp(8px,1vw,14px) auto clamp(40px,4.4vw,68px)}
.fb__reiter{display:flex;flex-wrap:wrap;justify-content:center;gap:12px}
/* Knöpfe wie die Instrumenten-Leiste darüber (.ins-r, .ins-pf), eigene Namen, weil deren Skript sonst zugreift */
.fb__w{position:relative;flex:none;display:flex;flex-direction:column;align-items:center;gap:3px;padding:12px 24px 13px;border:0;border-radius:999px;cursor:pointer;
  color:#fbf6ea;background:linear-gradient(180deg,#1b3561 0%,#0a1c3b 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14),inset 0 -1px 0 rgba(0,0,0,.4),0 0 0 1px rgba(220,198,143,.32),0 14px 24px -14px rgba(0,0,0,.85);
  transition:transform .4s cubic-bezier(.22,.61,.36,1),box-shadow .4s,background .5s,color .4s}
.fb__w small{font-family:var(--mono);font-size:.58rem;letter-spacing:.26em;text-transform:uppercase;color:rgba(220,198,143,.85);transition:color .4s}
.fb__w span{font-family:var(--serif);font-size:clamp(1.02rem,1.2vw,1.2rem);line-height:1.1;white-space:nowrap}
.fb__w:hover{transform:translateY(-2px);box-shadow:inset 0 1px 0 rgba(255,255,255,.18),inset 0 -1px 0 rgba(0,0,0,.4),0 0 0 1px rgba(220,198,143,.6),0 18px 28px -14px rgba(0,0,0,.9)}
.fb__w[aria-pressed="true"]{color:var(--tinte);background:linear-gradient(180deg,#fbf3e2 0%,#e6d4ad 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.9),inset 0 -1px 0 rgba(110,88,44,.35),0 0 0 1px rgba(220,198,143,.9),0 16px 30px -14px rgba(0,0,0,.9)}
.fb__w[aria-pressed="true"] small{color:#8a6f35}
.fb__pf{flex:none;display:flex;gap:10px}
.fb__pf button{width:48px;height:48px;border-radius:50%;border:0;cursor:pointer;display:grid;place-items:center;color:var(--tinte);background:radial-gradient(circle at 35% 30%,#fbf3e2,#cfbd98);box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 10px 18px -8px rgba(0,0,0,.6);transition:transform .3s var(--e1)}
.fb__pf button:hover{transform:translateY(-2px)}
.fb__pf svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.6}
[dir=rtl] .fb__pf svg{transform:scaleX(-1)}
.fb.fb-lebt .fbs{grid-area:1/1;z-index:1;padding:0;border:0;opacity:0;visibility:hidden;transition:opacity .45s ease,visibility 0s .45s}
.fb.fb-lebt .fbs.fb-an{opacity:1;visibility:visible;transition:opacity .6s ease .12s,visibility 0s}
.fb.fb-lebt .fbs.fb-an .fbs__q{animation:fbauf 1.15s var(--e1) .1s both}
.fb.fb-lebt .fbs.fb-an .fbz{animation:fbauf 1.15s var(--e1) calc(.22s + var(--k,0)*.13s) both}
.fb.fb-lebt .fbs.fb-los .fbs__siegel{animation:fbdruck .85s var(--e1) 1}
.fb.fb-lebt .fbs.fb-los .fbs__siegel i{animation:fbring 1s var(--e1) .12s 1 both}
.fb.fb-lebt .fbk img{transition:opacity .85s ease}
.fb.fb-lebt .fbz__hof{transition:opacity .85s ease}
.fb.fb-lebt .fbz__ok{transition:opacity .35s ease .18s,transform .85s var(--fd) .18s}
.fb.fb-lebt .fbz__t{transition:opacity .7s ease}
.fb.fb-lebt .fbz:not(.fb-hell) .fbk img{opacity:.3}
.fb.fb-lebt .fbz:not(.fb-hell) .fbz__hof{opacity:0}
.fb.fb-lebt .fbz:not(.fb-hell) .fbz__ok{opacity:0;transform:scale(.3)}
.fb.fb-lebt .fbz:not(.fb-hell) .fbz__t{opacity:.5}
.fb.fb-lebt .fbz.fb-hell .fbk__glanz{animation:fbglanz 1.15s var(--e1) .05s 1 both}
.fb.fb-lebt .fb__netz{display:block;position:absolute;z-index:0;left:0;top:0;width:100%;height:100%;overflow:visible;pointer-events:none;opacity:0;transition:opacity .3s ease}
.fb.fb-lebt .fb__netz.fb-da{opacity:1;transition:opacity 1s ease}
.fb__weg{fill:none;stroke:rgba(220,198,143,.66);stroke-width:1.2;stroke-linejoin:round;stroke-linecap:round}
.fb__bahn{fill:none;stroke:none}
.fb__weg2{fill:none;stroke:rgba(220,198,143,.09);stroke-width:8;stroke-linecap:round;stroke-linejoin:round}
.fb.fb-lebt .fb__funke{display:block;position:absolute;z-index:0;left:-14px;top:-14px;width:28px;height:28px;border-radius:50%;opacity:0;pointer-events:none;
  background:radial-gradient(circle closest-side,#fff 0,#fff 20%,rgba(255,240,200,.95) 36%,rgba(226,206,156,.45) 62%,rgba(220,198,143,0) 100%)}
@keyframes fbauf{from{opacity:0;transform:translateY(38px)}to{opacity:1;transform:none}}
@keyframes fbdruck{0%{transform:scale(1)}32%{transform:scale(.88)}100%{transform:scale(1)}}
@keyframes fbring{0%{transform:scale(1);opacity:.85}100%{transform:scale(1.9);opacity:0}}
@keyframes fbglanz{from{transform:translateX(-150%) skewX(-12deg)}to{transform:translateX(340%) skewX(-12deg)}}

/* --- schmal: Aufnahme oben, Ziele darunter als Zeilen (Bild links, Text rechts), der Weg läuft am Rand hinunter --- */
@media(max-width:860px){
  .fb{--sm:54px}
  .fb__reiter{gap:9px}
  .fb__w{padding:10px 17px 11px}
  .fb__w span{font-size:1rem}
  .fb__pf button{width:44px;height:44px}
}
/* Reiter gleichmässig: brechen sie um, dann drei und drei, nie vier und zwei (Robert 20.10.2026, Kacheln gleich verteilt) */
@media(min-width:561px) and (max-width:1380px){.fb__reiter{display:grid;grid-template-columns:repeat(3,auto);justify-content:center}}
@media(max-width:560px){
  .fb__reiter{display:grid;grid-template-columns:1fr 1fr;width:100%;max-width:372px;gap:8px}
  .fb__w{padding:9px 10px 10px}
  .fb__w small{font-size:.5rem;letter-spacing:.2em}
  .fb__pf{display:none}   /* vier Knöpfe in zwei Reihen genügen, die Pfeile kosten am Handy eine Zeile */
}
@media(max-width:860px){
  .fbs{grid-template-columns:minmax(0,1fr);padding:34px 0}
  .fbs__q{display:flex;flex-direction:column}
  .fbs__t{order:-1;margin:0 0 20px;text-align:center;align-items:center}
  .fbs__k{text-align:start}
  .fbs__b,[dir=rtl] .fbs__b,.fbz__b,[dir=rtl] .fbz__b{transform:none}
  .fbs__siegel{inset-inline-end:auto;inset-inline-start:2px;top:auto;bottom:calc(var(--sm)/-2);margin:0}   /* unten am Rand: von hier läuft der Weg am Rand hinunter und zweigt zu jeder Kachel ab */
  .fbs__z{grid-column:1;margin-top:calc(var(--sm)/2 + 28px);padding-inline-start:66px;grid-template-columns:minmax(0,1fr);gap:20px}
  .fbz{grid-template-columns:minmax(0,38%) minmax(0,1fr);gap:16px;align-items:start;text-align:start}
  .fbz:nth-child(even){margin-inline-start:0}
  .fbz__n{font-size:1.1rem}
  .fbz__s{font-size:.87rem;line-height:1.45;margin-top:5px}
  .fbs__t span{max-width:none}
  .fbz__ok{width:24px;height:24px;inset-inline-end:-7px;top:-7px}
}
'''

JS = '''<script id="fluss-auftritt">
/* Einmal ändern, überall richtig: Bühne mit vier Szenen, gewählt über Knöpfe und Pfeile. Bögen vom Siegel zu jeder Kachel, darüber fliegt je ein Lichtpunkt (nur transform und opacity). */
(function(){
  var f=document.querySelector('.fb');
  if(!f||!f.animate||!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var raum=f.querySelector('.fb__raum'),S=[].slice.call(f.querySelectorAll('.fbs')),W=[].slice.call(f.querySelectorAll('.fb__w')),netz=f.querySelector('.fb__netz'),F=[].slice.call(f.querySelectorAll('.fb__funke'));
  var akt=-1,sicht=false,T=[],D=[],R=22,zt=0,rt=0,PAUSE=3600;
  f.classList.add('fb-lebt');
  function spaeter(fn,ms){T.push(setTimeout(fn,ms))}
  function ruhe(){clearTimeout(rt);F.forEach(function(x){x.getAnimations().forEach(function(a){a.cancel()})})}
  function stopp(){T.forEach(clearTimeout);T=[];ruhe()}
  function ort(el){var x=0,y=0,e=el;while(e&&e!==raum){x+=e.offsetLeft;y+=e.offsetTop;e=e.offsetParent}return{x:x,y:y,w:el.offsetWidth,h:el.offsetHeight}}
  function z(v){return v.toFixed(1)}
  /* Gerade Wege: vom Siegel waagrecht zum Stamm (tx), am Stamm senkrecht, dann waagrecht zur Kachel; die Ecken gerundet */
  function eck(sx,sy,tx,ex,ey){var dx=ex>sx?1:-1,dy=ey>sy?1:-1,r=Math.min(18,Math.abs(ey-sy)/2,Math.abs(tx-sx)-2,Math.abs(ex-tx)-2);
    if(Math.abs(ey-sy)<1.5||r<1)return 'M'+z(sx)+' '+z(sy)+'L'+z(ex)+' '+z(ey);
    return 'M'+z(sx)+' '+z(sy)+'H'+z(tx-dx*r)+'Q'+z(tx)+' '+z(sy)+' '+z(tx)+' '+z(sy+dy*r)+'V'+z(ey-dy*r)+'Q'+z(tx)+' '+z(ey)+' '+z(tx+dx*r)+' '+z(ey)+'H'+z(ex)}
  function ab(sx,sy,ex,ey){var dx=ex>sx?1:-1,r=Math.max(0,Math.min(16,(ey-sy)/2,Math.abs(ex-sx)-2));   /* schmal: am Rand hinunter, dann im rechten Winkel zur Kachel */
    return 'M'+z(sx)+' '+z(sy)+'V'+z(ey-r)+'Q'+z(sx)+' '+z(ey)+' '+z(sx+dx*r)+' '+z(ey)+'H'+z(ex)}
  function wege(s){var q=ort(s.querySelector('.fbs__siegel')),g=ort(s.querySelector('.fbk--q')),sx=q.x+q.w/2,sy=q.y+q.h/2;
    return [].map.call(s.querySelectorAll('.fbz'),function(li){var k=ort(li.querySelector('.fbk')),ex,ey=k.y+k.h/2,c;
      if(k.x>=g.x+g.w-1){ex=k.x-R;return eck(sx,sy,sx+(ex-sx)*.6,ex,ey)}       /* Ziel rechts neben der Aufnahme */
      if(k.x+k.w<=g.x+1){ex=k.x+k.w+R;return eck(sx,sy,sx+(ex-sx)*.6,ex,ey)}   /* Ziel links (arabisch) */
      if(k.x-R>sx+6)return ab(sx,sy,k.x-R,ey);                                 /* schmal: Ziel liegt darunter */
      if(k.x+k.w+R<sx-6)return ab(sx,sy,k.x+k.w+R,ey);
      ex=k.x+k.w/2;ey=k.y-R;c=(ey-sy)*.55;return 'M'+z(sx)+' '+z(sy)+'C'+z(sx)+' '+z(sy+c)+' '+z(ex)+' '+z(ey-c)+' '+z(ex)+' '+z(ey)})}
  var B=[];
  function zeichne(){netz.setAttribute('viewBox','0 0 '+raum.offsetWidth+' '+raum.offsetHeight);var alle=D.join('');   /* ein Pfad für alle Wege: der gemeinsame Stamm wird nur einmal gemalt */
    netz.innerHTML='<path class="fb__weg2" d="'+alle+'"/><path class="fb__weg" d="'+alle+'"/>'+D.map(function(d){return '<path class="fb__bahn" d="'+d+'"/>'}).join('');
    B=[].slice.call(netz.querySelectorAll('.fb__bahn'))}
  function flug(el,k,ms){var b=B[k],K=[],n=40,i,t,c,len;if(!b)return;len=b.getTotalLength();   /* Stützpunkte auf dem Weg: der Punkt bleibt genau auf seiner Linie */
    for(i=0;i<=n;i++){t=i/n;c=b.getPointAtLength(len*t);
      K.push({offset:t,opacity:i===0||i===n?0:(i===1||i===n-1?.85:1),transform:'translate('+c.x.toFixed(1)+'px,'+c.y.toFixed(1)+'px) scale('+(i===0?.5:i===n?1.5:1)+')'})}
    return el.animate(K,{duration:ms,easing:'cubic-bezier(.55,0,.2,1)',fill:'both'})}
  function runde(){clearTimeout(rt);if(akt<0||!sicht||document.hidden||!D.length)return;   /* nach dem ersten Lauf fliegen die Punkte ruhig weiter, einer nach dem anderen */
    D.forEach(function(p,k){spaeter(function(){if(F[k])flug(F[k],k,1250)},k*520)});
    rt=setTimeout(runde,PAUSE+D.length*520)}
  function zeig(n){stopp();n=(n+S.length)%S.length;akt=n;var s=S[n],L=[].slice.call(s.querySelectorAll('.fbz'));
    S.forEach(function(x,i){x.classList.remove('fb-los');x.classList.toggle('fb-an',i===n);[].forEach.call(x.querySelectorAll('.fbz'),function(l){l.classList.remove('fb-hell')})});
    W.forEach(function(w,i){w.setAttribute('aria-pressed',i===n?'true':'false')});
    netz.classList.remove('fb-da');D=[];
    spaeter(function(){D=wege(s);zeichne();netz.classList.add('fb-da')},420);
    spaeter(function(){s.classList.add('fb-los');
      L.forEach(function(li,k){spaeter(function(){if(F[k]&&D[k])flug(F[k],k,1250);spaeter(function(){li.classList.add('fb-hell')},1080)},380+k*520)});
      rt=setTimeout(runde,380+L.length*520+1250+PAUSE)},1150)}
  W.forEach(function(w,i){w.addEventListener('click',function(){zeig(i)})});
  [].forEach.call(f.querySelectorAll('.fb__pf button'),function(b,i){b.addEventListener('click',function(){zeig((akt<0?0:akt)+(i?1:-1))})});
  function wach(){if(!sicht||document.hidden){ruhe();return}if(akt<0)zeig(0);else if(S[akt].querySelector('.fbz.fb-hell')){clearTimeout(rt);rt=setTimeout(runde,600)}}
  new IntersectionObserver(function(es){sicht=es[0].isIntersecting;wach()},{threshold:.3}).observe(raum);
  document.addEventListener('visibilitychange',wach);
  addEventListener('resize',function(){clearTimeout(zt);zt=setTimeout(function(){if(akt>=0){D=wege(S[akt]);zeichne()}},180)});
})();
</script>
'''
