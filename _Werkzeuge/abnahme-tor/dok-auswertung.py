#!/usr/bin/env python3
"""Abnahme-Tor · Auswertung der Dokumente: Bildprüfung (K27 Zeilen berühren sich), Tafel Dokument × Kriterium, Fundliste mit Bild,
Gegenprobe gegen Roberts Dokument-Funde am alten Stand.
Aufruf: python3 dok-auswertung.py <lauf> <tafel-ordner> [--alt <lauf-alt>] [--augen augen.json] [--titel …]"""
import json, os, re, sys, html, collections
import numpy as np
from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__))
LAUF, TAFEL = sys.argv[1], sys.argv[2]
arg = lambda n, d=None: sys.argv[sys.argv.index('--' + n) + 1] if '--' + n in sys.argv else d
os.makedirs(os.path.join(TAFEL, 'b'), exist_ok=True)
E = html.escape

KRIT = {}
for z in open(os.path.join(HIER, '..', 'ROBERTS-KRITERIEN.md'), encoding='utf-8'):
    m = re.match(r'(\d+)\. (.*?)\s\*\*(M\+A|M|A)\*\*', z.strip())
    if m: KRIT[int(m.group(1))] = {'satz': m.group(2), 'weise': m.group(3)}
SPALTEN = [2, 5, 7, 8, 10, 11, 12, 13, 14, 19, 20, 22, 23, 24, 25, 27, 29]

def tinte_zeilen(png, r):
    """Zahl der getrennten Tintenbänder im Kasten eines Titels (Zeilen, die sich berühren, verschmelzen zu einem Band)."""
    im = Image.open(png).convert('L'); W, H = im.size
    x0, y0, x1, y1 = max(0, int(r['x'])), max(0, int(r['y'])), min(W, int(r['x'] + r['w'])), min(H, int(r['y'] + r['h']))
    if x1 - x0 < 8 or y1 - y0 < 8: return None
    a = np.asarray(im.crop((x0, y0, x1, y1)), dtype=float)
    rand = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]); bg = float(np.median(rand))
    zeile = (np.abs(a - bg) > 60).mean(axis=1) > 0.002
    baender, im_band = 0, False
    for z in zeile:
        if z and not im_band: baender += 1
        im_band = z
    return baender

def lade(lauf):
    D = json.load(open(os.path.join(lauf, 'dokumente.json'), encoding='utf-8'))
    for d in D['dokumente']:
        neu = []
        for f in d.get('funde', []):
            if f.get('art') == 'zeilen-kandidat':
                p = os.path.join(lauf, 'blatt', f"{d['id']}-{f.get('seite', 0)}.png")
                if not os.path.exists(p): continue
                n = tinte_zeilen(p, f['r'])
                if n is not None and n < f['zeilen']:
                    neu.append({**f, 'art': 'zeilen', 'info': f"{f['zeilen']} Zeilen, aber nur {n} getrennte Tintenbänder: Unterlänge berührt Oberlänge"})
                continue
            if f.get('art') == 'grad' and str(f.get('info', '')).startswith('Haupttitel') and all(re.match(r'^(plakat|plakathoch|plakatganz|plakatrueck|buehne|ansicht)$', a or '') for a in d.get('aufbau', [])): continue   # Titel steht im gemalten Motiv
            neu.append(f)
        d['funde'] = neu
    return D

D = lade(LAUF)
AUGEN = json.load(open(arg('augen'), encoding='utf-8')) if arg('augen') and os.path.exists(arg('augen')) else {}
for d in D['dokumente']:   # Augen-Funde gehören in die Fundliste wie die maschinellen
    for k in range(1, 31):
        a = AUGEN.get(f"{d['quelle']}/{d['id']}/{k}")
        if a and a['urteil'] == 'rot': d['funde'].append({'k': k, 'art': 'auge', 'info': a['notiz'], 'seite': 0, 'r': None})

def zelle(d, k):
    fs = [f for f in d['funde'] if f.get('k') == k]
    if fs: return 'rot', fs
    a = AUGEN.get(f"{d['quelle']}/{d['id']}/{k}") or AUGEN.get(f"{d['quelle']}/{d['gruppe']}/{k}") or AUGEN.get(f"{d['quelle']}/*/{k}")
    if a: return a['urteil'], [{'info': a.get('notiz', '')}]
    return ('gruen', []) if KRIT.get(k, {}).get('weise') == 'M' else ('auge', [])

def blattbild(lauf, d, seite, gross=False):
    p = os.path.join(lauf, 'blatt', f"{d['id']}-{seite}.png")
    if not os.path.exists(p): return None
    im = Image.open(p).convert('RGB'); dr = ImageDraw.Draw(im)
    for f in d['funde']:
        r = f.get('r')
        if f.get('seite', 0) != seite or not r: continue
        dr.rectangle([r['x'] - 3, r['y'] - 3, r['x'] + max(r['w'], 4) + 3, r['y'] + max(r['h'], 4) + 3], outline=(255, 31, 90), width=4)
    z = f"{os.path.basename(lauf)}-{d['id']}-{seite}{'-g' if gross else ''}.jpg"
    im.thumbnail((620, 620) if gross else (170, 220)); im.save(os.path.join(TAFEL, 'b', z), quality=78)
    return z

titel = arg('titel', 'Abnahme-Tor · Dokumente')
quellen = collections.OrderedDict()
for d in D['dokumente']: quellen.setdefault(d['quelle'], []).append(d)
zahl = collections.Counter(); teile = []; fl = []
for q, ds in quellen.items():
    rows = []
    for d in ds:
        zellen = []
        for k in SPALTEN:
            st, fs = zelle(d, k); zahl[st] += 1
            tip = E(f"{k}. {KRIT.get(k, {}).get('satz', '')}" + ''.join('\n· ' + (f.get('info') or '') for f in fs[:5]))
            zellen.append(f'<td class="z z-{st}" title="{tip}">{len(fs) if st == "rot" else ""}</td>')
        bilder = ''.join(f'<img loading="lazy" src="b/{b}">' for b in [blattbild(LAUF, d, s) for s in range(len(d.get('bilder', [])))] if b)
        rows.append(f"<tr id='d{d['id']}'><td class='nr'>{d['id']}</td><td class='nm'><b>{E(d['titel'] or '')}</b><small>{E(d['gruppe'])} · {E(d.get('format') or '')} · {E('/'.join(x or '' for x in d.get('aufbau', [])))} · {E('/'.join(x or '' for x in d.get('ton', [])))}</small></td><td class='bi'>{bilder}</td>{''.join(zellen)}</tr>")
        if d['funde']:
            gb = ''.join(f'<img loading="lazy" src="b/{b}">' for b in [blattbild(LAUF, d, s, True) for s in range(len(d.get('bilder', [])))] if b)
            li = ''.join(f"<li><b>K{f.get('k')}</b> {E(f.get('info') or '')}{(' «' + E(f['text']) + '»') if f.get('text') else ''}</li>" for f in d['funde'])
            fl.append(f"<section class='fd' id='f{d['id']}'><h3>{d['id']} · {E(d['quelle'])} · {E(d['titel'] or '')}<small>{E(d['gruppe'])} · {E(d.get('format') or '')} · {E('/'.join(x or '' for x in d.get('aufbau', [])))}</small></h3><div class='fz'><div>{gb}</div><ol>{li}</ol></div></section>")
    rot = sum(1 for d in ds if d['funde'])
    kopfzeile = ''.join(f'<th title="{E(KRIT.get(k, {}).get("satz", ""))}">{k}<i>{KRIT.get(k, {}).get("weise", "")}</i></th>' for k in SPALTEN)
    teile.append(f"<section><h2>{E(q)} <small>{len(ds)} Dokumente · {rot} mit Fund · <a href='funde.html'>Fundliste mit Bildern</a></small></h2><div class='tw'><table><thead><tr><th>#</th><th>Dokument</th><th>Blatt</th>{kopfzeile}</tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>")

# Gegenprobe am alten Stand: Roberts Dokument-Funde
gp = ''
if arg('alt'):
    A = lade(arg('alt'))
    proben = [('Menükarte mit Löchern (Kriterium 10)', lambda d, f: f['k'] == 10 and d['gruppe'] == 'menuekarte'),
              ('«Ausgebucht» mit Löchern (Kriterium 10)', lambda d, f: f['k'] in (10, 11) and re.search('ausgebucht', (d['titel'] or '') + ' '.join(str(x) for x in d.get('aufbau', [])), re.I)),
              ('Speisekarte «Vom Pass» nicht im Stil (Kriterium 12)', lambda d, f: f['k'] == 12 and re.search('vom pass|speisekarte', (d['titel'] or '') + ' ' + d['gruppe'], re.I) and f.get('art') in ('versalien', 'trenner', 'schrift', 'rolle'))]
    zeilen = []
    for name, pr in proben:
        t = [(d, f) for d in A['dokumente'] for f in d['funde'] if pr(d, f)]
        if t:
            d, f = t[0]; b = blattbild(arg('alt'), d, f.get('seite', 0), True)
            zeilen.append(f"<tr><td class='ok'>gefunden</td><td><b>{E(name)}</b><small>{len(t)} Stellen · erste: {E(d['titel'] or '')} ({E(d['gruppe'])})<br>{E(f.get('info') or '')}</small></td><td>{f'<img src=b/{b}>' if b else ''}</td></tr>")
        else: zeilen.append(f"<tr><td class='nein'>NICHT gefunden</td><td><b>{E(name)}</b></td><td></td></tr>")
    ok = sum(1 for z in zeilen if "class='ok'" in z)
    gp = f"<section class='gp'><h2>Gegenprobe am Stand von heute früh: {ok} von {len(proben)} Dokument-Funden Roberts gefunden</h2><table class='gpt'>{''.join(zeilen)}</table></section>"

wf = ''.join(f"<li>K{f['k']} {E(f['info'])}</li>" for f in D.get('werkzeugFunde', []))
CSS = """body{font:14px/1.4 -apple-system,system-ui,sans-serif;margin:24px;background:#faf7f7;color:#1d1a22}h1{font-size:28px;margin:0 0 6px}h2{font-size:20px;margin:34px 0 10px}h2 small,h3 small{font-size:13px;font-weight:400;color:#666;display:block}
.tw{overflow-x:auto}table{border-collapse:collapse;background:#fff}th,td{border:1px solid #e6dede;padding:3px 4px;vertical-align:middle}th{position:sticky;top:0;background:#1d1a22;color:#fff;font-size:12px}th i{display:block;font-size:9px;font-style:normal;opacity:.7}
td.nm{min-width:240px;max-width:340px}td.nm small{display:block;color:#777;font-size:11px}td.bi img{height:120px;margin-right:4px}td.z{width:26px;text-align:center;font-weight:700;color:#fff;font-size:12px}
.z-rot{background:#ff1f5a}.z-gruen{background:#1f9d55}.z-auge{background:#d9cce4}.z-np{background:#9a9a9a}.leg span{display:inline-block;padding:2px 8px;margin-right:6px;border-radius:3px;color:#fff;font-size:12px}
.gpt td{padding:8px}.gpt img{max-width:420px;max-height:320px}.ok{background:#1f9d55;color:#fff;font-weight:700}.nein{background:#ff1f5a;color:#fff;font-weight:700}.gpt small{display:block;color:#555}
.fd{border-top:1px solid #ddd;padding:14px 0}.fz{display:flex;gap:20px;align-items:flex-start}.fz img{max-width:520px;max-height:620px;margin:0 8px 8px 0;border:1px solid #ccc}.fz ol{margin:0;padding-left:18px;max-width:640px}"""
n_dok = len(D['dokumente']); n_fund = sum(1 for d in D['dokumente'] if d['funde'])
kopf = f"""<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(titel)}</title><style>{CSS}</style>"""
open(os.path.join(TAFEL, 'index.html'), 'w', encoding='utf-8').write(f"""{kopf}<h1>{E(titel)}</h1>
<p>{n_dok} Dokumente aus der Werkstatt selbst gesetzt ({', '.join(f'{len(v)} {E(k)}' for k, v in quellen.items())}), WebKit. {n_fund} mit Fund. Felder: {zahl['rot']} rot · {zahl['gruen']} grün · {zahl['auge']} Auge offen.</p>
<p class="leg"><span style="background:#ff1f5a">rot = Fund</span><span style="background:#1f9d55">grün</span><span style="background:#b9a6c9">Auge offen (Kriterium A)</span> · Mauszeiger auf ein Feld zeigt Kriterium und Funde · <a href="funde.html">Fundliste mit Bildern</a></p>
{f'<p><b>Werkzeug:</b></p><ul>{wf}</ul>' if wf else ''}{gp}{''.join(teile)}</html>""")
open(os.path.join(TAFEL, 'funde.html'), 'w', encoding='utf-8').write(f"{kopf}<h1>{E(titel)} · Funde</h1><p>{n_fund} von {n_dok} Dokumenten mit Fund · <a href='index.html'>zur Tafel</a> · rote Rahmen = Stelle im Blatt</p>{''.join(fl)}</html>")
statistik = collections.Counter((f['k'], f['art']) for d in D['dokumente'] for f in d['funde'])
json.dump({'dokumente': n_dok, 'mit_fund': n_fund, 'felder': dict(zahl), 'funde_nach_art': {f'K{k} {a}': n for (k, a), n in sorted(statistik.items())}},
          open(os.path.join(TAFEL, 'ergebnis.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({'dokumente': n_dok, 'mit_fund': n_fund, 'felder': dict(zahl)}, ensure_ascii=False))
for (k, a), n in sorted(statistik.items()): print(f'  K{k} {a}: {n}')
if gp: print(re.sub('<[^>]+>', ' ', gp)[:600])
