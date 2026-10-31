#!/usr/bin/env python3
"""Tafel zum Messlauf.
  python3 tafel.py <lauf>                              → <lauf>/tafel.html (alle Funde eines Laufs, je Werkzeug, mit Ausschnittbild)
  python3 tafel.py <vorher> <nachher> <ziel.html> [offen.json]
                                                       → Vergleich vorher/nachher, Zahl je Werkzeug, offene Punkte (z. B. Plakatwerkstatt)
Bilder werden relativ zur Tafel verlinkt; die Tafel liegt im selben Baum wie die Läufe."""
import json, os, sys, html, collections

ART = {'ueberlauf': 'Text läuft aus dem Kasten', 'rand': 'Text klebt am Rand (unter 6 px)', 'wort': 'Wort ohne Trennstrich umgebrochen',
       'oval': 'Runder Knopf ist oval', 'reihe': 'Kacheln einer Reihe ungleich', 'ueberlappt': 'Elemente überdecken sich',
       'anschnitt': 'Am Bildschirmrand angeschnitten', 'doppelt': 'Navigation doppelt', 'gemischt': 'Inhaltsarten gemischt',
       'beschnitten': 'Plakat/Motiv beschnitten', 'einzelwort': 'Einzelnes Wort in der letzten Titelzeile',
       'text-mitte': 'Schrift im Knopf nicht mittig', 'zier-x': '«x» als Zierzeichen', 'gekuerzt': 'Gekürzt mit … (Hinweis)',
       'fehler': 'Lauf-Fehler'}
HINWEIS = {'gekuerzt', 'fehler'}   # zählt nicht als Fehler, steht nur da


def lade(lauf):
    d = json.load(open(os.path.join(lauf, 'funde.json'), encoding='utf-8'))
    return d['funde'], d.get('zustaende', [])


def schluessel(f):   # derselbe Fehler in beiden Läufen (ohne Zahlenwerte)
    import re
    return (f['k'], f['browser'], f['breite'], f['art'], f.get('sel', ''), re.sub(r'[\d.]+', '#', f.get('text', '')))


def zahl(funde):
    c = collections.Counter()
    for f in funde:
        if f['art'] not in HINWEIS:
            c[f['k']] += 1
    return c


CSS = '''<style>:root{--bg:#FAF4F4;--t:#16141B;--l:#5a5664;--k:#CF7233;--r:#c0392b;--g:#2f7d4f;--fl:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#16141B;--t:#FAF4F4;--l:#b9b3c2;--fl:#22202a}}
body{margin:0;background:var(--bg);color:var(--t);font:15px/1.5 system-ui,sans-serif}main{max-width:1280px;margin:0 auto;padding:28px 16px 80px}
h1{font:400 clamp(30px,4.6vw,52px)/1.05 Georgia,serif;margin:0 0 8px}h2{font:400 26px/1.2 Georgia,serif;margin:40px 0 8px}h3{font-size:14px;letter-spacing:.08em;text-transform:uppercase;color:var(--k);margin:22px 0 8px}
.s{color:var(--l)}table{border-collapse:collapse;width:100%;margin:10px 0}td,th{padding:7px 10px;border-bottom:1px solid rgba(0,0,0,.08);text-align:left}th{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--l)}
td.n{text-align:right;font-variant-numeric:tabular-nums}.rot{color:var(--r);font-weight:600}.gruen{color:var(--g);font-weight:600}
.f{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,340px);gap:12px;background:var(--fl);border-radius:10px;padding:12px 14px;margin:8px 0;box-shadow:0 6px 18px -12px rgba(0,0,0,.4)}
.f img{max-width:100%;height:auto;border-radius:6px;display:block}.f b{display:block}.f code{font-size:12px;color:var(--l);word-break:break-all}.mk{display:inline-block;font-size:11px;letter-spacing:.06em;padding:1px 7px;border-radius:99px;background:rgba(207,114,51,.14);color:var(--k);margin-right:6px}
@media (max-width:760px){.f{grid-template-columns:1fr}}</style>'''


def karte(f, basis, ziel_dir):
    b = ''
    if f.get('bild'):
        rel = os.path.relpath(os.path.join(basis, 'bilder', f['bild']), ziel_dir)
        b = f'<a href="{html.escape(rel)}"><img src="{html.escape(rel)}" alt="Ausschnitt" loading="lazy"></a>'
    zst = ', '.join(f.get('zustaende') or [f.get('zustand', '')])[:220]
    return (f'<div class="f"><div><span class="mk">{html.escape(ART.get(f["art"], f["art"]))}</span><span class="mk">{f["browser"]} {f["breite"]}</span>'
            f'<b>{html.escape(f.get("text") or "")}</b><div>{html.escape(f.get("info") or "")}</div>'
            f'<div class="s">Zustand: {html.escape(zst)}</div><code>{html.escape(f.get("sel") or "")}</code></div><div>{b}</div></div>')


def einzeln(lauf):
    funde, zst = lade(lauf)
    namen = {}
    for f in funde:
        namen.setdefault(f['k'], f.get('name', f['k']))
    teile = [f'<h1>Messlauf</h1><p class="s">{len([f for f in funde if f["art"] not in HINWEIS])} Funde, {len(zst)} Zustände gemessen. Hinweise (gekürzt mit …) zählen nicht.</p>']
    for k, n in namen.items():
        fk = [f for f in funde if f['k'] == k]
        teile.append(f'<h2>{html.escape(n)} · {len([f for f in fk if f["art"] not in HINWEIS])}</h2>')
        for art in ART:
            fa = [f for f in fk if f['art'] == art]
            if fa:
                teile.append(f'<h3>{ART[art]} · {len(fa)}</h3>' + ''.join(karte(f, lauf, lauf) for f in fa))
    open(os.path.join(lauf, 'tafel.html'), 'w', encoding='utf-8').write(
        f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Messlauf</title>{CSS}</head><body><main>{"".join(teile)}</main></body></html>')


def vergleich(vorher, nachher, ziel, offen=None):
    fv, zv = lade(vorher); fn, zn = lade(nachher)
    zd = os.path.dirname(ziel); cv, cn = zahl(fv), zahl(fn)
    namen = {}
    for f in fv + fn:
        namen.setdefault(f['k'], f.get('name', f['k']))
    weg = {schluessel(f) for f in fv} - {schluessel(f) for f in fn}
    zeilen = ''.join(f'<tr><td>{html.escape(namen[k])}</td><td class="n">{cv.get(k, 0)}</td><td class="n {"gruen" if cn.get(k, 0) == 0 else "rot"}">{cn.get(k, 0)}</td></tr>' for k in namen)
    teile = [f'<h1>Messlauf · vorher und nachher</h1><p class="s">Alle Werkzeuge und die Werkbank, Chromium und WebKit, 1440 × 900, 1280 × 800 und 390 × 844. '
             f'Gemessen: vorher {len(zv)} Zustände, nachher {len(zn)} Zustände. Hinweise («gekürzt mit …») sind nicht gezählt. Die Regeln «Schrift im Knopf nicht mittig» und «x als Zierzeichen» kamen erst nach dem Lauf vorher dazu; ihre Funde stehen nur nachher.</p>',
             f'<table><tr><th>Werkzeug</th><th>vorher</th><th>nachher</th></tr>{zeilen}<tr><td><b>Zusammen</b></td><td class="n"><b>{sum(cv.values())}</b></td><td class="n"><b>{sum(cn.values())}</b></td></tr></table>']
    if offen:
        o = json.load(open(offen, encoding='utf-8'))
        teile.append('<h2>Offen</h2>' + ''.join(f'<h3>{html.escape(x["titel"])}</h3><p class="s">{html.escape(x.get("satz", ""))}</p>' + ''.join(karte(f, nachher, zd) for f in fn if f['k'] in x.get('k', []) and f['art'] not in HINWEIS) for x in o))
    teile.append('<h2>Nachher noch da</h2>')
    for k, n in namen.items():
        fk = [f for f in fn if f['k'] == k and f['art'] not in HINWEIS and not (offen and any(k in x.get('k', []) for x in json.load(open(offen))))]
        if fk:
            teile.append(f'<h3>{html.escape(n)} · {len(fk)}</h3>' + ''.join(karte(f, nachher, zd) for f in fk))
    teile.append('<h2>Behoben (vorher gefunden, nachher nicht mehr)</h2>')
    for k, n in namen.items():
        fk = [f for f in fv if f['k'] == k and schluessel(f) in weg and f['art'] not in HINWEIS]
        if fk:
            teile.append(f'<h3>{html.escape(n)} · {len(fk)}</h3>' + ''.join(karte(f, vorher, zd) for f in fk))
    open(ziel, 'w', encoding='utf-8').write(
        f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Messlauf Culinarium</title>{CSS}</head><body><main>{"".join(teile)}</main></body></html>')


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) == 1:
        einzeln(a[0])
    else:
        vergleich(a[0], a[1], a[2], a[3] if len(a) > 3 else None)
    print('ok')
