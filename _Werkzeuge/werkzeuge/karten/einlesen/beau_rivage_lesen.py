"""Übernimmt die vier Karten des Grand Beau-Rivage unverändert als Daten.

    python3 werkzeuge/karten/einlesen/beau_rivage_lesen.py    → grundstand/beau-rivage.json

Quelle: <Projekt>/website/_karten/stand/<karte>.json (nur gelesen). Jede Karte steht Feld für Feld gleich unter
karten[].karte. Was das Werkzeug zusätzlich führt (Zeitraum, Sprachfassungen, Herkunft), steht daneben, nie in der Karte.
Ob die Übernahme stimmt, prüft getrennt einlesen/abgleich.py beau-rivage.
"""
import hashlib
import json
from pathlib import Path

HIER = Path(__file__).resolve().parent
QUELLE = Path.home() / 'Desktop/Website-Projekte/Grand Beau-Rivage/website/_karten/stand'
ZIEL = HIER.parent / 'grundstand' / 'beau-rivage.json'
KARTEN = ['ambiance', 'petite-suisse', 'vieux-rivage', 'weinkarte']   # Reihenfolge des Hauses (mission_control.py, ZIELE)

if __name__ == '__main__':
    karten = []
    for z in KARTEN:
        roh = (QUELLE / f'{z}.json').read_bytes()
        karten.append(dict(
            id=z,
            gilt=dict(von='', bis=''),
            fassungen={},
            herkunft=dict(original=f'Grand Beau-Rivage/website/_karten/stand/{z}.json', sha256=hashlib.sha256(roh).hexdigest(),
                          gelesen_mit='einlesen/beau_rivage_lesen.py'),
            offen=['Zeitraum der Karte: die Datei des Hauses nennt kein «gilt von» und kein «gilt bis».',
                   'Allergene je Gericht: die Datei des Hauses nennt keine.'],
            karte=json.loads(roh.decode('utf-8'))))
    d = dict(schema=1, haus='beau-rivage', karten=karten)
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'geschrieben: werkzeuge/karten/grundstand/beau-rivage.json · {len(karten)} Karten · '
          + ', '.join(f'{k["id"]} {sum(len(t.get("posten", [])) for t in k["karte"]["teile"])}' for k in karten))
