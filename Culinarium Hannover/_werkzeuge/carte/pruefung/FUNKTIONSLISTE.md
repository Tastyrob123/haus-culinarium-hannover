---
tags: [projekt, website]
status: aktiv
---

# La Carte · Culinarium Hannover · Funktionsliste (Master 3 und 4.3), 28.10.2026

Jede Zeile **bedient**, nicht nur geladen. Beleg = Prüfzeile der Bedienungsprobe `pruef/lauf.js` (Wegwerf-Daten, Prüfport 9089) in Chromium und Safari-Kern bei 1440 × 900 und 390 × 844; Ergebnisse in `pruefung/laeufe/`. «betrifft nicht» nur mit Grund.

## Rahmen (Master 3)

| Nr | Bedient wie | Stand |
|---|---|---|
| R01 Aufbau | `R01`: Kopf, Rand, Raum, Leiste, Fenster, Quittung mit aria-live, Kleid `culinarium`, Rahmen «Die Bühne» | erfüllt |
| R02 Auftakt | `auftakt.js` hält die Seite ruhig bis Daten, Schriften, Foto da sind; jede Ansicht ohne Konsolenfehler geöffnet (`A01`, `A99`) | erfüllt |
| R03 Fehlermelder | `R03`: Skriptfehler im Werkzeug kommt in `api/fehler` an und steht auf der Prüfseite | erfüllt |
| R04 Startfehler-Tür | `R04`: Status-Weg mit 500 → «La Carte startet nicht.» + «Prüfung öffnen» | erfüllt |
| R05 Kopfleiste | `R05` (3 Zeilen): Zeichen im Ring, Name aus dem Kleid, Haus, Titel der Karte, runde Knöpfe La Maison (127.0.0.1:9081), Prüfung, Anleitung, «Website ansehen» (Alle Abende); alle Links in Kopf und Rand antworten 200 | erfüllt |
| R06 Rand | `C01`, `C13`: zwei Gruppen mit Zwischentitel («Der nächste Abend», «Frühere Abende»), Marke «Entwurf», Wege | erfüllt |
| R07 Handy | `R07`: «Bereiche» öffnet, schliesst nach der Wahl; kein seitliches Verrutschen bei 390 auf jeder der 8 Karten | erfüllt |
| R08 Leiste | `R08`: «Entwurf: n Änderungen», «Alles veröffentlicht», gelb nach Ziehen | erfüllt |
| R09 Speichern-Knopf | `R09`: grün «Gespeichert», ⌘S auch aus der Vorschau | erfüllt |
| R10 Nichts still | `R10`: «Nichts geändert, nichts gespeichert.» | erfüllt |
| R11 Quittung | `R11`: Quittung mit «Rückgängig», «Vorher / nachher»; Rückgängig bedient | erfüllt |
| R12 Veröffentlichen | `R12`: erst «Vorher und nachher», Fortschritt mit 4 Schritten, ohne Entwurf kein Knopf | erfüllt |
| R13 Verlassen | `R13`: ungespeicherte Verschiebung → Browser fragt (Safari-Kern zeigt `beforeunload` in Playwright nicht, Ereignis gesetzt) | erfüllt |
| R14 Frühere Fassungen | `C12`: «Ursprünglicher Stand» + veröffentlichte Fassung, in den Entwurf holen | erfüllt |
| R15 Letzte Ansicht | `R15`: ohne Adresse die zuletzt gewählte Karte, aus La Maison die erste; Modus gemerkt | erfüllt |
| R16 Bühne | `R16` je Karte: Foto (Plakat des Abends bzw. die gedeckte Tafel), Zeichen, Titel | erfüllt |
| R17 Bewegung | `schweben.js` (nur transform/opacity, «Weniger Bewegung» respektiert), aus dem Vorbild unverändert | erfüllt |
| R18 Rundgang | `R18`: `?rundgang` mit Lichtkegel, vier Schritte über Abende, Teller und Drinks | erfüllt |
| R19 Zur Werkbank | `R19`: nur mit `?wb=`, Ziel http://127.0.0.1:9088/werkbank/ antwortet 200 | erfüllt |
| R20 Beispiele | «Der nächste Abend» zeigt als beschriftetes Beispiel die Karte vom Februar 2025 (wörtlich aus der Website, nie erfunden); «Frühere Fassungen» zeigt beschriftete Beispiele, solange nichts veröffentlicht ist | erfüllt |
| R21 Hell mit Bühne | Kopf in der Nacht der Bar, Raum Warmweiss; Auswahl, Schalter, Datum (Pfeile) im Hausstil, kein Datumsfeld des Systems (`C08`) | erfüllt |
| R22 Kein Passwort | fester Eintrag «Team Culinarium», keine Abfrage (`F10a`) | erfüllt |
| R23 Prüfseite | `C14`: Browser, Server, alle Karten, Druck, Sicherungen, Fehler, Reparaturen | erfüllt |
| R24 Sprache | Deutsch | erfüllt |

## La Carte (Master 4.3) in der Form des Culinarium

| Nr | Bedient wie | Stand |
|---|---|---|
| C01 | 8 Fotokacheln (Plakat je Abend), Modus Einfach/Fortgeschritten mit Satz, gemerkt | erfüllt |
| C02 | Gang ändern (Felder Gang, Teller, Drink), neuer Gang (Kopie eines vollen Gangs, Pflicht: Teller oder Drink), kopieren/abbrechen, ausblenden/zeigen, hoch/runter, Eintrag an der Rubrik «Upgrade nach Wahl», neue Rubrik, entfernen mit Nachfrage. Seiten verschieben: **betrifft nicht** (jede Menükarte ist ein Blatt); «Seite ausblenden» auf dem einzigen Blatt wird freundlich abgewiesen | erfüllt |
| C03 | Ticketpreis in der Schreibweise der Plakate: «85» → «85,00», «86,5» → «86,50», beim nächsten Abend «89» → «89,00 EUR» | erfüllt |
| C04 | Klick links ↔ rechts, Aufblinken, Doppelklick öffnet; gleiche Höhe, soweit die Vorschau scrollen kann (eine A4-Seite passt meist ganz in den Rahmen) | erfüllt |
| C05 | Fortgeschritten: wählen, ziehen mit Mass, ⌘Z/⌘⇧Z, Pfeiltasten, Gestalten (Schriften und Farben des Hauses, nur Normal/Versalien), Teil und Anordnung zurücksetzen, Doppelklick schreibt | erfüllt |
| C06 | Daten als Text, Ungültiges abgewiesen, fremdes HTML vom Server abgewiesen | erfüllt |
| C07 | Vorschau = PDF (`pruef/gleich.js`), Zoom per transform; Ansicht Website: «Alle Abende» mit offenem Fenster dieses Abends, «Der Abend», Startseite; Kartenwechsel öffnet den neuen Abend | erfüllt |
| C08 | **In der Form des Hauses (wie C24):** «Der nächste Abend» mit sechs festen Gängen (Teller + Drink), Datum Freitag/Samstag mit Pfeilen, «Nächsten Abend anlegen», «Die Gänge stehen noch nicht fest», mittig auf dem Blatt | erfüllt |
| C09 | Entwurf, Quittung, Rückgängig, Vorher/nachher, Verwerfen (bleibt im Verlauf) | erfüllt |
| C10 | Probe-PDF enthält den Entwurf | erfüllt |
| C11 | Veröffentlichen: Druck, Wort für Wort gegen die Daten, dann umschalten | erfüllt |
| C12 | Frühere Fassungen, Ursprünglicher Stand | erfüllt |
| C13 | Wege: Frühere Fassungen, Veröffentlichte PDF, Zur Werkbank, Alle Abende auf der Website, Le Bureau, Anschluss, Rundgang. «Unterlagen ansehen»: **betrifft nicht** (die Website des Culinarium hat keine Unterlagen-Seite) | erfüllt |
| C14 | Prüfseite, Fehlermelder, Startfehler-Tür | erfüllt |
| C15 | Alle Daten herunterladen (8 Karten mit Stand, Ursprung, Verlauf, Protokoll) | erfüllt |
| C16 | Online-Fassung: **offen** (Auftrag: nichts online; `online.json` nennt nur Stand- und Prüfweg) | offen mit Grund |
| C17 | Karten aus dem fertigen Satz als Baum (`einlesen.py`), Rundlauf Zeichen für Zeichen (`pruef/rund.js`) | erfüllt |
| C18, C21, C22 | Zeilen-Abgleich mit Seiten der Website: **betrifft nicht** in dieser Form (die Website baut die Menükarten aus `abende_info.py`, nicht aus PDF-Zeilen); Ersatz ist C27 | betrifft nicht |
| C19 | Rolle Spa: **betrifft nicht** (kein Spa) | betrifft nicht |
| C20 | PDF an die Adressen der Website: Weg gebaut (`website_pdfs`), durch die Demo-Sperre `DEMO` gesperrt (Prüfung `S01` «Demo-Sperre») | erfüllt (gesperrt bis Auftrag) |
| C23 | Leere Zeile fällt weg: Gang ohne Teller (Absacker) steht ohne leere Zeile und ohne «x» | erfüllt |
| C24 | siehe C08 | erfüllt |
| C25 | Kapitälchen/Kürzel: **betrifft nicht** (Karten des Hauses ohne Kürzel) | betrifft nicht |
| C26 | Karten aus den Originalen lesen: `karten_lesen.py` liest `website/abende_info.py` (abgelesen von Fotos der gedruckten Karten) und `website/bau.py` ABENDE, zwei Prüfwege (Wort für Wort, gegen `abende.html`), setzt im Kleid des Hauses (`satz_bau.py`) | erfüllt |
| C27 | Website liest die Karten aus La Carte: `karten.json` in der Form von `abende_info.KARTEN` entsteht bei jedem Veröffentlichen (`web.py`, Prüfung `C27`); `pruefe.py website`: unveränderte Karten = Website. Einbau in den Bau der Website **offen** (Revier `website/`) | erfüllt im Werkzeug, Einbau offen |

## Abnahme (Master 8)

| Punkt | Stand |
|---|---|
| Chromium, Safari-Kern; 1440 × 900, 390 × 844 | siehe `pruefung/laeufe/` |
| 1366 × 650, Firefox | nicht gelaufen (Auftrag nennt Chromium + WebKit, 1440 und 390) |
| Speichern → neu laden → noch da | `C09` |
| Veröffentlichen → Website | durch `DEMO` gesperrt; `karten.json` statt Website (C27) |
| Ungewöhnliche Eingaben (5'000 Zeichen, `<script>`, Emoji/Umlaute) | `A08` |
| Zwei Fenster, Netz weg | `A08` |
| Sicherheit 403/429/413/421/415 | `S01`, `S02` |
| Fremde Hausangaben | nur in Kommentaren (Herkunft der Vorlage) |
| Flüssigkeit 4×/6× | `pruefung/fluessig-*.txt` |
| `online.py alles voll` | offen (nichts online) |
