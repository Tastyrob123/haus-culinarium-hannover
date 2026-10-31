#!/usr/bin/env python3
"""Ideen für Papier: Drucksachen und Untersetzer für Culinarium (Werkbank-Chat 28.10.2026; Bauart wie papier.py des Schäfli, Inhalt und Kleid eigen).
   PYTHONPATH=<Kit> python3 _werkbank/papier.py "<website/_werkbank>"

Gedruckt wird, was an einem Abend vorkommt: die Karte am Platz (es gab gedruckte Karten, Foto «karte» der Website), ein Kärtchen zu Momos Techniken
(«Momo wird persönlich jeden Drink für dich erklären», Beitrag DbYnkdkjrNy), das Ticket, das der Gast nach der Buchung bekommt (Seite «Der Abend»), Briefpapier.
Das Gegenstück zum Sticker sind Untersetzer für die Theke: je Abendfarbe der Plakate zwei (Markenbuch, marke.json › abendfarben). Alles aus der Website
(website/index.html, website/bau.py) und dem Markenbuch gelesen, nichts abgetippt. Kein warmweisses Band mit Doppelrahmen (abgelehnt 26.10.).
Titel wie auf der Website: Fraunces leicht, Rudis Zeilen in Versalien mit Schrägstrich, kleine Zeilen in DM Mono gesperrt. Was von Tasty Studios ist, steht in MEINS."""
import html as _h, json, os, re
import papier_kern as P
import bogen_mitte  # noqa: F401  Druckbögen mittig (Tor 4, 30.10.2026)
from papier_kern import t, lin, linv, rahmen, kasten, foto, blatt, hz, hw, tx, hzz, hwz, strich, etikett, bogen_text, e
from kern import H, ROOT

WEB = os.path.dirname(ROOT)
NACHT, STRASSE, WARM, SCHIEFER, WEISS, CREME = '#16151a', '#1c1b21', '#222028', '#3a3845', '#faf4f4', '#f2eaea'
ORANGE, ORANGEH, ORANGET, TINTE, LEISE, RAHMEN = '#ef7649', '#f5a689', '#b15736', '#26242d', '#5b5763', '#b1adac'
_Z = os.path.relpath(os.path.join(WEB, 'assets', 'zeichen'), os.path.join(ROOT, '_werkbank', 'satz'))
TAPETE = f'url({_Z}/tapete-dunkel.svg) 50% 0/16mm auto'      # das feine Raster der dunklen Flächen der Website
ADR = 'Walk on the Wild Side · Haasemannstraße 13 · 30449 Hannover'
ZEILE = 'A UNiQUE EXPERiENCE BY MOMO X RUDI'
MB = json.load(open(os.path.join(os.path.dirname(WEB), '_kette', '05-markenbauer', 'marke.json'), encoding='utf-8'))
ABENDFARBEN = [(a['name'], a['hex'], a['plakat'], a['motiv']) for a in MB['abendfarben']]
AUF_NACHT = {a['name']: (a['hex'] if a['hex'].lower() in ('#b3ebfc', '#ef7649', '#94b253') else a['toene']['gold_h']) for a in MB['abendfarben']}   # dunkle Abendfarben auf der Nacht in ihrer hellen Stufe (Markenbuch › toene)

MEINS = ['Feldnamen auf Karte und Ticket', 'Die Sätze auf der Rückseite der Karte, des Tickets und der Drink-Kärtchen', 'Auswahl der Zeilen auf den Untersetzern']


def _text(s):
    t = _h.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()
    return re.sub(r'\xa0 +| +\xa0', '\xa0', t)   # Werkbank 30.10.2026: «LAUCH&nbsp;<i>/</i>» ergab festes plus normales Leerzeichen, doppelte Lücke vor dem «/»


_IDX = open(os.path.join(WEB, 'index.html'), encoding='utf-8').read()
# Rudis Teller, wie die Startseite sie zeigt (Block «Teller von Rudi», Zeilen I bis IV)
TELLER = [_text(x).replace(' / ', ' / ') for x in re.findall(r'<div class="fk-gang"><span class="fk-nr">[IVX]+</span><p>(.*?)</p></div>', _IDX)][:4]
# Momos Techniken mit ihrem Satz, wie im Abschnitt «Das erste Glas»
_G = _text(_IDX[_IDX.index('id="glas"'):_IDX.index('Dann kommen die Teller')])
TECHNIK = [(n, re.search(re.escape(n) + r'\s+(.+?\.)(?:\s|$)', _G).group(1)) for n in ('Fatwashing', 'Milkwashing', 'Enzyme')]


def vers(text):
    return e(text.upper())


def gaenge(y, farbe_nr, farbe_text, breite=120, x=14, groesse=4.1):
    roem = ['I', 'II', 'III', 'IV', 'V']
    aus = ''
    for i, z in enumerate(TELLER):
        teile = [e(w.strip()) for w in z.split('/')]
        aus += (t(0, y, roem[i], 'm c', f'font-size:2.1mm;letter-spacing:.2em;color:{farbe_nr}', 148)
                + t(x, y + 4.6, f' <span style="color:{farbe_nr}">/</span> '.join(teile), 's c',
                    f'font-size:{groesse}mm;line-height:1.3;letter-spacing:.06em;font-weight:340;color:{farbe_text}', breite))
        y += 19
    return aus


# ============================================================ Die Karte am Platz (A5 hoch, zwei Seiten)
def karte():
    v = (kasten(0, 0, 148, 210, f'background:{NACHT} {TAPETE}')
         + hw(74, 20, 104, WEISS)
         + t(0, 34, vers(ZEILE), 'm c', f'font-size:2.1mm;letter-spacing:.22em;color:{ORANGEH}', 148)
         + lin(64, 46, 20, ORANGE, .35)
         + t(0, 53, vers('Teller von Rudi'), 'm c', f'font-size:2.1mm;letter-spacing:.2em;color:{RAHMEN}', 148)
         + gaenge(66, ORANGE, WEISS)
         + lin(64, 150, 20, ORANGE, .35)
         + t(30, 158, vers('Abend'), 'm', f'font-size:1.9mm;letter-spacing:.16em;color:{RAHMEN}') + lin(30, 167, 40, 'rgba(250,244,244,.4)', .2)
         + t(80, 158, vers('Platz'), 'm', f'font-size:1.9mm;letter-spacing:.16em;color:{RAHMEN}') + lin(80, 167, 38, 'rgba(250,244,244,.4)', .2)
         + hz(74, 180, 9, ORANGE)
         + t(0, 194, e(ADR), 'm c', f'font-size:1.8mm;letter-spacing:.06em;color:{RAHMEN}', 148))
    tech = ''.join(t(22, 104 + i * 22, e(n), 's', f'font-size:5.2mm;font-weight:340;color:{TINTE}', 104)
                   + t(22, 111.5 + i * 22, e(s), '', f'font-size:2.9mm;line-height:1.45;color:{LEISE}', 104) for i, (n, s) in enumerate(TECHNIK))
    r = (hz(74, 16, 12, ORANGET)
         + t(0, 36, 'Fünf Drinks von Momo.', 's c', f'font-size:7.4mm;line-height:1.2;font-weight:340;color:{TINTE}', 148)
         + t(22, 52, 'Zu jedem Gang stellt Momo einen Signature Drink an euren Platz und erklärt ihn persönlich: was darin steckt und wie er gemacht ist.', 'c', f'font-size:3.3mm;line-height:1.55;color:{TINTE}', 104)
         + lin(64, 84, 20, ORANGE, .35)
         + t(0, 91, vers('Was Fett, Milch und Enzyme mit einem Drink machen'), 'm c', f'font-size:1.9mm;letter-spacing:.16em;color:{ORANGET}', 148)
         + tech
         + hw(74, 186, 52, SCHIEFER)
         + t(0, 196, vers(ZEILE), 'm c', f'font-size:1.6mm;letter-spacing:.2em;color:{LEISE}', 148))
    return [blatt(148, 210, v, '', f'background:{NACHT}'), blatt(148, 210, r, '', f'background:{WEISS}')]


# ============================================================ Drink-Kärtchen (A7 hoch, 74 × 105 mm): je Technik eines, eine Rückseite für alle
def drinks():
    farben = [ORANGE, ORANGEH, '#b3ebfc']   # Orange und Orange hell der Seite, Eisblau aus den Abendfarben
    aus = []
    for i, (n, s) in enumerate(TECHNIK):
        aus.append(blatt(74, 105, kasten(0, 0, 74, 105, f'background:{NACHT} {TAPETE}')
                         + t(0, 10, vers('Momo erklärt'), 'm c', f'font-size:1.8mm;letter-spacing:.2em;color:{RAHMEN}', 74)
                         + hz(37, 22, 9, farben[i])
                         + t(4, 40, e(n), 's c', f'font-size:{7.4 if len(n) < 10 else 6.6}mm;line-height:1.1;font-weight:340;color:{WEISS}', 66)
                         + lin(29, 52, 16, farben[i], .35)
                         + t(9, 58, e(s), 'c', f'font-size:2.9mm;line-height:1.5;color:{CREME}', 56)
                         + t(0, 93, vers('Culinarium'), 'm c', f'font-size:1.7mm;letter-spacing:.24em;color:{RAHMEN}', 74), '', f'background:{NACHT}'))
    aus.append(blatt(74, 105, hw(37, 30, 56, SCHIEFER) + t(0, 40, vers(ZEILE), 'm c', f'font-size:1.45mm;letter-spacing:.18em;color:{LEISE}', 74)
                     + lin(29, 52, 16, ORANGE, .35)
                     + t(9, 58, 'Zum Mitnehmen: wie euer Drink heute Abend gemacht ist.', 'c', f'font-size:2.9mm;line-height:1.5;color:{TINTE}', 56), '', f'background:{WEISS}'))
    return aus


# ============================================================ Ticket (DIN lang quer, 210 × 99 mm, mit Abriss)
def ticket():
    def feld(x, y, b, name, hell=True):
        return t(x, y, vers(name), 'm', f'font-size:1.9mm;letter-spacing:.16em;color:{RAHMEN if hell else LEISE}') + lin(x, y + 10, b, 'rgba(250,244,244,.42)' if hell else 'rgba(38,36,45,.4)', .2)
    v = (kasten(0, 0, 210, 99, f'background:{NACHT} {TAPETE}')
         + hw(14, 12, 86, WEISS, False)
         + t(14, 23.5, vers(ZEILE), 'm', f'font-size:1.9mm;letter-spacing:.2em;color:{ORANGEH}')
         + t(14, 36, 'Dein Platz an der Tafel.', 's', f'font-size:7mm;font-weight:340;color:{WEISS}')
         + feld(14, 55, 70, 'Abend') + feld(92, 55, 52, 'Beginn')
         + feld(14, 74, 70, 'Name') + feld(92, 74, 52, 'Plätze')
         + ''.join(f'<i class="abs" style="left:156mm;top:{4 + k * 4.6}mm;width:.35mm;height:2.4mm;background:rgba(250,244,244,.35)"></i>' for k in range(20))
         + kasten(158, 0, 52, 99, f'background:{ORANGE}')
         + hz(184, 14, 12, NACHT)
         + t(158, 40, vers('Ticket'), 'm c', f'font-size:2.2mm;letter-spacing:.24em;color:{NACHT}', 52)
         + t(158, 48, 'Nr.', 's c', f'font-size:9mm;font-weight:340;color:{NACHT}', 52)
         + lin(170, 70, 28, 'rgba(22,21,26,.5)', .2)
         + t(158, 82, vers('Haasemannstr. 13'), 'm c', f'font-size:1.7mm;letter-spacing:.14em;color:{NACHT}', 52))
    r = (hz(14, 12, 8, ORANGET, False)
         + t(14, 26, 'So findest du hin.', 's', f'font-size:6mm;font-weight:340;color:{TINTE}')
         + t(14, 37, 'Das Walk on the Wild Side liegt an der Hausecke Haasemannstraße und Rampenstraße in Linden. Am Schild über der Ecke erkennt man die Bar schon von weitem.', '', f'font-size:3.1mm;line-height:1.55;color:{TINTE}', 120)
         + t(14, 66, vers('Freitag ab 19:00 · Samstag ab 17:00'), 'm', f'font-size:2mm;letter-spacing:.14em;color:{ORANGET}')
         + t(14, 74, e(ADR), 'm', f'font-size:1.9mm;color:{LEISE}')
         + linv(150, 12, 75, RAHMEN, .25)
         + hw(181, 40, 46, SCHIEFER)
         + t(158, 50, vers(ZEILE), 'm c', f'font-size:1.3mm;letter-spacing:.14em;color:{LEISE}', 46))
    return [blatt(210, 99, v, '', f'background:{NACHT}'), blatt(210, 99, r, '', f'background:{WEISS}')]


# ============================================================ Briefpapier: Briefbogen A4 und Umschlag DIN lang
def briefpapier():
    bogen = (hw(105, 16, 70, SCHIEFER) + t(0, 27, vers(ZEILE), 'm c', f'font-size:1.9mm;letter-spacing:.22em;color:{LEISE}', 210)
             + lin(25, 40, 160, ORANGE, .25)
             + lin(4, 105, 5, 'rgba(38,36,45,.5)', .15) + lin(4, 210, 5, 'rgba(38,36,45,.5)', .15)
             + lin(25, 273, 160, ORANGE, .25) + hz(105, 277, 5, ORANGET)
             + t(0, 284, e(ADR), 'm c', f'font-size:1.95mm;letter-spacing:.06em;color:{TINTE}', 210))
    umschlag = (kasten(0, 0, 220, 110, f'background:{NACHT} {TAPETE}') + hw(14, 12, 58, WEISS, False) + t(14, 21, e(ADR), 'm', f'font-size:2mm;color:{ORANGEH}')
                + hz(204, 10, 6, ORANGE)
                + f'<i class="abs" style="left:118mm;top:52mm;width:90mm;height:44mm;background:{WEISS};border-radius:1mm"></i>')
    return [blatt(210, 297, bogen, '', f'background:{WEISS}'), blatt(220, 110, umschlag, '', f'background:{NACHT}')]


# ============================================================ Untersetzer für die Theke (rund, 94 mm): je Abendfarbe der Plakate zwei
D = 94
R_ = D / 2


def kreis():
    return f'M{R_} 0A{R_} {R_} 0 1 1 {R_ - .01} 0Z'


def hell(hx):
    r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
    return (r * 299 + g * 587 + b * 114) / 1000 > 150


def untersetzer(ident, grund, akzent, mitte, name, satz):
    schrift = SCHIEFER if hell(grund) else WEISS
    ring = bogen_text(ident + 'r', f'M{R_ - 36} {R_}A36 36 0 1 1 {R_ + 36} {R_}A36 36 0 1 1 {R_ - 36} {R_}', (e(ZEILE) + ' · ') * 2, 2.6, akzent if akzent != grund else schrift, 'm', .16)
    innen = (f'<path d="{kreis()}" fill="{grund}"/><circle cx="{R_}" cy="{R_}" r="{R_ - 3}" fill="none" stroke="{akzent if akzent != grund else schrift}" stroke-width=".35"/>' + ring + mitte(schrift))
    return etikett(ident, D, D, kreis(), innen, name, satz)


def untersetzer_alle():
    U, i = [], 0
    for name, hx, datum, motiv in ABENDFARBEN:
        i += 1
        U.append(untersetzer(f'u{i:02d}', hx, hx, lambda s: hzz(R_, R_ - 15, 26, s) + tx(R_, R_ + 22, vers(name), 3.4, s, 'm', .2),
                             f'{name}, {datum}', f'Die Farbe des Plakats vom {datum} ({motiv}), in der Mitte das C aus Rudis Wortmarke.'))
    worte = [('FATWASHING', 'Die erste von Momos Techniken.'), ('MILKWASHING', 'Die zweite, klar und weich.'), ('ENZYME', 'Die dritte, aus der Trübung wird Klarheit.'),
             ('LINDEN', 'Wo die Tafel steht.'), ('HAASEMANNSTR. 13', 'Die Adresse für den nächsten Abend.'), ('SEIT 2023', 'Das erste Pop-up war im Mai 2023.')]
    for (wort, satz), (name, hx0, _d, _m) in zip(worte, ABENDFARBEN):
        i += 1
        hx = AUF_NACHT[name]
        U.append(untersetzer(f'u{i:02d}', NACHT, hx, lambda s, w=wort, a=hx: hwz(R_, R_ - 13, 54, WEISS) + f'<rect x="{R_ - 9}" y="{R_ + 1}" width="18" height=".45" fill="{a}"/>'
                             + tx(R_, R_ + 11, e(w), 3.6 if len(w) < 12 else 3, a, 'm', .14), f'{wort.title() if len(wort) < 12 else wort}', satz + f' Linie in {name}.'))
    return U


def baue():
    Dr = []

    def d(ident, name, format_, blaetter, vorschau, satz, quelle):
        Dr.append(dict(id=ident, name=name, format=format_, blaetter=blaetter, vorschau=vorschau, satz=satz, quelle=quelle))
    d('karte', 'Die Karte am Platz', 'A5 hoch, zwei Seiten', karte(), [('karte', 1), ('karte-r', 2)],
      'Vorne Rudis Teller in seinen Zeilen, hinten Momos fünf Drinks und seine Techniken. Abend und Platz tragt ihr ein. Hier mit den Tellern, die auf eurer Startseite stehen.',
      'Startseite eurer Website: «Teller von Rudi» und «Das erste Glas»')
    d('drinks', 'Drink-Kärtchen', 'A7 hoch, drei Motive, eine Rückseite', drinks(), [('drink-1', 1), ('drink-2', 2), ('drink-3', 3), ('drink-r', 4)],
      'Zu jeder Technik ein kleines Kärtchen, das Momo zum Drink legt: Fatwashing, Milkwashing und Enzyme, jede mit ihrem Satz. Zum Mitnehmen.',
      'Abschnitt «Das erste Glas» eurer Website')
    d('ticket', 'Ticket', 'DIN lang quer, 210 × 99 mm, mit Abriss', ticket(), [('ticket', 1), ('ticket-r', 2)],
      'Das Ticket, das ein Gast nach der Buchung bekommt, als Blatt zum Ausdrucken: vorne Abend, Beginn, Name und Plätze, hinten der Weg zur Bar.',
      'Seite «Der Abend» und «Der Weg» eurer Website')
    d('briefpapier', 'Briefpapier', 'Briefbogen A4, Umschlag DIN lang', briefpapier(), [('briefbogen', 1), ('umschlag', 2)],
      'Briefbogen und Umschlag mit der Wortmarke und der Zeile eurer Plakate.', 'Plakate und Website')
    # zwanzig weitere Stücke für Tafel, Theke und Abend (Prüfchat Gestaltung 29.10.2026, papier_neu.py); Karton und Titel für die Seite in papier_neu_seite.json
    import papier_neu
    neu, seite_neu = papier_neu.stuecke(TELLER, TECHNIK)
    Dr += neu
    json.dump({k: dict(karton=[v['karton'][0], v['karton'][1]], titel=v['titel'], breit=sorted(v['breit'])) for k, v in seite_neu.items()},
              open(os.path.join(ROOT, '_werkbank', 'papier_neu_seite.json'), 'w'), ensure_ascii=False, indent=1)
    P.fertig(Dr, untersetzer_alle(), MEINS)


if __name__ == '__main__':
    baue()
