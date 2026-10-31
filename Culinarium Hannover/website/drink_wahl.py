#!/usr/bin/env python3
"""Culinarium Hannover · Seite «Das Haus» (bar.html), Abschnitt «Dein Drink, nach deinem Geschmack.», Runde 3, 27.10.2026.
Runde 2 Nr. 9 ist eingebaut (Robert «9»), danach Robert: «nochmal 15 weitere alternative Visualisierungen, das gefällt mir nicht».
Robert zu Runde 1: «alle super leer, nicht zur Seite passend, wenig da für viel Platz» (Runde 1 gesichert als drink_wahl.py.vor-runde2-2026-10-27).
Darum jetzt in der echten Seite: bar.html mit ihrer Schrift, ihren Farben und der Bildwand mit Fuge; der Abschnitt ist an seinem Platz
in 16 Fassungen umschaltbar (0 = heute), wie wahl.html. Jede Fassung dicht: sechs bis zwölf Fotos, Text und Titel ohne Leerflächen,
wo es passt mit Inhalt aus den Quellen (Momos Techniken aus Beitrag DbYnkdkjrNy, Derya und Momo).
Baut drink-wahl.html. Aufruf: python3 website/bau.py && python3 website/drink_wahl.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bau
from bau import E, foto, zl, sw

HIER = bau.HIER
bau.META.update(json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json'))))   # nur lesen, keine Bilder neu rechnen

TEXT = ('Eine Getränkekarte gibt es im Walk on the Wild Side nicht. Wer an die Theke kommt, erzählt, was er mag, '
        'und bekommt seinen eigenen Drink. Seit dem Reopening am 9. November 2023 führt Derya Ivkin die Bar, '
        'Momo steht mit ihr hinter der Theke.')
ZEILEN = ['Dein Drink,', 'nach deinem Geschmack.']
TECHNIKEN = (('Fatwashing', 'Die Spirituose nimmt den Geschmack eines Fetts an; kalt gestellt, wird das Fett wieder abgehoben.'),
             ('Milkwashing', 'Milch bindet die Trübstoffe und wird abgefiltert, der Drink wird klar und weich.'),
             ('Enzyme', 'Enzyme lösen die Trübung aus Fruchtsaft, der Geschmack bleibt.'))
R = 'clamp(200px,21vw,320px)'


def T(cls=''):
    return zl(ZEILEN, 'h2', 'fwk-titel' + (' ' + cls if cls else ''))


def X(i=1):
    return sw(TEXT, 'p', 'fwk-text', i)


def f(k, pos=None, sizes='(max-width:860px) 50vw, 25vw'):
    return foto(k, '', sizes, auf=False, pos=pos)


def z(k, st='', pos=None, sizes='(max-width:860px) 50vw, 25vw', name=''):
    return '<div style="%s">%s%s</div>' % (st, f(k, pos, sizes), '<p class="dw-name">%s</p>' % E(name) if name else '')


def wand(raster, zellen, cls=''):
    return '<div class="fw flaeche auf %s" style="%s">%s</div>' % (cls, raster, ''.join(zellen))


def fwk(extra=''):
    return '<div class="fwk"><div class="fwk-l">%s</div><div class="fwk-r"><div>%s%s</div></div></div>' % (T(), X(), extra)


def kblock(extra='', cls=''):
    return '<div class="dw-k %s">%s%s%s</div>' % (cls, T(), X(), extra)


NAMEN = ('<ul class="vn sw auf" style="--i:2"><li><b>Derya Ivkin</b><span>führt die Bar</span></li>'
         '<li><b>Momo</b><span>hinter der Theke</span></li></ul>')
TECH_DL = '<dl class="vt sw auf" style="--i:2">%s</dl>' % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (E(a), E(b)) for a, b in TECHNIKEN)


def tech_karte(st, dunkel=False):
    return ('<div class="fw-karte%s" style="%s"><p class="fk-zeile">MOMOS TECHNIKEN</p>%s<p class="fk-fuss">Statt einer Getränkekarte</p></div>'
            % (' dunkel' if dunkel else '', st, ''.join('<div class="fk-gang"><p>%s</p></div>' % E(a.upper()) for a, _ in TECHNIKEN)))


F = []   # (Haltung, HTML)
# Runde 3 (Robert 27.10.2026 nach Einbau von Runde 2 Nr. 9: «nochmal 15 weitere, das gefällt mir nicht»).
# Keine Fassung wiederholt eine aus Runde 2 (gesichert als drink_wahl.py.vor-runde3-2026-10-27) oder den Stand vor Nr. 9.


def ov(titel, satz):
    """Schrift unten im Bild, auf einem Verlauf ins Dunkle."""
    return '<div class="dw-ov"><h3>%s</h3><p>%s</p></div>' % (E(titel), E(satz))


def zov(k, st, titel, satz, pos=None, sizes='(max-width:860px) 50vw, 33vw'):
    return '<div style="%s">%s%s</div>' % (st, f(k, pos, sizes), ov(titel, satz))


# 01 Kopf unten: zuerst die Wand mit acht Fotos, darunter Titel links und Text mit Techniken rechts
F.append(('Kopf unten', '<div class="dw-unten">%s<div class="fwk"><div class="fwk-l">%s</div><div class="fwk-r"><div>%s%s</div></div></div></div>' % (wand(
    'grid-template-columns:1fr 1.3fr 1fr 1fr;grid-template-rows:repeat(2,clamp(180px,18vw,280px))',
    [z('ws12', 'grid-column:1;grid-row:1'), z('barneg', 'grid-column:2;grid-row:1/3', None, '(max-width:860px) 50vw, 32vw'), z('d3', 'grid-column:3;grid-row:1'), z('g2', 'grid-column:4;grid-row:1'),
     z('kanister', 'grid-column:1;grid-row:2'), z('schaum', 'grid-column:3;grid-row:2'), z('coupe', 'grid-column:4;grid-row:2')]), T(), X(), TECH_DL)))

# 02 Flügel: links und rechts je zwei Fotos übereinander, in der Mitte Titel, Text und Techniken
FL = 'grid-template-columns:1fr;grid-template-rows:repeat(2,clamp(220px,21vw,320px))'
F.append(('Flügel', '<div class="dw-fl">%s%s%s</div>' % (
    wand(FL, [z(k, sizes='(max-width:860px) 50vw, 28vw') for k in ('theke', 'ws29')]),
    kblock(TECH_DL, 'dw-flm'),
    wand(FL, [z(k, pos=p, sizes='(max-width:860px) 50vw, 28vw') for k, p in (('g5', None), ('glasnacht', '50% 58%'))]))))

# 03 Bild mit Text darauf: die Theke gross mit Titel und Text im Bild, rechts zwei Fotos, darunter vier
F.append(('Bild mit Text darauf', wand(
    'grid-template-columns:1fr 1fr 1fr 1fr;grid-template-rows:clamp(230px,22vw,330px) clamp(230px,22vw,330px) clamp(170px,15vw,230px)',
    ['<div class="dw-bild" style="grid-column:1/4;grid-row:1/3">%s<div class="dw-ovk">%s%s</div></div>' % (
        f('theke2', '50% 40%', '(max-width:860px) 100vw, 72vw'), T(), X()),
     z('ws31', 'grid-column:4;grid-row:1'), z('d3', 'grid-column:4;grid-row:2')] +
    [z(k, 'grid-column:%d;grid-row:3' % (i + 1)) for i, k in enumerate(('ws29', 'schaum', 'kanister', 'g4'))])))

# 04 Mittig: Titel und Text mittig, darunter fünf Spalten, hoch und quer gemischt
F.append(('Mittig über fünf Spalten', kblock(cls='dw-mitte') + wand(
    'grid-template-columns:repeat(5,1fr);grid-template-rows:repeat(2,clamp(170px,16vw,250px))',
    [z('momo', 'grid-column:1;grid-row:1/3', '50% 40%', '(max-width:860px) 50vw, 20vw'), z('d3', 'grid-column:2;grid-row:1'), z('ws12', 'grid-column:2;grid-row:2'),
     z('glasnacht', 'grid-column:3;grid-row:1/3', '50% 58%', '(max-width:860px) 50vw, 20vw'), z('schaum', 'grid-column:4;grid-row:1'), z('klaeren', 'grid-column:4;grid-row:2'),
     z('theke', 'grid-column:5;grid-row:1/3', '50% 40%', '(max-width:860px) 50vw, 20vw')])))

# 05 Paar gross: zwei hohe Fotos nebeneinander, rechts Titel, Text, Techniken und ein kleines Foto
F.append(('Paar gross', '<div class="dw-paar">%s%s</div>' % (wand(
    'grid-template-columns:1fr 1fr;grid-template-rows:clamp(460px,44vw,660px)',
    [z('glas', '', '50% 55%', '(max-width:860px) 50vw, 30vw'), z('momo', '', '50% 40%', '(max-width:860px) 50vw, 30vw')]),
    kblock(TECH_DL + '<div class="fw dw-klein sw auf" style="--i:3">%s</div>' % z('coupe')))))

# 06 Techniken im Bild: drei hohe Fotos, je eine Technik unten im Bild, darunter drei weitere Fotos
F.append(('Techniken im Bild', fwk() + wand(
    'grid-template-columns:repeat(3,1fr);grid-template-rows:clamp(300px,28vw,420px) clamp(170px,15vw,230px)',
    [zov(k, 'grid-column:%d;grid-row:1' % (i + 1), a, b) for i, (k, (a, b)) in enumerate(zip(('klaeren', 'kanister', 'm3'), TECHNIKEN))] +
    [z(k, 'grid-column:%d;grid-row:2' % (i + 1), sizes='(max-width:860px) 50vw, 33vw') for i, k in enumerate(('ws12', 'd3', 'schaum'))])))

# 07 Versetzte Spalten: vier Spalten mit Fotos, jede etwas anders hoch, in der ersten oben der Text
SP = (('ws31', 'theke'), ('d3', 'g1', 'ws12'), ('schaum', 'barneg'), ('g4', 'klaeren', 'ws28'))
F.append(('Versetzte Spalten', '<div class="dw-vs flaeche auf">%s</div>' % ''.join(
    '<div class="dw-sp" style="--v:%dpx">%s%s</div>' % (v, kblock(cls='dw-vsk') if i == 0 else '',
                                                      ''.join('<div class="dw-sb">%s</div>' % f(k, sizes='(max-width:860px) 50vw, 24vw') for k in sp))
    for i, (sp, v) in enumerate(zip(SP, (0, 70, 24, 110))))))

# 08 Zickzack: oben Text links und zwei Fotos rechts, unten drei Fotos links und die Techniken rechts
F.append(('Zickzack', '<div class="dw-zz"><div class="dw-z1">%s%s</div><div class="dw-z2">%s<div class="dw-k sw auf" style="--i:2">%s</div></div></div>' % (
    kblock(),
    wand('grid-template-columns:1fr 1fr;grid-template-rows:clamp(280px,26vw,400px)', [z(k, sizes='(max-width:860px) 50vw, 30vw') for k in ('theke', 'ws12')]),
    wand('grid-template-columns:repeat(3,1fr);grid-template-rows:clamp(220px,20vw,300px)', [z(k, sizes='(max-width:860px) 50vw, 20vw') for k in ('d3', 'schaum', 'glasnacht')]),
    TECH_DL)))

# 09 Quadrat und Reihe: vier Fotos im Quadrat links, rechts Text mit Derya und Momo, darunter eine Reihe über alles
F.append(('Quadrat und Reihe', '<div class="dw-qr">%s%s</div>%s' % (
    wand('grid-template-columns:1fr 1fr;grid-template-rows:repeat(2,clamp(190px,18vw,280px))', [z(k, sizes='(max-width:860px) 50vw, 26vw') for k in ('w3', 'momo_hoch', 'd3', 'schaum')]),
    kblock(NAMEN),
    '<div class="dw-abst">%s</div>' % wand('grid-template-columns:repeat(4,1fr);grid-template-rows:clamp(170px,15vw,230px)', [z(k) for k in ('ws29', 'kanister', 'g5', 'ws31')]))))

# 10 Kopf mit zwei kleinen: zwei schräg gelegte kleine Fotos neben dem Text (wie auf den anderen Seiten), darunter vier hohe
MINI = ''.join('<div class="tq-mini" style="--d:%sdeg;--i:%d">%s</div>' % (d, i, f(m, sizes='(max-width:860px) 30vw, 12vw')) for i, (m, d) in enumerate((('d2', -4), ('g4', 3))))
F.append(('Kopf mit zwei kleinen', '<div class="fwk"><div class="fwk-l">%s</div><div class="fwk-r"><div class="fwk-minis staffel auf">%s</div><div>%s</div></div></div>' % (T(), MINI, X()) + wand(
    'grid-template-columns:repeat(4,1fr);grid-template-rows:clamp(320px,31vw,470px)',
    [z(k, pos=p) for k, p in (('ws28', None), ('momo', '50% 40%'), ('klaeren', None), ('schaumglas', None))])))

# 11 Hoch und Stapel: ein hohes Foto links, rechts Titel und Text, darunter vier kleine im Quadrat
F.append(('Hoch und Stapel', '<div class="dw-hs">%s<div class="dw-k">%s%s%s</div></div>' % (
    wand('grid-template-columns:1fr;grid-template-rows:clamp(520px,50vw,740px)', [z('momo', '', '50% 40%', '(max-width:860px) 100vw, 44vw')]),
    T(), X(),
    wand('grid-template-columns:1fr 1fr;grid-template-rows:repeat(2,clamp(140px,12vw,190px))', [z(k, sizes='(max-width:860px) 50vw, 20vw') for k in ('d3', 'schaum', 'g2', 'kanister')], 'dw-st4'))))

# 12 Kontaktbogen: Kopf wie heute, darunter zwölf Fotos in zwei Reihen
K12 = ('ws12', 'theke', 'd3', 'g2', 'schaum', 'm1', 'ws28', 'ws31', 'klaeren', 'kanister', 'g5', 'glasnacht')
F.append(('Kontaktbogen', fwk() + wand(
    'grid-template-columns:repeat(6,1fr);grid-template-rows:repeat(2,clamp(150px,14vw,220px))',
    [z(k, sizes='(max-width:860px) 50vw, 17vw') for k in K12])))

# 13 Hoch und tief: links ein Foto oben, rechts eins tief, der Text dazwischen, unter dem Text ein kleines
F.append(('Hoch und tief', '<div class="dw-ht"><div class="dw-hoch">%s</div><div class="dw-k">%s%s<div class="fw dw-klein sw auf" style="--i:3">%s</div></div><div class="dw-tief">%s</div></div>' % (
    wand('grid-template-columns:1fr;grid-template-rows:clamp(380px,36vw,540px) clamp(150px,13vw,200px)', [z('theke', '', '50% 40%', '(max-width:860px) 50vw, 30vw'), z('kanister', '', None, '(max-width:860px) 50vw, 30vw')]),
    T(), X(), z('d3'),
    wand('grid-template-columns:1fr;grid-template-rows:clamp(400px,38vw,560px)', [z('glasnacht', '', '50% 58%', '(max-width:860px) 50vw, 30vw')]))))

# 14 Rahmen: acht Fotos rund um ein dunkles Feld mit dem Titel, darunter Text und Techniken nebeneinander
R14 = 'clamp(160px,15vw,230px)'
F.append(('Rahmen', wand(
    'grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(3,%s)' % R14,
    [z('ws12', 'grid-column:1;grid-row:1'), z('theke', 'grid-column:2;grid-row:1'), z('d3', 'grid-column:3;grid-row:1'), z('g2', 'grid-column:4;grid-row:1'),
     z('schaum', 'grid-column:1;grid-row:2'),
     '<div class="fw-karte dunkel dw-tk" style="grid-column:2/4;grid-row:2;justify-content:center">%s</div>' % T('dw-kt'),
     z('m1', 'grid-column:4;grid-row:2'),
     z('klaeren', 'grid-column:1;grid-row:3'), z('kanister', 'grid-column:2;grid-row:3'), z('g5', 'grid-column:3;grid-row:3'), z('glasnacht', 'grid-column:4;grid-row:3')]) +
    '<div class="dw-zwei">%s%s</div>' % (X(), TECH_DL)))

# 15 Reihe oben, Bühne unten: fünf kleine Quadrate oben, darunter ein grosses Foto und rechts Titel, Text, Techniken
F.append(('Reihe oben, Bühne unten', wand(
    'grid-template-columns:repeat(5,1fr);grid-template-rows:clamp(150px,14vw,210px)',
    [z(k, sizes='(max-width:860px) 50vw, 20vw') for k in ('ws12', 'd3', 'schaum', 'kanister', 'g4')]) +
    '<div class="dw-bu">%s%s</div>' % (
        wand('grid-template-columns:1fr;grid-template-rows:clamp(380px,36vw,540px)', [z('barneg', '', None, '(max-width:860px) 100vw, 56vw')]),
        kblock(TECH_DL))))


CSS = '''/* Wahl «Dein Drink», Runde 3 (drink_wahl.py). Nur für die Wahlseite. */
.dw-k{display:flex;flex-direction:column;gap:22px}
.dw-k .fwk-titel{font-size:clamp(44px,5vw,86px)}
.dw-kt{font-size:clamp(36px,3.6vw,62px);color:#FAF4F4}
.dw-tk{align-items:flex-start;text-align:left;gap:22px;padding:clamp(24px,2.8vw,44px)}
.dw-unten .fwk{margin:clamp(28px,4.5vh,52px) 0 0;align-items:start}
.dw-fl{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr) minmax(0,1fr);gap:clamp(22px,3vw,52px);align-items:center}
.dw-flm .fwk-titel{font-size:clamp(40px,4.2vw,72px)}
.dw-ov{position:absolute;z-index:2;left:0;right:0;bottom:0;padding:60px clamp(16px,1.6vw,26px) clamp(16px,1.6vw,24px);background:linear-gradient(0deg,rgba(12,10,14,.9),rgba(12,10,14,.6) 55%,rgba(12,10,14,0))}
.dw-ov h3{margin:0 0 6px;font:340 clamp(24px,2.2vw,34px)/1 var(--titel);font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 72;color:#FAF4F4}
.dw-ov p{margin:0;font-size:14px;line-height:1.5;color:rgba(250,244,244,.82);max-width:36ch}
.dw-bild .dw-ovk{position:absolute;z-index:2;inset:auto 0 0 0;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(20px,3vw,48px);align-items:end;padding:120px clamp(22px,3vw,48px) clamp(22px,3vw,40px);background:linear-gradient(0deg,rgba(12,10,14,.92),rgba(12,10,14,.7) 50%,rgba(12,10,14,0))}
.dw-bild .fwk-titel{font-size:clamp(40px,4.4vw,76px);color:#FAF4F4}
.dw-bild .fwk-text{color:rgba(250,244,244,.82)}
.dw-mitte{align-items:center;text-align:center;margin:0 auto clamp(28px,4.5vh,52px);max-width:760px}
.dw-mitte .fwk-text{max-width:56ch}
.dw-paar{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr);gap:clamp(28px,4vw,64px);align-items:center}
.dw-klein{grid-template-rows:clamp(150px,13vw,200px);width:100%}
.dw-vs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;align-items:start}
.dw-sp{display:flex;flex-direction:column;gap:12px;margin-top:var(--v)}
.dw-sb{height:clamp(200px,19vw,290px);overflow:hidden;border-radius:4px}
.dw-sb .foto{height:100%;width:100%;border-radius:0}
.dw-vsk{gap:16px;padding-bottom:10px}
.dw-vsk .fwk-titel{font-size:clamp(34px,3.3vw,56px)}
.dw-vsk .fwk-text{font-size:clamp(14px,1.05vw,16px)}
.dw-zz{display:grid;gap:clamp(24px,4vh,44px)}
.dw-z1{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:clamp(28px,4vw,64px);align-items:end}
.dw-z2{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.7fr);gap:clamp(28px,4vw,64px);align-items:center}
.dw-qr{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(28px,4vw,64px);align-items:center}
.dw-abst{margin-top:clamp(20px,3vh,32px)}
.dw-hs{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,4vw,64px);align-items:end}
.dw-st4{width:100%}
.dw-ht{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.9fr) minmax(0,1fr);gap:clamp(22px,3vw,52px);align-items:start}
.dw-tief{margin-top:clamp(60px,8vw,120px)}
.dw-ht .dw-k{padding-top:clamp(20px,4vw,60px)}
.dw-ht .fwk-titel{font-size:clamp(40px,4.2vw,72px)}
.dw-zwei{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,4vw,64px);margin-top:clamp(24px,3.6vh,40px);align-items:start}
.dw-bu{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.7fr);gap:clamp(28px,4vw,64px);align-items:center;margin-top:clamp(20px,3vh,32px)}
@media (max-width:860px){
  .dw-fl,.dw-paar,.dw-z1,.dw-z2,.dw-qr,.dw-hs,.dw-ht,.dw-zwei,.dw-bu{grid-template-columns:1fr}
  .dw-fl>.fw{grid-template-rows:none!important}
  .dw-bild{grid-column:1/-1!important;grid-row:span 3!important}
  .dw-bild .dw-ovk{grid-template-columns:1fr;padding-top:60px}
  .dw-vs{grid-template-columns:1fr 1fr}.dw-sp{margin-top:0}.dw-sp:first-child{grid-column:1/-1}.dw-sb{height:46vw}
  .dw-tief{margin-top:0}
  .dw-klein{grid-auto-rows:46vw}
}
'''

JS = r'''<script>
(function () {
  // Laufband (Fassung 11): Fortschritt als --p, nur transform
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function lauf() {
    document.querySelectorAll('[data-zieh]').forEach(function (el) {
      var r = el.getBoundingClientRect(), vh = innerHeight;
      var p = still ? .5 : Math.min(1, Math.max(0, (vh - r.top) / (vh + r.height)));
      el.style.setProperty('--p', p.toFixed(4));
    });
  }
  var t = false;
  addEventListener('scroll', function () { if (!t) { t = true; requestAnimationFrame(function () { t = false; lauf(); }); } }, { passive: true });
  addEventListener('resize', lauf); addEventListener('load', lauf); lauf();
})();
</script>'''

NAMEN_W = ['Heute'] + [n for n, _ in F]


def main():
    s = open(os.path.join(HIER, 'bar.html'), encoding='utf-8').read()
    i = s.index('v-bar-karte')
    a = s.rindex('<section', 0, i)
    b = s.index('</section>', i) + len('</section>')
    heute = s[a:b]
    teile = ['<div class="wv" data-n="0">%s</div>' % heute]
    for n, (_name, html) in enumerate(F, 1):
        teile.append('<div class="wv" data-n="%d" hidden><section class="vab bar-ab v-bar-karte dw%d" data-ton="warm"><div class="vi h-wand2">%s</div></section></div>' % (n, n, html))
    block = '<div class="wahl" id="drink" data-name="Dein Drink"><div class="wahl-marke"><b>Dein Drink</b><span data-nr>Fassung 0 · Heute</span></div>%s</div>' % ''.join(teile)
    s = s[:a] + block + s[b:]
    s = s.replace('<title>', '<title>Auswahl · Dein Drink · ', 1)
    s = s.replace('</head>', '<link rel="stylesheet" href="assets/wahl.css?v=%s">\n<style>\n%s\n</style>\n</head>' % (bau.VERSION, CSS), 1)
    leiste = '''<div id="wleiste"><div class="wl-kopf"><div class="wl-ab"><b data-wl-ab></b><span data-wl-nr></span><span data-wl-name></span></div>
<div class="wl-wahl" data-wl-wahl></div><div class="wl-knoepfe"><button type="button" data-wl-zur aria-label="Vorige Fassung">‹</button><button type="button" data-wl-vor aria-label="Nächste Fassung">›</button></div></div>
<div class="wl-daumen" data-wl-daumen></div></div>
<script>window.WAHL={namen:%s,ids:["drink"],daumen:false};</script>
<script src="assets/wahl.js?v=%s" defer></script>
%s''' % (json.dumps(NAMEN_W, ensure_ascii=False), bau.VERSION, JS)
    s = s.replace('</body>', leiste + '</body>', 1)
    ziel = os.path.join(HIER, 'drink-wahl.html')
    open(ziel, 'w', encoding='utf-8').write(s)
    print(ziel, len(F), 'Fassungen', len(s) // 1024, 'KB')


if __name__ == '__main__':
    main()
