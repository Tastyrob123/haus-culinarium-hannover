# Auftrag: Späher · Station 2 «Kunden analysieren» der Kette

Haus: Culinarium Hannover, Hannover-Linden
Projektordner: ~/Desktop/Website-Projekte/Culinarium Hannover/
Website heute: keine Website · https://www.instagram.com/culinarium_hannover/

Du arbeitest für mich (Robert, Tasty Studios) als **Späher** in der Kette: ein Haus, zwölf Rollen, Station für Station, jede Rolle ein eigener Chat. Du bist Station 2. Vor dir: nichts (die Kette beginnt mit diesem Link; Station 1, Kunden suchen, ist der Kundenfinder). Nach dir: der Sammler (Station 3). Arbeite durch bis zum Ende, ohne Zwischenfragen. Was du nicht weisst oder nicht belegen kannst, bleibt als «offen» im Paket stehen, nicht als Frage im Chat. Ich lese dein Ergebnis auf der Karte der Kette und bestätige dort.


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
5. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md", Abschnitt 1: Schritt 2 und «Zu Schritt 2» (Studie, Auftrag, eigene Seite; was bei Leads mit laufendem Angebot gilt), Abschnitt 2.9 (was nach KI aussieht) und 2.10 (Fakten).
6. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Briefing — Roberts Standard.md", Abschnitt 3 (bevor die erste Zeile gebaut wird: Familie, Konzept, Haus verstehen), 10 und 16.
7. `~/Desktop/Website-Projekte/_Kundenfinder/` (`bericht/`, `8_liste.py`): so sucht die Maschine, so sind die Kriterien, nach denen ein Haus überhaupt auf die Liste kam (Besitzerfamilien mit alten Seiten).
8. `~/SecondBrain/02 Projekte/`: gibt es zu dem Haus schon eine Projektdatei, geht sie vor; nichts dort Entschiedenes neu aufrollen. Nachbarordner in `~/Desktop/Website-Projekte/` ansehen: gehört das Haus zu einer Familie, deren Seiten ich schon abgenommen habe?

## 2 Bevor du anfängst

- Es gibt kein Paket vor dir. Lies die Nutzungsanzeige des Abos ab und merk dir den Prozentwert (`budget_vorher`).
- Falls `_kette/` im Projektordner noch fehlt, leg es an, dann «läuft»:
  ```bash
  python3 ~/Desktop/Website-Projekte/_Kette/kette.py anlegen "Culinarium Hannover"
  python3 ~/Desktop/Website-Projekte/_Kette/kette.py stand "Culinarium Hannover" 02 läuft
  ```

## 3 Aufgabe

Du schaust dir das Haus und seinen Auftritt an und sagst, ob es passt und was für ein Projekt es wird. Du baust nichts, du sammelst nicht das ganze Material (das macht der Sammler), du urteilst.

1. **Die heutige Website durchgehen.** Startseite und jede Unterseite, die ein Gast findet (Leiste, Fuss, Sitemap, `robots.txt`). Jede Seite als Text (`defuddle`, sonst Browser-Pane). Aufnahmen am Rechner und Handy nur als Prüfwerkzeug nach `_qa/` (unsichtbar mit `~/Desktop/Website-Projekte/_Kette/aufnahme.js`), nicht ins Briefing: die heutige Seite wird als Link gezeigt. Cookie-Fenster: «Alle ablehnen». Keine Anmeldung, kein Formular, keine Sperre umgehen.
2. **Stand einschätzen, mit Beleg je Punkt:** Alter der Technik (Baukasten, Agentur, WordPress, Frames), Bilder (grösste Fassung, Schärfe, eigene oder Stock), Handy-Fassung, Ladezeit, Sprachen, Buchungsweg (welches System, Link), Rechtstexte (Impressum, Datenschutz, AGB, Widerruf vorhanden ja/nein), Newsletter, Social-Konten, Auszeichnungen (an der Quelle geprüft, Michelin «empfohlen» ist kein Stern). Noten und Anzahl der Bewertungen auf Google, Booking, TripAdvisor mit Datum, nur ablesen.
3. **Was das Haus ausmacht:** Geschichte, Lage, Familie, Besonderheiten, in drei bis fünf Sätzen aus dem, was auf der Seite steht. Keine Deutung ohne Beleg.
4. **Familie und weitere Häuser:** gleiche Telefonnummer, gleiches Impressum, «Partnerhotel», Links. Jedes weitere Haus mit Adresse nennen. Prüfen, ob ich eines davon schon gebaut habe (Nachbarordner): dann gilt deren Machart (Website-Briefing Satz 3).
5. **Einordnen:** `studie` (ungefragt, als Geschenk), `auftrag` (es gibt eine Anfrage oder ein Angebot, siehe Projektdatei im Vault) oder `eigene-seite`. **Empfehlung «passt» oder «passt nicht» mit Begründung.** Passt heisst: inhabergeführtes Haus, kein Kettenbetrieb; die Seite ist sichtbar älter oder schwächer als das Haus selbst (Bilder, Handy, Technik, Geschichte unerzählt); es gibt echtes Material (Fotos, Geschichte, Karten), aus dem eine Seite werden kann; kein erkennbar laufender Relaunch. Passt nicht, wenn einer dieser Punkte klar dagegen spricht. Ein Zwischenergebnis («passt, wenn …») ist erlaubt und wird als offener Punkt eingetragen.

**Zusatz 17.10.2026 (Robert, nach dem ersten Durchlauf am Castell Son Claret):**
- **Zielmarkt vorerst Schweizer Luxushotels.** Robert: «jetzt gerade ist, glaube ich, sicherer mit Schweizer Luxushotels zu fahren». Ein Haus ausserhalb der Schweiz bekommt «passt nicht» oder «passt, wenn Robert es ausdrücklich will», mit Grund.
- **Die Familie steht über den Sternen** (Robert 17.10.2026). Gehört ein Haus zu einer Häuserfamilie, kommt es immer mit, auch mit drei, zwei oder einem Stern: «weil es zur Familie gehört». Auf der Familienseite steht es weiter unten. In der Aufbauphase geht es darum, sich strategisch zu positionieren, nicht stark zu selektieren. Sterne sind dann nie ein Grund für «passt nicht».
- **Agentur im Rücken: immer gleich mit analysieren** (Robert 17.10.2026: «Wir müssen die schlagen können»). Lies Fuss, Impressum, Quelltext und Generator-Angaben, zum Beispiel «Created by Profitroom», Agentur-Credit oder Baukasten mit Betreuungsvertrag. Trag in `einordnung.json` das Feld `"betreuung"` ein: Agentur oder Anbieter mit Beleg oder `"offen"`. Ist eine Agentur, ein Baukasten-Anbieter oder eine Plattform mit Betreuung erkennbar, ist das **kein Ausschlussgrund**, sondern ein eigener Abschnitt «Wer hinter der heutigen Seite steht» im Befund, mit Beleg und Datum je Punkt:
  1. Was das für eine Agentur ist: Name, Sitz, Grösse, Schwerpunkt, andere Hotelkunden.
  2. Wann die heutige Seite gebaut und zuletzt geändert wurde (Impressum, Quelltext, Archiv unter web.archive.org, Datumsangaben im Code).
  3. Welche Pakete und Preise die Agentur anbietet (Website, Pflege, Buchung, Lizenz), soweit öffentlich.
  4. Vertragsbedingungen aus ihren AGB: Mindestlaufzeit, Verlängerung, Kündigungsfrist.
  5. Nutzungsrechte: Wem gehören Seite, Code, Texte, Bilder, Adresse und Zugänge? Was bleibt dem Haus bei einer Kündigung? Gibt die Agentur Quellcode und Daten heraus?
  6. Wo wir besser sind, Punkt für Punkt gegen das, was die heutige Seite zeigt.

  Was nicht öffentlich ist (der tatsächlich unterschriebene Vertrag), steht als «ungeprüft, im Gespräch zu klären» da und wird nie als Tatsache über das Haus formuliert. Vorbild: Befund Wellness & Spa Zurbriggen, Abschnitt «Entscheid Robert 17.10.2026» (vioma). Der Abschnitt geht an die Analyse weiter und landet in der Präsentation.
- **Ist die heutige Seite schon gut, sag es deutlich.** Nenn, was sie gut macht. Daran misst sich später, womit wir darüber hinausgehen (Master 2.1, erste Regel «Erlebnis statt Abschnitte»).

## 4 Dein Paket: `_kette/02-spaeher/`

- `befund.md` mit genau diesen Überschriften: Das Haus in Kürze · Die heutige Seite (Stand mit Belegen) · Was fehlt · Was das Haus ausmacht · Familie und weitere Häuser · Noten · Empfehlung. Jede Angabe mit Quelle (Adresse, Datum).
- `seitenliste.json`: Liste `[{"url": "…", "titel": "…", "sprache": "de", "art": "start|zimmer|restaurant|angebote|anreise|kontakt|rechtstext|sonst", "bild_rechner": "bilder/…", "bild_handy": "bilder/…"}]`, vollständig, jede Sprache.
- `einordnung.json`: `{"art": "studie|auftrag|eigene-seite", "passt": true|false, "grund": "…", "familie": [{"name": "…", "ort": "…", "website": "…"}], "schon_gebaut": ["Ordnername"], "website_ordner": "website/", "buchung": {"system": "…", "link": "…"}}`. `website_ordner` ist dort, wo der Baumeister später baut: bei neuen Häusern `website/`, bei Häusern, deren Seite im Projektordner schon an der Wurzel liegt (Carlton-Europe: `bau.py` baut nach `./`), der Projektordner selbst (`./`).
- `befund.html`: der Befund als Seite auf dem Stand der Rivage-Werkbank (Abschnitt 6), mit Link zur heutigen Seite; Adresse über `kette.py adresse`.

## 5 Am Ende: Stand, Verbrauch, Briefing

1. Offene Punkte je einzeln eintragen (Punkt plus Fundstelle):
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py offen "Culinarium Hannover" 02 "Was fehlt oder nicht belegt ist" "wo es gesucht wurde"
   ```
2. **Das Dokument selbst ist das Briefing** (Robert 15.10.2026: «Ich will den Link zur Landingpage und nicht so eine dumme Übersicht mit irgendwelchen Screenshots.»). Dein Dokument ist eine fertige Seite auf dem Stand der Rivage-Werkbank (Abschnitt 6, erster Punkt), online oder lokal; die Adresse trägst du ein, die Karte öffnet sie direkt:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py adresse "Culinarium Hannover" 02 "<Link zur Seite>"
   ```
   Lokale Seiten im Hausordner sind über `http://127.0.0.1:8978/haus/Culinarium Hannover/…` erreichbar. Keine `briefing.html` mit Bildschirmfotos oder Zusammenfassung davor.
3. Nutzungsanzeige wieder ablesen und eintragen:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py verbrauch "Culinarium Hannover" 02 <vorher> <nachher>
   ```
4. Stand auf «liegt vor» mit einem Satz:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py stand "Culinarium Hannover" 02 "liegt vor" --notiz "Ein Satz, was jetzt vorliegt."
   ```
5. Karte starten, falls sie nicht läuft (`python3 ~/Desktop/Website-Projekte/_Kette/karte/server.py`, Port 8978), deine Station dort öffnen (http://127.0.0.1:8978/?haus=Culinarium Hannover) und ansehen: die Seite erscheint direkt, jede Lücke rot, kein Fehler in der Konsole. Erst dann melden. Dein Dokument ist `befund.html`: was fehlt, was das Haus ausmacht, Noten, die Empfehlung; die heutige Seite als Link, nicht als Bild.

Ich bestätige auf der Karte mit «passt, weiter» oder schicke mit einem Satz zurück. Kommt es zurück: Satz lesen (steht in `stand.json` unter `rueckgaben` und im Lernprotokoll der Master-Datei), genau das ändern, nichts drumherum, wieder «läuft» → «liegt vor».

## 6 Regeln, die nicht verhandelbar sind

- **Nichts verschicken, nichts veröffentlichen, nichts online stellen.** Keine Mail, keine Nachricht, kein Formular, kein Upload. Der letzte Knopf bleibt meiner (Regel 58, 61; Station 16).
- **Keine Zahl erfinden, nichts schätzen.** Jede Angabe hat eine Quelle (Datei im Projektordner oder Adresse mit Datum) oder heisst «offen». Zahlen, an denen etwas hängt, zweimal unabhängig prüfen (Regel 57).
- **Nichts löschen, nichts überschreiben,** was ein anderer angelegt hat: Pakete anderer Stationen, `_quelle/`, Sicherungen, Upload-Ordner, Bild-Streifen verschickter Mails. Du schreibst nur in `_kette/<dein Ordner>/` und in die Ordner, die dein Paket nennt. Vor jeder Änderung an Bestehendem eine Sicherung daneben (`*.vor-<was>-<datum>`).
- **Nicht am Original des Kunden vorbei.** Namen, Preise, Zeiten, Rechtstexte, Formulierungen kommen aus seinen Dateien in `_quelle/` und werden dagegen geprüft, nie abgetippt oder verschönert (Regel 60d). Was der Kunde nicht hat, bauen wir nicht dazu.
- **Bauer und Prüfer sind nie derselbe Chat.** Du prüfst nicht ab, was du selbst gebaut hast, und baust nicht nach, was du prüfst.
- **Jedes Dokument hat den Stand der Rivage-Werkbank (Regel 13.5 Nr. 13, Robert 15.10.2026: «Alle Dokumente … sehen nicht so aus wie beim Rivage. Nicht so geil, nicht so schön, nicht so luxuriös.»).** Bevor du ein Dokument baust, öffnest du http://127.0.0.1:8940/werkbank/ (Master 5b) und legst es daneben. Du baust mit dem Werkbank-Kit (`~/Desktop/Website-Projekte/_Werkbank-Kit/kern.py`, `werkbank.css`, `seiten.css`; Haken wie in `Grand Beau-Rivage/website/_werkbank/haus.py`), nicht mit eigenem CSS. Woran Robert den Stand erkennt: Titelschrift des Hauses mit Betonung in Gold oder Taupe · Tapete als zartes Gitter mit Medaillon aus dem Zeichen, nie ein grosses freies Motiv · Blätter mit runder Kante, hell und dunkel im Wechsel · Platten mit Kuhle statt flacher Felder · Fenster mit Foto und Satz · Geräte aus Blender mit echtem Inhalt · Farbkarten mit dem Foto, aus dem die Farbe kommt, und den abgeleiteten Tönen darunter · Fächer, Band zum Blättern, Laufzeile · Knöpfe mit Tiefe und Glanz · Abschnittsköpfe mittig mit dem Zeichen in Gold · Auftritte federleicht von unten. Flache Flächen, Groteske als Titel, Textblöcke und Farbfelder ohne Foto: nicht fertig, kommt zurück.
- **Keine Bildschirmfotos gebauter Seiten** in Meldungen, Briefings oder auf der Karte (Robert 15.10.2026: «Ich will auf die Seiten selber gucken, ich will drüber scrollen. Gib mir da keine Screenshots von den Seiten.»). Keine Scroll-Streifen, keine Ausschnitte, keine Rechner/Handy-Paare. Eine Seite wird nur als Link gezeigt (online oder lokal über den Server der Karte). Bildschirmfotos bleiben Prüfwerkzeug in `_qa/` und in Prüfberichten.
- Keine bezahlten Werkzeuge, wenn ein kostenloses geht (Regel 54), keine Unteragenten, keine Workflows. Im Vault wird nichts angelegt, keine Notiz, kein Todo (Regel 27b); Erkenntnisse kommen ins Paket. Chrome nie in den Vordergrund, Messungen und Aufnahmen nur unsichtbar (Playwright, `NODE_PATH=~/Aussen-Pruefung/node_modules`, Helfer `~/Desktop/Website-Projekte/_Kette/aufnahme.js`), nie `pkill` auf Chrome (Regel 49).
- Du nimmst keinen Kontakt zum Haus auf, in keiner Form. Du bewertest nicht das Haus, nur seinen Auftritt.
- Keine Mediathek herunterladen, keine Hunderte Bilder: das ist Station 3. Du brauchst nur die Aufnahmen der Seiten.

## 7 Meldung an mich

**Name plus klickbarer Link zur Seite, sonst nichts** (Robert 15.10.2026). Also: «Markenbuch Castell Son Claret: <Link>». Keine Zusammenfassung, kein Ablauf, keine Ursachen (Regel 52). Offene Punkte stehen in `stand.json` und auf der Karte, nicht im Chat.
