# Auftrag: Website für Culinarium Hannover

Du baust für mich (Robert, Tasty Studios) die erste Website von **Culinarium**: einer Reihe von Food-Pairing-Abenden in der Bar Walk on the Wild Side in Hannover-Linden. Rudi Napieraj kocht ein 3-Gänge-Menü (nicht mehr rein vegetarisch, Rudi 26.10.2026), Momo mixt zu jedem Gang einen Signature Drink und erklärt ihn persönlich, mit Techniken wie Fatwashing, Milkwashing und Klärung durch Enzyme. Vierzehn Plätze an einer langen Tafel, je ein Freitag und Samstag, ausgebucht bei der Ankündigung. Heute gibt es nur Instagram. Das ist ein **Auftrag** (Robert 25.10.2026), keine ungefragte Studie: Rudi ist Kunde des Backoffice und kennt mich persönlich. Die Seite soll sich so anfühlen wie meine Rivage- und Carlton-Seiten, dasselbe Niveau, aber eine eigene Welt mit eigenem Aufbau. Arbeite Stück für Stück in der Reihenfolge unten und bau erst, wenn das Konzept steht. In der Kette folgen auf diese Sammlung Analyse (04), Markenbuch (05) und Konzept-Board (06); was dort entschieden ist, geht diesem Prompt vor.

## 1 Zuerst lesen (vollständig, bevor du irgendetwas entwirfst)

1. Die Projektdatei im Vault: `~/SecondBrain/02 Projekte/Culinarium Hannover — Website.md`. Sie geht allem vor; nichts dort Entschiedenes neu aufrollen. Dazu `02 Projekte/Rudi-Projekt (Gastronomie).md` (Rudi als Backoffice-Kunde).
2. `~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Kern.md`, danach `Website-Bau — Standards & Ablauf (Master).md` (Abschnitt 2 Gestaltung, 3 Bausteine, 4 Bewegung, 6 Rückmeldung, 10 Abnahme, 13 Kette, Lernprotokoll) und `Tasty-Sprache — Boden und Charakter.md` von Stufe 0 abwärts.
3. `Website-Briefing — Roberts Standard.md`, `00 Kontext/Design-DNA — Vibe & Einflüsse.md`, `00 Kontext/Branding.md`.
4. CLAUDE.md Regel 55 (Flüssigkeit steht über allem), 57 (erst prüfen, dann sagen), 60.
5. Die Pakete der Kette: `_kette/02-spaeher/befund.md` und `einordnung.json`, `_kette/03-sammler/fakten.json` (jede Angabe mit Quelle), `sprachen.json`, und was danach in `04-analyst/`, `05-markenbauer/`, `06-konzepter/` liegt.
6. Das Material: `_quelle/`. Einstieg `Material-Übersicht.md`, `material.html`, `notizen.md`, dann `_quelle/recherche/Kundenprofil.md` ganz (neun Blätter, Checkliste fürs Gespräch, Liste der anzufordernden Dateien). Jeden Bogen in `_boegen/` ansehen, die Beitragstexte in `extern/ig*/beitraege.md` lesen.
7. UI-Fundus, Bereich «Restaurant bauen» (https://tasty-ui-fundus.vercel.app, lokal :8957), Bilder-Atlas (http://localhost:9011), Entwurfs-Maschine (`~/Desktop/Website-Projekte/_Entwurfs-Maschine/`) für die Projekt-Nummer-10-Prüfung.

## 2 Was von den Vorbildern übernommen wird und was nicht

**Übernommen wird das Gefühl und das Handwerk:** dunkle Flächen mit Tiefe im Wechsel mit hellen, ein Muster aus dem Zeichen des Hauses Ton in Ton; Titel, die zeilenweise kommen, Bilder, die von unten heraufschweben; Fenster mit einem stehenden echten Bild; Blatt Papier auf dunklem Grund für Menü und Preis; Knöpfe mit Tiefe und rundem Pfeil-Knauf; Leiste als schmale Insel, Buchen immer erreichbar.

**Nicht übernommen wird:** der Seitenaufbau der Hotels, ihre Auftakte, Farben und Schriften, Zimmer-Bausteine und alles, was ich dort abgelehnt habe. Kein Abschnitt steht nur da, weil ein anderes Haus ihn hat (Master 2.1, «Kein Baukasten»).

**Dieses Haus hat drei Arten von Besuchern, und jede braucht ihren Weg in zwei Sekunden:** wer zum nächsten Abend will (Termin, Menü, Preis, Platz sichern, Warteliste wenn ausgebucht); wer verschenken oder als Gruppe buchen will; und wer wissen will, was «Schulungen, Events, Consulting» heisst. Für die dritte Gruppe gibt es heute nur den Profilnamen: nichts dazuerfinden, Platz lassen, bis Rudi Inhalte liefert.

## 3 Das Haus (aus dem Material gelesen am 25.10.2026, vor Verwendung an der Quelle gegenprüfen)

- **Was es ist:** CULINARIUM, Instagram @culinarium_hannover, Name dort «Food Pairing | Schulungen | Events | Consulting», Bio «CULINARIUM / a unique experience / kreative Drinks & innovative Techniken» (`_qa/spaeher/ig-profil-rechner.txt`). Ort aller Abende: Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover (`_quelle/walk-on-the-wild-side/portale/google-maps.md`). Die Beiträge schreiben «Hasemannstrasse»: nie übernehmen. Kein Rechtsträger, kein Impressum, keine Mail, keine Telefonnummer unter dem Namen (`fakten.json`). Frage an mich: Wer ist Vertragspartner und steht im Impressum?
- **Der Abend** (`_quelle/extern/ig/beitraege.md`, Beitrag DbYnkdkjrNy vom 29.07.2026): 3-Gänge-Menü, damals als vegetarisch angekündigt, laut Rudi am 26.10.2026 nicht mehr rein vegetarisch, «5 von Momos Signature Drinks», Cocktail-Tasting mit Schulung, «Momo wird persönlich jeden Drink für dich erklären». Beginn Freitag 19:00, Samstag 17:00. 89,00 EUR. «nur 14 Plätze pro Abend» (DFqbLG2s_dc, 2025). Rudis Menü-Schreibweise «AUBERGINE / KOKOS / LIMETTE / SESAM» (`extern/ig-team/beitraege.md`). Dezember 2025 gab es ein Menü mit Ente, «auch in Veggie möglich» (`extern/ig-gaeste/beitraege.md`, DSnlBLECGyD): Frage an mich, ob vegetarisch der feste Standard bleibt.
- **Geschichte:** Pop-ups seit 20.05.2023, zuerst «BY MOMO X CHRISTOPH», 15 Plätze, 59 und 80 EUR; seit April 2024 mit Rudi; 69, dann 79, seit März 2026 89 EUR; September 2026 «AUSGEBUCHT!» (`fakten.json › termine`). Kein nächster Termin angekündigt.
- **Buchungsweg heute:** Instagram-Nachricht, dann PayPal; Storno «nicht rückerstattet» seit März 2026 (`fakten.json › buchungsweg`). Welches Ticketsystem kommt, entscheide nicht du: Vergleich in `Kundenprofil.md` Blatt 9.
- **Die Köpfe:** Rudolf «Rudi» Napieraj (Küche), Momo (Drinks, Klarname nicht öffentlich), Derya Ivkin (laut eigener Bio «Bar Owner» der Bar und «Food Pairing»), Sini als Stimme beim Aperitif 2024/25. Keine Bios öffentlich: die Über-uns-Texte entstehen erst aus dem Gespräch.
- **Die Bar:** Falstaff Bar Guide 2027, 91 Punkte als Cocktailbar (an der Quelle, `walk-on-the-wild-side/portale/falstaff-bars-wild-side.md`), Google 4,8 aus 75, eröffnet Ende Oktober 2017 in der ehemaligen Fussballkneipe Linden Journal, lange Tafel auf einer Empore, Möbel aus Kirchenbänken. Die Auszeichnung gehört der Bar, nicht Culinarium: nur mit Freigabe der Bar und so benannt.
- **Wie andere es sehen:** Hannover Prestige ist die einzige Seite ausserhalb von Instagram, die Culinarium nennt (`extern/portale/`); Hannover Eats Reel 12/2025 («Werbung | Einladung»), Luisa Verfürth 04/2024. Kein Eintrag bei Google unter dem Namen; Verwechslungsgefahr mit Culinar Herrenhausen und Culinarium Bad Nenndorf (`extern/verwechslungen/`).

## 4 CI und eigener Charakter

- **Zeichen und Wortmarke:** CULINARIUM in einer breiten 70er-Display-Antiqua mit tropfenförmigen Strichenden, darunter «A UNiQUE EXPERiENCE» in einer Grotesk mit kleinem i; auf den Plakaten doppelt gerahmt mit «BY MOMO X RUDI». Die saubere Logo-Datei ist das Profilbild in 1080 × 1080 (`_quelle/logo/culinarium-profilbild-1080.jpg`); als Vektor nachgezogen aus Profilbild und 2014-px-Plakat, je 4000 px (`_quelle/logo/nachgezogen/`). Das ist ein Nachzug, nicht die Datei des Gestalters; Schriftnamen nur visuell vermutet (Kundenprofil Blatt 5). Das endgültige Zeichen legt Station 05 fest.
- **Farben:** gemessen auf sechs Plakaten Off-White #FAF4F4 und Schiefer-Violett #3A3845, dazu je Abend eine eigene Akzentfarbe (Eisblau, Orange, Grasgrün, Nachtblau, Ochsenblut, Sepia; Kundenprofil Blatt 5). Das sind die Farben der Plakate, belegt als Hausfarben. Zwei Farbwelten legt erst Station 05 vor.
- **Charakter in drei Sätzen:** Zwei Leute an einer langen Tafel in einer Nachbarschaftsbar, einer kocht, einer mixt und erklärt. Jeder Abend hat sein eigenes Plakat, eine Mondfrau, ein Panther mit Eisbecher, ein Kürbis-Pin-up: die Reihe sammelt sich wie Ausgaben eines Magazins. Der Ton ist nahbar, im Du, mit Knappheit, die stimmt.
- **Bildmaterial, ehrlich:** Rudis eigene Dateien sind das Beste: 23 Mail-Anhänge und rund 90 Drive-Bilder, bis 4096 × 3072, dazu ein Film 1920 × 1080 und RAW-Fotos (`_quelle/vom-kunden/`, `drive/`, `drive-arw-vorschau/`): Tafel bei Kerzenlicht, Rudi und Momo bei der Arbeit, jeder Teller, die Drinks, das Team, die Bar von aussen. Wer fotografiert hat, steht nicht dabei. Öffentlich: alle 20 eigenen Instagram-Beiträge seit 2023 und 8 Highlights (`extern/ig/`, `extern/ig-highlights/`, Plakate 1440 px, Mondfrau 2014 × 2003, gedruckte Menükarten 2023), Irina Voronov 05/2024 und 07/2024, focusonbiz 2026, 55 Google-Fotos der Bar bis 4284 × 5712 (`walk-on-the-wild-side/google-maps/`). Gäste und Dritte nur Anschauung. Kein Bild ist schriftlich für die Website freigegeben; Herkunft der Plakat-Illustrationen offen.
- **Denkanstösse, keine Vorgabe:** die Abende als nummerierte Ausgaben mit ihrem Plakat; das Menü in Rudis Schreibweise als Typografie; der Drink, der erklärt wird (Fatwashing, Milkwashing, Klärung) als eigener Moment; die lange Tafel auf der Empore; «ausgebucht» als Zustand, der zur Warteliste führt; die Akzentfarbe des nächsten Abends als Farbe der Seite.

## 5 Bilder, Videos, Texte

- Auf die Seite kommen nur Bilder, deren Rechte Rudi bestätigt hat: zuerst seine eigenen Dateien aus `_quelle/vom-kunden/`, sobald sie dort liegen; dann `extern/ig/`, `extern/ig-team/`, `extern/ig-fotografen/` nur mit Freigabe der Fotografen. Zu jedem verwendeten Bild kennst du Datei und Herkunft (`herkunft.json`).
- Nie verwenden: `extern/ig-gaeste/`, `extern/ig-dritte/`, `walk-on-the-wild-side/ig-dritte/` (Gäste und Dritte), `extern/verwechslungen/`, Bilder der Bar ohne Freigabe der Bar, `extern/wikipedia-commons/` nur mit Namensnennung und nur für die Strasse.
- Fakten, Namen, Preise, Zeiten werden nie abgetippt oder verschönert, sondern aus dem Material gelesen und dagegen geprüft. Tippfehler der Beiträge nicht übernehmen. Was Culinarium nicht veröffentlicht (Schulungen, Events, Consulting im Einzelnen, Gutscheine, Gruppenpreise), steht nicht auf der Seite.
- Texte: Du-Ansprache wie heute, herzlich und knapp, deutsche Schreibung (ß), keine Emojis aus den Beiträgen übernehmen. Deutsch zuerst; weitere Sprachen nach `sprachen.json` erst in Station 15a. Keine Floskeln, keine Punkt-Etiketten, keine Nummern-Listen, keine Pillen-Reihen, nichts, was nach KI klingt (Master 2.3, 2.9).

## 6 Vorgehen, Stück für Stück

1. **Einordnen:** Auftrag, aber bis zu meinem Wort nur lokal, `noindex`. Die Seite kommt in `website/` neben `_quelle/`, eigener freier Port (vorher mit `lsof` prüfen).
2. **Recherche abschliessen** nur, wo etwas Bestimmtes fehlt (Master 1a). Offen sind laut `_kette/03-sammler/stand.json` unter anderem Rudis Dateien, Vertragspartner und Impressum, Bildrechte, das Verhältnis zur Bar, Momos Klarname, der nächste Termin.
3. **Bildauswahl:** aus allen erlaubten Ordnern die besten Bilder je Thema, als Bogen, Lücken benennen.
4. **Konzept-Board** (Station 06): Ideen für genau dieses Haus, Unterschied zu allen bisherigen Häusern je Abschnitt. Erst nach meinem Wort bauen.
5. **Designidentität** (Station 05): Farben, Titelschrift aus der Wortmarke, Zeichen als sauberer Vektor, Knöpfe, Flächen.
6. **Website:** statischer Bau aus einem Skript, reines HTML, CSS, JS, nativer Scroll, Termine, Menü und Preis an einer Stelle (eine Quelle für Seite, PDF und La Carte), Kopf und Fuss einmal. Nur `transform` und `opacity` bewegen.
7. **Nach jedem Abschnitt messen und ansehen:** Safari und Chrome, 320 bis 768 px und Desktop, gedrosselt. Am Handy «Platz sichern» im ersten Bildschirm. Im Konflikt fällt die Idee, nie die Flüssigkeit.
8. **Abnahme** nach Master Abschnitt 10: jeder Knopf geklickt, kein mailto, Formulare gehen nirgends hin, bis ich es sage, Rechtstexte erst mit den Angaben des Vertragspartners.
9. **Am Ende:** Korrekturen ins Lernprotokoll der Master-Datei, Bausteine in den UI-Fundus.

## 7 Wie du mit mir arbeitest

- Antworten im Chat kurz: was ist jetzt da, mit Adresse. Keine Fachbegriffe, keine Arbeitsschritte, keine Bildschirmfotos gebauter Seiten.
- «Mach das geiler» zu einem Abschnitt heisst: nur diesen Abschnitt verfeinern. Nach zwei abgelehnten Neuentwürfen zurück zum Ausgangsstand.
- Fakten des Hauses nie bei mir erfragen: was nicht öffentlich ist, bleibt «offen». Kontakt zu Rudi, Momo, Derya oder der Bar nehme nur ich auf.
- Nichts behaupten, was du nicht selbst geprüft hast. Nichts abschicken, nichts veröffentlichen.

---

**Weitere Häuser:** Die Bar Walk on the Wild Side (`_quelle/walk-on-the-wild-side/`) ist Ort, nicht Familie; ihr Betreiber ist öffentlich nicht belegt. Dirty Chicken Hannover (`_quelle/dirty-chicken/`) ist Rudis zweites Projekt, «Pop up coming soon»; ob es eine eigene Seite oder ein Kapitel bekommt, ist offen.
