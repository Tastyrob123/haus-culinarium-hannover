"""Probe-Antworten statt Claude (Robert 16.10.2026: «lokal bis zur Kostenrunde», keine bezahlten KI-Aufrufe in Prüfläufen).

Im Culinarium ist das der Standard: python3 _werkzeuge/reception/server.py 9084 (ohne RECEPTION_KI=1). Kopie aus dem Schäfli, dort aus dem Schlössli, Ruedihus, Carlton und Doldenhorn.
Dann ruft kein Teil von La Réception und vom Chat die KI auf und kein Schlüssel wird gelesen. Jede Stelle, die sonst Claude fragt, bekommt
eine Antwort in genau der Form, die Claude liefern würde, sichtbar als Probe beschriftet:
  Chat (gast.frage)        Text «Probe-Antwort ohne KI …»; nennt der Gast eine E-Mail oder Telefonnummer, ruft die Probe das Werkzeug «anfrage» auf
                           (so entsteht wie echt eine Anfrage im Eingang); enthält die Frage «lücke», meldet sie «nicht belegt».
  Brief (gast.anfrage)     «Betreff: …», Brief mit Anrede, offenen Stellen [in Klammern] und Gruss, darunter «---» mit Punkten fürs Team.
  Übersetzen               JSON mit betreff, text und verlauf in gleicher Länge.
  Wissen einlesen          Werkzeug «eintraege» mit einem Eintrag je Material.
"""
import json, re, time

BEREICH = 'Culinarium'



_CHAT = None


def _beleg(frage):
    """Antwort ohne KI aus dem belegten Wissen, wie der Chat auf der Website (_online/api/frage.py + steckbrief.json); None, wenn nicht ladbar.
    30.10.2026 (Oberchef, Tor K23): «Chat ausprobieren» zeigt keine «Probe/Demo»-Sätze mehr, sondern dieselben Antworten wie die Website."""
    global _CHAT
    try:
        if _CHAT is None:
            import importlib.util, json as _j, os as _o
            hier = _o.path.dirname(_o.path.abspath(__file__))
            spec = importlib.util.spec_from_file_location('probe_frage', _o.path.join(hier, '..', '..', '_online', 'api', 'frage.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
            sb = _j.load(open(_o.path.join(hier, 'steckbrief.json'), encoding='utf-8'))
            m.WISSEN = [{'fid': z['fid'], 'bereich': b['bereich'], 'gruppe': g['gruppe'], 'was': z['was'], 'angabe': z['angabe']}
                        for b in sb['bereiche'] for g in b['gruppen'] for z in g['zeilen']]
            _CHAT = m
        return _CHAT.antworte(frage)
    except Exception:
        return None

def _text(koerper):
    """Alles, was der Aufruf an Text mitschickt (System und Nachrichten), für die Erkennung der Stelle."""
    s = koerper.get('system')
    sys_t = s if isinstance(s, str) else ' '.join(b.get('text', '') for b in (s or []) if isinstance(b, dict))
    msg = []
    for m in koerper.get('messages') or []:
        c = m.get('content')
        if isinstance(c, str):
            msg.append(c)
        else:
            msg += [b.get('text', '') for b in c or [] if isinstance(b, dict) and b.get('type') == 'text']
    return sys_t, msg


def _antwort(text='', werkzeug=None):
    inhalt = [{'type': 'text', 'text': text}] if text else []
    if werkzeug:
        inhalt.append({'type': 'tool_use', 'id': 'toolu_probe', 'name': werkzeug[0], 'input': werkzeug[1]})
    return {'content': inhalt, 'stop_reason': 'tool_use' if werkzeug else 'end_turn', 'usage': {'input_tokens': 0, 'output_tokens': 0}}


def api(koerper):
    sys_t, msg = _text(koerper)
    werkzeuge = [w.get('name') for w in koerper.get('tools') or []]
    letzte = msg[-1] if msg else ''
    if 'eintraege' in werkzeuge:                                    # Wissen einlesen (gedaechtnis._auszug)
        m = re.search(r'BEREICH DES TEAMS: (.+)', letzte)
        bereich = (m.group(1).strip() if m else '') or BEREICH
        roh = ' '.join(msg)
        stueck = re.sub(r'\s+', ' ', roh.split('TEXT DES TEAMS:', 1)[-1] if 'TEXT DES TEAMS:' in roh else roh)[-220:].strip()
        return _antwort(werkzeug=('eintraege', {'grund': 'Aus dem Dokument übernommen', 'eintraege': [
            {'bereich': bereich, 'titel': (' '.join(stueck.split()[:6]) or 'Neuer Eintrag'), 'text': stueck, 'gueltig_bis': None}]}))
    if sys_t.startswith('Du übersetzt'):                             # reception.uebersetzen
        try:
            d = json.loads(letzte)
        except ValueError:
            d = {}
        return _antwort(json.dumps({'betreff': str(d.get('betreff', '')), 'text': str(d.get('text', '')),   # ohne KI: der Wortlaut des Gastes unverändert, ohne Probe-Beschriftung (Tor K23, 30.10.2026)
                                    'verlauf': [str(v) for v in d.get('verlauf') or []]}, ensure_ascii=False))
    if 'ANFRAGE:' in letzte:                                         # gast.anfrage (Brief)
        name = (re.search(r'Name:\s*(.+)', letzte) or re.search(r'"name":\s*"([^"]+)"', letzte))
        wer = name.group(1).strip() if name else 'Gast'
        allerg = (re.search(r'Allergien \(Formular\):\s*(.+)', letzte) or [None, ''])[1].strip()
        satz_al = f'Deine Angaben zu Allergien ({allerg}) gibt das Team an Rudi in der Küche weiter [Küche fragen].\n\n' if allerg and allerg != 'keine angegeben' else ''
        return _antwort(f'Betreff: Dein Platz an der Tafel\n\nHallo {wer},\n\n'
                        'danke für deine Nachricht und schön, dass du an einem unserer Abende dabei sein möchtest.\n\n'
                        'Der nächste Abend steht noch nicht fest [Termin eintragen]; sobald er feststeht, erfährst du es zuerst [Plätze prüfen].\n\n'
                        f'{satz_al}Damit wir deinen Platz in Ruhe vorbereiten können:\n- Freitag oder Samstag\n- wie viele Plätze\n\n'
                        'Bis bald an der Tafel\n\n[Name]\nCulinarium im Walk on the Wild Side'
                        '\n---\nGrundlage: Der Abend (Website)\nOffen: Termin, Plätze')
    # Chat (gast.frage, auch der zweite Schritt nach der Buchungsmaske)
    if any(isinstance(m.get('content'), list) and any(b.get('type') == 'tool_result' for b in m['content']) for m in koerper.get('messages') or []):
        return _antwort('OK')
    frage = letzte.strip()
    kontakt = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+|(?:\+|00)\d[\d\s]{7,}\d', frage)
    if kontakt and 'anfrage' in werkzeuge:
        name = re.search(r'(?:ich bin|mein name ist|name:|my name is|je suis)\s+([A-ZÄÖÜ][\w-]+(?:\s+[A-ZÄÖÜ][\w-]+)?)', frage, re.I)
        pers = re.search(r'(\d{1,3})\s*(?:personen|gäste|persons|people|personnes)', frage, re.I)
        art = 'feier' if re.search(r'feier|geburtstag|hochzeit|party|birthday|wedding|firmen|gruppe|privat', frage, re.I) else ('warteliste' if re.search(r'warteliste|nächste[nr]? abend|vormerk|platz|plätze|ticket', frage, re.I) else 'nachricht')
        return _antwort('Danke, deine Nachricht liegt jetzt beim Team. Es meldet sich persönlich bei dir.',
                        ('anfrage', {'art': art, 'name': name.group(1) if name else 'Gast', 'kontakt': kontakt.group(0), 'datum': None,
                                     'personen': int(pers.group(1)) if pers else None, 'anliegen': frage[:300]}))
    if 'lücke' in frage.lower() or 'luecke' in frage.lower():
        return _antwort('Dazu steht nichts in meinen Unterlagen. Ich gebe deine Frage gern ans Team weiter.', ('nicht_belegt', {'thema': frage[:80]}))
    if 'warteliste' in werkzeuge and re.search(r'warteliste|nächste[nr]? (abend|termin)|wann ist|platz (frei|buchen)|tickets?\b|next (evening|date)', frage, re.I):   # wie echt: der Weg zur Warteliste unter der Antwort
        b = _beleg(frage)
        return _antwort((b or {}).get('text') or 'Der nächste Termin steht noch nicht fest. Wer auf der Warteliste steht, erfährt ihn zuerst.',
                        ('warteliste', {'datum': None, 'uhrzeit': None, 'personen': None}))
    b = _beleg(frage)
    if b and b.get('belegt'):
        return _antwort(b['text'])
    return _antwort('Dazu steht nichts in meinen Unterlagen. Ich gebe deine Frage gern ans Team weiter.', ('nicht_belegt', {'thema': frage[:80]}))   # Uhrzeit: Prüfläufe erkennen daran, dass eine Antwort kam
