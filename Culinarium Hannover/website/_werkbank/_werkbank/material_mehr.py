#!/usr/bin/env python3
"""Culinarium: Sticker und Beigaben in den Ordner «Material» (Prüfchat Gestaltung 29.10.2026). Läuft nach material.py des Kits:
legt die PDFs und Bilder unter material/07 Sticker und material/08 Beigaben ab und setzt die zwei Ordner in material/index.html vor den Ausklang.
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/material_mehr.py "<website/_werkbank>"   (wiederholbar)"""
import json, os, re
import kern as K
from kern import H, ROOT, W, e, kap, PF
from material import lege, ZIEL


def baue():
    N = H.NAME
    sp = json.load(open(os.path.join(W, 'sticker_plan.json')))
    bp = json.load(open(os.path.join(W, 'beigaben_plan.json')))
    st = [('Druckbogen A3', lege('07 Sticker', os.path.join(ROOT, 'sticker', 'pdf', f'{H.KURZ}-sticker-druckbogen-a3.pdf'), f'{N} Sticker Druckbogen A3.pdf')),
          ('Alle einzeln', lege('07 Sticker', os.path.join(ROOT, 'sticker', 'pdf', f'{H.KURZ}-sticker-einzeln.pdf'), f'{N} Sticker einzeln.pdf'))]
    for x in sp['etiketten']:
        lege('07 Sticker/Bilder', os.path.join(W, 'roh', 'sticker', x['id'] + '.png'), 'Sticker ' + x['id'][1:] + ' ' + re.sub(r'[/:’]', ' ', x['name']).strip() + '.png')
    bg = [(d['name'], lege('08 Beigaben', os.path.join(ROOT, 'beigaben', 'pdf', f"{H.KURZ}-{d['id']}.pdf"), f"{N} {d['name']}.pdf")) for d in bp['druck']]
    pk = [(t, lege('09 Postkarten', os.path.join(ROOT, 'postkarten', 'pdf', f'{H.KURZ}-postkarten-{d}.pdf'), f'{N} Postkarten {t}.pdf'))
          for d, t in (('druck', 'mit Beschnitt'), ('sammelbogen-a3', 'Sammelbogen SRA3')) if os.path.exists(os.path.join(ROOT, 'postkarten', 'pdf', f'{H.KURZ}-postkarten-{d}.pdf'))]   # Oberchef 29.10.2026
    teile = ''
    for i, (name, satz, dateien, ident) in enumerate([('Sticker', f'Vierzig Sticker: der Druckbogen mit Schnittlinien, jeder einzeln und alle als Bild.', st, 'o-sticker'),
                                                       ('Beigaben', 'Menü-Rolle, Streichholzbriefchen, Drink-Fähnchen, Rezeptkarte und Gutschein, jede als PDF.', bg, 'o-beigaben'),
                                                       ('Postkarten', str(len(json.load(open(os.path.join(W, 'postkarten_plan.json')))['karten'])) + ' Postkarten, eine zu jedem Plakat: mit Beschnitt für die Druckerei und als Sammelbogen SRA3.', pk, 'o-postkarten')]):
        zeilen = ''.join(f'<li data-a="auf" style="--i:{min(k, 6)}"><a href="{e(h)}" target="_blank" rel="noopener"><span>{e(t)}</span><i>{PF}</i></a></li>' for k, (t, h) in enumerate(dateien))
        teile += f'''<section class="fl {['fl--papier', 'fl--creme', 'fl--papier'][i]} blatt ordnerz" id="{ident}">
  <div class="in">
    <div>{kap(7 + i, e(name))}<div class="lauf"><p data-a="worte">{e(satz)}</p></div></div>
    <ul class="dateien">{zeilen}</ul>
  </div>
</section>
'''
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r'<section class="fl [^"]*" id="o-(sticker|beigaben|postkarten)">.*?</section>\n', '', s, flags=re.S)
    s = s.replace('<section class="ausklang">', teile + '<section class="ausklang">', 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('Material: Sticker', len(sp['etiketten']), '· Beigaben', len(bp['druck']))


if __name__ == '__main__':
    K.gestaltung(); baue()
