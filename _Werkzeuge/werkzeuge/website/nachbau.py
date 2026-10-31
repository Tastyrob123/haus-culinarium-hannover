#!/usr/bin/env python3
"""Nach einem neuen Bau der Website eines Hauses: Kopie erneuern und den veröffentlichten Stand wieder darüberlegen.

  python3 werkzeuge/website/nachbau.py <haus> [port]      Port des Servers der Werkzeuge, Vorgabe 8970

Das ist die Antwort auf «Quelle in Bewegung» (STAND.md): Baut das Haus seine Seiten neu (bau.py), holt probe.py --neu die
neuen Seiten als Grundlage, dann schreibt der Server über «Seiten neu ausgeben» Grundlage + veröffentlichten Stand nach online/.
Am Ende steht, wie viele Änderungen ihren Platz nicht mehr finden (die Prüfseite nennt sie einzeln, «ohne Platz» räumt sie weg).
Anschluss im Seitenbau eines Hauses (eine Zeile am Ende von bau.py, nur wenn der Server läuft):
  subprocess.run(['python3', os.path.expanduser('~/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website/nachbau.py'), '<haus>'])
Schreibt nie in die Quelle des Hauses."""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

HIER = Path(__file__).resolve().parent


def ruf(port, methode, weg, daten=None):
    r = urllib.request.Request(f'http://127.0.0.1:{port}{weg}', method=methode, data=json.dumps(daten).encode() if daten is not None else None,
                               headers={'Content-Type': 'application/json', 'Origin': f'http://127.0.0.1:{port}'} if daten is not None else {})   # Origin: Server mit Herkunftsprüfung (Schaufenster) nehmen nur Schreibendes von der eigenen Adresse
    with urllib.request.urlopen(r, timeout=120) as a:
        return json.loads(a.read().decode('utf-8'))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    haus, port = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8970
    try:
        ruf(port, 'GET', f'/api/haus/{haus}')
    except Exception:
        sys.exit(f'Der Server der Werkzeuge antwortet auf Port {port} nicht. Nichts geändert.')
    print(subprocess.run([sys.executable, str(HIER / 'probe.py'), haus, '--neu'], capture_output=True, text=True, check=True).stdout.strip())
    print(ruf(port, 'POST', f'/api/x/website/reparieren/{haus}', {'was': 'ausgeben', 'wer': 'nachbau'}).get('meldung', ''))
    p = ruf(port, 'GET', f'/api/x/website/pruefung/{haus}')
    ohne = [x for x in p.get('punkte', []) if not x.get('gut')]
    print('Prüfung: alles in Ordnung.' if not ohne else 'Prüfung: ' + ' · '.join(x.get('titel', '') + ': ' + x.get('text', '') for x in ohne))


if __name__ == '__main__':
    main()
