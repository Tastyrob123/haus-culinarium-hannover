# Online-Demos der Werkzeuge (ohne Server)

Robert 1.11.2026: «Das sind alles Demos, die online laufen, keinen Impact auf die echte Seite haben und dazu dienen, dass der Kunde das Erlebnis hat … der Kunde soll erstmal die Versionen bekommen, die online MIT dem Werkbank-Link laufen und ihm erstmal Dummy-Werte anzeigen.»

Weg (in der Cloud, ohne Vercel):
1. **Aufnehmen:** Server des Hauses laufen (`bash cloud/server.sh`). Je Werkzeug-Port einen Aufnahme-Proxy starten:
   `python3 cloud/demo/proxy.py <proxyport> <werkzeugport> <aufnahme-ordner>`
   Dann die Zielliste mit den Proxy-Ports kopieren (`sed 's/:92\([0-9][0-9]\)/:93\1/g'`) und je Werkzeug `tor-schnell.js … --nur <k> --max 40 --tiefe 2 --breiten 1440` laufen lassen. Jede Anfrage samt Antwort landet im Aufnahme-Ordner.
2. **Bauen:** `python3 cloud/demo/bau.py <aufnahme> _werkzeuge/<werkzeug>/index.html <ausgabe> [links.json] "<hausordner>/_werkzeuge/<werkzeug>=_werkzeuge/<werkzeug>,<hausordner>/_werkzeuge/oberflaeche=assets/oberflaeche"`
   Ergebnis: statischer Ordner mit `index.html` (leitet zum Werkzeug), `_demo/karte.js` (aufgenommene Antworten), `_demo/shim.js` (Weiche: beantwortet Server-Anfragen mit den Beispielwerten, Speichern/Veröffentlichen sagen «geklappt», ändern nichts; Wege mit «/» vorn werden auf den Demo-Ordner gebogen; Band «Demo mit Beispielwerten»).
   `links.json` = {"9281": "<Adresse der Tresen-Demo>", …}: Verweise zwischen den Werkzeugen und aus der Werkbank.
3. **Prüfen:** Ordner unter einem Unterweg bereitstellen (`python3 -m http.server 9500` im Elternordner, Adresse mit `127.0.0.2`, nicht 127.0.0.1) und `node cloud/demo/test.js http://127.0.0.2:9500/<weg>/index.html bild.jpg` – Bild ansehen, fehlende Dateien nachziehen.
   Culinarium (1.11.): `DEMO_NACHZIEHEN="assets/schrift/=<haus>/website/assets/schrift/,assets/oberflaeche/=<haus>/_werkzeuge/oberflaeche/,_werkzeuge/carte/api/assets/=<haus>/website/assets/"` holt Dateien nach, die der Server mit 403/404 beantwortet hat. Vor der Aufnahme beim Schaufenster die Probe-Kopie anlegen (`python3 _Werkzeuge/werkzeuge/website/probe.py <haus>`), sonst nimmt es nur «Kopie fehlt» auf. Fehlt der Browser-Download, `/Users/robertreff/Aussen-Pruefung/node_modules/playwright(-core)` auf `/opt/node-tools/node_modules/…` verlinken.
   Weiche: schickt Seiten der Website an `links.json → "website"` (öffentliche Website, neues Fenster). Dateien mit Schlüssel/Passwort im Namen nimmt bau.py nie mit.
4. **Werkbank:** `node cloud/demo/werkbank-wege.js wege.json` (alle Seiten bei 1440 und 390, jeder Weg), dann `python3 cloud/demo/werkbank.py <haus>/website/_werkbank wege.json <ausgabe> links.json` (gleiche Dateien nur einmal, eine Bildgröße je Reihe, Werkzeug-Links → Demo-Adressen; höchstens 511 Dateien).
5. **Online:** je Werkzeug ein Artifact (claude.ai, höchstens 511 Dateien / 256 MB, je Veröffentlichung 255 Dateien, Datei ≤ 15 MB), danach die Werkbank mit `links.json` neu bauen, damit «Bedienen» die Demos öffnet.

## Gelernt beim Hochladen (Wild Side, 1.11.2026)
- Oberste Ordner mit «_» sind im Artifact reserviert: bau.py macht aus «_werkzeuge» → «uwerkzeuge» (Weiche findet beides).
- Antworten mit JSON auf Wegen mit «.html» (Schaufenster: api/x/website/seite/…) sind Daten, keine Seiten (bau.py legt sie unter demo/d/ ab).
- Website-Vorschau im Schaufenster kommt per iframe srcdoc: die Weiche biegt auch srcdoc-Wege um; Bilder der Vorschau aus den aufgenommenen Seiten nachziehen.
- Dateien mit ESC-Bytes oder U+FFFD (pdf-lib, fontkit) nimmt das Artifact nicht: in druck.js auf cdnjs/jsdelivr umstellen (pdf-lib 1.17.1, @pdf-lib/fontkit 1.1.1) und die lokalen Dateien weglassen.
- Dateien ohne Endung und .ase weglassen. Je Veröffentlichung ≤ 255 Dateien, dann mit `url` und neuem Paket nachladen.
