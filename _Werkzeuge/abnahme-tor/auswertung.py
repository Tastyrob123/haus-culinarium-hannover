#!/usr/bin/env python3
"""Abnahme-Tor · Auswertung: Bildprüfung der Dokumente (K10 Löcher/Mitte) und Kacheln (K4 leer), «zwei Wege zum selben Ziel» (K15),
Abdeckungstafel Inventar-Zeile × Kriterium, Fundliste mit Bild, Gegenprobe gegen Roberts Funde.
Aufruf: python3 auswertung.py <lauf-ordner> <tafel-ordner> [--gegenprobe gegenprobe.json] [--titel "…"] [--augen augen.json]
"""
import json, os, re, sys, html, glob, shutil
import numpy as np
from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__))
LAUF, TAFEL = sys.argv[1], sys.argv[2]
arg = lambda n, d=None: sys.argv[sys.argv.index('--' + n) + 1] if '--' + n in sys.argv else d
os.makedirs(os.path.join(TAFEL, 'b'), exist_ok=True)

# ---------- Kriterien aus ROBERTS-KRITERIEN.md lesen ----------
KRIT = {}
for z in open(os.path.join(HIER, '..', 'ROBERTS-KRITERIEN.md'), encoding='utf-8'):
    m = re.match(r'(\d+)\. (.*?)\s\*\*(M\+A|A\+M|M|A)\*\*', z.strip())
    if m: KRIT[int(m.group(1))] = {'satz': m.group(2), 'weise': m.group(3)}
DOK_K = {10, 11, 12, 13, 14}   # gelten nur, wo ein Dokument zu sehen ist

# ---------- Bildprüfung ----------
def dokument(pfad):
    """Löcher und Mitte eines Dokuments aus dem Bild: Zeilen mit Farbe (Abweichung vom Papier) im Innern, ohne Rahmen."""
    im = Image.open(pfad).convert('L'); w, h = im.size
    if w < 70 or h < 110: return None
    a = np.asarray(im, dtype=float)
    ring = np.concatenate([a[int(h * .02):int(h * .05), int(w * .1):int(w * .9)].ravel(), a[int(h * .95):int(h * .98), int(w * .1):int(w * .9)].ravel()])
    bg = float(np.median(ring)) if ring.size else float(np.median(a))
    y0, y1, x0, x1 = int(h * .07), int(h * .93), int(w * .12), int(w * .88)
    ink = np.abs(a[y0:y1, x0:x1] - bg) > 30
    zeile = ink.mean(axis=1) > 0.004
    if not zeile.any(): return {'leer': True}
    idx = np.where(zeile)[0]
    seg = []; s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if i - p > h * .012: seg.append((s, p)); s = i
        p = i
    seg.append((s, p))
    luecken = [((seg[i + 1][0] - seg[i][1]) / h, (seg[i][1] + y0) / h, (seg[i + 1][0] + y0) / h) for i in range(len(seg) - 1)]
    oben = (seg[0][0]) / h; unten = (y1 - y0 - seg[-1][1]) / h
    gr = max(luecken, default=(0, 0, 0))
    return {'loch': round(gr[0], 3), 'loch_von': round(gr[1], 3), 'loch_bis': round(gr[2], 3), 'oben': round(oben, 3), 'unten': round(unten, 3), 'teile': len(seg)}

def kachel(pfad):
    a = np.asarray(Image.open(pfad).convert('L'), dtype=float)
    if a.size < 900: return None
    h, w = a.shape; a = a[int(h * .15):int(h * .85), int(w * .15):int(w * .85)]   # nur das Innere: Rand, Rundung und Schatten verdecken sonst eine leere Fläche (Gegenprobe «Tapete leer»)
    return {'std': round(float(a.std()), 2), 'spanne': round(float(np.percentile(a, 98) - np.percentile(a, 2)), 1)}

def ueberdeckt(d, doks):
    r = d['r']
    for o in doks:
        if o is d: continue
        q = o['r']; ix = min(r['x'] + r['w'], q['x'] + q['w']) - max(r['x'], q['x']); iy = min(r['y'] + r['h'], q['y'] + q['h']) - max(r['y'], q['y'])
        if ix > 0 and iy > 0 and ix * iy > .15 * r['w'] * r['h'] and 'hinten' in d['sel']: return True
    return False

LOCH, MITTE = 0.14, 0.12
werkzeuge = []
for inv in sorted(glob.glob(os.path.join(LAUF, '*', 'inventar.json'))):
    I = json.load(open(inv, encoding='utf-8')); ordner = os.path.dirname(inv); k = os.path.basename(ordner)
    for zu in I['zustaende']:
        zu['funde'] = [f for f in zu.get('funde', []) if f.get('k') != 'bild']
        for d in zu.get('doks', []):
            if ueberdeckt(d, zu['doks']): continue
            p = os.path.join(ordner, 'bilder', d['datei'])
            if not os.path.exists(p): continue
            e = dokument(p); d['pruefung'] = e
            if not e or e.get('leer'): continue
            if e['loch'] > LOCH: zu['funde'].append({'k': 10, 'art': 'loch', 'sel': d['sel'], 'text': '', 'info': f"Loch {round(e['loch'] * 100)} % der Höhe (von {round(e['loch_von'] * 100)} % bis {round(e['loch_bis'] * 100)} %)", 'r': d['r'], 'dok': d['datei']})
            if abs(e['oben'] - e['unten']) > MITTE: zu['funde'].append({'k': 10, 'art': 'mitte', 'sel': d['sel'], 'text': '', 'info': f"Komposition nicht in der Mitte: oben {round(e['oben'] * 100)} %, unten {round(e['unten'] * 100)} % frei", 'r': d['r'], 'dok': d['datei']})
        for t in zu.get('kacheln', []):
            p = os.path.join(ordner, 'bilder', t['datei'])
            if not os.path.exists(p): continue
            e = kachel(p); t['pruefung'] = e
            if e and e['std'] < 3.5 and e['spanne'] < 18: zu['funde'].append({'k': 4, 'art': 'leer-bild', 'sel': t['sel'], 'text': '', 'info': f"Kachel wirkt leer: fast einfarbig (Streuung {e['std']}, Spanne {e['spanne']})", 'r': t['r'], 'kachel': t['datei']})
    # K15: Navigationspunkte derselben Gruppe, die zum selben oder fast gleichen Inhalt führen
    nav = [z for z in I['zustaende'] if z.get('steuer') and z['steuer']['wo'] != 'haupt' and z['art'] in ('navigation', 'reiter', 'ansicht')]
    jac = lambda a, b: len(set(a) & set(b)) / max(1, len(set(a) | set(b)))
    # Ein Klick, der den Inhalt gegenüber dem Zustand davor nicht ändert (Sprungmarke in einer langen Seite, Zurück/Weiter eines Karussells),
    # führt zu keinem eigenen Ziel; nur Punkte, die wirklich anderen Inhalt öffnen, können doppelte Wege sein (Tor-Anpassung 30.10.)
    nachWeg = {tuple(w.get('key') or w.get('text') for w in (z.get('weg') or [])): z for z in I['zustaende']}
    def eigen(z):
        v = nachWeg.get(tuple(w.get('key') or w.get('text') for w in (z.get('weg') or [])[:-1]))
        if not v: return True
        return not (jac(z['inhalt']['woerter'], v['inhalt']['woerter']) >= .9 and jac(z['inhalt']['bilder'], v['inhalt']['bilder']) >= .9)
    def neu(z):
        v = nachWeg.get(tuple(w.get('key') or w.get('text') for w in (z.get('weg') or [])[:-1]))
        if not v: return z['inhalt']
        return {k: [x for x in z['inhalt'][k] if x not in set(v['inhalt'][k])] for k in ('bilder', 'woerter')}
    SCHRITT = re.compile(r'^(zur[üu]ck|weiter|voriges|n[äa]chstes|vor|next|prev)\b', re.I)
    nav = [z for z in nav if eigen(z) and not SCHRITT.search(z['steuer']['text'].strip())]
    for i, a in enumerate(nav):
        for b in nav[i + 1:]:
            if a['steuer']['text'] == b['steuer']['text']: continue
            ha, hb = ((x.get('weg') or [{}])[-1].get('href') or '' for x in (a, b))
            if '#' in ha and '#' in hb and ha.split('#')[0] == hb.split('#')[0] and ha.split('#')[1] and hb.split('#')[1] and ha != hb: continue   # Sprungmarken zu verschiedenen Abschnitten derselben Seite
            if a['steuer']['gruppe'] != b['steuer']['gruppe']: continue   # nur Punkte derselben Navigation
            # verglichen wird, was der Klick öffnet: Inhalt neu gegenüber dem Zustand davor (eine lange Seite teilt sonst fast alles)
            da, db = (neu(x) for x in (a, b))
            bi, wo = jac(da['bilder'], db['bilder']), jac(da['woerter'], db['woerter'])
            if (len(da['bilder']) >= 6 and len(db['bilder']) >= 6 and bi >= .7 and not (len(da['woerter']) >= 10 and len(db['woerter']) >= 10 and wo < .5)) or (len(da['woerter']) >= 30 and len(db['woerter']) >= 30 and wo >= .85):
                for x, y in ((a, b), (b, a)):
                    x['funde'].append({'k': 15, 'art': 'zwei-wege', 'sel': x['steuer']['gruppe'], 'text': x['steuer']['text'], 'info': f"«{x['steuer']['text']}» zeigt denselben Inhalt wie «{y['steuer']['text']}» (Bilder {round(bi * 100)} %, Wörter {round(wo * 100)} % gleich)", 'r': None})
    for kn in I.get('kanten', []):
        pass
    stich = {}
    for f in glob.glob(os.path.join(ordner, 'stich-*.json')):
        S = json.load(open(f, encoding='utf-8')); stich[S['groesse'][0]] = {z['id']: z for z in S['zustaende']}
    for zu in I['zustaende']:   # Funde der Stichproben (1280/1000/390) gehören zum Zustand: Grün nur, wenn auch dort nichts offen ist
        zu['stichFunde'] = [dict(f, info=f"[{g}] " + (f.get('info') or '')) for g, S in stich.items() for f in (S.get(zu['id'], {}).get('funde') or []) if f.get('k')]
    werkzeuge.append({'k': k, 'I': I, 'ordner': ordner, 'stich': stich})

# ---------- Augen-Urteile (Kriterien A), falls vorhanden ----------
AUGEN = json.load(open(arg('augen'), encoding='utf-8')) if arg('augen') and os.path.exists(arg('augen')) else {}
# Mit dem Auge verworfene Maschinen-Funde (Fehlalarm, am Bild belegt): AUGEN['_verworfen'] = [{werkzeug, art, muster, grund}]
VERWORFEN = AUGEN.pop('_verworfen', []) if isinstance(AUGEN, dict) else []
def verworfen(wk, f):
    for v in VERWORFEN:
        if re.fullmatch(v.get('werkzeug', '.*'), wk) and re.fullmatch(v.get('art', '.*'), f.get('art') or '') and re.search(v.get('muster', ''), ' '.join([f.get('text') or '', f.get('info') or '', f.get('sel') or ''])): return v
    return None

# Bewegung (bewegung-tor.js) je Werkzeug: <lauf>/bewegung/bewegung.json oder --bewegung <datei>
BEWEGUNG = {}
for bp in [arg('bewegung')] + glob.glob(os.path.join(LAUF, 'bewegung', 'bewegung.json')) + glob.glob(os.path.join(LAUF, '*', 'bewegung', 'bewegung.json')):
    if bp and os.path.exists(bp):
        for sd in json.load(open(bp, encoding='utf-8'))['seiten']:
            e = BEWEGUNG.setdefault(sd['k'], {'funde': [], 'bilder': 0}); e['funde'] += sd['funde']; e['bilder'] += (sd.get('bewegt') or {}).get('bilder', 0) or 0

def zelle(zu, k):
    fs = [f for f in zu['funde'] + zu.get('stichFunde', []) if f.get('k') == k and not verworfen(zu['k'], f)]
    hatDok = (zu.get('dok') or {}).get('n', 0) > 0 or zu.get('doks')
    if k in DOK_K and not hatDok: return ('na', [])
    w = KRIT.get(k, {}).get('weise', 'A')
    if fs: return ('rot', fs)
    a = AUGEN.get(f"{zu['k']}/{zu['id']}/{k}") or AUGEN.get(f"{zu['k']}/*/{k}")
    if a: return (a['urteil'], [{'info': a.get('notiz', ''), 'k': k}])
    if w == 'A': return ('auge', [])
    if k == 10 and not any(d.get('pruefung') for d in zu.get('doks', [])): return ('np', [])
    if k in (34, 37):   # Bewegung: nur grün, wenn bewegung-tor.js diese Seite gemessen hat (sonst nicht prüfbar, nie stillschweigend grün)
        b = BEWEGUNG.get(zu['k'])
        if not b: return ('np', [{'info': 'Bewegung nicht gemessen (bewegung-tor.js fehlt)'}])
        bf = [f for f in b['funde'] if f.get('k') == k and not verworfen(zu['k'], dict(f, art='bewegung'))]
        return ('rot', bf) if bf else ('gruen', [{'info': f"bewegung-tor.js: {b.get('bilder', '?')} Bilder, kein Fund"}])
    return ('gruen', [])

# ---------- Bilder für die Tafel: Ansicht mit Fundrahmen ----------
def bild_mit_funden(w, zu):
    q = os.path.join(w['ordner'], 'bilder', zu.get('bild') or '')
    if not zu.get('bild') or not os.path.exists(q): return None, None
    ziel = f"{w['k']}-{zu['id']}.jpg"; voll = f"{w['k']}-{zu['id']}-voll.jpg"
    im = Image.open(q).convert('RGB'); d = ImageDraw.Draw(im)
    for f in zu['funde']:
        r = f.get('r')
        if not r or r['y'] > im.size[1] or r['y'] + r['h'] < 0: continue
        d.rectangle([r['x'] - 3, r['y'] - 3, r['x'] + r['w'] + 3, r['y'] + r['h'] + 3], outline=(255, 31, 90), width=3)
    im.save(os.path.join(TAFEL, 'b', voll), quality=72)
    t = im.copy(); t.thumbnail((360, 230)); t.save(os.path.join(TAFEL, 'b', ziel), quality=70)
    return ziel, voll

def ausschnitt(w, zu, f, n):
    """Bild zum Fund: Dokument- oder Kachelbild, sonst Ausschnitt aus der Ansicht."""
    for key in ('dok', 'kachel'):
        if f.get(key):
            p = os.path.join(w['ordner'], 'bilder', f[key]); z = f"{w['k']}-{zu['id']}-f{n}.jpg"
            im = Image.open(p).convert('RGB'); im.thumbnail((520, 520)); im.save(os.path.join(TAFEL, 'b', z), quality=78); return z
    q = os.path.join(w['ordner'], 'bilder', zu.get('bild') or '')
    r = f.get('r')
    if not r or not zu.get('bild') or not os.path.exists(q): return None
    im = Image.open(q).convert('RGB'); W, H = im.size
    if r['y'] > H or r['y'] + r['h'] < 0: return None
    pad = 40; box = (max(0, r['x'] - pad), max(0, r['y'] - pad), min(W, r['x'] + r['w'] + pad), min(H, r['y'] + r['h'] + pad))
    if box[2] - box[0] < 20 or box[3] - box[1] < 20: return None
    c = im.crop(box); d = ImageDraw.Draw(c); d.rectangle([r['x'] - box[0] - 3, r['y'] - box[1] - 3, r['x'] - box[0] + r['w'] + 3, r['y'] - box[1] + r['h'] + 3], outline=(255, 31, 90), width=3)
    if c.size[0] > 900: c.thumbnail((900, 600))
    z = f"{w['k']}-{zu['id']}-f{n}.jpg"; c.save(os.path.join(TAFEL, 'b', z), quality=80); return z

# ---------- Gegenprobe ----------
gegen = None
if arg('gegenprobe'):
    G = json.load(open(arg('gegenprobe'), encoding='utf-8')); gegen = []
    for g in G['funde']:
        rx = re.compile(g['muster'], re.I); treffer = []
        for w in werkzeuge:
            for zu in w['I']['zustaende']:
                kontext = ' '.join([zu['name'], ' '.join(zu.get('titel') or [])])
                for f in zu['funde']:
                    if f.get('k') != g['k']: continue
                    if rx.search(' '.join([f.get('text') or '', f.get('info') or '', f.get('sel') or '', kontext])): treffer.append((w, zu, f))
        gegen.append({'g': g, 'treffer': treffer})

# ---------- Tafel ----------
E = html.escape
FARBE = {'rot': ('#ff1f5a', 'rot'), 'gruen': ('#1f9d55', 'grün'), 'auge': ('#c9b8d6', 'Auge'), 'np': ('#9a9a9a', 'nicht prüfbar'), 'na': ('#eee', '–')}
titel = arg('titel', 'Abnahme-Tor')
alle_z = sum(len(w['I']['zustaende']) for w in werkzeuge)
teile = []; fundliste = []; zahl = {'rot': 0, 'gruen': 0, 'auge': 0, 'np': 0, 'na': 0}
for w in werkzeuge:
    I = w['I']; zs = I['zustaende']
    rows = []
    for zu in zs:
        klein, voll = bild_mit_funden(w, zu)
        zellen = []
        for k in range(1, max(KRIT) + 1):
            st, fs = zelle(zu, k); zahl[st] += 1
            tip = E(f"{k}. {KRIT.get(k, {}).get('satz', '')}" + ('\n' + '\n'.join('· ' + (f.get('info') or '') for f in fs[:6]) if fs else ''))
            zellen.append(f'<td class="z z-{st}" title="{tip}">{len(fs) if st == "rot" else ""}</td>')
        st_txt = []
        for gr, S in sorted(w['stich'].items()):
            s = S.get(zu['id'])
            if s: st_txt.append(f"{gr}: " + ('nicht erreicht' if s.get('nichtErreicht') else f"{len(s.get('funde', []))} Funde"))
        roh = [f for f in zu['funde'] + zu.get('stichFunde', []) if f.get('k') and not verworfen(zu['k'], f)]
        for n, f in enumerate(roh):
            fundliste.append((w, zu, f, n))
        rows.append(f"""<tr id="{w['k']}-{zu['id']}"><td class="nr">{zu['id']}</td><td class="nm"><b>{E(zu['name'])}</b><small>{E(zu['art'])}{' · ' + E(', '.join(st_txt)) if st_txt else ''}{' · gleichartig: ' + E(', '.join(str(g['zahl']) for g in zu.get('gleichartig', []))) + ' Stück, 3 bedient' if zu.get('gleichartig') else ''}</small></td>
<td class="bi">{f'<a href="b/{voll}" target="_blank"><img loading="lazy" src="b/{klein}"></a>' if klein else '–'}</td>{''.join(zellen)}</tr>""")
    rot = sum(1 for zu in zs for k in range(1, max(KRIT) + 1) if zelle(zu, k)[0] == 'rot')
    teile.append(f"""<section><h2>{E(I['werkzeug']['name'])} <small>{len(zs)} Zustände · {rot} rote Felder · {E(I['werkzeug']['url'])}{' · Inventar an der Obergrenze' if not I.get('voll', True) else ''}{' · ' + str(len(I.get('nichtErreicht', []))) + ' nicht erreicht' if I.get('nichtErreicht') else ''}</small></h2>
<div class="tw"><table><thead><tr><th>#</th><th>Zustand</th><th>Bild WebKit {I['groesse'][0]}×{I['groesse'][1]}</th>{''.join(f'<th title="{E(KRIT.get(k, {}).get("satz", ""))}">{k}<i>{KRIT.get(k, {}).get("weise", "")}</i></th>' for k in range(1, max(KRIT) + 1))}</tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>""")

json.dump([{'werkzeug': w['k'], 'zustand': zu['id'], 'name': zu['name'], 'k': f.get('k'), 'art': f.get('art'), 'text': f.get('text'), 'info': f.get('info'), 'sel': f.get('sel')} for w, zu, f, n in fundliste], open(os.path.join(TAFEL, 'funde.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)   # Fundliste zum Verteilen an die Bau-Chats

gp = ''
if gegen is not None:
    zeilen = []
    for x in gegen:
        g, t = x['g'], x['treffer']
        if t:
            w, zu, f = t[0]; n = zu['funde'].index(f); bild = ausschnitt(w, zu, f, n)
            zeilen.append(f"<tr><td class='ok'>gefunden</td><td><b>{E(g['name'])}</b><small>Kriterium {g['k']} · {len(t)} Stellen · erste: {E(w['I']['werkzeug']['name'])} #{zu['id']} {E(zu['name'])}<br>{E(f.get('info') or '')}</small></td><td>{f'<img src=b/{bild}>' if bild else ''}</td></tr>")
        else:
            zeilen.append(f"<tr><td class='nein'>NICHT gefunden</td><td><b>{E(g['name'])}</b><small>Kriterium {g['k']}</small></td><td></td></tr>")
    ok = sum(1 for x in gegen if x['treffer'])
    gp = f"<section class='gp'><h2>Gegenprobe: {ok} von {len(gegen)} Funden Roberts gefunden</h2><table class='gpt'>{''.join(zeilen)}</table></section>"

seite = f"""<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(titel)}</title>
<style>body{{font:14px/1.4 -apple-system,system-ui,sans-serif;margin:24px;background:#faf7f7;color:#1d1a22}}h1{{font-size:28px;margin:0 0 6px}}h2{{font-size:20px;margin:34px 0 10px}}h2 small{{font-size:13px;font-weight:400;color:#666;display:block}}
.tw{{overflow-x:auto}}table{{border-collapse:collapse;background:#fff}}th,td{{border:1px solid #e6dede;padding:3px 4px;vertical-align:middle}}th{{position:sticky;top:0;background:#1d1a22;color:#fff;font-size:12px}}th i{{display:block;font-size:9px;font-style:normal;opacity:.7}}
td.nm{{min-width:240px;max-width:340px}}td.nm small{{display:block;color:#777;font-size:11px}}td.bi img{{width:180px;display:block}}td.z{{width:26px;text-align:center;font-weight:700;color:#fff;font-size:12px}}
.z-rot{{background:#ff1f5a}}.z-gruen{{background:#1f9d55}}.z-auge{{background:#d9cce4}}.z-np{{background:#9a9a9a}}.z-na{{background:#f2eeee}}
.leg span{{display:inline-block;padding:2px 8px;margin-right:6px;border-radius:3px;color:#fff;font-size:12px}}.gpt td{{padding:8px}}.gpt img{{max-width:420px;max-height:260px}}.ok{{background:#1f9d55;color:#fff;font-weight:700}}.nein{{background:#ff1f5a;color:#fff;font-weight:700}}
.gpt small{{display:block;color:#555}}.kz{{columns:2;font-size:12px;color:#444}}</style>
<h1>{E(titel)}</h1><p>{alle_z} Zustände aus {len(werkzeuge)} Werkzeugen, je Zustand ein Bild in WebKit {werkzeuge[0]['I']['groesse'][0] if werkzeuge else ''} px, Stichproben 1280×800 und 390×844 in der Zeile. Felder: {zahl['rot']} rot · {zahl['gruen']} grün · {zahl['auge']} Auge (Kriterium A, mit dem Auge am Bild) · {zahl['np']} nicht prüfbar · {zahl['na']} entfällt (kein Dokument im Zustand).</p>
<p class="leg"><span style="background:#ff1f5a">rot = Fund</span><span style="background:#1f9d55">grün = gemessen, kein Fund</span><span style="background:#b9a6c9">Auge</span><span style="background:#9a9a9a">nicht prüfbar</span> · Mauszeiger auf ein Feld zeigt Kriterium und Funde · <a href="funde.html">Fundliste mit Bildern</a></p>
<ol class="kz">{''.join(f'<li value="{k}">{E(v["satz"])} <b>{v["weise"]}</b></li>' for k, v in sorted(KRIT.items()))}</ol>
{gp}{''.join(teile)}</html>"""
open(os.path.join(TAFEL, 'index.html'), 'w', encoding='utf-8').write(seite)

# Fundliste mit Bild (für den Oberchef)
fl = []
for w, zu, f, n in fundliste:
    b = ausschnitt(w, zu, f, n)
    fl.append(f"<tr><td>{f['k']}</td><td><b>{E(w['I']['werkzeug']['name'])}</b> #{zu['id']}<br><small>{E(zu['name'])}</small></td><td>{E(f.get('info') or '')}<br><small>{E(f.get('sel') or '')} {E((f.get('text') or '')[:60])}</small></td><td>{f'<img loading=lazy src=b/{b}>' if b else ''}</td></tr>")
open(os.path.join(TAFEL, 'funde.html'), 'w', encoding='utf-8').write(f"""<!doctype html><html lang="de"><meta charset="utf-8"><title>{E(titel)} · Funde</title><style>body{{font:14px/1.4 -apple-system,system-ui,sans-serif;margin:24px}}table{{border-collapse:collapse}}td{{border:1px solid #ddd;padding:6px;vertical-align:top}}img{{max-width:460px;max-height:300px}}small{{color:#666}}</style>
<h1>{E(titel)} · {len(fl)} Funde</h1><p><a href="index.html">zur Tafel</a></p><table><tr><th>K</th><th>Zustand</th><th>Fund</th><th>Bild</th></tr>{''.join(fl)}</table></html>""")
json.dump({'zustaende': alle_z, 'felder': zahl, 'funde': len(fl), 'gegenprobe': [{'name': x['g']['name'], 'gefunden': bool(x['treffer']), 'stellen': len(x['treffer'])} for x in gegen] if gegen is not None else None},
          open(os.path.join(TAFEL, 'ergebnis.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({'zustaende': alle_z, 'felder': zahl, 'funde': len(fl)}, ensure_ascii=False))
if gegen is not None:
    for x in gegen: print(('OK   ' if x['treffer'] else 'FEHLT') + ' ' + x['g']['name'] + (f" ({len(x['treffer'])})" if x['treffer'] else ''))
