#!/usr/bin/env python3
"""Culinarium · Termine buchen, nur als Vorschau (Robert 26.10.2026: Rudi will es als Überraschung, «erstmal dummyhaft simulieren»).
Setzt in abend.html vor die Warteliste einen Abschnitt «Die nächsten Abende» mit Beispielterminen, Platz buchen und gespielter Zahlung,
und baut termine-pflege.html, auf der man Termine einträgt. Alles bleibt im Browser (localStorage), es fliesst kein Geld, nichts geht raus.
Wird am Ende von varianten.py aufgerufen; läuft beliebig oft, ohne sich zu verdoppeln."""
import json, os, re
import bau

HIER = os.path.dirname(os.path.abspath(__file__))
V = bau.VERSION + 'p%d' % max(os.path.getmtime(os.path.join(HIER, 'assets', d)) for d in ('buchen.css', 'buchen.js'))  # neue Fassung lädt sofort, ohne alten Zwischenspeicher
bau.META.update(json.load(open(os.path.join(HIER, 'assets', 'bild', 'meta.json'))))
ANF, END = '<!--buchen-->', '<!--/buchen-->'

ABSCHNITT = ANF + '''<section class="tb" data-ton="nacht" id="termine-buchen" aria-label="Die nächsten Abende">
  <div class="tb-innen">
    <div class="tb-kopf">
      <p class="tb-kicker mono sw auf" style="--i:0">Die nächsten Abende</p>
      <h2 class="tb-titel zl auf" aria-label="Platz buchen."><span class="z"><span style="--i:1">Platz buchen.</span></span></h2>
      <p class="tb-text sw auf" style="--i:2">Such dir deinen Abend aus und zahl direkt. Dein Platz an der Tafel steht, das Ticket kommt per Mail.</p>
      <p class="tb-hinweis mono sw auf" style="--i:3">Vorschau · Termine und Zahlung sind nur simuliert</p>
    </div>
    <div class="tb-liste" data-termine></div>
  </div>
</section>
<div class="tb-dialog" id="tb-dialog" hidden role="dialog" aria-modal="true" aria-labelledby="tb-d-titel">
  <div class="tb-d-grund" data-zu></div>
  <div class="tb-d-karte">
    <button class="tb-d-zu" type="button" data-zu aria-label="Schließen"></button>
    <div class="tb-d-schritt" data-schritt="1">
      <p class="tb-kicker mono sw" style="--i:0" data-d-wann></p>
      <h3 class="tb-d-titel zl" id="tb-d-titel" aria-label="Dein Platz an der Tafel."><span class="z"><span style="--i:1">Dein Platz</span></span><span class="z"><span style="--i:2">an der Tafel.</span></span></h3>
      <div class="tb-d-feld sw" style="--i:3"><span class="tb-d-label">Wie viele Plätze?</span>
        <div class="tb-zaehler"><button type="button" data-plus="-1" aria-label="Weniger"></button><output data-anzahl>2</output><button type="button" data-plus="1" aria-label="Mehr"></button></div>
        <p class="tb-d-frei mono" data-d-frei></p></div>
      <div class="tb-d-zwei sw" style="--i:4">
        <label class="tb-d-feld"><span class="tb-d-label">Name</span><input name="tb-name" autocomplete="name"></label>
        <label class="tb-d-feld"><span class="tb-d-label">E-Mail</span><input name="tb-mail" type="email" autocomplete="email"></label>
      </div>
      <div class="tb-d-feld sw" style="--i:5"><span class="tb-d-label">Bezahlen mit</span>
        <div class="tb-zahl">
          <label><input type="radio" name="tb-zahl" value="PayPal" checked><span><b>PayPal</b><em>weiter zu PayPal</em></span></label>
          <label><input type="radio" name="tb-zahl" value="Karte"><span><b>Karte</b><em>Visa, Mastercard</em></span></label>
        </div></div>
      <div class="tb-d-summe sw" style="--i:6"><span>Zusammen</span><b data-summe></b></div>
      <div class="sw" style="--i:7"><button class="knopf tb-d-los" type="button" data-bezahlen><span>Jetzt bezahlen</span><i>@@PFEIL@@</i></button></div>
      <p class="tb-d-fehler" data-fehler hidden></p>
    </div>
    <div class="tb-d-schritt" data-schritt="2" hidden>
      <div class="tb-d-laden"><span></span></div>
      <p class="tb-d-laden-text sw" style="--i:1" data-laden-text>Verbindung zu PayPal …</p>
    </div>
    <div class="tb-d-schritt" data-schritt="3" hidden>
      <p class="tb-kicker mono sw" style="--i:0">Bezahlt · Vorschau</p>
      <div class="tb-ticket">
        <div class="tb-t-marke">%s</div>
        <p class="tb-t-zeile">A UNiQUE EXPERiENCE BY MOMO X RUDI</p>
        <p class="tb-t-fuer">Platz für</p>
        <p class="tb-t-name" data-t-name></p>
        <p class="tb-t-mehr"><span data-t-anzahl></span><span data-t-wann></span></p>
        <p class="tb-t-nr mono" data-t-nr></p>
        <p class="tb-t-ort">Walk on the Wild Side · Haasemannstraße 13</p>
      </div>
      <p class="tb-d-mail sw" style="--i:4" data-t-mail></p>
      <div class="sw" style="--i:5"><button class="knopf tb-d-fertig" type="button" data-zu><span>Fertig</span><i>@@PFEIL@@</i></button></div>
    </div>
  </div>
</div>''' % bau.marke('wm') + END


def abend():
    pfad = os.path.join(HIER, 'abend.html')
    h = open(pfad, encoding='utf-8').read()
    h = re.sub(re.escape(ANF) + '.*?' + re.escape(END), '', h, flags=re.S)
    i = h.index('<section class="warteliste"')
    h = h[:i] + ABSCHNITT + h[i:]
    h = re.sub(r'\n?<link rel="stylesheet" href="assets/buchen\.css[^>]*>', '', h)
    h = re.sub(r'\n?<script src="assets/buchen\.js[^>]*></script>', '', h)
    h = h.replace('</head>', '<link rel="stylesheet" href="assets/buchen.css?v=%s">\n</head>' % V, 1)
    h = h.replace('</body>', '<script src="assets/buchen.js?v=%s" defer></script>\n</body>' % V, 1)
    open(pfad, 'w', encoding='utf-8').write(h.replace('@@PFEIL@@', bau.PFEIL))


def pflege():
    s = [bau.kopf('Termine pflegen · Culinarium (Vorschau)', 'Vorschau: Termine für Culinarium eintragen.', 'termine-pflege.html')]
    s.append('''<section class="tp" data-ton="nacht">
  <div class="tp-innen">
    <p class="tb-kicker mono">Nur für das Team · Vorschau</p>
    <h1 class="tb-titel">Termine pflegen.</h1>
    <p class="tb-text">Neuen Abend eintragen, speichern, fertig: Er steht sofort auf der Seite «Der Abend» und lässt sich buchen. In dieser Vorschau bleibt alles in diesem Browser.</p>
    <form class="tp-neu" data-tp-neu>
      <label class="tb-d-feld"><span class="tb-d-label">Datum</span><input type="date" name="datum" required></label>
      <label class="tb-d-feld"><span class="tb-d-label">Beginn</span><input type="time" name="zeit" value="19:00" required></label>
      <label class="tb-d-feld"><span class="tb-d-label">Preis in EUR</span><input type="number" name="preis" value="89" min="0" step="1" required></label>
      <label class="tb-d-feld"><span class="tb-d-label">Plätze</span><input type="number" name="plaetze" value="14" min="1" max="40" required></label>
      <button class="knopf" type="submit"><span>Termin eintragen</span><i>@@PFEIL@@</i></button>
    </form>
    <div class="tp-liste" data-tp-liste></div>
    <div class="tp-fuss">%s
      <button class="tp-zurueck mono" type="button" data-tp-zurueck>Beispieltermine wiederherstellen</button></div>
  </div>
</section>''' % bau.knopf('Auf der Seite ansehen', 'abend.html#termine-buchen', 'leise'))
    s.append(bau.fuss())
    h = ''.join(s).replace('@@PFEIL@@', bau.PFEIL)
    h = h.replace('</head>', '<link rel="stylesheet" href="assets/buchen.css?v=%s">\n</head>' % V, 1)
    h = h.replace('</body>', '<script src="assets/buchen.js?v=%s" defer></script>\n</body>' % V, 1)
    open(os.path.join(HIER, 'termine-pflege.html'), 'w', encoding='utf-8').write(h)


if __name__ == '__main__':
    abend()
    pflege()
    print('buchen: abend.html + termine-pflege.html (Vorschau)')
