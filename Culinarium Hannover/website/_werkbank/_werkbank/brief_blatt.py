#!/usr/bin/env python3
"""Baustein in der Werkbank Culinarium (Werkbank-Chat 28.10.2026), über das Schäfli kopiert; die Herkunft steht darunter wie in der Vorlage.
Werkbank Wirtschaft am Schlössli (Vorlage Ruedihus), Brief (12.10.2026, Master 5b Punkt 2): das Haus über die ganze Breite, der Brief als helles Blatt darüber.

Eigen fürs Ruedihus: kein Wort zur Person (die Vorstellung steht einmal auf der Übersicht der vier Häuser), keine Karte mit den drei Orten.
Das Blatt liegt wie ein Brief auf dem Tisch: erster Absatz gross in der Titelschrift des Hauses, der Rest in zwei Spalten,
oben rechts im Foto die Einkerbung mit dem Hausnamen, unten Roberts Bild, Unterschrift und woher der Brief kommt.
Das Blatt steigt mit dem Scrollen herauf und ist von Anfang an ganz zu sehen (kein Einblenden über die Deckkraft).
Eingehängt in haus.py: brief_abschnitt = brief_blatt.abschnitt(globals()), CSS am Dateiende, BILDER an EIGENE_BILDER."""
import os
import orte_kurs as _OK

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)


def bilder(B):
    return [('bf-haus', B['bild'], 2400, dict(q=80, schnitt=B.get('schnitt', 2.0), lage=B.get('lage', (.5, .5))))]


def abschnitt(h):
    B = h['BRIEF']

    def bau(k):
        e, bild = k['e'], k['bild']
        # Roberts rundes Porträt rechts im Text des letzten Absatzes, der Text läuft um den Kreis (Robert 17.10.2026: «aussieht wie ein Rivage»,
        # Vorbild Brief der Rivage-Werkbank bf-ich mit bf-stuetze, nur gelesen); die Stütze ohne Breite schiebt das Bild auf seine Höhe
        ab = B['absaetze'][1:]
        ich = '<i class="bf-stuetze" aria-hidden="true"></i><span class="bf-ich">' + bild('robert', 'Robert Reff') + '</span>'
        # Robert 18.10.2026 23:22/23:31: links die ersten Absätze, rechts der letzte beim Porträt; beide Spalten oben bündig und unten gleich lang
        rest = '<div class="bf-links">' + ''.join(f'<p>{p}</p>' for p in ab[:-1]) + '</div><div class="bf-rechts">' + ich + f'<p>{ab[-1]}</p></div>'
        return f'''
<section class="fl {k['fl']} blatt bf" id="brief">
  <div class="in">
    {k['kap'](k['nr'], k['name'])}
    {k['titel'](k['zeilen'])}
    <figure class="bf-bild" data-a="heben">
      {bild('bf-haus', B['bild_alt'], lazy=False)}
    </figure>
    <!-- Gestaltung 28.10.2026: Zeile «CULINARIUM —— im Walk on the Wild Side» unter dem Bild entfernt; das Blatt liegt darüber (schaute nur halb hervor) und der Name stand als gesperrte Antiqua statt Rudis Wortmarke -->
    <article class="bf-blatt" data-a="heben">
      <p class="bf-gross">{B['absaetze'][0]}</p>
      <i class="bf-zier"></i>
      <div class="bf-text">{rest}</div>
      <script>(function(){{var t=document.currentScript.parentElement.querySelector('.bf-text');if(!t)return;var L=t.querySelector('.bf-links'),R=t.querySelector('.bf-rechts'),st=R&&R.querySelector('.bf-stuetze'),ich=R&&R.querySelector('.bf-ich');if(!L||!st||!ich)return;
function eben(){{if(innerWidth<900){{st.style.height='';return}}st.style.height='0px';var cs=getComputedStyle(ich),m=parseFloat(cs.marginTop)+parseFloat(cs.marginBottom);st.style.height=Math.max(0,L.offsetHeight-ich.offsetHeight-m)+'px'}}
eben();addEventListener('resize',eben);addEventListener('load',eben);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(eben)}})();</script>
      <footer class="bf-fuss">
        {f'<p class="bf-gruss">{B["schluss"]}</p>' if B.get('schluss') else ''}
        <div class="bf-fuss__reihe">{_OK.block('brief')}
        <p class="bf-name"><img class="bf-sig" src="eigen/unterschrift.webp" width="890" height="282" alt="Unterschrift Robert Reff" loading="lazy" decoding="async"><span>Robert Reff · Tasty Studios</span></p></div>
      </footer>
    </article>
  </div>
</section>'''
    return bau


CSS = """
/* Schäfli (wie Schlössli): der Name sitzt auf einer feinen Linie, keine Einkerbung */
.bf-horizont{display:flex;align-items:center;gap:clamp(14px,1.6vw,24px);margin:clamp(16px,1.8vw,26px) 0 0;color:var(--tinte)}
.bf-horizont b{font-family:var(--serif);font-weight:400;font-size:clamp(.92rem,1.1vw,1.1rem);letter-spacing:.2em;text-transform:uppercase;white-space:nowrap}
.bf-horizont i{flex:1;height:1px;background:var(--gold);transform-origin:0 50%}
.bf-horizont small{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--taupe);white-space:nowrap}
.bf-horizont[data-a="auf"] i{transform:scaleX(0);transition:transform 1.6s cubic-bezier(.16,1,.3,1) .2s}.bf-horizont.da i{transform:none}
@media(max-width:600px){.bf-horizont{flex-wrap:wrap}.bf-horizont i{flex-basis:100%;order:3}}

/* ---------- Brief (brief_blatt.py, 12.10.2026): Hausfoto über die ganze Breite, der Brief als Blatt darüber ---------- */
.bf-bild{position:relative;margin:clamp(26px,3vw,48px) 0 0;border-radius:26px;overflow:hidden;aspect-ratio:2;background:#cdbb9c;box-shadow:0 50px 60px -40px rgba(60,34,12,.62)}
.bf-bild img{display:block;width:100%;height:100%;object-fit:cover}
.bf-kerbe{position:absolute;right:0;top:0;padding:13px 22px 15px 26px;border-radius:0 0 0 22px;background:var(--papier);font-family:var(--serif);font-weight:700;font-size:clamp(1.06rem,1.3vw,1.4rem);line-height:1.2;color:var(--tinte)}
.bf-kerbe small{display:block;margin-top:4px;font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--taupe)}
.bf-kerbe::before,.bf-kerbe::after{content:'';position:absolute;width:22px;height:22px;background:radial-gradient(circle at 0 100%,transparent 21.5px,var(--papier) 22px)}
.bf-kerbe::before{right:100%;top:0}.bf-kerbe::after{right:0;top:100%}
.bf-blatt{position:relative;z-index:1;width:min(1180px,calc(100% - clamp(20px,7vw,150px)));margin:calc(-1*clamp(44px,8vw,140px)) auto 0;
  padding:clamp(28px,4.2vw,72px) clamp(22px,4.8vw,84px) clamp(24px,3vw,46px);border-radius:26px;background:var(--weiss);color:var(--tinte);
  box-shadow:inset 0 1px 0 #fffdf7,0 0 0 1px rgba(125,79,39,.2),0 46px 70px -46px rgba(60,34,12,.62),0 16px 28px -22px rgba(60,34,12,.3)}
.bf-gross{margin:0;font-family:var(--sans);font-weight:400;font-size:clamp(1.3rem,1.9vw,2.05rem);line-height:1.36;color:var(--tinte);text-wrap:pretty}
.bf-zier{display:block;width:64px;height:2px;margin:clamp(22px,2.6vw,38px) 0;background:var(--messing);opacity:.8}
.bf-text{display:flow-root;font-size:clamp(1.04rem,1.18vw,1.24rem);line-height:1.68;color:rgba(42,26,14,.86)}
.bf-text p{margin:0}.bf-text p+p{margin-top:1.05em}
@media(min-width:900px){.bf-text{columns:2;column-gap:clamp(36px,4.6vw,80px)}.bf-text p{break-inside:avoid}}
.bf-fuss{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:18px clamp(20px,3vw,48px);margin-top:clamp(26px,3.2vw,50px);padding-top:clamp(20px,2.4vw,34px);border-top:1px solid rgba(125,79,39,.34)}
.bf-wer{display:flex;align-items:center;gap:clamp(14px,1.6vw,22px);margin:0}
.bf-ich{flex:none;display:block;width:clamp(72px,6.2vw,96px);aspect-ratio:1;border-radius:50%;overflow:hidden;box-shadow:0 0 0 1px rgba(42,26,14,.2),0 0 0 5px #fffaf0,0 0 0 6px rgba(42,26,14,.2),0 18px 24px -14px rgba(60,34,12,.6)}
.bf-ich img{display:block;width:100%;height:100%;object-fit:cover;border-radius:50%}
.bf-wer b{display:block;font-family:var(--serif);font-weight:700;font-size:clamp(1.3rem,1.7vw,1.7rem);line-height:1.1}
.bf-wer small{display:block;margin-top:6px;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--taupe)}
.bf-sig{display:block;width:clamp(150px,15.5vw,230px);height:auto;margin-right:clamp(0px,3vw,48px);transform:rotate(-4deg);pointer-events:none}
@media(max-width:759px){.bf-bild{aspect-ratio:1.16;border-radius:22px 0 22px 22px}.bf-blatt{border-radius:22px}
  .bf-kerbe{padding:10px 14px 11px 18px;font-size:1rem}.bf-kerbe small{font-size:9.5px;letter-spacing:.12em}.bf-sig{margin-right:0}}
/* Auftritt: federleicht von unten, langer weicher Weg. Das Foto blendet dabei ein, das Blatt nicht (grosse helle Fläche: nur transform). */
.bf [data-a="heben"]{opacity:0;transform:translateY(150px) scale(.965);transition:opacity 1.3s cubic-bezier(.16,1,.3,1),transform 2.1s cubic-bezier(.16,1,.3,1)}
.bf [data-a="heben"].da{opacity:1;transform:none}
.bf .bf-blatt[data-a="heben"]{opacity:1}
@supports (animation-timeline: view()){
  .bf .bf-blatt[data-a="heben"],.bf .bf-blatt[data-a="heben"].da{transition:none;animation:bfBlattHoch cubic-bezier(.3,.25,.4,1) both;animation-timeline:view();animation-range:entry 0% cover 36%}
  @keyframes bfBlattHoch{from{transform:translate3d(0,150px,0) scale(.975)}to{transform:none}}
}
@media (prefers-reduced-motion:reduce){.bf [data-a="heben"]{opacity:1;transform:none;transition:none}.bf .bf-blatt[data-a="heben"]{animation:none;transform:none}}
/* ---------- Unterschrift wie beim Rivage (Werkbank-Chat 17.10.2026, Master Website-Bau 2): Porträt rund rechts im Text, der Text läuft herum;
   unten der Leitsatz links, rechtsbündig die Unterschrift, darunter klein Name und Tasty Studios. Das Hausfoto steht als Band, nichts wandert mit. ---------- */
.bf-text{display:block}
.bf-text p{margin:0 0 1.05em}.bf-text p:last-child{margin-bottom:0}.bf-text p+p{margin-top:0}
.bf-stuetze{float:right;width:0;height:calc(1*1.68em)}
.bf-ich{float:right;clear:right;width:clamp(118px,10vw,170px);aspect-ratio:1;margin:8px 8px 8px clamp(18px,1.8vw,28px);border-radius:50%;overflow:hidden;
  shape-outside:circle(50%) border-box;shape-margin:clamp(14px,1.4vw,22px);
  box-shadow:0 0 0 1px rgba(42,26,14,.2),0 0 0 6px #fffaf0,0 0 0 7px rgba(183,143,81,.55),0 20px 26px -14px rgba(60,34,12,.6)}
.bf-gruss{flex:1 1 100%;margin:0;font-family:var(--sans);font-weight:400;font-size:clamp(1.08rem,1.4vw,1.4rem);line-height:1.38;color:var(--tinte);text-wrap:pretty}
.bf-gruss q{quotes:'«' '»'}
.bf-name{margin:0 clamp(10px,4vw,56px) 0 auto;display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center}   /* Robert 18.10.2026: nicht ganz an den rechten Rand, kleiner, Luft */
.bf-name .bf-sig{margin-right:0;width:clamp(118px,11vw,168px);transform:rotate(-3deg)}
.bf-name span{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--taupe)}
@media(max-width:759px){.bf-stuetze{height:calc(2*1.68em)}.bf-ich{width:104px;shape-margin:16px}.bf-name{align-self:flex-end}}
/* Robert 18.10.2026 23:22: rechte Spalte oben bündig mit der linken, unten keine leere Fläche. Zwei feste Spalten (links die ersten Absätze, rechts der
   letzte beim Porträt); die Stütze schiebt das Porträt so weit hinunter, dass es mit dem letzten Wort links endet (BF_JS rechnet nach). */
.bf-links p+p{margin-top:0}@media(max-width:899px){.bf-rechts{margin-top:1.05em}}
@media(min-width:900px){.bf-text{columns:auto!important;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:clamp(36px,4.6vw,80px);align-items:stretch}
  .bf-rechts{display:flow-root}.bf-rechts .bf-ich{margin-bottom:0}}
/* Brief mit den drei Orten (29.10.2026): Kursblatt und Unterschrift in einer Reihe unter dem Gruss, beide auf einer Mitte, kein Loch */
.bf-fuss__reihe{flex:1 1 100%;display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);align-items:center;gap:clamp(22px,3.4vw,56px)}
.bf-fuss__reihe .bf-name{margin:0 auto;align-self:center}
@media(max-width:759px){.bf-fuss__reihe{grid-template-columns:1fr}.bf-fuss__reihe .bf-name{align-self:center}}
"""
