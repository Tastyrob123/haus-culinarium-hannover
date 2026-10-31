---
tags: [projekt, website]
status: aktiv
---

# Lieferung Die Pairing-Karte (La Carte, Karten) · Culinarium Hannover (28.10.2026)

Geliefert (Bau, Chat `culinarium-carte`). Abnahme durch einen neuen Chat nach Master Abschnitt 8 offen. Name im Werkzeug kommt aus `_werkzeuge/oberflaeche/kleid/culinarium.js`: **Die Pairing-Karte** (Robert 28.10.2026, Satz A «An der Bar»; Arbeitsname La Carte, Ordner und Adressen bleiben `carte`).

**Werkzeug:** http://localhost:9083/_werkzeuge/carte/
**Anleitung:** http://localhost:9083/_werkzeuge/carte/anleitung.html · **Prüfung:** http://localhost:9083/_werkzeuge/carte/pruefung.html
**Alle Karten als Bild:** http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/carte/pruefung/karten-alle.png

## Was steht

- **Die Karte am Platz für jeden Abend.** Culinarium hat keine Speisekarte, sondern zu jedem Abend eine Menükarte: Gang für Gang Rudis Teller und dazu Momos Drink. La Carte führt
  - **Der nächste Abend** (C08/C24 in der Form des Hauses): sechs feste Gänge (Amuse Bouche, Apéritif, Vorspeise, Hauptgang, Dessert, Absacker), je Teller und Drink, Datum Freitag/Samstag mit Pfeilen, «Nächsten Abend anlegen», «Die Gänge stehen noch nicht fest», Motto, Zeile «BY MOMO X RUDI», Ticketpreis, Hinweis. Bis das Haus einträgt, steht dort beschriftet als **Beispiel** die Karte vom Februar 2025 (wörtlich aus der Website, nichts erfunden).
  - **Sieben frühere Abende**, jeder mit seiner Karte, so wie sie auf dem Tisch lag: 15./16.9.2023 (Das erste Culinarium-Wochenende, mit «Upgrade nach Wahl»), 22./23.9.2023 (Whisky und Rum), 17./18.11.2023 (Winter is coming), 26./27.4.2024 (Kabinett der Illusionen), 19./20.7.2024 (Erdig, nur der Apéritif lesbar), 29./30.11.2024 (Apéritif und Vorspeise lesbar), 21./22.2.2025.
- **Nichts abgetippt:** `karten_lesen.py` liest Gänge, Teller und Drinks aus `website/abende_info.py` (KARTEN, abgelesen von Fotos der gedruckten Karten) und Datum, Preis, «BY MOMO X …» aus `website/bau.py` ABENDE, beide als Text (ast, nie importiert). Zwei Prüfwege: Wort für Wort gegen die Quelle, jeder Teller/Drink/Preis gegen die gebaute `website/abende.html`.
- **Gesetzt im Kleid des Hauses** (`satz_bau.py`, `satz/satz.css`): Grundlage ist die gedruckte Karte am Platz (Wortmarke, Gang, Teller in Versalien, Drink klein, Strich zwischen den Gängen), verfeinert: Warmweiss mit Kante in Kerzenlicht, Wortmarke als nachgezogener Vektor (`marke.svg #wm`), Titel in Fraunces mit weichen Enden, Rudis Zeilen in Versalien mit Schrägstrich, Gang als Etikett in Urbanist, Datum in DM Mono, zwischen Teller und Drink ein ruhiger Punkt in Kerze (seit 30.10.2026, vorher ein «x»), Ticketpreis als ruhige Marke. Nie fett, nie kursiv. Feste Schriftschnitte (kein Type 3), Sperrung höchstens .08em.
- **Werkzeug** wie die Tafel des Schäfli (gleiche Wege und Funktionen, Master 4.3), Rahmen und Namen aus `_werkzeuge/oberflaeche/` (Kleid culinarium, Rahmen «Die Bühne»; Wege zu Tresen 9081, Schaufenster 9082 und den anderen aus dem Kleid): Einfach (Liste, Fenster, «So steht es auf der Karte») und Fortgeschritten (direkt in der Karte), Entwurf, Quittung, Rückgängig, Vorher/nachher, Probe-PDF, Veröffentlichen mit Wort-für-Wort-Prüfung, frühere Fassungen, Prüfseite, Export, Rundgang, Zur Werkbank (9088), Ansicht Website (öffnet auf «Alle Abende» das Fenster dieses Abends).
- **Eine Quelle für Karte und Website (C27):** jedes Veröffentlichen schreibt `anschluss/karten.json` in der Form von `abende_info.KARTEN` (je Abend Gang, Teller, Drink, Preis, dazu der nächste Abend). Kette Station 10: `_kette/10-kartenmacher/karten.json` (`python3 _werkzeuge/carte/web.py kette`).
- **Demo-Sperre:** Datei `DEMO` liegt. La Carte schreibt nie in `website/`; der Anschluss lässt sich nicht einschalten (409 DEMO).

## Starten und prüfen

- `python3 _werkzeuge/carte/serve.py 9083` → http://localhost:9083/_werkzeuge/carte/ (läuft)
- Karten neu aus der Website: `python3 _werkzeuge/carte/karten_lesen.py` (prüft selbst) → `python3 _werkzeuge/carte/satz_bau.py` → `python3 _werkzeuge/carte/einlesen.py` (ein Stand des Hauses wird nie überschrieben)
- `python3 _werkzeuge/carte/pruefe.py alles` (Rundlauf, Wortlaut der Drucke gegen die Quellen, Karten = Website, Schriften der PDFs; Server muss laufen) · `zsh _werkzeuge/carte/pruef/demo.sh` (Bedienungsprobe Chromium/WebKit 1440/390, Wegwerf-Daten auf 9089) · `node pruef/gleich.js chromium|webkit` (Vorschau = PDF, 9091) · `node pruef/fluessig.js chromium` (9090) · `node pruef/bilder.js` (Bilder für La Maison und Werkbank, 9092)

## Wie geprüft (28.10.2026)

- **Einlesen** (`karten_lesen.py`): 7 Menükarten aus der Website, Wort für Wort gegen `abende_info.py`, jeder Teller, Drink, Preis gegen die gebaute `abende.html`: gleich.
- **`pruefe.py alles`** (echte Daten, Server 9083): Rundlauf Satz → Baum → Satz 7/7 Zeichen für Zeichen gleich, nächster Abend mit allen 12 Tellern/Drinks, Datum und Preis im Blatt; Wortlaut jeder gedruckten Karte gegen ihre Quelle 8/8 gleich; Karten in der Form der Website = `abende_info.KARTEN` 7/7; Schriften aller PDFs: nur feste TrueType-Schnitte, kein Type 3, keine zerfallenen Wörter. GESAMT GRÜN.
- **Bedienungsprobe** (`pruef/lauf.js`, jede Funktion gedrückt, Wegwerf-Daten auf 9089, Website unberührt): Chromium 1440 170/170 · Chromium 390 168/168 · Safari-Kern 1440 170/170 · Safari-Kern 390 168/168 (Protokolle `pruefung/laeufe/`). Darin u. a.: alle 8 Karten ohne Überlauf und ohne seitliches Verrutschen, Klick links/rechts, Gang ändern/neu/kopieren/ausblenden/verschieben, Rubrik «Upgrade nach Wahl», Preisschreibweise, Speichern → neu laden → noch da, Rückgängig, Probe-PDF und veröffentlichte PDF = Daten, frühere Fassungen, Fortgeschritten (wählen, ziehen, ⌘Z, Pfeile, Gestalten, direkt schreiben), Ansicht Website (Fenster des Abends offen), der nächste Abend (Pfeile, anlegen, Gänge folgen, Küche veröffentlicht selbst), `karten.json`, Rollen 403, Demo-Sperre 409, Herkunft 403, 415, 413, 421, 429, Prüfseite, Export, Fehlermelder, Startfehler-Tür, Rundgang, Zur Werkbank (9088 → 200), alle Links in Kopf und Rand 200, zwei Fenster (KONFLIKT), Netz weg, 5'000 Zeichen, `<script>`, Emoji/Umlaute, Verlassen mit offenen Eingaben, keine Konsolenfehler, keine toten Adressen.
- **Vorschau = PDF** (`pruef/gleich.js`, mit Gestaltung an einem Gang und am Titel): Chromium und Safari-Kern grün (mittlere Abweichung 0,9–1,7 von 255).
- **Fehlerbuch 10a** Zeile für Zeile: `pruefung/FEHLERBUCH-PRUEFUNG.md`; Funktionsliste R01–R24, C01–C27: `pruefung/FUNKTIONSLISTE.md`. Jede PDF-Seite angesehen: `pruefung/karten-alle.png`.
- **Fremde Hausangaben** (Suche aus dem Auftrag im Revier): nur in Kommentaren, die die Herkunft der Vorlage nennen; nirgends sichtbar.

## Messwerte (Regel 55, 28.10.2026, Rechnerlast 8–9 durch die parallelen Chats, Werte eher zu hoch)

- Chromium ungebremst: Karte steht nach 100–113 ms, Tippen → Vorschau 16 ms, Scrollen Liste und Vorschau 120 Bilder/s (schlechtestes Bild 10 ms), keine langen Aufgaben.
- Chromium Prozessor 4× + Slow 4G: 4,3–4,4 s (Grenze 6 s), Tippen 38 ms, Scrollen 120 Bilder/s, keine langen Aufgaben.
- Chromium Prozessor 6× + Slow 4G: 4,4–4,5 s, Tippen 67 ms, Scrollen 120 Bilder/s, 2 lange Aufgaben (längste 80 ms).
- Safari-Kern ungebremst: 258–365 ms, Tippen 31 ms, Scrollen 60 Bilder/s (Bildtakt headless), schlechtestes Bild 19 ms.
- Bewegung nur `transform`/`opacity` (aus dem Vorbild, nichts Neues bewegt).

## Offen, mit Grund

- **Website liest La Carte noch nicht:** Die Menükarten auf `abende.html` kommen aus `website/abende_info.py`. Damit Änderungen in La Carte dort erscheinen, muss der Bau der Website `karten.json` vor `abende_info.KARTEN` lesen (Revier `website/`, nicht La Carte; mit Auftrag und ohne DEMO). Bis dahin bleibt jede Seite der Website Byte für Byte, wie sie ist (`pruefe.py website`: unveränderte Karten = Website).
- **Nächster Abend unbekannt:** Ein Termin nach dem 25./26.9.2026 ist nirgends angekündigt; deshalb steht das beschriftete Beispiel. Kein Datum, kein Preis erfunden.
- **Karten nur teilweise lesbar** (Juli und November 2024, je ein Teil auf dem Foto; Nov. 2023 mit «…» in Hauptgang und Drinks): so übernommen, wie die Website sie führt; die gedruckte Karte zeigt nur das Lesbare.
- **Abende ohne überlieferte Karte** (Okt. 2023, Silvester 2023, Jan. 2024, Feb. 2025 … Sep. 2026 ohne Fotos der Karte; Rudis einzelne Teller aus seinen Beiträgen): keine Karte, nichts ergänzt.
- **Online** nicht gebaut und nicht hochgeladen (Auftrag); `online.json` nennt nur Stand- und Prüfweg für La Maison.
- **Kette Station 10** liess sich nicht auf «läuft» setzen: Station 09 ist nicht von Robert bestätigt (nur mit `--trotzdem` auf Roberts Wort). Paket `karten.json` liegt trotzdem in `_kette/10-kartenmacher/`; `../../_karten/stand/` aus dem Paket gibt es nicht (Daten liegen in `_werkzeuge/carte/_daten/stand/`, Revier).
- **Sicherheit vor der Auslieferung** (Master 5.3): Anmeldung, Grenzen online, Sicherung ausserhalb, wie bei allen Häusern offen.
- **Firefox und 1366 × 650** nicht gelaufen (Auftrag: Chromium + WebKit, 1440 und 390).

## Bilder

`_werkzeuge/carte/bilder/la-carte-*.webp` (Safari-Kern, für La Maison und Werkbank) · Zeigen-Mappe `_Oberchef/zeigen/culinarium/carte/` (1440 und 390), z. B. http://localhost:8978/haus/_Oberchef/zeigen/culinarium/carte/la-carte-1440.png und http://localhost:8978/haus/_Oberchef/zeigen/culinarium/carte/la-carte-handy-abend-390.png · Alle Karten: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/carte/karten-alle.png

## Messlauf 30.10.2026 (Chat Messlauf/Querprüfung)

«Website ansehen» im Rand führt wie im Kopf auf die Startseite (vorher doppelt mit «Alle Abende auf der Website»); Knöpfe ohne Knauf gleichen die Sperrung aus, Etikett «Neu» auf Versalhöhe. Bedienlauf `pruef/lauf.js` nachgezogen (R05 erwartet die Startseite): Chromium 1440 170/170, alle vier Läufe davor 169/170 nur wegen dieser Zeile.
Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/messlauf-2910/index.html

## Messlauf 30.10.2026, zweiter Durchgang (Chat Gestaltung)

Titel der Listenzeilen umbrechen ausgewogen (kein «Kräuterbutter» oder «Kirchhorst» allein in der zweiten Zeile). «Website ansehen» steht zwischen 901 und 1240 px als runder Knauf 42 × 42 wie die Knöpfe daneben, nicht mehr als hohe Kachel 32 × 42 (Überschreibung in `carte.css`; das Kleid `culinarium.css:117–118` hat dieselbe Stelle für alle Werkzeuge). Messlauf Chromium und WebKit, 1440, 1280, 1000 und 390: 0 Fehler (82 Hinweise «gekürzt», Zutatenzeilen mit …).
Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/messlauf-3010/pairing-karte-gestaltung/tafel.html
