"""Culinarium Hannover: Inhalt der Werkbank («Alles auf einen Blick») und ihrer Beigaben.   Werkzeug: ~/Desktop/Website-Projekte/_Werkbank-Kit/

Werkbank-Chat Culinarium, 28.10.2026 (Auftrag Oberchef, Roberts Wort: «alles, was passiert, wenn die Website soweit fertig ist … Werkzeugbank, Tools»).
Aufbau und Wege wie die Werkbank der Taverne zum Schäfli (jüngstes Vorbild, Stand 21.10.2026, nur gelesen und kopiert), Kleid und Worte von Culinarium:
die Nacht der Bar, Schiefer und Warmweiss der Plakate, Kerze aus den Abendfotos, Fraunces mit weichen Enden, Rudis Zeilen in Versalien mit Schrägstrich,
das «C» aus Rudis Wortmarke als Zeichen (bis 29.10.2026 das «x» von «Momo x Rudi»). Fakten nur aus der Website (website/bau.py und ihre Seiten) und _kette/03-sammler/fakten.json, nichts abgetippt.

Eigenes Revier: website/_werkbank/ ist der Projektordner des Kits (ROOT), die Website liegt eine Ebene höher (WEB) und wird nur gelesen;
assets/ ist ein Verweis auf website/assets (nur gelesen). Serviert von website/_werkbank/serve.py auf Port 9088 (zuerst das Revier, sonst die Website).
Ton: Robert und Rudi duzen sich (WhatsApp), die Website spricht im Du: der Brief sagt «Hallo Rudi», sonst «ihr/euch» an Rudi, Momo und Derya.
Deutsche Schreibung mit ß. Kein Preis in der Werkbank. Abende, keine Zimmer, kein Restaurant mit Tageskarte."""
import json
import os
import re as _re
import shutil
import sys
import glob as _glob
import hilfen as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # = website/_werkbank (Projektordner des Kits)
WEB = os.path.dirname(ROOT)                                          # = website/ (nur gelesen)
PROJ = os.path.dirname(WEB)
FAKTEN = json.load(open(os.path.join(PROJ, '_kette', '03-sammler', 'fakten.json'), encoding='utf-8'))


def bild(key, hoechstens=2400):
    """Grösste Fassung eines Fotos der Website bis «hoechstens» Pixel Breite (assets/bild/<key>-<breite>.webp) als voller Pfad für K.hausbild.
    So kommen die geschärften Fassungen des Bilder-Chats von selbst nach (bau.py schreibt sie unter demselben Schlüssel)."""
    b = sorted(int(m.group(1)) for p in _glob.glob(os.path.join(WEB, 'assets', 'bild', key + '-*.webp')) if (m := _re.search(r'-(\d+)\.webp$', p)) and int(m.group(1)) <= hoechstens)
    if not b:
        raise FileNotFoundError(f'Bild {key} fehlt in website/assets/bild')
    return os.path.join(WEB, 'assets', 'bild', f'{key}-{b[-1]}.webp')


NAME = 'Culinarium'
KURZ = 'culinarium'
LEISTE = 'CULINARIUM'
HAUSART = 'restaurant'
PORT = 9088
DOMAIN = 'culinarium-hannover.de'
HEUTE_URL = 'https://www.instagram.com/culinarium_hannover/'
ANREDE = 'Hallo Rudi'
RECHTE = 'Culinarium und den jeweiligen Fotografen.'
START_MS = 4200
WAHL = 'main > section'
ADRESSE = 'Walk on the Wild Side · Haasemannstraße 13 · 30449 Hannover'

# ---------- Farben: die der Website (website/assets/culinarium.css :root) ----------
# Nacht der Bar, Strasse, Warm, Schiefer der Plakate, Warmweiss der Plakate, Kerze aus den Abendfotos. «gold» ist hier die Kerze: die eine warme Farbe des Hauses.
FARBEN = dict(nacht='#16151a', tief='#1c1b21', navy='#222028', blau='#3a3845', papier='#faf4f4', creme='#f2eaea', weiss='#fffbfa',
              gold='#ef7649', messing='#b15736', taupe='#5b5763', tinte='#26242d', punkt='#ef7649', rot='#ef7649')
_SCHRIFT = os.path.join(WEB, 'assets', 'schrift')
SCHRIFT = dict(titel=('Fraunces', 'fraunces-soft.woff2'), titel_folge="Georgia,serif", ersatz="local('Georgia')", druckgewicht=340)
SCHRIFT_MEHR = ['urbanist.woff2']
DRUCKQUELLEN = []   # Fraunces und Urbanist setzt _werkbank/druckschrift.py fest (alle Achsen), der Kit nur Instrument Sans und DM Mono
DRUCKSCHRIFT = [('Fraunces', 340, 'Fraunces-Light.ttf'), ('Fraunces', 400, 'Fraunces-Regular.ttf'), ('Fraunces', 500, 'Fraunces-Regular.ttf'), ('Fraunces', 700, 'Fraunces-Regular.ttf'), ('Urbanist', 500, 'Urbanist-Medium.ttf'), ('Urbanist', 600, 'Urbanist-SemiBold.ttf')]
# Die Webschriften der Website unter den Namen, die der Kit erwartet (er sucht sie in assets/fonts; die Website legt sie unter assets/schrift ab)
_WF = os.path.join(ROOT, 'werkbank', 'fonts')
os.makedirs(_WF, exist_ok=True)
for _q, _z in (('fraunces-soft.woff2', 'fraunces-soft.woff2'), ('instrument.woff2', 'InstrumentSans-normal-400_600.woff2'), ('dmmono.woff2', 'DMMono-normal-400.woff2'), ('urbanist.woff2', 'urbanist.woff2')):
    if os.path.exists(os.path.join(_SCHRIFT, _q)):
        shutil.copy2(os.path.join(_SCHRIFT, _q), os.path.join(_WF, _z))
# Muster der Website: das feine Raster mit dem Zeichen (assets/zeichen/tapete-dunkel.svg, Ton in Ton), vom Wurzelweg aus
MUSTER = 'url(/assets/zeichen/tapete-dunkel.svg)'
MUSTER_B = '224px'
MUSTER_DRUCK = '16mm'
# Das Zeichen: das «C», erster Buchstabe von Rudis Wortmarke, als Datei aus dem Kleid (_werkzeuge/oberflaeche/kleid/culinarium-zeichen.svg), unverändert
# übernommen, nie nachgezeichnet (Robert 29.10.2026: «wieso ist in der werkbank überall dieses x ???»; vorher das «x» aus «Momo x Rudi», eigen/zeichen-x.svg).
_ZC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen', 'zeichen-c.svg')
open(_ZC, 'w', encoding='utf-8').write(open(os.path.join(os.path.dirname(WEB), '_werkzeuge', 'oberflaeche', 'kleid', 'culinarium-zeichen.svg'), encoding='utf-8').read())
ZEICHEN = K.svg_innen(_ZC)
ZEICHEN = (ZEICHEN[0], ZEICHEN[1].replace(' fill="#000"', ''))   # Farbe über currentColor, wie bei jedem Zeichen der Werkbank


def _wortmarke():
    """Die Wortmarke CULINARIUM aus website/assets/zeichen/marke.svg (Symbol «wm»), so wie die Website sie zeigt."""
    s = open(os.path.join(WEB, 'assets', 'zeichen', 'marke.svg'), encoding='utf-8').read()
    m = _re.search(r'<symbol id="wm" viewBox="([^"]+)">(.*?)</symbol>', s, _re.S)
    vb = ' '.join(str(float(x)).rstrip('0').rstrip('.') for x in m.group(1).split())
    return vb, _re.sub(r'\s+fill="currentColor"', '', _re.sub(r'\s*\n\s*', ' ', m.group(2))).strip()


WORT = _wortmarke()
ETIKETTEN = dict(ordner='untersetzer', name='Untersetzer', einzahl='Untersetzer')

SEITEN = [   # alle Seiten, die ein Gast als Seite wahrnimmt, dazu das Rechtliche (Sätze nur aus dem, was auf der Seite steht)
    ('index.html', 'Startseite', 8, 'Culinarium im Walk on the Wild Side, der Abend an der langen Tafel, das erste Glas, drei Gänge, die Plakate, das Haus, die Leute, Dirty Chicken und was Gäste vorher wissen wollen.', ''),
    ('abend.html', 'Der Abend', 4, 'Was auf den Tisch kommt, wann und wie viel, die nächsten Abende zum Buchen und die Warteliste.', ''),
    ('abende.html', 'Alle Abende', 3, 'Jeder Abend seit dem ersten Pop-up 2023 mit seinem Plakat, Jahr für Jahr in einer Vitrine.', ''),
    ('bar.html', 'Das Haus', 3, 'Walk on the Wild Side: die Bar in Linden, ihre Drinks, ihre Geschichte seit 2017 und wann sie offen hat.', ''),
    ('leute.html', 'Das Team', 3, 'Derya, Momo und Rudi mit ihrem Weg, die Mannschaft bei der Arbeit und wie alles kam.', ''),
    ('weg.html', 'Der Weg', 2, 'Die Haasemannstraße 13 in Linden, die Zeiten der Abende und die gezeichnete Karte.', ''),
    ('dirty-chicken.html', 'Dirty Chicken', 4, 'Das Pop-up aus demselben Haus: das Essen, die Nacht mit Live-Musik und das erste Pop-up im Tiedthof.', ''),
    ('impressum.html', 'Rechtliches', 1, 'Impressum und Datenschutz.', 'recht'),
]
LANG = {'Startseite': 'Startseite', 'Rechtliches': 'Impressum und Datenschutz'}
KURZNAME = {'Dirty Chicken': 'Dirty Chicken', 'Alle Abende': 'Abende'}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import namen_fall as _nf  # noqa: E402


def _werkzeugname(teil):
    """Name eines Werkzeugs aus der einen Stelle (_werkzeuge/oberflaeche/kleid/culinarium.js › namen, Schreiber culinarium-maison), nie fest geschrieben."""
    k = open(os.path.join(PROJ, '_werkzeuge', 'oberflaeche', 'kleid', 'culinarium.js'), encoding='utf-8').read()
    return dict(_re.findall(r"(\w+): '([^']+)'", _re.search(r'namen:\s*\{([^}]*)\}', k).group(1)))[teil]


# ---------- Unterlagen: die Karten des Hauses (La Carte von Culinarium, PDFs in unterlagen/pdf) ----------
SATZ_FUSS = 'Culinarium · im Walk on the Wild Side · Haasemannstraße 13 · 30449 Hannover'
UNTERLAGEN = dict(
    pflege=('Karten selbst ändern',   # Tor 4 30.10.2026: Knopf in einer Zeile; wohin er führt, sagt der Satz daneben
            'http://127.0.0.1:9083/_werkzeuge/carte/'),
    text='Zu jedem Abend gehört eine Karte am Platz: Gang für Gang Rudis Teller und Momos Drink. Hier liegen zwei davon neu gesetzt neben dem Foto der Karte, wie sie an diesem Abend auf dem Tisch lag.',
    seite_text='Die Karte am Platz, neu gesetzt im Kleid der neuen Seite: Gang für Gang Rudis Teller und Momos Drink. Links die Karte, wie sie an diesem Abend auf dem Tisch lag, rechts die Idee. Die Karten aller Abende pflegt ihr ' + _nf.in_(_werkzeugname('karten')) + '.',
    knopf2=('Der Abend auf der Website', '../abend.html'))
FAECHER = [('abend-2025-02-21', 'Februar 2025'), ('abend-2023-09-15', 'September 2023')]   # PDFs: unterlagen/pdf (aus La Carte, Lieferung 28.10.2026, sb_karten.py)

# ---------- Auftakt, Brief ----------
AUFTAKT = dict(
    titel=['Ein Abend,', 'eine Tafel.'],
    text='Die neue Website von Culinarium, so wie sie werden könnte. Dazu eure Karten für jeden Abend, sieben Werkzeuge, mit denen ihr Termine, Menüs und Plakate selbst führt, und Ideen für Papier und Instagram.',
    abzuege=[(bild('anstossen'), 'Am Tisch wird angestoßen'), (bild('glas'), 'Ein Drink von Momo'), (bild('kerze1'), 'Ein Drink wird erklärt')])
BRIEF = dict(
    art='kurz',
    bild=bild('tafelleer'), schnitt=2.0, lage=(.5, .5), bild_alt='Die lange Tafel im Walk on the Wild Side, gedeckt und mit Kerzen',
    schild=('Culinarium', 'im Walk on the Wild Side · Linden'), ort='Tasty Studios',
    absaetze=[
        'Ein Abend bei euch fängt an der Theke an: Momo stellt das erste Glas hin und erklärt, was darin steckt, dann kommt aus der Küche der erste Gang. Wer einmal an eurer Tafel saß, weiß, wie viel Sorgfalt in jedem Teller und jedem Drink liegt. Die neue Seite soll das zeigen, bevor jemand seinen Platz bucht.',
        'Heute gibt es Culinarium auf Instagram. Termine, Menü und Preis stehen in Bildunterschriften, gebucht wird über eine Nachricht und PayPal. Die neue Seite stellt alles an einen Ort: jeden Abend mit seinem Plakat, das Menü in deinen Zeilen, Momos Drinks, das Haus in Linden, und weiter unten Dirty Chicken. Ist ein Abend voll, trägt man sich auf die Warteliste ein.',
        'Um die Seite herum liegt, was ihr im Alltag braucht: die Karte für jeden Abend, Ideen für Papier und Instagram und sieben Werkzeuge, in denen ihr Termine, Menüs und Plakate selbst führt. Alles hier lässt sich anklicken und ausprobieren.'],
    schluss='<q>A unique experience.</q> <small>Culinarium</small>',
    abzuege=[])
GABEN = dict(seite='{n} Seiten.', unterlagen='Eure Karten.', papier='{d} Drucksachen und {e} Untersetzer.', feed='{n} Beiträge.', gaeste='Für eure Gäste.', studio='')
GABEN_BILDER = dict(seite=(bild('loch'), (.5, .5)), unterlagen=(bild('karte'), (.5, .5)), papier=(bild('kartglas'), (.5, .5)), material=(bild('flaschen'), (.5, .5)), gaeste=(bild('toast'), (.5, .5)))
LAUFWORTE = ['Culinarium', '<b>Momo x Rudi</b>', 'Eine lange Tafel', 'Fünf Signature Drinks', '<b>Linden</b>', 'A unique experience']
REIHENFOLGE = ['brief', 'vergleich', 'ideen', 'gefuege', 'seiten', 'unterlagen', 'handschrift', 'papier', 'material', 'dazu', 'schluss']   # der Feed kommt als eigene Bühne (feed_buehne.py)

# ---------- Website: Ideen (Aufnahmen _werkbank/sb_ideen.js → ansichten/Ideen), Vergleich (vorher.js → ansichten/Vorher) ----------
IDEEN = [   # (Aufnahme, Titel, Satz, Ausschnitt): jeder Satz nur aus dem, was auf der Aufnahme zu sehen ist
    ('Ideen/start', 'Culinarium zuerst', 'Die Wortmarke groß über den Bildern eines Abends, darunter in einem Satz, was Culinarium ist, und der Weg zum nächsten Abend.', '50% 50%'),
    ('Ideen/ebenen', 'Der Abend und das Haus', 'Gleich nach dem Auftakt steht, wessen Seite das ist: links die Abende an der langen Tafel, rechts die Bar, in der sie stattfinden.', '50% 50%'),
    ('Ideen/ablauf', 'So läuft ein Abend', 'Aperitif, drei Gänge, fünf Signature Drinks, Tasting und Schulung: der Abend Schritt für Schritt, jeder mit seinem Bild.', '50% 50%'),
    ('Ideen/glas', 'Das erste Glas', 'Momos Techniken mit Namen: Fatwashing, Milkwashing und Klärung mit Enzymen, jede in einem Satz erklärt.', '50% 50%'),
    ('Ideen/gaenge', 'Rudis Zeilen', 'Die Gänge in Rudis eigener Schreibweise, in Versalien mit Schrägstrich, jeder neben seinem Teller.', '50% 50%'),
    ('Ideen/plakate', 'Jeder Abend hat sein Plakat', 'Die Plakate seit dem ersten Pop-up an einer Wand, dicht wie eine Sammlung, mit dem Weg zu allen Abenden.', '50% 50%'),
    ('Ideen/chronik', 'Seit 2023', 'Vom ersten Pop-up im Mai 2023 bis zum ausgebuchten September 2026, Jahr für Jahr mit Bild.', '50% 50%'),
    ('Ideen/haus', 'Das Haus', 'Das Walk on the Wild Side als Ort aller Abende, mit Adresse und dem Weg zur Seite der Bar.', '50% 50%'),
    ('Ideen/dirty', 'Aus demselben Haus', 'Dirty Chicken weiter unten auf der Startseite, im eigenen Violett, mit eigener Seite.', '50% 50%'),
    ('Ideen/vitrinen', 'Alle Abende in Vitrinen', 'Je Jahr eine Vitrine, darin die Plakate mit Datum und Preis, so wie die Abende angekündigt waren.', '50% 50%'),
    ('Ideen/team', 'Drei Leute, ein Haus', 'Derya, Momo und Rudi mit ihrer Rolle, ihrem Satz und ihrem Weg in Jahreszeilen.', '50% 50%'),
    ('Ideen/weg', 'So findest du hin', 'Die Zeiten der Abende groß, darunter Adresse, Plus Code und die gezeichnete Karte von Linden.', '50% 50%'),
]
VORHER = [   # Culinarium hat heute keine Website: «heute» sind Aufnahmen von Instagram vom 25.10.2026 (sb_heute.py), «neu» die neue Seite
    ('startseite', 'Startseite', 'Aus einem Profil wird eine Seite.',
     ['Heute ist Culinarium ein Profil auf Instagram: der Name, drei Zeilen und die Beiträge. Neu steht eine Seite unter eigenem Namen, mit dem Weg zum nächsten Abend gleich oben.',
      'Was ein Abend ist, steht in einem Satz, bevor die Seite erzählt: ein Menü, fünf passende Drinks, eine lange Tafel.',
      'Das Haus, die Leute und Dirty Chicken haben je ihren eigenen Platz.'], 'index.html'),
    ('abend', 'Der Abend', 'Der Abend an einem Ort.',
     ['Heute stehen Menü, Uhrzeiten, Preis und der Weg zum Ticket im Text eines Beitrags. Neu hat der Abend eine eigene Seite.',
      'Was auf den Tisch kommt, wann es losgeht und was es kostet, groß und klar, auch am Telefon.',
      'Gebucht wird auf der Seite; ist ein Abend voll, trägt sich der Gast auf die Warteliste ein.'], 'abend.html'),
    ('abende', 'Alle Abende', 'Jedes Plakat mit seinem Abend.',
     ['Heute liegen die Plakate im Profil zwischen den anderen Beiträgen. Neu stehen alle Abende seit 2023 beisammen.',
      'Je Jahr eine Vitrine, jedes Plakat mit Datum und Preis, so wie der Abend angekündigt war.',
      'So sieht man auf einen Blick, wie Culinarium gewachsen ist.'], 'abende.html'),
]
VERGLEICH_TEXT = 'Links, wie Culinarium heute im Netz steht, rechts die neue Seite. Den Griff schiebt ihr hin und her, daneben steht, was neu ist.'


def gefuege(z):
    n = [
        ['fotos', 0, 0, 'Eure Fotos', 'von den Abenden', 'ein', 'Eure Fotos', 'Die Aufnahmen, die Rudi geschickt hat: die Tafel bei Kerzenlicht, Momo an der Bar, jeder Teller, die Mannschaft und die Bar von außen.', ['Tafel', 'Bar', 'Teller']],
        ['plakate', 0, 1, 'Eure Plakate', 'seit 2023', 'ein', 'Eure Plakate', 'Jedes Plakat seit dem ersten Pop-up, mit Datum, Preis und seiner Farbe.', ['Plakate', 'Farbe je Abend']],
        ['menues', 0, 2, 'Eure Menüs', 'in Rudis Zeilen', 'ein', 'Eure Menüs', 'Die Gänge in Rudis Schreibweise und Momos Signature Drinks, wie ihr sie angekündigt habt.', ['Gänge', 'Drinks']],
        ['texte', 0, 3, 'Eure Worte', 'aus euren Beiträgen', 'ein', 'Eure Worte', 'Was ihr auf Instagram über eure Abende schreibt, ist der Grund jeder Zeile auf der Seite.', ['Beiträge', 'Bio']],
        ['zeichen', 0, 4, 'Euer Logo', 'Rudis Original', 'ein', 'Euer Logo', 'CULINARIUM und «A UNiQUE EXPERiENCE» aus Rudis Original-Logo, in jeder Größe scharf.', ['Logo']],
        ['haus', 0, 5, 'Das Haus', 'Walk on the Wild Side', 'ein', 'Das Haus', 'Die Bar in Linden mit Adresse, Zeiten und Geschichte, als Ort jedes Abends.', []],
        ['bildwelt', 1, 0, 'Bildwelt', 'jedes Foto mit festem Platz', '', 'Bildwelt', 'Jedes Foto liegt in mehreren Größen vor, für den Rechner und fürs Handy, und sitzt mit seinem Ausschnitt fest.', ['Ausschnitt', 'Größen']],
        ['abenddaten', 1, 1, 'Die Abende', 'eine Stelle', '', 'Die Abende', 'Jeder Abend mit Plakat, Datum, Uhrzeit, Preis und Plätzen an einer Stelle. Daraus entstehen die Vitrinen, die Chronik und die nächsten Termine.', ['Datum', 'Preis', 'Plakat']],
        ['karten', 1, 2, 'Karte je Abend', 'Menü und Drinks', '', 'Karte je Abend', 'Das Menü und die Drinks eines Abends als Blatt, für den Tisch und als PDF.', []],
        ['muster', 1, 3, 'Nacht und Kerze', 'auf den Flächen', '', 'Farben und Muster', 'Die Nacht der Bar, Schiefer und Warmweiß der Plakate und die Kerze aus euren Fotos, dazu ein feines Raster Ton in Ton.', ['Farben', 'Raster']],
        ['zeilen', 1, 4, 'Rudis Zeilen', 'als Schrift', '', 'Rudis Zeilen', 'Die Gänge in Versalien mit Schrägstrich, wie Rudi sie schreibt, als feste Schrift der Seite.', []],
        ['chronik', 1, 5, 'Chronik', '2017 bis heute', '', 'Chronik', 'Die Bar seit 2017, das erste Pop-up 2023, Rudi seit 2024 und der ausgebuchte September 2026.', []],
        ['start', 2, 0, 'Startseite', 'der Abend zuerst', 'seite', 'Startseite', 'Vom Auftakt über das erste Glas und drei Gänge zu den Plakaten, zum Haus, zu den Leuten und zu Dirty Chicken. Von hier führt ein Weg zu jeder Seite.', ['Glas', 'Gänge', 'Plakate']],
        ['abend', 2, 1, 'Der Abend', 'buchen und Warteliste', 'seite', 'Der Abend', 'Was auf den Tisch kommt, wann und wie viel, die nächsten Abende und die Warteliste.', ['Menü', 'Termine']],
        ['abende', 2, 2, 'Alle Abende', 'in Vitrinen', 'seite', 'Alle Abende', 'Jeder Abend mit seinem Plakat, Jahr für Jahr.', []],
        ['team', 2, 3, 'Haus und Team', 'Bar und Leute', 'seite', 'Das Haus und das Team', 'Die Bar in Linden, Derya, Momo und Rudi, und der Weg zur Haasemannstraße.', []],
        ['dc', 2, 4, 'Dirty Chicken', 'das Pop-up', 'seite', 'Dirty Chicken', 'Das Pop-up aus demselben Haus mit eigener Seite im eigenen Violett.', []],
        ['buchen', 3, 0, 'Platz buchen', 'mit Ticket', 'sys', 'Platz buchen', 'Im Entwurf gespielt: einen Abend wählen, Plätze wählen, zahlen, das Ticket kommt per Mail. Welches Kassensystem es wird, entscheidet ihr.', []],
        ['warteliste', 3, 1, 'Warteliste', 'ins Werkzeug', 'sys', 'Warteliste', 'Wer keinen Platz mehr bekommt, trägt sich ein. Der Eintrag kommt im Werkzeug für die Gäste an, nie als Mail.', []],
        ['pdf', 3, 2, 'Karten als PDF', 'zum Teilen', 'sys', 'Karten als PDF', 'Jede Karte eines Abends liegt zusätzlich als PDF bereit.', []],
        ['studio', 3, 3, 'Sieben Werkzeuge', 'für euch', 'sys', 'Sieben Werkzeuge', 'Mit ihnen tragt ihr Termine, Menüs, Plakate und Texte selbst ein; jede Änderung wartet als Entwurf.', ['Termine', 'Menüs', 'Plakate']],
    ]
    k = [['fotos', 'bildwelt'], ['plakate', 'abenddaten'], ['plakate', 'muster'], ['menues', 'karten'], ['menues', 'zeilen'], ['texte', 'start'], ['zeichen', 'muster'], ['haus', 'chronik'],
         ['bildwelt', 'start'], ['bildwelt', 'team'], ['abenddaten', 'abend'], ['abenddaten', 'abende'], ['zeilen', 'start'], ['chronik', 'team'], ['muster', 'dc'],
         ['abend', 'buchen'], ['abend', 'warteliste'], ['karten', 'pdf'], ['studio', 'abend'], ['studio', 'abende'], ['studio', 'start']]
    return {'sp': ['Von euch', 'Daraus gemacht', 'Die Seiten', 'Im Hintergrund'], 'fx': [0.118, 0.372, 0.628, 0.882], 'n': n, 'k': k,
            'tour': ['fotos', 'plakate', 'menues', 'buchen', 'warteliste', 'studio'], 'fuss': 'Folgt einer Linie: Sie führt von dem, was von euch kommt, zur Seite',
            'start': ['Übersicht', 'Von euch zur Seite', 'Tippt eine Kachel an, dann leuchtet ihr Weg. Oder startet den Rundgang.']}


# ---------- Für eure Gäste (Gäste-Funktionen der Website, Aufnahmen sb_ideen.js → ansichten/Gaeste) ----------
GAESTE = [
    ('buchen', 'Platz buchen', 'Einen der nächsten Abende wählen, Plätze wählen und zahlen; das Ticket kommt per Mail. Im Entwurf ist die Zahlung nur gespielt.', '50% 0'),
    ('warteliste', 'Die Warteliste', 'Ist ein Abend voll, trägt sich der Gast auf dem Ticket ein: Freitag, Samstag oder egal, wie viele Plätze, Name und Mail.', '50% 50%'),
    ('menue', 'Was auf den Tisch kommt', 'Aperitif, drei Gänge und fünf Drinks auf einen Blick, mit Bildern aus euren Abenden.', '50% 50%'),
    ('zeiten', 'Wann und wie viel', 'Freitag ab 19 Uhr, Samstag ab 17 Uhr, die Plätze an der Tafel und der Preis des letzten Abends, groß und klar.', '50% 50%'),
    ('fragen', 'Gut zu wissen', 'Was Gäste vor ihrem ersten Abend wissen wollen, mit einer Antwort zum Antippen.', '50% 50%'),
    ('weg', 'Der Weg', 'Die Bar an der Ecke Haasemannstraße und Rampenstraße, auf einer Karte im Stil des Hauses.', '50% 50%'),
]
GAESTE_TEL = []
GAESTE_KNOEPFE = [('Platz buchen', '../abend.html#termine-buchen'), ('Auf die Warteliste', '../abend.html#warteliste'), ('Der Weg', '../weg.html')]
GAESTE_LINK = '../abend.html'
GABEN['gaeste'] = 'Platz buchen, die Warteliste, das Menü, die Zeiten, die Fragen und der Weg.'

# ---------- Handschrift (marke_werkbank.py) ----------
HANDSCHRIFT = dict(
    text='Eure Plakate haben schon alles, was eine Marke braucht: die Wortmarke, zwei feste Farben und je Abend eine eigene. Die Seite nimmt das auf, dazu eine weiche Titelschrift für die großen Zeilen, Rudis Zeilen in Versalien und die Kerze aus euren Fotos.',
    marke_etik='Logo und Zeichen', marke_text='Euer Logo kommt aus Rudis Original und bleibt in jeder Größe scharf: Schiefer auf Warmweiß, Warmweiß auf Dunkel, nie neu gesetzt.',
    schriften=[], farben=[], farben_etik='aus Plakaten und Fotos',
    muster_etik='Das feine Raster',
    muster_text='Auf den dunklen Flächen liegt ein feines Raster Ton in Ton. Man findet es auf der Seite, auf den Karten und auf jeder Drucksache.',
    knopf_text='Diese Knöpfe darf man drücken.', knoepfe=('Ausprobieren', 'Noch einmal'))

# ---------- Feed, Papier, Dateien ----------
FEED = dict(art='bogen', bogen=[1, 2, 3, 4, 5, 6, 7, 8, 9], bogen_zeile='Die ersten drei Reihen',
            text1='', text2='Tippt auf den Bildschirm, dann scrollt ihr durch den Feed wie am Handy.', kacheln=[])
PAPIER = dict(
    etik_text='An der Theke stehen Momos Drinks auf Untersetzern: zwölf Ideen in den Abendfarben eurer Plakate, mit dem C und euren Zeilen.',
    druck_text='Von der Karte am Platz bis zum Deckblatt für die Presse, dazu <a href="../sticker/index.html" target="_blank" rel="noopener">40 Sticker</a> und <a href="../beigaben/index.html" target="_blank" rel="noopener">fünf Beigaben</a>.',   # Kapitel VI (Prüfchat Gestaltung 29.10.2026)
    orte_e=[(3, 6, 28, -3), (36, 6, 28, 2), (69, 6, 28, -2), (3, 54, 28, 2), (36, 54, 28, -3), (69, 54, 28, 3)],   # drei mal zwei mit Abstand, nichts überdeckt (Robert 29.10.2026)
    orte_d=[('karte', 3, 16, 29, -3, 0), ('ausgebucht', 35.5, 16, 29, 2, 0), ('dc-flyer', 68, 16, 29, -2, 0)])   # drei Blätter nebeneinander (Robert 29.10.2026)
PAPIER_SEITE = dict(
    breit={'karte', 'karte-r', 'ticket', 'ticket-r', 'briefbogen', 'umschlag'},
    formen=set(),
    auslage=[('karte', 2, 2, 26, -6), ('ticket', 32, 8, 58, 3), ('drink-1', 74, 44, 17, 7), ('drink-2', 56, 56, 17, -4), ('karte-r', 6, 50, 26, 4), ('umschlag', 28, 70, 42, -3)],
    karton={'karte': ('', [('karte', 44, 'Vorderseite'), ('karte-r', 44, 'Rückseite')]),
            'drinks': ('', [('drink-1', 30, 'Fatwashing'), ('drink-2', 30, 'Milkwashing'), ('drink-3', 30, 'Enzyme')]),
            'ticket': ('', [('ticket', 88, 'Vorderseite'), ('ticket-r', 88, 'Rückseite')]),
            'briefpapier': ('', [('umschlag', 92, 'Umschlag'), ('briefbogen', 38, 'Briefbogen')])},
    titel={'karte': ['Die Karte', 'am Platz.'], 'drinks': ['Ein Kärtchen', 'zu jedem Drink.'], 'ticket': ['Ein Ticket', 'zum Mitnehmen.'], 'briefpapier': ['Briefbogen', 'und Umschlag.']},
    schatten={'karte', 'drinks', 'ticket', 'briefpapier'},
    flaeche=['fl--papier', 'fl--nacht tapete-leicht', 'fl--papier', 'fl--creme'],
    etik_titel=('Untersetzer', 'für die Theke.'),
    etik_text='Zum Drink an der Theke gehört ein Untersetzer. Hier sind {n} als Idee: sechs in den Abendfarben eurer Plakate, sechs auf der Nacht der Bar mit euren Zeilen.',
    etik_kap='Die Untersetzer', etik_kopf=['Zwölf', 'Untersetzer.'],
    etik_kopftext='Die Farben kommen von euren Plakaten, das C aus Rudis Wortmarke, die Zeilen von euren Abenden.',
    druck_text='Papier, das bei euch auf der Tafel, an der Theke oder im Umschlag landen könnte. Was nicht passt, lasst ihr einfach weg.',
    etik_auslage=[(2, 4, 30, -5), (35, 0, 30, 4), (68, 6, 30, -3), (4, 36, 30, 3), (37, 36, 30, -4), (70, 40, 28, 5), (12, 66, 28, 2), (46, 68, 28, -3), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)])
# Weitere Drucksachen (Prüfchat Gestaltung 29.10.2026): Karton, Titel und Breite je Stück aus papier_neu_seite.json (geschrieben von papier.py)
try:
    for _k, _v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'papier_neu_seite.json'), encoding='utf-8')).items():
        PAPIER_SEITE['karton'][_k] = (_v['karton'][0], [tuple(x) for x in _v['karton'][1]]); PAPIER_SEITE['titel'][_k] = _v['titel']
        PAPIER_SEITE['breit'].update(_v['breit']); PAPIER_SEITE['schatten'].add(_k)
except FileNotFoundError:
    pass
MATERIAL = dict(
    text='Was für den Entwurf neu entstanden ist, liegt sortiert in einem Ordner: die Karten als PDF, die Drucksachen, die Untersetzer, die Sticker, die Beigaben, die Postkarten, die Beiträge für Instagram und euer Logo als Datei.',
    streu=[(bild('m3'), 'Gläser mit Goldrand', -4, '-0.05'), (bild('schaum'), 'Schaum aus dem Siphon', 3, '0.04'), (bild('m5'), 'Haselnüsse', -2, '-0.07'),
           (bild('flaschen'), 'An der Bar', 4, '0.05'), (bild('baiser'), 'Baiser mit Beeren', -3, '-0.04')],   # kein Foto, das sonst auf der Werkbank steht
    druck_satz='Von der Karte am Platz bis zur Einladung für Stammgäste.',
    zeichen=[('Euer Logo', '../../_quelle/logo/original/culinarium-logo-original.svg', 'Culinarium Logo.svg')],   # Rudis Original (28.10.2026), wie auf der Website
    zeichen_satz='Rudis Original-Logo als Zeichnung, die in jeder Größe scharf bleibt.',
    auslage=[])
AUSBLICK = dict(text='Ein paar Dinge fehlen noch.', gross=('', '', ''), punkte=[], studio='')
SCHLUSS = dict(bild=bild('barnacht'))
KAPITEL = {
    'vergleich': dict(text=VERGLEICH_TEXT),
    'ideen': dict(text='Hinter jeder Stelle der Seite steht ein Gedanke. Zwölf davon sind hier aufgenommen, so wie die Seite heute aussieht.'),
    'gefuege': dict(text='Links, was von euch kommt, in der Mitte, was daraus geworden ist, rechts die Seiten und was im Hintergrund mitläuft.'),
    'seiten': dict(text='Eine Seite aussuchen, mit den Pfeilen weiterblättern. Rechts dieselbe Stelle am Handy, mit «Öffnen» seid ihr auf der echten Seite.'),
    'unterlagen': dict(text=UNTERLAGEN['text']),
    'gaeste': dict(text='Wer einen Abend bucht, will vorher wissen, was auf den Tisch kommt, wann es losgeht und wie er hinfindet. Auf der neuen Seite steht das an einem Ort, und ist ein Abend voll, bleibt der Gast auf der Warteliste.'),
    'papier': dict(text='Für Culinarium ist einiges entstanden: zwölf Untersetzer für Momos Drinks, 24 Drucksachen von der Karte am Platz bis zum Flyer, Mails für eure Gäste und eine Postkarte zu jedem Plakat.'),
    'material': dict(text='Wer eine Datei braucht, findet sie hier: jede Karte als PDF, jede Drucksache, jeden Untersetzer und euer Logo in voller Schärfe.'),
    'geprueft': dict(text='Bevor etwas davon zu euch kommt, wird es geöffnet, gelesen und gedrückt: am Handy wie am Rechner, jede Karte gegen eure Angaben, jedes Werkzeug in jedem Schritt. Das Blatt fasst es zusammen, der Bericht erzählt es ganz.'),
    'schluss': dict(text='Sagt mir offen, was euch am Entwurf gefällt und was nicht. Ändern lässt sich alles.'),
}
MEINS = ['Der Brief und alle Sätze der Werkbank', 'Titel und Sätze zu den Ideen, zum Gefüge, zu den Drucksachen und Untersetzern', 'Feldnamen und Zeilen auf Ticket und Platzkarte', 'Texte zu den Beiträgen des Feeds']

# ---------- Geprüft (nur Belegtes; Belege in website/_werkbank/pruefung/, Karten von La Carte, Werkzeuge aus ihren Lieferungen) ----------
import datetime as _dt
GEPRUEFT = [
    ('Die Website', 'seite', ['Alle Seiten in der Technik von Safari und von Chrome, am Handy und am Rechner: nichts läuft seitlich über, kein Skriptfehler, kein kaputtes Bild.',
                              'Auf vier- und sechsfach gebremster Rechenleistung gemessen, wie auf einem schwachen Gerät: Das Scrollen bleibt flüssig.',
                              'Jede Angabe kommt aus einer Stelle mit Quelle: Termine, Zeiten, Adresse, Menüs und Preise.']),
    ('Die Karten', 'karte', ['Jede Karte aus euren Angaben gelesen, nicht abgetippt.',
                             'Was ihr klären müsst, steht gesondert in der Liste der offenen Punkte.']),
    ('Die Werkzeuge', 'schloss', ['Jedes der sieben Werkzeuge in einem eigenen Durchgang gebaut und Knopf für Knopf bedient, nur mit erfundenen Daten.',
                                  'Kein Werkzeug verschickt etwas von selbst, keines öffnet ein Mailprogramm.']),
]
GEPRUEFT_PUNKTE = [
    ('Die Website', 'Jede Seite einmal am Handy und einmal am Rechner, in Safari und in Chrome. Auch ein älteres Gerät scrollt ruhig durch, nichts rutscht zur Seite.'),
    ('Die Karten', 'Gelesen aus euren eigenen Angaben, nicht abgeschrieben. Jeder Gang und jeder Drink steht so, wie ihr ihn angekündigt habt.'),
    ('Die Werkzeuge', 'Jedes der sieben in seinem eigenen Durchgang bedient, mit erfundenen Gästen und Zahlen. Keines schickt von sich aus eine Nachricht.'),
    ('Eure Daten', 'Gäste bekommen keine Kekse in den Browser. Was sie buchen oder auf die Warteliste schreiben, landet bei euch, und im Entwurf nie beim echten Haus.'),
]
GEPRUEFT_TRIO = [(bild('pass'), 1.6, (.5, .5), 'Am Pass'), (bild('klaeren'), 1.6, (.5, .5), 'An der Bar'), (bild('schildnacht'), 1.6, (.5, .5), 'An der Ecke')]
GEPRUEFT_OFFEN = 'Ein paar Fragen könnt nur ihr beantworten: wessen Angaben ins Impressum kommen, wer an welchem Foto und Plakat die Rechte hat und wer welches Werkzeug bekommt.'   # ohne «Vertragspartner» (Robert 1.11.2026)
GEPRUEFT_EIN = 'Hier steht in einfachen Worten, was an Website, Karten und Werkzeugen angesehen und ausprobiert wurde, und was danach noch bei euch liegt.'
GEPRUEFT_NAV = ['Website', 'Karten', 'Werkzeuge', 'Daten', 'Offen']
GEPRUEFT_MEHR = [
    ('Die Website', 'seite', 'Neun Seiten: sieben für eure Gäste von der Startseite bis Dirty Chicken, dazu Impressum und Datenschutz.', [
        'Jede Seite in Safari und in Chrome geöffnet, auf dem Handy und auf dem Rechner. Nichts verrutscht zur Seite, kein Bild fehlt, kein Skript bricht ab.',
        'Mit vier- und sechsfach gebremstem Rechner gescrollt, wie auf einem älteren Gerät. Die Seiten laufen ruhig, beim Laden springt nichts.',
        'Termine, Zeiten, Adresse, Menüs und Preise stehen an genau einer Stelle, mit ihrer Quelle, und jede Seite liest von dort.']),
    ('Die Karten', 'karte', 'Die Karte jedes Abends: Menü in Rudis Zeilen und Momos Drinks.', [
        'Gelesen aus euren Beiträgen und Unterlagen, nicht abgeschrieben.',
        'Neu gesetzt im Kleid der neuen Seite, die Schriften fest eingebettet.']),
    ('Die sieben Werkzeuge', 'schloss', 'Die Werkzeuge, mit denen ihr Termine, Menüs, Plakate und Gäste selbst führt.', [
        'Jedes Werkzeug in seinem eigenen Durchgang gebaut und Schritt für Schritt bedient, mit erfundenen Gästen und Zahlen.',
        'Kein Werkzeug schickt etwas von sich aus und keines öffnet ein Mailprogramm. Antworten an Gäste bleiben als Entwurf im Werkzeug, bis jemand sie selbst verschickt.']),
    ('Eure Daten und die eurer Gäste', 'schild', 'Was gespeichert wird und was nicht.', [
        'Gäste bekommen keine Cookies. Im Entwurf werden keine Besuche gezählt; ' + _nf.klein(_werkzeugname('besuche')) + ' zeigt erfundene Zahlen.',
        'Buchung und Warteliste laufen im Entwurf nur zur Probe; es fließt kein Geld, und nichts davon erreicht das echte Haus.',
        'Suchmaschinen sehen den Entwurf nicht, bis ihr ihn freigebt.']),
    ('Was offen bleibt', 'auge', 'Das könnt nur ihr entscheiden.', [
        'Wessen Angaben im Impressum stehen, und wie Culinarium und die Bar zueinander stehen.',
        'Wer an welchem Foto und an den Plakaten die Rechte hat.',
        'Im Entwurf öffnen sich die Werkzeuge ohne Anmeldung. Zum Umzug bekommt jede Person ihren eigenen Zugang.'])]
PRUEFDATUM = _dt.date(2026, 10, 30)
STEMPEL_TEXT = f'GEPRÜFT · CULINARIUM · {PRUEFDATUM:%d.%m.%Y} ·'
GEPRUEFT_BILD = bild('pass')

# ================================================================ Bausteine (Vorlage Schäfli, kopiert und umgeschrieben; Kit unverändert)
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
EIGENE, EIGENE_BILDER, FLAECHE = [], [], {}
CSS = ''
_WB = os.path.join(ROOT, 'werkbank')

import brief_blatt as _bb  # noqa: E402
brief_abschnitt = _bb.abschnitt(globals())
EIGENE_BILDER += _bb.bilder(BRIEF)
CSS += _bb.CSS
import kopf_mitte as _km  # noqa: E402
import auftakt_kacheln as _ak  # noqa: E402
CSS += _km.CSS + _ak.CSS
FLAECHE.update(brief='fl--papier tapete-hell', vergleich='fl--nacht tapete-leicht', ideen='fl--blau tapete-leicht', gefuege='fl--nacht tapete-leicht',
               seiten='fl--papier tapete-hell', gaeste='fl--navy tapete', unterlagen='fl--tief tapete-leicht', papier='fl--navy tapete', material='fl--papier tapete-hell',
               feed='fl--nacht tapete-leicht', geprueft='fl--navy tapete')
CSS += '''
/* ---------- Leichte Tapete: das feine Raster der Website auf jeder dunklen Fläche ---------- */
.tapete-leicht{background-image:linear-gradient(var(--tl),var(--tl)),var(--muster);background-size:auto,var(--musterb) auto;background-position:0 0,50% 0}
.fl--nacht.tapete-leicht{--tl:rgba(22,21,26,.35)}
.fl--blau.tapete-leicht{--tl:rgba(58,56,69,.3)}
.fl--tief.tapete-leicht{--tl:rgba(28,27,33,.35)}
.tapete-hell{background-image:url(/assets/zeichen/tapete-hell.svg);background-size:224px auto;background-position:50% 0}
/* ---------- Titel wie auf der Website: Fraunces mit weichen Enden, leicht, normale Schreibung, Betonung nur über die Farbe, nie fett, nie kursiv ---------- */
.zt,.t1,.t2,.t3,.wfen__t,.ins-t h3,.rgw .wfa__texte h3,.sbf-text h3,.hs2-ww+small{font-weight:340!important;font-variation-settings:"SOFT" 100,"WONK" 0}
.zt{text-transform:none;letter-spacing:-.012em}
.zt em,em{font-style:normal}
.kap--k .kap__geist{display:none}.kap--z span,.kap--k>span{font-family:var(--mono)!important;font-weight:400!important;font-size:12px!important;letter-spacing:.2em;text-transform:uppercase}
.wfen__t{text-transform:none;letter-spacing:-.01em}
h2,h3,.wege__t,.gb-blatt header h3,.rgw .wfa__texte h3,.fbz__n{font-weight:340!important;font-variation-settings:"SOFT" 100,"WONK" 0}
b,strong{font-weight:500}
.gb-blatt header h3{font-family:var(--serif);text-transform:uppercase;letter-spacing:.135em}
.wf .wege__t{font-family:var(--serif);text-transform:none;letter-spacing:-.01em;font-size:clamp(2rem,3.6vw,3.4rem)!important;line-height:1.1}
/* Rudis Zeilen: Versalien mit Schrägstrich, Urbanist wie die Zeile mit dem kleinen i */
@font-face{font-family:'Urbanist';font-style:normal;font-weight:100 900;font-display:swap;src:url('/assets/schrift/urbanist.woff2') format('woff2')}
.rz{font-family:'Urbanist',var(--sans);font-weight:500;letter-spacing:.16em;text-transform:uppercase}
'''

import marke_werkbank as _mw  # noqa: E402
EIGENE.append(_mw.abschnitt(globals())); EIGENE_BILDER += _mw.BILDER; CSS += _mw.CSS
FLAECHE['handschrift'] = 'fl--navy tapete'
import mails_reihe as _mr  # noqa: E402
CSS += _mr.CSS
EIGENE_BILDER += _mr.BILDER   # die drei Mails als dritte Karte im Papier (wb_kapitel.papier_mails)
import feed_buehne as _fb  # noqa: E402
_FEED_DA = os.path.exists(os.path.join(ROOT, 'feed', 'feed.json'))
if _fb.BEREIT and _FEED_DA:
    EIGENE.append(_fb.abschnitt(globals())); EIGENE_BILDER += _fb.BILDER; CSS += _fb.CSS
import fenster_ausblick as _fa  # noqa: E402
CSS += _fa.CSS
import geprueft_blatt as _gb  # noqa: E402
geprueft_abschnitt = _gb.abschnitt(globals())
_AN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ansichten')
for _i, _q in enumerate([os.path.join(_AN, 'Rechner', 'Startseite.jpg'), os.path.join(ROOT, 'unterlagen', 'img', 'n-abend-01.webp'),
                         os.path.join(_AN, 'Werkzeuge', 'bureau.jpg'), os.path.join(_AN, 'Gaeste', 'buchen.jpg')]):
    if os.path.exists(_q):
        EIGENE_BILDER.append((f'gp-{_i}', _q, 320, dict(q=80, schnitt=4 / 3, lage=(.5, 0))))
CSS += _gb.CSS

import fuss_faecher as _ff  # noqa: E402
if _ff.BEREIT:
    wege_abschnitt = _ff.abschnitt
    CSS += _ff.CSS
CSS += '''
/* Dateien: Fotos ohne Polaroid-Rand und ohne Bildzeile, ungleich groß, ohne Drehung */
#material .streu .abzug{padding:0!important;background:none!important;border-radius:clamp(10px,1vw,14px);overflow:hidden;--r:0deg!important;--r0:0deg!important;box-shadow:0 30px 40px -26px rgba(8,7,10,.6),0 10px 16px -10px rgba(8,7,10,.35)!important}
#material .streu .abzug span{display:none!important}
#material .streu .abzug img{display:block;width:100%;height:100%;object-fit:cover;border-radius:0!important}
@media(min-width:760px){#material .streu{align-items:center}#material .streu .abzug:nth-child(3){transform:scale(1.18);z-index:2}#material .streu .abzug:nth-child(2),#material .streu .abzug:nth-child(4){transform:scale(1.04);z-index:1}}
/* Flüssigkeit (Regel 55): Abschnitte außerhalb des Blicks werden nicht gezeichnet. Ausgenommen der Brief (überstehendes Blatt). */
@supports (content-visibility:auto){main>section.fl:not(#brief){content-visibility:auto;contain-intrinsic-size:auto 1400px}}
html.cv-alle main>section.fl:not(#brief){content-visibility:visible}
@media(min-width:760px){.vh-wahl>:first-child,#seiten .wahl>:first-child{margin-left:auto}.vh-wahl>:last-child,#seiten .wahl>:last-child{margin-right:auto}}
@media(max-width:480px){.kn{max-width:100%;height:auto;min-height:54px;padding-top:9px;padding-bottom:9px;white-space:normal;line-height:1.35;text-align:left}.kn i{flex:none}.kn-reihe{max-width:100%}}
.schluss .zt,.schluss .lauf p,.schluss .kap span{text-shadow:0 1px 2px rgba(8,7,10,.9),0 2px 16px rgba(8,7,10,.8),0 0 42px rgba(8,7,10,.55)}
'''


CV_JS = ("<script id=\"cv-hoehen\">(function(){var d=document.documentElement;function alle(){d.classList.add('cv-alle');requestAnimationFrame(function(){requestAnimationFrame(function(){d.classList.remove('cv-alle')})})}"
         "/* einmal alles zeichnen, damit jede Fläche ihre echte Höhe kennt: Sprungmarken landen genau (content-visibility) */"
         "if(document.readyState==='complete')setTimeout(alle,300);else addEventListener('load',function(){setTimeout(alle,300)});"
         "addEventListener('resize',function(){clearTimeout(alle.t);alle.t=setTimeout(alle,400)})})();</script>")
BRETT_HILFE = ("<script id=\"brett-hilfe\">(function(){var b=document.getElementById('brett'),k=document.getElementById('brett-noch');if(!b||!k||!('IntersectionObserver' in window))return;"
               "new IntersectionObserver(function(E,o){if(!E[0].isIntersecting)return;o.disconnect();setTimeout(function(){if(/\\bvor\\b/.test(b.className))k.click()},700)},{rootMargin:'0px 0px -35% 0px'}).observe(b)})();</script>")


def nach_bau():
    """Nach jedem Bau des Kits: Eigenes nach werkbank/eigen, Nacharbeit der Bausteine, Kapitel, Ruhe, Farben, Ihr-Form."""
    import re as _re, shutil as _sh
    from PIL import Image as _I
    q, z = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen'), os.path.join(_WB, 'eigen')
    os.makedirs(z, exist_ok=True)
    sig = _I.open(os.path.join(q, 'unterschrift-robert.webp')).convert('RGBA')
    r, g, b = (int(FARBEN['tinte'][i:i + 2], 16) for i in (1, 3, 5))
    _I.merge('RGBA', (*_I.new('RGB', sig.size, (r, g, b)).split(), sig.getchannel('A'))).save(os.path.join(z, 'unterschrift.webp'), 'WEBP', quality=90)
    _fa.fenster_bilder()
    for f in os.listdir(q):
        if f.startswith('fen-'):
            _sh.copy2(os.path.join(q, f), os.path.join(z, f))
    if _fb.BEREIT and _FEED_DA:
        _fb.bilder()
    if _ff.BEREIT:
        _ff.bilder()
    seite = os.path.join(_WB, 'index.html')
    _ak.anwenden(seite)
    _mw.anwenden(seite)
    _fa.anwenden(seite)
    _km.anwenden(seite)
    import fluss_werkbank as _fw
    _fw.anwenden(seite)
    import wb_kapitel as _kp
    _kp.anwenden(seite)
    # Nichts läuft mit dem Scrollen mit (Regel 55)
    t = open(seite, encoding='utf-8').read()
    t = _re.sub(r'\sdata-(?:drift|zug)="[^"]*"', '', t)
    ruhe = ('<style id="sb-ruhe">.bf .bf-blatt[data-a="heben"],.bf .bf-blatt[data-a="heben"].da{animation:none!important}.kap__geist{animation:none!important}'
            '.kn:hover,.kn:active,.rund:hover,.rund:active,.wahl button:active,.vh-wahl button:active,.bn button:hover,.bn button:active,.glanz:active,.ins-r:hover,.ins-r:active,.wf__pf:hover,.wf__pf:active,.rgc-p:hover,.rgc-p:active,.sbf-z:hover{transform:none!important;translate:none!important;scale:none!important}'
            '.kn{overflow:hidden}.ins-reiter,.fb__reiter{padding-top:10px!important;padding-bottom:26px!important;margin-top:-10px!important;margin-bottom:-26px!important}'
            '.wahl,.vh-wahl{padding-top:8px!important;padding-bottom:26px!important;margin-top:-8px!important;margin-bottom:-12px!important}'
            '.wfen .wfen__t{font-size:clamp(24px,3.6vw,54px)!important;line-height:1.14!important}.wfen .wfen__k{font-size:clamp(15px,1.36vw,19px)!important}'
            '#papier img.frei{filter:none!important;box-shadow:none!important}</style>')
    if 'id="sb-ruhe"' not in t:
        t = t.replace('</head>', ruhe + '</head>', 1)
    if 'id="brett-hilfe"' not in t:
        t = t.replace('</body>', BRETT_HILFE + '</body>', 1)
    if 'id="cv-hoehen"' not in t:
        t = t.replace('</body>', CV_JS + '</body>', 1)
    import sb_skripte as _sk
    for _id, _js in (('rh-vorladen', _sk.VORLADEN_JS), ('rh-frueh', _sk.FRUEH_JS), ('rh-zurueck', _sk.WB_JS), ('rh-karussell', _sk.KARUSSELL_JS)):
        if f'id="{_id}"' not in t:
            t = t.replace('</body>', _js + '\n</body>', 1)
    open(seite, 'w', encoding='utf-8').write(t)
    import feed_leicht as _fl
    if _fb.BEREIT and _FEED_DA:
        _fl.mach()
    import sb_farbe
    sb_farbe.anwenden()
    # Das Zeichen in Kerze als Datei für die Karte «Die Übergabe.» (als <img> wäre currentColor schwarz)
    vb, innen = ZEICHEN
    open(os.path.join(_WB, 'eigen', 'zeichen-kerze.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="{FARBEN["messing"]}">{innen}</svg>')
    open(os.path.join(_WB, 'eigen', 'zeichen-c.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="#000">{innen}</svg>')   # Maske für Schmuck im CSS (Listen, Namenszug)
    _ft = os.path.join(ROOT, 'feed', '_tafeln.html')
    if os.path.exists(_ft):
        _s = open(_ft, encoding='utf-8').read()
        if 'noindex' not in _s:
            _s = _s.replace('<head>', '<head><meta name="robots" content="noindex, nofollow">', 1) if '<head>' in _s else '<meta name="robots" content="noindex, nofollow">' + _s
            open(_ft, 'w', encoding='utf-8').write(_s)
    import sb_ki   # Seite «KI und eure Daten», Karte «Die Übergabe.» allein und als PDF (Robert 20.10.2026, 1.11.2026)
    sb_ki.bau()
    import du_gang   # zuletzt: die Sätze aus Kit und Vorlage von der Sie- in die Ihr-Form, deutsche Schreibung
    du_gang.anwenden()
    import nur_bewegung   # bewegt nur transform/opacity, Glanzkante dreht statt neu zu malen, Karte kommt herein (Abnahme-Tor 30.10.2026)
    nur_bewegung.anwenden(ROOT)
    import zeile_ganz   # kein Einzelwort allein in der letzten Titelzeile, Aufschrift im Fensterstapel frei (Abnahme-Tor 30.10.2026)
    zeile_ganz.anwenden(ROOT)
    import text_mitte   # Schrift optisch mittig in den Knöpfen aller Werkbank-Seiten (Messlauf «text-mitte», 29.10.2026)
    text_mitte.anwenden(ROOT)
    import bild_mass   # Bilder in der gezeigten Grösse, damit der Tab in WebKit nicht am Speicher scheitert (Abnahme-Tor 4, 30.10.2026)
    bild_mass.anwenden(ROOT)


TITEL_NEU = {   # eigene Überschriften von Culinarium (Werkbank-Regel 14), keine gleich wie beim Schäfli oder Schlössli
    ('Schön, dass Sie', 'hereinschauen.'): ('Schön, dass', 'ihr da seid.'),
    ('Ihre Website,', 'Seite für Seite.'): ('Heute im Netz,', 'morgen eine Seite.'),
    ('Die Ideen', 'hinter der Seite.'): ('Zwölf Stellen,', 'zwölf Gedanken.'),
    ('Wie alles', 'zusammenhängt.'): ('Was hinter', 'dem Abend steht.'),
    ('Alle Seiten zum', 'Durchblättern.'): ('Von der Tafel', 'bis Dirty Chicken.'),
    ('Vorschläge für', 'Ihre Gäste.'): ('Bevor der Gast', 'Platz nimmt.'),
    ('Ihre Unterlagen,', 'im selben Stil.'): ('Eure Karten,', 'Abend für Abend.'),
    ('Ein paar Ideen', 'für Papier.'): ('Für Tafel', 'und Theke.'),
    ('Ein Feed', 'für Instagram.'): ('Ein Feed,', 'der nach Abend aussieht.'),
    ('Alles liegt für', 'Sie bereit.'): ('Alle Dateien', 'an einem Ort.'),
    ('Alles geprüft,', 'bevor Sie es sehen.'): ('Ausprobiert,', 'Stück für Stück.'),
}
TEXT_NEU = [   # Sätze des Kits, die fürs Haus nicht stimmen (wb_kapitel.eigene_titel ersetzt sie wörtlich)
    ('Links Ihre Seite, wie sie heute ist, rechts der Entwurf. Schieben Sie den Griff hin und her, daneben steht, was neu ist.', VERGLEICH_TEXT),
]
KAP_NAME_NEU = {'Guten Tag': 'Ein Brief', 'Register': 'Inhalt', 'Zum Schluss': 'Bis Montag'}


# Farben und Schnitte schon in H.CSS setzen: baut ein anderer Schritt mit dem Kit (K.gestaltung), stehen so trotzdem die Töne des Hauses
# und kein fetter Schnitt in werkbank.css, nicht erst nach dem Farbgang.
import sb_farbe as _sf  # noqa: E402
CSS = _sf.ohne_fett(_sf.faerbe(CSS))

# Gestaltung 28.10.2026 (Prüfchat Gestaltung): Unterlagen «Heute und als Idee»: das Foto der Karte vom Tisch hat das Format des Blatts daneben (A-Format),
# beide Seiten gleich hoch, nicht ein langes Foto neben einem kürzeren Blatt (Regel «Spalten gleich hoch»).
CSS_SEITEN = '''
.upaar{align-items:center}
.ublatt--alt .ublatt__b{aspect-ratio:1/1.414!important}
.ublatt--alt .ublatt__b img{width:100%;height:100%;object-fit:cover}
'''
