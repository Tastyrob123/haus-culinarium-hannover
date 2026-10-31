---
tags: [projekt, website]
status: aktiv
---

# La Maison · Culinarium Hannover · Funktionsliste (28.10.2026)

Master Werkzeug-Bau 3 (R01–R24) und 4.1 (M01–M27), je Zeile: Vorlage gesehen (Schäfli-Stube, `Taverne zum Schäfli Wigoltingen/_werkzeuge/maison/`) · hier bedient (Beleg). Belege: `pruefung/pruefe.js` (80 Zeilen, Chromium + WebKit, 1440 × 900 und 390 × 844, je 80 grün / 0 rot), `pruefung/democheck.js` (jede Kachel, jeder Link, aus allen sechs Werkzeugen zurück), `pruefung/fluss.js`, `pruefung/lauf/breiten.js`. Bilder: `~/Desktop/Website-Projekte/_Oberchef/zeigen/culinarium/maison/`.

## Rahmen (R) — La Maison ändert nichts, R08–R14 betreffen sie nicht

| Nr | Stand | Beleg |
|---|---|---|
| R01 Aufbau | sinngemäss wie jede Zentrale: Leiste, Empfang, Säle, Fuss, Tür, `aria-live` am Bühnenrahmen | Aufbau aus Vorlage, `bau.py seite()` |
| R02 Auftakt | Bühne und Plakate erst nach Dekodieren, kein Vorhang | pruefe «Laden: alle Stücke aufgetreten» |
| R03 Fehlermelder | `fehler.js` vor allem anderen, Schlüssel `culinarium_werkzeuge_fehler`, max. 20, Netzfehler nie | Code; Server nimmt `POST /studio/api/fehler` an |
| R04 Startfehler-Tür | «La Maison startet nicht.» mit Grund, «Prüfung öffnen» (Prüfseite Le Bureau) und «Neu laden»; Wache 12 s | pruefe «Startfehler-Tür öffnet bei fehlendem Skript» |
| R05 Kopfleiste | Insel mit Zeichen + Name, sechs Werkzeuge, Eck-Knöpfe «Anleitungen», «Website ansehen» | pruefe «Eck-Knöpfe ganz im Bild», «Leiste: Namen nie unter einem Knopf» |
| R06 Rand | in der Zentrale als Insel und Fuss (Wege, Anleitungen) | democheck: jeder Link 200 |
| R07 Handy | unter 1360 nur Marke; 390/320 ohne seitliches Verrutschen | breiten.js 320–1600: `scrollWidth` = Breite |
| R08–R14 | betrifft nicht (La Maison speichert und veröffentlicht nichts) | — |
| R15 Letzte Ansicht | aus der Zentrale geöffnete Werkzeuge starten auf der Übersicht; Zentrale selbst ohne Ansichten | — |
| R16 Bühne | Bühne im Empfang (Ruhe: Fenster der Bar am Abend), Säle mit Kopf, Zeichen, Titel | Bilder |
| R17 Bewegung | Takt der Häuser, nur transform/opacity, «Weniger Bewegung» steht sofort | pruefe «Weniger Bewegung: nichts verschoben» |
| R18 Rundgang | fünf Schritte, Schlüssel `rundgang-culinarium-maison`, `?rundgang`, nicht für Prüfprogramme | Code `rundgang.js` (gebaut) |
| R19 Zur Werkbank | `zur-werkbank.js`, Schlüssel `culinarium-wb`, nur mit Herkunft `wb/wy/wbo` | democheck Teil E: Werkbank → Tresen → «Zur Werkbank» zurück, grün (151/0 je Kern) |
| R20 / M27 Beispiele | Le Registre und La Réception mit beschrifteten Beispielwerten («Beispiel») | pruefe Stand-Zeilen |
| R21 Hell mit Bühne | Kopf dunkel nur in den Bühnen, Raum Warmweiss, Säle im Wechsel hell / Nacht | Bilder |
| R22 Kein Passwort | bis zur Auslieferung (Robert 15.10.) | — |
| R23 Prüfseite | La Maison verlinkt die Prüfseite von Le Bureau (Startfehler-Tür); eigene Prüfung = `pruefung/` | — |
| R24 Deutsch | ja, `lang="de"`, Datum `de-DE` | pruefe «Gruss morgen/tag/abend» |

## La Maison (M)

| Nr | Stand | Beleg |
|---|---|---|
| M01 Leiste als Insel | erfüllt, Namen nur, wenn sie zwischen die Eck-Knöpfe passen (`passt()`) | pruefe |
| M02 Eck-Knöpfe | erfüllt | pruefe |
| M03 Gruss nach Tageszeit, Datum ausgeschrieben | erfüllt (`?gruss=morgen|tag|abend`), Datum vom Gerät des Betrachters, keine feste Zone in Aufnahmen | pruefe «Gruss …» |
| M04 Empfang, je Werkzeug ein Bild | «Die Plakatwand»: sechs Plakate mit Fotos der Abende und Bar, je mit einer Abendfarbe der echten Plakate (`marke.json → abendfarben`) | Bild `maison-1440.png` |
| M05 Stand je Werkzeug, live | alle sechs antworten (Bureau «Alles veröffentlicht», Carte «8 Karten, alle veröffentlicht», Imprimerie «66 Vorlagen in 12 Arten» (live), Réception, Livre, Registre); ohne Antwort Satz ohne Zahl | pruefe «Ohne Antwort: Sätze ohne Zahl», democheck Stand-Zeilen |
| M06 Zahlenzeile | «Heute X Besuche · Y zum Platz · Die Besucherliste öffnen» im Textfluss (eine Grundlinie), «Beispiel» leise in der Datumszeile | Code, Bild |
| M07 Laufband | läuft nur im Bild, hält ausserhalb | pruefe «Laufzeile läuft im Bild / hält ausserhalb» |
| M08 Säle mit echten Bildschirmen | neun Bildschirme aus den Werkzeugen (WebKit, 1440 @2x, nur GET): Bureau ×2, Carte, Imprimerie, Réception ×2, Livre ×2, Registre | `schirme.js`, `pruefung/schirme.json` (10 ohne Fehler) |
| M09 Stücke fliegen herein, Platten | erfüllt; dazu drei Menükarten (aus La Carte), drei Drucksachen (aus L’Imprimerie), sechs Fotos im Saal Le Livre | Bild `maison-1440-ganz.png` |
| M10 Fuss | Wortmarke, «Momo x Rudi», Die Abende (Bar, Adresse aus `fakten.json`), Anleitungen (alle sechs), Fragen | democheck Links |
| M11 Rundgang | fünf Schritte, Texte fürs Culinarium | `rundgang.js` |
| M12 Taste 1–6 | erfüllt (still im Rundgang) | pruefe «Taste n öffnet das Werkzeug» (alle sechs grün) |
| M13 Zwei Fassungen | `online/` ohne localhost, ohne Platzhalter (Bau bricht sonst ab); Kacheln ohne Andock-Datei zur Werkbank | `bau.py baue()` |
| M14 Stand-Weg mit Ersatz, Tageswert | Liste erlaubt; «Heute» aus `je_tag` | Code |
| M14b Registre-Ersatzweg | nicht nötig: Le Registre liefert Beispielwerte selbst auf jetzt gekürzt (`ablage_heute`) | Meldung culinarium-registre |
| M15 Bilder spätestens beim Auftritt | erfüllt | pruefe «keine kaputten Bilder» |
| M16 Empfang als Wegweiser | Zeiger/Fokus zeigt Vorschau, harter Wechsel nach `decode()` | pruefe «Zeile n: Vorschau zeigt Werkzeug n», «Tastatur-Fokus» |
| M17 Stand L’Imprimerie | «66 Vorlagen in 12 Arten» (live gelesen) | democheck |
| M18 Monate in Kacheln | betrifft L’Imprimerie | — |
| M19 Archive laden sofort / Stand Registre | Kachel «477 Besuche in 30 Tagen · Beispiel» | Bild |
| M20 Fassung aus dem Inhalt; Knopf-Namen geprüft | `?v=` = Prüfsumme; jede «Knopf»-Angabe der Tafeln gegen den Code des Werkzeugs (`knoepfe()`): alle gefunden | Bau-Ausgabe ohne «nicht im Code gefunden» |
| M21 Kacheln sanft | heben nichts, Kante in der Abendfarbe, Foto zoomt ruhig | pruefe «Zeile n: nichts hüpft» |
| M22 Kopf | neu 29.10.2026: Zeile Wortmarke · Bar · Ort über «Der Tresen»; rechts Datum, Gruss, Kennzahlen als Block auf der Grundlinie des Titels; Linie schlicht, keine «x» | `_Oberchef/zeigen/culinarium/tresen-kopf-2910/` |
| M23 Vorschau statt Foto, nichts hüpft | erfüllt | pruefe |
| M24 Ecke oben links gleich | das «C» im Ring, Name, «Bereich · Haus», aus dem gemeinsamen Kleid | alle Werkzeug-Bildschirme |
| M25 Farben eine Reihe | Saal Le Livre aus `livre/livre.json` | Bild |
| M26 Demo-Hinweis verdeckt nichts | «Beispiel» als Zeilenteil im Fluss | Bild |
