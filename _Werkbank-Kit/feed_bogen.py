#!/usr/bin/env python3
"""Feed als Bogen: das ganze Profil-Raster wird als eine Fläche geplant, nicht Beitrag für Beitrag (Feed-Planer, Robert 17.10.2026,
Master 5a Regel 10a: «dass jeder Instagram-Feed wirklich individuell und einzigartig strukturiert wird»).

Ein Stück liegt auf dem Raster (drei Spalten) und darf mehrere Felder decken: ein Foto, ein Plakat über drei Beiträge (w=3),
ein Hochformat über zwei oder drei Reihen (h=2/3), ein Block 2×2, ein Bild über sechs Beiträge (w=3, h=2) oder eine Tafel.
Jedes Stück wird in einem Stück gerechnet und dann in Beiträge 1080 × 1350 geschnitten. Im Raster zeigt Instagram von jedem Beitrag
nur die Mitte 3:4 (1012,5 px), deshalb ist ein Stück w·1012,5 + 2·33,75 px breit und h·1350 px hoch; nebeneinander schliessen
die Teile lückenlos an, geöffnet zeigt jeder Beitrag 33,75 px mehr an jedem Rand.

Im feed_daten.py des Hauses:
  REGEL = 'bogen'
  BOGEN = [dict(id=…, r=Reihe, c=Spalte, w=1, h=1, art='foto'|'html', bild=Schlüssel, fx=.5, fy=.5, html=…, texte=[…]), …]
          texte: ein Beitragstext je gedecktem Feld, Reihe für Reihe von links nach rechts.
          art 'html': html darf {bild:Schlüssel} enthalten, das wird zum Pfad einer getönten Fassung des Fotos.
  QUELLEN = ('_quelle',)   (Ordner, in denen die Originale aus assets/img/manifest.json liegen; ohne: die Fassung der Website)
  BOGEN_CSS = '…'   (Gestaltung der Tafeln, Schriften mit url('../_werkbank/fonts/…') relativ zu feed/)
  P = feed_bogen.p_liste(BOGEN)   (für feed.py: ein Eintrag je Beitrag, Motiv-Schlüssel eindeutig)
Gebaut wird über feed.py des Kits (oder des Hauses): bei REGEL 'bogen' ruft es bauen() und danach tafeln(), thumbs(), seite().
Nur echte Fotos des Hauses, nie Gästefotos, nie erzeugte Bilder (Master 5a Regel 10)."""
import html as _html, json, os, subprocess
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

SP, RAND, PH, PW = 1012.5, 33.75, 1350, 1080
KIT = os.path.dirname(os.path.abspath(__file__))


def masse(w, h):
    return round(w * SP + 2 * RAND), h * PH


def felder(st):
    return [(st['r'] + i, st['c'] + j) for i in range(st.get('h', 1)) for j in range(st.get('w', 1))]


def raster(BOGEN):
    """Feld (Reihe, Spalte) → (Stück, Nummer im Stück). Prüft: jedes Feld genau einmal, nichts ragt über drei Spalten."""
    belegt = {}
    for st in BOGEN:
        assert st['c'] + st.get('w', 1) <= 3, ('ragt hinaus', st['id'])
        fs = felder(st)
        assert len(st.get('texte', [])) == len(fs), ('ein Text je Beitrag', st['id'], len(st.get('texte', [])), len(fs))
        for i, f in enumerate(fs):
            assert f not in belegt, ('Feld doppelt', f, st['id'], belegt.get(f, ('',))[0]['id'] if f in belegt else '')
            belegt[f] = (st, i)
    reihen = max(r for r, _ in belegt) + 1
    for r in range(reihen):
        for c in range(3):
            assert (r, c) in belegt, ('Feld leer', r + 1, c + 1)
    assert len({st['id'] for st in BOGEN}) == len(BOGEN), 'id doppelt'
    return belegt, reihen


def p_liste(BOGEN):
    belegt, reihen = raster(BOGEN)
    return [('x', (belegt[(r, c)][0]['id'], belegt[(r, c)][1]), belegt[(r, c)][0]['texte'][belegt[(r, c)][1]]) for r in range(reihen) for c in range(3)]


_MANI = {}


def _finde(ROOT, quelle, key, basen=()):
    """Grösste Fassung eines Fotos: zuerst das Original aus der Quelle (assets/img/manifest.json, Feld «quelle», gesucht in basen),
    sonst die Fassung der Website (quelle() des Hauses), sonst ein Pfad relativ zum Projekt."""
    if basen:
        if ROOT not in _MANI:
            m = os.path.join(ROOT, 'assets', 'img', 'manifest.json')
            _MANI[ROOT] = json.load(open(m)) if os.path.exists(m) else {}
        q = (_MANI[ROOT].get(key) or {}).get('quelle')
        for b in basen if q else ():
            p = os.path.join(ROOT, b, q)
            if os.path.exists(p):
                return p
    try:
        return quelle(key)
    except FileNotFoundError:
        q = os.path.join(ROOT, key)
        if os.path.exists(q):
            return q
        raise


def _zuschnitt(im, zw, zh, fx, fy):
    w, h = im.size
    if w / h >= zw / zh:
        nw = h * zw / zh; x0 = max(0, min(w - nw, w * fx - nw / 2)); box = (x0, 0, x0 + nw, h)
    else:
        nh = w * zh / zw; y0 = max(0, min(h - nh, h * fy - nh / 2)); box = (0, y0, w, y0 + nh)
    teil = im.crop(tuple(round(v) for v in box))
    faktor = zw / teil.width
    teil = teil.resize((zw, zh), Image.LANCZOS)
    if faktor > 1.05:   # hochgerechnet: etwas nachschärfen, damit der geöffnete Beitrag nicht weich wirkt
        teil = teil.filter(ImageFilter.UnsharpMask(radius=1.6, percent=min(90, int(40 + 40 * (faktor - 1))), threshold=2))
    return teil, faktor


def _schneide(bild, st, POSTS, nr_von):
    for i, (r, c) in enumerate(felder(st)):
        x = round((c - st['c']) * SP); y = (r - st['r']) * PH
        bild.crop((x, y, x + PW, y + PH)).convert('RGB').save(os.path.join(POSTS, f'{nr_von[(r, c)]:02d}.jpg'), quality=91)


def bauen(ROOT, D, quelle, ton):
    ZIEL = os.path.join(ROOT, 'feed'); POSTS = os.path.join(ZIEL, 'posts'); ST = os.path.join(ZIEL, '_stuecke')
    for d in (POSTS, ST):
        os.makedirs(d, exist_ok=True)
    belegt, reihen = raster(D.BOGEN)
    nr_von = {(r, c): r * 3 + c + 1 for r in range(reihen) for c in range(3)}
    bericht = []
    # 1 Fotos direkt
    for st in D.BOGEN:
        if st.get('art', 'foto') != 'foto':
            continue
        zw, zh = masse(st.get('w', 1), st.get('h', 1))
        im = ImageOps.exif_transpose(Image.open(_finde(ROOT, quelle, st['bild'], getattr(D, 'QUELLEN', ())))).convert('RGB')
        teil, faktor = _zuschnitt(im, zw, zh, st.get('fx', .5), st.get('fy', .5))
        teil = ton(teil)
        teil.save(os.path.join(ST, st['id'] + '.jpg'), quality=90)
        _schneide(teil, st, POSTS, nr_von)
        bericht.append((st['id'], st.get('w', 1), st.get('h', 1), round(faktor, 2)))
    # 2 Tafeln und Plakate als Seite, ein Abschnitt je Stück
    tafeln = [st for st in D.BOGEN if st.get('art') == 'html']
    if tafeln:
        teile = ''
        for st in tafeln:
            zw, zh = masse(st.get('w', 1), st.get('h', 1))
            inhalt = st['html']
            while '{bild:' in inhalt:
                a = inhalt.index('{bild:'); b = inhalt.index('}', a); key = inhalt[a + 6:b]
                ziel = os.path.join(ST, 'q-' + key.replace('/', '_') + '.jpg')
                qp = _finde(ROOT, quelle, key, getattr(D, 'QUELLEN', ()))
                if not os.path.exists(ziel) or os.path.getmtime(ziel) < os.path.getmtime(qp):
                    q = ImageOps.exif_transpose(Image.open(qp)).convert('RGB')
                    ton(q).save(ziel, quality=93)
                inhalt = inhalt[:a] + '_stuecke/' + os.path.basename(ziel) + inhalt[b + 1:]
            teile += f'<section class="st {st.get("klasse", "")}" data-id="{_html.escape(st["id"])}" style="width:{zw}px;height:{zh}px">{inhalt}</section>\n'
        seite = (f'<!doctype html><html lang="de-CH"><meta charset="utf-8"><style>*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#555}}'
                 f'.st{{position:relative;overflow:hidden;margin:0 0 40px}}{getattr(D, "BOGEN_CSS", "")}</style><body>{teile}</body></html>')
        open(os.path.join(ZIEL, '_bogen.html'), 'w', encoding='utf-8').write(seite)
        subprocess.run(['node', os.path.join(KIT, 'feed_bogen_druck.js'), os.path.join(ZIEL, '_bogen.html'), ST], check=True)
        for st in tafeln:
            bild = Image.open(os.path.join(ST, st['id'] + '.png')).convert('RGB')
            zw, zh = masse(st.get('w', 1), st.get('h', 1))
            assert bild.size == (zw, zh), (st['id'], bild.size, (zw, zh))
            _schneide(bild, st, POSTS, nr_von)
            bericht.append((st['id'], st.get('w', 1), st.get('h', 1), 'Tafel'))
    # alte Beiträge über der neuen Zahl weg (der Feed kann kürzer sein als vorher)
    for f in os.listdir(POSTS):
        if f[:2].isdigit() and int(f[:2]) > reihen * 3:
            os.remove(os.path.join(POSTS, f))
    th = os.path.join(ZIEL, 'thumbs')
    if os.path.isdir(th):
        for f in os.listdir(th):
            if f[:2].isdigit() and int(f[:2]) > reihen * 3:
                os.remove(os.path.join(th, f))
    json.dump({'reihen': reihen, 'stuecke': [dict(id=s['id'], r=s['r'] + 1, c=s['c'] + 1, w=s.get('w', 1), h=s.get('h', 1), art=s.get('art', 'foto'), bild=s.get('bild', '')) for s in D.BOGEN]},
              open(os.path.join(ZIEL, 'bogen.json'), 'w'), ensure_ascii=False, indent=1)
    weich = [b for b in bericht if isinstance(b[3], float) and b[3] > 1.6]
    print('Bogen:', reihen, 'Reihen,', len(D.BOGEN), 'Stücke,', len(tafeln), 'Tafeln', ('· stark hochgerechnet: ' + ', '.join(f'{b[0]} ×{b[3]}' for b in weich)) if weich else '')
    return bericht
