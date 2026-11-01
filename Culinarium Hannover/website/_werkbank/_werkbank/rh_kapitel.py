#!/usr/bin/env python3
"""Baustein in der Werkbank Culinarium (Werkbank-Chat 28.10.2026), über das Schäfli kopiert; die Herkunft steht darunter wie in der Vorlage.
Werkbank Taverne zum Schäfli in acht Kapiteln (Vorlage Schlössli, dort Ruedihus) (Werkbank-Chat 17.10.2026; Aufbau wie die Werkbank des Carlton-Europe vom 15.10.2026, Technik über das
Waldhotel Doldenhorn (dh_kapitel.py, nur gelesen und kopiert), Kleid und Worte des Ruedihus):
Auftakt, Brief, «Worum es geht», Register → Was wir gefunden haben → Ihre Marke → Ihre Website → Karten und Unterlagen → Ihre Werkzeuge
→ Für draussen → Geprüft → Die Übergabe → Schluss und «Alles auf einen Blick».

  KAPITEL     Anker, Name, eine Zeile fürs Register, Name in der Leiste, Objekt. Leiste und Register lesen von hier.
              Der Befund (k1) zählt erst mit, wenn er gebaut ist (BEFUND_DA, setzt wb_kapitel.py): bis «Die Lupe» eingebaut ist, bleibt er draussen
              und die übrigen Kapitel zählen ab I. Die Anker k1 bis k8 bleiben fest.
  register()  der Fächer der freigestellten Objekte, je Kapitel eines; Pfeile, Ziffern, Tippen, Wischen, Tasten. Kein Aufklappen.
  kap()       über dem ersten Abschnitt eines Kapitels «Kapitel III» über dem Medaillon, dazu die grosse Ziffer im Hintergrund.
  platzhalter()  nur lokal (PLATZHALTER_ERLAUBT=0 bricht ab), falls eine Lieferung fehlt."""
import html, json, os
_PK = (lambda p: len(json.load(open(p))['karten']) if os.path.exists(p) else 13)(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'postkarten_plan.json'))   # Zahl der Postkarten aus dem Plan

e = html.escape
ROEM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
KAPITEL_ALLE = [  # Anker, Name, Zeile im Register, Name in der Leiste, Objekt
    ('k1', 'Befund des aktuellen Auftritts online', 'Wie Culinarium heute im Netz steht, an vier Beispielen mit Bild.', 'Befund', 'analyse-h'),
    ('k2', 'Eure Marke', 'Die Wortmarke, das C, die Schriften und die Farben eurer Plakate, gesammelt in einem eigenen Werkzeug.', 'Marke', 'livre'),
    ('k3', 'Eure Website', 'Das Profil von heute neben der neuen Seite, zwölf Stellen mit ihrem Gedanken und jede Seite von der Tafel bis Dirty Chicken.', 'Website', 'website'),
    ('k4', 'Karten und Unterlagen', 'Die Karte am Platz für jeden Abend, neu gesetzt neben der Karte, wie sie auf dem Tisch lag.', 'Karten', 'unterlagen'),
    ('k5', 'Eure Werkzeuge', 'Sieben Werkzeuge für Termine, Menüs, Plakate und Gäste, eines davon als Eingang zu allen.', 'Werkzeuge', 'maison'),
    ('k6', 'Für draußen', f'24 Drucksachen, zwölf Untersetzer, elf Mails, {_PK} Postkarten von euren Plakaten, 40 Sticker und fünf Beigaben, darunter ein Gutschein für einen Abend.', 'Draußen', 'drucksachen'),
    ('k7', 'Geprüft', 'Wie alles ausprobiert wurde, und welche Fragen bei euch liegen.', 'Geprüft', 'geprueft'),
    ('k8', 'Die Übergabe', 'Ihr bekommt alles, und es läuft so. Keine Bindung, kein Vertrag; laufende Betreuung optional, aber empfohlen.', 'Übergabe', 'vorschlag'),   # Robert 1.11.2026: statt «Das Angebot»
]
BEFUND_DA = False   # setzt wb_kapitel.py, sobald der Befund («Die Lupe») gebaut ist


def kapitel_liste():
    """Die Kapitel, die heute in der Werkbank stehen: (Nummer der Reihe, Anker, Name, Zeile, Leiste, Objekt)."""
    da = [k for k in KAPITEL_ALLE if BEFUND_DA or k[0] != 'k1']
    return [(i + 1, *k) for i, k in enumerate(da)]


def _nach_anker(a):
    for k in kapitel_liste():
        if k[1] == a:
            return k
    raise SystemExit(f'rh_kapitel: Kapitel {a} steht nicht in der Werkbank')


LOKAL = os.environ.get('PLATZHALTER_ERLAUBT', '1') != '0'
OFFEN = []
_ZVB = __import__('re').search(r'viewBox="([^"]+)"', open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', '..', '_werkzeuge', 'oberflaeche', 'kleid', 'culinarium-zeichen.svg'), encoding='utf-8').read()).group(1)   # viewBox des «C» (29.10.)
ZEICHEN = f'<svg class="kap__z" viewBox="{_ZVB}" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>'   # das «C» des Hauses


def nr(n):
    return ROEM[n - 1]


def kap(a, mehr=''):
    """Kopf des ersten Abschnitts eines Kapitels (a = Anker k1 … k8): «Kapitel III» klein über dem Medaillon, darunter der Name des Kapitels."""
    n, _, name, _, _, _ = _nach_anker(a)
    return f'<p class="kap kap--z kap--k" data-a="auf"{mehr}><span class="kap__geist" aria-hidden="true">{nr(n)}</span><small class="kap__nr">Kapitel {nr(n)}</small>{ZEICHEN}<span>{e(name)}</span></p>'


def leiste():
    return ''.join(f'<a href="#{a}">{e(l)}</a>' for _, a, _, _, l, _ in kapitel_liste()) + '<a href="#uebersicht">Übersicht</a>'


PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'


def register(kopf):
    """Register mit den freigestellten Objekten: derselbe Fächer wie «Alles auf einen Blick», je Kapitel ein Objekt, darunter Ziffer, Name, Satz, «Zum Kapitel»."""
    K_ = kapitel_liste()
    karten = ''.join(
        f'<a class="fblatt" href="#{a}" data-i="{i}"><img src="eigen/fo-{o}.webp" width="1000" height="1000" alt="Kapitel {nr(n)}: {e(name)}" loading="lazy" decoding="async"></a>'
        for i, (n, a, name, z, _, o) in enumerate(K_))
    texte = ''.join(
        f'<div class="{"an" if i == 0 else ""}"><p class="rgc-t__k">Kapitel {nr(n)}</p><h3>{e(name)}</h3><p>{e(z)}</p>'
        f'<a class="kn kn--klein" href="#{a}">Zum Kapitel<i>{PF}</i></a></div>'
        for i, (n, a, name, z, _, o) in enumerate(K_))
    punkte = ''.join(f'<button type="button" class="rgc-p" data-i="{i}" aria-label="Kapitel {nr(n)}">{nr(n)}</button>' for i, (n, *_r) in enumerate(K_))
    li = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg>'
    re_ = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>'
    return f'''
<section class="fl fl--nacht tapete-leicht blatt rg" id="register">
  <div class="in">
    {kopf}
    <div class="rgw">
      <div class="wfa" data-rgw tabindex="0" aria-roledescription="Karussell" aria-label="Die Kapitel">
        <div class="wfa__b">{karten}</div>
        <div class="wfa__fuss">
          <button type="button" class="wf__pf" data-f="-1" aria-label="Voriges Kapitel">{li}</button>
          <div class="wfa__texte" aria-live="polite">{texte}</div>
          <button type="button" class="wf__pf" data-f="1" aria-label="Nächstes Kapitel">{re_}</button>
        </div>
        <div class="rgc-punkte">{punkte}</div>
      </div>
    </div>
  </div>
</section>
<script>(function(){{var f=document.querySelector('.rgw [data-rgw]');if(!f)return;
var bl=[].slice.call(f.querySelectorAll('.fblatt')),tx=[].slice.call(f.querySelectorAll('.wfa__texte>div')),P=[].slice.call(f.querySelectorAll('.rgc-p')),n=bl.length,ist=0,halb=Math.floor(n/2);
function zeige(k){{ist=(k%n+n)%n;bl.forEach(function(b,i){{var p=((i-ist+n+halb)%n)-halb;b.setAttribute('data-p',p);b.setAttribute('aria-hidden',p!==0);b.tabIndex=p===0?0:-1}});tx.forEach(function(t,i){{t.classList.toggle('an',i===ist)}});P.forEach(function(p,i){{p.setAttribute('aria-pressed',i===ist?'true':'false')}})}}
[].forEach.call(f.querySelectorAll('[data-f]'),function(b){{b.addEventListener('click',function(){{zeige(ist+(+b.getAttribute('data-f')))}})}});
P.forEach(function(p,i){{p.addEventListener('click',function(){{zeige(i)}})}});
bl.forEach(function(b,i){{b.addEventListener('click',function(ev){{if(i!==ist){{ev.preventDefault();zeige(i)}}}})}});
f.addEventListener('keydown',function(ev){{if(ev.key==='ArrowRight')zeige(ist+1);else if(ev.key==='ArrowLeft')zeige(ist-1)}});
var x0=null,st=f.querySelector('.wfa__b');st.addEventListener('touchstart',function(ev){{x0=ev.touches[0].clientX}},{{passive:true}});st.addEventListener('touchend',function(ev){{if(x0===null)return;var d=ev.changedTouches[0].clientX-x0;x0=null;if(Math.abs(d)>40)zeige(ist+(d<0?1:-1))}},{{passive:true}});
if('IntersectionObserver' in window)new IntersectionObserver(function(es,o){{es.forEach(function(x){{if(x.isIntersecting){{f.classList.add('da');o.disconnect()}}}})}},{{threshold:.25}}).observe(f);else f.classList.add('da');zeige(0)}})();</script>'''


def platzhalter(titel, wer, was, hell=False):
    """Nur lokal sichtbar und als Platzhalter beschriftet. Geht nie online: online.py baut mit PLATZHALTER_ERLAUBT=0, dann bricht der Bau hier ab."""
    OFFEN.append(f'{titel} ({wer})')
    if not LOKAL:
        raise SystemExit(f'Platzhalter «{titel}» steht noch (liefert {wer}). Erst einhängen, dann hochladen.')
    return (f'<div class="ph{" ph--hell" if hell else ""}" role="note"><p class="ph__k">Platzhalter · nur lokal</p><h3>{e(titel)}</h3>'
            f'<p>{e(was)}</p><p class="ph__w">liefert {e(wer)} · über _werkbank/LIEFERUNGEN.md</p></div>')


CSS = '''
/* ---------- Dichter und filmischer (Robert 15.10.2026: «ich scrolle sehr viel durch Leerräume», «cineastischer») ---------- */
:root{--abschnitt:clamp(60px,6.6vw,108px)}
.kopfzeile{margin-bottom:clamp(30px,3.4vw,56px)}
.kap.kap--z~.zt.zt{font-size:clamp(2rem,4.5vw,4.9rem)}
.kap__z{width:clamp(54px,5.4vw,86px)}
.kopfzeile .lauf{margin-top:clamp(14px,1.6vw,24px)}
.kap--k{position:relative}
.kap__geist{position:absolute;left:50%;top:50%;z-index:-1;translate:-50% -46%;font-family:var(--serif);font-weight:400;font-size:clamp(12rem,30vw,34rem);line-height:1;letter-spacing:.02em;color:var(--gold);opacity:.07;white-space:nowrap;pointer-events:none;-webkit-user-select:none;user-select:none}
.fl--papier .kap__geist,.fl--creme .kap__geist{color:var(--taupe);opacity:.09}
.kopfzeile{position:relative;isolation:isolate}
@supports (animation-timeline:view()){
  .kap__geist{animation:kgGeist linear both;animation-timeline:view();animation-range:entry 0% exit 90%}
  @keyframes kgGeist{0%{translate:-50% -10%;scale:.86;opacity:0}35%{opacity:.09}100%{translate:-50% -80%;scale:1.08;opacity:0}}
  .kopfzeile .zt .z>span{will-change:transform}
}
/* Farben der Marke (Robert 15.10.2026: «eleganter hochkommen, die gehen alle zu schnell hoch»): länger, weicher, deutlicher gestaffelt */
.m2.lebt .m2-gr{transition:opacity 1.8s var(--e2),translate 3.2s var(--e1),scale 3.2s var(--e1)!important}
.m2.lebt .m2-gr:nth-child(2){transition-delay:.35s!important}.m2.lebt .m2-gr:nth-child(3){transition-delay:.7s!important}.m2.lebt .m2-gr:nth-child(4){transition-delay:1.05s!important}
.m2.lebt .m2-chip i{transition:transform 2.4s var(--e1) 1s!important}
.m2.lebt .m2-gruppen,.m2.lebt .m2-glanz{transition:opacity 1.6s ease 1.9s!important}
@media(prefers-reduced-motion:reduce){.kap__geist{animation:none}}
/* ---------- Kapitel (kapitel.py, 15.10.2026): «Kapitel III» über dem CE im Kopf des ersten Abschnitts ---------- */
.kap__nr{display:block;font-family:var(--mono);font-size:clamp(.7rem,.78vw,.8rem);letter-spacing:.32em;text-indent:.32em;text-transform:uppercase;color:var(--gold);opacity:.9}
.fl--papier .kap__nr,.fl--creme .kap__nr{color:var(--taupe)}
.kap--k>span{font-size:clamp(1.08rem,1.24vw,1.3rem)}
/* ---------- Papier mit drei Karten: Aufkleber, Drucksachen, Mails (15.10.2026) ---------- */
@media(min-width:1000px){.papier{grid-template-columns:1fr 1fr}}   /* vier Karten (Untersetzer, Drucksachen, Mails, Postkarten): zwei mal zwei, keine Lücke (29.10.2026) */
.pk--mail{background:#f4ecdc;color:var(--tinte);box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(150,125,64,.36)}
.pk--mail p{color:rgba(12,21,38,.86)}
.pk--mail .kn{--o:#1f3f77;--m:#0b1f40;--u:#040d1e;--t:#fff;--licht:rgba(255,255,255,.26);--kante:rgba(0,0,0,.55);--tf:rgba(6,20,43,.6);--ko:#fbf3e2;--ku:#cfbd98;--kt:var(--tinte);--klicht:rgba(255,255,255,.9)}
.mlp img{display:block;width:100%;height:auto;aspect-ratio:1200/1920;object-fit:cover;object-position:50% 0;border-radius:5px;box-shadow:0 0 0 1px rgba(12,21,38,.12),0 22px 26px -18px rgba(40,30,10,.7)}
/* Fuss «Alles auf einen Blick»: zweite Zeile in Gold wie alle Überschriften */
.wf .wege__t em{font-style:normal;color:var(--gold)}
/* ---------- Register mit freigestellten Objekten (15.10.2026, vierte Fassung): derselbe Fächer wie der Fuss ---------- */
.rg .kopfzeile{margin-bottom:clamp(10px,1.4vw,24px)}
.rgw{text-align:center}
.rgw .wfa{position:relative;margin-top:clamp(10px,1.6vw,30px);outline:none}
.rgw .wfa__b{position:relative;height:clamp(240px,34vw,500px)}
.rgw .wfa__b::before{content:'';position:absolute;left:50%;top:50%;width:min(70vw,760px);height:min(52vw,560px);transform:translate(-50%,-50%);border-radius:50%;
  background:radial-gradient(closest-side,rgba(220,198,143,.12),rgba(220,198,143,.04) 55%,transparent);pointer-events:none}
.rgw .fblatt{position:absolute;left:50%;top:0;height:100%;aspect-ratio:1;margin:0;display:block;cursor:pointer;
  --x:0%;--s:.5;--o:0;transform:translateX(calc(-50% + var(--x))) scale(var(--s));opacity:var(--o);pointer-events:none;
  transition:transform .95s cubic-bezier(.2,.8,.2,1),opacity .6s cubic-bezier(.2,.8,.2,1)}
.rgw .fblatt img{width:100%;height:100%;object-fit:contain;display:block}
.rgw .fblatt[data-p="0"]{--x:0%;--s:1;--o:1;z-index:5;pointer-events:auto}
.rgw .fblatt[data-p="-1"]{--x:-74%;--s:.66;--o:.5;z-index:4;pointer-events:auto}
.rgw .fblatt[data-p="1"]{--x:74%;--s:.66;--o:.5;z-index:4;pointer-events:auto}
.rgw .fblatt[data-p="-2"]{--x:-128%;--s:.46;--o:.2;z-index:3;pointer-events:auto}
.rgw .fblatt[data-p="2"]{--x:128%;--s:.46;--o:.2;z-index:3;pointer-events:auto}
.rgw .fblatt[data-p="-3"]{--x:-170%}.rgw .fblatt[data-p="3"]{--x:170%}
.rgw .wfa:not(.da) .fblatt{--x:0%;--s:.7;--o:0}
.rgw .wfa__fuss{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:clamp(14px,3vw,50px);max-width:820px;margin:0 auto}
.rgw .wfa__texte{display:grid;text-align:center}
.rgw .wfa__texte>div{grid-area:1/1;display:flex;flex-direction:column;align-items:center;opacity:0;visibility:hidden;transform:translateY(14px);transition:opacity .4s ease,transform .6s ease,visibility 0s .45s}
.rgw .wfa__texte>div.an{opacity:1;visibility:visible;transform:none;transition:opacity .6s ease .15s,transform .8s ease .15s}
.rgw .wfa__texte h3{margin:0;font-family:var(--serif);font-weight:400;font-size:clamp(1.7rem,2.6vw,2.7rem);line-height:1.1;color:var(--weiss)}
.rgw .wfa__texte h3::after{content:'';display:block;width:96px;height:8px;margin:clamp(14px,1.4vw,18px) auto 0;
  background:linear-gradient(90deg,transparent,rgba(220,198,143,.8) 18%,rgba(220,198,143,.8) 40%,transparent 40%,transparent 60%,rgba(220,198,143,.8) 60%,rgba(220,198,143,.8) 82%,transparent) 0 3.5px/100% 1px no-repeat}
.rgw .wfa__texte p{margin:clamp(12px,1.2vw,16px) auto 0;max-width:46ch;font-size:clamp(1.02rem,1.14vw,1.16rem);line-height:1.56;color:rgba(251,246,234,.8)}
.rgw .wfa__texte .kn{margin-top:clamp(18px,1.8vw,26px);align-self:center}
.wf__pf{width:56px;height:56px;border-radius:50%;display:grid;place-items:center;cursor:pointer;color:var(--weiss);border:1px solid rgba(220,198,143,.4);
  background:radial-gradient(circle at 50% 30%,#24477f,#0b1f40 60%,#06142b);box-shadow:0 14px 22px -12px rgba(0,0,0,.9),inset 0 1px 0 rgba(255,255,255,.12);transition:border-color .4s}
.wf__pf svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.wf__pf:hover{border-color:rgba(240,223,174,.9)}
.rgw .wfa__zahl{max-width:none;margin-top:clamp(18px,2vw,28px);text-align:center;font-family:var(--mono);font-size:.82rem;letter-spacing:.24em;color:var(--taupe)}
@media(max-width:700px){
  .rgw .wfa__b{height:min(78vw,340px)}
  .rgw .fblatt[data-p="-1"]{--x:-62%;--s:.55;--o:.4}.rgw .fblatt[data-p="1"]{--x:62%;--s:.55;--o:.4}
  .rgw .fblatt[data-p="-2"],.rgw .fblatt[data-p="2"]{--o:0}
  .rgw .wfa__fuss{grid-template-columns:1fr 1fr;justify-items:center;row-gap:20px}
  .rgw .wfa__texte{grid-column:1/-1;grid-row:1}
  .rgw .wfa__fuss>button:first-of-type{justify-self:end}.rgw .wfa__fuss>button:last-of-type{justify-self:start}
}
.rgc-t__k{font-family:var(--mono);font-size:.72rem;letter-spacing:.3em;text-transform:uppercase;color:var(--gold)}
.rgw .wfa__texte>div>p:not(.rgc-t__k){margin-top:10px}
.rgc-punkte{display:flex;justify-content:center;flex-wrap:wrap;gap:8px;margin-top:clamp(20px,2.2vw,30px)}
.rgc-p{min-width:44px;padding:7px 10px;border-radius:999px;font-family:var(--serif);font-size:.96rem;color:rgba(251,246,234,.6);box-shadow:inset 0 0 0 1px rgba(220,198,143,.3);transition:color .4s,background .4s}
.rgc-p[aria-pressed="true"]{color:var(--tinte);background:var(--gold)}
.rg__ce{display:inline-block;width:clamp(36px,3.2vw,46px);height:auto;color:#c2a560;fill:url(#cegold)}
/* ---------- Platzhalter (nur lokal, nie online) ---------- */
.ph{max-width:880px;margin:clamp(24px,3vw,44px) auto 0;padding:clamp(26px,3vw,44px);border-radius:22px;border:1.5px dashed rgba(220,198,143,.6);color:rgba(255,255,255,.88);text-align:center;background:repeating-linear-gradient(135deg,rgba(220,198,143,.05) 0 14px,transparent 14px 28px)}
.ph--hell,.fl--papier .ph,.fl--creme .ph{border-color:rgba(138,117,69,.6);color:var(--tinte)}
.ph__k{font-family:var(--mono);font-size:.74rem;letter-spacing:.24em;text-transform:uppercase;color:#e0a96a}
.ph h3{margin:12px 0 10px;font-family:var(--serif);font-weight:400;font-size:clamp(1.5rem,2.2vw,2.2rem)}
.ph p{max-width:56ch;margin-inline:auto}
.ph__w{margin-top:14px!important;font-family:var(--mono);font-size:.78rem;opacity:.7}
'''
