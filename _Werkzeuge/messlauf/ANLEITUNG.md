# Messlauf · Pflicht vor jeder Übergabe an Robert

Seit 29.10.2026 (Oberchef): Robert fand selbst eine Kachel «PREISLISTE», deren Wort am Rand klebt, einen ovalen Haus-Knopf, zwei Navigationspunkte auf dieselbe Seite und Plakate, deren Wortmarke unten abgeschnitten war. Der Messlauf findet so etwas, bevor Robert es sieht.

## Ein Befehl

```bash
~/Desktop/Website-Projekte/_Werkzeuge/messlauf/messlauf.sh culinarium
```

Ergebnis: `_Oberchef/zeigen/<haus>/messlauf-<TTMM>/lauf-<HHMM>/tafel.html` (über `http://localhost:8978/haus/_Oberchef/zeigen/…` öffnen), dazu `funde.json` und `bilder/` (ein Ausschnitt je Fund, rot umrandet).

Schneller, nur ein Teil: `messlauf.sh culinarium "" --nur schaufenster,markenbuch --browser webkit --groesse 390`.
Vergleich zweier Läufe: `python3 tafel.py <lauf-vorher> <lauf-nachher> <ziel.html> [offen.json]`.

## Was er tut

- Liest die Ziele aus `ziele-<haus>.json` (Werkzeug, Unterseiten, Werkbank mit Beigaben). Neues Haus: Datei kopieren, Adressen tauschen.
- Je Browser (Chromium, WebKit) und Grösse (1440 × 900, 1280 × 800, 390 × 844): Start, jeder Navigationspunkt (frisch geladen), in jeder Ansicht Reiter, Menüs, «Neu …», Dialoge, Auswahl (höchstens 14 je Ansicht, jede Schaltfläche nur einmal je Werkzeug), der Rundgang Schritt für Schritt, auf dem Handy das Menü.
- Nie gedrückt: Löschen, Senden, Veröffentlichen, Hochladen, Speichern, Übernehmen, Bestätigen, Bezahlen, Drucken, KI fragen. Schreibwege (POST/PUT/DELETE) beantwortet der Messlauf selbst, nichts kommt beim Server an. mailto/tel abgefangen, neue Fenster geschlossen.
- Vor dem Messen: Seite einmal durchrollen, Bewegungen abwarten.

## Die Regeln (messen.js)

| Art | Fund, wenn … |
|---|---|
| ueberlauf | Text breiter/höher als sein abschneidender Kasten, oder Text ragt sichtbar aus Knopf/Kachel |
| rand | Text in Knopf oder Kachel (≤ 420 × 320 px, mit Fläche) näher als 6 px am linken oder rechten Rand |
| wort | Wort ohne Trennstrich mitten im Wort umgebrochen |
| oval | Knopf nur mit Symbol, oder runder Knauf in einem Knopf: Breite ≠ Höhe um mehr als 1 px |
| reihe | Gleich breite Kacheln derselben Klasse in einer Reihe: Oberkante, Höhe, Titelgrösse oder Titel-Grundlinie (erste und letzte Zeile) ungleich |
| ueberlappt | Zwei Text- oder Knopf-Zeilen überdecken sich sichtbar (gefächerte, gedrehte Elemente und enger Zeilenabstand ausgenommen) |
| anschnitt | Seite verrutscht seitlich, oder Element vom Bildschirmrand angeschnitten (ausser in seitlich scrollenden Leisten) |
| doppelt | Zwei Navigationspunkte zeigen ≥ 80 % dieselben Titel, Kacheln und Bilder, oder führen auf dieselbe Adresse (Zeichen oben und Sprungmarken ausgenommen) |
| gemischt | Navigationspunkt «Fotos/Bilder» zeigt Plakate, oder «Plakate» zeigt Fotos |
| beschnitten | Plakat, Motiv, Vorlage oder Wortmarke im Bild (Dateiname pl_/plakat/poster/motiv/vorlage/wortmarke/logo, Bildbeschreibung mit «Plakat») mit object-fit cover in einem Kasten, dessen Seitenverhältnis um mehr als 2 % abweicht: die Schrift im Bild wird abgeschnitten. Behebung: Kasten aufs Seitenverhältnis des Plakats, oder contain auf der Motivfarbe |
| einzelwort | Titel (3+ Wörter, höchstens 3 Zeilen), dessen letzte Zeile nur ein Wort ist (z. B. «2026» allein). Behebung: text-wrap:balance |
| text-mitte | Schrift in Knopf, Pille, Etikett (Fläche, höchstens 80 px hoch) sitzt nicht optisch mittig: Mitte der Versalhöhe (bzw. x-Höhe bei reiner Kleinschrift, gemessen mit canvas measureText) weicht senkrecht mehr als 0,5 px von der Mitte des Kastens ab, bei zentrierten Knöpfen auch waagrecht; Symbol allein im Rundknopf: Mitte der gezeichneten Form. Unterlängen und Akzente zählen nicht. Behebung zentral im Kleid: text-box: trim-both cap alphabetic (Versalien) bzw. ex alphabetic, line-height:1, Höhe über Padding, gemessener Ausgleich ohne text-box (Robert 29.10.2026) |
| zier-x | «x» oder «×» als Zier- oder Trennzeichen: im ::before/::after, allein stehend oder zwischen zwei Wörtern. Erlaubt nur in Namen («Momo x Rudi», auch MOMO X RUDI) und als Schliessen-Knopf. Behebung: als Trenner ein kleiner Punkt oder «·» auf der optischen Mitte, als Schmuck ersatzlos oder ein feiner Strich (Kriterium 24, Robert 29.10.2026) |
| gekuerzt | Hinweis, kein Fehler: Text mit … oder Zeilenbegrenzung gekürzt, Eingabe länger als ihr Feld |

Fehlalarm gefunden? Regel in `messen.js` schärfen, nicht den Fund wegerklären. Jede Änderung hier unten eintragen.

## Änderungen

| Datum | Was |
|---|---|
| 29.10.2026 | Angelegt (Querprüfungs-Chat): Regeln ueberlauf … anschnitt, doppelt, gemischt; dazu beschnitten und einzelwort (Oberchef: Plakate im Schaufenster «Alle Abende» unten abgeschnitten, «2026» allein in der zweiten Zeile) |
| 29.10.2026 | Regel zier-x (Kriterium 24, Robert: kein «x» als Zier- oder Trennzeichen; erlaubt in Namen, Massen, Schliessen-Knopf) |
| 29.10.2026 | Regel text-mitte (Robert: «Die Schriften in deinen Buttons sitzen IMMER falsch»): Versalhöhe/x-Höhe per measureText gegen Kastenmitte, 0,5 px; waagrecht nur bei zentrierten Knöpfen (Flex: justify-content center) |
| 29.10.2026 | Geschärft nach Fehlalarmen: Foto-Vorschauen sind keine Symbol-Knöpfe; Listeneinträge, Menü-Schalter, Sprungmarken und Zeichen oben zählen nicht als Navigation; rollende Ziffern (1–2 Zeichen) sind kein Überlauf; Fenster/Overlays über dem Inhalt sind keine Überschneidung; Text hinter «…» zählt nicht; Fotos einer Plakatwand sind keine Plakate; Reihen ohne laufende Bewegung (offsetTop) |
| 30.10.2026 | text-mitte geschärft: versteckter Text (clip-Muster für Vorleser, Fläche unter 2 px) zählt nicht («Neu» am Handy in der Werkstatt); steht das Zeichen über der Beschriftung (flex-direction column), wird die Gruppe aus gezeichnetem Zeichen und Schrift gemessen (Mail-Kacheln «Titel», «Foto»). Beleg: `tm_vergleich.js` alt gegen neu auf denselben Seiten |
| 30.10.2026 | einzelwort geschärft: ausgewogen umbrochene Titel (letzte Zeile mindestens 60 % der längsten, z. B. «In den Hausregeln / nachschlagen.») sind kein Einzelwort; «2026» allein unter einer langen Zeile bleibt ein Fund |
| 30.10.2026 | Durchrollen liest die Seitenhöhe bei jedem Schritt neu (nachgeladene Bilder verlängern die Seite; sonst standen Titel ganz unten noch in ihrer Startlage und galten als «überdeckt»). Umschalter mit aria-pressed in einer Gruppe (z. B. «Einfach»/«Frei») sind keine Navigation |
| 30.10.2026 | `nur_regel.js` nimmt mehrere Arten (`ML_ART=text-mitte,oval`); `tafel.py` zeigt text-mitte und zier-x |
| 30.10.2026 | Grösse 1000 × 650 (Roberts Fenster) wählbar: `--groesse 1000`; ohne Schalter bleibt 1440,1280,390 |
| 30.10.2026 | zier-x erweitert (Robert: «das X hat auf der ganzen Seite nichts zu suchen»): gedrehtes «+» (CSS transform/rotate, auch in ::before/::after und über Eltern), zwei gekreuzte Balken in ::before/::after, gezeichnetes × im SVG (zwei Diagonalen, die sich mittig kreuzen; nur Zeichen bis 96 px mit höchstens acht Strichen). Erlaubt: Namen («Momo x …»), Masse, Schliessen-Knöpfe, Auf/Zu-Knöpfe (aria-expanded), unsichtbare Zustände (opacity 0), «+» an Zählern, Pfeile und Haken. Beleg: das alte Fuss-× (Sicherung culinarium.css.vor-punkt-2026-10-30) hat die alte Regel übersehen, die neue findet es in Chromium und WebKit; Website live danach 0 |
| 30.10.2026 | rand und ueberlauf: Text für Vorleser (clip-Muster, Fläche unter 2 px) zählt nicht («Website ansehen» bei 1000 px meldete «0 px vom linken Rand») |
| 30.10.2026 | wort: nur ein Bruch zwischen zwei Buchstaben desselben Wortes ist ein Fund (Zeichen für Zeichen geprüft); Umbruch am Bindestrich («3-Gänge-/Menü») ist erlaubt |

## Nur eine Regel messen (schnell)

`ML_ART=text-mitte node nur_regel.js <adressen.txt> [ausgabe.json]` (eine Adresse je Zeile; ML_BROWSER, ML_GROESSE wählbar). Ebenso für `zier-x`, `beschnitten`, `einzelwort` …

## Speicher (30.10.2026, cu-messlauf, Anlass: WebKit-Absturz auf der Werkbank, cu-werkbank)
- `messen.js` hält je Element ein Stil-Objekt (Map) statt bei jedem Aufruf ein neues anzulegen.
- Abschnitt 4 «Überschneidungen» prüft nur noch Paare, deren Kästen sich überhaupt schneiden (nach Oberkante sortiert), in derselben Reihenfolge wie vorher; `ebene()` je Element gemerkt.
- Gleiche Funde auf Werkbank, Markenbuch, Besucherliste, Tresen, Plakatwerkstatt, Pairing-Karte, Website (1440 + 390). Werkbank-Startseite 1280: eine Messung 2,8 s / +430 MB → 0,1 s / +57 MB; 20 Messungen hintereinander 145–223 MB, kein Absturz. Sicherung `messen.js.vor-speicher-2026-10-30`.

## Zeichen aus ::before/::after (30.10.2026, cu-messlauf, Auftrag Oberchef)
- Neu in `messen.js` (Abschnitt 4b): Ein Zeichen aus `::before`/`::after` mit sichtbarem Text, das absolut gesetzt ist, wird ein eigener Kasten. Gemessen wird die Tinte des Zeichens (canvas measureText), nicht der Zeilenkasten.
- Überschneidungen (K5, `ueberlappt`): Das Zeichen wird gegen jeden Text geprüft, auch gegen den Text des eigenen Elements. Ausgenommen ist nur der Knopf, in dem es steht. Fund: `sel` endet auf `::before`/`::after`.
- Rand (`rand`): Ein Zeichen in Knopf oder Kachel folgt derselben 6-px-Regel wie Text.
- Zeichen im Textfluss (nicht absolut) überdecken nichts und werden nicht geprüft. Ebenfalls nicht geprüft wird eine Kopie des eigenen Wortes als Leuchten oder Schatten (Neon auf der Bar-Seite, `content: attr(data-t) / ""`), die liegt gewollt deckungsgleich. Gelesen wird nur der Text vor einem Alternativtext.
- Beleg: Im Gästebuch («Das wurde gefragt») mit dem alten Fehler (Polster links 0) schlägt die Regel an: «« ⟷ Was ist Fatwashing?». Mit Polster 0 Funde. Tresen 0. Website Deutsch und Englisch, 9 Seiten je Sprache, 1440 und 390: aus der neuen Regel 0 Funde (die übrigen Funde wie vorher). Sicherung `messen.js.vor-pseudo-2026-10-30`.
