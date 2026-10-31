#!/usr/bin/env python3
"""Baustein in der Werkbank Culinarium (Werkbank-Chat 28.10.2026), über das Schäfli kopiert; die Herkunft steht darunter wie in der Vorlage.
Werkbank Culinarium (Vorlage Schäfli, dort Ruedihus; Werkbank-Chat 28.10.2026; Master 5b Punkte 12, 19, 20):

1. Zwei Fenster zwischen gleichfarbigen Abschnitten: Bild und Satz stehen, der Ausschnitt wandert. Bauart wie die Fenster der Websites nach dem
   Safari-Befund vom 11.10.2026: niemand beschneidet, Bild und Satz liegen ganz unten (z-index −1), die deckenden Nachbarn verdecken alles ausserhalb.
   Die Sätze gehören zum Angebot (Wortlaut aus dem Brief und dem Abschnitt Studio), nie ein Gäste-Satz der Website (Robert 12.10.2026).
     vor «Studio»:  der Blick durchs Fenstergitter auf den Garten, «So einfach wie eine Tafel neu zu beschriften.»
     vor «Ausblick»: die zwei Laibe Brot, «Alles liegt auf dem Tisch.»
   Die Bilder sind die Fenster-Fassungen der Ruedihus-Seite (assets/img/fenster-*.webp, das Dunkel ist ins Bild gerechnet).
2. «Was noch dazukommt» als Tafel: Wandholz mit Butzenscheiben und doppeltem Goldrand, oben ein Foto des Hauses neben dem nächsten Schritt,
   darunter die offenen Punkte als Spalten. Ersetzt den Kit-Abschnitt «dazu» über EIGENE.
Eingehängt am Ende von haus.py."""
import os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
import haus as _H
VB = _H.ZEICHEN[0]

FENSTER = [   # id, vor welchem Abschnitt, Bild (Foto der Website, abgedunkelt nach _werkbank/eigen/fen-<id>-*.webp), Zeilen, kleine Zeile, Bildbeschreibung
    dict(id='fenster-haus', vor='papier', bild='theke', zeilen=('Ihr führt die Seite', 'selbst.'), klein='Für Termine, Menüs, Plakate und Gäste gibt es je ein eigenes Werkzeug.',
         alt='Hinter der Theke des Walk on the Wild Side unter dem Negroni-Schriftzug'),
    dict(id='fenster-tisch', vor='material', bild='kerze3', zeilen=('Ein Abend,', 'ein Auftritt.'), klein='Website, Karten, Werkzeuge und Papier im Kleid von Culinarium.',
         alt='Blick durch die Tür auf die lange Tafel bei Kerzenlicht'),
]
BILDER = [('ab-foto', 'tafelleer', 1200, dict(q=78, schnitt=1.22, lage=(.4, .5)))]


def _mass(bild):
    from PIL import Image
    return Image.open(_H.bild(bild)).size


def fenster_bilder():
    """Die Fenster-Fotos mit dem Dunkel im Bild (kein Verlauf über dem Bild), drei Breiten, nach _werkbank/eigen/ (nach_bau kopiert sie nach werkbank/eigen)."""
    from PIL import Image
    for F in FENSTER:
        im = Image.open(_H.bild(F['bild'])).convert('RGB')
        im = Image.blend(im, Image.new('RGB', im.size, (22, 21, 26)), .42)
        for br in (1200, 1800, 2400):
            k = im.resize((br, round(im.height * br / im.width)), Image.LANCZOS) if im.width > br else im
            k.save(os.path.join(W, 'eigen', f"fen-{F['id']}-{br}.webp"), 'WEBP', quality=80, method=5)


def fenster_html(F):
    b, h = _mass(F['bild'])
    return f'''<section class="wfen" id="{F['id']}" aria-label="{F['zeilen'][0]} {F['zeilen'][1]}">
  <div class="wfen__f">
    <img src="eigen/fen-{F['id']}-1800.webp" srcset="eigen/fen-{F['id']}-1200.webp 1200w, eigen/fen-{F['id']}-1800.webp 1800w, eigen/fen-{F['id']}-2400.webp 2400w" sizes="100vw" width="{b}" height="{h}" alt="{F['alt']}" loading="lazy" decoding="async">
    <div class="wfen__in"><svg class="wfen__z" viewBox="{VB}" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg><h2 class="wfen__t"><span>{F['zeilen'][0]}</span><span><em>{F['zeilen'][1]}</em></span></h2><p class="wfen__k">{F['klein']}</p></div>
  </div>
</section>
'''


JS = '''<script id="wfen-js">
/* Fenster: der Satz kommt, wenn der Ausschnitt gut im Bild ist, und ruht unsichtbar, solange das Fenster nicht im Bild ist */
(function () {
  [].forEach.call(document.querySelectorAll('.wfen'), function (f) {
    if (!('IntersectionObserver' in window)) { f.classList.add('da'); return; }
    f.classList.add('weg');
    new IntersectionObserver(function (es) { f.classList.toggle('weg', !es[0].isIntersecting); }).observe(f);
    new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { o.disconnect(); f.classList.add('da'); } }, { threshold: 0.35 }).observe(f);
  });
})();
</script>
'''


def setz(t):
    """Die Fenster vor ihre Abschnitte. Mehrfach anwendbar."""
    if 'id="hz"' not in t:
        return t
    for F in FENSTER:
        if f'id="{F["id"]}"' in t:
            continue
        m = re.search(r'<section class="[^"]*" id="' + F['vor'] + '"', t)
        if m:
            # der Abschnitt davor bekommt runde Ecken auch unten, damit das Fenster in den Ecken hervorschaut
            t = t[:m.start()] + fenster_html(F) + t[m.start():]
    if 'class="wfen"' in t and 'id="wfen-js"' not in t:
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


def ausblick_abschnitt(H):
    """Eintrag für EIGENE: ersetzt den Kit-Abschnitt «dazu». Texte aus haus.AUSBLICK."""
    AU = H['AUSBLICK']

    def bau(k):
        e, bild = k['e'], k['bild']
        g = AU['gross']
        punkte = ''.join(f'<li data-a="auf" style="--i:{i % 2}"><h3>{e(t)}</h3><p>{x}</p></li>' for i, (t, x) in enumerate(AU['punkte']))
        return f'''
<section class="fl {k['fl']} blatt ab" id="dazu">
  <div class="in">
    {k['kopf']()}
    <div class="ab-tafel" data-a="heben">
      <div class="ab-oben">
        <figure class="ab-bild">{bild('ab-foto', AU.get('bild_alt', ''))}</figure>
        <div class="ab-schritt">
          <svg class="ab-z" viewBox="{VB}" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>
          <small>{e(g[0])}</small>
          <h3>{e(g[1])}</h3>
          <i class="ab-linie"></i>
          <p>{g[2]}</p>
        </div>
      </div>
      <div class="ab-trenn" aria-hidden="true"><i></i><b></b><i></i></div>
      <ul class="ab-liste ab-liste--{len(AU['punkte'])}">{punkte}</ul>
    </div>
  </div>
</section>'''
    return dict(key='dazu', nach='material', nav='', name='Ausblick', zeilen=['Was noch', 'dazukommt.'], text=AU['text'], bau=bau)


CSS = '''
/* ---------- Fenster in der Werkbank (fenster_ausblick.py, 12.10.2026): stehendes Bild, stehender Satz, der Ausschnitt wandert.
   Niemand beschneidet: Bild und Satz liegen mit z-index −1 unter den Abschnitten, die deckenden Nachbarn decken ab. ---------- */
.wfen{position:relative;min-height:min(84vh,800px);margin-top:calc(var(--rund)*-1);color:#fff}
.wfen::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--tief)}
.wfen__f{position:absolute;left:0;right:0;top:-100vh;top:-100lvh;bottom:-100vh;bottom:-100lvh;pointer-events:none}
.wfen__f>img{position:sticky;top:0;z-index:-1;display:block;width:100%;height:100vh;height:100lvh;object-fit:cover;margin-bottom:-100vh;margin-bottom:-100lvh}
.wfen__in{position:sticky;top:50%;z-index:-1;transform:translateY(-50%);padding:0 var(--rand);text-align:center}
.wfen.weg .wfen__in{visibility:hidden}
.wfen__z{display:block;width:clamp(50px,5.9vw,92px);height:auto;margin:0 auto clamp(16px,1.8vw,28px);color:#f3cd94;fill:currentColor}
.wfen__t{margin:0;font-family:var(--serif);font-weight:700;font-size:clamp(2rem,5.5vw,5.9rem);line-height:1.05;color:#fff;
  text-shadow:0 .02em .04em rgba(15,8,3,.85),0 .06em .16em rgba(15,8,3,.72),0 .14em .42em rgba(15,8,3,.5)}
.wfen__t span{display:block}
.wfen__t em{font-style:normal;color:#f3cd94}
.wfen__k{margin:clamp(16px,1.8vw,26px) auto 0;max-width:46ch;font-family:'Gelasio Blatt',var(--serif);font-weight:500;font-size:clamp(1.14rem,1.7vw,1.7rem);line-height:1.4;color:#fff;
  text-shadow:0 1px 2px rgba(15,8,3,.92),0 2px 10px rgba(15,8,3,.8)}
.wfen__z,.wfen__t span,.wfen__k{opacity:0;transform:translateY(34px);transition:opacity 1.3s cubic-bezier(.16,1,.3,1),transform 1.7s cubic-bezier(.16,1,.3,1)}
.wfen__t span:nth-child(1){transition-delay:.12s}.wfen__t span:nth-child(2){transition-delay:.24s}.wfen__k{transition-delay:.42s}
.wfen.da .wfen__z,.wfen.da .wfen__t span,.wfen.da .wfen__k{opacity:1;transform:none}
#handschrift,#material{border-radius:var(--rund)}
@media(max-width:860px){.wfen{min-height:62svh}}
@media (prefers-reduced-motion:reduce){.wfen__z,.wfen__t span,.wfen__k{opacity:1;transform:none;transition:none}}

/* ---------- «Was noch dazukommt» als Tafel (fenster_ausblick.py): Wandholz mit Butzenscheiben, doppelter Goldrand,
   oben ein Foto des Hauses und der nächste Schritt, darunter die offenen Punkte als Spalten ---------- */
.ab .kopfzeile{margin-bottom:clamp(44px,5vw,84px)}
.ab-tafel{position:relative;border-radius:clamp(26px,2.6vw,38px);padding:clamp(30px,4.4vw,76px) clamp(22px,4.4vw,76px) clamp(26px,3.6vw,60px);color:#fbf5ea;
  background:var(--blau) var(--muster) 50% 0/var(--musterb) auto;
  box-shadow:inset 0 1px 0 rgba(255,236,200,.12),0 0 0 1px rgba(125,79,39,.6),0 70px 90px -56px rgba(31,18,9,.9),0 26px 40px -30px rgba(31,18,9,.55)}
.ab-tafel::before,.ab-tafel::after{content:"";position:absolute;pointer-events:none;border:1px solid rgba(201,133,67,.5);border-radius:clamp(16px,1.8vw,26px);inset:clamp(10px,1.1vw,16px)}
.ab-tafel::after{inset:clamp(15px,1.5vw,22px);border-color:rgba(201,133,67,.22);border-radius:clamp(12px,1.5vw,21px)}
.ab [data-a="heben"]{opacity:1;transform:translate3d(0,120px,0) scale(.974);transform-origin:50% 100%;transition:transform 2.2s cubic-bezier(.16,1,.3,1)}
.ab [data-a="heben"].da{transform:none}
.ab-oben{display:grid;gap:clamp(28px,4.4vw,84px);align-items:center}
@media(min-width:900px){.ab-oben{grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr)}}
.ab-bild{margin:0;border-radius:clamp(16px,1.7vw,24px);overflow:hidden;aspect-ratio:1.22;background:var(--tief);
  box-shadow:0 0 0 1px rgba(201,133,67,.55),0 0 0 7px rgba(42,24,10,.92),0 0 0 8px rgba(201,133,67,.28),0 40px 50px -30px rgba(0,0,0,.95)}
.ab-bild img{display:block;width:100%;height:100%;object-fit:cover}
@media (hover:hover){.ab-bild img{transition:transform 2.2s cubic-bezier(.16,1,.3,1)}.ab-bild:hover img{transform:scale(1.05);transition-duration:2.8s}}
.ab-z{display:block;width:clamp(46px,4.2vw,66px);height:auto;color:#ef7649;fill:currentColor;margin-bottom:clamp(16px,1.8vw,26px)}
.ab-schritt small{display:block;font-family:var(--mono);font-size:clamp(11.5px,.86vw,13px);letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}
.ab-schritt h3{margin:clamp(12px,1.3vw,20px) 0 0;font-family:var(--serif);font-weight:700;font-size:clamp(2.3rem,4.2vw,4.4rem);line-height:1.02;color:#fbf5ea}
.ab-linie{display:block;width:clamp(56px,5vw,84px);height:2px;margin:clamp(20px,2.2vw,32px) 0;background:linear-gradient(90deg,#c98543,rgba(201,133,67,0))}
.ab-schritt p{margin:0;max-width:46ch;font-size:clamp(1.02rem,1.12vw,1.14rem);line-height:1.66;color:rgba(251,245,234,.86)}
.ab-trenn{display:flex;align-items:center;justify-content:center;gap:16px;margin:clamp(34px,4.4vw,72px) 0 clamp(8px,1vw,16px)}
.ab-trenn i{flex:1;height:1px;background:linear-gradient(90deg,rgba(201,133,67,0),rgba(201,133,67,.55))}
.ab-trenn i:last-child{background:linear-gradient(90deg,rgba(201,133,67,.55),rgba(201,133,67,0))}
.ab-trenn b{width:9px;height:9px;border-radius:50%;border:1px solid #c98543}
.ab-liste{list-style:none;margin:0;padding:0;display:grid}
.ab-liste li{padding:clamp(24px,2.6vw,40px) 0}
.ab-liste li+li{border-top:1px solid rgba(201,133,67,.2)}
.ab-liste h3{margin:0;font-family:var(--serif);font-weight:700;font-size:clamp(1.4rem,1.76vw,1.76rem);line-height:1.16;color:#f3cd94}
.ab-liste h3::after{content:"";display:block;width:34px;height:2px;margin:14px 0 14px;background:linear-gradient(90deg,#c98543,rgba(201,133,67,0))}
.ab-liste p{margin:0;max-width:52ch;font-size:clamp(.98rem,1.04vw,1.06rem);line-height:1.66;color:rgba(251,245,234,.8)}
@media(min-width:760px){
  .ab-liste{grid-template-columns:repeat(2,minmax(0,1fr))}
  .ab-liste li{padding-inline:clamp(20px,2.8vw,48px)}
  .ab-liste li:nth-child(2n+1){padding-inline-start:0}.ab-liste li:nth-child(2n){padding-inline-end:0;border-inline-start:1px solid rgba(201,133,67,.2)}
  .ab-liste li:nth-child(2){border-top:0}
}
@media(min-width:1140px){
  .ab-liste--3{grid-template-columns:repeat(3,minmax(0,1fr))}
  .ab-liste--3 li:nth-child(n){padding-inline:clamp(24px,2.8vw,48px);border-top:0;border-inline-start:1px solid rgba(201,133,67,.2)}
  .ab-liste--3 li:first-child{padding-inline-start:0;border-inline-start:0}.ab-liste--3 li:last-child{padding-inline-end:0}
}
@media (prefers-reduced-motion:reduce){.ab [data-a="heben"]{transform:none;transition:none}.ab-bild img{transition:none;transform:none!important}}
'''
