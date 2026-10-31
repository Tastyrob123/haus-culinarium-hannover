---
tags: [projekt, website]
status: aktiv
---

# Das Markenbuch (Le Livre, Marke) · Culinarium Hannover · Lieferung (28.10.2026)

Status: fertig, lokal geprüft, nichts online, nichts verschickt. Endstand 28.10.2026 14:2x (nach Roberts Namenswahl und den 23 geschärften Fotos des Bilder-Chats neu gebaut und neu geprüft).

**Adresse:** http://localhost:9085/_werkzeuge/livre/
Markenbuch: http://localhost:9085/_werkzeuge/livre/buch.html · Anleitung: http://localhost:9085/_werkzeuge/livre/anleitung.html · Stand-Weg für die Zentrale: http://localhost:9085/marke/livre.json
Lieferung im Browser: http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/livre/LIEFERUNG.md
Server: `python3 _werkzeuge/livre/server.py 9085` aus dem Projektordner (Markenprüfung ohne Claude, Probe-Antwort). Neu bauen: `python3 _werkzeuge/livre/bau.py`, Anleitung `python3 _werkzeuge/livre/anleitung_bau.py`.
Name: aus dem gemeinsamen Kleid (`_werkzeuge/oberflaeche/kleid/culinarium.js › namen.marke`), seit Roberts Entscheid vom 29.10.2026 «Das Markenbuch». Kein Name steht fest im Werkzeug.
Bilder für Zentrale, Werkbank und Oberchef (1440 und 390, WebKit): http://localhost:8978/haus/_Oberchef/zeigen/culinarium/livre/livre-uebersicht-1440.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/livre/livre-fotos-1440.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/livre/livre-foto-1440.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/livre/livre-dateien-1440.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/livre/livre-pruefung-1440.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/livre/livre-markenbuch-1440.png (je auch «-390.png»). Neu aufnehmen: `node _werkzeuge/livre/pruefung/schirm.js <ordner>`. Belege: http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/livre/pruefung/belege/band-auf-den-plakaten.png · http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/livre/pruefung/belege/vorher-nachher-tafel.png · http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/livre/pruefung/belege/markenbuch-pdf-alle-seiten.png

## Was steht

- **Fotos (L02, L09, L18):** 231 Fotos aus dem Bildregister der Website (`BILD` in `website/bau.py`, per ast gelesen, `register.py`; dazu die Bilder je Abend genau wie `bau.py` sie dazurechnet), 5 doppelte zusammengeführt, in 10 Bereichen (Die Bar in Linden, An der Tafel, Rudis Teller, Momos Drinks, Am Pass, Die Leute, Plakate, Bilder der Abende, Dirty Chicken, Walk on the Wild Side). Herkunft je Foto in Worten: 193 von Culinarium (Rudis Dateien, Instagram von Culinarium, Rudi und Momo, Dirty Chicken; Plakate mit «Rechte an der Illustration offen»), 38 mit fremden Rechten (Instagram der Bar Walk on the Wild Side: Ort der Abende, gehört nicht zu Culinarium, Freigabe offen), keines mit KI erzeugt. Je Foto vier Grössen (Beitrag, Story, Website, Druck in voller Grösse von Rudis Original), Ausschnitt ziehbar, zwei Wege in die Plakatwerkstatt (:9087, `?haus=culinarium`). Kein Saison-Filter (Culinarium kennt keine Saison). Filter als Wortreihe mit Schrägstrich wie Rudis Zeilen, keine Pillen-Reihe.
- **Geschärfte Fotos kommen von selbst nach (L22):** der Registerstand vor dem Schärfen ist gesichert (`_register-vor-schaerfen.json`, 236 Einträge, 28.10.2026 11:5x, vor jeder Änderung des Bilder-Chats). Jedes Foto, das `culinarium-bilder` auf `_quelle/ki/geschaerft/` umstellt, zeigt nach `python3 _werkzeuge/livre/bau.py` «Vorher / Nachher / Schieber». Stand 13:5x: 24 Fotos mit Vorher (23 vom Bilder-Chat geschärft, gelesen aus `GESCHAERFT` in `website/bau.py` genau wie die Website es darüberlegt; dazu das Team hinter der Theke, mit KI auf 4K gerechnet). Alle 24 als Tafel nebeneinander gelegt und gemessen: gleicher Ausschnitt (Korrelation 1,0, mittlere Abweichung 0,4–1,0 von 255), http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/livre/pruefung/belege/vorher-nachher-tafel.png. Kommen weitere dazu: `python3 _werkzeuge/livre/bau.py`.
- **Logo & Dateien (L03):** Rudis Original-Logo (28.10.2026) Pfad für Pfad: Wortmarke mit Zeile «A UNiQUE EXPERiENCE» (Original #383944 wie im PDF, dazu Schiefer auf Hell und Warmweiss auf Dunkel, Rudis PDF unverändert), die Wortmarke allein, die Zeile allein; nur die Farben, die das Markenbuch erlaubt. Dirty Chicken: Logo und das D als Rudis Originale (PNG und PDF), nie umgefärbt. Drei Tapeten der Website (Nacht, Warmweiss, Dirty Chicken). Das Instagram-Profilbild zum Nachschlagen. 14 Farben der Website (jede in `culinarium.css` gefunden) in vier Gruppen mit je einem eigenen Foto, dazu die sechs Farben der Abende je mit ihrem Plakat; CSS, JSON, ASE. Vier Schriften Byte für Byte die der Website (Fraunces, Urbanist, Instrument Sans, DM Mono) mit Schriftprobe als Ausschnitt der Website, ZIP mit TTF und Lizenzen. Alles als ein ZIP (2,9 MB). 34 Dateien.
- **Markenprüfung (L04, L10):** Bild oder PDF bis 30 MB, Farben ohne KI gemessen (ΔE 2000 gegen die Palette), Rest beurteilt Claude nur mit `LIVRE_KI=1` (Regel 54); ohne Schalter Probe-Antwort, deutlich beschriftet. Regeln der Prüfung neu für Culinarium (Abende, Farben, Abendfarbe pro Plakat, Violett nur für Dirty Chicken, Fraunces leicht, Rudis Zeilen, Wortmarke, Tapete, Du-Ton, Wertigkeit statt Menge). Beispiel: ein eigens gezeichneter Beitrag «Ein Abend mit Momo x Rudi» mit Rudis Foto und Wortmarke, aber Baskerville, Gold und reinem Schwarz: gemessen «Farben fremd · passt nicht», Urteile als Beispiel beschriftet.
- **Markenbuch (L05):** das Markenbuch der Station 05 (Farbwelt A «Plakat»), im Stand der Website (Fehlerbuch 10a, neue Zeile 28.10.): Rudis Original statt des Platzhalters in allen Symbolen und Zeichen-Dateien, Fraunces wie die Titel der Website (wght 340, SOFT 100, als feste Schrift festgesetzt, nie fett), Schriftwerte wie `culinarium.css`; ohne Internes (Platzhalter-Hinweise, Welt B mit Probe-Seiten, «Projekt Nummer 10», Schriftwahl gegen den Platzhalter, Vermerk Station/Tasty). Das Band (Wortmarke im doppelt gerahmten warmweissen Feld) steht nur noch als Merkmal der Plakate, belegt mit vier Plakaten (Block «Auf den Plakaten» im Blatt Zeichen; auf allen 12 Plakaten seit Oktober 2023, http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/livre/pruefung/belege/band-auf-den-plakaten.png); der Baustein «Das Band» und die Logo-Fassungen «Auf dem Band» und «Unter dem Foto» sind raus (Oberchef 28.10.2026; Robert hat das Band am 26.10. als Beschriftung abgelehnt). 13 Blätter, Leiste des Buchs als Werkzeug-Leiste (zurück, Blätter in einer Zeile ab 1366 px, «Als PDF sichern»), Logo richtig und falsch als eigene Seite mit dem Original. PDF 37 Seiten A4 quer, als Bildtafel angesehen.
- **Rahmen (R01–R24, L11, L12):** gemeinsame Oberfläche (Rahmen «Die Bühne», Kleid `culinarium` von culinarium-maison), Fehlermelder (`cu-livre-fehler`), Startfehler-Tür mit Namen, Ladezeichen nach 280 ms, Auftakt, Rundgang (vier Schritte, Schild fest über der Leiste, Farben Nacht/Kerze), «Zur Werkbank» mit Schlüssel `culinarium-wb` und Herkunft `wbo` (Werkbank :9088), Wege zu anderen Werkzeugen auf deren Server (127.0.0.1:<port>). Knöpfe wie Website und Kleid: Platte mit rundem Knauf in Kerze. Server nur lokal mit Host-, Herkunfts-, Grössen- und Mengengrenzen.
- **Anleitung:** neun Kapitel mit Bildern aus dem echten Werkzeug (WebKit), Texte für Culinarium.
- **Online-Weg vorbereitet, nicht hochgeladen:** `online.json`, `online/livre_online.py` (Le Livre veröffentlicht nichts; Downloads online in Website-Grösse).

## Station 05 nachgezogen (Auftrag Oberchef, 28.10.2026)

Werkbank (`papier.py`, `marke_werkbank.py`, `sb_strom.js`), Tresen und Schaufenster lesen aus `_kette/05-markenbauer/`. Mit `python3 _werkzeuge/livre/station5_nachziehen.py`
(wiederholbar, liest immer aus den Sicherungen `*.vor-website-stand-2026-10-28`) steht die Station jetzt auf dem Stand der Website:
- `marke/markenbuch.html` und `marke/logo-richtig-falsch/index.html`: dieselben Umstellungen wie in Le Livre (Rudis Original, Fraunces 340 SOFT 100, Interna raus, Band nur auf den Plakaten mit Beleg). http://localhost:8978/haus/Culinarium%20Hannover/_kette/05-markenbauer/marke/markenbuch.html
- `marke.json`: wortmarke (original), schriften (Werte und Dateien der Website), band, darstellungsidee, knopf, merkmale_nicht, neu website_stand, stand. Unverändert: abendfarben, farben, farbwelten, welt, ton.
- `marke/bilder/`: neu `plakat-2023-10.jpg`, `plakat-2024-04.jpg` (Beleg), `herkunft.json` ergänzt; neu `marke/schriften/Fraunces-340-wie-website.woff2`. Sonst nichts überschrieben.
- Werkbank und Tresen gemeldet (neu bauen, Marke-Stellen gegen die Website prüfen).

## Wie geprüft (Ergebnisse in `pruefung/ergebnisse/`, Bilder in `pruefung/belege/`)

| Lauf | Ergebnis |
|---|---|
| Bedienen (`bedienen.js`) Chromium 1440 × 900 | 62 von 62 |
| Bedienen WebKit 1440 × 900 | 62 von 62 |
| Bedienen Chromium 390 × 844 | 60 von 60 |
| Bedienen WebKit 390 × 844 | 60 von 60 |
| Rahmen und Grenzfälle (`zusatz.js`) Chromium | 15 von 15 (R02, R03, R04, R15, R17, R18, R19 aus der Werkbank :9088, L09, Suche mit 5'000 Zeichen/`<script>`/Emoji/Umlauten, L10 über 30 MB/29 MB/169 MP/400 px/kein Bild/PDF drei Seiten, Netz weg, zwei Fenster, 320 und 390 px, Markenbuch, Druck 37 Seiten) |
| Rahmen und Grenzfälle WebKit | 14 von 14 (Druck-PDF nur in Chromium); erster Lauf 13/14: Farbtabelle bei 320 px 3 px zu breit, behoben |
| Fehlerbuch 10a (`fehlerbuch.js`, neu) Chromium und WebKit | je 4 von 4 (58 kein roher Code, 66 helle Titel auf Dunkel, 127 Kopf bei 920–1240 px, 115 Rundgang-Schild fest) |
| Dateien (`dateien_pruef.py`, Teil A neu) | 11 von 11: Farben = Website bzw. Plakate, Schriften Byte für Byte, Wortmarke Pfad für Pfad Rudis Original (auch im Markenbuch), Originale Byte für Byte, PNG gefüllt in ihrer Farbe, ZIP vollständig, alle 231 Fotos in vier Grössen (924 Dateien), Druck = Rudis Original, Probe ohne Schlüssel und ohne Anfrage nach aussen |
| Sicherheit (`sicherheit.py`) | 15 von 15 (421, 403 Origin und Sec-Fetch-Site, 413, 415, 400, 429 mit Retry-After, 22 gesperrte Pfade inkl. `_quellen.json`, `_register-vor-schaerfen.json`, `website/bau.py`) |

Alle Läufe nacheinander, nie zwei Browser zugleich: `zsh _werkzeuge/livre/pruefung/alles.sh <bilderordner>`. Bilder: `pruefung/belege/` (Grenzfälle je Browser, Schirmbilder, Markenbuch als PDF und als Bildtafel aller 37 Seiten).

Speichern → neu laden: Le Livre speichert nichts (nur «Ergebnis sichern» als Datei auf dem Rechner); geprüft ist «Neuladen bleibt in der Ansicht» und dass nichts gespeichert wird.

**Flüssigkeit (Regel 55, `pruefung/fluss.js`, Chromium gedrosselt, echtes Scrollen bis ganz unten, Rechnerlast 6–17 durch die anderen Chats im ersten vollständigen Lauf, also eher zu schlecht als zu gut):**

| Ansicht | 1440 · 4× | 1440 · 6× | 390 · 4× | 390 · 6× |
|---|---|---|---|---|
| Übersicht | 8.3 / 9.2 ms / 0 von 82 | 8.3 / 9.2 ms / 0 von 82 | 8.3 / 9.2 ms / 0 von 136 | 8.3 / 9.3 ms / 0 von 138 |
| Fotos (alle 231 nachgeladen) | 8.3 / 9.2 ms / 0 von 913 | 8.3 / 9.2 ms / 4 von 905 | 8.3 / 9.2 ms / 0 von 1049 | 8.3 / 9.3 ms / 1 von 1071 |
| Logo & Dateien | 8.3 / 9.2 ms / 0 von 308 | 8.3 / 9.2 ms / 0 von 308 | 8.3 / 9.2 ms / 0 von 456 | 8.3 / 9.2 ms / 0 von 464 |
| Markenprüfung | 8.3 / 9.2 ms / 0 von 138 | 8.3 / 9.2 ms / 0 von 137 | 8.3 / 9.2 ms / 0 von 204 | 8.3 / 9.2 ms / 0 von 201 |
| Markenbuch | 8.4 / 16.7 ms / 1 von 1234 | 9.3 / 17.5 ms / 2 von 1072 | 8.3 / 9.2 ms / 0 von 10199 | 8.3 / 9.3 ms / 1 von 10207 |

Je Zelle: Bild-Mitte / p95 / Bilder über 33 ms. Rund 120 Bilder je Sekunde, Springen beim Laden höchstens 0.0044. Zweiter Lauf nach dem Namenswechsel (Rechnerlast 7–32) bestätigt die Werte bis 390 · 4×, brach dann bei Last 32 mit einer Zeitüberschreitung des Seitenaufrufs ab (Server antwortete danach in 2 ms); Markenbuch 1440 · 6× bei Last 28: p95 42,8 ms. Werte: `pruefung/ergebnisse/fluss.jsonl`.

## Fehlerbuch 10a Zeile für Zeile (was Le Livre betrifft)

| Zeile | Stand bei Culinarium |
|---|---|
| Roher Vorlagen-Code (`{…}`, undefined, NaN, None) | nirgends, gemessen in allen Ansichten, vier Foto-Fenstern, Markenbuch, Anleitung (`fehlerbuch.js` 58) |
| Fakten nur aus der Quelle dieses Hauses | Fotos und Herkunft aus `website/bau.py` und den `herkunft.json`, Farben aus `culinarium.css`, Abendfarben aus `marke.json`, Logo aus `_quelle/logo/original/`; keine Auszeichnungen (Falstaff gehört der Bar); Suche nach fremden Hausangaben im Revier: nur Vermerke «Vorbild Schäfli» und Prüfmuster |
| Bilder in jeder Liste, doppelte Einträge zusammengeführt | Fotos mit Bild, je Farbgruppe ein Foto, je Abendfarbe ihr Plakat, Schriften mit Ausschnitt der Website; 5 Doppelte zusammengeführt |
| Kein Foto zweimal auf einem Bildschirm, Farbfeld ganz | Bühnen je Ansicht eigene Fotos (Fassade, Kerzen, Karte am Platz, Pass), Übersicht-Kacheln andere; Gruppenfotos keins doppelt (bedienen 41) |
| Titel auf dunklem Grund hell | Kopf und Startbild 246–253 von 255 (`fehlerbuch.js` 66) |
| Titel im Kopf überdeckt nie einen Knopf | 920, 1000, 1100, 1240 px in jeder Ansicht (`fehlerbuch.js` 127) |
| Rundgang-Schild fest, wandert nie | 24 px rechts über der Leiste, gleich nach dem Scrollen, nach neuer Fenstergrösse wieder über der Leiste (`fehlerbuch.js` 115: 24 px vom rechten Rand, 14 px über der Leiste, gleich nach Scrollen und neuer Fenstergrösse) |
| Markenbuch = bestätigtes Markenbuch der Station 05 | ja, `buch.py aus_station5()`, im Stand der Website (siehe oben; Station 05 steht auf «liegt vor») |
| Kein Vergleich mit anderen Häusern, keine Kette, keine Pfade im Kundenbuch | Bau bricht ab bei Platzhalter, Station, Tasty, Welt B, anderen Häusern, `_quelle/`, `_kette/` (`buch.py`), Prüflauf bedienen 59 |
| Markenbuch als PDF ohne zerschnittene Karten | Druckregeln (`break-inside:avoid`, kleine Abstände, Fenster-Bild als eigene Seite), 37 Seiten als Bildtafel angesehen |
| «Als PDF sichern» wartet über `addEventListener` | `buch.js` wie das Vorbild, Knopf direkt nach dem Öffnen geprüft |
| Probe ohne KI lobt nie Grelles | Beispiel mit Gold und Schwarz: «passt nicht»; reines Schwarz zählt nicht als Hausfarbe (aus dem Schäfli übernommen) |
| Wortmarke nie über die Deckung umfärben | Rudis Logo ist einfarbiger Vektor: einfarbig erlaubt (nur Schiefer, Warmweiss); Dirty Chicken nur Original |
| SVG zu PNG über `data:` | ja (`bau.py svg_png`) |
| Schriftproben nur aus reinen Elementen | `listen_bilder.js` nimmt nur Elemente, deren Kinder alle dieselbe Schrift haben |
| Prüfläufe klicken Kacheln mittig | `scrollIntoView({block:'center'})` in allen Läufen |
| «Zur Werkbank» mit `wbo` auf eigenem Prüfserver | aus :9088 geöffnet → `http://127.0.0.1:9088/werkbank/index.html` (zusatz 76) |
| Wege zu anderen Werkzeugen auf deren Server | Zentrale :9081, Plakatwerkstatt :9087, je 127.0.0.1 (bedienen 10, 31) |
| Gemessene Farben kompakt (L04) | Farbband und Raster wie das Vorbild; bei 320 px in WebKit stand die Tabelle 3 px über (längerer Spaltenkopf), behoben |
| `[hidden]` gegen `display`-Klassen | Fenster ohne eigene `display`-Regel, Öffnen und Schliessen geprüft (bedienen 32–36) |
| Keine «Wer arbeitet hier?»-Abfrage, keine ausgegrauten Knöpfe | gibt es nicht |

## Offen (mit Grund)

- **Band:** erledigt nach Antwort des Oberchefs (28.10.): nur noch als Merkmal der Plakate, belegt; Baustein und Band-Fassungen raus.
- **Farbwerte CHARAKTER.md ↔ Website:** CHARAKTER.md nennt Kerze #CF7233 und Nacht #16141B, die Website trägt #EF7649 und #16151A; Le Livre zeigt die Website. An den Oberchef gemeldet.
- **Weitere geschärfte Fotos:** stellt `culinarium-bilder` noch mehr um, einmal `python3 _werkzeuge/livre/bau.py` (24 sind heute drin).
- **Markenprüfung mit Claude:** aus, bis Robert den Schalter freigibt (Regel 54).
- **Fotos der Bar (38) und Plakat-Illustrationen:** Rechte offen, im Werkzeug gekennzeichnet; Fotograf je Foto von Rudi offen.
- **Sprachen (L01, L08):** nur Deutsch, Sprachplan nicht entschieden (Schritt 15a).
- **Online:** nicht hochgeladen (Auftrag). **Firefox und 1366 × 650:** nicht gelaufen (Auftrag nennt Chromium und WebKit, 1440 und 390). **Anmeldung (R22):** bis zur Auslieferung kein Passwort.
- **R08–R14, R23 (Leiste mit Speichern/Veröffentlichen, Fassungen, eigene Prüfseite):** betrifft nicht, Le Livre ändert nichts (wie Vorbild); die Leiste trägt Bildrechte und das ZIP.
- **L19 (Druck mit Ausschnitt), L21 (Auszeichnungen):** betrifft nicht; die Website zeigt keine Ausschnitte (nur Bildmitte), Culinarium hat keine Auszeichnungen.

## Gelernt (eingetragen im Werkzeug-Master)

- 10a: Original-Logo nach Station 05 → Markenbuch im Werkzeug auf das Original nachziehen, Bau bricht bei «Platzhalter» ab.
- Abschnitt 9: Marken-ZIP packt sich selbst ein (erst die Liste, dann das ZIP; der erste Bau wuchs auf 23 GB, sofort gelöscht). Längere Spaltenköpfe der Farbtabelle in WebKit 320 px messen. Werkzeugnamen mit Artikel nie roh in einen Satz («Zurück zum Markenbuch», «in der Plakatwerkstatt»).

## Messlauf 30.10.2026 (Chat Messlauf/Querprüfung)

Rundgang-Knopf «Weiter» (`livre/rundgang.js`) mit Schrift im eigenen span, optisch mittig; Anleitung «So ist das Markenbuch aufgebaut.» bricht nicht mehr mit einem Wort allein um (festes Leerzeichen in `anleitung_bau.py`). Matrix 62/62, 62/62, 60/60, 60/60; Zusatz 15/15 und 14/14 (L05 auf zwölf Blätter nachgezogen: «Farbwelt» ist seit 29.10. auf Roberts Wort draussen).
Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/messlauf-2910/index.html

## Markenbuch ans Tor 30.10.2026 (Chat Werkbank, Oberchef-Auftrag)

Farbkacheln zwischen 901 und 1279 px: Foto über den Farben, Reihe bleibt eine Reihe (M25), Innenabstand 10 px, Unterzeile .72rem; Datum bricht nach «/» um (`livre.js`, `<wbr>`). Unter 1000 px werden Reihen ab fünf Farben zum Band zum Wischen wie am Handy. Ab 1280 unverändert. Hausregeln: Farb- und Schattenübergänge raus (`buch.py`, Regel 55). Anleitung lädt das Kleid (`anleitung.vorlage.html`). ?v-Stempel auf Stand des Kleids. Messlauf (`--groesse 1000` neu): Markenbuch, Hausregeln, Anleitung bei 1440/1280/1000/390, Chromium + WebKit, 0 Funde ausser Hinweisen «gekürzt»; Farbkacheln zusätzlich bei 1100 und 960 nachgemessen, 0.

## Tor 3, 30.10.2026 (12 Funde, Chat Werkbank)

App: Bildzeile in den Fotos ganz, ausgewogen umbrochen, nie gekürzt; Farbkacheln nie unter 132 px (Gruppen ab fünf Farben mit Foto als Streifen darüber, passt die Reihe nicht, Band zum Wischen, Container-Abfrage); RGB-Werte brechen nie um; Bildrechte ohne offene Frage (`livre.js`, `bau.py` Quelle je Foto). Hausregeln (`buch.py`): x raus aus Text und Tapete (auch Tapeten-Dateien in `dateien/`, `bau.py`); Rechtehinweis neu; «Woher die / Farben kommen.»; Zutatenzeile ohne Trenner am Zeilenanfang, «Der Teller» ungeteilt; 5 % auf der Grundlinie; Kapitel-Leiste in zwei Reihen zu sechs, nie unter dem Blatt (auch 1440: «Mitnehmen» lag darunter), am Handy ohne Rauten; Musterzeilen nur zwischen Wörtern; Bildraster am Handy ohne Loch; Stempel der Stilblätter aus dem Inhalt. Anleitung: «So ist das Markenbuch aufgebaut.» ohne festes Leerzeichen (WebKit rückte ein), Probe-Hinweis in Kap. 07 ersetzt, Kap. 04 ohne offene Rechtefrage. Geprüft in WebKit 1440/1280/1000/390 an den geänderten Stellen.

## Tor 2 (M1–M10), Tor 3 Nr. 13, kein «×» (30.10.2026, Chat Werkbank)

Eine Navigation in den Hausregeln (Kapitel nur noch in der Inhaltsleiste, zwei Reihen zu sechs; PDF-Knopf rechts). 5 % nie abgeschnitten. Fotos der Bar heissen «von der Bar» statt «fremde Rechte» (App, Anleitung). Logo «Richtig» in drei Spalten, Titel oben bündig; Downloads: letzter Eintrag volle Breite; Haltung und Herkunft auf einer Oberkante; Musterzeilen ausgewogen; Ortszeile am Handy untereinander ohne Raute; Anleitung: letztes Thema volle Breite. Weniger Bewegung: in den Hausregeln keine Auftritte, keine Schleifen. Kein «×»: Schliessen-Knopf der App mit Zurück-Pfeil (`livre.js` ZU), «Falsch»-Zeichen roter Kreis mit Querstrich (`buch.py`).

## Tor 3 Nachprüfung (30.10.2026)

RGB der Farbkarten in den Hausregeln nie umbrochen; Musterzeilen mit Trennern am Handy einzeilig (kleiner gesetzt), «BY MOMO X RUDi» bricht nie; zweiter Knopf «Logo richtig und falsch» im Schluss raus; Probe-Hinweis der Markenprüfung raus (`livre.js`); abgeschnittene Farbrolle «… in A» gekürzt. Weniger Bewegung: 0 laufende Animationen (WebKit 390/1440).

## Tor 3 N, O, P (30.10.2026, cu-messlauf)
- N: Kein Schrägstrich mehr am Anfang einer Zeile in den Filterzeilen (Bereich, Format, Herkunft). Jedes Wort trägt seinen Trenner, die Zeile schneidet den vor dem ersten Wort ab; mitten in der Zeile bleibt alles wie vorher. livre.css (Block am Ende).
- O: Platzhalter im Suchfeld kürzer: «Suchen: Tafel, Drink, Plakat», passt bei 390. livre.js (T.suchen).
- P (Hänger bei 390 nach Fotos → Die Bar in Linden → Rudis Teller): Im Tor-Werkzeug (Kopie mit Protokoll, WebKit 390 × 844) fünfmal hintereinander durchgelaufen, je 21–22 s, kein Hänger. Zweimal hing es vorher beim Messen, beide Male lief gleichzeitig ein zweiter Browser von mir; ohne Parallellauf nie. In der Seite läuft keine Schleife: Raster 22 Kacheln, kein Nachladen, Auftritte enden. Einzige Bewegung, die nie «fertig» meldet: das scrollgebundene Ziehen des Kopffotos aus dem Kleid (woZug, view()) – das Tor wartet darauf höchstens 2,5 s.
- bau.py gelaufen: livre.css?v=039694aa92, livre.js?v=6204c1952d. Sicherungen `*.vor-filterzeile-2026-10-30`.
- Q (Tor 3, Fenstertitel mit Einzelwort): Die letzten zwei Wörter jedes Fenstertitels hängen mit festem Leerzeichen zusammen, Bindestriche darin brechen nicht. Wird das Paar breiter als die Spalte, bricht der Titel wieder frei. Am Handy (bis 420 px) ist der Fenstertitel 28 statt 32 px gross. Alle 167 Titel bei 1440, 1280, 1000 und 390 geprüft: kein Überstand, kein Einzelwort. Bleibt nur «Plakat ⏎ Silvester-Frühshoppen» (zwei Wörter, das zweite passt nicht neben das erste). text-wrap:balance aus dem Kleid bleibt; ein nowrap-Block hätte sich damit in WebKit nicht umbrechen lassen. livre.js (zusammen, Prüfung nach dem Öffnen), livre.css (letzte Zeilen). Sicherungen `*.vor-fenstertitel-2026-10-30`.
- R (Tor 3, Anleitung, Kapiteltitel mit Einzelwort): anleitung_bau.py hängt die letzten zwei Wörter jedes Kapiteltitels mit festem Leerzeichen zusammen («So ist das ⏎ Markenbuch aufgebaut.», «In den ⏎ Hausregeln nachschlagen.»). anleitung.html neu gebaut (sha1 7a1bf5a38d), bau.py gelaufen. Alle Titel (h1, h2) bei 1440, 1280, 1000 und 390 gemessen: kein Einzelwort, kein Überstand. Sicherungen `*.vor-fundR-2026-10-30`.
- R, zweiter Anlauf (Tor 3): Das Kleid teilt Titel beim Auftritt in Wort-Blöcke (WO_ZEILEN); zwischen den Blöcken brach auch das feste Leerzeichen um, und die zweite Zeile begann mit diesem Leerzeichen (eingerückt). Jetzt stehen die letzten zwei Wörter in einem Teil mit white-space:nowrap. Gemessen an den gerenderten Titeln mit laufender Bewegung (Range.getClientRects) bei 1440, 1280, 1000 und 390: kein Einzelwort, keine Einrückung. Stempel anleitung.html sha1 18d8b287a2. Sicherungen `*.vor-fundR2-2026-10-30`.
- S (Tor 3, Logo & Dateien → Schriften): Muster mit Trenner («LAUCH / BLUMENKOHL / CHIPOTLE», «Haasemannstraße 13 · 30449 Hannover») in ganze Glieder geteilt; der Trenner steht nur zwischen zwei Gliedern derselben Zeile (am Zeilenanfang abgeschnitten), nie im Wort gebrochen (overflow-wrap normal). Beschreibung: Bereich und Werte untereinander statt mit «·», letzte zwei Wörter fest verbunden, ebenso im Lesetext-Muster. 901–1320 px: Probe links über zwei Reihen, Muster oben über die volle Breite, Name/Text und Knopf darunter. Gemessen alle vier Zeilen bei 1440, 1280, 1100, 1000, 901, 390: kein Einzelwort, kein Überstand, nichts ragt aus der Zeile; am Bild 1440, 1280, 1000, 390. Kurz (rund 2 Min.) startete das Markenbuch nicht (Namensgleichheit «teile»), behoben. Sicherungen `*.vor-fundS-2026-10-30`.

## Tor 3 Fund T (30.10.2026): Rahmen-Beschriftung im Foto-Fenster
- Beschriftung des Ausschnitt-Rahmens bleibt im Rahmen und frei vom runden Zurück-Knopf (`beschrifte()` in livre.js, `--lt` + `white-space:pre` in livre.css).
- Passt sie nicht in eine Zeile: Name und Mass untereinander, ohne Trenner; bei der Story am Handy das Mass zusätzlich in zwei Zeilen («1080 auf» / «1920 px»). Liegt der Rahmen unter dem Knopf, rutscht sie unter ihn.
- Geprüft «Am Pass werden die Teller angerichtet», alle vier Grössen, Rahmen mittig, ganz links, ganz rechts: 390 und 1440 (dort einzeilig wie bisher), kein Treffer am Knopf, nichts über den Rahmen hinaus.
- Stempel: livre.js?v=c683ee6b6e, livre.css?v=eb1e39426a. Sicherungen `*.vor-fundT-2026-10-30`.
