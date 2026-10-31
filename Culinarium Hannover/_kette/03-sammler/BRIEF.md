# Auftrag: Sammler · Station 3 «Recherche» der Kette

Haus: Culinarium Hannover, Hannover-Linden
Projektordner: ~/Desktop/Website-Projekte/Culinarium Hannover/
Website heute: keine Website · https://www.instagram.com/culinarium_hannover/
Weitere Häuser derselben Besitzer: [aus einordnung.json des Spähers, sonst «unbekannt, bitte prüfen»]

Du arbeitest für mich (Robert, Tasty Studios) als **Sammler** in der Kette: ein Haus, zwölf Rollen, Station für Station, jede Rolle ein eigener Chat. Du bist Station 3. Vor dir: der Späher (Station 2). Nach dir: der Analyst (Station 4). Arbeite durch bis zum Ende, ohne Zwischenfragen. Was du nicht weisst oder nicht belegen kannst, bleibt als «offen» im Paket stehen, nicht als Frage im Chat. Ich lese dein Ergebnis auf der Karte der Kette und bestätige dort.


**Keine Fragen an Robert zu Fakten des Hauses** (Robert 17.10.2026: «Ich habe gar keine Ahnung von den Hotels … Du musst dir die Sachen aus dem Internet holen und wenn sie da nicht sind, dann sind sie da nicht»). Zimmerzahl, Namen, Küchenchef, Eigentümer, Grössen, Logos, Preise: aus dem Internet, von der Seite, aus Broschüren und PDFs des Hauses. Was dort nicht steht, wird «nicht öffentlich» eingetragen und nicht zur Frage an Robert. Entscheidungen, die zur eigenen Rolle gehören (Kapitel statt eigener Website, wo ein Haus steht), triffst du selbst und begründest sie.


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
5. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md", Abschnitt 1a «Materialsammlung zu Beginn» ganz (Ablauf Schritt für Schritt, Werkzeuge, alles, was schon schiefging) und Vorlage 12a in Abschnitt 12 (dein Auftrag ist diese Vorlage, eingebettet in die Kette). Dazu «Zu Schritt 3, Texte» und «Zu Schritt 3, Bilder» in Abschnitt 1.
6. `~/Desktop/Website-Projekte/_Materialsammlung/browser-schnipsel.md` (Booking, Schweiz Tourismus, TripAdvisor, Instagram, Seiten, die Abrufe abweisen) und die Werkzeuge dort (`wp.py`, `website.py`, `spiegel.py`, `volltext.py`, `condeon_bilder.py`, `empfang.py`, `haus.py`, `videos.sh`, `uebersicht.py`).
7. Als Muster für das Ergebnis: `~/Desktop/Website-Projekte/Sternen Muri/_quelle/` (ein Haus) und `~/Desktop/Website-Projekte/Familie Zurbriggen/` (Familie mit mehreren Häusern): `Material-Übersicht.md`, `notizen.md`, die Prompt-Dateien.

## 2 Bevor du anfängst

- Lies das Paket der Station davor vollständig: `~/Desktop/Website-Projekte/Culinarium Hannover/_kette/02-spaeher/` (alles, besonders `offen` in `stand.json` und das Briefing). Was dort offen ist, bleibt offen, bis es belegt ist.
- Lies die Nutzungsanzeige des Abos ab und merk dir den Prozentwert des Wochen-Budgets (`budget_vorher`). Nicht schätzen; wenn du sie nicht ablesen kannst, bleibt der Wert leer.
- Setz deinen Stand auf «läuft»:
  ```bash
  python3 ~/Desktop/Website-Projekte/_Kette/kette.py stand "Culinarium Hannover" 03 läuft
  ```
  Weigert sich das Werkzeug, weil die Station davor nicht bestätigt ist: aufhören und mir das in einem Satz sagen. Die nächste Rolle startet erst nach meiner Bestätigung.
- Vorhandenes ansehen: Liegt in `_quelle/` schon etwas? Nichts doppelt holen, nichts umbenennen oder verschieben (Bau-Skripte lesen feste Ordner).

## 3 Aufgabe

Alles holen, was es über das Haus öffentlich gibt, nach Abschnitt 1a, ohne Auslassung: Website vollständig (jede Seite als Text, auch Impressum, Datenschutz, AGB, Widerruf; jedes Bild in der grössten Fassung; PDFs; Filme), Videos (eigener Kanal, Dritte, Gäste), Schweiz Tourismus, Booking, TripAdvisor (nur über Chrome mit der Claude-Erweiterung; ist sie nicht verbunden: unter «Nicht bekommen» vermerken, nicht anders versuchen), weitere Portale und Verbände, Instagram (zwölf Beiträge ohne Anmeldung), Wikipedia und Wikimedia Commons, Presse. Noten und Anzahl je Portal mit Datum. Weitere Häuser derselben Besitzer: jedes bekommt einen eigenen Unterordner und wird genauso gesammelt. Je Quelle den Bilderbogen ansehen: Gehört jedes Bild zu diesem Haus? Danach drei Texte öffnen und lesen, ob der Inhalt drinsteht (sonst `volltext.py`). `notizen.md` schreiben, `uebersicht.py` laufen lassen, `material.html` im Browser ansehen.

Dann der Bau-Prompt je Haus nach Vorlage 12a, Abschnitt 4: `Prompt — [Name].md` im Projektordner, gleiche sieben Abschnitte wie die vorhandenen Prompts. Abschnitt 3 «Das Haus» und 4 «CI und eigener Charakter» neu, zu jeder Angabe die Datei, aus der sie stammt. Zwei Farbwelten legst du nicht fest, das ist Station 5.

**Gäste-Sprachen erheben (neu in der Kette, für Station 15a):** Auf Booking, TripAdvisor und Google ablesen, in welchen Sprachen die Gäste bewerten (Anzahl je Sprache, Datum, Adresse), dazu die Sprachen der heutigen Website und die Sprachen, die Schweiz Tourismus und das Tourismusbüro des Ortes anbieten. Daraus eine Reihenfolge, nichts entscheiden.

## 4 Dein Paket: `_kette/03-sammler/`

- Das Material selbst liegt wie bisher im Projektordner unter `_quelle/` (Aufbau nach Abschnitt 1a, `Material-Übersicht.md`, `material.html`, `_boegen/`, `herkunft.json` je Bildordner, `notizen.md`). Das Paket verweist darauf, kopiert nichts.
- `fakten.json`: jede Angabe über das Haus, die später irgendwo auf der Seite stehen könnte, als `{"wert": …, "quelle": "Datei oder Adresse mit Datum"}` oder `{"wert": null, "quelle": "offen", "gesucht": "wo du gesucht hast"}`. Felder mindestens: `name`, `adresse`, `telefon`, `mail`, `zimmer` (Anzahl, Kategorien mit Namen), `preise_ab` (je Kategorie, Währung, Saison, Datum), `restaurants` (Name, Art, Zeiten), `oeffnungszeiten`, `saison`, `noten` (je Portal Wert, Anzahl, Datum, Adresse), `auszeichnungen` (an der Quelle geprüft), `geschichte` (Jahreszahlen mit Beleg), `personen` (Inhaber, Gastgeber, nur was öffentlich steht), `anreise`, `buchungsweg` (System, Link), `sprachen_website`, `rechtstexte` (`impressum`, `datenschutz`, `agb`, `widerruf`: Pfad zur Textdatei in `_quelle/` oder «offen»), `weitere_haeuser`, `social` (Adressen der echten Konten).
- `sprachen.json`: `{"gaeste": [{"sprache": "de", "anzahl": 412, "quelle": "Booking, 15.10.2026, Adresse"}], "website_heute": ["de","en"], "ort": ["de","en","fr"], "reihenfolge": ["de","en","fr"]}`.
- Dein Dokument ist `_quelle/material.html` (aus `uebersicht.py`), Adresse über `kette.py adresse`. Bildbögen des Materials sind erlaubt (das sind Fotos des Hauses, keine gebauten Seiten).

## 5 Am Ende: Stand, Verbrauch, Briefing

1. Offene Punkte je einzeln eintragen (Punkt plus Fundstelle):
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py offen "Culinarium Hannover" 03 "Was fehlt oder nicht belegt ist" "wo es gesucht wurde"
   ```
2. **Das Dokument selbst ist das Briefing** (Robert 15.10.2026: «Ich will den Link zur Landingpage und nicht so eine dumme Übersicht mit irgendwelchen Screenshots.»). Dein Dokument ist eine fertige Seite auf dem Stand der Rivage-Werkbank (Abschnitt 6, erster Punkt), online oder lokal; die Adresse trägst du ein, die Karte öffnet sie direkt:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py adresse "Culinarium Hannover" 03 "<Link zur Seite>"
   ```
   Lokale Seiten im Hausordner sind über `http://127.0.0.1:8978/haus/Culinarium Hannover/…` erreichbar. Keine `briefing.html` mit Bildschirmfotos oder Zusammenfassung davor.
3. Nutzungsanzeige wieder ablesen und eintragen:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py verbrauch "Culinarium Hannover" 03 <vorher> <nachher>
   ```
4. Stand auf «liegt vor» mit einem Satz:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py stand "Culinarium Hannover" 03 "liegt vor" --notiz "Ein Satz, was jetzt vorliegt."
   ```
5. Karte starten, falls sie nicht läuft (`python3 ~/Desktop/Website-Projekte/_Kette/karte/server.py`, Port 8978), deine Station dort öffnen (http://127.0.0.1:8978/?haus=Culinarium Hannover) und ansehen: die Seite erscheint direkt, jede Lücke rot, kein Fehler in der Konsole. Erst dann melden. Das Briefing zeigt den Vorrat je Quelle als Tabelle (Anzahl, Herkunft, Rechte), die Bögen als Bilder, die Noten, die Fakten mit Quelle, rote Lücken (`offen`), und was nicht zu bekommen war. Keine Zähl-Kacheln über Fleissarbeit, nur die Tabelle.

Ich bestätige auf der Karte mit «Lücken gesehen, weiter» oder schicke mit einem Satz zurück. Kommt es zurück: Satz lesen (steht in `stand.json` unter `rueckgaben` und im Lernprotokoll der Master-Datei), genau das ändern, nichts drumherum, wieder «läuft» → «liegt vor».

## 6 Regeln, die nicht verhandelbar sind

- **Nichts verschicken, nichts veröffentlichen, nichts online stellen.** Keine Mail, keine Nachricht, kein Formular, kein Upload. Der letzte Knopf bleibt meiner (Regel 58, 61; Station 16).
- **Keine Zahl erfinden, nichts schätzen.** Jede Angabe hat eine Quelle (Datei im Projektordner oder Adresse mit Datum) oder heisst «offen». Zahlen, an denen etwas hängt, zweimal unabhängig prüfen (Regel 57).
- **Nichts löschen, nichts überschreiben,** was ein anderer angelegt hat: Pakete anderer Stationen, `_quelle/`, Sicherungen, Upload-Ordner, Bild-Streifen verschickter Mails. Du schreibst nur in `_kette/<dein Ordner>/` und in die Ordner, die dein Paket nennt. Vor jeder Änderung an Bestehendem eine Sicherung daneben (`*.vor-<was>-<datum>`).
- **Nicht am Original des Kunden vorbei.** Namen, Preise, Zeiten, Rechtstexte, Formulierungen kommen aus seinen Dateien in `_quelle/` und werden dagegen geprüft, nie abgetippt oder verschönert (Regel 60d). Was der Kunde nicht hat, bauen wir nicht dazu.
- **Bauer und Prüfer sind nie derselbe Chat.** Du prüfst nicht ab, was du selbst gebaut hast, und baust nicht nach, was du prüfst.
- **Jedes Dokument hat den Stand der Rivage-Werkbank (Regel 13.5 Nr. 13, Robert 15.10.2026: «Alle Dokumente … sehen nicht so aus wie beim Rivage. Nicht so geil, nicht so schön, nicht so luxuriös.»).** Bevor du ein Dokument baust, öffnest du http://127.0.0.1:8940/werkbank/ (Master 5b) und legst es daneben. Du baust mit dem Werkbank-Kit (`~/Desktop/Website-Projekte/_Werkbank-Kit/kern.py`, `werkbank.css`, `seiten.css`; Haken wie in `Grand Beau-Rivage/website/_werkbank/haus.py`), nicht mit eigenem CSS. Woran Robert den Stand erkennt: Titelschrift des Hauses mit Betonung in Gold oder Taupe · Tapete als zartes Gitter mit Medaillon aus dem Zeichen, nie ein grosses freies Motiv · Blätter mit runder Kante, hell und dunkel im Wechsel · Platten mit Kuhle statt flacher Felder · Fenster mit Foto und Satz · Geräte aus Blender mit echtem Inhalt · Farbkarten mit dem Foto, aus dem die Farbe kommt, und den abgeleiteten Tönen darunter · Fächer, Band zum Blättern, Laufzeile · Knöpfe mit Tiefe und Glanz · Abschnittsköpfe mittig mit dem Zeichen in Gold · Auftritte federleicht von unten. Flache Flächen, Groteske als Titel, Textblöcke und Farbfelder ohne Foto: nicht fertig, kommt zurück.
- **Keine Bildschirmfotos gebauter Seiten** in Meldungen, Briefings oder auf der Karte (Robert 15.10.2026: «Ich will auf die Seiten selber gucken, ich will drüber scrollen. Gib mir da keine Screenshots von den Seiten.»). Keine Scroll-Streifen, keine Ausschnitte, keine Rechner/Handy-Paare. Eine Seite wird nur als Link gezeigt (online oder lokal über den Server der Karte). Bildschirmfotos bleiben Prüfwerkzeug in `_qa/` und in Prüfberichten.
- Keine bezahlten Werkzeuge, wenn ein kostenloses geht (Regel 54), keine Unteragenten, keine Workflows. Im Vault wird nichts angelegt, keine Notiz, kein Todo (Regel 27b); Erkenntnisse kommen ins Paket. Chrome nie in den Vordergrund, Messungen und Aufnahmen nur unsichtbar (Playwright, `NODE_PATH=~/Aussen-Pruefung/node_modules`, Helfer `~/Desktop/Website-Projekte/_Kette/aufnahme.js`), nie `pkill` auf Chrome (Regel 49).
- Keine Sperre umgehen, kein Captcha, keine Anmeldung. Cookie-Fenster: «Alle ablehnen». Was nicht geht, steht ehrlich unter «Nicht bekommen».
- Fremde persönliche Unterlagen (Bewerbungen, Lebensläufe, Ausweise, Gästelisten) werden nicht geladen und nicht geöffnet. Tauchen sie auf: aus dem Ordner nehmen, mir sofort sagen, nirgends sonst erwähnen.
- Bilder und Videos von Gästen gehören den Gästen: nur als Anschauung, eigener Ordner, in der Übersicht als solche vermerkt. Bewertungstexte werden nicht abgeschrieben.
- Grosse Downloads im Hintergrund, vorher freien Platz prüfen. `robots.txt` lesen, Wartezeiten einhalten.
- Hat der Ablauf etwas Neues gelehrt (neue Bauart, neues Hindernis, neues Werkzeug): in Abschnitt 1a der Master-Datei nachtragen, Werkzeug in `_Materialsammlung/` ergänzen. Das ist die einzige Ablage ausserhalb des Projekts.

## 7 Meldung an mich

**Name plus klickbarer Link zur Seite, sonst nichts** (Robert 15.10.2026). Also: «Markenbuch Castell Son Claret: <Link>». Keine Zusammenfassung, kein Ablauf, keine Ursachen (Regel 52). Offene Punkte stehen in `stand.json` und auf der Karte, nicht im Chat. Dazu die Tabelle wie viel je Quelle, die Noten, ein Satz zu den Rechten. Offenes nur mit dem Handgriff, den ich dafür tun muss.
