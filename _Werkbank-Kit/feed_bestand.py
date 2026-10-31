#!/usr/bin/env python3
"""Bestandsabgleich des Feeds (Oberchef 29.10.2026, Robert: «die werden jetzt nicht ihren gesamten Feed löschen … Bilder von Essen oder so will
ich jetzt nicht doppelt drin haben … bei den Plakaten … eine Ausnahme»). Der Feed der Werkbank setzt den echten Instagram-Feed fort: kein Foto,
das dort schon steht, kommt nochmal vor, auch nicht als anderer Ausschnitt. Ausnahmen (z. B. Plakate) schaltet jedes Haus selbst frei.

Läuft in feed.py vor dem Bau, immer wenn es einen Instagram-Bestand gibt:
  feed_daten.py des Hauses (alles freiwillig):
    IG_BESTAND = ['../../_quelle/extern/ig/*.jpg', …]   Globs relativ zu <Projekt> (Ordner mit _werkbank/), ohne Angabe: <Haus>/_quelle/extern/ig/*.jpg
    BESTAND_AUSNAHMEN = ('p_', 'pl_')                   Schlüssel-Anfänge, die doppelt vorkommen dürfen (Plakate usw.)
    BESTAND_KANDIDATEN = ['r01', 'g2', …]               weitere Fotos, die nur für den Bericht abgeglichen werden (feed/bestand.json)
  Stücke mit bestand=True (die echten bisherigen Beiträge selbst) werden nicht geprüft.
Vergleich: pHash (DCT 8 × 8) des ganzen Bilds und dreier Mittelausschnitte, dazu ORB-Merkmale mit Homographie (findet andere Ausschnitte
desselben Fotos). Ergebnis: feed/bestand.json; doppelte Fotos brechen den Bau mit einer Liste ab.
Allein: python3 feed_bestand.py "<Projekt>"   (gleicher Abgleich, ohne Bau)"""
import glob, json, os, re, sys

import cv2
import numpy as np

ORB = cv2.ORB_create(nfeatures=1500)
BF = cv2.BFMatcher(cv2.NORM_HAMMING)
_CACHE = {}


def _grau(pfad):
    im = cv2.imdecode(np.fromfile(pfad, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    if im is None:   # WebP o. Ä., das OpenCV nicht liest: über Pillow
        from PIL import Image
        im = np.array(Image.open(pfad).convert('L'))
    k = 640 / max(im.shape)
    return cv2.resize(im, None, fx=k, fy=k, interpolation=cv2.INTER_AREA) if k < 1 else im


def _phash(g):
    d = cv2.dct(np.float32(cv2.resize(g, (32, 32), interpolation=cv2.INTER_AREA)))[:8, :8]
    return (d > np.median(d)).flatten()


def merkmale(pfad):
    if pfad not in _CACHE:
        g = _grau(pfad)
        h, w = g.shape
        hashes = [_phash(g)]
        for s in (.8, .65, .5):   # Mittelausschnitte: ein anders beschnittenes Original trifft einen davon
            ch, cw = int(h * s), int(w * s)
            hashes.append(_phash(g[(h - ch) // 2:(h + ch) // 2, (w - cw) // 2:(w + cw) // 2]))
        kp, des = ORB.detectAndCompute(g, None)
        _CACHE[pfad] = (hashes, kp, des, (w, h), g)
    return _CACHE[pfad]


def gleich(a, b):
    """(ja/nein, Grund): dasselbe Foto, auch als anderer Ausschnitt oder in anderer Grösse."""
    ha, ka, da, *_ = merkmale(a)
    hb, kb, db, *_ = merkmale(b)
    d = min(int(np.count_nonzero(x != y)) for x in ha for y in hb)
    if d <= 6:
        return True, f'pHash {d}'
    if da is None or db is None or len(ka) < 20 or len(kb) < 20:
        return False, ''
    paare = [m for m, n in (p for p in BF.knnMatch(da, db, k=2) if len(p) == 2) if m.distance < .75 * n.distance]
    if len(paare) < 25:
        return False, ''
    pa = np.float32([ka[m.queryIdx].pt for m in paare]); pb = np.float32([kb[m.trainIdx].pt for m in paare])
    H, maske = cv2.findHomography(pa, pb, cv2.RANSAC, 4.0)
    if H is None:
        return False, ''
    innen = int(maske.sum())
    # Gegenprobe am Bildinhalt: b auf a abbilden und im gemeinsamen Bereich vergleichen. Gleiche Vorlagen mit anderem Motiv
    # (jedes Plakat hat Rahmen, Wortmarke und Band an derselben Stelle) passen geometrisch, aber nicht im Inhalt.
    m_ = maske.ravel().astype(bool)
    if m_.sum() < 40 or innen / len(paare) < .5:
        return False, ''
    ga, gb = _CACHE[a][4], _CACHE[b][4]
    hoch, breit = ga.shape
    zu = cv2.warpPerspective(gb, np.linalg.inv(H), (breit, hoch))
    da_ = cv2.warpPerspective(np.ones_like(gb) * 255, np.linalg.inv(H), (breit, hoch)) > 0
    if da_.mean() < .15:
        return False, ''
    x = cv2.GaussianBlur(ga, (5, 5), 0)[da_].astype(np.float32); y = cv2.GaussianBlur(zu, (5, 5), 0)[da_].astype(np.float32)
    r = float(np.corrcoef(x, y)[0, 1]) if x.std() > 1 and y.std() > 1 else 0.
    if r >= .8:
        return True, f'Ausschnitt ({innen} Punkte, Inhalt {r:.2f})'
    return False, ''


def bestand_dateien(ROOT, D):
    globs = getattr(D, 'IG_BESTAND', None)
    if globs is None:   # Standard: <Haus>/_quelle/extern/ig/ (Haus = der Ordner über website/)
        haus = ROOT
        for _ in range(4):
            if os.path.isdir(os.path.join(haus, '_quelle', 'extern', 'ig')):
                break
            haus = os.path.dirname(haus)
        globs = [os.path.join(haus, '_quelle', 'extern', 'ig', '*.jpg')]
    out = []
    for g in globs:
        out += sorted(glob.glob(g if os.path.isabs(g) else os.path.join(ROOT, g)))
    return out


def _bilder_im_feed(D, quelle):
    """(Schlüssel, Pfad) aller Fotos des Feeds, ohne die echten bisherigen Beiträge."""
    out = []
    if getattr(D, 'REGEL', '') == 'bogen':
        for st in D.BOGEN:
            if st.get('bestand'):
                continue
            if st.get('art', 'foto') == 'foto':
                out.append((st.get('schluessel') or os.path.basename(st['bild']).rsplit('-', 1)[0], st['bild']))
            for pfad in re.findall(r'\{bild:([^}]+)\}', st.get('html', '')):
                out.append((os.path.basename(pfad).rsplit('-', 1)[0], pfad))
    else:
        for p in D.P:
            if p[0].partition(':')[0] in ('f', 'p', 'a'):
                out.append((p[1], p[1]))
    return [(k, v if os.path.isabs(v) and os.path.exists(v) else quelle(v)) for k, v in out]


def pruefen(ROOT, D, quelle):
    bestand = bestand_dateien(ROOT, D)
    if not bestand:
        return None
    aus = tuple(getattr(D, 'BESTAND_AUSNAHMEN', ()))
    quelle = getattr(D, 'quelle', None) or quelle   # das Bildregister des Hauses kennt mehr Schlüssel als das des Kits
    im_feed = _bilder_im_feed(D, quelle)
    extra = [(k, quelle(k)) for k in getattr(D, 'BESTAND_KANDIDATEN', ()) if k not in {x for x, _ in im_feed}]
    bericht, doppelt = {}, []
    ziel = os.path.join(ROOT, 'feed'); os.makedirs(ziel, exist_ok=True)
    # Zwischenspeicher: ein Foto wird nur neu verglichen, wenn es oder der Bestand sich geändert hat
    cache_pfad = os.path.join(ziel, 'bestand-cache.json')
    zeichen = '|'.join(f'{os.path.basename(b)}:{int(os.path.getmtime(b))}' for b in bestand)
    try:
        cache = json.load(open(cache_pfad))
        cache = cache['fotos'] if cache.get('bestand') == zeichen else {}
    except (OSError, ValueError, KeyError):
        cache = {}
    for k, pfad in im_feed + extra:
        if k in bericht:
            continue
        ck = f'{pfad}:{int(os.path.getmtime(pfad))}'
        if ck not in cache:
            cache[ck] = next(([os.path.basename(b), grund] for b in bestand for ja, grund in [gleich(pfad, b)] if ja), None)
        treffer = cache[ck]
        bericht[k] = dict(im_feed=any(k == x for x, _ in im_feed), ausnahme=k.startswith(aus) if aus else False,
                          gepostet=treffer[0] if treffer else '', grund=treffer[1] if treffer else '')
        if treffer and bericht[k]['im_feed'] and not bericht[k]['ausnahme']:
            doppelt.append(f'{k} ist schon gepostet ({treffer[0]}, {treffer[1]})')
    json.dump(dict(bestand=zeichen, fotos=cache), open(cache_pfad, 'w'))
    json.dump(dict(bestand=[os.path.basename(b) for b in bestand], ausnahmen=list(aus), fotos=bericht, doppelt=doppelt),
              open(os.path.join(ziel, 'bestand.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'Bestand: {len(bestand)} gepostete Bilder · {len(im_feed)} Bilder im Feed geprüft · {sum(1 for v in bericht.values() if v["gepostet"])} schon gepostet'
          f' · doppelt im Feed: {len(doppelt)}')
    if doppelt:
        raise SystemExit('Feed nicht gebaut, diese Fotos stehen schon im Instagram-Feed des Hauses:\n  ' + '\n  '.join(doppelt))
    return bericht


if __name__ == '__main__':
    ROOT = os.path.abspath(sys.argv[1])
    sys.path.insert(0, os.path.join(ROOT, '_werkbank')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import feed_daten as D
    pruefen(ROOT, D, getattr(D, 'quelle', None) or (lambda k: k))
