"""Probelauf des Speichers in einem eigenen Wegwerf-Ordner. Start: python3 unterbau/pruefe.py
Rührt die echten Daten nie an. Am Ende steht BESTANDEN oder die Stelle, die nicht stimmt."""
import os
import sys
import tempfile
from pathlib import Path

tmp = tempfile.mkdtemp(prefix='werkzeuge-probe-')
os.environ['WERKZEUGE_DATEN'] = tmp
sys.path.insert(0, str(Path(__file__).resolve().parent))
import speicher as s  # noqa: E402

H, W = 'probehaus', 'website'
gezaehlt = 0


def pruef(wahr, was):
    global gezaehlt
    gezaehlt += 1
    if not wahr:
        print('NICHT BESTANDEN:', was)
        sys.exit(1)


def wirft(fehler, tun, was):
    try:
        tun()
    except fehler:
        pruef(True, was)
    else:
        pruef(False, was + ' (kein Fehler gekommen)')


a = s.lesen(H, W)
pruef(a['live'] is None and a['entwurf'] is None and not a['offen'], 'leerer Anfang')

a = s.grundstand_setzen(H, W, {'fruehstueck': '07:00 bis 10:30'}, 'probe')
pruef(a['live'] == {'fruehstueck': '07:00 bis 10:30'} and not a['offen'], 'Grundstand')
wirft(s.Konflikt, lambda: s.grundstand_setzen(H, W, {}, 'probe'), 'zweiter Grundstand wird abgelehnt')

wirft(s.Konflikt, lambda: s.entwurf_schreiben(H, W, {'fruehstueck': 'x'}, None, 'probe'), 'Schreiben ohne Kennung wird abgelehnt')
b = s.entwurf_schreiben(H, W, {'fruehstueck': '07:00 bis 11:00'}, a['kennung_live'], 'probe')
pruef(b['offen'] and b['live'] == a['live'] and b['entwurf']['fruehstueck'] == '07:00 bis 11:00', 'Entwurf gespeichert, live unverändert')
pruef(s.lesen(H, W) == b, 'nach neuem Lesen noch da')

wirft(s.Konflikt, lambda: s.entwurf_schreiben(H, W, {'fruehstueck': 'y'}, a['kennung_live'], 'zweiter'), 'veraltete Kennung gibt Konflikt')
pruef(s.lesen(H, W)['entwurf']['fruehstueck'] == '07:00 bis 11:00', 'Konflikt hat nichts überschrieben')

c = s.veroeffentlichen(H, W, 'probe', 'Frühstück länger')
pruef(c['live']['fruehstueck'] == '07:00 bis 11:00' and c['entwurf'] is None and not c['offen'], 'veröffentlicht')
wirft(s.Konflikt, lambda: s.veroeffentlichen(H, W, 'probe'), 'ohne Änderung nichts zu veröffentlichen')

v = s.verlauf(H, W)
pruef(len(v) == 1 and v[0]['notiz'] == 'Frühstück länger', 'Verlauf hat die abgelöste Fassung')
pruef(s.fassung_lesen(H, W, v[0]['fassung'])['daten'] == a['live'], 'Fassung enthält den alten Stand')
wirft(s.Unbekannt, lambda: s.fassung_lesen(H, W, '../../etc'), 'falsche Fassung wird abgelehnt')

d = s.zurueckholen(H, W, v[0]['fassung'], 'probe')
pruef(d['offen'] and d['entwurf'] == a['live'] and d['live'] == c['live'], 'Zurückholen legt nur einen Entwurf an')
e = s.veroeffentlichen(H, W, 'probe', 'zurück')
pruef(e['live'] == a['live'] and len(s.verlauf(H, W)) == 2, 'alter Stand wieder live, Verlauf wächst')

f = s.entwurf_schreiben(H, W, {'fruehstueck': 'z'}, e['kennung_live'], 'probe')
g = s.entwurf_verwerfen(H, W, 'probe')
pruef(f['offen'] and g['entwurf'] is None and g['live'] == e['live'], 'Entwurf verwerfen')

live = Path(tmp) / H / W / 'live.json'
h = s.entwurf_schreiben(H, W, {'fruehstueck': '08:00'}, g['kennung_live'], 'probe')
s.veroeffentlichen(H, W, 'probe')
live.write_text('{kaputt', encoding='utf-8')
pruef(s.lesen(H, W)['live'] == e['live'], 'beschädigte Datei: Sicherung (Stand vor der letzten Änderung) kommt zurück, nie still leer')
pruef(s.protokoll(H, W)[0]['was'] == 'aus-sicherung', 'die Rückkehr aus der Sicherung steht im Protokoll')
live.write_text('{kaputt', encoding='utf-8')
(live.parent / 'live.json.gut').unlink()
wirft(s.Beschaedigt, lambda: s.lesen(H, W), 'beschädigt ohne Sicherung bricht ab')

wirft(s.Unbekannt, lambda: s.lesen('../x', W), 'falscher Hausname wird abgelehnt')
pruef(len(s.protokoll(H, W)) >= 8 and any(z['was'] == 'veroeffentlicht' for z in s.protokoll(H, W)), 'Protokoll führt mit')

print(f'BESTANDEN · {gezaehlt} Prüfungen · Wegwerf-Ordner {tmp}')
