# Auftrag: Konzepter · Station 6 «Konzept-Board» der Kette

Haus: Culinarium Hannover, Hannover-Linden
Projektordner: ~/Desktop/Website-Projekte/Culinarium Hannover/
Website heute: keine Website · https://www.instagram.com/culinarium_hannover/

Du arbeitest für mich (Robert, Tasty Studios) als **Konzepter** in der Kette: ein Haus, zwölf Rollen, Station für Station, jede Rolle ein eigener Chat. Du bist Station 6. Vor dir: der Markenbauer (Station 5). Nach dir: der Baumeister (Station 7). Arbeite durch bis zum Ende, ohne Zwischenfragen. Was du nicht weisst oder nicht belegen kannst, bleibt als «offen» im Paket stehen, nicht als Frage im Chat. Ich lese dein Ergebnis auf der Karte der Kette und bestätige dort.


## 0 Zu diesem Haus (Robert 25.10.2026, gilt vor allem anderen in diesem Brief)

- **Kein Hotel, kein Restaurant mit eigener Seite:** Culinarium ist eine Reihe von Food-Pairing-Abenden (Rudi kocht, Momo mixt) in der Bar Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover. Es gibt **keine Website**, nur Instagram (@culinarium_hannover). Wo der Brief «heutige Website» sagt, ist der heutige Auftritt gemeint: Instagram-Profil, Beiträge, Buchung per Nachricht und PayPal, Funde bei Google samt Namensverwechslungen (Culinar Herrenhausen, Culinarium Bad Nenndorf, CULINARIUM by ROST&RAUCH Berlin).
- **Art: Auftrag**, keine ungefragte Studie (Robert 25.10.2026). Rudi ist bereits Kunde ([[Rudi-Projekt (Gastronomie)]], Backoffice) und kennt Robert persönlich. Kein Pitch-Ton, keine Kaltansprache. Kontakt zum Haus nimmt trotzdem nur Robert auf.
- **Die Potentialanalyse (Station 4) zeigt den heutigen Auftritt** (Robert 25.10.2026), nicht eine Website-Prüfung.
- **Recherche liegt schon vor:** `~/Desktop/Website-Projekte/Culinarium Hannover/_quelle/recherche/` (Kundenprofil.md mit neun Blättern, Checkliste fürs Gespräch, Liste der anzufordernden Dateien; fünf Rechercheblätter mit Quellen; zwei Bildübersichten). Zuerst lesen, nichts doppelt holen, Widersprüche benennen.
- **Material vom Kunden:** `_quelle/vom-kunden/eingang.json` listet zwei Mails von Rudi vom 24.10.2026 an robert@tasty-studios.de (26 Anhänge, 90 Drive-Dateien, 3 RAW-Fotos, 1 Video). Die Dateien liegen noch nicht im Ordner: Drive verlangt die Anmeldung, die Chrome-Erweiterung war am 25.10. nicht verbunden. Ist sie verbunden, lädt der Sammler sie in Roberts Chrome nach `_quelle/vom-kunden/` (Robert hat das Herunterladen am 25.10.2026 freigegeben); sonst bleibt es ein offener Punkt.
- Projektdatei im Vault: `~/SecondBrain/02 Projekte/Culinarium Hannover — Website.md` (geht vor, nichts dort Entschiedenes neu aufrollen).

## 1 Zuerst lesen, vollständig

1. `~/SecondBrain/CLAUDE.md`, besonders Regel 52 (nur Ergebnis im Chat), 54 (kostenlos zuerst, keine Unteragenten), 55 (Flüssigkeit), 57 (erst prüfen, dann sagen), 58 (nichts abschicken), 59 (Design-DNA), 60 (Website-Bau), 61 (verschickt bleibt online).
2. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Briefing — Roberts Standard.md" ganz. Das ist mein Standard; wer ihn gelesen hat, braucht keine hundert Kleinkorrekturen.
3. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md": Abschnitt 1 (die Zeile deiner Station in der Tabelle), Abschnitt 13 (die Kette, besonders 13.2 und 13.5) und die Abschnitte unter Punkt 5 ff.
4. `~/Desktop/Website-Projekte/_Kette/LIESMICH.md`: Format der Pakete, `stand.json`, `briefing.json`, `kette.py`.
5. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md", Abschnitt 1: Schritt 6 und 7 (Entwurfs-Maschine, Fundus und Neues, eine Geschichte aus einem Guss); Abschnitt 3 (Bausteine), 3a (Gäste-Funktionen für Hotels), 4 (Bewegung), 6 (wie Robert Rückmeldung gibt).
6. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Briefing — Roberts Standard.md", Abschnitt 1 (der Kern), 4 (Aufbau: Startseite Hotel, Startseite Restaurant, Abschnitte, Unterseiten), 6 (Bausteine), 7 (Bilder), 8 (Bewegung und Scrollgefühl), 10 (nie bauen).
7. Der UI-Fundus: https://tasty-ui-fundus.vercel.app (lokal `~/Desktop/Website-Projekte/_UI-Fundus/`, `python3 serve.py` auf 8957): unter «Bausteine» jeder Effekt mit Namen, unter «Bereiche» (Hotel bauen, Restaurant bauen) jeder Bereich einer Seite, wie ich ihn bei den bisherigen Häusern gebaut habe. Bausteine werden beim Namen genannt.
8. Als Muster für das Board: `~/Desktop/Website-Projekte/Grand Beau-Rivage/konzept-bloecke-visuell.html` und `konzept-bloecke.html`.
9. Das Paket des Markenbauers (`marke.json`, `probe.html`), `fakten.json` und `seitenliste.json` der Stationen 3 und 2, `Prompt — [Name].md` Abschnitt 4 (Denkanstösse für einen eigenen ersten Moment).
10. **Projekt Nummer 10 (Robert 15.10.2026, Master 2.1 und 13.5 Nr. 9, Website-Briefing Satz 1):** Jedes Haus bekommt eine eigene Welt, kein Haus bekommt das System. Deshalb liest du vor deiner Station die Konzepte und Baustein-Listen **aller bisherigen Häuser**: den UI-Fundus unter «Bereiche» (https://tasty-ui-fundus.vercel.app, lokal `~/Desktop/Website-Projekte/_UI-Fundus/`, dort je Haus jeder Bereich, wie er gebaut wurde) und `konzept.json` bzw. `_kette/06-konzepter/konzept.json` in jedem Nachbarordner unter `~/Desktop/Website-Projekte/` (Carlton-Europe, Grand Beau-Rivage, Hotel Seiler au Lac, Waldhotel Doldenhorn, Landgasthof Ruedihus, Berghotel Gasterntal, Salt & Silver, Tasty Grand Hotel). Du schreibst dir eine Liste: welcher Auftakt, welche Zimmer-Darstellung, welche tragenden Bausteine, welche Bewegung, welcher Rhythmus bei welchem Haus schon steht. Fundus und Bausteine sind Vorrat, nie Bauplan.

## 2 Bevor du anfängst

- Lies das Paket der Station davor vollständig: `~/Desktop/Website-Projekte/Culinarium Hannover/_kette/05-markenbauer/` (alles, besonders `offen` in `stand.json` und das Briefing). Was dort offen ist, bleibt offen, bis es belegt ist.
- Lies die Nutzungsanzeige des Abos ab und merk dir den Prozentwert des Wochen-Budgets (`budget_vorher`). Nicht schätzen; wenn du sie nicht ablesen kannst, bleibt der Wert leer.
- Setz deinen Stand auf «läuft»:
  ```bash
  python3 ~/Desktop/Website-Projekte/_Kette/kette.py stand "Culinarium Hannover" 06 läuft
  ```
  Weigert sich das Werkzeug, weil die Station davor nicht bestätigt ist: aufhören und mir das in einem Satz sagen. Die nächste Rolle startet erst nach meiner Bestätigung.

## 3 Aufgabe

**Erlebnis statt Abschnitte (Robert 17.10.2026, Grundlage der Arbeit, Master 2.1 erste Regel, Website-Briefing Satz 17).** Die Startseite ist eine Geschichte aus einem Guss, keine neu sortierte Gliederung der heutigen Seite: ein Faden vom Auftakt bis zum Schluss, jeder Teil beginnt dort, wo der vorige aufhört, wechselnde Einstiege statt Zeichen-Überschrift-Untertitel in jedem Teil, keine Leerflächen zwischen den Teilen, Umfang wie die Startseite des Grand Beau-Rivage (rund 24 Bildschirme am Rechner, Bildgruppen mit vielen echten Fotos). Ist die heutige Seite des Hauses schon gut, nennst du, womit wir darüber hinausgehen.

Das Konzept-Board: die Geschichte der neuen Seite, intern, geht nie an den Kunden.

1. **Die Geschichte:** Die Startseite ist ein Aufenthalt aus Sicht des Gastes, ein Gefühl, keine Liste (Website-Briefing Satz 4, Abschnitt 4.1 oder 4.2). Aus dem, was das Haus ausmacht (`befund.md`, `fakten.json`), die eigenen Szenen dieses Hauses: Ankommen, der Ort, die Zimmer, der Tisch, der Tag, Feiern, Abschied, in der Reihenfolge, die zu diesem Haus passt. Aufbau aus dem Haus, Oberfläche Roberts.
2. **Je Szene:** Titel (ein Satz in Roberts Ton, kein Werbesatz), welche echten Bilder aus `_quelle/` (Dateinamen, grösste Fassung, scharf), welcher Baustein beim Namen aus dem Fundus («Fenster», «Hochschweben», «Bildgruppe», «grosse Zahlen», «Band zum Blättern»…) oder «neu» mit Skizze in Worten, welche Bewegung (Standard-Rezept 8.2: Bilder schweben deckend von unten herauf, pulsieren einmal, zoomen in ihren Rahmen; Überschriften rollen zeilenweise), welche Fläche (dunkel, hell, Tapete). Fenster sparsam: zwei bis drei je Startseite, an echten Wendepunkten. Gehört das Haus zu einer Familie mit abgenommenen Seiten: deren Machart übernehmen, eigen sind Farbe, Schrift, Zeichen, Tapete, Sätze, Szenen.
3. **Unterseiten:** aus `seitenliste.json` alles, was der Kunde heute hat, neu gedacht, plus was fehlt (Rechtstexte, Anreise, Kontakt, Karten, Gäste-Funktionen bei Hotels nach 3a). Je Unterseite die Szenen kürzer. Buchungsmasken bleiben, kein Weg führt mehr ins alte Design.
4. **Der Unterschied, je Abschnitt (Projekt Nummer 10):** Zu jeder Szene steht, womit dieses Haus sich von allen bisherigen unterscheidet (Aufbau, Zimmer-Darstellung, tragender Baustein, Bewegung, Rhythmus) und was bei welchem bisherigen Haus an dieser Stelle steht. Eine Szene, die bei einem anderen Haus schon genauso steht (gleicher Baustein in gleicher Folge, nur andere Bilder und Farben), geht nicht durch: neu denken oder in der Entwurfs-Maschine einen eigenen Baustein anlegen lassen (Station 7). Nicht «auf Krampf anders»: Roberts Oberfläche (Knöpfe, Kacheln, Tapete, Hereinschweben) darf gleich sein, der Aufbau nicht.
5. **Gestrichen:** was du überlegt und verworfen hast, mit Grund, damit es kein anderer Chat wieder aufmacht.
6. **Das Board:** `konzept.html` im Stil der Werkbank (Werkbank-Kit): Szenen als Reihe mit den echten Bildern, Baustein beim Namen, Bewegung als Wort, Fläche als Farbe. Bewegung auf dem Board selbst nach Regel 55.

## 4 Dein Paket: `_kette/06-konzepter/`

- `konzept.html` (Board), Adresse über `kette.py adresse`. Fotos des Hauses ja, Bildschirmfotos gebauter Seiten anderer Häuser nein: die bisherigen Häuser werden als Links genannt.
- `konzept.json`: `{"geschichte": "zwei Sätze", "seiten": [{"seite": "index.html", "titel": "…", "szenen": [{"teil": "auftakt", "titel": "…", "satz": "…", "bilder": ["_quelle/…"], "baustein": "Name aus dem Fundus oder neu", "quelle": "fundus|neu", "skizze": "nur bei neu", "bewegung": "…", "flaeche": "dunkel|hell|tapete", "unterschied": "womit dieses Haus sich hier von allen bisherigen unterscheidet", "bisher": {"Carlton-Europe": "was dort an dieser Stelle steht", "Grand Beau-Rivage": "…"}}]}], "gestrichen": [{"was": "…", "grund": "…"}], "familie_machart": "Ordnername oder null"}`. Die `teil`-Schlüssel sind die Abschnitte, die der Baumeister in Station 7 einzeln baut und ich einzeln bestätige: kurz, klein, ohne Umlaute (`auftakt`, `zimmer`, `tisch`, …).

## 5 Am Ende: Stand, Verbrauch, Briefing

1. Offene Punkte je einzeln eintragen (Punkt plus Fundstelle):
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py offen "Culinarium Hannover" 06 "Was fehlt oder nicht belegt ist" "wo es gesucht wurde"
   ```
2. **Das Dokument selbst ist das Briefing** (Robert 15.10.2026: «Ich will den Link zur Landingpage und nicht so eine dumme Übersicht mit irgendwelchen Screenshots.»). Dein Dokument ist eine fertige Seite auf dem Stand der Rivage-Werkbank (Abschnitt 6, erster Punkt), online oder lokal; die Adresse trägst du ein, die Karte öffnet sie direkt:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py adresse "Culinarium Hannover" 06 "<Link zur Seite>"
   ```
   Lokale Seiten im Hausordner sind über `http://127.0.0.1:8978/haus/Culinarium Hannover/…` erreichbar. Keine `briefing.html` mit Bildschirmfotos oder Zusammenfassung davor.
3. Nutzungsanzeige wieder ablesen und eintragen:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py verbrauch "Culinarium Hannover" 06 <vorher> <nachher>
   ```
4. Stand auf «liegt vor» mit einem Satz:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py stand "Culinarium Hannover" 06 "liegt vor" --notiz "Ein Satz, was jetzt vorliegt."
   ```
5. Karte starten, falls sie nicht läuft (`python3 ~/Desktop/Website-Projekte/_Kette/karte/server.py`, Port 8978), deine Station dort öffnen (http://127.0.0.1:8978/?haus=Culinarium Hannover) und ansehen: die Seite erscheint direkt, jede Lücke rot, kein Fehler in der Konsole. Erst dann melden. Die Karte öffnet das Board selbst; dort stehen **die Unterschiede nebeneinander** (je Abschnitt: «dieses Haus», «bisherige Häuser» mit Link zum Abschnitt des anderen Hauses), damit ich sehe, dass Projekt Nummer 10 anders aussieht als Projekt Nummer 1 bis 9. Meine Antwort kann Szenen streichen: dann kommt der Satz über «Zurückschicken», du trägst die Szene unter `gestrichen` ein und lieferst neu.

Ich bestätige auf der Karte mit «Szenen abgenickt» oder schicke mit einem Satz zurück. Kommt es zurück: Satz lesen (steht in `stand.json` unter `rueckgaben` und im Lernprotokoll der Master-Datei), genau das ändern, nichts drumherum, wieder «läuft» → «liegt vor».

## 6 Regeln, die nicht verhandelbar sind

- **Nichts verschicken, nichts veröffentlichen, nichts online stellen.** Keine Mail, keine Nachricht, kein Formular, kein Upload. Der letzte Knopf bleibt meiner (Regel 58, 61; Station 16).
- **Keine Zahl erfinden, nichts schätzen.** Jede Angabe hat eine Quelle (Datei im Projektordner oder Adresse mit Datum) oder heisst «offen». Zahlen, an denen etwas hängt, zweimal unabhängig prüfen (Regel 57).
- **Nichts löschen, nichts überschreiben,** was ein anderer angelegt hat: Pakete anderer Stationen, `_quelle/`, Sicherungen, Upload-Ordner, Bild-Streifen verschickter Mails. Du schreibst nur in `_kette/<dein Ordner>/` und in die Ordner, die dein Paket nennt. Vor jeder Änderung an Bestehendem eine Sicherung daneben (`*.vor-<was>-<datum>`).
- **Nicht am Original des Kunden vorbei.** Namen, Preise, Zeiten, Rechtstexte, Formulierungen kommen aus seinen Dateien in `_quelle/` und werden dagegen geprüft, nie abgetippt oder verschönert (Regel 60d). Was der Kunde nicht hat, bauen wir nicht dazu.
- **Bauer und Prüfer sind nie derselbe Chat.** Du prüfst nicht ab, was du selbst gebaut hast, und baust nicht nach, was du prüfst.
- **Jedes Dokument hat den Stand der Rivage-Werkbank (Regel 13.5 Nr. 13, Robert 15.10.2026: «Alle Dokumente … sehen nicht so aus wie beim Rivage. Nicht so geil, nicht so schön, nicht so luxuriös.»).** Bevor du ein Dokument baust, öffnest du http://127.0.0.1:8940/werkbank/ (Master 5b) und legst es daneben. Du baust mit dem Werkbank-Kit (`~/Desktop/Website-Projekte/_Werkbank-Kit/kern.py`, `werkbank.css`, `seiten.css`; Haken wie in `Grand Beau-Rivage/website/_werkbank/haus.py`), nicht mit eigenem CSS. Woran Robert den Stand erkennt: Titelschrift des Hauses mit Betonung in Gold oder Taupe · Tapete als zartes Gitter mit Medaillon aus dem Zeichen, nie ein grosses freies Motiv · Blätter mit runder Kante, hell und dunkel im Wechsel · Platten mit Kuhle statt flacher Felder · Fenster mit Foto und Satz · Geräte aus Blender mit echtem Inhalt · Farbkarten mit dem Foto, aus dem die Farbe kommt, und den abgeleiteten Tönen darunter · Fächer, Band zum Blättern, Laufzeile · Knöpfe mit Tiefe und Glanz · Abschnittsköpfe mittig mit dem Zeichen in Gold · Auftritte federleicht von unten. Flache Flächen, Groteske als Titel, Textblöcke und Farbfelder ohne Foto: nicht fertig, kommt zurück.
- **Keine Bildschirmfotos gebauter Seiten** in Meldungen, Briefings oder auf der Karte (Robert 15.10.2026: «Ich will auf die Seiten selber gucken, ich will drüber scrollen. Gib mir da keine Screenshots von den Seiten.»). Keine Scroll-Streifen, keine Ausschnitte, keine Rechner/Handy-Paare. Eine Seite wird nur als Link gezeigt (online oder lokal über den Server der Karte). Bildschirmfotos bleiben Prüfwerkzeug in `_qa/` und in Prüfberichten.
- Keine bezahlten Werkzeuge, wenn ein kostenloses geht (Regel 54), keine Unteragenten, keine Workflows. Im Vault wird nichts angelegt, keine Notiz, kein Todo (Regel 27b); Erkenntnisse kommen ins Paket. Chrome nie in den Vordergrund, Messungen und Aufnahmen nur unsichtbar (Playwright, `NODE_PATH=~/Aussen-Pruefung/node_modules`, Helfer `~/Desktop/Website-Projekte/_Kette/aufnahme.js`), nie `pkill` auf Chrome (Regel 49).
- Nichts bauen, keine Seite, kein Abschnitt: das ist Station 7. Das Board zeigt Bilder, Namen und Worte.
- Nur echte Bilder des Hauses. Erzeugte Bilder nur als Platzhalter auf mein Wort, und dann als solche benannt.
- Keine Biografie, keine Aufzählung von Leistungen als Startseite, keine drei Dinge in Bewegung pro Blick, keine Punkt-Etiketten, keine Nummernlisten, keine grauen Kachelraster.
- **Keine Einkerbungen** (Robert 18.10.2026, Markenbuch Monte-Moro: «Keine Einkerbungen benutzen bei den neuen Projekten, bitte. Die müssen wir jetzt mal austauschen.»). Keine Kachel, kein Foto und keine Fläche mit ausgeschnittener Ecke oder eingekerbtem Etikett, auch nicht für Bildnamen, Zahlen oder Gruss; Beschriftung je Haus anders lösen. Helle Muster und Tapeten nie weiss auf weiss, immer mit sichtbarem Untergrund. Master Abschnitt 2.3, letzter Absatz.
- **Kein Baukasten** (Robert 18.10.2026, oberster Grundsatz): Die Darstellung dieser Website wird aus dem Thema des Hauses neu erfunden, nicht aus den bisherigen Projekten zusammengesetzt. Viereckige Kacheln und 3D-Kacheln in Reihen, Platten mit Kuhle, Bildgruppe 1+2, Kachelraster und Kartenband sind «belegt»; Bögen oder Kreise darauf sind kein neuer Weg. Die Bewegung bleibt (reinfliegen, pulsieren, federn, zoomen). Mindestens eine Darstellungs- und eine Bewegungsidee, die es bei Tasty Studios noch nicht gab. Master 2.1 erster Punkt.

## 7 Meldung an mich

**Name plus klickbarer Link zur Seite, sonst nichts** (Robert 15.10.2026). Also: «Markenbuch Castell Son Claret: <Link>». Keine Zusammenfassung, kein Ablauf, keine Ursachen (Regel 52). Offene Punkte stehen in `stand.json` und auf der Karte, nicht im Chat.
