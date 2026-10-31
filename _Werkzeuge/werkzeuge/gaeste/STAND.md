# Werkzeug «gaeste» · La Réception (Grandhotel) · Der Gastgeber (Landhaus)

Stand 12.10.2026, erster Bau und am selben Abend die Bühne (siehe «Bühne»). Zuerst `../../STAND.md` lesen (Aufbau, Speicher, wem was gehört). Diese Datei sagt, was hier steht, was offen ist und wie jeder Prüfpunkt belegt ist.

## Was steht

Ein Werkzeug für jedes Haus: `http://127.0.0.1:8970/werkzeuge/gaeste/?haus=<kennung>`. Probehäuser: `?haus=gasterntal` (Landhaus), `?haus=beau-rivage` (Grandhotel). Der Modus-Knopf oben rechts wechselt Namen, Schrift und Farben.

| Bereich | Was er tut |
|---|---|
| Übersicht | Lage in drei Platten (Eingang, ohne Antwort, Wissen), zuletzt angefragt, Liste «Noch offen» mit allem, was in den Quellen fehlt |
| Eingang | Anfragen aus dem Chat (Zimmer, Tisch, Feier, Tagung): Angaben, Gespräch, Antwortentwurf (KI oder Gerüst ohne KI), ändern, sichern, kopieren, im Mailprogramm öffnen, erledigt, löschen. Verschickt wird nichts |
| Das wurde gefragt | jede Frage an den Chat nach Themen; ohne Antwort → «Antwort nachtragen» oder abhaken |
| Wissen des Hauses | «Vom Team» (anlegen, ändern, entfernen) · «Aus Website und Unterlagen» (ansehen, suchen, neu einlesen) · «Angaben des Hauses». Jede Änderung ist ein Entwurf |
| Probe-Chat | das Team fragt wie ein Gast; «Wie veröffentlicht» oder «Mit dem Entwurf»; unter jeder Antwort, woher sie kommt |
| Auswertung | die häufigsten Fragen (im Wortlaut gebündelt), nach Themen, nach Sprache; nur Gäste oder mit Proben |
| Verlauf | frühere Fassungen ansehen und zurückholen, Protokoll «wer hat wann was getan» |
| Kosten und Schutz | Stand der KI, Kosten des Monats, Obergrenze setzen, Grenzen, gespeicherte Daten von Gästen, Löschen auf Wunsch eines Gastes |

Immer sichtbar: Band «Eine Anfrage wartet» (dazu Zahl im Titel des Fensters und am Bereich Eingang; das Werkzeug sieht jede Minute nach und wenn das Fenster wieder nach vorn kommt) · die eine Stelle für den Stand der KI · unten die Entwurfs-Leiste · nach jedem Speichern eine Quittung mit «Vorher, nachher» und «Rückgängig».

Bewusst draussen: selbst buchen, selbst Mails verschicken, Zugriff auf das Buchungssystem.

## Bühne (Robert 12.10.2026 abends: «viel geiler, viel atmosphärischer, viel hochwertiger animiert, beim Luxushotel luxuriöser, beim anderen mehr in den Wald passend, 3D»)

Vorbild waren die bestehenden Werkzeuge des Grand Beau-Rivage (La Maison, La Réception, L’Imprimerie): dunkle Bühne, helle Inseln, Fotos des Hauses. Gearbeitet wird weiter auf hellem Papier, der Aufbau bleibt der einer Profi-Software.

| | Grandhotel | Landhaus |
|---|---|---|
| Grund | Marine mit der Tapete des Hauses | Tannendunkel, aus Tanne und Fels der Welt gemischt |
| Kulisse oben | Foto des Hauses hinter einem Schleier (Grand Beau-Rivage: die Halle mit Leuchter) | Foto des Tals, davor zwei gezeichnete Tannenreihen, dazwischen zieht Nebel |
| Zeichen im Kopf | Zeichen des Hauses in Gold | Schriftzug des Hauses in Holz |
| Übersicht | drei Kacheln mit Foto, Tiefe und Zahl im Knauf; sie neigen sich zur Maus und kommen von rechts herein | dieselben, mit Holzkante |
| Probe-Chat | das Handy des Gastes dreht sich herein, darin der echte Chat; daneben, was das Team dazu sieht | dasselbe |
| Kulisse | füllt den ganzen Bildschirm und bleibt stehen, darüber Schleier und Tapete | füllt den ganzen Bildschirm und bleibt stehen, Tannenreihen am unteren Rand |
| Überall | Inseln (Bänder, Leiste), Auftritt jedes Stücks beim Wechsel des Bereichs, Fenster heben sich aus der Tiefe, Sprechblasen und Quittungen gleiten herein, Balken wachsen | dasselbe |

Regeln dahinter: bewegt wird nur über `transform`; was hereinkommt, ist von Anfang an deckend; nichts hellt bei Maus auf; kein Vorhang beim Laden; nach dem Scrollen 300 ms keine Neigung; `prefers-reduced-motion` schaltet jede Bewegung ab; Auftritte nur beim Wechsel des Bereichs, nicht bei jeder Änderung.

**Roberts zweite Runde am selben Abend, umgesetzt:** Die Leiste links steht fest und geht über die ganze Höhe durch (dunkel, mit Zeichen und Namen oben; sie bewegt sich nicht mehr mit). Jeder Bereich ausser der Übersicht hat oben links eine Zurück-Taste (zurück zum vorigen Bereich). Das Hintergrundbild war mitten im Bildschirm abgeschnitten: Als Vorschlag füllt es jetzt den ganzen Bildschirm und bleibt stehen; Robert wollte darüber reden, sein Urteil ist offen. Der Eingang sieht aus wie ein Posteingang (Name, Uhrzeit, zwei Zeilen Vorschau, Schilder) und öffnet nichts von selbst: Eine neue Anfrage bleibt neu, bis jemand sie anklickt.

**Beispiel-Anfragen:** `beispiele.json` hält je Haus vier erfundene Anfragen (zwei neu, eine gelesen mit Antwortentwurf, eine erledigt). Im Eingang tragen sie das Schild «Beispiel», zählen nie als Gäste, und «Beispiele entfernen» löscht sie restlos (`pruef.js`, Schritt 14). In den echten Daten beider Häuser sind sie seit 12.10.2026 abends geladen. Der Antwortentwurf beim Gasterntal (Wandergruppe) stammt samt Anfrage aus dem Probelauf im Projekt vom 10.10.2026, seine Zahlen stehen im heutigen Wissen. Der Antwortentwurf beim Grand Beau-Rivage (Klausur) ist am 12.10.2026 mit der echten KI geschrieben (ein Aufruf, USD 0.18), auf Grundlage der Mail-Vorlage 07; jede Angabe darin (Raum «Jungfrau», Bestuhlung, CHF 94, Einzelzimmer, Nummer des Event-Teams) steht so in den Quellen.

**Aufgefallen in der Quelle des Grand Beau-Rivage:** Auf der Website steht einmal «Restaurant «L’Ambiance», Mai bis Oktober» und einmal «Abendessen … ganzjährig im Restaurant «L’Ambiance»». Der Chat und der Entwurf geben wieder, was dasteht. Zu klären ist das auf der Website.

**Kleid je Haus:** Kulisse, drei Kachel-Fotos, Tapete, Zeichen oder Schriftzug sind Bilder des Hauses. `python3 werkzeuge/gaeste/kleid.py <haus>` liest sie aus dem Projekt des Hauses (nur lesen, Auswahl in `quellen.json` unter «kleid») und legt verkleinerte Kopien nach `kleid/<haus>/` (zusammen 0,8 MB). Erzeugt ist nichts. Ein Haus ohne Kleid bekommt die Bühne seiner Welt ohne Fotos.

**Gemessen 12.10.2026** (Rechner vierfach gedrosselt, 1440 breit, Chromium ohne Fenster): Auftritt der Übersicht 115 bis 116 Bilder je Sekunde, Handy im Probe-Chat 117 bis 118, Neigen der Kacheln 120, Scrollen 120. Längstes einzelnes Bild 74 ms, im Augenblick des Wechsels.

**Offen:** Roberts Urteil, vor allem zum Hintergrundbild über den ganzen Bildschirm. Die Kulisse des Grand Beau-Rivage ist ein Hochformat-Foto im Ausschnitt und wirkt unter dem Schleier weich; ein Querformat der Halle gibt es im Projekt nicht. Das Landhaus hat keine Tapete. Zähler laufen nicht hoch. Website und Karten (andere Chats) haben die Bühne nicht.

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html`, `gaeste.css`, `gaeste.js` | Oberfläche. Alles Sichtbare aus `stamm/welt.css`, eigene Klassen mit `ga-` |
| `api.py` | eigene Wege `/api/x/gaeste/<haus>/…` (Liste im Kopf der Datei) |
| `ki.py` | Anweisung an die KI, Aufruf, Kosten, feste Probe-Antworten, Gerüst ohne KI |
| `einlesen.py`, `quellen.json` | liest den ersten Stand eines Hauses aus dessen Quellen (nur lesen). Ein neues Haus ist ein Eintrag in `quellen.json` |
| `kleid.py`, `kleid/<haus>/` | die Bilder des Hauses für die Bühne (siehe «Bühne») |
| `pruef.js`, `pruef_teile.py` | fester Durchlauf (siehe «Prüfen») |
| `schlusslauf.json` | die zehn echten Antworten der KI vom 12.10.2026 mit Zählern (erfundener Gast «Prüfgast») |
| `PRUEFAUFTRAG.md` | Auftrag für einen eigenen Chat, der alles unabhängig nachprüft |

## Wo die Daten liegen (nur über `unterbau/speicher.py`)

- **`gaeste`**: das Wissen. `haus` (Angaben), `wissen` (Abschnitte aus Website, Unterlagen, Umgebung), `team` (nachgetragene Antworten), `vorlagen` (Mail-Vorlagen des Hauses), `karten` (Startfragen), `einstellungen` (Obergrenze, Grenzen, Aufbewahrung), `eingelesen` (wann, woraus, was offen ist). Weg: Entwurf → Vorher, nachher → Veröffentlichen → Verlauf → Zurückholen. **Hier stehen nie Daten von Gästen**, damit der Verlauf keine enthält.
- **`gaeste-betrieb`**: Anfragen, Fragen, Zähler für Grenzen und Kosten. Wird sofort gespeichert. Liegt im Entwurfs-Fach dieses Namens, weil der Speicher dort die Kennung prüft (zwei Schreiber überschreiben sich nicht). Nur hier stehen Daten von Gästen. Das ist eine Notlösung, siehe «Wünsche an den Stamm».

Eingelesen am 12.10.2026 (beim ersten Öffnen eines Hauses von selbst, sonst `python3 werkzeuge/gaeste/einlesen.py <haus>`):

| Haus | Wissen | Vorlagen | Fragen aus dem Projekt | offen |
|---|---|---|---|---|
| Berghotel Gasterntal | 10 Abschnitte, 57 175 Zeichen (6 Seiten, Karte 2026, 3 Seiten der Umgebung) | keine | 6 Probefragen vom 10.10.2026 (`antworten-gasterntal.json`), als «Probelauf im Projekt» gekennzeichnet | Mail-Vorlagen je Anliegen, Absender je Anliegen, Fragen echter Gäste |
| Grand Beau-Rivage | 19 Abschnitte, 136 314 Zeichen (9 Seiten, 5 Unterlagen, 5 Seiten der Umgebung) | 3 Vorlagen in 6 Sprachen (Buchung, Tisch, Feiern und Tagen) | keine (`_gast/daten` ist leer) | Fragen echter Gäste |

Fragen echter Gäste gibt es in keinem der beiden Projekte lokal. Sie liegen, wenn überhaupt, im Online-Speicher der Häuser und wurden nicht geholt.

## KI

- Betriebsart über `GAESTE_KI`: `probe` (feste Antworten, kostet nichts) · `aus` · leer = echte KI. Schlüssel: `ANTHROPIC_API_KEY` und `ANTHROPIC_WORKSPACE_ID` aus der Umgebung, sonst erster Schlüssel und erster Arbeitsbereich der Notiz «API Key Claude» (Pfad über `GAESTE_SCHLUESSEL_DATEI` änderbar). Der Schlüssel steht in keiner Datei des Projekts.
- Modell `claude-sonnet-5-5` (aus `_gast/gast.py` der Häuser, Roberts Entscheid vom 10.10.2026). Aufruf ohne Zusatzpaket über `urllib`, wie in allen Vorlagen. Chat mit `effort: low`, Antwortentwurf mit `effort: medium`. Das Wissen liegt im Zwischenspeicher der KI (fünf Minuten).
- Ohne KI (kein Schlüssel, leeres Guthaben, Obergrenze, Störung) läuft alles weiter: Der Chat verweist an die Rezeption, Antwortentwürfe kommen als Gerüst, und das Band unter dem Kopf sagt es.

**Gemessen im Schlusslauf am 12.10.2026 (10 Aufrufe, zusammen USD 0.57; Preisliste vom 06.10.2026: Eingang 2.00, Zwischenspeicher schreiben 2.50, lesen 0.20, Ausgang 10.00 USD je Million Tokens):**

| | Tokens des Wissens je Frage | erste Frage (Zwischenspeicher kalt) | jede weitere innert fünf Minuten |
|---|---|---|---|
| Gasterntal | 35 177 | USD 0.09 (gemessen 0.0905 mit Antwort) | USD 0.007 fürs Wissen, dazu Frage und Antwort |
| Grand Beau-Rivage | 76 630 | USD 0.19 fürs Wissen | USD 0.015 fürs Wissen, dazu Frage und Antwort |

Ein Antwortentwurf fürs Gasterntal las rund 18 500 Tokens (kalt rund USD 0.05). Antwortzeiten: 6 bis 25 Sekunden, die erste Frage am längsten. Was ein Monat kostet, hängt allein an der Zahl der Fragen und daran, wie dicht sie kommen; eine Zahl dafür gibt es erst mit echten Gästen. Hochgerechnet ist hier nichts.

Inhalt geprüft: Jede Angabe der zehn Antworten (Sauna 90 Minuten, CHF 60 und 50, zwei Stunden Vorlauf, Saisonschluss 25.10.2026, warme Küche bis 20:30, Transport CHF 15 und mindestens CHF 30, Spa 7.30 bis 21.00, Beauty 9.00 bis 19.00, Tageseintritt CHF 30 ab 16 Jahren, Day Spa CHF 45, Royal Suite 60 m² für bis zu sechs Personen) steht so in den Quellen. Der 24.10.2026 ist ein Samstag.

## Prüfen

```
node werkzeuge/gaeste/pruef.js                 alle zwölf Läufe (2 Häuser × 2 Welten × 1440, 390, 320), rund zwei Minuten
node werkzeuge/gaeste/pruef.js gasterntal land 390
python3 werkzeuge/gaeste/pruef_teile.py        nur die Teile ohne Oberfläche
python3 unterbau/pruefe.py                     Speicher des Stamms
```

`pruef.js` startet je Lauf einen eigenen Server auf 8974 mit Wegwerf-Daten und festen Probe-Antworten, ohne Fenster, und beendet ihn über seine PID. Antwortet auf 8974 schon etwas, bricht er ab und beendet nichts.

Ergebnis 12.10.2026, nach Bühne und zweiter Runde: `pruef_teile.py` 44 von 44 · `pruef.js` 12 Läufe mit 185 oder 186 Prüfungen, 2224 von 2224 · `unterbau/pruefe.py` BESTANDEN (21).

## Prüfpunkte (Liste aus `../../STAND.md`)

| Prüfpunkt | Stand | Beleg oder was fehlt |
|---|---|---|
| Backend | **offen** | Läuft nur, solange `unterbau/serve.py` auf diesem Rechner läuft. Fällt der Server aus, sagt die Oberfläche «Der Server antwortet nicht. Ihre Eingabe ist noch nicht gespeichert.» (`gaeste.js`, `ruf`), beim Start eine Tür mit Stichwort. Nichts startet ihn neu |
| Datenbank | **erfüllt im Rahmen des Stamms, sonst offen** | Zwei Ablagen über den Speicher. Zwei gleichzeitige Schreiber: `pruef.js` «Konflikt» (Wissen: 409, nichts überschrieben, danach beide Änderungen da) und «Konflikt am Antwortentwurf»; `pruef_teile.py` vier Schreiber, 60 von 60 Einträgen. Grösse: Wissen bis zwei Millionen Zeichen und 500 Antworten des Teams (`api.py`, `_pruefe_doc`), Betrieb bis 5000 Fragen und zwölf Monate. Offen: Der Betrieb ist ein einziges Dokument, jedes Schreiben schreibt es ganz |
| Authentication und Rollen | **offen** | Keine Anmeldung. Der Name für das Protokoll wird am Gerät gemerkt und ist frei wählbar; jede Änderung nennt `wer` |
| Rechteverwaltung | **offen** | fehlt ganz |
| API-Sicherheit | **teils erfüllt** | Geprüft wird: Stand vor dem Speichern (`_pruefe_doc`, `pruef_teile.py` sechs Fälle, `pruef.js` «kaputter Stand»), Länge und Form jeder Frage, Kennungen, unbekanntes Haus. Daten sind nicht als Datei abrufbar, Text von Gästen wird als Text gezeigt (`pruef.js` «Eingaben»). Offen: Die allgemeinen Wege des Stamms nehmen jeden Stand ungeprüft an, und `DELETE /api/entwurf/<haus>/gaeste-betrieb` würde den ganzen Betrieb löschen. Wer den Server erreicht, darf alles; die Herkunft einer Frage (`gast` oder `probe`) nennt der Aufrufer selbst |
| Rate Limits | **teils erfüllt** | Je Gespräch 20 Fragen in zehn Minuten und 80 am Tag, gesamt 2000 am Tag, 60 Antwortentwürfe der KI am Tag, Obergrenze je Monat in USD. Belege: `pruef.js` «Grenze» (21. Frage → Pause), `pruef_teile.py` «Obergrenze». Offen: Die Grenze je Besucher hängt an einer Kennung, die der Browser selbst wählt, und ist damit umgehbar (der Unterbau reicht die Adresse des Absenders nicht durch). Die Zahlen stammen vom Carlton-Europe und sind für kein Haus bemessen: 2000 Fragen am Tag wären beim Grand Beau-Rivage mindestens USD 30 am Tag. Die Obergrenze je Monat ist bei beiden Häusern nicht gesetzt |
| Logging | **teils erfüllt** | Wissen: Protokoll des Speichers, im Bereich «Verlauf» sichtbar (`pruef.js` «Protokoll nennt das Veröffentlichen»). Betrieb: jede Frage mit Antwort, jede Störung der KI als Stand. Fehler des Servers stehen in dessen Ausgabe; `pruef.js` verlangt, dass dort kein «FEHLER» steht. Offen: Das Protokoll von `gaeste-betrieb` wächst je Frage um eine Zeile und wird nie gekürzt; Fehler im Browser sammelt niemand |
| Backups | **teils erfüllt** | Wissen: jede veröffentlichte Fassung im Verlauf, Zurückholen als Entwurf (`pruef.js` «Zurückholen»), dazu die Sicherung des Speichers. Betrieb: nur die Sicherung des letzten Stands, bewusst ohne Verlauf (sonst liesse sich nichts löschen). Offen: keine Kopie ausserhalb des Rechners |
| Deployment | **offen** | Nichts ist hochgeladen. Git-Commit je Schritt, nur dieser Ordner |
| CMS-Datenmodell | **erfüllt fürs Einlesen, sonst teils** | Ein drittes Haus ist `haeuser/<haus>/haus.json` und ein Eintrag in `quellen.json`. `pruef_teile.py`: ohne Eintrag startet es leer mit «offen», mit Eintrag werden die Seiten gelesen, fehlendes Telefon steht als offen da. Offen: Eine neue Art von Quelle braucht Code in `einlesen.py`; die Themen der Auswertung sind eine allgemeine Wortliste, nicht je Haus |
| Übersetzungsworkflow | **teils erfüllt** | Es gibt keine Übersetzungen, die veralten können: Das Wissen ist deutsch, die KI antwortet in der Sprache der Frage. Beleg: `schlusslauf.json`, englische Frage nach dem Töpferkurs wurde aus der deutsch nachgetragenen Antwort englisch beantwortet. Offen: Niemand prüft fremdsprachige Antworten; die deutsche Lesefassung im Antwortentwurf steht in der Anweisung, ist aber nicht am echten Fall geprüft; Mail-Vorlagen gibt es nur beim Grand Beau-Rivage; das Gerüst ohne KI und die Oberfläche sind nur deutsch |
| KI-Kosten | **erfüllt für Anzeige und Grenze, offen für den Monat** | Gemessene Kosten je Frage oben. Bereich «Kosten und Schutz» zeigt Aufrufe, Tokens, USD des Monats und den gemessenen Schnitt (`pruef.js` «Kosten»). Obergrenze je Monat setzbar (`pruef.js` «Obergrenze», `pruef_teile.py`). Leeres Guthaben: Chat verweist an die Rezeption, Entwurf als Gerüst, Band sagt es (`pruef_teile.py`, vier Fälle mit ersetztem Aufruf; am echten leeren Konto nicht geprüft, das Guthaben reichte). Offen: Die Obergrenze zählt die eigenen Zähler, nicht die Rechnung von Anthropic, und kann um einen Aufruf überschritten werden; Monatskosten sind erst mit echten Gästen bekannt |
| Prompt-Injection-Schutz | **teils erfüllt** | Bauart (`ki.py`, Kopf der Datei): Text von Gästen nur im Gespräch; in der Anweisung nichts Internes; drei Werkzeuge mit strengem Schema, keines führt etwas aus; eine Anfrage wird nur abgelegt, wenn der Kontakt wörtlich im Text des Gastes steht; Antworten mit Sätzen der Anweisung gehen nicht hinaus; Text des Teams und fremde Seiten gelten als Auskunft, Kopfzeilen darin werden entschärft; die Oberfläche setzt nur Text. Belege: `pruef_teile.py` (16 Fälle), `pruef.js` «Text von Gästen wird nie ausgeführt», `schlusslauf.json` zwei echte Versuche (Systemprompt verlangt; falsche «System»-Nachricht mit Rabatt und Gratis-Suite): beide abgelehnt, nichts preisgegeben, kein Werkzeug aufgerufen. Offen: Zwei Versuche sind kein Nachweis; wer die Website des Hauses oder die eingelesenen fremden Seiten ändern kann, schreibt in die Anweisung; die Prüfung auf Sätze der Anweisung fängt keine Umschreibung |
| DSGVO und Schweizer Datenschutz | **offen** | Fest steht, was entsteht (Bereich «Kosten und Schutz», «Daten von Gästen»): Fragen mit abgedeckten Adressen und Nummern (`pruef_teile.py`), Anfragen mit Name und Kontakt, nichts im Verlauf des Wissens (`pruef.js` «Datenschutz»), keine Adresse des Rechners. Offen: Datenschutzerklärung für dieses Werkzeug; Vertrag und Übermittlung an Anthropic (jede Frage geht dorthin); wer im Haus die Daten sehen darf (keine Anmeldung); Namen, die ein Gast in eine Frage schreibt, bleiben im Wortlaut stehen |
| Datenlöschung | **erfüllt auf diesem Rechner** | Von selbst nach zwölf Monaten (`pruef_teile.py`), einzeln je Anfrage oder Frage, und je Gast über die Suche; danach steht im ganzen Speicher nichts mehr, auch nicht in der Sicherung (`pruef.js` «Löschen auf Wunsch», sucht in jeder Datei). Offen: Die Frist greift beim nächsten Schreiben, nicht zu einer Uhrzeit; eine Frage ohne Namen lässt sich keinem Gast zuordnen; was bei Anthropic liegt, löscht das Werkzeug nicht |
| Verfügbarkeit | **teils erfüllt** | KI aus: beschrieben und belegt (siehe KI-Kosten). Server aus: Quittung oder Tür. Offen: Das Fenster für Gäste auf der Website ist nicht angeschlossen; was der Gast bei einem Ausfall sieht, ist hier nur der Text der Antwort |
| Monitoring | **offen** | Niemand wird gerufen. Ansatz: `GET /api/x/gaeste/<haus>/ueberblick` liefert den Stand der KI und die wartenden Anfragen, auch für die Zentrale |
| Booking-Integration | **betrifft dieses Werkzeug nicht** | Es bucht nicht und fragt das Buchungssystem nicht. Es zeigt nur die Adresse der Buchung aus den Quellen des Hauses; fehlt sie, steht «offen» |

## Was offen ist (über die Prüfpunkte hinaus)

1. **Das Fenster für Gäste ist nicht angeschlossen.** Die Websites der Häuser fragen weiter ihre eigene Funktion `/api/gast`. Der Weg dafür steht (`POST …/chat` mit `herkunft: gast`), ist aber ohne Anmeldung und nur lokal. Bis dahin gibt es hier keine Fragen echter Gäste.
2. **Der Probe-Chat zeigt Inhalt und Weg der Antwort, nicht das Aussehen des Fensters auf der Website.** Buchungsmaske und Zimmermappe der Vorlage sind hier nur als Hinweis «Weg zur Buchung» da.
3. **Roberts Urteil zur Gestaltung steht aus.** Insbesondere die Bausteine, die es im Stamm nicht gibt (unten).
4. **«Geöffnet heisst gelesen»:** Wer eine neue Anfrage öffnet, setzt sie ohne Knopf auf gelesen (der Hinweis verschwindet). Das ist die einzige Stelle ohne Quittung.
5. **Wetter:** Die echte KI bekommt die Vorhersage von Open-Meteo (frei, 30 Minuten gemerkt), wie in den Vorlagen. Im Prüflauf wird sie nicht geholt.
6. **Ausweichen bei Ablehnung:** Lehnt die KI eine Frage ab, kommt der Verweis an die Rezeption. Ein zweites Modell wird bewusst nicht gefragt, damit die Kosten je Frage berechenbar bleiben.
7. **Offizielles Paket von Anthropic statt `urllib`:** sobald der echte Unterbau Pakete erlaubt.
8. **Antwortentwurf in fremder Sprache** (mit deutscher Lesefassung) ist gebaut, aber mit der echten KI nicht geprüft. Geprüft sind zwei Entwürfe auf Deutsch: Gasterntal ohne Vorlage (Schlusslauf), Grand Beau-Rivage mit Mail-Vorlage (Beispiel «Klausur»).
9. **Nur in Chromium geprüft.** Der Lauf im Safari-Kern ist vorbereitet (`PRUEF_BROWSER=webkit node werkzeuge/gaeste/pruef.js`), auf diesem Rechner fehlt aber eine Playwright-Fassung, die zum vorhandenen Safari-Kern passt. Auf einem echten iPhone oder in Safari hat das Werkzeug noch niemand geöffnet.

## Im eigenen Ordner gelöst, weil es im Stamm fehlt (siehe auch «Wünsche an den Stamm» in `../../STAND.md`)

Bausteine in `gaeste.css`, alle nur aus Werten von `welt.css`: Rand mit Bereichen (schmal: aufklappbar) · Band unter dem Kopf · Fenster · Sprechblase · Balken · Vorher/nachher mit Markierung · Schild (Rahmen, ohne Farbe) · Textknopf · Zeilen für lange Angaben · Umbruch langer Wörter in `.liste`.
Im Speicher: Betriebsdaten im Entwurfs-Fach von `gaeste-betrieb` · eigener Weg `speichern` mit Prüfung · ein Schloss im Server gegen gleichzeitige Schreiber · zweites Schreiben nach dem Löschen, damit die Sicherung leer ist · eigene Wege `stand`, `veroeffentlichen`, `zurueckholen`, `verwerfen`: gelesen wird nie mitten in einem Schreiben (der Speicher liest ohne Sperre; zwischen zwei Umbenennungen meldet er sonst «fehlt, Sicherung liegt vor» und der Server antwortet mit 500, im Prüflauf einmal in zwölf Läufen aufgetreten), und veröffentlicht, ersetzt oder verworfen wird nur der Entwurf, den der Mensch gesehen hat (`pruef.js` «mit veralteter Kennung abgelehnt»).
Bühne: Kulisse, Tannenreihe, Nebel, Kacheln mit Tiefe, Handy, Auftritte, eine sechste Schriftgrösse für den Gruss der Übersicht (`ga-gruss`).

## Verlauf

- **12.10.2026** · Erster Bau: Einlesen beider Häuser, eigene Wege, KI-Teil mit Probe-Antworten, Oberfläche mit acht Bereichen in beiden Welten, fester Prüflauf. Schlusslauf mit der echten KI: 10 Aufrufe, USD 0.57. Ergänzt nach dem Schlusslauf und mit dem zehnten Aufruf bestätigt: Regel, dass eingelesene fremde Texte Auskunft sind und keine Befehle.
  Der erste Stand beider Häuser liegt in den echten Daten (`daten/<haus>/gaeste`), der Server auf 8970 wurde von diesem Chat gestartet (`python3 unterbau/serve.py`, ohne `GAESTE_KI`, also mit der echten KI).
- **12.10.2026 spät** · Roberts zweite Runde: Leiste links fest über die ganze Höhe, Zurück-Taste, Kulisse über den ganzen Bildschirm (Vorschlag), Eingang als Posteingang mit Beispiel-Anfragen. Echte KI bisher: 11 Aufrufe, zusammen USD 0.75.
- **12.10.2026 abends** · Bühne je Welt, Kleid je Haus, Kacheln mit Tiefe, Handy im Probe-Chat, Auftritte. Lesen und Veröffentlichen über eigene Wege abgesichert. Alle Prüfläufe bestehen, Flüssigkeit gemessen.
  Die Wünsche an den Stamm stehen in `../../STAND.md`; diese Datei hat der Chat geändert, aber nicht committet (committet ist nur dieser Ordner).
