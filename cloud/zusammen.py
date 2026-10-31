#!/usr/bin/env python3
"""Führt die Ergebnisse aller Cloud-Rechner zusammen: Abdeckungstafel (Abnahme-Tor), Messlauf-Tafel, Zeiten und Kosten.
Aufruf: python3 cloud/zusammen.py <lauf-ordner> <ergebnis-ordner> [--titel "…"] [--run <run-id>]
Ergebnis: <ergebnis>/index.html (Übersicht), tor/ (Abdeckungstafel), messlauf/ (Tafel), zeiten.json, zusammenfassung.md."""
import glob, html, json, math, os, shutil, subprocess, sys, datetime

LAUF, ERG = sys.argv[1], sys.argv[2]
arg = lambda n, d=None: sys.argv[sys.argv.index('--' + n) + 1] if '--' + n in sys.argv else d
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TW = os.path.join(WS, '_Werkzeuge')
H = json.load(open(os.path.join(WS, 'cloud', 'haus.json'), encoding='utf-8'))
os.makedirs(ERG, exist_ok=True)
PREIS_MIN = 0.006   # US-Dollar je Minute, Linux 2 Kerne, GitHub-Preisliste ab 01.01.2026 (über dem Freikontingent)

# ---------- Messlauf: Teilergebnisse der Rechner zu einem Lauf ----------
ML = os.path.join(LAUF, 'messlauf'); alle_f, alle_z = [], []
for d in sorted(glob.glob(os.path.join(ML, '*', 'funde.json'))):
    teil = os.path.basename(os.path.dirname(d)); j = json.load(open(d, encoding='utf-8'))
    os.makedirs(os.path.join(ML, 'bilder'), exist_ok=True)
    for f in j.get('funde', []):
        if f.get('bild'):
            q = os.path.join(os.path.dirname(d), 'bilder', f['bild'])
            if os.path.exists(q):
                neu = teil + '-' + f['bild']; shutil.copy(q, os.path.join(ML, 'bilder', neu)); f['bild'] = neu
        alle_f.append(f)
    alle_z += j.get('zustaende', [])
if alle_f or alle_z:
    json.dump({'zeit': datetime.datetime.utcnow().isoformat(), 'funde': alle_f, 'zustaende': alle_z}, open(os.path.join(ML, 'funde.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    subprocess.run([sys.executable, os.path.join(TW, 'messlauf', 'tafel.py'), ML])
    os.makedirs(os.path.join(ERG, 'messlauf'), exist_ok=True)
    for n in ('tafel.html', 'funde.json'):
        if os.path.exists(os.path.join(ML, n)): shutil.copy(os.path.join(ML, n), os.path.join(ERG, 'messlauf', n))
    if os.path.isdir(os.path.join(ML, 'bilder')): shutil.copytree(os.path.join(ML, 'bilder'), os.path.join(ERG, 'messlauf', 'bilder'), dirs_exist_ok=True)

# ---------- Abnahme-Tor: Abdeckungstafel ----------
subprocess.run([sys.executable, os.path.join(TW, 'abnahme-tor', 'auswertung.py'), LAUF, os.path.join(ERG, 'tor'), '--titel', arg('titel', 'Abnahme in der Cloud') + ' · ' + H['haus']])

# ---------- Zahlen ----------
inv = {}
for f in glob.glob(os.path.join(LAUF, '*', 'inventar.json')):
    j = json.load(open(f, encoding='utf-8')); k = os.path.basename(os.path.dirname(f))
    st = {}
    for s in glob.glob(os.path.join(os.path.dirname(f), 'stich-*.json')):
        sj = json.load(open(s, encoding='utf-8')); st[os.path.basename(s)[6:-5]] = {'zustaende': len(sj['zustaende']), 'funde': sum(len(z.get('funde', [])) for z in sj['zustaende']), 'nicht': sum(1 for z in sj['zustaende'] if z.get('nichtErreicht'))}
    inv[k] = {'zustaende': len(j['zustaende']), 'funde': sum(len(z.get('funde', [])) for z in j['zustaende']), 'nicht': len(j.get('nichtErreicht', [])), 'voll': j.get('voll'), 'stich': st}
json.dump({k: v['zustaende'] for k, v in inv.items()}, open(os.path.join(ERG, 'zustaende.json'), 'w'), indent=1)   # für die Teilgrösse des nächsten Laufs (haus.json «zustaende»)
ml_funde = [f for f in alle_f if f.get('art') not in ('gekuerzt', 'fehler')]

# ---------- Zeiten aus GitHub (Rechner-Minuten, Gesamtdauer) ----------
jobs, run = [], {}
rid = arg('run'); repo = os.environ.get('GITHUB_REPOSITORY')
if rid and repo:
    try:
        out = subprocess.run(['gh', 'api', '--paginate', f'repos/{repo}/actions/runs/{rid}/jobs?per_page=100', '--jq', '.jobs[]|{name,started_at,completed_at,conclusion}'], capture_output=True, text=True, timeout=120).stdout
        jobs = [json.loads(z) for z in out.splitlines() if z.strip()]
        run = json.loads(subprocess.run(['gh', 'api', f'repos/{repo}/actions/runs/{rid}', '--jq', '{created_at,run_started_at}'], capture_output=True, text=True, timeout=60).stdout or '{}')
    except Exception as e: print('Zeiten aus GitHub nicht gelesen:', e)
iso = lambda s: datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))
jetzt = datetime.datetime.now(datetime.timezone.utc)
dauer = []
for j in jobs:
    if not j.get('started_at'): continue
    ende = iso(j['completed_at']) if j.get('completed_at') else jetzt
    dauer.append({'name': j['name'], 'sek': max(0, (ende - iso(j['started_at'])).total_seconds()), 'ergebnis': j.get('conclusion')})
minuten = sum(math.ceil(d['sek'] / 60) for d in dauer)   # GitHub rechnet jeden Rechner auf volle Minuten auf
gesamt = (jetzt - iso(run['run_started_at'])).total_seconds() if run.get('run_started_at') else None
eigene = [json.load(open(f)) for f in glob.glob(os.path.join(LAUF, '_zeiten', '*.json'))]
zeiten = {'rechner': len(dauer), 'rechner_minuten': minuten, 'kosten_usd_ohne_freikontingent': round(minuten * PREIS_MIN, 2),
          'gesamt_minuten': round(gesamt / 60, 1) if gesamt else None, 'laengster_rechner': max(dauer, key=lambda d: d['sek']) if dauer else None,
          'jobs': dauer, 'pruefschritte': eigene}
json.dump(zeiten, open(os.path.join(ERG, 'zeiten.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- Übersicht ----------
e = html.escape
tor_f = sum(v['funde'] for v in inv.values()); tor_z = sum(v['zustaende'] for v in inv.values()); st_z = sum(s['zustaende'] for v in inv.values() for s in v['stich'].values())
nicht = sum(v['nicht'] for v in inv.values()) + sum(s['nicht'] for v in inv.values() for s in v['stich'].values())
zeilen = ''.join(f"<tr><td>{e(k)}</td><td>{v['zustaende']}</td><td>{v['funde']}</td><td>{' · '.join(f'{g}: {s['zustaende']} Zust., {s['funde']} Funde' for g, s in sorted(v['stich'].items()))}</td><td>{v['nicht'] or ''}</td></tr>" for k, v in sorted(inv.items()))
lang = sorted(dauer, key=lambda d: -d['sek'])[:12]
jz = ''.join(f"<tr><td>{e(d['name'])}</td><td>{d['sek'] / 60:.1f} min</td><td>{e(str(d['ergebnis']))}</td></tr>" for d in lang)
mz = lambda x: f'{x:.0f}' if x is not None else '–'
seite = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Abnahme · {e(H['haus'])}</title>
<style>body{{font:16px/1.5 -apple-system,system-ui,sans-serif;margin:0;background:#f6f4ef;color:#111}}main{{max-width:1100px;margin:0 auto;padding:40px 20px}}
h1{{font-size:44px;margin:0 0 6px}}.k{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:24px 0}}.k div{{background:#fff;border-radius:14px;padding:16px}}
.k b{{display:block;font-size:30px}}table{{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;margin:12px 0 28px}}td,th{{text-align:left;padding:8px 12px;border-bottom:1px solid #eee;font-size:14px}}
a.t{{display:inline-block;background:#111;color:#fff;text-decoration:none;border-radius:999px;padding:12px 22px;margin:6px 8px 6px 0}}</style></head><body><main>
<h1>{e(H['haus'])}</h1><p>{e(arg('titel', 'Abnahme in der Cloud'))} · Lauf {e(str(rid or ''))} · {jetzt.strftime('%d.%m.%Y %H:%M')} UTC</p>
<p><a class="t" href="tor/index.html">Abdeckungstafel öffnen</a><a class="t" href="messlauf/tafel.html">Messlauf-Tafel öffnen</a></p>
<div class="k"><div><b>{tor_z}</b>Zustände im Inventar</div><div><b>{st_z}</b>Zustände in 1280 / 1000 / 390</div><div><b>{tor_f}</b>Funde Tor (1440)</div><div><b>{len(ml_funde)}</b>Funde Messlauf</div>
<div><b>{nicht}</b>nicht erreicht</div><div><b>{mz(zeiten['gesamt_minuten'])} min</b>Dauer des ganzen Laufs</div><div><b>{len(dauer)}</b>Rechner</div><div><b>{minuten}</b>Rechner-Minuten (≈ {zeiten['kosten_usd_ohne_freikontingent']} $ ohne Freikontingent)</div></div>
<h2>Werkzeuge</h2><table><tr><th>Ziel</th><th>Zustände</th><th>Funde</th><th>Stichproben</th><th>nicht erreicht</th></tr>{zeilen}</table>
<h2>Längste Rechner</h2><table><tr><th>Rechner</th><th>Dauer</th><th>Ergebnis</th></tr>{jz}</table></main></body></html>"""
open(os.path.join(ERG, 'index.html'), 'w', encoding='utf-8').write(seite)
md = (f"## {H['haus']} · Abnahme in der Cloud\n\n| | |\n|---|---|\n| Zustände Inventar | {tor_z} |\n| Zustände Stichproben | {st_z} |\n| Funde Tor | {tor_f} |\n"
      f"| Funde Messlauf | {len(ml_funde)} |\n| nicht erreicht | {nicht} |\n| Dauer ganzer Lauf | {mz(zeiten['gesamt_minuten'])} min |\n| Rechner | {len(dauer)} |\n| Rechner-Minuten | {minuten} (≈ {zeiten['kosten_usd_ohne_freikontingent']} $) |\n")
open(os.path.join(ERG, 'zusammenfassung.md'), 'w', encoding='utf-8').write(md)
print(md)
