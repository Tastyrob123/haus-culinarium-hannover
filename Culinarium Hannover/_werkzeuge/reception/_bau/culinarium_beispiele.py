#!/usr/bin/env python3
"""Beispiele für La Réception von Culinarium Hannover (28.10.2026, Muster _bau/schaefli_beispiele.py der Taverne zum Schäfli): schreibt gast_beispiele.json
(Anfragen im Eingang) und gast_beispiel_fragen.json («Das wurde gefragt»). Namen und Adressen sind erfunden (example.com), in der Oberfläche steht
«Beispiel» dabei (Master E10, R20). Jede Angabe in Antworten und Briefen steht so in gast/gast_wissen.txt oder gast/gast_umgebung.txt (Wortlaut der Website,
Vorverkauf laut Instagram); Preis, Zeiten, Plätze sind nicht erfunden, ein Termin für den nächsten Abend wird nie genannt (steht noch nicht fest).
Zwei Fragen haben mit Absicht keine Antwort (Nussallergie, alkoholfrei): dazu sagt die Website nichts, Lücken zum Nachtragen. Nie erfinden, das Team
habe etwas nachgetragen (gast_beispiel_nachgetragen.json bleibt leer, die Oberfläche zeigt beschriftete Musterkarten).
Die Formular-Anfragen haben genau die Zeilen, die baustein/anfrage.js schickt. Prüfung am Ende: jede Zahl der Antworten steht im Wissen.
Aufruf: python3 _werkzeuge/reception/_bau/culinarium_beispiele.py"""
import json, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, C)
from reception import DANKE   # Dank an den Gast mit dem Namen des Werkzeugs aus kleid/culinarium.js
KONTAKT = 'Telefon der Bar +49 163 3909578 · Instagram @culinarium_hannover'
TEAM = '- Telefon der Bar: +49 163 3909578\n- Instagram: @culinarium_hannover'


def web(seite, seite_name, zeilen):
    n = '\n'.join(zeilen)
    return {'web': True, 'an': KONTAKT, 'seite': seite, 'seite_name': seite_name, 'nachricht': n,
            'verlauf': [['user', f'Über ein Formular der Website (Seite {seite_name}): ' + n]]}


def chat(*z):
    return {'verlauf': [[('user' if i % 2 == 0 else 'assistant'), t] for i, t in enumerate(z)]}


A = [
    dict(vor=[0, 9, 12], art='warteliste', status='neu', abteilung='Warteliste', name='Lena Hoffmann', kontakt='lena.hoffmann@example.com',
         datum='Freitag', uhrzeit='ab 19:00', personen=2, sprache='de', anliegen='Warteliste: Freitag, 2 Plätze', betreff='', text='', team='', formular='warteliste',
         **web('/abend.html#warteliste', 'Der Abend', ['Tag: Freitag, ab 19:00', 'Plätze: 2'])),
    dict(vor=[1, 20, 5], art='warteliste', status='gelesen', abteilung='Warteliste', name='Jonas Albers', kontakt='jonas.albers@example.com',
         datum='Freitag oder Samstag', uhrzeit='', personen=4, sprache='de', anliegen='Warteliste: Freitag oder Samstag, 4 Plätze', formular='warteliste',
         betreff='Dein Platz an der Tafel',
         text=('Hallo Jonas,\n\ndanke, dass du dich eingetragen hast. Du stehst mit vier Plätzen auf der Warteliste, Freitag oder Samstag ist dir beides recht.\n\n'
               'Der nächste Abend steht noch nicht fest. Sobald es so weit ist, erfährst du es vor allen anderen. '
               'An der Tafel gibt es nur wenige Plätze, und Tickets gibt es bisher nur im Vorverkauf.\n\n'
               'Freitags geht es ab 19 Uhr los, samstags ab 17 Uhr: ein Aperitif zum Ankommen, drei Gänge von Rudi und fünf Drinks von Momo, der dir jeden am Tisch erklärt.\n\n'
               'Bis bald an der Tafel\n\nMomo und Rudi\nCulinarium im Walk on the Wild Side'),
         team=('Grundlage: Der Abend (Warteliste, «Der nächste Termin steht noch nicht fest»), Startseite «Gut zu wissen» (Vorverkauf, Freitag ab 19, Samstag ab 17).\n'
               'Offen: Termin des nächsten Abends, ob vier Plätze zusammen frei sind.'),
         **web('/abend.html#warteliste', 'Der Abend', ['Tag: Freitag oder Samstag, beides geht', 'Plätze: 4'])),
    dict(vor=[1, 11, 30], art='abend', status='gelesen', abteilung='Abende', name='Mira Schulte', kontakt='mira.schulte@example.com', datum='', personen=2, sprache='de',
         anliegen='Zwei Plätze am nächsten Abend; eine Person hat eine Nussallergie.',
         betreff='Zwei Plätze an der Tafel und deine Nussallergie',
         text=('Hallo Mira,\n\ndanke für deine Nachricht. Für den nächsten Abend merken wir dich mit zwei Plätzen vor; der Termin steht noch nicht fest.\n\n'
               'Dass eine von euch keine Nüsse verträgt, gibt das Team an Rudi in der Küche weiter. Er stimmt mit dir ab, was auf euren Tellern landet.\n\n'
               'Zuletzt kostete der Abend 89,00 EUR, mit drei Gängen, fünf Drinks, Tasting und Schulung. Tickets gibt es nur im Vorverkauf.\n\n'
               'Bis bald an der Tafel\n\nMomo und Rudi\nCulinarium im Walk on the Wild Side'),
         team=('Grundlage: Startseite «Gut zu wissen» (89,00 EUR zuletzt, Vorverkauf), Der Abend (drei Gänge, fünf Drinks). Allergien: dazu sagt die Website nichts.\n'
               'Offen: Termin, Preis des nächsten Abends, Nussallergie mit Rudi klären.'),
         **chat('Hallo, wir möchten gern zu zweit zum nächsten Culinarium. Eine von uns hat eine Nussallergie.',
                'Der nächste Termin steht noch nicht fest; auf der Warteliste erfährst du ihn zuerst. Zur Nussallergie sagt die Website nichts, Rudi in der Küche klärt das mit dir. Magst du mir deinen Namen und eine E-Mail-Adresse geben?',
                'Mira Schulte, mira.schulte@example.com',
                DANKE['de'])),
    dict(vor=[2, 18, 45], art='feier', status='neu', abteilung='Feiern', name='Kai Brandt', kontakt='+49 151 2345678', datum='Samstag, 13. März 2027', personen=12, sprache='de',
         anliegen='Die lange Tafel für den 40. Geburtstag, 12 Personen.', betreff='', text='', team='',
         **chat('Kann man die lange Tafel auch für eine eigene Feier haben? Ich werde 40, wir wären 12.',
                'Ja, die lange Tafel gibt es auch für eure eigene Feier; reservieren geht bei der Bar per Nachricht oder Telefon. Wenn du magst, gebe ich deine Anfrage weiter: Wie heisst du, und wie erreicht dich das Team?',
                'Kai Brandt, 0151 2345678, am liebsten Samstag, 13. März 2027',
                DANKE['de'])),
    dict(vor=[3, 14, 10], art='feier', status='gelesen', abteilung='Feiern', name='Tim Becker', kontakt='tim.becker@example.com', datum='Freitag, 4. Dezember 2026', personen=18, sprache='de',
         anliegen='Weihnachtsfeier der Firma an der langen Tafel, 18 Personen.', betreff='', text='', team='',
         **chat('Wir sind 18 Kollegen und suchen etwas für die Weihnachtsfeier am 4. Dezember. Geht das bei euch?',
                'Die lange Tafel gibt es auch für eure eigene Feier; ob es für 18 passt, klärt das Team mit dir. Wie heisst du, und wie erreicht dich das Team?',
                'Tim Becker, tim.becker@example.com',
                DANKE['de'])),
    dict(vor=[4, 10, 20], art='nachricht', status='erledigt', abteilung='Nachrichten', name='Sophie Wagner', kontakt='sophie.wagner@example.com', datum='', personen=1, sprache='de',
         anliegen='Kann am gebuchten Abend nicht kommen und fragt, ob sie ihr Ticket zurückgeben kann.',
         betreff='Dein Ticket',
         text=('Hallo Sophie,\n\nschade, dass du nicht kommen kannst. Da die Plätze an der Tafel begrenzt sind, können Tickets nicht rückerstattet werden; so steht es auch beim Vorverkauf.\n\n'
               'Wenn jemand deinen Platz übernehmen möchte, schreib uns kurz, wer an deiner Stelle kommt.\n\n'
               'Bis bald in Linden\n\nMomo und Rudi\nCulinarium im Walk on the Wild Side'),
         team='Grundlage: Startseite «Gut zu wissen» und der Beitrag zum letzten Abend («Tickets nicht rückerstattet»).\nOffen: ob ein Platz weitergegeben werden darf (steht nirgends).',
         **chat('Ich habe ein Ticket, kann aber nicht kommen. Kann ich es zurückgeben?',
                'Tickets werden nicht rückerstattet, weil die Plätze an der Tafel begrenzt sind. Magst du dem Team schreiben? Dann brauche ich deinen Namen und eine E-Mail-Adresse.',
                'Sophie Wagner, sophie.wagner@example.com',
                DANKE['de'])),
    dict(vor=[5, 21, 15], art='abend', status='gelesen', abteilung='Abende', name='Emma Clarke', kontakt='emma.clarke@example.com', datum='', personen=2, sprache='en',
         anliegen='Visiting Hannover with her partner and would like two seats at the next evening.',
         betreff='Two seats at the table',
         text=('Hi Emma,\n\nthank you for your message. The next evening has not been fixed yet; once it is, you will be among the first to know.\n\n'
               'On Fridays we start at 7 pm, on Saturdays at 5 pm: an aperitif, three courses from Rudi and five drinks from Momo, who explains each one at the table. '
               'There are only a few seats, and tickets are sold in advance only.\n\n'
               'See you at the table\n\nMomo und Rudi\nCulinarium im Walk on the Wild Side'),
         team='Grundlage: Startseite «Gut zu wissen» (Freitag ab 19, Samstag ab 17, Vorverkauf), Der Abend (Aperitif, drei Gänge, fünf Drinks).\nOffen: Termin, Plätze.',
         deutsch={'betreff': 'Zwei Plätze an der Tafel',
                  'text': ('Hallo Emma,\n\ndanke für deine Nachricht. Der nächste Abend steht noch nicht fest; sobald er feststeht, erfährst du es mit als Erste.\n\n'
                           'Freitags beginnen wir um 19 Uhr, samstags um 17 Uhr: ein Aperitif, drei Gänge von Rudi und fünf Drinks von Momo, der jeden am Tisch erklärt. '
                           'Es gibt nur wenige Plätze, Tickets gibt es nur im Vorverkauf.\n\nBis bald an der Tafel\n\nMomo und Rudi\nCulinarium im Walk on the Wild Side')},
         verlauf_de=['Hallo, wir sind im Frühjahr in Hannover und würden gern zu zweit zum nächsten Abend kommen. Ist das möglich?',
                     'Der nächste Termin steht noch nicht fest; auf der Warteliste erfährst du ihn zuerst. Magst du mir deinen Namen und eine E-Mail-Adresse geben?',
                     'Emma Clarke, emma.clarke@example.com',
                     DANKE['de']],
         **chat('Hi, we are visiting Hannover in spring and would love two seats at the next evening. Is that possible?',
                'The next date has not been fixed yet; on the waiting list you hear about it first. Could you give me your name and an email address?',
                'Emma Clarke, emma.clarke@example.com',
                'Thank you. This is a draft by Tasty Studios: your request does not go to the team, it is only kept for viewing in the host tool.')),
]

F = [
    dict(vor=[0, 10, 20], sprache='de', belegt=True, frage='Wann ist der nächste Abend?', buchung=True,
         antwort='Der nächste Termin steht noch nicht fest. Wer auf der Warteliste steht, erfährt ihn zuerst.\n- Freitag: ab 19 Uhr\n- Samstag: ab 17 Uhr\n- Plätze: wenige, an einer Tafel'),
    dict(vor=[0, 8, 55], sprache='de', belegt=True, frage='Was kostet ein Abend?',
         antwort='Zuletzt kostete ein Abend 89,00 EUR, am 25. und 26. September 2026.\n- Darin: drei Gänge, fünf Drinks, Tasting und Schulung\n- Tickets: nur im Vorverkauf'),
    dict(vor=[1, 19, 5], sprache='de', belegt=True, frage='Was ist Fatwashing?',
         antwort='Die Spirituose nimmt den Geschmack eines Fetts an; kalt gestellt, wird das Fett wieder abgehoben. Momo erklärt jeden Drink am Tisch.'),
    dict(vor=[1, 13, 40], sprache='de', belegt=False, thema='Nussallergie', frage='Ich habe eine Nussallergie, geht das?',
         antwort='Dazu steht nichts in meinen Unterlagen; Rudi in der Küche klärt es mit dir. Frag am besten direkt:\n' + TEAM),
    dict(vor=[2, 17, 25], sprache='de', belegt=True, frage='Kann ich mein Ticket zurückgeben?',
         antwort='Tickets werden nicht rückerstattet, weil die Plätze an der Tafel begrenzt sind.'),
    dict(vor=[2, 9, 10], sprache='de', belegt=True, frage='Wo ist das genau?',
         antwort='Im Walk on the Wild Side in Linden.\n- Adresse: Haasemannstraße 13, 30449 Hannover\n- Ecke: Haasemannstraße, Ecke Rampenstraße\n- Plus Code: 9PC7+49 Hannover'),
    dict(vor=[3, 12, 30], sprache='de', belegt=False, thema='Alkoholfrei', frage='Gibt es den Abend auch alkoholfrei?',
         antwort='Dazu steht nichts in meinen Unterlagen. Frag am besten direkt:\n' + TEAM),
    dict(vor=[3, 15, 45], sprache='en', belegt=True, frage='What time does the evening start?',
         antwort='On Fridays from 7 pm, on Saturdays from 5 pm. Culinarium takes place on single weekends, usually a Friday and the Saturday after.'),
    dict(vor=[4, 11, 0], sprache='de', belegt=True, frage='Wann gibt es wieder Dirty Chicken?',
         antwort='Dirty Chicken gibt es nur an einzelnen Tagen; die Termine stehen auf Instagram bei @dirtychicken.hannover.'),
    dict(vor=[4, 18, 20], sprache='de', belegt=True, frage='Kann ich die lange Tafel für meinen Geburtstag haben?',
         antwort='Ja, die lange Tafel gibt es auch für eure eigene Feier.\n- Reservieren: bei der Bar per Nachricht oder Telefon\n- Telefon der Bar: +49 163 3909578'),
]
for f in F:
    f.setdefault('thema', ''); f.setdefault('buchung', False)


def pruefen():
    """Jede Zahl in Antworten und Briefen steht im Wissen (Website, Umgebung); kein Datum des nächsten Abends."""
    w = ''.join(open(os.path.join(C, 'gast', n), encoding='utf-8').read() for n in ('gast_wissen.txt', 'gast_umgebung.txt'))
    erlaubt = {'40', '12', '18', '4', '2', '13', '2027', '2026', '1', '0151', '2345678', '7', '5'}   # Angaben der erfundenen Gäste (Alter, Personen, Wunschtage, Nummer) und englische Uhrzeiten
    fehler = []
    for x in [a.get('text', '') + ' ' + a.get('betreff', '') for a in A] + [f['antwort'] for f in F]:
        for z in re.findall(r'\d+(?:[.,]\d+)?', x.replace('+49 163 3909578', '').replace('9PC7+49', '')):
            if z not in w and z not in erlaubt:
                fehler.append(z)
    if fehler:
        sys.exit('PRUEF · Zahlen ohne Beleg: ' + ', '.join(sorted(set(fehler))))


if __name__ == '__main__':
    pruefen()
    json.dump(A, open(os.path.join(C, 'gast_beispiele.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(F, open(os.path.join(C, 'gast_beispiel_fragen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump([], open(os.path.join(C, 'gast_beispiel_nachgetragen.json'), 'w', encoding='utf-8'))
    print(len(A), 'Anfragen,', len(F), 'Fragen (davon', sum(1 for f in F if not f['belegt']), 'ohne Antwort)')
