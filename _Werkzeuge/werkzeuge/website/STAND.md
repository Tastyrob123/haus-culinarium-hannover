# Werkzeug «website» · Le Bureau (Grandhotel) · Der Schreibtisch (Landhaus)

Stand 12.10.2026, abends. Zuerst lesen, bevor hier etwas geändert wird. Neueste Einträge unten unter «Verlauf».
Gebaut als Prototyp, der für jedes Haus gilt. Roberts Urteil zur Gestaltung steht aus.

## Wo

- Adresse: `http://127.0.0.1:8970/werkzeuge/website/?haus=gasterntal` (Landhaus) · `…/?haus=beau-rivage` (Grandhotel)
- Prüfseite: `http://127.0.0.1:8970/werkzeuge/website/pruefung.html?haus=<haus>`
- Server: `python3 unterbau/serve.py` (Port 8970, siehe `_Werkzeuge/STAND.md`). Antwortet `curl -s http://127.0.0.1:8970/api/haus/gasterntal`, läuft er schon.
- Kopie der Seiten anlegen oder nach einem neuen Bau des Hauses erneuern: `python3 werkzeuge/website/probe.py <haus> [--neu]`.
  Die Kopie (`_probe/`) liegt nicht in Git. Fehlt sie, sagt das Werkzeug das beim Start und führt zur Prüfung.

## Woraus es abgeleitet ist (Robert, 12.10.2026 spät: «Wir haben das schon gemacht»)

Aufbau, Ablauf und Wortlaut kommen aus dem bestehenden Le Bureau des Grand Beau-Rivage
(`~/Desktop/Website-Projekte/Grand Beau-Rivage/website/studio/`, online https://grand-beau-rivage-entwurf.vercel.app/studio/). Das Original ist unberührt.
Der erste Bau dieses Werkzeugs hatte einen eigenen Aufbau (helle Fläche, drei Spalten); er liegt in Git vor dem Commit «Aufbau aus dem bestehenden Le Bureau abgeleitet».

| Aus dem Le Bureau übernommen | Hier |
|---|---|
| Dunkler Grund mit der Tapete des Hauses, Zeichen im Kopf, Titel der Ansicht in der Mitte mit dem Stand darunter | gleich. Zeichen und Tapete kommen aus den Dateien des Hauses (`kleid` in der Beschreibung), die Tapete liegt nur in der Welt des Hauses |
| Rand links als helle schwebende Platte: Übersicht · Die Website · Für alle Seiten · Karten · Entwurf | gleich, dazu «Das Haus» mit den Listen (Zimmer, Säle …) |
| Übersicht: Gruss nach Tageszeit, Lage (Entwurf, Website, Karten), «Häufig gebraucht», «Die Website, Bereich für Bereich» als Kacheln mit Foto | gleich. Am Beau-Rivage dieselben zehn Bereiche, Sätze und Fotos wie im Original (`studio.py`, `BEREICHE`), am Gasterntal ergeben sie sich aus den Seiten |
| Bereich: Stellen links (Suche, Abschnitte zum Aufklappen, die Stelle öffnet sich unter ihrer Zeile), Seite rechts (Rechner/Handy, Sprache, «Gross öffnen») | gleich |
| Zeiten & Preise: Karten je Seite, Filter Alle · Preise · Zeiten · Grössen und Dauer, «In der Seite» | gleich, dazu Suche; dieselbe Angabe auf vielen Seiten ist eine Zeile |
| Leiste unten: was offen ist · Speichern · Vorher, nachher · Veröffentlichen. Eingaben warten, bis gespeichert wird | gleich (mehrere Eingaben zugleich, die Leiste zählt sie, Cmd/Strg+S speichert) |
| Quittung über der Leiste: «Gespeichert», Vorher/nachher ansehen, Rückgängig | gleich, mit dem alten und dem neuen Wortlaut |
| Entwurf & Vergleich («Vorher, nachher.»), Frühere Fassungen, Hinweis für Gäste, Sprachen | gleich |

Was das Original hat und hier fehlt: **Angaben des Hauses** (Telefon, E-Mail, Adresse, Links einmal für alle Seiten; hier geht es über «An allen N Stellen ändern»), **Google-Texte**, **Fotos hochladen**, **Anleitung**, die Probe des Hinweis-Bands, der Fortschritt beim Veröffentlichen.
Was hier dazukommt: der Modus-Knopf, die Listen des Hauses, die anderen Sprachen direkt im Formular mit Vorschlag bei Zahlen, die Sperre für Karten samt Weg zum Karten-Werkzeug, die Prüfseite nach dem Muster des Gasterntal.
Farben: das Original hat Grün für «Gespeichert» und Gold für «Veröffentlichen». Hier kommt alles aus `welt.css`: «Gespeichert» zeigt Wort und Haken, «Veröffentlichen» ist eine Taste im Metall der Welt (Gold oder Holz).

## Was steht

| Auftrag | Stand |
|---|---|
| Seite wählen, in der Vorschau auf Text oder Foto klicken, ändern, speichern | steht. Text mit einfacher Auszeichnung (kursiv, fett, Umbruch, Link), die Vorschau schreibt beim Tippen mit. Foto: tauschen gegen ein Foto, das auf der Website schon vorkommt, dazu die Bildbeschreibung |
| «Zeiten und Preise»: alle Zahlen an einer Stelle | steht. Gasterntal 61 Angaben, Beau-Rivage 228 (Kopie vom 12.10.2026), gelesen aus den Seiten. Dieselbe Angabe auf mehreren Seiten (Fuss) ist eine Zeile und wird überall zusammen geändert. Gleicher Wortlaut unter verschiedener Überschrift bleibt getrennt (Abend 18.00 – 21.30 in zwei Restaurants) |
| Sprachen | steht. Zu jeder Änderung die Felder aller Sprachen des Hauses, mit dem Text, der bisher auf der Seite dieser Sprache steht. Ohne Übersetzung steht dort der neue deutsche Text. Ändert sich im Deutschen nur eine Zahl, schlägt das Werkzeug die Übersetzung mit der neuen Zahl vor. Eine Übersetzung lässt sich auch allein ändern |
| Hotel-Bereiche, je Haus ein oder aus | steht. Gasterntal: Zimmer, Zimmerpreise, Packages, Unterlagen, Hinweis; Säle und Stellen aus. Beau-Rivage: Zimmer & Suiten, Säle, Pauschalen, Packages, Unterlagen, Stellen, Hinweis |
| Entwurf, Leiste unten, Vorher/nachher, Veröffentlichen, Verlauf, Zurückholen über den gemeinsamen Speicher | steht |
| Prüfseite mit Lexikon (Sehen, Grund, Tun) | steht. Läuft ohne `website.js`, ohne `website.css` und ohne Server-Teil. 34 Einträge, vier Reparaturen mit zwei Drücken |
| Karten-Abschnitte gesperrt, führen zu «karten» | steht. In der Vorschau gepunktet umrandet, rechts der Weg zu La Carte / Die Tafel; der Server lehnt jede Änderung dort ab |
| Draussen: Gestaltung, Abschnitte umbauen, Buchung | bleibt draussen. Ein Abschnitt oder Eintrag lässt sich ausblenden und wieder zeigen, mehr nicht |

## Aufbau

```
werkzeuge/website/
├── index.html · website.js · website.css   das Werkzeug, Aufbau wie das Le Bureau. Klassen mit Vorsatz ws-, jede Farbe/Schrift/Rundung aus /stamm/welt.css
├── pruefung.html · pruefung.js · pruefung.css   die Prüfseite, eigenständig (Vorsatz wsp-)
├── api.py          eigene Wege unter /api/x/website/… (Liste oben in der Datei). Kennt kein Haus
├── schicht.py      liest eine gebaute Seite, findet jede Stelle, legt die Änderungen darüber. Schreibt nichts
├── ausgabe.py      die EINZIGE Stelle, die Seiten schreibt (_probe/<haus>/online/). Hier käme später das echte Ziel hin
├── probe.py        legt die Kopie eines Hauses an (cp -c -R): grundlage/ (nie verändert) und online/
├── beschreibe.py   Hilfe beim Schreiben einer Beschreibung (Gerüst einer Seite, Treffer eines Selektors, --pruefe)
├── haeuser/<haus>.json   die Beschreibung je Haus: Seiten, Sprachen, Bereiche der Website (Name, Satz, Foto), Listen des Hauses mit Feldern, gesperrte Abschnitte, Zeichen und Tapete. Orte, Beschriftungen und Sätze des Werkzeugs; jeder Text der Website wird aus den Seiten gelesen
├── pruef.js        der feste Durchlauf (Port 8972, Wegwerf-Daten, Wegwerf-Kopie, unsichtbar)
├── PRUEFAUFTRAG.md Auftrag für einen unabhängigen Prüf-Chat
└── _probe/         Kopien der gebauten Seiten, nicht in Git
```

**Die Schicht** (liegt im Speicher, Werkzeug `website`, je Haus `live`, `entwurf`, `verlauf`):

```
{ "texte":  [{seite, h, n, neu, alt, sprachen:{en:…}, nur_sprachen?}],   h = Fingerabdruck aus Art und sichtbarem Text, n = das wievielte Mal auf der Seite
  "bilder": [{seite, b, n, neu, alt, alt_alt, alt_sprachen}],            b = Name der Bilddatei
  "links":  [{seite, h, n, neu, alt, t}],
  "aus":    [{seite, h, n, t}],                                           ausgeblendete Abschnitte
  "hinweis": {an, text, von, bis, link, linktext, sprachen} }
```

Ist die Schicht leer, gibt `schicht.anwenden()` jede Seite Byte für Byte zurück. Eine Stelle einer anderen Sprache findet ihr deutsches Gegenstück
über den Pfad im Aufbau der Seite (vom nächsten Element mit `id` aus), nie über den Text.
Die Bereiche (Zimmer, Säle …) und «Zeiten und Preise» sind Ansichten auf dieselbe Schicht, kein zweites Datenmodell: ein Feld ist eine Stelle auf einer Seite.

## Ein drittes Haus anschliessen

Nötig ist eine Beschreibung, kein Umbau:

1. `haeuser/<haus>/haus.json` im Stamm (Kennung, Name, Welt, Quelle). Gehört dem Stamm, also über Robert.
2. `werkzeuge/website/haeuser/<haus>.json` schreiben:
   - `seiten`: jede gebaute Seite (`datei`, bei Unterseiten `unter`). Die Namen liest das Werkzeug aus dem Menü der Website.
   - `sprachen`: je Sprache `code`, `ordner`, `name`. Leer bei einem Haus mit nur Deutsch.
   - `kopie.ordner`: was die Seiten brauchen (meist `assets`).
   - `kleid`: `zeichen` (Datei des Hauses; `zeichen_art` «bild» für ein farbiges Zeichen, «maske» für einen einfarbigen Schriftzug, der die Farbe der Welt annimmt), `tapete` und `tapete_breite`, falls das Haus eine hat.
   - `website`: die Bereiche der Website wie im Le Bureau, je `key`, `name`, `satz`, `seiten` (auch `zimmer-*`), `foto` (Name eines Fotos der Website). Fehlt der Abschnitt, ist jede Hauptseite ein Bereich: Name aus dem Menü, Satz aus den Überschriften, Foto das erste grosse der Seite.
   - `gesperrt`: Selektoren der Karten-Abschnitte mit `werkzeug: "karten"`.
   - `auslassen`: Selektoren für Stellen, die das Haus doppelt führt und die nie geändert werden sollen.
   - `vorschau.ohne_skripte`: Skripte der Seite, die in der Vorschau nichts verloren haben (Chat, Messung, Abrufe von Wetter und Preisen).
   - `bereiche`: je Bereich `quellen` mit `seite` (auch `zimmer-*`), `jedes` (Selektor eines Eintrags) und `felder` (`key`, `label`, `art`, `wo`).
     Ein Bereich, den das Haus nicht hat: `{"an": false}`.
   - bei Bedarf `bild_groessen` (Endung der Bildgrössen im Dateinamen) und `zahlen.muster`.
3. `python3 werkzeuge/website/beschreibe.py <haus> <seite>` zeigt das Gerüst einer Seite, mit einem Selektor dahinter die Treffer und ihre Stellen. So findet man `jedes` und `wo`.
4. `python3 werkzeuge/website/probe.py <haus>` und `python3 werkzeuge/website/beschreibe.py <haus> --pruefe`: jeder Bereich nennt seine Einträge und jedes Feld, das fehlt.
5. Prüfseite öffnen: alle Punkte müssen stehen (Byte für Byte, Zuordnung der Sprachen, Bereiche).

Voraussetzungen, die ein Haus erfüllen muss: fertig gebaute HTML-Seiten in einem Ordner, andere Sprachen in Unterordnern mit demselben Aufbau wie die deutsche Seite.
Was ein Feld sein kann: `text`, `lang`, `zahl` (eine oder mehrere Textstellen; ob es eine Zahl ist, erkennt das Werkzeug am Inhalt), `liste` (bis 60 Stellen), `bild`, `bilder`, `link`.
Die Selektoren können: tag, `#id`, `.klasse`, `[attr]`, `[attr="wert"]` (auch `^=` `$=` `*=` `~=`), `:nicht(…)`, Nachfahre, Kind (`>`), Komma.

## Was offen ist und wo die Grenzen liegen

- **Roberts Urteil zur Gestaltung** steht aus. Nicht in Safari geprüft, nur im Chrome-Kern (unsichtbar).
- **Nichts neu anlegen.** Ein Zimmer, ein Package, eine Stelle lässt sich ändern und ausblenden, nicht hinzufügen. Dafür braucht es den Bau des Hauses. Der Rahmen (Master, Abschnitt 7) verlangt ein geführtes «Neu anlegen»: fehlt.
- **Keine neuen Fotos.** Tauschen geht nur gegen Fotos der Website. Hochladen fehlt (kein Ort für Dateien im Speicher, keine Bildgrössen).
- **Eingebettete Daten bleiben stehen.** Was eine Seite aus einem Datenblock im Skript zeichnet (am Beau-Rivage Zimmer-Finder und Saal-Regler), erreicht das Werkzeug nicht. Wer dort «312 m²» im Text ändert, ändert den Regler nicht mit.
- **Nicht änderbar:** Überschriften, die aus einzelnen Buchstaben gebaut sind (Auftakt am Beau-Rivage), Texte in Fenstern der Seite (`dialog`), Platzhalter in Formularen, Google-Texte (Titel, Beschreibung).
- **Feldarten `wahl`, `mehrfach`, `fest`** aus der Carlton-Vorlage gibt es nicht als eigene Arten. «Zeigen oder ausblenden» ist bei jedem Eintrag ein Knopf, «fest» ist die Sperre über `gesperrt`. Für `mehrfach` gibt es auf einer gebauten Seite keine Stelle.
- **Arabisch:** 8792 von 9142 deutschen Stellen haben ein Gegenstück, weil die Seite dort anders aufgebaut ist. Wo keines da ist, ändert das Werkzeug in dieser Sprache nichts und sagt das im Feld. Englisch, Französisch, Chinesisch 9138, Koreanisch 9124.
- **Der Hinweis für Gäste** nimmt Schrift und Farbe von der Seite. Je Haus gestaltet ist er nicht.
- **«Rückgängig»** gilt für das letzte Speichern, solange die Quittung steht (im Original bleibt jeder Schritt auf dem Server liegen). Danach: einzelne Änderung «Zurücknehmen» oder ein Stand aus dem Verlauf.
- **Speichern-Knopf:** der Rahmen und das Original nennen grau, gelb, grün. `welt.css` kennt dafür keine Farben. Gebaut, in der Leiste unten: hell (nichts offen), mit Rand im Metall der Welt und «N Eingaben noch nicht gespeichert» (offen), «Gespeichert» mit Haken (sechs Sekunden nach dem Speichern). Robert entscheidet, ob das reicht.
- **Fotos** öffnen ein Fenster mit eigenem «Speichern» (wie im Original); alles andere wartet in der Leiste.
- **Auf dem Handy** steht die Seite oben und die Liste der Stellen darunter; «Vorher, nachher» liegt dort im Rand unter «Entwurf & Vergleich», nicht in der Leiste.
- **Online heisst hier: die Kopie.** Veröffentlichen schreibt nach `_probe/<haus>/online/`. Der Weg zur echten Website des Hauses ist nicht gebaut (siehe Deployment).
- **Die Vorschau führt die Skripte der Seite aus,** im selben Ursprung wie das Werkzeug. Lokal ohne Folgen, für draussen braucht die Vorschau eine eigene Adresse.
- **Veröffentlichen sind zwei Schritte** (Stand im Speicher, dann Seiten schreiben), keine Einheit. Scheitert der zweite, meldet es das Werkzeug, die Prüfung zeigt die Abweichung, «Seiten neu ausgeben» behebt sie.

## Prüfen

- `node werkzeuge/website/pruef.js` (im Ordner `_Werkzeuge`): eigener Server auf 8972 mit Wegwerf-Daten und Wegwerf-Kopie frisch aus den Quellen, unsichtbar, beendet nur den eigenen Server per PID.
  Ausschnitt: `node werkzeuge/website/pruef.js gasterntal land 1440`. Mit `LAUT=1` steht jede einzelne Prüfung da.
- Letzter voller Lauf (12.10.2026, nachts, nach dem Umbau auf den Aufbau des Le Bureau): **BESTANDEN · 1459 Prüfungen** · Häuser gasterntal, beau-rivage · Welten land, grand · Breiten 1440, 390, 320. Rund sechs Minuten.
- Was der Lauf zulässt und warum: genau eine Zeile in der Konsole je Ablauf, «409 (Conflict)». Der Browser schreibt jede 4xx-Antwort in die Konsole, die 409 ist die erwartete Antwort des Speichers beim Konflikt.
- An den Quellen arbeiten andere Chats. Wird eine Seite zwischen Kopieren und Vergleich neu gebaut, zieht der Lauf sie einmal nach und sagt das in der Ausgabe.
- `python3 unterbau/pruefe.py` nach dem Bau: BESTANDEN · 21 Prüfungen. In `stamm/` und `unterbau/` ist nichts geändert.

## Prüfpunkte (Liste aus `_Werkzeuge/STAND.md`)

| Prüfpunkt | Stand | Beleg, Lücke |
|---|---|---|
| Backend | **offen** | Läuft nur mit `unterbau/serve.py` auf diesem Rechner. Stürzt er ab, startet ihn niemand neu. Verloren geht dabei nichts: das Werkzeug hält keinen Stand im Prozess, nur einen Zwischenspeicher der gelesenen Seiten |
| Datenbank | **erfüllt im Rahmen des Stamms, sonst offen** | Eine Schicht je Haus im Speicher, eine Regel je geänderter Stelle mit altem und neuem Wortlaut (eine Zeit im Fuss von 31 Seiten = 31 Regeln). Höchstens 400 Änderungen je Speichern, 6000 Zeichen je Text. Zwei Schreiber: 409 statt Überschreiben, im Lauf geprüft (Server und Browser). Offen: keine Datenbank, keine Grenze für Verlauf und Protokoll |
| Authentication und Rollen | **offen** | Keine Anmeldung. `wer` ist ein Name, den man im Verlauf frei einträgt |
| Rechteverwaltung | **offen** | fehlt |
| API-Sicherheit | **teils** | Geprüft wird jede Eingabe: Seite und Sprache müssen in der Beschreibung stehen, die Stelle muss es geben, gesperrte Stellen 423, Text wird gesäubert (im Lauf: Skript, Ereignis-Attribut, `javascript:`-Link kommen nicht durch), Links und Daten haben eine feste Form, `ausgabe.py` schreibt nur in den Ordner `online`. Offen: kein Schutz nach aussen, kein Schutz gegen fremde Seiten, die im Namen eines angemeldeten Menschen schreiben, die Vorschau führt Skripte der Seite im Ursprung des Werkzeugs aus, `_probe/` wird als Datei ausgeliefert |
| Rate Limits | **offen** | fehlt |
| Logging | **erfüllt lokal** | Wer wann gespeichert, veröffentlicht, zurückgeholt, verworfen hat: Protokoll des Speichers, sichtbar unter «Verlauf». Fehler: Ausgabe des Servers, dazu merkt sich das Werkzeug seine Fehler im Browser und die Prüfseite liest sie. Offen: die Ausgabe des Servers wird nirgends aufbewahrt |
| Backups | **teils** | Jeder veröffentlichte Stand liegt im Verlauf und lässt sich zurückholen (im Lauf: danach jede Datei wieder Byte für Byte wie gebaut). Die Grundlage wird nie verändert (im Lauf per Prüfsumme). Offen: keine Kopie ausserhalb des Rechners, Zwischenstände des Entwurfs werden nicht aufbewahrt |
| Deployment | **für die Kopie erfüllt, für die echte Website offen** | Veröffentlichen prüft zuerst, ob jede Änderung ihre Stelle findet (sonst 422, nichts wird veröffentlicht), wechselt dann den Stand im Speicher und schreibt nur die Dateien, die sich ändern, jede erst in eine Nebendatei. Zurück: Zurückholen und Veröffentlichen. Die Prüfung vergleicht jede Datei online mit Grundlage + Stand, «Seiten neu ausgeben» stellt sie her (im Lauf: verstellte Seite erkannt und behoben). Offen: das Hochladen zum Haus (käme in `ausgabe.py`), Veröffentlichen als eine Einheit, und der Fall «das Haus baut seine Website neu»: `probe.py --neu` holt die neuen Seiten, die Prüfung nennt Änderungen ohne Platz, einen selbsttätigen Abgleich gibt es nicht |
| CMS-Datenmodell | **erfüllt, mit den Grenzen oben** | Zwei Häuser mit verschiedenem Aufbau, 0 und 5 weiteren Sprachen, verschiedenen Bereichen laufen aus demselben Code. Im Code des Werkzeugs steht kein Haus (im Lauf durchsucht). Ein drittes Haus ist eine Beschreibung (Abschnitt oben). Grenzen: nur fertig gebaute HTML-Seiten; ein Feld ist eine Stelle im HTML; keine neuen Einträge; eingebettete Daten bleiben aussen vor; die Sprachseiten müssen wie die deutsche aufgebaut sein. Nicht belegt: ein drittes Haus wurde nicht angeschlossen |
| Übersetzungsworkflow | **erfüllt für Text, Hinweis, Bildbeschreibung** | Ändert sich das Deutsche: jede Sprache bekommt ein Feld mit dem bisherigen Text. Ohne Übersetzung steht dort der neue deutsche Text, damit keine alte Zeit stehen bleibt (im Lauf an Französisch geprüft), mit Übersetzung diese (Englisch). Nur die Zahl geändert: Vorschlag mit der neuen Zahl, sichtbar im Feld, mit gespeichert (im Lauf geprüft). Wer merkt, dass etwas fehlt: die Leiste unten zählt es, das Fenster vor dem Veröffentlichen sagt es und bietet «Erst übersetzen», die Ansicht «Sprachen» listet es, die Prüfseite nennt es. Nur eine Übersetzung ändern: das Deutsche und die anderen Sprachen bleiben Zeichen für Zeichen (im Lauf geprüft). Offen: keine Übersetzung durch eine Maschine, niemand wird benachrichtigt, Stellen ohne Gegenstück (Arabisch) bleiben unverändert, Links und ausgeblendete Abschnitte gelten in jeder Sprache gleich |
| KI-Kosten | **betrifft dieses Werkzeug nicht** | Es ruft keine KI. Der Vorschlag für Übersetzungen tauscht nur Zahlen |
| Prompt-Injection-Schutz | **betrifft dieses Werkzeug nicht** | Keine KI. Verwandt: was ein Mensch eingibt, wird gesäubert (siehe API-Sicherheit) |
| DSGVO und Schweizer Datenschutz | **offen, kleiner Umfang** | Daten von Gästen entstehen hier nicht. Es entstehen: der frei eingetragene Name im Protokoll und im Browser (`ws-wer`), die gewählte Welt und die Fehlerliste im Browser. Zu regeln, sobald es eine Anmeldung gibt |
| Datenlöschung | **offen** | Verlauf und Protokoll wachsen ohne Grenze. Löschen lässt sich nur der Entwurf. Der Speicher bietet keinen Weg, einen Stand oder einen Namen zu entfernen |
| Verfügbarkeit | **teils** | Die Website des Hauses hängt nicht am Werkzeug: steht es, bleiben die Seiten, wie sie sind. Steht der Server: das Werkzeug sagt «antwortet nicht» und führt zur Prüfung. Startet das Werkzeug nicht: Meldung mit Tür zur Prüfung (im Lauf geprüft). Offen: alles jenseits dieses Rechners |
| Monitoring | **offen** | Die Prüfseite prüft nur, wenn jemand sie öffnet |
| Booking-Integration | **betrifft dieses Werkzeug nicht** | Buchung bleibt beim Buchungssystem des Hauses. In der Vorschau sind die Abrufe der Seite (Preise, Wetter, Chat) über die Beschreibung abgeschaltet |

Beim Bauen aufgefallen, gehört als Punkt in die Liste des Stamms: **Quelle in Bewegung.** An den Websites der Häuser wird weiter gebaut. Jedes Werkzeug, das auf gebauten Seiten arbeitet, braucht eine Antwort darauf, was mit gespeicherten Änderungen geschieht, wenn die Seite darunter neu gebaut wird.

## Wünsche an den Stamm

1. **Ziel für gebaute Seiten.** Der Speicher kennt nur Daten. Das Werkzeug schreibt die veröffentlichten Seiten deshalb selbst, an einer einzigen Stelle (`ausgabe.py`). Wunsch: ein Weg im Unterbau, der Dateien eines Hauses entgegennimmt.
2. **Eigene Wege können nur JSON antworten und sehen keine Parameter hinter dem Fragezeichen.** Die Vorschau kommt deshalb als JSON und wird als `srcdoc` in den Rahmen gesetzt. Wunsch: eigene Wege dürfen HTML antworten.
3. **Ablage für hochgeladene Dateien** (Fotos, PDFs). Fehlt, deshalb gibt es kein Hochladen.
4. **Speicher:** `veroeffentlichen`, `zurueckholen` und `entwurf_verwerfen` nehmen keine erwartete Kennung. Das Werkzeug fragt vor dem Zurückholen nach und prüft vor dem Veröffentlichen selbst, aber nicht in derselben Sperre. Dazu: Zwischenstände des Entwurfs für ein dauerhaftes «Rückgängig».
5. **Bausteine, die hier mit eigenem Vorsatz gebaut sind und in `welt.css` gehören könnten:** kleine Taste ohne Knauf (`ws-taste`), Auswahl im Stil des Hauses (`ws-auswahl`), Fenster (`ws-fenster`), Zeile als Taste (`ws-zeile`), Zeichen «fehlt» als Rahmen (`ws-fehlt`), Text-Feld zum Hineinschreiben (`ws-text`).
6. **Sprachen des Hauses in `haus.json`.** Stehen jetzt in der Beschreibung des Werkzeugs, andere Werkzeuge brauchen sie auch.
7. **Entscheid zum Speichern-Knopf:** Rahmen sagt grau, gelb, grün, das Artbook kennt dafür keine Farben.
8. **Kleid des Hauses an einer Stelle** (19.10.2026, Schlössli): `_Werkzeuge/haeuser/<haus>/kleid.css` setzt die Werte von `welt.css` in der Welt des Hauses. `website.js` lädt es über `kleid.stil` aus `api.py`; andere Werkzeuge könnten es genauso laden. Wunsch: `welt.js` lädt es selbst, sobald ein Haus eins hat.
9. **Stand-Weg für La Maison im Unterbau** (19.10.2026): `ueberblick` liegt jetzt als eigener Weg `/api/x/website/ueberblick/<haus>`; die anderen Werkzeuge des Stamms haben keinen.

## Verlauf

- **12.10.2026, abends** · Erster Bau. Vorlagen gelesen (Grand Beau-Rivage `studio_inhalt.py` als Bauart der Schicht, Carlton `I.liste`, Gasterntal Prüfseite). Beim Prüfen gefunden und behoben: Einträge eines langen Bereichs wurden auf null Höhe zusammengedrückt; auf dem Handy lag die Quittung hinter dem Blatt mit dem Formular; eine langsam ladende Ansicht überschrieb die nächste; die Vorschau lud Dateien zuerst von der Adresse des Werkzeugs; dieselbe Zeit in zwei Restaurants wurde als eine Angabe geführt; die Auswahl der Seite ging zu, wenn die Vorschau fertig lud.
- **12.10.2026, spät** · Schlusslauf `pruef.js` bestanden (1337 Prüfungen, drei volle Läufe hintereinander ohne Ausfall: 1248, 1265, 1337, dazwischen Prüfungen ergänzt). Kopien beider Häuser frisch aus den Quellen geholt (`probe.py --neu`). Unter der echten Adresse (Port 8970, der Server lief schon aus einem anderen Chat) beide Häuser unsichtbar geöffnet: keine Fehler, Prüfseite 11 von 11 (Gasterntal) und 16 von 16 Punkten (Beau-Rivage). In den echten Daten liegt je Haus der erste Stand: leer, also die Website, wie sie gebaut ist. Die Wünsche stehen auch in `_Werkzeuge/STAND.md` unter «Wünsche an den Stamm» (dort nicht committet, wie bei den anderen Werkzeugen).
- **12.10.2026, nachts** · Auf Roberts Wort («Wir haben das schon gemacht») aus dem bestehenden Le Bureau des Grand Beau-Rivage abgeleitet: Übersicht mit Gruss, Lage und Kacheln, die Website Bereich für Bereich mit Stellen links und Seite rechts, Zeiten & Preise als Karten je Seite, Leiste unten mit Speichern · Vorher, nachher · Veröffentlichen, Quittung darüber, Entwurf & Vergleich in einer Ansicht, Frühere Fassungen. Eingaben warten jetzt wie im Original, bis gespeichert wird, auch über den Wechsel der Ansicht hinweg. Dasselbe für das Berghotel im Landhaus (Schriftzug des Hauses im Kopf, Bereiche aus den Seiten). `index.html`, `website.css`, `website.js` neu geschrieben, `api.py` um die Bereiche der Website und das Kleid des Hauses ergänzt, `pruef.js` auf den neuen Aufbau umgestellt. Voller Lauf: 1459 Prüfungen bestanden. `unterbau/pruefe.py` BESTANDEN. Unter der echten Adresse (8970) beide Häuser unsichtbar geöffnet, keine Fehler. Roberts Urteil steht aus.
- **19.10.2026, abends** · Drittes Haus: **Wirtschaft am Schlössli**, Bottighofen (Restaurant, nur Deutsch, Welt «land», Station 11 der Kette). Beschreibung `haeuser/schloessli.json` (11 Seiten, sieben Bereiche der Website, Bereiche des Hauses Anlässe und Team mit freiem Schlüssel, Karten-Stellen gesperrt), ohne Umbau des Werkzeugs. Neu für jedes Haus: `kopie.unter` (Quelle = Projektordner), Kleid des Hauses als Stilblätter (`kleid.stil`, `data-haus`, gezeichnet erst nach dem Laden), Startbild mit Aussenfoto (`kleid.foto`), Stand-Weg `ueberblick`, Beispiele statt Leere in «Entwurf & Vergleich» und «Frühere Fassungen», `nachbau.py`, `fluss.js`, `pruef.js` mit `PRUEF_PORT`, `MOTOR=webkit`, `PLAYWRIGHT_PFAD`. Behoben: ein Bereich mit nur einer Seite schrieb «null» unter den Titel. Läufe: schloessli Chromium 1440/390/320 und Safari-Kern 1440/390 bestanden, gasterntal 1440 als Gegenprobe (Zahlen im Paket des Schlössli, `_kette/11-werkbank/werkzeuge/website/STAND.md`).
