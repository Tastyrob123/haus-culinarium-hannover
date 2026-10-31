#!/usr/bin/env python3
"""Befund-Seite des Spähers (Station 2) für Culinarium Hannover, gebaut mit dem Werkbank-Kit.
   python3 bau_befund.py   → befund.html + werkbank/ + bilder/ in diesem Ordner. Inhalt aus befund.md / einordnung.json (25.10.2026).
   Vorlage: Hotel Alpenhof Weisstannen, _kette/02-spaeher/bau_befund.py. Es gibt keine Website: «heutige Seite» ist das Instagram-Profil."""
import json, os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
os.environ['HAUS'] = HIER
sys.path.insert(0, os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit'))
import kern as K
from kern import H, e, kn, kap, titel, PF

Q = os.path.join(HIER, '_quelle-bilder')
HEUTE = 'https://www.instagram.com/culinarium_hannover/'
KARTE = 'http://127.0.0.1:8978/?haus=Culinarium%20Hannover'
B = lambda t: f'<span class="bf-beleg">{t}</span>'
OFFEN = lambda t='offen': f'<span class="bf-offen">{t}</span>'
IG = lambda k: f'<a href="https://www.instagram.com/p/{k}/" target="_blank" rel="noopener">{k}</a>'


def bild(name, breite=1600, schnitt=None, lage=(.5, .5), dunkel=None, ziel=None):
    quelle = os.path.join(Q, name + '.jpg')
    ziel_n = ziel or name
    pfad = os.path.join(HIER, 'bilder', ziel_n + '.webp')
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    if not os.path.exists(pfad) or os.path.getmtime(pfad) < os.path.getmtime(quelle):
        K.webp(quelle, pfad, breite, q=80, schnitt=schnitt, lage=lage, dunkel=dunkel)
    return 'bilder/' + ziel_n + '.webp'


def muster():
    vb, innen = H.ZEICHEN
    w, h = [float(x) for x in vb.split()[2:]]
    s = 30 / w
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">'
           f'<g fill="none" stroke="#d4b483" stroke-opacity=".10" stroke-width="1"><path d="M0 .5H240M.5 0V240"/></g>'
           f'<g fill="#d4b483" fill-opacity=".09" transform="translate({120 - 15} {120 - h * s / 2}) scale({s})">{innen}</g></svg>')
    open(os.path.join(HIER, 'werkbank', 'muster.svg'), 'w').write(svg)


def blatt(i, ident, name, zeilen, text, innen, fl):
    return f'''<section class="fl {fl} blatt" id="{ident}">
  <div class="in">
    {K.kopf(i, name, zeilen, text)}
    {innen}
  </div>
</section>'''


def liste(punkte):
    return '<ul class="bf-liste">' + ''.join(f'<li data-a="auf" style="--i:{min(k, 6)}"><b>{t}</b>{x}</li>' for k, (t, x) in enumerate(punkte)) + '</ul>'


def tab(kopf, zeilen):
    return ('<table class="bf-tab" data-a="auf"><thead><tr>' + ''.join(f'<th>{k}</th>' for k in kopf) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in z) + '</tr>' for z in zeilen) + '</tbody></table>')


def satz(t, oben=24):
    return f'<div class="lauf" style="margin-top:{oben}px"><p data-a="worte">{t}</p></div>'


def zwei(l_titel, l, r_titel, r):
    ul = lambda xs: '<ul>' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>'
    return f'<div class="bf-zwei" data-a="auf"><div><h3>{l_titel}</h3>{ul(l)}</div><div><h3>{r_titel}</h3>{ul(r)}</div></div>'


def baue():
    K.gestaltung()
    muster()
    b_auf = bild('C9z2rj1MRb2-1', 2000, schnitt=16 / 10, lage=(.5, .55), dunkel=(.45, .5), ziel='auftakt-dunkel')
    b_schluss = bild('DbYnkdkjrNy-2', 2000, schnitt=16 / 10, lage=(.5, .3), dunkel=(.45, .5), ziel='schluss-dunkel')
    b_mond = bild('DbYnkdkjrNy-1', 1100, ziel='plakat-mondfrau')
    b_panther = bild('DVjkofijp6R-1', 1000, ziel='plakat-panther')
    b_kuerbis = bild('DPwlqcfiKcA-1', 1000, ziel='plakat-kuerbis')
    b_teller = bild('De1pn9ttMoX-1', 1100, ziel='teller-rudi')
    b_drink = bild('DFqZn2UMYMV-1', 900, ziel='drink-recap')
    b_giessen = bild('DFqZn2UMYMV-2', 1600, schnitt=4 / 3, lage=(.5, .45), ziel='giessen-recap')
    b_bar = bild('DecaAh8oxYw-1', 900, schnitt=4 / 3, ziel='familie-bar')
    b_dirty = bild('DZiug6EoMRr-1', 900, schnitt=4 / 3, ziel='familie-dirty-chicken')
    b_tafel = bild('C9z2rj1MRb2-2-innen', 1400, schnitt=4 / 3, lage=(.5, .4), ziel='tafel-voronov')

    streu = ''.join(f'<div class="abzug" data-a="schweb" style="left:{x}%;top:{y}%;width:{w}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}"><img src="{s}" alt=""></div>'
                    for i, (s, x, y, w, r) in enumerate([(b_mond, 4, 2, 46, -3), (b_teller, 46, 26, 42, 2.5), (b_drink, 14, 50, 30, -1.5)]))
    auftakt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(2, 'Späher · Befund')}
      {titel(['Ausgebucht,', 'aber ohne Adresse.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte">Culinarium Hannover: Rudi kocht vegetarisch, Momo mixt zu jedem Gang einen Drink und erklärt ihn, an der langen Tafel der Bar Walk on the Wild Side in Linden. Es gibt keine Website, nur ein Instagram-Profil. Hier steht, wie dieser Auftritt dasteht, was fehlt, was die Abende ausmacht und ob es passt. Projektart Auftrag. Jede Angabe mit Quelle, Stand 25. Oktober 2026.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Instagram öffnen', HEUTE, neu=True)}{kn('Zur Empfehlung', '#empfehlung', 'kn--linie')}</div>
    </div>
    <div class="auslage" aria-hidden="true">{streu}</div>
  </div>
</section>'''

    haus = blatt(1, 'haus', 'Das Haus in Kürze', ['Zwei Köpfe,', 'eine lange Tafel.'],
                 'Kein Restaurant und kein Hotel: eine Reihe von Abenden, rund drei Doppeltermine im Jahr, ohne eigenen Rechtsträger.',
                 tab(['Angabe', 'Wert', 'Quelle'], [
                     ['Format', 'Vegetarisches 3-Gänge-Menü, 5 Signature Drinks, Cocktail-Tasting mit Schulung zu Fatwashing, Milkwashing und Klärung durch Enzyme', B(IG('DbYnkdkjrNy') + ', 29.07.2026')],
                     ['Team', 'Rudolf «Rudi» Napieraj (Küche), Momo (Drinks, Klarname ' + OFFEN('nicht öffentlich') + '), Derya Ivkin', B('Bio @culinarium_hannover, 25.10.2026')],
                     ['Ort', 'Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover-Linden', B('Google Maps, 25.10.2026')],
                     ['Termine', 'Freitag 19:00 und Samstag 17:00 · zuletzt 27./28.03. und 25./26.09.2026 · nächster ' + OFFEN('nicht angekündigt'), B(IG('DVjkofijp6R') + ', ' + IG('DbYnkdkjrNy'))],
                     ['Preis', '89,00 EUR (2026) · 2023 noch 59 bis 80 EUR', B('Beiträge; Kundenprofil Blatt 3')],
                     ['Plätze', '14 pro Abend laut Beiträgen · Tafel der Bar laut Verzeichnissen 8 bis 12 · ' + OFFEN('welche Zahl gilt'), B('Kundenprofil Blatt 3, 4, 5')],
                     ['Seit', 'Pop-up mit Momo seit 20.05.2023, mit Rudi seit April 2024', B('Kundenprofil Blatt 3')],
                     ['Rechtlich', 'Kein Rechtsträger, kein Impressum, kein Register · culinarium-hannover.de frei', B('DENIC, 24.10.2026')],
                 ]), 'fl--papier')

    agentur = blatt(2, 'agentur', 'Wer hinter dem heutigen Auftritt steht', ['Keine Agentur,', 'nur ein Profil.'],
                    'Es gibt nichts abzulösen: keine Seite, keinen Baukasten, keinen Vertrag. Der ganze Auftritt läuft über Instagram und eine PayPal-Zahlung nach Nachricht.',
                    liste([('Plattform', 'Instagram (Meta), Konto @culinarium_hannover, vom Team selbst geführt. Wer das Konto besitzt: ' + OFFEN('im Gespräch zu klären') + '.'),
                           ('Seit wann', f'Erster eigener Beitrag 20.05.2023, letzter eigener Beitrag 29.07.2026 ({IG("DbYnkdkjrNy")}).'),
                           ('Buchung', '«Tickets ausschließlich per Vorverkauf über PayPal. Schreibt uns hierzu gerne eine Nachricht.» Kein Ticketsystem, keine Warteliste, kein Beleg.'),
                           ('Gestaltung', 'Plakate ohne Nennung, wer sie macht. Herkunft der Illustrationen (Stock, KI, eigene Collage) und Schrift der Wortmarke: ' + OFFEN() + '.'),
                           ('Nutzungsrechte', 'Fotos gehören den Fotografen (Irina Voronov, focusonbiz_hannover, Recap 02/2025 ohne Namen). Ein Repost ist keine Web-Lizenz.')])
                    + zwei('Wo wir besser sind', ['Eine Adresse, die man weitergeben kann', 'Termine, Menü und Preis an einem Ort', 'Buchen ohne Nachricht, mit Beleg und Warteliste', 'Impressum, Datenschutz, AGB mit Stornoregel', 'Bei Google gefunden statt Culinar Herrenhausen'],
                           'Was dem Haus bleibt', ['Das Profil, so wie es ist', 'Die Plakate als Reihe, jetzt mit Archiv', 'Rudis Schreibweise der Gerichte', 'Kein Vertrag, den jemand kündigen muss']), 'fl--nacht')

    fenster1 = f'''<section class="fl fl--nacht blatt" style="padding-top:0">
  <div class="in"><div class="fen" data-a="schweb"><div class="fen__k"><i></i><i></i><i></i><span>Recap Februar 2025 · Fotograf nicht genannt · 1440 px</span></div><img src="{b_giessen}" alt="Sauce wird über einen Teller gegossen" loading="lazy"></div>
  {satz('So sieht ein Culinarium-Abend aus, wenn ihn jemand fotografiert. Auf Instagram liegt er zwischen zwei Plakaten, ohne Namen und ohne Link.', 22)}</div>
</section>'''

    plakate = ''.join(f'<figure data-a="auf" style="--i:{i}"><img src="{s}" alt="{e(t)}" loading="lazy"><figcaption>{t}</figcaption></figure>'
                      for i, (s, t) in enumerate([(b_mond, 'Mondfrau · 09/2026 · Akzent Sepia #553827'), (b_panther, 'Panther mit Eisbecher · 03/2026 · Ochsenblut #881301'), (b_kuerbis, 'Kürbis-Pin-up · 11/2025 · Nachtblau #15354A')]))
    seite = blatt(3, 'seite', 'Die heutige Seite', ['Ein Profil,', 'das wie eine Sammlung aussieht.'],
                  'Eine Website gibt es nicht. Abgelesen ist das Instagram-Profil am 25. Oktober 2026, am Rechner und am Handy, ohne Anmeldung, optionale Cookies abgelehnt.',
                  tab(['Punkt', 'Stand', 'Beleg'], [
                      ['Technik', 'keine Website, nur Instagram', B('Profil; DENIC 24.10.2026')],
                      ['Profil', '«Food Pairing | Schulungen | Events | Consulting» · «CULINARIUM a unique experience» · drei Team-Konten', B('Profil 25.10.2026')],
                      ['Reichweite', '1.079 Follower, 28 Beiträge, 8 Story-Highlights · zweimal abgelesen (24. und 25.10.)', B('_qa/spaeher/ig-profil-rechner.txt')],
                      ['Link in der Bio', OFFEN('keiner'), B('Profil 25.10.2026')],
                      ['Takt', 'ein eigener Beitrag alle 3 bis 5 Monate, nur zu Terminen', B('Kundenprofil Blatt 7')],
                      ['Bilder', 'Instagram-Fassungen 1440 px, Plakate bis 2014 × 2003 px', B('_quelle-bilder/')],
                      ['Handy', 'Bio und erste Beiträge sichtbar, danach Anmeldefenster', B('_qa/spaeher/ig-profil-handy.jpg')],
                      ['Sprachen', 'nur Deutsch', B('Beiträge')],
                      ['Buchung', 'Nachricht, dann PayPal-Vorkasse · «nicht rückerstattet»', B(IG('DbYnkdkjrNy'))],
                      ['Rechtstexte', OFFEN('Impressum, Datenschutz, AGB, Widerruf: keine'), B('Profil; Kundenprofil Blatt 1')],
                      ['Newsletter, Warteliste, Gutschein', OFFEN('keine'), B('Profil, Beiträge')],
                      ['Google', OFFEN('kein Eintrag') + ' · die Suche zeigt u. a. Culinar Herrenhausen', B('Google Maps, 25.10.2026')],
                      ['Fehler', '«Hasemannstrasse», «@rudi_san», «3-Gange», «in vollen Zugen», März-Datum «/25»', B(IG('DbYnkdkjrNy') + '; Kundenprofil Blatt 5')],
                  ]) + satz('<b>Was der Auftritt gut macht:</b> Die Marke ist fertig. Jedes Plakat seit 2023 folgt demselben System, wechselnde Illustration oben, darunter das warmweisse Band mit der doppelt gerahmten Wortmarke und «A UNiQUE EXPERiENCE BY MOMO X RUDI». Zwei feste Farben, eine Akzentfarbe je Abend. Das Raster sieht aus wie eine Sammlung. Daran misst sich alles, was wir bauen.', 26)
                  + f'<div class="bf-plakate">{plakate}</div>', 'fl--papier')

    fehlt = blatt(4, 'fehlt', 'Was fehlt', ['Was der Gast', 'heute nicht findet.'],
                  'Die Nachfrage ist da, die Abende sind ausgebucht. Was fehlt, ist alles, was nach dem Plakat kommt.',
                  liste([('Eine Adresse', 'Kein Link in der Bio, keine Domain, nichts, was man weitergeben kann.'),
                         ('Ein Buchungsweg', 'Nachricht schreiben, PayPal, kein Beleg, keine Warteliste. Wer zu spät kommt, ist weg.'),
                         ('Ein Kalender', 'Termine stehen nur in Bildunterschriften. Heute ist kein nächster Abend angekündigt.'),
                         ('Rechtstexte', 'Kein Impressum, kein Datenschutz, keine AGB, obwohl Geld fliesst und die Stornoregel streng ist.'),
                         ('Google', 'Wer «Culinarium Hannover» sucht, findet Culinar Herrenhausen, Bad Nenndorf oder Berlin.'),
                         ('Das Angebot jenseits der Abende', '«Schulungen, Events, Consulting» stehen im Profilnamen. Belegt ist nur die Schulung als Teil des Abends.'),
                         ('Die Köpfe', 'Über Rudi und Momo gibt es ausserhalb von Instagram keine Zeile.')]), 'fl--nacht')

    ausmacht = blatt(5, 'ausmacht', 'Was das Haus ausmacht', ['Jeder Drink', 'wird erklärt.'],
                     'Zwei Leute an einer langen Tafel. Rudi kocht vegetarisch, Momo mixt zu jedem Gang einen Drink und erklärt ihn persönlich, mit Techniken, die in Hannover sonst niemand vorführt.',
                     liste([('Die Küche', 'Rudis Gerichte heissen wie ihre Zutaten: «AUBERGINE / KOKOS / LIMETTE / SESAM». Vegetarisch als Standard, im Dezember 2025 einmal mit Ente.'),
                            ('Die Bar', 'Fatwashing, Milkwashing, Klärung mit Enzymen. Kein Wettbewerber in Hannover bewirbt das (Kundenprofil Blatt 8).'),
                            ('Der Ort', 'Nachbarschafts-Mixology-Bar in Linden, ehemaliges Fussballlokal, Möbel aus Kirchenbänken, die Tafel auf einer kleinen Empore.'),
                            ('Der Weg', 'Vom Pop-up für 59 bis 80 EUR im Jahr 2023 zum ausgebuchten Abend für 89 EUR im Jahr 2026.'),
                            ('Die Plakate', 'Jeder Abend hat sein eigenes Motiv. Die Reihe sammelt sich wie Ausgaben eines Magazins.')]), 'fl--papier')

    fenster2 = f'''<section class="fl fl--papier blatt" style="padding-top:0">
  <div class="in"><div class="fen" data-a="schweb"><div class="fen__k"><i></i><i></i><i></i><span>Die Tafel · Juli 2024 · Foto Irina Voronov</span></div><img src="{b_tafel}" alt="Gedeckter Platz mit Menükarte an der Tafel" loading="lazy"></div>
  {satz('Die Menükarte liegt schon auf dem Teller. Profi-Fotos gibt es, nur gehören sie den Fotografen, nicht dem Haus.', 22)}</div>
</section>'''

    fam = [('Culinarium Hannover', 'Abende im Walk on the Wild Side', 'Rudolf Napieraj · Momo · Derya Ivkin', 'Instagram 1.079 Follower · keine Website', HEUTE, b_teller),
           ('Walk on the Wild Side', 'Haasemannstraße 13, 30449 Hannover', 'Derya Ivkin laut eigener Bio «Bar Owner» · gegründet 2017 von Elbert/Schindler', 'Instagram 2.678 Follower · Google 4,8 · keine Website', 'https://www.instagram.com/walkonthewildside_hannover/', b_bar),
           ('Dirty Chicken Hannover', '«Pop up coming soon»', 'Rudolf Napieraj', 'Instagram 297 Follower, 4 Beiträge · keine Website', 'https://www.instagram.com/dirtychicken.hannover/', b_dirty)]
    karten = ''.join(f'<a href="{e(w)}" target="_blank" rel="noopener" data-a="auf"><img src="{img}" alt="{e(n)}" loading="lazy"><div><b>{e(n)}</b><small>{e(o)}<br>{e(g)}<br>{e(s)}</small></div></a>' for n, o, g, s, w, img in fam)
    familie = blatt(6, 'familie', 'Familie und weitere Häuser', ['Eine Bar,', 'ein Pop-up.'],
                    'Drei Namen, kein gemeinsamer Rechtsträger. Die Bar ist die Bühne, Dirty Chicken ist Rudis zweites Projekt. Gebaut hat Robert noch keines davon.',
                    f'<div class="bf-fam">{karten}</div>'
                    + zwei('Was geprüft ist', ['Derya Ivkins Bio: «Bar Owner @walkonthewildside_hannover», «Food Pairing @culinarium_hannover» (25.10.2026)', 'Rudis Bio verlinkt Culinarium und Dirty Chicken (25.10.2026)', 'Bar bei Google: 4,8, ohne Website, +49 163 3909578', 'Kein Ordner zu den dreien in Website-Projekte'],
                           'Was offen bleibt', ['Wer die Bar heute betreibt: im Register ' + OFFEN('nicht belegt'), 'Ob Dirty Chicken mitkommt (Robert bot im Sommer beides an)', 'Abgrenzung zum Private Dining der Bar am selben Tisch (bis 12 Personen, 89 EUR)', 'Bilder der Bar und von Dirty Chicken: aus deren Profilen, nur zur Zuordnung']), 'fl--nacht')

    noten = blatt(7, 'noten', 'Noten', ['Kein Eintrag,', 'aber volle Tische.'],
                  'Abgelesen am 25. Oktober 2026, nur abgelesen. Culinarium selbst hat keine Bewertungen, weil es nirgends eingetragen ist.',
                  tab(['Quelle', 'Note', 'Anzahl'], [['Google, Culinarium', OFFEN('kein Eintrag'), '–'],
                                                     ['Google, Walk on the Wild Side', '4,8', 'nicht angezeigt · 76 laut Restaurant Guru, 24.10.2026'],
                                                     ['Booking, TripAdvisor', 'nicht gelistet', '–'],
                                                     ['Facebook, Bar', '4,2 laut Restaurant Guru · ' + OFFEN('an der Quelle nicht geprüft'), '10'],
                                                     ['Auszeichnung', 'Falstaff 89 Punkte 2026 für die Bar laut Drittlisting · ' + OFFEN('an der Quelle nicht geprüft'), '–'],
                                                     ['Stimmen', '@hannover_eats Reel 12/2025 «Werbung | Einladung» · @luisaverfuerth 04/2024', '5.404 Aufrufe']]), 'fl--papier')

    widerspruch = blatt(8, 'widersprueche', 'Widersprüche zur Recherche', ['Was sich seit gestern', 'geklärt hat.'],
                        'Die Recherche vom 24. Oktober konnte Instagram und Google Maps nicht öffnen. Heute ging beides, ohne Anmeldung.',
                        liste([('Derya Ivkin', 'Recherche: «Rolle in der Bio nicht benannt». Heute in ihrer Bio: «Bar Owner» und «Food Pairing @culinarium_hannover». Eigene Angabe, kein Registerbeleg.'),
                               ('Dirty Chicken', 'Recherche: «im Web nicht auffindbar». Es gibt das Konto @dirtychicken.hannover, verlinkt aus Rudis Bio.'),
                               ('Google', 'Recherche: nicht prüfbar. Heute: kein Eintrag für Culinarium, die Bar mit Eintrag ohne Website.'),
                               ('Plätze', '14 pro Abend laut Beiträgen gegen 8 bis 12 für die Tafel laut Verzeichnissen. Bleibt offen.')]), 'fl--nacht')

    empfehlung = f'''<section class="schluss" id="empfehlung">
  <img class="schluss__b" src="{b_schluss}" alt="Plakat zum September-Abend mit zwei Gläsern unter einer Wolke aus Lichtern" loading="lazy">
  <div class="in">
    {kap(9, 'Empfehlung')}
    <p class="bf-urteil" data-a="auf">Passt, als Auftrag. <em>Drei Fragen zuerst.</em></p>
    <div class="lauf">
      <p data-a="worte">Robert hat es ausdrücklich gewollt, deshalb gilt der Zielmarkt Schweiz hier nicht. Kleinstes inhabergeführtes Format, keine Kette. Der Auftritt ist viel schwächer als die Sache: eine fertige Marke und ausgebuchte Abende ohne Adresse, ohne Buchung, ohne Impressum. Material ist da, kein Relaunch läuft, die Domain ist frei.</p>
      <p data-a="worte">Vor dem Bau klärt Robert im Gespräch: wer Vertragspartner ist und ins Impressum kommt, wem Fotos, Illustrationen und Schrift gehören, und wie Culinarium zur Bar steht. Bis dahin arbeitet die Kette mit dem, was Rudi geschickt hat.</p>
    </div>
    <div class="kn-reihe" data-a="auf">{kn('Instagram öffnen', HEUTE, neu=True)}{kn('Zur Karte der Kette', KARTE, 'kn--linie')}</div>
  </div>
</section>'''

    haupt = auftakt + haus + agentur + fenster1 + seite + fehlt + ausmacht + fenster2 + familie + noten + widerspruch + empfehlung
    html = K.rahmen('Befund', 'Station 2 der Kette: Befund des Spähers zu Culinarium Hannover.', 'Befund', haupt,
                    'Befund von Robert Reff, Tasty Studios, für die interne Kette. Fotos, Plakate und Texte gehören ' + H.RECHTE)
    html = html.replace('../werkbank/', 'werkbank/')
    html = html.replace(f'<a class="glanz" href="werkbank/index.html">Zur Werkbank{PF}</a>', f'<a class="glanz" href="{HEUTE}" target="_blank" rel="noopener">Instagram{PF}</a>')
    html = html.replace('<a class="insel__m" href="werkbank/index.html">', '<a class="insel__m" href="#">')
    html = html.replace('<html lang="de-CH">', '<html lang="de">')
    K.schreib(os.path.join(HIER, 'befund.html'), html)
    print('befund.html geschrieben,', len(html) // 1024, 'KB')


if __name__ == '__main__':
    baue()
