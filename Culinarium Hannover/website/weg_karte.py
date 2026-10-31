#!/usr/bin/env python3
"""Culinarium Hannover · Der Weg: die gezeichnete Karte im Strich des Hauses (Robert 28.10.2026: «eine im Stil des Hauses gezeichnete Karte bei der Weg»;
die Öffnungszeiten der Bar stehen bei «Das Haus», hier nicht mehr). Strassen, Ihme, Parks und Haltestellen aus OpenStreetMap
(`_quelle/karte/osm-linden-2026-10-28.json`), als feine Linien auf Nacht, die Bar als Schild in Kerze an der Ecke Haasemannstraße / Rampenstraße.
Ein bewegter Moment: das Schild der Bar setzt sich und pulst einmal (nur transform). Kein Lichthof (Robert 28.10.2026: «sieht billig umgesetzt aus»); die Ecke zeigt sich durch Haasemannstraße und Rampenstraße in Kerze. Am Handy zeigt die Karte die Mitte (slice).
Aufruf aus varianten.py (WEGSEITE, wand_html); zum Probieren: python3 website/weg_karte.py > /tmp/karte.svg"""
import json, math, os
HIER = os.path.dirname(os.path.abspath(__file__))
LAT0, LON0 = 52.3702598, 9.7134621          # Haasemannstraße 13
W, H = 1400, 760
M_PX = 0.62                                   # Meter je Bildpunkt → 868 × 471 m
MLAT, MLON = 111320.0, 111320.0 * math.cos(math.radians(LAT0))
NAMEN = ['Limmerstraße', 'Deisterstraße', 'Blumenauer Straße', 'Haasemannstraße', 'Rampenstraße', 'Stephanusstraße', 'Fössestraße', 'Falkenstraße',
         'Von-Alten-Allee', 'Egestorffstraße', 'Kötnerholzweg', 'Schwarzer Bär', 'Am Küchengarten', 'Elisenstraße', 'Spinnereistraße', 'Davenstedter Straße',
         'Minister-Stüve-Straße', 'Nieschlagstraße', 'Pfarrlandstraße', 'Posthornstraße', 'Ricklinger Straße', 'Stärkestraße', 'Lindener Marktplatz']
KLASSEN = {'tertiary': 3.2, 'tertiary_link': 3.2, 'residential': 1.9, 'living_street': 1.6, 'pedestrian': 2.6, 'unclassified': 1.9}
HALTE = {'Am Küchengarten', 'Lindener Marktplatz', 'Schwarzer Bär', 'Leinaustraße', 'Glocksee'}


def xy(p):
    return ((p['lon'] - LON0) * MLON / M_PX + W / 2, (LAT0 - p['lat']) * MLAT / M_PX + H / 2)


def pfad(pts, schliessen=False):
    return 'M' + 'L'.join('%.1f %.1f' % xy(p) for p in pts) + ('Z' if schliessen else '')


def im_bild(pts, rand=0):
    return any(-rand <= x <= W + rand and -rand <= y <= H + rand for x, y in map(xy, pts))


def laenge(pts):
    q = list(map(xy, pts))
    return sum(math.hypot(q[i + 1][0] - q[i][0], q[i + 1][1] - q[i][1]) for i in range(len(q) - 1))


def ringe(stuecke):
    """Aussenwege eines Multipolygons zu geschlossenen Ringen verketten (Enden gleich = anschliessen)."""
    k = lambda p: (round(p['lat'], 7), round(p['lon'], 7))
    rest, out = [list(s) for s in stuecke], []
    while rest:
        ring = rest.pop(0)
        hin = True
        while hin and k(ring[0]) != k(ring[-1]):
            hin = False
            for i, s in enumerate(rest):
                if k(s[0]) == k(ring[-1]): ring += s[1:]; rest.pop(i); hin = True; break
                if k(s[-1]) == k(ring[-1]): ring += list(reversed(s))[1:]; rest.pop(i); hin = True; break
                if k(s[-1]) == k(ring[0]): ring = s[:-1] + ring; rest.pop(i); hin = True; break
                if k(s[0]) == k(ring[0]): ring = list(reversed(s))[:-1] + ring; rest.pop(i); hin = True; break
        out.append(ring)
    return out


def karte():
    d = json.load(open(os.path.join(HIER, '..', '_quelle', 'karte', 'osm-linden-2026-10-28.json')))
    els = d['elements']
    wasser, parks, strassen, namen_wege, halte = [], [], [], {}, {}
    for e in els:
        t = e.get('tags', {})
        if e['type'] == 'way' and 'geometry' in e:
            g = e['geometry']
            if t.get('natural') == 'water' or t.get('waterway') == 'riverbank':
                wasser.append(pfad(g, True))
            elif t.get('leisure') == 'park' or t.get('landuse') == 'grass':
                if im_bild(g): parks.append(pfad(g, True))
            elif t.get('highway') in KLASSEN and t.get('area') != 'yes' and im_bild(g, 40):   # Plätze (area=yes) nicht als Umriss zeichnen
                strassen.append((KLASSEN[t['highway']], pfad(g), t.get('highway') + (' ecke' if t.get('name') in ('Haasemannstraße', 'Rampenstraße') else '')))
                n = t.get('name')
                if n in NAMEN:
                    namen_wege.setdefault(n, []).append(g)
        elif e['type'] == 'relation' and t.get('natural') == 'water':
            for ring in ringe([m['geometry'] for m in e.get('members', []) if m.get('role') == 'outer' and 'geometry' in m]):
                wasser.append(pfad(ring, True))
        elif e['type'] == 'node' and t.get('railway') == 'tram_stop' and t.get('name') in HALTE:
            halte.setdefault(t['name'], []).append(e)
    # Namen: je Strasse der längste Zug im Bild, Text läuft von links nach rechts (oder von unten nach oben)
    labels = []
    for n, wege in namen_wege.items():
        wege = [g for g in wege if im_bild(g)]
        if not wege: continue
        g = max(wege, key=laenge)
        q = list(map(xy, g))
        if q[0][0] > q[-1][0] + 1 or (abs(q[0][0] - q[-1][0]) <= 1 and q[0][1] < q[-1][1]):
            g = list(reversed(g))
        l = laenge(g)
        if l < 90: continue
        labels.append((n, 'M' + 'L'.join('%.1f %.1f' % xy(p) for p in g), l))
    # Haltestellen: ein Punkt je Name (Mittel der Knoten)
    stops = []
    for n, ks in halte.items():
        x = sum(xy(k)[0] for k in ks) / len(ks); y = sum(xy(k)[1] for k in ks) / len(ks)
        if -20 <= x <= W + 20 and -20 <= y <= H + 20:
            stops.append((n, x, y))
    bx, by = xy({'lat': LAT0, 'lon': LON0})
    svg = ['<svg class="wk-karte" viewBox="0 0 %d %d" role="img" aria-label="Karte: Walk on the Wild Side, Haasemannstraße 13, Ecke Rampenstraße, in Hannover-Linden" preserveAspectRatio="xMidYMid slice">' % (W, H)]
    svg.append('<defs><clipPath id="wk-clip"><rect width="%d" height="%d"/></clipPath></defs>' % (W, H))
    svg.append('<rect width="%d" height="%d" fill="#15141A"/>' % (W, H))
    svg.append('<g clip-path="url(#wk-clip)">')
    svg.append('<g class="wk-wasser">%s</g>' % ''.join('<path d="%s"/>' % p for p in wasser))
    svg.append('<g class="wk-park">%s</g>' % ''.join('<path d="%s"/>' % p for p in parks))
    svg.append('<text class="wk-ort" x="%d" y="%d" text-anchor="middle">Linden</text>' % (W / 2, H / 2 + 56))
    for breite, p, art in sorted(strassen, key=lambda s: s[0]):
        svg.append('<path class="wk-s %s" d="%s" stroke-width="%.1f"/>' % (art, p, breite))
    svg.append('<defs>%s</defs>' % ''.join('<path id="wk-n%d" d="%s"/>' % (i, p) for i, (_n, p, _l) in enumerate(labels)))
    svg.append('<g class="wk-namen">%s</g>' % ''.join('<text><textPath href="#wk-n%d" startOffset="50%%" text-anchor="middle">%s</textPath></text>' % (i, n.upper()) for i, (n, _p, _l) in enumerate(labels)))
    svg.append('<g class="wk-halte">%s</g>' % ''.join(
        '<g transform="translate(%.1f %.1f)"><circle r="7"/><circle r="2.4" class="wk-hp"/><text x="13" y="4">%s</text></g>' % (x, y, n) for n, x, y in stops))
    # die Bar: Lichthof, Schild in Kerze mit Namen, Leitlinie zum Text
    svg.append('<g class="wk-bar" transform="translate(%.1f %.1f)">'
               '<g class="wk-schild"><rect x="-9" y="-9" width="18" height="18" rx="2"/><rect x="-5" y="-5" width="10" height="10" rx="1" class="wk-schild-in"/></g>'
               '<path class="wk-leit" d="M-14 -14 L-58 -58 L-96 -58"/>'
               '<text class="wk-bar-name" x="-104" y="-52" text-anchor="end">Walk on the Wild Side</text><text class="wk-bar-satz" x="-104" y="-30" text-anchor="end">Haasemannstraße 13 · Ecke Rampenstraße</text></g>' % (bx, by))
    # Nordpfeil und Massstab
    svg.append('<g class="wk-nord" transform="translate(%d 56)"><path d="M0 -22 L7 6 L0 1 L-7 6 Z"/><text y="26" text-anchor="middle">N</text></g>' % (W - 60))
    m100 = 100 / M_PX
    svg.append('<g class="wk-mass" transform="translate(%d %d)"><path d="M0 0 H%.1f M0 -6 V6 M%.1f -6 V6"/><text x="%.1f" y="22" text-anchor="middle">100 m</text></g>' % (48, H - 48, m100, m100, m100 / 2))
    svg.append('</g></svg>')
    return ('<div class="wk-rahmen auf"><div class="wk-platte">%s</div><p class="wk-unter">Walk on the Wild Side<span>Haasemannstraße 13 · Ecke Rampenstraße</span></p>'
            '<p class="wk-quelle mono">Karte nach OpenStreetMap</p></div>') % ''.join(svg)


if __name__ == '__main__':
    print(karte())
