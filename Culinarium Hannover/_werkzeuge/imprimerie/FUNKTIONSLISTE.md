# L’Imprimerie · Culinarium Hannover · Funktionsliste

Jede Zeile ist ein Handgriff, den `_qa/funktionen.js` am Werkzeug ausführt (Klick, Eingabe, Tastendruck, Download) und am Ergebnis prüft: dieselbe Liste wie beim Carlton (`Carlton-Europe Interlaken/_werkzeuge/imprimerie/FUNKTIONSLISTE.md`, 109 Zeilen) und damit wie im Grand Beau-Rivage. Gebaut von `_qa/liste_bauen.py`, Stand 28.10.2026 16:56. Prüfserver `python3 serve.py 9087`, Probe-Antworten statt KI, Wegwerf-Daten im Browser jedes Laufs.

- **Chromium 1440: 106 von 106**
- **Chromium 390: 103 von 105**
- **Safari-Kern 1440: 106 von 106**
- **Safari-Kern 390: 103 von 105**


## 1 Laden

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Laden 1: Startseite steht | ✓ | ✓ | ✓ | ✓ |
| Laden 2 (neu geladen): Startseite steht | ✓ | ✓ | ✓ | ✓ |
| Kopfzeile mit Name des Werkzeugs und Haus | ✓ | ✓ | ✓ | ✓ |
| Zurück zu La Maison (runder Knopf mit Haus) | ✓ | ✓ | ✓ | ✓ |
| Knopf Le Livre in der Kopfzeile | ✓ | ✓ | ✓ | ✓ |
| Suchfeld mit ⌘K | ✓ | ✓ | ✓ | ✓ |

## 2 Übersicht

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Begrüssung nach Tageszeit | ✓ | ✓ | ✓ | ✓ |
| Satz mit Datum | ✓ | ✓ | ✓ | ✓ |
| Feld «Zum Beispiel …» und Knopf «Fünf Entwürfe» | ✓ | ✓ | ✓ | ✓ |
| Verweis «N fertige Vorlagen in M Arten» | ✓ | ✓ | ✓ | ✓ |
| Anlässe der nächsten Wochen: eine grosse, drei Querkarten | ✓ | ✗ | ✓ | ✗ |
| Abteilungen des Hauses: Mosaik mit zwei grossen Kacheln | ✓ | ✗ | ✓ | ✗ |
| Zuletzt bearbeitet: Karten da | ✓ | ✓ | ✓ | ✓ |
| Kachel «Anlass» öffnet die Detailansicht | ✓ | ✓ | ✓ | ✓ |
| Detail: Zahl der Vorlagen = Zahl der Karten (+ weitere der Bibliothek) | ✓ | ✓ | ✓ | ✓ |
| Detail: Zurück-Pfeil führt zur Übersicht | ✓ | ✓ | ✓ | ✓ |
| Kachel «Abteilung» öffnet die Detailansicht | ✓ | ✓ | ✓ | ✓ |
| «Alle Anlässe & Events» führt zur Liste | ✓ | ✓ | ✓ | ✓ |
| «Alle Abteilungen» führt zur Liste | ✓ | ✓ | ✓ | ✓ |
| «Alle Medien» führt zu Meine Medien | ✓ | ✓ | ✓ | ✓ |
| Verweis «N fertige Vorlagen …» öffnet Arten und Vorlagen | ✓ | ✓ | ✓ | ✓ |

## 3 Seitenleiste

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Punkt «start» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Punkt «events» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Punkt «abteilungen» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Punkt «hinweise» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Punkt «newsletter» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Punkt «meine» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Punkt «freigegeben» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Punkt «neu» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Punkt «fotos» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Punkt «livre» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Punkt «marke» zeigt seine Ansicht | ✓ | ✓ | ✓ | ✓ |
| Zähler an den Punkten | ✓ | ✓ | ✓ | ✓ |
| Überfahren: Eintrag rückt nach rechts | ✓ | – | ✓ | – |
| Suche auf der Übersicht wechselt zu Meine Medien und filtert | ✓ | ✓ | ✓ | ✓ |
| «Neu erstellen» öffnet Arten und Vorlagen | ✓ | ✓ | ✓ | ✓ |
| Hilfe und Führung öffnet das Hilfemenü | ✓ | ✓ | ✓ | ✓ |

## 4 Anlässe & Events

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Bühne mit Foto über der Ansicht | ✓ | ✓ | ✓ | ✓ |
| Anlässe in Monatszeilen mit Monatsname | ✓ | ✓ | ✓ | ✓ |
| Keine leere Zeile rechts: jede Monatszeile füllt die Breite | ✓ | ✓ | ✓ | ✓ |
| Kachel öffnet Detail mit Foto als Bühne, Zahl und Motiven | ✓ | ✓ | ✓ | ✓ |
| Detail: Vorlage öffnet im Editor mit passendem Namen | ✓ | ✓ | ✓ | ✓ |
| Editor: «Übersicht» bringt zurück | ✓ | ✓ | ✓ | ✓ |

## 5 Abteilungen

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Bühne | ✓ | ✓ | ✓ | ✓ |
| Kacheln = Abteilungen des Katalogs | ✓ | ✓ | ✓ | ✓ |
| Jede Abteilung öffnet: Zahl = Karten (+ weitere) | ✓ | ✓ | ✓ | ✓ |

## 6 Hinweise im Haus

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Bühne und Karten | ✓ | ✓ | ✓ | ✓ |
| Hinweis öffnet im Editor, Beispielwerte statt Klammern | ✓ | ✓ | ✓ | ✓ |

## 7 Newsletter & E-Mail

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Versendbare E-Mails: Kacheln mit Foto | ✓ | ✓ | ✓ | ✓ |
| «Als Bild»: Vorlagen öffnen im Editor | ✓ | ✓ | ✓ | ✓ |

## 8 Meine Medien und Freigabe

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Bühne, Beispiele als Karten, «Neues Medium» | ✓ | ✓ | ✓ | ✓ |
| Beispiel öffnen: Editor mit Kopie | ✓ | ✓ | ✓ | ✓ |
| Freigeben-Dialog (Abteilungen wählen) → Schild und Zähler | ✓ | ✓ | ✓ | ✓ |
| Ansicht «Freigegeben»: je Abteilung eine Zeile mit Drucksachen | ✓ | ✓ | ✓ | ✓ |
| Umbenennen einer Drucksache | ✓ | ✓ | ✓ | ✓ |
| Kopie anlegen | ✓ | ✓ | ✓ | ✓ |
| PDF aus der Karte speichern (Download) | ✓ | ✓ | ✓ | ✓ |
| Löschen mit Rückfrage | ✓ | ✓ | ✓ | ✓ |

## 9 Arten und Vorlagen

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Arten als Blätter (Zahl je Art auf der Karte) | ✓ | ✓ | ✓ | ✓ |
| Gruppen-Filter (Zum Mitnehmen, Karten …) filtern die Arten | ✓ | ✓ | ✓ | ✓ |
| Direkt beschreiben: Feld und Knopf | ✓ | ✓ | ✓ | ✓ |
| «Alle N Vorlagen des Hauses durchsuchen»: Zahl = Bibliothek | ✓ | ✓ | ✓ | ✓ |
| Galerie: Suche, Art, Bereich, Grund | ✓ | ✓ | ✓ | ✓ |
| Galerie: Vorlage übernehmen → Editor | ✓ | ✓ | ✓ | ✓ |
| Art öffnen (Flyer): Format, Beschreiben, Vorlagen der Art | ✓ | ✓ | ✓ | ✓ |
| Art: Format wechseln setzt die Vorlagen neu | ✓ | ✓ | ✓ | ✓ |
| Art: «Zurück» führt zu den Arten | ✓ | ✓ | ✓ | ✓ |
| Leeres Blatt: Format wählen, Editor öffnet | ✓ | ✓ | ✓ | ✓ |

## 10 Fotos des Hauses

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Fotos als Raster mit Zahl | ✓ | ✓ | ✓ | ✓ |
| Bereichs-Filter und Suche | ✓ | ✓ | ✓ | ✓ |
| «Daraus gestalten»: Arten mit dem Foto in den Vorlagen | ✓ | ✓ | ✓ | ✓ |
| Foto lösen (×) bringt alle Arten zurück | ✓ | ✓ | ✓ | ✓ |

## 11 Le Livre und Marke

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Le Livre: drei Reiter (Bildarchiv, Dateien, Farben) | ✓ | ✓ | ✓ | ✓ |
| Le Livre: Farbe kopieren | ✓ | ✓ | ✓ | ✓ |
| Le Livre öffnen (Verweis) | ✓ | ✓ | ✓ | ✓ |
| Marke des Hauses: Farben, Schriften, Tapete, Regeln, Angaben | ✓ | ✓ | ✓ | ✓ |

## 12 Editor

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Editor öffnet, Blatt gesetzt | ✓ | ✓ | ✓ | ✓ |
| Reiter Entwerfen, Vorlagen, Fotos, Ablage | ✓ | ✓ | ✓ | ✓ |
| Gestalten-Leiste ist zu, bis etwas gewählt wird | ✓ | ✓ | ✓ | ✓ |
| Element wählen öffnet die Leiste «Gestalten» (Schrift, Grösse, Textart, Farbe) | ✓ | ✓ | ✓ | ✓ |
| Schriftart wechseln | ✓ | ✓ | ✓ | ✓ |
| Schriftgrösse in pt (+) ändert das Blatt | ✓ | ✓ | ✓ | ✓ |
| Textart Kursiv/Versal | ✓ | ✓ | ✓ | ✓ |
| Text direkt auf dem Blatt (Doppelklick) schreiben, Rückgängig | ✓ | ✓ | ✓ | ✓ |
| Wiederholen (⇧⌘Z) | ✓ | ✓ | ✓ | ✓ |
| Foto wählen (Fotos des Hauses) tauscht das Bild | ✓ | ✓ | ✓ | ✓ |
| Aufbau wechseln (alle Aufbauten) ohne Fehler | ✓ | ✓ | ✓ | ✓ |
| Grund wechseln (Marine, Papier, Creme) | ✓ | ✓ | ✓ | ✓ |
| Tapete (ohne, dunkel, hell) | ✓ | ✓ | ✓ | ✓ |
| Format wechseln (10 Formate) | ✓ | ✓ | ✓ | ✓ |
| Seite neu setzen | ✓ | ✓ | ✓ | ✓ |
| Rückseite anlegen, kopieren, löschen | ✓ | ✓ | ✓ | ✓ |
| Elemente hinzufügen (Titel, Text, Linie, Fläche, Rahmen, Zeichen) | ✓ | ✓ | ✓ | ✓ |
| Zoom und Schnittkante | ✓ | ✓ | ✓ | ✓ |
| Druckprüfung nennt Platzhalter | ✓ | ✓ | ✓ | ✓ |
| Speichern: pdf (Download) | ✓ | ✓ | ✓ | ✓ |
| Speichern: marken (Download) | ✓ | ✓ | ✓ | ✓ |
| Speichern: png (Download) | ✓ | ✓ | ✓ | ✓ |
| Speichern: json (Download) | ✓ | ✓ | ✓ | ✓ |
| PDF: Beschnitt 3 mm, Schriften eingebettet | ✓ | ✓ | ✓ | ✓ |
| Verwerfen fragt nach, danach Meine Medien | ✓ | ✓ | ✓ | ✓ |
| Editor: «Übersicht» sichert, Eintrag in Meine Medien | ✓ | ✓ | ✓ | ✓ |
| Le Livre im Editor: Fach öffnet (Fotos, Logo, Farben) | ✓ | ✓ | ✓ | ✓ |

## 13 Fehler

| Handgriff | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Keine Skriptfehler, keine Konsolenfehler | ✓ | ✓ | ✓ | ✓ |
| Keine Antworten ≥ 400 | ✓ | ✓ | ✓ | ✓ |
| Kein seitliches Verrutschen | ✓ | ✓ | ✓ | ✓ |

## Abweichungen im Einzelnen

- Chromium 390: Anlässe der nächsten Wochen: eine grosse, drei Querkarten · 333,333,333
- Chromium 390: Abteilungen des Hauses: Mosaik mit zwei grossen Kacheln · 5 Kacheln, 0 gross
- Safari-Kern 390: Anlässe der nächsten Wochen: eine grosse, drei Querkarten · 333,333,333
- Safari-Kern 390: Abteilungen des Hauses: Mosaik mit zwei grossen Kacheln · 5 Kacheln, 0 gross
