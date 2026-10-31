#!/usr/bin/env python3
"""Culinarium Hannover · Team-Hero (leute.html): Satz und Knopf am unteren Rand neu setzen, 28.10.2026.
Satz neu und ohne Knopf seit 28.10.2026 (Robert: «getragen» raus, Knopf im Hero führt woandershin, macht keinen Sinn).
Robert: «nicht schön gelöst im Hero mit dem Button unten rechts und dem Text unten links … wie man diese beiden Elemente
unten rechts und unten links nochmal irgendwie anders verwursten kann».
Nur Satz und Knopf ändern sich; Bild, Freisteller, Titel und Verläufe bleiben genau wie in leute.html. Fassung 0 ist der heutige Stand.
Baut leute-unten-wahl.html. Aufruf: python3 website/team_unten_wahl.py (liest das fertige leute.html)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bau import HIER, VERSION, PFEIL

R = '.tu%d .sa-ueber'
F = []   # (Name, at-text-HTML, CSS am Desktop, CSS am Handy; am Handy gilt sonst der heutige Stand: untereinander, links)


def satz(i=2, cls=''):
    return '<p class="sw auf at-satz%s" style="--i:%d">Die Menschen hinter Culinarium und dem Walk on the Wild Side.</p>' % (
        (' ' + cls) if cls else '', i)


def knoepfe(i=4):
    return ('<div class="knoepfe sw auf" style="--i:%d"><a class="knopf" href="abend.html" aria-label="Der Abend"><span>Der Abend</span><i>%s</i></a></div>' % (i, PFEIL))


def zeile(i=4):
    """Der Knopf als feine Zeile: Versalien und der Kerzen-Kreis mit Pfeil."""
    return '<a class="sw auf tu-zeile" style="--i:%d" href="abend.html"><span>Der Abend</span><i>%s</i></a>' % (i, PFEIL)


def at(inner, cls=''):
    return '<div class="at-text%s">%s</div>' % ((' ' + cls) if cls else '', inner)


# Auf der Mittelachse: der Satz steht mittig unter dem Titel, wie Leiste und Titel
F.append(('Auf der Mittelachse', at(satz()), '''
{r} .at-text{{flex-direction:column;align-items:center;justify-content:flex-end;text-align:center;gap:20px}}
{r} .at-satz{{max-width:640px;font-size:21px}}
''', '''{r} .at-text{{align-items:center;text-align:center}} {r} .at-satz{{font-size:19px}}'''))

# Die Bauchbinde: eine helle Linie über die ganze Breite, darunter der Satz
F.append(('Die Bauchbinde', at(satz()), '''
{r} .at-text{{align-items:center;padding-top:24px;border-top:1px solid rgba(250,244,244,.3)}}
{r} .at-satz{{max-width:none;font-size:20px}}
{r} .knopf{{margin-top:0}}
''', ''))

# Rechts: rechtsbündig in der rechten Ecke
F.append(('Rechts', at(satz()), '''
{r} .at-text{{flex-direction:column;align-items:flex-end;text-align:right;gap:20px}}
{r} .at-satz{{max-width:520px;font-size:21px}}
''', '''{r} .at-text{{align-items:flex-end}}'''))

# Die Unterzeile: der Satz in Fraunces gross und mittig
F.append(('Die Unterzeile', at(satz()), '''
{r} .at-text{{flex-direction:column;align-items:center;text-align:center;gap:22px}}
{r} .at-satz{{max-width:980px;font:300 clamp(24px,2.3vw,36px)/1.25 var(--titel);letter-spacing:-.01em;color:#FAF4F4}}
''', '''{r} .at-text{{align-items:center;text-align:center}} {r} .at-satz{{font:300 24px/1.25 var(--titel);color:#FAF4F4}}'''))

# Der Streifen: ein Streifen Nacht über die ganze Breite deckt den unteren Bildrand, darin der Satz; Bild, Freisteller und Titel bleiben wie heute
F.append(('Der Streifen', at(satz()), '''
{r}{{--st:150px}}
{r} .at-text{{left:0;right:0;bottom:0;height:var(--st);padding:0 var(--rand);background:#16151A;align-items:center;justify-content:center;gap:56px}}
{r} .at-satz{{max-width:560px;font-size:21px}}
{r} .knopf{{margin-top:0}}
''', '''{r}{{--st:210px}} {r} .at-text{{left:0;right:0;bottom:0;height:var(--st);padding:0 18px;background:#16151A;justify-content:center}}'''))

# Die Tafel: ein breites Feld in Nacht, mittig unten, darin der Satz
F.append(('Die Tafel', at(satz()), '''
{r} .at-text{{left:0;right:0;margin:0 auto;width:min(1000px,calc(100% - 2*var(--rand)));align-items:center;gap:40px;padding:24px 36px;background:#16151A;justify-content:center;text-align:center;border-radius:6px;box-shadow:0 24px 60px -24px rgba(0,0,0,.8)}}
{r} .at-satz{{max-width:none;font-size:20px}}
{r} .knopf{{margin-top:0;flex:none}}
''', '''{r} .at-text{{padding:22px;background:#16151A;border-radius:6px}}'''))

# Gross über die Breite: der Satz in Fraunces über zwei Drittel der Breite
F.append(('Gross über die Breite', at(satz()), '''
{r} .at-text{{align-items:flex-end;gap:48px}}
{r} .at-satz{{max-width:min(980px,64vw);font:300 clamp(26px,2.7vw,42px)/1.2 var(--titel);letter-spacing:-.01em;color:#FAF4F4}}
{r} .knopf{{margin-top:0;margin-bottom:4px}}
''', '''{r} .at-satz{{font:300 24px/1.25 var(--titel);color:#FAF4F4}}'''))

GEMEINSAM = '''
#wleiste{bottom:auto;top:74px;width:min(1180px,calc(100vw - 16px))}  /* der untere Rand des Heros ist das, was gewählt wird: Leiste nach oben */
#wleiste .wl-kopf{margin-bottom:0}
#wleiste .wl-daumen{display:none}
#unten.vab{padding:0}  /* in leute.html über .vab:has(>.vi.sa); hier steckt der Kopf eine Ebene tiefer */
.tu-zeile{display:inline-flex;align-items:center;gap:14px;color:#FAF4F4;text-decoration:none;font:700 12.5px/1 var(--etikett);letter-spacing:.14em;text-transform:uppercase}
.tu-zeile i{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--kerze);color:#fff}
.tu-zeile svg{width:18px;height:18px;transition:transform .8s var(--k)}
.tu-zeile:hover svg{transform:translateX(3px)}
'''


def main():
    seite = open(os.path.join(HIER, 'leute.html')).read()
    m = re.search(r'<section class="(vab bar-ab v-lt-kopf[^"]*)"([^>]*)>(.*?)</section>', seite, re.S)
    assert m, 'Kopf in leute.html nicht gefunden'
    inner = m.group(3)
    a = re.search(r'<div class="at-text">.*?</p></div>', inner, re.S)
    assert a, 'Satz im Kopf nicht gefunden'
    teile = ['<div class="wv tu tu0" data-n="0">%s</div>' % inner]
    css = [GEMEINSAM]
    for i, (_n, html, c, h) in enumerate(F, 1):
        teile.append('<div class="wv tu tu%d" data-n="%d" hidden>%s</div>' % (i, i, inner[:a.start()] + html + inner[a.end():]))
        css.append('@media (min-width:861px){%s}' % c.format(r=R % i))
        if h:
            css.append('@media (max-width:860px){%s}' % h.format(r=R % i))
    neu = '<section class="%s wahl"%s id="unten" data-name="Satz"><div class="wahl-marke"><b>Team</b><span data-nr></span></div>%s</section>' % (m.group(1), m.group(2), ''.join(teile))
    seite = seite[:m.start()] + neu + seite[m.end():]
    namen = ['Heute: Satz unten links'] + [n for n, _h, _c, _m in F]
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["unten"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>''' % (json.dumps(namen, ensure_ascii=False), VERSION)
    seite = seite.replace('<title>', '<title>Team-Hero unten wählen · ', 1)
    seite = seite.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<style>%s</style>\n</head>' % (VERSION, ''.join(css)), 1)
    seite = seite.replace('</body>', leiste + '\n</body>', 1)
    open(os.path.join(HIER, 'leute-unten-wahl.html'), 'w').write(seite)
    print('Seite leute-unten-wahl.html', len(seite) // 1024, 'KB,', len(F), 'Fassungen + heute')


if __name__ == '__main__':
    main()
