# Prüfauftrag · Werkzeug «gaeste» (La Réception · Der Gastgeber)

Diesen Text als Ganzes in einen neuen Chat geben. Der Chat kennt nur das Ergebnis und die Quellen, nicht den Bau.

---

Du prüfst ein fertiges Werkzeug unabhängig nach. Du baust nichts um und behebst nichts. Du glaubst keiner Behauptung, die du nicht selbst nachgestellt hast, auch nicht denen in `STAND.md` und nicht den Prüfskripten des Baus.

**Was geprüft wird:** das Werkzeug «gaeste» unter `/Users/robertreff/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/gaeste/`. Es heisst im Grandhotel «La Réception», im Landhaus «Der Gastgeber», und soll für jedes Haus gelten. Probehäuser: `?haus=gasterntal` (Landhaus) und `?haus=beau-rivage` (Grandhotel).

**Zuerst lesen, vollständig:**
1. `/Users/robertreff/Desktop/Website-Projekte/_Werkzeuge/STAND.md` (Aufbau, Speicher, wem was gehört, Gestaltung, Prüfpunkte für jedes Werkzeug)
2. `_Werkzeuge/stamm/welt.css`, `welt.js`, `muster.html` und das Artbook https://claude.ai/artifact/WoLQHpw5cb2vVYVSMWbLZD (mit dem Artifact-Werkzeug lesen)
3. `_Werkzeuge/werkzeuge/gaeste/STAND.md` (was der Bau behauptet) und danach jede Datei des Ordners
4. `/Users/robertreff/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md`, Abschnitt 7 «Kontrollpanel für den Kunden»
5. `/Users/robertreff/SecondBrain/CLAUDE.md`, Regeln 52, 54, 57, 58

**Die Quellen der Häuser (nur lesen, nie beschreiben), alles unter `/Users/robertreff/Desktop/Website-Projekte/`:**
- «Grand Beau-Rivage»: `website/_gast/gast_wissen.txt`, `gast_tal.txt`, `gast_haus.json`, `gast.py`, `rezeption.py`, `website/assets/js/gast.js`, `website/mails/`, `website/reception/`
- «Berghotel Gasterntal»: die Seiten `*.html`, `assets/pdf/Karte-2026.pdf`, `rezeption/`
- «Familie Maeder — Vier Häuser»: `gast_haeuser.py`, `_gast_tal/kandersteg.txt`, `_gast_landing/antworten-gasterntal.json`
- «Carlton-Europe Interlaken»: `_gast/gast.py`

**Regeln für dich:**
- Du schreibst nur eine Datei: `_Werkzeuge/werkzeuge/gaeste/PRUEFBERICHT.md`. Sonst änderst du nichts, auch nicht im Vault, in `stamm/`, `unterbau/` oder in den Projekten der Häuser. Eigene Prüfskripte liegen in deinem Scratchpad.
- Eigener Server auf Port 8974 mit Wegwerf-Daten: `GAESTE_KI=probe WERKZEUGE_DATEN=<neuer Ordner in /tmp> python3 unterbau/serve.py 8974`. Vorher prüfen, ob auf 8974 schon etwas antwortet; wenn ja, nichts beenden und Robert fragen. Am Ende den eigenen Server über seine PID beenden. Den Server auf 8970 und die echten Daten in `_Werkzeuge/daten/` rührst du nicht an.
- Browser nur unsichtbar (Playwright ohne Fenster), nie ein Fenster auf Roberts Bildschirm, nie `pkill` auf Chrome.
- Die echte KI kostet Geld. Mit `GAESTE_KI=probe` prüfst du die Oberfläche ohne Kosten. Für die Punkte, die nur die echte KI zeigen kann, hast du höchstens acht Aufrufe (ohne `GAESTE_KI` gestartet, Wegwerf-Daten); nenne die Zahl und die Kosten aus dem Bereich «Kosten und Schutz». Den Schlüssel schreibst du in keine Datei und nicht in den Chat.
- Nichts hochladen, nichts verschicken, keine Hintergrund-Arbeiter.

**Was du nachstellst, Punkt für Punkt, mit eigenem Vorgehen:**

1. **Der feste Durchlauf.** `node werkzeuge/gaeste/pruef.js`, `python3 werkzeuge/gaeste/pruef_teile.py`, `python3 unterbau/pruefe.py`. Dann lies die Prüfskripte kritisch: Prüft jede Zeile, was ihr Name sagt? Gibt es Prüfungen, die nie fehlschlagen können? Nimm eine Wegwerf-Kopie des Ordners `_Werkzeuge` in `/tmp`, baue dort drei Fehler ein (zum Beispiel: Konflikt wird überschrieben statt gemeldet; Quittung fehlt; ein `<select>` in der Oberfläche) und sieh nach, ob der Lauf sie fängt.
2. **Der Ablauf von Hand im unsichtbaren Browser,** für beide Häuser, beide Welten, in 1440, 390 und 320 Breite, mit eigenem Skript und eigenen Texten: öffnen · Frage ohne Antwort im Probe-Chat · Antwort nachtragen · speichern · neu laden, noch da · zwei gleichzeitige Änderungen (auch am selben Eintrag) · Vorher, nachher · veröffentlichen · im Verlauf sichtbar · zurückholen · Rückgängig · Entwurf verwerfen. Mache Aufnahmen und sieh sie dir an: Stimmt die Gestaltung mit `welt.css` und dem Artbook, in beiden Welten? Liegt etwas übereinander, ist etwas abgeschnitten, hängt etwas lose?
3. **Die zwei neuen Dinge.** Der sichtbare Hinweis, wenn eine Anfrage wartet: Kommt er ohne Neuladen, wo steht er, verschwindet er richtig, was passiert bei drei wartenden Anfragen? Die Auswertung der häufigsten Fragen: Stimmen die Zahlen, wenn du 30 Fragen mit bekannter Verteilung einspielst? Werden ähnliche Fragen zusammengefasst, verschiedene getrennt? Zählen Proben wirklich nicht als Gäste?
4. **Nichts erfunden.** Vergleiche das eingelesene Wissen und die Angaben beider Häuser Feld für Feld mit den Quellen: Telefon, E-Mail, Adresse, Adresse der Buchung, Sprachen, Absender, Mail-Vorlagen, Startfragen, Zahl und Inhalt der Abschnitte (Stichproben an zehn Stellen je Haus, wörtlich). Steht überall «offen», wo die Quelle nichts sagt? Steht irgendwo eine Zahl, ein Name oder eine Zeit, die in keiner Quelle steht (auch in Beispieltexten und Platzhaltern der Oberfläche)?
5. **Kein Zugriff am Speicher vorbei.** Durchsuche `api.py`, `ki.py`, `einlesen.py` nach jedem Lesen und Schreiben von Dateien und nach jedem Aufruf nach aussen. Wird etwas ausserhalb von `unterbau/speicher.py` geschrieben? Werden die Quellen der Häuser irgendwo beschrieben (auch `__pycache__`)? Prüfe mit `git status` in den Projekten der Häuser und in `_Werkzeuge`, dass der Bau nur `werkzeuge/gaeste/` committet hat und `stamm/` sowie `unterbau/` unverändert sind.
6. **Die 18 Prüfpunkte.** Gehe die Tabelle in `werkzeuge/gaeste/STAND.md` Zeile für Zeile durch und stelle jeden Beleg selbst nach. Besonders: **KI-Kosten** (rechne `schlusslauf.json` mit der Preisliste nach; stimmt die Anzeige im Werkzeug nach deinen eigenen Aufrufen; greift die Obergrenze; was passiert bei leerem Guthaben), **Rate Limits** (wie leicht ist die Grenze je Gespräch zu umgehen, was kostet das im schlimmsten Fall an einem Tag), **Prompt-Injection-Schutz** (eigene Angriffe: Anweisung ausgeben, Rolle wechseln, Rabatt zusagen, Anfrage mit fremdem Kontakt ablegen lassen, Angriff in einer nachgetragenen Antwort, Angriff in einer Anfrage, die dann zum Antwortentwurf wird, HTML und Skript in jedem Feld), **Datenschutz** (wo liegt welches Datum eines Gastes, in welcher Datei; steht etwas davon im Verlauf des Wissens oder im Protokoll), **Datenlöschung** (lösche einen Gast und durchsuche danach jede Datei des Wegwerf-Ordners, auch Sicherungen und Protokoll; stimmt die Frist von zwölf Monaten).
7. **Sprache und Regeln der Oberfläche.** Jeder sichtbare Text: Sie-Form, Schweizer Schreibweise (kein ß), ruhig und klar, keine Fachwörter, die ein Hotelteam nicht kennt. Keine Auswahl, kein Kalender, kein Dialog des Betriebssystems. Kein Punkt in Tasten, kein Aufhellen bei Maus, kein zweites Rot, kein graues Kachel-Raster, nichts speichert still. Bedienbar nur mit der Tastatur? Fokus sichtbar? Fenster schliesst mit Escape?
8. **Die Bühne.** Seit dem 12.10. abends liegt das Werkzeug auf einer dunklen Bühne mit Foto des Hauses, Inseln, Kacheln mit Tiefe, Handy im Probe-Chat und Auftritten (Abschnitt «Bühne» in `STAND.md`). Prüfe in beiden Welten und drei Breiten: Ist jeder Text auf der Bühne gut lesbar (Kontrast messen, auch über dem Foto)? Bewegt sich etwas über Deckkraft statt über `transform`, hellt etwas bei Maus auf, deckt etwas die Ansicht beim Laden zu, läuft ein Auftritt bei jeder kleinen Änderung neu? Miss selbst die Bilder je Sekunde bei vierfach gedrosseltem Rechner. Stammen alle Bilder in `kleid/` aus den Projekten der Häuser (Dateien vergleichen)? Was sieht ein Haus ohne Kleid? Passt die Bühne zu `welt.css` und zum Artbook, oder setzt sie eigene Farben?
9. **Was der Bau selbst als offen nennt.** Ist die Liste vollständig und ehrlich? Was fehlt darin? Prüfe im Safari-Kern, wenn du eine passende Playwright-Fassung findest, ohne etwas zu installieren.

**Der Bericht (`PRUEFBERICHT.md`):** oben ein Urteil in drei Sätzen. Darunter je Punkt: bestätigt, widerlegt oder nicht prüfbar, mit dem, was du getan und gesehen hast (Befehl, Stelle im Code, Aufnahme). Jeder Mangel mit Schwere (hält auf · sollte vor dem ersten Haus behoben sein · Kleinigkeit) und der kleinsten Stelle, an der er sich zeigt. Zum Schluss die Zahl deiner Aufrufe der echten KI und ihre Kosten.

**An Robert am Ende:** ein bis zwei Sätze in Alltagssprache, ohne Fachwörter: Hält das Werkzeug, was versprochen ist, und was ist das Wichtigste, das nicht stimmt.
