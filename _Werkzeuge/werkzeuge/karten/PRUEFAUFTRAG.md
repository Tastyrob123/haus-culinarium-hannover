# Prüfauftrag · Werkzeug «karten» (La Carte · Die Tafel)

Dieser Text ist ein fertiger Auftrag für einen eigenen Chat. Ab der Linie kopieren.

---

Du prüfst das Werkzeug «karten» (Grandhotel: La Carte, Landhaus: Die Tafel) unabhängig nach. Gebaut hat es ein anderer Chat am 12.10.2026.
Du kennst nur das Ergebnis und die Originale. Du vertraust keinem Prüfskript und keinem Bericht des Baus, du misst selbst.
Du änderst nichts am Werkzeug. Findest du einen Fehler, beschreibst du ihn so, dass man ihn nachstellen kann, und lässt ihn stehen.

ZUERST LESEN, vollständig:
1. /Users/robertreff/Desktop/Website-Projekte/_Werkzeuge/STAND.md (Aufbau, Speicher, wem was gehört, Starten und prüfen, Prüfpunkte für jedes Werkzeug)
2. /Users/robertreff/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/karten/STAND.md (was der Bau behauptet: das ist deine Liste dessen, was zu widerlegen oder zu bestätigen ist)
3. /Users/robertreff/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md, Abschnitt 2.10 «Fakten und Kundendaten» und Abschnitt 7, Punkt «Karten-Kontrollpanel Mission Control»
4. /Users/robertreff/SecondBrain/CLAUDE.md, Regeln 52, 54, 57, 58

DEIN ORDNER: Du schreibst genau eine Datei: /Users/robertreff/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/karten/_qa/pruefbericht-unabhaengig.md.
Hilfsskripte legst du in deinen Scratchpad, nicht ins Projekt. Im Vault änderst du nichts. In stamm/, unterbau/, den anderen Werkzeugen und im Code von karten änderst du nichts.
Die Projekte der Häuser liest du nur. Die echten Daten (_Werkzeuge/daten/) liest du nur über den Server und schreibst nie hinein:
jede Prüfung, die etwas ändert, läuft auf eigenem Port 8973 mit Wegwerf-Daten (WERKZEUGE_DATEN=<Scratchpad-Ordner> python3 unterbau/serve.py 8973,
davor WERKZEUGE_DATEN=<derselbe> python3 werkzeuge/karten/einlesen.py alle). Den eigenen Server beendest du danach per PID.
Prüfen nur unsichtbar (Playwright ohne Fenster, wie _qa/aufnahme.js es findet), nie ein Fenster auf Roberts Bildschirm, nie pkill auf Chrome.
Nichts hochladen, nichts verschicken, keine Hintergrund-Arbeiter.

DIE ORIGINALE:
- Berghotel Gasterntal: /Users/robertreff/Desktop/Website-Projekte/Berghotel Gasterntal/assets/pdf/Karte-2026.pdf (Word-PDF des Hauses, 2 Seiten).
- Grand Beau-Rivage: /Users/robertreff/Desktop/Website-Projekte/Grand Beau-Rivage/website/_karten/stand/ambiance.json, petite-suisse.json, vieux-rivage.json, weinkarte.json.

WAS DU PRÜFST

A · DIE DATEN GEGEN DAS ORIGINAL
0. Zwei Stände beim Gasterntal: Veröffentlicht ist der Wortlaut des Hauses (der Bau behauptet: gleich werkzeuge/karten/grundstand/gasterntal.json,
   ohne jede Abweichung vom Original). Daneben liegt ein Entwurf mit 26 Berichtigungen an 28 Stellen
   (werkzeuge/karten/_qa/gasterntal-berichtigt.md, Liste aus Berghotel Gasterntal/_werkbank/satz_daten.py, BERICHTIGT). Prüfe beides getrennt:
   veröffentlichter Stand gegen Original Wort für Wort, und Entwurf gegen veröffentlichten Stand: sind es genau die gelisteten Stellen, keine mehr,
   keine weniger, und ist jede eine eindeutige Berichtigung und keine Verschönerung? Zeigt «Vorher / nachher» im Werkzeug genau diese Stellen?
   Falls Robert den Entwurf inzwischen veröffentlicht oder verworfen hat: sag, welchen Zustand du vorgefunden hast, und prüfe den.
1. Gasterntal: Lies das Original selbst, auf zwei Wegen: als Bild (jede Seite gross rendern und mit eigenen Augen lesen) und als Text.
   Vergleiche damit den veröffentlichten Stand aus dem Speicher (GET /api/stand/gasterntal/karten, Feld live) und die Datei
   werkzeuge/karten/grundstand/gasterntal.json. Jedes Gericht, jeder Preis, jede Schreibweise, jede Angabe zum Preis («33cl», «Portion»),
   jede Zuordnung von Preis zu Gericht, auch in den Tafeln mit drei Spalten (steht «7.00» beim Apfelwein in der richtigen Spalte?).
   Benutze dafür NICHT werkzeuge/karten/einlesen/abgleich.py und NICHT gasterntal_lesen.py, schreib deinen eigenen Vergleich.
   Der Bau behauptet: Wortlaut des Hauses ohne jede Berichtigung, nur Leerraum vereinheitlicht, Anordnung in Lesefolge. Stimmt das Wort für Wort?
   Steht irgendwo etwas, das nicht im Original steht? Fehlt etwas, das im Original steht (auch im Bild des Umschlags)? Ist die Liste «offen» vollständig?
2. Beau-Rivage: Sind die vier Karten im Speicher (Feld live, karten[].karte) Feld für Feld gleich den vier Dateien des Hauses? Zähle Einträge und Preise selbst.
3. Gegenprobe: Ändere in den Wegwerf-Daten absichtlich einen Preis, einen Buchstaben und vertausche zwei Preise benachbarter Gerichte. Fällt jeder dieser
   Fehler in deinem eigenen Vergleich auf? Erst dann gilt dein Vergleich. Lass danach zusätzlich abgleich.py laufen: kommt es zum selben Ergebnis wie du?

B · DIE PDF
1. Hol jede der fünf PDF (GET /api/x/karten/pdf/<haus>/<karte>, Feld pdf ist base64). Lies den Text heraus und vergleiche ihn mit den Daten:
   steht jeder Name, jede Zeile, jeder Preis da, steht nichts Zusätzliches da ausser dem Namen des Hauses (Umschlag und Kopf jeder Innenseite)?
   Steht jeder Preis in der Zeile seines Gerichts? Prüfe das für alle Gerichte, nicht für Stichproben.
2. Rendere jede Seite als Bild und sieh sie an. Regeln: kein Gericht steht allein auf einer Seite, keine Rubrik ist von ihrem ersten Gericht getrennt
   (auch nicht, wenn zwischen beiden eine Erläuterung steht), nichts läuft über den Rand oder in die Fusszeile, Spaltenköpfe stehen über ihren Spalten,
   nichts überlappt, keine Seite ist fast leer. Sieht die Karte des Landhauses nach Landhaus aus und die des Grandhotels nach Grandhotel?
3. Vorschau gegen PDF: Öffne das Werkzeug und vergleiche je Karte die Vorschau rechts mit der PDF: gleich viele Seiten, gleicher Umbruch, gleicher Text je Seite.
4. Versuche, die Regeln des Umbruchs zu brechen (in den Wegwerf-Daten): sehr langes Gericht, viele Gerichte ausblenden, sodass eine Rubrik nur noch eines hat,
   neue Rubrik ohne Gericht, neue Rubrik mit genau einem Gericht ganz am Ende, zwanzig neue Gerichte in einer Rubrik. Was zeigt die Vorschau, was sagt «Veröffentlichen»?

C · DAS WERKZEUG
0. Der Aufbau soll eins zu eins La Carte am Grand Beau-Rivage sein (so wie es dem Haus gezeigt wurde), als Gerüst für jedes Haus und in zwei Welten.
   Sieh dir das Original an (läuft es, unter http://127.0.0.1:8940/mission-control/, NUR ansehen, dort nichts speichern und nichts veröffentlichen;
   sonst die Dateien in Grand Beau-Rivage/website/mission-control/ lesen) und vergleiche Bereich für Bereich: Kopfleiste, Seitenleiste, Kopf, Liste, Karte,
   Leiste, Fenster, Quittungen, Abläufe, Wortlaut. Wo weicht das Werkzeug ab, und steht jede Abweichung mit Grund in der Tabelle
   «Bewusst anders» von werkzeuge/karten/STAND.md? Fehlt dort eine? Sieht das Grandhotel aus wie das Original, und trägt derselbe Bau das Landhaus?
Beide Häuser (?haus=gasterntal, ?haus=beau-rivage), beide Welten (Knopf oben rechts), Breiten 1440, 390 und 320. Schreib deinen eigenen Durchlauf,
benutze nicht werkzeuge/karten/pruef.js (lass ihn am Ende einmal laufen und vergleiche sein Urteil mit deinem).
1. Der feste Ablauf: öffnen · Preis ändern · speichern · neu laden, noch da · Konflikt bei zwei gleichzeitigen Änderungen (zwei Seiten, wird wirklich nichts überschrieben?) ·
   Vorher / nachher · veröffentlichen · die PDF enthält den neuen Preis · im Verlauf sichtbar · zurückholen · die PDF ist wieder die alte.
2. Alles andere, was das Werkzeug anbietet: neuer Eintrag (Rubrik wählen, dann das Fenster mit «So steht es auf der Karte»), Klick in die Karte, neue Rubrik, ausblenden und wieder einblenden, entfernen und «Rückgängig», Schalter «Karte / Website», verschieben (Eintrag und ganze Rubrik, auch am ersten und letzten Platz),
   Deckblatt, Karte einrichten (Zeitraum mit falschem Datum, «bis» vor «von»), Allergene, Weg «Fortgeschritten» (schreiben, speichern, «Daten der Karte», Wechsel der Karte und des Wegs mit ungespeicherter Eingabe),
   Rückgängig, Entwurf verwerfen, Probe-PDF, PDF öffnen, Verlauf ansehen, Wechsel der Karte am Grandhotel.
3. Versuche es kaputtzumachen: leerer Name, Preis mit Buchstaben, sehr lange Texte, Zeichen wie < > & " ' und Emojis, zwei Fenster gleichzeitig, Veröffentlichen während ein zweites Fenster speichert,
   Anfragen direkt an die Wege des Servers mit falschen Daten (falsche Form, fremdes Haus, unbekannte Karte, riesige Eingabe), Aufruf ohne ?haus=, mit unbekanntem Haus.
   Geht dabei je ein veröffentlichter Stand verloren oder kaputt? Entsteht je eine PDF, die nicht zu den Daten passt? Wird je etwas still gespeichert oder still verworfen?
4. Bei jedem Schritt: kein seitlicher Überlauf, keine Fehler in der Konsole, keine Auswahl, kein Kalender und kein Dialog des Betriebssystems, nichts deckt die Ansicht beim Laden zu,
   kein Knopf wird bei Maus heller, kein Punkt in Tasten, gewählt ist ein Rahmen. Texte in Sie-Form und Schweizer Schreibweise (ss statt ß), keine Fachwörter.
4a. Kleid des Hauses: Zeichen, Tapete und Fotos kommen aus werkzeuge/karten/kleid/<haus>/ (angelegt mit kleid.py aus dem Projekt des Hauses). Sind es wirklich
   die Dateien des Hauses, unverändert bis auf Zuschnitt und die Beschränkung der Zeichnung auf Formen? Kann über die Zeichnung etwas ausgeführt werden?
   Stehen Zeichen und Tapete auf der gedruckten Karte dort, wo sie in den Karten des Hauses stehen? Was zeigt ein Haus ohne Kleid?
5. Gestaltung: Kommt jede Farbe, Schrift und Rundung aus stamm/welt.css (keine festen Farbwerte in karten.css und satz.css)? Wechselt der Knopf Namen, Schrift und Farben des Werkzeugs,
   und bleibt die Karte dabei in der Welt des Hauses? Liest du irgendwo Metall (Gold, Holz) als Lesetext, ein zweites Rot, ein graues Kachel-Raster?
6. Preise in der Schreibweise des Hauses: «9», «9.5», «9,5», «CHF 9», «9.-» in verschiedenen Rubriken beider Häuser. Was wird daraus, und ist es jedes Mal die Schreibweise der Nachbarn?
7. Kein Zugriff am Speicher vorbei: Lies api.py, modell.py, pdf.js, einlesen.py. Wird irgendwo eine Datei gelesen oder geschrieben, die nicht über unterbau/speicher.py geht
   (erlaubt: haus.json lesen, die eigenen Dateien des Satzes von der Platte in den Druck-Browser geben)? Bleibt nach einem Druck irgendwo eine Datei oder ein Prozess liegen?

D · DIE PRÜFPUNKTE
Geh die Liste «Prüfpunkte für jedes Werkzeug» aus der gemeinsamen STAND.md Punkt für Punkt durch und vergleiche mit der Tabelle in werkzeuge/karten/STAND.md.
Für jeden Punkt: Stimmt, was dort als erfüllt steht, und trägt der genannte Beleg? Ist etwas als erfüllt gemeldet, das nur behauptet ist? Fehlt unter «offen» etwas?
Zwei Punkte besonders:
- CMS-Datenmodell: Bau selbst ein drittes Haus (eigene Datei in der Form aus modell.py, mit Dingen, die die zwei Probehäuser nicht haben: anderes Format, Preise mit Komma,
  drei Karten, eine Karte ganz ohne Rubriken, eine Rubrik mit fünf Spalten) und lies es mit einlesen.py --datei in die Wegwerf-Daten. Läuft das Werkzeug damit, ohne dass du etwas am Code änderst?
  Was geht nicht?
- Übersetzungsworkflow: Ändere eine deutsche Zeile, die eine englische unter sich hat. Wer merkt wo, dass die englische fehlt? Was steht danach in der PDF?
  Leg eine Sprachfassung an (fassungen) und ändere das Deutsche: gilt sie als veraltet, und sagt das Werkzeug es dem Menschen, bevor er veröffentlicht?

DEIN BERICHT (werkzeuge/karten/_qa/pruefbericht-unabhaengig.md)
- Oben in drei Zeilen: Urteil zu Daten, PDF, Werkzeug (stimmt · stimmt mit Einschränkung · stimmt nicht).
- Dann je Abschnitt A bis D jede Prüfung mit: was geprüft, wie gemessen, Ergebnis, Beleg (Zahl, Zeile, Bildname). «Nicht prüfbar» ist ein gültiges Ergebnis, eine Vermutung nicht.
- Jeder Fehler mit Weg zum Nachstellen und mit der Einschätzung, ob er Daten des Hauses gefährdet, die gedruckte Karte verfälscht oder nur stört.
- Jede Stelle, an der werkzeuge/karten/STAND.md etwas behauptet, das du nicht bestätigen kannst.
- Am Ende: python3 unterbau/pruefe.py und node werkzeuge/karten/pruef.js je einmal laufen lassen und ihr Ergebnis neben deines stellen. Wo weichen sie ab?
- Aufräumen: eigener Server per PID beendet, Wegwerf-Daten gelöscht, in _Werkzeuge ist ausser deinem Bericht nichts geändert (git status zeigt es).

An Robert am Ende ein bis zwei Sätze in Alltagssprache: stimmt die Karte, stimmt das Werkzeug, und was ist das Wichtigste, das nicht stimmt.
