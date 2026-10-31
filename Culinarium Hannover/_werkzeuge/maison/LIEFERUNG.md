---
tags: [projekt, website]
status: aktiv
---

# Der Tresen (Zentrale, Arbeitsname La Maison) · Culinarium Hannover · Lieferung 28.10.2026

Status: fertig (lokal), Chat `culinarium-maison`. Nichts online, nichts verschickt.

**Links** (nur localhost, Regel Robert 28.10.2026; alle mit curl auf 200 geprüft)
- Der Tresen (Zentrale): http://localhost:9081/_werkzeuge/maison/ (Prüfserver `python3 _werkzeuge/maison/server.py 9081`)
- Gemeinsamer Rahmen, Musterseite: http://localhost:9081/assets/oberflaeche/muster.html?haus=culinarium · Anleitung http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/oberflaeche/UMSTELLUNG.md
- Diese Lieferung: http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/maison/LIEFERUNG.md · Funktionsliste http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/maison/FUNKTIONSLISTE.md · Fehlerbuch http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/maison/pruefung/FEHLERBUCH.md
- Namenstafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/namen-tafel.png
- Bilder: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/maison/maison-1440.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/maison/maison-390.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/maison/maison-1440-ganz.png

## Was steht

1. **Gemeinsamer Rahmen `_werkzeuge/oberflaeche/`** (einziger Schreiber dieser Chat): Stamm wie Schäfli (`grund.css`, `rahmen-buehne.css`, `oberflaeche.js`, `muster.html`), Kleid Culinarium `kleid/culinarium.{js,css}` mit Werten der gebauten Website (Nacht #16151A, Strasse #1C1B21, Schiefer #3A3845, Warmweiss #FAF4F4, Kerze #EF7649/#F5A689/#B15736, Dirty Chicken #8953A9 nur über `.wo-dc`), Fraunces SOFT, Instrument Sans, Urbanist, DM Mono, nie fett, nie kursiv; Zeichen = das «C» der nachgezogenen Wortmarke (`kleid/culinarium-zeichen.svg`, unverändert aus `marke.svg #wm`); Ornament = das «x» von «Momo x Rudi». Namen an einer Stelle (`WO_HAUS.namen`, Arbeitsnamen bis zur Wahl), Wege lokal je Port auf 127.0.0.1. Alle sechs Werkzeuge haben ihn eingebunden (Bildschirme).
2. **Zentrale «Die Plakatwand»**: Kopf mit Wortmarke, «Der Tresen», Gruss, Datum, Zahlenzeile «Heute … Besuch(e) · … zum Platz»; links die Bühne (in Ruhe die Fenster der Bar am Abend, beim Darüberfahren die echte Vorschau des Werkzeugs), rechts sechs Plakate mit Fotos der Abende, je mit einer Abendfarbe der echten Plakate (`marke.json → abendfarben`), Stand live aus jedem Werkzeug. Darunter je Werkzeug ein Saal mit echtem Bildschirm (9 Bildschirme), Tafel «So geht’s» mit den echten Knopf-Namen (gegen den Code geprüft), Stücke (3 Menükarten aus La Carte, 3 Drucksachen aus L’Imprimerie, 6 Fotos im Saal Le Livre, 12 Hausfarben in einer Reihe), Weg zum Platz mit den Stufen von Le Registre, Fuss mit allen sechs Anleitungen.
3. Bau: `python3 _werkzeuge/maison/bau.py` (lokal + `online/`, Fassung aus dem Inhalt, bricht bei fremden Hausangaben ab). Bildschirme neu: `node _werkzeuge/maison/schirme.js [werkzeug]` (WebKit, nur GET), dann `bau.py`.
4. Funktionsliste R01–R24 / M01–M27: `FUNKTIONSLISTE.md`; Fehlerbuch Zeile für Zeile: `pruefung/FEHLERBUCH.md`.

## Wie geprüft

- `pruefung/pruefe.js`: Chromium **80 grün / 0 rot**, WebKit **80 grün / 0 rot** (1440 × 900 und 390 × 844; Laden, Konsole leer, keine kaputten Bilder, kein Überlaufen, erstes Bild ganz, Leiste, Gruss, Vorschau je Zeile per Zeiger und Tastatur, nichts hüpft, Tasten 1–6, Laufband, Weniger Bewegung, Startfehler-Tür, ohne Antwort Satz ohne Zahl).
- `pruefung/democheck.js`: Chromium **151 grün / 0 rot**, WebKit **151 grün / 0 rot**: jede Kachel und jeder Link geöffnet (200), aus allen sechs Werkzeugen zurück in den Tresen mit Zahlen, Weg zum Platz ohne Anteil über 100 %, Werkbank → Tresen → «Zur Werkbank» zurück.
- Zwischenbreiten 320–1600 (`pruefung/breiten-webkit.txt`): kein seitliches Verrutschen.
- Flüssigkeit (`pruefung/fluss-ergebnis.txt`, Chromium gedrosselt): 1440 4× p50 8,3 / p95 9,2 ms, 6× p95 9,2 ms; 390 4× p95 9,2 ms, 6× p95 9,3 ms; CLS 0,004–0,005; ein langes Bild 308 ms bei 4× beim ersten Dekodieren der Bildschirme (6×: 42 ms). Nur transform/opacity.
- Speichern → neu laden: betrifft die Zentrale nicht (speichert nichts ausser dem Rundgang-Merker).

## Offen, mit Grund

- ~~Namen~~ **gewählt (Robert 28.10.2026, Satz A):** Der Tresen · Das Schaufenster · Die Pairing-Karte · Das Gästebuch · Das Markenbuch · Die Besucherliste · Die Plakatwerkstatt; eingetragen in `kleid/culinarium.js`, den sechs Werkzeugen und der Werkbank gemeldet. Alle neun Bildschirme mit den neuen Namen neu aufgenommen (28.10.2026), Tresen neu gebaut.
- ~~Werkbank → Tresen → «Zur Werkbank»~~ erledigt: die Werkbank verlinkt den Tresen mit Herkunft, Demo-Check grün.
- ~~Zur Entscheidung~~ **entschieden (Oberchef 28.10.2026):** das Kleid folgt der gebauten Website (Kerze #EF7649, Nacht #16151A, Instrument Sans im Fliesstext), sie ist Roberts abgenommener Stand; `CHARAKTER.md` ist dort veraltet.
- **Neu entschieden (Robert 28.10.2026, über Oberchef, sein letztes Wort):** je Anfrage drei bis fünf ganz neue Plakate im Stil von Rudis Plakaten. Tafel «So geht’s» der Plakatwerkstatt darauf umgestellt («Abend beschreiben» → «Vorschläge anlegen» → «Diesen bearbeiten» → «Druckfertig speichern», «Plakat-Motive»; alle im Code gefunden), Beispiel-Plakat bleibt Rudis «Goldener Herbst». Bildschirm der Plakatwerkstatt neu aufgenommen (Seitenleiste «Abend beschreiben», «Plakat-Motive»), pruefe Chromium/WebKit je 80/0. Vorheriger Stand:
- ~~KI-Erzeugung raus (Robert 28.10.2026, über Oberchef):~~ Tafel «So geht’s» der Plakatwerkstatt neu (Abend und Illustration · Im Editor fertig machen · Drucken), das KI-Plakat aus dem Saal genommen (gesichert in `_sicherung/vor-ki-raus-2026-10-28/`), Menükarte und Beitrag bleiben. Nach «fertig» der Plakatwerkstatt: Tafel mit ihren echten Knopf-Namen («Neues Plakat», «Illustration wählen», «Diese nehmen», «Plakat-Motive», «Vorderseite», «Rückseite», «Druckfertig speichern», alle im Code gefunden), Bildschirm neu, Plakat des Abends mit Rudis Illustration «Goldener Herbst»; pruefe Chromium/WebKit je 80/0, democheck je 151/0 (erster Lauf je 1 rot «Werkbank hat Weg zur Zentrale», zweiter Lauf grün; der Link steht fest in der Werkbank).
- **Laden nachgebessert (29.10.2026, Gegenprobe Oberchef):** Fensterfotos auf den sichtbaren Streifen zugeschnitten, srcset 600/900 px, am Handy eigenes Band; Stile vor den Fotos, Fotos vorgeladen mit Vorrang; Fenster sofort da, Foto blendet ein (onload), Schweben 0,8 s gestaffelt bis 1,2 s, wartet auf nichts; Fraunces und Instrument Sans mit swap und Ersatz. Gemessen (1440, Retina): ungedrosselt alle Fotos sichtbar nach 0,29 s WebKit / 0,38 s Chromium, gedrosselt (1,6 Mbit/s, 150 ms, CPU 4×) nach 2,35–2,43 s. Markenbuch jetzt Momo vor der Bar (das Shaker-Foto war gedrosselt zu schwer). pruefe 80/0 und democheck 151/0 in beiden Kernen.
- **Empfang neu wie beim Rivage (29.10.2026, Robert: «kannst du das machen wie beim Rivage?»):** fünf hohe Fenster über den ganzen Schirm (Bar bei Nacht, Rudi am Tisch, gedeckte Tafel, Anstossen, Momo an der Bar), unten je Bereich, Name, Stand live, runder Knopf; darüber in der Mitte Wortmarke · Bar · Ort, «Der Tresen» gross, Gruss, Datum, Zahlenzeile der Besucherliste (Taste 6). Fotos vorgeladen mit Vorrang, Platzhalter in der Motivfarbe. pruefe.js und democheck.js auf den neuen Empfang umgestellt: pruefe Chromium 80/0, WebKit 80/0 (ein Lauf vorher 79/1 «Taste 1», bei Wiederholung zweimal grün), democheck je 151/0; WebKit 1440/1280/390 ohne Überlauf; gedrosselt (1,6 Mbit/s, CPU 4×) erster Schirm nach 4,4 s. Vergleich: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/tresen-hero-2910/rivage.html · Sicherung `*.vor-hero-rivage-2026-10-29`.
- **Kopf neu (29.10.2026, Robert: «der header sieht scheiße aus»):** Wortmarke · Bar · Ort in einer Zeile über «Der Tresen»; rechts Datum, Gruss, Kennzahlen als Block auf der Grundlinie des Titels; keine «x», Trenner «·», Linie schlicht; «Besuchszahlen als Beispiel» leise in der Datumszeile. Nur im Tresen (kein anderes Werkzeug hat diesen Kopf). WebKit 1440/1280/390 (dazu 1000/700/320) ohne Überlauf; pruefe Chromium/WebKit je 80/0, democheck WebKit 151/0. Vorher/nachher: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/tresen-kopf-2910/index.html
- Ändert ein Werkzeug sichtbar etwas: `node schirme.js <werkzeug>` und `bau.py`.
- Sicherheit (`_wache.py`), Online-Fassung hochladen: nicht Teil dieses Auftrags.

## Nachtrag 30.10.2026 (Bewegung, Rundgang)
- Titel des Empfangs und der Säle steigen Zeile für Zeile (`quelle/maison.js` teilt sie, `quelle/maison.css`), die Fotos der fünf Fenster zoomen beim Laden ein, die Wegstufen der Besucherliste steigen gestaffelt (`bau.py`, `data-r` am `.m-weg`), alle Zahlen aus den Werkzeugen laufen beim Ankommen hoch.
- Rundgang neu an den Empfang angepasst (`bau.py`, `rundgang()`): Schritt 1 Titel, 2 «Ein Fenster je Werkzeug», 3 «Heute auf der Website» (Zahlenzeile), 4 Leiste, 5 erster Saal. Vorher beschrieb Schritt 3 das grosse Bild des alten Empfangs.
- Geprüft: `pruefung/pruefe.js` 80/0 und `pruefung/democheck.js` 153/0 in WebKit und Chromium; neu `pruefung/rundgang-check.js` (?rundgang, 1440/1000/390, Weiter, ←/→/Enter, Überspringen, Escape, Ende, danach frei bedienbar) 81/0 in beiden; Bewegungs-Tor ohne Fund, 4× gedrosselt 1 von 1073 Bildern über 50 ms.
- Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/tresen-3010/index.html · Tresen: http://localhost:9081/_werkzeuge/maison/
- Sicherungen `*.vor-bewegung2-2026-10-30`, `bau.py.vor-rundgang-2026-10-30`.
