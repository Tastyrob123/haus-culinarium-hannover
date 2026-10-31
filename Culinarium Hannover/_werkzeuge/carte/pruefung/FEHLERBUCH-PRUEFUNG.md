---
tags: [projekt, website]
status: aktiv
---

# La Carte · Culinarium · Fehlerbuch 10a Zeile für Zeile (28.10.2026)

Gelesen: Werkzeug-Master Abschnitt 10a ganz (181 Zeilen). Hier jede Zeile, die La Carte, Karten-PDFs oder «alle Werkzeuge» betrifft, mit Nachweis am Culinarium. Zeilen zu L’Imprimerie, Le Registre, La Réception, Werkbank, Feeds und Website-Seiten anderer Häuser betreffen dieses Werkzeug nicht.

| Fehlerbuch (Haus, Datum) | Regel | Am Culinarium |
|---|---|---|
| Schäfli 21.10. Demo-Check: Reparaturen des Schlössli fehlten | Reparaturen eines Demo-Checks in jedes kopierte Haus | Kopie aus dem Schäfli **nach** dessen Demo-Check (Zur Werkbank mit `wbo`, Ansicht Website je Karte, Abschnitts-Ziele, Anleitung, Demo-Sperre) – alle sechs Punkte im Code nachgesehen und bedient (`R19`, `C07`, `S01`) |
| Schäfli 21.10. Wege «Auf der Website» | Sprungziele gegen die gebaute Seite prüfen, jeden Link aufrufen | Website-Ansicht öffnet `#ad-<Plakat-ID>` per `data-abend` der gebauten `abende.html` (`C07`); alle Links in Kopf und Rand 200 (`R05`) |
| Schäfli 21.10. Le Bureau: Daten unter `assets/daten/` gesperrt | jede Seite der Vorschau mit Konsole und Netz lesen | Website-Ansicht: abende.html, abend.html, index.html geladen, keine toten Adressen (`A99`) |
| Schlössli 19.10. Karten schwächer als das Original | auf dem Original aufbauen, nie schwächer | Grundlage ist die gedruckte Karte am Platz (Foto 22.02.2025): Wortmarke, Gang, Teller in Versalien, Drink klein, Strich zwischen den Gängen; verfeinert in Fraunces/Instrument/Urbanist/DM Mono und Kerze; Bild `pruefung/karten-alle.png` |
| Schlössli 19.10. halbleere Seiten | jede Seite gefüllt oder zusammengezogen | kurze Karten (Juli/Nov 2024) werden bis 180 % eingepasst, Wortmarke wächst nur bis 112 %; mittig, kein leerer unterer Teil (`C08`-Messung) |
| Schlössli 19.10. Kürzelketten, Menüpreis als Satz in Klammern, Menü wie Rubrik | Menüpreis als Marke, Menü mit eigenem Kopf | Ticketpreis als Marke (Angabe klein, Zahl in Fraunces, Währung DM Mono, Linien), Kopf mit Wortmarke, Titel, Datum, «BY MOMO X RUDI» |
| Schlössli 19.10. Idee kopiert die Machart nur | Eigenheiten prüfen und besser lösen | «|» der gedruckten Karte in Rudis Tellern als « / » wie in Rudis Beiträgen; «•••» zwischen Teller und Drink durch das «x» von «Momo x Rudi» ersetzt; Absacker ohne Teller ohne «x» |
| Schlössli 19.10. zwei Titel derselben Ebene verschieden | gleiche Ebene gleich gesetzt | alle Gänge, Teller, Drinks einheitlich (Klassen `sb-gn`, `sb-n`, `sb-dr`) |
| Schlössli 20.10. Kartenpult Vorschau-Fenster ungleich hoch / Fortgeschritten Seitenleiste | Kacheln bündig, Seitenleiste bis unten | aus dem Vorbild unverändert, Bilder 1440 angesehen |
| Schlössli 20.10. Wer arbeitet hier? | keine Abfrage, fester Eintrag | «Team Culinarium» (`F10a`) |
| Schlössli 20.10. Plus-Knöpfe ohne Körper | Knöpfe des Rahmens | `F10a` «Gang am Ende» mit Körper und Knauf |
| Schlössli 20.10. Knöpfe schweben über Bild und Text | eigene Zeile unter dem gewählten Eintrag | `F10a` |
| Schlössli 20.10. Verlaufsfläche fremder Farbe hinter Kreisen | runde Knöpfe frei, keine fremde Farbe | `F10a`; alle Farben des Schäfli umgefärbt (Liste in `carte.css`/`tafel.css`), Suche nach `#B38346`, `#7D433A`, `Petrona`: keine mehr |
| Schlössli 20.10. untere Leiste (Satz, ausgegraute Knöpfe, eine Quelle) | nur wirksame Knöpfe, ein Zustand | `R12`, `F10a` Leiste |
| Schlössli 20.10. Titel der Leiste überdeckt Knopf | Platzregel | `leistePasst()` aus dem Vorbild; 390-Lauf ohne Verrutschen |
| Schlössli 20.10. Kapitälchen als zwei Texte | ein Feld = ein Text | im Culinarium keine Kapitälchen; Teller ist ein Text |
| Schlössli 20.10. Knopfzeile bricht irgendwo um | feste Umbruchstelle | aus dem Vorbild, Bild 390 angesehen |
| Schlössli 20.10. Kopf: Titel schiebt sich über Knöpfe | Titel nimmt nur freien Platz | längster Titel «Das erste Culinarium-Wochenende» bei 1440 und 390 geprüft (`R07`, Bilder) |
| Schlössli 20.10. Bilder in jeder Liste | jede Liste mit Bild, kein Foto doppelt, nur Fotos, die das Gericht zeigen | Kacheln mit Plakat je Abend; in der Liste trägt der Titel das Plakat einmal, Gänge ohne Foto (es gibt kein Foto dieser Teller) |
| Schlössli 21.10. Wege zu anderen Werkzeugen auf falschem Server | jeder Link aufgerufen | Ports aus `WO_HAUS.ports`, 127.0.0.1; `R05` ruft alle auf |
| Schlössli 21.10. schwebender Knopf «Zur Werkbank» | Ziel aufrufen | `R19`: 127.0.0.1:9088/werkbank/ → 200 |
| Schlössli 21.10. Ansicht Website bleibt beim Kartenwechsel | Kartenwechsel → Seite der Karte | `C07` Kartenwechsel öffnet den neuen Abend |
| Schlössli 21.10. Kopfbild am Handy: langes Wort | Titel bei 390 gemessen | Bild 390 «Der nächste Abend», «Das erste Culinarium-Wochenende» |
| Schlössli 21.10. Anleitung nicht nachgezogen | Anleitung im selben Zug | `anleitung.html` neu für das Culinarium (Abende, Teller, Drinks, Demo, Stichwörter) |
| Schlössli 21.10. Titel nur aus Satzzeichen | ganzer Wortlaut | Absacker ohne Teller zeigt «Absacker», Ticket «Ticket» |
| Schlössli 21.10. Fehlerlisten vor Demo | Fehlerlisten leeren | echte Daten: keine Fehlerliste (Prüfläufe nur mit Wegwerf-Daten) |
| Schlössli 21.10. Zentrale relativ verlinkt | Zentrale auf ihrem Server, 127.0.0.1 | Knopf La Maison → http://127.0.0.1:9081/_werkzeuge/maison/ (`R05`) |
| Schäfli 21.10. variable Schriften im PDF (Type 3) | feste Schnitte, `pdffonts` | `fonts_statisch.py` (Fraunces SOFT 100 in drei Schnitten, Instrument, Urbanist, DM Mono); `pruefe.py schrift`: kein Type 3 |
| Querprüfung 21.10. Demo-Sperre | Datei `DEMO`, Prüfsumme der Website vorher = nachher | `DEMO` liegt; Einschalten → 409 DEMO (`S01`); Läufe schreiben nur in Wegwerf-Ordner; `website/` nie geschrieben |
| Schäfli 24.10. Online-Druck kannte fremde Karten | `ZIELE` online = lokal | Online-Teil nicht übernommen (nichts online), Hinweis in `online.json` |
| Schäfli 24.10. `fetch` ohne `.catch` in der Website | Website-Ansicht beim Wechsel | Website nicht Revier; Wechsel der Seiten in der Ansicht ohne Konsolenfehler (`A99`) |
| Rundgang-Schild wandert | Schild fest | `rundgang.js` aus dem Schäfli (mit Reparatur) |
| Kacheln gleichmässig in Reihen | höchstens vier, Rest mittig | Rand als Liste, keine Kachelreihen im Werkzeug |
| Abschnitt 9: gesperrte Versalien ≤ .08em | pdftotext liest ganze Wörter | Teller .06em, Etiketten .08em; `pruefe.py schrift` ganze Wörter |
| Abschnitt 9: zsh teilt Variablen nicht | `${=c}` | beim ersten Prüflauf selbst getroffen, mit `${=m}` behoben |
| Abschnitt 9: Gestalten-Farben und -Schriften im Server | `LAGE_WAHL` = SATZ | `LAGE_WAHL` = Schlüssel von `SATZ.SCHRIFT`/`SATZ.FARBE`; `pruef/gleich.js` speichert eine Gestaltung (Kerze, DM Mono, Versalien) |
| Abschnitt 9: Flächen im Satz dürfen nicht schrumpfen | `flex:1 0 auto` | `.sb-quer` |
| Abschnitt 9: Datum auf Bildern | keine feste Zeitzone | Aufnahmen ohne `timezoneId` |

Neu gefunden am Culinarium (allgemein, an den Oberchef gemeldet und in Master 10a/9 eingetragen):
1. **Absacker als Vorlage:** «Neuer Eintrag» kopierte den letzten Eintrag einer Karte; ist das ein Gang ohne Teller (oder der Preis), fehlt im neuen Eintrag das Feld. Regel: Vorlage für neue Einträge ist der letzte Eintrag mit allen Feldern seiner Art.
2. **Silbentrennung am Bindestrich und pdftotext:** «FETA-» am Zeilenende liest pdftotext als «FETAKÄSE»; Wortvergleiche zählen Bindestriche auf beiden Seiten nicht, Teller bekommen `text-wrap:balance`.
