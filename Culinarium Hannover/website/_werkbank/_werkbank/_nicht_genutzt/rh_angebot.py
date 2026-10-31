#!/usr/bin/env python3
"""Werkbank Landgasthof Ruedihus, Kapitel «Das Angebot» (Werkbank-Chat 17.10.2026; Aufbau, Stil und Karte aus dh_angebot.py des Waldhotel Doldenhorn,
dort aus angebot_kapitel.py des Carlton-Europe, nur gelesen und kopiert; Worte des Ruedihus). Roberts Regeln vom 17.10.2026: kein Preis, kein Beispielpreis,
kein Rechner hier (er steht einmal in «Worum es geht»), die Zusammenfassung luxuriös mit echtem Hausfoto, kein Drängen zum Gespräch, nie ein Angebot vorbeizukommen.
  angebot()     Zusammenfassung mit Hausfoto · Umfang in vier Lagen · Aufbau und Daten (der frühere «Ausblick» geht hier auf)
  umsetzung()   der Weg zum Einzug, acht Wochen als Band, darunter «Ein Vorschlag.» als Menükarte mit PDF und Gang IV «Wo die KI arbeitet»
  karte_seite() werkbank/karte.html, karte_pdf() → werkbank/vorschlag-landgasthof-ruedihus.pdf (rh_karte_druck.js)"""
import json, os, re, subprocess

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)

PREISE_ZEIGEN = False   # Robert 17.10.2026: keine Preise, keine Beispielpreise, nirgends; den Preis nennt das Haus
DATUM = 'Hamburg, 17. Oktober 2026'
PDF_NAME = 'vorschlag-landgasthof-ruedihus.pdf'
BILD = ('ag-haus', 'haus-winter')   # das Holzhaus im Schnee, warmes Licht hinter den Butzenscheiben (Design-DNA: warmes Licht im Dunkeln)
LIVRE_FOTOS = len(json.load(open(os.path.join(ROOT, '_werkzeuge', 'livre', 'livre.json'), encoding='utf-8'))['fotos'])


def zusammenfassung(z):
    # Werkbank-Regel 14 (17.10.2026 abends): eigene Worte des Ruedihus, gegen Carlton, Doldenhorn und Gasterntal gelegt
    return [
        f'Im Ruedihus beginnt vieles in der Stube, und so ist auch dieser Entwurf aufgebaut: die Website mit {z["seiten"]} Seiten, sieben Werkzeuge für Ihr Team, {z["unterlagen"]} Unterlagen vom Schpiszettel bis zum Heft mit den Menuvorschlägen, {z["druck"]} Drucksachen, {z["etiketten"]} Etiketten für die Zündhölzer, {z["mails"]} Mails, ein Feed für Instagram und das Hausbuch mit {LIVRE_FOTOS} Fotos. Alles davon ist anklickbar.',
        'Damit die Seite unter doldenhorn-ruedihus.ch ans Netz geht, braucht es noch vier Dinge aus dem Haus: die Zugänge zu Domain, SimpleBooking und Mail, ein Wort zu den Fotos, die Angaben für Impressum und Datenschutz und jemanden, der gegenliest.',
        'Was Direktbuchungen dem Ruedihus im Jahr ausmachen können, zeigt ein Rechenbeispiel ganz am Anfang, mit Ihren eigenen Zahlen. Und wenn sie einmal läuft, bleibe ich gern dabei: Ihr Team pflegt selbst, für CHF 350 im Monat, oder ich pflege für Sie, für CHF 700 im Monat, beides monatlich kündbar. Mehr dazu auf der Karte weiter unten.']   # Robert 18.10.2026 19:54
ZUS_ORT = 'Landgasthof Ruedihus · Kandersteg · seit 1753'


def umfang(z):
    return [
        ('Fertig zum Anklicken', [f'{z["seiten"]} Seiten, jede der vier Zimmerarten mit eigener', 'Die fünf Stuben, drei Karten und die Herkunft der Produkte', 'Der Jahreslauf mit einem Menu zu jedem Anlass',
                                  'Zu zweit, die Geschichte seit 1753, Das Haus', 'Seiten vor der Anreise und zur Abreise, die Zimmermappe', 'Zimmer-Finder, Gutschein, Fest-Rechner, Anfrage-Fenster',
                                  'Die Rezeption im Chat', f'{z["unterlagen"]} Unterlagen im Stil der Seite', f'{z["druck"]} Drucksachen, {z["etiketten"]} Zündholz-Etiketten', f'{z["mails"]} Nachrichten an Gäste',
                                  f'{z["feed"]} Bilder für Instagram', f'{LIVRE_FOTOS} Fotos im Hausbuch']),
        ('Im Entwurf in Betrieb', ['Die Stube', 'Der Schreibtisch', 'Die Tafel', 'Der Gastgeber mit dem Chat', 'Das Hausbuch', 'Das Besucherbuch', 'Die Werkstatt']),
        ('Kommt aus Ihrem Haus', ['Domain, SimpleBooking und Mail: die Zugänge', 'Ein Wort zu den Fotos', 'Impressum und Datenschutz: Ihre Angaben', 'Die Telefonnummer fürs Papier',
                                  'Jemand, der Seiten und Karten gegenliest', 'Für Preise auf der Seite: SimpleBooking freischalten']),
        ('Gedacht, noch nicht gebaut', ['Einen Tisch mit freier Uhrzeit reservieren', 'Die Tagesteller der Woche gleich auf der Startseite'])]


AUFBAU = ['Jede Seite liegt fertig da und lädt ohne Umweg über ein Programm.', 'Sieben Werkzeuge, sieben eigene Zugänge.', 'Gebucht wird weiter in Ihrem SimpleBooking.',
          'Der Chat antwortet nur aus Ihren Seiten und Karten.', 'Eine Öffnungszeit wird einmal eingetragen und stimmt dann überall.', 'Ein älterer Stand ist mit einem Klick wieder da.']
DATEN = ['Kein Cookie und niemand, der Gäste verfolgt.', 'Der Chat fragt nie nach Karte oder Pass.', 'Eine Falle hält Maschinen aus den Anfrage-Fenstern.', 'Das Besucherbuch kennt keine Namen.',
         'Ab dem Einzug ein Passwort für jede Person.', 'Bis dahin sieht keine Suchmaschine die Seite.']

WOCHEN = [  # Titel, Ich, Ihr Haus, Dabei
    ('Anfangen', 'Ein Gespräch per Video oder über WhatsApp, danach die Liste, welche Zugänge es braucht.', 'Die Zugänge zu Domain, SimpleBooking und Mail.', 'Familie Maeder, Rezeption'),
    ('Gegenlesen', 'Was Sie anstreichen, ist am selben Tag geändert.', 'Seiten, Karten und Unterlagen lesen.', 'Rezeption, Küche, Service'),
    ('Verbinden', 'SimpleBooking, Anfragen und Chat anschliessen, jedem Werkzeug sein Passwort geben.', 'Einen Namen bei SimpleBooking, der Bescheid weiss.', 'Rezeption, Buchungsanbieter'),
    ('Bilder und Recht', 'Die freigegebenen Fotos einsetzen, Impressum und Datenschutz mit Ihren Angaben füllen.', 'Welche Fotos bleiben, und die Angaben des Hauses.', 'Familie Maeder'),
    ('Das Team schaut', 'Rezeption, Küche, Service und Event-Team gehen alles durch; am Freitag steht die zweite Fassung.', 'Die Zeit, alles einmal durchzugehen.', 'Das ganze Team'),
    ('Umzug vorbereiten', 'Die alten Adressen leiten weiter, Google erfährt davon, ein Probelauf zeigt, ob alles hält.', 'Die Rechtstexte freigeben.', 'Familie Maeder'),
    ('Zeigen', 'Je Werkzeug eine Stunde per Video, mit denen, die damit arbeiten.', 'Eine Stunde je Runde.', 'Rezeption, Küche, Service'),
    ('Einziehen', 'Die Seite geht unter doldenhorn-ruedihus.ch ans Netz, und zwei Wochen lang schaue ich jeden Tag nach ihr.', 'Ihr Ja.', 'Familie Maeder')]
WOCHEN_SATZ = 'Acht Wochen, wenn alles glatt geht. Bleibt einmal etwas liegen, wartet nur dieser Schritt, die anderen gehen weiter.'

KARTE_KOPF = ('Landgasthof Ruedihus · Kandersteg', 'Ein Vorschlag.', 'Eigentum, Pflege und die Zeit danach, gesetzt wie die Karte einer Stube.')
GAENGE = ('Was Ihnen gehört', 'Was ich übernehme', 'Gut zu wissen')
EIGENTUM = ['Dem Haus gehören Website, Werkzeuge, Unterlagen, Drucksachen, Mails, Beiträge und das Hausbuch.', 'Domain, Server und jeder Zugang stehen auf Ihrem Namen.',
            'Die Fotos gehören weiter Ihnen und Ihren Fotografen.', 'Ein Ordner mit jeder Datei liegt bei Ihnen.', 'Trennen sich unsere Wege, geht alles mit Ihnen.']


def preis():
    """Titel, Zusatz rechts («Betrag|klein darunter»), Satz oder Liste. Pflege mit Preis seit Robert 18.10.2026 19:54, Bau ohne Preis."""
    return [
        ('Der Bau', 'bis zum Einzug', 'Alles, was in diesem Entwurf liegt, angepasst, bis es zum Ruedihus passt, und dann ans Netz gebracht.'),
        ('Ihr Team pflegt selbst', 'CHF 350 im Monat|monatlich kündbar', [   # Robert 18.10.2026 19:54, alle vier Häuser
         'Ich halte Server, Domain, Sicherungen und Aktualisierungen in Ordnung und achte auf Sicherheit und Datenschutz.', 'Hakt ein Werkzeug, richte ich es, ohne dafür eine Rechnung zu schreiben.', 'Sie hören spätestens am nächsten Werktag von mir.']),
        ('Ich pflege für Sie', 'CHF 700 im Monat|monatlich kündbar', [
         'Dazu alles aus «Ihr Team pflegt selbst».', 'Kuttel-Woche, Metzgete, Ruedi-Tag und die Stubete bereite ich vor, mit Texten, Bildern und Drucksachen.', 'Was der Chat wissen muss, halte ich auf dem neuesten Stand.', 'Einmal im Monat ein paar Zeilen: woher die Gäste kamen und was ich verbessern würde.']),
        ('Wünsche darüber hinaus', 'nach Absprache', 'Ein weiterer Bereich oder eine Funktion, die es noch nicht gibt: vorher bekommen Sie ein Angebot.')]


DANACH = ['Einen Preis für die Website sowie die Tools nennen wir hier bewusst nicht. Was Sie sehen, ist kein Paket von der Stange, sondern für Ihre vier Häuser gebaut, und dafür gibt es keinen passenden Listenpreis. Darum drehen wir es um: Sagen Sie uns, was Ihnen dieser Auftritt wert ist. Was Sie für angemessen halten, ist der Preis, über den wir sprechen können.',   # Robert 18.10.2026 19:56 (über Oberchef), gleicher Wortlaut in allen vier Werkbänken
             # Robert 18.10.2026 ~14:25: zwei Entscheider, das System als Ganzes, nichts «auch einzeln»   # Werkbank-Regel 13 (Robert 17.10.2026): die Lücke beim Preis sichtbar machen, eigener Satz (Carlton und Doldenhorn haben ihre)
          'Rechnungen von Druckerei, Fotografen und Lektorat gehen weiter direkt an Sie, genauso die Gebühren der Systeme, die Sie heute nutzen.',
          'Für den Chat stellt der Anbieter des Sprachmodells nach Verbrauch Rechnung; wie hoch er höchstens werden darf, bestimmen wir zusammen.']
# Robert 18.10.2026 ~00:35: «Wir hatten doch beim Rivage schon einmal festgesetzt, die Preise. Warum schreiben wir die da nicht hin?»
# Preise des Anbieters (nicht von Robert), Werte und Zusatzzeilen wie in der Karte des Grand Beau-Rivage (nur gelesen).
KI_PREISE = {'Rezeption im Chat': ('USD 0.19', 'Erste Frage eines Gastes nach einer Pause; jede weitere innert fünf Minuten 1 bis 2 Cent.'),
             'Die Werkstatt': ('bis USD 0.35', 'Fünf Entwürfe nach einer Pause; danach bis USD 0.17. Die fertigen Vorlagen kosten nichts.'),
             'Der Gastgeber': ('bis USD 0.27', 'Ein Antwortentwurf nach einer Pause; danach bis USD 0.10. Links einlesen kostet je nach Länge der Seite.'),
             'Das Hausbuch': ('bis USD 0.06', 'Eine Markenprüfung.')}
KI_FUSS = 'Preise des Anbieters, Stand Oktober 2026. Was ein Monat kostet, hängt daran, wie oft Gäste und Team die KI nutzen; die Obergrenze hält es im Rahmen.'
# Robert 18.10.2026 ~14:40: «… dass wir die Website in den verschiedenen Sprachen mit übersetzen wollen. Und welche jetzt erstmal für die Demozwecke
# … aber dass der Kunde auf jeden Fall weiß und sieht, dass da noch mehr Sprachen kommen sollen.»
SPRACHEN = [('Deutsch', True), ('Englisch', False), ('Französisch', False), ('Koreanisch', False), ('Chinesisch', False), ('Japanisch', False)]   # Robert 18.10.2026 15:35: «Auf Deutsch recht», übersetzt wird nach dem Auftrag
SPRACHEN_HTML = '<div class="sp-zeile"><p>Die Website kommt in sechs Sprachen: Deutsch, Englisch, Französisch, Koreanisch, Chinesisch, Japanisch.</p></div>'   # Robert 18.10.2026 17:13/17:16: nur diese eine Zeile, sonst nichts über Sprachen
KI_GANG = 'Wo die KI arbeitet'   # Regel 8 (17.10.2026), Vorbild Gang IV der Karte des Grand Beau-Rivage
KI_SATZ = 'An vier Stellen hilft ein Sprachmodell. Bezahlt wird es über ein Konto, das Ihrem Haus gehört, nach Verbrauch; ich lege das Konto an und eine Grenze je Monat fest.'
KI = [('Rezeption im Chat', 'Antwortet Gästen auf der Website.'), ('Der Gastgeber', 'Entwirft die Antwortbriefe und liest Links ein.'),
      ('Die Werkstatt', 'Legt aus einem Satz fünf Entwürfe an.'), ('Das Hausbuch', 'Hält Entwürfe gegen die Marke des Hauses.')]
KI_MEHR = 'Mehr zu KI und Ihren Daten'   # werkbank/ki.html (rh_ki.py)
PDF_KNOPF = 'Als PDF speichern'

ZEICHEN = '<svg class="ag-z" viewBox="0 0 1044 1398" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>'
ORNAMENT = '<div class="ag-orn" aria-hidden="true"><i></i><b></b><i></i></div>'


def _h(e, n, t):
    return f'<h3 class="ag-h"><span>{n}</span>{e(t)}</h3>'


def bilder(webp, haus):
    return {BILD[0]: webp(haus(BILD[1]), BILD[0], 960, 80, schnitt=0.8, lage=(0.42, 0.5))}


def angebot(k):
    e, bild, z = k['e'], k['bild'], k['z']
    zz = zusammenfassung(z)
    # Roberts rundes Porträt rechts im Text vor dem letzten Absatz, Unterschrift rechtsbündig (Robert 17.10.2026: «aussieht wie ein Rivage oben»)
    ich = '<span class="ag-ich" data-a="auf">' + bild('robert', 'Robert Reff') + '</span>'
    zus = ''.join((ich if i == len(zz) - 1 else '') + f'<p data-a="auf" style="--i:{i + 1}">{e(p)}</p>'.replace('«Worum es geht»', '<a href="#worum">«Worum es geht»</a>') for i, p in enumerate(zz))
    reg = ''.join(f'<a href="#ag-{a}"><span>{n:02d}</span>{e(t)}</a>' for n, (a, t) in enumerate((('kurz', 'Zusammenfassung'), ('umfang', 'Umfang'), ('aufbau', 'Aufbau'), ('daten', 'Daten'), ('wochen', 'Wochen'), ('vorschlag', 'Vorschlag')), 1))

    spalten = ''.join(f'<div class="ag-sp ag-sp--{i + 1}" data-a="auf" style="--i:{i}"><h4>{e(t)}</h4><ul>' + ''.join(f'<li>{e(p)}</li>' for p in pp) + '</ul></div>' for i, (t, pp) in enumerate(umfang(z)))
    liste = lambda pp: '<ul class="ag-l">' + ''.join(f'<li data-a="auf" style="--i:{i % 3}">{e(p)}</li>' for i, p in enumerate(pp)) + '</ul>'
    return f'''
<section class="fl fl--nacht tapete-leicht blatt ag" id="k8">
  <div class="in">
    {k['kopfk']('k8', ['Was zum Ruedihus', 'gehört.'], 'Was gebaut ist, was es noch braucht und wie es danach weitergeht, auf ein paar Blättern, in Ruhe zum Ansehen.')}
    <nav class="ag-reg" data-a="auf" aria-label="In diesem Kapitel">{reg}</nav>
    <div class="ag-blatt ag-kurz" id="ag-kurz" data-a="mkhoch">
      <figure class="ag-bild"><div class="ag-bild__f">{bild(BILD[0], 'Der Landgasthof Ruedihus im Schnee, Licht hinter den Butzenscheiben')}</div><figcaption>{e(ZUS_ORT)}</figcaption></figure>
      <div class="ag-text">
        {_h(e, '01', 'Zusammenfassung')}
        {zus}
        <p class="ag-sig"><span class="ag-sig__b">{bild('unterschrift', 'Unterschrift Robert Reff')}</span><small>Robert Reff · Tasty Studios</small></p>
      </div>
    </div>
    {_A.teil(e, z, LIVRE_FOTOS, _h, SPRACHEN_HTML)}
  </div>
</section>'''


def karte_html(e):
    gang = lambda n, t: f'<p class="mn-gang"><span>{n}</span>{e(t)}</p>'
    zeilen = lambda pp: '<ul class="mn-l">' + ''.join(f'<li>{e(p)}</li>' for p in pp) + '</ul>'
    p = ''
    for t, r, satz in preis():
        unten = (f'<ul class="mn-p__l">' + ''.join(f'<li>{e(x)}</li>' for x in satz) + '</ul>') if isinstance(satz, list) else f'<p class="mn-p__s">{e(satz)}</p>'
        a, _, k = r.partition('|')   # «Betrag|klein darunter»
        p += f'<li class="mn-p"><p class="mn-p__z"><b>{e(t)}</b><i></i><span>{e(a)}{f"<small class=mn-p__k>{e(k)}</small>" if k else ""}</span></p>{unten}</li>'
    return f'''<article class="mn" id="ag-vorschlag" data-a="mkhoch">
        <header class="mn-kopf">
          {ZEICHEN}
          <p class="mn-haus">{e(KARTE_KOPF[0])}</p>
          <h3 class="mn-titel">{e(KARTE_KOPF[1])}</h3>
          <p class="mn-unter">{e(KARTE_KOPF[2])}</p>
        </header>
        {ORNAMENT}
        {gang('I', GAENGE[0])}
        {zeilen(EIGENTUM)}
        {ORNAMENT}
        {gang('II', GAENGE[1])}
        <ul class="mn-l mn-preise">{p}</ul>
        {ORNAMENT}
        {gang('III', GAENGE[2])}
        {zeilen(DANACH)}
        {ORNAMENT}
        {gang('IV', KI_GANG)}
        <p class="mn-unter mn-ki-satz">{e(KI_SATZ)}</p>
        <ul class="mn-l mn-preise">{''.join(f'<li class="mn-p"><p class="mn-p__z"><b>{e(t_)}</b><i></i><span>{e(KI_PREISE[t_][0])}</span></p><p class="mn-p__s">{e(s_ + ' ' + KI_PREISE[t_][1])}</p></li>' for t_, s_ in KI)}</ul>
        <p class="mn-fuss">{e(KI_FUSS)}</p>
        <p class="mn-ki"><a class="kn kn--klein" href="ki.html">{e(KI_MEHR)}<i><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg></i></a></p>
        <footer class="mn-ende"><i></i><span>{e(DATUM)}</span><i></i></footer>
        <p class="mn-pdf"><a class="kn kn--klein" href="{PDF_NAME}" download>{e(PDF_KNOPF)}<i><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg></i></a></p>
      </article>'''


def umsetzung(k):
    e = k['e']
    wochen = ''.join(
        f'<article class="um-w" data-a="kipp" style="--i:{min(i, 3)}"><p class="um-w__n"><b>{i + 1:02d}</b><small>Woche {i + 1}</small></p><h3>{e(t)}</h3>'
        f'<div class="um-w__r"><span>Ich</span><p>{e(ich)}</p></div><div class="um-w__r"><span>Ihr Haus</span><p>{e(haus)}</p></div><div class="um-w__r um-w__r--wer"><span>Dabei</span><p>{e(wer)}</p></div></article>'
        for i, (t, ich, haus, wer) in enumerate(WOCHEN))
    return f'''
<section class="fl fl--navy tapete blatt um" id="ag-wochen">
  <div class="in">
    {k['kopf'](0, 'Das Angebot', ['Der Weg zum Einzug,', 'Woche für Woche.'], 'Vom ersten Gespräch bis zum Tag, an dem doldenhorn-ruedihus.ch die neue Seite zeigt, und die Karte für die Zeit danach.')}
    <div class="gang um-gang"><div class="band">{wochen}</div>{k['gangfuss']()}</div>
    <p class="um-satz" data-a="auf">{e(WOCHEN_SATZ)}</p>
    <div class="mn-buehne">
      {karte_html(e)}
    </div>
  </div>
</section>'''


def karte_seite():
    """werkbank/karte.html: die Karte aus der gebauten Werkbank, allein auf Papier, mit denselben Stilen."""
    idx = os.path.join(ROOT, 'werkbank', 'index.html')
    t = open(idx, encoding='utf-8').read()
    m = re.search(r'<article class="mn".*?</article>', t, re.S)
    css = re.search(r'<link rel="stylesheet" href="[^"]*werkbank\.css[^"]*">', t)
    defs = ''.join(re.findall(r'<svg width="0" height="0"[^>]*>.*?</svg>', t, re.S))
    fonts = ''.join(re.findall(r'<link rel="preload"[^>]*as="font"[^>]*>', t))
    karte = m.group(0).replace('data-a="mkhoch"', 'class="da"').replace('<article class="mn" id="ag-vorschlag" class="da">', '<article class="mn da">')
    html = f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ein Vorschlag · Landgasthof Ruedihus</title>
<meta name="robots" content="noindex, nofollow">
{fonts}
{css.group(0)}
<style>
html,body{{margin:0;background:#1f1209}}
body{{min-height:100vh;display:flex;align-items:flex-start;justify-content:center;padding:clamp(20px,4vw,64px) clamp(16px,3vw,40px)}}
.mn{{opacity:1!important;transform:none!important;transition:none!important}}
.mn-ki{{display:none!important}}
.mn-pdf{{display:none!important}}
@page{{margin:0}}
@media print{{html,body{{background:#fbf6ea;padding:0;display:block}}.mn{{width:100%;max-width:none;border-radius:0;box-shadow:none;padding:16mm 18mm}}.mn::before{{inset:7mm}}.mn::after{{inset:9.5mm}}.mn-gang,.mn-l li,.mn-p{{break-inside:avoid}}}}
</style>
</head>
<body>
{defs}
{karte}
</body>
</html>
'''
    open(os.path.join(ROOT, 'werkbank', 'karte.html'), 'w', encoding='utf-8').write(html)


def karte_pdf():
    s = os.path.join(ROOT, 'werkbank', 'karte.html')
    r = subprocess.run(['node', os.path.join(W, 'rh_karte_druck.js'), s], capture_output=True, text=True)
    print((r.stdout.strip().splitlines() or [''])[-1] if r.returncode == 0 else 'karte_druck.js: ' + (r.stdout + r.stderr)[-600:])


CSS = '''
/* ---------- «Das Angebot» (angebot_ebene.py, 14.10.2026): Nacht mit leichter Tapete, helle Blätter mit doppeltem Goldrand, Serife ---------- */
.ag .kopfzeile{margin-bottom:clamp(30px,3.4vw,54px)}
.ag-reg{display:flex;flex-wrap:wrap;gap:8px clamp(18px,2.6vw,44px);justify-content:center;margin:0 auto clamp(44px,5vw,80px);padding-bottom:18px;border-bottom:1px solid rgba(210,191,152,.28)}
.ag-reg a{display:inline-flex;align-items:baseline;gap:9px;font:400 12.5px/1.2 var(--serif);letter-spacing:.22em;text-transform:uppercase;color:#ecdcb4;text-decoration:none;opacity:.8;transition:opacity .4s}
.ag-reg a span{font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:var(--gold)}
.ag-reg a:hover{opacity:1}
.ag-teil{margin-top:clamp(40px,4.6vw,76px)}
.ag-blatt{position:relative;padding:clamp(28px,3.8vw,64px);border-radius:clamp(22px,2.4vw,34px);background:linear-gradient(rgba(251,246,234,.86),rgba(251,246,234,.86)),#fbf6ea var(--muster) 50% 0/var(--musterb) auto;color:var(--tinte);
  box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(150,125,64,.5),0 70px 90px -56px rgba(0,0,0,.9),0 26px 40px -30px rgba(0,0,0,.6)}
.ag-blatt::before,.ag-blatt::after{content:"";position:absolute;pointer-events:none;border:1px solid rgba(150,125,64,.5);border-radius:clamp(14px,1.6vw,24px);inset:clamp(10px,1.1vw,16px)}
.ag-blatt::after{inset:clamp(15px,1.5vw,22px);border-color:rgba(150,125,64,.22);border-radius:clamp(11px,1.3vw,19px)}
.ag [data-a="mkhoch"]{opacity:0;transform:translateY(120px) scale(.97);transition:opacity 1.3s cubic-bezier(.16,1,.3,1),transform 2.1s cubic-bezier(.16,1,.3,1);transition-delay:var(--vz,0ms)}
.ag [data-a="mkhoch"].da{opacity:1;transform:none}
.ag-h{display:flex;align-items:baseline;gap:16px;margin:0 0 clamp(18px,2vw,28px);font-family:var(--serif);font-size:clamp(1.9rem,2.6vw,2.7rem);line-height:1.08;color:var(--tinte)}
.ag-h span{font-family:var(--mono);font-size:clamp(.78rem,.9vw,.92rem);letter-spacing:.16em;color:#967d40}
/* Zusammenfassung (Robert 17.10.2026: «ästhetischer, ansprechender, luxuriöser», echtes Hausfoto): das Haus am Abend hochkant unter einem
   Bogen wie die Fenster des Hauses, doppelter Goldrand, darunter die Adresse; rechts der Text mit Initiale in Gold, unten Roberts Unterschrift.
   Bis das Foto da ist, steht sein kleines Abbild im Bogen (nie ein leeres Feld). */
.ag-kurz{display:grid;gap:clamp(30px,4.4vw,80px);align-items:center;grid-template-columns:minmax(0,1fr);padding:clamp(30px,4.6vw,80px)}
@media(min-width:900px){.ag-kurz{grid-template-columns:minmax(0,.78fr) minmax(0,1.22fr)}}
.ag-bild{margin:0;text-align:center}
.ag-bild__f{position:relative;aspect-ratio:4/5;border-radius:999px 999px 18px 18px;overflow:hidden;background:#0b1f40;
  box-shadow:0 0 0 1px rgba(150,125,64,.55),0 0 0 8px #fbf6ea,0 0 0 9px rgba(150,125,64,.3),0 46px 60px -40px rgba(6,20,43,.75)}
.ag-bild__f img{display:block;width:100%;height:100%;object-fit:cover}
.js .ag-bild img.ld:not(.da),.js .ag-bild img.ld.da{opacity:1;animation:none}
@media (hover:hover){.ag-bild__f img{transition:transform 2.2s cubic-bezier(.16,1,.3,1)}.ag-bild__f:hover img{transform:scale(1.04);transition-duration:2.8s}}
.ag-bild figcaption{display:inline-flex;align-items:center;gap:12px;margin-top:clamp(18px,1.8vw,26px);font:400 clamp(10.5px,.82vw,12px)/1.3 var(--serif);letter-spacing:.28em;text-transform:uppercase;color:#967d40}
.ag-bild figcaption::before,.ag-bild figcaption::after{content:"";width:22px;height:1px;background:rgba(150,125,64,.6)}
.ag-text{max-width:60ch}
.ag-kurz .ag-h{margin-bottom:clamp(22px,2.4vw,34px);padding-bottom:clamp(16px,1.6vw,22px);border-bottom:1px solid rgba(150,125,64,.3)}
.ag-text p{margin:0;font-family:var(--serif);font-size:clamp(1.12rem,1.3vw,1.34rem);line-height:1.62;color:rgba(12,21,38,.84)}
.ag-text p+p{margin-top:1em}
.ag-text p:first-of-type{font-size:clamp(1.32rem,1.66vw,1.72rem);line-height:1.45;color:var(--tinte)}
.ag-text p:first-of-type::first-letter{float:left;margin:.08em .12em 0 0;font-size:3.3em;line-height:.8;color:#967d40}
.ag-text a{color:#7a6530;text-decoration:underline;text-decoration-color:rgba(150,125,64,.45);text-underline-offset:.2em}
.ag-text a:hover{text-decoration-color:#7a6530}
.ag-text{display:flow-root}
.ag-text .ag-ich+p{margin-top:1em}
.ag-text .ag-sig{display:flex;flex-direction:column;align-items:center;gap:4px;clear:both;width:max-content;margin:clamp(26px,2.8vw,40px) clamp(10px,4vw,48px) 0 auto;text-align:center}   /* Unterschrift rechtsbündig (Robert 17.10.2026) */
.ag-ich{float:right;width:clamp(104px,8.6vw,148px);aspect-ratio:1;margin:6px 8px 8px clamp(16px,1.6vw,26px);border-radius:50%;overflow:hidden;shape-outside:circle(50%) border-box;shape-margin:clamp(14px,1.4vw,22px);
  box-shadow:0 0 0 1px rgba(12,21,38,.17),0 0 0 6px #fbf6ea,0 0 0 7px rgba(150,125,64,.45),0 20px 26px -16px rgba(12,21,38,.5)}
.ag-ich img{display:block;width:100%;height:100%;object-fit:cover;border-radius:50%}
.ag-sig__b{display:block;width:clamp(110px,10vw,150px)}   /* Robert 18.10.2026: kleiner, nicht am Rand */
.ag-sig__b img{display:block;width:100%;height:auto}
.ag-sig small{padding-bottom:0;font:400 10.5px/1.3 var(--serif);letter-spacing:.24em;text-transform:uppercase;color:#967d40}
@media(max-width:899px){.ag-bild__f{max-width:420px;margin:0 auto}}
/* Nutzen: ein Blatt, drei Rechnungen untereinander (Robert 14.10.2026). Links Nummer, Titel, Satz; rechts die Rechnung als ruhige Zeilen, das Ergebnis in Gold. */
.ag-ein{margin:0 0 clamp(8px,1vw,14px);max-width:66ch;font-family:var(--serif);font-size:clamp(1.12rem,1.3vw,1.34rem);line-height:1.6;color:rgba(12,21,38,.8)}
.ag-wert .ag-orn{max-width:none;margin:clamp(26px,3vw,44px) 0}
.ag-r{display:grid;gap:clamp(22px,3vw,56px);align-items:start}
@media(min-width:900px){.ag-r{grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr)}}
.ag-r__n{margin:0 0 12px;font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;color:#967d40}
.ag-r__t h4{margin:0;font-family:var(--serif);font-size:clamp(1.7rem,2.1vw,2.2rem);line-height:1.1;color:var(--tinte)}
.ag-r__t p:last-child{margin:14px 0 0;max-width:46ch;font-family:var(--serif);font-size:clamp(1.06rem,1.14vw,1.2rem);line-height:1.6;color:rgba(12,21,38,.78)}
.ag-r__r{padding-top:6px}
.ag-zl{display:flex;align-items:baseline;justify-content:space-between;gap:18px;padding:12px 0;border-bottom:1px solid rgba(150,125,64,.26)}
.ag-zl__n{font-family:var(--serif);font-size:clamp(1.16rem,1.26vw,1.34rem);line-height:1.4;color:rgba(12,21,38,.86)}
.ag-zl__w{flex:none;display:flex;align-items:baseline;gap:8px;cursor:text}
.ag-zl input{width:7.5em;appearance:none;-webkit-appearance:none;background:transparent;border:0;border-radius:0;padding:2px 0;text-align:right;
  font-family:var(--serif);font-size:clamp(1.5rem,1.7vw,1.8rem);line-height:1.1;color:var(--tinte);outline:0;transition:border-color .3s}
.ag-zl input:focus{color:#967d40}
.ag-zl__w small{font-family:var(--serif);font-style:italic;font-size:clamp(.98rem,1.04vw,1.08rem);color:rgba(12,21,38,.62);white-space:nowrap}
.ag-erg{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px;padding-top:clamp(18px,2vw,26px)}
.ag-erg b{font-family:var(--serif);font-size:clamp(2.8rem,3.6vw,3.8rem);line-height:.95;color:#967d40}
.ag-erg span{font-family:var(--serif);font-style:italic;font-size:clamp(1.1rem,1.2vw,1.3rem);color:#967d40}
.ag-erg small{flex-basis:100%;margin-top:4px;font-family:var(--serif);font-size:clamp(1.04rem,1.1vw,1.16rem);color:rgba(12,21,38,.76)}
@media(max-width:600px){.ag-zl{flex-wrap:wrap}.ag-zl__w{width:100%;justify-content:flex-end}.ag-zl input{width:8em}}
/* Umfang (Robert 14.10.2026 abends: «rechts unten so viel Leerraum», «mach das geiler»): kein Vierer-Raster mehr, sondern drei Lagen,
   die das Blatt füllen: oben «Steht, zum Anklicken» über die ganze Breite mit den Punkten in drei Spalten, darunter «Läuft im Entwurf» und
   «Braucht etwas von Ihnen» nebeneinander, unten «Eine Idee» als Band mit drei Punkten in einer Zeile. Goldlinien wie in der Menükarte. */
.ag-spalten{display:grid;gap:0}
.ag-sp{padding:clamp(18px,2vw,30px) 0}
.ag-sp+.ag-sp{border-top:1px solid rgba(150,125,64,.3)}
.ag-sp h4{margin:0 0 6px;font-family:var(--serif);font-size:clamp(1.7rem,2vw,2.1rem);line-height:1.12;color:var(--tinte)}
.ag-sp h4::after{content:"";display:block;width:34px;height:1px;margin:12px 0 8px;background:linear-gradient(90deg,#967d40,rgba(150,125,64,0))}
.ag-sp ul,.ag-l{list-style:none;margin:0;padding:0}
.ag-sp li{padding:12px 0;border-top:1px solid rgba(150,125,64,.18);font-family:var(--serif);font-size:clamp(1.18rem,1.3vw,1.4rem);line-height:1.35;color:rgba(12,21,38,.9)}
.ag-sp li:first-child{border-top:0}
@media(min-width:760px){
  .ag-sp--1 ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:clamp(22px,2.6vw,44px)}
  .ag-sp--1 li:nth-child(-n+3){border-top:0}
  .ag-spalten{grid-template-columns:repeat(2,minmax(0,1fr))}
  .ag-sp--1,.ag-sp--4{grid-column:1/-1}
  .ag-sp--2{padding-inline-end:clamp(22px,2.6vw,44px)}
  .ag-sp--3{padding-inline-start:clamp(22px,2.6vw,44px);border-inline-start:1px solid rgba(150,125,64,.3)}
  .ag-sp--4 ul{display:flex;flex-wrap:wrap;gap:0 clamp(18px,2vw,34px)}
  .ag-sp--4 li{border-top:0;padding:10px 0;display:flex;align-items:center;gap:clamp(18px,2vw,34px)}
  .ag-sp--4 li+li::before{content:"";width:7px;height:7px;border:1px solid #967d40;transform:rotate(45deg);flex:none}
}
@media(min-width:1100px){.ag-sp--1 ul{grid-template-columns:repeat(4,minmax(0,1fr))}.ag-sp--1 li:nth-child(-n+4){border-top:0}}
/* Aufbau und Daten nebeneinander, je eine Zeile je Punkt */
.ag-zwei{display:grid;gap:clamp(36px,4vw,64px)}
@media(min-width:900px){.ag-zwei{grid-template-columns:repeat(2,minmax(0,1fr))}}
.ag-l li{position:relative;padding:15px 0 15px 30px;border-top:1px solid rgba(150,125,64,.18);font-family:var(--serif);font-size:clamp(1.24rem,1.4vw,1.5rem);line-height:1.4;color:rgba(12,21,38,.9)}
.ag-l li:first-child{border-top:0;padding-top:0}
.ag-l li::before{content:"";position:absolute;left:3px;top:1.05em;width:7px;height:7px;border:1px solid #967d40;transform:rotate(45deg)}
.ag-l li:first-child::before{top:.5em}
@media (prefers-reduced-motion:reduce){.ag [data-a="mkhoch"]{opacity:1;transform:none;transition:none}.ag-bild__f img{transition:none;transform:none!important}}

/* ---------- «Die Implementierung» (angebot_ebene.py, 14.10.2026): acht helle Wochen-Karten als Band, darunter die Karte «Ein Vorschlag.» ---------- */
.um .kopfzeile{margin-bottom:clamp(30px,3.4vw,54px)}
.um-gang .band{gap:clamp(16px,1.8vw,26px)}
.um-w{display:flex;flex-direction:column;width:clamp(290px,27vw,400px);padding:clamp(24px,2.4vw,34px);border-radius:26px;color:var(--tinte);background:#fbf6ea;
  box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(150,125,64,.45),0 40px 50px -36px rgba(0,0,0,.9)}
.um-w__n{display:flex;align-items:baseline;gap:12px;margin:0 0 10px}
.um-w__n b{font-family:var(--serif);font-size:clamp(2.4rem,2.8vw,3rem);line-height:.9;color:#967d40}
.um-w__n small{font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:rgba(12,21,38,.5)}
.um-w h3{margin:0 0 16px;font-family:var(--serif);font-size:clamp(1.5rem,1.8vw,1.9rem);line-height:1.1;color:var(--tinte)}
.um-w__r{padding:11px 0;border-top:1px solid rgba(150,125,64,.3)}
.um-w__r span{display:block;margin-bottom:4px;font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:#967d40}
.um-w__r p{margin:0;font-family:var(--serif);font-size:clamp(1.08rem,1.14vw,1.2rem);line-height:1.5;color:rgba(12,21,38,.86)}
.um-w__r--wer{margin-top:auto}
.um-w__r--wer p{color:var(--tinte)}
@media(max-width:700px){.um-w{width:78vw}}
.um-satz{margin:clamp(10px,1.2vw,18px) auto 0;max-width:62ch;text-align:center;font-family:var(--serif);font-size:clamp(1.12rem,1.35vw,1.4rem);line-height:1.5;color:rgba(255,255,255,.88)}
.um-woche{display:none}
/* Die Karte: ein Menü des Hauses, mittig, Papier mit zarter Tapete, doppelter Goldrand, Zeichen oben, Gänge mit Ornament */
.mn-buehne{display:flex;justify-content:center;margin-top:clamp(48px,5.6vw,96px);padding:0 0 clamp(10px,1vw,18px)}
.mn{position:relative;width:min(100%,900px);padding:clamp(34px,5vw,84px) clamp(22px,5.6vw,96px) clamp(30px,4vw,64px);text-align:center;color:var(--tinte);
  background:linear-gradient(rgba(251,246,234,.86),rgba(251,246,234,.86)),#fbf6ea var(--muster) 50% 0/var(--musterb) auto;border-radius:6px;
  box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(150,125,64,.55),0 90px 110px -60px rgba(0,0,0,.95),0 30px 50px -30px rgba(0,0,0,.7)}
.mn::before,.mn::after{content:"";position:absolute;pointer-events:none;border:1px solid rgba(150,125,64,.6);inset:clamp(10px,1.2vw,18px)}
.mn::after{inset:clamp(14px,1.6vw,24px);border-color:rgba(150,125,64,.26)}
.um [data-a="mkhoch"]{opacity:0;transform:translateY(120px) scale(.97);transition:opacity 1.3s cubic-bezier(.16,1,.3,1),transform 2.1s cubic-bezier(.16,1,.3,1)}
.um [data-a="mkhoch"].da{opacity:1;transform:none}
.ag-z{display:block;width:clamp(56px,5.6vw,88px);height:auto;margin:0 auto clamp(16px,1.8vw,26px);color:#b08d44;fill:url(#cegold)}
.mn-haus{margin:0;font:400 clamp(11px,.9vw,13px)/1.3 var(--serif);letter-spacing:.32em;text-transform:uppercase;color:#967d40}
.mn-titel{margin:clamp(14px,1.4vw,20px) 0 0;font-family:var(--serif);font-size:clamp(2.6rem,4.4vw,4.4rem);line-height:1;color:var(--tinte)}
.mn-unter{margin:clamp(12px,1.2vw,16px) auto 0;max-width:46ch;font-family:var(--serif);font-style:italic;font-size:clamp(1.08rem,1.2vw,1.24rem);line-height:1.5;color:rgba(12,21,38,.68)}
.ag-orn{display:flex;align-items:center;justify-content:center;gap:14px;margin:clamp(28px,3.2vw,48px) auto clamp(22px,2.4vw,34px);max-width:420px}
.ag-orn i{flex:1;height:1px;background:linear-gradient(90deg,rgba(150,125,64,0),rgba(150,125,64,.7))}
.ag-orn i:last-child{background:linear-gradient(90deg,rgba(150,125,64,.7),rgba(150,125,64,0))}
.ag-orn b{width:8px;height:8px;transform:rotate(45deg);border:1px solid #967d40}
.mn-gang{margin:0 0 clamp(16px,1.8vw,24px);font-family:var(--serif);font-size:clamp(1.7rem,2.3vw,2.3rem);line-height:1.1;color:var(--tinte)}
.mn-gang span{display:block;margin-bottom:8px;font:400 11px/1 var(--serif);letter-spacing:.3em;color:#967d40}
.mn-l{list-style:none;margin:0 auto;padding:0;max-width:62ch}
.mn-l li{padding:9px 0;font-family:var(--serif);font-size:clamp(1.08rem,1.2vw,1.26rem);line-height:1.55;color:rgba(12,21,38,.88)}
.mn-preise{max-width:600px;text-align:left}
.mn-p{padding:clamp(12px,1.2vw,16px) 0!important}
.mn-p+.mn-p{border-top:1px solid rgba(150,125,64,.22)}
.mn-p__z{display:flex;align-items:baseline;gap:10px;margin:0}
.mn-p__z b{flex:none;font-family:var(--serif);font-weight:600;font-size:clamp(1.14rem,1.3vw,1.34rem);color:var(--tinte)}
.mn-p__z i{flex:1;border-bottom:1px dotted rgba(150,125,64,.8);transform:translateY(-.3em)}
.mn-p__z span{flex:none;font-family:var(--serif);font-size:clamp(1.08rem,1.2vw,1.26rem);color:#7a6530;white-space:nowrap}
.mn-p__k{display:block;margin-top:2px;font-size:.72em;text-align:right;opacity:.75}
.mn-p__l{list-style:none;margin:6px 0 0;padding:0}.mn-p__l li{padding:2px 0 2px 1.1em!important;position:relative;font-style:italic;font-size:clamp(.98rem,1.06vw,1.08rem)!important;line-height:1.5!important;color:rgba(12,21,38,.68)!important}.mn-p__l li::before{content:'–';position:absolute;left:0;color:#7a6530}
.mn-p__s{margin:5px 0 0;font-family:var(--serif);font-style:italic;font-size:clamp(.98rem,1.06vw,1.08rem);line-height:1.5;color:rgba(12,21,38,.68)}
.mn-fuss{margin:clamp(14px,1.4vw,20px) 0 0;font-family:var(--serif);font-style:italic;font-size:.98rem;color:rgba(12,21,38,.6)}
.mn-ende{display:flex;align-items:center;justify-content:center;gap:16px;margin-top:clamp(30px,3.4vw,52px)}
.mn-ende i{width:clamp(30px,4vw,60px);height:1px;background:rgba(150,125,64,.55)}
.mn-ende span{font:400 10.5px/1 var(--serif);letter-spacing:.26em;text-transform:uppercase;color:#967d40}
.mn-pdf{margin:clamp(22px,2.4vw,34px) 0 0}
.mn-ki{margin:clamp(16px,1.8vw,24px) 0 0}.mn-ki-satz{margin-bottom:clamp(10px,1.2vw,16px)!important}
@media print{.mn-ki{display:none}}
.mn-pdf .kn{--o:#1f3f77;--m:#0b1f40;--u:#040d1e;--t:#fff;--licht:rgba(255,255,255,.26);--kante:rgba(0,0,0,.55);--tf:rgba(6,20,43,.6);--ko:#fbf3e2;--ku:#cfbd98;--kt:var(--tinte);--klicht:rgba(255,255,255,.9)}
@media(max-width:600px){.mn-p__z{flex-wrap:wrap;justify-content:center;text-align:center}.mn-p__z i{display:none}.mn-p__z span{width:100%;white-space:normal}.mn-p__k{text-align:center}.mn-preise{text-align:center}}
@media (prefers-reduced-motion:reduce){.um [data-a="mkhoch"]{opacity:1;transform:none;transition:none}}
'''


# Robert 18.10.2026 «vorschlag a»: «Was dazugehört», «Das Gerüst» und «Was mit Daten geschieht» in Fassung A (rh_angebot_a.py)
import rh_angebot_a as _A  # noqa: E402
CSS += _A.CSS
