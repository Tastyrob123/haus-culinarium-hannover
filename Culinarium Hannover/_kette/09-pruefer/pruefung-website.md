---
tags: [projekt, website, pruefung]
status: liegt vor
---

# Culinarium Hannover · Website-Prüfung 28.10.2026

Prüfer: `culinarium-website-pruefung` (unabhängig, hat nicht an der Website gebaut). Geprüft auf eigenem Server, Roberts Server 8765 nicht angefasst.

- Website (Roberts Server): http://localhost:8765/index.html
- Prüfserver: http://localhost:8768/index.html
- Dieser Bericht: http://localhost:8978/haus/Culinarium%20Hannover/_qa/pruefung-2810/pruefung-website.md
- Bildtafel (alle Fundbilder vorher/nachher, Seiten 1440 und 390): http://localhost:8978/haus/_Oberchef/zeigen/culinarium/website-pruefung/index.html

**Kurz:** Acht echte Fehler gefunden und repariert. Sie betrafen seitliches Verrutschen am Handy auf vier Seiten und im Fuss, eine Warteliste, die die E-Mail verlor, zu kleine Bilddateien an fünf Stellen und einen Auftakt, der bei ausgefallenem Skript unsichtbar blieb. Am Look hat sich ab 390 px Breite nichts geändert. Offen sind ein toter Knopf «Zur Website der Bar», die fehlende Hauptüberschrift auf der Startseite, die 15 versteckten Hero-Fassungen in `abend.html` und zwei Texte; für alle braucht es eine Entscheidung.

## Was geprüft wurde

| Prüfung | Umfang | Ergebnis (Endstand, Version 26192) |
|---|---|---|
| Laden, Konsole, Netz | 10 Seiten × Chromium + WebKit × 1440×900, 1000×800 (Roberts Safari), 390×844 = 60 Läufe | 0 Konsolenfehler, 0 fehlende Dateien |
| Durchscrollen, hängende Auftritte | gleiche 60 Läufe, nach dem Durchscrollen | 0 `.auf` ohne Auslöser, nichts unsichtbar hängen geblieben (Ausnahme gewollt: auf «Alle Abende» blendet der Hero-Text beim Scrollen aus, das «Mehr»-Schild erscheint nur beim Überfahren) |
| Seitliches Verrutschen | 10 Seiten × 2 Engines × 1440, 1000, 390, 360, 320, beim Laden **und** bei jedem Scrollschritt | vorher 7 Seiten × Breiten betroffen, jetzt 0 |
| Bilder kaputt / zu gross gezogen | 760 Bilder (Chromium, Retina-Dichte) | 0 kaputt, 0 über 80 % ihrer Auflösung |
| Geladene Datei passt zur Anzeige (`sizes`) | 760 Bilder, 1440 und 1000 @2x | vorher 17 Stellen unter 1,5-facher Dichte, jetzt 5 Grenzfälle, alle ≥ 1,29 (innerhalb der 80-%-Regel) |
| Filme | 3 Filme (Startseite 2, Dirty Chicken 1) | spielen im Bild, Chromium + WebKit |
| Bedienung | Chromium + WebKit × 1440 + 390 | 4 × 35 Schritte grün (Liste unten) |
| Links und Anker | 126 interne Verweise, 7 externe | 1 toter Link (offen, siehe unten) |
| Flüssigkeit (Regel 55) | Chromium 1440, CPU 4× und 6× gedrosselt, ganze Seite gescrollt | 4×: 107–118 B/s, 6×: 84–117 B/s (Tabelle unten) |
| Auftakt ohne Skript / langsame Leitung | 7 Seiten | ohne JavaScript alles sichtbar; Ausfall des Seitenskripts jetzt abgefangen |
| Fremde Hausangaben | Text aller 10 Seiten | keine (Beau-Rivage, Interlaken, Schäfli usw.: 0 Treffer) |

## Repariert

Vor jeder Änderung gesichert (`*.vor-pruefung-2026-10-28`: `bau.py`, `varianten.py`, `assets/culinarium.css`, `assets/culinarium.js`), Datei direkt vor dem Schreiben neu gelesen, nur die eigene Stelle per Ersetzen mit Prüfung geändert, `VERSION` in `bau.py` erhöht, mit `python3 website/bau.py` neu gebaut. Keine Bildpfade in `BILD` angefasst.

### 1 · Dirty Chicken am Handy 461 statt 390 px breit (Chromium/Android)
Die Überschrift «Das erste Pop-up.» liess Chromium das einspaltige Raster `.pp15` auf 440 px Mindestbreite rechnen (WebKit: 354 px). Folge: Android-Chrome verkleinert die ganze Seite, rechts ist Text abgeschnitten («im Tied…»).
Reparatur: `@media (max-width:860px){.pp15{grid-template-columns:minmax(0,1fr)}}` in `culinarium.css`. Chromium rechnet jetzt wie Safari.
Bild: `f1-dirty-chicken-390-vergleich.jpg` · gemessen vorher 461/390 px, nachher 390/390.

### 2 · Team-Seite verrutscht beim Laden (Handy 462 px, 1000er-Fenster 1046 px)
Das Bildpaar im Zickzack (`.zz-bilder`) startet seinen Auftritt 90 px nach rechts versetzt und schob die Seite bis zum Auslösen breiter, in beiden Engines.
Reparatur: `.v-lt-koepfe{overflow-x:clip}` (der Abschnitt ist immer bildschirmbreit, der Auftritt sieht gleich aus).
Bild: `f2-leute-390-beim-laden-vergleich.jpg` · vorher 462/390, nachher 390/390. (Hinweis kam zuerst von der Lernauswertung, hier nachgemessen.)

### 3 · Fuss auf 320 und 360 px auf allen Seiten zu breit
In der rechten Fuss-Spalte passten «Sandwiches & More» (`white-space:nowrap`) und «@dirtychicken.hannover» nicht in 133 bzw. 153 px.
Reparatur nur unter 380 px: `dd` darf umbrechen, der Instagram-Name bricht nach dem Punkt um (`@dirtychicken.<span class="fu-u"></span>hannover` in `bau.py`, Umbruchstelle per CSS nur ≤ 380 px), Zeilenhöhe 1,25. Ab 390 px unverändert.
Bild: `f3-fuss-320-vergleich.jpg` · vorher 341/320, nachher 320/320.

### 4 · Startseite 320 px: Zeile «Bar: Donnerstag bis Samstag ab 19 Uhr» ragt 15 px hinaus
`varianten.py` setzt in Info-Zeilen jedes Leerzeichen geschützt; diese Zeile ist so 317 px breit und unteilbar.
Reparatur: nach dem Doppelpunkt eines Etiketts bleibt ein normales Leerzeichen (`replace(':&#160;', ': ', 1)`), betrifft nur diese eine Zeile; bricht nur auf 320 px nach «Bar:» um.
Bild: `f4-start-ueberleitung-320-vergleich.jpg`.

### 5 · Startseite 390 px: Aufkleber ragt 1–2 px über den Rand
Der gedrehte Stern-Aufkleber (`.mit-stk .stk-stern`) im Dirty-Chicken-Abschnitt stand 1–2 px über dem Rand (Seite 391/392 px).
Reparatur: `.v-dirty-chicken{overflow-x:clip}`. Bild: `f5-start-aufkleber-390-vergleich.jpg`.

### 6 · Warteliste im Fuss verliert auf «Der Abend» die E-Mail
Auf jeder anderen Seite funktioniert «Vormerken» (E-Mail wird mitgenommen). Auf `abend.html` selbst springt der Knopf nur zum Anker, die Seite lädt nicht neu, die E-Mail kam nie im Formular an.
Reparatur in `culinarium.js`: Ist das Formular schon auf der Seite, wird die E-Mail direkt eingetragen und hingesprungen.
Beleg: Bedienungstest «Fuss-Warteliste von abend» vorher ROT (`wert:""`), nachher grün in Chromium + WebKit, 1440 + 390.

### 7 · Zu kleine Bilddateien auf Retina (`sizes` passte nicht zur Anzeige)
| Stelle | Anzeige 1440 | `sizes` vorher → nachher | geladen vorher → nachher |
|---|---|---|---|
| Startseite, Laufband, Paarbilder | 558 px | 20vw → 40vw | 640er (1,15×) → 1600er |
| Startseite, Laufband, Querbild / Hochbild | 806 / 496 px | 46vw / 28vw → 57vw / 35vw | → 1600er |
| Dirty Chicken, Bildsäulen im Hero | 354 × 443 (cover) | 18vw → 30vw | 640er (0,96–1,44×) → 1000er |
| Dirty Chicken, Hochkant-Rahmen | 440 × 688 (cover) | 32vw → 60vw | 640er bei 1000 px (1,16×) → 1600er |
| Dirty Chicken, Seitenbilder neben dem Film (`nx15-seite`) | 419 × 666 (cover) | 22vw → 46vw | 640er in WebKit (0,96×) → 1000er |
In `varianten.py` und `dc_nacht.py` (Sicherung `dc_nacht.py.vor-pruefung-2026-10-28`), keine Bildpfade. Endstand: in Chromium und WebKit kein Bild mehr unter 1,25-facher Dichte, also überall innerhalb der 80-%-Regel. (Hinweis zu Teilen auch vom Bilder-Chat.)

### 8 · Auftakt bleibt unsichtbar, wenn das Seitenskript ausfällt (Master 9)
Lädt `culinarium.js` nicht (Netzabbruch, Fehler), blieben alle Titel und Sätze im Schlitz versteckt, auf jeder Seite, für immer.
Reparatur im Kopf-Skript (`bau.py`): Ist das Seitenskript bis `DOMContentLoaded` nicht gelaufen, wird die Klasse `js` entfernt und alles steht. Im Normalbetrieb greift das nie (gegengeprüft: `html.js` bleibt, Auftritte laufen).
Bild: `ohne-seitenskript-index.jpg` (Seitenskript abgefangen, alles sichtbar).

### 9 · Plakate angeschnitten (Robert 28.10., «komische Cuts an Welten in Bildern», Auftrag Oberchef)
Gemessen wurde jedes Plakatbild aller Seiten (Chromium + WebKit, 1440 / 1000 / 390): Seitenverhältnis Rahmen gegen Datei bei `object-fit:cover`.
- **Startseite «Seit 2023»:** Pop-up-Plakat Mai 2023 im Hochformat-Rahmen. Es fehlten 28 %, rechts war das Datum «20/05/202…» angeschnitten.
- **Team-Seite «Wie es kam»:** Plakate Mai und Herbst 2023 im Querformat-Rahmen. Es fehlten 25 %; die Wortmarke CULINARIUM war unten halb weg, die Unterzeile ganz.
- **Dirty Chicken:** Pop-up-Plakat (Hochformat 9:16) im Querformat-Rahmen. Es fehlten 58 %, «DIRTY DRINKS» war unten abgeschnitten.

Reparatur: `bau.py` bekommt `PLAKAT_GANZ = {'pop23', 'pl23', 'dc_plakat'}`. `foto()` gibt diesen Plakaten die Klasse `plakat-ganz`. In der CSS sitzt das Plakat ganz (`object-fit:contain`) mit Innenrand `clamp(8px,6%,18px)` auf seinem eigenen Papierton `#FAF4F4` (gemessen am Rand der Instagram-Plakate). Rahmen, Raster, Abstände und Bewegung bleiben, wie sie sind. Sicherungen: `bau.py.vor-plakat-ganz-2026-10-28`, `assets/culinarium.css.vor-plakat-ganz-2026-10-28`. Version 26189.

Prüfung nachher:
- Kein Plakatbild verliert mehr als 2 % (Chromium + WebKit, alle drei Breiten).
- Jede Aufnahme ist selbst angesehen, auch vergrössert. Die Wortmarke steht ganz, und das «2023»-Schild auf der Startseite liegt nur auf dem Papierrand.
- Startseite, Team-Seite und Dirty Chicken zeigen in beiden Engines 0 Konsolenfehler und kein Verrutschen.

Bilder: `f9-plakat-*-vergleich.jpg`, `bogen-*.jpg`.

Hinweise:
- Roberts Bild `funde-05` habe ich auf «Alle Abende» nicht gefunden. Die 14 Vitrinen-Plakate dort sind quadratisch und stehen in allen Breiten und beiden Engines ganz, im Abend-Fenster ebenso. Laut `FUNDE.md` stammen die Funde aus den Werkzeugen bzw. der Werkbank; die Karte mit «89,00 EUR · AUSGEBUCHT» über dem Datum kommt vermutlich aus einem Werkzeug.
- Weiter offen (Gestaltung, nicht geändert): Der Hero «Alle Plakate» (Plakatwand) wird am Handy zu 72 % beschnitten. (Knopf und Dirty-Chicken-Plakat: siehe 10 und 11.)

### 10 · «Mehr zum Abend» lag auf der Wortmarke der Plakate (Auftrag Oberchef)
Auf «Alle Abende» stand der Knopf unten auf dem Plakat (`bottom:12px`). Am Handy (ohne Maus) war er immer sichtbar und deckte die Wortmarke CULINARIUM ab, am Rechner beim Überfahren ebenso.
Reparatur: `.vit-mehr` sitzt jetzt 8 px unter dem Plakat (`top:calc(100% + 8px)`), auf der Spiegelfläche. Am Rechner bleibt der Abstand zum Datum 78 px (Chromium + WebKit, 1000). Sicherung `culinarium.css.vor-plakat-zuschnitt-2026-10-28`. Bilder: `f10-*`.

### 11 · Dirty Chicken: Plakatfoto klein im breiten Feld (Auftrag Oberchef)
Neuer Zuschnitt `website/_zuschnitt/dc-plakat-ganz.jpg` (640 × 898) aus `_quelle/dirty-chicken/ig/2026-06-06_dirtychicken.hannover_DZPYEOJIfVb-1.jpg`; das Original ist unverändert. Er zeigt das Plakat ganz, mit allen vier Aufklebern, ohne Pflanzen oben und unten.
- **Einbau:** neuer Bildschlüssel `dc_plakat_ganz` in `bau.py`. `dc_plakat` behält seinen Pfad, weil es an anderen Stellen weiterläuft. Der Zuschnitt wird nur im Bildraster der Dirty-Chicken-Seite verwendet (`dc_nacht.py`).
- **Feld:** Das Plakat füllt die Höhe ganz. Der Rest des Querfelds trägt das Dirty-Chicken-Violett `#8953A9` statt eines hellen Kastens.
- **Grenze:** Ein ganzes Hochformat-Plakat (0,71) kann ein Querfeld (4:3) nur in der Höhe füllen; die volle Breite ginge nur mit Anschnitt.
- Sicherungen `bau.py` / `dc_nacht.py` `.vor-plakat-zuschnitt-2026-10-28`, Version 26190. Bilder: `f11-*`.

Beide in Chromium + WebKit bei 1440 / 1000 / 390 aufgenommen und selbst angesehen; «Alle Abende» und Dirty Chicken ohne Konsolenfehler, ohne Verrutschen.

### 12 · Versandfertig (Robert 28.10.2026 über den Oberchef)
**Hero-Fassungen raus.** `abend_auftakt.py` und `ueberleitung.py` bauen bei fester Wahl (`WAHL = 5` bzw. `1`) nur noch diese eine Fassung: keine Fassung 0, keine 14 versteckten, keine Fassungs-Leiste mit Vorschaubildern. `abend-auftakt.js` und `ueberleitung.js` legen die Fassungen nach ihrer Nummer ab, kommen ohne Leiste aus und laden Nachbarn nur, wenn es sie gibt (bisher hätten sie Fehler geworfen).
- `abend.html`: 133 → 43 KB, 16 → 1 h1.
- `index.html`: 192 → 159 KB.
- Jede echte Seite hat genau ein h1.
- Pixelvergleich vorher/nachher (Auftakt «Der Abend» und Überleitung Startseite, Chromium + WebKit, 1440/1000/390, ruhig und bewegt): 23 von 24 Aufnahmen Byte für Byte gleich. Bei der einen (WebKit 390, bewegt) weichen 55 verstreute Bildpunkte innerhalb eines Fotos ab, also Ladezustand der Bilddatei; zwei Läufe des neuen Baus sind identisch.
- Wahlseiten unverändert.

**ß statt ss** (in den Bau-Quellen, nicht im HTML): angestoßen, anstoßen, stoßen, draußen/Draußen, außen, weiß/weiße/weißem/weißer, Weißwein, hießen, Hühnerfuß, Schließen (Menü-Knopf und Fenster), Straße.
- Die Speisekarten-Zitate («weiße Schokolade», «weißer Port») folgen jetzt dem Original auf Instagram.
- Rudis Versalien (z. B. «WEISSE SCHOKOLADE») bleiben: In Versalien ist SS richtig.
- Bildschlüssel wie `anstossen` und Kommentare sind nicht angefasst.
- Das Impressum enthält noch keine Anbieter-Adresse (Platzhalter), dort war nichts zu ändern.
- Endkontrolle aller zehn Seiten (Text, alt, aria-label): 0 ss-Reste.

**Bar-Knopf.** Auf Anweisung des Oberchefs nicht umgestellt: Die Website ist online, dort führt der Knopf zur Bar-Seite unter /wildside/. Die Zeile in `varianten.py` steht wieder genau wie vorher. `knopf()` in `bau.py` hat einen optionalen vierten Wert `neu` (Standard aus); er wird derzeit nirgends genutzt.

**Prüfung nachher:** 60 Läufe (10 Seiten × Chromium/WebKit × 1440/1000/390) ohne Konsolen- oder Netzfehler, ohne Verrutschen, ohne hängende Auftritte, kein Bild über 80 % seiner Auflösung. Bedienung WebKit 1440 und Chromium 390 je 35/35 grün. Nach dem Zurücknehmen des Bar-Knopfs: bar, abend und index nochmals in beiden Engines grün. Jede echte Seite hat genau ein h1.

Sicherungen `*.vor-versand-2026-10-28`: `bau.py`, `varianten.py`, `abende_info.py`, `abend_auftakt.py`, `buchen.py`, `ueberleitung.py`, `assets/culinarium.js`, `assets/abend-auftakt.js`, `assets/ueberleitung.js`. Version 26191.

### 13 · Reste aus dem Demo-Check (Oberchef 28.10.2026)
- **Chronik, September 2026, in die Vergangenheit:** Startseite «Seit 2023»: «Der Abend war ausgebucht, bevor er begann.» Team-Seite «Wie es kam»: «Der September-Abend war ausgebucht, Dirty Chicken feierte Opening.» Die Einträge 2023–2025 stehen im erzählenden Präsens einer Chronik («Rudi kommt in die Küche») und lesen sich nicht als bevorstehend; sie sind unverändert. Für Robert zum Abwägen: Damit wechselt die Zeitform innerhalb der Chronik.
- **Esc schließt das Handy-Menü**, genau wie der Knopf: Menü zu, Knopf wieder «Menü», Seite scrollt wieder, Fokus zurück auf den Knopf. Geprüft in Chromium + WebKit (390) auf bar, abende und abend.
- Prüfung: Startseite und Team-Seite in Chromium + WebKit bei 1440/1000/390 ohne Fehler und ohne Verrutschen; Bedienung WebKit 390 35/35, Chromium 1440 ohne Konsolenfehler. Sicherungen `*.vor-demo-rest-2026-10-28` (`varianten.py`, `assets/culinarium.js`, `bau.py`). Version 26192.

## Bedienung (je Chromium + WebKit, 1440 und 390, alle grün)

Menü bzw. Leiste auf allen 10 Seiten auf/zu und Weiterleitung · alle 14 Abend-Kacheln auf «Alle Abende» öffnen ihr Fenster, schliessen per Knopf und Escape · «Platz buchen»: leere Felder gemeldet, Anzahl +/−, Summe (3 × 89,00 = 267,00 EUR), Zahlung gespielt bis zum Ticket, Fenster zu, Seite scrollt wieder, nach Neuladen «Noch 6 von 14» · Warteliste auf «Der Abend»: Pflichtfelder, Eintrag mit Bestätigung · Fuss-Warteliste von Impressum und von «Der Abend» · Anker `abend.html#warteliste` landet 40 px unter der Kante · Termine pflegen: anlegen → neu laden → noch da → erscheint auf «Der Abend» → entfernen · 3 Filme spielen · Laufband läuft von selbst · `tel:` abgefangen, nicht ausgeführt · 0 Konsolenfehler.
Kein Formular nutzt `mailto`; Buchung und Warteliste sind Vorschauen und schicken nichts ab (steht so auf der Seite).
Bilder: `bedienen-*.jpg`.

## Flüssigkeit (Chromium 1440 × 900, ganze Seite mit dem Mausrad, Bilder pro Sekunde)

| Seite | 4× | 6× | Bemerkung |
|---|---|---|---|
| Startseite | 107 | 84 | 6×: einzelne Bilder um 42 ms im Bereich Dirty Chicken / Fragen / Bis bald (14 300–15 500 px), max. 124 ms |
| Alle Abende | 118 | 114 | |
| Der Abend | 118 | 113 | |
| Das Haus | 115 | 108 | |
| Team | 117 | 107 | 6×: ein Bild 176 ms beim Übergang Chronik |
| Der Weg | 117 | 116 | |
| Dirty Chicken | 118 | 110 | |
| Termine pflegen | 109 | 116 | |
| Impressum / Datenschutz | 117 | 117 | |
Vergleich Carlton-Europe 15.10.: 118–120 bei 4×. Nichts ruckelt sichtbar; an der Bewegung wurde nichts geändert.

## Offen (nicht geändert, mit Grund)

1. **Knopf «Zur Website der Bar»** (lokal ohne Ziel; online führt er laut Oberchef zu /wildside/) (`bar.html`, Schluss-Fenster; Quelle `varianten.py` `WILDSIDE = '../../Walk%20on%20the%20Wild%20Side%20Hannover/website/'`). Er zeigt auf den Ordner eines anderen Projekts und geht nur, wenn die Seite als Datei geöffnet wird; auf http://localhost:8765/bar.html und online endet er im 404. Ein richtiges Ziel (Adresse der Bar-Website) kann ich nicht erfinden → Oberchef.
2. ~~Startseite ohne Hauptüberschrift~~ → **erledigt** auf Entscheid des Oberchefs (28.10.): unsichtbares `<h1 class="vh">Culinarium</h1>` in `lockup()` von `bau.py` (Sicherung `bau.py.vor-pruefung-h1-2026-10-28`), Version 26188. Startseite hat genau ein h1; erster Schirm mit und ohne h1 Byte für Byte gleich (Chromium + WebKit, 1440 + 390); Durchlauf ohne Fehler, ohne Verrutschen. Der Knopf «Zur Website der Bar» bleibt laut Robert bis zum Online-Stellen so; (c)–(g) bleiben für Roberts Feintuning.
3. **`abend.html` trägt alle 16 Hero-Fassungen** (15 versteckt, 16 `h1`, 7 Bilder geladen ohne Anzeige, Seite 133 KB statt rund 40 KB). Vermutlich gewollt zum Umschalten (`?f=`); vor dem Online-Gehen auf die gewählte Fassung kürzen.
4. **Langsame Leitung**: Bei 1,6 Mbit/s steht der Titel nach 4,3 s («Alle Abende») bis 8,0 s («Dirty Chicken»), weil er auf das Seitenskript am Ende und 231 KB CSS wartet. Master 9 will einen Startschuss im Kopf nach ~700 ms. Das ändert den Zeitpunkt des Auftritts, also Gestaltung → Robert/Oberchef. (Der Ausfall-Fall ist mit Reparatur 8 erledigt.)
5. **Texte** (nicht meine Sache, nur gemeldet): `bar.html` «SESSION mit DJs an den Decks» ist ein Insider-Wort ohne Erklärung; `leute.html` Zitat «Ich bin die Karte.» (Derya, Neue Presse 2024). Die Lernauswertung meldet dazu Roberts Satz vom 26.10. «klingt ultra arrogant». Das habe ich nicht selbst nachgeprüft.
6. **Startseite 6× gedrosselt 84 B/s** im Bereich Dirty Chicken / Fragen / Bis bald: beobachten, kein sichtbares Ruckeln.
7. **Bildstufen in `bau.py` (`STUFEN = 640, 1000, 1600, 2400`)**, Hinweis vom Bilder-Chat: Quellen mit 1440–1599 px bekommen höchstens die 1000er, grosse Vollbilder höchstens die 2400er. Nach der sizes-Reparatur verletzt keine Stelle mehr die 80-%-Regel (gemessen 1440, 1000, 390, beide Engines). Eine Zwischenstufe in Quellbreite bzw. eine 2880er-Stufe wäre schärfer, aber schwerer zu laden. Das ist eine Abwägung → Oberchef, nicht geändert.
8. **Feintuning für Robert** (Gestaltung, nur aufgelistet): Das Handy-Menü hat keinen Eintrag «Warteliste», die Leiste am Rechner schon.
9. **Zählung (Le Registre)**: `messung.js` absichtlich nicht eingebaut (Wunsch des Registre-Chats, 8765 nimmt kein POST an). Klassen `.wt-form`, `.fu-wl-f`, `[data-buchen]`, `#tb-dialog` habe ich nicht umbenannt.
10. **Kette**: «läuft» liess sich am Anfang nicht setzen (Station 08 wartete auf Roberts Bestätigung, `--trotzdem` nicht benutzt); am Ende wurde «liegt vor» angenommen.

## Lernen (an Oberchef und Lernauswertung gemeldet, gilt für alle Häuser)

1. Seitliches Verrutschen **beim Laden und auf 320/360 px** messen, nicht nur nach dem Durchscrollen auf 390. Auftritte mit seitlichem Startversatz verbreitern die Handyseite, bis sie auslösen.
2. In Rastern `minmax(0,1fr)` statt `1fr`. Chromium und WebKit rechnen die Mindestbreite verschieden (hier 440 gegen 354 px).
3. `sizes` an der echten Rahmenbreite messen. Bei `object-fit:cover` in Hochkant-Rahmen zählt die Höhe mit, sonst lädt Retina Dateien in halber Breite.
4. Ein Formular, das auf die eigene Seite springt, lädt nicht neu: Werte direkt eintragen statt über `sessionStorage`.
5. Auftritte brauchen einen Rückfall, falls das Seitenskript ausfällt (Kopf-Skript nimmt `js` zurück).

## Dateien

- Prüfskripte: `_qa/pruefung-2810/pruefen.js` (Laden/Scrollen/Bilder), `rand-lauf.js` (Verrutschen), `bedienen.js`, `fluss.js`, `fluss-stelle.js`, `auftakt.js`, `ohne-skript.js`, `netz.js`, `fundbilder.js`
- Rohdaten: `roh-chromium.json`, `roh-webkit.json`, `schluss-*.txt`, `fluss.txt`, `schaerfe.txt`, `bedienen-*.json`
- Seitenbilder je Engine: `_qa/pruefung-2810/roh/<engine>/<seite>-<breite>-oben.jpg` und `-ganz.jpg`
