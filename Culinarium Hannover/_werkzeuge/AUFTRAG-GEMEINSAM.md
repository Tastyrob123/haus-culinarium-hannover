---
tags: [projekt, website]
status: aktiv
---

# Culinarium Hannover · Bilder, Werkzeuge, Werkbank, Prüfung — gemeinsamer Auftrag (Oberchef, 28.10.2026)

Robert, 28.10.2026, wörtlich: «Okay, die Kulinarium-Seite ist jetzt soweit für mich in Ordnung. Es gibt noch so ein paar Kleinigkeiten, wie Button vielleicht nochmal mittig setzen oder so. Aber das mache ich dann hinterher im Feintuning. Ich möchte, dass du jetzt Folgendes machst. Und zwar alles, was passiert, wenn die Website soweit fertig ist. Das heißt, Bilder schärfen, Werkzeugbank, Tools und du hast da ja für ein Protokoll für.»

Ablauf nach `~/Desktop/Website-Projekte/_Werkzeuge/OBERCHEF-PAKET.md`. Vorlage dieser Datei: `Taverne zum Schäfli Wigoltingen/_werkzeuge/AUFTRAG-GEMEINSAM.md` (21.10.2026), Hauswerte getauscht.

**Feintuning gehört Robert.** Kleinigkeiten an der Website (Knopf mittig o. ä.) macht Robert danach selbst mit seinem Website-Chat. Niemand baut daran vorab herum.

## Das Haus in drei Zeilen

Culinarium ist kein Hotel und kein Restaurant mit Tageskarte: Food-Pairing-Abende «Momo x Rudi» in der Bar Walk on the Wild Side, Hannover-Linden (Haasemannstraße). Rudi (Küche) richtet Gänge an, Momo (Drinks) stellt fünf Signature Drinks dazu und erklärt jeden; wenige Plätze an einer Tafel; jeder Abend hat sein eigenes Plakat. Dazu Rudis zweite Küche Dirty Chicken (eigene Seite `dirty-chicken.html`). Alles Weitere: `CHARAKTER.md` im Projektordner.

Für die Werkzeuge heisst das (Umsetzungsplan aus dem Master bleibt, Inhalt kommt aus diesem Haus): Karten = Menü und Drinks je Abend; Termine/Warteliste/Buchen = die Abende (siehe `website/termine-pflege.html`, `website/buchen.py`); Drucksachen = Plakate je Abend in der Plakat-Sprache des Hauses; Gäste-Chat = Fragen zu Abenden, Plätzen, Unverträglichkeiten. Fehlt eine Angabe: an den Oberchef, nie erfinden.

## Wer was macht (je Chat genau ein Revier)

| Chat | Revier (nur hier schreiben) | Port |
|---|---|---|
| culinarium-bilder | `_quelle/ki/geschaerft/`, in `website/bau.py` nur die Quellpfade in `BILD` (und `FILM`-Poster, falls geschärft), danach `python3 website/bau.py` | – |
| culinarium-website-pruefung | `website/` ausser Quellpfaden in `BILD`; Prüfordner `_qa/pruefung-2810/` | 8768 |
| culinarium-maison (Zentrale) | `_werkzeuge/maison/` **und** das gemeinsame `_werkzeuge/oberflaeche/` (einziger Schreiber) | 9081 |
| culinarium-bureau (Website pflegen) | `_werkzeuge/bureau/` | 9082 |
| culinarium-carte (Karten) | `_werkzeuge/carte/` | 9083 |
| culinarium-reception (Gäste-Chat-Team) | `_werkzeuge/reception/` | 9084 |
| culinarium-livre (Marke) | `_werkzeuge/livre/` | 9085 |
| culinarium-registre (Besuche) | `_werkzeuge/registre/` | 9086 |
| culinarium-imprimerie (Drucksachen) | `_werkzeuge/imprimerie/` | 9087 |
| culinarium-werkbank | `website/_werkbank/` | 9088 |
| culinarium-lernauswertung | Vault-Dateien der Tasty-Sprache, Master 11 / 10a, Design-DNA | – |

Projektordner: `/Users/robertreff/Desktop/Website-Projekte/Culinarium Hannover/` (kein Git, Worktrees schützen ihn nicht, immer absolute Pfade). Website lokal: läuft bereits unter http://localhost:8765/ (Roberts Server, `.claude/launch.json` «culinarium», nie beenden). Eigene Prüfserver nur auf dem eigenen Port.

## Chat-Namen zum Anschreiben (SendMessage)

`culinarium-bilder` · `culinarium-website-pruef` (Website-Prüfung, Name so gekürzt) · `culinarium-maison` · `culinarium-bureau` · `culinarium-carte` · `culinarium-reception` · `culinarium-livre` · `culinarium-registre` · `culinarium-imprimerie` · `culinarium-werkbank` · `culinarium-lernauswertun` (Lernauswertung, gekürzt) · Oberchef = der Chat, der euch gestartet hat. Im Zweifel `ListAgents`.

## Pflichtlektüre vor dem ersten Handgriff (ganz, nicht überfliegen)

1. `~/SecondBrain/04 Ressourcen/Design & Look & Feel/Werkzeug-Bau — Die sieben Werkzeuge (Master).md` — Abschnitt 3 (Rahmen), 4.x (dein Werkzeug, Funktion für Funktion = der Umsetzungsplan), 5 (Sicherheit), 6/6a/6b, 7 (Bauablauf), 8 (Abnahme), 9 (Fallen), **10a Fehlerbuch Zeile für Zeile**.
2. `~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md` (Abschnitte 5a Werkbank, 7a Sicherheit, 9, 11 Lernprotokoll, 13.5) und `Website-Briefing — Roberts Standard.md`.
3. `~/SecondBrain/04 Ressourcen/Design & Look & Feel/Tasty-Sprache — Boden und Charakter.md` (von Stufe 0 abwärts) und `~/SecondBrain/00 Kontext/Design-DNA — Vibe & Einflüsse.md`.
4. `CHARAKTER.md` des Culinarium (Geschichte, Register, Gegenstände, Marke, Bildbestand) und die Website selbst im Browser (headless): `index.html`, `abende.html`, `abend.html`, `bar.html`, `leute.html`, `weg.html`, `dirty-chicken.html`, `termine-pflege.html`, `impressum.html`, `datenschutz.html`. Die `*-wahl*.html` und `*.vor-*` sind Wahlseiten und Sicherungen, keine Website.
5. **Vorbild = Taverne zum Schäfli** (`~/Desktop/Website-Projekte/Taverne zum Schäfli Wigoltingen/_werkzeuge/<werkzeug>/` und `website/_werkbank/`), jüngster Stand mit Demo-Check (`DEMOCHECK.md`), `LIEFERUNG.md`, `FUNKTIONSLISTE*.md`, `*.vor-*`-Sicherungen (zeigen, was Robert beanstandet hat). Dahinter Wirtschaft am Schlössli. Technik-Referenz: Grand Beau-Rivage. **Alle drei nur lesen, nie ändern.**
6. Memory-Index `~/.claude/projects/-Users-robertreff-SecondBrain/memory/MEMORY.md`, besonders «Website & Design», «Bilder & Fotos» und die Werkzeug-Einträge (Fehlerbuch, Standards 17.10., Werkzeuge hell, Rundgang, Zur Werkbank, Anfragen ins Fenster, Namen je Haus, Websitetexte für Aussenstehende), dazu `~/.claude/CLAUDE.md` (Texte für Gastro: Wertigkeit, nie Masse; Hero gross).

## Kleid: Culinarium, nicht Schäfli umgefärbt

Gleicher Aufbau, gleiche Wege, gleiche Funktionen wie im Vorbild. Das Kleid kommt aus der Culinarium-Website (`CHARAKTER.md` Abschnitt 4 und `website/assets/*.css`): Nacht `#16141B`, Schiefer `#3A3845`, Warmweiss `#FAF4F4`, Kerze `#CF7233`; Dirty Chicken Violett `#8953A9` nur, wo es um Dirty Chicken geht. Fraunces mit weichen Enden (SOFT 100, wght 300–420) für Titel, Rudis Zeilen in Versalien mit Schrägstrich («LAUCH / BLUMENKOHL / CHIPOTLE»), Urbanist für Lesetext, DM Mono für Zahlen und Daten; nie fett, nie kursiv. Wortmarke nur der nachgezogene Vektor aus `_quelle/logo/nachgezogen/` bzw. wie in der Website verbaut. Das «x» von «Momo x Rudi», Kerzenlicht, die Plakate je Abend mit eigener Akzentfarbe. Mehr als Farbe tauschen (Master 3). Keine Einkerbungen, keine Punkt-Etiketten, keine Pillen-Reihen, nie basic, Kopf dunkel und Raum hell (Werkzeuge hell). Nicht wieder: warmweisses Band mit Doppelrahmen als Beschriftung (abgelehnt 26.10.).

Texte: Besucher kennen Rudi, Momo und das Konzept nicht (kein Insider-Wort ohne Erklärung). Jeder Satz wertet auf: Sorgfalt, Handarbeit, der einzelne Gast. Zahlen nur als Exklusivität (wenige Plätze), nie als Menge.

## Werkzeug-Namen

Bis Robert gewählt hat, Arbeitsnamen aus der Tabelle oben. Der Chat `culinarium-maison` legt drei Namenssätze vor (Funktionswort zuerst, Haus-Bezug dazu, je Werkzeug Name + ein Satz + Alternative; Welt der Bar und der Abende, nicht Grandhotel-Französisch übernehmen, nur wenn es passt) als Bildtafel in `~/Desktop/Website-Projekte/_Oberchef/zeigen/culinarium/namen-tafel.png` und meldet sie an den Oberchef. Namen nur in `_werkzeuge/oberflaeche/` (eine Stelle), die anderen lesen von dort.

## Feste Regeln für jeden Chat

- **Keine Fragen an Robert, keine Knöpfe.** Fragen zu Inhalt/Gestaltung und Ablauf gehen per Nachricht an den Oberchef-Chat. Nie um «weiter» bitten.
- Gebaut wird Roberts Auftrag und echte Fehler. Eigene Gestaltungsideen nur als Vorschlag mit Bild über den Oberchef.
- Daten nie abtippen: Namen, Preise, Termine, Menüs aus der Website (`website/bau.py`, `website/*.py`, `website/termine*`) bzw. den Originalen in `_quelle/` (`karte/`, `vom-kunden/`, `extern/`, `_kette/03-sammler/fakten.json`) lesen und dagegen prüfen. Preise nie raten: fehlt eine Zahl, bleibt sie offen und geht an den Oberchef. Keine fremden Hausangaben: am Ende `grep -rn -i "Beau-Rivage\|Interlaken\|Bottighofen\|Wigoltingen\|Schlössli\|Schäfli\|Kuchler\|Rivage\|Maeder\|Carlton\|Zurbriggen\|Doldenhorn"` im eigenen Revier, jeder Treffer muss gewollt sein.
- Nur eigene Zeilen ändern, vor dem Schreiben Änderungsdatum prüfen, nie ganze Dateien aus Sicherungen zurückschreiben. Sicherung vor jedem grösseren Eingriff (`*.vor-<was>-2026-10-28`). An `website/` arbeitet parallel Roberts eigener Website-Chat (Feintuning): Datei kurz vor dem Schreiben neu lesen.
- Nichts im Vordergrund auf Roberts Bildschirm öffnen. Browser nur headless (Playwright Chromium + WebKit), max. eine Instanz, eigenen Prozess sauber beenden, **nie pkill/killall auf Chrome, python oder online.py**, nie den Server auf 8765 beenden. mailto/tel in Tests abfangen, nie ausführen. Keine mailto-Wege in Werkzeugen (Formulare/Fenster).
- Lokal bauen und prüfen. **Nicht online stellen, nichts verschicken.** KI-Aufrufe in Prüfläufen mit Probe-Antworten (`ki=0`); Claude-API-Schlüssel nie benutzen.
- Flüssigkeit (Regel 55): gedrosselt 4×/6× messen, Werte notieren; nur `transform`/`opacity`.
- Kette: Station 08 führt `culinarium-bilder`, 09 `culinarium-website-pruefung`, 11 die Werkbank (Teile je Werkzeug setzen die Werkzeug-Chats mit `--teil <schlüssel>`): `python3 ~/Desktop/Website-Projekte/_Kette/kette.py stand "Culinarium Hannover" <nr> läuft` am Anfang, `"liegt vor" --notiz "…"` am Ende.
- **Fertig heisst:** jede Zeile aus Master 3 (R01–R24) und 4.x des eigenen Werkzeugs **bedient** (nicht nur geladen), Chromium + WebKit, 1440 × 900 und 390 × 844, keine Konsolenfehler, kein seitliches Verrutschen, Speichern → neu laden → noch da, Fehlerbuch 10a Zeile für Zeile gegen das eigene Werkzeug abgehakt. Belege in `<revier>/pruefung/`.
- **Lernen:** Jeder Fehler, den du findest, der für alle Häuser gilt: als Regel in Master 10a (Fehlerbuch) bzw. Website-Master 11 eintragen und dem Oberchef melden, damit er gegen die anderen Häuser gestellt wird.
- Am Ende: Bilder (1440 + 390) und eine Zeile nach `~/Desktop/Website-Projekte/_Oberchef/zeigen/culinarium/<revier>/`, `LIEFERUNG.md` im Revier (was steht, wie geprüft, Messwerte, offen mit Grund, **voller Link, nur localhost, nie `file:///`** (Robert 28.10.2026): eigener Server `http://localhost:<port>/…`, sonst Kette-Server `http://localhost:8978/haus/<Pfad ab Website-Projekte, Leerzeichen als %20>`; jeden Link vor dem Senden mit `curl` auf 200 prüfen), Meldung «fertig» mit Link an den Oberchef.

## Reihenfolge und Abhängigkeiten

- Bilder schärfen läuft zuerst. Die Werkbank baut Gerüst und Texte sofort, setzt Fotos aber erst ein, wenn `culinarium-bilder` «geschärft fertig» meldet (an Oberchef und Werkbank-Chat).
- `culinarium-maison` legt zuerst `_werkzeuge/oberflaeche/` an und meldet es den sechs Werkzeug-Chats; bis dahin lesen sie Pflichtlektüre und Vorbild und bauen ihre Daten-Schicht.
- Die Werkzeuge nehmen Fotos aus `website/assets/bild/` (Register `BILD` in `website/bau.py`), so kommen die geschärften automatisch nach.
- Die Werkbank bekommt die Bildschirme der Werkzeuge aus `<revier>/pruefung/` bzw. `zeigen/`; Kapitel «Ihre Werkzeuge» erst, wenn die sieben «fertig» gemeldet haben.
- Die Website-Prüfung arbeitet parallel, ändert keine Bildpfade (gehören dem Bilder-Chat) und nichts am Look.
- Die Lernauswertung beginnt sofort mit den bisherigen Culinarium-Chats (Website-Bau 25.–28.10.) und nimmt die neuen Chats am Ende dazu.
