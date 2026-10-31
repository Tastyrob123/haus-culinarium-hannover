#!/usr/bin/env python3
"""Entscheidungen im Nachtlauf, nur aus gemessenen Zahlen dieses Durchgangs.
  nacht_pruefen.py probe <probe-ordner>   → ok=true, wenn jeder Probe-Teil erfolgreich und ≤ 15 min; misst Minuten je Zustand
  nacht_pruefen.py budget                 → weiter=true, wenn bisher verbrauchte Minuten + Hochrechnung Plakatwerkstatt ≤ Kontingent
Ausgaben nach GITHUB_OUTPUT und in die Zusammenfassung."""
import glob, json, math, os, subprocess, sys
WS = os.environ.get('GITHUB_WORKSPACE', '.'); H = json.load(open(os.path.join(WS, 'cloud', 'haus.json')))
REPO, RUN = os.environ['GITHUB_REPOSITORY'], os.environ['GITHUB_RUN_ID']
KONTINGENT = int(os.environ.get('KONTINGENT', '2000')); GRENZE = float(os.environ.get('TEIL_MAX_MIN', '15'))
def jobs():
    out = subprocess.run(['gh', 'api', '--paginate', f'repos/{REPO}/actions/runs/{RUN}/jobs?per_page=100', '--jq', '.jobs[]|{name,conclusion,started_at,completed_at}'], capture_output=True, text=True).stdout
    return [json.loads(z) for z in out.splitlines() if z.strip()]
from datetime import datetime, timezone
iso = lambda t: datetime.fromisoformat(t.replace('Z', '+00:00'))
dauer = lambda j: ((iso(j['completed_at']) if j.get('completed_at') else datetime.now(timezone.utc)) - iso(j['started_at'])).total_seconds() / 60 if j.get('started_at') else 0
def aus(**kv):
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        for k, v in kv.items(): f.write(f'{k}={v}\n')
    with open(os.environ.get('GITHUB_STEP_SUMMARY', '/dev/null'), 'a') as f:
        f.write('\n'.join(f'- {k}: {v}' for k, v in kv.items()) + '\n')
    print(kv)
if sys.argv[1] == 'probe':
    teile = [j for j in jobs() if j['name'].startswith('probe / teil')]
    lang = max((dauer(j) for j in teile), default=99); ok = bool(teile) and all(j['conclusion'] == 'success' for j in teile) and lang <= GRENZE
    zust = 0
    for f in glob.glob(os.path.join(sys.argv[2], '_teile', '*', '*', 'inventar.json')):
        zust += sum(1 for z in json.load(open(f))['zustaende'] if not z.get('fremd'))
    minuten = sum(math.ceil(dauer(j)) for j in teile)
    mpz = round(minuten / zust, 3) if zust else 1.0
    aus(ok=str(ok).lower(), laengster_teil_min=round(lang, 1), probe_minuten=minuten, probe_zustaende=zust, minuten_je_zustand=mpz)
else:
    alle = jobs(); verbraucht = sum(math.ceil(dauer(j)) for j in alle)
    mpz = float(os.environ.get('MPZ', '1'))
    z = H.get('zustaende', {}); pw = sum(v for k, v in z.items() if k.startswith('plakatwerkstatt'))
    hoch = math.ceil(pw * mpz * 2.5 + 60)   # 1440 + 390 alle + 1280/1000 Stichproben ≈ 2,5 Messungen je Zustand, + Messlauf/Bewegung (heute gemessen ca. 40 min)
    oeff = os.environ.get('OEFFENTLICH') == 'true'   # öffentlicher Ordner: Minuten kostenlos, keine Grenze
    aus(weiter=str(oeff or verbraucht + hoch <= KONTINGENT).lower(), oeffentlich=oeff, verbraucht=verbraucht, hochrechnung_plakatwerkstatt=hoch, kontingent=KONTINGENT)
