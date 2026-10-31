#!/usr/bin/env python3
"""Ordner «Material»: alles, was für den Entwurf neu entstanden ist, sortiert in material/ (+ Übersichtsseite).
   python3 material.py "<Projektordner>"
   Liegt vorerst lokal. Auf Roberts Wort geht derselbe Ordner nach Google Drive, dann zeigt der Knopf der Werkbank dorthin."""
import glob, json, os, shutil
import kern as K
from kern import H, ROOT, W, e, kn, titel, kap, zahl, PF

ZIEL = os.path.join(ROOT, 'material')
ET = H.ETIKETTEN


def lege(ordner, quelle, name=None):
    d = os.path.join(ZIEL, ordner); os.makedirs(d, exist_ok=True)
    z = os.path.join(d, name or os.path.basename(quelle))
    if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(quelle):
        shutil.copy2(quelle, z)
    return ordner + '/' + os.path.basename(z)


def baue():
    K.gestaltung()
    plan = json.load(open(os.path.join(W, 'papier_plan.json')))
    U = json.load(open(os.path.join(W, 'unterlagen.json')))
    N = H.NAME
    O = []
    d = [(u['name'], lege('01 Unterlagen', os.path.join(ROOT, 'unterlagen', 'pdf', u['ziel'] + '.pdf'), f"{N} {u['name'].replace(':', '').replace('/', ' ')}.pdf")) for u in U]
    O.append(('Unterlagen', 'Ihre Unterlagen als Idee im Stil der neuen Seite, jede als PDF.', d))
    d = [(x['name'], lege('02 Drucksachen', os.path.join(ROOT, 'drucksachen', 'pdf', f"{H.KURZ}-{x['id']}.pdf"), f"{N} {x['name']}.pdf")) for x in plan['druck']]
    O.append(('Drucksachen', H.MATERIAL['druck_satz'], d))
    eo = ET['ordner']
    d = [('Druckbogen A3', lege('03 ' + ET['name'], os.path.join(ROOT, eo, 'pdf', f'{H.KURZ}-{eo}-druckbogen-a3.pdf'), f'{N} {ET["name"]} Druckbogen A3.pdf')),
         ('Alle einzeln', lege('03 ' + ET['name'], os.path.join(ROOT, eo, 'pdf', f'{H.KURZ}-{eo}-einzeln.pdf'), f'{N} {ET["name"]} einzeln.pdf'))]
    for x in plan['etiketten']:
        lege(f'03 {ET["name"]}/Bilder', os.path.join(W, 'roh', 'papier', x['id'] + '.png'), ET['einzahl'] + ' ' + x['name'].replace('’', '').replace('/', ' ') + '.png')
    O.append((ET['name'], 'Der Druckbogen mit Schnittlinien, jedes Stück einzeln und alle als Bild.', d))
    d = [(t, lege('04 Zeichen', os.path.join(ROOT, q), n)) for t, q, n in H.MATERIAL['zeichen']]
    O.append(('Zeichen', H.MATERIAL['zeichen_satz'], d))
    n_an = 0
    for art in ('Rechner', 'Handy'):
        for f in sorted(glob.glob(os.path.join(W, 'ansichten', art, '*.jpg'))):
            lege('05 Ansichten der neuen Website/' + art, f); n_an += 1
    O.append(('Ansichten der neuen Website', 'Jede Seite des Entwurfs als Bild, am Rechner und am Handy.', [('Am Rechner', '05 Ansichten der neuen Website/Rechner/Startseite.jpg'), ('Am Handy', '05 Ansichten der neuen Website/Handy/Startseite.jpg')]))
    fj = os.path.join(ROOT, 'feed', 'feed.json')
    if os.path.exists(fj):
        for f in sorted(glob.glob(os.path.join(ROOT, 'feed', 'posts', '*.jpg'))):
            lege('06 Instagram/Beiträge', f, 'Beitrag ' + os.path.basename(f))
        lege('06 Instagram', os.path.join(ROOT, 'feed', 'avatar.jpg'), 'Profilbild.jpg')
        fd = json.load(open(fj))
        K.schreib(os.path.join(ZIEL, '06 Instagram', 'Texte zu den Beiträgen.txt'),
                  'Biografie\n' + fd['profil']['titel'] + '\n' + '\n'.join(fd['profil']['bio']) + '\n' + fd['profil']['link'] + '\n\n' + '\n\n'.join(f"Beitrag {p['n']}\n{p['cap']}" for p in fd['posts']) + '\n')
        O.append(('Instagram', f'Die {zahl(len(fd["posts"])).lower()} Beiträge in voller Grösse, das Profilbild und die Texte dazu.', [('Profilbild', '06 Instagram/Profilbild.jpg'), ('Texte zu den Beiträgen', '06 Instagram/Texte zu den Beiträgen.txt'), ('Erster Beitrag', '06 Instagram/Beiträge/Beitrag 01.jpg')]))
    FL = ['fl--papier', 'fl--creme']
    teile = ''
    for i, (name, satz, dateien) in enumerate(O):
        zeilen = ''.join(f'<li data-a="auf" style="--i:{min(k, 6)}"><a href="{e(h)}" target="_blank" rel="noopener"><span>{e(t)}</span><i>{PF}</i></a></li>' for k, (t, h) in enumerate(dateien))
        teile += f'''<section class="fl {FL[i % 2]} blatt ordnerz" id="o{i + 1}">
  <div class="in">
    <div>{kap(i + 1, e(name))}<div class="lauf"><p data-a="worte">{e(satz)}</p></div></div>
    <ul class="dateien{" dateien--2" if len(dateien) > 6 else ""}">{zeilen}</ul>
  </div>
</section>
'''
    streu = ''.join(f'<div class="{kl}" data-a="schweb" style="left:{x}%;top:{y}%;width:{b}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}"><img src="{src}" alt=""></div>' for i, (kl, src, x, y, b, r) in enumerate(H.MATERIAL['auslage']))
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('material'), 'Material')}
      {titel(['Alles liegt für', 'Sie bereit.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">Was für den Entwurf neu entstanden ist, liegt hier sortiert in {zahl(len(O)).lower()} Ordnern. Sie können jede Datei ansehen und herunterladen.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#material')}</div>
    </div>
    <div class="auslage" aria-hidden="true">{streu}</div>
  </div>
</section>
{teile}
<section class="ausklang"><div class="in"><p data-a="auf">Fehlt Ihnen eine Datei oder ein Format, schreiben Sie mir gern.</p><div class="kn-reihe" data-a="auf">{kn('Robert schreiben', 'mailto:robert@tasty-studios.de?subject=' + N.replace(' ', '%20') + '%20Material')}{kn('Zur Werkbank', '../werkbank/index.html#material', 'kn--linie')}</div></div></section>'''
    seite = K.rahmen('Material', f'Alles, was für den Entwurf der neuen Website des {N} entstanden ist, sortiert zum Ansehen und Herunterladen.', 'Material', haupt,
                     f'Die Dateien gehören zum Entwurf von Robert Reff, Tasty Studios, und sind keine offiziellen Unterlagen des Hauses. Fotos, Zeichen und Texte gehören {H.RECHTE}')
    K.schreib(os.path.join(ZIEL, 'index.html'), seite)
    anzahl = sum(len(fs) for _, _, fs in os.walk(ZIEL)) - 1
    print('Material:', len(O), 'Ordner,', anzahl, 'Dateien,', n_an, 'Ansichten')


if __name__ == '__main__':
    baue()
