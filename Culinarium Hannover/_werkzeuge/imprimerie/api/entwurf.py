"""Drucksachen-Studio · /api/entwurf: aus einem Satz des Hauses einen Entwurf machen.
Die KI setzt nicht selbst, sie wählt Format, Aufbau (eine der elf Vorlagen), Grund und Fotos und schreibt die Texte.
Gesetzt wird im Browser mit den Vorlagen des Hauses, deshalb bleibt jeder Entwurf in der Marke.
Wissen = Marke (Farben, Schriften, Regeln) + Fotokatalog + Wortlaut der Website und Unterlagen des Hauses.
Schlüssel: ANTHROPIC_API_KEY (+ ANTHROPIC_WORKSPACE_ID für Nutzer-Schlüssel), wie bei der Rezeption im Chat."""
import json, os, time, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler

HIER = os.path.dirname(os.path.abspath(__file__))
# Wissen und Marke des Hauses: neben dieser Datei (eigenes Projekt, lokal) oder online im Haus unter api/_lib/imprimerie/_daten (online.json)
DATEN = next((d for d in (os.path.join(HIER, '_daten'), os.path.join(HIER, '_lib', 'imprimerie', '_daten')) if os.path.isdir(d)), os.path.join(HIER, '_daten'))
MODELL = os.environ.get('DS_MODELL', 'claude-sonnet-5-5')

FORMATE = {
    'a6h': 'A6 hoch, 105 × 148 mm: Karte, kleiner Flyer, Tischaufsteller',
    'a6q': 'A6 quer, 148 × 105 mm: Postkarte, Ansichtskarte',
    'a5h': 'A5 hoch, 148 × 210 mm: Flyer, Menükarte',
    'a5q': 'A5 quer, 210 × 148 mm: Einladung, Flyer quer',
    'a4h': 'A4 hoch, 210 × 297 mm: Aushang, Speisekarte, Infoblatt',
    'a3h': 'A3 hoch, 297 × 420 mm: Plakat',
    'dlh': 'DL hoch, 99 × 210 mm: schmale Menü- oder Getränkekarte, Programm, langer Flyer',
    'dlq': 'DL quer, 210 × 99 mm: Gutschein, Ticket',
    'q148': 'Quadrat, 148 × 148 mm: Grusskarte, Einladung',
    'insta': 'Instagram 4:5, Beitrag fürs Handy (kein Druck); als Karussell bis zehn Bilder',
    'story': 'Story 9:16 für Instagram und WhatsApp (kein Druck)',
    'a7q': 'A7 quer, 105 × 74 mm: Tischkarte, Platzkarte, kleine Hinweiskarte',
    'ig11': 'Instagram 1:1, quadratisch wie die Plakate der Abende (kein Druck); für das Plakat des Abends mit «plakat» und «plakatrueck»',
    'schild': 'Namensschild, 90 × 55 mm: Namensschild zum Anstecken, Ausweis für Tagungen',
}
VORLAGEN = {
    'deckel': ('Titelblatt: Zeichen gross, Titel, kurze Goldlinie, Zeile darunter, optional ein kurzer Satz. Für Deckblätter, Ankündigungen mit starkem Titel, Karten ohne Foto.', ['ueber', 'titel', 'unter', 'text', 'fuss']),
    'buehne': ('Bild oben: grosses Foto über gut die Hälfte, das Zeichen sitzt auf der Naht, darunter Zeile, Titel, Text, Handlungszeile. Für Flyer, Plakate, Aushänge mit Foto.', ['bild', 'ueber', 'titel', 'text', 'aktion', 'fuss']),
    'ansicht': ('Ansichtskarte: Foto randlos, kleines Schild unten links mit Ortsname und Zeile. NUR Haus von aussen oder Landschaft, Titel = Ort wie auf einer echten Postkarte («Linden», «Hannover»).', ['bild', 'titel', 'unter']),
    'karte': ('Karte mit Liste: Zeichen klein, Titel, kursive Einleitung, dann Einträge mit Name, Beschreibung, Preis, dazwischen Haarlinien. Für Speise-, Getränke-, Wein-, Behandlungs- und Preiskarten. Bis etwa 14 Einträge pro Seite, sonst auf mehrere Seiten verteilen.', ['ueber', 'titel', 'text', 'liste', 'fuss']),
    'einladung': ('Einladung: doppelter Goldrahmen, Zeile, grosser Titel, Linie, wann, wo (kursiv), Text, Bitte um Antwort, kleines Zeichen unten.', ['ueber', 'titel', 'wann', 'wo', 'text', 'aktion']),
    'programm': ('Programm: Titel linksbündig, darunter Termine mit Datum, Titel und Ort. Für Veranstaltungen, Wochenprogramm, Tagesablauf einer Tagung oder Hochzeit.', ['ueber', 'titel', 'termine', 'fuss']),
    'fenster': ('Bild im Rahmen: Foto mit feinem Goldrahmen auf der Fläche (Passepartout), darunter Titel, Zeile, Text. Ruhiger und edler als «buehne».', ['bild', 'ueber', 'titel', 'unter', 'text', 'fuss']),
    'geteilt': ('Bild und Text geteilt: quer halb Foto links, halb Text rechts; hoch Text oben, Foto unten randlos. Für Restaurant, Wellness, Angebote, Instagram.', ['bild', 'ueber', 'titel', 'text', 'aktion', 'fuss']),
    'gutschein': ('Gutschein: Zeichen, Titel «Gutschein» (oder anders), Zeile, Wert, kurzer Text, Felder Für / Von / Nr. Am besten im Format dlq.', ['titel', 'unter', 'wert', 'text', 'fuss']),
    'plakat': ('Plakat des Abends in der Sprache der Culinarium-Plakate: Bild oben im warmweissen Rand, darunter die Wortmarke CULINARIUM im Kasten und das Band mit der Zeile. «ueber» = «WALK ON THE WILD SIDE», «zeile» = «A UNiQUE EXPERiENCE BY MOMO X RUDI», «akzent» = Farbe des Abends (#rrggbb). Format ig11, a3h oder story.', ['bild', 'ueber', 'zeile', 'akzent']),
    'plakatrueck': ('Rückseite des Abend-Plakats: Bild randlos, oben links «WALK\nON THE\nWILD SIDE», unten die Daten in der Form «27 / 11 / 26» mit Uhrzeit «19:00 UHR», rechts «3 GÄNGE MENÜ\n5 SiGNATURE DRiNKS», Linie in der Akzentfarbe. Immer zweite Seite nach «plakat».', ['bild', 'ueber', 'tag1', 'zeit1', 'tag2', 'zeit2', 'text', 'akzent']),
    'menue': ('Menükarte am Tisch: Wortmarke, Zeile, Titel «Menü», Datum des Abends, je Gang {gang, name (Teller), detail (Drink)} wie auf den Karten der Abende. Format dlh.', ['titel', 'ueber', 'liste', 'text', 'fuss', 'akzent']),
    'aushang': ('Aushang: Zeichen oben, Titel, Linie, gut lesbarer Text mit Zeilenumbrüchen, Handlungszeile. Für Hinweise, Öffnungszeiten, Hausregeln, Tischaufsteller.', ['ueber', 'titel', 'text', 'aktion', 'fuss']),
    'tuer': ('Türhänger: oben das Loch für die Klinke, darunter Zeichen, grosser Titel, Linie, Zeile in zweiter Sprache (unter), kurzer Text, Handlungszeile. Nur im Format tuer.', ['ueber', 'titel', 'unter', 'text', 'aktion']),
    'kartengruss': ('Postkarten-Rückseite: links Zeichen, Name des Hauses, Zeile und ein kurzer Gruss, rechts Markenfeld und vier Adresszeilen. IMMER die zweite Seite einer «ansicht», nie «rueckseite» für Postkarten.', ['titel', 'text']),
    'rueckseite': ('Rückseite mit Adresse: Zeichen, Wortmarke, Zeile, ein Satz, Adresse, Telefon, Mail, Web. Für die Rückseite von Flyern und Karten.', ['text']),
}
FELDER = {
    'ueber': 'kleine Zeile in gesperrten Versalien über dem Titel, z. B. der Betrieb («Culinarium» oder «Walk on the Wild Side») oder das Datum des Abends oder der Anlass; 1–5 Wörter',
    'titel': 'der Titel, 1–5 Wörter, mit \\n für einen gewollten Umbruch; keine Ausrufezeichen',
    'unter': 'Zeile unter dem Titel in gesperrten Versalien: Datum, Zeitraum, Zusatz; kurz',
    'text': 'ein bis drei kurze Sätze oder Zeilen mit \\n (bei «aushang» der Haupttext)',
    'aktion': 'Handlungszeile: Zeiten, Reservierung, Telefon; kurz',
    'wann': 'Datum und Uhrzeit, z. B. «31. Dezember 2026 · ab 18.00 Uhr»',
    'wo': 'Ort im Haus',
    'wert': 'Betrag des Gutscheins, z. B. «CHF 100»',
    'bild': 'Schlüssel eines Fotos aus dem Fotokatalog (genau so geschrieben)',
    'fuss': 'Fusszeile; weglassen = Adresse und Telefon des Hauses; leerer Text "" = keine Fusszeile',
    'liste': 'Einträge {name, detail, preis} (detail und preis dürfen fehlen)',
    'termine': 'Termine {wann, was, wo}',
}


def _system(haus):
    M = json.load(open(os.path.join(DATEN, haus + '.json'), encoding='utf-8'))
    wissen = open(os.path.join(DATEN, haus + '-wissen.txt'), encoding='utf-8').read()
    bilder = '\n'.join(M.pop('bilder'))
    vorlagen = '\n'.join(f'- {k}: {v[0]} Felder: {", ".join(v[1])}' for k, v in VORLAGEN.items())
    felder = '\n'.join(f'- {k}: {v}' for k, v in FELDER.items())
    formate = '\n'.join(f'- {k}: {v}' for k, v in FORMATE.items())
    return f'''Du bist der Gestalter aller Drucksachen des {M["voll"]} in {M["ort"]}. Mitarbeitende des Hauses sagen dir in einem Satz, was sie brauchen. Du lieferst einen fertigen Entwurf über das Werkzeug «entwurf». Gesetzt wird mit den Vorlagen des Hauses: du wählst Format, Aufbau, Grund und Fotos und schreibst die Texte. Farben, Schriften, Zeichen und Tapete setzt das Studio selbst.

DIE MARKE DES HAUSES
{json.dumps(M, ensure_ascii=False, indent=1)}

GRUND (ton) je Seite
- dunkel: Marine mit der Tapete, Gold für Zeichen und Zeilen. Für Abend, Feste, Bar, Titelblätter, Gutscheine, Einladungen.
- hell: Papier, Marine-Schrift. Für Karten mit viel Text, Preislisten, Programme, Aushänge am Tag.
- creme: Creme mit heller Tapete. Für Wellness, Frühstück, Sommer, Terrasse, leichte Anlässe.
Wechsle bei zweiseitigen Stücken nicht wild: Vorder- und Rückseite meist im selben Grund, eine helle Innenseite zu einer dunklen Hülle ist gut.

FORMATE
{formate}

AUFBAUTEN (vorlage)
{vorlagen}

FELDER
{felder}

SO ARBEITEST DU
1. Ein Stück aus einer Seite, ausser der Auftrag oder das Stück verlangen mehr: Flyer und Karten zum Mitnehmen bekommen meist eine «rueckseite» als zweite Seite; lange Listen gehen auf mehrere «karte»-Seiten. Höchstens vier Seiten, ausser beim Karussell.
2. Wenn kein Format vorgegeben ist, wähle das, was ein gutes Hotel für diesen Zweck drucken würde.
3. Fotos: nur Schlüssel aus dem Fotokatalog, passend zum Thema, in der richtigen Lage (quer für «ansicht» quer und «buehne», hoch oder quer für «fenster»). Lies die Bildbeschreibung genau. Nie dasselbe Foto zweimal im selben Stück.
4. Texte im Ton des Hauses: du-Form, herzlich, knapp, ein bisschen Strasse, nie werblich laut, kein Ausrufezeichen im Titel, keine Floskeln wie «unvergesslich», «einzigartiges Erlebnis», «Vom … zum …». Jeder Satz wertet auf: Sorgfalt, Handarbeit, der einzelne Gast; Zahlen nur als Exklusivität («vierzehn Plätze»), nie als Menge. Deutsche Schreibung (ß), Anführungszeichen „…“, Preise «89,00 EUR», Zeiten «ab 19 Uhr». Rudis Teller so, wie er sie schreibt: Versalien mit Schrägstrich («LAUCH / BLUMENKOHL / CHIPOTLE»). Deutsch, ausser der Auftrag verlangt eine andere Sprache.
5. Fakten nur aus dem WISSEN unten oder aus dem Auftrag: Namen der Betriebe, Zeiten, Preise, Gerichte, Daten genau so übernehmen. Was du nicht sicher weisst (Preis, Datum, Uhrzeit, Menüfolge, Ansprechperson), schreibst du als Platzhalter in eckigen Klammern, z. B. «[Preis]» oder «[Datum]», und nennst es in «hinweise». Erfinde nie eine Zahl.
6. Wenig Text. Ein Titel trägt das Blatt, der Rest begleitet. Lieber eine Zeile weniger.
7. «hinweise»: höchstens vier kurze Sätze an die Mitarbeitenden, was sie noch prüfen oder ausfüllen sollten. Leer lassen, wenn alles belegt ist.
8. Karussell (Instagram, Format insta): verlangt der Auftrag ein Karussell, eine Serie oder mehrere Bilder als einen Beitrag, liefere drei bis zehn Seiten. Alle Seiten im selben Grund und in derselben Bildsprache (gleicher oder eng verwandter Aufbau), jede mit eigenem Foto. Die erste Seite ist der Einstieg mit dem Titel, die folgenden erzählen je einen Teil, die letzte trägt die Handlungszeile. Pro Seite wenig Text.
9. Baut der Auftrag auf einer offenen Drucksache auf, behalte ihren Inhalt und ändere nur, was verlangt ist.

FOTOKATALOG (Schlüssel | Lage | Beschreibung)
{bilder}

WISSEN: Wortlaut der Website und der Unterlagen des Hauses (Stand des Website-Entwurfs)
{wissen}'''


def _werkzeug(varianten=False):
    eintrag = {'type': 'object', 'properties': {'name': {'type': 'string'}, 'detail': {'type': 'string'}, 'preis': {'type': 'string'}}, 'required': ['name']}
    termin = {'type': 'object', 'properties': {'wann': {'type': 'string'}, 'was': {'type': 'string'}, 'wo': {'type': 'string'}}, 'required': ['was']}
    inhalt = {'type': 'object', 'properties': {k: {'type': 'string', 'description': v} for k, v in FELDER.items() if k not in ('liste', 'termine')}}
    inhalt['properties']['liste'] = {'type': 'array', 'items': eintrag, 'description': FELDER['liste']}
    inhalt['properties']['termine'] = {'type': 'array', 'items': termin, 'description': FELDER['termine']}
    seite = {'type': 'object', 'properties': {
        'vorlage': {'type': 'string', 'enum': list(VORLAGEN)}, 'ton': {'type': 'string', 'enum': ['dunkel', 'hell', 'creme']}, 'inhalt': inhalt},
        'required': ['vorlage', 'ton', 'inhalt']}
    if varianten:
        return {
            'name': 'entwuerfe', 'description': 'Fünf verschiedene Gestaltungen derselben Drucksache übergeben.',
            'input_schema': {'type': 'object', 'properties': {
                'name': {'type': 'string', 'description': 'kurzer Name der Drucksache für die Ablage, z. B. «Plakat Neujahrskonzert»'},
                'format': {'type': 'string', 'enum': list(FORMATE)},
                'varianten': {'type': 'array', 'minItems': 5, 'maxItems': 5, 'items': {'type': 'object', 'properties': {
                    'titel': {'type': 'string', 'description': 'zwei bis vier Wörter, was diese Gestaltung ausmacht, z. B. «Foto gross, Marine» oder «Ruhig auf Papier»'},
                    'seiten': {'type': 'array', 'minItems': 1, 'maxItems': 10, 'items': seite}}, 'required': ['titel', 'seiten']}},
                'hinweise': {'type': 'array', 'items': {'type': 'string'}, 'maxItems': 4},
            }, 'required': ['name', 'format', 'varianten', 'hinweise']},
        }
    return {
        'name': 'entwurf', 'description': 'Den fertigen Entwurf der Drucksache übergeben.',
        'input_schema': {'type': 'object', 'properties': {
            'name': {'type': 'string', 'description': 'kurzer Name der Drucksache für die Ablage, z. B. «Plakat des Abends»'},
            'format': {'type': 'string', 'enum': list(FORMATE)},
            'seiten': {'type': 'array', 'minItems': 1, 'maxItems': 10, 'items': {'type': 'object', 'properties': {
                'vorlage': {'type': 'string', 'enum': list(VORLAGEN)}, 'ton': {'type': 'string', 'enum': ['dunkel', 'hell', 'creme']}, 'inhalt': inhalt},
                'required': ['vorlage', 'ton', 'inhalt']}},
            'hinweise': {'type': 'array', 'items': {'type': 'string'}, 'maxItems': 4},
        }, 'required': ['name', 'format', 'seiten', 'hinweise']},
    }


SPRACHEN = {'de': 'Deutsch (Schweizer Schreibung, ss statt ß, Du-Form wie das Haus («du», herzlich, knapp))', 'en': 'Englisch (britisch, höflich)', 'fr': 'Französisch (vous-Form)',
            'zh': 'vereinfachtes Chinesisch', 'ko': 'Koreanisch (höfliche Form)', 'ar': 'modernes Hocharabisch'}


def _bildtext_werkzeug():
    return {'name': 'bildtext', 'description': 'Den Bildtext für den Beitrag übergeben.', 'input_schema': {'type': 'object', 'properties': {
        'text': {'type': 'string', 'description': 'der Bildtext ohne Hashtags: zwei bis fünf kurze Absätze, getrennt durch eine Leerzeile; erste Zeile ein ruhiger Einstieg'},
        'hashtags': {'type': 'array', 'items': {'type': 'string'}, 'minItems': 5, 'maxItems': 12, 'description': 'passende Hashtags mit #, ohne Leerzeichen'},
        'hinweise': {'type': 'array', 'items': {'type': 'string'}, 'maxItems': 3, 'description': 'was die Mitarbeitenden noch prüfen oder ausfüllen sollten; leer, wenn alles belegt ist'}},
        'required': ['text', 'hashtags', 'hinweise']}}


def bildtext(daten, haus):
    """Bildtext unter einem Instagram-Beitrag, einer Story oder einem Karussell: Text + Hashtags in der gewählten Sprache, Fakten nur aus dem Wissen."""
    b = daten.get('bildtext') or {}
    sprache = b.get('sprache') if b.get('sprache') in SPRACHEN else 'de'
    seiten = b.get('seiten') or []
    if not seiten:
        raise ValueError('Beitrag fehlt')
    art = {'story': 'eine Story', 'karussell': f'ein Karussell aus {len(seiten)} Bildern'}.get(b.get('art'), 'einen Instagram-Beitrag')
    nachricht = (f'Schreibe den Bildtext für {art} des Hauses auf Instagram, in {SPRACHEN[sprache]}. '
                 'So steht es auf den Bildern (je Bild die Texte, dazu das Foto als Schlüssel aus dem Fotokatalog):\n'
                 + json.dumps(seiten, ensure_ascii=False)[:8000] +
                 '\n\nRegeln: Ton des Hauses, ruhig, herzlich, präzise, nie werblich laut, kein Ausrufezeichen, keine Emojis, keine Floskeln. '
                 'Der Text erzählt, was auf den Bildern nicht steht, und wiederholt die Bildtexte nicht wörtlich. Beim Karussell darf er zum Weiterwischen einladen. '
                 'Fakten (Namen, Zeiten, Preise, Daten, Saisons, Angebote, Gerichte, Getränke, Ausstattung) nur aus dem WISSEN oder von den Bildern; nenne nichts, was das Haus anbietet, wenn es dort nicht steht, auch keine Beilagen oder Ergänzungen, keine Aussicht, Lage oder Ausstattung, die dort nicht beschrieben ist; was fehlt, als [Platzhalter] in eckigen Klammern in der Sprache des Textes und in «hinweise» nennen. Erfinde nie eine Zahl. '
                 'Am Ende eine Handlungszeile (Reservierung, Telefon oder Website), nur mit belegten Angaben. '
                 'Hashtags: fünf bis zwölf, passend zu Haus, Ort, Region und Thema; in der Sprache des Textes, wo das üblich ist, sonst die gängigen englischen oder deutschen. '
                 f'Die «hinweise» schreibst du auf Deutsch. Heute ist der {time.strftime("%d.%m.%Y")}. Antworte nur über das Werkzeug «bildtext», ohne Text davor.')
    return _frage(haus, nachricht, _bildtext_werkzeug(), 3000), sprache


def _frage(haus, nachricht, werkzeug, max_tokens):
    koerper = {
        'model': MODELL, 'max_tokens': max_tokens,
        'system': [{'type': 'text', 'text': _SYS[haus], 'cache_control': {'type': 'ephemeral'}}],
        'tools': [werkzeug], 'tool_choice': {'type': 'auto'},   # dieses Modell nimmt kein erzwungenes Werkzeug; der Auftrag verlangt es im Text
        'messages': [{'role': 'user', 'content': nachricht}],
    }
    if not os.environ.get('ANTHROPIC_API_KEY'):
        raise RuntimeError('KI-FREIGABE · Die KI ist für dieses Haus noch nicht freigeschaltet. Vorlagen, Bearbeiten und PDF gehen ohne sie.')
    req = urllib.request.Request('https://api.anthropic.com/v1/messages', data=json.dumps(koerper).encode('utf-8'), method='POST',
                                 headers={'content-type': 'application/json', 'x-api-key': os.environ['ANTHROPIC_API_KEY'], 'anthropic-version': '2023-06-01',
                                          'anthropic-workspace-id': os.environ.get('ANTHROPIC_WORKSPACE_ID', '')})
    try:
        with urllib.request.urlopen(req, timeout=110) as r:
            antwort = json.loads(r.read())
    except urllib.error.HTTPError as e:
        text = e.read().decode('utf-8', 'replace')
        if 'credit balance' in text or 'usage limits' in text or 'regain access' in text:
            raise RuntimeError('KI-GUTHABEN · Das Guthaben für die KI ist aufgebraucht.')
        raise RuntimeError(f'KI-Dienst antwortet mit {e.code}')
    for b in antwort.get('content', []):
        if b.get('type') == 'tool_use':
            return b['input'], antwort.get('usage', {})
    raise RuntimeError('Keine Antwort über das Werkzeug')


_SYS = {}


def entwurf(daten):
    haus = str(daten.get('haus') or 'culinarium')
    if not haus.replace('-', '').isalnum() or not os.path.exists(os.path.join(DATEN, haus + '.json')):
        raise ValueError('Unbekanntes Haus')
    if haus not in _SYS:
        _SYS[haus] = _system(haus)
    if daten.get('bildtext'):
        (e, verbrauch), sprache = bildtext(daten, haus)
        return {'bildtext': {'text': e.get('text', ''), 'hashtags': e.get('hashtags', []), 'hinweise': e.get('hinweise', []), 'sprache': sprache}, 'verbrauch': verbrauch}
    auftrag = str(daten.get('auftrag') or '').strip()[:1500]
    if len(auftrag) < 4:
        raise ValueError('Auftrag fehlt')
    nachricht = 'Auftrag: ' + auftrag
    if daten.get('format'):
        nachricht += f'\nFormat ist vorgegeben: {daten["format"]}.'
    if daten.get('basis'):
        nachricht += '\n\nDie offene Drucksache, auf der aufgebaut werden soll:\n' + json.dumps(daten['basis'], ensure_ascii=False)[:12000]
    fuenf = bool(daten.get('varianten'))
    if fuenf:
        nachricht += ('\n\nLiefere FÜNF deutlich verschiedene Gestaltungen desselben Stücks über das Werkzeug «entwuerfe», ohne Text davor. '
                      'Jede Variante mit anderem Aufbau oder anderem Grund (dunkel, hell, creme gemischt), wo es passt mit anderem Foto. '
                      'Die Fakten sind in allen fünf gleich; Titel und Texte dürfen in Länge und Ton leicht variieren. '
                      'Alle fünf im selben Format. Ordne sie so, dass die stärkste Variante zuerst kommt.')
    nachricht += f'\n\nHeute ist der {time.strftime("%d.%m.%Y")}.' + ('' if fuenf else ' Antworte nur über das Werkzeug «entwurf», ohne Text davor.')
    e, verbrauch = _frage(haus, nachricht, _werkzeug(fuenf), 14000 if fuenf else 6000)
    return {('entwuerfe' if fuenf else 'entwurf'): e, 'verbrauch': verbrauch}


_ZUGRIFF = {}
GROESSE = 60000   # Bytes je Anfrage (Auftrag bis 1'500 Zeichen + offene Drucksache bis 12'000 Zeichen)


def erlaubt(ip):
    jetzt = time.time()
    l = [t for t in _ZUGRIFF.get(ip, []) if jetzt - t < 3600]
    if len(l) >= 40:
        return False
    l.append(jetzt); _ZUGRIFF[ip] = l
    return True


def wache(kopf, ip, groesse=GROESSE, zaehlen=True):
    """Vor jedem Aufruf der KI (online und lokal gleich, Prüfung 16.10.2026, Master Werkzeug-Bau 5.2/5.3):
    nur von der eigenen Seite (Origin = Host, Sec-Fetch-Site nicht cross-site) → 403, nur JSON → 415, höchstens GROESSE Bytes → 413,
    höchstens 40 Entwürfe je Stunde und Absender → 429. Gibt (code, meldung) oder None zurück. Rollen gibt es hier keine:
    L’Imprimerie ändert nichts auf der Website, jede Drucksache bleibt im Browser des Hauses."""
    from urllib.parse import urlparse
    host = (kopf.get('x-forwarded-host') or kopf.get('host') or '').split(',')[0].strip().lower()
    herkunft = (kopf.get('origin') or '').strip().lower()
    if herkunft and herkunft != 'null' and urlparse(herkunft).netloc != host:
        return 403, 'HERKUNFT · Anfragen nur von der Seite der Plakatwerkstatt.'
    if (kopf.get('sec-fetch-site') or '').lower() == 'cross-site':
        return 403, 'HERKUNFT · Anfragen nur von der Seite der Plakatwerkstatt.'
    if 'application/json' not in (kopf.get('content-type') or '').lower():
        return 415, 'FORM · Erwartet wird JSON.'
    try:
        n = int(kopf.get('content-length') or 0)
    except ValueError:
        return 400, 'FORM · Länge der Anfrage fehlt.'
    if n > groesse:
        return 413, 'GROESSE · Anfrage zu gross.'
    if zaehlen and not erlaubt(ip):
        return 429, 'GRENZE · Zu viele Entwürfe in kurzer Zeit. Bitte in einer Stunde wieder.'
    return None


class handler(BaseHTTPRequestHandler):
    def _sende(self, code, daten):
        b = json.dumps(daten, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('content-type', 'application/json; charset=utf-8')
        self.send_header('cache-control', 'no-store')
        self.send_header('content-length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        self._sende(200, {'ok': True, 'modell': MODELL})

    def do_POST(self):
        ip = (self.headers.get('x-forwarded-for') or self.client_address[0]).split(',')[0].strip()
        nein = wache({k.lower(): v for k, v in self.headers.items()}, ip)
        if nein:
            return self._sende(nein[0], {'fehler': nein[1]})
        try:
            n = int(self.headers.get('content-length') or 0)
            daten = json.loads(self.rfile.read(n) or b'{}')
            self._sende(200, entwurf(daten))
        except ValueError as e:
            self._sende(400, {'fehler': str(e)})
        except Exception as e:
            self._sende(502, {'fehler': str(e)})

    def log_message(self, *a):
        pass
