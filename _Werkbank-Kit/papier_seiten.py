#!/usr/bin/env python3
"""Baut die Seiten drucksachen/ und <etiketten>/ aus papier_plan.json und den Vorschaubildern (node papier_druck.js),
   schreibt papier.json für die Werkbank.   python3 papier_seiten.py "<Projektordner>"
   Texte je Haus: H.PAPIER_SEITE in haus.py. Sie-Form, Schweizer Schreibung, alles als Idee."""
import json, os
from PIL import Image
import kern as K
import schatten
from kern import H, ROOT, W, e, kn, titel, kap, zahl

ROH = os.path.join(W, 'roh', 'papier')
plan = json.load(open(os.path.join(W, 'papier_plan.json')))
S = H.PAPIER_SEITE
ET = H.ETIKETTEN
M = {}
# Weitere Ideen aus Roberts Auswahl (Sechs Häuser — Drucksachen/mehr.py): Bilder und PDFs liegen schon in drucksachen/
_MJ = K.lies('papier_mehr.json', {'druck': []})
MEHR = _MJ['druck']
RASTER = _MJ.get('raster', '')   # kleine Galerie am Ende mit den Kleinigkeiten (mehr.py); die wichtigen Stücke stehen im Wechsel als Abschnitte


def webp(name, ordner, breite, backen=False):
    ziel = os.path.join(ROOT, ordner, 'img'); os.makedirs(ziel, exist_ok=True)
    im = Image.open(os.path.join(ROH, name + '.png')).convert('RGBA')
    if im.width > breite:
        im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
    if backen:   # Schatten im Bild statt per CSS (schatten.py)
        im = schatten.backe(im)
    im.save(os.path.join(ziel, name + '.webp'), 'WEBP', quality=88, method=5)
    M[name] = im.size


def bild(name, alt='', lazy=True):
    w, h = M[name]
    return f'<img src="img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}"{" loading=\"lazy\" decoding=\"async\"" if lazy else ""}>'


def drucksachen():
    for d in MEHR:
        M.update({k: tuple(v) for k, v in d['masse'].items()})
    for d in plan['druck']:
        for name, _ in d['vorschau']:
            webp(name, 'drucksachen', 1000 if name in S['breit'] else 640)
    aus = ''.join(f'<div class="{"form" if n in S["formen"] else "blattbild"}" data-a="schweb" style="left:{x}%;top:{y}%;width:{w}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}">{bild(n, lazy=False)}</div>' for i, (n, x, y, w, r) in enumerate(S['auslage']))
    n = len(plan['druck']) + len(MEHR)
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('papier'), 'Ideen für Papier')}
      {titel([zahl(n) + ' Ideen', 'für Papier.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">{S.get('druck_text', 'Beim Bauen der Website sind mir ein paar Dinge eingefallen, die es bei Ihnen schon gibt oder die gut zu Ihrem Haus passen könnten. Hier liegen sie im Stil der neuen Seite. Das sind alles nur Ideen. Nehmen Sie sich davon, was Ihnen gefällt.')}</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#papier')}{kn(ET['name'], f'../{ET["ordner"]}/index.html', 'kn--linie')}</div>
    </div>
    <div class="auslage" aria-hidden="true">{aus}</div>
  </div>
</section>
'''
    FL = S.get('flaeche', ['fl--papier', 'fl--creme', 'fl--navy tapete', 'fl--papier', 'fl--creme', 'fl--nacht', 'fl--papier', 'fl--creme'])
    for i, d in enumerate(plan['druck']):
        kl, stuecke = S['karton'][d['id']]
        sch = ' sch' if d['id'] in S['schatten'] else ''
        haengt = d['id'] in S.get('haengt', ())
        figs = ''.join(f'<figure class="{"haengt" if haengt else ""}{sch}" data-a="schweb" style="width:{w}%;--i:{k % 4}">{bild(nm, d["name"] + (" · " + u if u else ""))}{f"<figcaption>{e(u)}</figcaption>" if u else ""}</figure>' for k, (nm, w, u) in enumerate(stuecke))
        haupt += f'''<section class="fl {FL[i % len(FL)]} blatt stueck{" stueck--r" if i % 2 else ""}" id="{d['id']}">
  <div class="in">
    <div class="stueck__t">
      {kap(i + 1, e(d['name']))}
      {titel(S['titel'][d['id']])}
      <div class="lauf"><p data-a="worte">{e(d['satz'])}</p></div>
      <p class="stueck__f" data-a="auf">{e(d['format'])}</p>
      <div class="kn-reihe" data-a="auf">{kn('Als PDF ansehen', f"pdf/{H.KURZ}-{d['id']}.pdf", neu=True)}</div>
    </div>
    <div class="karton {kl}">{figs}</div>
  </div>
</section>
'''
    for j, d in enumerate([x for x in MEHR if not x.get('klein')]):
        i = len(plan['druck']) + j
        sch = ' sch' if d['schatten'] else ''
        figs = ''.join(f'<figure class="{"haengt" if d["haengt"] else ""}{sch}" data-a="schweb" style="width:{w}%;--i:{k % 4}">{bild(nm, d["name"] + (" · " + u if u else ""))}{f"<figcaption>{e(u)}</figcaption>" if u else ""}</figure>' for k, (nm, w, u) in enumerate(d['karton']))
        haupt += f'''<section class="fl {FL[i % len(FL)]} blatt stueck{" stueck--r" if i % 2 else ""}" id="{d['id']}">
  <div class="in">
    <div class="stueck__t">
      {kap(i + 1, e(d['name']))}
      {titel(d['titel'])}
      <div class="lauf"><p data-a="worte">{e(d['satz'])}</p></div>
      <p class="stueck__f" data-a="auf">{e(d['format'])}</p>
      <div class="kn-reihe" data-a="auf">{kn('Als PDF ansehen', f"pdf/{d['pdf']}", neu=True)}</div>
    </div>
    <div class="karton">{figs}</div>
  </div>
</section>
'''
    letzte = FL[(len(plan['druck']) + len([x for x in MEHR if not x.get('klein')]) - 1) % len(FL)]
    haupt += RASTER.replace('fl--creme blatt galerie-p', 'fl--papier blatt galerie-p') if 'creme' in letzte else RASTER   # Galerie hebt sich von der letzten Fläche ab
    haupt += f'''<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es {zahl(len(plan['etiketten'])).lower()} {e(ET['name'])} und Ihre Unterlagen im selben Stil.</p><div class="kn-reihe" data-a="auf">{kn(ET['name'], f'../{ET["ordner"]}/index.html')}{kn('Unterlagen', '../unterlagen/index.html', 'kn--linie')}{kn('Zur Werkbank', '../werkbank/index.html#papier', 'kn--linie')}</div></div></section>'''
    K.schreib(os.path.join(ROOT, 'drucksachen', 'index.html'), K.rahmen('Ideen für Papier', f'{zahl(n)} Ideen für Drucksachen des {H.NAME}.', 'Drucksachen', haupt))


def etiketten():
    O = ET['ordner']
    gb = bool(S.get('etik_schatten'))   # Schatten fest im Bild (Grand Beau-Rivage 12.10.2026); Marke für die Sprachfassungen
    for x in plan['etiketten']:
        webp(x['id'], O, 640, backen=gb)
    marke = os.path.join(ROOT, O, '.schatten')
    if gb:
        open(marke, 'w').write('Schatten fest im Bild (schatten.py)\n')
    elif os.path.exists(marke):
        os.remove(marke)
    im = Image.open(os.path.join(ROH, 'etiketten-bogen.png')).convert('RGB'); im.thumbnail((1500, 1500))
    os.makedirs(os.path.join(ROOT, O, 'img'), exist_ok=True)
    im.save(os.path.join(ROOT, O, 'img', 'bogen.webp'), 'WEBP', quality=84); M['bogen'] = im.size
    E = plan['etiketten']
    aus = ''.join(f'<div data-a="schweb" style="left:{x}%;top:{y}%;width:{w}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}">{bild(E[i]["id"], lazy=False)}</div>' for i, (x, y, w, r) in enumerate(S['etik_auslage']) if w and i < len(E))
    if S.get('etik_haufen'):   # Haufen wie bei Salt & Silver (Robert 12.10.2026): alle übereinander, jeder mit Lage, Breite, Drehung, fallen nacheinander herein
        ids = {x['id'] for x in E}
        aus = ''.join(f'<i style="--x:{x}%;--y:{y}%;--w:{w}%;--r:{r}deg;--i:{i}">{bild(k, lazy=False)}</i>' for i, (k, x, y, w, r) in enumerate(S['etik_haufen']) if k in ids)
        aus = (f'<div class="haufen" aria-hidden="true">{aus}</div>'
               "<script>(function(){var h=document.querySelector('.haufen');if(!h)return;var b=[].slice.call(h.querySelectorAll('img')),n=0,los=function(){h.classList.add('los')};"
               "b.forEach(function(i){var f=function(){if(++n>=b.length)los()};if(i.complete)f();else{i.addEventListener('load',f);i.addEventListener('error',f)}});setTimeout(los,1600)})();</script>")
    ein = S.get('etik_einblenden', 'kipp')
    liste = ''.join(f'<li data-a="{ein}" style="--i:{i % 4}"><span class="b">{bild(x["id"], ET["einzahl"] + ": " + x["name"])}</span><h3>{e(x["name"])}</h3><p>{e(x["satz"])}</p><small>{x["b"]} × {x["h"]} mm</small></li>' for i, x in enumerate(E))
    n = len(E)
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('papier'), 'Ideen für Papier')}
      {titel([f'{zahl(n)} {S["etik_titel"][0]}', S['etik_titel'][1]], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">{S['etik_text'].format(n=zahl(n).lower())}</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#papier')}{kn('Drucksachen', '../drucksachen/index.html', 'kn--linie')}</div>
    </div>
    {aus if S.get('etik_haufen') else f'<div class="auslage" aria-hidden="true">{aus}</div>'}
  </div>
</section>
<section class="fl {S.get('etik_flaeche', ['fl--navy tapete', 'fl--papier'])[0]} blatt" id="etiketten">
  <div class="in">
    <div class="kopfzeile"><div>{kap(1, S['etik_kap'])}{titel(S['etik_kopf'])}</div><div class="lauf"><p data-a="worte">{S['etik_kopftext']}</p></div></div>
    <ul class="etk{' etk--gb' if gb else ''}">{liste}</ul>
  </div>
</section>
<section class="fl {S.get('etik_flaeche', ['fl--navy tapete', 'fl--papier'])[1]} blatt stueck" id="druck">
  <div class="in">
    <div class="stueck__t">
      {kap(2, 'Für die Druckerei')}
      {titel(['Der', 'Druckbogen.'])}
      <div class="lauf"><p data-a="worte">Alle {e(ET['name'])} liegen in Originalgrösse auf {zahl(plan['boegen']).lower()} {"Bogen" if plan['boegen'] == 1 else "Bögen"} im Format A3, mit einer Schnittlinie je Stück. Dazu gibt es jedes einzeln als PDF.</p></div>
      <p class="stueck__f" data-a="auf">{n} {e(ET['name'])} · {plan['masse'][0]} bis {plan['masse'][1]} mm · Schnittlinie in Magenta</p>
      <div class="kn-reihe" data-a="auf">{kn('Druckbogen als PDF', f'pdf/{H.KURZ}-{O}-druckbogen-a3.pdf', neu=True)}{kn('Alle einzeln als PDF', f'pdf/{H.KURZ}-{O}-einzeln.pdf', 'kn--linie', neu=True)}</div>
    </div>
    <div class="bogenblick" data-a="gross">{bild('bogen', 'Druckbogen A3 mit Schnittlinien')}</div>
  </div>
</section>
<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es {zahl(len(plan['druck']) + len(MEHR)).lower()} Drucksachen und Ihre Unterlagen im selben Stil.</p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn('Unterlagen', '../unterlagen/index.html', 'kn--linie')}{kn('Zur Werkbank', '../werkbank/index.html#papier', 'kn--linie')}</div></div></section>'''
    K.schreib(os.path.join(ROOT, O, 'index.html'), K.rahmen(ET['name'], f'{zahl(n)} Ideen für {ET["name"]} des {H.NAME}.', ET['name'], haupt))


if __name__ == '__main__':
    K.gestaltung()
    drucksachen(); etiketten()
    json.dump({'druck': [{'id': d['id'], 'name': d['name'], 'seiten': d['seiten']} for d in plan['druck'] + MEHR], 'etiketten': [{'id': x['id'], 'name': x['name']} for x in plan['etiketten']]},
              open(os.path.join(W, 'papier.json'), 'w'), ensure_ascii=False, indent=1)
    print('Seiten gebaut: drucksachen/,', ET['ordner'] + '/ ·', len(plan['druck']), 'Drucksachen,', len(plan['etiketten']), ET['name'])
