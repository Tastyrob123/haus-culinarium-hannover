---
tags: [projekt, website]
status: aktiv
---

# Fehlerbuch 10a gegen La Réception · Culinarium Hannover (28.10.2026)

Jede Zeile des Fehlerbuchs (Werkzeug-Master 10a), die La Réception, «alle Werkzeuge», den Rundgang, Prüfseite oder Anleitung betrifft, am Culinarium-Stand nachgesehen. Beleg = Schritt im Prüflauf (`culinarium.js`, `zusatz.js`, `democheck.js`, `breiten.js`, Protokolle in `lauf/`) oder Bild in `bilder/`. Zeilen anderer Werkzeuge (La Carte, Le Livre, Le Registre, L’Imprimerie, Werkbank, Feed, Weinberater) betreffen dieses Werkzeug nicht.

| Fehlerbuch-Zeile (Kurzform) | Stand | Beleg |
|---|---|---|
| Chat ausprobieren: Spalte mit fester Zeile, nur die Liste im Gerät rollt; zehn Fragen hintereinander | erfüllt | `democheck.js`: 14 Gästefragen nacheinander, Eingabefeld bleibt sichtbar |
| Probe-Antwort sagt «Demo» in Alltagssprache, nie Schlüssel/Guthaben | erfüllt | `probe_ki.py`, `democheck.js` prüft «Schlüssel|API|Claude» = 0 |
| Kontakt des Gastes reiner Text, kein mailto/tel im Werkzeug | erfüllt | `culinarium.js` «Kein Mailprogramm …», `democheck.js` Links, Kai Brandt mit Telefonnummer als Text |
| Zeichen im Knauf mit `wo-ic`, gleich gross | erfüllt (aus dem Schäfli übernommen, `woKn`) | Bild `chromium-1440-start.jpg` (Anleitung-Knauf) |
| Kopftitel nimmt nur freien Platz, überdeckt nie einen Knopf | erfüllt | `breiten.js` (390 bis 1440, jede Ansicht) |
| Bilder in jeder Liste, gross genug, kein Foto zweimal untereinander | erfüllt | `culinarium.js` «Bilder in jeder Liste»: Eingang 7, Gefragt 10, Nachgetragen 3, Wissen 6; je Art mehrere Fotos |
| Titelzeile auf dunkler Fläche hell, Betonung aus der Schriftstärke | erfüllt | `breiten.js` misst die Farbe des Bühnentitels; Kleid `culinarium.css` |
| Dunkle Arbeitsflächen nur Töne des Kleids; unter der Bühne ≥ 30 px Luft | erfüllt | Farben über `_bau/culinarium_kleid.py` in die Töne Nacht/Schiefer gerechnet; Abstand aus dem Schäfli (34 px) |
| ≥ 16 px zwischen Schrift und Kachel/Schild | erfüllt | `culinarium.js` «Eingang ruhig gesetzt»: 18 px |
| Angaben in Gruppen (Wann · Gast · Woher), Wörter nie mitten getrennt | erfüllt | Bild `chromium-1440-eingang.jpg`: Tag · Zeit · Plätze, Kontakt · Sprache · Für die Küche, Woher als Zeile |
| Zitat nur, was der Gast schrieb; Formular als Liste; Karte nicht gestreckt | erfüllt | `culinarium.js`: Rest 26 px; Warteliste-Anfragen ohne Zitat, Angaben als Liste |
| Chat-Antworten gesetzt (Absender, Absätze, Liste mit Stichwort) | erfüllt | `antwortHTML()` unverändert aus dem Schäfli; Bild `chromium-1440-gefragt.jpg` |
| Karteikarten: Etikett 10 px, Blöcke 22 px | erfüllt (Stamm-CSS unverändert) | Bild `chromium-1440-nachgetragen.jpg` |
| Rundgang-Schild steht fest, wandert nie | erfüllt | `culinarium.js`: Schild 0 px |
| Brief «Nur Text» = «Gestalten» (Schrift, Linien, Betreff bricht um, Felder ohne Rahmen) | erfüllt | `culinarium.js`: Textarea, 3 Zeilen, Rand 0/0, transparent, Stärke 400; Bild `chromium-1440-nurtext.jpg` |
| Jede Ansicht bei 920/1000/1024/1100/1240 ohne Überragen (jedes Element) | erfüllt | `breiten.js` |
| Werkzeug-Titel bei 390 gegen das Kopfbild | erfüllt | `breiten.js` 390 |
| Anleitung nennt nur, was im Werkzeug steht, kein anderes Haus | erfüllt | `anleitung.html` neu auf Culinarium (Arten, Hinweise, Fotos, PDF-Name); Suche nach fremden Häusern leer |
| Bildadressen auch in CSS/`style` prüfen; Prüflauf zählt jede Netzantwort ≥ 400 in Anleitung und Prüfseite | erfüllt | `democheck.js` (Anleitung, Prüfseite); Fund im ersten Lauf: Bühne «Das weiss der Chat» zeigte auf `schild-1000.webp` (Foto des Schäfli), behoben → `schildnah` |
| Jeder Link in Kopf und Rand antwortet, Wege zu anderen Werkzeugen auf deren Server, nie localhost | erfüllt | `culinarium.js` «Jeder Link …»: Zentrale `127.0.0.1:9081`, Bureau 9082 … Druck 9087 je 200. Fund: der Kopf nahm `/_werkzeuge/maison/` relativ (auf 9084 ohne Server der Zentrale), behoben in `reception.js` |
| Seiten aus dem Werkzeug im Rahmen des Hauses (Name aus `WO_HAUS.namen`, Kleid) | erfüllt | `pruefung.html`, `anleitung.html` laden `kleid/culinarium.*` |
| Keine «Wer arbeitet hier?»-Abfrage, fester Eintrag «Team Culinarium» | erfüllt | `culinarium.js` (Namensabfrage 0), `WER = 'Team Culinarium'` |
| Prüfseite vor einer Demo: Fehlerlisten leeren, danach nochmal bedienen | erfüllt | `zusatz.js` «Prüfseite ohne Rot» nach den Läufen |
| Knöpfe im Arbeitsbereich mit Körper und Knauf, keine eigenen Knopfstile | erfüllt (aus dem Schäfli) | Bilder Eingang und Brief |
| Kacheln gleichmässig auf Reihen (≤ 4, keine allein) | erfüllt | «Nach Art»: vier Arten in einer Reihe (Bild `chromium-1440-start.jpg` unten) |
| «Zur Werkbank» nur aus der Werkbank, verdeckt nichts | erfüllt (Stamm aus dem Schäfli, Schlüssel `culinarium-wb`) | ohne Werkbank kein Knopf (`culinarium.js`, keine Konsolenfehler) |
| Nie fett, nie kursiv (Culinarium-Kleid) | erfüllt | Stile auf 400 gesetzt, Textart «Kursiv» im Brief entfernt; `culinarium.js` misst Betreff 400 |
| Falsches Datum auf Bildern (keine feste Zeitzone in Aufnahmen) | erfüllt | Aufnahmen ohne `timezoneId` |

Neu eingetragen in Master 10a (allgemeine Regel): siehe LIEFERUNG.md, Abschnitt «Lernen».
