---
tags: [projekt, website]
status: aktiv
---

# Baustein: Warteliste der Website → Eingang von La Réception · Culinarium Hannover

Gebaut am 28.10.2026 vom Chat `culinarium-reception` (Werkzeug Gäste-Chat-Team), Muster: Baustein des Gastgebers der Taverne zum Schäfli. Auf der Website ist **nichts** eingebaut; das macht der Website-Chat (Revier `website/`), sobald der Oberchef es freigibt.

## Was er tut

- Die Website hat ein Formular für das Team: die Warteliste «Dein Platz an der Tafel.» auf `abend.html` (`form.wt-form`: Tag Freitag/Samstag/egal, Plätze 1 bis 6, Name, E-Mail). Heute löst sich nur der Abriss «Vorgemerkt», nichts geht weg («Diese Vorschau verschickt noch nichts.»).
- Mit dem Baustein geht jeder Eintrag in den Eingang von La Réception (Art «Warteliste», Abteilung «Warteliste», Tag, Plätze, Name, E-Mail, Seite). Erst wenn La Réception ihn angenommen hat, löst sich der Abriss wie bisher; der kleine Satz darunter heisst dann «Dein Eintrag liegt beim Team.».
- Kommt der Eintrag nicht an: Meldung unter dem Ticket mit Telefon der Bar und Instagram, die Eingaben bleiben. Nie `mailto:`, nie ein Mailprogramm.
- `culinarium.js` der Website bleibt unverändert: der Baustein fängt das Abschicken im Fang-Durchlauf am Dokument ab und gibt es nach der Annahme an die Website weiter.
- Unberührt: «Vormerken» im Fuss (schickt nichts, trägt nur die E-Mail auf Der Abend ein) und «Platz buchen» (gespielte Zahlung, `buchen.js`).

## Einbauen (Website-Chat, über `bau.py`)

1. `_werkzeuge/reception/baustein/anfrage.js` nach `website/assets/anfrage.js` kopieren.
2. In `bau.py` auf `abend.html` **nach** `culinarium.js` einhängen: `<script src="assets/anfrage.js?v={VERSION}" defer></script>`.
3. Ziel der Anfragen: auf dem Server von La Réception (:9084) gilt der Standard `/_werkzeuge/reception/api/formular`. Läuft die Website auf :8765, braucht es `data-api` mit voller Adresse **und** eine Weiterleitung, weil La Réception nur Aufrufe von der eigenen Seite annimmt (Herkunft 403). Vorschlag wie im Schäfli: der Website-Server reicht `POST /_werkzeuge/reception/api/formular` an `http://127.0.0.1:9084` weiter.
4. Datenschutz: der Satz zur Warteliste auf `datenschutz.html` («wird erst gespeichert, wenn der Ticketweg steht») muss dann sagen, wo der Eintrag liegt (La Réception, zwölf Monate, Löschung auf Wunsch). Vorschlag: «Was du in die Warteliste einträgst (Name, E-Mail, Tag, Plätze), liegt beim Team von Culinarium und wird nach zwölf Monaten gelöscht, auf Wunsch sofort.» Vom Haus zu prüfen.

## Geprüft

`pruefung/culinarium.js` öffnet `abend.html` auf dem Prüfserver mit dem Baustein (in die Seite gesetzt, nicht in die Website geschrieben), trägt Name, E-Mail, Tag und Plätze ein, schickt ab und sieht nach, dass der Eintrag im Eingang liegt (auch mit `<script>` und Emoji im Namen, entschärft) und der Abriss sich löst; ohne Verbindung steht die Meldung mit Telefon der Bar, die Eingaben bleiben.
