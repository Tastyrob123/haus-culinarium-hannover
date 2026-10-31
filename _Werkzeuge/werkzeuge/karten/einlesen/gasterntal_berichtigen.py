"""Berichtigt in der Karte des Berghotels Gasterntal die eindeutigen Tippfehler des Originals, als veröffentlichte Änderung.

    python3 werkzeuge/karten/einlesen/gasterntal_berichtigen.py --als-entwurf  → Berichtigungen als ENTWURF hinlegen (Stand seit 12.10.2026 23:00):
                                                                           veröffentlicht bleibt der Wortlaut des Hauses, Robert oder das Haus
                                                                           entscheidet im Werkzeug («Vorher / nachher» → Veröffentlichen oder verwerfen)
    python3 werkzeuge/karten/einlesen/gasterntal_berichtigen.py          → berichtigen, drucken, prüfen, veröffentlichen
    python3 werkzeuge/karten/einlesen/gasterntal_berichtigen.py --zeige  → nur zeigen, was sich ändern würde

Der erste Stand im Speicher ist der Wortlaut des Hauses (Abgleich ohne Abweichung). Diese Berichtigung kommt DANACH, als
eigene Fassung mit Notiz: sie steht im Werkzeug unter «Frühere Fassungen» und lässt sich dort zurückholen.
Was berichtigt wird, steht nicht hier, sondern in der Liste des Hauses-Projekts (_werkbank/satz_daten.py, BERICHTIGT,
von Robert am 09.10.2026 so eingeführt; dieselbe Liste steckt in der Karte, die dem Haus als Unterlage gezeigt wurde).
Regel dazu: Website-Bau — Standards & Ablauf (Master), 2.10: eindeutige Tippfehler werden in Unterlagen berichtigt, gelistet, gemeldet.
Veröffentlicht wird über den Weg des Werkzeugs: PDF neu, PDF gegen Daten geprüft, erst dann umgeschaltet.
"""
import ast
import copy
import json
import sys
import time
from pathlib import Path

HIER = Path(__file__).resolve().parent
KARTEN = HIER.parent
sys.path.insert(0, str(KARTEN))
sys.path.insert(0, str(KARTEN.parent.parent / 'unterbau'))
import api  # noqa: E402
import speicher  # noqa: E402

QUELLE = Path.home() / 'Desktop/Website-Projekte/Berghotel Gasterntal/_werkbank/satz_daten.py'
HAUS = 'gasterntal'


def liste():
    baum = ast.parse(QUELLE.read_text(encoding='utf-8'))
    for k in baum.body:
        if isinstance(k, ast.Assign) and any(getattr(z, 'id', '') == 'BERICHTIGT' for z in k.targets):
            return [tuple(x) for x in ast.literal_eval(k.value)]
    raise SystemExit('BERICHTIGT nicht gefunden')


def berichtige(doc, paare):
    """Wendet jedes Paar auf jeden Text der Karte an. Rückgabe: {(alt, neu): Anzahl}."""
    gezaehlt = {}

    def einmal(t, alt, neu):
        """Ersetzt alt durch neu, aber nie dort, wo schon neu steht («brown» → «brown butter» darf nicht zweimal greifen)."""
        maske = '\x00'
        frei = t.replace(neu, maske)
        n = frei.count(alt)
        return frei.replace(alt, neu).replace(maske, neu), n

    def text(t):
        for alt, neu, _ in paare:
            if '<br>' not in alt and alt in t:
                t, n = einmal(t, alt, neu)
                if n:
                    gezaehlt[(alt, neu)] = gezaehlt.get((alt, neu), 0) + n
        return t

    def block(zeilen):      # Paare über einen Zeilenwechsel hinweg (im Projekt als <br> geschrieben)
        ganz = '<br>' + '<br>'.join(zeilen) + '<br>'
        for alt, neu, _ in paare:
            if '<br>' in alt and alt in ganz:
                neu_ganz, n = einmal(ganz, alt, neu)
                if n and neu_ganz.count('<br>') == ganz.count('<br>'):
                    gezaehlt[(alt, neu)] = gezaehlt.get((alt, neu), 0) + n
                    ganz = neu_ganz
        # Paare, deren Wörter im Original auf zwei Zeilen stehen («über Allergene» / «Zutaten»): Wort für Wort ersetzen, der Zeilenwechsel bleibt
        import re
        for alt, neu, _ in paare:
            wa, wn = alt.split(), neu.split()
            if '<br>' in alt or len(wa) != len(wn) or len(wa) < 2 or any(alt in z for z in ganz[4:-4].split('<br>')):
                continue
            muster = re.compile(r'(\s|<br>)+'.join(re.escape(w) for w in wa))
            m = muster.search(ganz)
            if m and '<br>' in m.group(0):
                trenner = re.split('|'.join(re.escape(w) for w in wa), m.group(0))[1:-1]
                ersatz = ''.join(w + (trenner[i] if i < len(trenner) else '') for i, w in enumerate(wn))
                ganz = ganz[:m.start()] + ersatz + ganz[m.end():]
                gezaehlt[(alt, neu)] = gezaehlt.get((alt, neu), 0) + 1
        return ganz[4:-4].split('<br>')

    for e in doc['karten']:
        for t in e['karte']['teile']:
            if t['art'] == 'deckel':
                t['titel'], t['unter'] = text(t['titel']), text(t.get('unter', ''))
                t['zeilen'] = [text(z) for z in block(t.get('zeilen') or [])] if t.get('zeilen') else []
                continue
            for u in t['posten']:
                for f in ('titel', 'zusatz', 'text', 'name'):
                    if isinstance(u.get(f), str):
                        u[f] = text(u[f])
                if isinstance(u.get('en'), str):
                    u['en'] = text(u['en'])
                for f in ('koepfe', 'einheiten'):
                    if u.get(f):
                        u[f] = [text(x) for x in u[f]]
                if u.get('zeilen'):
                    for z, neu in zip(u['zeilen'], block([z['text'] for z in u['zeilen']])):
                        z['text'] = text(neu)
    return gezaehlt


if __name__ == '__main__':
    paare = liste()
    s = speicher.lesen(HAUS, 'karten')
    if s['live'] is None:
        raise SystemExit('Für das Gasterntal ist noch nichts eingelesen (einlesen.py gasterntal).')
    if s['entwurf'] is not None:
        raise SystemExit('Es liegt ein Entwurf vor. Der wird nicht überschrieben: erst veröffentlichen oder verwerfen.')
    if '--als-entwurf' in sys.argv and not berichtige(copy.deepcopy(s['live']), paare):
        # Die Berichtigungen sind schon veröffentlicht: zuerst den Wortlaut des Hauses (erster Stand) wieder veröffentlichen
        grund = json.loads((KARTEN / 'grundstand' / 'gasterntal.json').read_text(encoding='utf-8'))
        fassung = next((f['fassung'] for f in speicher.verlauf(HAUS, 'karten') if speicher.kennung(speicher.fassung_lesen(HAUS, 'karten', f['fassung'])['daten']) == speicher.kennung(grund)), None)
        if not fassung:
            raise SystemExit('Der erste Stand (Wortlaut des Hauses) steht nicht im Verlauf. Nichts geändert.')
        s = speicher.zurueckholen(HAUS, 'karten', fassung, 'einlesen')
        status, antwort = api.bearbeite('POST', ['veroeffentlichen', HAUS], {'erwartet': s['kennung_entwurf'], 'wer': 'einlesen', 'notiz': 'Wortlaut des Hauses wieder veröffentlicht; die Berichtigungen liegen als Entwurf bereit'}, speicher)
        if status != 200:
            speicher.entwurf_verwerfen(HAUS, 'karten', 'einlesen')
            raise SystemExit(f'Nichts geändert: {antwort}')
        s = antwort['stand']
        print('Wortlaut des Hauses wieder veröffentlicht (PDF neu gedruckt und geprüft).')
    neu = copy.deepcopy(s['live'])
    gezaehlt = berichtige(neu, paare)
    angewendet = [(a, n, g, gezaehlt[(a, n)]) for a, n, g in paare if (a, n) in gezaehlt]
    fehlt = [(a, n, g) for a, n, g in paare if (a, n) not in gezaehlt]
    for a, n, g, z in angewendet:
        print(f'  {z}× «{a}» → «{n}» ({g})')
    print(f'{len(angewendet)} Berichtigungen an {sum(x[3] for x in angewendet)} Stellen · {len(fehlt)} Einträge der Liste betreffen diese Karte nicht (Willkommensschreiben) oder stehen schon richtig da')
    if '--zeige' in sys.argv or not angewendet:
        sys.exit(0)
    s = speicher.entwurf_schreiben(HAUS, 'karten', neu, s['kennung_live'], 'einlesen')
    tabelle = ['| Im Original | Berichtigt | Grund | Stellen |', '|---|---|---|---|'] + [f'| {a.replace("|", "/")} | {n.replace("|", "/")} | {g} | {z} |' for a, n, g, z in angewendet]
    rest = ['', '## Nicht in der Liste des Projekts, deshalb unberührt', '', '- Preis «5.50.» mit Punkt bei «Rugenbräu Alkoholfrei» (im Original so).',
            '- Mundart, Namen und Preise bleiben, wie das Haus sie schreibt.', '', '## Einträge der Liste, die diese Karte nicht betreffen', ''] + [f'- «{a}» → «{n}» ({g})' for a, n, g in fehlt] + ['']
    if '--als-entwurf' in sys.argv:
        md = ['# Berichtigungen · Berghotel Gasterntal · Karte', '',
              f'Stand {time.strftime("%d.%m.%Y %H:%M")} · erzeugt von `werkzeuge/karten/einlesen/gasterntal_berichtigen.py --als-entwurf` · nicht von Hand ändern.', '',
              '**Veröffentlicht ist der Wortlaut des Hauses** (siehe `gasterntal-abgleich.md`). Die eindeutigen Tippfehler, die das Projekt des Hauses listet '
              '(`Berghotel Gasterntal/_werkbank/satz_daten.py`, `BERICHTIGT`), liegen **als Entwurf** im Werkzeug. Die Entscheidung ist offen: '
              'im Werkzeug «Vorher / nachher» ansehen, dann «Veröffentlichen» oder «Entwurf verwerfen».', ''] + tabelle + rest
        (KARTEN / '_qa' / 'gasterntal-berichtigt.md').write_text('\n'.join(md), encoding='utf-8')
        print(f'als Entwurf abgelegt, nichts veröffentlicht · Liste: werkzeuge/karten/_qa/gasterntal-berichtigt.md')
        sys.exit(0)
    status, antwort = api.bearbeite('POST', ['veroeffentlichen', HAUS], {'erwartet': s['kennung_entwurf'], 'wer': 'einlesen', 'notiz': 'Tippfehler des Originals berichtigt (Liste des Projekts)'}, speicher)
    if status != 200:
        speicher.entwurf_verwerfen(HAUS, 'karten', 'einlesen')
        raise SystemExit(f'NICHT veröffentlicht, der Entwurf ist wieder weg: {antwort}')
    b = antwort['bericht'][0]
    md = ['# Berichtigungen · Berghotel Gasterntal · Karte', '',
          f'Stand {time.strftime("%d.%m.%Y %H:%M")} · erzeugt von `werkzeuge/karten/einlesen/gasterntal_berichtigen.py` · nicht von Hand ändern.', '',
          'Der erste Stand im Speicher ist der Wortlaut des Hauses (siehe `gasterntal-abgleich.md`). Danach, als eigene veröffentlichte Fassung, sind die '
          'eindeutigen Tippfehler berichtigt, die das Projekt des Hauses listet (`Berghotel Gasterntal/_werkbank/satz_daten.py`, `BERICHTIGT`). '
          'Im Werkzeug steht der Stand davor unter «Frühere Fassungen» und lässt sich zurückholen.', '',
          f'Veröffentlicht über das Werkzeug: PDF mit {b["seiten"]} Seiten neu gedruckt und gegen die Daten geprüft.', '',
          '| Im Original | Berichtigt | Grund | Stellen |', '|---|---|---|---|']
    md += [f'| {a.replace("|", "/")} | {n.replace("|", "/")} | {g} | {z} |' for a, n, g, z in angewendet]
    md += ['', '## Nicht berichtigt, weil es nicht in der Liste des Projekts steht', '',
           '- Preis «5.50.» mit Punkt bei «Rugenbräu Alkoholfrei» (im Original so).',
           '- Mundart, Namen und Preise bleiben, wie das Haus sie schreibt.', '',
           '## Einträge der Liste, die diese Karte nicht betreffen', ''] + [f'- «{a}» → «{n}» ({g})' for a, n, g in fehlt] + ['']
    (KARTEN / '_qa' / 'gasterntal-berichtigt.md').write_text('\n'.join(md), encoding='utf-8')
    print(f'veröffentlicht · PDF {b["seiten"]} Seiten, geprüft · Liste: werkzeuge/karten/_qa/gasterntal-berichtigt.md')
