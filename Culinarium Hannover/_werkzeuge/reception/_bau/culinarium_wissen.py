#!/usr/bin/env python3
"""Wissen des Chats für La Réception des Culinarium Hannover (28.10.2026). Muster: _bau/schaefli_wissen.py der Taverne zum Schäfli (nur gelesen).
Liest nur, aus dem Projektordner:
  _werkzeuge/reception/_bau/website-text/*.txt   Wortlaut der Website, wie ein Gast ihn sieht (node _bau/website_text.js, ohne Beispieltermine)
  _quelle/extern/ig/beitraege.md                 der Beitrag zum letzten Abend (Vorverkauf, Rückgabe), Wortlaut
  _kette/03-sammler/fakten.json                  Kontaktwege, Plus Code, Instagram (jede Zeile mit ihrer Quelle)
Schreibt: gast/gast_wissen.txt, gast/gast_umgebung.txt, gast/gast_haus.json und vorlagen/*.txt.
Nichts wird abgetippt oder umformuliert; jeder Satz, den dieses Skript für Vorlagen und Umgebung übernimmt, muss wörtlich in der Quelle stehen,
sonst bricht es ab. «Vegetarisch» kommt nicht ins Wissen (Rückmeldung Rudi 26.10.2026: nicht mehr rein vegetarisch, CHARAKTER.md Abschnitt 8).
Die Beispieltermine und die gespielte Zahlung auf «Der Abend» («Vorschau · Termine und Zahlung sind nur simuliert») sind keine Angaben des Hauses
und bleiben draussen. Fehlt etwas, fehlt es auch im Chat und der Chat verweist an das Team.
Aufruf: python3 _werkzeuge/reception/_bau/culinarium_wissen.py   (nach neuen Quellen erneut, danach steckbrief_bau.py)"""
import json, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))     # _werkzeuge/reception
PROJ = os.path.dirname(os.path.dirname(C))
WT = os.path.join(C, '_bau', 'website-text')
ZIEL = os.path.join(C, 'gast')
SEITEN = [('index', 'Startseite'), ('abend', 'Der Abend (Culinarium, Warteliste)'), ('abende', 'Alle Abende'), ('bar', 'Das Haus: Walk on the Wild Side'),
          ('leute', 'Team'), ('weg', 'Der Weg'), ('dirty-chicken', 'Dirty Chicken (Pop-up)')]
NAV = {'Zum Inhalt', 'Der Abend', 'Alle Abende', 'Das Haus', 'Team', 'Der Weg', 'Dirty Chicken', 'Warteliste', 'Menü', 'Startseite'}
FUSS_ANFANG = 'Ein Menü, fünf passende Drinks, eine lange Tafel.'


def seite(n):
    roh = open(os.path.join(WT, n + '.txt'), encoding='utf-8').read()
    kopf, _, rumpf = roh.partition('\n\n')
    abgerufen = (re.search(r'^Abgerufen: (.+)$', kopf, re.M) or [None, ''])[1]
    zeilen = rumpf.splitlines()
    while zeilen and zeilen[0] in NAV:      # Leiste oben
        zeilen.pop(0)
    if FUSS_ANFANG in zeilen:               # Fuss: steht auf jeder Seite gleich, einmal als eigener Teil
        i = zeilen.index(FUSS_ANFANG)
        while i and zeilen[i - 1] in ('Culinarium', 'CULINARIUM'):
            i -= 1
        zeilen, fuss = zeilen[:i], zeilen[i:]
    else:
        fuss = []
    text = '\n'.join(z for z in zeilen if not re.fullmatch(r'[‹›+−]|\d{1,2}', z))
    return text, fuss, abgerufen


def muss(satz, quelle_text, wo):
    if satz not in quelle_text:
        sys.exit(f'FEHLT · «{satz[:80]}» steht nicht in {wo}. Nichts geschrieben.')
    return satz


def bau():
    os.makedirs(ZIEL, exist_ok=True)
    os.makedirs(os.path.join(C, 'vorlagen'), exist_ok=True)
    teile, fuss, alles = [], [], ''
    for n, titel in SEITEN:
        t, f, ab = seite(n)
        fuss = fuss or f
        alles += '\n' + t
        teile.append(f'=== Seite: {titel} · Culinarium Hannover (Website: {n}.html; Wortlaut wie auf der Seite, abgerufen {ab}) ===\n{t}')
    teile.append('=== Seite: Das Haus, Fenster beim Scrollen (Website: bar.html) ===\nDas ganze Haus auf seiner eigenen Seite.\n'
                 + muss('Konzerte am Donnerstag, SESSION mit DJs an den Decks, Gastschichten, Anlässe und die lange Tafel für eure eigene Feier.',
                        open(os.path.join(PROJ, 'website', 'bar.html'), encoding='utf-8').read(), 'bar.html'))
    teile.append('=== Fuss jeder Seite (Culinarium, das Haus, das Pop-up, Warteliste) ===\n' + '\n'.join(fuss))
    alles += '\n' + '\n'.join(fuss)
    if re.search(r'vegetar', '\n'.join(teile), re.I) and not re.search(r'Alle Abende', '\n'.join(teile)):
        sys.exit('PRUEF · «vegetarisch» ausserhalb der Geschichte der Abende.')
    wissen = '\n\n'.join(teile) + '\n'

    # Umgebung: Wege zum Ticket und zum Team, Lage (fakten.json und der Beitrag zum letzten Abend, Wortlaut)
    ig = open(os.path.join(PROJ, '_quelle', 'extern', 'ig', 'beitraege.md'), encoding='utf-8').read()
    fk = json.load(open(os.path.join(PROJ, '_kette', '03-sammler', 'fakten.json'), encoding='utf-8'))
    vv = muss('Tickets ausschließlich per Vorverkauf über PayPal.', ig, 'beitraege.md (DbYnkdkjrNy)')
    nachr = muss('Schreibt uns hierzu gerne eine Nachricht', ig, 'beitraege.md (DbYnkdkjrNy)')
    rueck = muss('Da die Plätze begrenzt sind, bitten wir um Verständnis, dass Tickets nicht rückerstattet werden können.', ig, 'beitraege.md (DbYnkdkjrNy)')
    plus = muss('9PC7+49 Hannover', alles, 'der Website (weg.html)')
    bar_tel = muss('+49 163 3909578', alles, 'der Website (Fuss)')
    res = muss('Reservieren geht per Nachricht oder Telefon.', alles, 'der Website (bar.html)')
    if fk['telefon']['wert'] is not None or fk['mail']['wert'] is not None:
        sys.exit('PRUEF · fakten.json kennt jetzt Telefon oder Mail von Culinarium: Umgebung neu schreiben.')
    umgebung = f"""=== Tickets für einen Abend (Beitrag von @culinarium_hannover zum Abend am 25. und 26. September 2026, veröffentlicht 29.07.2026, Wortlaut) ===
{vv}
{nachr} (gemeint: eine Nachricht an @culinarium_hannover auf Instagram)
{rueck}

=== Kontakt (Recherche des Hauses, 25.10.2026, _kette/03-sammler/fakten.json) ===
Culinarium hat keine eigene Telefonnummer und keine eigene E-Mail-Adresse. Fragen zu einem Abend: eine Nachricht an @culinarium_hannover auf Instagram.
Die Bar Walk on the Wild Side, in der Culinarium stattfindet: Telefon {bar_tel}. {res}
Instagram: @culinarium_hannover (Culinarium), @walkonthewildside_hannover (die Bar), @dirtychicken.hannover (Dirty Chicken).

=== Lage (Google Maps, 25.10.2026) ===
Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover (Linden-Mitte), Ecke Rampenstraße. Plus Code {plus}.
Weitere Angaben zur Anreise (Haltestelle, Parkplatz) stehen in keiner Quelle des Hauses.
"""
    kontakt = f'der Bar unter {bar_tel} oder mit einer Nachricht an @culinarium_hannover auf Instagram'
    haus = {
        'name': 'Culinarium', 'ort': 'Hannover-Linden', 'tel': bar_tel, 'mail': '', 'kontakt': kontakt,
        'adresse': 'Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover',
        'zeiten': 'Culinarium an einzelnen Wochenenden, Freitag ab 19 Uhr und Samstag ab 17 Uhr; die Bar Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr',
        'art': 'Food-Pairing-Abende an der langen Tafel in der Bar Walk on the Wild Side: drei Gänge, fünf Signature Drinks, vierzehn Plätze',
        'ruhetage': 'Culinarium gibt es nur an einzelnen Wochenenden (Freitag ab 19 Uhr, Samstag ab 17 Uhr), der nächste Termin steht noch nicht fest; die Bar hat Sonntag bis Mittwoch geschlossen',
        'fahrplan': '', 'kategorien': [], 'orte': [],
        'reservation': '/abend.html#warteliste', 'reservation_name': 'Warteliste',
        'muster': ('Frage: Wann ist der nächste Abend?\nAntwort: Der nächste Termin steht noch nicht fest. Wer auf der Warteliste steht, erfährt ihn zuerst.\n'
                   '- Freitag: ab 19 Uhr\n- Samstag: ab 17 Uhr\n- Plätze: vierzehn an einer Tafel\n\n'
                   'Frage: Habt ihr einen Kinderstuhl?\nAntwort: Dazu steht nichts in meinen Unterlagen. Frag am besten direkt:\n'
                   f'- Telefon der Bar: {bar_tel}\n- Instagram: @culinarium_hannover'),
    }
    # Vorlagen der Briefe: was das Haus selbst schreibt (E31), Wortlaut der Website
    abend_t = seite('abend')[0]; start_t = seite('index')[0]; bar_t = seite('bar')[0]
    bar_html = open(os.path.join(PROJ, 'website', 'bar.html'), encoding='utf-8').read()   # das Fenster der Bar-Seite zeigt seinen Satz erst beim Scrollen
    js = open(os.path.join(PROJ, 'website', 'assets', 'culinarium.js'), encoding='utf-8').read()
    danke = muss("'Danke, ' + fName.value.trim()", js, 'website/assets/culinarium.js (Warteliste)')
    vorlagen = {
        'warteliste': [muss('Vierzehn Plätze an einer Tafel, und der letzte Abend war ausgebucht. Trag dich ein: Sobald der nächste Termin feststeht, erfährst du es vor allen anderen.', abend_t, 'abend.html'),
                       'Bestätigung des Formulars auf der Website: «Danke, [Name]. Du stehst auf der Liste: [Tag], [Personen].»' if danke else '',
                       muss('Tickets gibt es bisher nur im Vorverkauf. Sobald der nächste Abend feststeht, erfahren es die zuerst, die auf der Warteliste stehen.', start_t, 'index.html')],
        'abend': [muss('Tickets gibt es bisher nur im Vorverkauf. Sobald der nächste Abend feststeht, erfahren es die zuerst, die auf der Warteliste stehen.', start_t, 'index.html'),
                  muss('Das Menü wechselt mit jedem Abend. Was genau kommt, steht auf der Karte an deinem Platz.', start_t, 'index.html'),
                  muss('„Da die Plätze begrenzt sind, bitten wir um Verständnis, dass Tickets nicht rückerstattet werden können.“', start_t, 'index.html'),
                  vv + ' ' + nachr + '.'],
        'feier': [muss('Konzerte am Donnerstag, SESSION mit DJs an den Decks, Gastschichten, Anlässe und die lange Tafel für eure eigene Feier.', bar_html, 'bar.html (Fenster «Das ganze Haus auf seiner eigenen Seite.»)'),
                  muss('Dazu Gastschichten, Konzerte, DJ-Abende und private Abende an der langen Tafel.', start_t, 'index.html'),
                  muss('Reservieren geht per Nachricht oder Telefon.', bar_t, 'bar.html')],
    }
    open(os.path.join(ZIEL, 'gast_wissen.txt'), 'w', encoding='utf-8').write(wissen)
    open(os.path.join(ZIEL, 'gast_umgebung.txt'), 'w', encoding='utf-8').write(umgebung)
    json.dump(haus, open(os.path.join(ZIEL, 'gast_haus.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for alt in os.listdir(os.path.join(C, 'vorlagen')):
        if alt.endswith('.txt') and alt[:-4] not in vorlagen:
            os.remove(os.path.join(C, 'vorlagen', alt))
    for k, z in vorlagen.items():
        open(os.path.join(C, 'vorlagen', k + '.txt'), 'w', encoding='utf-8').write('\n\n'.join(x for x in z if x) + '\n')
    print(f'gast_wissen.txt {len(wissen) // 1024} kB · gast_umgebung.txt {len(umgebung)} Zeichen · gast_haus.json · vorlagen: {", ".join(vorlagen)}')


if __name__ == '__main__':
    bau()
