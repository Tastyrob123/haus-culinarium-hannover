#!/usr/bin/env python3
"""Sammlung des Sammlers (Station 3) für Culinarium Hannover, gebaut mit dem Werkbank-Kit.
   python3 bau_sammlung.py   → sammlung.html + werkbank/ + bilder/ in diesem Ordner.
   Inhalt aus fakten.json, sprachen.json, stand.json und _quelle/ (25.10.2026). Zahlen des Vorrats werden beim Bau im Ordner gezählt.
   Vorlage: Hotel Alpenhof Weisstannen, _kette/03-sammler/bau_sammlung.py. Es gibt keine Website: Quellen sind Instagram, Portale der Bar, Presse."""
import json, os, sys, re
HIER = os.path.dirname(os.path.abspath(__file__))
os.environ['HAUS'] = HIER
sys.path.insert(0, os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit'))
import kern as K
from kern import H, e, kn, titel, kap, PF

PROJ = os.path.dirname(os.path.dirname(HIER))
QU = os.path.join(PROJ, '_quelle')
FAKT = json.load(open(os.path.join(HIER, 'fakten.json'), encoding='utf-8'))
SPR = json.load(open(os.path.join(HIER, 'sprachen.json'), encoding='utf-8'))
HEUTE = 'https://www.instagram.com/culinarium_hannover/'
MAT = '../../_quelle/material.html'
PROMPT = '../../Prompt%20%E2%80%94%20Culinarium%20Hannover.md'
BEFUND = '../02-spaeher/befund.html'
O = '<span class="bf-offen">offen</span>'
BILD = ('.jpg', '.jpeg', '.png', '.webp')


def bild(rel, ziel, breite=1600, schnitt=None, lage=(.5, .5), dunkel=None):
    quelle = os.path.join(QU, rel)
    z = os.path.join(HIER, 'bilder', ziel + '.webp')
    os.makedirs(os.path.dirname(z), exist_ok=True)
    if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(quelle):
        K.webp(quelle, z, breite, q=80, schnitt=schnitt, lage=lage, dunkel=dunkel)
    return 'bilder/' + ziel + '.webp'


def zaehl(rel, endungen=BILD):
    p = os.path.join(QU, rel)
    if not os.path.isdir(p):
        return 0
    return sum(1 for f in os.listdir(p) if f.lower().endswith(endungen))


def beitraege(rel):
    p = os.path.join(QU, rel, 'beitraege.md')
    return len(re.findall(r'^## ', open(p, encoding='utf-8').read(), re.M)) if os.path.exists(p) else 0


def muster():
    vb, innen = H.ZEICHEN
    w, h = [float(x) for x in vb.split()[2:]]
    s = 30 / w
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">'
           f'<g fill="none" stroke="#d4b483" stroke-opacity=".10" stroke-width="1"><path d="M0 .5H240M.5 0V240"/></g>'
           f'<g fill="#d4b483" fill-opacity=".09" transform="translate({120 - 15} {120 - h * s / 2}) scale({s})">{innen}</g></svg>')
    open(os.path.join(HIER, 'werkbank', 'muster.svg'), 'w').write(svg)


def b(t):
    return f'<span class="bf-beleg">{t}</span>'


def tab(kopf, zeilen):
    return ('<table class="bf-tab" data-a="auf"><thead><tr>' + ''.join(f'<th>{k}</th>' for k in kopf) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in z) + '</tr>' for z in zeilen) + '</tbody></table>')


def blatt(i, ident, name, zeilen, text, innen, fl):
    return f"""<section class="fl {fl} blatt" id="{ident}">
  <div class="in">
    {K.kopf(i, name, zeilen, text)}
    {innen}
  </div>
</section>"""


def fenster(img, satz, kopfzeile, alt, fl='fl--nacht'):
    return f"""<section class="fl {fl} blatt" style="padding-top:0">
  <div class="in"><div class="fen" data-a="schweb"><div class="fen__k"><i></i><i></i><i></i><span>{kopfzeile}</span></div><img src="{img}" alt="{alt}" loading="lazy"></div>
  <div class="lauf" style="margin-top:22px"><p data-a="worte">{satz}</p></div></div>
</section>"""


def baue():
    K.gestaltung()
    muster()
    b_mond = bild('extern/ig/2026-07-29_culinarium_hannover_DbYnkdkjrNy-1.jpg', 'plakat-mondfrau', 1100)
    b_tafel = bild('extern/ig-fotografen/2024-07-24_voronov_irina_C9z2rj1MRb2-8.jpg', 'tafel-voronov', 1400)
    b_teller = bild('extern/ig-team/2026-10-23_rudi__san_De1pn9ttMoX-1.jpg', 'teller-aubergine', 900)
    b_schaum = bild('vom-kunden/63875.jpg', 'rudi-tafel-mail', 1800, schnitt=4 / 3, lage=(.5, .5))
    b_recap = bild('extern/ig/2025-02-04_culinarium_hannover_DFqZn2UMYMV-1.jpg', 'recap-giessen', 1600, schnitt=4 / 3, lage=(.5, .5))
    b_panther = bild('extern/ig/2026-03-06_culinarium_hannover_DVjkofijp6R-1.jpg', 'plakat-panther', 900, schnitt=4 / 5)
    b_kuerbis = bild('extern/ig/2025-10-13_culinarium_hannover_DPwlqcfiKcA-1.jpg', 'plakat-kuerbis', 900, schnitt=4 / 5)
    b_nacht = bild('walk-on-the-wild-side/portale/neotaste_3.jpeg', 'bar-dunkel', 1600, dunkel=(.45, .62))

    streu = ''.join(f'<div class="abzug" data-a="schweb" style="left:{x}%;top:{y}%;width:{w}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}"><img src="{s}" alt=""></div>'
                    for i, (s, x, y, w, r) in enumerate([(b_tafel, 2, 6, 58, -2.5), (b_mond, 48, 26, 44, 2.5), (b_teller, 12, 54, 30, -1.5)]))
    auftakt = f"""<section class="sk">
  <div class="in">
    <div>
      {kap(3, 'Sammler · Recherche')}
      {titel(['Alles, was es', 'über Culinarium gibt.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">Culinarium hat keine Website. Gesammelt ist alles, was es gibt: Rudis eigene Fotos und Filme aus Mail und Drive, alle Instagram-Beiträge seit 2023 und alle acht Highlights, die Fotografen, die Bar mit 55 Google-Fotos, Falstaff, TripAdvisor und Presse, und die Wortmarke als Vektor. Jede Angabe mit Quelle, was noch fehlt, in Rot mit dem Handgriff, der es löst. Stand 26. Oktober 2026.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Material ansehen', MAT)}{kn('Zu den Lücken', '#luecken', 'kn--linie')}</div>
    </div>
    <div class="auslage" aria-hidden="true">{streu}</div>
  </div>
</section>"""

    zeilen = [
        ['Rudis Dateien', f'{zaehl("vom-kunden")} Mail-Anhänge · {zaehl("vom-kunden/drive")} Drive-Bilder · 1 Film · {zaehl("vom-kunden/drive", (".arw",))} RAW', 'zwei Mails vom 24.10.2026, Drive in Roberts Chrome geladen; Bilder bis 4096 × 3072, Film 1920 × 1080', 'Kunde; Fotografen je Datei ' + O],
        ['Instagram Culinarium', f'{beitraege("extern/ig")} Beiträge · {zaehl("extern/ig")} Bilder · {zaehl("video/hotel-kanal", (".mp4",))} Filme', 'alle eigenen Beiträge seit 09/2023: Plakate 1440 px (Mondfrau 2014 × 2003), gedruckte Menükarten 2023, Recaps', 'Culinarium; Illustrationen: Herkunft ' + O],
        ['Instagram-Highlights', f'{zaehl("extern/ig-highlights")} Bilder · {zaehl("extern/ig-highlights", (".mp4",))} Filme', 'alle 8 Highlights 2023–2026, 1170 × 2080, über Roberts Anmeldung', 'Culinarium; Reposts Dritter möglich'],
        ['Team', f'{beitraege("extern/ig-team")} Beiträge · {zaehl("extern/ig-team")} Bilder · 1 Film', 'Rudi (@rudi__san): Gerichte, Kochporträt; Momo (@momo012027): Pop-up-Plakate 2023', 'Rudi, Momo; Fotos 2026 von focusonbiz_hannover'],
        ['Fotografen', f'{beitraege("extern/ig-fotografen")} Beiträge · {zaehl("extern/ig-fotografen")} Bilder · 1 Film', 'Irina Voronov 05/2024 und 07/2024, focusonbiz_hannover 05/2026', 'Fotografen. Keine Web-Lizenz'],
        ['Gäste und Creator', f'{beitraege("extern/ig-gaeste")} Beiträge · {zaehl("extern/ig-gaeste")} Bilder · 2 Filme', 'Luisa Verfürth 04/2024, Hannover Eats 12/2025 (ganzes Menü im Text)', 'Gäste. Nur Anschauung'],
        ['Logo', f'{zaehl("logo/nachgezogen", (".png",))} PNG · {zaehl("logo/nachgezogen", (".svg",))} Vektoren', 'Logo-Datei 1080 × 1080 (Profilbild), daraus und aus dem 2014-px-Plakat als Vektor nachgezogen, 4000 px', 'Culinarium; Original-Vektor ' + O],
        ['Bar: Google', f'{zaehl("walk-on-the-wild-side/google-maps")} Fotos · 75 Rezensionen gelesen', 'Google-Eintrag der Bar, bis 4284 × 5712', 'Google-Nutzer bzw. Bar. Nur Anschauung'],
        ['Bar: Instagram vollständig', f'82 Beiträge · {zaehl("walk-on-the-wild-side/ig")} + {zaehl("walk-on-the-wild-side/ig-dritte")} Bilder · {zaehl("walk-on-the-wild-side/video", (".mp4",))} Filme', 'alle Beiträge seit dem Reopening 09.11.2023 und alle 4 Highlights: Sip & Sound, Gastschichten, Konzerte, Silvester, Valentinstag mit Rudi, Kiezfeste', 'Bar; Mitautoren je Bild in herkunft.json'],
        ['Bar: Facebook', f'{zaehl("walk-on-the-wild-side/facebook")} Fotos', 'Seite «Walk on the Wildside», 2017–2025, bis 2048 px', 'Bar. Nur mit Freigabe'],
        ['Das Dach', 'dach.md', 'Wild Side als Hauptgeschäft, Culinarium und Dirty Chicken darunter; Übergabe Elbert → Ivkin Ende 2023 (Neue Presse, HAZ)', 'Belege je Verbindung'],
        ['Bar: Instagram, Portale, Presse', f'{zaehl("walk-on-the-wild-side/ig")} + {zaehl("walk-on-the-wild-side/portale")} + {zaehl("walk-on-the-wild-side/ig-dritte")} Bilder · {zaehl("walk-on-the-wild-side/portale", (".md",))} Portaltexte · {zaehl("walk-on-the-wild-side/presse", (".md",))} Presse', 'Falstaff, TripAdvisor, NeoTaste, Restaurant Guru, Essen in Hannover, En Primeur, Pearl, fizzz/Meininger 2018, Thomas Lasser 2017', 'Bar. Nur mit Freigabe der Bar'],
        ['Hannover Prestige', f'{zaehl("extern/portale")} Bild · 1 Text', 'einzige Seite ausserhalb von Instagram, die Culinarium nennt; Foto 1638 × 2048', 'Portal, Fotograf nicht genannt'],
        ['Dirty Chicken', f'{beitraege("dirty-chicken/ig")} Beiträge · {zaehl("dirty-chicken/ig")} Bilder · 2 Filme', '@dirtychicken.hannover, Rudis zweites Projekt', 'Rudi; Fotos focusonbiz_hannover'],
        ['Commons', f'{zaehl("extern/wikipedia-commons")} Bilder', 'Haasemannstraße, bis 4320 px; Nr. 13 ohne eigenes Foto', 'CC BY-SA 4.0, mit Namensnennung'],
        ['Noch gesperrt', '5 Drive-Dateien', '115351, 115442, 115445, 115389, 36541', O + ': Freigabe durch Rudi'],
    ]
    vorrat = blatt(1, 'vorrat', 'Der Vorrat je Quelle', ['Was da ist,', 'und wem es gehört.'],
                   'Gezählt im Ordner _quelle/ beim Bau dieser Seite. Zu jedem Bildordner gibt es eine herkunft.json mit Adresse, Datum, Konto und Mitautoren jedes Bildes, die Texte der Beiträge wörtlich in beitraege.md.',
                   tab(['Quelle', 'Anzahl', 'Herkunft', 'Rechte'], zeilen) +
                   f'<div class="kn-reihe" data-a="auf">{kn("Material-Übersicht öffnen", MAT)}</div>', 'fl--papier')

    boegen = [('vom-kunden_drive', 'Rudis Drive', 'Die eigenen Fotos: Tafel bei Kerzenlicht, Rudi und Momo an der Arbeit, jeder Teller, die Drinks, die Bar von aussen, das Team vor dem Negroni-Schild.'),
              ('vom-kunden', 'Rudis Mail-Anhänge', 'Rudi beim Anrichten, Teller in Serie, Team, Bar von aussen, bis 4096 × 3072.'),
              ('extern_ig', 'Instagram Culinarium', 'Jedes Plakat seit September 2023 mit Datums-Seite, die gedruckten Menükarten, die Recaps.'),
              ('extern_ig-highlights', 'Highlights', 'Das Story-Archiv: Menükarten am Tisch, Gänge, Drinks, Plakate.'),
              ('walk-on-the-wild-side_google-maps', 'Google, die Bar', 'Raum, Decke, Tresen, Drinks, Abende; Fotos von Inhabern und Gästen gemischt.'),
              ('extern_ig-fotografen', 'Fotografen', 'Die Serie von Irina Voronov vom Juli 2024 (Tafel, Raum, Teller, teils mit Polaroid-Rahmen) und das Titelbild des Reels von focusonbiz.'),
              ('extern_ig-team', 'Rudi und Momo', 'Die Pop-up-Plakate 2023 «BY MOMO X CHRISTOPH», Rudis Gerichte 2024 bis 2026, Rudi beim Anrichten.'),
              ('extern_ig-gaeste', 'Gäste', 'Luisa Verfürth im April 2024 mit Menükarte, Hannover Eats im Dezember 2025. Nur Anschauung.'),
              ('walk-on-the-wild-side_portale', 'Die Bar auf Portalen', 'Fassade an der Haasemannstraße, Raum mit Empore, Bar, Tresen.'),
              ('walk-on-the-wild-side_ig', 'Die Bar auf Instagram', 'Valentinstag «WILD SIDE x RUDI IN LOVE», Abende mit Gästen am Plattenteller.')]
    fig = ''.join(f'<figure data-a="auf"><img src="{bild("_boegen/" + k + ".jpg", "bogen-" + k, 1800)}" alt="Bilderbogen {e(t)}" loading="lazy"><figcaption><b>{e(t)}</b>{e(s)}</figcaption></figure>' for k, t, s in boegen)
    bogen = blatt(2, 'boegen', 'Die Bögen', ['Jedes Bild', 'gegen das Haus geprüft.'],
                  'Je Quelle ein Bogen. Bilder von Strassenfesten, die nur die Bar als Mitautorin nennen, sind aussortiert. Gäste und Dritte liegen in eigenen Ordnern und sind nur Anschauung.',
                  f'<div class="sa-boegen">{fig}</div>', 'fl--nacht')

    f1 = fenster(b_schaum, 'Aus Rudis eigenen Dateien, 4096 × 3072 Pixel: doppelt so gross wie alles, was öffentlich zu finden war. Wer fotografiert hat, steht nicht dabei.',
                 'Rudis Mail vom 24.10.2026 · 63875.jpg', 'Foto aus Rudis Dateien')

    noten = blatt(3, 'noten', 'Noten', ['Was andere', 'darüber sagen.'],
                  'Abgelesen am 25. und 26. Oktober 2026, jede an ihrer Quelle. Culinarium selbst hat keinen Eintrag; die Noten gehören der Bar, in der die Abende stattfinden.',
                  tab(['Quelle', 'Note', 'Anzahl', 'Beleg'], [
                      ['Google, Culinarium', 'kein Eintrag', '–', b('Google Maps (Späher)')],
                      ['Google, Walk on the Wild Side', '4,8 von 5 (67 × 5, 4 × 4, 2 × 3, 1 × 2, 1 × 1)', '75, davon 49 mit Text', b('alle 75 gelesen, 26.10.2026')],
                      ['Falstaff, Walk on the Wild Side', '91 Punkte, Bar Guide 2027, Cocktailbar (Drinks 47/50, Style 18/20, Service 18/20, Range 8/10, +2)', '–', b('falstaff-bars-wild-side.md · die Recherche nannte 89 (2026)')],
                      ['NeoTaste, Walk on the Wild Side', '4,8', '40 Bewertungen', b('neotaste.md')],
                      ['TripAdvisor, Bar «Wild Side»', '0 Bewertungen, keine Fotos, Ort falsch «Pattensen»', '0', b('portale/tripadvisor.md')],
                      ['TripAdvisor, Culinarium', 'kein Eintrag', '–', b('Suche 26.10.2026')],
                      ['Booking.com', 'betrifft nicht', '–', b('Abende, kein Haus')]]), 'fl--papier')

    F = FAKT
    def w(x):
        return e(str(x['wert'])) if x.get('wert') is not None else O
    def qq(x):
        q = x.get('quelle')
        if q == 'offen':
            q = 'gesucht: ' + x.get('gesucht', '')
        return b(e(q)[:190])
    pr = ' · '.join(e(p['preis'] + ' (' + p['termin'] + ')') for p in F['preise_ab']['wert'][:3])
    fz = [['Name', w(F['name']), qq(F['name'])], ['Ort', w(F['adresse']), qq(F['adresse'])],
          ['Rechtsträger', O, qq(F['rechtstraeger'])], ['Telefon', O, qq(F['telefon'])], ['Mail', O, qq(F['mail'])],
          ['Der Abend', e(F['restaurants']['wert'][0]['art']) + '<br>' + e(F['restaurants']['wert'][0]['zeiten']), qq(F['restaurants'])],
          ['Plätze', 'je Abend 15 (2023), 20 (Okt. 2023), 12 (2024), 14 (2025); Tafel der Bar «bis zu 14» bzw. «8 bis 12»', b('fakten.json › plaetze')],
          ['Preis', pr, qq(F['preise_ab'])],
          ['Buchung', e(F['buchungsweg']['wert']['system']), qq(F['buchungsweg'])],
          ['Storno', e(F['buchungsweg']['wert']['storno']), b('DVjkofijp6R, DbYnkdkjrNy, DJw8OqGMY1G')],
          ['Rhythmus', w(F['saison']), qq(F['saison'])],
          ['Köpfe', ' · '.join(e(p['name'] + ' (' + p['rolle'][:60] + ')') for p in F['personen']['wert']), qq(F['personen'])],
          ['Fotografen', ' · '.join(e(p['name']) for p in F['fotografen']['wert']) + ' · Karsten Davideit (fizzz 2018)', qq(F['fotografen'])],
          ['Auszeichnung', 'Falstaff 91 Punkte, für die Bar, nicht für Culinarium', qq(F['auszeichnungen'])],
          ['Sprache heute', 'Deutsch', qq(F['sprachen_website'])],
          ['Rechtstexte', 'Impressum, Datenschutz, AGB, Widerruf: keine ' + O, qq(F['rechtstexte'])],
          ['Social', 'Instagram 1.079 Follower, 28 Beiträge; kein Facebook, TikTok, YouTube', qq(F['social'])],
          ['Weitere', 'Bar Walk on the Wild Side (Ort) · Dirty Chicken Hannover (Rudi)', qq(F['weitere_haeuser'])]]
    fakten = blatt(4, 'fakten', 'Fakten mit Quelle', ['Jede Angabe', 'mit ihrer Datei.'],
                   'Auszug aus fakten.json. Preise, Zeiten und Sätze stehen dort wörtlich wie in den Beiträgen; Tippfehler der Beiträge sind vermerkt, nicht übernommen.',
                   tab(['Angabe', 'Wert', 'Quelle'], fz), 'fl--nacht')

    zl = '<ul class="sa-zeit">' + ''.join(f'<li data-a="auf"><b>{e(t["datum"])}</b><div>{e(t["was"])}<small>{e(t["quelle"])}</small></div></li>' for t in F['termine']['wert']) + '</ul>'
    geschichte = blatt(5, 'geschichte', 'Die Abende mit Beleg', ['Vom Pop-up', 'zur ausgebuchten Tafel.'],
                       'Nur Termine, die ein Beitrag nennt. Das Jahr kommt aus dem Veröffentlichungsdatum, wenn der Beitrag es weglässt.',
                       zl, 'fl--papier')
    f2 = fenster(b_recap, 'Das Recap vom Februar 2025 auf dem eigenen Konto. Die Recherche nannte den Fotografen unbekannt; der Beitrag führt Irina Voronov als Mitautorin. Ein Hinweis, kein Beleg.',
                 'Recap 02/2025 · @culinarium_hannover', 'Ein Drink mit Erdbeere, Recap Februar 2025')

    stand = json.load(open(os.path.join(HIER, 'stand.json'), encoding='utf-8'))
    lk = ''.join(f'<li data-a="auf">{e(p["punkt"])}<small>{e(p["wo"])}</small></li>' for p in stand.get('offen', []))
    luecken = blatt(6, 'luecken', 'Lücken', ['Was offen ist,', 'in Rot.'],
                    'Jeder Punkt steht auch in stand.json und auf der Karte. Was nicht öffentlich ist, bleibt offen; nichts davon ist geschätzt.',
                    f'<ul class="sa-luecken">{lk}</ul>', 'fl--nacht')

    nb = [('5 Drive-Dateien', 'Für robert@tasty-studios.de gesperrt. Handgriff: Rudi gibt sie frei, oder du forderst in Drive Zugriff an (geht als Anfrage an Rudi).'),
          ('Logo im Original', 'Geholt: die Logo-Datei in 1080 px und zwei Vektor-Nachzüge in 4000 px (logo/). Es fehlt nur die Datei des Gestalters mit Schriftname. Handgriff: Rudi darum bitten.'),
          ('Meininger', 'Geholt: Artikel 2018 und Bild, aber nur 300 × 200; grösser hat es nur der Verlag (Fotograf Karsten Davideit).'),
          ('Ein Beitrag von 2023', 'CxV8w05oSIZ ist auch angemeldet gelöscht.')]
    sp = SPR
    nicht = blatt(7, 'nicht', 'Was noch fehlt, Rechte, Sprachen', ['Was noch fehlt,', 'und wer es löst.'],
                  'Kein Bild ist nachweislich für eine Website freigegeben: Die Fotos gehören Irina Voronov, focusonbiz_hannover und ungenannten Fotografen, die Herkunft der Plakat-Illustrationen ist offen, Gäste und Dritte sind nur Anschauung, die Bilder der Bar gehören der Bar.',
                  '<ul class="bf-liste">' + ''.join(f'<li data-a="auf" style="--i:{min(k, 6)}"><b>{t}</b>{x}</li>' for k, (t, x) in enumerate(nb)) + '</ul>' +
                  tab(['Sprachen', 'Was', 'Quelle'], [
                      ['Gäste', 'Google: 45 deutsch, 4 englisch (von 49 Texten); Instagram nur deutsch', b('sprachen.json')],
                      ['Auftritt heute', ', '.join(sp['website_heute']), b(e(sp['website_quelle']))],
                      ['Ort', 'Deutsch, Englisch und 19 weitere', b(e(sp['ort_quelle'])[:170])],
                      ['Reihenfolge', ' → '.join(sp['reihenfolge']), b(e(sp['begruendung'])[:170])]]), 'fl--papier')

    paar = f"""<div class="bf-paar">
  <figure data-a="auf"><img src="{b_panther}" alt="Plakat mit Panther und Eisbecher, März 2026" loading="lazy"><figcaption>März 2026: Panther mit Eisbecher, Ochsenblut. 89 EUR.</figcaption></figure>
  <figure data-a="auf" style="--i:1"><img src="{b_kuerbis}" alt="Plakat mit Kürbis-Pin-up, November 2025" loading="lazy"><figcaption>November 2025: Kürbis-Pin-up, Nachtblau. Freitag bei der Ankündigung ausverkauft.</figcaption></figure>
</div>"""

    schluss = f"""<section class="schluss" id="schluss">
  <img class="schluss__b" src="{b_nacht}" alt="Die Bar Walk on the Wild Side am Abend" loading="lazy">
  <div class="in">
    {kap(8, 'Weiter')}
    <p class="bf-urteil" data-a="auf">Das Material liegt. <em>Station 4 kann lesen.</em></p>
    <div class="lauf"><p data-a="worte">Alles liegt in _quelle/ im Projektordner, die Übersicht als Seite, die Fakten in fakten.json, die Gäste-Sprachen in sprachen.json, der Bau-Prompt neben dem Material. Die Lücken oben bleiben offen, bis eine Quelle sie hergibt. Was noch fehlt, liegt bei Rudi.</p></div>
    {paar}
    <div class="kn-reihe" data-a="auf">{kn('Material-Übersicht', MAT)}{kn('Das Dach', '../../_quelle/dach.md', 'kn--linie')}{kn('Bau-Prompt', PROMPT, 'kn--linie')}{kn('Befund', BEFUND, 'kn--linie')}{kn('Instagram heute', HEUTE, 'kn--linie', neu=True)}</div>
  </div>
</section>"""

    haupt = auftakt + vorrat + bogen + f1 + noten + fakten + geschichte + f2 + luecken + nicht + schluss
    html = K.rahmen('Sammlung', 'Station 3 der Kette: Sammlung des Materials zu Culinarium Hannover.', 'Sammlung', haupt,
                    'Sammlung von Robert Reff, Tasty Studios, für die interne Kette. Fotos, Zeichen und Texte gehören ' + H.RECHTE)
    html = html.replace('../werkbank/', 'werkbank/')
    html = re.sub(r'<a [^>]*href="mailto:[^"]*"[^>]*>(.*?)</a>', r'\1', html)
    html = html.replace(f'<a class="glanz" href="werkbank/index.html">Zur Werkbank{PF}</a>', f'<a class="glanz" href="{MAT}">Material{PF}</a>')
    html = html.replace('<a class="insel__m" href="werkbank/index.html">', '<a class="insel__m" href="#">')
    html = html.replace('<html lang="de-CH">', '<html lang="de">')
    K.schreib(os.path.join(HIER, 'sammlung.html'), html)
    print('sammlung.html geschrieben,', len(html) // 1024, 'KB')


if __name__ == '__main__':
    baue()
