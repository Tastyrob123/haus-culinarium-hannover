# Werkzeuge · Stamm (angelegt 12.10.2026)

Zuerst lesen, bevor hier etwas gebaut wird. Neueste Einträge unten unter «Verlauf».

## Worum es geht

Die sechs Werkzeuge, die bisher je Haus als eigene Kopie entstanden sind (zuletzt am Grand Beau-Rivage),
werden hier **einmal** gebaut. Ein Haus ist danach nur noch Inhalt und Kleid.
Robert-Entscheid 12.10.2026: sechs Prototypen «in Perfektion», jedes neue Haus bekommt sie als fertiges Gerüst.

| Schlüssel | Was es tut | Grandhotel | Landhaus | Ordner |
|---|---|---|---|---|
| `zentrale` | Zentrale | La Maison | Die Stube | `werkzeuge/zentrale/` (kommt zuletzt) |
| `website` | Website pflegen | Le Bureau | Der Schreibtisch | `werkzeuge/website/` |
| `karten` | Karten und Preislisten | La Carte | Die Tafel | `werkzeuge/karten/` |
| `druck` | Drucksachen und Beiträge | L’Imprimerie | Die Werkstatt | `werkzeuge/druck/` (wenn alles andere steht) |
| `gaeste` | Gästen antworten | La Réception | Der Gastgeber | `werkzeuge/gaeste/` |
| `marke` | Marke und Bilder | Le Livre | Das Hausbuch | `werkzeuge/marke/` |

Zwei Welten, ein Bau: **Grandhotel** (gelesen aus dem Grand Beau-Rivage) und **Landhaus** (gelesen aus dem
Berghotel Gasterntal, Farbwelt «Tal: Fels, Kander, Tanne»). Jedes Werkzeug wechselt die Welt mit einem Knopf.
Das Artbook dazu: https://claude.ai/artifact/WoLQHpw5cb2vVYVSMWbLZD (gleiche Werte wie `stamm/welt.css`).

## Aufbau

```
_Werkzeuge/
├── STAND.md              diese Datei
├── stamm/                gehört allen: nur nach Absprache ändern (siehe «Wem was gehört»)
│   ├── welt.css          beide Welten: Farben, Schrift, Rundung, Platte/Kuhle, Knöpfe, Feld, Liste, Leiste
│   ├── welt.js           setzt und wechselt die Welt, kennt die Namen (Welt.name('karten'))
│   ├── schriften/        alle Schriften als Dateien, nichts lädt von aussen
│   └── muster.html       jeder Baustein in beiden Welten, zum Nachsehen
├── unterbau/             gehört allen: nur nach Absprache ändern
│   ├── speicher.py       die EINZIGE Stelle, die Daten liest und schreibt
│   ├── serve.py          ein Server für alle Werkzeuge, Port 8970
│   └── pruefe.py         Probelauf des Speichers (21 Prüfungen)
├── werkzeuge/<schlüssel>/  je Werkzeug ein Ordner, gehört dem Chat, der es baut
├── haeuser/<haus>/haus.json  Kennung, Name, Welt, Quelle (nur lesen)
├── daten/                schreibt nur der Speicher, nie von Hand, nicht in Git
└── _qa/aufnahme.js       unsichtbare Aufnahme einer Adresse in beiden Welten
```

## Wem was gehört (damit kein Chat einem anderen etwas kaputt macht)

1. **Ein Chat, ein Ordner.** Wer `website` baut, schreibt nur in `werkzeuge/website/`. Dasselbe für `karten` und `gaeste`.
2. **`stamm/` und `unterbau/` ändert kein Werkzeug-Chat still.** Fehlt dort etwas (ein Baustein, ein Weg im Speicher),
   wird es zuerst im eigenen Ordner gelöst und unten unter «Wünsche an den Stamm» eingetragen. Robert entscheidet, was hochwandert.
3. **Die Quellen der Häuser werden nur gelesen.** Nie in `~/Desktop/Website-Projekte/Grand Beau-Rivage/` oder
   `…/Berghotel Gasterntal/` schreiben. Dort arbeiten andere Chats, am Grand Beau-Rivage läuft ein Angebot.
   Was ein Werkzeug vom Haus braucht, liest es ein und legt es über den Speicher ab.
4. **Eigene Klassen mit Vorsatz:** `ws-` (website), `kt-` (karten), `ga-` (gaeste). Kurze Namen ohne Vorsatz haben am
   Grand Beau-Rivage schon einmal ein anderes Werkzeug zerschossen (`.zw`).
5. **Git:** jeder Chat committet nur seinen Ordner (`git add werkzeuge/<schlüssel> && git commit`). Vor jeder grösseren
   Änderung ein Commit, damit jeder Schritt zurückgenommen werden kann. Kein `git add -A`, kein Force.

## Speicher (Vertrag, bleibt gleich, wenn später die echte Ablage dahinter kommt)

Jedes Werkzeug hat je Haus: `live` (veröffentlicht), `entwurf` (gespeichert, noch nicht online), `verlauf` (frühere Fassungen).

| Weg | Tut |
|---|---|
| `GET /api/stand/<haus>/<werkzeug>` | `live`, `entwurf`, `kennung_live`, `kennung_entwurf`, `offen` |
| `PUT /api/entwurf/<haus>/<werkzeug>` `{daten, erwartet, wer}` | speichert als Entwurf. `erwartet` = zuletzt gelesene Kennung (Entwurf, sonst Live). Stimmt sie nicht: 409 Konflikt, nichts wird überschrieben |
| `DELETE /api/entwurf/<haus>/<werkzeug>` | Entwurf verwerfen |
| `POST /api/veroeffentlichen/<haus>/<werkzeug>` `{wer, notiz}` | Entwurf wird live, der vorige Stand kommt in den Verlauf |
| `GET /api/verlauf/<haus>/<werkzeug>` · `GET /api/fassung/<haus>/<werkzeug>/<fassung>` | frühere Fassungen |
| `POST /api/zurueckholen/<haus>/<werkzeug>` `{fassung, wer}` | alte Fassung wird **Entwurf**, online erst mit Veröffentlichen |
| `GET /api/protokoll/<haus>/<werkzeug>` | wer hat wann was getan |
| `GET /api/haus/<haus>` | `haus.json` |
| `/api/x/<werkzeug>/<rest>` | eigene Wege: `werkzeuge/<werkzeug>/api.py` mit `bearbeite(methode, rest, daten, speicher)` → `(status, antwort)` |

Fehler: `{"fehler": "…", "stichwort": "…"}`. Der erste Stand eines Werkzeugs kommt mit `speicher.grundstand_setzen(haus, werkzeug, daten, wer)`.
Der Speicher liest nie still leer: beschädigte Datei → Sicherung (Stand vor der letzten Änderung, steht dann als `aus-sicherung`
im Protokoll), keine Sicherung → Abbruch mit `beschaedigt`.

## Starten und prüfen

- Server: `python3 unterbau/serve.py` (Port 8970). Vorher `curl -s http://127.0.0.1:8970/api/haus/gasterntal` — antwortet er, läuft er
  schon in einem anderen Chat: mitbenutzen, **nie beenden**. Er lädt `api.py` bei jedem Aufruf frisch, ein Neustart ist nur nach
  Änderungen in `unterbau/` nötig.
- Speicher: `python3 unterbau/pruefe.py` muss `BESTANDEN` zeigen.
- Eigene Prüfläufe eines Werkzeugs laufen auf **eigenem Port mit Wegwerf-Daten**, nie gegen die echten:
  `WERKZEUGE_DATEN=/tmp/… python3 unterbau/serve.py 8972` (website 8972, karten 8973, gaeste 8974), danach den eigenen Prozess per PID beenden.
- Ansehen: `node _qa/aufnahme.js <adresse> <name>` legt Bilder beider Welten (Rechner und Handy) nach `_qa/aufnahmen/`.
  Immer unsichtbar, nie ein Fenster auf Roberts Bildschirm, nie `pkill` auf Chrome.

## Gestaltung (Kurzfassung, das Artbook ist die lange)

- Alles Sichtbare kommt aus `stamm/welt.css`. Kein Werkzeug setzt eine eigene Farbe, Schrift oder Rundung.
- Hell ist der Normalzustand. Metall (Gold, Holz) zeichnet und schreibt nie Lesetext. Das Rot gibt es einmal: die Marke «Entwurf».
- Platte = anfassen, Kuhle = etwas gehört hinein. Aufbau wie eine Profi-Software, im Stil des Hauses.
- Nie: Punkt in Tasten oder Auswahlkarten · Aufhellen bei Maus · Auswahl, Kalender, Uhrzeit des Betriebssystems ·
  Etikett mit Farbpunkt über einer Überschrift · graues Kachel-Raster · Vorhang beim Laden · stilles Speichern ·
  erfundene Namen, Zeiten, Preise (Kundendaten werden gelesen und gegen das Original geprüft).
- Jede Ansicht hat unten die Entwurfs-Leiste und nach jedem Speichern eine sichtbare Quittung mit «Vorher, nachher» und «Rückgängig».

**Im Landhaus neu gesetzt (nicht aus dem Projekt gelesen, Roberts Urteil offen):** Platte und Kuhle (gebaut wie im Grandhotel aus den
Tönen der Gasterntal-Knöpfe) · Kapitelzeile in DM Mono · zweite Titelzeile in Tanne · Rot als Marke «Entwurf» in beiden Welten.

## Noch nicht da (bewusst, kommt mit dem echten Unterbau)

Anmeldung · Rollen und Rechte · Ablage ausserhalb dieses Rechners · tägliche Sicherung · Überwachung · Begrenzung von Anfragen.
Die Werkzeuge werden so gebaut, dass diese Dinge später in `unterbau/` einziehen, ohne dass ein Werkzeug umgebaut wird:
kein Werkzeug schreibt selbst Dateien, keines kennt Pfade des Speichers, jede Änderung nennt `wer`.

## Prüfpunkte für jedes Werkzeug (Robert 12.10.2026, allgemein wichtig)

Jeder Chat, der ein Werkzeug baut, und jeder Prüfauftrag danach geht diese Liste Punkt für Punkt durch und schreibt je Punkt in die
`STAND.md` des Werkzeugs: **erfüllt** (mit Beleg), **offen** (was fehlt) oder **betrifft dieses Werkzeug nicht** (warum).
Kein Punkt wird übersprungen, keiner ohne Beleg als erfüllt gemeldet. Die Liste ist nicht abgeschlossen: fällt beim Bauen ein weiterer Punkt auf, kommt er hier dazu.

| Prüfpunkt | Die Frage dahinter | Stand im Stamm am 12.10.2026 |
|---|---|---|
| Backend | Läuft das Werkzeug, ohne dass Robert da ist? Was passiert bei einem Absturz? | nur lokal: `unterbau/serve.py` auf diesem Rechner |
| Datenbank | Wo liegen die Daten, wie gross dürfen sie werden, was passiert bei zwei gleichzeitigen Schreibern? | Dateien über `speicher.py`, Sperre je Werkzeug, Konflikt statt Überschreiben. Keine Datenbank |
| Authentication und Rollen | Wer darf hinein, wer darf was? | fehlt. Jede Änderung nennt schon `wer` |
| Rechteverwaltung | Kann das Haus selbst Zugänge anlegen, sperren, entziehen? | fehlt |
| API-Sicherheit | Kommt jemand von aussen an Daten oder Dateien, die er nicht sehen darf? Wird jede Eingabe geprüft? | Server hört nur auf 127.0.0.1, gesperrte Ordner und Pfade geprüft. Für aussen nicht gebaut |
| Rate Limits | Kann jemand das Werkzeug oder die KI mit Anfragen überfluten? | fehlt |
| Logging | Steht fest, wer wann was geändert hat? Stehen Fehler irgendwo? | Protokoll je Werkzeug, Fehler in der Ausgabe des Servers |
| Backups | Lässt sich jeder Stand zurückholen? Gibt es eine Kopie ausserhalb des Rechners? | Sicherung der letzten Fassung und Verlauf. Keine Kopie ausserhalb |
| Deployment | Wie kommt eine Änderung online, ohne dass etwas anderes kaputtgeht? Wie geht es zurück? | keines. Git je Schritt, nichts wird hochgeladen |
| CMS-Datenmodell | Passt ein drittes Haus hinein, ohne dass das Werkzeug umgebaut wird? | je Werkzeug zu belegen |
| Übersetzungsworkflow | Was passiert mit den anderen Sprachen, wenn sich das Deutsche ändert? Wer merkt, dass eine Übersetzung fehlt? | je Werkzeug zu belegen |
| KI-Kosten | Was kostet eine Anfrage, was ein Monat? Gibt es eine Obergrenze? Was passiert bei leerem Guthaben? | je Werkzeug zu belegen. Guthaben war am 10.10. und 12.10. leer |
| Prompt-Injection-Schutz | Kann ein Gast oder ein eingelesener Text die KI dazu bringen, Regeln zu brechen oder Internes preiszugeben? | je Werkzeug zu belegen |
| DSGVO und Schweizer Datenschutz | Welche Daten von Gästen entstehen, wo liegen sie, wer sieht sie, was steht in der Datenschutzerklärung? | offen |
| Datenlöschung | Wann wird was gelöscht, und kann das Haus eine Löschung auf Wunsch eines Gastes ausführen? | fehlt. Am Carlton werden Fragen nach 12 Monaten gelöscht |
| Verfügbarkeit | Was sieht der Gast und was das Team, wenn ein Teil ausfällt? | lokal, nicht gebaut |
| Monitoring | Merkt jemand, dass etwas steht, bevor das Haus anruft? | fehlt |
| Booking-Integration | Was braucht das Werkzeug vom Buchungssystem, und was, wenn es nicht antwortet? | bleibt beim Buchungssystem des Hauses. SimpleBooking weist Vercel-Server zeitweise ab |

## Wünsche an den Stamm

(Hier eintragen: Datum · Werkzeug · was fehlt · wie es vorläufig im eigenen Ordner gelöst ist.)

- **12.10.2026 · gaeste · Ablage für Betriebsdaten** (Anfragen, Fragen, Zähler): Dinge, die sofort gelten, nie veröffentlicht werden, einzeln gelöscht werden müssen und eine Aufbewahrungsfrist haben. Vorläufig: eigenes Fach `gaeste-betrieb`, nur im Entwurf, mit Kennung und Wiederholen (`werkzeuge/gaeste/api.py`, `_aendere`). Schwäche: ein einziges Dokument, die allgemeinen Wege können es ungeprüft überschreiben oder löschen, sein Protokoll wächst je Frage.
- **12.10.2026 · gaeste · Absender einer Anfrage:** `bearbeite(methode, rest, daten, speicher)` bekommt weder Adresse noch Kopfzeilen. Eine Grenze je Besucher lässt sich so nur an eine Kennung hängen, die der Browser selbst wählt.
- **12.10.2026 · gaeste · `veroeffentlichen` und `zurueckholen` ohne `erwartet`:** Wer veröffentlicht, kann eine Änderung mitnehmen, die er nicht gesehen hat; Zurückholen ersetzt einen fremden Entwurf. Vorläufig: Die Oberfläche liest den Stand unmittelbar davor neu und fragt nach.
- **12.10.2026 · gaeste · Entwurf verwerfen ohne `erwartet`** (gleiche Lücke, gebraucht für «Rückgängig»).
- **12.10.2026 · gaeste · Prüfung des Stands vor dem Speichern** je Werkzeug auch auf den allgemeinen Wegen (`PUT /api/entwurf`). Vorläufig: eigener Weg `speichern` mit Prüfung; der allgemeine Weg bleibt offen.
- **12.10.2026 · gaeste · Bausteine in `welt.css`:** Rand mit Bereichen (schmal aufklappbar) · Band unter dem Kopf · Fenster · Quittung mit Schliessen · Sprechblase · Balken · Vorher/nachher mit Markierung · Schild ohne Farbe · Textknopf · Zeilen für lange Angaben · `.liste` mit Umbruch langer Wörter (läuft bei 320 Breite sonst über) · Knöpfe bei 320 Breite (lange Beschriftungen passen nicht). Vorläufig alle als `ga-…` in `werkzeuge/gaeste/gaeste.css`.
- **12.10.2026 · gaeste · `_qa/aufnahme.js`** nimmt nur eine Adresse auf, ohne Klicks. Vorläufig: eigener Durchlauf `werkzeuge/gaeste/pruef.js`.
- **12.10.2026 · gaeste · `speicher.lesen` liest ohne Sperre:** Zwischen den zwei Umbenennungen eines Schreibens fehlt die Datei einen Augenblick; ein Leser bekommt dann «fehlt, Sicherung liegt vor» und der Server antwortet mit 500 (im Prüflauf einmal in zwölf Läufen). Vorläufig: eigene Wege `stand`, `veroeffentlichen`, `zurueckholen`, `verwerfen` in `werkzeuge/gaeste/api.py`, die mit einem Schloss im Server lesen und es bei diesem Fehler noch einmal versuchen. Die allgemeinen Wege haben die Lücke weiter.
- **12.10.2026 · gaeste · Bühne und Kleid für alle Werkzeuge** (Robert am Abend: atmosphärischer, hochwertiger bewegt, Luxus im Grandhotel, Wald im Landhaus, 3D): dunkle Bühne je Welt, Kulisse mit Foto des Hauses, Inseln, Kacheln mit Tiefe, Auftritte, dazu je Haus ein Ordner mit Kulisse, Kacheln, Tapete, Zeichen. Vorläufig nur im Werkzeug gaeste: `werkzeuge/gaeste/gaeste.css` (Abschnitte Kulisse, Kopf, Bänder, Übersicht, Auftritt), `kleid.py`, `kleid/<haus>/`. Die helle Regel des Artbooks («Hell ist der Normalzustand») gilt dort nur noch für die Inseln, nicht für den Grund.
- **12.10.2026 · karten · Ablage für Dateien:** Der Speicher kennt nur Daten. Die gedruckte PDF jeder Karte liegt deshalb als base64 in einem eigenen Fach `karten-pdf-<karte>` (Kennung der Daten, Seiten, PDF). Schwäche: jeder neue Druck legt die vorige PDF in den Verlauf, 100 bis 500 kB je Karte, ohne Obergrenze.
- **12.10.2026 · karten · Eigene Wege antworten nur mit JSON:** `/api/x/…` kann keine Datei ausliefern. Vorläufig: PDF als base64 in der Antwort, der Browser baut daraus die Datei.
- **12.10.2026 · karten · Prüfung vor dem Umschalten auch auf den allgemeinen Wegen** (deckt sich mit dem Wunsch von gaeste): `PUT /api/entwurf` nimmt Daten in jeder Form an, `POST /api/veroeffentlichen` schaltet um, ohne dass die PDF gedruckt und gegen die Daten geprüft ist. Vorläufig: eigene Wege `entwurf` und `veroeffentlichen` in `werkzeuge/karten/api.py`; wer am Werkzeug vorbei veröffentlicht, bekommt beim nächsten Abruf der PDF einen Nachdruck mit Prüfung (`nachgedruckt: true`).
- **12.10.2026 · karten · Bausteine in `welt.css`:** Fenster · Auswahlliste im Stil des Hauses · kleine runde Taste · Textknopf · Vorher/nachher mit Markierung · gewählte Taste auf Dunkel (Rahmen in Tinte ist dort nicht zu sehen, bei karten in Metall) · Ziffern auf der Linie für Titel und Preise (die Antiqua des Grandhotels setzt «1» sonst wie ein kleines «I») · kursiver Schnitt der Leseschrift fehlt (englische Zeilen der Karte stehen deshalb heller statt kursiv). Vorläufig alle als `kt-…` in `werkzeuge/karten/karten.css` und `satz.css`.
- **12.10.2026 · karten · `welt.js` bei unbekanntem Haus:** Die Antwort 404 von `/api/haus/<haus>` wird nicht ausgelesen, die Anfrage bleibt für Prüfwerkzeuge offen (Warten auf «Netz ruhig» hängt). Dazu: die `haus.json` eines neuen Hauses legt der Stamm an; ohne sie läuft ein Haus als Grandhotel mit seiner Kennung als Namen.
- **12.10.2026 · karten · Zeichen, Tapete und Fotos des Hauses:** jedes Werkzeug holt sie heute selbst (`werkzeuge/karten/kleid.py`, `werkzeuge/gaeste/kleid.py`, je eigener Ordner `kleid/<haus>/`, je eigenes Rezept). Gehört an eine Stelle (wohl «marke» oder `haeuser/<haus>/`).
- **12.10.2026 · karten · Der Server lädt nur `api.py` frisch:** Hilfsdateien daneben (`modell.py`) bleiben bis zum Neustart beim alten Stand; der Server auf 8970 lief so kurz mit zwei Ständen und antwortete mit Fehlern. Vorläufig lädt `werkzeuge/karten/api.py` sein `modell` bei jedem Aufruf selbst neu.
- **12.10.2026 · karten · Vorschlag für die Prüfpunkte:** «Druck und Dateien: was muss auf dem Server liegen, damit eine PDF entsteht (Browser, Schriften, Prüfwerkzeug), und was geschieht, wenn es fehlt?» Bei karten: node, Playwright mit Chromium, poppler; fehlt eines, wird mit Stichwort `druck` abgebrochen und nichts veröffentlicht.
- **12.10.2026 · website · Ziel für gebaute Seiten:** Der Speicher kennt nur Daten. Die veröffentlichten Seiten schreibt das Werkzeug deshalb selbst, an einer einzigen Stelle (`werkzeuge/website/ausgabe.py`, Ordner `_probe/<haus>/online/`). Schwäche: Stand im Speicher und Seiten auf der Platte sind zwei Schritte, keine Einheit; die Prüfseite vergleicht beide und «Seiten neu ausgeben» behebt eine Abweichung.
- **12.10.2026 · karten · Abgebrochene Verbindungen:** Lädt der Browser neu, während ein Aufruf läuft, schreibt `unterbau/serve.py` `FEHLER … BrokenPipeError` samt Spur
  und versucht noch eine Antwort 500 zu senden. Das sieht in der Ausgabe wie ein Fehler des Werkzeugs aus. Vorläufig: `werkzeuge/karten/pruef.js` zählt solche Abbrüche nicht. Wunsch: still übergehen.
- **12.10.2026 · website · Eigene Wege antworten nur mit JSON und sehen keine Parameter hinter dem Fragezeichen** (deckt sich mit karten): Die Vorschau einer Seite kommt als JSON und wird als `srcdoc` in den Rahmen gesetzt, Angaben stehen im Pfad. Folge: die Vorschau läuft im Ursprung des Werkzeugs.
- **12.10.2026 · website · Ablage für hochgeladene Dateien** (deckt sich mit karten): fehlt, deshalb lässt sich ein Foto nur gegen eines tauschen, das auf der Website schon vorkommt.
- **12.10.2026 · website · `veroeffentlichen`, `zurueckholen`, `entwurf_verwerfen` ohne `erwartet`** (deckt sich mit gaeste). Vorläufig: eigener Weg `veroeffentlichen` prüft die Kennung vorher, aber nicht in derselben Sperre; vor dem Zurückholen fragt das Werkzeug nach. Dazu: Zwischenstände des Entwurfs für ein dauerhaftes «Rückgängig» (jetzt nur, solange die Quittung steht).
- **12.10.2026 · website · Sprachen des Hauses in `haus.json`:** stehen jetzt in `werkzeuge/website/haeuser/<haus>.json`, andere Werkzeuge brauchen sie auch.
- **12.10.2026 · website · Bausteine in `welt.css`:** kleine Taste ohne Knauf · Auswahl im Stil des Hauses · Fenster · Zeile als Taste · Zeichen «fehlt» als Rahmen · Feld zum Hineinschreiben mit Auszeichnung. Vorläufig mit Vorsatz `ws-` in `website.css`.
- **12.10.2026 · website · Entscheid zum Speichern-Knopf:** der Rahmen (Master, Abschnitt 7) nennt grau, gelb, grün, das Artbook kennt dafür keine Farben. Vorläufig: hell, dunkel mit «Eingabe noch nicht gespeichert», «Gespeichert» mit Haken.
- **12.10.2026 · website · Vorschlag für die Prüfpunkte:** «Quelle in Bewegung: was geschieht mit gespeicherten Änderungen, wenn das Haus seine Website neu baut?» Bei website: `probe.py --neu` holt die neuen Seiten, die Prüfseite nennt Änderungen ohne Platz, einen selbsttätigen Abgleich gibt es nicht.
- **19.10.2026 · marke (Schlössli) · Prüfläufe nach der Umstellung auf «Die Bühne»:** Die Bedienläufe des Hausbuchs (`pruefung/funktionen.js`, `zusatz.js`, aus Doldenhorn und Ruedihus) suchen die Klassen von vor der Umstellung (`.li-k`, `.li-hero`) und brechen ab. Vorläufig: neuer Lauf `Wirtschaft am Schlössli Bottighofen/_werkzeuge/livre/pruefung/bedienen.js` (57 Zeilen, Klassen des Pakets `wo-…`). Wunsch: die Bedienläufe gehören mit dem Oberflächen-Paket in den Stamm, damit jedes Haus denselben Lauf nimmt.

- **19.10.2026 · gaeste (Schlössli) · Restaurant ohne Zimmer:** Arten, Ruhetage, Ferien, Plätze je Etage und Allergen-Kürzel stehen beim Schlössli als Hauswerte im Code des Werkzeugs (`Wirtschaft am Schlössli Bottighofen/_werkzeuge/reception/reception.py`). Wunsch: als Angaben des Hauses in `haeuser/<haus>/haus.json` (Art des Betriebs, Ruhetage, Ferien, Räume mit Plätzen, Allergen-Kürzel der Karte), damit jedes Restaurant sie ohne Code bekommt. Gebaut wurde nach Master Werkzeug-Bau 2.1 als Kopie des Ruedihus, nicht im Stamm.

## Verlauf

- **12.10.2026** · Stamm angelegt: `welt.css`, `welt.js`, Schriften, Musterseite, Speicher, Server, Probelauf. Geprüft: Speicher 21 von 21,
  alle Wege des Servers per Abruf, Musterseite in beiden Welten am Rechner und in Handybreite ohne Überlauf und ohne Fehler.
  Die Ordner `werkzeuge/website`, `karten`, `gaeste` sind leer und warten auf ihre Chats.
