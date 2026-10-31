#!/usr/bin/env python3
"""Culinarium: fünf Beigaben als Druckvorlage (Prüfchat Gestaltung 29.10.2026, Auftrag Oberchef nach Robert: «überleg dir nochmal, was man sonst
noch Cooles für so ein Konzept entwickeln könnte an Beigaben»). Menü-Rolle mit Banderole, Streichholzbriefchen, Drink-Fähnchen, Postkarten der Plakate,
Rezeptkarte eines Drinks. Gesetzt in papier_neu.beigaben(), Seite beigaben/ im Kleid der Drucksachen.
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/beigaben.py "<website/_werkbank>"          →  satz/beigabe-*.html, beigaben_plan.json
   node _werkbank/sticker_druck.js "<…>" beigaben, dann  python3 _werkbank/beigaben.py "<…>" --seite"""
import json, os, sys
import papier_kern as P
import kern as K
from kern import H, ROOT, W, e, kn, titel, kap, zahl
import papier_neu as N


def setzen():
    import papier as PA
    B, S = N.beigaben(PA.TELLER)
    for d in B:
        P.seite('beigabe-' + d['id'], d['blaetter'], d['name'])
    json.dump({'druck': [{k: d[k] for k in ('id', 'name', 'format', 'vorschau', 'satz')} | {'seiten': len(d['blaetter']), 'karton': S[d['id']]['karton'][1], 'titel': S[d['id']]['titel']} for d in B]},
              open(os.path.join(W, 'beigaben_plan.json'), 'w'), ensure_ascii=False, indent=1)
    print('Beigaben gesetzt:', len(B))


def seite():
    from PIL import Image
    K.gestaltung()
    plan = json.load(open(os.path.join(W, 'beigaben_plan.json')))
    roh, ziel = os.path.join(W, 'roh', 'beigaben'), os.path.join(ROOT, 'beigaben', 'img')
    os.makedirs(ziel, exist_ok=True)
    M = {}
    for d in plan['druck']:
        for name, _ in d['vorschau']:
            im = Image.open(os.path.join(roh, name + '.png')).convert('RGBA')
            if im.width > 1000:
                im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
            im.save(os.path.join(ziel, name + '.webp'), 'WEBP', quality=88, method=5); M[name] = im.size
    FL = ['fl--papier', 'fl--nacht tapete-leicht', 'fl--creme', 'fl--papier', 'fl--creme']
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('papier'), 'Ideen für Papier')}
      {titel([zahl(len(plan['druck'])) + ' Beigaben', 'für den Abend.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">Kleine Dinge, die ein Gast vom Abend mitnimmt oder am Platz findet. Alle im Stil der neuen Seite, jede als Druckvorlage. Was nicht passt, lasst ihr einfach weg.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#papier')}{kn('Drucksachen', '../drucksachen/index.html', 'kn--linie')}</div>
    </div>
  </div>
</section>
'''
    for i, d in enumerate(plan['druck']):
        figs = ''.join(f'<figure class="sch" data-a="schweb" style="width:{w}%;--i:{k % 4}"><img src="img/{nm}.webp" width="{M[nm][0]}" height="{M[nm][1]}" alt="{e(d["name"])}" loading="lazy" decoding="async">'
                       f'{f"<figcaption>{e(u)}</figcaption>" if u else ""}</figure>' for k, (nm, w, u) in enumerate(d['karton']))
        haupt += f'''<section class="fl {FL[i % len(FL)]} blatt stueck{" stueck--r" if i % 2 else ""}" id="{d['id']}">
  <div class="in">
    <div class="stueck__t">
      {kap(i + 1, e(d['name']))}
      {titel(d['titel'])}
      <div class="lauf"><p data-a="worte">{e(d['satz'])}</p></div>
      <p class="stueck__f" data-a="auf">{e(d['format'])}</p>
      <div class="kn-reihe" data-a="auf">{kn('Als PDF ansehen', f"pdf/{H.KURZ}-{d['id']}.pdf", neu=True)}</div>
    </div>
    <div class="karton">{figs}</div>
  </div>
</section>
'''
    haupt += f'''<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es Drucksachen, Untersetzer und Sticker im selben Stil.</p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn('Sticker', '../sticker/index.html', 'kn--linie')}</div></div></section>'''
    K.schreib(os.path.join(ROOT, 'beigaben', 'index.html'), K.rahmen('Beigaben', f'{zahl(len(plan["druck"]))} Beigaben für die Abende des {H.NAME}.', 'Beigaben', haupt))
    print('Seite gebaut: beigaben/ ·', len(plan['druck']), 'Beigaben')


if __name__ == '__main__':
    seite() if '--seite' in sys.argv else setzen()
