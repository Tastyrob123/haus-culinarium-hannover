"""Zweiter, getrennter Durchgang: vergleicht die eingelesenen Karten Zeile für Zeile mit dem Original.

    python3 werkzeuge/karten/einlesen/abgleich.py gasterntal     → _qa/gasterntal-abgleich.md, Exitcode 1 bei Abweichung
    python3 werkzeuge/karten/einlesen/abgleich.py beau-rivage    → _qa/beau-rivage-abgleich.md

Gasterntal: Das Original (PDF des Hauses) wird hier mit einem ANDEREN Werkzeug gelesen als beim Einlesen
(pdftotext -bbox: einzelne Wörter mit Lage; das Einlesen nimmt pdftohtml -xml: Textstücke mit Schrift).
Geprüft wird in drei Schritten, die nichts voneinander wissen:
  1 Wort für Wort: jedes Wort des Originals steht gleich oft in den Daten und umgekehrt (Gross/Klein, Satzzeichen, Akzente genau).
  2 Zeile für Zeile: die Zeilen jeder Spalte werden der Reihe nach den Einträgen zugeteilt. Ein Eintrag muss seine Zeilen
    genau aufbrauchen, kein Wort mehr, keines weniger. So steht jeder Preis in der Zeile seines Gerichts.
  3 Gegenprobe: vier absichtliche Fehler (Preis, Buchstabe, zwei Preise vertauscht, Zeile weg) müssen auffallen.

Beau-Rivage: Die vier Karten sind unverändert übernommen. Verglichen wird Eintrag für Eintrag mit den Dateien des
Hauses (website/_karten/stand/*.json), dazu dieselbe Gegenprobe.
"""
import collections
import copy
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HIER = Path(__file__).resolve().parent
KARTEN = HIER.parent
PROJEKTE = Path.home() / 'Desktop/Website-Projekte'
ZEICHEN_OHNE_TEXT = {'➢'}   # Aufzählungszeichen des Originals (Schrift Wingdings), Gestaltung


def woerter_von(text):
    return [w for w in re.split(r'\s+', text or '') if w and w not in ZEICHEN_OHNE_TEXT]


# ---------- Daten → Einheiten zum Vergleichen ----------

def einheiten_der_karte(karte):
    """Jede Einheit: (Art und Stelle in den Daten, Liste der Wörter). Umschlag: Titel und jede Zeile einzeln."""
    deckel, posten = [], []
    for ti, t in enumerate(karte['teile']):
        if t['art'] == 'deckel':
            deckel.append((f'Umschlag · Titel', woerter_von(t.get('titel', '')) + woerter_von(t.get('unter', ''))))
            for i, z in enumerate(t.get('zeilen') or []):
                deckel.append((f'Umschlag · Zeile {i + 1}', woerter_von(z)))
            continue
        for i, u in enumerate(t['posten']):
            w = []
            for k in ('titel', 'en', 'zusatz', 'text', 'name', 'preis'):
                if k in u and isinstance(u[k], str):
                    w += woerter_von(u[k])
            for k in ('koepfe', 'einheiten', 'preise'):
                for x in u.get(k) or []:
                    w += woerter_von(x)
            for z in u.get('zeilen') or []:
                w += woerter_von(z['text'])
                for x in z.get('preise') or []:
                    w += woerter_von(x)
            was = u.get('titel') or u.get('name') or u.get('text') or (u.get('zeilen') or [{}])[0].get('text', '')
            posten.append((f'{u["t"]} «{was}»', w))
    return deckel, posten


def alle_woerter(karte):
    d, p = einheiten_der_karte(karte)
    return [w for _, ww in d + p for w in ww] + woerter_von(karte.get('fuss', ''))


# ---------- Original → Zeilen je Spalte (pdftotext -bbox) ----------

def original_zeilen(pdf, spalten_grenze=300.0):
    """Liste der Spalten in Lesefolge (Seite 1 links, Seite 1 rechts, Seite 2 links, …), jede eine Liste von Zeilen,
    jede Zeile eine Liste von Wörtern von links nach rechts."""
    roh = subprocess.run(['pdftotext', '-bbox', str(pdf), '-'], capture_output=True, text=True, check=True).stdout
    seiten, akt = [], None
    for z in roh.splitlines():
        if '<page ' in z:
            akt = []
            seiten.append(akt)
        m = re.search(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*)</word>', z)
        if m:
            import html
            akt.append((float(m.group(1)), float(m.group(4)), html.unescape(m.group(5)), float(m.group(3))))
    spalten = []
    for si, ws in enumerate(seiten, 1):
        for name, teil in (('links', [w for w in ws if w[0] < spalten_grenze]), ('rechts', [w for w in ws if w[0] >= spalten_grenze])):
            zeilen = []
            for x, unten, text, x_ende in sorted(teil, key=lambda w: (w[1], w[0])):
                if text in ZEICHEN_OHNE_TEXT:
                    continue
                if zeilen and abs(zeilen[-1]['unten'] - unten) <= 2.6:
                    zeilen[-1]['w'].append((x, text, x_ende))
                else:
                    zeilen.append({'unten': unten, 'w': [(x, text, x_ende)]})
            fertig = []
            for z in zeilen:
                ww = []
                for x, text, x_ende in sorted(z['w']):
                    # pdftotext -bbox trennt ein Wort, wo die Schrift wechselt. Stossen zwei Stücke ohne Lücke aneinander, sind sie ein Wort.
                    if ww and x - ww[-1][1] < 0.8:
                        ww[-1] = (ww[-1][0] + text, x_ende)
                    else:
                        ww.append((text, x_ende))
                fertig.append([t for t, _ in ww])
            spalten.append((f'Seite {si} {name}', fertig))
    return spalten


def original_woerter(pdf):
    """Alle Wörter der Textschicht in der Folge von pdftotext (ohne Lage): die Gegenkontrolle zu den Zeilen."""
    roh = subprocess.run(['pdftotext', str(pdf), '-'], capture_output=True, text=True, check=True).stdout
    return woerter_von(roh)


# ---------- Schritt 2: Zeile für Zeile ----------

def zeile_fuer_zeile(karte, spalten):
    """Teilt die Zeilen des Originals der Reihe nach den Einheiten der Daten zu. Rückgabe: (Protokoll, Abweichungen)."""
    deckel, posten = einheiten_der_karte(karte)
    zeilen = [(ort, i + 1, z) for ort, zz in spalten for i, z in enumerate(zz)]
    protokoll, abw = [], []
    zi = 0
    pi, di = 0, 0

    def versuche(einheit, ab):
        """Wie viele Zeilen ab «ab» braucht die Einheit genau auf? 0 = passt nicht."""
        soll = collections.Counter(einheit[1])
        ist = collections.Counter()
        for n in range(1, 12):
            if ab + n > len(zeilen):
                return 0
            ist.update(zeilen[ab + n - 1][2])
            if ist == soll:
                return n
            if ist - soll:          # ein Wort mehr, als der Eintrag hat: passt nicht
                return 0
        return 0

    while pi < len(posten) or di < len(deckel):
        kandidaten = []
        if pi < len(posten):
            kandidaten.append(('p', posten[pi]))
        if di < len(deckel):
            kandidaten.append(('d', deckel[di]))
        treffer = None
        for art, e in kandidaten:
            n = versuche(e, zi)
            if n:
                treffer = (art, e, n)
                break
        if not treffer:
            art, e = kandidaten[0]
            rest = ' '.join(zeilen[zi][2]) if zi < len(zeilen) else '(Original zu Ende)'
            ort = f'{zeilen[zi][0]}, Zeile {zeilen[zi][1]}' if zi < len(zeilen) else '–'
            abw.append(f'{e[0]}: Daten «{" ".join(e[1])}» passen nicht zum Original ab {ort}: «{rest}»')
            # weiter mit dem nächsten Eintrag, damit eine Abweichung nicht alle folgenden verdeckt
            if art == 'p':
                pi += 1
            else:
                di += 1
            # Zeilen überspringen, bis der nächste Eintrag wieder passt (höchstens 6)
            naechste = posten[pi] if pi < len(posten) else (deckel[di] if di < len(deckel) else None)
            if naechste:
                for sprung in range(0, 7):
                    if versuche(naechste, zi + sprung):
                        zi += sprung
                        break
            continue
        art, e, n = treffer
        benutzt = zeilen[zi:zi + n]
        protokoll.append((f'{benutzt[0][0]}, Zeile {benutzt[0][1]}' + (f'–{benutzt[-1][1]}' if n > 1 else ''),
                          ' / '.join(' '.join(z[2]) for z in benutzt), e[0]))
        zi += n
        if art == 'p':
            pi += 1
        else:
            di += 1
    if zi < len(zeilen):
        for ort, nr, z in zeilen[zi:]:
            abw.append(f'{ort}, Zeile {nr}: «{" ".join(z)}» steht im Original, aber in keinem Eintrag der Daten')
    return protokoll, abw, min(zi, len(zeilen))


def wort_fuer_wort(karte, pdf):
    daten = collections.Counter(alle_woerter(karte))
    orig = collections.Counter(original_woerter(pdf))
    fehlt, dazu = orig - daten, daten - orig
    abw = [f'«{w}» steht {n}-mal mehr im Original als in den Daten' for w, n in sorted(fehlt.items())]
    abw += [f'«{w}» steht {n}-mal mehr in den Daten als im Original' for w, n in sorted(dazu.items())]
    return sum(orig.values()), sum(daten.values()), abw


# ---------- Schritt 3: Gegenprobe ----------

def gegenproben(karte):
    """Vier absichtliche Fehler. Jeder gibt (Beschreibung, veränderte Karte)."""
    def posten_von(k):
        return next(t for t in k['teile'] if t['art'] == 'inhalt')['posten']
    aus = []
    a = copy.deepcopy(karte); g = [u for u in posten_von(a) if u['t'] == 'gericht' and u.get('preise') and u['preise'][-1]]
    alt = g[3]['preise'][-1]; g[3]['preise'][-1] = alt[:-1] + ('1' if alt[-1] != '1' else '2')
    aus.append((f'Preis von «{g[3]["name"]}» von {alt} auf {g[3]["preise"][-1]}', a))
    b = copy.deepcopy(karte); g = [u for u in posten_von(b) if u['t'] == 'gericht' and len(u['name']) > 5]
    alt = g[10]['name']; g[10]['name'] = alt[:2] + ('x' if alt[2] != 'x' else 'y') + alt[3:]
    aus.append((f'ein Buchstabe im Namen «{alt}» → «{g[10]["name"]}»', b))
    c = copy.deepcopy(karte); g = [u for u in posten_von(c) if u['t'] == 'gericht' and u.get('preise')]
    paar = next((x, y) for x, y in zip(g, g[1:]) if len(x['preise']) == 1 == len(y['preise']) and x['preise'] != y['preise']
                and bool(x.get('einheiten')) == bool(y.get('einheiten')))
    paar[0]['preise'], paar[1]['preise'] = paar[1]['preise'], paar[0]['preise']
    aus.append((f'Preise von «{paar[0]["name"]}» und «{paar[1]["name"]}» vertauscht (Wörter bleiben gleich, nur die Zeile ist falsch)', c))
    d = copy.deepcopy(karte); g = [u for u in posten_von(d) if u['t'] == 'gericht' and u.get('zeilen')]
    weg = g[2]['zeilen'].pop()
    aus.append((f'Zeile «{weg["text"]}» bei «{g[2]["name"]}» entfernt', d))
    return aus


# ---------- Bericht ----------

def md_tabelle(kopf, zeilen):
    def zelle(t):
        return str(t).replace('|', '\\|')
    return '\n'.join(['| ' + ' | '.join(kopf) + ' |', '|' + '---|' * len(kopf)] + ['| ' + ' | '.join(zelle(x) for x in z) + ' |' for z in zeilen])


def gasterntal():
    seed = json.loads((KARTEN / 'grundstand' / 'gasterntal.json').read_text(encoding='utf-8'))
    eintrag = seed['karten'][0]
    karte = eintrag['karte']
    pdf = PROJEKTE / 'Berghotel Gasterntal' / 'assets/pdf/Karte-2026.pdf'
    sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
    spalten = original_zeilen(pdf)
    n_orig, n_daten, abw_wort = wort_fuer_wort(karte, pdf)
    protokoll, abw_zeile, zugeteilt = zeile_fuer_zeile(karte, spalten)
    abw_herkunft = [] if eintrag['herkunft']['sha256'] == sha else ['Das Original ist nicht mehr die Datei, aus der gelesen wurde (Prüfsumme anders)']
    proben = []
    for was, falsch in gegenproben(karte):
        _, _, a1 = wort_fuer_wort(falsch, pdf)
        _, a2, _ = zeile_fuer_zeile(falsch, spalten)
        proben.append((was, len(a1), len(a2), 'aufgefallen' if (a1 or a2) else 'NICHT AUFGEFALLEN'))
    probe_ok = all(p[3] == 'aufgefallen' for p in proben)
    n_zeilen = sum(len(z) for _, z in spalten)
    posten = next(t for t in karte['teile'] if t['art'] == 'inhalt')['posten']
    art = collections.Counter(u['t'] for u in posten)
    n_preise = sum(1 for u in posten for p in u.get('preise') or [] if p)
    ok = not (abw_wort or abw_zeile or abw_herkunft) and probe_ok
    t = [f'# Abgleich · Berghotel Gasterntal · Karte «{karte["name"]}»', '',
         f'Stand {time.strftime("%d.%m.%Y %H:%M")} · erzeugt von `werkzeuge/karten/einlesen/abgleich.py gasterntal` · nicht von Hand ändern.', '',
         f'**Ergebnis: {"OHNE ABWEICHUNG" if ok else "ABWEICHUNGEN, die Karte kommt so nicht in den Speicher"}**', '',
         '## Was verglichen wurde', '',
         f'- Original: `Berghotel Gasterntal/assets/pdf/Karte-2026.pdf` (Word-PDF des Hauses, 2 Seiten), Prüfsumme `{sha[:16]}…` '
         f'{"= die Datei, aus der gelesen wurde" if not abw_herkunft else "≠ gelesene Datei"}.',
         '- Daten: `werkzeuge/karten/grundstand/gasterntal.json`, gelesen mit `einlesen/gasterntal_lesen.py` (pdftohtml).',
         '- Dieser Durchgang liest das Original neu und mit einem anderen Werkzeug (pdftotext, Wörter mit Lage).', '',
         '## Zahlen', '',
         md_tabelle(['Was', 'Original', 'Daten', 'Befund'], [
             ['Wörter (genau: Gross/Klein, Satzzeichen, Akzente)', n_orig, n_daten, 'gleich' if not abw_wort else f'{len(abw_wort)} Abweichungen'],
             ['Zeilen des Originals', n_zeilen, f'{zugeteilt} zugeteilt (an {len(protokoll)} Einträge und Zeilen des Umschlags)', 'jede Zeile zugeteilt' if not abw_zeile and zugeteilt == n_zeilen else f'{len(abw_zeile)} Abweichungen'],
             ['Einträge', '–', f'{len(posten)} ({", ".join(f"{n} {a}" for a, n in sorted(art.items()))})', ''],
             ['Preise', '–', n_preise, 'jeder in der Zeile seines Gerichts' if not abw_zeile else 'siehe Abweichungen'],
         ]), '',
         '## Abweichungen', '']
    alle = abw_herkunft + abw_wort + abw_zeile
    t += [f'- {a}' for a in alle] if alle else ['Keine.']
    t += ['', '## Gegenprobe (absichtliche Fehler müssen auffallen)', '',
          md_tabelle(['Absichtlicher Fehler', 'Wort für Wort', 'Zeile für Zeile', 'Befund'], [[w, a, b, c] for w, a, b, c in proben]), '',
          'Der dritte Fehler lässt alle Wörter gleich. Er fällt nur im Durchgang Zeile für Zeile auf, deshalb gibt es beide.', '',
          '## Was aus dem Original so übernommen ist, wie es dasteht', '',
          'Die Daten sind der Wortlaut des Hauses. Nichts ist berichtigt, nichts ergänzt. Auffälliges im Original, das deshalb auch in den Daten steht '
          '(das Projekt des Hauses führt dazu eine Liste von Berichtigungen in `_werkbank/satz_daten.py`, sie ist hier NICHT angewendet):', '']
    auff = ['Mineral /Süssgetränke', 'Apfelschorlle', '5.50.', 'Aperitiv', 'N0 45 Chardonnay', 'N0 40 Rivola', 'Sardo del Duero', 'Gin Gordons',
            'Gin Hendricks', 'www.Berghotelgasterntal ch', '. Das frische Wild', 'Vogelisi- Kaffee', 'Allergene', 'Tagesssuppe', 'Soup of day',
            'Pastamaufaktur', 'and brown', 'Blauseforelle', 'saucisson With', 'Perserving', 'or with applesauce', 'Linzer Cacke', 'Fruit Cacke',
            '37.5-43%', 'ausschließlich']
    text = ' '.join(alle_woerter(karte))
    deckel_text = ' '.join(w for _, ww in einheiten_der_karte(karte)[0] for w in ww)
    t += [f'- «{a}»' for a in auff if a in text or a in deckel_text]
    fehlen = [a for a in auff if a not in text and a not in deckel_text]
    if fehlen:
        t += ['', 'Nicht (mehr) so in den Daten: ' + ', '.join(f'«{a}»' for a in fehlen)]
    t += ['', '## Offen (steht nicht im Original)', ''] + [f'- {o}' for o in eintrag['offen']]
    t += ['', '## Was beim Einlesen verändert ist', '',
          '- Leerraum: mehrere Leerzeichen sind eines, Leerzeichen am Rand sind weg («Rosé  Pink Ladybird» → «Rosé Pink Ladybird»).',
          '- Anordnung: die Karte des Hauses ist ein gefaltetes Blatt mit zwei Spalten je Seite. In den Daten stehen die Einträge in Lesefolge '
          '(Seite 1 links, Seite 1 rechts, Seite 2 links, Seite 2 rechts); der Umschlag (Seite 1 rechts oben) ist das Deckblatt.',
          '- Sonst nichts.', '',
          '## Zeile für Zeile', '',
          md_tabelle(['Original', 'Wortlaut im Original', 'Eintrag in den Daten'], protokoll), '']
    (KARTEN / '_qa' / 'gasterntal-abgleich.md').write_text('\n'.join(t), encoding='utf-8')
    print(f'gasterntal: {n_orig} Wörter, {n_zeilen} Zeilen, {len(posten)} Einträge, {n_preise} Preise · '
          f'{"OHNE ABWEICHUNG" if ok else str(len(alle)) + " Abweichungen"} · Gegenprobe {"alle aufgefallen" if probe_ok else "NICHT bestanden"}')
    for a in alle[:40]:
        print('  ·', a)
    return ok


def beau_rivage():
    seed = json.loads((KARTEN / 'grundstand' / 'beau-rivage.json').read_text(encoding='utf-8'))
    quelle = PROJEKTE / 'Grand Beau-Rivage' / 'website' / '_karten' / 'stand'
    zeilen, abw, proben = [], [], []
    for eintrag in seed['karten']:
        z = eintrag['id']
        roh = (quelle / f'{z}.json').read_bytes()
        orig = json.loads(roh.decode('utf-8'))
        karte = eintrag['karte']
        sha = hashlib.sha256(roh).hexdigest()
        n = 0
        if eintrag['herkunft']['sha256'] != sha:
            abw.append(f'{z}: die Datei des Hauses ist nicht mehr die, die übernommen wurde (Prüfsumme anders)')
        if list(karte.keys()) != list(orig.keys()):
            abw.append(f'{z}: Felder der Karte anders: {sorted(set(karte) ^ set(orig))}')
        for k in orig:
            if k != 'teile' and karte.get(k) != orig[k]:
                abw.append(f'{z}: Feld «{k}» anders')
        if len(karte['teile']) != len(orig['teile']):
            abw.append(f'{z}: {len(karte["teile"])} Teile statt {len(orig["teile"])}')
        for ti, (a, b) in enumerate(zip(karte['teile'], orig['teile'])):
            if a.get('art') == 'deckel' or b.get('art') == 'deckel':
                n += 1
                if a != b:
                    abw.append(f'{z}: Deckblatt (Teil {ti + 1}) anders')
                continue
            if len(a['posten']) != len(b['posten']):
                abw.append(f'{z}: Teil {ti + 1} hat {len(a["posten"])} Einträge statt {len(b["posten"])}')
            for i, (x, y) in enumerate(zip(a['posten'], b['posten'])):
                n += 1
                if x != y:
                    abw.append(f'{z}: Teil {ti + 1}, Eintrag {i + 1} anders: Daten {json.dumps(x, ensure_ascii=False)[:120]} · Haus {json.dumps(y, ensure_ascii=False)[:120]}')
        preise = sum(1 for t in karte['teile'] for u in t.get('posten', []) for p in (u.get('preise') or []) + ([u['preis']] if u.get('preis') else [])
                     + [q for zz in u.get('zeilen') or [] for q in zz.get('preise') or []] if p)
        gleich = karte == orig
        zeilen.append([z, karte['name'], n, preise, f'`{sha[:16]}…`', 'gleich' if gleich else 'ANDERS'])
        if not gleich and not any(a.startswith(z + ':') for a in abw):
            abw.append(f'{z}: Karte nicht gleich (Stelle nicht eingegrenzt)')
        # Gegenprobe: ein Preis und ein Buchstabe anders, die Prüfung muss es merken
        f = copy.deepcopy(karte)
        g = [u for t in f['teile'] for u in t.get('posten', []) if u.get('t') == 'gericht' and u.get('preise')]
        g[1]['preise'][0] = g[1]['preise'][0] + '0'
        g[2]['name'] = g[2]['name'][:-1]
        proben.append([z, f'Preis von «{g[1]["name"]}» und Name «{g[2]["name"]}…» verändert', 'aufgefallen' if f != orig else 'NICHT AUFGEFALLEN'])
    ok = not abw and all(p[2] == 'aufgefallen' for p in proben)
    t = ['# Abgleich · Grand Beau-Rivage · vier Karten', '',
         f'Stand {time.strftime("%d.%m.%Y %H:%M")} · erzeugt von `werkzeuge/karten/einlesen/abgleich.py beau-rivage` · nicht von Hand ändern.', '',
         f'**Ergebnis: {"OHNE ABWEICHUNG" if ok else "ABWEICHUNGEN, die Karten kommen so nicht in den Speicher"}**', '',
         'Die vier Karten des Hauses sind unverändert übernommen: `Grand Beau-Rivage/website/_karten/stand/<karte>.json` steht Feld für Feld gleich '
         'unter `karten[].karte` in `werkzeuge/karten/grundstand/beau-rivage.json`. Um die Karte herum führt das Werkzeug eigene Angaben '
         '(Zeitraum, Sprachfassungen, Herkunft), die Karte selbst ist nicht angefasst.', '',
         md_tabelle(['Karte', 'Name', 'Einträge verglichen', 'Preise', 'Prüfsumme der Datei des Hauses', 'Befund'], zeilen), '',
         '## Abweichungen', ''] + ([f'- {a}' for a in abw] if abw else ['Keine.']) + ['',
         '## Gegenprobe', '', md_tabelle(['Karte', 'Absichtlicher Fehler', 'Befund'], proben), '',
         '## Was das für den Wortlaut heisst', '',
         'Die Dateien des Hauses sind schon berichtigte Fassungen (jede Karte führt ihre Liste unter `berichtigt` und den Vergleich mit der '
         'ursprünglichen PDF unter `pruef`). Diese Listen sind mit übernommen. Gegen die ursprünglichen PDF des Hauses ist hier NICHT neu geprüft, '
         'nur gegen die Karten-Dateien, wie der Auftrag es sagt.', '',
         '## Offen (steht in den Dateien nicht)', '',
         '- Zeitraum je Karte: die Dateien nennen kein «gilt von» und kein «gilt bis» (der Dateiname der ursprünglichen PDF sagt «Summer 2026»).',
         '- Allergene je Gericht: keine.', '- Die fünf Sprachfassungen des Hauses (`_karten/sprachen/`) sind nicht übernommen, der Auftrag nennt nur die vier Karten.', '']
    (KARTEN / '_qa' / 'beau-rivage-abgleich.md').write_text('\n'.join(t), encoding='utf-8')
    print(f'beau-rivage: {len(seed["karten"])} Karten, {sum(z[2] for z in zeilen)} Einträge · {"OHNE ABWEICHUNG" if ok else str(len(abw)) + " Abweichungen"}')
    for a in abw[:40]:
        print('  ·', a)
    return ok


if __name__ == '__main__':
    haus = sys.argv[1] if len(sys.argv) > 1 else ''
    if haus not in ('gasterntal', 'beau-rivage'):
        raise SystemExit('abgleich.py gasterntal | beau-rivage')
    sys.exit(0 if (gasterntal() if haus == 'gasterntal' else beau_rivage()) else 1)
