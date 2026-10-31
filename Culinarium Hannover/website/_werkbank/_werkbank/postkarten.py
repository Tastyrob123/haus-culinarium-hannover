#!/usr/bin/env python3
"""Culinarium: Postkarten aller Plakate (Prüfchat Gestaltung 29.10.2026, Robert: «aus den bestehenden Plakaten … für jedes Plakat, was sie bisher
hatten, so eine richtig schöne Postkarte … Das können sie dann so bei sich auslegen im Laden»).
Eine Karte je echtem Plakat (13 Abende seit September 2023, das erste Pop-up im Mai 2023, das erste Dirty-Chicken-Pop-up). Vorn A6 hoch: das Plakat ganz,
nie angeschnitten, auf einem Rand in der Farbe des Motivs. Hinten A6 quer im Stil der Postkarte: links Abend, Datum, Name des Motivs und klein der Ort,
rechts Platz zum Schreiben mit Adresslinien und ein Markenfeld mit dem C. Druck-PDF mit 3 mm Beschnitt, Sammelbogen SRA3, Fächer und Kartenständer als Bild.
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/postkarten.py "<website/_werkbank>"            → satz/postkarten*.html, postkarten_plan.json
   node _werkbank/postkarten_druck.js "<…>"   dann   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/postkarten.py "<…>" --seite"""
import json, os, sys
import papier_kern as P
from papier_kern import blatt, e, t
import kern as K
from kern import H, ROOT, W, kn, titel, kap, zahl
import papier_neu as N

PROJ = N.PROJ
VORL = json.load(open(os.path.join(N.VORL, 'abendplakat.json'), encoding='utf-8'))['vorlagen']
MOT = {m['key'][3:]: m for m in json.load(open(os.path.join(PROJ, '_werkzeuge', 'imprimerie', 'haeuser', 'culinarium', 'motive.json'), encoding='utf-8'))}
BX = {b['key']: b for b in json.load(open(os.path.join(PROJ, '_werkzeuge', 'imprimerie', 'haeuser', 'culinarium', 'marke.json'), encoding='utf-8'))['bilder']}
B = 3   # Beschnitt


def karten():
    K_ = []
    # die zwei Pop-up-Plakate sind keine Vorlagen mehr in abendplakat.json (Gestaltung 29.10.), haben aber je eine Postkarte: 13 Abende + 2 = 15
    keys = [v['inhalt']['bild'] for v in VORL if v['vorlage'] == 'plakatganz']
    keys += [k for k in ('dc_plakat_ganz', 'pop23') if k not in keys]
    for key in keys:
        if key.startswith('po_'):
            m = MOT[key[3:]]; name, farbe = m['titel'], m['rueck_farbe']
            abend = next(v['titel'] for v in VORL if v['vorlage'] == 'plakatganz' and v['inhalt']['bild'] == key).replace('Plakat · ', '')
            zeile = 'Culinarium'
        elif key == 'pop23':
            name, farbe, abend, zeile = 'Das erste Pop-up', '#4a4330', 'Sa 20. Mai 2023', 'Culinarium'
        else:
            name, farbe, abend, zeile = 'Dirty Chicken', N.VIOLETT, 'Das erste Pop-up', 'Dirty Chicken'
        b = BX.get(key, {'w': 1, 'h': 1})
        K_.append(dict(id=f'pk{len(K_) + 1:02d}', key=key, name=name, farbe=farbe, abend=abend, zeile=zeile, ia=b['w'] / b['h'], dc=key.startswith('dc_')))
    return K_


def vorn(k, rand=0):
    """A6 hoch, 105 × 148; rand = Beschnitt ringsum (Druck)."""
    b, h = 105 + 2 * rand, 148 + 2 * rand
    pw = 105 - 2 * 9                                  # Plakat 87 mm breit, 9 mm Rand seitlich
    ph = pw / k['ia']
    if ph > 148 - 30: ph = 148 - 30; pw = ph * k['ia']
    x, y = rand + (105 - pw) / 2, rand + (148 - ph) / 2 - 7
    unter = 'Dirty Chicken · Walk on the Wild Side' if k['dc'] else 'Culinarium · Walk on the Wild Side'
    inn = (f'<i class="abs" style="inset:0;background:{k["farbe"]}"></i>'
           f'<img class="abs" src="{e(N.bild(k["key"]))}" style="left:{x}mm;top:{y}mm;width:{pw}mm;height:{ph}mm;object-fit:contain;box-shadow:0 .6mm 2.4mm rgba(0,0,0,.35)" alt="">'
           f'<div class="abs" style="left:{rand}mm;top:{y + ph + 7}mm;width:105mm;text-align:center">{N.et(unter, 1.8, "rgba(250,244,244,.82)", .14)}</div>')
    return blatt(b, h, inn, '', f'background:{k["farbe"]}')


def hinten(k, rand=0):
    """A6 quer, 148 × 105: links der Abend, rechts Adresse und Markenfeld mit dem C."""
    b, h = 148 + 2 * rand, 105 + 2 * rand
    r = rand
    zeichen = N.dz(11) if k['dc'] else N.zw(11, N.SCHIEFER)
    links = (f'<div class="abs" style="left:{r + 10}mm;top:{r + 12}mm;width:52mm;bottom:{r + 12}mm;display:flex;flex-direction:column;justify-content:space-between">'
             f'<div>{N.et("Plakat von Rudi", 1.8, N.KERZET, .14)}<div style="height:3mm"></div>'
             f'{N.ti(e(k["name"]), 6.4, N.SCHIEFER, 1.12)}<div style="height:2.4mm"></div>'
             f'<i style="display:block;width:8mm;height:.35mm;background:{k["farbe"]}"></i><div style="height:2.4mm"></div>'
             f'{N.tx(k["abend"], 3, N.TINTE)}</div>'
             f'<div>{N.et("Walk on the Wild Side · Haasemannstraße 13", 1.55, N.KERZET, .08)}<div style="height:1mm"></div>'
             f'{N.et("@dirtychicken.hannover" if k["dc"] else "@culinarium_hannover", 1.55, N.KERZET, .08)}</div></div>')
    trenn = f'<i class="abs" style="left:{r + 72}mm;top:{r + 12}mm;width:.25mm;height:81mm;background:{N.KERZE}"></i>'
    marke = (f'<div class="abs" style="left:{r + 148 - 10 - 20}mm;top:{r + 10}mm;width:20mm;height:24mm;border:.3mm dashed rgba(38,36,45,.45);border-radius:.8mm;'
             f'display:flex;align-items:center;justify-content:center">{zeichen}</div>')
    linien = ''.join(f'<i class="abs" style="left:{r + 80}mm;top:{r + 50 + n * 11}mm;width:58mm;height:.25mm;background:rgba(38,36,45,.38)"></i>' for n in range(4))
    return blatt(b, h, f'<i class="abs" style="inset:0;background:{N.WEISS}"></i>' + links + trenn + marke + linien, '', f'background:{N.WEISS}')


def setzen():
    KK = karten()
    N.bild('barnacht'); N.bild('theke')   # Hintergrund für das Bild am Kartenständer
    vor = [vorn(k) for k in KK]; hin = [hinten(k) for k in KK]
    P.seite('postkarten', [x for p in zip(vor, hin) for x in p], 'Postkarten')                                  # Vorschau: vorn, hinten, je Karte
    P.seite('postkarten-druck', [x for k in KK for x in (vorn(k, B), hinten(k, B))], 'Postkarten, Druck mit Beschnitt')
    # Sammelbogen SRA3 quer (450 × 320 mm): acht Vorderseiten in Originalgrösse mit Schnittmarken. Auf A3 (420 × 297) passen acht A6-Karten nur ohne
    # jeden Rand; der Bogen schnitt die vierte Spalte ab (Tor 4, 30.10.2026). SRA3 ist der übliche Bogen im Digitaldruck, die Karten stehen mittig.
    BW, BH, LUFT = 450, 320, 3
    boegen = []
    for s0 in range(0, len(KK), 8):
        teil = KK[s0:s0 + 8]; inn = ''
        x0, y0 = (BW - (4 * 105 + 3 * LUFT)) / 2, (BH - (2 * 148 + LUFT)) / 2
        for n, k in enumerate(teil):
            x, y = x0 + (n % 4) * (105 + LUFT), y0 + (n // 4) * (148 + LUFT)
            inn += f'<div class="abs" style="left:{x}mm;top:{y}mm;width:105mm;height:148mm;overflow:hidden">{vorn(k).replace('style="width:', 'style="margin:0;width:', 1)}</div>'
            inn += f'<i class="abs" style="left:{x}mm;top:{y}mm;width:105mm;height:148mm;outline:.15mm solid #e6007e"></i>'
        inn += t(14, 4, f'{e(H.NAME)} · Postkarten der Plakate · Sammelbogen {s0 // 8 + 1} von {(len(KK) + 7) // 8} · SRA3 quer · Originalgröße · Schnittlinie in Magenta', 'm', 'font-size:2.1mm;color:#26242d')
        boegen.append(blatt(BW, BH, inn, '', 'background:#fff'))
    P.seite('postkarten-bogen', boegen, 'Postkarten, Sammelbogen')
    json.dump({'karten': [{k2: k[k2] for k2 in ('id', 'key', 'name', 'abend', 'farbe')} for k in KK], 'boegen': len(boegen)},
              open(os.path.join(W, 'postkarten_plan.json'), 'w'), ensure_ascii=False, indent=1)
    print('Postkarten gesetzt:', len(KK), 'Karten,', len(boegen), 'Sammelbögen')


def seite():
    K.gestaltung()
    plan = json.load(open(os.path.join(W, 'postkarten_plan.json')))
    KK = plan['karten']
    from PIL import Image
    roh, ziel = os.path.join(W, 'roh', 'postkarten'), os.path.join(ROOT, 'postkarten', 'img'); os.makedirs(ziel, exist_ok=True)
    M = {}
    for f in os.listdir(roh):
        if not f.endswith('.png'): continue
        im = Image.open(os.path.join(roh, f)).convert('RGBA')
        if im.width > 1400: im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(os.path.join(ziel, f[:-4] + '.webp'), 'WEBP', quality=88, method=5); M[f[:-4]] = im.size
    img = lambda n, alt='': f'<img src="img/{n}.webp" width="{M[n][0]}" height="{M[n][1]}" alt="{e(alt)}" loading="lazy" decoding="async">'
    liste = ''.join(f'<li data-a="kipp" style="--i:{n % 4}"><span class="b pk-paar">{img(k["id"] + "-v", k["name"])}{img(k["id"] + "-h", "Rückseite")}</span><h3>{e(k["name"])}</h3><p>{e(k["abend"])}</p><small>A6 · vorn hoch, hinten quer</small></li>' for n, k in enumerate(KK))
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('papier'), 'Ideen für Papier')}
      {titel([zahl(len(KK)), 'Postkarten von', 'euren Plakaten.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">Für jedes Plakat, das es bisher gab, eine Postkarte: vorne das Plakat ganz auf einem Rand in seiner Farbe, hinten der Abend, Platz zum Schreiben und das C im Markenfeld. Zum Auslegen an der Bar und zum Mitnehmen.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#papier')}{kn('Druck-PDF', f'pdf/{H.KURZ}-postkarten-druck.pdf', 'kn--linie', neu=True)}</div>
    </div>
    <div class="auslage" aria-hidden="true"><div data-a="schweb" style="left:0;top:0;width:100%;--r:0deg;--r0:0deg;--i:2">{img("faecher", "")}</div></div>
  </div>
</section>
<section class="fl fl--nacht tapete-leicht blatt stueck" id="staender">
  <div class="in">
    <div class="stueck__t">{kap(1, 'An der Bar')}{titel(['Im Ständer', 'an der Theke.'])}<div class="lauf"><p data-a="worte">So könnten die Karten an der Bar stehen: jede Saison ein paar neue, zum Mitnehmen nach dem Abend.</p></div></div>
    <div class="karton"><figure class="sch" data-a="schweb" style="width:96%">{img("staender", "Kartenständer an der Bar")}</figure></div>
  </div>
</section>
<section class="fl fl--papier blatt" id="karten">
  <div class="in">
    <div class="kopfzeile"><div>{kap(2, 'Die Karten')}{titel([zahl(len(KK)), 'Postkarten.'])}</div><div class="lauf"><p data-a="worte">Jedes Plakat ganz, nie angeschnitten. Die Farbe des Rands kommt aus dem Motiv.</p></div></div>
    <ul class="etk">{liste}</ul>
  </div>
</section>
<section class="fl fl--creme blatt stueck" id="druck">
  <div class="in">
    <div class="stueck__t">{kap(3, 'Für die Druckerei')}{titel(['Der', 'Sammelbogen.'])}
      <div class="lauf"><p data-a="worte">Alle Karten mit 3 mm Beschnitt als ein PDF, dazu {zahl(plan["boegen"]).lower()} Sammelbögen SRA3 mit Schnittlinien.</p></div>
      <div class="kn-reihe" data-a="auf">{kn('Druck-PDF', f'pdf/{H.KURZ}-postkarten-druck.pdf', neu=True)}{kn('Sammelbogen SRA3', f'pdf/{H.KURZ}-postkarten-sammelbogen-a3.pdf', 'kn--linie', neu=True)}</div></div>
    <div class="bogenblick" data-a="gross">{img("bogen", "Sammelbogen SRA3")}</div>
  </div>
</section>
<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es Drucksachen, Sticker und Beigaben im selben Stil.</p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn('Sticker', '../sticker/index.html', 'kn--linie')}</div></div></section>'''
    css = '<style>.etk .b.pk-paar{display:flex!important;flex-direction:row!important;gap:4%;align-items:center;justify-content:center;height:auto!important;aspect-ratio:auto!important}.etk .b.pk-paar img{position:static!important;width:40%!important;height:auto!important;max-height:none!important}.etk .b.pk-paar img+img{width:56%!important}</style>'   # Tor 4 30.10.2026: vorn und hinten nebeneinander, nie über dem Titel
    K.schreib(os.path.join(ROOT, 'postkarten', 'index.html'), K.rahmen('Postkarten', f'{zahl(len(KK))} Postkarten von den Plakaten des {H.NAME}.', 'Postkarten', css + haupt))
    print('Seite gebaut: postkarten/ ·', len(KK), 'Karten')


if __name__ == '__main__':
    seite() if '--seite' in sys.argv else setzen()
