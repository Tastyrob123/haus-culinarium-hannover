"""Eigene Wege des Werkzeugs «gaeste» (La Réception · Der Gastgeber).  /api/x/gaeste/<haus>/<was>

Zwei Ablagen, beide NUR über den Speicher (unterbau/speicher.py), nie an ihm vorbei:
  gaeste           das Wissen des Hauses für den Chat: eingelesene Seiten und Unterlagen, was das Team nachgetragen hat,
                   Einstellungen. Geht den Weg Entwurf → Vorher, nachher → Veröffentlichen → Verlauf → Zurückholen.
                   Hier stehen NIE Daten von Gästen, damit der Verlauf keine enthält.
  gaeste-betrieb   was im Betrieb anfällt: Anfragen (Eingang), jede Frage an den Chat, Zähler für Grenzen und Kosten.
                   Wird sofort gespeichert (kein Veröffentlichen). Liegt im Entwurfs-Fach dieses Namens, weil der Speicher
                   dort die Kennung prüft: zwei gleichzeitige Schreiber überschreiben sich nicht (siehe _aendere).
                   Nur hier stehen Daten von Gästen. Löschen: einzeln, je Gast, und von selbst nach der Aufbewahrungsfrist.

GET   start         legt beim ersten Öffnen den Grundstand aus den Quellen des Hauses an (einlesen.py), meldet Lage und KI
GET   ueberblick    Zahlen für Leiste, Hinweis «Anfrage wartet» und später die Zentrale
GET   betrieb       Anfragen, Fragen, Kosten, Stand der KI
GET   stand         der Stand des Wissens (wie /api/stand, aber nie mitten in einem Schreiben gelesen)
POST  speichern     {daten, erwartet, wer}   Wissen als Entwurf, vorher geprüft; veraltete Kennung → 409
POST  veroeffentlichen {erwartet, wer, notiz} · zurueckholen {erwartet, fassung, wer} · verwerfen {erwartet, wer}
                    wie die allgemeinen Wege, aber nur, wenn der Entwurf noch der gesehene ist (sonst 409)
POST  einlesen      liest die Quellen neu und gibt sie zurück (gespeichert wird erst mit «speichern»)
POST  chat          {messages, sprache, gespraech, stand, herkunft, wer}   eine Frage an die Rezeption im Chat
POST  anfrage       {id, v, status | betreff, text, wer}   Anfrage: gelesen, erledigt, Antwortentwurf geändert
POST  entwurf       {id, hinweis, ohne_ki, wer}   Antwortentwurf schreiben lassen (KI) oder Gerüst ohne KI
POST  frage         {id, erledigt, wer}
POST  weg           {id, wer}   eine Anfrage (mit ihrem Gespräch) oder eine Frage endgültig löschen
POST  gast-suchen   {suche}     alles zu einem Gast finden
POST  gast-loeschen {ids, wer}  und endgültig löschen
POST  beispiele     {tun: laden | entfernen}   Beispiel-Anfragen des Hauses aus beispiele.json (Schild «Beispiel», nie als Gast gezählt)
POST  ki-pruefen    kleinster Aufruf der KI: stehen Schlüssel und Guthaben?
Verschickt wird nirgends etwas. Gebucht wird nirgends etwas.
"""
import copy
import datetime
import hashlib
import importlib.util
import json
import os
import random
import re
import sys
import threading
import time
import types
from pathlib import Path

HIER = Path(__file__).resolve().parent


def _lade(name):
    """Die Nachbardateien bei jedem Aufruf frisch, wie der Server es mit api.py tut."""
    spec = importlib.util.spec_from_file_location('gaeste_' + name, HIER / (name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ki = _lade('ki')
einlesen = _lade('einlesen')

W, WB = 'gaeste', 'gaeste-betrieb'
# Ein Schloss, das zwischen den Aufrufen bestehen bleibt (api.py wird je Aufruf frisch geladen): Schreiber desselben Servers
# stellen sich an. Gegen Schreiber von aussen schützt weiter die Kennung des Speichers (siehe _aendere).
_Z = sys.modules.setdefault('_gaeste_zustand', types.ModuleType('_gaeste_zustand'))
if not hasattr(_Z, 'rschloss'):
    _Z.rschloss = threading.RLock()


def _lesen(speicher, haus, werkzeug):
    """Liest einen Stand, während kein Schreiber dieses Werkzeugs schreibt. Der Speicher liest ohne Sperre: Zwischen den zwei
    Umbenennungen eines Schreibens fehlt die Datei einen Augenblick («fehlt, Sicherung liegt vor»). Dann kurz warten, noch einmal."""
    for versuch in range(8):
        try:
            with _Z.rschloss:
                return speicher.lesen(haus, werkzeug)
        except speicher.Beschaedigt:
            if versuch == 7:
                raise
            time.sleep(0.03)
ARTEN = ki.ARTEN
HOECHSTENS_FRAGEN = 5000        # mehr Fragen hält dieses eine Dokument nicht sinnvoll: die ältesten fallen dann heraus
THEMEN = [('Feiern und Tagen', r'hochzeit|feier|bankett|tagung|seminar|meeting|event|saal|wedding|conference|banquet|mariage|séminaire|gruppe'),
          ('Essen und Trinken', r'restaurant|essen|tisch|frühstück|mittag|abend.*essen|menü|karte|wein|bar\b|fondue|terrasse|table|breakfast|dinner|lunch|menu|wine|vegan|vegetar|allerg'),
          ('Zimmer und Buchung', r'zimmer|suite|buch|übernacht|nacht|lager|room|book|stay|night|chambre|réserv|frei\b|verfügbar|available|check.?in|check.?out|früh.*anreis|geöffnet|saison|offen'),
          ('Spa und Sauna', r'spa|sauna|bad\b|pool|schwimm|massage|behandlung|fitness|wellness|dampf|piscine|treatment'),
          ('Anreise und Parken', r'park|garage|anreise|bahnhof|shuttle|zug|auto|bus|strasse|flughafen|komme ich|arrive|arrival|station|train|airport|parking|venir|gare'),
          ('Ausflüge und Wetter', r'ausflug|wetter|wander|berg|see\b|schiff|schnee|ski|bahn|unternehmen|weather|hike|excursion|lake|mountain|météo|randonn'),
          ('Hund und Familie', r'hund|dog|chien|kind|kinder|baby|famil|child')]
_MAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
_NUMMER = re.compile(r'(?:\+|00)?\d[\d\s/().-]{7,}\d')


def _fehler(status, text, stichwort):
    return status, {'fehler': text, 'stichwort': stichwort}


def _jetzt():
    return datetime.datetime.now().astimezone().isoformat(timespec='seconds')


def _neu(vorsatz):
    return f'{vorsatz}{int(time.time() * 1000):x}{random.randrange(36 ** 4):04x}'


def thema_von(text):
    t = (text or '').lower()
    for name, muster in THEMEN:
        if re.search(muster, t):
            return name
    return 'Weitere Fragen'


# ---------------------------------------------------------------- Wissen (Ablage «gaeste»)
def _grundstand(speicher, haus):
    """Der Stand des Wissens. Gibt es noch keinen, wird er aus den Quellen des Hauses gelesen und abgelegt."""
    s = _lesen(speicher, haus, W)
    if s['live'] is not None:
        return s
    doc = einlesen.lies(haus)                     # ValueError, wenn Haus oder Quelle fehlen
    proben = doc.pop('probefragen', [])
    try:
        with _Z.rschloss:
            s = speicher.grundstand_setzen(haus, W, doc, 'einlesen')
    except speicher.Konflikt:                     # ein zweiter Aufruf war schneller
        return _lesen(speicher, haus, W)
    if proben:
        def tun(d):
            if not d['fragen']:
                for p in proben:
                    d['fragen'].append({'id': _neu('f'), 'zeit': p['zeit'], 'frage': p['frage'][:600], 'antwort': p['antwort'][:2000], 'belegt': True, 'thema': '',
                                        'gruppe': thema_von(p['frage']), 'sprache': 'de', 'buchung': False, 'anfrage': '', 'gespraech': '', 'herkunft': 'quelle',
                                        'erledigt': False, 'art': 'echt'})
        _aendere(speicher, haus, tun, 'einlesen')
    return s


def _pruefe_doc(d):
    """Was als Wissen gespeichert werden darf. Gibt den ersten Mangel als Satz zurück, sonst None."""
    if not isinstance(d, dict) or d.get('fassung') != 1:
        return 'Der Stand hat nicht die Form, die dieses Werkzeug kennt.'
    for k, typ in (('haus', dict), ('wissen', list), ('team', list), ('einstellungen', dict), ('vorlagen', dict), ('karten', list)):
        if not isinstance(d.get(k), typ):
            return f'Im Stand fehlt der Teil «{k}».'
    if len(d['team']) > 500:
        return 'Mehr als 500 nachgetragene Antworten fasst dieses Werkzeug nicht.'
    ids = set()
    for x in d['team']:
        if not isinstance(x, dict) or not re.match(r'^[a-z0-9-]{1,40}$', str(x.get('id', ''))) or x['id'] in ids:
            return 'Eine nachgetragene Antwort hat keine gültige Kennung.'
        ids.add(x['id'])
        f, a = str(x.get('frage', '')).strip(), str(x.get('antwort', '')).strip()
        if not (3 <= len(f) <= 400) or not (3 <= len(a) <= 2000):
            return 'Bitte Frage (3 bis 400 Zeichen) und Antwort (3 bis 2000 Zeichen) ausfüllen.'
        if any(not isinstance(x.get(k, ''), str) or len(x.get(k, '')) > 80 for k in ('zeit', 'wer', 'aus')):
            return 'Eine nachgetragene Antwort hat ungültige Angaben.'
    gross = 0
    for a in d['wissen']:
        if not isinstance(a, dict) or any(not isinstance(a.get(k), str) for k in ('id', 'art', 'titel', 'quelle', 'text')) or a['art'] not in ('seite', 'unterlage', 'tal'):
            return 'Ein Abschnitt des Wissens hat nicht die erwartete Form.'
        gross += len(a['text'])
    if gross > 2_000_000:
        return 'Das Wissen ist grösser als zwei Millionen Zeichen.'
    e = d['einstellungen']
    o = e.get('obergrenze_monat_usd')
    if o is not None and (isinstance(o, bool) or not isinstance(o, (int, float)) or not (0 < o <= 10000)):
        return 'Die Obergrenze je Monat ist eine Zahl zwischen 0 und 10 000, oder leer.'
    for k in ('besucher_10min', 'besucher_tag', 'gesamt_tag', 'anfrage_tag'):
        if isinstance(e.get(k), bool) or not isinstance(e.get(k), int) or not (1 <= e[k] <= 100000):
            return 'Eine Grenze für Anfragen ist keine ganze Zahl.'
    if isinstance(e.get('aufbewahrung_monate'), bool) or not isinstance(e.get('aufbewahrung_monate'), int) or not (1 <= e['aufbewahrung_monate'] <= 36):
        return 'Die Aufbewahrung ist eine Zahl von 1 bis 36 Monaten.'
    return None


# ---------------------------------------------------------------- Betrieb (Ablage «gaeste-betrieb»)
def _leer():
    return {'fassung': 1, 'anfragen': [], 'fragen': [], 'zaehler': {'tag': '', 'gesamt': 0, 'entwurf': 0, 'gespraeche': {}, 'monate': {}, 'ki': {'stand': '', 'text': '', 'zeit': ''}}}


def _betrieb(speicher, haus):
    s = _lesen(speicher, haus, WB)
    d = s['entwurf'] if isinstance(s['entwurf'], dict) else _leer()
    return d, s['kennung_entwurf']


def _aufraeumen(d, monate):
    """Aufbewahrungsfrist: Anfragen und Fragen, die älter sind, fallen bei jedem Schreiben heraus."""
    grenze = (datetime.date.today() - datetime.timedelta(days=int(30.44 * monate))).isoformat()
    for k in ('anfragen', 'fragen'):
        d[k] = [x for x in d[k] if str(x.get('zeit', ''))[:10] >= grenze]
    if len(d['fragen']) > HOECHSTENS_FRAGEN:
        d['fragen'] = d['fragen'][-HOECHSTENS_FRAGEN:]
    z = d['zaehler']
    heute = time.strftime('%Y-%m-%d')
    if z.get('tag') != heute:
        z.update(tag=heute, gesamt=0, entwurf=0, gespraeche={})
    z['monate'] = {m: v for m, v in sorted(z.get('monate', {}).items())[-24:]}


def _aendere(speicher, haus, tun, wer='', monate=12):
    """Liest, ändert, schreibt mit der gelesenen Kennung. Hat inzwischen jemand anderes geschrieben, noch einmal von vorn."""
    for versuch in range(30):
        with _Z.rschloss:
            d, kennung = _betrieb(speicher, haus)
            d = copy.deepcopy(d)
            _aufraeumen(d, monate)
            ergebnis = tun(d)
            try:
                speicher.entwurf_schreiben(haus, WB, d, kennung, wer)
                return ergebnis
            except speicher.Konflikt:
                pass
        time.sleep(0.01 * (versuch + 1) + random.random() * 0.03)
    raise speicher.Konflikt('Der Betriebsstand wird gerade von mehreren Seiten geändert. Bitte noch einmal.')


def _monat(z):
    return z['monate'].setdefault(time.strftime('%Y-%m'), {'aufrufe': 0, 'ein': 0, 'schreiben': 0, 'lesen': 0, 'aus': 0, 'usd': 0.0, 'ohne_preis': 0})


def _zaehle(d, tokens, modell):
    if not tokens or not any(tokens.values()):
        return
    m = _monat(d['zaehler'])
    m['aufrufe'] += 1
    for k in ('ein', 'schreiben', 'lesen', 'aus'):
        m[k] += int(tokens.get(k) or 0)
    usd = ki.kosten(modell, tokens)
    if usd is None:
        m['ohne_preis'] += 1
    else:
        m['usd'] = round(m['usd'] + usd, 6)


def _ki_stand(d, stand, text=''):
    d['zaehler']['ki'] = {'stand': stand, 'text': text, 'zeit': _jetzt()}


def _ki_lage(d, einst):
    """Die eine Stelle, an der steht, ob die KI antwortet."""
    art = ki.art()
    z = d['zaehler']
    monat = z.get('monate', {}).get(time.strftime('%Y-%m'), {})
    grenze = einst.get('obergrenze_monat_usd')
    lage = {'art': art, 'stand': 'ok', 'text': '', 'zeit': z.get('ki', {}).get('zeit', ''), 'preis_stand': ki.PREIS_STAND}
    if art == 'probe':
        lage.update(stand='probe', text='Die KI ist nicht angeschlossen. Der Chat antwortet mit festen Probe-Antworten, Antwortentwürfe kommen als Gerüst.')
    elif art == 'aus':
        lage.update(stand='kein-schluessel', text='Die KI ist nicht angeschlossen: Es ist kein Schlüssel hinterlegt. Eingang, Fragen und Wissen arbeiten weiter, Antwortentwürfe kommen als Gerüst.')
    elif grenze is not None and monat.get('usd', 0) >= grenze:
        lage.update(stand='obergrenze', text=f'Die Obergrenze für diesen Monat ist erreicht (USD {grenze:.2f}). Bis zum Monatswechsel antwortet der Chat mit dem Verweis an die Rezeption, Antwortentwürfe kommen als Gerüst.')
    elif z.get('ki', {}).get('stand') in ('guthaben-leer', 'schluessel-ungueltig'):
        lage.update(stand=z['ki']['stand'], text=z['ki']['text'] + ' Eingang, Fragen und Wissen arbeiten weiter, Antwortentwürfe kommen als Gerüst.')
    elif z.get('ki', {}).get('stand') in ('ueberlastet', 'fehler'):
        lage.update(stand=z['ki']['stand'], text=z['ki']['text'])
    return lage


def _ueberblick(d, einst):
    an, fr = d['anfragen'], d['fragen']
    neu = [a for a in an if a.get('status') == 'neu']
    gaeste = [f for f in fr if f.get('herkunft') == 'gast']
    return {'anfragen_neu': len(neu), 'anfragen_offen': sum(1 for a in an if a.get('status') != 'erledigt'), 'anfragen_gesamt': len(an),
            'fragen_gesamt': len(fr), 'fragen_gaeste': len(gaeste), 'ohne_antwort': sum(1 for f in fr if f.get('belegt') is False and not f.get('erledigt')),
            'letzte_frage': max((f['zeit'] for f in fr), default=''),
            'beispiele': sum(1 for a in an if a.get('herkunft') == 'beispiel'),
            'wartet': [{'id': a['id'], 'art': a.get('art'), 'name': a.get('name', ''), 'zeit': a.get('zeit', '')} for a in sorted(neu, key=lambda a: a.get('zeit', ''))[:5]],
            'ki': _ki_lage(d, einst)}


def _oeffentlich(d):
    """Der Betriebsstand für die Oberfläche: ohne die Zähler je Gespräch."""
    z = d['zaehler']
    return {'anfragen': sorted(d['anfragen'], key=lambda a: a.get('zeit', ''), reverse=True),
            'fragen': sorted(d['fragen'], key=lambda f: f.get('zeit', ''), reverse=True),
            'kosten': {'monat': time.strftime('%Y-%m'), 'monate': z.get('monate', {}), 'heute': {'tag': z.get('tag', ''), 'fragen': z.get('gesamt', 0), 'entwuerfe': z.get('entwurf', 0)}}}


# ---------------------------------------------------------------- Chat
def _chat(speicher, haus, k):
    messages = k.get('messages')
    if not isinstance(messages, list) or not messages or len(messages) > 40:
        return _fehler(400, 'Es fehlt die Frage.', 'anfrage-unvollstaendig')
    messages = [{'role': 'assistant' if m.get('role') == 'assistant' else 'user', 'content': str(m.get('content', ''))[:ki.HOECHSTENS_ZEICHEN]} for m in messages if isinstance(m, dict)]
    letzte = next((m['content'] for m in reversed(messages) if m['role'] == 'user'), '').strip()
    if len(letzte) < 2:
        return _fehler(400, 'Es fehlt die Frage.', 'anfrage-unvollstaendig')
    herkunft = 'probe' if k.get('herkunft') == 'probe' else 'gast'
    gespraech = re.sub(r'[^a-z0-9]', '', str(k.get('gespraech', '')).lower())[:24] or _neu('g')
    s = _grundstand(speicher, haus)
    mit_entwurf = herkunft == 'probe' and k.get('stand') == 'entwurf' and s['entwurf'] is not None
    doc = s['entwurf'] if mit_entwurf else s['live']
    einst = doc.get('einstellungen') or {}
    sp = str(k.get('sprache') or 'de')[:2]

    def einlass(d):                              # Grenzen: je Gespräch und gesamt je Tag
        z = d['zaehler']
        jetzt = time.time()
        g = [t for t in z['gespraeche'].get(gespraech, []) if jetzt - t < 86400]
        if z['gesamt'] >= einst.get('gesamt_tag', 2000) or len(g) >= einst.get('besucher_tag', 80) or len([t for t in g if jetzt - t < 600]) >= einst.get('besucher_10min', 20):
            return False
        g.append(round(jetzt))
        z['gespraeche'][gespraech] = g
        z['gesamt'] += 1
        return True

    monate = einst.get('aufbewahrung_monate', 12)
    if not _aendere(speicher, haus, einlass, 'chat', monate):
        return 200, {'text': ki.grenze_text(doc, sp), 'grenze': True, 'belegt': None}
    d0, _ = _betrieb(speicher, haus)
    lage = _ki_lage(d0, einst)
    a, stand, stand_text = None, 'ok', ''
    if lage['stand'] == 'probe':
        a = ki.probe_frage(doc, messages, sp)
    elif lage['art'] == 'echt' and lage['stand'] != 'obergrenze':
        try:
            a = ki.frage(doc, messages, sp, str(k.get('heute', ''))[:10])
        except ki.KiFehler as f:
            stand, stand_text = f.stand, f.text
    ausfall = a is None
    if ausfall:
        a = {'text': ki.ruhe_text(doc, ki.sprache_von(doc, sp, letzte)[0]), 'belegt': None, 'thema': '', 'buchung': False, 'anfrage': None,
             'sprache': ki.sprache_von(doc, sp, letzte)[0], 'tokens': {}, 'modell': ''}
    frage_text = letzte
    antwort_text = a['text']
    for muster in (_MAIL, _NUMMER):                # Adressen und Nummern der Gäste stehen nie im Protokoll der Fragen
        for treffer in set(muster.findall(letzte)):
            antwort_text = antwort_text.replace(treffer, '[Kontakt]')
        frage_text = muster.sub('[E-Mail]' if muster is _MAIL else '[Nummer]', frage_text)
    fid = _neu('f')

    def ablegen(d):
        aid = ''
        e = a.get('anfrage')
        if e:
            verlauf = [{'rolle': m['role'], 'text': m['content'][:600]} for m in messages[-8:]] + [{'rolle': 'assistant', 'text': a['text'][:1200]}]
            alt = next((x for x in d['anfragen'] if x.get('gespraech') == gespraech and x.get('art') == e['art'] and x.get('status') != 'erledigt'), None)
            if alt:                                # der Gast ergänzt Datum oder Personen: dieselbe Anfrage, nicht eine zweite
                for feld in ('name', 'kontakt', 'datum', 'personen', 'anliegen'):
                    if e.get(feld) not in (None, ''):
                        alt[feld] = e[feld]
                alt.update(verlauf=verlauf, entwurf=None, geaendert=_jetzt(), v=alt.get('v', 0) + 1)
                aid = alt['id']
            else:
                aid = _neu('a')
                d['anfragen'].append({'id': aid, 'v': 1, 'zeit': _jetzt(), **e, 'sprache': a['sprache'], 'gespraech': gespraech, 'verlauf': verlauf,
                                      'status': 'neu', 'entwurf': None, 'herkunft': herkunft})
        d['fragen'].append({'id': fid, 'zeit': _jetzt(), 'frage': frage_text[:600], 'antwort': antwort_text[:2000], 'belegt': a['belegt'], 'thema': a.get('thema', ''),
                            'gruppe': thema_von(frage_text), 'sprache': a['sprache'], 'buchung': bool(a.get('buchung')), 'anfrage': aid, 'gespraech': gespraech,
                            'herkunft': herkunft, 'erledigt': False, 'art': 'ausfall' if ausfall else ('probe' if lage['stand'] == 'probe' else 'echt'),
                            'mit_entwurf': mit_entwurf})
        _zaehle(d, a.get('tokens'), a.get('modell'))
        if lage['art'] == 'echt' and lage['stand'] != 'obergrenze':
            _ki_stand(d, stand, stand_text)
        return aid, _ueberblick(d, einst)

    aid, ue = _aendere(speicher, haus, ablegen, 'chat', monate)
    return 200, {'text': a['text'], 'belegt': a['belegt'], 'thema': a.get('thema', ''), 'buchung': (doc['haus'].get('buchung') or 'offen') if a.get('buchung') else '',
                 'anfrage': aid, 'sprache': a['sprache'], 'frage_id': fid, 'gespraech': gespraech, 'ausfall': ausfall, 'mit_entwurf': mit_entwurf, 'ueberblick': ue}


# ---------------------------------------------------------------- Antwortentwurf
def _entwurf(speicher, haus, k):
    s = _grundstand(speicher, haus)
    doc = s['live']
    einst = doc.get('einstellungen') or {}
    monate = einst.get('aufbewahrung_monate', 12)
    d0, _ = _betrieb(speicher, haus)
    a = next((x for x in d0['anfragen'] if x['id'] == k.get('id')), None)
    if not a:
        return _fehler(404, 'Diese Anfrage gibt es nicht mehr.', 'anfrage-fehlt')
    lage = _ki_lage(d0, einst)
    e, stand, stand_text, hinweis = None, 'ok', '', ''
    mit_ki = not k.get('ohne_ki') and lage['art'] == 'echt' and lage['stand'] != 'obergrenze'
    if mit_ki:
        def einlass(d):
            if d['zaehler']['entwurf'] >= einst.get('anfrage_tag', 60):
                return False
            d['zaehler']['entwurf'] += 1
            return True
        if not _aendere(speicher, haus, einlass, k.get('wer', ''), monate):
            mit_ki, hinweis = False, 'Für heute sind genug Entwürfe von der KI geschrieben. Dies ist das Gerüst ohne KI.'
        else:
            try:
                e = ki.entwurf(doc, a, str(k.get('hinweis') or '')[:2000])
            except ki.KiFehler as f:
                stand, stand_text = f.stand, f.text
                hinweis = f.text + ' Dies ist das Gerüst ohne KI.'
    if e is None:
        e = ki.entwurf_ohne_ki(doc, a)
    tokens, modell = e.pop('tokens'), e.pop('modell')
    e['zeit'] = _jetzt()

    def tun(d):
        x = next((y for y in d['anfragen'] if y['id'] == a['id']), None)
        if not x:
            return None
        x['entwurf'] = e
        x['v'] = x.get('v', 0) + 1
        if x.get('status') == 'neu':
            x['status'] = 'gelesen'
        _zaehle(d, tokens, modell)
        if mit_ki:
            _ki_stand(d, 'ok' if stand == 'abgelehnt' else stand, '' if stand == 'abgelehnt' else stand_text)
        return copy.deepcopy(x), _ueberblick(d, einst)

    r = _aendere(speicher, haus, tun, k.get('wer', ''), monate)
    if not r:
        return _fehler(404, 'Diese Anfrage gibt es nicht mehr.', 'anfrage-fehlt')
    return 200, {'anfrage': r[0], 'hinweis': hinweis, 'ueberblick': r[1]}


# ---------------------------------------------------------------- Löschen
def _loesche(speicher, haus, ids, wer, monate):
    """Löscht Anfragen samt den Fragen ihres Gesprächs und einzelne Fragen. Danach ein zweites Schreiben,
    damit auch die Sicherung des Speichers (Stand vor der letzten Änderung) die Daten nicht mehr enthält."""
    ids = set(ids)

    def tun(d):
        gespraeche = {a.get('gespraech') for a in d['anfragen'] if a['id'] in ids and a.get('gespraech')}
        vorher = len(d['anfragen']) + len(d['fragen'])
        d['anfragen'] = [a for a in d['anfragen'] if a['id'] not in ids]
        d['fragen'] = [f for f in d['fragen'] if f['id'] not in ids and not (f.get('gespraech') in gespraeche and f.get('gespraech'))]
        return vorher - len(d['anfragen']) - len(d['fragen'])

    n = _aendere(speicher, haus, tun, wer, monate)
    _aendere(speicher, haus, lambda d: d.update(geloescht_zuletzt=_jetzt()), wer, monate)
    return n


def _treffer(d, suche):
    s = suche.lower()
    eng = re.sub(r'[\s/().-]', '', s)
    aus = []
    for a in d['anfragen']:
        heu = ' '.join([a.get('name', ''), a.get('kontakt', ''), a.get('anliegen', '')] + [v.get('text', '') for v in a.get('verlauf') or []]).lower()
        if s in heu or (len(eng) >= 5 and eng in re.sub(r'[\s/().-]', '', heu)):
            aus.append({'id': a['id'], 'art': 'anfrage', 'zeit': a.get('zeit', ''), 'titel': f"{ARTEN.get(a.get('art'), 'Anfrage')} · {a.get('name') or 'ohne Namen'}", 'text': a.get('anliegen', '')[:160]})
    schon = {a['gespraech'] for a in d['anfragen'] if a['id'] in {x['id'] for x in aus} and a.get('gespraech')}
    for f in d['fragen']:
        if f.get('gespraech') in schon and f.get('gespraech'):
            continue                                # fällt mit der Anfrage
        if s in (f.get('frage', '') + ' ' + f.get('antwort', '')).lower():
            aus.append({'id': f['id'], 'art': 'frage', 'zeit': f.get('zeit', ''), 'titel': 'Frage an den Chat', 'text': f.get('frage', '')[:160]})
    return aus


def _beispiele(haus):
    try:
        return json.loads((HIER / 'beispiele.json').read_text(encoding='utf-8')).get(haus) or []
    except (OSError, ValueError):
        return []


def _beispiele_laden(speicher, haus, doc, wer, monate):
    """Legt die Beispiel-Anfragen des Hauses in den Eingang (Schild «Beispiel», Herkunft «beispiel», nie als Gast gezählt)."""
    liste = _beispiele(haus)
    jetzt = datetime.datetime.now().astimezone()

    def tun(d):
        da = {a['id'] for a in d['anfragen']}
        n = 0
        for b in liste:
            if b['id'] in da:
                continue
            zeit = (jetzt - datetime.timedelta(minutes=b.get('vor_minuten', 0))).isoformat(timespec='seconds')
            verlauf = [{'rolle': r, 'text': x} for r, x in b.get('verlauf', [])]
            entwurf = None
            p = b.get('aus_projekt')
            if p:                                   # Anfrage und Antwortentwurf, die im Projekt des Hauses schon liegen (nur lesen)
                q = (HIER.parent.parent / 'haeuser' / haus / 'haus.json')
                try:
                    quelle = Path(os.path.expanduser(json.loads(q.read_text(encoding='utf-8'))['quelle']))
                    paar = json.loads((quelle / p['datei']).resolve().read_text(encoding='utf-8'))[p['schluessel']]
                    verlauf = [{'rolle': 'user', 'text': str(paar[0])[:600]}] + verlauf
                    roh = paar[1]
                    sauber = lambda s: re.sub(r'\*\*(.+?)\*\*', r'\1', str(s or '')).strip()
                    entwurf = {'betreff': sauber(roh.get('betreff')), 'text': sauber(roh.get('text')), 'team': sauber(roh.get('team')), 'vorlage': '', 'absender': ki.absender(doc, b['art']),
                               'art': 'probelauf', 'zeit': zeit, 'hinweis': p.get('hinweis', '')}
                except (OSError, ValueError, KeyError, IndexError, TypeError):
                    entwurf = None
            g = 'bsp' + re.sub(r'[^a-z0-9]', '', b['id'])
            d['anfragen'].append({'id': b['id'], 'v': 1, 'zeit': zeit, 'art': b['art'], 'name': b['name'], 'kontakt': b['kontakt'], 'datum': b.get('datum', ''), 'personen': b.get('personen'),
                                  'anliegen': b['anliegen'], 'sprache': b.get('sprache', 'de'), 'gespraech': g, 'verlauf': verlauf, 'status': b.get('status', 'neu'), 'entwurf': entwurf, 'herkunft': 'beispiel'})
            erste = next((v['text'] for v in verlauf if v['rolle'] == 'user'), b['anliegen'])
            for muster, ersatz in ((_MAIL, '[E-Mail]'), (_NUMMER, '[Nummer]')):
                erste = muster.sub(ersatz, erste)
            d['fragen'].append({'id': 'f-' + b['id'], 'zeit': zeit, 'frage': erste[:600], 'antwort': (verlauf[-1]['text'] if verlauf else '')[:2000], 'belegt': True, 'thema': '', 'gruppe': thema_von(erste),
                                'sprache': b.get('sprache', 'de'), 'buchung': False, 'anfrage': b['id'], 'gespraech': g, 'herkunft': 'beispiel', 'erledigt': False, 'art': 'beispiel'})
            n += 1
        return n
    return _aendere(speicher, haus, tun, wer, monate)


def _kleid(haus):
    """Die Bilder des Hauses für die Bühne (kleid/<haus>/kleid.json, von kleid.py angelegt). Fehlen sie, gibt es keine."""
    p = HIER / 'kleid' / haus / 'kleid.json'
    try:
        k = json.loads(p.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None
    return {x: k.get(x) for x in ('kulisse', 'kacheln', 'tapete', 'zeichen', 'schriftzug')}


# ---------------------------------------------------------------- Wege
def bearbeite(methode, rest, daten, speicher):
    if len(rest) != 2:
        return _fehler(404, 'Weg unbekannt', 'weg-unbekannt')
    haus, was = rest
    k = daten if isinstance(daten, dict) else {}
    wer = str(k.get('wer') or '')[:80]
    if not re.match(r'^[a-z0-9][a-z0-9-]{0,40}$', haus) or not (HIER.parent.parent / 'haeuser' / haus / 'haus.json').exists():
        return _fehler(404, 'Dieses Haus gibt es nicht.', 'haus-unbekannt')
    try:
        s = _grundstand(speicher, haus)
    except ValueError as f:
        return _fehler(502, str(f), 'quelle-fehlt')
    einst = (s['live'] or {}).get('einstellungen') or {}
    monate = einst.get('aufbewahrung_monate', 12)

    if methode == 'GET':
        d, kennung = _betrieb(speicher, haus)
        if was == 'start':
            return 200, {'ok': True, 'haus': s['live']['haus'].get('name', ''), 'ueberblick': _ueberblick(d, einst), 'kleid': _kleid(haus), 'beispiele_da': bool(_beispiele(haus))}
        if was == 'ueberblick':
            return 200, _ueberblick(d, einst)
        if was == 'stand':
            return 200, s
        if was == 'betrieb':
            return 200, {**_oeffentlich(d), 'ueberblick': _ueberblick(d, einst), 'modell': ki.modell(s['live']),
                         'preise': ki.PREISE.get(ki.modell(s['live'])), 'preis_stand': ki.PREIS_STAND}
        return _fehler(404, 'Weg unbekannt', 'weg-unbekannt')
    if methode != 'POST':
        return _fehler(405, 'Nicht erlaubt', 'nicht-erlaubt')

    if was == 'speichern':
        mangel = _pruefe_doc(k.get('daten'))
        if mangel:
            return _fehler(400, mangel, 'eingabe')
        with _Z.rschloss:
            return 200, speicher.entwurf_schreiben(haus, W, k['daten'], k.get('erwartet'), wer)      # veraltete Kennung → Konflikt → 409
    if was in ('veroeffentlichen', 'zurueckholen', 'verwerfen'):
        # Wie die allgemeinen Wege des Speichers, aber mit der Kennung des Entwurfs, den der Mensch gesehen hat:
        # niemand veröffentlicht, ersetzt oder verwirft etwas, das inzwischen jemand anderes geändert hat.
        with _Z.rschloss:
            jetzt = _lesen(speicher, haus, W)
            if k.get('erwartet') != jetzt['kennung_entwurf']:
                return 409, {'fehler': 'Der Entwurf wurde inzwischen von jemand anderem geändert.', 'stichwort': 'konflikt'}
            if was == 'veroeffentlichen':
                return 200, speicher.veroeffentlichen(haus, W, wer, str(k.get('notiz') or '')[:200])
            if was == 'zurueckholen':
                return 200, speicher.zurueckholen(haus, W, str(k.get('fassung') or ''), wer)
            return 200, speicher.entwurf_verwerfen(haus, W, wer)
    if was == 'einlesen':
        try:
            neu = einlesen.lies(haus)
        except ValueError as f:
            return _fehler(502, str(f), 'quelle-fehlt')
        neu.pop('probefragen', None)
        return 200, {k2: neu.get(k2) for k2 in ('haus', 'karten', 'muster', 'wissen', 'vorlagen', 'tal_hinweis', 'eingelesen')}
    if was == 'chat':
        return _chat(speicher, haus, k)
    if was == 'entwurf':
        return _entwurf(speicher, haus, k)
    if was == 'anfrage':
        def tun(d):
            a = next((x for x in d['anfragen'] if x['id'] == k.get('id')), None)
            if not a:
                return 'fehlt', None
            if k.get('v') is not None and k.get('v') != a.get('v', 0):
                return 'konflikt', copy.deepcopy(a)
            if k.get('status') in ('neu', 'gelesen', 'erledigt'):
                a['status'] = k['status']
            if isinstance(k.get('text'), str) and a.get('entwurf'):
                a['entwurf']['text'] = k['text'][:12000]
                if isinstance(k.get('betreff'), str):
                    a['entwurf']['betreff'] = k['betreff'][:300]
                a['entwurf']['geaendert'] = _jetzt()
                a['entwurf']['geaendert_von'] = wer
            a['v'] = a.get('v', 0) + 1
            return 'ok', (copy.deepcopy(a), _ueberblick(d, einst))
        wie, r = _aendere(speicher, haus, tun, wer, monate)
        if wie == 'fehlt':
            return _fehler(404, 'Diese Anfrage gibt es nicht mehr.', 'anfrage-fehlt')
        if wie == 'konflikt':
            return 409, {'fehler': 'Diese Anfrage wurde inzwischen von jemand anderem geändert.', 'stichwort': 'konflikt', 'anfrage': r}
        return 200, {'anfrage': r[0], 'ueberblick': r[1]}
    if was == 'frage':
        def tun(d):
            f = next((x for x in d['fragen'] if x['id'] == k.get('id')), None)
            if not f:
                return None
            f['erledigt'] = bool(k.get('erledigt'))
            return _ueberblick(d, einst)
        ue = _aendere(speicher, haus, tun, wer, monate)
        return (200, {'ok': True, 'ueberblick': ue}) if ue else _fehler(404, 'Diese Frage gibt es nicht mehr.', 'frage-fehlt')
    if was == 'weg':
        n = _loesche(speicher, haus, [str(k.get('id', ''))], wer, monate)
        if not n:
            return _fehler(404, 'Dieser Eintrag existiert nicht mehr.', 'eintrag-fehlt')
        return 200, {'geloescht': n, 'ueberblick': _ueberblick(_betrieb(speicher, haus)[0], einst)}
    if was == 'gast-suchen':
        suche = str(k.get('suche') or '').strip()
        if len(suche) < 3:
            return _fehler(400, 'Bitte mindestens drei Zeichen eingeben: Name, E-Mail oder Telefonnummer.', 'eingabe')
        return 200, {'treffer': _treffer(_betrieb(speicher, haus)[0], suche)}
    if was == 'gast-loeschen':
        ids = [str(x) for x in (k.get('ids') or []) if isinstance(x, str)][:500]
        if not ids:
            return _fehler(400, 'Nichts ausgewählt.', 'eingabe')
        n = _loesche(speicher, haus, ids, wer, monate)
        return 200, {'geloescht': n, 'ueberblick': _ueberblick(_betrieb(speicher, haus)[0], einst)}
    if was == 'beispiele':
        if k.get('tun') == 'entfernen':
            d = _betrieb(speicher, haus)[0]
            ids = [a['id'] for a in d['anfragen'] if a.get('herkunft') == 'beispiel'] + [f['id'] for f in d['fragen'] if f.get('herkunft') == 'beispiel']
            n = _loesche(speicher, haus, ids, wer, monate) if ids else 0
        else:
            n = _beispiele_laden(speicher, haus, s['live'], wer, monate)
        return 200, {'anzahl': n, 'ueberblick': _ueberblick(_betrieb(speicher, haus)[0], einst)}
    if was == 'ki-pruefen':
        if ki.art() != 'echt':
            return 200, {'ueberblick': _ueberblick(_betrieb(speicher, haus)[0], einst)}
        stand, text, tokens = 'ok', '', {}
        try:
            tokens = ki.pruefe()
        except ki.KiFehler as f:
            stand, text = f.stand, f.text

        def tun(d):
            _zaehle(d, tokens, ki.MODELL_VORGABE)
            _ki_stand(d, stand, text)
            return _ueberblick(d, einst)
        return 200, {'ueberblick': _aendere(speicher, haus, tun, wer, monate)}
    return _fehler(404, 'Weg unbekannt', 'weg-unbekannt')
