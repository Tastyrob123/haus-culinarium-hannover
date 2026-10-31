---
tags: [projekt, website]
status: aktiv
---

# Lieferung La Réception (Team hinter dem Gäste-Chat) · Culinarium Hannover (28.10.2026)

Fertig gebaut und selbst geprüft (Bauer `culinarium-reception`), Abnahme durch einen neuen Chat nach Master Abschnitt 8 offen. Nichts online, nichts verschickt, keine KI aufgerufen, kein Schlüssel gelesen.

**Adresse:** http://localhost:9084/_werkzeuge/reception/ · Anleitung http://localhost:9084/_werkzeuge/reception/anleitung.html · Prüfung http://localhost:9084/_werkzeuge/reception/pruefung.html (alle mit curl auf 200 geprüft)
**Diese Lieferung:** http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/reception/LIEFERUNG.md

- Start: `python3 _werkzeuge/reception/server.py 9084` aus dem Projektordner. Liefert die Website unter http://127.0.0.1:9084/ (nur lesen), das gemeinsame Kleid aus `_werkzeuge/oberflaeche/` unter `/assets/oberflaeche/`, den Chat unter `/api/gast`. Ohne `RECEPTION_KI=1` antwortet alles mit beschrifteten Probe-Antworten (E18/E23).
- Name im Werkzeug: nur aus `_werkzeuge/oberflaeche/kleid/culinarium.js › namen.gaeste` (culinarium-maison). Robert hat am 28.10.2026 Satz A «An der Bar» gewählt: **Das Gästebuch**. Im Werkzeug, in Anleitung, Prüfseite, Rundgang, im Dank an den Gast («liegt nur zur Ansicht im Gästebuch»), in der LIESMICH und im Dateinamen des Datenexports kommt der Name aus dieser einen Stelle (Python liest `namen:` per Regex, `reception.NAME`); geprüft im sichtbaren Text aller Ansichten, im Chat, in Anleitung und Prüfseite: kein alter Arbeitsname mehr. Die Beispiel-Daten wurden dafür neu angelegt (Sicherung `daten.vor-namen-2026-10-28`, nur Beispiele).
- Vorbild: der Gastgeber der Taverne zum Schäfli (nur gelesen, APFS-Klon), mit allen Korrekturen seines Demo-Checks. Kleid neu gerechnet (`_bau/culinarium_kleid.py`: Ochsenblut → Nacht/Schiefer, Schildgold → Kerze, Kalk → Warmweiss; Petrona → Fraunces mit weichen Enden; nie fett, nie kursiv), Daten, Texte und Prüfläufe neu fürs Culinarium.

## Was steht

- **Eingang** mit vier Arten: Warteliste, Platz am Abend, Eigene Feier (die lange Tafel), Nachricht; Abteilungen Warteliste, Abende, Feiern, Nachrichten. Hinweise je Anfrage aus den Angaben des Hauses, nie gespeichert: der nächste Termin steht noch nicht fest; ein Tag ausser Freitag (ab 19) und Samstag (ab 17); mehr Plätze, als die Warteliste nimmt (6) oder die Tafel hat (14); Bar geschlossen Sonntag bis Mittwoch (bei eigener Feier); Allergie oder Wunsch zur Küche (die Website sagt dazu nichts: «Rudi fragen»); Ticket zurückgeben (wird nicht rückerstattet). Neu als E35 im Master.
- **Brief** im Kleid des Hauses: Briefkopf «Culinarium · A UNiQUE EXPERiENCE BY MOMO X RUDI · Walk on the Wild Side», das «C» der Wortmarke, Fuss mit Haasemannstraße 13, Telefon der Bar und Instagram (Culinarium hat keine Mail-Adresse, `fakten.json`). Gestalten und «Nur Text» als dasselbe Blatt, PDF A4 vom Server («Culinarium – Name – Datum.pdf»), Text kopieren, kein Mailprogramm. Ton: Du, herzlich, knapp, Wertigkeit (der einzelne Gast, das erklärte Glas, der von Hand angerichtete Teller), vierzehn Plätze nur als «wenige Plätze». Vorlagen nur aus dem Wortlaut des Hauses: `vorlagen/warteliste.txt`, `abend.txt`, `feier.txt`.
- **Das wurde gefragt**, **Vom Team nachgetragen**, **Das weiss der Chat** (45 belegte Zeilen in zehn Bereichen: Culinarium, Der Abend & Warteliste, Tickets & Preise, Drinks & Küche, Kontakt, Das Haus (Bar), Team, Der Weg, Dirty Chicken, Alle Abende), **Chat ausprobieren** (Handy im Kleid, Du-Form, «Auf die Warteliste» statt Reservation).
- **Wissen des Chats** aus dem Wortlaut der Website, wie ein Gast ihn sieht (`_bau/website_text.js` headless gegen :8765: innerText ohne Beispieltermine und gespielte Zahlung, «Gut zu wissen» aufgeklappt) plus `_quelle` (Vorverkauf und Rückgabe aus dem Instagram-Beitrag zum letzten Abend, Kontaktwege und Plus Code aus `fakten.json`). `_bau/culinarium_wissen.py` bricht ab, wenn ein übernommener Satz nicht wörtlich in der Quelle steht; `steckbrief_bau.py` ebenso je Zeile. Gegenprobe gegen die laufende Website: `python3 _werkzeuge/reception/pruefung/steckbrief_gegen_website.py` → 57 Belege und 14 Kernangaben alle auf der Website. «Vegetarisch» steht nirgends als Merkmal (Rückmeldung Rudi 26.10.).
- **Beispiele**: sieben Anfragen und zehn Fragen (zwei mit Absicht ohne Antwort: Nussallergie, alkoholfrei), erfundene Gäste mit example.com, beschriftet (`_bau/culinarium_beispiele.py`, prüft jede Zahl gegen das Wissen). Kein erfundener Nachtrag des Teams.
- **Anschluss der Website**: `baustein/anfrage.js` + `baustein/ANLEITUNG.md`: fängt das Warteliste-Ticket auf Der Abend ab, legt den Eintrag in den Eingang, löst den Abriss erst nach der Annahme; ohne Verbindung Meldung mit Telefon der Bar und Instagram, Eingaben bleiben. **Auf der Website nicht eingebaut** (gehört dem Website-Chat, auf Wort des Oberchefs).
- Prüfseite (`pruefung.html`, Lexikon, Reparaturen, ZIP-Export «La-Reception-Culinarium-Datum.zip»), Anleitung mit zwölf Kapiteln aufs Culinarium umgeschrieben, Bilder neu.

## Wie geprüft (bedient, nicht geladen)

Probe-Kopie mit Wegwerf-Daten (Server :9184, `RECEPTION_DATEN` im Notizblock, `RECEPTION_FORMULAR_GRENZE=200`), Playwright headless über `pruefung/schutz.js` (mailto/tel abgefangen), ein Browser zugleich:

| Lauf | Chromium 1440 | WebKit 1440 | Chromium 390 | WebKit 390 |
|---|---|---|---|---|
| `pruefung/culinarium.js` (Hauptlauf) | 27/27 | 26/26 | 27/27 | 27/27 |
| `pruefung/zusatz.js` | 8/8 | – | – | 8/8 |
| `pruefung/democheck.js` | 5/5 | – | – | 5/5 |
| `pruefung/breiten.js` (je Browser alle Breiten 390, 920, 1000, 1024, 1100, 1240, 1440 × fünf Ansichten) | 35/35 | 35/35 | (in den 35 enthalten) | (in den 35 enthalten) |

Protokolle `pruefung/lauf-*.txt` und `pruefung/lauf/*.json`, Bilder `pruefung/bilder/`, PDF `pruefung/lauf/brief-*.pdf`.

- **Hauptlauf**: jede Ansicht zweimal ohne Konsolenfehler, ohne 404, ohne kaputte Bilder, ohne Überlaufen; kein roher Code; kein mailto/tel, keine Namensabfrage, keine fremden Hausnamen; jeder Link in Kopf und Rand antwortet (Zentrale :9081, Bureau :9082 … Druck :9087, eigene Wege 200); Auswahl und Kalender im Hausstil; Bilder in jeder Liste (Eingang 7, Gefragt 10, Nachgetragen 3, Wissen 6); Hinweise bei den richtigen Anfragen (Lena Termin offen, Tim 18 > 14 Plätze, Mira Küche fragen, Sophie Ticket, Kai ohne Hinweis); Luft 18 px, Rest 26 px, Rundgang-Schild 0 px; Abteilungen zählen wie der Server; Brief schreiben (Probe, Du-Ton, Briefkopf) → ändern → sichern → **neu laden → noch da**; PDF «Culinarium – Jonas Albers – Datum.pdf»; zwei Fenster: veraltete Fassung abgewiesen (KONFLIKT), nichts überschrieben; «Nur Text» = «Gestalten»; erledigt ↔ offen; auf Deutsch lesen (Emma Clarke); Lücke nachtragen → Karte → entfernen; Wissen suchen («Fatwashing» trifft, «Kinderstuhl» → noch nicht im Wissen); Chat ausprobieren → Beispiel-Anfrage im Eingang; **Website-Warteliste über den Baustein** (Samstag, 4 Plätze, Name mit `<script>` und Emoji entschärft, Abriss erst nach Annahme), ohne Name (Website sagt, was fehlt, nichts im Eingang), ohne Verbindung (Meldung mit Telefon der Bar und Instagram, Eingaben bleiben); Sicherheit `formular`: fremde Herkunft 403, ungültiger Kontakt 422, Maschinenfeld legt nichts ab, über 12 kB 413; am Handy klappen die Bereiche auf und nach der Wahl zu.
- **Zusatzlauf**: Filter Neu/Offen/Erledigt, Text kopieren (kein Mailprogramm), Löschen mit Rückfrage, «Abteilung fragen» → Antwort eintragen, Angabe anlegen → neu laden → noch da → entfernen, ZIP-Export, Prüfseite ohne Rot, Verlassen mit ungespeicherter Eingabe fragt nach.
- **Demo-Check**: 14 Gästefragen nacheinander (nächster Abend, Beginn, Platz, Preis, Essen, Milkwashing, Ticket zurück, Weg, Bar, Feier mit 25, Nussallergie, Dirty Chicken, englisch, Warteliste mit Mail): jede beantwortet, als Demo beschriftet, kein Technikwort, Eingabefeld bleibt sichtbar (798 von 900 px); jede Anfrage geöffnet; 32 Ziele in Werkzeug, Anleitung und Prüfseite erreichbar; Anleitung mit allen Bildern und Sprüngen; Prüfseite «Alles in Ordnung» (gelb: Probe ohne KI, Anmeldung, Warteliste noch nicht angeschlossen).
- **Gegenprobe Wissen ↔ Website**: 57 Belege, 14 Kernangaben, alle auf der Website. Textdurchgang über alle Ansichten, jede Anfrage, Anleitung und Prüfseite: kein Wort aus dem Vorbild (Restaurant, Tisch reservieren, Festsaal, Gutschein, Ferien, CHF …).
- **Flüssigkeit** (Chromium 1440, Wechsel der Ansichten und Scrollen, nur transform/opacity): 4× gedrosselt 111 Bilder/s, 3 über 50 ms, längstes 92 ms; 6× gedrosselt 110 Bilder/s, 4 über 50 ms, längstes 158 ms.
- **PDF** mit dem Auge: Briefkopf mit dem «C», Plakatzeile wie auf den Plakaten (pdftotext Wort für Wort lesbar), das «x» statt Raute, keine Zierecken des Vorbilds.
- Gefunden und behoben nach der Lieferung: eine Sicherung des Datenordners (`daten.vor-…`) wäre über den Server lesbar gewesen; jetzt sind alle Daten-Ordner und alle `.vor-`-Sicherungen gesperrt (404 geprüft).
- Gefunden und behoben beim Bau: Bühnenfoto «schild» aus dem Vorbild (404) → `schildnah`; Kopf-Wege relativ (Zentrale ohne Server) → Ports; Plakatzeile in der PDF zerfiel (Sperrung .2em) → .06em; Stile fett/kursiv aus dem Vorbild → 400/aufrecht; Brief-Wahl «Kursiv» entfernt.

## Offen, mit Grund

- Abnahme durch einen neuen Chat (Bauer ist nie Prüfer, Master 8).
- **Allergien und Unverträglichkeiten**: Website und Quellen sagen nichts dazu. Der Chat sagt das offen und gibt die Frage ans Team («Rudi fragen»); eine Regel des Hauses fehlt (an den Oberchef).
- **Kontakt**: Culinarium hat keine eigene Mail-Adresse und kein Telefon (`fakten.json`); Brief und Chat nennen das Telefon der Bar und Instagram. Bestätigen lassen, welcher Weg gilt.
- **Warteliste auf der Website**: Baustein nicht eingebaut (Website-Chat); dazu Weiterleitung :8765 → :9084 und Datenschutz-Satz (Vorschlag in `baustein/ANLEITUNG.md`).
- Online-Fassung von La Réception: nicht gebaut (Auftrag: nichts online). Anmeldung, Rollen, `_wache.py`: bei der Auslieferung (Master 5.3).
- Echte KI-Antworten nur mit `RECEPTION_KI=1` und Freigabe; geprüft ist der Probe-Betrieb.
- Firefox und 1366 × 650 nicht gelaufen (nicht verlangt); Netz weg beim Brief-Sichern nicht nachgestellt (Warteliste ohne Netz ja).
- (erledigt) Kopf-Wege der gemeinsamen Oberfläche waren relativ; culinarium-maison hat es zentral in `kleid/culinarium.js` behoben, die eigene Zeile in `reception.js` bleibt als Absicherung (prüft ebenfalls auf «/», nichts doppelt).

## Bilder

Für Oberchef und Werkbank (WebKit, 1440 und 390; Übersicht, Eingang, Brief, Gefragt, Wissen, Chat; dazu der Brief als A4-PDF): `~/Desktop/Website-Projekte/_Oberchef/zeigen/culinarium/reception/`, zum Beispiel http://localhost:8978/haus/_Oberchef/zeigen/culinarium/reception/reception-1440-1-uebersicht.jpg

Der Server auf 9084 läuft (eigener Prozess, `nohup`); neu starten: `python3 _werkzeuge/reception/server.py 9084` aus dem Projektordner.

## Lernen

- Master 10a, neue Zeile 28.10.2026: Wege zu anderen Werkzeugen im Kopf lokal immer auf deren Port (127.0.0.1:<port>), Prüflauf ruft jeden Link in Kopf und Rand auf.
- Master 4.4, neue Zeile E35: Abende ohne festen Termin (Warteliste statt Reservation).
- Fehlerbuch Zeile für Zeile: `pruefung/FEHLERBUCH-10A.md`.

## Messlauf 30.10.2026 (Chat Messlauf/Querprüfung)

Umschalter (`.wahl2`) gleichen die Sperrung aus, Beispielfragen im Probe-Chat auf Versalhöhe; langer Gruppentitel («Allergien & Unverträglichkeiten») überdeckt den Zähler am Handy nicht mehr. Hauptlauf 27/27, 27/27, 26/26, 27/27, Breiten 35/35 je Browser. Start gedrosselt 2,03 s (Median aus 5), ungedrosselt 0,33 s.
Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/messlauf-2910/index.html

## Probe-Einträge raus + Messlauf auf 0 (30.10.2026, Übernahme durch culinarium-imprimerie)
- Probe-Einträge vom 29.10. («Probe EN (culinarium-mobil)» …14-48-48, «Probe EN ticket» …14-49-32) aus `daten/anfragen/` genommen; Sicherung `daten.vor-probe-raus-2026-10-30/`. Eingang zeigt die 7 Beispiel-Gäste, auch nach dem Abholen von online.
- Messlauf Gästebuch + Anleitung, Chromium und WebKit, 1440 / 1280 / 1000 / 390: vorher 6 (2 «gekürzt» Nussallergie-Frage, 2 «gekürzt» Hinweiszeile im Brief am Handy, 2 Einzelwort «accessible?» in WebKit), bei 1000 zusätzlich text-mitte «Gestalten» (WebKit, 0,5 px).
  - `culinarium-reception.css`: Fragen der Übersicht bis drei Zeilen; Hinweiszeile im Brief am Handy zweizeilig (feste Höhe, kein Springen); Karteikarten-Frage `text-wrap:balance`; nur Safari: «Gestalten / Nur Text» ¼ px Ausgleich (`@supports (font:-apple-system-body)`).
  - `reception.js`: Karteikarten-Frage hält die letzten zwei Wörter zusammen (WebKit gleicht balance hier nicht aus).
  - Nachher: 0 Funde, ausser «rand» am Kopf-Knopf «Website ansehen» bei 1000 px (Text für Vorleser versteckt, nur Symbol sichtbar). Fehlalarm der Regel, an cu-messlauf gemeldet. Tafel: `_Oberchef/zeigen/culinarium/messlauf-3010/gaestebuch-c/tafel.html`.
- Bedienprüfung `pruefung/culinarium.js` (Wegwerf-Daten auf :9184): Chromium 1440/1280/1000/390 27/27, WebKit 1440/1280/1000/390 26/26. Prüfschritt «Kinderstuhl» scrollt jetzt zum Hinweis und liest WebKits «nochnichts» am Zeilenumbruch mit.
- Sicherungen `*.vor-gaestebuch-messlauf-2026-10-30`, `pruefung/culinarium.js.vor-1000-2026-10-30`.
- 30.10.2026: «×» in der Meldung (z. B. «Wieder offen») sass in Safari 1,4 px zu tief (Ersatzschrift); nur Safari 2 px Ausgleich unten (`@supports (font:-apple-system-body)`), Chromium unverändert. Beide Browser 1440/390: 0. Sicherung `culinarium-reception.css.vor-quit-x-2026-10-30`. Der Hänger des Tors nach «Wieder offen» war ein Hänger des Prüflaufs, im Gästebuch nicht nachstellbar.
- 30.10.2026: Bewegungs-Tor-Rest erledigt: bei «weniger Bewegung» zoomt auch das Foto im Blatt nicht mehr (`studio/schweben.css`, reduced-motion-Block um `[data-sw] img` erweitert; Sicherung `studio/schweben.css.vor-ruhe-2026-10-30`). Nachgeprüft Chromium + WebKit: mit reduce 0 laufende Animationen, ohne unverändert. Fassungsnummern mit `_bau/fassungen.py`.
- 30.10.2026 (Oberchef, Robert: kein X): alle «×» im Gästebuch ersetzt durch den Zurück-Pfeil wie «Verwerfen» in der Pairing-Karte: Meldung, Fenster, Gestalten-Platte, Probe-Chat, Rundgang-Schild (`reception.js` ZU, `studio/rundgang.js`); kein Drehen mehr beim Überfahren. Safari-Ausgleich fürs alte × entfernt. Gestalten-Platte: «−»/«+» gezeichnet, Sperrschrift-Knöpfe optisch mittig. Gemessen Chromium + WebKit 1440/1000/390: 0; Bedienprüfung WebKit 1440 26/26, Chromium 390 27/27. Kleid-Stempel neu (fassungen.py). Sicherungen `*.vor-ohne-x-2026-10-30`.
