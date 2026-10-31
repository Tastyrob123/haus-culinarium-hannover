#!/usr/bin/env python3
"""Werkbank Culinarium: Ihr-Form und deutsche Schreibung (Werkbank-Chat 28.10.2026). Kit und Vorlagen (Schäfli, Schlössli, Ruedihus) sprechen
im Sie und schreiben Schweizer «ss». Robert und Rudi duzen sich, die Website spricht im Du: die Werkbank spricht Rudi, Momo und Derya mit «ihr» an.
Läuft als letzter Schritt nach jedem Bau über die gebauten Seiten des Reviers (nur Text, nie Adressen, Skripte oder Bilder) und meldet, was
danach noch nach Sie klingt. Mehrfach anwendbar."""
import glob, os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
ERSATZ = [   # (alt, neu) ganze Wendungen, wie sie Kit und Vorlage schreiben (gefunden mit dem Suchlauf am Ende dieser Datei, 28.10.2026)
    ('Dazu gibt es zwölf Untersetzer und Ihre Unterlagen im selben Stil.', 'Dazu gibt es zwölf Untersetzer und eure Karten im selben Stil.'),
    ('Drucksachen und Ihre Unterlagen im selben Stil.', 'Drucksachen und eure Karten im selben Stil.'),
    ('Originalgrösse', 'Originalgröße'),
    ('in voller Grösse', 'in voller Größe'),
    ('Sie bereit.', 'euch bereit.'),
    ('Sie können jede Datei ansehen und herunterladen.', 'Ihr könnt jede Datei ansehen und herunterladen.'),
    ('Ihre Unterlagen,', 'Eure Karten,'),
    ('Wählen Sie eine Unterlage und blättern Sie mit den Pfeilen. Links steht Ihre heutige Fassung, rechts die Idee im Stil der neuen Seite.', 'Wählt eine Karte und blättert mit den Pfeilen. Links steht die Karte, wie sie auf dem Tisch lag, rechts die Idee im Stil der neuen Seite.'),
    ('Adresse, Telefon, Reservation, Karte und Öffnungszeiten werden beim Freigeben', 'Adresse, Termine, Plätze und Zeiten der Abende werden beim Freigeben'),
    ('So kann eine KI, die Gästen bei der Suche hilft, Ihre Karte, Anlässe und Angebote auch wirklich lesen.', 'So kann eine KI, die Gästen bei der Suche hilft, eure Abende, Menüs und Plakate auch wirklich lesen.'),
    ('Ersetzt die neue Seite Ihre heutige, führt jede bisherige Adresse auf die passende neue Seite. So geht kein Platz in den Suchergebnissen verloren, und kein geteilter Link läuft ins Leere.',
     'Heute gibt es keine Website. Die neue Seite bekommt eine eigene Adresse, und der Link in der Bio auf Instagram führt dorthin; so findet jeder, der euch sucht, denselben Weg.'),
    ('Für Ihre Gäste', 'Für eure Gäste'),
    ('Wenn Sie zu einem Punkt mehr wissen möchten, fragen Sie mich einfach.', 'Wenn ihr zu einem Punkt mehr wissen möchtet, fragt mich einfach.'),
    ('unter Ihrer eigenen Adresse', 'unter eurer eigenen Adresse'),
    ('Was ausserhalb der Website zählt, gehört genauso dazu: der Eintrag bei Google Maps, Ihre Bewertungen und gleiche Angaben auf Tripadvisor, den Restaurantführern und Portalen.',
     'Was außerhalb der Website zählt, gehört genauso dazu: ein Eintrag bei Google Maps und gleiche Angaben überall, wo Culinarium genannt wird.'),
]


def seiten():
    for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        r = os.path.relpath(p, ROOT)
        if r.split(os.sep)[0] in ('_werkbank', 'assets', 'pruefung') or r.startswith('feed' + os.sep + '_'):
            continue
        yield p


def text_teile(t, f):
    """Wendet f nur auf Text zwischen Tags an (nicht in <script>, <style>, Attributen)."""
    teile = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', t, flags=re.S)
    return ''.join(x if (x.startswith('<')) else f(x) for x in teile)


def attribute(t):
    """Dieselben Wendungen in alt, aria-label, title und content."""
    return re.sub(r'((?:alt|aria-label|title|content)=")([^"]*)(")', lambda m: m.group(1) + umformen(m.group(2)) + m.group(3), t)


def umformen(s):
    for a, n in ERSATZ:
        s = s.replace(a, n)
    return s


def anwenden():
    n = 0
    for p in seiten():
        a = open(p, encoding='utf-8').read()
        if os.path.relpath(p, ROOT) == os.path.join('werkbank', 'impressum.html'):   # Rechtstext von Tasty Studios an alle Besucher: Sie-Form bleibt
            continue
        b = attribute(text_teile(a, umformen))
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    return n


def suchlauf():
    """Was danach noch nach Sie oder Schweizer Schreibung klingt (Text und Attribute), zur Prüfung."""
    import html as _h
    aus = set()
    for p in seiten():
        if os.path.basename(p) == 'impressum.html':
            continue
        t = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', '', open(p, encoding='utf-8').read(), flags=re.S)
        t = re.sub(r'(?:alt|aria-label|title|content)="([^"]*)"', lambda m: '>' + m.group(1) + '<', t)
        for z in _h.unescape(re.sub(r'<[^>]+>', '\n', t)).split('\n'):
            if re.search(r'\b(Sie|Ihnen|Ihre[mnrs]?)\b|(?<!\w)Ihr (?!entscheidet|führt|hört|lest|schaut|zahlt)|grösse|Grösse|\bgross\b|schliess|heisst|\bweiss\b|ausser', z):
                aus.add((os.path.relpath(p, ROOT), z.strip()[:200]))
    return sorted(aus)


if __name__ == '__main__':
    print('Ihr-Form:', anwenden(), 'Seiten')
    for x in suchlauf():
        print(*x, sep=' | ')
