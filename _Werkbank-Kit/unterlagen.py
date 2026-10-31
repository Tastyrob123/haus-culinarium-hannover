#!/usr/bin/env python3
"""Seite «Unterlagen»: jede Unterlage des Hauses, heutige Fassung und Idee im Stil der Seite, Seite für Seite nebeneinander.
   python3 unterlagen.py "<Projektordner>"   →  unterlagen/index.html (+ unterlagen/img)
   Die PDFs entstehen mit satz.py + satz_druck.js, hier werden sie nur gezeigt. Seitenbilder in doppelter Breite (1500 px),
   sonst sind sie auf Roberts Schirm unscharf."""
import glob, json, os, subprocess
from PIL import Image
import kern as K
from kern import H, ROOT, W, e, kn, titel, kap, zahl, PF, LI, RE

ZIEL = os.path.join(ROOT, 'unterlagen'); IMG = os.path.join(ZIEL, 'img'); os.makedirs(IMG, exist_ok=True)
ROH = os.path.join(W, 'roh', 'unterlagen'); os.makedirs(ROH, exist_ok=True)


def seiten(pdf, kennung):
    marke = os.path.join(ROH, kennung + '.json')
    if os.path.exists(marke) and os.path.getmtime(marke) > os.path.getmtime(pdf) and all(os.path.exists(os.path.join(IMG, x[0])) for x in json.load(open(marke))):
        return json.load(open(marke))
    for alt in glob.glob(os.path.join(ROH, kennung + '-*.png')):
        os.remove(alt)
    subprocess.run(['pdftoppm', '-r', '170', '-png', pdf, os.path.join(ROH, kennung)], check=True)
    aus = []
    for i, f in enumerate(sorted(glob.glob(os.path.join(ROH, kennung + '-*.png')))):
        im = Image.open(f).convert('RGB')
        if im.width > 1500:
            im = im.resize((1500, round(im.height * 1500 / im.width)), Image.LANCZOS)
        name = f'{kennung}-{i + 1:02d}.webp'
        im.save(os.path.join(IMG, name), 'WEBP', quality=84, method=5)
        aus.append([name, im.width, im.height]); os.remove(f)
    json.dump(aus, open(marke, 'w'))
    return aus


def baue():
    K.gestaltung()
    plan = json.load(open(os.path.join(W, 'unterlagen.json')))
    D = []
    for d in plan:
        neu = seiten(os.path.join(ROOT, 'unterlagen', 'pdf', d['ziel'] + '.pdf'), 'n-' + d['ziel'])
        alt = seiten(os.path.join(ROOT, d['quelle']), 'h-' + d['ziel'])
        D.append({'id': d['ziel'], 'name': d['name'], 'gruppe': d['gruppe'], 'neu': neu, 'alt': alt, **({'altmap': d['alt_seiten']} if d.get('alt_seiten') else {})})
        if len(neu) != len(alt) and not d.get('alt_seiten'):
            print('  Achtung, Seitenzahl verschieden:', d['ziel'], len(alt), len(neu))
    n = len(D)
    U = H.UNTERLAGEN
    wahl = ''.join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-id="{d["id"]}">{e(d["name"])}</button>' for i, d in enumerate(D))
    orte = {1: [(30, 2, 40, -3)], 2: [(10, 6, 40, -6), (50, 0, 40, 5)], 3: [(2, 8, 38, -7), (31, 0, 38, 2), (60, 6, 38, 7)], 4: [(0, 10, 36, -8), (21, 4, 36, -3), (42, 0, 36, 3), (63, 7, 36, 8)]}
    zeig = H.FAECHER[:4]
    faecher = ''.join(f'<div class="blattbild" data-a="schweb" style="left:{x}%;top:{y}%;width:{b}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}"><img src="img/n-{k}-01.webp" alt=""></div>'
                      for i, ((k, _), (x, y, b, r)) in enumerate(zip(zeig, orte[len(zeig)])))
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('unterlagen'), 'Unterlagen')}
      {titel(['Ihre Unterlagen,', 'im selben Stil.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">{U['seite_text'].format(n=zahl(n), nk=zahl(n).lower())}</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Durchblättern', '#blaettern')}{kn('Zur Werkbank', '../werkbank/index.html#unterlagen', 'kn--linie')}</div>
    </div>
    <div class="auslage auslage--pdf" aria-hidden="true">{faecher}</div>
  </div>
</section>
<section class="fl fl--papier blatt" id="blaettern">
  <div class="in">
    <div class="kopfzeile"><div>{kap(1, 'Durchblättern')}{titel(['Heute und', 'als Idee.'])}</div><div class="lauf"><p data-a="worte">Wählen Sie eine Unterlage und blättern Sie mit den Pfeilen. Links steht Ihre heutige Fassung, rechts die Idee im Stil der neuen Seite.</p></div></div>
    <div class="uwahl" data-a="auf" role="group" aria-label="Unterlage wählen">{wahl}</div>
    <div class="uschau" data-a="auf" tabindex="0">
      <div class="uschalter" role="group" aria-label="Fassung"><button type="button" aria-pressed="false" data-s="alt">Heute</button><button type="button" aria-pressed="true" data-s="neu">Idee</button></div>
      <div class="upaar">
        <figure class="ublatt ublatt--alt"><div class="ublatt__b"></div><figcaption>Heute</figcaption></figure>
        <figure class="ublatt ublatt--neu"><div class="ublatt__b"></div><figcaption>Idee</figcaption></figure>
        <button class="rund schau__p schau__p--l" type="button" data-zur aria-label="Vorige Seite">{LI}</button>
        <button class="rund schau__p schau__p--r" type="button" data-vor aria-label="Nächste Seite">{RE}</button>
      </div>
      <div class="ufuss">
        <div><h3></h3><p class="mono"></p></div>
        <div class="kn-reihe"><a class="kn kn--klein" href="#" target="_blank" rel="noopener" data-pdf>Idee als PDF<i>{PF}</i></a>{f'<a class="kn kn--klein kn--linie" href="{e(U["pflege"][1])}" target="_blank" rel="noopener" data-pflege>{e(U["pflege"][0])}<i>{PF}</i></a>' if U.get('pflege') else ''}</div>
      </div>
    </div>
  </div>
</section>
<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es Ideen für Papier: Drucksachen und <span style="white-space:nowrap">{e(H.ETIKETTEN['name'])}.</span></p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn(H.ETIKETTEN['name'], f'../{H.ETIKETTEN["ordner"]}/index.html', 'kn--linie')}{kn('Zur Werkbank', '../werkbank/index.html#unterlagen', 'kn--linie')}</div></div></section>
<script>window.UNTERLAGEN={json.dumps(D, ensure_ascii=False)};</script>
<script src="unterlagen.js?v={int(os.path.getmtime(os.path.join(K.KIT, 'unterlagen.js')))}" defer></script>'''
    seite = K.rahmen('Unterlagen', f'{zahl(n)} Unterlagen des {H.NAME} als Idee im Stil der neuen Website, jede neben der heutigen Fassung.', 'Unterlagen', haupt,
                     f'Die neuen Fassungen sind Ideen von Robert Reff, Tasty Studios, und keine offiziellen Unterlagen des Hauses. Fotos, Zeichen und Texte gehören {H.RECHTE}')
    K.schreib(os.path.join(ZIEL, 'index.html'), seite)
    K.schreib(os.path.join(ZIEL, 'unterlagen.js'), open(os.path.join(K.KIT, 'unterlagen.js'), encoding='utf-8').read())
    print('Unterlagen:', n, 'mit', sum(len(d['neu']) for d in D), 'Seiten')


if __name__ == '__main__':
    baue()
