"""Ausgabe · die einzige Stelle des Werkzeugs «website», die Seiten schreibt.

Die Daten des Werkzeugs (Schicht, Entwurf, Verlauf) liegen im gemeinsamen Speicher. Hier steht nur, was daraus «online» wird:
die Kopie der gebauten Seiten unter _probe/<haus>/online/. Kommt später ein echtes Ziel (Hochladen zum Haus), wird nur diese
Datei ersetzt; api.py ruft weiter schreibe() und vergleich().

Geschrieben wird erst in eine Nebendatei, dann umbenannt. Was schon stimmt, wird nicht angefasst.
Umgebung: WEBSITE_PROBE = anderer Ordner für die Kopien (Prüfläufe arbeiten auf einer Wegwerf-Kopie)."""
import fcntl
import os
from contextlib import contextmanager
from pathlib import Path

HIER = Path(__file__).resolve().parent


def probe_ordner():
    return Path(os.environ.get('WEBSITE_PROBE') or HIER / '_probe')


@contextmanager
def sperre(haus):
    """Ein Veröffentlichen zur Zeit je Haus."""
    with open(probe_ordner() / haus / '.ausgabe-sperre', 'w') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def vergleich(haus, seiten):
    """Welche Dateien online anders sind als sie sein sollen (seiten: Pfad → Bytes)."""
    o = probe_ordner() / haus / 'online'
    return [rel for rel, roh in seiten.items() if not (o / rel).is_file() or (o / rel).read_bytes() != roh]


def schreibe(haus, seiten):
    """Schreibt jede Seite, die online noch anders ist. Antwort: die geschriebenen Pfade."""
    o = (probe_ordner() / haus / 'online').resolve()
    geschrieben = []
    for rel in vergleich(haus, seiten):
        ziel = (o / rel).resolve()
        if o not in ziel.parents:
            raise OSError(f'{rel} liegt ausserhalb der Kopie')
        neben = ziel.with_suffix(ziel.suffix + '.neu')
        with open(neben, 'wb') as f:
            f.write(seiten[rel])
            f.flush()
            os.fsync(f.fileno())
        os.replace(neben, ziel)
        geschrieben.append(rel)
    return geschrieben
