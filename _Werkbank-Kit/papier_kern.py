#!/usr/bin/env python3
"""Ideen für Papier: Bausteine zum Setzen von Drucksachen und Etiketten in mm (Vorlage: Carlton-Europe/_werkbank/papier.py).
   Je Haus: <Projekt>/_werkbank/papier.py  →  importiert diese Bausteine, setzt die Stücke und ruft am Ende fertig(plan).
   Danach: node papier_druck.js "<Projekt>"  und  python3 papier_seiten.py "<Projekt>".
   Keine CSS-Masken und keine weichen Schatten im Druck (die Apple-Vorschau zeichnet sie falsch): Formen sind Pfade."""
import html, json, math, os
import kern as K
from kern import H, ROOT, W

SATZ = os.path.join(W, 'satz'); os.makedirs(SATZ, exist_ok=True)
e = html.escape
F = H.FARBEN
DEFS = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><g id="hz">' + H.ZEICHEN[1] + '</g><g id="hw">' + H.WORT[1] + '</g>' + getattr(H, 'DEFS_MEHR', '') + '</defs></svg>'
_zb, _zh = (float(x) for x in H.ZEICHEN[0].split()[2:])
_wb, _wh = (float(x) for x in H.WORT[0].split()[2:])
_zx, _zy = (float(x) for x in H.ZEICHEN[0].split()[:2])
_wx, _wy = (float(x) for x in H.WORT[0].split()[:2])
FAM = {'s': H.SCHRIFT['titel'][0], 'm': 'DM Mono', 'i': 'Instrument Sans'}


def hz(x, y, b, farbe, mitte=True):
    """Das Zeichen des Hauses, unverändert. x, y in mm, b = Breite in mm."""
    h = b * _zh / _zb
    return f'<svg class="abs" style="left:{x - (b / 2 if mitte else 0)}mm;top:{y}mm;width:{b}mm;height:{h}mm;color:{farbe}" viewBox="{H.ZEICHEN[0]}" fill="currentColor"><use href="#hz"/></svg>'


def hw(x, y, b, farbe, mitte=True):
    """Schriftzug / Wortmarke des Hauses."""
    h = b * _wh / _wb
    return f'<svg class="abs" style="left:{x - (b / 2 if mitte else 0)}mm;top:{y}mm;width:{b}mm;height:{h}mm;color:{farbe}" viewBox="{H.WORT[0]}" fill="currentColor"><use href="#hw"/></svg>'


def t(x, y, text, kl='', stil='', b=None):
    """Text an mm-Koordinaten (y = Oberkante). kl: s Titelschrift, m mono, c zentriert, r rechts."""
    br = f'width:{b}mm;' if b else ''
    return f'<div class="t {kl}" style="left:{x}mm;top:{y}mm;{br}{stil}">{text}</div>'


def lin(x, y, b, farbe=None, d=.25):
    return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{b}mm;height:{d}mm;background:{farbe or F["messing"]}"></i>'


def linv(x, y, h, farbe=None, d=.25):
    return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{d}mm;height:{h}mm;background:{farbe or F["messing"]}"></i>'


def rahmen(a, farbe, r=3, d=.25):
    return f'<i class="abs" style="inset:{a}mm;border:{d}mm solid {farbe};border-radius:{r}mm"></i>'


def kasten(x, y, b, h, stil):
    return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{b}mm;height:{h}mm;{stil}"></i>'


def foto(key, x, y, b, h, lage='50% 50%', mehr=''):
    pfad = os.path.relpath(K.hausbild(key), SATZ)
    return f'<img class="abs" src="{e(pfad)}" style="left:{x}mm;top:{y}mm;width:{b}mm;height:{h}mm;object-fit:cover;object-position:{lage};{mehr}">'


def blatt(b, h, innen, kl='', stil='', form=''):
    """Eine Seite in mm. form = Aussparung für die Vorschau (im Druck bleibt das Blatt rechteckig, die Kontur ist gezeichnet)."""
    f = f' data-form="{form}"' if form else ''
    return f'<section class="blatt {kl}" data-b="{b}" data-h="{h}"{f} style="width:{b}mm;height:{h}mm;{stil}">{innen}</section>'


def seite(ident, blaetter, titel):
    doc = f'''<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><title>{e(titel)} · {e(H.NAME)}</title>
<link rel="stylesheet" href="papier.css"></head><body>{DEFS}{''.join(blaetter)}</body></html>'''
    K.schreib(os.path.join(SATZ, ident + '.html'), doc)


# ---------------------------------------------------------------- Etiketten (SVG, Masse in mm)
def etikett(ident, b, h, form, innen, name, satz):
    """form: SVG-Pfad der Aussenkontur (Druck und Schnitt), innen: Zeichnung."""
    return {'id': ident, 'b': b, 'h': h, 'form': form, 'innen': innen, 'name': name, 'satz': satz}


def tx(x, y, text, groesse, farbe, art='s', sperr=0, anker='middle', mehr=''):
    return f'<text x="{x}" y="{y}" text-anchor="{anker}" font-family="{FAM[art]}" font-size="{groesse}" letter-spacing="{sperr}em" fill="{farbe}" {mehr}>{text}</text>'


def bogen_text(ident, d, text, groesse, farbe, art='m', sperr=.2):
    return (f'<path id="{ident}" d="{d}" fill="none"/><text font-family="{FAM[art]}" font-size="{groesse}" letter-spacing="{sperr}em" fill="{farbe}" text-anchor="middle"><textPath href="#{ident}" startOffset="50%">{text}</textPath></text>')


def hzz(x, y, b, farbe):
    """Zeichen des Hauses innerhalb eines SVG (Etikett): x = Mitte, y = Oberkante, b = Breite."""
    s = b / _zb
    return f'<g transform="translate({x - b / 2},{y}) scale({s})" fill="{farbe}"><g transform="translate({-_zx},{-_zy})"><use href="#hz"/></g></g>'


def hwz(x, y, b, farbe):
    s = b / _wb
    return f'<g transform="translate({x - b / 2},{y}) scale({s})" fill="{farbe}"><g transform="translate({-_wx},{-_wy})"><use href="#hw"/></g></g>'


def stern(x, y, r, farbe, zacken=4):
    p = []
    for i in range(zacken * 2):
        a = math.pi / zacken * i - math.pi / 2
        rr = r if i % 2 == 0 else r * .34
        p.append(f'{x + rr * math.cos(a):.2f},{y + rr * math.sin(a):.2f}')
    return f'<polygon points="{" ".join(p)}" fill="{farbe}"/>'


def strich(b=18, y=0, x=0, farbe=None, d=.35):
    return f'<rect x="{x - b / 2}" y="{y}" width="{b}" height="{d}" fill="{farbe or F["gold"]}"/>'


def fertig(druck, etiketten, meins, bogenzeile=None):
    """druck = [dict(id, name, format, blaetter, vorschau, satz, quelle)] · etiketten = [etikett(...)] → Satzdateien + papier_plan.json"""
    plan = {'druck': [], 'etiketten': []}
    for d in druck:
        seite(d['id'], d['blaetter'], d['name'])
        plan['druck'].append({k: d[k] for k in ('id', 'name', 'format', 'vorschau', 'satz', 'quelle')} | {'seiten': len(d['blaetter'])})
    alle = ''
    for x in etiketten:
        svg = f'<svg class="abs" style="inset:0;width:{x["b"]}mm;height:{x["h"]}mm" viewBox="0 0 {x["b"]} {x["h"]}">{x["innen"]}</svg>'
        alle += blatt(x['b'], x['h'], svg, 'etikett', 'background:transparent')
        plan['etiketten'].append({k: x[k] for k in ('id', 'b', 'h', 'name', 'satz', 'form')})
    seite('etiketten', [alle], H.ETIKETTEN['name'])
    # Druckbogen A3 quer: alle in Originalgrösse mit Schnittlinie, so viele Bögen wie nötig
    boegen, akt, x0, y0, zeile_h = [], [], 14, 16, 0
    for x in etiketten:
        if x0 + x['b'] > 420 - 14:
            x0, y0, zeile_h = 14, y0 + zeile_h + 9, 0
        if y0 + x['h'] > 297 - 12:
            boegen.append(akt); akt, x0, y0, zeile_h = [], 14, 16, 0
        akt.append((x, x0, y0)); x0 += x['b'] + 9; zeile_h = max(zeile_h, x['h'])
    boegen.append(akt)
    seiten_b = []
    for nr, akt in enumerate(boegen):
        inn = ''.join(f'<svg class="abs" style="left:{ox}mm;top:{oy}mm;width:{x["b"]}mm;height:{x["h"]}mm;overflow:visible" viewBox="0 0 {x["b"]} {x["h"]}">{x["innen"].replace("id=\"" + x["id"], "id=\"b" + x["id"]).replace("#" + x["id"], "#b" + x["id"])}<path d="{x["form"]}" fill="none" stroke="#e6007e" stroke-width=".15"/></svg>'
                      for x, ox, oy in akt)
        inn += t(14, 6.5, f'{e(H.NAME)} · {e(H.ETIKETTEN["name"])} · Druckbogen {nr + 1} von {len(boegen)} · A3 quer · Originalgrösse · Schnittlinie in Magenta', 'm', f'font-size:2.1mm;color:{F["tinte"]}')
        seiten_b.append(blatt(420, 297, inn, '', 'background:#fff'))
    seite('etiketten-bogen', seiten_b, H.ETIKETTEN['name'] + ', Druckbogen')
    plan['boegen'] = len(boegen); plan['meins'] = meins
    plan['masse'] = [min(min(x['b'], x['h']) for x in etiketten), max(max(x['b'], x['h']) for x in etiketten)]
    json.dump(plan, open(os.path.join(W, 'papier_plan.json'), 'w'), ensure_ascii=False, indent=1)
    # Satz-CSS mit festen Schnitten der Hausschrift (TTF, sonst landet die Schrift als «Type 3» in der PDF)
    css = open(os.path.join(K.KIT, 'papier.css'), encoding='utf-8').read()
    kopf = K.druckschrift_css()
    rest = css[css.index('*{box-sizing:border-box}'):].replace("'Baskerville CE',Georgia,serif", f"'{H.SCHRIFT['titel'][0]}',{H.SCHRIFT.get('titel_folge', 'Georgia,serif')}")
    K.schreib(os.path.join(SATZ, 'papier.css'), kopf + K.faerbe(rest) + getattr(H, 'CSS_PAPIER', ''))
    print('gesetzt:', len(plan['druck']), 'Drucksachen,', sum(x['seiten'] for x in plan['druck']), 'Seiten,', len(etiketten), H.ETIKETTEN['name'] + ',', plan['boegen'], 'Druckbögen')
