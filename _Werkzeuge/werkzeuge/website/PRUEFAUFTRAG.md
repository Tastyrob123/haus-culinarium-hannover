# Prüfauftrag · Werkzeug «website» (Le Bureau · Der Schreibtisch)

Diesen Text als Auftrag in einen eigenen Chat geben. Der Chat kennt nur das Ergebnis und die Quellen, nicht den Bau.

---

Du prüfst unabhängig ein fertig gemeldetes Werkzeug. Du hast es nicht gebaut und glaubst keiner Aussage, die du nicht selbst nachgestellt hast. Du behebst nichts: du berichtest, Robert entscheidet.

## Was vorliegt

- Das Werkzeug: `/Users/robertreff/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website/`
  (`index.html`, `website.js`, `website.css`, `api.py`, `schicht.py`, `ausgabe.py`, `probe.py`, `beschreibe.py`, `pruefung.html`, `pruefung.js`, `pruefung.css`, `pruef.js`, `haeuser/gasterntal.json`, `haeuser/beau-rivage.json`, `STAND.md`).
- Der gemeinsame Unterbau, nur lesen: `_Werkzeuge/STAND.md`, `stamm/welt.css`, `stamm/welt.js`, `unterbau/speicher.py`, `unterbau/serve.py`.
- Das Artbook der zwei Welten: https://claude.ai/artifact/WoLQHpw5cb2vVYVSMWbLZD (mit dem Artifact-Werkzeug lesen).
- Der feste Rahmen für jedes Kontrollpanel: `/Users/robertreff/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md`, Abschnitt 7.
- Die Quellen der zwei Probehäuser, nur lesen: `~/Desktop/Website-Projekte/Berghotel Gasterntal/` und `~/Desktop/Website-Projekte/Grand Beau-Rivage/website/`.
- **Das Vorbild:** das bestehende Le Bureau des Grand Beau-Rivage, online https://grand-beau-rivage-entwurf.vercel.app/studio/ (eine Probe: was man dort speichert, bleibt im eigenen Browser) und im Quelltext `~/Desktop/Website-Projekte/Grand Beau-Rivage/website/studio/`. Robert am 12.10.2026: das Werkzeug soll daraus abgeleitet sein, dazu dasselbe für das Berghotel im Landhaus. Vergleich Ansicht für Ansicht (Übersicht, Bereich, Zeiten & Preise, Hinweis, Sprachen, Entwurf & Vergleich, Frühere Fassungen, Handy): was fehlt, was weicht ab, was ist schlechter gelöst als im Original? Nimm Aufnahmen beider nebeneinander.
- Die Vorlagen, an denen sich das Werkzeug messen lässt, nur lesen: am Grand Beau-Rivage `website/studio/`, `studio.py`, `studio_inhalt.py`; am Carlton-Europe Interlaken `control/` und `I.liste(…)`; am Berghotel Gasterntal `studio/`, `studio.py`.

## Was das Werkzeug laut Auftrag können muss

1. Seite wählen, in der Vorschau auf Text oder Foto klicken, ändern, speichern.
2. «Zeiten und Preise»: alle Zahlen der Website an einer Stelle.
3. Sprachen: zu jeder Änderung die Felder der anderen Sprachen des Hauses.
4. Hotel-Bereiche wie am Carlton (Zimmer, Preisstufen, Packages, Säle, Zeiten und Preise, Unterlagen, Stellen, Hinweis für Gäste), je Haus ein- oder ausgeschaltet: ein Landgasthof ohne Säle sieht keine Säle.
5. Entwurf, Leiste unten mit dem, was offen ist, Vorher/nachher nebeneinander, Veröffentlichen, Verlauf, Zurückholen. Alles über den gemeinsamen Speicher.
6. Eigene Prüfseite, die auch läuft, wenn das Werkzeug selbst nicht startet, mit Lexikon (Sehen, Grund, Tun).
7. Draussen bleibt: Gestaltung ändern, Abschnitte umbauen, Buchung. Karten-Abschnitte sind gesperrt und führen zum Werkzeug «karten».

So muss es gebaut sein:

- Alles Sichtbare aus `stamm/welt.css`. Der Modus-Knopf wechselt Namen, Schrift, Farben. Aufbau wie eine Profi-Software.
- Zwei Probehäuser laufen: `?haus=gasterntal` (Landhaus) und `?haus=beau-rivage` (Grandhotel). Die Quellen bleiben unberührt, gearbeitet wird auf einer Kopie unter `werkzeuge/website/_probe/<haus>/`, die nicht in Git liegt. Die Änderungen liegen als Schicht im Speicher.
- Welche Felder ein Haus hat, steht in einer Beschreibung je Haus, nicht im Code. Ein drittes Haus heisst: eine Beschreibung schreiben.
- Die Vorschau zeigt die Seite ohne Einblend-Bewegung. Nichts speichert still: nach jedem Speichern eine Quittung mit «Vorher, nachher» und «Rückgängig». Der Speichern-Knopf ist immer zu sehen.
- Kundendaten werden nie abgetippt: der Ausgangsstand ist aus der Seite gelesen.
- Oberfläche in Sie-Form, Schweizer Schreibweise (ss statt ß).
- Die unveränderte Seite ist vor und nach dem Einhängen Byte für Byte gleich. Kein seitlicher Überlauf bei 1440, 390 und 320 Breite, keine Fehler in der Konsole, keine Auswahl des Betriebssystems.

## Regeln für dich

- Nichts hochladen, nichts verschicken. Keine Hintergrund-Arbeiter.
- Browser nur unsichtbar (headless), nie ein Fenster auf Roberts Bildschirm, nie `pkill` oder `killall` auf Chrome.
- Eigener Server auf **Port 8975** mit Wegwerf-Daten und Wegwerf-Kopie, am Ende per PID beenden:
  `WERKZEUGE_DATEN=<tmp> WEBSITE_PROBE=<_Werkzeuge>/werkzeuge/website/_probe-nachpruefung python3 unterbau/serve.py 8975`
  (die Kopie vorher mit `WEBSITE_PROBE=… python3 werkzeuge/website/probe.py gasterntal beau-rivage` anlegen, am Ende löschen). Läuft auf 8970 oder 8972 etwas: nicht anfassen.
- Nichts ändern in `stamm/`, `unterbau/`, `werkzeuge/website/`, in den Quellen der Häuser, in `daten/` und in `_probe/`. Deine einzige Datei: `werkzeuge/website/PRUEFBERICHT.md`.
- `pruef.js` darfst du lesen und laufen lassen, aber es zählt nicht als Beleg. Schreib eigene Prüfungen (im Wegwerf-Ordner), die anders vorgehen als `pruef.js`.

## Was du nachprüfst

**A · Jede Aussage in `werkzeuge/website/STAND.md`.** Geh die Datei Satz für Satz durch. Zu jedem «erfüllt» in der Tabelle der Prüfpunkte: stell den Beleg selbst nach. Zu jedem «offen»: stimmt die Beschreibung der Lücke, oder ist sie grösser?

**B · Die neun Schritte, selbst gebaut, für beide Häuser, beide Welten, 1440 · 390 · 320:**
öffnen · einen Text und eine Zeit ändern · speichern · neu laden, noch da · Konflikt bei zwei gleichzeitigen Änderungen (zwei Browser-Kontexte, dazu derselbe Fall an derselben Stelle) · Vorher/nachher zeigt genau diese Stellen (zähl die markierten Elemente und vergleiche mit dem Entwurf) · veröffentlichen · die Kopie der Seite zeigt den neuen Stand (Datei auf der Platte und im Browser) · im Verlauf sichtbar · zurückholen · Seite wieder alt (Byte-Vergleich mit `cmp` oder `shasum`, nicht mit dem Werkzeug).
Dazu in jeder Ansicht: `scrollWidth` gegen `innerWidth`, Konsole, `select`/`input[type=date|time|…]`, Speichern-Knopf im sichtbaren Bereich.
**Zusätzlich im Safari-Kern (Playwright `webkit`, headless):** der Bau wurde nur im Chrome-Kern geprüft.

**C · Dinge, bei denen ein Bau typischerweise schönfärbt. Such gezielt nach dem Gegenbeispiel:**

1. *Byte für Byte:* Vergleich Quelle ↔ `grundlage` ↔ `online` mit eigenen Mitteln, vor dem ersten Öffnen, nach dem Öffnen, nach Veröffentlichen und Zurückholen. Auch die Seiten der Sprachen.
2. *Nichts abgetippt:* Stehen in `haeuser/*.json`, `api.py`, `website.js` Texte, Zeiten, Preise oder Namen eines Hauses? Zeigt das Werkzeug irgendwo einen Wert, der nicht wörtlich in der gebauten Seite steht? Nimm zehn Zeilen aus «Zeiten und Preise» je Haus und such sie im Quelltext der Seite.
3. *Zeiten und Preise vollständig:* Zähl mit einem eigenen Muster die Zeiten und Preise in den Seiten und vergleiche mit der Liste. Was fehlt (Fenster, eingebettete Daten, Attribute)? Was steht doppelt? Werden zwei verschiedene Angaben mit gleichem Wortlaut irgendwo zusammengelegt (gleicher Preis für zwei Dinge)? Wird eine Angabe, die auf jeder Seite steht, wirklich überall geändert?
4. *Sprachen:* Nimm je Sprache des Grand Beau-Rivage zwanzig zufällige Stellen und prüf von Hand, ob das zugeordnete Gegenstück wirklich dieselbe Stelle ist. Ändere einen deutschen Text ohne Übersetzung, mit Übersetzung, nur eine Übersetzung ohne Änderung im Deutschen: was steht danach in jeder der fünf Sprachen? Was passiert mit Stellen ohne Gegenstück (Arabisch)? Bleibt eine vorhandene Übersetzung je still durch Deutsch ersetzt, ohne dass das Werkzeug es vorher sagt?
5. *Bereiche:* Stimmen die Einträge von Zimmer, Säle, Packages, Preisstufen, Unterlagen, Stellen mit dem überein, was auf den Seiten steht? Sieht das Gasterntal wirklich keine Säle und keine Stellen (Navigation und direkter Abruf)? Schreib eine dritte Beschreibung für ein Haus deiner Wahl aus `~/Desktop/Website-Projekte/` (zum Beispiel Landgasthof Ruedihus oder Carlton-Europe, nur in deiner Wegwerf-Kopie und unter eigenem Namen in einem Wegwerf-Ordner): wie weit kommst du, ohne `api.py`, `schicht.py` oder `website.js` anzufassen? Wo zwingt dich das Werkzeug doch zu einer Code-Änderung?
6. *Speichern:* Gibt es irgendeinen Weg, auf dem etwas ohne Knopf oder ohne Quittung gespeichert wird? Geht eine offene Eingabe je still verloren (Seite wechseln, andere Stelle anklicken, Welt wechseln, Fenster schmal ziehen)? Ist der Speichern-Knopf je verdeckt (Blatt auf dem Handy, Fenster, Menü)? Überholt eine langsame Ansicht je eine schnellere (schnell zwischen zwei Ansichten wechseln)?
7. *Konflikt:* zwei Schreiber auf verschiedene Stellen, auf dieselbe Stelle, einer veröffentlicht während der andere tippt, einer holt zurück während der andere tippt, «Rückgängig» nach fremdem Speichern. Wird je etwas überschrieben, ohne dass es jemand liest?
8. *Eingaben:* Versuch, über ein Textfeld, einen Link, den Hinweis, eine Bildbeschreibung oder direkt über `/api/x/website/aendern/<haus>` etwas in die Seite zu bringen, das dort nicht hingehört (Skript, Ereignis-Attribut, `javascript:`-Link, Stil, fremde Klasse, überlange Eingabe, Pfad mit `..`, Seite oder Sprache ausserhalb der Beschreibung). Lässt sich eine gesperrte Karten-Stelle auf irgendeinem Weg ändern oder ausblenden?
9. *Prüfseite:* Läuft sie wirklich ohne `website.js`, ohne `website.css`, ohne Server-Teil? Hat jedes Stichwort, das Server oder Werkzeug melden können, einen Lexikon-Eintrag (such die Stichworte selbst zusammen)? Stimmen die Einträge sachlich? Führt jede Reparatur aus, was sie sagt, und nichts darüber hinaus?
10. *Gestaltung:* Setzt `website.css`, `pruefung.css` oder ein Skript irgendwo eine eigene Farbe, Schrift oder Rundung statt der Werte aus `welt.css`? Verstösst etwas gegen das Kapitel «Nie» im Artbook (Punkt in Tasten, Aufhellen bei Maus, Systemauswahl, Etikett mit Farbpunkt, graues Kachel-Raster, Vorhang beim Laden, stilles Speichern, zweites Rot, erfundene Zahlen)? Wechselt der Modus-Knopf wirklich alles (auch Fenster, Quittung, Prüfseite, Umrandungen in der Vorschau)? Texte: Sie-Form, kein ß, kein Fachwort, das ein Hotel nicht versteht. Mach Aufnahmen aller Ansichten in beiden Welten bei 1440 und 390 und sieh sie dir an: wirkt es wie eine Profi-Software im Stil des Hauses?
11. *Vorschau:* Steht jede Stelle sofort da (keine Einblend-Bewegung), auch weit unten auf der Seite? Stimmen Vorschau und veröffentlichte Seite im Wortlaut überein?
12. *Grenzen:* Was kann das Werkzeug nicht, ohne dass `STAND.md` es sagt? Achte auf: Texte in Fenstern der Seite, eingebettete Daten (Zimmer-Finder, Saal-Regler), Überschriften aus einzelnen Buchstaben, Bildbeschreibungen, Google-Texte, neue Einträge, neue Fotos.
13. *Unterbau unberührt:* `git -C <_Werkzeuge> log --stat` zeigt nur Dateien unter `werkzeuge/website/`? `git status` sauber bis auf Bekanntes? `python3 unterbau/pruefe.py` zeigt BESTANDEN? Liegt `_probe/` wirklich nicht in Git? Sind die Quellen der Häuser unverändert (`git status` dort, falls Git, sonst Änderungszeiten gegen den Zeitpunkt des Baus)?

**D · Die Prüfpunkte aus `_Werkzeuge/STAND.md`** (Backend bis Booking-Integration), besonders CMS-Datenmodell, Übersetzungsworkflow und Deployment: Für jeden Punkt dein eigenes Urteil mit Beleg, unabhängig von dem, was `werkzeuge/website/STAND.md` schreibt.

## Was du ablieferst

`werkzeuge/website/PRUEFBERICHT.md`:

- oben drei Zeilen: bestanden oder nicht, die schwersten Funde, was du nicht prüfen konntest;
- dann je Fund: was du getan hast (so, dass man es nachstellen kann), was du erwartet hast, was geschah, wie schwer es wiegt (verhindert die Arbeit · führt zu falschen Angaben auf der Website · stört · Schönheitsfehler);
- dann die Liste aus A und D mit «bestätigt», «widerlegt» oder «nicht prüfbar» je Aussage;
- kein Lob, keine Zusammenfassung des Baus.

An Robert im Chat: ein bis zwei Sätze in Alltagssprache, was das Ergebnis ist und wo der Bericht liegt.
