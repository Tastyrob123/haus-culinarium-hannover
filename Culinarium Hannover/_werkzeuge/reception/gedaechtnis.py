"""Das weiss der Chat · La Réception, Culinarium Hannover (28.10.2026, Kopie aus der Taverne zum Schäfli, dort aus dem Schlössli und Ruedihus) (Robert 16.10.2026: «so eine Art Gehirn, was man sich anschauen kann»).

Alles, was die Rezeption im Chat über das Haus und die Umgebung weiss, an einem Ort, für das Team lesbar und korrigierbar:
  Grundlage    gast_wissen.txt (Seiten und Unterlagen der Website des Hauses, _bau/culinarium_wissen.py) und gast_umgebung.txt (Lage, Anreise, Geschichte),
               in Abschnitte zerlegt (Seite → Überschrift; Unterlagen ohne Überschriften nach Seiten der PDF). Diese Dateien bleiben
               unverändert, das Team legt Berichtigungen darüber: einen Abschnitt neu fassen, ausblenden oder zurück auf die Website.
  Ergänzt      Einträge des Teams (Bereich, Titel, Text, gültig bis) und Einträge aus Links (Veranstaltung, Seite eines Anbieters):
               die Seite wird im Hintergrund gelesen, Claude zieht nur heraus, was dort steht, die Einträge gelten sofort und sind
               als «aus Link» mit Datum markiert. Ein Link lässt sich neu einlesen, dann ersetzen die neuen Einträge die alten.
  Verlauf      Jede Änderung mit Zeit, damit das Haus sieht, was wann dazukam.

Wirkung im Chat: anweisung(basis) setzt die Berichtigungen an genau der Stelle von WISSEN bzw. TALWISSEN ein (nach Lage im Text, nicht per
Suchen, weil gleiche Abschnitte mehrfach vorkommen) und hängt die Ergänzungen als eigenen Block an, der bei Widerspruch vorgeht.
Abgelaufene Einträge (gültig bis vor heute) gehen nicht mehr in den Chat, bleiben aber sichtbar.

Speicher: _gast/daten/gedaechtnis/ (korrekturen.json · eintraege.json · links.json · verlauf.json). Nur lokal (serve.py), Stand 16.10.2026."""
import base64, datetime, hashlib, html, ipaddress, json, os, re, shutil, socket, threading, time, urllib.error, urllib.parse, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website')   # die Website des Culinarium (Überschriften der Seiten)
WISSEN_DIR = os.path.join(HIER, 'gast')    # gast_wissen.txt und gast_umgebung.txt (_bau/culinarium_wissen.py)
DATEN = os.path.join(os.environ.get('RECEPTION_DATEN') or os.environ.get('REZEPTION_DATEN') or os.path.join(HIER, 'daten'), 'gedaechtnis')
SCHLOSS = threading.RLock()
QUELLEN = (('gast_wissen.txt', 'WISSEN'), ('gast_umgebung.txt', 'TALWISSEN'))
BEREICHE = ['Culinarium', 'Der Abend & Warteliste', 'Tickets & Preise', 'Drinks & Küche', 'Kontakt', 'Das Haus (Bar)', 'Team', 'Der Weg', 'Dirty Chicken',
            'Alle Abende', 'Veranstaltungen', 'Fragen & Antworten']
# Seite bzw. Teil des Wissens → Bereich (Kopfzeile im Wissen: «=== Seite: … (Website: x.html; …) ===», in der Umgebung «=== Tickets … ===», «=== Kontakt … ===», «=== Lage … ===»)
SEITE_BEREICH = [(r'Website: index\.html', 'Culinarium'), (r'Website: abend\.html', 'Der Abend & Warteliste'), (r'Website: abende\.html', 'Alle Abende'),
                 (r'Website: bar\.html', 'Das Haus (Bar)'), (r'Website: leute\.html', 'Team'), (r'Website: weg\.html', 'Der Weg'),
                 (r'Website: dirty-chicken\.html', 'Dirty Chicken'), (r'Fuss jeder Seite', 'Culinarium'), (r'Tickets für einen Abend', 'Tickets & Preise'),
                 (r'^Kontakt', 'Kontakt'), (r'^Lage', 'Der Weg'), (r'^Talwissen', 'Der Weg')]
UNTERLAGE_NAME = {}
PREISZEILE = re.compile(r'^\s*Alle Preise in EUR', re.I)


# ---------------------------------------------------------------- Dateien
def _pfad(n):
    return os.path.join(DATEN, n)

def _lies(n, standard):
    try:
        return json.load(open(_pfad(n), encoding='utf-8'))
    except OSError:
        return standard
    except ValueError:              # beschädigt: letzte gute Fassung, sonst laut melden statt still leer (das nächste Schreiben würde alles löschen)
        try:
            return json.load(open(_pfad(n) + '.gut', encoding='utf-8'))
        except (OSError, ValueError):
            raise ValueError(f'DATEI · Die Ablage «{n}» ist beschädigt und hat keine gute Sicherung. Bitte die Prüfung öffnen.')

def _schreib(n, d):
    os.makedirs(DATEN, exist_ok=True)
    tmp = _pfad(n) + '.neu'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    try:
        json.load(open(_pfad(n), encoding='utf-8')); shutil.copy2(_pfad(n), _pfad(n) + '.gut')
    except (OSError, ValueError):
        pass
    os.replace(tmp, _pfad(n))

def _jetzt():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo('Europe/Zurich')).isoformat(timespec='seconds')
    except Exception:  # noqa: BLE001
        return datetime.datetime.now().astimezone().isoformat(timespec='seconds')

def _heute():
    return _jetzt()[:10]

def _merke(art, titel, bereich='', ref='', wer='Team', mehr=''):
    with SCHLOSS:
        v = _lies('verlauf.json', [])
        v.append({'zeit': _jetzt(), 'art': art, 'titel': titel[:160], 'bereich': bereich, 'ref': ref, 'wer': wer, 'mehr': mehr[:300]})
        _schreib('verlauf.json', v[-2000:])


# ---------------------------------------------------------------- Grundlage in Abschnitte zerlegen
def _schoen(t):
    """Überschriften aus dem Seitenbau: «Zimmer& Suiten.» → «Zimmer & Suiten», «Aare.Das» → «Aare. Das»."""
    t = re.sub(r'(\S)&', r'\1 &', t.strip())
    t = re.sub(r'([a-zäöü»])\.([A-ZÄÖÜ«])', r'\1. \2', t)
    return t.rstrip('.').strip() or '…'

_KOEPFE = {}

def _koepfe():
    """Überschriften der gebauten Seiten mit Wortgrenzen ({ohne Leerzeichen: Überschrift}); im Wissen sind die Zeilen der Überschrift zusammengeklebt."""
    if _KOEPFE:
        return _KOEPFE
    web = WEB
    for f in os.listdir(web):
        if not f.endswith('.html'):
            continue
        try:
            s = open(os.path.join(web, f), encoding='utf-8').read()
        except OSError:
            continue
        for h in re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', s, flags=re.S):
            t = re.sub(r'<span class="z"[^>]*>|<br\s*/?>', ' ', h)
            t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', t))).strip()
            if 2 < len(t) < 160:
                _KOEPFE.setdefault(re.sub(r'\s', '', t), t)
    _KOEPFE.setdefault('', '')
    return _KOEPFE

def _kopf_schoen(roh):
    k = re.sub(r'\s', '', roh)
    if not k:
        return _schoen(roh)
    beste = ''
    for schl, t in _koepfe().items():
        if schl and k.startswith(schl) and len(schl) > len(beste):
            beste = schl
    return _schoen(_koepfe()[beste]) if beste and len(beste) >= 4 else _schoen(roh)

def _block_name(kopf):
    m = re.match(r'Seite: (.+?) · ', kopf)
    if m:
        return 'Website', _schoen(m.group(1)), (re.search(r'(?:Entwurf|Website): ([\w.-]+)', kopf) or [None, ''])[1]
    m = re.match(r'Unterlage des Hauses: (.+?) \(PDF', kopf)
    if m:
        return 'Unterlage', UNTERLAGE_NAME.get(m.group(1), m.group(1).replace('-', ' ')), m.group(1)
    m = re.match(r'Talwissen: (.+?)(?: · Quelle (\S+))?(?: · (?:abgerufen|gelesen) (.+))?$', kopf)
    if m:
        return 'Umgebung', m.group(1), m.group(2) or ''
    return 'Grundlage', kopf[:80], ''

def _bereich(kopf):
    for muster, b in SEITE_BEREICH:
        if re.search(muster, kopf):
            return b
    return 'Das Haus'

_CACHE = {}

def abschnitte():
    """Liste aller Abschnitte der Grundlage mit Lage im Text: {aid, datei, von, bis, text, titel, block, art, bereich, stand, quelle}."""
    sig = tuple((n, os.path.getmtime(os.path.join(WISSEN_DIR, n)) if os.path.exists(os.path.join(WISSEN_DIR, n)) else 0) for n, _ in QUELLEN)
    if _CACHE.get('sig') == sig:
        return _CACHE['liste']
    liste = []
    for datei, name in QUELLEN:
        p = os.path.join(WISSEN_DIR, datei)
        if not os.path.exists(p):
            continue
        roh = open(p, encoding='utf-8').read()
        stand = datetime.datetime.fromtimestamp(os.path.getmtime(p)).astimezone().isoformat(timespec='seconds')
        zeilen = roh.splitlines(keepends=True)
        pos, kopf, art, block, ref, teile = 0, '', 'Grundlage', 'Einleitung', '', []
        for z in zeilen:   # Zeilen mit Lage
            teile.append((pos, z)); pos += len(z)
        # Gruppen: === Kopf === beginnt einen Block; ## beginnt einen Abschnitt (Website, Talwissen); Unterlagen: je PDF-Seite (Preiszeile) ein Abschnitt
        stuecke, aktuell = [], None
        def schliesse():
            if aktuell and aktuell['zeilen']:
                stuecke.append(aktuell)
        def unter_kopf(i):   # Zwischenüberschrift einer Unterlage: Grossbuchstaben ohne Einzug (Behandlungen) oder Zeile nach einem Preis vor einem Gericht (Barkarte)
            s = teile[i][1].rstrip('\n')
            if re.fullmatch(r'[A-ZÄÖÜ][A-ZÄÖÜ’\'&\- ]{4,}', s):
                return True
            nach = [teile[j][1] for j in range(i + 1, min(i + 3, len(teile)))]
            return (i > 0 and 'CHF' in teile[i - 1][1] and s.strip() and 'CHF' not in s and '|' not in s and len(nach) == 2
                    and 'CHF' not in nach[0] and '|' not in nach[0] and ('|' in nach[1] or 'CHF' in nach[1]))
        for i, (lage, z) in enumerate(teile):
            s = z.rstrip('\n')
            if s.startswith('=== ') and s.rstrip().endswith('==='):
                schliesse()
                kopf = s.strip('= ').strip(); art, block, ref = _block_name(kopf)
                aktuell = {'kopf': kopf, 'art': art, 'block': block, 'ref': ref, 'zeilen': [], 'ueber': ''}
                continue
            if aktuell is None:
                aktuell = {'kopf': '', 'art': 'Grundlage', 'block': 'Vorbemerkung', 'ref': '', 'zeilen': [], 'ueber': ''}
            neu = (art != 'Unterlage' and s.startswith('## ')) or (art == 'Unterlage' and (PREISZEILE.match(s) and len(aktuell['zeilen']) > 6
                                                                                       or len(aktuell['zeilen']) > 14 and unter_kopf(i)
                                                                                       or len(aktuell['zeilen']) > 40 and i > 0 and 'CHF' in teile[i - 1][1] and 'CHF' not in s))
            if neu and aktuell['zeilen'] and any(x[1].strip() for x in aktuell['zeilen']):
                schliesse()
                aktuell = {'kopf': kopf, 'art': art, 'block': block, 'ref': ref, 'zeilen': [], 'ueber': ''}
            if s.startswith('## ') and not aktuell['ueber']:
                aktuell['ueber'] = s[3:]
            aktuell['zeilen'].append((lage, z))
        schliesse()
        zaehler = {}
        for st in stuecke:
            von = st['zeilen'][0][0]; bis = st['zeilen'][-1][0] + len(st['zeilen'][-1][1])
            text = roh[von:bis]
            if not text.strip():
                continue
            if st['art'] == 'Unterlage':   # Titel: erste Zeile mit Inhalt nach der Preiszeile («Vorspeisen | Starters»)
                kand = [x[1].strip() for x in st['zeilen'] if x[1].strip() and not PREISZEILE.match(x[1]) and not x[1].strip().startswith('All prices')]
                gross = []
                for k in kand[:8]:   # bis zu zwei Überschriften in Grossbuchstaben («SCHWEIZ / SWITZERLAND», «WEISS / WHITE»)
                    k = k.split(' / ')[0].split('|')[0].strip()
                    k = re.sub(r'\s+', ' ', k)
                    if k.isupper() and not re.search(r'\d', k) and len(k) > 2 and k != 'CHF' and k.title() not in gross:
                        gross.append(k.title().replace('’S', '’s'))
                    if len(gross) == 2:
                        break
                titel = ' · '.join(gross) if gross else next((k.split('|')[0].strip() for k in kand if '|' in k), kand[0] if kand else st['block'])
                titel = re.sub(r'\s+', ' ', titel)
            else:
                titel = _kopf_schoen(st['ueber']) if st['ueber'] else (st['block'] if st['art'] != 'Grundlage' else 'Vorbemerkung')
            schl = f"{datei}|{st['kopf']}|{titel}"
            zaehler[schl] = zaehler.get(schl, 0) + 1
            aid = hashlib.sha1(f"{schl}|{zaehler[schl]}".encode('utf-8')).hexdigest()[:12]
            m = re.search(r'(?:abgerufen|gelesen) (?:am )?([0-9]{1,2}\.? ?[0-9A-Za-zä]+\.? ?20[0-9]{2})', st['kopf'])
            liste.append({'aid': aid, 'datei': datei, 'name': name, 'von': von, 'bis': bis, 'text': text.strip('\n'), 'titel': titel[:140],
                          'block': st['block'], 'art': st['art'], 'ref': st['ref'], 'bereich': _bereich(st['kopf'] or datei),
                          'stand': stand, 'gelesen': m.group(1) if m else '', 'pruef': hashlib.sha1(text.encode('utf-8')).hexdigest()[:12]})
    _CACHE.update(sig=sig, liste=liste)
    return liste


# ---------------------------------------------------------------- Steckbrief (steckbrief.json aus steckbrief_bau.py)
def steckbrief():
    """Der Steckbrief mit den Änderungen des Teams je Zeile (fakten.json: fid → {angabe | aus, zeit})."""
    try:
        sb = json.load(open(os.path.join(HIER, 'steckbrief.json'), encoding='utf-8'))
    except (OSError, ValueError):
        return []
    fk = _lies('fakten.json', {})
    for b in sb['bereiche']:
        for g in b['gruppen']:
            for z in g['zeilen']:
                if z['fid'] in fk:
                    z['team'] = fk[z['fid']]
    return sb['bereiche']

def _fakt(fid):
    for b in steckbrief():
        for g in b['gruppen']:
            for z in g['zeilen']:
                if z['fid'] == fid:
                    return b['bereich'], g['gruppe'], z
    raise ValueError('WISSEN · Diese Zeile gibt es nicht mehr. Bitte neu laden.')

def fakten_block():
    l = []
    for b in steckbrief():
        for g in b['gruppen']:
            for z in g['zeilen']:
                t = z.get('team')
                if not t:
                    continue
                if t.get('aus'):
                    l.append(f"[{b['bereich']} · {g['gruppe']}] {z['was']}: gilt nicht mehr (bisher «{z['angabe']}»). Nicht mehr nennen; bei Fragen dazu an die Rezeption verweisen.")
                else:
                    l.append(f"[{b['bereich']} · {g['gruppe']}] {z['was']}: {t['angabe']} (vom Team am {t['zeit'][:10]} berichtigt, bisher «{z['angabe']}»)")
    if not l:
        return ''
    return ('\n\nVOM TEAM BERICHTIGT (gilt vor WISSEN und TALWISSEN; steht dort etwas anderes, ist es veraltet):\n' + '\n'.join(l))


# ---------------------------------------------------------------- Wirkung im Chat
def _ergaenzt_aktiv():
    h = _heute()
    return [e for e in _lies('eintraege.json', []) if not e.get('aus') and (not e.get('gueltig_bis') or e['gueltig_bis'] >= h)]

def neue_texte():
    """{datei: Text mit Berichtigungen des Teams} nur für Dateien mit Berichtigungen."""
    kor = _lies('korrekturen.json', {})
    if not kor:
        return {}
    aus = {}
    for datei, _ in QUELLEN:
        p = os.path.join(WISSEN_DIR, datei)
        if not os.path.exists(p):
            continue
        roh = open(p, encoding='utf-8').read()
        l = sorted((a for a in abschnitte() if a['datei'] == datei and a['aid'] in kor), key=lambda a: -a['von'])
        if not l:
            continue
        t = roh
        for a in l:   # von hinten nach vorn, damit die Lagen stimmen
            k = kor[a['aid']]
            ersatz = '' if k.get('aus') else (f"[Vom Team des Hauses berichtigt am {k['zeit'][:10]}, gilt statt der Website:]\n{k['text'].strip()}\n" if k.get('text') else None)
            if ersatz is None:
                continue
            t = t[:a['von']] + ersatz + t[a['bis']:]
        aus[datei] = (roh, t)
    return aus

def ergaenzt_block():
    l = _ergaenzt_aktiv()
    if not l:
        return ''
    def zeile(e):
        q = e.get('quelle') or {}
        herkunft = f"aus {q.get('url')}, gelesen am {q.get('gelesen', '')[:10]}" if q.get('art') == 'link' else f"vom Team am {(e.get('geaendert') or e.get('zeit'))[:10]}"
        return (f"[{e.get('bereich', '')}] {e.get('titel', '')}" + (f" (gilt bis {e['gueltig_bis']})" if e.get('gueltig_bis') else '') +
                f"\n{e.get('text', '').strip()}\nQuelle: {herkunft}")
    return ('\n\nVOM TEAM ERGÄNZT (gilt wie WISSEN; widerspricht etwas hier WISSEN oder TALWISSEN, gilt dieser Block. Einträge «aus» einem Link '
            'hat das Team von der Seite eines Anbieters übernommen: nenne die Seite als Quelle und bei Veranstaltungen den Hinweis, Zeiten und Preise dort zu prüfen):\n'
            + '\n\n'.join(zeile(e) for e in l))

def anweisung(basis):
    """Die Anweisung des Chats mit allem, was das Team berichtigt und ergänzt hat."""
    t = basis
    for datei, (alt, neu) in neue_texte().items():
        if t.count(alt) == 1:
            t = t.replace(alt, neu)
    return t + fakten_block() + ergaenzt_block()

def wissen_text(wissen):
    """WISSEN (gast_wissen.txt) mit Berichtigungen und Ergänzungen, für den Entwurf der Antwort-Mails."""
    nt = neue_texte().get('gast_wissen.txt')
    return (nt[1] if nt and nt[0] == wissen else wissen) + fakten_block() + ergaenzt_block()


# ---------------------------------------------------------------- Link lesen (im Hintergrund)
class _Text(object):
    """Seite → lesbarer Text: Skripte, Stile, Navigation weg, Absätze als Zeilen, JSON-LD (Veranstaltungen) bleibt dabei."""
    @staticmethod
    def aus(roh):
        ld = ' '.join(re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', roh, flags=re.S | re.I))[:6000]
        titel = html.unescape(re.sub(r'\s+', ' ', (re.search(r'<title[^>]*>(.*?)</title>', roh, flags=re.S | re.I) or [None, ''])[1])).strip()
        s = re.sub(r'<(script|style|noscript|svg|nav|footer|header|form|iframe)\b[^>]*>.*?</\1>', ' ', roh, flags=re.S | re.I)
        s = re.sub(r'<br\s*/?>|</(p|div|li|h\d|tr|section|article|dd|dt)>', '\n', s, flags=re.I)
        s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
        s = re.sub(r'[ \t\xa0]+', ' ', s)
        s = '\n'.join(z.strip() for z in s.splitlines() if z.strip())
        return titel, s, ld

def _sicher(url):
    u = urllib.parse.urlparse(url)
    if u.scheme not in ('http', 'https') or not u.hostname:
        raise ValueError('LINK · Bitte eine vollständige Adresse mit https:// einfügen.')
    try:
        for info in socket.getaddrinfo(u.hostname, None):
            ip = ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                raise ValueError('LINK · Diese Adresse ist nicht öffentlich erreichbar.')
    except socket.gaierror:
        raise ValueError('LINK · Diese Adresse gibt es nicht. Bitte prüfen.')
    return url

def _hole(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
                                               'Accept-Language': 'de-CH,de;q=0.9,en;q=0.7'})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            typ = r.headers.get('Content-Type', '')
            roh = r.read(3_000_000)
    except urllib.error.HTTPError as e:
        raise ValueError(f'SEITE · Die Seite antwortet mit Fehler {e.code}. Bitte die Adresse prüfen oder den Text der Seite einfügen.')
    except (urllib.error.URLError, socket.timeout, TimeoutError):
        raise ValueError('SEITE · Die Seite war nicht erreichbar. Bitte später neu einlesen oder den Text der Seite einfügen.')
    if 'pdf' in typ.lower():
        raise ValueError('PDF · Eine PDF lässt sich hier noch nicht einlesen. Bitte den Text der PDF in das Feld «Text» kopieren.')
    m = re.search(r'charset=([\w-]+)', typ)
    for enc in ([m.group(1)] if m else []) + ['utf-8', 'latin-1']:
        if enc:
            try:
                return roh.decode(enc)
            except (LookupError, UnicodeDecodeError):
                continue
    return roh.decode('utf-8', 'replace')

AUSZUG = """Du hilfst dem Team von Culinarium in Hannover-Linden (Food-Pairing-Abende an der langen Tafel in der Bar Walk on the Wild Side, dazu das Pop-up Dirty Chicken), das Wissen des Chats auf der Website aktuell zu halten. Das Team gibt dir neues Material:
eigenen Text, Seiten aus Links (Veranstaltung, Angebot eines Anbieters in der Region), Dokumente (zum Beispiel eine neue Karte, ein Programm) oder Fotos
(zum Beispiel das Plakat eines Abends, ein Aushang, die Karte am Platz). Zieh daraus heraus, was ein Gast von Culinarium wissen will, und gib es als Einträge zurück.

Regeln:
- Nur, was wörtlich im Material steht oder auf dem Foto lesbar ist. Nichts ergänzen, nichts schätzen, kein Wissen von ausserhalb. Fehlt eine Angabe (Uhrzeit, Preis), lässt du sie weg. Unleserliches lässt du weg.
- Schreibt das Team selbst etwas (TEXT DES TEAMS), gilt das als Angabe des Hauses, auch wenn es kurz ist.
- Je Veranstaltung, Angebot oder Thema ein Eintrag. Höchstens 12 Einträge; bei langen Programmen oder Karten die für Gäste wichtigsten, Karten als ein Eintrag je Abschnitt mit den Preisen.
- titel: kurz, wie ein Gast danach fragen würde («Der Abend im November», «Dirty Chicken im Dezember»).
- text: auf Deutsch, wie die Website schreibt (ss statt ß, Namen wie Haasemannstraße bleiben), zwei bis sechs ganze Sätze, sachlich, mit Datum, Uhrzeit, Ort, Preis, Anmeldung und Ansprechstelle, soweit vorhanden. Keine Werbesprache.
- bereich: einer aus der Liste. Veranstaltungen mit Datum sind «Veranstaltungen». Wählt das Team einen Bereich (BEREICH DES TEAMS), nimm ihn.
- gueltig_bis: bei Veranstaltungen und befristeten Angaben der letzte Tag (JJJJ-MM-TT), sonst null. Jahr nur, wenn es dasteht oder eindeutig folgt; sonst null.
- Ist im Material nichts, was Gäste brauchen, gib eine leere Liste und in grund einen Satz, warum.
Antworte ausschliesslich mit dem Werkzeug «eintraege»."""

WERKZEUG = {'name': 'eintraege', 'description': 'Die Einträge für das Wissen der Rezeption im Chat.',
            'input_schema': {'type': 'object', 'required': ['eintraege', 'grund'], 'additionalProperties': False,
                             'properties': {'grund': {'type': 'string'},
                                            'eintraege': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False,
                                                          'required': ['bereich', 'titel', 'text', 'gueltig_bis'],
                                                          'properties': {'bereich': {'type': 'string', 'enum': BEREICHE[:-1]},
                                                                         'titel': {'type': 'string'}, 'text': {'type': 'string'},
                                                                         'gueltig_bis': {'type': ['string', 'null']}}}}}}}

_G = None   # das geladene gast.py (für _api und MODELL), gesetzt von rezeption.einbinden

def _ki(koerper, api=None):
    """Aufruf an Claude über gast.py; Fehler des Dienstes (Guthaben, Grenze, Ausfall) als klare Meldung statt «Fehler 400»."""
    try:
        return (api or _G._api)(koerper)
    except urllib.error.HTTPError as e:
        try:
            m = json.loads(e.read().decode('utf-8')).get('error', {}).get('message', '')
        except Exception:  # noqa: BLE001
            m = ''
        if 'usage limit' in m or 'credit' in m.lower():
            raise ValueError('KI · Der Chat hat sein Guthaben für diesen Monat aufgebraucht und antwortet gerade nicht. Sobald es wieder frei ist, geht es hier weiter.')
        raise ValueError(f'KI · Der Chat-Dienst antwortet gerade nicht (Fehler {e.code}). Bitte in ein paar Minuten noch einmal.')
    except (urllib.error.URLError, socket.timeout, TimeoutError):
        raise ValueError('KI · Der Chat-Dienst war nicht erreichbar. Bitte in ein paar Minuten noch einmal.')

def _gueltig_bis(s):
    return s if isinstance(s, str) and re.fullmatch(r'20\d\d-\d\d-\d\d', s or '') else None


# ---------------------------------------------------------------- Neues Wissen einlesen: Text, Links, Dokumente, Fotos (im Hintergrund)
# Dateien des Teams liegen unter daten/gedaechtnis/dateien/<lid>/ (für «Neu einlesen» und als Beleg). Claude liest PDF und Fotos selbst
# (Inhaltsblöcke document/image), Word-Dateien und Text werden hier zu Text.
BILD = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
TEXTART = ('.txt', '.md', '.csv')
URL = re.compile(r'https?://[^\s<>«»"]+')

def _docx_text(roh):
    import io, zipfile
    with zipfile.ZipFile(io.BytesIO(roh)) as z:
        x = z.read('word/document.xml').decode('utf-8', 'replace')
    x = re.sub(r'</w:p>', '\n', x); x = re.sub(r'<w:tab/>', '\t', x)
    return html.unescape(re.sub(r'<[^>]+>', '', x)).strip()

def _bloecke(lid, auftrag):
    """Inhaltsblöcke für Claude aus Text, Links und Dateien; Fehler einzelner Links werden notiert, solange anderes Material da ist."""
    bl, notiz, titel = [], [], ''
    for url in auftrag.get('urls', []):
        try:
            t, text, ld = _Text.aus(_hole(_sicher(url)))
            if len(text) < 200 and not ld:
                raise ValueError('SEITE · Die Seite zeigt ihren Inhalt erst im Browser. Bitte den Text der Seite ins Feld kopieren.')
            titel = titel or t
            bl.append({'type': 'text', 'text': f'SEITE {url} (Titel: {t})' + (f'\nStrukturierte Angaben (JSON-LD): {ld}' if ld else '') + f'\n{text[:40000]}'})
        except ValueError as e:
            notiz.append(re.sub(r'^[A-ZÄÖÜ]+ · ', '', str(e)))
    ordner = _pfad(os.path.join('dateien', lid))
    for f in auftrag.get('dateien', []):
        p = os.path.join(ordner, f['datei'])
        try:
            roh = open(p, 'rb').read()
        except OSError:
            notiz.append(f'{f["name"]} fehlt.'); continue
        typ, name = f.get('typ', ''), f['name']
        titel = titel or name
        if typ == 'application/pdf' or name.lower().endswith('.pdf'):
            bl.append({'type': 'text', 'text': f'DOKUMENT {name}:'})
            bl.append({'type': 'document', 'source': {'type': 'base64', 'media_type': 'application/pdf', 'data': base64.b64encode(roh).decode('ascii')}})
        elif typ in BILD:
            bl.append({'type': 'text', 'text': f'FOTO {name}:'})
            bl.append({'type': 'image', 'source': {'type': 'base64', 'media_type': typ, 'data': base64.b64encode(roh).decode('ascii')}})
        elif name.lower().endswith('.docx'):
            bl.append({'type': 'text', 'text': f'DOKUMENT {name}:\n{_docx_text(roh)[:40000]}'})
        elif name.lower().endswith(TEXTART):
            bl.append({'type': 'text', 'text': f'DOKUMENT {name}:\n{roh.decode("utf-8", "replace")[:40000]}'})
        else:
            notiz.append(f'{name}: diese Art Datei lässt sich nicht lesen.')
    if auftrag.get('text'):
        bl.append({'type': 'text', 'text': 'TEXT DES TEAMS:\n' + auftrag['text']})
    return bl, notiz, titel

def _auszug(bloecke, bereich, hinweis=''):
    if _G is None:
        raise ValueError('CHAT · Der Assistent ist noch nicht geladen. serve.py neu starten.')
    kopf = f'Heute ist {_heute()}.' + (f'\nBEREICH DES TEAMS: {bereich}' if bereich else '') + (f'\nHinweis des Teams: {hinweis}' if hinweis else '')
    a = _ki({'model': _G.MODELL, 'max_tokens': 8000, 'tools': [WERKZEUG], 'system': AUSZUG,
             'messages': [{'role': 'user', 'content': [{'type': 'text', 'text': kopf}] + bloecke}]})
    for b in a.get('content', []):
        if b.get('type') == 'tool_use' and b.get('name') == 'eintraege':
            return b.get('input') or {}
    roh = ''.join(b.get('text', '') for b in a.get('content', []) if b.get('type') == 'text')
    m = re.search(r'\{.*\}', roh, flags=re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except ValueError:
            pass
    raise ValueError('AUSZUG · Das Material liess sich nicht auswerten. Bitte noch einmal versuchen.')

def _setze_job(lid, **k):
    with SCHLOSS:
        ls = _lies('links.json', [])
        for x in ls:
            if x['lid'] == lid:
                x.update(k)
        _schreib('links.json', ls)

def _lauf(lid, auftrag, von=''):
    try:
        bl, notiz, titel = _bloecke(lid, auftrag)
        if not bl:
            raise ValueError('EINGABE · ' + (' '.join(notiz) or 'Nichts zum Einlesen da.'))
        erg = _auszug(bl, auftrag.get('bereich') or '', auftrag.get('hinweis') or '')
        jetzt = _jetzt()
        roh_l = [e for e in (erg.get('eintraege') or []) if isinstance(e, dict) and (e.get('titel') or '').strip() and (e.get('text') or '').strip()][:12]
        urls = auftrag.get('urls') or []
        art = 'link' if urls and not auftrag.get('dateien') and not auftrag.get('text') else 'eingabe'
        with SCHLOSS:
            alle = _lies('eintraege.json', [])
            alt = [e for e in alle if (e.get('quelle') or {}).get('lid') == lid]
            alle = [e for e in alle if (e.get('quelle') or {}).get('lid') != lid]
            wids = []
            for n, e in enumerate(roh_l):
                wid = f'l{lid}-{n}'
                ber = auftrag.get('bereich') if auftrag.get('bereich') in BEREICHE else (e['bereich'] if e.get('bereich') in BEREICHE else 'Veranstaltungen')
                alle.append({'wid': wid, 'bereich': ber, 'titel': e['titel'].strip()[:140], 'text': e['text'].strip()[:3000],
                             'gueltig_bis': _gueltig_bis(e.get('gueltig_bis')), 'zeit': jetzt, 'geaendert': jetzt, 'von': von,
                             'quelle': {'art': art, 'url': urls[0] if urls else '', 'titel': titel[:160], 'gelesen': jetzt, 'lid': lid,
                                        'dateien': [f['name'] for f in auftrag.get('dateien', [])]}})
                wids.append(wid)
            _schreib('eintraege.json', alle)
        _setze_job(lid, status='fertig' if wids else 'leer', fertig=jetzt, wids=wids, titel=titel[:160] or auftrag.get('titel', ''),
                   meldung=' '.join(notiz)[:300] if wids else ((erg.get('grund') or '') + (' ' + ' '.join(notiz) if notiz else ''))[:300])
        if wids:
            herkunft = ', '.join([urllib.parse.urlparse(u).hostname.replace('www.', '') for u in urls] + [f['name'] for f in auftrag.get('dateien', [])]) or 'Text des Teams'
            _merke('link', f"{len(wids)} {'Angabe' if len(wids) == 1 else 'Angaben'} aus {herkunft}" + (' (neu eingelesen)' if alt else ''),
                   roh_l[0].get('bereich', ''), lid, von or 'Team', ' · '.join(e['titel'] for e in roh_l)[:300])
    except Exception as e:  # noqa: BLE001
        m = str(e) if isinstance(e, ValueError) else 'FEHLER · Das Einlesen ist abgebrochen. Bitte noch einmal versuchen.'
        _setze_job(lid, status='fehler', fertig=_jetzt(), meldung=re.sub(r'^[A-ZÄÖÜ]+ · ', '', m)[:300])

GRENZE_DATEI = 20 * 1024 * 1024

def einlesen(text='', dateien=None, bereich='', von='', lid='', hinweis=''):
    """Neues Wissen: Text, Links im Text, Dateien (base64 vom Browser). Ohne Links und Dateien und mit gewähltem Bereich wird der Text
    direkt zur Angabe (geht auch, wenn die KI nicht antwortet). Sonst liest ein Hintergrund-Faden alles und legt die Angaben an.
    Mit lid: denselben Auftrag neu einlesen (gespeicherte Dateien und Text)."""
    with SCHLOSS:
        ls = _lies('links.json', [])
    if lid:
        alt = next((x for x in ls if x['lid'] == lid), None)
        if not alt:
            raise ValueError('WISSEN · Diesen Auftrag gibt es nicht mehr.')
        auftrag = alt.get('auftrag') or {'urls': [alt['url']] if alt.get('url') else [], 'text': '', 'dateien': [], 'bereich': ''}
    else:
        text = (text or '').strip()[:60000]
        urls = list(dict.fromkeys(u.rstrip('.,;)') for u in URL.findall(text)))[:5]
        rest = URL.sub('', text).strip()
        dateien = [f for f in (dateien or []) if isinstance(f, dict) and f.get('daten')][:10]
        bereich = bereich if bereich in BEREICHE else ''
        if not urls and not dateien and len(rest) < 3:
            raise ValueError('EINGABE · Bitte etwas schreiben, einen Link einfügen oder eine Datei dazulegen.')
        if not urls and not dateien and bereich:   # eigener Text mit Bereich: direkt ins Wissen
            erste = re.split(r'(?<=[^\d\s][.!?])\s+(?=[A-ZÄÖÜ«])|\n', rest, maxsplit=1)[0].strip().rstrip('.')
            titel = erste if len(erste) <= 70 else erste[:67].rsplit(' ', 1)[0] + ' …'
            return {'direkt': post('wissen_eintrag', {'bereich': bereich, 'titel': titel, 'text': rest, 'von': von})['eintrag']}
        for u in urls:
            _sicher(u)
        lid = hashlib.sha1(f'{text}|{time.time()}'.encode('utf-8')).hexdigest()[:8]
        ordner = _pfad(os.path.join('dateien', lid))
        abgelegt = []
        for n, f in enumerate(dateien):
            try:
                roh = base64.b64decode(f['daten'].split(',', 1)[-1])
            except Exception:  # noqa: BLE001
                raise ValueError(f'DATEI · {f.get("name", "Datei")} liess sich nicht lesen.')
            if len(roh) > GRENZE_DATEI:
                raise ValueError(f'DATEI · {f.get("name", "Datei")} ist grösser als 20 MB.')
            name = re.sub(r'[^\w.\- äöüÄÖÜ]', '_', str(f.get('name') or f'datei-{n}'))[:100]
            os.makedirs(ordner, exist_ok=True)
            datei = f'{n:02d}-{name}'
            open(os.path.join(ordner, datei), 'wb').write(roh)
            abgelegt.append({'name': name, 'typ': str(f.get('typ') or '')[:60], 'datei': datei, 'groesse': len(roh)})
        auftrag = {'urls': urls, 'text': rest, 'dateien': abgelegt, 'bereich': bereich, 'hinweis': hinweis[:400]}
    titel = auftrag['dateien'][0]['name'] if auftrag.get('dateien') else (urllib.parse.urlparse(auftrag['urls'][0]).hostname or '').replace('www.', '') if auftrag.get('urls') else (auftrag.get('text') or '')[:60]
    with SCHLOSS:
        ls = [x for x in _lies('links.json', []) if x['lid'] != lid]
        eintrag = {'lid': lid, 'url': (auftrag.get('urls') or [''])[0], 'zeit': _jetzt(), 'status': 'liest', 'titel': titel, 'wids': [], 'von': von, 'auftrag': auftrag,
                   'art': 'eingabe' if auftrag.get('dateien') or auftrag.get('text') else 'link'}
        ls.append(eintrag)
        _schreib('links.json', ls)
    threading.Thread(target=_lauf, args=(lid, auftrag, von), daemon=True).start()
    return {'link': eintrag}

def link_lesen(url, text='', hinweis='', lid='', von=''):
    """Alter Weg (nur ein Link oder eingefügter Text) über einlesen()."""
    if lid:
        return einlesen(lid=lid, von=von)['link']
    url = (url or '').strip()
    if url and not re.match(r'https?://', url):
        url = 'https://' + url
    return einlesen(text=(url + '\n' + (text or '')).strip(), von=von, hinweis=hinweis).get('link')


# ---------------------------------------------------------------- Schnittstelle (/reception/api/wissen…)
def get(was, q=None):
    if was == 'wissen':
        kor = _lies('korrekturen.json', {})
        l = []
        for a in abschnitte():
            k = kor.get(a['aid'])
            l.append({k2: a[k2] for k2 in ('aid', 'name', 'titel', 'block', 'art', 'ref', 'bereich', 'stand', 'gelesen', 'text')}
                     | ({'korrektur': {**k, 'veraltet': k.get('pruef') not in (None, a['pruef'])}} if k else {}))
        h = _heute()
        eintraege = [dict(e, abgelaufen=bool(e.get('gueltig_bis') and e['gueltig_bis'] < h)) for e in _lies('eintraege.json', [])]
        return {'steckbrief': steckbrief(), 'offen': list(reversed(_lies('offen.json', []))), 'abschnitte': l, 'eintraege': eintraege, 'links': list(reversed(_lies('links.json', [])))[:60],
                'verlauf': list(reversed(_lies('verlauf.json', [])))[:200], 'bereiche': BEREICHE, 'heute': h}
    if was == 'wissen_links':
        return {'links': list(reversed(_lies('links.json', [])))[:60]}
    raise ValueError('WISSEN · Unbekannte Ansicht.')

def _von(d):
    """Name der Person, die etwas einträgt (Robert 16.10.2026: «dass man weiss, wer das eingetragen hat»). Pflicht bei allem, was das Wissen ändert."""
    v = re.sub(r'\s+', ' ', str(d.get('von') or '')).strip()[:60]
    if len(v) < 2:
        raise ValueError('NAME · Bitte deinen Namen eintragen, damit das Team weiss, wer das geändert hat.')
    return v

def _abschnitt(aid):
    a = next((x for x in abschnitte() if x['aid'] == aid), None)
    if not a:
        raise ValueError('WISSEN · Diesen Abschnitt gibt es nicht mehr. Bitte neu laden.')
    return a

def post(was, d):
    if was == 'wissen_offen':        # Thema, zu dem nichts im Wissen steht: bei einer Abteilung nachgefragt, bis die Antwort eingetragen ist
        thema = str(d.get('thema') or '').strip()[:120]; an = str(d.get('an') or '').strip()[:80]
        if len(thema) < 2:
            raise ValueError('EINGABE · Bitte das Thema nennen.')
        von = _von(d)
        with SCHLOSS:
            l = _lies('offen.json', [])
            e = {'oid': 'o' + str(int(time.time() * 1000)), 'thema': thema, 'an': an, 'zeit': _jetzt(), 'von': von}
            l.append(e); _schreib('offen.json', l[-300:])
        _merke('offen', f'{thema} · {an} gefragt' if an else thema, '', e['oid'], von)
        return {'ok': True, 'offen': e}
    if was == 'wissen_offen_weg':
        with SCHLOSS:
            _schreib('offen.json', [x for x in _lies('offen.json', []) if x.get('oid') != d.get('oid')])
        return {'ok': True}
    if was == 'wissen_fakt':         # Zeile des Steckbriefs: neue Angabe, nicht mehr nennen oder zurück
        bereich, gruppe, z = _fakt(d.get('fid'))
        von = _von(d)
        with SCHLOSS:
            fk = _lies('fakten.json', {})
            if d.get('zurueck'):
                fk.pop(z['fid'], None); art = 'zurueck'
            elif d.get('aus'):
                fk[z['fid']] = {'aus': True, 'zeit': _jetzt(), 'von': von}; art = 'aus'
            else:
                angabe = str(d.get('angabe') or '').strip()[:600]
                if len(angabe) < 1:
                    raise ValueError('EINGABE · Bitte die Angabe ausfüllen. Gilt sie nicht mehr, «Nicht mehr nennen» wählen.')
                if angabe == z['angabe']:
                    fk.pop(z['fid'], None); art = 'zurueck'
                else:
                    fk[z['fid']] = {'angabe': angabe, 'zeit': _jetzt(), 'von': von}; art = 'geaendert'
            _schreib('fakten.json', fk)
        _merke(art, f"{z['was']} ({gruppe})", bereich, z['fid'], von)
        return {'ok': True}
    if was == 'wissen_aendern':      # Abschnitt der Grundlage neu fassen
        a = _abschnitt(d.get('aid')); text = str(d.get('text') or '').strip()[:8000]
        if len(text) < 3:
            raise ValueError('EINGABE · Bitte den Text ausfüllen. Soll der Chat das gar nicht mehr wissen, «Ausblenden» wählen.')
        with SCHLOSS:
            kor = _lies('korrekturen.json', {})
            kor[a['aid']] = {'text': text, 'zeit': _jetzt(), 'pruef': a['pruef']}
            _schreib('korrekturen.json', kor)
        _merke('geaendert', a['titel'], a['bereich'], a['aid'])
        return {'ok': True}
    if was == 'wissen_aus':          # Abschnitt aus- oder wieder einblenden
        a = _abschnitt(d.get('aid'))
        with SCHLOSS:
            kor = _lies('korrekturen.json', {})
            if d.get('aus'):
                kor[a['aid']] = {'aus': True, 'zeit': _jetzt(), 'pruef': a['pruef']}
            else:
                kor.pop(a['aid'], None)
            _schreib('korrekturen.json', kor)
        _merke('aus' if d.get('aus') else 'an', a['titel'], a['bereich'], a['aid'])
        return {'ok': True}
    if was == 'wissen_zurueck':      # Berichtigung verwerfen: wieder wie auf der Website
        a = _abschnitt(d.get('aid'))
        with SCHLOSS:
            kor = _lies('korrekturen.json', {}); kor.pop(a['aid'], None); _schreib('korrekturen.json', kor)
        _merke('zurueck', a['titel'], a['bereich'], a['aid'])
        return {'ok': True}
    if was == 'wissen_eintrag':      # Eintrag des Teams anlegen oder ändern (auch Einträge aus Links)
        titel = str(d.get('titel') or '').strip()[:140]; text = str(d.get('text') or '').strip()[:4000]
        bereich = d.get('bereich') if d.get('bereich') in BEREICHE else 'Das Haus'
        if len(titel) < 2 or len(text) < 3:
            raise ValueError('EINGABE · Bitte Titel und Text ausfüllen.')
        von = _von(d)
        jetzt = _jetzt()
        with SCHLOSS:
            alle = _lies('eintraege.json', [])
            alt = next((e for e in alle if e.get('wid') == d.get('wid')), None)
            if alt:
                alt.update(titel=titel, text=text, bereich=bereich, gueltig_bis=_gueltig_bis(d.get('gueltig_bis')), geaendert=jetzt, vom_team=True, von=von)
            else:
                alt = {'wid': 't' + str(int(time.time() * 1000)), 'bereich': bereich, 'titel': titel, 'text': text,
                       'gueltig_bis': _gueltig_bis(d.get('gueltig_bis')), 'zeit': jetzt, 'geaendert': jetzt, 'quelle': {'art': 'team'}, 'von': von}
                alle.append(alt)
            _schreib('eintraege.json', alle)
        _merke('geaendert' if d.get('wid') else 'neu', titel, bereich, alt['wid'], von)
        return {'ok': True, 'eintrag': alt}
    if was == 'wissen_eintrag_aus':
        with SCHLOSS:
            alle = _lies('eintraege.json', [])
            e = next((x for x in alle if x.get('wid') == d.get('wid')), None)
            if not e:
                raise ValueError('WISSEN · Diesen Eintrag gibt es nicht mehr.')
            e['aus'] = bool(d.get('aus')); _schreib('eintraege.json', alle)
        _merke('aus' if e['aus'] else 'an', e['titel'], e.get('bereich', ''), e['wid'], str(d.get('von') or 'Team')[:60])
        return {'ok': True}
    if was == 'wissen_eintrag_weg':
        with SCHLOSS:
            alle = _lies('eintraege.json', [])
            e = next((x for x in alle if x.get('wid') == d.get('wid')), None)
            if not e:
                raise ValueError('WISSEN · Diesen Eintrag gibt es nicht mehr.')
            _schreib('eintraege.json', [x for x in alle if x.get('wid') != d.get('wid')])
        _merke('entfernt', e['titel'], e.get('bereich', ''), e['wid'], str(d.get('von') or 'Team')[:60])
        return {'ok': True}
    if was == 'wissen_einlesen':     # Neues Wissen aus dem Eingabefeld: Text, Links, Dokumente, Fotos
        return {'ok': True, **einlesen(d.get('text'), d.get('dateien'), str(d.get('bereich') or ''), _von(d), str(d.get('lid') or ''))}
    if was == 'wissen_link':
        return {'ok': True, 'link': link_lesen(d.get('url'), d.get('text'), str(d.get('hinweis') or ''), str(d.get('lid') or ''), _von(d))}
    if was == 'wissen_link_weg':     # Link samt seinen Einträgen entfernen
        lid = d.get('lid')
        with SCHLOSS:
            ls = _lies('links.json', []); x = next((y for y in ls if y['lid'] == lid), None)
            if not x:
                raise ValueError('WISSEN · Diesen Link gibt es nicht mehr.')
            _schreib('links.json', [y for y in ls if y['lid'] != lid])
            alle = _lies('eintraege.json', [])
            n = sum(1 for e in alle if (e.get('quelle') or {}).get('lid') == lid)
            _schreib('eintraege.json', [e for e in alle if (e.get('quelle') or {}).get('lid') != lid])
            import shutil
            shutil.rmtree(_pfad(os.path.join('dateien', re.sub(r'\W', '', str(lid)))), ignore_errors=True)
        _merke('entfernt', f"Link {urllib.parse.urlparse(x.get('url') or '').hostname or 'Text'} mit {n} {'Eintrag' if n == 1 else 'Einträgen'}", 'Veranstaltungen', lid)
        return {'ok': True}
    if was == 'wissen_probe':        # Frage an den Chat mit dem jetzigen Wissen, ohne Protokoll
        f = str(d.get('frage') or '').strip()[:600]
        if len(f) < 3:
            raise ValueError('EINGABE · Bitte eine Frage eingeben.')
        if _G is None:
            raise ValueError('CHAT · Der Assistent ist noch nicht geladen. serve.py neu starten.')
        roh = _G._api
        _G._api = lambda k: _ki(k, roh)   # klare Meldung, wenn der Dienst nicht antwortet
        try:
            a = _G.frage([{'role': 'user', 'content': f}], heute=_heute(), sprache='de')
        finally:
            _G._api = roh
        return {'text': a.get('text', ''), 'belegt': a.get('belegt', True)}
    raise ValueError('WISSEN · Unbekannter Auftrag.')
