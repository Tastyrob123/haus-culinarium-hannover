"""Der Chat von Culinarium Hannover (Food-Pairing-Abende an der langen Tafel in der Bar Walk on the Wild Side, Linden; dazu das Pop-up Dirty Chicken).
Kopie aus der Taverne zum Schäfli (28.10.2026, dort aus dem Schlössli, Carlton-Europe und Ruedihus), Warteliste für den nächsten Abend statt Tischreservation.
Auf der Website von Culinarium gibt es den Chat noch nicht; in La Réception läuft er unter «Chat ausprobieren» (Python ohne Zusatzpakete).

Eingang (POST, JSON):
  {"messages":[{"role":"user"|"assistant","content":"…"}], "mappe":bool, "sprache":"de|en|fr", "heute":"YYYY-MM-DD"}   Gästechat
  {"modus":"anfrage", "mail":"…", "hinweis":"…"}                                                                     Antwort-Entwurf auf eine Anfrage
Wissen: gast_wissen.txt (Wortlaut der Website) und gast_umgebung.txt (Tickets laut Instagram, Kontaktwege, Lage). Ohne Orte in gast_haus.json
holt der Chat kein Wetter (am Rechner nichts aus dem Netz). Der Chat antwortet nur daraus.
Schlüssel: ANTHROPIC_API_KEY, ANTHROPIC_WORKSPACE_ID beim Vercel-Projekt. Jede Gästefrage geht mit Antwort an /api/fragen (Speicher fürs Studio,
siehe fragen.js), gesichert mit GAST_GEHEIM. Schutz gegen Missbrauch: Grenzen je Besucher und je Tag (siehe GRENZEN), nur Aufrufe von der eigenen Seite."""
from http.server import BaseHTTPRequestHandler
import collections, datetime, json, os, re, threading, time, urllib.request, urllib.error

HIER = os.path.dirname(os.path.abspath(__file__))
def _lies(n):
    try:
        return open(os.path.join(HIER, n), encoding='utf-8').read()
    except OSError:
        return ''
WISSEN = _lies('gast_wissen.txt')
TAL = _lies('gast_umgebung.txt')
# Das Haus (gast_haus.json daneben, aus den Quellen des Culinarium, _bau/culinarium_wissen.py). Ohne die Datei startet der Chat nicht mit fremden Werten:
# Vorfall 10.10.2026 (Carlton-Hundepreise als Antwort im Gasterntal), deshalb stehen hier keine Werte und kein Muster eines anderen Hauses mehr.
HAUS = {'name': 'Culinarium', 'ort': 'Hannover-Linden', 'tel': '', 'mail': '', 'kontakt': '', 'adresse': '', 'zeiten': '', 'fahrplan': '', 'kategorien': [], 'orte': [],
        'art': 'Food-Pairing-Abende', 'ruhetage': '', 'reservation_name': 'Warteliste'}
try:
    HAUS.update(json.loads(_lies('gast_haus.json') or '{}'))
except ValueError:
    pass
MUSTER_CARLTON = ''
REGELN_MEHR = f'''- Sprache: Schreibt der Gast Englisch, Französisch oder eine andere Sprache, antwortest du vollständig in seiner Sprache, auch die Punkte. Nur bei deutschen Fragen deutsch.
- Du bist ein KI-Assistent, kein Mensch. Wenn jemand fragt, sag das.
- Bleib bei Culinarium, seinen Abenden, Drinks und Gängen, der Bar Walk on the Wild Side, dem Pop-up Dirty Chicken, {HAUS['ort']} und dem Weg dorthin. Zu anderen Themen freundlich zurück zum Abend.
- Persönliche Daten (Kreditkarten, Ausweise, PayPal-Zugang) nimmst du nicht entgegen; dafür ist das Team da.
- Schreibe immer zuerst deine Antwort an den Gast, dann erst ein Werkzeug.
- Widersprechen sich die Seiten der Website und eine ältere Unterlage, gilt die Website.
- Sagt eine Seite «auf Anfrage» oder nennt keinen Preis, nennst du auch keinen.'''   # 15.10.2026: vorher standen diese Regeln versehentlich im Muster
MUSTER = HAUS.get('muster') or MUSTER_CARLTON
MODELL = 'claude-sonnet-5-5'   # Robert 10.10.2026: alle Häuser auf Sonnet 5.5 (Haiku 4.5 irrte bei Öffnungstagen und erfand Ausflüge; davor Opus 5.5).
MODELL = HAUS.get('modell') or MODELL   # je Haus umstellbar (gast_haus.json): Doldenhorn seit 10.10.2026 auf Sonnet 5.5, Haiku machte dort Fehler (Au Gourmet samstags zu)
GRENZE = 1000 if 'haiku' in MODELL else 4000   # Sonnet denkt vor der Antwort mit; mit 1000 brach die Antwort mitten im Satz ab (10.10.2026)
TEL = HAUS['tel']
MAIL = HAUS['mail']
KONTAKT = HAUS.get('kontakt') or ' oder '.join(x for x in (TEL, MAIL) if x)   # Culinarium: die Bar am Telefon oder eine Nachricht auf Instagram (keine eigene Mail)
HOECHSTENS_NACHRICHTEN = 12   # nur die letzten Beiträge reisen mit
HOECHSTENS_ZEICHEN = 600      # je Frage
# Grenzen gegen Missbrauch: je Besucher (IP) und gesamt je Tag. Darüber antwortet die Rezeption freundlich mit der Telefonnummer.
GRENZEN = {'besucher_10min': 20, 'besucher_tag': 80, 'gesamt_tag': 2000, 'anfrage_tag': 60}
SPRACHE = {'de': 'Deutsch, Schreibung wie die Website (ss statt ß, Namen wie Haasemannstraße bleiben)', 'en': 'Englisch (britische Schreibung)', 'fr': 'Französisch'}

ANWEISUNG = f"""Du bist der Chat von {HAUS['name']} in {HAUS['ort']} ({HAUS['art']}) und beantwortest Fragen der Gäste im Chatfenster der Website.

Regeln:
- Antworte nur mit dem, was in WISSEN oder TALWISSEN steht. WISSEN ist der Wortlaut der Website (Der Abend, Alle Abende, Das Haus, Team, Der Weg, Dirty Chicken); TALWISSEN sind die Wege zum Ticket und zum Team. Erfinde nichts dazu, auch keine Preise, Termine, Plätze, Gänge oder Regeln.
- Steht die Antwort nirgends, sag das offen und verweise an das Team: {KONTAKT}. Rufe dann zusätzlich das Werkzeug nicht_belegt auf.
- Termine und Plätze: Der nächste Termin steht noch nicht fest; nenne nie ein Datum, das nicht in WISSEN steht. Du kannst nichts prüfen und nichts zusagen. Rufe das Werkzeug warteliste auf, sobald der Gast einen Platz will oder wissen möchte, wann der nächste Abend ist. {HAUS['ruhetage']}.
- Allergien und Unverträglichkeiten: Die Website sagt dazu nichts. Sag, dass Rudi in der Küche es mit dem Gast klärt, und nimm es in eine Anfrage auf. Sag nie von dir aus, ein Gang sei frei davon. «Vegetarisch» ist kein Merkmal der Abende; sag nicht, dass sie vegetarisch sind.
- Form (wichtig, der Gast liest auf dem Handy): Erst EIN kurzer Satz mit der direkten Antwort. Wenn es mehrere Angaben gibt (Zeiten, Preis, Ablauf), danach höchstens vier Punkte, jeder auf einer eigenen Zeile, beginnend mit «- », im Muster «Stichwort: Angabe». Kein Absatz länger als zwei Sätze. Nur, was gefragt ist; Zusätzliches höchstens als ein kurzer Satz am Schluss.
- Ton wie die Website: immer «du», herzlich, knapp, ein bisschen Linden. Jeder Satz macht den Abend wertvoller (der einzelne Gast, das erklärte Glas, der von Hand angerichtete Teller); vierzehn Plätze nur als «wenige Plätze», nie als Menge. Nie «gute Frage», «gerne doch», «leider» am Satzanfang oder andere Floskeln. Keine Emojis, kein Fettdruck, keine Überschriften, keine Gedankenstriche.
- Nichts Ungefragtes: Fragt jemand nach dem Weg, kein Wort zum Preis. Fragt jemand nach den Drinks, nichts zu Dirty Chicken.
{REGELN_MEHR}
- Warteliste: Du prüfst nichts selbst, sag nie «ich prüfe», «ich zeige» oder «ich schaue nach». Erster Satz: Auf der Warteliste erfährt der Gast den nächsten Abend zuerst. Nennt der Gast etwas Besonderes (Allergie, Anlass, mehrere Plätze) oder stellt er dazu eine Frage, folgen die Angaben aus WISSEN als Punkte, im selben Text, bevor du die Warteliste aufrufst. Die Frage des Gastes bleibt nie unbeantwortet.

So sehen gute Antworten aus (nur die FORM übernehmen; Zahlen und Angaben stammen immer aus WISSEN dieses Hauses, nie aus den Mustern):
{MUSTER}

WISSEN:
{WISSEN}

TALWISSEN:
{TAL or '(keins)'}"""

# ANFRAGE: Grundfassung; La Réception setzt beim Einbinden ihre eigene (reception.ANFRAGE_GBR) ein.
ANFRAGE = f"""Du schreibst im Namen des Teams von {HAUS['name']} in {HAUS['ort']} den Entwurf einer Antwort an einen Gast (Warteliste, Platz an einem Abend, eigene Feier).

Regeln:
- Alles, was du an Preisen, Zeiten, Plätzen, Drinks und Gängen nennst, steht wörtlich in WISSEN. Erfinde nichts; der nächste Termin steht noch nicht fest, setz dafür [Termin eintragen].
- Freie Plätze kannst du nicht prüfen: setz dafür [Plätze prüfen].
- Was in der Anfrage fehlt (Tag, Plätze, Wünsche), erfragst du freundlich am Ende, in einer kurzen Liste.
- Was das Team selbst entscheiden muss, markierst du in eckigen Klammern, zum Beispiel [Preis bestätigen].
- Ton der Website: Du, herzlich, knapp, keine Werbesprache, keine Emojis, kein Fettdruck. Kurze Absätze.
- Sprache: die Sprache der Anfrage.
- Form: Zeile 1 «Betreff: …», dann Leerzeile, dann die Antwort mit Anrede und Gruss «Bis bald an der Tafel» und darunter «[Name], {HAUS['name']} im Walk on the Wild Side».
- Nach der Antwort eine Zeile «---» und darunter für das Team, nicht für den Gast: «Grundlage:» mit den Seiten, aus denen die Angaben stammen, und «Offen:» mit dem, was das Team vor dem Senden klären muss.

WISSEN:
{WISSEN}"""

WERKZEUGE = [{
    'name': 'warteliste',
    'description': 'Zeigt dem Gast im Chat den Weg zur Warteliste auf der Seite «Der Abend» (Tag, Plätze, Name, E-Mail). Aufrufen, sobald der Gast einen Platz will oder wissen möchte, wann der nächste Abend ist. Eintragen, was der Gast schon genannt hat, den Rest null lassen.',
    'strict': True,
    'input_schema': {'type': 'object', 'additionalProperties': False,
                     'required': ['datum', 'uhrzeit', 'personen'],
                     'properties': {'datum': {'type': ['string', 'null'], 'description': 'Tag: fr, sa, egal oder null'},
                                    'uhrzeit': {'type': ['string', 'null'], 'description': 'immer null (die Abende beginnen Freitag 19 Uhr, Samstag 17 Uhr)'},
                                    'personen': {'type': ['integer', 'null'], 'description': 'Plätze (1 bis 6) oder null'}}}},
    {
    'name': 'nicht_belegt',
    'description': 'Vermerk für das Haus: Die Frage des Gastes liess sich aus WISSEN und TALWISSEN nicht beantworten. Das Team sieht diese Fragen in seinem Werkzeug und trägt die Antwort nach.',
    'strict': True,
    'input_schema': {'type': 'object', 'additionalProperties': False, 'required': ['thema'],
                     'properties': {'thema': {'type': 'string', 'description': 'Worum es ging, in zwei bis vier Wörtern auf Deutsch, z. B. «Nussallergie»'}}}}]
MAPPE = """

Zusatz: Der Gast sitzt bereits an der Tafel. Antworte wie das Team vor Ort (was heute kommt, wo etwas ist), nicht wie für jemanden, der erst auf die Warteliste will."""

# ---------------------------------------------------------------- Wetter (Open-Meteo, frei, ohne Schlüssel), 30 Minuten gemerkt
WMO = {0: 'klar', 1: 'überwiegend klar', 2: 'teils bewölkt', 3: 'bedeckt', 45: 'Nebel', 48: 'Raureifnebel', 51: 'leichter Niesel', 53: 'Niesel', 55: 'starker Niesel',
       61: 'leichter Regen', 63: 'Regen', 65: 'starker Regen', 66: 'gefrierender Regen', 67: 'gefrierender Regen', 71: 'leichter Schneefall', 73: 'Schneefall', 75: 'starker Schneefall',
       77: 'Schneegriesel', 80: 'Regenschauer', 81: 'Regenschauer', 82: 'heftige Regenschauer', 85: 'Schneeschauer', 86: 'starke Schneeschauer', 95: 'Gewitter', 96: 'Gewitter mit Hagel', 99: 'Gewitter mit Hagel'}
ORTE = [tuple(o) for o in HAUS['orte']]
_WETTER = {'zeit': 0, 'text': ''}

def wetter():
    if time.time() - _WETTER['zeit'] < 1800 and _WETTER['text']:
        return _WETTER['text']
    zeilen = []
    try:
        for name, la, lo in ORTE:
            u = (f'https://api.open-meteo.com/v1/forecast?latitude={la}&longitude={lo}&current=temperature_2m,weather_code'
                 '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunset&timezone=Europe%2FZurich&forecast_days=3')
            with urllib.request.urlopen(u, timeout=4) as r:
                d = json.load(r)
            c, t = d['current'], d['daily']
            zeilen.append(f"{name}: jetzt {c['temperature_2m']:.0f} °C, {WMO.get(c['weather_code'], 'unbekannt')}. " + ' · '.join(
                f"{tag}: {WMO.get(w, '?')}, {lo_:.0f} bis {hi:.0f} °C, Regen {p} %, Sonnenuntergang {s[-5:]}"
                for tag, w, lo_, hi, p, s in zip(t['time'], t['weather_code'], t['temperature_2m_min'], t['temperature_2m_max'], t['precipitation_probability_max'], t['sunset'])))
        _WETTER.update(zeit=time.time(), text='Vorhersage Open-Meteo, abgerufen ' + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).strftime('%d.%m.%Y %H:%M') + '\n' + '\n'.join(zeilen))
    except Exception:  # noqa: BLE001  ohne Wetter antwortet die Rezeption trotzdem
        pass
    return _WETTER['text'] or '(Wetter gerade nicht abrufbar: auf meteoschweiz.ch verweisen)'

# ---------------------------------------------------------------- Grenzen je Besucher und Tag (im Speicher der laufenden Funktion)
SCHLOSS = threading.Lock()
BESUCHER = collections.defaultdict(list)
TAG = {'tag': '', 'n': 0, 'anfrage': 0}

def erlaubt(ip, art='gast'):
    jetzt, heute = time.time(), time.strftime('%Y-%m-%d')
    with SCHLOSS:
        if TAG['tag'] != heute:
            TAG.update(tag=heute, n=0, anfrage=0); BESUCHER.clear()
        if art == 'anfrage':
            if TAG['anfrage'] >= GRENZEN['anfrage_tag']:
                return False
            TAG['anfrage'] += 1
            return True
        z = [t for t in BESUCHER[ip] if jetzt - t < 86400]
        if len(z) >= GRENZEN['besucher_tag'] or len([t for t in z if jetzt - t < 600]) >= GRENZEN['besucher_10min'] or TAG['n'] >= GRENZEN['gesamt_tag']:
            BESUCHER[ip] = z
            return False
        z.append(jetzt); BESUCHER[ip] = z; TAG['n'] += 1
        return True

GRENZE_TEXT = {'de': f'Du hast in kurzer Zeit sehr viele Fragen gestellt. Damit alle Gäste eine Antwort bekommen, mache ich hier kurz Pause. Das Team ist direkt für dich da: {KONTAKT}.',
               'en': f'You have asked a great many questions in a short time. So that every guest gets an answer, I will pause here for a moment. The team is happy to help directly: {TEL} or {MAIL}.',
               'fr': f'Vous avez posé beaucoup de questions en peu de temps. Pour que chaque client reçoive une réponse, je fais une petite pause. L’équipe vous aide volontiers : {TEL} ou {MAIL}.'}
NICHTS = {'de': f'Dazu kann ich hier nichts sagen. Das Team hilft dir weiter: {KONTAKT}.',
          'en': f'I am afraid I cannot help with that here. The team will gladly assist: {TEL} or {MAIL}.',
          'fr': f'Je ne peux malheureusement pas vous renseigner ici. L’équipe vous aide volontiers : {TEL} ou {MAIL}.'}

def _api(koerper):
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages', data=json.dumps(koerper).encode('utf-8'), method='POST',
        headers={'content-type': 'application/json', 'x-api-key': os.environ['ANTHROPIC_API_KEY'], 'anthropic-version': '2023-06-01',
                 'anthropic-workspace-id': os.environ.get('ANTHROPIC_WORKSPACE_ID', '')})   # Nutzer-Schlüssel brauchen den Arbeitsbereich dazu
    with urllib.request.urlopen(req, timeout=55) as r:
        return json.load(r)


def frage(messages, mappe=False, heute='', sprache='de'):
    verlauf = []
    for m in messages[-HOECHSTENS_NACHRICHTEN:]:
        rolle = 'assistant' if m.get('role') == 'assistant' else 'user'
        inhalt = str(m.get('content', ''))[:HOECHSTENS_ZEICHEN].strip()
        if not inhalt:
            continue
        if verlauf and verlauf[-1]['role'] == rolle:   # zwei gleiche Rollen nacheinander nimmt die API nicht
            verlauf[-1]['content'] += '\n' + inhalt
        else:
            verlauf.append({'role': rolle, 'content': inhalt})
    if not verlauf or verlauf[0]['role'] != 'user':
        verlauf.insert(0, {'role': 'user', 'content': 'Hallo'})
    if verlauf[-1]['role'] != 'user':
        verlauf.append({'role': 'user', 'content': 'Mach bitte weiter.'})
    sp = sprache if sprache in SPRACHE else 'de'
    # Sprache der letzten Frage erkennen: Haiku antwortete auf englische Fragen sonst deutsch (10.10.2026)
    letzte = verlauf[-1]['content'].lower()
    worte = set(re.findall(r"[a-zäöüéèàç']+", letzte))
    if len(worte & {'the', 'is', 'are', 'do', 'does', 'can', 'we', 'you', 'there', 'what', 'how', 'when', 'where', 'our', 'my', 'have', 'bring', 'serve'}) >= 2: sp = 'en'
    elif len(worte & {'le', 'la', 'les', 'est', 'vous', 'nous', 'avez', 'quel', 'quelle', 'pour', 'chien', 'peut', 'comment', 'où', 'je', 'une', 'des'}) >= 2: sp = 'fr'
    antwort = _api({
        'model': MODELL, 'max_tokens': GRENZE, 'tools': WERKZEUGE,
        'system': [{'type': 'text', 'text': ANWEISUNG, 'cache_control': {'type': 'ephemeral'}},
                   {'type': 'text', 'text': (MAPPE if mappe else '') + f'\n\nWETTER:\n{wetter()}\n\nHeute ist {heute or time.strftime("%Y-%m-%d")}. Antworte auf {SPRACHE[sp]}.'}],
        'messages': verlauf})
    if antwort.get('stop_reason') == 'refusal':
        return {'text': NICHTS[sp], 'belegt': False, 'thema': 'abgelehnt'}
    text = ''.join(b.get('text', '') for b in antwort.get('content', []) if b.get('type') == 'text').strip()
    werk = {b.get('name'): b.get('input') for b in antwort.get('content', []) if b.get('type') == 'tool_use'}
    maske, lucke = werk.get('warteliste'), werk.get('nicht_belegt')
    # Ruft die Rezeption die Buchungsmaske auf, endet ihr Text dort. Fragte der Gast dazu noch etwas (Spa, Essen, Anreise), blieb das
    # unbeantwortet oder endete mit einem Doppelpunkt (10.10.2026). Darum ein zweiter, kurzer Schritt: die Rezeption sieht die Maske
    # als erledigt und ergänzt nur, was noch offen ist. Der Zwischenspeicher macht den zweiten Schritt billig.
    if maske and antwort.get('stop_reason') == 'tool_use':
        try:
            erg = _api({
                'model': MODELL, 'max_tokens': GRENZE, 'tools': WERKZEUGE,
                'system': [{'type': 'text', 'text': ANWEISUNG, 'cache_control': {'type': 'ephemeral'}},
                           {'type': 'text', 'text': (MAPPE if mappe else '') + f'\n\nWETTER:\n{wetter()}\n\nHeute ist {heute or time.strftime("%Y-%m-%d")}. Antworte auf {SPRACHE[sp]}.'}],
                'messages': verlauf + [{'role': 'assistant', 'content': antwort['content']},
                                       {'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': b['id'],
                                        'content': 'Der Weg zur Warteliste steht jetzt unter deiner Antwort. Ist eine Frage des Gastes (ausser freie Plätze) noch nicht beantwortet, '
                                                   'beantworte sie jetzt als höchstens fünf Punkte «- Stichwort: Angabe», nur mit Angaben, die so in WISSEN stehen. Keine Einleitung, keine Überschrift, kein Fettdruck, keine Frage am Schluss, die Maske nicht erwähnen. Ist alles beantwortet, antworte nur mit OK.'}
                                        for b in antwort['content'] if b.get('type') == 'tool_use']}]})
            mehr = ''.join(x.get('text', '') for x in erg.get('content', []) if x.get('type') == 'text').strip()
            if mehr and erg.get('stop_reason') != 'refusal' and mehr.rstrip('.').upper() != 'OK':
                text = (text + '\n' + mehr).strip()
        except Exception:  # noqa: BLE001
            pass
        if text.endswith(':'):   # nichts nachgekommen: den angefangenen Satz nicht stehen lassen
            text = text.rsplit('\n', 1)[0].strip() if '\n' in text else ''
    if not text:
        text = ({'de': 'Auf der Warteliste erfährst du den nächsten Abend zuerst.', 'en': 'On the waiting list you hear about the next evening first.',
                 'fr': 'Sur la liste d’attente, tu apprends la prochaine soirée en premier.'} if maske else NICHTS)[sp]
    n = antwort.get('usage', {})
    return {'text': text, 'maske': maske, 'belegt': not lucke, 'thema': (lucke or {}).get('thema', ''),
            'tokens': {'ein': n.get('input_tokens'), 'cache': n.get('cache_read_input_tokens'), 'aus': n.get('output_tokens')}}


def anfrage(mail, hinweis=''):
    antwort = _api({
        'model': MODELL, 'max_tokens': 3000 if 'haiku' in MODELL else 7000,   # Sonnet denkt mit: mit 3000 brach der Entwurf mitten in der Liste ab (10.10.2026)
       
        'system': [{'type': 'text', 'text': ANFRAGE, 'cache_control': {'type': 'ephemeral'}},
                   {'type': 'text', 'text': f'Heute ist {time.strftime("%Y-%m-%d")}.'}],
        'messages': [{'role': 'user', 'content': 'ANFRAGE:\n' + mail[:12000] + ('\n\nHINWEIS DES TEAMS:\n' + hinweis[:2000] if hinweis.strip() else '')}]})
    if antwort.get('stop_reason') == 'refusal':
        return {'text': '', 'fehler': 'Diese Anfrage lässt sich nicht automatisch beantworten. Bitte selbst schreiben.'}
    text = ''.join(b.get('text', '') for b in antwort.get('content', []) if b.get('type') == 'text').strip()
    mail_teil, _, team = text.partition('\n---')
    m = re.match(r'\s*Betreff:\s*(.+)\n', mail_teil)
    return {'betreff': m.group(1).strip() if m else '', 'text': (mail_teil[m.end():] if m else mail_teil).strip(), 'team': team.strip()}


ABDECKEN = [(re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'), '[E-Mail]'), (re.compile(r'(?:\+|00)?\d[\d\s/().-]{7,}\d'), '[Nummer]')]

def merke(host, daten):
    """Frage und Antwort an den Speicher fürs Studio (fragen.js). Mail-Adressen und Nummern der Gäste werden vorher abgedeckt.
    Scheitert das, bleibt die Antwort an den Gast davon unberührt."""
    geheim = os.environ.get('GAST_GEHEIM')
    if not geheim or not host:
        return
    for muster, ersatz in ABDECKEN:
        daten['frage'] = muster.sub(ersatz, daten.get('frage', ''))
    try:
        req = urllib.request.Request(f'https://{host}/api/fragen', data=json.dumps(daten).encode('utf-8'), method='POST',
                                     headers={'content-type': 'application/json', 'x-gast-geheim': geheim})
        urllib.request.urlopen(req, timeout=4).close()
    except Exception:  # noqa: BLE001
        pass


class handler(BaseHTTPRequestHandler):
    def _sende(self, code, daten):
        roh = json.dumps(daten, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(roh)))
        self.end_headers()
        self.wfile.write(roh)

    def _ip(self):
        return (self.headers.get('x-forwarded-for') or self.client_address[0] or '').split(',')[0].strip()

    def do_GET(self):
        self._sende(200, {'ok': True, 'modell': MODELL, 'wissen_zeichen': len(WISSEN), 'tal_zeichen': len(TAL), 'wetter': wetter()[:80]})

    def do_POST(self):
        try:
            host = (self.headers.get('host') or '').split(':')[0]
            herkunft = self.headers.get('origin') or self.headers.get('referer') or ''
            if herkunft and host and f'//{host}' not in herkunft:   # nur Aufrufe von der eigenen Seite
                return self._sende(403, {'fehler': 'nicht erlaubt'})
            n = int(self.headers.get('Content-Length') or 0)
            if n > 40000:
                return self._sende(413, {'fehler': 'zu lang'})
            daten = json.loads(self.rfile.read(n) or b'{}')
            if daten.get('modus') == 'anfrage':
                mail = str(daten.get('mail') or '').strip()
                if len(mail) < 20:
                    return self._sende(400, {'fehler': 'Bitte die Anfrage einfügen.'})
                if not erlaubt(self._ip(), 'anfrage'):
                    return self._sende(429, {'fehler': 'Für heute sind genug Entwürfe geschrieben. Morgen geht es weiter.'})
                return self._sende(200, anfrage(mail, str(daten.get('hinweis') or '')))
            messages = daten.get('messages') or []
            if not isinstance(messages, list):
                return self._sende(400, {'fehler': 'messages fehlt'})
            sp = str(daten.get('sprache') or 'de')[:2]
            sp = sp if sp in SPRACHE else 'de'
            if not erlaubt(self._ip()):
                return self._sende(200, {'text': GRENZE_TEXT[sp], 'grenze': True})
            a = frage(messages, mappe=bool(daten.get('mappe')), heute=str(daten.get('heute', ''))[:10], sprache=sp)
            letzte = next((str(m.get('content', '')) for m in reversed(messages) if m.get('role') == 'user'), '')
            merke(host, {'frage': letzte[:HOECHSTENS_ZEICHEN], 'antwort': a['text'][:2000], 'belegt': a.get('belegt', True), 'thema': a.get('thema', ''),
                         'mappe': bool(daten.get('mappe')), 'sprache': sp, 'buchung': bool(a.get('maske'))})
            self._sende(200, a)
        except urllib.error.HTTPError as e:
            self._sende(502, {'fehler': 'api', 'status': e.code, 'text': e.read().decode('utf-8', 'replace')[:400]})
        except Exception as e:  # noqa: BLE001
            self._sende(500, {'fehler': type(e).__name__, 'text': str(e)[:300]})

    def log_message(self, *a):   # Vercel schreibt die Zugriffe selbst
        pass
