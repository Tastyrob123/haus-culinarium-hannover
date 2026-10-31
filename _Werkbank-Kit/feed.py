#!/usr/bin/env python3
"""Instagram-Feed als Idee: Beiträge, Profilbild, Biografie, Handy-Vorschau.   (Vorlage: Carlton-Europe/_werkbank/feed.py)
   python3 feed.py "<Projekt>"           Fotos zuschneiden, Tafeln setzen (feed/_tafeln.html), feed.json und feed/index.html schreiben
   node feed_druck.js "<Projekt>"        Tafeln und Profilbild als Bilder rendern
   python3 feed.py "<Projekt>"           noch einmal, für die Raster-Bilder der Tafeln
   node feed_druck.js "<Projekt>" --handy   Handy für die Werkbank aufnehmen

Inhalt je Haus: <Projekt>/_werkbank/feed_daten.py (PROFIL, HIGHLIGHTS, P, SEITE).
Regeln (Master 5a, Regel 10): echte Fotos des Hauses, nie Gästefotos, nie erzeugte Bilder; ein Ton für alle Fotos, ein Schriftsystem
für alle Tafeln; kein Motiv doppelt. Der Aufbau ist je Haus ein anderer (Robert 09.10.2026: nicht jeder Feed nach demselben Schema), D.REGEL:
  'eine'    je Reihe genau eine Tafel, ihr Platz wandert (Carlton-Europe)
  'spalten' drei Spalten mit je einem Thema, Tafeln nur in der mittleren
  'schach'  Bild und Blatt im Wechsel
  'reihen'  ganze Reihen, in denen ein Bild über drei Beiträge läuft (Art 'p'), dazwischen freie Reihen
  'bogen'   freier Bogen mit eigenen Formen je Haus (feed_bogen.py, seit 17.10.2026; Master 5a Regel 10a)
Arten: f Foto · t Satz auf dem Muster (t:hell auf Papier, t:<klasse> eigene) · a Blatt mit Bild · e Etikett · k Blatt aus der Karte · p Teil eines breiten Bildes.
Die Beitragstexte sind von Tasty Studios; Sätze auf den Tafeln stammen vom Haus (Quelle je Tafel im Kommentar der Daten).
Bestandsabgleich (29.10.2026, feed_bestand.py): Gibt es einen Instagram-Bestand des Hauses (Standard <Haus>/_quelle/extern/ig/*.jpg, sonst
IG_BESTAND in feed_daten.py), prüft feed.py vor dem Bau jedes Foto des Feeds dagegen (pHash und Ausschnitt-Vergleich) und bricht ab, wenn eines
schon gepostet ist. Der Feed setzt den echten Feed fort, er ersetzt ihn nicht. Ausnahmen je Haus: BESTAND_AUSNAHMEN = ('p_', …) (Plakate o. Ä.);
die echten bisherigen Beiträge selbst tragen bestand=True. Bericht: feed/bestand.json."""
import html, json, os, re
from PIL import Image, ImageEnhance
import kern as K
from kern import H, ROOT, W
import feed_daten as D

ZIEL = os.path.join(ROOT, 'feed'); POSTS = os.path.join(ZIEL, 'posts'); THUMBS = os.path.join(ZIEL, 'thumbs')
for d in (POSTS, THUMBS):
    os.makedirs(d, exist_ok=True)
e = html.escape
F = H.FARBEN
PROFIL, HIGHLIGHTS, P = D.PROFIL, D.HIGHLIGHTS, D.P
_vb, _zi = H.ZEICHEN
_zb, _zh = (float(x) for x in _vb.split()[2:])
HZ = lambda farbe, b: f'<svg viewBox="{_vb}" width="{b}" height="{b * _zh / _zb:.0f}" fill="{farbe}">{_zi}</svg>'
REIHEN = len(P) // 3
assert len(P) % 3 == 0
ART = [p[0].partition(':')[0] for p in P]
BILD = ('f', 'p')
REGEL = getattr(D, 'REGEL', 'eine')
for r in range(REIHEN):
    reihe = ART[r * 3:r * 3 + 3]
    if REGEL == 'eine':
        assert sum(1 for a in reihe if a not in BILD) == 1, ('Reihe', r + 1)
    elif REGEL == 'spalten':
        assert reihe[0] in BILD and reihe[2] in BILD, ('Reihe', r + 1)
    elif REGEL == 'schach':
        assert all((a in BILD) == ((r + c) % 2 == 0) for c, a in enumerate(reihe)), ('Reihe', r + 1)
    elif REGEL == 'reihen':
        assert reihe.count('p') in (0, 3), ('Reihe', r + 1)


def _motiv(p, a):
    if a in ('t', 'k'):
        return ' '.join(p[1]) if isinstance(p[1], list) else p[1] + ' ' + ' '.join(p[2])
    return (p[1], p[2]) if a == 'p' else p[1]


assert len({_motiv(p, a) for p, a in zip(P, ART)}) == len(P), 'ein Motiv doppelt'


def quelle(key):
    return K.hausbild(key)


def ton(im):
    """Ein Ton für alle Fotos: etwas ruhiger in der Farbe, leicht mehr Kontrast, eine Spur zur Farbwelt des Hauses."""
    fa, ko, rr, bb = getattr(D, 'TON', (.93, 1.04, 1.02, .965))
    im = ImageEnhance.Color(im).enhance(fa)
    im = ImageEnhance.Contrast(im).enhance(ko)
    r, g, b = im.split()
    return Image.merge('RGB', (r.point(lambda v: min(255, int(v * rr))), g, b.point(lambda v: min(255, int(v * bb)))))


def foto(key, fx, nr):
    im = Image.open(quelle(key)).convert('RGB')
    w, h = im.size
    zb = h * 4 / 5
    if zb <= w:
        x0 = max(0, min(w - zb, w * fx - zb / 2)); box = (round(x0), 0, round(x0 + zb), h)
    else:
        zh = w * 5 / 4; fy = getattr(D, 'HOCH', {}).get(key, .5); y0 = max(0, min(h - zh, h * fy - zh / 2)); box = (0, round(y0), w, round(y0 + zh))
    im = ton(im.crop(box).resize((1080, 1350), Image.LANCZOS))
    im.save(os.path.join(POSTS, f'{nr:02d}.jpg'), quality=90)
    return im



def breit(key, teil, fy, nr):
    """Ein Bild über drei Beiträge: ein Streifen 3105 × 1350, jeder Beitrag zeigt 1080 davon. Im Raster (3:4, je Seite 34 px weniger) schliessen die drei Teile lückenlos an."""
    im = Image.open(quelle(key)).convert('RGB')
    w, h = im.size
    sv = 3105 / 1350
    if w / h >= sv:
        nw = h * sv; x0 = (w - nw) / 2; box = (round(x0), 0, round(x0 + nw), h)
    else:
        nh = w / sv; y0 = max(0, min(h - nh, h * fy - nh / 2)); box = (0, round(y0), w, round(y0 + nh))
    st = im.crop(box).resize((3105, 1350), Image.LANCZOS)
    x = round(teil * 1012.5)
    im = ton(st.crop((x, 0, x + 1080, 1350)))
    im.save(os.path.join(POSTS, f'{nr:02d}.jpg'), quality=90)
    return im


TAFEL_CSS_ROH = '''
__SCHRIFT__*{box-sizing:border-box;margin:0;padding:0}
body{background:#333}
.k{position:relative;width:1080px;height:1350px;overflow:hidden;margin:0 0 20px;font-family:'B',__FOLGE__}
.k--t,.k--e{background:#0b1f40 __MUSTER__ 50% 50%/__MB__ auto;color:#f4ecdc}
.k--a{background:#f4ecdc;color:#0b1f40}
/* das Raster zeigt 3:4, also 34 px weniger je Seite: der Rahmen hält Abstand */
.k i.r{position:absolute;inset:86px 96px;border:1.5px solid rgba(220,198,143,.62)}
.k--a i.r{border-color:rgba(138,117,69,.6)}
.k .ce{position:absolute;left:0;right:0;top:170px;display:flex;justify-content:center}
.k .satz{position:absolute;left:120px;right:120px;top:50%;transform:translateY(-46%);text-align:center;font-size:112px;line-height:1.14;letter-spacing:-.005em}
.k .satz b{font-weight:400;color:#dcc68f;display:block}
.k .satz span{display:block}
.k .lin{position:absolute;left:50%;bottom:262px;width:110px;height:2px;margin-left:-55px;background:#dcc68f}
.k .kl{position:absolute;left:120px;right:120px;bottom:186px;text-align:center;font-family:'M',monospace;font-size:23px;letter-spacing:.2em;text-transform:uppercase;color:#dcc68f}
.k--a .kl{color:#8a7545}.k--a .lin{background:#a98a45}
.k--a .name{position:absolute;left:0;right:0;top:268px;text-align:center;font-size:92px;line-height:1.1}
.k--a .bild{position:absolute;left:138px;right:138px;top:424px;height:640px;display:flex;align-items:center;justify-content:center}
.k--a .bild img{width:100%;height:100%;object-fit:cover;object-position:var(--op,50% 50%);display:block;border:1.5px solid rgba(11,31,64,.5);padding:12px;background:#fbf6ea}
.k--a .lin{bottom:236px}.k--a .kl{bottom:164px}.k--a .ce{top:150px}
.k--a .bild svg{height:100%;width:auto}
.k--e .et{position:absolute;left:50%;top:50%;width:700px;transform:translate(-50%,-50%) rotate(-5deg)}
.k--e .et img{width:100%;display:block;filter:drop-shadow(0 30px 34px rgba(0,0,0,.5))}
.k--t.hell{background:#f4ecdc;color:#0b1f40}
.k--t.hell i.r{border-color:rgba(138,117,69,.6)}.k--t.hell .satz b{color:#8a7545}.k--t.hell .kl{color:#8a7545}.k--t.hell .lin{background:#a98a45}
/* Blatt aus der Karte: Stube, Name des Gerichts, seine Zeile und der Preis, wie auf der Karte des Hauses */
.k--k{background:#f4ecdc;color:#0b1f40}
.k--k i.r{border-color:rgba(138,117,69,.6)}
.k--k i.r::after{content:'';position:absolute;inset:10px;border:1px solid rgba(138,117,69,.35)}
.k--k .ce{top:158px}
.k--k .mit{position:absolute;left:150px;right:150px;top:330px;bottom:330px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.k--k .name{font-size:104px;line-height:1.08}
.k--k .name span{display:block}
.k--k .zl{margin-top:44px;font-family:'S',Arial,sans-serif;font-size:45px;line-height:1.42;color:rgba(11,31,64,.8);max-width:660px}
.k--k .pr{position:absolute;left:150px;right:150px;bottom:236px;display:flex;align-items:baseline;gap:16px;font-size:62px}
.k--k .pr i{flex:1;border-bottom:3px dotted rgba(11,31,64,.4);transform:translateY(-10px)}
.k--k .pr small{font-family:'M',monospace;font-size:23px;letter-spacing:.2em;text-transform:uppercase;color:#8a7545}
.k--k .kl{position:absolute;left:120px;right:120px;bottom:160px;text-align:center;font-family:'M',monospace;font-size:21px;letter-spacing:.2em;text-transform:uppercase;color:#8a7545}
.av{width:640px;height:640px;border-radius:50%;background:#0b1f40 __MUSTER__ 50% 50%/__MB__ auto;display:flex;align-items:center;justify-content:center;position:relative}
.av::after{content:'';position:absolute;inset:34px;border-radius:50%;border:3px solid rgba(220,198,143,.7)}
'''


def tafel_css():
    t = [x for x in H.DRUCKSCHRIFT if x[0] == H.SCHRIFT['titel'][0]][0]
    schrift = f"@font-face{{font-family:'B';src:url('../_werkbank/fonts/{t[2]}') format('truetype')}}\n@font-face{{font-family:'M';src:url('../_werkbank/fonts/DMMono-Regular.ttf') format('truetype')}}\n@font-face{{font-family:'S';src:url('../_werkbank/fonts/InstrumentSans-Regular.ttf') format('truetype')}}\n"
    css = K.faerbe(TAFEL_CSS_ROH.replace('__SCHRIFT__', '')).replace('__MUSTER__', H.MUSTER).replace('__MB__', getattr(D, 'MUSTER_B', '360px')).replace('__FOLGE__', H.SCHRIFT.get('titel_folge', 'Georgia,serif'))
    return schrift + css + '.av{border-radius:0}.av::after{border-radius:50%}' + getattr(D, 'TAFEL_CSS', '')


def tafeln():
    o = ''
    lage = getattr(D, 'LAGE', {})
    for nr, p in enumerate(P, 1):
        art, _, kl = p[0].partition(':')
        if art == 't':
            zl = p[1]
            satz = ''.join(f'<b>{e(z)}</b>' if i == len(zl) - 1 else f'<span>{e(z)}</span>' for i, z in enumerate(zl))
            o += f'<section class="k k--t {kl}" data-nr="{nr}"><i class="r"></i><div class="ce">{HZ(F["gold"], getattr(D, "ZEICHEN_B", 150))}</div><div class="satz" style="font-size:{getattr(D, "SATZ_PX", 112)}px">{satz}</div><i class="lin"></i><p class="kl">{e(p[2])}</p></section>'
        elif art == 'k':   # ('k', Stube, [Name in Zeilen], Zeile, Preis, Text)
            name = ''.join(f'<span>{e(z)}</span>' for z in p[2])
            o += (f'<section class="k k--k {kl}" data-nr="{nr}"><i class="r"></i><div class="ce">{HZ(F["messing"], getattr(D, "ZEICHEN_B", 150) * .7)}</div>'
                  f'<div class="mit"><p class="name">{name}</p><p class="zl">{e(p[3])}</p></div><p class="pr"><small>CHF</small><i></i><span>{e(p[4])}</span></p><p class="kl">{e(p[1])}</p></section>')
        elif art == 'a':
            pfad = os.path.relpath(quelle(p[1]), ZIEL)
            bild = f'<img src="{e(pfad)}" style="--op:{lage.get(p[1], "50% 50%")}">'
            o += f'<section class="k k--a" data-nr="{nr}"><i class="r"></i><div class="ce">{HZ(F["messing"], getattr(D, "ZEICHEN_B", 150) * .7)}</div><p class="name">{e(p[2])}</p><div class="bild">{bild}</div><i class="lin"></i><p class="kl">{e(p[3])}</p></section>'
        elif art == 'e':
            o += f'<section class="k k--e" data-nr="{nr}"><i class="r"></i><div class="et"><img src="../_werkbank/roh/papier/{p[1]}.png"></div></section>'
    o += f'<div class="av" id="av">{HZ(F["gold"], getattr(D, "AV_B", 330))}</div>'
    K.schreib(os.path.join(ZIEL, '_tafeln.html'), f'<!doctype html><meta charset="utf-8"><style>{tafel_css()}</style>{o}')

IC = {
    'plus': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 8v8M8 12h8"/></svg>',
    'menu': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    'raster': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M9 3v18M15 3v18M3 9h18M3 15h18"/></svg>',
    'reels': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M3 8h18M9 3l3 5M15 3l3 5"/><path d="m10.5 11.5 4 2.5-4 2.5z" fill="currentColor"/></svg>',
    'person': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="12" cy="10" r="3"/><path d="M6.5 19a6 6 0 0 1 11 0"/></svg>',
    'herz': '<svg width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><path d="M12 20.5s-7.5-4.6-7.5-10a4.2 4.2 0 0 1 7.5-2.6 4.2 4.2 0 0 1 7.5 2.6c0 5.400-7.5 10-7.5 10z"/></svg>',
    'blase': '<svg width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><path d="M20.5 11.5a8.5 8.5 0 0 1-12.6 7.400L3.5 20.5l1.600-4.400A8.5 8.5 0 1 1 20.5 11.5z"/></svg>',
    'pfeil': '<svg width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><path d="M21 3 10.5 13.5M21 3l-6.5 18-4-7.5L3 9.5z"/></svg>',
    'merk': '<svg width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><path d="M6 3.5h12v17l-6-4.5-6 4.5z"/></svg>',
    'haus': '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><path d="M3.5 10.5 12 3.5l8.5 7V20.5h-5.5v-6h-6v6H3.5z"/></svg>',
    'lupe': '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>',
}


def seite():
    daten = {'profil': PROFIL, 'posts': [{'n': f'{i:02d}', 'cap': p[-1]} for i, p in enumerate(P, 1)], 'hl': [h[0] for h in HIGHLIGHTS]}
    json.dump(daten, open(os.path.join(ZIEL, 'feed.json'), 'w'), ensure_ascii=False, indent=1)
    z = PROFIL['zahlen']
    doc = f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Feed · {e(H.NAME)}</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['nacht']}">
<style>
@font-face{{font-family:'Baskerville CE';font-weight:400 700;font-display:swap;src:url('../werkbank/fonts/{H.SCHRIFT['titel'][1]}') format('woff2')}}
@font-face{{font-family:'Instrument Sans';font-weight:400 600;font-display:swap;src:url('../werkbank/fonts/InstrumentSans-normal-400_600.woff2') format('woff2')}}
@font-face{{font-family:'DM Mono';font-weight:400;font-display:swap;src:url('../werkbank/fonts/DMMono-normal-400.woff2') format('woff2')}}
:root{{--nacht:#06142b;--navy:#0b1f40;--gold:#dcc68f;--papier:#f4ecdc;--e1:cubic-bezier(.16,1,.3,1);--e2:cubic-bezier(.32,.72,0,1)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:var(--nacht);color:#fff;font-family:'Instrument Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
body{{background:var(--nacht) __MUSTER__ 50% 0/__MB2__ auto;min-height:100vh}}
button{{font:inherit;color:inherit;background:none;border:0;cursor:pointer}}
a{{color:inherit;text-decoration:none}}
.stage{{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;gap:clamp(40px,7vw,110px);padding:56px 24px}}
.aside{{max-width:430px}}
.aside>*{{opacity:0;transform:translateY(34px);animation:auf 1.2s var(--e1) forwards}}
.aside>*:nth-child(2){{animation-delay:.1s}}.aside>*:nth-child(3){{animation-delay:.2s}}.aside>*:nth-child(4){{animation-delay:.3s}}.aside>*:nth-child(5){{animation-delay:.4s}}.aside>*:nth-child(6){{animation-delay:.5s}}.aside>*:nth-child(7){{animation-delay:.6s}}
@keyframes auf{{to{{opacity:1;transform:none}}}}
.aside svg.ce{{width:74px;height:auto;color:var(--gold);margin-bottom:30px;display:block}}
.aside .kap{{display:flex;align-items:center;gap:16px;font-family:'Baskerville CE',Georgia,serif;color:var(--gold);font-size:1.08rem;margin-bottom:22px}}
.aside .kap i{{width:64px;height:1px;background:currentColor;opacity:.75}}
.aside h1{{font-family:'Baskerville CE',Georgia,serif;font-weight:400;font-size:clamp(2.8rem,4.6vw,4.3rem);line-height:1.06;margin-bottom:26px}}
.aside h1 em{{font-style:normal;color:var(--gold);display:block}}
.aside p{{font-size:1.1rem;line-height:1.66;color:rgba(255,255,255,.82)}}
.aside p+p{{margin-top:14px}}
.aside dl{{display:grid;grid-template-columns:auto 1fr;gap:10px 20px;margin-top:30px;padding-top:24px;border-top:1px solid rgba(220,198,143,.3);font-size:.98rem}}
.aside dt{{font-family:'DM Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);padding-top:3px}}
.aside dd{{color:rgba(255,255,255,.82);line-height:1.5}}
.kn{{position:relative;overflow:hidden;display:inline-flex;align-items:center;gap:14px;height:54px;padding:0 8px 0 26px;border-radius:999px;margin-top:32px;font-family:'DM Mono',monospace;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:#0c1526;
  background:linear-gradient(180deg,#fbf3e2,#e8dbbf 46%,#cfbd98);box-shadow:inset 0 1px 0 rgba(255,255,255,.92),inset 0 -3px 0 rgba(110,88,44,.38),0 16px 26px -14px rgba(0,0,0,.6);transition:transform .55s var(--e2)}}
.kn:hover{{transform:translateY(-2px)}}.kn:active{{transform:translateY(1px) scale(.985)}}
.kn i{{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,#1e3c72,#050f22);color:#fbf6ea;box-shadow:inset 0 1px 0 rgba(255,255,255,.24),0 3px 6px rgba(0,0,0,.35)}}
.kn svg{{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.2}}
/* Gerät */
.devwrap{{position:relative;flex:none;opacity:0;transform:translateY(90px) rotate(3deg);animation:geraet 1.5s var(--e1) .25s forwards}}
@keyframes geraet{{to{{opacity:1;transform:none}}}}
.device{{width:402px;height:874px;border-radius:62px;background:#000;padding:12px;position:relative;box-shadow:0 0 0 2px #2c2e36,0 0 0 9px #0a0c12,0 0 0 10px rgba(220,198,143,.35),0 60px 90px -30px rgba(0,0,0,.85)}}
.screen{{width:100%;height:100%;border-radius:50px;overflow:hidden;background:#000;position:relative;display:flex;flex-direction:column;font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Arial,sans-serif}}
.island{{position:absolute;top:11px;left:50%;transform:translateX(-50%);width:124px;height:36px;border-radius:20px;background:#000;z-index:30}}
.status{{height:54px;display:flex;align-items:flex-end;justify-content:space-between;padding:0 30px 8px 36px;font-size:16px;font-weight:600;flex:none;position:relative;z-index:25;background:#000}}
.status .ic{{display:flex;gap:6px;align-items:center}}
.scroll{{flex:1;overflow-y:auto;overflow-x:hidden;scrollbar-width:none}}
.scroll::-webkit-scrollbar{{display:none}}
.top{{display:flex;align-items:center;justify-content:space-between;padding:6px 16px 10px;position:sticky;top:0;background:#000;z-index:20}}
.top .u{{display:flex;align-items:center;gap:6px;font-size:20px;font-weight:700;letter-spacing:-.01em}}
.top .r{{display:flex;gap:22px}}
.head{{display:flex;align-items:center;gap:22px;padding:4px 16px 10px}}
.avr{{width:86px;height:86px;border-radius:50%;padding:2px;background:conic-gradient(#a98a45,#f3e3b8,#7d6228,#dcc68f,#a98a45);flex:none}}
.avr img{{width:100%;height:100%;border-radius:50%;border:3px solid #000;display:block;object-fit:cover}}
.nums{{display:flex;flex:1;justify-content:space-around;text-align:center}}
.nums b{{display:block;font-size:17px;font-weight:700}}
.nums span{{font-size:13px;color:#e8e8e8}}
.bio{{padding:0 16px;font-size:14px;line-height:1.38}}
.bio .n{{font-weight:600}}.bio .cat{{color:#a8a8a8}}.bio .l{{color:#e0f1ff;font-weight:600}}
.btns{{display:flex;gap:6px;padding:12px 16px 4px}}
.btns div{{flex:1;background:#262626;border-radius:9px;text-align:center;font-size:14px;font-weight:600;padding:8px 0}}
.btns div.p{{background:#0095f6}}
.hl{{display:flex;gap:14px;padding:14px 16px 12px;overflow-x:auto;scrollbar-width:none}}
.hl::-webkit-scrollbar{{display:none}}
.h{{text-align:center;font-size:12px;flex:none;width:68px}}
.h i{{display:block;width:66px;height:66px;border-radius:50%;border:1px solid #3a3a3a;padding:3px;margin:0 auto 6px}}
.h i img{{width:100%;height:100%;border-radius:50%;object-fit:cover;display:block}}
.tabs{{display:flex;border-bottom:1px solid #262626;position:sticky;top:48px;background:#000;z-index:19}}
.tabs div{{flex:1;display:flex;justify-content:center;padding:11px 0;color:#8e8e8e}}
.tabs div.on{{color:#fff;box-shadow:inset 0 -1.5px 0 #fff}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}}
.t{{aspect-ratio:3/4;overflow:hidden;background:#0b1f40;position:relative;cursor:pointer;padding:0;display:block;width:100%}}
.t img{{width:100%;height:100%;object-fit:cover;display:block;opacity:0;transform:scale(1.08);transition:opacity .9s var(--e1),transform 1.3s var(--e1);transition-delay:calc(var(--i)*55ms + .9s)}}
.geladen .t img{{opacity:1;transform:none}}
.nav{{height:82px;flex:none;display:flex;justify-content:space-around;align-items:flex-start;padding-top:12px;border-top:1px solid #1d1d1d;background:#000}}
.nav .me{{width:26px;height:26px;border-radius:50%;border:2px solid #fff;overflow:hidden}}
.nav .me img{{width:100%;height:100%;object-fit:cover;display:block}}
.post{{position:absolute;inset:0;background:#000;z-index:40;display:flex;flex-direction:column;transform:translateX(100%);transition:transform .5s var(--e2);visibility:hidden}}
.post.on{{transform:none;visibility:visible}}
.post .bar{{height:54px;flex:none}}
.post .ph{{display:flex;align-items:center;gap:10px;padding:8px 14px}}
.post .ph b{{font-size:14px}}
.post .ph .mini{{width:32px;height:32px;border-radius:50%;overflow:hidden;border:1px solid #333}}
.post .ph .mini img{{width:100%;height:100%;object-fit:cover;display:block}}
.post .ph .back{{margin-right:6px;font-size:24px;line-height:1;padding:4px 8px 6px 0}}
.post .body{{flex:1;overflow-y:auto;scrollbar-width:none}}
.post .body::-webkit-scrollbar{{display:none}}
.post .img{{width:100%;aspect-ratio:4/5;display:block;object-fit:cover;background:#0b1f40}}
.post .act{{display:flex;gap:16px;padding:10px 14px 4px}}
.post .act span{{margin-left:auto}}
.post .cap{{padding:6px 14px 18px;font-size:14px;line-height:1.42}}
.post .cap b{{font-weight:600}}
.post .cap span{{white-space:pre-line}}
.post .ph .wer{{display:flex;flex-direction:column;line-height:1.2}}
.post .ph .wer small{{font-size:12px;color:#d4d4d4}}
.post .nx{{display:flex;justify-content:space-between;padding:0 14px 22px;font-size:13px;color:#a8a8a8}}
.post .nx button{{padding:6px 0}}
@media (max-width:1000px){{.stage{{gap:44px}}.aside{{max-width:340px}}}}
@media (max-width:820px){{
  body{{background:#000}}
  .stage{{padding:0;gap:0;min-height:100svh;display:block}}
  .aside{{display:none}}
  .devwrap{{animation:none;opacity:1;transform:none}}
  .device{{width:100vw;height:100svh;border-radius:0;padding:0;box-shadow:none}}
  .screen{{border-radius:0}}.island{{display:none}}.status{{height:14px}}.status>*{{display:none}}.post .bar{{height:14px}}
  .zurueck{{display:flex}}
}}
.zurueck{{display:none;position:fixed;z-index:60;right:14px;bottom:96px;height:44px;padding:0 18px;border-radius:999px;align-items:center;font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#0c1526;background:linear-gradient(180deg,#fbf3e2,#cfbd98);box-shadow:0 10px 20px -8px rgba(0,0,0,.8)}}
@media (prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none!important;transition:none!important}}.aside>*,.devwrap,.t img{{opacity:1!important;transform:none!important}}}}
</style>
</head>
<body>
<div class="stage">
  <div class="aside">
    <svg class="ce" viewBox="{_vb}" fill="currentColor" aria-hidden="true">{_zi}</svg>
    <p class="kap"><b style="font-weight:400">{K.nr('feed'):02d}</b><i></i><span>Instagram</span></p>
    <h1>{e(D.SEITE.get('titel', ['Ein Feed', 'als Idee.'])[0])} <em>{e(D.SEITE.get('titel', ['Ein Feed', 'als Idee.'])[1])}</em></h1>
    <p>{D.SEITE['text1']}</p>
    <p>{D.SEITE['text2']}</p>
    <dl>
      <dt>Beiträge</dt><dd>{len(P)} in {K.zahl(REIHEN).lower()} Reihen, 1080 × 1350</dd>
      {f"<dt>Aufbau</dt><dd>{D.SEITE['aufbau']}</dd>" if D.SEITE.get('aufbau') else ''}
      <dt>Bilder</dt><dd>{D.SEITE['bilder']}</dd>
      <dt>Texte</dt><dd>{D.SEITE.get('texte', 'Ideen von mir, die Sätze auf den Tafeln stammen von Ihnen')}</dd>
    </dl>
    <a class="kn" href="../werkbank/index.html#feed">Zur Werkbank<i><svg viewBox="0 0 16 16"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg></i></a>
  </div>
  <div class="devwrap"><div class="device" id="device"><div class="screen">
    <div class="island"></div>
    <div class="status"><span>9:41</span><span class="ic">
      <svg width="18" height="12" viewBox="0 0 18 12" fill="#fff"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg>
      <svg width="26" height="12" viewBox="0 0 26 12"><rect x=".5" y=".5" width="22" height="11" rx="3" fill="none" stroke="#fff" opacity=".5"/><rect x="2" y="2" width="19" height="8" rx="2" fill="#fff"/><rect x="24" y="4" width="1.6" height="4" rx=".8" fill="#fff" opacity=".5"/></svg></span></div>
    <div class="scroll" id="scroll">
      <div class="top"><div class="u">{PROFIL['name']} <svg width="12" height="8" viewBox="0 0 12 8"><path d="M1 1.5 6 6.5l5-5" stroke="#fff" stroke-width="1.8" fill="none"/></svg></div><div class="r">{IC['plus']}{IC['menu']}</div></div>
      <div class="head">
        <div class="avr"><img src="avatar.jpg" alt="Profilbild: das Zeichen des Hauses"></div>
        <div class="nums"><div><b>{z['beitraege']}</b><span>Beiträge</span></div><div><b>{z['follower']}</b><span>Follower</span></div><div><b>{z['gefolgt']}</b><span>Gefolgt</span></div></div>
      </div>
      <div class="bio"><div class="n">{e(PROFIL['titel'])}</div><div class="cat">{e(PROFIL['art'])}</div>{''.join(f'<div>{e(b)}</div>' for b in PROFIL['bio'])}<div class="l">{PROFIL['link']}</div></div>
      <div class="btns"><div class="p">Folgen</div><div>Nachricht</div><div>Kontakt</div></div>
      <div class="hl">{''.join(f'<div class="h"><i><img src="thumbs/h-{i}.jpg" alt=""></i>{e(h[0])}</div>' for i, h in enumerate(HIGHLIGHTS))}</div>
      <div class="tabs"><div class="on">{IC['raster']}</div><div>{IC['reels']}</div><div>{IC['person']}</div></div>
      <div class="grid" id="grid">{''.join(f'<button class="t" type="button" data-i="{i}" style="--i:{i}" aria-label="Beitrag {i + 1} öffnen"><img src="thumbs/{i + 1:02d}.jpg" alt=""{" loading=lazy" if i > 11 else ""}></button>' for i in range(len(P)))}</div>
    </div>
    <div class="nav">{IC['haus']}{IC['lupe']}{IC['plus']}{IC['reels']}<div class="me"><img src="avatar.jpg" alt=""></div></div>
    <div class="post" id="post" aria-hidden="true">
      <div class="bar"></div>
      <div class="ph"><button class="back" type="button" id="zu" aria-label="Zurück zum Profil">‹</button><div class="mini"><img src="avatar.jpg" alt=""></div><div class="wer"><b>{PROFIL['name']}</b>{'<small id="port"></small>' if getattr(D, 'ORT', '') else ''}</div></div>
      <div class="body"><img class="img" id="pimg" alt=""><div class="act">{IC['herz']}{IC['blase']}{IC['pfeil']}<span>{IC['merk']}</span></div>
        <div class="cap"><b>{PROFIL['name']}</b> <span id="pcap"></span></div>
        <div class="nx"><button type="button" id="vor">‹ Vorheriger</button><span id="pnr"></span><button type="button" id="nach">Nächster ›</button></div></div>
    </div>
  </div></div></div>
</div>
<a class="zurueck" href="../werkbank/index.html#feed">Zur Werkbank</a>
<script>
(function () {{
  var D = {json.dumps([p[-1] for p in P], ensure_ascii=False)}, O = {json.dumps([getattr(D, 'ORTE', {}).get(i, getattr(D, 'ORT', '')) for i in range(1, len(P) + 1)], ensure_ascii=False)}, po = document.getElementById('port'), post = document.getElementById('post'), img = document.getElementById('pimg'), cap = document.getElementById('pcap'), nr = document.getElementById('pnr'), n = 0;
  function zeig(i) {{ n = (i + D.length) % D.length; img.src = 'posts/' + ('0' + (n + 1)).slice(-2) + '.jpg'; cap.textContent = D[n]; nr.textContent = (n + 1) + ' / ' + D.length; if (po) po.textContent = O[n]; post.classList.add('on'); post.setAttribute('aria-hidden', 'false'); post.querySelector('.body').scrollTop = 0; }}
  function zu() {{ post.classList.remove('on'); post.setAttribute('aria-hidden', 'true'); }}
  document.getElementById('grid').addEventListener('click', function (e) {{ var t = e.target.closest('.t'); if (t) zeig(+t.dataset.i); }});
  document.getElementById('zu').addEventListener('click', zu);
  document.getElementById('vor').addEventListener('click', function () {{ zeig(n - 1); }});
  document.getElementById('nach').addEventListener('click', function () {{ zeig(n + 1); }});
  document.addEventListener('keydown', function (e) {{ if (!post.classList.contains('on')) return; if (e.key === 'Escape') zu(); if (e.key === 'ArrowRight') zeig(n + 1); if (e.key === 'ArrowLeft') zeig(n - 1); }});
  requestAnimationFrame(function () {{ document.body.classList.add('geladen'); }});
}})();
</script>
</body>
</html>
'''
    doc = K.faerbe(doc.replace('__MUSTER__', 'MUSTERPLATZ')).replace('MUSTERPLATZ', H.MUSTER).replace('__MB2__', H.MUSTER_B).replace("'Baskerville CE',Georgia,serif", "'Baskerville CE'," + H.SCHRIFT.get('titel_folge', 'Georgia,serif'))
    K.schreib(os.path.join(ZIEL, 'index.html'), doc)


def thumbs():
    """Raster-Ansicht 3:4 (wie Instagram: 34 px je Seite weniger) und die runden Titelbilder."""
    for i in range(1, len(P) + 1):
        p = os.path.join(POSTS, f'{i:02d}.jpg')
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert('RGB')
        w, h = im.size; zb = h * 3 / 4
        im.crop((round((w - zb) / 2), 0, round((w + zb) / 2), h)).resize((540, 720), Image.LANCZOS).save(os.path.join(THUMBS, f'{i:02d}.jpg'), quality=86)
    for i, (_, key, fx) in enumerate(HIGHLIGHTS):
        im = Image.open(quelle(key)).convert('RGB'); w, h = im.size; s = min(w, h)
        x0 = max(0, min(w - s, w * fx - s / 2)); y0 = (h - s) // 2
        ton(im.crop((round(x0), y0, round(x0 + s), y0 + s)).resize((200, 200), Image.LANCZOS)).save(os.path.join(THUMBS, f'h-{i}.jpg'), quality=88)
    roh = os.path.join(ZIEL, 'avatar-roh.png')
    if os.path.exists(roh):   # Profilbild aus der gerenderten Tafel
        Image.open(roh).convert('RGB').resize((640, 640), Image.LANCZOS).save(os.path.join(ZIEL, 'avatar.jpg'), quality=92)


if __name__ == '__main__':
    import feed_bestand; feed_bestand.pruefen(ROOT, D, quelle)   # Bestandsabgleich: nichts, was schon im Instagram-Feed steht (feed_bestand.py)
    if REGEL == 'bogen':   # Feed-Planer 17.10.2026: das Raster als eine Fläche mit eigenen Formen je Haus (feed_bogen.py)
        import feed_bogen; feed_bogen.bauen(ROOT, D, quelle, ton); tafeln(); thumbs(); seite(); raise SystemExit
    for nr, p in enumerate(P, 1):
        if p[0] == 'f':
            foto(p[1], p[2], nr)
        elif p[0] == 'p':
            breit(p[1], p[2], p[3], nr)
    tafeln(); thumbs(); seite()
    print('Feed:', len(P), 'Beiträge,', sum(1 for a in ART if a in BILD), 'Fotos,', sum(1 for a in ART if a not in BILD), 'Tafeln, Aufbau:', REGEL)
