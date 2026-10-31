---
tags: [projekt, website]
status: aktiv
---

# Lieferung · Die Besucherliste (Le Registre, Besuche) · Culinarium Hannover

Status: fertig, lokal, nichts online, nichts verschickt (28.10.2026, Chat «culinarium-registre»).

**Werkzeug:** http://localhost:9086/_werkzeuge/registre/  (Server: `python3 _werkzeuge/registre/server.py 9086` im Projektordner; Bilder ohne Tagesgruss: `?gruss=tag`)
**Anleitung:** http://localhost:9086/_werkzeuge/registre/anleitung.html (zehn Kapitel, Bilder aus dem Werkzeug)
**Stand-Weg für La Maison:** http://localhost:9086/api/registre?tage=30&beispiel=1 (die Zentrale liest ihn über http://127.0.0.1:9081/_weiter/registre/…)
**Bilder für Oberchef und Werkbank:** http://localhost:8978/haus/_Oberchef/zeigen/culinarium/registre/registre-start-1440.png (dazu `-390`, `besuche`, `buchung`, `herkunft`, je 1440 und 390, erstes Bild und `-ganz`)
**Funktionsliste:** http://localhost:8978/haus/Culinarium%20Hannover/_werkzeuge/registre/FUNKTIONSLISTE.md

## Was steht

- **Kopie des Besucherbuchs der Taverne zum Schäfli** (jüngstes Vorbild, mit allen Funden des Demo-Checks vom 21.10.; nur gelesen), Rahmen aus der gemeinsamen Oberfläche von Culinarium (`_werkzeuge/oberflaeche/`, Kleid `culinarium`, nur gelesen). Name nur aus `kleid/culinarium.js`: Robert hat am 28.10. Satz A «An der Bar» gewählt, das Werkzeug heisst **«Die Besucherliste»**, die Zentrale «Der Tresen». Werkzeug, Rand, Rundgang und Anleitung lesen ihn von dort (Anleitung und ihre Bilder danach neu gebaut). Der Eröffnungssatz sagte «Wie ein Gästebuch …»; weil «Das Gästebuch» jetzt der Name des Gäste-Chat-Werkzeugs ist, heisst er nun «Wer deine Website besucht hat: …».
- **Kleid Culinarium, nicht Schäfli umgefärbt:** Fraunces mit weichen Enden für Titel, Instrument Sans im Lauf, DM Mono für Zahlen, nie fett, nie kursiv; Farben nur über die Variablen des Kleids (Nacht, Schiefer, Warmweiss, Kerzenlicht); das «C» der Wortmarke als Zeichen (Kopf, Leere, Anleitung, Favicon); Knöpfe und Wahlen mit der Kante der Website (10 px), keine Pillen-Reihen. Auch Rundgang-Karte, «Zur Werkbank»-Knopf und Anleitung tragen jetzt das Kleid (im Vorbild Schäfli stand die Rundgang-Karte noch im Blau des Rivage, siehe Lernen).
- **Bühnen** je Ansicht mit Rudis Fotos aus dem Bildregister der Website (`/assets/bild/<schlüssel>-1600.webp`, geschärfte ziehen von selbst nach): Übersicht die Fenster der Bar am Abend (aus dem Kleid), Besuche ein Teller wird an den Tisch gebracht, Herkunft die Schilder an der Hausecke in Linden, Zeit ein Drink bei Nacht, Seiten die Plakatwand, Verlauf zwei Köche am Pass, Zum Platz angestossen bei Kerzen an der Tafel, So wird gezählt ein Tablett mit Gläsern. Kein Bühnenfoto wiederholt ein Seitenbild der Ansicht.
- **Seiten von Culinarium** (`python3 registre.py seiten`): neun Seiten mit den Namen, die die Website selbst nennt (Seiten-Leiste im Fuss: Startseite, Der Abend, Alle Abende, Das Haus, Team, Der Weg, Dirty Chicken, Impressum, Datenschutz); je Seite das erste eigene Foto in ihrem Inhalt, keins doppelt; Impressum und Datenschutz ein freies Foto der Bar. Wahlseiten und `termine-pflege.html` zählen nie.
- **Wege von Culinarium** (Master G14, Schlüssel wie in allen Häusern): «Platz buchen» geöffnet (`fenster`) · Platz gebucht, erst wenn das Ticket steht (`buchung`) · auf die Warteliste gesetzt, erst bei «Danke … Du stehst auf der Liste» (`booking`) · Warteliste im Ticket begonnen (`tisch`) · Warteliste im Fuss mit E-Mail (`anfrage`) · Telefon der Bar (`anruf`) · Instagram von Culinarium oder dem Team (`mail`) · weiter zur Bar oder zu Dirty Chicken (`chat`) · Route auf «Der Weg» (`route`). Die Ansicht heisst «Zum Platz» (Platz gebucht oder Warteliste).
- **Neu, Master G16:** Bei Culinarium bucht nur «Der Abend». Damit «Von der Startseite zum Platz» und «Welche Seiten vor dem Platz lagen» etwas sagen, zählt jede Seite, die ein Besuch bis zu seinem Platz ansah (`platz_bis` in `registre.py`, `platzBis` in `registre.js`, eigene Rechnung in `nachrechnen.py`). Der Weg zum Platz (Trichter): Besuche → «Der Abend» geöffnet → Platz gebucht oder Warteliste; La Maison übernimmt genau diese Stufen (gemeldet, von `culinarium-maison` bestätigt).
- **Eigene Zählung von Culinarium** (Master G09): eigener Schlüssel `~/Desktop/Website-Projekte/_Schluessel/culinarium-hannover.txt` (nur seine Prüfsumme in `anschluss.py` und `online/registre.py`), eigenes Geheimnis, eigener Speicher (lokal `_daten/`, online nur `REGISTRE_READ_WRITE_TOKEN`, sonst `/tmp/culinarium-hannover-registre-demo`). Uhrzeit und Tag in Hannover (Europe/Berlin).
- **Beispielwerte von Culinarium**, überall als Beispiel beschriftet: Orte Hannover und Region, Hildesheim, Braunschweig, Celle, Hamburg, Berlin, wenige von weiter her; Herkunft vor allem Instagram und Google, dazu Facebook, Hannover Marketing; meist am Handy, am Abend, zum Wochenende hin mehr. In der Vorführung gibt es nur Beispielwerte.
- **Zählung für die Website liegt bereit, ist aber nicht eingebaut:** `vorschlag/messung.js` (soll später `website/assets/messung.js` werden). Nicht jetzt, weil Roberts Server auf 8765 ein reiner Dateiserver ist: dort zeigt jede Seite mit der Zählung den Konsolenfehler «501». An `culinarium-website-pruefung` gemeldet. Datenschutz-Satz als Vorschlag: `vorschlag/datenschutz-text.md` (erst einfügen, wenn die Zählung online läuft; vom Haus zu prüfen).

## Wie geprüft

- **`abnahme.js` (91 Zeilen = Master 3 R01–R24 und 4.6 G01–G16, jede bedient, nicht nur geladen):** Chromium und WebKit, je 1440 × 900 und 390 × 844, an der Probe-Kopie `~/Desktop/Website-Projekte/_Probe Culinarium Registre/` mit Wegwerf-Daten unter `/tmp` (auf dem eigenen Port 9086, das Werkzeug dafür angehalten): **91 von 91 grün in allen vier Läufen**, zweimal (vor und nach dem Umstellen der Beispielbesuche auf «ab Mitternacht», damit «heute» am frühen Morgen in Hannover nicht 0 zeigt); nach der Namenswahl die 15 Zeilen mit Namen und Zahlen (A05, A09, B01, B03, B05, B06, C03, G01, H01, L02, O01, P02, Q01, Q02, Q05) in Chromium 1440 und WebKit 390 noch einmal: grün. Darin: alle acht Ansichten, Zeitraum 7/30/90 gemerkt, Filter, Besuch wählen ohne Springen, lange Besuchskarte (G15), Kopf, Rand und Rand-Klappe am Handy, Leiste, Meldungen, Rundgang, Anleitung, «Als Tabelle sichern» (CSV gegen die Daten), Fehlermelder, Startfehler-Tür, Sicherheit des Dienstes (fremde Herkunft 403, Zeile über 300 Zeichen 413, zu viele Anfragen 429, Ausfuhr nur mit Schlüssel, keine Quelltexte), Sicherheitsregel der Online-Fassung (CSP), «Zur Werkbank», die Zählung an den echten Seiten (Z01: Startseite Telefon, Instagram, Warteliste im Fuss → «Der Abend»; leeres «Jetzt bezahlen» zählt nicht, gebucht zählt erst mit Ticket; leere Warteliste zählt nicht, ausgefüllt zählt; Route; Z01b: Fuss ohne E-Mail zählt nicht, Bar, Dirty Chicken, Team-Instagram; Z02: nicht mitzählen, Prüfbrowser, Werkzeug). Protokoll `_pruefung/abnahme-4laeufe.log`, Ergebnis `abnahme-ergebnis.json`, `FUNKTIONSLISTE.md`.
- **`_pruefung/nachrechnen.py`:** jede Auswertung unabhängig aus den Rohdaten nachgerechnet (7/30/90 Tage, auf Uhrzeiten gekürzt, um 1/3/7 Tage geschoben, echte Zählung mit 160 Zeilen und 11 ungültigen, Datenschutz): **0 Abweichungen** (`_pruefung/nachrechnen.txt`).
- **`pruefung/fehlerbuch.js`** (Fehlerbuch 10a gemessen): Chromium und WebKit × 1440, 1366, 1240, 1180, 1100, 1000, 920, 390, 320 × acht Ansichten = 144 Messungen je Regel. Grün: roher Vorlagen-Code nirgends, Kopf-Titel überdeckt keinen Knopf, Titel auf dunkler Bühne hell, unter der Bühne ≥ 30 px (Handy 24), Überschrift nie ohne Luft, kein seitliches Verrutschen, **jedes Element** im Fenster, **kein abgeschnittener Text**, Vergleich: Name stösst nie an die Zahl, jeder Listeneintrag mit Bild, Listenbilder ≥ 72 px, kein mailto/tel im Werkzeug, Titel passt ins Kopfbild, kein Foto zweimal (ausser Besuchsliste, so festgelegt), Rundgang-Schild steht fest. Einzig «Kacheln gleichmässig» meldete 4× am Handy die neun Werte in einer Spalte: das ist die Regel selbst (Zeile 86, am Handy eine Spalte), die Messung war falsch und ist berichtigt. `pruefung/fehlerbuch-ergebnis.json`.
- **Schneller Blick** (`pruefung/blick.js`, jede Ansicht ganz durchgescrollt, Chromium und WebKit, 1440 und 390): keine Konsolenfehler, keine Antwort ≥ 400, kein leeres Bild, nichts ragt hinaus. Bilder in `pruefung/bilder/`.
- **Flüssigkeit** (Regel 55, `mess.js`, Chromium gedrosselt, Ansichtswechsel + Scrollen, `pruefung/fluessigkeit.txt`): 4× p50 8,3 ms / p95 10,2 ms (1440) und 10,1 ms (390), höchstens 3 von ~1100 Bildern über 33 ms; 6× p95 10,3 ms, höchstens 6 von ~1100 über 33 ms, gleich auch mit «weniger Bewegung» (also Rechnerlast, 10 bei der Messung).
- **Fremde Hausangaben:** Suche nach Rivage/Interlaken/Bottighofen/Wigoltingen/Schlössli/Schäfli/Kuchler/Maeder/Carlton/Zurbriggen/Doldenhorn im Revier: nur Herkunftsvermerke in Kommentaren (woher kopiert), keine sichtbare Angabe.

## Fehlerbuch 10a gegen dieses Werkzeug (die Zeilen, die ein Besucherbuch oder alle Werkzeuge betreffen)

| Regel | Stand bei Culinarium |
|---|---|
| Listenbilder 104 × 78 (Handy 72 × 54), Text nie abgeschnitten, Wörter nie mitten getrennt | erfüllt, gemessen (144/144) |
| Fund eines Schwesterhauses nachgezogen (Vergleich, Woche für Woche, Wahlen am Handy, lange Karte G15) | alle aus dem Schäfli-Demo-Check übernommen und gemessen |
| Jeder Link in Kopf und Rand antwortet 200 (Website, Anleitung, Zentrale) | erfüllt (Q01, B03) |
| «Zur Werkbank»: Herkunft `wb`/`wy`/`wbo`, Knopf unten links frei (`data-neben`, `data-ueber`) | erfüllt (Q02); Schlüssel `culinarium-wb` |
| Zentrale aus dem Werkzeug immer auf ihrem eigenen Server (127.0.0.1:9081) | erfüllt (Link aus `WO_HAUS.ports`, B03) |
| Weg zum Tisch/Platz in der Zentrale = Stufen und Rechnung des Besucherbuchs, nie über 100 % | an `culinarium-maison` gemeldet, dort übernommen |
| Dunkle Flächen nur Töne des Kleids; Schrift auf Dunkel hell; Titel hell | erfüllt (144/144) |
| Keine Farbe der Vorlage eines anderen Hauses stehen lassen | erfüllt nach Suche über **alle** Dateien, auch Skripte mit eingebautem CSS (neuer Fund, siehe Lernen) |
| Kein mailto/tel im Werkzeug | erfüllt (144/144) |
| Kopf-Titel überdeckt nie einen Knopf (920–1240) | erfüllt (144/144) |
| Unter der Bühne ≥ 30 px, zwischen Schrift und Kachel ≥ 16 px | erfüllt |
| Kacheln gleichmässig, Handy eine Spalte | erfüllt |
| Rundgang-Schild steht fest | erfüllt (18/18) |
| Keine «Wer arbeitet hier?»-Abfrage, keine ausgegrauten Knöpfe, Leiste eine Quelle | erfüllt (gibt es nicht; Leiste: Beispielwerte + «Als Tabelle sichern») |
| Roher Vorlagen-Code (`{`, undefined, NaN, None) | nirgends (144/144) |
| Anleitung nennt nur dieses Haus und wird mit jeder Änderung nachgezogen | erfüllt, neu gebaut mit Bildern vom heutigen Stand |
| Texte: Wertigkeit, keine Menge, kein Insider-Wort ohne Erklärung | geprüft: «wer sich seinen Platz an der Tafel sichert», keine Stückzahlen als Pointe |

## Lernen (für alle Häuser eingetragen, Master 10a und 4.6)

1. **Rundgang im Rivage-Blau** (neu, 10a): `rundgang.js` bringt sein CSS als Zeichenkette mit; im Besucherbuch des **Schäfli und des Schlössli** steht die Rundgang-Karte noch in `#A2B6CF`/`#041023` mit «Open Sans». Regel: nach dem Umfärben alle Dateien nach den Hexwerten der Vorlage durchsuchen, auch Skripte. **Offen dort** (nur gelesen, an den Oberchef gemeldet).
2. **Feste Sommerzeit in Prüfungen** (neu, 10a): die übernommene Abnahme setzte «16 Uhr» fest mit `+02:00`; seit dem 25.10. falsch. Regel: Ortszeit aus der Zone rechnen. Steckt noch in den Abnahmen von Schäfli und Schlössli.
3. **Zählung nicht auf einen reinen Dateiserver** (neu, 10a): `messung.js` erst einbauen, wenn der Server der Website `/api/registre` annimmt; sonst 501 in jeder Konsole.
4. **G16** (neu, 4.6): Weg zum Platz, wo nur eine Seite bucht.

## Offen (mit Grund)

- **Zählung auf der Website:** nicht eingebaut (Grund oben); einbauen beim Online-Gehen oder mit einem Hausserver, der `/api/registre` mit 204 annimmt. Revier `website/` gehört `culinarium-website-pruefung`.
- **Online:** nichts hochgeladen (Auftrag). `online.json` steht für den gemeinsamen Online-Weg; Speicher und Online-Probe erst mit dem Hochladen des Hauses.
- **Anmeldung mit Passwort (R22):** erst bei der Auslieferung (Robert 15.10.2026).
- **Firefox und 1366/320 als volle Abnahme** (Master 8): nicht verlangt («Fertig heisst» nennt Chromium + WebKit, 1440 + 390); `ALLE=1 node abnahme.js` läuft sie (12 Läufe), 1366 und 320 sind in der Fehlerbuch-Messung enthalten.

## Nachtrag 29.10.2026 · ohne Leere (Chat culinarium-maison im Auftrag des Oberchefs)

Robert: «Da sieht das … noch sehr leer aus, links.» In jeder Ansicht stehen die Spalten jetzt gleich hoch und gefüllt (Kriterium 4), nur mit Werten, die die Besucherliste wirklich zählt:
- Übersicht: links drei Blätter statt eines halb leeren: «Woher die Gäste kommen» nach Orten (Knopf «Alle Orte»), «Wie sie zu dir finden» (Gekommen über), «Handy oder Rechner».
- Herkunft: «Gerät» links unter «Gekommen über», «Sprache des Browsers» rechts unter «Orte» (13 Orte); keine halb leere zweite Reihe mehr.
- Verlauf: die Wochen verteilen sich über die Höhe der Vergleichstabelle.
- Zum Platz: rechts neu «Plätze Woche für Woche» unter «Der Weg zum Platz».
- Technik: `.zwei--fuell` in `registre.css` (Stapel teilen sich die Höhe, Listen verteilen Resthöhe zwischen die Zeilen). Sicherung `registre.js|css.vor-uebersicht-2026-10-29`.
- Geprüft: `pruefung/fehlerbuch.js` 0 Fehler, `pruefung/blick.js webkit` ohne Fehler; Höhenmessung je Ansicht (WebKit 1440): beide Spalten gleich, Rest unter jedem Blatt 20–33 px (Innenabstand).
- Vorher/nachher: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/besucherliste-uebersicht-2910/index.html

## Messlauf 30.10.2026 (Chat Messlauf/Querprüfung)

Anleitung «So ist die Besucherliste aufgebaut.» ohne Einzelwort. Abnahme `abnahme.js` an die Übersicht «ohne Leere» (29.10.) angepasst (H03, K01, K03), Nachrechnen und Zahl-Prüfungen mit «weniger Bewegung» (die Zahlen laufen seit 30.10. hoch), Anschluss ans Gästebuch im Prüfbrowser angenommen (Z01), Einzahl «Ein Besuch heute» (N05), Hinweis an der Säule erst nach dem Einschweben geprüft (H02): 91 von 91 Zeilen grün in Chromium und WebKit, 1440 und 390.
Tafel: http://localhost:8978/haus/_Oberchef/zeigen/culinarium/messlauf-2910/index.html

## Abnahme-Tor 30.10.2026 · Löcher (cu-messlauf im Auftrag des Oberchefs)
- Gestreckte Blätter (Übersicht, Herkunft, Zum Platz): der freie Platz geht an das Blatt mit der langen Liste, kurze Listen bis vier Zeilen behalten ihre Höhe; in der gestreckten Liste verteilt er sich über, zwischen und unter den Zeilen; Blatt-Titel 4 px näher an der Liste. Vorher «Gerät» 22 %, «Der Weg zum Platz» 16 %, «Plätze Woche für Woche» 14 % Loch, jetzt alle unter 14 % (Bildprüfung des Tors, WebKit 1440 + 390).
- Besuchskarte (ab 1181 px, bleibt so hoch wie das Fenster): unter einem kurzen Weg zeigt die freie Höhe die Seite, auf der der Gast ankam; bei einem langen Weg entfällt das Bild (unter 90 px). Vorher 42 % Loch bei einem Besuch mit einer Seite.
- Nicht geändert: «Versalien in Culinarium Mono» ist ein Fehlalarm, «Culinarium Mono» ist DM Mono (Kleid, `schrift/dmmono.woff2`). Die übrigen Funde von Tor 2 und Tor 6 hat cu-tresen-kleid um 11:39 behoben.
Sicherungen `*.vor-luecken-2026-10-30` (registre.js, registre.css, index.html).

## Abnahme-Tor 6, Teil 2 und 3 (12–24) und Prüfung von Teil 1, 30.10.2026 (cu-messlauf)
Am Bild geprüft (WebKit, 1440 / 1000 × 650 / 390, je Stelle ein Blick): Teil 1 (1–11, gebaut vom Tresen-Kleid) stimmt; dazu nachgebessert:
Anleitungs-Hero am Rechner gross (Titel bis 6,6 rem, Satz 20 px, sonst leere Tafel rechts), Rundgang ohne Leiste über dem Gezeigten, «Weiter» in schmaler Karte ganz drin (Wegstriche entfallen unter 290 px).
Teil 2/3: 12 alle zehn Anleitungsbilder neu (k05 bei 400 px, Kennzahlen ganz) · 13/21 Seiten-Tabelle: 621–1240 px ohne Balkenspalte, Handy Bild links, Name und «… im Schnitt» untereinander, Zeitwerte nie umbrochen, Köpfe gleich klein ·
14 Verlauf Handy «3:48 Min.» einzeilig · 15 Besuche-Liste bei jeder Breite Zeit oben, Seiten und Dauer darunter; «Besuche je Tag»: «· Verlauf» bleibt zusammen · 16 Herkunft-Band Handy einzeilig, Zahlen auf einer Linie ·
17 Besuche-Filter Handy als Wischleiste · 18 Anleitungskopf Handy wie vom Tresen-Kleid gebaut, geprüft · 19 «Gerät» nicht mehr gestreckt (Block «Löcher») · 20 «Alle Besuche» als Knopf mit Knauf und → ·
22 bis 760 px Fensterhöhe kommt die Leiste erst nach dem ersten Scrollen · 23 Ranglisten 701–1240 px untereinander, Namensspalte nach dem längsten Namen · 24 «Zum Platz» Etiketten mit zwei Zeilen Platz, Zahlen auf einer Linie.
Sicherungen `*.vor-luecken-2026-10-30` (culinarium.css, registre.js, registre.css, index.html, anleitung.html, anleitung.vorlage.html, anleitung_bilder.js, Ordner anleitung.vor-luecken-2026-10-30).
Nachtrag 25/26: Leiste «… mit Besuchen aussieht.» mit festem Leerzeichen und ohne ausgewogenen Umbruch (1000 px geprüft); Orte in der Besuche-Liste halten die letzten zwei Wörter zusammen («Frankfurt am / Main, Deutschland», 1280 px geprüft).
Nachtrag 27/28: «Am meisten angesehen» Namen nie umbrochen, Namensspalte nach dem längsten Namen (höchstens 270 px), «… im Schnitt» bricht nur vor «im Schnitt» (1440/1280/390 geprüft); Kennzahlen «Zum Platz» je Reihe gleich hohe Etiketten, Zahlen auf einer Linie (1440/1000 geprüft).

## Nachtrag Besuchskarte (30.10.2026, cu-messlauf)
- Loch zwischen letztem Schritt und Fussnote bei Besuchen mit wenigen Seiten: Das Bild unter dem Weg hat jetzt mindestens 140 px und wird nie mehr ausgeblendet; die Karte wächst dafür. 30 Besuche bei 1440 × 900 und 1280 × 720 gemessen: Abstand Weg → Fussnote überall nur noch Bild + 14 px. Am Bild geprüft: Hannover 27.10. 17:27, Hildesheim 28.10. 21:33.
- Dateien: registre.css (Block `.besuch__buehne`), index.html (?v=). Sicherungen `*.vor-buehne-2026-10-30`.
- Fund 30 (Meldung unter dem Rundgang-Schild): Solange eine Meldung steht, tritt das Schild «Kurzer Rundgang» zurück und kommt nach dem Schliessen wieder. Geprüft bei 1440 und 390 mit «Als Tabelle sichern». Datei: culinarium.css (letzte Zeilen), index.html (?v=). Sicherung `culinarium.css.vor-meldung-2026-10-30`.

## Fund 31 (Tor 6, 30.10.2026, cu-messlauf)
- Unterzeile der Besuchskarte: Der Trenner «·» zwischen Seiten und Dauer hängt jetzt am folgenden Wert (` ·&nbsp;`) und steht nie am Zeilenende. Bei schmaler Spalte beginnt die zweite Zeile mit «· 1 Min. 24 Sek.».
- Etikett «Bar, Dirty Chicken» → zwei Teile: am Rechner «Bar · Dirty Chicken» (Trenner fest gebunden), bis 600 px übereinander ohne Trenner. registre.js (karteBesuch), culinarium.css (letzte Zeilen), index.html (?v). Am Bild geprüft: 390 Besuche und Übersicht, 1440 Besuche, 1000 Übersicht. Sicherungen `*.vor-fund31-2026-10-30`.
- Besuch «Braunschweig, Heute 12:18»: kein echter Besuch, sondern ein Beispielwert. beispiel/30.json enthält ihn am letzten Tag. Die Beispielwerte werden auf heute geschoben und bei der jetzigen Uhrzeit abgeschnitten (ablage_heute/kuerzen), darum zählt die Liste im Lauf des Tages hoch (478 → 479 nach 12:18).
- Nachtrag Fund 31 (19:45): Seiten und Dauer sind zwei Teile, jeder bleibt ganz. Der Trenner gehört zum zweiten Teil und wird am Zeilenanfang abgeschnitten, er steht also nur zwischen zwei Teilen derselben Zeile. Bricht die Zeile, stehen «eine Seite» und «1 Min. 24 Sek.» ohne Trenner untereinander. Das Etikett steht in jeder Karte unter 440 px zweizeilig (Container-Abfrage statt Bildschirmbreite), also auch in der schmalen Liste bei 1280. Gemessen über alle Karten bei 390, 1000, 1280 und 1440: kein Trenner am Zeilenrand. Sicherungen `*.vor-fund31b-2026-10-30`.
