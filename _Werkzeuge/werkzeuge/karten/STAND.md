# karten · La Carte (Grandhotel) · Die Tafel (Landhaus)

Stand 12.10.2026, abends. Zuerst `../../STAND.md` lesen (Aufbau, Speicher, wem was gehört), dann diese Datei.

**Adresse:** `http://127.0.0.1:8970/werkzeuge/karten/?haus=gasterntal` und `…?haus=beau-rivage`
(Server: `python3 unterbau/serve.py`; läuft er schon, mitbenutzen). Der Knopf oben rechts wechselt die Welt des Werkzeugs.

## Aufbau der Oberfläche: eins zu eins nach La Carte am Grand Beau-Rivage (Robert 12.10.2026, 21:40)

Robert: «Das Konzept, das wir schon geschickt haben, eins zu eins adaptieren, daraus einen Dummy weiterentwickeln, dann für das
Luxushotel mit der vorgegebenen Farbwelt und für das Waldhotel in seiner Welt.» Die erste Fassung dieses Werkzeugs hatte einen eigenen
Aufbau (helle Arbeitsfläche, Auswahlliste, vier Schritte). Sie ist ersetzt. Vorlage ist `Grand Beau-Rivage/website/mission-control/`
(`mc.js`, `mc.css` Fassung 2, `mc-bureau.css` Fassung 3), so wie es dem Haus gezeigt wurde.

**Übernommen, Zug um Zug:** dunkler Raum · Kopfleiste als Insel (Zeichen, Name des Werkzeugs, in der Mitte die Karte und ihr Stand) ·
Seitenleiste als Papierplatte mit «Ihre Karten», dem Schalter Einfach / Fortgeschritten samt Erklärsatz und den «Wegen» · Kopf mit Zeichen,
zweifarbigem Titel («Karte *L’Ambiance.*»), Zeile mit Raute, Satz und «Neuer Eintrag» · links die Einträge als Platten (Deckblatt dunkel,
Rubrik mit «Eintrag hinzufügen» und Pfeilen, Zeilen mit Preis rechts und Tasten beim Überfahren, Kennzeichen Neu / Geändert / Verschoben /
Ausgeblendet, unten «Eintrag am Ende» und «Neue Rubrik») · rechts die Karte auf heller Platte mit «5 Seiten, wie in der PDF» und Grösser / Kleiner ·
unten die Leiste als schwebende Insel (Stand, «Vorher / nachher», «Probe-PDF», «Alles gespeichert», «Veröffentlichen») · Fenster mit grossem
zweifarbigem Titel, links die Felder, rechts «So steht es auf der Karte» · Quittungen als Insel links über der Leiste mit «Rückgängig» und
«Vorher / nachher» · dieselben Abläufe und derselbe Wortlaut, wo er für jedes Haus gilt (Klick auf einen Eintrag öffnet ihn, Klick in die
Karte ebenso, jede Änderung sofort im Entwurf, Veröffentlichen führt über «Vorher und nachher», «Daten der Karte» im Weg Fortgeschritten).

**Das Kleid des Hauses** (seit 12.10.2026 22:45, wie im Original): Zeichen, Tapete und ein Foto je Karte kommen vom Haus selbst.
`kleid.py <haus>` liest sie aus dem Projekt des Hauses (nur lesen, Rezept in `quellen.json`) und legt sie nach `kleid/<haus>/`, so wie es
`werkzeuge/gaeste/` tut. Grand Beau-Rivage: Medaillon, Tapete und die vier Fotos aus La Carte. Berghotel Gasterntal: der Schriftzug des Hauses
(ein rundes Zeichen hat es nur als Bild mit dem Tippfehler «NAUR»), keine Tapete, als Foto die gedeckte Tafel (für dieses Werkzeug gewählt).
Das Zeichen steht in Kopfleiste, Kopf und Deckblatt-Zeile, die Fotos an «Ihre Karten», die Tapete auf dem Raum, aber nur in der Welt des Hauses
(wechselt der Knopf die Welt, bleibt die Fläche frei). **Auf der gedruckten Karte** steht das Zeichen auf dem Umschlag und im Kopf jeder Seite,
die Tapete auf dem Umschlag, wie in den Karten des Hauses. Ein Haus ohne Kleid (Prüflauf «drittes Haus») bekommt einen Ring mit seinen
Anfangsbuchstaben, Kacheln mit Initialen und seinen Namen auf der Karte.

**Bewusst anders, weil es für jedes Haus und in beiden Welten gelten muss:**

| Im Original | Hier | Grund |
|---|---|---|
| Farben und Verläufe fest in der Stildatei | jede Farbe, Schrift und Rundung aus `stamm/welt.css` (Roberts «vorgegebene Farbwelt», Artbook); der Hauptknopf «Veröffentlichen» ist wie im Original aus Metall, gemischt aus den Farben der Welt | ein Bau, zwei Welten; die Grandhotel-Werte sind dieselben wie am Haus |
| Lichtstreif und Aufhellen bei Maus, Fläche blendet ein | Knöpfe des Stamms (geben nach, Knauf rückt), Platten schweben deckend herein | Regeln «Nie» des Artbooks |
| Kennzeichen in Gelb und Grün | Kennzeichen ohne Farbe; der Speicherknopf wird wie im Original zu Metall, sobald etwas offen ist; Rot nur die Marke «Entwurf» | ein Farbpunkt je Ansicht |
| Schalter «Karte / Website» zeigt die Seite des Hauses | Schalter steht da; «Website» sagt ehrlich «noch nicht angeschlossen» | die Seiten der Häuser lesen ihre Karte noch nicht aus diesem Werkzeug |
| Wege zu Unterlagen, Werkbank, Website, Anleitung, Le Bureau | dafür «PDF der Karte öffnen», «Karte einrichten», oben der Modus-Knopf | es gibt noch keine Nachbar-Werkzeuge, an die es anschliesst |
| Kästchen und Auswahlliste des Betriebssystems (Auf der Karte zeigen, Sprache des Hinweises) | Schalter und Tasten im Stil des Hauses | Regel «keine Systemauswahl» |
| ein Feld «Preis», mehrere mit · getrennt | dasselbe Feld; dazu auf Wunsch «Preis mit Angabe» («33cl», «Portion») und feste Spalten einer Tafel | die Karte des Gasterntals braucht beides |
| Entwurf je Karte | ein Entwurf je Haus (alle Karten), an jeder Karte steht «Entwurf», wenn sie betroffen ist | Vertrag des gemeinsamen Speichers |
| Veröffentlichen baut PDF und Website in drei Minuten, mit Schritten | PDF in Sekunden; das Fenster nennt die Schritte, hakt sie aber nicht einzeln ab | ein Aufruf, kein Fortschritt zum Mitlesen |
| Vorschau im selben Dokument | Vorschau in eigenem Rahmen (`druck.html`) | die Karte bleibt in der Welt des Hauses, während der Knopf die Welt des Werkzeugs wechselt |

**Wie im Original, seit 12.10.2026 nachts:** Entfernen (Papierkorb an jeder Zeile und Rubrik, «Von der Karte nehmen» im Fenster, mit Rückfrage und
«Rückgängig»), daneben das Ausblenden (Auge) aus dem Auftrag.

**Dazugekommen** (hat das Original nicht): Konflikt bei zwei gleichzeitigen Änderungen, Name und Notiz beim Veröffentlichen, «Ansehen» einer
früheren Fassung, «Was zuletzt geschah», Zeitraum der Karte, Allergene, Vermerk «Englisch nachziehen», Prüfung PDF gegen Daten vor dem Umschalten.

## Was steht

| Was | Wo | Stand |
|---|---|---|
| Karte des Landhauses als Daten | `grundstand/gasterntal.json`, gelesen mit `einlesen/gasterntal_lesen.py` aus der PDF des Hauses | 1 Karte «Ässe u trinke», 100 Einträge, 103 Preise, Wortlaut des Hauses |
| Karten des Grandhotels als Daten | `grundstand/beau-rivage.json`, übernommen mit `einlesen/beau_rivage_lesen.py` | 4 Karten, 397 Einträge, unverändert |
| Abgleich gegen das Original | `einlesen/abgleich.py` → `_qa/gasterntal-abgleich.md`, `_qa/beau-rivage-abgleich.md` | beide OHNE ABWEICHUNG, Gegenprobe fällt auf |
| Erster Stand im Speicher | `einlesen.py alle` (ruft `grundstand_setzen`, nur nach bestandenem Abgleich) | beide Häuser eingelesen, PDF je Karte liegt bereit |
| Datenmodell | `modell.py` (Form, Prüfung jeder Eingabe, PDF gegen Daten, Sprachen) | für jedes Haus dasselbe |
| Satz der gedruckten Karte | `satz.js`, `satz.css`, `druck.html` | eine Datei für Vorschau und PDF |
| PDF-Druck | `pdf.js` (unsichtbarer Browser, etwa 1 Sekunde je Karte) | über `api.py` |
| Eigene Wege | `api.py`: uebersicht, entwurf, probe, veroeffentlichen, pdf, kontrolle | |
| Oberfläche | `index.html`, `karten.js`, `karten.css` | eins zu eins nach La Carte am Grand Beau-Rivage, beide Welten, 1440 / 390 / 320 |
| Fester Prüfdurchlauf | `pruef.js` → `_qa/pruef-letzter-lauf.txt` | BESTANDEN, 614 Prüfungen, rund 230 Sekunden (zuletzt 12.10.2026 23:20) |
| Kleid der Häuser | `kleid.py`, `quellen.json` → `kleid/<haus>/` | Zeichen, Tapete, Fotos für beide Probehäuser |
| Tippfehler des Gasterntals | `einlesen/gasterntal_berichtigen.py` → `_qa/gasterntal-berichtigt.md` | 26 Berichtigungen an 28 Stellen, liegen als Entwurf bereit; veröffentlicht ist der Wortlaut des Hauses |
| Speicher-Probelauf | `python3 unterbau/pruefe.py` | BESTANDEN, 21 Prüfungen |
| Auftrag für die unabhängige Prüfung | `PRUEFAUFTRAG.md` | fertig, als Prompt für einen eigenen Chat |

### Was das Werkzeug kann

- **Karte wählen** (Seitenleiste «Ihre Karten»), **Eintrag ändern** (Klick auf die Zeile oder auf den Text in der Karte), **neuer Eintrag**
  geführt (erst die Rubrik, dann das Fenster mit Art, Feldern und «So steht es auf der Karte»), **neue Rubrik** (erscheint auf der Karte,
  sobald ein Eintrag darin steht), **ausblenden** (Auge, der Eintrag bleibt in den Daten) oder **entfernen** (Papierkorb, mit Rückfrage und «Rückgängig», wie im Original), **verschieben** (Eintrag oder ganze Rubrik),
  Deckblatt, «Karte einrichten» (Zeitraum, Fusszeile).
- **Preise in der Schreibweise des Hauses:** Die Zahl genügt. «9» wird am Gasterntal «9.00», im L’Ambiance «CHF 9», in einem Haus mit
  «11,5» bleibt «12,5». Massgeblich sind die Preise in derselben Rubrik, sonst die der Karte.
- **Zwei Wege:** «Einfach» (Liste und Fenster) und «Fortgeschritten» (direkt in der Karte schreiben, gespeichert wird mit dem Knopf in der
  Leiste; dazu «Daten der Karte» als Text).
- **Rechts immer die Karte, wie sie gedruckt wird.** Vorschau, das kleine «So steht es auf der Karte» im Fenster und die PDF kommen aus
  derselben Druckseite und demselben Satz. Der Prüflauf vergleicht je Karte Seite für Seite: gleich viele Seiten, auf jeder derselbe Text.
- **Die Karte folgt der Welt des Hauses** (`haus.json`), der Modus-Knopf oben rechts wechselt nur das Werkzeug.
- **Entwurf → Vorher / nachher → Veröffentlichen → Frühere Fassungen → In den Entwurf holen** über den gemeinsamen Speicher. Nach jedem
  Speichern eine Quittung mit «Rückgängig» und «Vorher / nachher». Ohne Änderung: «Nichts geändert, nichts gespeichert.»
- **Veröffentlichen** druckt jede geänderte Karte neu, prüft die PDF Wort für Wort gegen die Daten, prüft die Regeln des Umbruchs und schaltet
  erst dann um. Stimmt etwas nicht, wird nichts veröffentlicht (Stichwörter `umbruch`, `pdf-ungleich-daten`, `druck`).
- **Umbruch:** kein Gericht allein auf einer Seite, keine Rubrik von ihrem ersten Gericht getrennt (auch nicht mit Erläuterung dazwischen),
  nichts läuft über das Blatt. Erzwungen in `satz.js` (`packe`, `allein_beheben`), nachgeprüft mit `regeln()` in Vorschau, PDF-Druck und Prüflauf.
- **Im Datenmodell vorgesehen, leer:** Zeitraum je Karte (`gilt.von`, `gilt.bis`) und Allergene je Gericht (14 Zutaten nach Lebensmittelrecht,
  im Fenster unter «Allergene angeben»; gesetzt erscheinen sie als Zeile «Enthält: …» unter dem Gericht).
- **Draussen bleiben:** Bestellen, Kasse, Kalkulation.

### Die Karte des Gasterntals: was Robert wissen muss

- Gelesen aus `Berghotel Gasterntal/assets/pdf/Karte-2026.pdf` (Word-PDF des Hauses vom 9.5.2026, 2 Seiten, gefaltetes Blatt mit zwei Spalten).
  Kein Wort ist abgetippt: `gasterntal_lesen.py` nimmt jeden Text aus der Textschicht, die Regeln sagen nur, welches Stück in welches Feld gehört.
- **Erster Stand = Wortlaut des Hauses, mit seinen Tippfehlern** («Tagesssuppe», «Apfelschorlle», «Aperitiv», «N0 45», «Linzer Cacke» …):
  so steht er in `grundstand/gasterntal.json`, so prüft ihn der Abgleich, so wurde er als Grundstand gesetzt.
- **Veröffentlicht ist der Wortlaut des Hauses.** Die 26 Berichtigungen, die das Projekt des Hauses für die Karte listet
  (`_werkbank/satz_daten.py`, `BERICHTIGT`, dieselben wie in der Unterlage, die dem Haus gezeigt wurde), **liegen als Entwurf bereit** und warten
  auf Roberts Wort: im Werkzeug «Vorher / nachher» zeigt jede Stelle, «Veröffentlichen» setzt sie, «Verwerfen» lässt den Wortlaut des Hauses stehen.
  Jede Stelle steht auch in `_qa/gasterntal-berichtigt.md`. Abgelegt mit `einlesen/gasterntal_berichtigen.py --als-entwurf`.
  Im Verlauf steht dazu eine Fassung von 22:48, in der die Berichtigungen kurz veröffentlicht waren (meine Entscheidung, zurückgenommen).
  Nicht in der Liste und deshalb auch im Entwurf unverändert: der Preis «5.50.» mit Punkt bei «Rugenbräu Alkoholfrei».
- Anordnung: die Einträge stehen in Lesefolge des Originals (Getränke, Leitsatz, Speisen, Jugendschutz), der Umschlag ist das Deckblatt.
  Im neuen Satz sind es 9 Seiten A4 statt eines gefalteten Blatts.
- Als «offen» in den Daten: Zeitraum, Allergene je Gericht, Währung (steht nirgends auf der Karte), das Zeichen des Umschlags (Bild, kein Text),
  Fettdruck und Aufzählungszeichen (Gestaltung).

## Was offen ist

**Roberts Antworten vom 12.10.2026, 23:30:** «Waldhotel» meint das Berghotel Gasterntal. Die Umsetzung (La Carte eins zu eins, Grandhotel-Kleid und
Welt des Landhauses) passt. Die 26 Berichtigungen bleiben als Entwurf liegen, veröffentlicht bleibt der Wortlaut des Hauses; Robert entscheidet
später im Werkzeug. Damit sind die Punkte 0 und 1 unten beantwortet bis auf die Berichtigungen selbst.

0. **Roberts Wort zu den 26 Berichtigungen** der Gasterntal-Karte: sie liegen als Entwurf im Werkzeug, veröffentlicht ist der Wortlaut des Hauses.
1. **Roberts Urteil** zur Fassung «eins zu eins nach La Carte» in beiden Welten und zu den Abweichungen in der Tabelle oben, dazu zur gedruckten
   Karte des Landhauses (dort ist der Satz neu, am Grandhotel aus dem Satz des Hauses abgeleitet). Im Landhaus sind Schriftzug statt Zeichen und
   das Foto der Tafel meine Wahl aus dem Material des Hauses.
2. **Preis «5.50.»** bei «Rugenbräu Alkoholfrei» steht mit Punkt da, wie im Original (nicht in der Liste der Berichtigungen).
3. **Anbindung an die Website des Hauses fehlt.** Die PDF gibt es nur im Werkzeug («PDF öffnen»). Die Restaurant-Seiten und die Unterlagen
   der beiden Häuser lesen weiter aus ihren Projekten, nicht aus diesem Speicher.
4. **Kaputter Entwurf:** Wird am Werkzeug vorbei ein Entwurf in falscher Form gespeichert (allgemeiner Weg des Servers), startet das Werkzeug
   nicht mit ihm, bietet aber an, ihn zu verwerfen, und veröffentlicht ihn nie. Verhindern kann es das Speichern selbst nicht (Wunsch an den Stamm).
4a. **Sprachfassungen** (eigene Karte je Sprache): das Modell und die Erkennung «veraltet» stehen, bearbeiten und drucken lassen sie sich noch
   nicht. Die fünf Sprachfassungen des Grand Beau-Rivage sind nicht übernommen.
5. **Neue Karte anlegen oder eine Karte entfernen** geht noch nicht im Werkzeug (nur über `einlesen.py`).
6. **Im Weg «Fortgeschritten»** lässt sich schreiben und über «Daten der Karte» alles ändern, aber nichts mit Knöpfen anlegen oder verschieben.
6a. **Quittungen** stehen links über der Leiste auf der Liste (wie im Original). Durch ihre Fläche klickt man hindurch, nur ihre Knöpfe fangen den Klick.
7. **Nur im Chromium-Kern geprüft**, nicht in Safari und Firefox. Bedienung mit Tastatur und Vorleseprogramm ist angelegt (Fokus, Beschriftungen),
   aber nicht eigens geprüft.
8. **PDF des Grandhotels:** den gesperrten Namen des Hauses liest ein Textauszug buchstabenweise («G R A N D»). Für das Auge und den Druck
   ohne Belang, für die Suche in der PDF nicht schön.
9. **PDF = Daten** prüft Wörter und Seiten, nicht die Stelle auf dem Blatt. Dass der Preis in der Zeile seines Gerichts steht, prüft der
   Prüflauf an den geänderten Gerichten, nicht an allen.
10. Alles aus der Liste «Noch nicht da» der gemeinsamen STAND.md (Anmeldung, Rechte, Ablage ausserhalb des Rechners, Überwachung, Grenzen).

## Datenmodell (CMS-Datenmodell)

Ein Haus = ein Dokument im Speicher unter `karten` (`modell.py`, Kopf der Datei):

```
{ schema: 1, haus,
  karten: [ { id, gilt: {von, bis}, fassungen: { en: { stand_de, karte } }, herkunft, offen: [],
              karte: { ziel, name, gruppe, format: [breite, höhe], kl, fuss, teile: [ deckel | inhalt ] } } ] }
Posten: rubrik · land · zw · kopf · zeile · notiz · gericht · frei
gericht: name, zusatz, zeilen[{text, en, fett, preise}], preise[], einheiten[], allergene[], uebersetzung, aus
```

- Die Karten des Grand Beau-Rivage passen **unverändert** hinein (Abgleich: Feld für Feld gleich).
- Für das Gasterntal kamen vier freiwillige Felder dazu, die jedes Haus brauchen kann: `einheiten` (Angabe zum Preis: «33cl», «Portion»),
  `koepfe` auch am Zwischentitel, `zusatz` an der Rubrik («ab 2 Personen»), leere Preiszelle in einer Tafel.
- Was das Werkzeug um die Karte führt (Zeitraum, Sprachfassungen, Herkunft, Offenes), steht neben der Karte, nie in ihr.
- Ausgeblendet = `aus: true`. Gelöscht wird nie.
- Im Code des Werkzeugs steht kein Haus (`grep -i "gasterntal\|rivage"` in karten.js, satz.js, satz.css, karten.css, druck.html, index.html,
  api.py, modell.py, pdf.js: nichts ausser Beispielen in Kommentaren). Häuser stehen nur in `einlesen/`, `grundstand/` und im Prüflauf.

## Prüfpunkte (Liste aus der gemeinsamen STAND.md, Punkt für Punkt)

| Prüfpunkt | Stand | Beleg oder was fehlt |
|---|---|---|
| Backend | **offen** | Läuft nur auf diesem Rechner über `unterbau/serve.py`. Für die PDF braucht der Server node, Playwright mit Chromium und poppler. Absturz mitten im Veröffentlichen: umgeschaltet wird erst nach bestandener Prüfung in einem Schritt des Speichers; liegen schon neue PDF ab, aber der Stand ist noch der alte, merkt `pdf` das an der Kennung und druckt nach. |
| Datenbank | **offen**, Teil erfüllt | Dateien über den Speicher, kein direkter Zugriff. Grössen heute: Gasterntal 24 kB, Beau-Rivage 99 kB je Stand; die Fächer der PDF 190 bis 900 kB je Karte (base64, mit einer abgelösten Fassung). Keine Obergrenze: jeder veröffentlichte Stand und jede abgelöste PDF bleiben im Verlauf. Zwei Schreiber: Konflikt statt Überschreiben, im Prüflauf in 12 von 12 Durchläufen belegt («Konflikt hat nichts überschrieben»). |
| Authentication und Rollen | **offen** | Fehlt. Jede Änderung nennt `wer`, aber das ist der Name, den jemand eintippt, nicht geprüft. |
| Rechteverwaltung | **offen** | Fehlt. |
| API-Sicherheit | **offen**, Teil erfüllt | Erfüllt: jede Eingabe über die eigenen Wege wird auf Form, Arten, Längen und Kennungen geprüft (`modell.pruefe`, Antwort 422; Prüflauf «Daten in falscher Form werden abgelehnt»). Texte werden überall als Text gesetzt, nie als HTML (Prüflauf «eingeschleuste Zeichen … nicht ausgeführt»). Der PDF-Druck lädt nur die Stildatei des Stamms, die Schriften und drei eigene Dateien von der Platte und nichts aus dem Netz. Offen: die allgemeinen Wege des Servers (`PUT /api/entwurf`, `POST /api/veroeffentlichen`) nehmen die Karten ungeprüft an und umgehen die PDF-Prüfung (Wunsch an den Stamm); niemand wird angemeldet; nach aussen nicht gebaut. |
| Rate Limits | **offen** | Fehlt. `probe`, `veroeffentlichen` und `pdf` starten je Aufruf einen Browser (etwa 1 Sekunde): ohne Grenze lässt sich der Rechner damit beschäftigen. |
| Logging | **erfüllt** (lokal) | Protokoll des Speichers je Haus: wer, wann, was (Entwurf, verworfen, veröffentlicht mit Notiz, zurückgeholt). Im Werkzeug unter «Frühere Fassungen» zu lesen («Was zuletzt geschah»). Jede Fehlermeldung trägt ein Stichwort. Fehler des Servers stehen in seiner Ausgabe (der Prüflauf verlangt, dass dort keine stehen). Einschränkung: `wer` ist nicht geprüft. |
| Backups | **offen**, Teil erfüllt | Jeder veröffentlichte Stand bleibt im Verlauf und lässt sich zurückholen (Prüflauf: «PDF wieder alt», «Daten wieder genau wie vor dem Durchlauf»). Sicherung der letzten Fassung macht der Speicher. Keine Kopie ausserhalb des Rechners. |
| Deployment | **offen** | Nichts ist online, nichts wird hochgeladen. Git je Schritt im eigenen Ordner. Wie die PDF und die Karten auf die Website des Hauses kommen, ist nicht gebaut. |
| CMS-Datenmodell | **erfüllt** | Prüflauf «drittes Haus»: ein erfundenes Haus (`_qa/probehaus.json`, anderes Format A5, Preise mit Komma, Tafel, Allergene, Sprachfassung) kommt mit `einlesen.py --datei` in den Speicher und läuft ohne eine Zeile Änderung am Werkzeug: Liste, Preis in seiner Schreibweise, veröffentlichen, PDF, Kontrolle. Dazu der Abschnitt «Datenmodell» oben. Einschränkung: seine `haus.json` legt der Stamm an; ohne sie lief es als Grandhotel. |
| Übersetzungsworkflow | **Teil erfüllt, Teil offen** | Zwei Fälle. (1) Englische Zeile in derselben Karte (beide Probehäuser): Ändert jemand das Deutsche und das Englische nicht, bekommt der Eintrag den Vermerk `uebersetzung: offen`, steht in der Liste als «Englisch nachziehen», im Fenster beim englischen Feld, und vor dem Veröffentlichen im Fenster «Vorher und nachher» als Hinweis mit Namen. Veröffentlichen bleibt möglich (das Haus entscheidet), die Karte erscheint dann mit der bisherigen englischen Zeile. Belegt im Prüflauf je Haus. (2) Eigene Karte je Sprache (`fassungen`): jede trägt die Kennung des deutschen Stands, zu dem sie passt. Ändert sich das Deutsche, gilt sie sofort als veraltet (`uebersicht`, Prüflauf «drittes Haus») und das Fenster «Vorher und nachher» sagt vor dem Veröffentlichen, dass sie zurückbleibt. Offen: Sprachfassungen bearbeiten, drucken und als «nachgezogen» bestätigen; welche Einträge sich seit der Übersetzung geändert haben, zeigt das Werkzeug noch nicht einzeln. |
| KI-Kosten | **betrifft dieses Werkzeug nicht** | Es ruft keine KI. |
| Prompt-Injection-Schutz | **betrifft dieses Werkzeug nicht** | Keine KI liest die Texte. Was eingegeben wird, wird nur gesetzt und gedruckt. |
| DSGVO und Schweizer Datenschutz | **offen**, klein | Keine Daten von Gästen. Personenbezogen ist nur der Name, den Mitarbeitende beim Veröffentlichen eintragen (Verlauf, Protokoll, dazu im Browser gemerkt). Gehört in die Regelung, sobald es eine Anmeldung gibt. |
| Datenlöschung | **offen** | Verlauf, Protokoll und abgelöste PDF werden nie gelöscht, das Werkzeug bietet dafür nichts an. Mit ihnen bleiben die eingetragenen Namen. |
| Verfügbarkeit | **offen** | Gäste berührt das Werkzeug nicht. Fällt es aus, kann das Team nichts ändern; was veröffentlicht ist, bleibt. Solange die Website die Karte nicht aus diesem Speicher holt, hängt für den Gast nichts daran. |
| Monitoring | **offen** | Fehlt. Vorbereitet: `GET /api/x/karten/kontrolle/<haus>` prüft Form, PDF vorhanden, PDF = Daten und antwortet mit `gut: true/false`; das kann eine Überwachung abfragen. |
| Booking-Integration | **betrifft dieses Werkzeug nicht** | Karten haben mit der Buchung nichts zu tun. |

## Prüfen

```
cd ~/Desktop/Website-Projekte/_Werkzeuge
node werkzeuge/karten/pruef.js        # 12 Durchläufe + Werkzeug je Haus + drittes Haus, Port 8973, Wegwerf-Daten, unsichtbar
python3 unterbau/pruefe.py            # Speicher
python3 werkzeuge/karten/einlesen/abgleich.py gasterntal     # Daten gegen das Original, schreibt _qa/gasterntal-abgleich.md
python3 werkzeuge/karten/einlesen/abgleich.py beau-rivage
curl -s http://127.0.0.1:8970/api/x/karten/kontrolle/gasterntal   # veröffentlichter Stand: Form, PDF, PDF = Daten
```

`pruef.js` startet seinen eigenen Server und beendet ihn per PID, liest nie die echten Daten und bricht ab, wenn Port 8973 belegt ist.
Nur zum Entwickeln: `PRUEF_NUR=werkzeug node werkzeuge/karten/pruef.js` lässt die zwölf Durchläufe aus (zählt nicht als bestanden).

## Gelernt beim Bauen

- **Abgleich braucht zwei Durchgänge.** Wort für Wort merkt nicht, wenn zwei Preise vertauscht sind. Erst der Durchgang Zeile für Zeile
  (jeder Eintrag muss seine Zeilen genau aufbrauchen) fängt das. Die Gegenprobe hat es gezeigt.
- **`pdftotext -bbox` trennt ein Wort, wo die Schrift wechselt** (im Original: Anführungszeichen in anderer Grösse). Stücke ohne Lücke gehören zusammen.
- **Gesperrte Versalien liest pdftotext buchstabenweise.** Vergleiche von PDF-Text deshalb auf Zeichen oder mit der Regel «gleiche Zeichen, anders getrennt».
- **Die Vorschau steckt in einem eigenen Rahmen** (`druck.html`), weil die Karte in der Welt des Hauses bleiben muss, während das Werkzeug die Welt
  wechselt. Verkleinert wird mit `transform`, nie mit `zoom`: sonst bricht der Text anders um als in der PDF.
- **Eine Rubrik ohne Eintrag wird nicht gedruckt.** Sonst steht sie nach «Neue Rubrik» allein am Ende einer Seite. `modell.gedruckte_posten`
  und `satz.js` müssen dieselbe Regel haben, sonst stimmt PDF gegen Daten nicht.
- **Zwei aufeinanderfolgende Rubriken sind erlaubt** («Einisch öpis anders» über «Suppä» im Gasterntal): die erste ist ein Obertitel, kein Versehen.
- **`SATZ_VERSION`** in `satz.js` und `modell.py` zusammen hochzählen, wenn sich am Satz etwas ändert: gespeicherte PDF gelten dann als veraltet
  und werden beim nächsten Abruf neu gedruckt und geprüft.
- **Der gemeinsame Server lädt nur `api.py` frisch, nicht dessen Hilfsdateien.** Nach einer Änderung an `modell.py` lief der Server auf 8970 mit
  der neuen `api.py` und der alten `modell.py` und antwortete mit einem Fehler. `api.py` lädt `modell` deshalb bei jedem Aufruf neu (`importlib.reload`).
- **Zwei Dinge, ein Klassenname:** `kt-deck__z` hiess das Zeichen und die Zeilen des Deckblatts, die Zeilen wurden 34 mm schmal. Das Zeichen heisst `kt-deck__m`.
- **Eine Quittung vom Schritt davor täuscht den Prüflauf.** Jede Quittung beginnt mit «Gespeichert im Entwurf». Wer nur darauf wartet, läuft weiter,
  bevor gespeichert ist. Das hat einen echten Wettlauf gezeigt: «Speichern» und sofort der Wechsel des Wegs öffnete eine Rückfrage, die beim Ende
  des Speicherns verschwand, ohne zu wechseln. Jetzt wartet der Wechsel das laufende Speichern ab (`laufend`, `offeneFrage` in karten.js).
- **Ein Fenster setzt die Schreibmarke 30 ms nach dem Öffnen ins erste Feld.** Tippt ein Prüfskript sofort in ein anderes Feld, landet der Text
  im ersten («40Mango Garnelen Salat»). Im Prüflauf deshalb auf den Fokus warten, bevor getippt wird.
- **Was am unteren Rand steht, liegt unter der schwebenden Leiste.** Prüfschritte holen ihr Ziel in die Mitte, bevor sie klicken.
- **`pdftotext` über die Standardeingabe blieb im Prüflauf einmal ohne Ende stehen** (Rechner unter Last durch andere Läufe, der Lauf stand elf Minuten).
  Der Prüflauf gibt die PDF jetzt als Datei im Wegwerf-Ordner und mit Frist. Im Server hat das Lesen der PDF eine Frist von 60 Sekunden und bricht
  mit Stichwort `druck` ab, statt zu hängen.
- **«Broken pipe» in der Ausgabe des Servers ist kein Fehler des Werkzeugs:** lädt der Browser neu, während ein Aufruf läuft, legt er auf, und
  `unterbau/serve.py` schreibt dazu `FEHLER … BrokenPipeError` samt Spur. Nachgestellt mit einem rohen Aufruf, der sofort auflegt. Der Prüflauf
  zählt solche Abbrüche nicht als Fehler, alles andere weiterhin. Wunsch an den Stamm: abgebrochene Verbindungen still übergehen.
- **Zwei Prüfläufe zugleich gehen nicht:** der zweite meldet «Port 8973 ist belegt» und bricht ab, ohne den ersten zu stören.
- **`waitUntil: 'networkidle'` hängt bei einem Haus ohne `haus.json`** (welt.js liest die Antwort 404 nicht aus). Im Prüflauf `load` und danach
  auf `KT.bereit()` warten.

## Verlauf

- **12.10.2026 nachts** · Entfernen, Schalter «Karte / Website» und Metallknopf wie im Original nachgezogen. Berichtigungen der
  Gasterntal-Karte zurückgenommen und als Entwurf abgelegt (Roberts Entscheidung, nicht meine).

- **12.10.2026 22:50** · Kleid der Häuser (Zeichen, Tapete, Fotos) im Werkzeug und auf der gedruckten Karte, wie im Original. Tippfehler der
  Gasterntal-Karte als eigene Fassung berichtigt und veröffentlicht. Fehler am laufenden Server (alte `modell.py`) gefunden und behoben.

- **12.10.2026 spät** · Oberfläche neu aufgebaut, eins zu eins nach La Carte am Grand Beau-Rivage, für beide Welten (Abschnitt oben).
  Die erste Fassung steht im Git davor (`222d681`). Satz, Daten, eigene Wege und Speicher unverändert. `druck.html` kann jetzt
  Unterschriften je Seite, Seiten nebeneinander, einen einzelnen Eintrag und Klickstellen. Prüflauf neu geschrieben: 585 Prüfungen bestanden.
  Dabei gefunden und behoben: lange Preisangaben («Kinder 12.00 · Für Erwachsene 26.00 · Kleine Portion 22.00») liefen am Handy seitlich
  über (stehen jetzt untereinander); eine Quittung lag über Knöpfen der Liste.

- **12.10.2026 abends** · Werkzeug gebaut. Karten beider Probehäuser als Daten, Abgleich ohne Abweichung, erster Stand im Speicher. Satz, PDF-Druck,
  Oberfläche mit beiden Wegen, eigene Wege, fester Prüfdurchlauf (575 Prüfungen bestanden), Speicher-Probelauf bestanden (21). Echte Adresse auf
  Port 8970 unsichtbar geöffnet (beide Häuser, ohne Überlauf und ohne Fehler), `kontrolle` für beide Häuser gut. Nichts hochgeladen.
  In `stamm/` und `unterbau/` nichts geändert; sieben Wünsche stehen in der gemeinsamen STAND.md (dort nicht committet, weil der Auftrag
  nur den eigenen Ordner committen lässt).
