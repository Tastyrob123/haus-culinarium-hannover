"""La Réception (Team hinter dem Gäste-Chat) · Culinarium Hannover (28.10.2026, Kopie aus der Taverne zum Schäfli, dort aus dem Schlössli und Ruedihus).
Culinarium sind Food-Pairing-Abende an der langen Tafel in der Bar Walk on the Wild Side, Hannover-Linden: drei Gänge, fünf Signature Drinks, vierzehn Plätze,
an einzelnen Wochenenden (Freitag ab 19 Uhr, Samstag ab 17 Uhr). Kein Restaurant mit Tageskarte, keine Zimmer.

Zwei Dinge kommen herein:
  Eingang      Die Warteliste der Website («Dein Platz an der Tafel.» auf Der Abend: Tag, Plätze, Name, E-Mail) und Anfragen aus dem Chat, sobald ein Gast
               Name und Kontakt nennt (Platz an einem Abend, eigene Feier an der langen Tafel, Nachricht). Das Team bekommt dazu einen Antwortentwurf
               im Ton der Website (Du, herzlich, knapp), auf Grundlage dessen, was das Haus selbst schreibt (vorlagen/), ändert ihn und schickt ihn selbst.
               Hier wird nichts verschickt. Zu jeder Anfrage stehen Hinweise dabei: kein Culinarium-Tag, mehr als vierzehn Plätze, Bar geschlossen,
               Allergien (die Website sagt dazu nichts: Küche fragen), Ticket zurückgeben.
  Gefragt      Jede Frage mit Antwort. Wo der Chat keine Antwort hatte (Werkzeug «nicht_belegt»), trägt das Team sie einmal nach;
               ab dann antwortet der Chat damit (Block «NACHGETRAGEN VOM TEAM» in der Anweisung).

Speicher: Dateien unter daten/ (oder RECEPTION_DATEN), im selben Aufbau wie der Online-Speicher beim Carlton (Vercel Blob, _gast/fragen.js):
  fragen/JJJJ-MM-TT/<zeit>-<zufall>.json · anfragen/JJJJ-MM-TT/<zeit>-<zufall>.json · nachgetragen.json · status.json
Einträge älter als zwölf Monate werden gelöscht (Datenschutzerklärung; der Satz dazu fehlt auf der Website noch, siehe LIEFERUNG.md).

Eingebunden von server.py: reception.einbinden(gast_modul) hängt sich an gast/gast.py, ohne die Datei zu ändern."""
import datetime, glob, hashlib, html, json, os, random, re, shutil, threading, time
try:   # «Das weiss der Chat» (16.10.2026, nur lokal): Berichtigungen und Ergänzungen des Teams am Wissen. Online fehlt die Datei: dann wie bisher.
    import gedaechtnis
except ImportError:
    gedaechtnis = None

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website')   # die Website des Culinarium (nur gelesen)
DATEN = os.environ.get('RECEPTION_DATEN') or os.environ.get('REZEPTION_DATEN') or os.path.join(HIER, 'daten')
def _name(teil='gaeste', standard='Das Gästebuch'):
    """Name eines Werkzeugs aus der einen Stelle (_werkzeuge/oberflaeche/kleid/culinarium.js › namen), nie fest im Code (Robert wählt, culinarium-maison trägt ein)."""
    try:
        s = open(os.path.join(os.path.dirname(HIER), 'oberflaeche', 'kleid', 'culinarium.js'), encoding='utf-8').read()
        m = re.search(r"namen:\s*\{([^}]*)\}", s)
        n = re.search(teil + r":\s*'([^']+)'", m.group(1)) if m else None
        return n.group(1) if n else standard
    except OSError:
        return standard


NAME = _name()
NAME_IM = ('im ' + NAME[4:]) if NAME.startswith('Das ') else ('in der ' + NAME[4:]) if NAME.startswith('Die ') else ('im ' + NAME[4:]) if NAME.startswith('Der ') else ('in ' + NAME)   # «im Gästebuch»

SCHLOSS = threading.Lock()
LOKAL = threading.local()
ARTEN = {'warteliste': 'Warteliste', 'abend': 'Platz am Abend', 'feier': 'Eigene Feier', 'nachricht': 'Nachricht', 'gutschein': 'Gutschein'}   # gutschein: «Einen Abend verschenken» auf der Website (29.10.2026)   # Abende an der Tafel, keine Zimmer, keine Tageskarte (28.10.2026)
# Culinarium hat keine eigene Mail-Adresse und kein Telefon (fakten.json, 25.10.2026): Tickets laufen über eine Nachricht an @culinarium_hannover, die Bar
# hat +49 163 3909578. Die Briefe hier sind Entwürfe; das Team schickt sie auf seinem eigenen Weg. Grundlage ist, was das Haus selbst schreibt:
# vorlagen/warteliste.txt (Warteliste auf Der Abend), vorlagen/abend.txt («Gut zu wissen» und der Vorverkauf laut Instagram), vorlagen/feier.txt (die lange Tafel für eure eigene Feier).
MAIL = ''
TEL = '+49 163 3909578'
KONTAKT = 'Telefon der Bar +49 163 3909578 · Instagram @culinarium_hannover'
VORLAGE = {'warteliste': ('warteliste', KONTAKT), 'abend': ('abend', KONTAKT), 'feier': ('feier', KONTAKT), 'nachricht': ('', KONTAKT)}
VORLAGEN_DATEIEN = ('warteliste.txt', 'abend.txt', 'feier.txt')
# Die «Abteilung» ist im Culinarium die Art der Arbeit (wer sich darum kümmert), nicht eine Mail-Adresse.
ABTEILUNG_VON = {}
ART_ABTEILUNG = {'warteliste': 'Warteliste', 'abend': 'Abende', 'feier': 'Feiern', 'nachricht': 'Nachrichten', 'gutschein': 'Gutscheine'}
FORMULARE = ('warteliste', 'vormerken', 'allgemein')
# Allergien: die Website hat kein Feld dafür; ein Baustein-Feld, falls die Warteliste eins bekommt, nimmt diese Namen.
ALLERGENE = {k: k for k in ('Gluten', 'Laktose', 'Nüsse', 'Krustentiere', 'Fisch', 'Ei', 'Sellerie', 'Senf')}
# Wann Culinarium stattfindet (abend.html, index.html «Gut zu wissen»): an einzelnen Wochenenden, Freitag ab 19 Uhr, Samstag ab 17 Uhr; vierzehn Plätze an einer Tafel.
# Die Bar (bar.html): Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr, Sonntag bis Mittwoch geschlossen. Die Warteliste nimmt 1 bis 6 Plätze (culinarium.js).
ABEND_TAGE = {4: 'Freitag ab 19 Uhr', 5: 'Samstag ab 17 Uhr'}   # Montag = 0
BAR_ZU = (6, 0, 1, 2)   # Sonntag bis Mittwoch
TAG_NAME = {0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch', 3: 'Donnerstag', 4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'}
TAFEL = 14
SPRACHEN = ('de', 'en', 'fr')
# Themen für «Das wurde gefragt»: Wortlisten in den Sprachen der Gäste, erste passende gewinnt
THEMEN = [('Allergien & Unverträglichkeiten', r'allerg|gluten|laktose|lactose|zöliak|unverträg|nuss|nüss|erdnuss|sellerie|senf|krusten|vegan|vegetar|intoler|nut\b|nuts|dairy|celiac'),
          ('Termine & Warteliste', r'termin|nächste[nr]? abend|wann|warteliste|vormerk|datum|wochenende|freitag|samstag|uhr\b|beginn|next|when|date|waiting'),
          ('Tickets & Preise', r'ticket|preis|kost|euro|eur\b|€|paypal|vorverkauf|zurückgeb|rückerstat|storn|ausgebucht|price|cost|refund'),
          ('Eigene Feier & Gruppen', r'feier|geburtstag|hochzeit|firmen|gruppe|privat|tafel mieten|jga|party\b|birthday|wedding|group|private'),
          ('Drinks & Menü', r'drink|cocktail|alkohol|alkoholfrei|menü|menu|gang|gänge|essen|teller|fatwash|milkwash|enzym|tasting|schulung|food'),
          ('Dirty Chicken', r'dirty|chicken|huhn|hähnchen|sandwich|pop-?up|pommes|krautsalat'),
          ('Die Bar', r'bar\b|wild side|theke|öffnung|geöffnet|offen|konzert|dj\b|session|reservier'),
          ('Anfahrt', r'anfahrt|anreise|weg\b|adresse|wo ist|bahn|tram|üstra|bus\b|auto|park|fahrrad|linden|haasemann|where|address'),
          ('Team', r'rudi|momo|derya|koch|köchin|team|wer kocht|who')]
ABDECKEN = [(re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'), '[E-Mail]'), (re.compile(r'(?:\+|00)?\d[\d\s/().-]{7,}\d'), '[Nummer]')]


# ---------------------------------------------------------------- Dateien
def _pfad(*t):
    return os.path.join(DATEN, *t)

def _lies(p, standard):
    try:
        return json.load(open(p, encoding='utf-8'))
    except OSError:
        return standard
    except ValueError:              # beschädigt: die letzte gute Fassung nehmen
        try:
            return json.load(open(p + '.gut', encoding='utf-8'))
        except (OSError, ValueError):
            return standard

def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.neu'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    try:
        json.load(open(p, encoding='utf-8')); shutil.copy2(p, p + '.gut')   # nur eine lesbare Fassung wird zur Sicherung
    except (OSError, ValueError):
        pass
    os.replace(tmp, p)

def _neue_id(art):
    jetzt = datetime.datetime.now().astimezone()
    zeit = jetzt.isoformat(timespec='seconds')
    return zeit, f'{art}/{zeit[:10]}/{zeit.replace(":", "-").replace("+", "_")}-{random.randrange(36**6):06x}.json'

def _gueltig(id_, art):
    return bool(re.fullmatch(art + r'/\d{4}-\d{2}-\d{2}/[\w.-]+\.json', id_ or '')) and os.path.exists(_pfad(id_))

def _alle(art):
    l = []
    for f in sorted(glob.glob(_pfad(art, '*', '*.json')), reverse=True):
        d = _lies(f, None)
        if d:
            d['id'] = os.path.relpath(f, DATEN)
            l.append(d)
    return l

def aufraeumen():
    """Einträge älter als zwölf Monate löschen (ganze Tagesordner)."""
    grenze = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
    n = 0
    for art in ('fragen', 'anfragen'):
        for o in glob.glob(_pfad(art, '*')):
            if os.path.basename(o) < grenze:
                shutil.rmtree(o, ignore_errors=True); n += 1
    return n


# ---------------------------------------------------------------- Ablegen (aus dem Chat)
def thema_von(text):
    t = (text or '').lower()
    for name, muster in THEMEN:
        if re.search(muster, t):
            return name
    return 'Weitere Fragen'

def lege_frage(daten):
    for muster, ersatz in ABDECKEN:
        daten['frage'] = muster.sub(ersatz, daten.get('frage', ''))
    zeit, id_ = _neue_id('fragen')
    e = {'zeit': zeit, 'frage': str(daten.get('frage', ''))[:600], 'antwort': str(daten.get('antwort', ''))[:2000], 'belegt': daten.get('belegt') is not False,
         'thema': str(daten.get('thema', ''))[:80], 'gruppe': thema_von(daten.get('frage', '')), 'sprache': str(daten.get('sprache', 'de'))[:2],
         'buchung': bool(daten.get('buchung')), 'mappe': bool(daten.get('mappe')), 'anfrage': daten.get('anfrage') or ''}
    if daten.get('beispiel'):
        e['beispiel'] = True; e['probe'] = True
    with SCHLOSS:
        _schreib(_pfad(id_), e)
    if random.random() < 0.05:
        aufraeumen()
    return id_

def lege_anfrage(eingabe, gespraech, sprache, verlauf):
    """Legt eine Anfrage ab. Kommt im selben Gespräch dieselbe Art noch einmal (Gast ergänzt Datum oder Personen), wird sie ergänzt, nicht verdoppelt."""
    art = eingabe.get('art') if eingabe.get('art') in ARTEN else 'nachricht'
    with SCHLOSS:
        for a in _alle('anfragen')[:80]:
            if a.get('gespraech') == gespraech and a.get('art') == art and a.get('status') != 'erledigt':
                for k in ('name', 'kontakt', 'datum', 'personen', 'anliegen'):
                    if eingabe.get(k) not in (None, ''):
                        a[k] = eingabe[k]
                a['verlauf'] = verlauf; a['entwurf'] = None; a['geaendert'] = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
                id_ = a.pop('id'); _schreib(_pfad(id_), a)
                return id_
        zeit, id_ = _neue_id('anfragen')
        _schreib(_pfad(id_), {'zeit': zeit, 'art': art, 'name': str(eingabe.get('name') or '')[:120], 'kontakt': str(eingabe.get('kontakt') or '')[:160],
                              'datum': str(eingabe.get('datum') or '')[:120], 'personen': eingabe.get('personen'), 'anliegen': str(eingabe.get('anliegen') or '')[:1200],
                              'sprache': sprache, 'gespraech': gespraech, 'verlauf': verlauf, 'status': 'neu', 'entwurf': None})
        return id_


# ---------------------------------------------------------------- Beispiele im Eingang
BEISPIEL_STAND = 3   # Culinarium: eigene Beispiele des Hauses ab Stand 3 (28.10.2026)   # 3: deutsche Lesefassungen der fremdsprachigen Briefe (16.10.2026) · 1: fünf Anfragen und neun Fragen (13./14.10.2026) · 2: zwölf Anfragen, 24 Fragen, drei Antworten des Teams, Entwürfe neu geschrieben (15.10.2026)


def _jetzt():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo('Europe/Berlin'))
    except Exception:
        return datetime.datetime.now().astimezone()


def _zeit_vor(jetzt, vor):
    tage, h, m = vor
    z = (jetzt - datetime.timedelta(days=tage)).replace(hour=h, minute=m, second=0, microsecond=0)
    if z > jetzt:
        z -= datetime.timedelta(days=1)
    return z.isoformat(timespec='seconds')


def _stand(marke):
    """Welcher Beispiel-Stand liegt in diesem Datenordner: 0 = noch keiner, 1 = alte Marke ohne Stand."""
    if not os.path.exists(marke):
        return 0
    return int(_lies(marke, {}).get('stand') or 1)


def _quelle(e):
    """Kennung des Textstands, aus dem eine Lesefassung stammt: ändert das Team den Brief, ist die Übersetzung veraltet."""
    return hashlib.sha1(((e.get('betreff') or '') + '\n' + (e.get('text') or '')).encode('utf-8')).hexdigest()[:12]


UEBERSETZEN = """Du übersetzt für das Team von Culinarium (Food-Pairing-Abende in einer Bar) einen Antwortbrief an einen Gast und das Gespräch, das der Gast im Chat geführt hat, ins Deutsche.
Die Übersetzung ist nur zum Mitlesen für das Team und wird nie verschickt. Übersetze genau und vollständig, nichts weglassen, nichts hinzufügen,
Schreibung wie die Website (ss statt ß, Namen wie Haasemannstraße bleiben). Stellen in eckigen Klammern bleiben in eckigen Klammern, übersetzt. Namen, Adressen, Zahlen und Preise bleiben, wie sie sind.
Antworte ausschliesslich mit JSON: {"betreff": "…", "text": "…", "verlauf": ["…", …]} – «verlauf» hat genau so viele Einträge wie im Eingang, in derselben Reihenfolge."""

def uebersetzen(id_):
    """Deutsche Lesefassung eines fremdsprachigen Briefs und seines Chat-Gesprächs (Robert 16.10.2026: «der Mitarbeiter … muss das auch nochmal kurz
    übersetzen können … sehen, wie das übersetzt aussieht, bevor er es abschickt»). Wird gespeichert und gilt, bis der Brief geändert wird."""
    if not _gueltig(id_, 'anfragen'):
        raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
    a = _lies(_pfad(id_), {})
    e = a.get('entwurf') or {}
    if not e.get('text'):
        raise ValueError('ÜBERSETZEN · Es gibt noch keinen Brief.')
    q = _quelle(e)
    if (e.get('deutsch') or {}).get('quelle') == q and a.get('verlauf_de'):
        return {'deutsch': e['deutsch'], 'verlauf_de': a['verlauf_de']}
    if _G is None:
        raise ValueError('CHAT · Der Assistent ist noch nicht geladen.')
    verlauf = [v.get('text', '') for v in a.get('verlauf') or []]
    eingabe = json.dumps({'betreff': e.get('betreff', ''), 'text': e['text'], 'verlauf': verlauf}, ensure_ascii=False)
    antwort = _G._api({'model': _G.MODELL, 'max_tokens': 6000, 'system': UEBERSETZEN, 'messages': [{'role': 'user', 'content': eingabe}]})
    roh = ''.join(b.get('text', '') for b in antwort.get('content', []) if b.get('type') == 'text').strip()
    roh = re.sub(r'^```(?:json)?\s*|\s*```$', '', roh)
    try:
        d = json.loads(roh[roh.index('{'):roh.rindex('}') + 1])
    except (ValueError, json.JSONDecodeError):
        raise ValueError('ÜBERSETZEN · Die Übersetzung kam unvollständig zurück. Bitte noch einmal versuchen.')
    with SCHLOSS:
        a = _lies(_pfad(id_), {})
        a['entwurf']['deutsch'] = {'betreff': str(d.get('betreff') or ''), 'text': str(d.get('text') or ''), 'quelle': q}
        vd = d.get('verlauf') if isinstance(d.get('verlauf'), list) else []
        a['verlauf_de'] = [str(x) for x in vd][:len(verlauf)] if len(vd) == len(verlauf) else a.get('verlauf_de') or []
        _schreib(_pfad(id_), a)
    return {'deutsch': a['entwurf']['deutsch'], 'verlauf_de': a['verlauf_de']}


def beispiele():
    """Beispiel-Anfragen mit fertigem Entwurf (gast_beispiele.json), damit das Haus sieht, wie der Eingang arbeitet (Robert 13.10.2026, erweitert 15.10.2026).
    Je Datenordner merkt sich beispiele.json den Stand. Ein neuer Stand legt nur die neu hinzugekommenen Beispiele an und schreibt die Entwürfe der
    noch vorhandenen neu; gelöschte Beispiele kommen nicht wieder. Liegt beim ersten Mal schon eine echte Anfrage da, bleibt der Eingang wie er ist.
    Namen und Adressen sind erfunden (example.com), in der Oberfläche steht «Beispiel» dabei."""
    marke = _pfad('beispiele.json')
    if _stand(marke) >= BEISPIEL_STAND:
        return 0
    with SCHLOSS:
        stand = _stand(marke)
        if stand >= BEISPIEL_STAND:
            return 0
        alt = _lies(marke, {}).get('anzahl', 0) if stand else 0
        da = {a.get('gespraech'): a for a in _alle('anfragen') if a.get('beispiel')}
        if not stand and any(not a.get('beispiel') for a in _alle('anfragen')):
            _schreib(marke, {'angelegt': '', 'anzahl': 0, 'stand': BEISPIEL_STAND})
            return 0
        liste = _lies(os.path.join(HIER, 'gast_beispiele.json'), [])
        jetzt = _jetzt(); n_neu = 0
        for n, b in enumerate(liste, 1):
            nr, absender = VORLAGE.get(b['art'], VORLAGE['nachricht'])
            absender = b.get('an') or absender
            g = f'beispiel-{n}'
            if g in da and stand >= 2:   # schon auf Stand 2: nur die deutsche Lesefassung dazu, Text, Gestaltung und Status bleiben
                a = da[g]; id_ = a.pop('id')
                if b.get('deutsch') and a.get('entwurf'):
                    a['entwurf']['deutsch'] = dict(b['deutsch'], quelle=_quelle(a['entwurf']))
                if b.get('verlauf_de'):
                    a['verlauf_de'] = b['verlauf_de']
                _schreib(_pfad(id_), a)
                continue
            if g in da:   # noch vorhanden: Entwurf und Angaben auf den neuen Stand, Status des Teams bleibt
                a = da[g]; id_ = a.pop('id')
                a.update({'name': b['name'], 'kontakt': b['kontakt'], 'datum': b['datum'], 'personen': b['personen'], 'anliegen': b['anliegen'],
                          'verlauf': [{'rolle': r, 'text': t} for r, t in b['verlauf']]})
                a['entwurf'] = {'betreff': b['betreff'], 'text': b['text'], 'team': b['team'], 'vorlage': nr, 'absender': absender, 'zeit': a.get('zeit')}
                if b.get('deutsch'):
                    a['entwurf']['deutsch'] = dict(b['deutsch'], quelle=_quelle(a['entwurf']))
                if b.get('verlauf_de'):
                    a['verlauf_de'] = b['verlauf_de']
                _schreib(_pfad(id_), a)
                continue
            if n <= alt:  # gab es schon und wurde gelöscht
                continue
            zeit = _zeit_vor(jetzt, b['vor'])
            _schreib(_pfad('anfragen', zeit[:10], f"{zeit[11:19].replace(':', '-')}_{g}.json"),
                     {'zeit': zeit, 'art': b['art'], 'name': b['name'], 'kontakt': b['kontakt'], 'datum': b['datum'], 'personen': b['personen'], 'anliegen': b['anliegen'],
                      'sprache': b['sprache'], 'gespraech': g, 'verlauf': [{'rolle': r, 'text': t} for r, t in b['verlauf']], 'status': b['status'], 'beispiel': True, **{k: b[k] for k in ('an', 'abteilung', 'seite', 'seite_name', 'web', 'nachricht', 'formular', 'allergene', 'uhrzeit', 'platz') if b.get(k)},
                      'entwurf': (dict({'betreff': b['betreff'], 'text': b['text'], 'team': b['team'], 'vorlage': nr, 'absender': absender, 'zeit': zeit},
                                       **({'deutsch': dict(b['deutsch'], quelle=_quelle(b))} if b.get('deutsch') else {})) if b.get('text') else None),   # Anfragen ohne Brief: den schreibt der Assistent auf Knopfdruck (Probe ohne KI: probe_ki.py)
                      **({'verlauf_de': b['verlauf_de']} if b.get('verlauf_de') else {})})
            n_neu += 1
        _schreib(marke, {'angelegt': jetzt.isoformat(timespec='seconds'), 'anzahl': len(liste), 'stand': BEISPIEL_STAND})
        return n_neu


def beispiel_fragen():
    """Beispiel-Fragen für «Das wurde gefragt» (gast_beispiel_fragen.json, Robert 14.10.2026: «Beispielfragen einsetzen in der Rezeption», erweitert 15.10.2026)
    und Beispiel-Antworten des Teams (gast_beispiel_nachgetragen.json). Stand wie bei beispiele(): ein neuer Stand legt nur Neues an.
    Die Antworten der Fragen stehen so im Wissen des Chats (Website und Unterlagen des Hauses); einige Fragen haben mit Absicht keine Antwort
    (Lücken zum Nachtragen). Die nachgetragenen Beispiele gehen nicht ins Wissen des Chats. In der Oberfläche steht «Beispiel» dabei."""
    marke = _pfad('beispiele_fragen.json')
    if _stand(marke) >= BEISPIEL_STAND:
        return 0
    with SCHLOSS:
        stand = _stand(marke)
        if stand >= BEISPIEL_STAND:
            return 0
        alt = _lies(marke, {}).get('anzahl', 0) if stand else 0
        jetzt = _jetzt()
        if not stand and glob.glob(_pfad('fragen', '*', '*.json')):
            _schreib(marke, {'angelegt': '', 'anzahl': 0, 'stand': BEISPIEL_STAND})
            return 0
        if stand and not alt:   # damals lag schon eine echte Frage da: auch jetzt keine Beispiele dazwischen
            _schreib(marke, {'angelegt': '', 'anzahl': 0, 'stand': BEISPIEL_STAND})
            return 0
        liste = _lies(os.path.join(HIER, 'gast_beispiel_fragen.json'), [])
        n_neu = 0
        for n, b in enumerate(liste, 1):
            if n <= alt:
                continue
            zeit = _zeit_vor(jetzt, b['vor'])
            _schreib(_pfad('fragen', zeit[:10], f"{zeit[11:19].replace(':', '-')}_beispiel-{n}.json"),
                     {'zeit': zeit, 'frage': b['frage'], 'antwort': b['antwort'], 'belegt': bool(b.get('belegt', True)), 'thema': b.get('thema', ''),
                      'gruppe': thema_von(b['frage']), 'sprache': b['sprache'], 'buchung': bool(b.get('buchung')), 'mappe': False, 'anfrage': '', 'beispiel': True})
            n_neu += 1
        ng = nachgetragen()
        if not any(str(x.get('nid', '')).startswith('beispiel-') for x in ng):
            for n, b in enumerate(_lies(os.path.join(HIER, 'gast_beispiel_nachgetragen.json'), []), 1):
                ng.append({'nid': f'beispiel-{n}', 'frage': b['frage'], 'antwort': b['antwort'], 'zeit': _zeit_vor(jetzt, b['vor']), 'quelle': '', 'beispiel': True})
            _schreib(_pfad('nachgetragen.json'), ng)
        _schreib(marke, {'angelegt': jetzt.isoformat(timespec='seconds'), 'anzahl': len(liste), 'stand': BEISPIEL_STAND})
        return n_neu


# ---------------------------------------------------------------- Nachgetragen vom Team
def nachgetragen():
    return _lies(_pfad('nachgetragen.json'), [])

def wissen_block():
    l = [x for x in nachgetragen() if (x.get('antwort') or '').strip() and not x.get('beispiel')]   # Beispiele sind erfunden, der Chat sagt sie nicht
    if not l:
        return ''
    return ('\n\nNACHGETRAGEN VOM TEAM (gilt wie WISSEN; das Team des Hauses hat diese Antworten selbst geschrieben, nachdem Gäste danach gefragt hatten):\n'
            + '\n'.join(f'Frage: {x["frage"]}\nAntwort des Hauses: {x["antwort"]}' for x in l))


# ---------------------------------------------------------------- Anbindung an _gast/gast.py
ZUSATZ = """

Anfragen an das Team (Werkzeug anfrage):
- Möchte ein Gast auf die Warteliste für den nächsten Abend, einen Platz an einem Abend, die lange Tafel für eine eigene Feier oder dem Team etwas schreiben, bietest du an, es an das Team weiterzugeben. Dafür brauchst du den Namen und eine E-Mail-Adresse oder Telefonnummer; frag in einem Satz danach.
- Sobald Name und Kontakt genannt sind, rufst du das Werkzeug anfrage auf, mit allem, was der Gast gesagt hat (Tag, Plätze, Wünsche). Ohne Kontakt rufst du es nicht auf.
- Deine Antwort dazu: ein Satz, dass dies ein Entwurf von Tasty Studios ist und die Anfrage deshalb nicht an das Team geht; für eine echte Anfrage hilft die Bar am Telefon oder eine Nachricht an @culinarium_hannover auf Instagram. Sag nie, dass ein Platz reserviert, bestätigt oder weitergegeben ist.
- Für die Warteliste allein ist das Formular auf der Seite «Der Abend» der schnellste Weg; die Anfrage ist ein Angebot zusätzlich, wenn der Gast Fragen oder Wünsche hat. Der nächste Termin steht noch nicht fest: nenne nie ein Datum, das nicht in WISSEN steht.
- Allergien und Unverträglichkeiten: Die Website sagt dazu nichts. Nimm sie immer in die Anfrage auf und sag, dass die Küche es mit dem Gast klärt. Ob ein Gang frei davon ist, sagst du nie."""

WERKZEUG = {
    'name': 'anfrage',
    'description': 'Gibt eine Anfrage des Gastes an das Team von Culinarium weiter (Warteliste für den nächsten Abend, Platz an einem Abend, eigene Feier an der langen Tafel, Nachricht). Nur aufrufen, wenn Name und E-Mail oder Telefon genannt sind.',
    'strict': True,
    'input_schema': {'type': 'object', 'additionalProperties': False, 'required': ['art', 'name', 'kontakt', 'datum', 'personen', 'anliegen'],
                     'properties': {'art': {'type': 'string', 'enum': list(ARTEN)},
                                    'name': {'type': 'string', 'description': 'Name, wie der Gast ihn nennt'},
                                    'kontakt': {'type': 'string', 'description': 'E-Mail-Adresse oder Telefonnummer, wörtlich'},
                                    'datum': {'type': ['string', 'null'], 'description': 'Tag oder Datum, wie der Gast ihn nennt (Freitag, Samstag, egal, ein Datum), oder null'},
                                    'personen': {'type': ['integer', 'null'], 'description': 'Anzahl Plätze oder null'},
                                    'anliegen': {'type': 'string', 'description': 'Worum es geht, in ein bis drei Sätzen auf Deutsch, mit allen Wünschen des Gastes; Allergien und Unverträglichkeiten immer ausdrücklich'}}}}

DANKE = {'de': f'Danke. Dies ist ein Entwurf von Tasty Studios: Die Anfrage geht nicht an das Team, sie liegt nur zur Ansicht {NAME_IM}.',
         'en': 'Thank you. This is a draft by Tasty Studios: your request does not go to the team, it is only kept for viewing in the host tool.',
         'fr': 'Merci. Ceci est une ébauche de Tasty Studios : votre demande n’est pas transmise à l’équipe, elle est seulement conservée pour être consultée.'}

ANFRAGE_GBR = """Du schreibst im Namen des Teams von Culinarium den Entwurf einer Antwort an einen Gast. Culinarium sind Food-Pairing-Abende an der langen Tafel in der Bar Walk on the Wild Side, Haasemannstraße 13, Hannover-Linden: ein Aperitif, drei Gänge aus der Küche von Rudi Napieraj, fünf Signature Drinks von Momo mit Tasting und einer kleinen Schulung am Tisch, vierzehn Plätze, an einzelnen Wochenenden (Freitag ab 19 Uhr, Samstag ab 17 Uhr). Der Gast hat über die Warteliste der Website oder im Chat geschrieben (Warteliste, Platz an einem Abend, eigene Feier an der langen Tafel, Nachricht).

Regeln:
- Grundlage ist, wo vorhanden, die VORLAGE: was das Haus selbst schreibt (Warteliste: die Sätze auf «Der Abend» und die Bestätigung des Formulars; Platz an einem Abend: «Gut zu wissen» und der Vorverkauf; eigene Feier: die Sätze der Bar-Seite). Übernimm daraus den Inhalt und die Haltung, nicht Satz für Satz. Was für die Antwort fehlt (Tag, Plätze, bei einer Feier Anlass und Datum), erfragst du freundlich am Ende, in einer kurzen Liste. Gibt es keine Vorlage, gilt nur der Ton.
- Alles, was du an Preisen, Zeiten, Plätzen, Drinks und Gängen nennst, steht wörtlich in WISSEN (Wortlaut der Website). Erfinde nichts. Der nächste Termin steht noch nicht fest: nenne kein Datum, setz dafür [Termin eintragen]. Der letzte Preis war 89,00 EUR; für einen neuen Abend setzt du [Preis bestätigen].
- Freie Plätze kannst du nicht prüfen: setz dafür [Plätze prüfen]. Mehr als vierzehn Plätze hat die Tafel nicht. Eine eigene Feier an der langen Tafel bestätigt die Bar: [Feier mit der Bar klären]. Tickets gibt es nur im Vorverkauf und sie werden nicht rückerstattet; sag das freundlich, wenn der Gast danach fragt. Was das Team entscheiden muss, steht in eckigen Klammern, kurz und in normaler Schreibung. Das Werkzeug zeigt diese Stellen als offene Felder im Brief.
- Allergien und Unverträglichkeiten: Nenne jede, die der Gast angibt, ausdrücklich und schreib, dass Rudi in der Küche es mit dem Gast abstimmt [Küche fragen]. Sag nie von dir aus, ein Gang sei frei davon. «Vegetarisch» ist kein Merkmal der Abende; wünscht der Gast es, gehört es zu [Küche fragen].
- Ton der Website: Du, herzlich, knapp, ein bisschen Linden. Jeder Satz macht den Abend wertvoller: der einzelne Gast, der Platz an der Tafel, das Glas, das Momo erklärt, der Teller, den Rudi von Hand anrichtet. Nie Masse, nie Abfertigung, keine Stückzahlen als Pointe; vierzehn Plätze nur als «wenige Plätze». Keine Werbesprache (nicht «kulinarisches Highlight», «Genuss pur», «unvergesslich»), keine Emojis, kein Fettdruck. Kurze Absätze. Schreibung wie die Website (ss statt ß, Namen wie Haasemannstraße bleiben).
- Anrede «Hallo [Vorname],» bzw. in der Sprache des Gastes, Gruss «Bis bald an der Tafel» oder «Bis bald in Linden».
- Sprache: die Sprache des Gastes (steht bei der Anfrage).
- Form: Zeile 1 «Betreff: …» (persönlich, mit Anlass oder Tag), dann Leerzeile, dann die Antwort mit Anrede und Gruss, darunter zwei Zeilen: «[Name]» und «Culinarium im Walk on the Wild Side». Adresse und Telefon der Bar stehen schon im Briefkopf, nicht wiederholen.
- Nach der Antwort eine Zeile «---» und darunter für das Team, nicht für den Gast: «Grundlage:» mit den Seiten, aus denen die Angaben stammen, und «Offen:» mit dem, was das Team vor dem Senden klären muss.

WISSEN:
"""

_G = None

def einbinden(g):
    """Hängt La Réception an das geladene Modul _gast/gast.py: Werkzeug «anfrage», Wissen des Teams, Ablage statt Online-Speicher."""
    global _G
    _G = g
    os.makedirs(DATEN, exist_ok=True)
    g.WERKZEUGE = [w for w in g.WERKZEUGE if w.get('name') != 'anfrage'] + [WERKZEUG]
    if gedaechtnis:
        gedaechtnis._G = g
    basis = g.ANWEISUNG
    g.ANFRAGE = ANFRAGE_GBR + g.WISSEN
    roh_api, roh_frage, roh_ip = g._api, g.frage, g.handler._ip

    def api(koerper):
        a = roh_api(koerper)
        for b in a.get('content', []):
            if b.get('type') == 'tool_use' and b.get('name') == 'anfrage':
                LOKAL.anfrage = b.get('input') or {}
        return a

    def ip(self):
        LOKAL.ip = roh_ip(self)
        # «Chat ausprobieren» in La Réception lädt die Website mit ?probe=1: Fragen und Anfragen daraus gelten als Beispiel (Robert 16.10.2026)
        LOKAL.probe = 'probe=1' in (self.headers.get('referer') or self.headers.get('Referer') or '') or self.headers.get('X-Reception-Probe') == '1'
        return LOKAL.ip

    def frage(messages, mappe=False, heute='', sprache='de'):
        LOKAL.anfrage = None
        g.ANWEISUNG = (gedaechtnis.anweisung(basis) if gedaechtnis else basis) + ZUSATZ + wissen_block()   # vom Team Berichtigtes, Ergänztes und Nachgetragenes gilt ab der nächsten Frage
        a = roh_frage(messages, mappe=mappe, heute=heute, sprache=sprache)
        e = getattr(LOKAL, 'anfrage', None)
        LOKAL.anfrage = None
        if e and (e.get('kontakt') or '').strip():
            erste = next((str(m.get('content', '')) for m in messages if m.get('role') == 'user'), '')
            gespraech = hashlib.sha1((getattr(LOKAL, 'ip', '') + '|' + erste[:300]).encode('utf-8')).hexdigest()[:16]
            sp = sprache if sprache in SPRACHEN else 'de'
            if re.search(r"\b(the|is|are|could|would|we|our|table|room|please)\b", (messages[-1].get('content') or '').lower()) and sp == 'de':
                sp = 'en'
            if a.get('text') in g.NICHTS.values() or not a.get('text'):   # Text endete am Werkzeug: kurzer Dank statt «dazu kann ich nichts sagen»
                a['text'] = DANKE.get(sp, DANKE['en'])
            verlauf = [{'rolle': m.get('role'), 'text': str(m.get('content', ''))[:600]} for m in messages[-8:]] + [{'rolle': 'assistant', 'text': a.get('text', '')[:1200]}]
            LOKAL.letzte = lege_anfrage(e, gespraech, sp, verlauf)
            if getattr(LOKAL, 'probe', False) and LOKAL.letzte:
                with SCHLOSS:
                    x = _lies(_pfad(LOKAL.letzte), {})
                    if x:
                        x['beispiel'] = True; x['probe'] = True; _schreib(_pfad(LOKAL.letzte), x)
        return a

    def merke(host, daten):
        if getattr(LOKAL, 'probe', False):   # Tor 3 G1 (30.10.2026): Proben des Teams («Chat ausprobieren», ?probe=1) kommen nicht unter die Gästefragen
            return
        try:
            lege_frage(dict(daten, anfrage=getattr(LOKAL, 'letzte', None) or '', beispiel=bool(getattr(LOKAL, 'probe', False))))
        except Exception:  # noqa: BLE001  die Antwort an den Gast bleibt davon unberührt
            pass

    roh_erlaubt = g.erlaubt
    PROBEN = {'tag': '', 'n': 0}

    def erlaubt(ip_, art='gast'):
        """Proben des Teams («Chat ausprobieren», Prüfläufe) zählen nicht gegen die Grenzen der Gäste, haben aber eine eigene: 400 am Tag (Carlton 17.10.2026)."""
        if getattr(LOKAL, 'probe', False) and art == 'gast':
            heute = time.strftime('%Y-%m-%d')
            with SCHLOSS:
                if PROBEN['tag'] != heute:
                    PROBEN.update(tag=heute, n=0)
                PROBEN['n'] += 1
                return PROBEN['n'] <= 400
        return roh_erlaubt(ip_, art)

    g._api, g.frage, g.merke, g.handler._ip, g.erlaubt = api, frage, merke, ip, erlaubt
    # Die Frage im Protokoll soll wissen, ob daraus eine Anfrage wurde: do_POST ruft frage(), dann merke(); dazwischen merkt sich LOKAL.letzte die Kennung.
    roh_post = g.handler.do_POST

    def do_post(self):
        LOKAL.letzte = None; LOKAL.probe = False
        return roh_post(self)
    g.handler.do_POST = do_post
    return g


# ---------------------------------------------------------------- Entwurf
def vorlage_text(art, sprache):
    """Die Fragen des Hauses aus seinem eigenen Mail-Link (vorlagen/<nr>.txt, Deutsch); ohne Vorlage leer. Der Assistent schreibt in der Sprache des Gastes."""
    nr, absender = VORLAGE.get(art, VORLAGE['nachricht'])
    if not nr:
        return '', absender, 'de', ''
    try:
        t = open(os.path.join(HIER, 'vorlagen', nr + '.txt'), encoding='utf-8').read().strip()
    except OSError:
        return nr, absender, 'de', ''
    return nr, absender, 'de', t


def _datum_aus(text):
    """Datum aus den Angaben der Formulare («Do, 22. Oktober 2026», «22.10.2026», «2026-10-22»); sonst None."""
    t = str(text or '')
    mon = {m: i for i, m in enumerate(('januar', 'februar', 'märz', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'dezember'), 1)}
    try:
        m = re.search(r'(\d{4})-(\d{2})-(\d{2})', t)
        if m:
            return datetime.date(int(m[1]), int(m[2]), int(m[3]))
        m = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', t)
        if m:
            return datetime.date(int(m[3]), int(m[2]), int(m[1]))
        m = re.search(r'(\d{1,2})\.\s*([A-Za-zÄÖÜäöü]+)\s+(\d{4})', t)
        if m and m[2].lower() in mon:
            return datetime.date(int(m[3]), mon[m[2].lower()], int(m[1]))
    except ValueError:
        return None
    return None


def hinweise(a):
    """Hinweise fürs Team zu einer Anfrage, nur aus Angaben des Hauses gerechnet (nicht gespeichert, bei jedem Lesen neu):
    kein Culinarium-Tag (Abende Freitag ab 19, Samstag ab 17 Uhr), Bar geschlossen (Sonntag bis Mittwoch), mehr als die vierzehn Plätze der Tafel,
    Allergien (die Website sagt nichts dazu: Küche fragen), Ticket zurückgeben (wird nicht rückerstattet), Termin steht noch nicht fest."""
    h = []
    d = _datum_aus(a.get('datum'))
    art = a.get('art')
    if d:
        if d.weekday() not in ABEND_TAGE and art in ('warteliste', 'abend'):
            h.append({'art': 'ruhetag', 'text': f'{TAG_NAME[d.weekday()]}: Culinarium-Abende gibt es freitags ab 19 und samstags ab 17 Uhr'})
        if d.weekday() in BAR_ZU and art == 'feier':
            h.append({'art': 'ruhetag', 'text': f'{TAG_NAME[d.weekday()]}: die Bar hat Sonntag bis Mittwoch geschlossen'})
    elif art in ('warteliste', 'abend'):
        h.append({'art': 'termin', 'text': 'Der nächste Termin steht noch nicht fest: Gast kommt auf die Warteliste'})
    try:
        p = int(a.get('personen') or 0)
    except (TypeError, ValueError):
        p = 0
    if p > TAFEL:
        h.append({'art': 'gruppe', 'text': f'{p} Personen: mehr als die {TAFEL} Plätze an der Tafel'})
    elif p >= 7 and art in ('warteliste', 'abend'):
        h.append({'art': 'gruppe', 'text': f'{p} Plätze: die Warteliste nimmt bis 6, bei {p} von {TAFEL} Plätzen den Abend gemeinsam planen'})
    al = [ALLERGENE.get(x, x) for x in (a.get('allergene') or []) if isinstance(x, str)]
    text = ' '.join(str(a.get(k) or '') for k in ('anliegen', 'nachricht'))
    text = re.sub(r'(?:Wünsche, Allergien|Allergien)\s*:|keine angegeben', ' ', text)   # Feldnamen der Formulare zählen nicht, nur was der Gast schreibt
    frei = re.findall(r'allerg\w*|unverträglich\w*|verträgt keine?\b|zöliak\w*|gluten\w*|laktose\w*|nuss\w*|nüsse|vegetar\w*|vegan\w*', text, re.I)
    if al:
        h.append({'art': 'allergie', 'text': 'Allergien und Wünsche: ' + ', '.join(al) + ' (Küche fragen)'})
    elif frei:
        h.append({'art': 'allergie', 'text': 'Allergie oder Wunsch zur Küche im Text: die Website sagt dazu nichts, Rudi fragen'})
    if re.search(r'zurückgeb\w*|rückerstatt\w*|stornier\w*|absagen|refund|cancel', text, re.I):
        h.append({'art': 'ticket', 'text': 'Ticket zurückgeben: Tickets werden nicht rückerstattet (Vorverkauf)'})
    return h

def entwurf(id_, hinweis=''):
    if not _gueltig(id_, 'anfragen'):
        raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
    if _G is None:
        raise ValueError('CHAT · Der Assistent ist noch nicht geladen. Einmal eine Frage im Chat stellen oder server.py neu starten.')
    a = _lies(_pfad(id_), {})
    nr, absender, sp_v, vorlage = vorlage_text(a.get('art'), a.get('sprache', 'de'))
    absender = KONTAKT   # Culinarium hat keine Mail-Adresse: der Brief nennt die Wege des Hauses (Bar, Instagram)
    gast = '\n'.join(f"{'Gast' if v.get('rolle') == 'user' else 'Chat des Hauses'}: {v.get('text', '')}" for v in a.get('verlauf') or [])
    mail = (f"Art: {ARTEN.get(a.get('art'), a.get('art'))}\nAbteilung: {a.get('abteilung') or ART_ABTEILUNG.get(a.get('art'), 'Nachrichten')}\nName: {a.get('name')}\nKontakt: {a.get('kontakt')}\nDatum: {a.get('datum') or 'nicht genannt'}\n"
            f"Personen: {a.get('personen') or 'nicht genannt'}\nAnliegen: {a.get('anliegen')}\nSprache des Gastes: {a.get('sprache')}\n\nGESPRÄCH IM CHAT:\n{gast}\n\n"
            f"Allergien (Formular): {', '.join(ALLERGENE.get(x, x) for x in a.get('allergene') or []) or 'keine angegeben'}\nHinweise: {'; '.join(x['text'] for x in hinweise(a)) or 'keine'}\n\n"
            f"VORLAGE DES HAUSES ({nr or 'keine'}, Sprache {sp_v}):\n{vorlage or '(keine: nur der Ton des Hauses)'}")
    _G.ANFRAGE = ANFRAGE_GBR + (gedaechtnis.wissen_text(_G.WISSEN) if gedaechtnis else _G.WISSEN) + wissen_block()   # derselbe Stand wie im Chat
    r = _G.anfrage(mail, hinweis)
    if r.get('fehler'):
        raise ValueError('ENTWURF · ' + r['fehler'])
    entwurf_neu = {'betreff': r.get('betreff', ''), 'text': r.get('text', ''), 'team': r.get('team', ''), 'vorlage': nr, 'absender': absender,
                   'zeit': datetime.datetime.now().astimezone().isoformat(timespec='seconds')}
    with SCHLOSS:
        # frisch lesen: während der Assistent schrieb (Sekunden), kann das Team die Anfrage geändert haben (Status, Notiz, Betreff);
        # vorher überschrieb der alte Stand von oben diese Änderungen (17.10.2026)
        a = _lies(_pfad(id_), a)
        entwurf_neu['fassung'] = ((a.get('entwurf') or {}).get('fassung', 0) or 0) + 1
        a['entwurf'] = entwurf_neu
        if a.get('status') == 'neu':
            a['status'] = 'gelesen'
        _schreib(_pfad(id_), a)
    return a['entwurf']


# ---------------------------------------------------------------- Schnittstelle für La Réception (/reception/api/<was>)
def ueberblick():
    an = _alle('anfragen'); fr = _alle('fragen'); ng = nachgetragen()
    erledigt = set(_lies(_pfad('status.json'), {}).get('fragen_erledigt', []))
    luecken = [f for f in fr if not f.get('belegt') and f['id'] not in erledigt]
    return {'anfragen_neu': sum(1 for a in an if a.get('status') == 'neu'), 'anfragen_offen': sum(1 for a in an if a.get('status') != 'erledigt'),
            'anfragen_gesamt': len(an), 'fragen_gesamt': len(fr), 'ohne_antwort': len(luecken), 'nachgetragen_gesamt': len(ng),
            'letzte_frage': fr[0]['zeit'] if fr else '', 'speicher': os.path.relpath(DATEN, WEB)}

# ---------------------------------------------------------------- Online-Eingang der Website (29.10.2026)
# Die Website läuft auf Vercel, das Gästebuch auf Roberts Rechner. Was Gäste dort eintragen (assets/anfrage.js), liegt in der Funktion /api/anfrage
# (privater Speicher in Frankfurt). Das Gästebuch holt es mit dem Schlüssel aus online/schluessel.txt ab, legt es wie ein Formular in den Eingang
# und löscht es danach online. RECEPTION_ONLINE=aus schaltet das Abholen ab (Prüfläufe mit Wegwerf-Daten), eine andere Adresse geht ebenso.
# Nur das echte Gästebuch (Datenordner daten/) holt von selbst ab. Probe-Kopien mit RECEPTION_DATEN holen nur mit ausdrücklichem RECEPTION_ONLINE,
# sonst nähmen Prüfläufe echte Einträge der Gäste in ihre Wegwerf-Daten mit (29.10.2026: zwei Proben so verschwunden).
ONLINE_API = os.environ.get('RECEPTION_ONLINE') or ('https://culinarium-hannover-entwurf.vercel.app/api/anfrage' if DATEN == os.path.join(HIER, 'daten') else 'aus')
ONLINE_SCHLUESSEL = os.path.join(HIER, 'online', 'schluessel.txt')
ONLINE_STAND = {'zeit': '', 'neu': 0, 'fehler': ''}
_ONLINE_SCHLOSS = threading.Lock()


def online_abholen():
    """Holt die Anfragen der Website ab; jede kommt genau einmal in den Eingang (online_id), erst danach wird sie online gelöscht."""
    import urllib.parse, urllib.request
    if ONLINE_API == 'aus' or not _ONLINE_SCHLOSS.acquire(blocking=False):
        return 0
    try:
        k = open(ONLINE_SCHLUESSEL, encoding='utf-8').read().strip()
        with urllib.request.urlopen(ONLINE_API + '?' + urllib.parse.urlencode({'k': k}), timeout=20) as r:
            roh = json.load(r)
        liste, fragen = roh.get('anfragen') or [], roh.get('fragen') or []
        schon = {a.get('online_id') for a in _alle('anfragen') + _alle('fragen') if a.get('online_id')}
        neu = 0
        for f in fragen:   # der Gäste-Chat der Website: jede Frage mit Antwort, ohne Antwort als Lücke unter «Das wurde gefragt»
            oid = str(f.get('id') or '')
            if not re.fullmatch(r'fragen/\d{4}-\d{2}-\d{2}/[\w-]+\.json', oid):
                continue
            if f.get('probe'):   # Tor 3 (30.10.2026): Probe-Fragen der Website (?probe=1, Prüfläufe) kommen nicht unter die Gästefragen; online wird sie trotzdem gelöscht
                pass
            elif oid not in schon:
                fid = lege_frage({'frage': f.get('frage', ''), 'antwort': f.get('antwort', ''), 'belegt': f.get('belegt') is not False, 'thema': f.get('thema', ''), 'sprache': f.get('sprache', 'de')})
                with SCHLOSS:
                    x = _lies(_pfad(fid), {})
                    x.update({'online_id': oid, 'web': True, **({'probe': True} if f.get('probe') else {})})
                    try:
                        x['zeit'] = datetime.datetime.fromisoformat(str(f.get('zeit'))).astimezone().isoformat(timespec='seconds')
                    except ValueError:
                        pass
                    _schreib(_pfad(fid), x)
                neu += 1
            weg = urllib.request.Request(ONLINE_API + '?' + urllib.parse.urlencode({'k': k, 'weg': oid}), data=b'', method='POST')
            urllib.request.urlopen(weg, timeout=20).read()
        for a in liste:
            oid = str(a.get('id') or '')
            if not re.fullmatch(r'anfragen/\d{4}-\d{2}-\d{2}/[\w-]+\.json', oid):
                continue
            if oid not in schon:
                try:
                    post('formular', {**{k_: v for k_, v in a.items() if k_ != 'id'}, 'website': '', 'online_id': oid})
                except ValueError as e:   # nimmt das Gästebuch nicht an: online liegen lassen, Stand zeigt es
                    ONLINE_STAND['fehler'] = f'{oid}: {e}'
                    continue
                neu += 1
            weg = urllib.request.Request(ONLINE_API + '?' + urllib.parse.urlencode({'k': k, 'weg': oid}), data=b'', method='POST')
            urllib.request.urlopen(weg, timeout=20).read()
        ONLINE_STAND.update(zeit=datetime.datetime.now().astimezone().isoformat(timespec='seconds'), neu=neu)
        if not any(str(a.get('id')) in ONLINE_STAND['fehler'] for a in liste):
            ONLINE_STAND['fehler'] = ''
        return neu
    except Exception as e:  # noqa: BLE001 (kein Netz, Schlüssel fehlt, Speicher besetzt): beim nächsten Mal wieder
        ONLINE_STAND['fehler'] = type(e).__name__ + ': ' + str(e)[:160]
        return 0
    finally:
        _ONLINE_SCHLOSS.release()


def get(was, q=None):
    if was.startswith('wissen') and gedaechtnis:
        return {**gedaechtnis.get(was, q), 'nachgetragen': nachgetragen()} if was == 'wissen' else gedaechtnis.get(was, q)
    beispiele(); beispiel_fragen()
    if was == 'ueberblick':
        return ueberblick()
    if was == 'anfragen':
        an = _alle('anfragen')
        for a in an:
            a['hinweise'] = hinweise(a)
            a['allergene_lang'] = [ALLERGENE.get(x, x) for x in a.get('allergene') or [] if isinstance(x, str)]
        return {'anfragen': an, **ueberblick()}
    if was == 'fragen':
        erledigt = set(_lies(_pfad('status.json'), {}).get('fragen_erledigt', []))
        fr = _alle('fragen')
        for f in fr:
            f['erledigt'] = f['id'] in erledigt
            f['gruppe'] = thema_von(f.get('frage'))
        return {'fragen': fr, 'nachgetragen': nachgetragen(), **ueberblick()}
    if was == 'vorlage':
        nr, absender, sp, t = vorlage_text((q or {}).get('art', ['nachricht'])[0], (q or {}).get('sprache', ['de'])[0])
        return {'vorlage': nr, 'absender': absender, 'sprache': sp, 'text': t}
    raise ValueError('ANFRAGE · Unbekannte Ansicht.')

def brief_pdf(id_, port):
    """Der Brief einer Anfrage als A4-PDF: Chromium setzt brief-pdf.html (brief_pdf.js, Playwright wie in La Carte). Gibt (Bytes, Dateiname) zurück."""
    import subprocess, tempfile
    if not _gueltig(id_, 'anfragen'):
        raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
    a = _lies(_pfad(id_), {}); e = a.get('entwurf') or {}
    if not e.get('text'):
        raise ValueError('BRIEF · Zu dieser Anfrage gibt es noch keinen Brief.')
    daten = {'name': a.get('name') or '', 'kontakt': a.get('kontakt') or '', 'absender': e.get('absender') or KONTAKT,
             'betreff': e.get('betreff') or '', 'text': e.get('text') or '', 'gestalt': e.get('gestalt') or {}}
    node = shutil.which('node') or next((x for x in ('/opt/homebrew/bin/node', '/usr/local/bin/node') if os.path.exists(x)), None)
    if not node:
        raise ValueError('PDF · node ist nicht installiert (wird für das PDF gebraucht).')
    with tempfile.TemporaryDirectory() as t:
        quelle, ziel = os.path.join(t, 'brief.json'), os.path.join(t, 'brief.pdf')
        with open(quelle, 'w', encoding='utf-8') as f:
            json.dump(daten, f, ensure_ascii=False)
        try:
            r = subprocess.run([node, os.path.join(HIER, 'brief_pdf.js'), str(port), quelle, ziel], capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            raise ValueError('PDF · Das PDF liess sich nicht setzen (Zeitüberschreitung).')
        if r.returncode != 0 or not os.path.exists(ziel):
            raise ValueError('PDF · Das PDF liess sich nicht setzen. Ist Playwright installiert? ' + (r.stderr or '')[-160:])
        roh = open(ziel, 'rb').read()
    wer = re.sub(r'[\\/:*?"<>|\n\r]+', ' ', a.get('name') or 'Gast').strip()[:60] or 'Gast'
    return roh, f'Culinarium – {wer} – {datetime.date.today().strftime("%d.%m.%Y")}.pdf'


def post(was, d):
    if was.startswith('wissen') and gedaechtnis:
        return gedaechtnis.post(was, d)
    beispiele(); beispiel_fragen()
    if was == 'uebersetzen':
        return {**uebersetzen(d.get('id')), **ueberblick()}
    if was == 'entwurf':
        return {'entwurf': entwurf(d.get('id'), str(d.get('hinweis') or '')[:2000]), **ueberblick()}
    if was == 'anfrage':            # Status, Notiz oder geänderter Entwurf des Teams
        id_ = d.get('id')
        if not _gueltig(id_, 'anfragen'):
            raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
        with SCHLOSS:
            a = _lies(_pfad(id_), {})
            aendert = a.get('entwurf') and (isinstance(d.get('entwurf_text'), str) or isinstance(d.get('gestalt'), dict))
            if aendert and isinstance(d.get('fassung'), int) and d['fassung'] != a['entwurf'].get('fassung', 0):
                raise ValueError('KONFLIKT · Dieser Brief wurde inzwischen in einem anderen Fenster geändert. Deine Eingabe ist noch hier; bitte kopieren, neu laden und wieder einsetzen.')
            if aendert:
                a['entwurf']['fassung'] = a['entwurf'].get('fassung', 0) + 1
            if d.get('status') in ('neu', 'gelesen', 'erledigt'):
                a['status'] = d['status']
            if isinstance(d.get('entwurf_text'), str) and a.get('entwurf'):
                if 'original' not in a['entwurf']:
                    a['entwurf']['original'] = {'text': a['entwurf'].get('text') or '', 'betreff': a['entwurf'].get('betreff') or ''}
                a['entwurf']['text'] = d['entwurf_text'][:12000]
                if isinstance(d.get('betreff'), str):
                    a['entwurf']['betreff'] = d['betreff'][:300]
                a['entwurf']['geaendert'] = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
            if isinstance(d.get('gestalt'), dict) and a.get('entwurf') and len(json.dumps(d['gestalt'])) < 20000:   # Anordnung des Briefs (verschoben, Grösse, Bündigkeit, Kopftexte)
                a['entwurf']['gestalt'] = d['gestalt']
            _schreib(_pfad(id_), a)
        return {'ok': True, 'fassung': (a.get('entwurf') or {}).get('fassung', 0), **ueberblick()}
    if was == 'formular':           # Formular der Website (baustein/anfrage.js): landet im Eingang, nicht in einem Mailfach (Rivage E12, Ruedihus 17.10.2026, Schlössli 19.10.2026, Schäfli 21.10.2026, Culinarium 28.10.2026)
        if d.get('website'):        # Feld, das Menschen nicht sehen: nur Maschinen füllen es aus
            return {'ok': True}
        name, kontakt = str(d.get('name') or '').strip()[:120], str(d.get('kontakt') or '').strip()[:160]
        if not kontakt:
            raise ValueError('FORMULAR · Bitte E-Mail oder Telefon angeben, damit das Haus antworten kann.')
        if not re.fullmatch(r'[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]{2,}|\+?[\d\s/().-]{7,24}', kontakt):
            raise ValueError('FORMULAR · Bitte eine gültige E-Mail-Adresse oder Telefonnummer angeben.')
        art = d.get('art') if d.get('art') in ARTEN else 'nachricht'
        sp = d.get('sprache') if d.get('sprache') in SPRACHEN else 'de'
        try:
            pers = max(1, min(60, int(d.get('personen'))))   # die Warteliste nimmt 1 bis 6, eine Feier mehr
        except (TypeError, ValueError):
            pers = None
        anliegen = str(d.get('anliegen') or '').strip()[:300]
        nachricht = str(d.get('nachricht') or '').strip()[:6000]   # Angaben des Formulars + Nachricht des Gastes (bis 1'200) + Wünsche ohne Grenze: 1'200 schnitt still ab (Prüfung 17.10.2026); die Anfrage selbst bleibt unter 12 kB
        an = KONTAKT
        allergene = [x for x in (d.get('allergene') or []) if x in ALLERGENE][:len(ALLERGENE)] if isinstance(d.get('allergene'), list) else []
        seite = str(d.get('seite') or '')[:160]
        seite = re.sub(r'[^\w./?#=&%-]', '', seite) if seite.startswith('/') else ''   # Weg der Seite (mit ? und #), nur harmlose Zeichen
        seite_name = re.sub(r'[<>]', '', str(d.get('seite_name') or ''))[:80]
        formular = d.get('formular') if d.get('formular') in FORMULARE else 'allgemein'
        text = nachricht or anliegen
        id_ = lege_anfrage({'art': art, 'name': name, 'kontakt': kontakt, 'datum': str(d.get('datum') or '')[:120], 'personen': pers, 'anliegen': anliegen or text[:200]},
                           'formular-' + hashlib.sha1(f'{time.time()}{random.random()}'.encode()).hexdigest()[:12], sp,
                           [{'rolle': 'user', 'text': f'Über ein Formular der Website (Seite {seite_name or seite or "unbekannt"}): ' + text}])
        with SCHLOSS:
            x = _lies(_pfad(id_), {})
            x.update({'web': True, 'an': an, 'abteilung': ART_ABTEILUNG.get(art, 'Nachrichten'), 'seite': seite, 'seite_name': seite_name, 'formular': formular,
                      'nachricht': nachricht, 'allergene': allergene, 'uhrzeit': str(d.get('uhrzeit') or '')[:20], 'platz': str(d.get('platz') or '')[:60], 'hund': d.get('hund') is True})
            if d.get('probe') is True:
                x['probe'] = True
            if d.get('online_id'):   # von der Website über /api/anfrage (online_abholen): Zeit des Gastes und Kennung im Online-Speicher
                x['online_id'] = str(d['online_id'])[:120]
                try:
                    x['zeit'] = datetime.datetime.fromisoformat(str(d.get('zeit'))).astimezone().isoformat(timespec='seconds')
                except ValueError:
                    pass
            _schreib(_pfad(id_), x)
        return {'ok': True, 'danke': DANKE.get(sp, DANKE['de'])}
    if was == 'weg':                # Anfrage oder Frage löschen (Wunsch des Gastes, Test)
        id_ = d.get('id', '')
        art = id_.split('/')[0]
        if art not in ('anfragen', 'fragen') or not _gueltig(id_, art):
            raise ValueError('ANFRAGE · Dieser Eintrag existiert nicht.')
        with SCHLOSS:
            os.remove(_pfad(id_))
            for rest in ('.gut', '.neu'):
                try:
                    os.remove(_pfad(id_) + rest)
                except OSError:
                    pass
        return {'ok': True, **ueberblick()}
    if was == 'frage':              # Frage erledigt / wieder offen
        id_ = d.get('id')
        if not _gueltig(id_, 'fragen'):
            raise ValueError('FRAGE · Diese Frage gibt es nicht mehr.')
        with SCHLOSS:
            s = _lies(_pfad('status.json'), {}); l = [x for x in s.get('fragen_erledigt', []) if x != id_]
            if d.get('erledigt'):
                l.append(id_)
            s['fragen_erledigt'] = l[-5000:]
            _schreib(_pfad('status.json'), s)
        return {'ok': True, **ueberblick()}
    if was == 'nachtragen':         # Antwort des Teams auf eine Frage ohne Antwort
        frage_ = str(d.get('frage') or '').strip()[:400]; antwort = str(d.get('antwort') or '').strip()[:2000]
        if len(frage_) < 3 or len(antwort) < 3:
            raise ValueError('EINGABE · Bitte Frage und Antwort ausfüllen.')
        with SCHLOSS:
            l = nachgetragen()
            nid = d.get('nid') or ('n' + str(int(time.time() * 1000)))
            alt = next((x for x in l if x.get('nid') == nid), None)
            eintrag = {'nid': nid, 'frage': frage_, 'antwort': antwort, 'zeit': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                       'quelle': d.get('quelle') or (alt or {}).get('quelle') or ''}
            l = [x for x in l if x.get('nid') != nid] + [eintrag]
            _schreib(_pfad('nachgetragen.json'), l)
            if d.get('quelle') and _gueltig(d['quelle'], 'fragen'):
                s = _lies(_pfad('status.json'), {}); fe = set(s.get('fragen_erledigt', [])); fe.add(d['quelle'])
                s['fragen_erledigt'] = sorted(fe)[-5000:]; _schreib(_pfad('status.json'), s)
        return {'ok': True, 'eintrag': eintrag, **ueberblick()}
    if was == 'nachtragen_weg':
        with SCHLOSS:
            _schreib(_pfad('nachgetragen.json'), [x for x in nachgetragen() if x.get('nid') != d.get('nid')])
        return {'ok': True, **ueberblick()}
    raise ValueError('ANFRAGE · Unbekannter Auftrag.')
