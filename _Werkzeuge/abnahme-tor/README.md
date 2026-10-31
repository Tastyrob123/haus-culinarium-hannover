# Abnahme-Tor (seit 29.10.2026)

Pflicht laut `OBERCHEF-PAKET.md`, Abschnitt «Abnahme-Tor vor Robert». Gemessen wird gegen jeden Satz in `ROBERTS-KRITERIEN.md`. Ohne Grün des Tors sieht Robert nichts.

## Was es tut
1. **Inventar aus dem Werkzeug selbst** (`tor.js`): Das Tor öffnet jedes Ziel aus der Zielliste und klickt jede bedienbare Stelle an, die nichts verändert.
   - Jeder neue Zustand kommt ins Inventar: Navigation, Reiter, Fenster, «Neu erstellen», Vorlage, Dokument, Unterseite, Editor mit offener Leiste (Klick auf die grösste Schrift im Dokument, je hohes und queres Dokument).
   - Zustände werden an ihrer Kennung erkannt: Weg, aktive Navigation, offene Fenster, Titel, Dokumente.
   - Gleichartige Stücke im Inhalt (z. B. 231 Fotos) werden zu dritt bedient. Führt eins davon zu einem Dokument, werden alle bedient, denn jede Vorlage zählt einzeln. Navigationen werden immer vollständig bedient.
   - Bekommt ein Werkzeug neue Zustände, stehen sie beim nächsten Lauf im Inventar, ohne dass jemand eine Liste pflegt.
2. **Messung jedes Zustands**: WebKit 1440×900 mit Bild. Es laufen der Messlauf (`../messlauf/messen.js`) und die Ergänzungen in `seite.js`:
   - **K1** Rundknopf ohne eigene Fläche
   - **K2** Platzhalter abgeschnitten; Beschriftung ohne Luft im Knopf
   - **K4** leere Kachel und Hintergrund-Flächen (Bildprüfung)
   - **K6** gemeinsame linke Kante
   - **K7** Einzelwort in der letzten Zeile
   - **K8** blasser Platzhalter
   - **K10** Löcher und Mitte der Dokumente (Bildprüfung)
   - **K12** Stil: Versalien und Trennzeichen laut `stil` in der Zielliste; liegt ein `stilblatt.json` vor, sind dessen Werte einzutragen
   - **K14** doppelte Marke
   - **K15** zwei Wege zum selben Ziel
   - **K18** zu wenige Vorlagen

   Danach folgen Stichproben bei 1280×800, 1000×650 (Roberts Safari) und 390×844.
3. **Messlauf** (Pflicht vor jeder Übergabe, `../messlauf/messlauf.sh <haus>`, Anleitung `../messlauf/ANLEITUNG.md`): `lauf.js` startet ihn am Ende des Oberflächen-Laufs selbst (Chromium + WebKit, 1440/1280/390, Tafel unter `<ausgabe>/messlauf/`). Seine Messfunktion `messen.js` läuft ausserdem in jedem Zustand des Tors (Kriterien 1, 2, 3, 5, 7 «einzelwort», 13 «beschnitten»).
4. **Auswertung** (`auswertung.py`): Abdeckungstafel Zustand × Kriterium mit grün, rot, Auge (Kriterium A, Urteil mit dem Auge in `augen.json`), nicht prüfbar oder entfällt. Dazu kommen eine Fundliste mit Bild und, falls angegeben, die Gegenprobe gegen Roberts Funde.

## Aufruf
```
node lauf.js ziele-<haus>.json <haus>/_qa/abnahme-tor/<lauf> --parallel 4
python3 auswertung.py <haus>/_qa/abnahme-tor/<lauf> _Oberchef/zeigen/<haus>/abnahme-tor --titel "…" [--gegenprobe gegenprobe-<haus>.json] [--augen augen.json]
```
Die Zielliste `ziele-<haus>.json` kommt aus `../messlauf/ziele-<haus>.json`. Dazu kommen der Bereich (`bereich`), das Vorwissen im Browser (`localStorage`) und die Hausregeln (`stil`).

Gesperrt ist alles, was etwas verändert oder verschickt (`gefahr`). POST-Anfragen beantwortet das Tor selbst, damit kein Server schreibt; mailto und tel werden abgefangen.

## Gegenprobe
Jeder Fund Roberts kommt als Zeile in `gegenprobe-<haus>.json`: Kriterium und Suchmuster. Das Tor muss ihn am Stand vor der Reparatur finden. Findet es ihn nicht, wird erst das Tor erweitert, dann die Reparatur gemeldet.
Culinarium 29.10.: Der alte Stand der Plakatwerkstatt wurde aus den Sicherungen `*.vor-*-2026-10-29` unter `Culinarium Hannover/_qa/abnahme-tor/alt/` zusammengesetzt (Port 9187).

## Schnelle Fassung (seit 31.10.2026): `lauf-schnell.sh`, `tor-schnell.js`

**Warum.** Gemessen am Culinarium-Bestand (31.10.): Das alte Tor brauchte je Zustand rund 13 s, davon **0,3 s Messen** und 12 s Warten:
frischer Browser und Nachspielen des ganzen Klickwegs für jeden Zustand (4,2 s Laden + 7–9 s Weg), dazu bei jedem Schritt bis 2,5 s Warten auf
Einblend-Animationen. Die Plakatwerkstatt (464 Zustände) brauchte so 305 min allein für 1440 px, die Stichproben in anderen Breiten noch einmal 14–16 s je Zustand.
Ein Volllauf aller Werkzeuge waren Tage; in der Cloud 5.538 Rechner-Minuten.

**Was anders ist** (gleiche Messfunktionen `messen.js` und `seite.js`, gleiche Kriterien, gleiche Ausgabe für `auswertung.py`):
1. Ein Browser bleibt offen. Jeder Zustand wird an Ort und Stelle erkundet und wieder zurückgenommen (Escape bei Fenstern, Zurück bei Adresswechsel,
   Reiter erneut anklicken). Zum nächsten Zustand geht es über den gemeinsamen Vorfahren, nicht von vorn. Nur wenn der Rückweg nicht ankommt,
   wird der Weg einmal frisch nachgespielt (steht als `zaehler.nachgespielt` im Inventar).
2. Während der Messung sind Einblend-Animationen aus (`reducedMotion` + Stil mit 1-ms-Dauer). Gewartet wird auf Netz und DOM (150 ms Ruhe), nicht auf feste Fristen.
   Bewegung (Kriterien 34, 37) misst wie bisher `bewegung-tor.js` mit Bewegung.
3. **Jeder Zustand in jeder Breite**: 1440, 1280, 1000 (Roberts Safari) und 390 im selben Fenster durch Grössenwechsel, nicht mehr nur Stichproben.
   Am Handy zusätzlich «Menü offen» in Start- und Navigationszuständen. Ausgabe: `inventar.json` + `bilder/` (1440), `stich-<W>.json` + `stich-<W>/` je weitere Breite.
4. Gleiche Layouts werden erkannt (`skelett`: Gerüst der sichtbaren Elemente ohne Text; `gleichWie`, wenn Gerüst und Fundmenge gleich sind). Gemessen wird trotzdem
   jeder Zustand, denn gleiches Gerüst heisst nicht gleiche Funde (Fotos derselben Sammlung haben verschiedene Seitenverhältnisse). Die Tafel zeigt es in der Zeile.
5. Gleichartige Stücke ohne Dokument: die ersten drei und dazu das mit dem längsten und dem kürzesten Text.

**Aufruf**
```
./lauf-schnell.sh <haus> <lauf-name> [P=3] [k1 k2 …]       # alles: Tore je Werkzeug (P gleichzeitig), Bewegung, Dokumente, Auswertung, Messwerte
./lauf-schnell.sh culinarium 0111-werkbank 1 werkbank      # ein Werkzeug gleich nach dem Bau
node tor-schnell.js ziele-<haus>.json <ausgabe> --nur <k> [--breiten 1440,1280,1000,390] [--max 700] [--tiefe 4]
python3 vergleich.py <lauf-alt> <lauf-neu> [k …]            # findet der neue Lauf jede Fundstelle des alten? (Art + Stelle + Meldung, alle Breiten)
python3 zeiten.py <lauf>                                    # Zustände, Minuten, Sekunden je Zustand, Rückwege je Werkzeug
```
Tafel: `http://localhost:8978/haus/_Oberchef/zeigen/<haus>/abnahme-tor/<lauf-name>/index.html`. Speicher: ein WebKit 400–800 MB, P=3 ist auf dem 24-GB-Mac sicher.
`TOR_BEWEGUNG=1` lässt die Animationen an (nur zum Vergleich). `TOR_HAENGER_MIN`, `TOR_KLICK_MIN` wie beim alten Tor.

**Gemessen am Culinarium (31.10.2026, gleicher Stand, altes gegen neues Tor):** siehe unten «Messwerte».
