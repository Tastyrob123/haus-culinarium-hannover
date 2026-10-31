"""Das Besucherbuch (Le Registre) · Culinarium Hannover: der Dienst /api/registre als zwei Funktionen, damit der eigene Server des Werkzeugs (server.py,
Port 9086) und später der Hausserver (Anschluss bei der Auslieferung) genau dasselbe antworten. Online antwortet online/registre.py (gleiche Regeln, eigener Speicher).

  antwort_get(query)                      → (code, daten)   Vorführung: Beispielwerte (ablage_heute); mit ?k=<Schlüssel> echte Werte; ?export=1 nur mit Schlüssel
  antwort_post(pfad_query, roh, ip, ua)   → (code, daten)   eine Zeile von assets/js/messung.js; ?fehler=1 Skriptfehler des Werkzeugs (nur ins Protokoll)
Schlüssel: nur seine Prüfsumme steht hier (G09); der Schlüssel liegt ausserhalb des Projekts in ~/Desktop/Website-Projekte/_Schluessel/culinarium-hannover.txt.
Geht das Haus in Betrieb: VORFUEHRUNG = False hier, in online/registre.py und in registre.js (Entscheid Robert)."""
import hashlib, os, sys, urllib.parse

HIER = os.path.dirname(os.path.abspath(__file__))
if HIER not in sys.path:
    sys.path.insert(0, HIER)
import importlib.util  # noqa: E402
_sp = importlib.util.spec_from_file_location('registre_culinarium', os.path.join(HIER, 'registre.py'))   # nach Pfad, nie über den Namen (Werkzeug-Master F10)
RG = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(RG)

VORFUEHRUNG = True
SCHLUESSEL = 'f04c5cb0b86365e3510f65ef03e89c959d16338e9d8717a0c6f9fcb57638b8b7'   # SHA-256 des eigenen Schlüssels von Culinarium (28.10.2026), nie der eines anderen Hauses
ORT_LOKAL = ('DE', 'Hannover', 'NI')   # lokal kennt niemand das Land der Verbindung


def _echt(q):
    return not VORFUEHRUNG or hashlib.sha256((q.get('k') or [''])[0].encode()).hexdigest() == SCHLUESSEL


def antwort_get(query):
    q = urllib.parse.parse_qs(query or '')
    tage = (q.get('tage') or ['30'])[0]
    try:
        if (q.get('export') or [''])[0]:   # Datenexport: nur echte Werte, nur mit Schlüssel
            if not _echt(q) or (q.get('beispiel') or [''])[0]:
                return 403, {'fehler': 'ZUGANG · Die Besuche gibt es nur mit Schlüssel.'}
            return 200, RG.ausfuhr(tage)
        if (q.get('beispiel') or [''])[0] or not _echt(q):
            return 200, RG.ablage_heute(tage)
        return 200, RG.stand(tage)
    except Exception as e:  # noqa: BLE001  keine Fehlerspur nach aussen
        return 500, {'fehler': 'SERVER · Auswertung fehlgeschlagen (' + type(e).__name__ + ').'}


def antwort_post(query, roh, ip, ua):
    if len(roh or b'') > 300:
        return 413, {'fehler': 'GROESSE · Eine Zeile hat höchstens 300 Zeichen.'}
    if 'fehler=1' in (query or ''):   # Fehlermelder des Werkzeugs: nur ins Protokoll, nichts gespeichert
        sys.stderr.write('Das Besucherbuch, Fehler im Browser: ' + (roh or b'').decode('utf-8', 'replace')[:300].replace('\n', ' ') + '\n')
        return 204, None
    try:
        RG.melde(roh, ip, ua or '', *ORT_LOKAL)
    except Exception:  # noqa: BLE001  die Website wartet auf keine Antwort
        pass
    return 204, None
