#!/usr/bin/env python3
"""Werkbank Culinarium (Vorlage Schäfli, dort Ruedihus), Abschnitt Instagram (12.10.2026, Master 5b Punkt 16): das Handy als Gerät aus Blender in der Mitte,
ringsum acht Beiträge als Polaroids: Teller, Plakate und Gläser aus dem Feed «Momo x Rudi» (Culinarium, 28.10.2026).

Bauart des Handys wie beim Grand Beau-Rivage (frontales Gehäuse, der Bildschirm ist ein Rechteck): das Gehäuse hat ein Loch, der Feed liegt als
Bild darunter. Ein Klick auf den Bildschirm lädt die echte Feed-Seite in dieselbe Fläche, danach scrollt das Rad im Feed; ein kleiner Hinweis
steht darunter. Gehäuse geraete/handy-geraet.png + handy.json (übernommen), Bildschirm geraete/schirm-feed.png (node _werkbank/geraete/schirme.js feed).
Die acht Beiträge kommen klein aus feed/posts/ nach werkbank/eigen/ (der Kit-Bau leert nur img/).
Eingehängt am Ende von haus.py über H.EIGENE (key 'feed' ersetzt den Kit-Abschnitt)."""
import json, os

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
G = os.path.join(W, 'geraete')
_LJ = os.path.join(G, 'handy.json')
LAGE = json.load(open(_LJ)) if os.path.exists(_LJ) else None
BEREIT = bool(LAGE) and all(os.path.exists(os.path.join(G, f)) for f in ('handy-geraet.png', 'schirm-feed-sb.png'))
BILDER = [('feed-geraet', os.path.join(G, 'handy-geraet.png'), 4000, dict(q=88)), ('feed-schirm', os.path.join(G, 'schirm-feed-sb.png'), 900, dict(q=84))] if BEREIT else []

# Beitrag (Nummer in feed/posts), Bildzeile, Drehung, Wandern beim Scrollen. Vier links, vier rechts; je Seite zwei Reihen.
# 17.10.2026: Feed «Stube für Stube, Zimmer für Zimmer» (feed_daten.py, 27 Beiträge, nur echte Fotos). Die Räume tragen ihren Namen im Bild,
# deshalb steht darunter, was man dort findet.
# Feed «Ein Horizont» des Feed-Planers (19.10.2026, 21 Beiträge, nur echte Fotos); Auswahl laut seiner Meldung, Bildzeilen von mir
POLAROIDS = [(15, 'Blumenkohl mit Kürbis', -3, '0'), (37, 'Ein Abend an der Tafel', 3, '0'), (18, 'Plakat, Juli 2024', -2, '0'), (53, 'Du erzählst, er mixt', 3, '0'),
             (20, 'Durchs Sieb, ins Glas', -3, '0'), (31, 'Am Pass', 2, '0'), (52, 'Momo hinter der Bar', -2, '0'), (59, 'Kurz vor dem ersten Gang', 3, '0')]   # neuer Feed mit 60 Beiträgen (29.10.2026): die stärksten, jeder von anderer Art
BLAETTER = set()   # keine Zettel mehr, nur Fotos
ORTE = [(1, 6), (20.5, 0), (3.5, 52), (22, 47), (62, 2), (80.5, 7), (63.5, 49), (81.5, 54)]   # links, oben in Prozent der Bühne
HINWEIS = 'Auf den Bildschirm klicken und durch den Feed scrollen'


def bilder():
    """Die acht Beiträge klein nach werkbank/eigen/ (360 breit), nur wenn sie fehlen oder der Beitrag neuer ist."""
    from PIL import Image
    z = os.path.join(ROOT, 'werkbank', 'eigen')
    os.makedirs(z, exist_ok=True)
    for nr, *_ in POLAROIDS:
        q, ziel = os.path.join(ROOT, 'feed', 'posts', f'{nr:02d}.jpg'), os.path.join(z, f'fpo-{nr:02d}.webp')
        if os.path.exists(q) and (not os.path.exists(ziel) or os.path.getmtime(ziel) < os.path.getmtime(q)):
            Image.open(q).convert('RGB').resize((360, 450), Image.LANCZOS).save(ziel, 'WEBP', quality=82, method=6)


def abschnitt(g):
    """EIGENE-Eintrag für haus.py. g = globals() von haus.py (FEED)."""
    FD = g['FEED']

    def bau(k):
        kn, e, m = k['kn'], k['e'], k['m']
        gw, gh = m['feed-geraet']; sw, sh = m['feed-schirm']
        x, y, b, h_ = LAGE['schirm']
        handy = (f'<div class="fb-h" data-a="schweb" style="--i:0"><div class="fb-h__b" style="aspect-ratio:{gw}/{gh}">'
                 f'<img class="ld frei fb-h__g" src="img/feed-geraet.webp" width="{gw}" height="{gh}" alt="Das Instagram-Profil von Culinarium als Idee, auf einem Handy" loading="lazy" decoding="async">'
                 f'<img class="ld fb-h__s" src="img/feed-schirm.webp" width="{sw}" height="{sh}" alt="" loading="lazy" decoding="async" style="left:{x * 100:.3f}%;top:{y * 100:.3f}%;width:{b * 100:.3f}%;height:{h_ * 100:.3f}%">'
                 f'<div class="fb-h__e" style="left:{x * 100:.3f}%;top:{y * 100:.3f}%;width:{b * 100:.3f}%;height:{h_ * 100:.3f}%">'
                 '<span class="fb-h__k"><span class="a">Zum Scrollen klicken</span><span class="b">Wird geöffnet …</span><i><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 3.5v14.2l3.9-3.2 2.7 6 2.3-1-2.7-5.9 5.3-.4z"/></svg></i></span>'
                 '</div></div></div>')
        pola = ''.join(
            f'<figure class="fb-p fb-p--{"b" if nr in BLAETTER else "f"}" data-a="schweb" data-drift="{dr}" style="left:{lx}%;top:{ly}%;--i:{n + 1};--r:{r}deg;--r0:{r * 3}deg">'
            f'<img src="eigen/fpo-{nr:02d}.webp" width="360" height="450" alt="" loading="lazy" decoding="async"><figcaption>{e(name)}</figcaption></figure>'
            for n, ((nr, name, r, dr), (lx, ly)) in enumerate(zip(POLAROIDS, ORTE)))
        js = '''<script>(function(){var h=document.querySelector('#feed .fb-h');if(!h||!matchMedia('(hover:hover) and (pointer:fine)').matches)return;
var e=h.querySelector('.fb-h__e'),f=null,warte=0;
function mass(){if(f){var k=e.clientWidth/393;f.style.height=(e.clientHeight/k).toFixed(2)+'px';f.style.transform='scale('+k.toFixed(5)+')'}}
function weg(){clearTimeout(warte);if(f){f.remove();f=null}e.classList.remove('live','laedt');document.documentElement.classList.remove('lap-ruhe')}
function zeig(x){if(x!==f||x.classList.contains('da'))return;clearTimeout(warte);x.classList.add('da');e.classList.remove('laedt');e.classList.add('live')}
/* Robert 18.10.2026 «dauert sehr lange»: der Feed lädt unsichtbar vor, sobald das Kapitel näherkommt; der Klick zeigt ihn sofort (wie Doldenhorn) */
function baue(){if(f)return f;var x=document.createElement('iframe');x.title='Instagram-Feed des Hauses als Idee';x.tabIndex=-1;
x.onload=function(){try{var d=x.contentDocument,st=d.createElement('style');
st.textContent='html,body{margin:0!important;padding:0!important;overflow:hidden!important;background:#000!important}.wer,.u,.zurueck,.kap{display:none!important}.stage{display:block!important;padding:0!important;margin:0!important;min-height:0!important}.devwrap{animation:none!important;opacity:1!important;transform:none!important;position:fixed!important;left:0!important;top:0!important;margin:0!important}#device{width:393px!important;height:100vh!important;padding:0!important;margin:0!important;border-radius:0!important;box-shadow:none!important;border:0!important}.screen{border-radius:0!important}.island{display:none!important}';
d.head.appendChild(st)}catch(q){}x.__ok=1;if(e.classList.contains('laedt'))setTimeout(function(){zeig(x)},80)};
f=x;x.src='../feed/index.html';e.appendChild(x);mass();return x}
function live(){var x=baue();e.classList.add('laedt');document.documentElement.classList.add('lap-ruhe');if(x.__ok)zeig(x);else{clearTimeout(warte);warte=setTimeout(function(){zeig(x)},9000)}}
e.addEventListener('click',function(){if(!f||!f.classList.contains('da'))live()});addEventListener('resize',mass);
new IntersectionObserver(function(E){if(E[0].isIntersecting)baue();else weg()},{rootMargin:'120% 0px 120% 0px'}).observe(h)})();</script>'''
        return f'''
<section class="fl {k['fl']} blatt fb" id="feed">
  <div class="in">
    {k['kopf']()}
    <div class="fb-b" aria-hidden="true">{pola}{handy}</div>
    <p class="fb-hin">{e(HINWEIS)}</p>
    <div class="fb-t">
      {''.join(f'<div class="lauf"><p data-a="worte">{t}</p></div>' for t in (FD['text1'], FD['text2']) if t.strip())}
    </div>
    <div class="kn-reihe" data-a="auf" style="margin-top:clamp(26px,3vw,44px);justify-content:center">{kn('Feed ansehen', '../feed/index.html', neu=True)}</div>
  </div>
  {js}
</section>'''
    return dict(key='feedbuehne', nach='papier', name='Instagram', zeilen=['Ein Feed,', 'der nach Abend aussieht.'], text='', bau=bau)


def _css():
    if not BEREIT:
        return ''
    g = LAGE['gehaeuse']                      # Gehäuse im Bild (links, oben, Breite, Höhe als Anteil des Bildes)
    bw, bh = LAGE['groesse']
    breite = 24 / g[2]                        # das Gehäuse selbst (ohne Schattenrand) steht 24 % der Bühne breit, mittig
    links = 50 - breite * (g[0] + g[2] / 2)
    hb = 62 / g[2]
    ho, hu = -hb * (bh / bw) * g[1] * .55, -hb * (bh / bw) * (1 - g[1] - g[3]) * .6
    return f'''
/* ---------- Instagram: Handy als Gerät aus Blender in der Mitte, acht Beiträge als Polaroids ringsum (feed_buehne.py, 12.10.2026, Auswahl 17.10.2026) ---------- */
.fb .kopfzeile{{margin-bottom:clamp(30px,3.6vw,60px)}}
.fb-b{{position:relative;max-width:1320px;margin:0 auto;aspect-ratio:1320/735}}
.fb-h{{position:absolute;left:{links:.2f}%;top:-3%;width:{breite:.2f}%;z-index:2}}
.fb-h__b{{position:relative;width:100%}}
.fb-h img{{position:absolute;display:block;max-width:none;filter:none}}
.fb-h .fb-h__g{{left:0;top:0;width:100%;height:auto;z-index:2;pointer-events:none}}
.fb-h .fb-h__s{{z-index:1;object-fit:cover}}
.fb-h__e{{position:absolute;z-index:1;overflow:hidden;border-radius:4.5% / 2.1%}}
.fb-h__e iframe{{position:absolute;left:0;top:0;width:393px;height:851px;max-width:none;border:0;background:#000;transform-origin:0 0;opacity:0;pointer-events:none;z-index:3;transition:opacity .3s linear}}
.fb-h__e iframe.da{{opacity:1;pointer-events:auto}}
.fb-h__k{{display:none}}
.fb-p{{position:absolute;width:16.5%;margin:0;padding:0;background:none;border-radius:14px;overflow:hidden;box-shadow:0 1px 1px rgba(0,0,0,.3),0 30px 40px -22px rgba(0,0,0,.85),0 10px 16px -10px rgba(0,0,0,.5);z-index:1}}
.fb-p img{{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover}}
.fb-p figcaption{{display:none;padding:.62em 0 .7em;text-align:center;font-family:var(--serif);font-weight:700;font-size:clamp(.72rem,1vw,1rem);line-height:1.2;color:#2a1a0e;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.fb-hin{{display:none;margin:clamp(10px,1.2vw,18px) auto 0;text-align:center;font-family:var(--mono);font-size:11px;letter-spacing:.14em;line-height:1.5;text-transform:uppercase;color:var(--gold);z-index:3}}
.fb-t{{display:grid;gap:clamp(18px,3vw,56px);max-width:1080px;margin:clamp(34px,4vw,64px) auto 0}}
.fb-t .lauf{{max-width:none;margin:0}}
@media(min-width:860px){{.fb-t{{grid-template-columns:1fr 1fr}}}}
/* Gestaltung 28.10.2026: steht nur ein Satz da, sitzt er mittig über dem Knopf statt allein in der rechten Spalte */
.fb-t:has(>.lauf:only-child){{grid-template-columns:1fr;max-width:640px;text-align:center}}
@media(hover:hover) and (pointer:fine) and (min-width:701px){{
  .fb-hin{{display:block}}
  .fb-h__e{{cursor:pointer}}.fb-h__e.laedt{{cursor:progress}}.fb-h__e.live{{cursor:auto}}
  .fb-h__k{{position:absolute;left:50%;bottom:9.5%;z-index:2;transform:translateX(-50%);display:flex;align-items:center;gap:8px;padding:3px 3px 3px 13px;border-radius:999px;pointer-events:none;
    font-family:var(--mono);font-size:.56rem;letter-spacing:.14em;text-transform:uppercase;line-height:1;white-space:nowrap;color:var(--tinte);
    background:linear-gradient(180deg,#fbfcfe 0%,#d0dae7 100%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.9),inset 0 -1px 0 rgba(15,54,120,.35),0 0 0 1px rgba(162,182,207,.8),0 12px 22px -8px rgba(0,0,0,.8),0 3px 8px rgba(0,0,0,.4);transition:opacity .3s}}
  .fb-h__k i{{flex:none;width:24px;height:24px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,#1d4f9e 0%,#0b1d3d 100%);box-shadow:inset 0 1px 0 rgba(255,236,200,.2)}}
  .fb-h__k svg{{width:12px;height:12px;fill:none;stroke:#e7ecf3;stroke-width:1.7;stroke-linejoin:round}}
  .fb-h__k .b{{display:none}}.fb-h__e.laedt .fb-h__k .a{{display:none}}.fb-h__e.laedt .fb-h__k .b{{display:inline}}
  .fb-h__e.live .fb-h__k{{opacity:0}}
}}
@media(max-width:700px){{
  .fb-b{{aspect-ratio:auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px 10px}}
  .fb-h{{position:relative;left:auto;top:auto;grid-column:1/-1;order:-1;width:{hb:.2f}%;margin:{ho:.2f}% auto {hu:.2f}%}}
  .fb-p{{position:relative;left:auto!important;top:auto!important;width:100%;padding:4% 4% 0}}
  .fb-p{{padding:0}}.fb-p figcaption{{display:none}}
}}
'''


CSS = _css()
