#!/usr/bin/env python3
"""Culinarium Hannover · Station 06 Konzepter · Konzept-Board (26.10.2026).
Baut bilder/*.webp, konzept.html und konzept.json aus inhalt.py. Machart nach dem Board des Schäfli (_kette/06-konzepter/_bau/bau.py),
Farben vorläufig aus den Plakaten (Markenbuch Station 05 fehlt), Akzent aus den Fotos gemessen (Kerzenlicht in 4004, 3887, 3858).
Aufruf: python3 _bau/bau.py"""
import html, json, os, sys
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
PAKET = os.path.dirname(HIER)
PROJ = os.path.abspath(os.path.join(PAKET, '..', '..'))
sys.path.insert(0, HIER)
from inhalt import B, F, HAEUSER, GESCHICHTE_SATZ, GESCHICHTE, WEGE, IDEEN, SZENEN, UEBERLEITUNG, SEITEN, GESTRICHEN, OFFEN  # noqa: E402

E = html.escape
ZUM_PROJEKT = '../../'
GROSS = ('momo', 'rudi', 'glas', 'teller', 'pass', 'trio')


# ---------------------------------------------------------------- Bilder
def bild(k):
    quelle = B[k][0]
    breit = 2000 if k in GROSS else 1200
    ziel = os.path.join(PAKET, 'bilder', k + '.webp')
    if not os.path.exists(ziel):
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        im = Image.open(os.path.join(PROJ, quelle))
        im.draft('RGB', (breit, breit * 2))
        im = im.convert('RGB')
        if im.width > breit:
            im = im.resize((breit, round(im.height * breit / im.width)), Image.LANCZOS)
        im.save(ziel, 'WEBP', quality=80, method=6)
    return 'bilder/%s.webp' % k


for _k in B:
    bild(_k)


def film(k):
    return ZUM_PROJEKT + F[k][0]


ZEICHEN = open(os.path.join(PAKET, 'assets', 'zeichen.svg'), encoding='utf-8').read()
ZEICHEN = ZEICHEN[ZEICHEN.index('<svg'):].replace('<svg ', '<svg class="z" aria-hidden="true" ', 1)
PFEIL = '<svg class="pf" viewBox="0 0 22 10"><path d="M0 5h20M16 1l4 4-4 4"/></svg>'


# ---------------------------------------------------------------- Bühne: Skizze mit echten Bildern, Masse in Hundertsteln der Breite (cqw)
def pos(x, y, w, h=None):
    s = 'left:%.2fcqw;top:%.2fcqw;width:%.2fcqw' % (x, y, w)
    return s + (';height:%.2fcqw' % h if h is not None else '')


def bandhtml(t1, t2, cls=''):
    return '<span class="band-in"><b>%s</b><small>%s</small></span>' % (E(t1), E(t2))


def buehne(st, teil):
    if not st:
        return ''
    if st.get('fenster'):
        return ('<div class="fenster" data-a><img src="%s" alt="" decoding="async"><p class="fsatz schlitz" data-a><span>%s</span></p></div>'
                % (bild(st['fenster']), E(st['satz'])))
    teile, paar = [], 0
    for el in st['el']:
        art = el[0]
        if art == 'bild':
            _, k, x, y, w, h, op = el
            paar += 1
            teile.append('<figure class="b-bild" data-p="%d" style="%s"><img src="%s" alt="" decoding="async" style="object-position:%s"></figure>'
                         % (paar, pos(x, y, w, h), bild(k), op))
        elif art == 'film':
            _, k, x, y, w, h = el
            paar += 1
            teile.append('<figure class="b-bild b-film" data-p="%d" style="%s"><video muted playsinline preload="metadata" src="%s#t=0.1"></video>'
                         '<span class="spiel">Film · %d s</span></figure>' % (paar, pos(x, y, w, h), E(film(k)), F[k][3]))
        elif art == 'band':
            _, t1, t2, x, y, w = el
            teile.append('<p class="b-band" data-a style="%s">%s</p>' % (pos(x, y, w), bandhtml(t1, t2)))
        elif art == 'text':
            _, t, x, y, w, cls = el
            inner = '<span>%s</span>' % E(t)
            teile.append('<p class="b-text b-%s%s" data-a style="%s">%s</p>' % (cls, ' schlitz' if cls == 'ort' else '', pos(x, y, w), inner))
        elif art == 'knopf':
            _, t, x, y = el
            teile.append('<span class="knopf b-knopf" data-a style="left:%.2fcqw;top:%.2fcqw">%s %s</span>' % (x, y, E(t), PFEIL))
        elif art == 'worte':
            _, worte, x, y, w = el
            li = ''.join('<li class="schlitz%s" data-a><span>%s</span></li>' % (' an' if i == 0 else '', E(t)) for i, t in enumerate(worte))
            teile.append('<ul class="b-worte" style="%s">%s</ul>' % (pos(x, y, w), li))
        elif art == 'tafel':
            _, oben, unten, satz = el
            bw = 100 / len(oben)
            for reihe, ks, y in ((0, oben, 0), (1, unten, 29)):
                for i, k in enumerate(ks):
                    teile.append('<figure class="b-bild b-platz" data-flaeche style="%s"><img src="%s" alt="" decoding="async"></figure>' % (pos(i * bw, y, bw, 23), bild(k)))
            teile.append('<p class="b-tisch" data-a style="%s"><span>%s</span></p>' % (pos(0, 23, 100, 6), E(satz)))
    return '<div class="buehne-hulle"><div class="buehne" style="height:%.2fcqw">%s</div></div>' % (st['h'], ''.join(teile))


FLAECHE = {'bild': ('matt', 'Foto als Fenster'), 'hell': ('hell', 'Hell, Warmweiss der Plakate'), 'tapete': ('tapete', 'Hell mit Tapete aus dem Rahmen der Wortmarke'),
           'dunkel': ('dunkel', 'Dunkel, Schiefer-Violett der Plakate'), 'matt': ('matt', 'Matt, Platz gehalten'),
           'dc': ('dc', 'Farbe von Dirty Chicken (vorläufig, offen)')}


def link(haus):
    u = HAEUSER.get(haus)
    return ('<a href="%s" target="_blank" rel="noopener">%s</a>' % (E(u), E(haus))) if u else E(haus)


def szene(s):
    cls, fl = FLAECHE[s['flaeche']]
    bisher = ''.join('<li><span class="haus">%s</span><span>%s</span></li>' % (link(h), E(t)) for h, t in s['bisher'].items())
    dateien = [B[k][0].split('/')[-1] for k in s['bilder']] + [F[k][0].split('/')[-1] for k in s.get('filme', [])]
    bilder = ''.join('<li>%s</li>' % E(d) for d in dateien) or '<li>keine Bilder</li>'
    skizze = ('<div class="skizze" data-a><h4>Skizze und Zweifel</h4><p>%s</p></div>' % E(s['skizze'])) if s.get('skizze') else ''
    ueber = UEBERLEITUNG.get(s['teil'])
    ueber_html = ('<div class="ueber"><i></i><p>%s</p></div>' % E(ueber)) if ueber else ''
    return '''
<section class="szene %(cls)s" id="%(teil)s">
 <div class="innen">
  <header class="skopf">%(z)s
   <p class="mono steil">%(teil)s</p>
   <h2 class="schlitz" data-a><span>%(titel)s</span></h2>
   <p class="ssatz">%(satz)s</p>
  </header>
  %(buehne)s
  <div class="drei">
   <div class="frage" data-a><h4>Einfall aus dem Haus</h4><p>%(einfall)s</p></div>
   <div class="frage" data-a><h4>Komposition</h4><p>%(komposition)s</p></div>
   <div class="frage" data-a><h4>Moment</h4><p>%(moment)s</p></div>
  </div>
  %(skizze)s
  <div class="steck">
   <div><h4>Baustein</h4><p><b class="bs">%(baustein)s</b> <span class="quelle q-%(quelle)s">%(qname)s</span></p></div>
   <div><h4>Bewegung</h4><p>%(bewegung)s</p></div>
   <div><h4>Fläche</h4><p><i class="chip chip--%(cls)s"></i>%(fl)s</p></div>
   <div class="bilder"><h4>Bilder aus _quelle</h4><ul>%(bilder)s</ul></div>
  </div>
  <div class="vergleich">
   <div class="dieses"><h4>Dieses Haus</h4><p>%(unterschied)s</p></div>
   <div class="bisher"><h4>Bisherige Häuser an dieser Stelle</h4><ul>%(bisher)s</ul></div>
  </div>
 </div>
 %(ueber)s
</section>''' % dict(cls=cls, teil=s['teil'], z=ZEICHEN, titel=E(s['titel']), satz=E(s['satz']), buehne=buehne(s.get('stage'), s['teil']),
                     einfall=E(s['einfall']), komposition=E(s['komposition']), moment=E(s['moment']), skizze=skizze,
                     baustein=E(s['baustein']), quelle=s['quelle'], qname='aus dem Fundus' if s['quelle'] == 'fundus' else 'neu',
                     bewegung=E(s['bewegung']), fl=E(fl), bilder=bilder, unterschied=E(s['unterschied']), bisher=bisher, ueber=ueber_html)


def kopf():
    wege = ''.join(
        '<article class="weg%s" data-a><div class="weg-bilder">%s</div><div class="weg-text"><p class="mono">%s</p><h3>%s</h3><p>%s</p></div></article>' % (
            ' weg--an' if a == 'Empfohlen' else '', ''.join('<img src="%s" alt="" decoding="async">' % bild(k) for k in ks), E(a), E(t), E(x))
        for a, t, x, ks in WEGE)
    ideen = ''.join('<div class="idee" data-a><p class="mono">%s</p><h3>%s</h3><p>%s</p></div>' % (E(a), E(b), E(c)) for a, b, c in IDEEN)
    inhalt = ''.join('<a href="#%s">%s</a>' % (s['teil'], E(s['titel'])) for s in SZENEN)
    return '''
<header class="kopf-board dunkel">
 <div class="innen">
  <p class="mono kz">Konzept-Board · Station 06 · intern · 26. Oktober 2026</p>
  <p class="b-band kopf-band" data-a>%s</p>
  <p class="geschichte" data-a>%s</p>
  <p class="geschichte2" data-a>%s</p>
 </div>
</header>
<section class="szene hell" id="wege">
 <div class="innen">
  <header class="skopf">%s<p class="mono steil">Wie die Konzepte und die Menschen auf die Seite kommen</p><h2 class="schlitz" data-a><span>Drei Wege, einer davon trägt.</span></h2></header>
  <div class="wege">%s</div>
 </div>
</section>
<section class="szene tapete ideen-teil">
 <div class="innen">
  <header class="skopf">%s<p class="mono steil">Was es bei Tasty Studios noch nicht gab</p><h2 class="schlitz" data-a><span>Alles kommt als Paar.</span></h2></header>
  <div class="ideen">%s</div>
  <nav class="inhalt"><p class="mono">Das Drehbuch der Startseite, Gang für Gang</p>%s</nav>
 </div>
</section>''' % (bandhtml('CULINARIUM', 'A unique experience by Momo x Rudi'), E(GESCHICHTE_SATZ), E(GESCHICHTE), ZEICHEN, wege, ZEICHEN, ideen, inhalt)


def unterseiten():
    rows = []
    for s in SEITEN:
        sz = ''.join('<li><span class="mono">%s</span><span>%s</span>%s</li>' % (
            E(t), E(x), ''.join('<img src="%s" alt="" decoding="async">' % bild(b) for b in bs)) for t, x, bs in s['szenen'])
        rows.append('<div class="useite" data-a><h3>%s</h3><p class="mono">%s</p><ul>%s</ul></div>' % (E(s['titel']), E(s['seite']), sz))
    return '''
<section class="szene matt" id="unterseiten"><div class="innen">
 <header class="skopf">%s<h2 class="schlitz" data-a><span>Unterseiten, kürzer erzählt.</span></h2>
 <p class="ssatz">Heute gibt es keine Seite, nur Instagram. Was ein Gast braucht, kommt dazu: der Abend mit Menü und Buchung, alle bisherigen Abende, die Leute, Dirty Chicken, der Weg zur Bar und die Rechtstexte. Jede Unterseite beginnt mit einem Paar wie die Startseite, mit anderen Bildern.</p></header>
 <div class="useiten">%s</div>
</div></section>''' % (ZEICHEN, ''.join(rows))


def liste(titel, satz, items, cls, id_):
    li = ''.join('<li><b>%s</b><span>%s</span></li>' % (E(a), E(b)) for a, b in items)
    return '''<section class="szene %s" id="%s"><div class="innen">
 <header class="skopf">%s<h2 class="schlitz" data-a><span>%s</span></h2><p class="ssatz">%s</p></header>
 <ul class="zliste">%s</ul></div></section>''' % (cls, id_, ZEICHEN, E(titel), E(satz), li)


TAPETE = ('data:image/svg+xml,' + '%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2788%27 height=%2788%27%3E'
          '%3Crect x=%2724%27 y=%2724%27 width=%2740%27 height=%2740%27 fill=%27none%27 stroke=%27%233A3845%27 stroke-opacity=%27.09%27 stroke-width=%271.4%27/%3E'
          '%3Crect x=%2729%27 y=%2729%27 width=%2730%27 height=%2730%27 fill=%27none%27 stroke=%27%233A3845%27 stroke-opacity=%27.07%27 stroke-width=%27.8%27/%3E%3C/svg%3E')

CSS = r'''
@font-face{font-family:'Fraunces';src:url(assets/fonts/fraunces-var.woff2) format('woff2');font-weight:100 900;font-display:swap}
@font-face{font-family:'Instrument Sans';src:url(assets/fonts/InstrumentSans-normal-400_600.woff2) format('woff2');font-weight:400 600;font-display:swap}
@font-face{font-family:'DM Mono';src:url(assets/fonts/DMMono-normal-400.woff2) format('woff2');font-weight:400;font-display:swap}
:root{--nacht:#24232D;--tief:#2E2C39;--schiefer:#3A3845;--weiss:#FAF4F4;--weiss2:#EFE6E2;--tinte:#2A2833;--licht:#CF7233;--licht-h:#E9A26C;--licht-t:#9A4E1E;
 --dc:#EFE4CF;--dc-tinte:#2F3A22;
 --titel:'Fraunces',Georgia,serif;--lauf:'Instrument Sans',system-ui,sans-serif;--mono:'DM Mono',ui-monospace,Menlo,monospace;
 --rand:clamp(16px,5vw,64px);--e1:cubic-bezier(.16,1,.3,1);--rund:clamp(22px,2.6vw,34px)}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--weiss);color:var(--tinte);font:400 16.5px/1.62 var(--lauf);-webkit-font-smoothing:antialiased;overflow-x:hidden}
img,video{display:block;max-width:100%}a{color:inherit}
.innen{max-width:1240px;margin:0 auto;padding:0 var(--rand)}
.mono{font-family:var(--mono);font-size:11.5px;letter-spacing:.17em;text-transform:uppercase}
.dunkel{background:var(--schiefer);color:#F3EEEE}
.hell{background:var(--weiss)}
.tapete{background-color:var(--weiss);background-image:url("TAPETE");background-size:88px}
.matt{background:var(--weiss2)}
.dc{background:var(--dc);color:var(--dc-tinte)}
.szene{position:relative;border-radius:var(--rund) var(--rund) 0 0;margin-top:calc(var(--rund)*-1);padding:clamp(64px,8vw,112px) 0 clamp(72px,8vw,112px)}
/* Band aus den Plakaten: warmweiss, doppelt gerahmt */
.b-band,.kopf-band{margin:0;background:var(--weiss);color:var(--schiefer);text-align:center;padding:1.1cqw 1.4cqw;
 box-shadow:inset 0 0 0 2px var(--schiefer),inset 0 0 0 5px var(--weiss),inset 0 0 0 6px var(--schiefer),0 26px 40px -26px rgba(16,14,22,.7);z-index:5}
.band-in{display:block}
.band-in b{display:block;font:560 clamp(13px,3.1cqw,44px)/1 var(--titel);letter-spacing:.11em;font-variation-settings:'SOFT' 100,'WONK' 1}
.band-in small{display:block;font:500 clamp(8px,.9cqw,12px)/1.2 var(--lauf);letter-spacing:.2em;text-transform:uppercase;margin-top:.7cqw}
.kopf-band{display:inline-block;padding:22px 34px;margin:24px auto 34px}
.kopf-band .band-in b{font-size:clamp(2.2rem,6vw,4.6rem)}
.kopf-band .band-in small{font-size:12px;margin-top:10px}
/* Kopf */
.kopf-board{padding:clamp(80px,11vw,150px) 0 clamp(110px,12vw,170px);text-align:center;border-radius:0}
.kopf-board .kz{color:var(--licht-h)}
.geschichte{font:420 clamp(1.3rem,2.5vw,2rem)/1.36 var(--titel);max-width:38ch;margin:0 auto;color:#F6F0F0;text-wrap:balance}
.geschichte2{max-width:66ch;margin:26px auto 0;opacity:.84}
/* Szenen-Kopf */
.skopf{margin-bottom:clamp(28px,4vw,48px)}
.skopf .z{width:40px;height:auto;color:var(--licht);fill:currentColor;display:block;margin-bottom:14px}
.steil{color:var(--licht-t);margin:0 0 8px}.dunkel .steil{color:var(--licht-h)}
.skopf h2{font:460 clamp(1.9rem,3.8vw,3.3rem)/1.08 var(--titel);margin:0;color:var(--schiefer);max-width:26ch;font-variation-settings:'SOFT' 100}
.dunkel .skopf h2{color:#F6F0F0}.dc .skopf h2{color:var(--dc-tinte)}
.ssatz{max-width:70ch;margin:14px 0 0;opacity:.88}
.schlitz{overflow:hidden}.schlitz>span{display:inline-block}
.js .schlitz[data-a]>span{transform:translateY(108%);transition:transform 1.1s var(--e1)}
.js .schlitz[data-a].da>span{transform:none}
.js [data-a]:not(.schlitz){transform:translateY(46px);transition:transform 1.3s var(--e1)}
.js [data-a]:not(.schlitz).da{transform:none}
/* Bühne */
.buehne-hulle{container-type:inline-size;margin:0 0 clamp(30px,4vw,52px)}
.buehne{position:relative}
.buehne>*{position:absolute;margin:0}
.b-bild{overflow:hidden;background:#1c1b22}
.b-bild img,.b-bild video{width:100%;height:100%;object-fit:cover}
.b-bild img{transform:scale(1.12);transition:transform 1.6s var(--e1)}
.b-bild.da img{transform:none}
/* Anstossen: beide Hälften von unten, die zweite später, ein gemeinsamer Puls an der Naht */
.js .b-bild[data-p]{transform:translateY(60px);transition:transform 1.25s var(--e1)}
.js .b-bild[data-p="2"],.js .b-bild[data-p="4"]{transition-delay:.125s}
.js .b-bild[data-p].da{transform:none;animation:puls .5s 1.15s var(--e1) 1}
.js .b-bild[data-p="2"].da,.js .b-bild[data-p="4"].da{animation-delay:1.15s}
@keyframes puls{0%{transform:none}45%{transform:scale(1.018)}100%{transform:none}}
.js .b-platz{transform:translateY(60px);transition:transform 1.2s var(--e1)}
.js .b-platz.da{transform:none}
.b-film .spiel{position:absolute;left:10px;bottom:10px;font:400 10.5px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;background:var(--weiss);color:var(--schiefer);padding:7px 9px;border-radius:5px;cursor:pointer}
.b-text{z-index:4}
.b-ort{font:460 3.6cqw/1.05 var(--titel);color:var(--schiefer);font-variation-settings:'SOFT' 100}
.dunkel .b-ort{color:#F6F0F0}
.b-lauf{font:400 clamp(12px,1.35cqw,18px)/1.5 var(--lauf)}
.b-zitat{font:420 clamp(13px,1.9cqw,26px)/1.3 var(--titel);color:#F6F0F0}
.b-mono{font:400 clamp(10px,1cqw,13px)/1.6 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--licht-t)}
.dunkel .b-mono{color:var(--licht-h)}
.b-klein{font:400 clamp(10px,1.05cqw,14px)/1.5 var(--lauf);opacity:.8}
.b-worte{list-style:none;padding:0;z-index:4}
.b-worte li{font:500 3.3cqw/1.12 var(--titel);letter-spacing:.06em;color:color-mix(in srgb,#F6F0F0 55%,transparent)}
.b-worte li+li::before{content:'/ ';color:var(--licht)}
.b-worte li.an span{color:var(--licht-h)}
.b-tisch{z-index:4;display:flex;align-items:center;justify-content:center;background:linear-gradient(180deg,#3b2a1f,#2a1d15);color:var(--licht-h);
 box-shadow:inset 0 1px 0 rgba(255,220,180,.25),inset 0 -1px 0 rgba(0,0,0,.4)}
.b-tisch span{font:400 clamp(9px,1.25cqw,15px)/1 var(--mono);letter-spacing:.22em;text-transform:uppercase}
.b-knopf{z-index:6}
/* Fenster */
.fenster{position:relative;border-radius:var(--rund);overflow:hidden;margin:0 0 clamp(30px,4vw,52px);aspect-ratio:21/9}
.fenster img{width:100%;height:100%;object-fit:cover;object-position:50% 55%}
.fsatz{position:absolute;inset:auto 0 0 40%;margin:0;padding:80px 6% 7%;text-align:right;font:440 clamp(1.3rem,3vw,2.6rem)/1.16 var(--titel);color:#fff;
 background:radial-gradient(ellipse 80% 90% at 72% 88%,rgba(20,16,22,.82),rgba(20,16,22,.42) 45%,rgba(20,16,22,0) 78%)}
/* Drei Wege */
.wege{display:grid;gap:clamp(16px,2.4vw,30px)}
.weg{display:grid;grid-template-columns:minmax(220px,1fr) 1.6fr;gap:clamp(18px,3vw,40px);align-items:center;background:#fff;border-radius:var(--rund);padding:18px;
 box-shadow:0 26px 44px -34px rgba(20,16,30,.55)}
.weg-bilder{display:flex;gap:0;border-radius:calc(var(--rund) - 8px);overflow:hidden;aspect-ratio:4/3}
.weg-bilder img{flex:1;min-width:0;height:100%;object-fit:cover}
.weg h3{font:460 clamp(1.4rem,2.4vw,2rem)/1.12 var(--titel);margin:6px 0 10px;color:var(--schiefer)}
.weg p{margin:0}.weg .mono{color:var(--licht-t)}
.weg--an{background:var(--schiefer);color:#F3EEEE;box-shadow:0 30px 50px -30px rgba(20,16,30,.7),inset 0 0 0 1px color-mix(in srgb,var(--licht) 50%,transparent)}
.weg--an h3{color:#F6F0F0}.weg--an .mono{color:var(--licht-h)}
/* Drei Fragen, Steckbrief, Vergleich */
.drei{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2.4vw,32px);margin-bottom:28px}
.frage{background:#fff;border-radius:20px;padding:22px 24px;box-shadow:inset 0 1px 0 rgba(255,255,255,.7),0 24px 40px -34px rgba(20,16,30,.5)}
.dunkel .frage{background:rgba(255,255,255,.07);box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}
.dc .frage{background:#FBF6EC}
h4{font:400 11px/1.3 var(--mono);letter-spacing:.17em;text-transform:uppercase;margin:0 0 8px;color:var(--licht-t)}
.dunkel h4{color:var(--licht-h)}
.frage p,.steck p,.vergleich p{margin:0}
.skizze{margin:0 0 28px;max-width:86ch}.skizze p{margin:0}
.steck{display:grid;grid-template-columns:2fr 2.4fr 1.3fr 2fr;gap:22px;padding:22px 0;border-top:1px solid color-mix(in srgb,currentColor 18%,transparent);border-bottom:1px solid color-mix(in srgb,currentColor 18%,transparent);margin-bottom:28px}
.bs{font-weight:500}
.quelle{display:inline-block;font:400 10.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;padding:6px 10px;border-radius:6px;margin-left:6px;vertical-align:2px}
.q-neu{background:var(--licht);color:#fff}.q-fundus{background:var(--weiss2);color:var(--tinte);box-shadow:inset 0 0 0 1px rgba(0,0,0,.12)}
.chip{display:inline-block;width:18px;height:18px;border-radius:5px;vertical-align:-4px;margin-right:8px;border:1px solid rgba(0,0,0,.15)}
.chip--dunkel{background:var(--schiefer)}.chip--hell{background:var(--weiss)}.chip--matt{background:var(--weiss2)}.chip--tapete{background:var(--weiss)}.chip--dc{background:var(--dc)}
.bilder ul{margin:0;padding:0;list-style:none;font:400 11.5px/1.6 var(--mono);word-break:break-all;opacity:.8}
.vergleich{display:grid;grid-template-columns:1fr 1.6fr;gap:clamp(18px,3vw,40px)}
.dieses p{font:420 1.22rem/1.42 var(--titel)}
.bisher ul{margin:0;padding:0;list-style:none}
.bisher li{display:grid;grid-template-columns:minmax(150px,210px) 1fr;gap:14px;padding:9px 0;border-bottom:1px solid color-mix(in srgb,currentColor 12%,transparent)}
.bisher .haus a{text-decoration:none;border-bottom:1px solid var(--licht);font-weight:500}
/* Überleitung */
.ueber{max-width:1240px;margin:clamp(40px,5vw,70px) auto 0;padding:0 var(--rand)}
.ueber i{display:block;height:6px;width:54px;background:var(--licht);border-radius:1px;margin-bottom:14px}
.ueber p{margin:0;font:420 1.2rem/1.4 var(--titel);max-width:52ch}
/* Ideen und Inhalt */
.ideen{display:grid;grid-template-columns:1fr 1fr;gap:clamp(16px,2.4vw,32px);margin-top:10px}
.idee{background:var(--schiefer);color:#F3EEEE;border-radius:var(--rund);padding:30px 32px;box-shadow:0 30px 50px -34px rgba(20,16,30,.6),inset 0 0 0 1px color-mix(in srgb,var(--licht) 30%,transparent)}
.idee .mono{color:var(--licht-h)}
.idee h3{font:460 1.7rem/1.15 var(--titel);margin:8px 0 12px;color:#F6F0F0}
.idee p{margin:0}
.inhalt{margin-top:clamp(36px,5vw,60px);display:flex;flex-wrap:wrap;gap:10px 22px;align-items:baseline}
.inhalt .mono{width:100%;color:var(--licht-t);margin:0 0 6px}
.inhalt a{text-decoration:none;border-bottom:1px solid var(--licht);padding-bottom:2px}
/* Unterseiten */
.useiten{display:grid;grid-template-columns:repeat(2,1fr);gap:clamp(16px,2.4vw,30px)}
.useite{background:#fff;border-radius:20px;padding:24px 26px;box-shadow:0 26px 44px -34px rgba(20,16,30,.5)}
.useite h3{font:460 1.5rem/1.15 var(--titel);margin:0 0 4px;color:var(--schiefer)}
.useite>.mono{color:var(--licht-t);margin:0 0 14px}
.useite ul{list-style:none;margin:0;padding:0}
.useite li{display:grid;grid-template-columns:112px 1fr;gap:6px 14px;padding:10px 0;border-top:1px solid rgba(20,16,30,.1)}
.useite li img{grid-column:2;width:120px;height:80px;object-fit:cover;border-radius:6px;display:inline-block;margin:4px 8px 0 0}
.useite li .mono{font-size:10.5px;color:var(--licht-t)}
.zliste{list-style:none;margin:0;padding:0;columns:2;column-gap:clamp(20px,4vw,56px)}
.zliste li{break-inside:avoid;padding:12px 0;border-top:1px solid color-mix(in srgb,currentColor 16%,transparent)}
.zliste b{display:block;font-weight:500;margin-bottom:2px}
.zliste span,.useite li span,.dieses p,.frage p,.skizze p{overflow-wrap:anywhere}
/* Knopf: Tiefe und Glanz, im Kerzenlicht */
.knopf{display:inline-flex;align-items:center;gap:14px;height:4cqw;min-height:34px;max-height:54px;padding:0 1.8cqw;border-radius:7px;overflow:hidden;
 font:400 clamp(9px,.9cqw,11.5px)/1 var(--mono);letter-spacing:.17em;text-transform:uppercase;color:#fff;white-space:nowrap;
 background:linear-gradient(180deg,var(--licht-h),var(--licht) 58%,var(--licht-t));box-shadow:inset 0 1px 0 rgba(255,255,255,.5),inset 0 -2px 0 rgba(0,0,0,.2),0 22px 34px -20px rgba(0,0,0,.6)}
.knopf .pf{width:22px;height:10px;stroke:currentColor;fill:none;stroke-width:1.2}
.fuss{background:var(--nacht);color:#E6DDDD;padding:60px 0 70px;text-align:center;border-radius:var(--rund) var(--rund) 0 0;margin-top:calc(var(--rund)*-1);position:relative}
.fuss .z{width:34px;color:var(--licht);fill:currentColor;margin:0 auto 14px;display:block;height:auto}
@media (max-width:760px){
 .drei,.vergleich,.ideen,.useiten,.weg{grid-template-columns:1fr}
 .steck{grid-template-columns:1fr 1fr}
 .bisher li{grid-template-columns:1fr;gap:2px}
 .zliste{columns:1}
 .b-text,.b-worte,.b-knopf{display:none}
 .b-tisch span{font-size:7px;letter-spacing:.12em}
 .fenster{aspect-ratio:4/5}
 .useite li{grid-template-columns:1fr}
 .useite li img{grid-column:1}
}
@media (prefers-reduced-motion:reduce){.js [data-a],.js [data-a]>span,.b-bild,.b-bild img{transform:none!important;transition:none!important;animation:none!important}}
'''.replace('TAPETE', TAPETE)

JS = r'''<script>
document.documentElement.classList.add('js');
(function(){
 var els=document.querySelectorAll('[data-a],.b-bild');
 function an(e){e.classList.add('da');var v=e.querySelector&&e.querySelector('video');if(v&&!v.dataset.lief){v.dataset.lief=1;v.play().catch(function(){})}}
 if(!('IntersectionObserver' in window)){els.forEach(an);return}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){an(e.target);io.unobserve(e.target)}})},{rootMargin:'0px 0px -4% 0px'});
 var vh=window.innerHeight||800;
 els.forEach(function(e){var r=e.getBoundingClientRect();if(r.top<vh&&r.bottom>0){an(e)}else{io.observe(e)}});
 document.querySelectorAll('.b-film').forEach(function(f){f.addEventListener('click',function(){var v=f.querySelector('video');v.currentTime=0;v.play().catch(function(){})})});
})();
</script>'''


def main():
    body = kopf() + ''.join(szene(s) for s in SZENEN) + unterseiten()
    body += liste('Gestrichen.', 'Überlegt und verworfen, damit es kein anderer Chat wieder aufmacht.', GESTRICHEN, 'hell', 'gestrichen')
    body += liste('Offen.', 'Was nicht belegt ist oder fehlt; steht auch auf der Karte unter Station 06.', OFFEN, 'matt', 'offen')
    body += '<footer class="fuss">%s<p class="mono">Culinarium Hannover · Konzept-Board · nur intern, geht nie an den Kunden</p></footer>' % ZEICHEN
    doc = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           '<meta name="robots" content="noindex"><title>Konzept · Culinarium</title>'
           '<meta name="description" content="Konzept-Board Station 06: wie die Konzepte und die Menschen von Culinarium auf die Seite kommen.">'
           '<link rel="icon" href="assets/zeichen.svg"><style>%s</style></head><body>%s%s</body></html>' % (CSS, body, JS))
    open(os.path.join(PAKET, 'konzept.html'), 'w', encoding='utf-8').write(doc)

    szenen = []
    for s in SZENEN:
        d = dict(teil=s['teil'], titel=s['titel'], satz=s['satz'], bilder=[B[k][0] for k in s['bilder']] + [F[k][0] for k in s.get('filme', [])],
                 baustein=s['baustein'], quelle=s['quelle'])
        if s.get('skizze'):
            d['skizze'] = s['skizze']
        d.update(bewegung=s['bewegung'], flaeche=s['flaeche'], einfall=s['einfall'], komposition=s['komposition'], moment=s['moment'],
                 unterschied=s['unterschied'], bisher=s['bisher'], ueberleitung=UEBERLEITUNG.get(s['teil']))
        szenen.append(d)
    seiten = [dict(seite='index.html', titel='Startseite', szenen=szenen)]
    for s in SEITEN:
        seiten.append(dict(seite=s['seite'], titel=s['titel'], szenen=[dict(teil=t, satz=x, bilder=[B[b][0] for b in bs]) for t, x, bs in s['szenen']]))
    k = dict(geschichte=GESCHICHTE_SATZ + ' ' + GESCHICHTE, geschichte_satz=GESCHICHTE_SATZ,
             wege=[dict(stand=a, name=t, satz=x, bilder=[B[b][0] for b in bs]) for a, t, x, bs in WEGE],
             ideen=[dict(art=a, name=b, satz=c) for a, b, c in IDEEN],
             seiten=seiten, gestrichen=[dict(was=a, grund=b) for a, b in GESTRICHEN],
             offen=[dict(punkt=a, wo=b) for a, b in OFFEN],
             farbwelt='vorläufig aus den Plakaten: Warmweiss #FAF4F4, Schiefer-Violett #3A3845; Akzent Kerzenlicht #CF7233 aus den Fotos 4004, 3887, 3858 gemessen (Station 05 fehlt)',
             familie_machart=None, bisherige_haeuser={k: v for k, v in HAEUSER.items() if v},
             stand='26.10.2026, auf Roberts Auftrag im Chat vor den Stationen 04 und 05')
    json.dump(k, open(os.path.join(PAKET, 'konzept.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ok', os.path.getsize(os.path.join(PAKET, 'konzept.html')), 'Bytes')


main()
