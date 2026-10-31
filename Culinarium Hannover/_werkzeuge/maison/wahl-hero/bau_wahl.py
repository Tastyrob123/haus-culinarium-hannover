#!/usr/bin/env python3
"""Wahlseite Hero des Tresens (29.10.2026, Robert: «bitte für den Tresen ein anderes Interface … das muss richtig einladen»).
Baut sechs Fassungen als echte Seiten: der gebaute Tresen (../index.html) mit neuem Empfang unter dem Kopf. Werkzeuge, Wege, Stand-Schlüssel
und Abendfarben kommen aus dem gebauten Tresen, Fotos und Alt-Texte aus dem Bildregister der Website (bau.py → BILDER_W), der nächste Abend
aus website/bau.py. Nichts von Hand. Aufruf: python3 wahl-hero/bau_wahl.py"""
import html, importlib.util, os, re
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
MAISON = os.path.dirname(HIER)
HAUS = os.path.dirname(os.path.dirname(MAISON))
BILD = os.path.join(HAUS, 'website', 'assets', 'bild')

s = importlib.util.spec_from_file_location('bau', os.path.join(MAISON, 'bau.py')); bau = importlib.util.module_from_spec(s); s.loader.exec_module(bau)
REG = bau.BILDER_W
e = lambda t: html.escape(str(t), quote=True)

QUELLE = open(os.path.join(MAISON, 'index.html'), encoding='utf-8').read()
a = QUELLE.index('<div class="rw-feld">')
z = QUELLE.index('</p>', QUELLE.index('<p class="m-hilfe">', a)) + 4
FELD = QUELLE[a:z]
WM = re.search(r'<svg class="rw-kopf__wm".*?</svg>', QUELLE, re.S).group(0).replace('rw-kopf__wm', 'f2-wm')

T = []
for m in re.finditer(r'<li class="hz-z rw-g" style="--i:\d;--pk:(#\w+);--pa:(#\w+)" data-abend="[^"]+"><a href="([^"]+)" data-taste="(\d)">.*?'
                     r'<small class="rw-nr">N° \d · ([^<]+)</small><b class="rw-name">([^<]+)</b><span class="rw-stand" data-stand="([^"]+)">([^<]*)</span>', FELD, re.S):
    pk, pa, href, taste, art, name, stand, ersatz = m.groups()
    T.append(dict(k=re.search(r'/_werkzeuge/(\w+)/', href).group(1), pk=pk, pa=pa, href=href, taste=taste, art=html.unescape(art),
                  name=html.unescape(name), stand=stand, ersatz=html.unescape(ersatz)))
assert len(T) == 6, T
W = {t['k']: t for t in T}

WEB = open(os.path.join(HAUS, 'website', 'bau.py'), encoding='utf-8').read()
NAECHST = re.search(r"sw\('(Der Termin steht[^']*)'\)", WEB).group(1)
ZULETZT = re.search(r'<span class="mono">Zuletzt</span> ([^<]+)</p>', WEB).group(1)

# Je Werkzeug ein Foto, das zeigt, wofür es da ist
FOTO = {'bureau': 'fensterdraussen', 'carte': 'kartglas', 'imprimerie': 'pl23', 'reception': 'kerze2', 'livre': 'theke', 'registre': 'flur'}


def breiten(k):
    return sorted(int(f[len(k) + 1:-5]) for f in os.listdir(BILD) if f.startswith(k + '-') and f[len(k) + 1:-5].isdigit())


VORLADEN = []   # Bilder im ersten Bildschirm: im <head> vorgeladen (Fund Oberchef 29.10.2026: Hero-Bilder blieben im ersten Bild schwarz)


def motivfarbe(k):
    """Platzhalter in der Farbe des Motivs statt Schwarz: Mittelwert des kleinsten Bildes."""
    im = Image.open(os.path.join(BILD, f'{k}-{breiten(k)[0]}.webp')).convert('RGB').resize((1, 1), Image.LANCZOS)
    return '#%02x%02x%02x' % im.getpixel((0, 0))


def img(k, sizes, cls='', lade='eager', extra=''):
    """lade='eager' heisst erster Bildschirm: sofort, mit Vorrang und vorgeladen; 'lazy' für Bilder, die erst beim Zeigen kommen."""
    b = breiten(k); gross = b[-1] if b[-1] <= 1600 else 1600
    w, h = Image.open(os.path.join(BILD, f'{k}-{b[-1]}.webp')).size
    srcset = ', '.join(f'/assets/bild/{k}-{x}.webp {x}w' for x in b if x <= 1600)
    pos = REG.get(k, {}).get('pos', '50% 50%')
    c = f' class="{cls}"' if cls else ''
    vorn = ''
    if lade == 'eager':
        vorn = ' fetchpriority="high"'
        VORLADEN.append(f'<link rel="preload" as="image" href="/assets/bild/{k}-{gross}.webp" imagesrcset="{srcset}" imagesizes="{sizes}" fetchpriority="high">')
    return (f'<img{c} src="/assets/bild/{k}-{gross}.webp" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" '
            f'alt="{e(REG.get(k, {}).get("alt", ""))}" style="object-position:{pos};background-color:{motivfarbe(k)}" loading="{lade}" decoding="async"{vorn}{extra}>')


def stand(t, cls=''):
    return f'<span class="{cls}" data-stand="{t["stand"]}">{e(t["ersatz"])}</span>'


PFEIL = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'


def f1():
    bilder = ''.join(img(k, '(max-width:700px) 50vw, 25vw') for k in ('barnacht', 'fassade', 'barlicht', 'schildnacht'))
    band = ''.join(f'<li class="hz-z" style="--pk:{t["pk"]}"><a href="{t["href"]}" data-taste="{t["taste"]}"><small>{e(t["art"])}</small>'
                   f'<b>{e(t["name"])}</b>{stand(t)}</a></li>' for t in T)
    return f'<div class="f1"><div class="f1-bilder">{bilder}</div><ul class="hz-tafel f1-band" aria-label="Alle Werkzeuge">{band}</ul></div>'


def f2():
    gang = ''.join(f'<li class="hz-z"><a href="{t["href"]}" data-taste="{t["taste"]}"><small>{e(t["art"])}</small><b>{e(t["name"])}</b>{stand(t)}</a></li>' for t in T)
    return (f'<div class="f2"><figure class="f2-foto">{img("coupe", "(max-width:700px) 50vw, 26vw")}</figure>'
            f'<div class="f2-karte">{WM}<p class="f2-menue">Menü</p><p class="f2-datum" data-heute>&nbsp;</p>'
            f'<ul class="hz-tafel" aria-label="Alle Werkzeuge">{gang}</ul><p class="f2-fuss">{e(bau.BAR)} · {e(bau.STRASSE)}</p></div>'
            f'<figure class="f2-foto">{img("kartglas", "(max-width:700px) 50vw, 26vw")}</figure></div>')


def f3():
    zeiten = [('Vor dem Abend', 'kanister', ('carte', 'imprimerie')), ('Mit den Gästen', 'kerze2', ('reception', 'bureau')),
              ('Nach dem Abend', 'lachen', ('registre', 'livre'))]
    sp = ''
    for titel, k, ws in zeiten:
        li = ''.join(f'<li class="hz-z"><a href="{W[w]["href"]}" data-taste="{W[w]["taste"]}"><b>{e(W[w]["name"])}</b>{stand(W[w])}</a></li>' for w in ws)
        sp += f'<section class="f3-zeit"><figure>{img(k, "(max-width:700px) 33vw, 22vw")}</figure><h2>{e(titel)}</h2><ul>{li}</ul></section>'
    return (f'<div class="f3"><div class="f3-abend">{img("barlicht", "(max-width:1000px) 92vw, 24vw", "f3-grund")}<p class="f3-k">Der nächste Abend</p><p class="f3-h">{e(NAECHST.split(". ")[0])}.</p>'
            f'<p class="f3-s">{e(NAECHST.split(". ", 1)[1])}</p><p class="f3-z"><span>Zuletzt</span>{e(ZULETZT)}</p>'
            f'<a class="f3-web" href="/abend.html" target="_blank" rel="noopener">Den Abend auf der Website ansehen</a></div>'
            f'<div class="f3-zeiten hz-tafel">{sp}</div></div>')


def f4():
    fe = ''.join(f'<li class="hz-z"><a href="{t["href"]}" data-taste="{t["taste"]}"><span class="f4-fenster">{img(FOTO[t["k"]], "(max-width:700px) 31vw, 15vw")}</span>'
                 f'<small>{e(t["art"])}</small><b>{e(t["name"])}</b>{stand(t)}</a></li>' for t in T)
    return (f'<div class="f4"><p class="f4-satz">Sechs Fenster in die Bar. Hinter jedem liegt, was den nächsten Abend vorbereitet.</p>'
            f'<ul class="hz-tafel f4-reihe" aria-label="Alle Werkzeuge">{fe}</ul></div>')


def f5():
    li = ''.join(f'<li class="hz-z"><a href="{t["href"]}" data-taste="{t["taste"]}" style="--pa:{t["pa"]}"><small>{e(t["art"])}</small><b>{e(t["name"])}</b>'
                 f'{stand(t, "f5-stand")}<i>{PFEIL}</i></a></li>' for t in T)
    bilder = img('fassade', '(max-width:700px) 92vw, 30vw', 'hz-bild hz-bild--ruhe an', extra=' data-vorschau="ruhe"')
    unter = f'<span data-vorschau="ruhe" class="an">{e(REG["fassade"]["alt"])}</span>'
    for i, t in enumerate(T):
        bilder += img(FOTO[t['k']], '(max-width:700px) 92vw, 30vw', 'hz-bild', 'lazy', f' data-vorschau="{i}"')
        unter += f'<span data-vorschau="{i}">{e(t["name"])} · {e(REG[FOTO[t["k"]]]["alt"])}</span>'
    return (f'<div class="f5"><ul class="hz-tafel f5-liste" aria-label="Alle Werkzeuge">{li}</ul>'
            f'<figure class="f5-bild"><div class="f5-rahmen">{bilder}</div><figcaption class="hz-unter" aria-live="polite">{unter}</figcaption></figure></div>')


def f6():
    def bon(i, t):
        return (f'<li class="hz-z" style="--d:{(-1) ** i * (0.5 + (i % 3) * 0.2):.2f}deg"><a href="{t["href"]}" data-taste="{t["taste"]}"><i class="f6-klammer"></i>'
                f'<small>{e(t["art"])}</small><b>{e(t["name"])}</b>{stand(t)}<span class="f6-ab">Öffnen {PFEIL}</span></a></li>')
    reihen = ''.join(f'<div class="f6-schiene"></div><ul class="f6-bons">{"".join(bon(i, t) for i, t in list(enumerate(T))[j:j + 3])}</ul>' for j in (0, 3))
    return (f'<div class="f6"><figure class="f6-pass">{img("kueche", "(max-width:700px) 92vw, 28vw")}</figure>'
            f'<div class="hz-tafel f6-haken" aria-label="Alle Werkzeuge">{reihen}</div></div>')


FASSUNGEN = [
    (1, 'Drei Fenster am Abend', 'Die Bar von draussen bei Nacht über die ganze Breite, darunter die sechs Werkzeuge als eine dunkle Leiste.', f1),
    (2, 'Das Gedeck', 'Die Werkzeuge stehen wie die Gänge auf einer Culinarium-Menükarte, links und rechts Drink und Gläser wie am Platz.', f2),
    (3, 'Der Abend in drei Zeiten', 'Was vor dem Abend, mit den Gästen und danach zu tun ist, daneben der nächste Abend, wie die Website ihn nennt.', f3),
    (4, 'Die Fassade bei Nacht', 'Sechs Fenster in einer Reihe auf der dunklen Wand, hinter jedem das Bild, das zeigt, wofür das Werkzeug da ist.', f4),
    (5, 'Die ruhige Liste', 'Sechs Namen gross untereinander, daneben ein grosses Foto, das beim Zeigen auf einen Namen dessen Bild zeigt.', f5),
    (6, 'Die Bons am Pass', 'Neben den Köchen am Pass hängen die sechs Werkzeuge wie Bons an zwei Schienen, jeder mit seinem Stand.', f6),
]

DATUM = ("<script>(function(){var d=document.querySelector('[data-heute]');if(d)d.textContent=new Date().toLocaleDateString('de-DE',"
         "{weekday:'long',day:'numeric',month:'long',year:'numeric'});})();</script>")


def seite(n, name, satz, fn):
    VORLADEN.clear()
    h = QUELLE[:a] + fn() + QUELLE[z:]
    h = h.replace('<head>', '<head>\n<base href="../">\n' + '\n'.join(dict.fromkeys(VORLADEN)), 1)
    h = re.sub(r'<title>[^<]*</title>', f'<title>Der Tresen · Hero {n}: {e(name)}</title>', h, count=1)
    h = h.replace('</head>', '<link rel="stylesheet" href="wahl-hero/hero.css">\n</head>', 1)
    h = h.replace('<section class="m-empfang rw tapete"', f'<section class="m-empfang rw tapete wahl f{n}-empfang"', 1)
    h = h.replace('</body>', DATUM + '\n</body>', 1)
    open(os.path.join(HIER, f'hero-{n}.html'), 'w', encoding='utf-8').write(h)


if __name__ == '__main__':
    for f in FASSUNGEN:
        seite(*f)
    print('gebaut:', ', '.join(f'hero-{n}.html' for n, *_ in FASSUNGEN))
