"""einlesen.py · bringt die Karten eines Hauses als ersten Stand in den Speicher (grundstand_setzen).

    python3 werkzeuge/karten/einlesen.py gasterntal
    python3 werkzeuge/karten/einlesen.py beau-rivage
    python3 werkzeuge/karten/einlesen.py alle
    python3 werkzeuge/karten/einlesen.py --datei <karten.json> <haus>     ein weiteres Haus aus einer Datei derselben Form

Für die zwei Probehäuser läuft vorher der Abgleich gegen das Original (einlesen/abgleich.py). Nur ohne Abweichung
kommt die Karte in den Speicher. Gibt es für das Haus schon einen Stand, geschieht nichts: der Speicher lässt einen
zweiten Grundstand nicht zu, und gepflegte Karten werden nie überschrieben.
Wohin geschrieben wird, bestimmt wie überall WERKZEUGE_DATEN (Prüfläufe: ein Wegwerf-Ordner).
"""
import json
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
sys.path.insert(0, str(HIER.parent.parent / 'unterbau'))
import modell as M  # noqa: E402
import speicher  # noqa: E402

HAEUSER = ('gasterntal', 'beau-rivage')


def setze(haus, datei, mit_abgleich):
    if mit_abgleich:
        r = subprocess.run([sys.executable, str(HIER / 'einlesen' / 'abgleich.py'), haus], capture_output=True, text=True)
        print('  Abgleich:', r.stdout.strip().splitlines()[0] if r.stdout.strip() else r.stderr.strip()[-200:])
        if r.returncode:
            print(f'  {haus}: NICHT eingelesen, der Abgleich zeigt Abweichungen (werkzeuge/karten/_qa/{haus}-abgleich.md)')
            return False
    d = json.loads(Path(datei).read_text(encoding='utf-8'))
    f = M.pruefe(d, haus)
    if f:
        print(f'  {haus}: NICHT eingelesen, die Daten haben nicht die Form des Werkzeugs: {f}')
        return False
    if speicher.lesen(haus, 'karten')['live'] is not None:
        gleich = speicher.lesen(haus, 'karten')['kennung_live'] == speicher.kennung(d)
        print(f'  {haus}: es gibt schon einen Stand im Speicher ({"gleich dem Grundstand" if gleich else "inzwischen gepflegt"}), nichts geändert')
        return True
    s = speicher.grundstand_setzen(haus, 'karten', d, 'einlesen')
    print(f'  {haus}: {len(d["karten"])} Karte(n) im Speicher, Kennung {s["kennung_live"]}')
    return True


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == '--datei':
        gut = setze(a[2], a[1], False)
    elif len(a) == 1 and (a[0] in HAEUSER or a[0] == 'alle'):
        gut = all([setze(h, HIER / 'grundstand' / f'{h}.json', True) for h in (HAEUSER if a[0] == 'alle' else [a[0]])])
    else:
        raise SystemExit(__doc__)
    sys.exit(0 if gut else 1)
