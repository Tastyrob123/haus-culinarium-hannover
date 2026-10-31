---
tags: [projekt, website]
status: entwurf
---

# Die Plakatwerkstatt (L’Imprimerie) · Culinarium Hannover · Lieferung

**Stand:** liegt vor, 28.10.2026 (Chat «culinarium-imprimerie», gemeinsamer Auftrag `_werkzeuge/AUFTRAG-GEMEINSAM.md`). Lokal, nichts hochgeladen, nichts verschickt, keine KI aufgerufen. Bauer ist nie Prüfer: die Abnahme nach Werkzeug-Master Abschnitt 8 macht ein neuer Chat.

## Wo

- **Werkzeug:** http://localhost:9087/_werkzeuge/imprimerie/ · Server starten im Projektordner: `python3 _werkzeuge/imprimerie/serve.py 9087`
- **Prüfseite:** http://localhost:9087/_werkzeuge/imprimerie/pruefung.html · **Newsletter-Baukasten:** http://localhost:9087/_werkzeuge/imprimerie/mail.html · **Anleitung (Demo-Video):** http://localhost:9087/_werkzeuge/imprimerie/hilfe/index.html
- **Diese Lieferung:** http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/imprimerie/LIEFERUNG.md · **Funktionsliste:** http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/imprimerie/FUNKTIONSLISTE.md
- **Für die Zentrale (M17):** Stand-Weg `/_werkzeuge/imprimerie/haeuser/culinarium/vorlagen/index.json` (67 Vorlagen in 12 Arten). Für Aufnahmen ohne Begrüssung `localStorage['ds-culinarium-willkommen'] = '1'`.
- **Name:** «Die Plakatwerkstatt» (Robert, Satz A, aus `_werkzeuge/oberflaeche/kleid/culinarium.js → WO_HAUS.namen`, der einen Stelle), Wege «Der Tresen», «Das Plakatarchiv». Tausch = Zeile im Kleid, dann `python3 _qa/culinarium_anpassen.py`. Dateien und Adressen bleiben `imprimerie`.
- **Revier:** nur `_werkzeuge/imprimerie/`. Gelesen, nicht geschrieben: `_werkzeuge/oberflaeche/` (culinarium-maison), `_werkzeuge/livre/livre.json` (Plakatarchiv), `_werkzeuge/maison/zur-werkbank.js`, `website/` (Farben, Schriften, Zeichen, Fotos, `bau.py` ABENDE/ZEILEN/BILD, `abende_info.py` KARTEN, `assets/buchen.js` Beispieltermine), `_quelle/` (Plakate, Rudis Original-Logo, Beiträge), Taverne zum Schäfli (Vorbild).

## Was gebaut ist

Kopie der Werkstatt der Taverne zum Schäfli (Kern Carlton → Rivage, alle Korrekturen I01–I18, Demo-Checks Schlössli und Schäfli), angezogen mit dem Kleid des Culinarium aus der gebauten Website: Nacht `#16151A`, Schiefer `#3A3845`, Warmweiss `#FAF4F4`, Kerze `#EF7649`; Fraunces 340 SOFT 100 für Titel, Instrument Sans für Lesetext, DM Mono für Zahlen, Urbanist 600 nur für die Zeilen der Plakate (wie `.tb-t-zeile`/`.fk-zeile` der Website); alle als feste TrueType-Schnitte (kein Type 3 im PDF). Zeichen: das «C» der Wortmarke; Wortmarke: Rudis Original (`_quelle/logo/original/`, wie die Website seit 28.10.). Dirty Chicken nur in eigenen Stücken, in seinem Violett `#8953A9` mit dem D mit Hühnerfuss. Alles wiederholbar, nichts von Hand in den Kerndateien:

```
python3 bau.py                        Marke, feste Schnitte, Zeichen (C, Wortmarke, D), Tapete, 172 Fotos + 13 Plakat-Illustrationen, Akzentfarbe je Abend
python3 _qa/wissen_bau.py             Wissen: Beiträge, Fakten, Abende, Menükarten, Beispieltermine, Wortlaut der Plakate, 10 Seiten der Website
python3 _qa/vorlagen_culinarium.py    67 Vorlagen, katalog.js, Beispiele, sechs Mails (bricht ab bei jedem nicht belegten Satz, jeder Zahl, jedem fremden Haus)
node _qa/mail_marken.js               Kopf (Wortmarke + Zeile), Fuss, Trenner der Mails als Bild
python3 _qa/culinarium_anpassen.py    Kern aus _qa/carlton-vorlage/ ins Kleid des Culinarium, Namen aus dem Kleid, Aufbauten aus _qa/plakat.js.txt
python3 _qa/qa_culinarium.py          Prüfskripte aufs Haus umstellen (Schwellen des Hauses, Namen aus dem Kleid)
zsh _qa/kette_voll.sh                 PDF aller Vorlagen, Prüfkette, Kopfbreiten, Oberfläche, Kontrast, Flüssigkeit, Filme
```

**Hauptsache: das Plakat je Abend in der Sprache der echten Plakate.** Drei neue Aufbauten (`_qa/plakat.js.txt`), ausgemessen an den Plakaten seit 2023 (`_quelle/extern/ig/`):
- **«Plakat des Abends» (vorn):** warmweisser Rand, Bildfeld oben, darunter die Wortmarke CULINARIUM im Kasten mit feiner grauer Linie und das Band «A UNiQUE EXPERiENCE BY MOMO X RUDI» (wie damals auch «BY MOMO X CHRISTOPH», «BY MOMO»). Das Band steht nur auf den Plakaten, so wie auf Rudis echten Plakaten; auf Menükarten, Beiträgen und allem anderen nie. Über dem Bild «WALK ON THE WILD SIDE», darunter eine Linie in der Akzentfarbe des Abends.
- **«Plakat, Rückseite mit Daten»:** Bild randlos, oben links «WALK / ON THE / WILD SIDE», unten «27 / 11 / 26 · 19:00 UHR», «28 / 11 / 26 · 17:00 UHR», daneben «3 GÄNGE MENÜ / 5 SiGNATURE DRiNKS», Linie in der Akzentfarbe.
- **«Menükarte am Tisch»:** Wortmarke, Zeile, «Menü», Datum, je Gang Teller und Drink, so wie die Website die Karten der Abende zeigt.
- Formate: Instagram 1:1 (wie die Plakate), A3 zum Aushang, Story; jedes Format setzt dieselben Inhalte neu.

**Vorlagen: 67 in 12 Arten, jeder Satz belegt**
- **Plakate je Abend (14):** jedes der 13 Plakate seit September 2023 im Rahmen des Hauses (Illustration aus dem echten Plakat ausgeschnitten, Zeile und Akzentfarbe des Abends) und ein Beitrag «Jeder Abend hat sein Plakat».
- **Die nächsten Abende (Anlässe & Events):** die Beispieltermine der Website (`buchen.js`: Fr 27./Sa 28. November und Fr 18./Sa 19. Dezember 2026, Vorschau) mit je acht Motiven: Plakat vorn und hinten, Rückseite allein, A3-Aushang, Story, Menükarte am Tisch, Ankündigung mit Zeiten und Preis (89,00 EUR, Website), Flyer, «Ausgebucht». Farbe je Abend aus den Terminplakaten der Website. Dazu Dirty Chicken als Pop-up (Flyer mit eigener Rückseite, Beitrag, Story, in Violett).
- **Menükarten am Tisch (11):** die fünf ganz lesbaren Karten der Abende (`abende_info.py KARTEN`, Gang · Teller · Drink, wörtlich), Rudis vier Zeilen als Tischaufsteller mit dem Foto genau dieses Tellers, «Rudis Zeilen», «Das Menü ändert sich mit jedem Abend».
- **Drinks & Techniken (6), An der Tafel (7), Das Haus (4), Hinweise im Haus (6), Newsletter-Bilder (6), sechs versendbare Mails** (Der nächste Abend, Warteliste: Platz frei, Rückblick, Einladung an Stammgäste, Dein Platz an der Tafel, Danke). Kein `mailto`, kein Telefon: das Culinarium hat keine Nummer und keine Mailadresse (fakten.json «offen»), alle Knöpfe führen zum Instagram-Konto.
- **Bewusst nicht drin:** Gutscheine (das Haus bietet keine an), Zimmer-, Hotel- und Housekeeping-Stücke, Ansichtskarten, Visitenkarten, Plakate anderer Abende der Bar, «vegetarisch» als Merkmal (nur wörtlich auf alten Karten), Preise ausser dem Preis des Abends aus der Website.

## Behoben beim Bauen (über die Skripte, wiederholbar)

- **Gesperrte Versalien zerfielen im PDF** («H A A S E M A N N …»): der Kern setzt Mono-Zeilen mit .22 em; jetzt höchstens .08 em in jeder Rolle, Fusszeile und «Versalien gesperrt». 0 zerfallene Wörter in allen 67 PDFs. Steckt im Kern jeder L’Imprimerie, **in Master 10a eingetragen**.
- «WALK ON THE WILD SIDE» in der Akzentfarbe war auf Fotos bei Nacht kaum lesbar (grüner Dezember-Abend): jetzt warmweiss, die Farbe des Abends als Linie darunter.
- Dirty Chicken stand in Nacht mit dem «C»: eigener Ton «Violett» mit dem D (`zeichen3`), eigene Rückseite.
- Abteilungen: «Dirty Chicken» stand allein in der letzten Reihe des Mosaiks; jetzt fünf Abteilungen (eine grosse, vier kleine), Dirty Chicken als Anlass; Liste der Abteilungen mit mittiger letzter Reihe.
- Newsletter-Baukasten lud die Schriften des Vorbilds (404); Probe-Antworten der KI-Prüfung und der Markenprüfung stammten aus einem anderen Haus («Wildabend»): ersetzt durch echte Probe-Antworten dieses Servers.
- Schwellen der Prüfskripte auf die Zahlen des Hauses (6 Hinweise, 5 Abteilungen, 19 Arten), Fehlerbuch-Regel «Schwellen gelten fürs Haus».

## Selbst geprüft (28.10.2026, unsichtbar, Prüfserver :9087, ohne KI)

Logs `_qa/lauf/`, Belege `pruefung/` (Bilder `pruefung/bilder/`, Drucksachen `pruefung/drucksachen/`, Sicherheit `pruefung/sicherheit.txt`).

| Lauf | Chromium | Safari-Kern |
|---|---|---|
| PDF jeder Vorlage über «Druckfertig speichern» | 67 von 67 ohne Befund, 0 Konsolenfehler, 9 Formate, alle Schriften CID TrueType (kein Type 3), 0 Masken, 0 Verläufe, 0 zerfallene Wörter; jede Seite als Tafel angesehen | – |
| Funktionsliste 1440 × 900 | 106 / 106 | 106 / 106 |
| Funktionsliste 390 × 844 | 103 / 105 | 103 / 105 |
| Rahmen (R03, R04, R07, R09, R15, R17, R19, R23) | 8 / 8 | 8 / 8 |
| Sonderfälle (zwei Fenster, 5'000 Zeichen, `<script>`, Emoji, Foto 30 MB / 400 px, Datei ohne Bild, kaputte Arbeitsdatei, Netz weg, leeres Guthaben) | 22 / 22 | 22 / 22 |
| KI-Probe (ohne KI) · Markenprüfung-Probe | 8 / 8 · 5 / 5 | 8 / 8 · 5 / 5 |
| Zahlen und Reste anderer Häuser | 29 grün, 0 rot | 29 grün, 0 rot |
| Echte Maus 1440 / 390 | 37 / 37 · 37 / 37 | 37 / 37 · 37 / 37 |
| Kopf 920/1000/1100/1240, kein roher Code | grün | grün |
| Oberfläche «Die Bühne» 1440, 390, 320 | 22 / 22 (beide Kerne) | |
| Titel auf dunklen Flächen | keiner unter 3:1 | keiner unter 3:1 |
| Mails (sechs, Bilder da, kein `mailto`) | 7 / 7 | – |

Die zwei offenen Zeilen am Handy sind dieselben wie in allen Häusern und gewollt: «eine grosse, drei Querkarten» und «Mosaik» stehen am Handy untereinander. KI-Probe und Maus 390 in Chromium waren im Kettenlauf unter Rechnerlast einmal rot (Zeitüberschreitung), im Einzellauf grün.

**Sicherheit** (curl gegen :9087): fremde Herkunft 403, kein JSON 415, 70 KB 413, Haus `../gbr` 400, Probe-Entwurf 200; `serve.py`, `bau.py`, `_qa/…`, `api/…`, `.env.local`, `LIEFERUNG.md`, `../../website/bau.py`, Ausbruch über `/assets/bild/..%2f..` je 404. Grenze 40 Entwürfe je Stunde wie im Kern (nicht ausgelöst, sonst sperrt sie die Prüfläufe eine Stunde).

**Flüssigkeit (Regel 55), Chromium unsichtbar, unter Rechnerlast (elf Chats parallel):**

| | Median | 95 % | längstes | über 50 ms |
|---|---|---|---|---|
| Galerie aller Vorlagen, schnell scrollen, 4× | 8,3 ms | 9,2 ms | 33 ms | 0 von 660 |
| dasselbe, 6× | 8,3 ms | 9,3 ms | 43 ms | 0 von 634 |
| Editor, Titel ziehen mit Einrasten, 4× / 6× | 8,3 ms | 9,2 ms | 41 / 50 ms | 0 / 1 |
| Editor, Rückgängig, 4× / 6× | 8,3 ms | 9,3 ms | 16 / 17 ms | 0 |

**Anleitung:** neun Kurzfilme der Führung und Demo-Video (79 s, vier Kapitel) am Culinarium aufgenommen, Probe ohne KI, Name aus dem Kleid (`hilfe/`).

## Fehlerbuch 10a, Zeile für Zeile gegen dieses Werkzeug

| Zeile (Regel) | Stand hier |
|---|---|
| Sperrung höchstens .08 em, PDF mit `pdftotext` prüfen | neu eingetragen (28.10.), hier umgesetzt, 0 zerfallene Wörter |
| Feste Schnitte statt variabler Schriften, kein Type 3 | 6 TrueType-Schnitte aus den Schriften der Website, `pdffonts` nur CID TrueType |
| Beispielwerte statt Klammern | keine Klammer in den Vorlagen; erfundene Namen (Lena Brandt …), Daten = Beispieltermine der Website |
| Roher Code ({…}, undefined, NaN, None) nirgends | `kopfbreite.js` in allen Ansichten grün |
| Bilder in jeder Liste, keine Karte allein, letzte Reihe mittig | Anlässe, Abteilungen, Newsletter mit Foto; 5 Abteilungen im Mosaik ohne Lücke; Liste mittig |
| Titel auf dunklem Grund hell; dunkle Flächen nur in den Tönen des Kleids | `kontrast.js` keiner unter 3:1; Hausschicht nimmt `--wo-nacht`/`--wo-nacht2` |
| Werkzeug-Bilder ohne Begrüssung | Merker `ds-culinarium-willkommen`, alle Bilder ohne Fenster davor |
| Kopf 920–1240: Titel nie über einem Knopf | grün |
| Wege zwischen Werkzeugen 127.0.0.1 / Port aus dem Kleid; «Zur Werkbank» mit `data-ueber` | Tresen :9081, Plakatarchiv :9085, Website :8765 |
| Kein mailto, Kontakt als Text | auch im Mail-Baukasten entfernt; keine Telefonnummer des Hauses vorhanden |
| Hausname mit Artikel («das Culinarium» → «des Culinarium»), nie fest «der …» | Grammatik-Prüfung im Anpass-Lauf grün |
| Fotos nur, die das Werkzeug zeigen darf | Plakate anderer Abende der Bar, Logo als Foto, Plakatwand raus; Plakatarchiv gefiltert (I18) |
| Schwellen gelten fürs Haus | Prüfseite ab 60 Vorlagen, Prüfskripte auf 5/6/19 |
| Filme je Haus, nie fremde | neun Kurzfilme + Demo am Culinarium |
| Rundgang-Schild / «Wer arbeitet hier?» / Leiste unten / Karten-PDF-Zeilen | betrifft dieses Werkzeug nicht (eigene Führung, keine Namensabfrage, kein Veröffentlichen, Preise nur wie auf der Website) |


## Stand 28.10.2026 nachts: «Abend beschreiben» mit neuen Konzepten, «Plakat-Motive» mit Rudis Originalen

Roberts letztes Wort (direkt, 28.10.): «ich will pro Anfrage 3 4 oder 5 (je nachdem was ausgewählt war) an neuen» und (über den Oberchef) «die vorlagen die wir haben nehmen wir als grundlage zum verständnis aber entwickeln auf der grundlage komplett neue und weitergedachte konzepte … korridor / rahmen sind die bisherigen posts». Davor galt kurz «KI-Erzeugung raus» und vorher «die sehen alle zu sehr nach KI aus». Alle Zwischenstände sind gesichert: `_qa/sicherung/vor-ki-raus-2026-10-28/`, `_qa/sicherung/vor-ki-zurueck-2026-10-28/`. Die KI-Bilder des Tages (Sammlung, Stiltest) liegen in `_archiv-ki-2810/` und werden nicht ausgeliefert (404).

- **Abend beschreiben** (http://localhost:9087/_werkzeuge/imprimerie/): Thema, Gastkoch, Konzept (Gerichte, Drinks), Wochenende, 3 / 4 / 5 Vorschläge. Je Anfrage entstehen genau so viele **neue** Plakate, vorn und hinten:
  1. **Konzept je Vorschlag** (`api/konzept.py`): eine eigene Bildidee aus Thema, Gerichten, Drinks und Gastkoch. Die Ideen einer Anfrage unterscheiden sich in Bildwitz, Figur und Farbwelt. Keine wiederholt eines der 13 echten Plakate (`BESTAND`). Mit Claude Haiku 5.5, sobald der Schlüssel in `~/.config/tasty/anthropic.env` liegt; sonst als Probe nach Regeln. Die Karte zeigt die Idee in einer Zeile über dem Plakat.
  2. **Bild aus Konzept und Stilblatt** (`stil/stilgrundlagen.md`, Kurzform `STIL_EN`). Rudis Plakate gehen nicht als Bildvorlage mit (`STILREFERENZ = False`). Die Rückseite ist ein eigenes Begleitbild zum selben Konzept. Über Higgsfield, sobald der Schlüssel in `~/.config/tasty/higgsfield.env` liegt.
  3. **Prüfung je Bild** (`_qa/kopfzone.py`): Kopfzone frei, Kontrast 4,5:1, klar andere Farbwelt als die übrigen Vorschläge (Abstand ≥ 15), nicht zu nah an einem der 13 Originale (`naehe` < 0,40). Sonst wird einmal neu erzeugt.
  4. **Ohne Bildschlüssel:** Die neuen Konzepte stehen da, mit dem Satz, dass das Bild mit dem Schlüssel entsteht. **Nie vorhandene Motive als Ersatz.**
  5. **Grenzen** (`api/plakat.py GRENZEN`): 3 Durchgänge je Gerät und Tag, 40 Bilder am Tag. `PLAKAT_KI=0` schaltet ab.
  6. **Gespeichert und sofort da:** Roberts Sommerabend und Herbstabend (`_qa/abend-roh/abende.json`, noch im ersten Stil; werden neu erzeugt, sobald der Schlüssel liegt).
- **Plakat-Motive:** nur Rudis 13 Illustrationen, jede ganz. Steht «WALK ON THE WILD SIDE» schon im Bild, setzt die Werkstatt keine zweite Kopfzeile. Die Rückseite ist ein ruhiger, satter Grund in der Farbwelt der Illustration (`bau.py rueckfarbe`). Die letzte Reihe steht mittig, ohne Loch.
- **Plakate der Anlässe und Tresen-Bilder** (`_werkzeuge/maison/roh/druck/`) kommen aus Rudis Illustrationen (Tresen: «Goldener Herbst»).
- **Archiv der Plakate:** jedes echte Plakat ganz, vorne und hinten (`plakatganz`).
- **Plakat-Stil:** Kopfzeile Urbanist 800 mit Luft zum Rand, Bandzeile fett ohne Umbruch, Rückseite im Satz der echten (kleines i, keine Linie, kein Schleier).
- **Gestaltungs-Funde** (culinarium-gestaltung, drei Runden) behoben: Etiketten, rechte Spalte, Beispiele einmal gekennzeichnet, Fotozahl aus dem Plakatarchiv (231), Kachel ohne angeschnittenes Plakat, «Zuletzt bearbeitet» ohne Restreihe, Suchfeld am Handy, Dirty Chicken mit Opening 30. Mai 2026, Sammlung ohne Restreihe.
- **Higgsfield heute:** 129 Credits für Versuche (1006,34 → 877,34). Seither nichts mehr.
- **Prüfkette 28.10. nachts** (`_qa/lauf/ende-2810.txt`):
  - Plakat-Lauf Chromium/WebKit 1440/390: je 18/18.
  - PDF 66/66 ohne Fehler, 0 zerfallene Wörter.
  - Funktionen 1440: 106/106; 390: 103/105 (die zwei bekannten Handy-Zeilen).
  - Rahmen 8/8, Sonderfälle 22/22, KI-Probe 8/8, Markenprüfung 5/5, Zahlen 29/0, Maus 37/37 in beiden Kernen.
  - Mails 7/7, Kopfbreite grün, Oberfläche 22/22, Kontrast ohne Titel unter 3:1.
  - Galerie und Editor im Median 8,3 ms, Demo-Film 78,7 s, neun Kurzfilme der Führung neu aufgenommen (`hilfe/schritt-1…9.mp4`).

## Offen, mit Grund

- **Schlüssel:** Higgsfield (Bilder) in `~/.config/tasty/higgsfield.env`, Anthropic (Konzepte) in `~/.config/tasty/anthropic.env`; beide liegen leer bereit (chmod 600). Erst danach der Test mit echtem Auftrag: ob die Higgsfield-API GPT Image 2.5 führt und welches Modell Stil und Inhalt trennt.
- **Online-Anschluss:** `online.json` bereit (Form wie Schäfli), nicht angeschlossen; Online-Adresse des Hauses gibt es noch nicht.
- **Illustrationen der Plakate** liegen nur in Instagram-Grösse (um 1330 px): auf A3 meldet die Druckprüfung zu wenig Auflösung. Für Drucke braucht es die Originaldateien des Gestalters (Rechte an den Illustrationen laut CHARAKTER.md offen).
- **Der nächste Abend** steht noch nicht fest; die Vorlagen nehmen die Beispieltermine der Website. Steht ein echter Termin, in `website/assets/buchen.js` bzw. den Terminen eintragen und `python3 _qa/vorlagen_culinarium.py` + `culinarium_anpassen.py` laufen lassen. Die Menükarte der nächsten Abende zeigt als Beispiel die Karte vom Februar 2025.
- **Plakat März 2026:** die Rückseite schreibt «27 / 03 / 25» (Jahr 25 statt 26), so abgelesen, nicht verwendet.
- **Nach Auftrag:** Firefox, 1366 × 650, echte Geräte, Druck auf Papier, Anmeldung.

## Stand 29.10.2026: alle Vorschläge im Werkzeug
- Robert: «die vorschläge bitte direkt im tool alle anzeigen und nicht auf so ner random ass seite».
- «Abend beschreiben» zeigt unter dem Formular «Alle Vorschläge»: je Abend Überschrift, darunter die Vorschläge vorn und hinten mit Konzeptzeile und «Diesen bearbeiten».
- Quelle: `GET api/plakat` (`plakat.alle()`), ohne Kosten; erste Fassungen erscheinen nicht.
- Prüfung: Plakat-Tests Chromium 1440 und WebKit 390, je 18/18, ohne Konsolenfehler und ohne seitliches Verrutschen.

## Stand 29.10.2026: erster echter Live-Lauf (Auftrag Oberchef)
- Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/imprimerie/live-2910/index.html
- Sommer (Aperol Spritz, gegrillter Pfirsich, Burrata) und Herbst (Wildente, Steinpilze, Riesling), je 3 Vorschläge über den Server wie im Browser: 6 von 6 entstanden, 16 Bilder.
- Modell higgsfield-ai/soul/standard, 3 Credits (0,188 $) je Bild laut estimate; Lauf 48 Credits, Referenztest 3 Credits. Die API führt kein GPT Image (openai/gpt-image-*, seedream, flux, nano-banana, recraft → model_not_found); vorhanden u. a. soul/v2/standard, soul/reference, ideogram/v3.
- image_urls wird angenommen, wirkt aber nicht (Testbild: gerahmtes Bild an einer Wand, Signatur, kein Stil von Rudi). STILREFERENZ bleibt aus.
- Nähe zu den 13 Originalen 0,28–0,40 (Grenze 0,65), Kopfzone überall frei. Konzepte aus der Probe, Anthropic-Schlüssel leer.
- Behoben: Tageszähler verlor Buchungen bei parallelen Vorschlägen (Sperre); nicht gebrauchte Wiederholungen gehen an die Tagesgrenze zurück. Zähler heute korrigiert auf 37 von 40.
- Modelltest 29.10. (Oberchef): http://localhost:8978/haus/_Oberchef/zeigen/culinarium/imprimerie/live-2910/modelle.html
  - soul/reference: Feld laut API-Schema `image_reference_url` (ein Bild), dazu `style_strength`; kopiert die Vorlage fast 1:1 samt Kopfzeile, Nähe 0,56 bleibt unter 0,65 (die Pixel-Messung erkennt Kopien nicht).
  - ideogram/v3 (nur `1k`, unbekannte Felder werden still angenommen): folgt dem Konzept, gemalter Vintage-Stil, blass, mit Signatur. Bestes Modell der API, unter GPT Image 2.5.
  - Im Katalog der Konsole außerdem: ideogram/v4.0 (0,96 Credits), recraft/v4.1/text-to-image (0,56), soul/v2/standard (0,05); nicht getestet. Nichts umgestellt, HF_REFERENZ_FELD nicht eingetragen.
- Modell umgestellt 29.10. (Oberchef): MODELL = recraft/v4.1/text-to-image (Sicherung api/plakat.py.vor-modell-2026-10-29). Felder je Modell in MODELL_FELDER; soul/reference in GESPERRT (bild_erzeugen bricht ab). Signatur-Prüfung schrift() mit einer Wiederholung bleibt im Live-Weg.
  - Abrechnung (GET /models/usage, 1 Credit = 0,0625 $): soul/standard 0,0625 $, soul/reference 0,0625 $, ideogram/v3 0 $, ideogram/v4.0 0,10 $, recraft/v4.1 0,035 $ je Bild. Abgeschickte Aufträge mit Zeitüberschreitung werden trotzdem berechnet.
  - Tageszähler auf den echten Stand 63 gesetzt (laut Abrechnung), Grenze bleibt 40: heute keine Live-Bilder mehr. Hinweis im Werkzeug jetzt «rund 7 Cent» je Vorschlag.
  - Plakat-Tests mit PLAKAT_KI=0: 18/18. Mit Schlüssel und Live-Server schlägt der Test «Ohne Schlüssel» erwartungsgemäss fehl.
- Lauf mit recraft im Werkzeug 29.10. (Oberchef): Tageszähler vorher auf 0 (Tests zählen nicht), Herbstabend «Kürbisrisotto, geschmorte Rinderbacke und Spätburgunder», 3 Vorschläge durch die Oberfläche: 3/3 in 51 s, 8 Bilder = 0,28 $ laut Abrechnung, Nähe 0,26–0,51. Vorschlag 1 Kopfzone nicht frei (keine Kopfzeile gesetzt), Vorschlag 2 Pfauenkopf berührt die Kopfzeile trotz «frei». Tafel: live-2910/index.html#recraft. Zähler danach 8/40.
- 29.10. mittags (Robert): Karten «entsteht» richten sich nach der Höhe des Blattfachs (ragten in breiten Karten über Text). Vorschläge grösser nach Spaltenbreite (vorn bis 400 px, Rückseite 72 % dicht daneben), Plakat-Motive unverändert. Buchung je Vorschlag 2 Bilder statt 4, eine Wiederholung bucht ihr Bild erst bei Bedarf (vorher wurden Vorschlag 3 und 4 abgewiesen, obwohl Bilder frei waren). Roberts Testlauf (2 Plakate) nach _qa/sicherung/robert-test-2910/ verschoben, Tageszähler auf 0. Tests 18/18 WebKit 1440 und Chromium 390.

## Stand 29.10.2026 mittags: Einpassen und Nachprüfung (Oberchef, Punkte 1–5 und 7)
- Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/imprimerie/einpassen-2910/index.html
- 1 Karten-Unterschrift (ms-bureau.css): 19 px, text-wrap balance, Abstände 16/8 px; Hochformate einer Reihe gleich hoch (start.js reihen, --s). Sicherung *.vor-unterschrift-2026-10-29.
- 2 Editor einpassen (studio.js passeZoom, studio.css): Seite mittig, Rand 40 px, kein 320-px-Platzhalter, ResizeObserver passt beim Auf/Zu der rechten Leiste an, Anzeige = echter Massstab. Sicherung *.vor-einpassen-2026-10-29.
- 3 Leiste «Vorlagen» (studio.css): Zeilenraster mit subgrid, Bild/Titel/Text je Reihe bündig.
- 4 Kopfzone (_qa/kopfzone.py): Objektmass statt Spaltenzählung (objekt ≤ 0,04, objekt_hoehe ≤ 0,45); Pfau jetzt belegt, Gegenprobe Soul 6, Beispiele 8, Originale 13 unverändert. Sicherung kopfzone.py.vor-objekt-2026-10-29.
- 5 Druckprüfung (druck.js DS.pruefe, DS.kopfBox): gemalte Kopfzeile angeschnitten = rot; Lage aus motive.json kopf_box/ganz_kopf_box (macOS Vision, _qa/schrift_box, bau.py schreibt sie künftig mit). Heute 70 von 88 Kombinationen angeschnitten (Layout beim Gestaltungs-Chat). API-Weg: Vorderseite 5:4 (VORN_FORMAT), Bildauftrag hält die Figur in der mittleren Hälfte.
- 7 Newsletter (mail.js/css): «Verschickt mit» in zwei Sätzen erklärt, Bearbeiten-Tipp getrennt. Sicherung mail.js.vor-versand-2026-10-29.
- Tests: Plakat 18/18 WebKit 1440 und Chromium 390. Funktionsliste bricht bei «Das Plakatarchiv» ab: Seitenleisten-Punkt «livre» fehlt seit einer Änderung um 12:00 (nicht von hier).

## Stand 29.10.2026 nachmittags: Punkte 8, 11, 12 und Fundliste 01–24 der Gestaltung
- Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/imprimerie/einpassen-2910/index.html (#p8, #p11, #p12, #fund)
- 8 Feld «Etwas anderes für …» wächst mit (start.js passeFeld). 11 «Farben & Schriften» Raster nach Inhalt, Tapete als Band mit Blatt (start.js zeichneMarke, ms-bureau.css). 12 Fuss der Leiste wie die Navigation, Wege als Etiketten (ms-bureau.css).
- Fundliste: 01/02 Leiste, 03 Platzhalter kurz, 04 Rückseiten ohne Wortreste, 05 dunkler Grund unter Kacheln, 06/12 Restreihen mittig, 07/08/13 ausgewogener Umbruch, 09 Konzeptzeilen gleich hoch, 10 Formular volle Breite, 11 Filter an der Chip-Kante, 12 Chips 4+4 und Suchbeispiele, 14 ganze Plakate in Fotokacheln, 15 eine Zahl je Sache («Neue Vorschläge» eigene Gruppe), 16 Farben kurz und einmal, 17 Texte, 18 Name im Kopf zweizeilig, 19 Meldung über der Fussleiste, 21 Reglerwerte, 22 Führung ohne 404, 23 «Culinarium im November/Dezember», 24 digitale Formate ohne Beschnitt.
- Sicherungen *.vor-feld / *.vor-tapete / *.vor-fuss / *.vor-fundliste-2026-10-29. Plakat-Tests 18/18 (WebKit 1440, Chromium 390).
- Offen: Punkt 9 Stilprüfung wartet auf haeuser/culinarium/stilblatt.json.
- 9 Stilprüfung (druck.js DS.stilPruefe, Stilblatt haeuser/culinarium/stilblatt.json): Versalien, Trenner, Rollen, Achse, Zierzeichen, Mindestgrade, Wortmarke, Komposition (Loch/Füllung/optische Mitte zwischen Kopf- und Fusszeile). Schranke in «Fünf Entwürfe» (studio.js entwerfen, bis 3 Runden). 116 Vorlagen: 48 durchgefallen (Liste in der Tafel #p9). Gegenprobe: alt «Vom Pass» und alt «Ausgebucht» fallen durch, neue Story besteht, neue «Vom Pass» verfehlt die optische Mitte knapp (7 % / 6 %).
- Anschlüsse 29.10.: Art «newsletter» in ARTEN, Galerie öffnet im eigenen Format, «anlass» der Bibliothek beim Anlass (Dirty Chicken 12). Prüflauf 326 Kombinationen: Kopfzeile angeschnitten 0. «x»-Regel in der Stilprüfung.
- 14 Du-Anrede in allen Ansichten (Sicherungen *.vor-du-2026-10-29); Gruss tagsüber «Schön, dass du da bist». Achtung: _qa/culinarium_anpassen.py baut den Kern aus _qa/carlton-vorlage neu und würde die Änderungen dieses Tages (aller Chats) überschreiben.
- 29.10. abends: Stilprüfung mit mindestgrade_zweck (Menükarte wie DL) und Achse der Textspalte (fenster/geteilt quer). Prüflauf 329 Kombinationen: 4 rot (Löcher Menükarten September 2023), Kopfzeile 0; eigenes Format 118/119; Gegenprobe vollständig.
- 29.10. abends, Endstand: DS.pruefe über 329 Kombinationen 0 rot (41 mit gelbem Hinweis: Fotos 150–220 dpi, Text nah am Rand, Gutschein-Platzhalter), Stilprüfung eigenes Format 119/119, Kontaktbogen Kopfzeile 0/88, Gegenprobe vollständig.
- 29.10. abends: Kopfzeile wie Rudi (Anton OFL, Rolle kopf, DS.kopfzeileRudi in vorlagen.js, Farbe je Bild kopfzone.rudi_kopf → kopf_rudi, Schatten/Leuchten in satz.js und druck.js). Tafel _Oberchef/zeigen/culinarium/imprimerie/kopfzeile-2910/. Druckprüfung 0 rot.
- 29.10. Abnahme-Tor 1/5/6/7: Probe-Entwürfe (serve.py probe: Text aus nächster Vorlage, Wortstamm + Artnamen, Dirty Chicken immer Ton dc, Beispielnamen), V.plakathoch für Abend-Vorschläge in hohen Formaten (plakat.js), plakatrueck sicherer Rand, Rückbild nur ab 150 dpi. Tafel kopfzeile-2910#tor.

## Formate je Aufbau, Türhänger weg (29.10.2026, Auftrag Oberchef)
- Reiter «Vorlagen» (studio.js `zeichneVorlagen`): zeigt je Format nur Aufbauten, deren `DS.VORLAGEN[k].formate` das Format enthält; ohne Angabe wie bisher. Die Formatliste des Reiters enthält nur Formate, die mindestens ein Aufbau kann.
- druck.js: `DS.formatPasst(k, fk)` und `DS.kombinationen()`; Prüfläufe über alle Kombinationen nehmen nur diese Paare (314 Kombinationen, 0 rot, 3 nicht vorhandene fallen weg).
- `V.plakathoch` hat eigene Liste: a6h, a5h, a4h, a3h, insta, story.
- Türhänger entfernt: Format `tuer` (satz.js), Aufbau `V.tuer` und Beispiel (vorlagen.js), Suchwörter (start.js), Beispiel im Generator (_qa/vorlagen_culinarium.py, _qa/beispiele.json).
- Stempel: satz 44, vorlagen 43, druck 54, studio 64, start 73. Sicherungen `*.vor-formate-2026-10-29`.
- Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/imprimerie/formate-2910/index.html

## Kopfzeile scharf, Plakat hoch fertig (29.10.2026, Auftrag Oberchef und Gestaltung)
- Robert: «ist das unscharf …?» Der weiche Hof ist weg. `DS.kopfTiefe(hex, art, gr)` (satz.js) liefert den harten Schatten (dx .022 gr, dy .04 gr, Schriftfarbe zu 55 % dunkler, ohne Blur) und nur bei «leuchten» einen weiten, schwachen Hof (Blur .5 gr). Bildschirm: text-shadow; PNG: Hof versetzt gezeichnet, Schrift ohne Schatten darüber; PDF: Hof aus 48 schwachen Kopien auf drei Ringen ausserhalb der Kante, dann harter Schatten, dann Schrift.
- Grösse: Rudi (Vision) 80 % Breite / 10,1 % Höhe des Motivs, unsere 81 % / 11 %: unverändert.
- Plakat hoch: Beispiel in DS.BEISPIEL (Kürbis bei Kerzen, freie Kopfzone; auch in _qa/beispiele.json und _qa/vorlagen_culinarium.py), Formate + dlh.
- druck.js: Meldung «füllt nur …» mit einer Nachkommastelle.
- Stempel: satz 46, vorlagen 45, druck 57. Sicherungen `*.vor-kopfscharf-2026-10-29`, `*.vor-plakathoch-2026-10-29`.
- Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/imprimerie/kopfscharf-2910/index.html

## «Alle Vorschläge» schnell (29.10.2026, Auftrag Oberchef; Robert: «brauchen aber ewig zum Laden»)
- Ursache: api/plakat öffnete bei jedem Aufruf alle Vollbilder neu und rechnete die Kopfzonen-Messung (23 s für 8 Vorschläge).
- api/plakat.py `ablegen`: einmal beim Entstehen Vorschau `haeuser/culinarium/vorschau/<key>.webp` (600 px breit, q82) und Motivfarbe; Masse, Farbe und Kopfzonen-Messung im Zwischenspeicher `api/_daten/plakat-vorschau.json`. Die Liste liest nur noch diesen: 4–13 ms.
- serve.py: Vorschauen mit `cache-control: public, max-age=31536000, immutable` (URL trägt ?v=<Stand>), alles andere weiter no-store.
- satz.js: `DS.bildUrl` nimmt für Vorschauen `bildIndex[key].vorschau`; Bilder bekommen `loading`/`fetchPriority` vor src und den Platzhalter in der Motivfarbe. studio.js `miniBox(doc, i, box, o)` reicht das durch.
- plakat.js: Liste wird beim Start geholt (gleichzeitig mit dem Formular), gezeichnet beim Öffnen der Ansicht; erste Reihe eager/high und im Hintergrund vorgeladen, alles darunter lazy. Das volle Bild lädt erst der Editor.
- Stempel: satz 47, studio 65, plakat 22. Sicherungen `*.vor-schnell-2026-10-29`. Server 9087 neu gestartet.

## Galerien ruhig, Menü-Entwürfe, Story, Knopfschrift (29.10.2026, Auftrag Oberchef)
- vorschaubild.js (neu, nach studio.js): `DS.VB` mit Schlüssel (Inhalt + Stand satz/vorlagen/druck/dokumente.js), Liste `api/vorschau`, Bild-Karte mit Platzhalter in Papierfarbe und 0,25 s Einblenden, Laden 150 % voraus, Nachziehen fehlender Bilder im Leerlauf (DS.png → POST api/vorschau). start.js: `vorschau()`, `passDoc()` (Meine Medien) und die Vorlagen-Galerie nehmen die fertigen Bilder.
- serve.py: GET/POST `api/vorschau`, Ablage `haeuser/culinarium/vorschau-dok/<schlüssel>.webp` + index.json (Papierfarbe), Cache immutable. Vorab bauen: `node _qa/vorschaubilder_bauen.js` (~100 s). Alte Bilder bleiben liegen (Aufräumen fehlt noch).
- serve.py Probe: Menükarten-Entwürfe alle im Aufbau «menue» (Ausrichtung, Rahmen, Grund verschieden).
- vorlagen.js: Plakat hoch ohne Daten nimmt Datum/Uhrzeit/Text aus DS.BEISPIEL.plakathoch (Story aus dem Reiter «Vorlagen»).
- ms-bureau.css, mail.css: Knopfschrift auf Versalhöhe beschnitten, #seitenwahl halbe Sperrung links.
- Stempel: vorlagen 46, start 74, vorschaubild 3, ms-bureau.css 22, mail.css 11. Sicherungen `*.vor-vorschaubild-…`, `*.vor-menueentwuerfe-…`, `*.vor-story-…`, `*.vor-textmitte-2026-10-29`.
- Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/imprimerie/galerien-2910/index.html

## Start schneller, Safari, Prüfskript (29.10.2026, Auftrag Oberchef)
- druck.js: `DS.ladePdf()` lädt pdf-lib und fontkit erst beim ersten PDF; `DS.vorladenPdf(M)` beim Zeigen auf «Druckfertig speichern» (studio.js) holt sie samt Druck-TTF vor. index.html lädt beides nicht mehr. PDF unverändert (gleiche Bytes).
- satz.js: Bildschirmschriften als woff2-Teilmenge Latein (375 → 121 KB), TTF nur noch fürs PDF. bau.py `bildschirm_woff2()` baut sie mit.
- serve.py: Text (JS, CSS, JSON, HTML, SVG) gzip mit Last-Modified/304; Cache «no-cache» statt «no-store» (api/ bleibt no-store).
- vorschaubild.js: zweiter Schlüssel nur aus dem Inhalt; fehlt das Bild des aktuellen Stands, steht sofort das des letzten Stands und wird nach dem Nachrechnen getauscht, der Server löscht das alte. Kein Live-Satz mehr beim Start nach einem neuen Stand.
- ms-bureau.css: Arbeitsfläche und Kopf unsichtbar, solange die Übersicht offen ist (WebKit malte sie beim Scrollen mit).
- vorlagen.js `STIL.kopf`, studio.js Schriftwechsel ohne STIL-Eintrag ohne Fehler.
- _qa/funktionen.js: «Le Livre» nicht mehr in der Navigation erwartet; Fotozähler = sichtbare Fotos (214 vom Haus + 28 der Website = 242; 18 im Plakatarchiv bewusst ausgenommen über marke.json «raus»).
- Stempel: satz 48, druck 58, studio 67, vorlagen 47, start 75, vorschaubild 4, ms-bureau.css 23. Sicherungen `*.vor-start-…`, `*.vor-gzip-…`, `*.vor-vbstand-…`, `*.vor-safari-…`, `*.vor-stilkopf-…`, `*.vor-livre-2026-10-29`.

## 30.10.2026 (neuer Account, Auftrag Oberchef, Punkte 1–6)
- Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/imprimerie/3010/index.html
- 1 Plakat hoch: die 112 Farb- und 12 Titel-Funde stammten aus der alten Tor-Kopie der Gestaltung (ohne Rolle «kopf», ohne plakathoch als Bildaufbau). Das aktuelle `_Werkzeuge/abnahme-tor/dok-tor.js` (Muster + Vorschläge, 655 Dokumente): 0 K12-Farbe, 0 K8 bei plakathoch. Kein Code geändert.
- 2 Start: satz.js `ladeMarke` holt marke.json, Markenbuch und druck.json gleichzeitig und lädt die Schriften, sobald marke.json sie nennt; index.html lädt die acht Bildschirmschriften und marke/druck/livre.json vor; serve.py komprimiert auch die Startseite selbst (35 → 10 KB). start.js: Kachel-Fotos als `data-bg`, gesetzt erst nahe am Bildschirm (IntersectionObserver), grosse Fotos über `DS.bildFuer` in passender Stufe (rund 1,5–2 × Anzeigebreite statt 2400er), Vorholen und grosse Kachelfotos erst nach «bereit»; plakat.js holt die Liste der Vorschläge erst nach «bereit». Gedrosselt 7,0 → 4,5 s (1195 → 577 KB), ungedrosselt 0,52–0,74 → 0,21–0,27 s.
  - Offen, Ziel 3 s nicht erreicht: die Startseite wartet (Robert «in einem Zug», höchstens 1,6 s) auf die Fotos des ersten Bildschirms; dazu teilen sich die Leitung die Schriften des Kleids (64 KB) und das Startbild des Kleids (fassade-1000, 91 KB). Unter 3 s geht es nur, wenn weniger Bytes vor dem ersten Knopf liegen; Vorladen des Startbilds probiert und verworfen (verschob die Skripte, Ergebnis gleich).
- 3 Safari: «Arten und Vorlagen» 1440 56–58 fps (Last 13–20), alle Ansichten 57–60, Handy 60, Chromium 117–120, keine Aufgaben über 50 ms. «Alle Vorlagen» zeigte beim schnellen Scrollen 12 leere Karten: Bilder in Blöcken mit content-visibility melden sich erst im Bild; vorschaubild.js beobachtet jetzt den Block und lädt alle seine Bilder → 0.
- 4 «Neu» am Handy: span `display:none` (ms-bureau.css), `aria-label="Neu"` am Knopf.
- 5 Messlauf: mail.css Haus-Knopf 38×38, Ansicht-Knöpfe 30×30, «Ansehen» 38×38; Bausteine als zwei volle Reihen (4 + 3), alle 74 px hoch, Gruppe mittig mit gemessenem Ausgleich je Zeichen; Felder als mitwachsende Zeilen (mail.js `wachse`, Enter schliesst); Vorschauzeile im Posteingang ganz statt mit «…»; Navigation ohne Beschnitt (ms-bureau.css). Messlauf oval/rand/gekuerzt/text-mitte/zier-x auf Start und Mail: 0 (Chromium, WebKit, 1440, 390). api/plakat.py: Hinweis ohne Geld («Live mit KI: Jeder Vorschlag entsteht in diesem Moment neu, gemalt für euren Abend.»).
- 6 Bewegung: `reinschweben` der Vorlagen-Karten von unten statt seitwärts (studio.css). Abgestimmt mit cu-tresen-kleid: .mk und .pk-karte schweben über bewegung.js, .stueck nicht in deren Liste (eigene gestaffelte Bewegung).
- Prüfungen: funktionen.js 105/105 (Chromium 1440; der Abteilungs-Test wartet jetzt 2,9 s, weil die Zahl seit 30.10. 1,4 s hochläuft), WebKit 390 101/104 wie vor den Änderungen (Mosaik-Tests gelten nur am Rechner, ResizeObserver-Meldung), plakat_funktionen 18/18 (WebKit 1440, Chromium 390), Druck-dpi `druckpruefung_vorlagen.js`: 1 rot «Angefangen hat es klein» A4 mit Foto flur 118 dpi (bestand vorher, druck.json der Gestaltung ist seit 28.10. leer), Vorschaubilder neu gebaut. Server 9087 neu gestartet, Log `_qa/log/server9087.log`.
- Sicherungen `*.vor-start3s-2026-10-30`, `*.vor-neu-…`, `*.vor-voraus-…`, `*.vor-messlauf-…`, `*.vor-cent-…`, `*.vor-bewegung-…`, `_qa/funktionen.js.vor-zahl-2026-10-30`.

## 30.10.2026 nachts: Nachträge Oberchef und Gestaltung
- Start gedrosselt 4,5 → 2,98–3,02 s (Messskript), im Bild 2,91–2,98 s (neu in `_qa/startmess.js`: `knopf_im_bild`, Playwright meldet rund 0,1–0,5 s später), 455 KB; ungedrosselt 0,23 s. Wege: index.html lädt katalog.js früh und fragt die Kachelfotos des ersten Bildschirms gleich an (nächste vier Anlässe, erste drei Abteilungen, kleine Fassung); start.js wartet nur auf Fotos des ersten Bildschirms (vorher 1,15 Bildschirmhöhen); Anton am Bildschirm nur Grossbuchstaben (bau.py, 31 → 15 KB), alles andere über die TTF mit getrennten unicode-range (satz.js, sonst lädt Chromium beide).
- druck.js: Achsen-Ausnahme `achse.zweispaltig_quer` (Einladung, Rückseite in a6q/dlq): zwei Achsen = Mitten der linken und rechten Textgruppe. `_qa/rot_vorlagen.js` (aus dem Scratch der Gestaltung übernommen, PORT=9471): 0 rot von 317.
- Grundlinien beim ersten `DS.druckplan`: das Messblatt schwebte über die Bewegung des Kleids (Liste enthält `.blatt`), Text 3–5 mm verschoben. `DS.seiteDom` setzt `data-wo-bw-nie` auf jedes Blatt; druck.js misst den Ursprung je Text neu. Erster = zweiter Aufruf (0,00 mm).
- Gruss: Stunden wie der Tresen (WO.gruss), nachts «Guten Abend»; geprüft 1, 4, 5, 10, 11, 17, 18, 23 Uhr.
- Kleid-Stempel in index.html (grund, rahmen-buehne, kleid/culinarium.css|js, oberflaeche.js) als md5 des Inhalts neu.
- Prüfungen: funktionen 105/105, plakat 18/18 (WebKit 1440, Chromium 390), rot_vorlagen 0/317, Druck-dpi 0 rot, Messlauf Start + Mail 0, Scrollen Safari 57–60 fps, Vorschaubilder neu. Stempel satz 53, druck 60, start 79.
- Sicherungen `*.vor-zweispaltig-…`, `*.vor-blattruhig-…`, `*.vor-anton-2026-10-30` (auch `schriften/Anton-400.woff2.vor-anton-…`).

## 30.10.2026: Tor-Funde dok-3010 (Menükarten)
- Beispiel-Menükarten tragen nur noch das Menü ihres eigenen, vergangenen Abends: Arten (`INHALT.menuekarte.menue` in start.js), Muster (`DS.BEISPIEL.menue` in vorlagen.js), `_qa/beispiele.json` und der Generator `_qa/vorlagen_culinarium.py` nehmen die Menükarte «Fr 21. und Sa 22. Februar 2025» mit ihrem Menü aus website/abende_info.py (KARTEN DFqbLG2s_dc). Die Anlässe Nov./Dez. 2026 haben keine Menükarte mehr (katalog.js von Hand nachgezogen wie der Generator es jetzt schreibt; der Generator selbst wurde nicht ausgeführt, er schreibt auch vorlagen/*.json der Gestaltung).
- serve.py Probe («Entwerfen» ohne KI): Menükarten kommender Abende werden nie gewählt (`menue_kommt`); ein Auftrag mit «Menükarte» nimmt eine Menükarte (vorher die Karte «Pairing zum Gang»), bei Gleichstand den jüngsten vergangenen Abend mit vollem Datum. Die fünf Entwürfe unterscheiden sich in Aufbau, Gewichtung und Satz: Menükarte wie die Vorlage, Menükarte im anderen Ton, Teller und Drinks als Liste, nur die Drinks (ab drei Drinks, sonst Menükarte Plakatpapier), die Teller in Rudis Zeilen mit Drink darunter (nur bei kurzen Zeilen, sonst Menükarte Plakatpapier). Geprüft für Feb. 2025, Sept. 2023, April 2024: 15 Entwürfe, 0 rot.
- Tor-Lauf (dok-tor.js, Arten + Entwerfen + Muster, 843 Dokumente): keine Funde ausser Bildprüfungs-Kandidaten; kein Datum Nov./Dez. 2026 in den Entwürfen. Funktionen 105/105, Plakat 18/18, Druckprüfung 0 rot von 311, Druck-dpi 0 rot, Vorschaubilder neu. Stempel start 80, vorlagen 48, katalog 36. Sicherungen `*.vor-menue-2026-10-30`.
- 30.10. (Fund K20 der Gestaltung): «Dann haste allet richtig jemacht!» (Satz von Dirty Chicken) von allen Culinarium-Blättern genommen: Muster «Bild im Rahmen» (DS.BEISPIEL.fenster) und Katalog «Wer dahinter steht» → «Hinter den Plakaten stehen dieselben Leute, Abend für Abend.» (Website bau.py); «Danke für den Abend» in Katalog (zweimal) und Mail (Vorschauzeile und Text) → «Nichts wäre all das ohne unsere tollen Gäste! Danke an alle, die da waren.» (Culinarium-Instagram 2023). Generator, beispiele.json, mail_vorlagen.js.txt nachgezogen; bei Dirty Chicken (vorlagen_neu_2910.py) bleibt der Satz. Stempel vorlagen 49, katalog 37, mail.js 10. Druckprüfung 0 rot, Funktionen 105/105, Messlauf Mail 0, Vorschaubilder neu. Sicherungen `*.vor-dcsatz-2026-10-30`.
- 30.10. Messlauf-Funde (cu-messlauf, Notiz messlauf-3010-plakatwerkstatt.md), nur Stilvorlagen und mail.html, keine eingefrorene Datei: «Zurück zur Drucksache» wird in der Kopfleiste nicht mehr zusammengedrückt (ms-bureau.css 26); Prüfliste am Handy unter der Kopfleiste in voller Breite statt links aus dem Bild und über «Als Datei speichern»; Foto-Dialog: Schliessen 36×36, Titel «Fotos des Hauses» einzeilig, Suche darunter, Platzhalter «Suchen: Abend, Tafel …» ganz lesbar (mail.css 17). Ovale Knöpfe im Mail-Kopf und «PREISLISTE» waren schon behoben (Lauf älter). Bewusst so: Prüfliste am Rechner liegt als Aufklapp-Liste über der Vorschau; Handy-Vorschau im Rundgang kürzt den Beitragstext nach drei Zeilen wie Instagram.

## Tor werkstatt-3010c + kein «×» (30.10.2026, Mittag)
- K5 Mail-Kopf bei 1000: «HTML kopieren» als runder Knopf, Marke ohne Untertitel, enger (mail.css). Rechte Kante 989 px von 1000.
- K7 Vorlagen-Liste: ausgewogen umbrochen, schmal 14,5 px; kurze Namen einzeilig, nie ein Wort allein.
- K4 «Leere E-Mail»: kleines leeres Mailblatt statt dunkler Tapete.
- K1 «Neu erstellen» ohne Wort 36 × 36 (alle Breiten bis 1380).
- K33 Willkommen als Karte an der Ecke ohne Abdunkeln (fuehrung.js + studio.css), Seite bleibt bedienbar.
- K35 Rückgängig/Wiederholen: Pfeile auf die Mitte gesetzt (Form 4,5–19,5 statt 7–22).
- K2/K8 Platzhalter kürzer und dunkler («Etwa: …», «Etwas anderes? Kurz beschreiben …», Suche bei < 1100 kurz); Auswahlwerte ganz, notfalls zweizeilig; Name im Handy-Rahmen ganz.
- K3 Vorlagen-Kacheln einer Reihe gleich hoch.
- K18 «Eine Vorlage» statt «1 Vorlagen»; mehr Vorlagen je Art ist Sache der Gestaltung (vorlagen/*.json, nicht angefasst).
- Kein «×» (Robert): Masse «A auf B» (studio.js, start.js, instagram.js, index.html); Schliessen-Knöpfe mit Zurück-Pfeil (fuehrung, lelivre, instagram, mail.html, studio.js, start.js), Löschen/Entfernen mit Papierkorb (mail.js, studio.js); kein Drehen beim Überfahren.
- Kleid-Stempel neu (md5). Gemessen gezielt WebKit 1440/1280/1000/390: Kopf, Vorlagen-Liste, Platzhalter, Neu-Knopf, Kachelhöhen; Willkommen am Bild.
- Versionen: studio.css 77, start.js 82, studio.js 68, instagram.js 39, fuehrung.js 38, lelivre.js c3, mail.css 19, mail.js 11. Sicherungen *.vor-tor-3010c-2026-10-30.

## Tor werkstatt-3010e + Mail (Tor 2), 30.10.2026 13:10
- Arten-Zahl: `haeuser/culinarium/vorlagen/index.json` je Eintrag Feld «gruppe» (Name wie in der Werkstatt, z. B. «Einladung und Gutschein»), «art» unverändert; `_qa/vorlagen_culinarium.py` schreibt das Feld künftig mit. Start zählt Arten aus «gruppe»: «115 fertige Vorlagen in 11 Arten» (nur Arten mit Bibliothek). Sicherung index.json.vor-gruppe-2026-10-30.
- Platzhalter Auftrag (Art-Seite) unter 1100 px «Kurz beschreiben …»; Studio-Auftrag «Etwa: …» und dunkler (K8).
- Ziffern 3/4/5 «Vorschläge» mittig (plakat.css). Handy-Vorschau: erster Satz, bis vier Zeilen.
- Führung am Studio: Karte an der Ecke, kein Abdunkeln, nur feiner Ring um die gezeigte Stelle (K33); Fehler bei Schritt ohne Film behoben (fuehrung.js).
- Mail: Vorschau passt sich der Spalte an (scale, nie angeschnitten, kein Seitwärtsscrollen; 981–1180 px schmalere Platten); «MOMO X RUDI» mit festen Leerzeichen; Fuss «Walk on the Wild Side» / «Haasemannstraße 13 · 30449 Hannover» ohne Trenner am Zeilenende.
- Versionen: start.js 85, studio.css 79, plakat.css 18, fuehrung.js 39, mail.css 21, mail.js 14, mail-satz.js 3.

## Tor 1, werkstatt-3110a (31.10.2026)
Behoben in start.js v91, studio.css v85, studio.js v69, lelivre.js c4, ms-bureau.css v27, index.html (Sicherungen `.vor-tor-3110a-2026-10-31`):
1. Logo aufs Plakat: echte Masse werden vor dem Einsetzen gemessen, Kasten = Bild (5,418 zu 5,418).
2. Fotos des Hauses und Fotoleiste in Logo & Farben zeigen das ganze Bild (contain), nichts angeschnitten.
3. Filter-Pillen brechen nicht mehr, «Weitere Fotos» passt.
4. Fuss: Pillentext steht auf der Kante von Symbol und Kleinschrift.
5. Titel: Mail-Karten und Vorlagennamen halten die letzten zwei Wörter zusammen, keine Silbentrennung in Kartentiteln.
6. Format-Wahl: Name und Punkt zusammen; im Reiter «Mit einer Vorlage» Format und Grund untereinander, eine Zeile.
7. Grund-Wahl: 9 px Luft je Seite.
8. Handy: Platzhalter «Suchen» (66 px in 71 px).
