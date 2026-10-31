#!/usr/bin/env python3
"""Steckbrief für «Das weiss der Chat» von Culinarium Hannover (28.10.2026, Kopie des Bauskripts der Taverne zum Schäfli; Muster Grand Beau-Rivage).

Jede Zeile: Stichwort, Angabe, Beleg. Der Beleg ist eine Stelle, die wörtlich in `gast/gast_wissen.txt` (Wortlaut der Website) oder
`gast/gast_umgebung.txt` (Tickets laut Instagram, Kontaktwege, Lage) steht; dieses Skript bricht ab, wenn ein Beleg dort nicht vorkommt
oder eine Zahl der Angabe nicht im Umfeld des Belegs steht (nichts abgetippt oder verschönert).
Bewusst NICHT im Steckbrief, weil die Quellen es nicht sagen: Allergien und Unverträglichkeiten (die Website sagt dazu nichts; der Chat gibt die Frage
an das Team, die Küche klärt es), vegetarisch oder vegan (kein Merkmal mehr, Rückmeldung Rudi 26.10.2026), Kinder, Hunde, Barrierefreiheit,
Haltestelle und Parkplatz, Gutscheine, der Termin des nächsten Abends (steht noch nicht fest). Die Beispieltermine auf «Der Abend» sind keine Angaben des Hauses.
«Veranstaltungen» und «Fragen & Antworten» füllt das Team selbst.
Ergebnis: steckbrief.json daneben, gelesen von gedaechtnis.py. Nach jedem neuen Wissen (python3 _bau/culinarium_wissen.py) erneut laufen lassen.
Aufruf: python3 _werkzeuge/reception/steckbrief_bau.py"""
import hashlib, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
WISSEN = os.path.join(HIER, 'gast')
DATEIEN = ('gast_wissen.txt', 'gast_umgebung.txt')

# Bereich → Gruppen → Zeilen (Stichwort, Angabe, Beleg)
S = [
 ('Culinarium', [
  ('Auf einen Blick', [
   ('Was es ist', 'Food-Pairing-Abende an der langen Tafel im Walk on the Wild Side, Hannover-Linden', 'Food-Pairing-Abende an der langen Tafel im Walk on the Wild Side, Hannover-Linden.'),
   ('Am Abend', 'ein Menü mit fünf passenden Drinks an einer langen Tafel', 'ein Menü mit fünf passenden Drinks an einer langen Tafel für vierzehn Gäste'),
   ('Wann', 'an einzelnen Wochenenden, meist ein Freitag und der Samstag danach', 'Culinarium gibt es an einzelnen Wochenenden, meist ein Freitag und der Samstag danach.'),
   ('Beginn', 'Freitag ab 19 Uhr, Samstag ab 17 Uhr', 'Freitags ab 19 Uhr, samstags ab 17 Uhr.'),
   ('Plätze', 'vierzehn an einer langen Tafel', 'Vierzehn Gäste an einer langen Tafel.'),
   ('Seit wann', 'seit 2023: aus einem Pop-up an der Bar sind ausgebuchte Abende geworden', 'Aus einem Pop-up an der Bar sind ausgebuchte Abende geworden.'),
  ]),
 ]),
 ('Der Abend & Warteliste', [
  ('So läuft ein Abend', [
   ('Aperitif', 'zum Ankommen', 'Aperitif', 'zum Ankommen'),
   ('Drei Gänge', 'von Rudi, an jedem Abend neu', 'von Rudi, an jedem Abend neu'),
   ('Fünf Drinks', 'Momos Signature Drinks, passend zum Essen', 'Momos Signature Drinks, passend zum Essen'),
   ('Tasting und Schulung', 'Momo erklärt jeden Drink am Tisch: Fatwashing, Milkwashing, Klärung mit Enzymen', 'Momo erklärt jeden Drink am Tisch: Fatwashing, Milkwashing, Klärung mit Enzymen'),
   ('Das Menü', 'ändert sich mit jedem Abend; was es gibt, steht auf der Karte an deinem Platz', 'Das Menü ändert sich mit jedem Abend.', 'Was genau es gibt, steht auf der Karte an deinem Platz.'),
  ]),
  ('Der nächste Abend', [
   ('Termin', 'steht noch nicht fest', 'Der nächste Termin steht noch nicht fest.'),
   ('Warteliste', 'wer sich einträgt, erfährt den nächsten Termin vor allen anderen', 'Trag dich ein: Sobald der nächste Termin feststeht, erfährst du es vor allen anderen.'),
   ('Eintragen', 'auf «Der Abend»: Tag (Freitag, Samstag oder egal), Plätze, Name und E-Mail; im Fuss jeder Seite mit der E-Mail vormerken', 'Egal', 'Dein Platz am nächsten Abend.'),
  ]),
 ]),
 ('Tickets & Preise', [
  ('Preis', [
   ('Zuletzt', '89,00 EUR am 25. und 26. September 2026, ausgebucht', 'Zuletzt 89,00 EUR am 25. und 26. September 2026.'),
   ('Darin', 'drei Gänge, fünf Drinks, Tasting und Schulung', 'Angekündigt waren drei Gänge, fünf Drinks, Tasting und Schulung.'),
  ]),
  ('Tickets', [
   ('Vorverkauf', 'Tickets gibt es bisher nur im Vorverkauf, per PayPal; dazu eine Nachricht an @culinarium_hannover', 'Tickets gibt es bisher nur im Vorverkauf.', 'Tickets ausschließlich per Vorverkauf über PayPal.'),
   ('Zurückgeben', 'nicht möglich: Tickets werden nicht rückerstattet', 'Da die Plätze begrenzt sind, bitten wir um Verständnis, dass Tickets nicht rückerstattet werden können.'),
  ]),
 ]),
 ('Drinks & Küche', [
  ('Die Drinks', [
   ('Wer', 'Momo (Mohamed Ben Khelifa) mixt die Signature Drinks hinter der Bar des Hauses', 'Die Drinks mixt Momo, hinter der Bar des Hauses.'),
   ('Fatwashing', 'die Spirituose nimmt den Geschmack eines Fetts an, kalt gestellt wird das Fett wieder abgehoben', 'Die Spirituose nimmt den Geschmack eines Fetts an; kalt gestellt, wird das Fett wieder abgehoben.'),
   ('Milkwashing', 'Milch bindet die Trübstoffe und wird abgefiltert, der Drink wird klar und weich', 'Milch bindet die Trübstoffe und wird abgefiltert, der Drink wird klar und weich.'),
   ('Enzyme', 'lösen die Trübung aus Fruchtsaft, der Geschmack bleibt', 'Enzyme lösen die Trübung aus Fruchtsaft, der Geschmack bleibt.'),
  ]),
  ('Die Küche', [
   ('Wer', 'Rudi Napieraj kocht die drei Gänge', 'In der Küche steht Rudi Napieraj.'),
   ('Rudis Zeilen', 'LAUCH / BLUMENKOHL / CHIPOTLE, so schreibt er seine Teller', 'LAUCH / BLUMENKOHL / CHIPOTLE', 'Seine Teller schreibt er in drei, vier Wörtern, so stehen sie auch hier.'),
   ('Gemüse', 'steht bei ihm oft im Mittelpunkt: Lauch, Blumenkohl, Kürbis, Rote Bete', 'Gemüse steht bei ihm oft im Mittelpunkt: Lauch, Blumenkohl, Kürbis, Rote Bete.'),
  ]),
 ]),
 ('Kontakt', [
  ('So erreichst du das Team', [
   ('Culinarium', 'keine eigene Telefonnummer und keine E-Mail-Adresse; Fragen zu einem Abend per Nachricht an @culinarium_hannover auf Instagram', 'Culinarium hat keine eigene Telefonnummer und keine eigene E-Mail-Adresse.'),
   ('Die Bar', 'Telefon +49 163 3909578; reservieren per Nachricht oder Telefon', 'Telefon +49 163 3909578.', 'Reservieren geht per Nachricht oder Telefon.'),
   ('Instagram', '@culinarium_hannover, @walkonthewildside_hannover, @dirtychicken.hannover', 'Instagram: @culinarium_hannover (Culinarium), @walkonthewildside_hannover (die Bar), @dirtychicken.hannover (Dirty Chicken).'),
  ]),
 ]),
 ('Das Haus (Bar)', [
  ('Walk on the Wild Side', [
   ('Was', 'eine Nachbarschafts-Mixology-Bar in Linden, Haasemannstraße 13: Drinks, Events, private Veranstaltungen und Tastings', 'eine Nachbarschafts-Mixology-Bar in Linden, Haasemannstraße 13. Drinks, Events, private Veranstaltungen und Tastings.'),
   ('Ohne Karte', 'wer an die Theke kommt, erzählt, was er mag, und bekommt seinen eigenen Drink', 'Eine Getränkekarte gibt es im Walk on the Wild Side nicht.'),
   ('Geöffnet', 'Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr; Sonntag bis Mittwoch geschlossen', 'Donnerstag 19 bis 1 Uhr · Freitag und Samstag 19 bis 2 Uhr', 'Sonntag bis Mittwoch'),
   ('Eigene Feier', 'die lange Tafel für eure eigene Feier; dazu Konzerte, DJ-Abende, Gastschichten', 'die lange Tafel für eure eigene Feier'),
   ('Seit', 'Ende Oktober 2017 in Linden; seit dem Reopening am 9. November 2023 führt Derya Ivkin die Bar', 'Christoph Elbert und Verena Schindler eröffneten die Bar Ende Oktober 2017 in Linden', 'Seit dem Reopening am 9. November 2023 führt Derya Ivkin sie.'),
  ]),
 ]),
 ('Team', [
  ('Drei Leute, ein Haus', [
   ('Derya Ivkin', 'führt die Bar, das Haus von Culinarium, seit dem Reopening im November 2023', 'Führt das Walk on the Wild Side, das Haus von Culinarium, seit dem Reopening im November 2023.'),
   ('Momo', 'Mohamed Ben Khelifa, mixt die Signature Drinks und erklärt jeden selbst', 'Steht hinter der Bar und mixt die Signature Drinks, auch die fünf eines Culinarium-Abends, und erklärt jeden selbst.'),
   ('Rudi Napieraj', 'kocht seit 2024 bei Culinarium und steht beim Pop-up Dirty Chicken in der Küche', 'Kocht seit 2024 bei Culinarium, drei Gänge an der langen Tafel, und steht beim Pop-up Dirty Chicken in der Küche.'),
  ]),
 ]),
 ('Der Weg', [
  ('Hinfinden', [
   ('Adresse', 'Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover', 'Haasemannstraße 13', '30449 Hannover'),
   ('Ecke', 'Haasemannstraße, Ecke Rampenstraße, am Schild über der Hausecke', 'Haasemannstraße, Ecke Rampenstraße', 'Am Schild über der Hausecke erkennst du die Bar schon von weitem.'),
   ('Plus Code', '9PC7+49 Hannover', '9PC7+49 Hannover'),
  ]),
 ]),
 ('Dirty Chicken', [
  ('Das Pop-up', [
   ('Was', 'Fried Chicken im Brötchen mit Paprika-Honig-Mayo und eingelegten Zwiebeln, Chunks mit Spicy Glaze und grüner Sauce, Pommes, Krautsalat, Dirty Drinks und Musik', 'Im Brötchen mit Paprika-Honig-Mayo und eingelegten Zwiebeln, als Chunks mit Spicy Glaze und grüner Sauce.'),
   ('Wann', 'nur an einzelnen Tagen; die Termine stehen auf Instagram @dirtychicken.hannover', 'Nur an einzelnen Tagen.', '@dirtychicken.hannover'),
   ('Opening', '30. Mai 2026, 14 bis 22 Uhr, im AM:PM Café im Tiedthof, Goseriede 4', '30. Mai 2026, 14 bis 22 Uhr', 'AM:PM Café im Tiedthof, Goseriede 4'),
  ]),
 ]),
 ('Alle Abende', [
  ('Bisher', [
   ('Erstes Pop-up', '20. Mai 2023 mit Momo', 'Das erste Pop-up gab es am 20. Mai 2023 mit Momo.'),
   ('Name', '2023 «by Momo x Christoph», seit Juli 2024 «by Momo x Rudi»', '2023 hiessen die Abende „by Momo x Christoph“, seit Juli 2024 „by Momo x Rudi“.'),
   ('Plakate', 'seit September 2023 bekommt jeder Abend ein eigenes Plakat', 'Seit September 2023 bekommt jeder Culinarium-Abend ein eigenes Plakat.'),
  ]),
 ]),
]


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def main():
    quelle = {n: open(os.path.join(WISSEN, n), encoding='utf-8').read() for n in DATEIEN}
    roh = {n: norm(t) for n, t in quelle.items()}
    fehler, aus = [], []
    for bereich, gruppen in S:
        gl = []
        for gruppe, zeilen in gruppen:
            zl = []
            for was, angabe, beleg, *mehr in zeilen:
                datei = next((n for n, t in roh.items() if norm(beleg) in t), None)
                if not datei or any(not any(norm(m) in t for t in roh.values()) for m in mehr):
                    fehler.append(f'Beleg fehlt: {bereich} / {was}: «{beleg}»')
                    continue
                # jede Zahl der Angabe steht im Umfeld eines Belegs (±1500 Zeichen), nicht nur irgendwo im Wissen
                fen = ''
                for bl in [beleg] + mehr:
                    for t in roh.values():
                        i = t.find(norm(bl))
                        if i >= 0:
                            fen += t[max(0, i - 1500):i + 1500].replace('’', '')
                for zahl in re.findall(r'\d+(?:[.,]\d+)?', (gruppe + ' ' + angabe).replace('’', '')):
                    if zahl not in fen:
                        fehler.append(f'Zahl {zahl} nicht beim Beleg: {bereich} / {was}')
                fid = hashlib.sha1(f'{bereich}|{gruppe}|{was}'.encode('utf-8')).hexdigest()[:10]
                zl.append({'fid': fid, 'was': was, 'angabe': angabe, 'beleg': norm(beleg), 'datei': datei, 'mehr': [norm(m) for m in mehr]})
            gl.append({'gruppe': gruppe, 'zeilen': zl})
        aus.append({'bereich': bereich, 'gruppen': gl})
    if fehler:
        print('\n'.join(fehler)); sys.exit(1)
    json.dump({'stand': max(os.path.getmtime(os.path.join(WISSEN, n)) for n in DATEIEN), 'bereiche': aus},
              open(os.path.join(HIER, 'steckbrief.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(sum(len(g['zeilen']) for b in aus for g in b['gruppen']), 'Zeilen, alle belegt')


if __name__ == '__main__':
    main()
