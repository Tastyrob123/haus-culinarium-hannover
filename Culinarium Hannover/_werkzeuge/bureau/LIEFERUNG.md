---
tags: [projekt, website]
status: aktiv
---

# Das Schaufenster (Website pflegen, Arbeitsname Le Bureau) · Culinarium Hannover · Lieferung

**Status: fertig gebaut und selbst bedient, lokal. Nichts online, nichts verschickt.** Bau-Chat `culinarium-bureau`, 28.10.2026. Bauer ist nie Prüfer: die Abnahme nach Master 8 macht ein neuer Chat.

## Wo (Links, alle mit curl auf 200 geprüft)

- **Werkzeug:** http://localhost:9082/_werkzeuge/bureau/ · Server `python3 _werkzeuge/bureau/serve.py 9082` im Projektordner (läuft).
- **Ansicht Termine:** http://localhost:9082/_werkzeuge/bureau/?ansicht=e:termine
- **Anleitung:** http://localhost:9082/_werkzeuge/bureau/anleitung.html (neun Schritte, echte Bildschirme)
- **Prüfseite (R23, R04):** http://localhost:9082/werkzeuge/website/pruefung.html?haus=culinarium
- **Rundgang:** http://localhost:9082/_werkzeuge/bureau/?rundgang
- **Stand-Weg für den Tresen (Zentrale):** `GET http://localhost:9082/_werkzeuge/bureau/api/ueberblick` → `{aenderungen, zuletzt:{zeit}, bereiche, seiten, termine:{wartet, zahl}}` (an `culinarium-maison` gemeldet, dort eingebunden)
- **Website, wie «online» wäre (Probe-Kopie):** http://localhost:9082/werkzeuge/website/_probe/culinarium/online/index.html
- **Ordner:** http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/bureau/ · diese Datei http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/bureau/LIEFERUNG.md
- **Bilder für den Oberchef:** http://localhost:8978/haus/_Oberchef/zeigen/culinarium/bureau/bureau-uebersicht-1440.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/bureau/bureau-uebersicht-390.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/bureau/bureau-termine-1440.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/bureau/bureau-termine-390.png · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/bureau/bureau-vorher-nachher-1440.webp · http://localhost:8978/haus/_Oberchef/zeigen/culinarium/bureau/bureau-foto-tauschen-1440.webp
- **Name:** `_werkzeuge/oberflaeche/kleid/culinarium.js › namen.website` = «Das Schaufenster» (Robert 28.10.2026, Satz A «An der Bar»); Kopf, Titel, Startbild, Rundgang («Das ist das Schaufenster»), Anleitung und Prüfseite lesen ihn von dort, im Revier steht kein Name fest (geprüft: kein Arbeitsname mehr sichtbar). Hausname im Satz mit Artikel: «die Website des Culinariums».

## Was gebaut ist

Das Schaufenster ist der Schreibtisch des Stamms (`~/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website/`, Schicht über den gebauten Seiten) im gemeinsamen Rahmen von Culinarium (`_werkzeuge/oberflaeche/`, Rahmen «Die Bühne», Kleid von `culinarium-maison`), gleich aufgebaut wie Le Bureau des Schäfli, dazu die **Termine der Abende** als eigene Ansicht.

| Teil | Was |
|---|---|
| `beschreibung.py` → `_Werkzeuge/werkzeuge/website/haeuser/culinarium.json` und `_Werkzeuge/haeuser/culinarium/haus.json` | Beschreibung, **nie von Hand**: 9 Seiten aus dem Menü der gebauten Website, 8 Bereiche mit Foto (Startseite, Der Abend, Alle Abende, Das Haus, Team, Der Weg, Dirty Chicken, Rechtliches), Bereich des Hauses «Alle Abende» (14 Abende aus `abende.html`: Datum, Preis und Zusatz, Zeile, Plakat), Angaben aus dem Fuss von `index.html` gelesen (Telefon der Bar mit Link zum Anrufen, Strasse, PLZ/Ort, drei Instagram-Adressen), Zeiten & Preise mit «EUR», Google-Texte, eigenes Foto hochladen (`assets/bild`), ausgelassen: die Termine (eigene Ansicht), die Einzelbilder der Scroll-Filme und die freigestellten Leute im Team-Kopf (keine tauschbaren Fotos) |
| **Termine** (`termine.py`, `termine-ansicht.js`) | Die nächsten Abende stehen auf der Website als Daten (`website/assets/buchen.js › BEISPIEL`, gebaut von `website/buchen.py`), nicht als Text. Gelesen aus `buchen.js` (nie abgetippt, nie verändert); Entwurf, Stand, Verlauf in `_daten/termine.json` mit Sicherung `.gut`. Je Abend sein **Plakat** (Wortmarke, Datum, Akzentfarbe, «n frei»/ausgebucht), Datum als Auswahl im Hausstil (Tag, Monat, Jahr), Beginn, Preis, Plätze; «Neuer Abend» (Vorschlag: eine Woche nach dem letzten, dessen Zeit, Preis, Plätze), «Von der Seite nehmen», «Wie gespeichert», Vorher/nachher, Vorschau der Seite «Der Abend» 1440/390 und «Gross öffnen», Frühere Fassungen mit «Ursprünglicher Stand». Eingaben warten gelb in der Leiste, «Speichern»/Cmd+S und «Veröffentlichen» gelten für Termine und Texte zusammen. Ausgeliefert wird, indem der Server `buchen.js` der Probe-Kopie beim Ausliefern mit dem Stand füllt (ohne Änderung Byte für Byte wie gebaut, mit Änderung eigener Schlüssel im Browser-Speicher, damit eine alte Vorschau aus `termine-pflege.html` den Stand nicht überdeckt). Prüfung jedes Felds auf dem Server mit Stichwort (Datum, Zeit, Preis 1–999, Plätze 1–40 und nie unter den vergebenen, keine zwei Abende zur selben Zeit, höchstens 40), 409 KONFLIKT bei zwei Fenstern |
| Haken im Stamm (`website.js`) | `window.WS_EIGEN`: eigene Ansichten eines Hauses in Rand, «Häufig gebraucht», Leiste, Kopf, Lage-Platte, «Entwurf & Vergleich», Speichern und Veröffentlichen. Ohne `WS_EIGEN` keine Wirkung (Gegenprobe Gasterntal siehe unten). Dazu Zeiten & Preise erkennen «EUR». Sicherung `website.js.vor-eigene-ansichten-2026-10-28`. **Nicht committet**: in derselben Datei liegt eine fremde, nicht committete Änderung vom 24.10. (`gruppen()`, Aussen-Prüfung); Commit über den Oberchef |
| Rahmen (`index.html`, `bureau.css`, `fehlermelder.js`, `rundgang.js`, `zur-werkbank.js`, `schweben.*`, `anleitung.*`, `pruefung-haus.*`, `bau.py`) | aus dem Schäfli, auf Culinarium umgestellt: Kleid nur aus `--wo-*` (kein eigener Hexwert), Rundgang fünf Schritte mit «Die nächsten Abende», «Zur Werkbank» mit Schlüssel `culinarium-wb`, Fehlermelder an den Server, Prüfseite im Kleid mit Teil «Termine der Abende» und zwölf Lexikon-Einträgen der Termin-Stichworte, Anleitung neun Schritte mit echten Bildschirmen (`pruefung/anleitung_bilder.js`), Fassungsnummern aus dem Inhalt (`bau.py`) |
| `serve.py` | Rahmen um den Server des Stamms: `/assets/oberflaeche/` aus dem Rahmen, `/assets/` aus `website/assets/`, Termine-Wege, Vorschau des Entwurfs `/_werkzeuge/bureau/vorschau/`, Stand-Weg `ueberblick`, Wege zu den anderen Werkzeugen (9081 Zentrale … 9087, immer 127.0.0.1). Sicherheit: Host 421, fremde/fehlende Herkunft 403, nur JSON 415, über 3 MB 413 (Foto bis 36 MB), Grenze je Minute 429, Kopfzeilen gegen Einbetten, `.py` und `_daten` nicht abrufbar (`pruefung/sicherheit.txt`) |

## Wie geprüft (selbst, Bauer)

- **Bedient nach 4.2 und 8** (`pruefung/bedienen.js`, eigener Server, Wegwerf-Daten und Wegwerf-Kopie, unsichtbar, räumt auch bei Abbruch auf): **Chromium 1440 88/88 · Safari-Kern 1440 88/88 · Chromium 390 89/89 · Safari-Kern 390 89/89 · Chromium 320 89/89** (`pruefung/lauf-bedienen-*.log`, Bilder `pruefung/bilder/bedienen-*`). Darin u. a.: Angaben (Telefon an allen Stellen und in allen Links zum Anrufen), Prüfung beim Tippen und auf dem Server, `<script>`/Emoji/Umlaute, leer, 5'000 Zeichen, Google-Titel mit Zähler und Vorschau, Foto tauschen und eigenes Foto (400 px, PDF, 30 MB, Text als .jpg abgewiesen; 1600 px in vier WebP-Grössen), Netz weg beim Speichern (Meldung, Eingabe bleibt), **Termine**: vier Abende aus `buchen.js`, Preis ändern (gelb, Leiste), «Neuer Abend», 0 Plätze abgewiesen (Stichwort), «Von der Seite nehmen», Speichern mit Quittung, Speichern → neu laden → noch da, Vorher/nachher drei Zeilen, Vorschau zeigt Entwurf, Website noch alten Stand, 409, 30. Februar und `<script>` abgewiesen, fremde Herkunft 403, «Entwurf & Vergleich» nennt die Termine, Veröffentlichen zusammen mit Texten (Fenster nennt die Termine), Website liefert die neuen Termine, Ursprung zurückgeholt → `buchen.js` Byte für Byte wie gebaut; Stamm: Zurückholen auf den Ursprung → alle 9 Seiten Byte für Byte wie vorher; Rundgang, Fehlermelder, Handy-Rand schliesst nach der Wahl, S01/S03, **echte Website unverändert** (Prüfsumme aller Seiten und `buchen.js` vor/nach allen Schreibwegen; einmal rot, weil der Website-Chat um 12:18:50 alle Seiten neu gebaut hat, Wiederholung grün), keine Konsolenfehler.
- **Fehlerbuch nachgemessen** (`pruefung/masse.js`, echter Server, nur lesen): Chromium 93/93, Safari-Kern 93/93: zwölf Ansichten bei 390, 920, 1000, 1100, 1240, 1440 ohne Element über den Rand, Kopf-Titel deckt keinen Knopf; jede der 9 Seiten in der Vorschau, Anleitung, Prüfseite ohne Netzantwort ab 400 und ohne Konsolenfehler; alle Links in Kopf und Rand antworten, keiner auf localhost; «Zur Werkbank» nur aus der Werkbank (Ziel `http://127.0.0.1:9088/werkbank/index.html#werkzeuge`); Verlassen mit offener Termin-Eingabe fragt nach (R13).
- **Prüfseite** (`pruefung/pruefseite.js`): 18 Punkte des Stamms grün, Teil «Termine der Abende» grün, Sprung `#lex-termin-plaetze` öffnet den Eintrag, «Zum Werkzeug» führt zurück ins Bureau.
- **Flüssigkeit gedrosselt** (Regel 55, Chromium, Rechnerlast 35–37; `pruefung/fluss.json`, `fluss-termine.json`): Öffnen 106 / 257 / 399 ms (1× / 4× / 6×) · Scrollen Bildabstand p95 9,2 / 9,3 / 9,1 ms · Bereich Liste 44 / 130 / 196 ms, Seite in der Vorschau 110 / 255 / 330 ms · Zeiten & Preise 136 / 342 / 348 ms · **Termine** öffnen 114 / 479 / 730 ms, Tippen bis zur Leiste 18 / 36 / 70 ms, «Neuer Abend» bis gezeichnet 6 / 32 / 58 ms, Scrollen p95 9,2 / 9,1 / 9,2 ms. Gefunden und behoben: jedes Neuzeichnen lud die eingebettete Vorschau neu; jetzt bleibt sie stehen, solange der Entwurf gleich ist.
- **Gegenprobe Stamm** (anderes Haus, fester Lauf `pruef.js gasterntal land 1440`, eigener Port): 156 von 158, jede Funktion grün (`pruefung/gegenprobe-gasterntal.log`). Rot bleiben zwei Bau-Regeln, nicht aus diesem Bau: «im Code steht kein Haus» trifft einen Kommentar «Schäfli» in `website.js`, der schon im letzten Commit steht (meine Kommentare nennen kein Haus mehr); «kein ß» trifft `culinarium.json`, weil die Adresse in Hannover «Haasemannstraße» heisst (deutsches Haus, Wert von der Website). Vorschlag an den Oberchef: die ß-Regel im Stamm nur für Schweizer Häuser.
- **Hausfremde Angaben** (`grep` der Liste aus dem Auftrag): Treffer nur in Herkunftsvermerken der Code-Kommentare, nirgends sichtbar.

## Funktionskatalog (Master 4.2) · bedient

B Übersicht (Gruss, Lage-Platte mit Termin-Entwurf, sieben Kacheln 4 + 3 mit «Neuer Abend» zuerst, acht Bereiche mit Foto) · C Bereich im Umfang des Stamms (Stellen links, Seite rechts, Klick in die Seite, Ausblenden statt Löschen, Rechner/Handy) · D Foto tauschen und eigenes Foto · E Angaben mit «steht n× und als n Links auf m Seiten» · F Zeiten & Preise (mit EUR) · G: Culinarium hat keine Karte auf der Website, die das Kartenwerkzeug führt (Menü steht nur als Text), deshalb keine gesperrten Stellen · H Hinweis für Gäste (Text, Ab/Bis, Link) · I Google-Texte · J Sprachen: betrifft das Haus nicht (nur Deutsch) · K Entwurf & Vergleich (mit Termin-Block) · L Speichern bis Zurückholen (R09–R14, L13 zwei Fenster, auch für Termine) · M Prüfung (eigene Seite, Lexikon, Reparaturen) · **L19 Termine** (neu, Master 4.2).

Rahmen R01–R24: R01 Aufbau · R02 Auftakt (Rahmen) · R03 Fehlermelder (an den Server, geprüft) · R04 Startfehler-Tür (Stamm) · R05 Kopf mit Name aus der einen Stelle · R06 Rand mit Zahlen · R07 Handy, schliesst nach Wahl · R08 Leiste · R09 Speichern-Knopf ruhig/gelb/grün, Cmd+S · R10 nichts speichert still · R11 Quittung mit Rückgängig (auch Termine) · R12 Veröffentlichen mit Fenster und Notiz · R13 Verlassen fragt · R14 Frühere Fassungen mit Ursprung (auch Termine) · R15 letzte Ansicht gemerkt · R16 Bühne · R17 Bewegung (`schweben.js`) · R18 Rundgang · R19 Zur Werkbank · R20 Beispiele statt Leere (Termine leer, Vorher/nachher leer, Verlauf leer) · R21 hell mit Bühne, Auswahl und Datum im Hausstil · R22 kein Passwort · R23 Prüfseite · R24 Deutsch.

## Fehlerbuch 10a, Zeile für Zeile gegen das Schaufenster

| Zeile | Stand |
|---|---|
| Vorschau: jede Seite öffnen, Konsole und Netz | erfüllt (`masse.js`, 9 Seiten, Netz ab 400: keine) |
| Prüflauf schreibt nur in Wegwerf-Daten | erfüllt (Fehlerprotokoll und Termine unter `WERKZEUGE_DATEN`); echtes Protokoll ist leer |
| Kein Zeichnen vor dem ersten Stand | erfüllt (Stamm), Termine werden vor dem ersten Zeichnen geladen (`bereit`) |
| «Zur Werkbank»: eingebunden, Stücke frei (`data-ueber`, `data-neben`), Ziel auf dem echten Server | erfüllt (gemessen, Ziel 9088) |
| Jedes Werkzeug bei 920/1000/1100/1240 ansehen, nichts ragt hinaus, Kopf-Titel deckt nie einen Knopf | erfüllt (`masse.js`) |
| Hausname nie hinter festem Artikel | erfüllt (Suche «des/dem/im/vom Culinarium»: keine Treffer) |
| Wege zu anderen Werkzeugen: 127.0.0.1, Abruf 200 | erfüllt; Le Livre (9085) lief beim Prüfen noch nicht (Hinweis im Log) |
| Prüfseite im Rahmen des Hauses (Name, Kleid, kein Weltknopf, zurück ins Werkzeug) | erfüllt |
| Nach jedem Seitenbau Prüfung des Schreibtischs | `nachbau.py culinarium 9082` zweimal gelaufen («alles in Ordnung»); Anschluss-Zeile in `website/bau.py` fehlt (fremdes Revier, siehe offen) |
| Knöpfe des Stamms mit Abstand und Schrift der Rahmen-Knöpfe; Ansicht mit offenem Entwurf ansehen | erfüllt (Bilder «Entwurf & Vergleich» mit Entwurf) |
| Bildkacheln gemessen (> 40 px), alle acht mit Foto | erfüllt (vier Fotos nachgezogen, die der Stamm nicht fand) |
| Zeichen im Knauf mit `wo-ic` | erfüllt («Neuer Abend», «Auf der Seite ansehen» aus `WO.ic`) |
| Bilder in jeder Liste | erfüllt: Termine mit ihrem Plakat, Alle Abende mit Plakat (ein Abend 2023 hat keins, Website ebenso), Google-Texte je Seite eigenes Foto (Impressum, Datenschutz neu mit Foto), Bereiche mit Foto |
| Fenster mit klebenden Stücken `overflow:clip` | erfüllt (`zusatz_css`) |
| Dunkle Flächen nur Töne des Kleids | erfüllt (`bureau.css` ohne Hexwert) |
| Rundgang-Schild fest über der Leiste | erfüllt (Kopie unverändert in der Lage) |
| Knöpfe mit Körper und Knauf | erfüllt für Startbild-Knöpfe; Zeilen-Aktionen als Text-Links wie im Stamm |
| Keine «Wer arbeitet hier?»-Abfrage | erfüllt (Protokoll «Team Culinarium») |
| Leiste: eine Quelle, keine ausgegrauten Knöpfe | erfüllt (`leiste_klar`), zählt Termine mit |
| Fehlerlisten vor der Demo leeren | erfüllt (echtes Protokoll leer, keine Fehler) |
| Demo-Sperre für Schreibwege in die Website | betrifft das Bureau nicht (schreibt nur in die Probe-Kopie); Beleg Prüfsumme der echten Website vor/nach jedem Schreibweg |
| Anleitung mit jeder Änderung nachgezogen, nennt kein anderes Haus | erfüllt (neun Schritte, Bilder neu aufgenommen) |
| Bildadressen in Stylesheets beim Kopieren | erfüllt (`anleitung.css` Zeichen des Hauses) |
| Übrige Zeilen (Karten-PDFs, Feed, Weinkarte, Markenbuch, La Carte, La Réception, L’Imprimerie, La Maison, Werkbank) | betreffen das Schaufenster nicht |

Neu in den Master eingetragen (28.10.2026): **4.2 L19** (eigene Ansichten, Termine als Daten), **Erweiterungs-Log** L19, **10a** drei Zeilen (Anker im iframe rollt die Werkzeug-Seite; EUR und Film-Einzelbilder beim Anschluss eines Hauses; Prüfläufe räumen bei Abbruch auf).

## Offen (mit Grund)

- **Stamm-Commit:** `werkzeuge/website/website.js` und die neue Beschreibung liegen im Stamm-Git uncommittet, weil in `website.js` schon eine fremde Änderung vom 24.10. offen ist. Entscheid über den Oberchef.
- **Anschluss im Seitenbau:** eine Zeile am Ende von `website/bau.py` (`nachbau.py culinarium 9082`), damit die Probe-Kopie nach jedem Neubau nachzieht. `website/` gehört der Website-Prüfung bzw. Roberts Feintuning-Chat: Wunsch an den Oberchef. Bis dahin von Hand: `python3 ~/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website/nachbau.py culinarium 9082`.
- **Termine sind auf der Website eine Vorschau** (Robert 26.10.: Buchen nur simuliert). Das Bureau pflegt die Liste, die `buchen.js` zeigt; «vergeben» kommt aus der Liste und ist hier nicht änderbar. Mit einem echten Buchungsweg käme die Zahl von dort.
- **Rollen und Anmeldung** (5.3): kein Passwort bis zur Auslieferung (Robert 15.10.).
- **Hinweis für Gäste gestalten** (Farbe, Schrift) und **Fortschritt beim Veröffentlichen in Schritten**: hat der Stamm nicht (wie Schäfli).
- **Online:** nur lokal; in der Demo ist Veröffentlichen online aus (Robert 17.10.).

## Messlauf 30.10.2026 (Chat Messlauf/Querprüfung)

Umschalter (`.ws-wahl2`) und kleine Tasten (`.ws-taste`) mit Schrift auf Versalhöhe zugeschnitten (Höhe unverändert 34/36 px); Plakat-Fotos in den Fotokacheln einer Seite stehen ganz (Dirty Chicken «Pop up»). Bedienlauf: Chromium 1440 88/88, Chromium 390 89/89, WebKit 390 89/89; WebKit 1440 87/88 wegen «ResizeObserver loop» aus dem gemeinsamen Kleid (gemeldet an Tresen/Kleid, tritt auch mit der alten bureau.css auf). Start gedrosselt 1,65 s (Median aus 5, Fast 3G + CPU 4×), ungedrosselt 0,10 s.
Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/messlauf-2910/index.html
