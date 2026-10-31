---
tags: [projekt, website]
status: aktiv
---

# Werkbank Culinarium · Fehlerbuch Zeile für Zeile (Werkbank-Chat, 28.10.2026)

Quellen: Werkzeug-Master 10a (alle Zeilen mit Werkbank, Feed, Karten, Unterlagen, Drucksachen, Mails, «Zur Werkbank»), Website-Master 5a / 5b-neu / 11 (Werkbank-Einträge 17.–21.10.), Fehlerbuch-Abgleich der Schäfli-Werkbank (21.10.), Memory «Zur Werkbank», «Rundgang», «KI-Kosten nur auf KI-Seite», «Werkbänke nie gleich aufbauen», «Befund: vier Funde», «Werkbank-Angebot», AUFTRAG-GEMEINSAM.md.

| Regel | Stand Culinarium | Wie geprüft |
|---|---|---|
| Kapitel 1 Befund: nur die vier stärksten Funde, Satz zu allen, Rest hinter dem Knopf | ja: 01–04 aus dem Befund des Spähers (Culinarium hat keine Website und keine Potentialanalyse); «Von den 7 Punkten … die übrigen stehen im ganzen Befund»; eigene Befund-Seite `befund/` für Rudi, Momo, Derya (nicht die interne Kette-Seite) | Seite angesehen 1440/390, Bedienprobe Pfeil |
| Befund: höchstens zwei Bilder je Fund, keine Klickstrecke; kein Vorwurf, keine Mutmaßung | ja, je Fund Handy und höchstens ein Ausschnitt; Sätze nur aus Belegen (Beitrag, Profil, DENIC, Google Maps) | Text gelesen |
| Kapitel 8 ganzes Angebot (Was ihr bekommt, Umfang, Aufbau, Daten, Woche für Woche, «Ein Vorschlag.» + PDF, KI-Seite) | ja | Seite, `werkbank/karte.html`, PDF angesehen |
| KI-Kosten nie auf der Karte «Ein Vorschlag.» und nicht im PDF, nur auf `ki.html` | ja: Gang IV nennt je Stelle nur das Werkzeug | `pdftotext` der PDF |
| Kein Preis, kein Beispielpreis; der Bau «Den Betrag nennt ihr» | ja; Betreuung ohne Zahl und ohne Platzhalter (Robert 28.10.2026: «Kein Betrag auf der Werkbank, die Stelle bleibt ohne Zahl.»), als Gang III «Laufende Betreuung» | Karte, Kapitel VIII, `pdftotext` der PDF |
| Alle sieben Werkzeuge immer in der Werkbank, auch während ein Chat baut («Da fehlt ein Tool») | ja, alle sieben im Laptop; solange ein Chat baut, mit dem Stand seines Prüfservers | Bau-Protokoll, Bild Kapitel V |
| Reiter gleich viele je Reihe (4 + 3) | ja | Bild 1440 |
| Werkzeug-Bilder ohne Begrüßung oder Namensabfrage | ja (Rundgang-Schlüssel gesetzt, Besucherliste mit `?gruss=tag`) | alle Aufnahmen angesehen |
| Kein Versprechen, was ein Werkzeug nicht kann (Pairing-Karte schreibt nicht in die Website, nichts online) | ja: Texte zur Pairing-Karte und Szene «Einmal ändern» nennen nur Karte am Platz und PDF | Text |
| Werkzeug-Namen nur aus der einen Stelle, mit Artikel im richtigen Fall | ja: `kleid/culinarium.js` (Satz A), `namen_fall.py` («in der Pairing-Karte», «Den Tresen öffnen») | Text der gebauten Seiten durchsucht |
| Wege zu Werkzeugen immer 127.0.0.1, nie localhost | ja; auch wenn die Kette `localhost` meldet, setzt die Werkbank 127.0.0.1 (`rh_werkzeuge._weg`) | `grep localhost` in `werkbank/index.html`: 0 |
| «Zur Werkbank» in jedem Werkzeug über `wbo`, Ziel auf dem echten Server | Links tragen beim Klick `wb=de.<abschnitt>&wy=&wbo=http://127.0.0.1:9088` (`sb_skripte.WB_JS`); Ziel `/werkbank/index.html` von Bureau und Tresen bestätigt | Klickweg |
| Kein «Zur Werkbank» auf der Website | ja, keine Seite der Website nennt die Werkbank; die Werkbank fasst `website/` nicht an | `grep` aller neun Seiten: 0 |
| Wegweiser (Register) und Fuß nur mit Laptops, nie zwei gleiche Geräte nebeneinander | ja, alle Objekte Laptops oder Papier | `objekte_bau.py`, Register angesehen |
| Gestaltung des Kits in eigener Datei (`kapitel.css`) | ja | ganze Seite gescrollt |
| Roher Vorlagen-Code ({…}, undefined, NaN, None) nirgends sichtbar | ja | Text aller Seiten durchsucht |
| Feed eigen, Gegenprobe gegen alle bisherigen | ja, «Momo x Rudi» (feste Mittelspalte mit den Plakaten), `feed-bestand.md` | Tabelle |
| Feed: keine angeschnittenen Menschen, keine Schrift außer auf den Plakaten, keine gestapelten Bilder mit Text | ja, keine Menschen | Raster angesehen |
| Feed: gleicher Grundton nicht neben-/übereinander | ja, helle Teller nie übereinander | Raster angesehen |
| Karten wie die anderen aufgebaut (Seite «Heute und als Idee») | ja: zwei Karten von La Carte (Die Pairing-Karte) neben dem Foto der gedruckten Karte; nur eigene Fotos, keine Story mit Gäste-Namen | Unterlagen-Seite angesehen |
| Mails nie eigener Abschnitt, dritte Karte im Papier; Mail-Seite seitlich mit «Ganze Mail» | ja | Bedienprobe |
| Nichts öffnet ein Mailprogramm | ja, 0 mailto auf allen Seiten | `seiten_pruef.js` |
| Drucksachen aus dem Betrieb, keine Visitenkarte, kein warmweißes Band mit Doppelrahmen (abgelehnt 26.10.) | ja: Karte am Platz (es gab gedruckte Karten), Drink-Kärtchen, Ticket, Briefpapier; Untersetzer statt Sticker | Bilder angesehen |
| Logo nur, wie die Website es zeigt (seit 28.10. Rudis Original, vorher Platzhalter) | ja: Wortmarke aus `website/assets/zeichen/marke.svg` (aus dem Original gebaut), Datei unter «Dateien» = Original-SVG; Zeichen der Werkbank ist das «x» aus «Momo x Rudi» | Tafel, Drucksachen, Mails angesehen; kein «Platzhalter» und kein «nachgezogen» im Text |
| Keine Einkerbungen | ja, 0 Elemente mit «kerbe» | `seiten_pruef.js` |
| Kein Foto zweimal auf der Werkbank | ja: Auftakt, Brief, Worum, Marke (Markenbuch-Bilder), Fenster, Geprüft, Dateien, Feed-Abzüge, Schluss je eigene Fotos | Zuteilung im Code |
| Zwei Fenster mit verschiedenen Bildern und Sätzen zum Angebot, nie Gäste-Sätze | ja: «Ihr führt die Seite selbst.» · «Ein Abend, ein Auftritt.» | Seite angesehen |
| Keine Vorstellung Roberts, Brief nur, was stimmt (Auftrag, kein Geschenk) | ja: Brief an Rudi, keine Vorstellung (Rudi kennt Robert) | Text |
| Überschriften eigen je Haus (Werkbank-Regel 14) | ja, `TITEL_NEU` eigen, keine gleich wie Schäfli oder Schlössli | Liste |
| Anrede: Robert und Rudi duzen sich, Website im Du | Brief «Hallo Rudi», sonst «ihr/euch», deutsche Schreibung mit ß (`du_gang.py` mit Suchlauf); Rechtstext von Tasty Studios im Sie | `du_gang.py` Suchlauf: nur das Pronomen «Sie» bleibt |
| Texte für Gastro: Wertigkeit, nie Masse; Zahlen nur als Exklusivität | ja; der Rechner nennt Plätze und Preis nur für Rudi und Partner | Text gelesen |
| Titel nie fett, nie kursiv | ja (`ohne_fett`, Fraunces 340, `font-style:normal`) | CSS |
| Fremde Hausangaben | nur Herkunftsvermerke in Code-Kommentaren | `grep` aus dem Auftrag |
| Kein Live-Urteil der KI versprochen (Entwurf antwortet mit Proben) | ja, KI-Seite und Karte «Ein Vorschlag.» sagen es | Text |
| PDF ohne «Type 3» | ja (feste Schnitte, `druckschrift.py` setzt alle Achsen von Fraunces) | `pdffonts` |
