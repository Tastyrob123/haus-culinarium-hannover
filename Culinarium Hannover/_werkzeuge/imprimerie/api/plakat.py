"""Plakatwerkstatt · «Abend beschreiben» (Funktion 2, Auftrag Oberchef 28.10.2026, Roberts Idee: «Event abend Konzept und Thema zu beschreiben und dann wird
auf der Grundlage i wie 3-5 vorschläge generiert die man wie in einem Basic Photoshop / Canva mäßig bearbeiten kann»; Robert 28.10.: «Sinn der Sache ist, dass du
mir neue generierst, andere» und «lass doch jetzt da die KI live laufen … ich will, dass die Leute sehen, was das kann»).

POST /_werkzeuge/imprimerie/api/plakat  {thema, konzept, gast, zahl, monat}            → Plan: {vorschlaege (Probe), live, hinweis}
POST /_werkzeuge/imprimerie/api/plakat  {…, nr, durchgang, geraet}                       → ein neuer Vorschlag: {vorschlag, bilder} (Vorder- und Rückseite)

- Live (Schlüssel nur auf dem Server: ~/.config/tasty/higgsfield.env oder Umgebung HF_API_KEY_ID / HF_API_KEY_SECRET; nie im Browser): je Vorschlag ein
  eigener Bildauftrag (Thema, Konzept, Gastkoch, Hausstil, freie Kopfzone) an Higgsfield, Vorderseite 4:3 mit Kopfzonen-Prüfung (einmal neu bei Befund),
  Rückseite 1:1 mit Schriftfarbe nach Kontrast. Die Bilder legt der Server in haeuser/culinarium/bilder/ ab, der Browser bindet sie als Fotos ein.
- Grenzen (GRENZEN, eine Stelle): je Gerät 3 Durchgänge am Tag, gesamt 40 Bilder am Tag. Fehler, leeres Guthaben oder Grenze → Rückfall auf passende
  Motive der Sammlung mit Hinweis.
- Gespeicherte Antworten (_qa/abend-roh/abende.json): schon erzeugte Abende (Roberts Sommerabend 28.10.) kommen ohne neue Kosten wieder.
- Probe (ohne Schlüssel): Motive aus der Sammlung, streng nach Jahreszeit des Themas (sonst des Datums), kein Motiv doppelt."""
import hashlib, io, json, os, re, sys, threading, time, urllib.error, urllib.request
from datetime import date

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAUS = os.path.join(HIER, 'haeuser', 'culinarium')
MOTIVE = os.path.join(HAUS, 'motive.json')
ABENDE = os.path.join(HIER, '_qa', 'abend-roh')
SCHLUESSEL = os.path.expanduser('~/.config/tasty/higgsfield.env')
ZAEHLER = os.path.join(HIER, 'api', '_daten', 'plakat-ki-zaehler.json')
GRENZEN = {'durchgaenge_je_geraet': 3, 'bilder_je_tag': 40}   # Schutz für Roberts Guthaben (Oberchef 28.10.), hier und nur hier einstellen
SPERRE = threading.Lock()   # Tageszähler: parallele Vorschläge eines Durchgangs überschrieben sich sonst gegenseitig (29.10.)
FARBEN = {}   # Durchgang → Vorschlag → Farbwelt vorn/hinten (Prüfung auf klar verschiedene Farbwelten)
# Rudis Plakate gehen NICHT als Bildvorlage mit (sonst kopiert das Modell Mondfrau, Panther, Kürbisse; Oberchef 28.10.); nur wenn ein Modell Stil und
# Inhalt nachweislich trennt, STILREFERENZ = True setzen
STILREFERENZ = False
REFERENZEN = ['pl_DbYnkdkjrNy', 'pl_DPwlqcfiKcA', 'pl_C17kqAXLfs_', 'pl_DFqbLG2s_dc']   # Mondfrau, Pin-up mit Kürbissen und Kerzen, Glitzer und Gläser, Panther
REFERENZ_CACHE = os.path.join(HIER, 'api', '_daten', 'plakat-referenzen.json')
API = 'https://api.higgsfield.ai'
# Bildmodell der Higgsfield-API (Modelltest 29.10., Tafel live-2910/modelle.html): Recraft v4.1 trägt Konzept und gemalte Malerei am ehesten, ohne Signatur,
# 0,56 Credits je Bild. soul/standard malt flach, ideogram signiert. Anderes Modell über HF_BILDMODELL in der Schlüsseldatei.
MODELL = 'recraft/v4.1/text-to-image'
MODELL_FELDER = {   # Felder je Modell laut API-Schema (estimate-Prüfung 29.10.); höchste Auflösung, die das Modell nimmt
    'recraft/v4.1/text-to-image': {'resolution': '1k'},
    'ideogram/v4.0': {'rendering_speed': 'QUALITY'},
    'ideogram/v3': {'resolution': '1k'},
    'higgsfield-ai/soul/standard': {'resolution': '1080p'},
}
VORN_FORMAT = {'recraft/v4.1/text-to-image': '5:4', 'ideogram/v4.0': '5:4'}   # Motivfeld des Plakats (Instagram 1:1, Quadrat) ist 1,28:1; 4:3 nur, wo das Modell kein 5:4 kennt
GESPERRT = ('higgsfield-ai/soul/reference',)   # kopiert Rudis Plakate 1:1 samt Kopfzeile (Modelltest 29.10.): darf nie laufen
HINWEIS_LIVE = 'Live mit KI: Jeder Vorschlag entsteht in diesem Moment neu, gemalt für euren Abend.'   # kein Geld in der Werkstatt (Oberchef 30.10.2026)
HINWEIS_PROBE = 'Probe: Motive aus der Sammlung. Mit KI entstehen hier neue.'
JAHRESZEIT_WORTE = {'Sommer': ('sommer', 'summer', 'grill', 'strand', 'sonnen', 'rosé', 'beach'),
                    'Winter': ('winter', 'weihnacht', 'advent', 'schnee', 'silvester', 'glühwein', 'ski', 'punsch'),
                    'Frühling': ('frühling', 'frühjahr', 'ostern', 'spargel', 'bärlauch', 'blüte'),
                    'Herbst': ('herbst', 'kürbis', 'pilz', 'trüffel', 'wildbret', 'ernte', 'oktober')}
sys.path.insert(0, os.path.join(HIER, '_qa'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import konzept as KZ   # Konzept je Vorschlag aus Thema, Gerichten, Drinks und Gastkoch (Robert 28.10.: «komplett neue und weitergedachte konzepte»)
try:
    import kopfzone   # Kopfzonen-Prüfung und Schriftfarbe der Rückseite (dieselbe wie für die Sammlung)
except Exception:   # online ohne _qa: ohne Prüfung, Farben nach Voreinstellung
    kopfzone = None

STIL = ('A lush, hand-painted vintage poster illustration in exactly the style of the reference images (the house illustrator of these evening posters): '
        'gouache and oil painting look, soft brushwork, a slightly faded printed texture, one bold surreal idea with only two or three elements, '
        'a calm plain background (a wall, a sky or a curtain in one colour), deliberately playful scale. The dishes and drinks are painted as part of the '
        'illustration, never like a food photograph. No cinematic lighting, no glow, no glossy rendering, no orange-and-teal colour grading, no depth of field, '
        'no busy scenery, no extra objects. The top quarter of the image must stay a completely calm, empty area of the plain background in one even colour, '
        'with no objects, heads, hands, lines or details reaching into it; all subjects stay in the lower three quarters, and that calm area is either very '
        'light (a pale tint) or very dark (a deep shade) of the colour world given below, never a middle tone, so lettering reads on it. '
        'Absolutely no text, no letters, no words, no logos, no signage.')
RUECK = ('A calm hand-painted companion picture for the back of the same vintage poster, in the style of the reference images: soft brushwork, a slightly faded '
         'printed texture, few elements, no glow, no glossy rendering. The upper-left third and the whole bottom third stay calm and uncluttered in a deep, dark shade '
         'of the colour world (soft plain painted texture) so that white typography reads clearly on them; the main objects sit in the right half. '
         'Absolutely no text, no letters, no words, no logos.')
WINKEL = ['oversized cocktail glasses as part of the landscape', 'a warm evening scene outdoors under an open sky, candles on the table, everything low in the picture',
          'a sunny 1960s travel-poster scene', 'an elegant animal as the host of the evening, its head well below the top quarter of the picture',
          'a still life where the dish becomes a landscape']
JAHR = {12: 'Winter', 1: 'Winter', 2: 'Winter', 3: 'Frühling', 4: 'Frühling', 5: 'Frühling', 6: 'Sommer', 7: 'Sommer', 8: 'Sommer', 9: 'Herbst', 10: 'Herbst', 11: 'Herbst'}


def _w(t):
    return {w for w in re.findall(r'[a-zäöüß]{4,}', str(t or '').lower())}


# Bildauftrag mit Struktur (Robert 28.10.: «keinen Sinn, keine Struktur, geht nicht auf das wirkliche Thema ein»): die genannten Gerichte und Drinks
# sind die Hauptsache des Bildes, die Jahreszeit gibt Licht und Ort, und jeder Vorschlag hat eine eigene Bildidee.
SAISON_ORT = {'Frühling': 'a fresh spring evening with blossoms', 'Sommer': 'a warm summer evening outdoors',   # nur Ort und Zeit; die Farben gibt die Farbwelt
              'Herbst': 'an autumn evening with a few falling leaves', 'Winter': 'a winter night with snow outside and candlelight inside'}
# Farbwelt je Vorschlag (Oberchef 28.10.: «Rudis echte Rückseiten wechseln die Farbwelt kräftig»): vorn und hinten dieselbe, die Vorschläge eines Abends klar verschieden
FARBWELTEN = {
    'Herbst': ['copper and burnt orange with warm amber', 'deep fir green with brass and cream', 'plum and violet with dusty rose', 'midnight blue with gold'],
    'Sommer': ['turquoise and coral', 'lemon yellow and sky blue', 'flamingo pink and jungle green', 'deep ultramarine with white and gold'],
    'Winter': ['ice blue and silver', 'bottle green and gold', 'deep burgundy and cream', 'violet night with silver glitter'],
    'Frühling': ['sage green and cream', 'blossom pink and mint', 'lemon yellow and lavender', 'turquoise and terracotta'],
    None: ['deep turquoise and amber', 'rose pink and jungle green', 'violet and silver', 'emerald green and cream'],
}


def farbwelt(thema, konzept, nr):
    l = FARBWELTEN[jahreszeit_aus(thema + ' ' + konzept)]
    return l[nr % len(l)]


IDEEN = [
    'IDEA: the dishes and drinks of the evening, oversized and gleaming, stand in the landscape like monuments, tiny elegant 1960s guests stroll between them',
    'IDEA: an elegant animal host in a tailored suit serves exactly these dishes and drinks at a beautifully laid table; its head stays well below the top quarter',
    'IDEA: a still life where the dishes become the landscape itself (hills, paths, a river of the drink), seen from slightly above',
    'IDEA: a 1960s travel poster where the dishes and drinks are the destination: a stylish couple arrives by vintage car at a table set with them',
    'IDEA: a theatre stage in the open air where the dishes and drinks are the stars under a single spotlight, low in the picture',
]


def _gerichte(konzept):
    return [t.strip() for t in re.split(r',|\bund\b|\bmit\b|&|\+|;|/', str(konzept or '')) if t.strip()]


def bildauftrag(thema, konzept, gast, nr):
    jz = jahreszeit_aus(thema + ' ' + konzept)
    g = _gerichte(konzept)
    teile = [STIL,
             f"MAIN SUBJECT, clearly recognisable and painted as part of the illustration (not like a food photograph): {', '.join(g)}." if g else '',
             f'Evening theme: {thema}.' if thema else '',
             f'Setting: {SAISON_ORT[jz]}.' if jz else '',
             f'Hint at the guest chef ({gast}) only through objects, never as a portrait.' if gast else '',
             IDEEN[nr % len(IDEEN)] + '.',
             f'COLOUR WORLD, used boldly for sky, walls, fabrics and light: {farbwelt(thema, konzept, nr)}.']
    return ' '.join(t for t in teile if t)


# Rückseite wie Rudis echte: ein ruhiges Begleitbild mit eigener Szene in der Farbwelt des Vorschlags, kein Teller auf dunklem Tisch
RUECK_SZENE = ['candles, a few old books and a single glass of the drink on a velvet table', 'a lush jungle of large leaves with an elegant animal half hidden in it',
               'a dreamy evening sky with a glittering cloud and a crescent moon above quiet rooftops', 'hand-painted tiles with a vase of seasonal flowers and one glass',
               'a quiet window at night with heavy curtains, a single candle and the drink on the sill']


def rueckauftrag(thema, konzept, nr):
    """Begleitbild der Rückseite (1:1) wie die echten: still, satt, in der Farbwelt des Vorschlags, je Vorschlag eine eigene Szene; dunkle ruhige Flächen dort, wo die Schrift steht."""
    g = _gerichte(konzept)
    teile = [RUECK, f'Companion image to an evening about: {thema}.' if thema else '',
             'Scene: ' + RUECK_SZENE[nr % len(RUECK_SZENE)] + '. No plate of food in the picture; at most one small hint of the evening' + (f" ({g[-1]})" if g else '') + '.',
             f'COLOUR WORLD, dominant and saturated: {farbwelt(thema, konzept, nr)}.']
    return ' '.join(t for t in teile if t)


def jahreszeit_aus(text):
    t = str(text or '').lower()
    for jz, worte in JAHRESZEIT_WORTE.items():
        if any(w in t for w in worte):
            return jz
    return None


def vorschlaege(daten):
    thema = str(daten.get('thema') or '').strip()[:120]
    konzept = str(daten.get('konzept') or '').strip()[:600]
    gast = str(daten.get('gast') or '').strip()[:60]
    if len(thema + konzept) < 3:
        raise ValueError('THEMA · Bitte ein Thema oder ein paar Worte zum Abend eingeben.')
    zahl = max(3, min(5, int(daten.get('zahl') or 4)))
    monat = int(str(daten.get('monat') or '0') or 0)
    motive = [m for m in json.load(open(MOTIVE, encoding='utf-8')) if not m.get('schrift')]
    woerter = _w(thema + ' ' + konzept)
    jahreszeit = jahreszeit_aus(thema + ' ' + konzept) or JAHR.get(monat)
    passend = [m for m in motive if m['schlagworte'].get('jahreszeit') == jahreszeit]
    if len(passend) >= zahl:   # Sommer heisst Sommermotive (Robert 28.10.: drei Wintermotive für einen Sommerabend)
        motive = passend
    def punkte(m):
        s = m['schlagworte']
        text = ' '.join([m['titel'], s.get('thema', ''), s.get('farbe', ''), s.get('stimmung', ''), s.get('jahreszeit', '')]).lower()
        p = sum(3 for w in woerter if w in text)
        if jahreszeit and s.get('jahreszeit') == jahreszeit:
            p += 2
        if not m.get('schrift'):
            p += 1.5
        if m.get('quelle') == 'ki':
            p += 1
        return p
    gewaehlt = sorted(motive, key=lambda m: -punkte(m))[:zahl]
    def treffer(m):
        s_ = m['schlagworte']; t = ' '.join([m['titel'], s_.get('thema', '')]).lower()
        return any(w in t for w in woerter if not jahreszeit_aus(w))
    titel = (thema or konzept.split('.')[0])[:40]
    aus = []
    for i, m in enumerate(gewaehlt):
        aus.append(dict(motiv=m['key'], titel=titel, akzent=m.get('akzent') or '#ef7649', schrift=bool(m.get('schrift')),
                        bildauftrag=bildauftrag(thema, konzept, gast, i),
                        treffer=treffer(m),
                        warum=f"Motiv «{m['titel']}» · {m['schlagworte'].get('jahreszeit', '')} · {m['schlagworte'].get('stimmung', '')}"))
    return aus


def schluessel():
    """(Key-ID, Secret, Modell) aus der Umgebung oder ~/.config/tasty/higgsfield.env; None, solange Robert keinen eingetragen hat."""
    w = {k: os.environ.get(k, '') for k in ('HF_API_KEY_ID', 'HF_API_KEY_SECRET', 'HF_BILDMODELL', 'HF_REFERENZ_FELD')}
    if os.path.exists(SCHLUESSEL):
        for z in open(SCHLUESSEL, encoding='utf-8'):
            if '=' in z and not z.lstrip().startswith('#'):
                k, v = z.split('=', 1)
                if k.strip() in w and not w[k.strip()]:
                    w[k.strip()] = v.strip().strip('"\'')
    if ':' in w['HF_API_KEY_ID'] and not w['HF_API_KEY_SECRET']:   # «Copy API key» der Higgsfield-Konsole liefert einen Schlüssel «Key-ID:Secret» (29.10.)
        w['HF_API_KEY_ID'], w['HF_API_KEY_SECRET'] = w['HF_API_KEY_ID'].split(':', 1)
    if not (w['HF_API_KEY_ID'] and w['HF_API_KEY_SECRET']):
        return None
    return w['HF_API_KEY_ID'], w['HF_API_KEY_SECRET'], w['HF_BILDMODELL'] or MODELL, w['HF_REFERENZ_FELD']


FUELL = {'mit', 'und', 'der', 'die', 'das', 'ein', 'eine', 'einen', 'für', 'zum', 'zur', 'am', 'im', 'von', 'dem', 'den', 'des', 'auf'}


def _schluessel_text(t):
    return {w for w in re.sub(r'[^a-z0-9äöüß]+', ' ', str(t or '').lower()).split() if len(w) > 1 and w not in FUELL}


def gespeichert(daten):
    """Schon erzeugter Abend mit denselben Worten (Thema, Konzept, Gastkoch): kommt ohne neue Kosten wieder."""
    f = os.path.join(ABENDE, 'abende.json')
    if not os.path.exists(f):
        return None
    such = _schluessel_text(' '.join(str(daten.get(k) or '') for k in ('thema', 'konzept', 'gast')))
    for a in json.load(open(f, encoding='utf-8')):
        if _schluessel_text(' '.join(a.get(k, '') for k in ('thema', 'konzept', 'gast'))) == such:
            return a
    return None


def _zaehler():
    heute = date.today().isoformat()
    try:
        z = json.load(open(ZAEHLER, encoding='utf-8'))
    except Exception:
        z = {}
    return z if z.get('datum') == heute else {'datum': heute, 'bilder': 0, 'geraete': {}}


def _zaehlen(z):
    os.makedirs(os.path.dirname(ZAEHLER), exist_ok=True)
    json.dump(z, open(ZAEHLER, 'w', encoding='utf-8'))


def grenze(geraet, durchgang, bilder=2):
    """Prüft und bucht: je Gerät GRENZEN['durchgaenge_je_geraet'] Durchgänge am Tag, gesamt GRENZEN['bilder_je_tag'] Bilder. Gibt eine Meldung zurück oder None."""
    with SPERRE:
        return _grenze(geraet, durchgang, bilder)


def _grenze(geraet, durchgang, bilder):
    z = _zaehler(); g = z['geraete'].setdefault(geraet or '?', [])
    if durchgang not in g and len(g) >= GRENZEN['durchgaenge_je_geraet']:
        return f"Heute sind auf diesem Gerät schon {GRENZEN['durchgaenge_je_geraet']} Durchgänge mit KI gelaufen. Morgen geht es wieder; bis dahin Motive aus der Sammlung."
    if z['bilder'] + bilder > GRENZEN['bilder_je_tag']:
        return 'Für heute sind alle Bilder dieser Vorschau vergeben. Morgen geht es wieder; bis dahin Motive aus der Sammlung.'
    if durchgang not in g:
        g.append(durchgang)
    z['bilder'] += bilder; _zaehlen(z)
    return None


def _hf(pfad, daten, s, methode='POST', kennung=None):
    kopf = {'Authorization': f'Key {s[0]}:{s[1]}', 'Content-Type': 'application/json', 'Accept': 'application/json'}
    if kennung:
        kopf['Idempotency-Key'] = kennung   # gleicher Auftrag noch einmal gesendet: Higgsfield erzeugt und berechnet ihn nur einmal
    req = urllib.request.Request(pfad if pfad.startswith('http') else API + '/' + pfad.lstrip('/'), method=methode,
                                 data=json.dumps(daten).encode('utf-8') if daten is not None else None, headers=kopf)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or b'{}')


def referenzen(s):
    """Rudis Stilvorlagen einmal zu Higgsfield laden (files/generate-upload-url, PUT) und die öffentlichen Adressen merken."""
    try:
        c = json.load(open(REFERENZ_CACHE, encoding='utf-8'))
        if c.get('keys') == REFERENZEN and c.get('urls'):
            return c['urls']
    except Exception:
        pass
    urls = []
    for k in REFERENZEN:
        f = os.path.join(HAUS, 'bilder', k + '.webp')
        if not os.path.exists(f):
            continue
        u = _hf('files/generate-upload-url', {'content_type': 'image/webp'}, s)
        req = urllib.request.Request(u['upload_url'], data=open(f, 'rb').read(), method='PUT', headers=u.get('upload_headers') or {'Content-Type': 'image/webp'})
        with urllib.request.urlopen(req, timeout=60):
            pass
        urls.append(u['public_url'])
    os.makedirs(os.path.dirname(REFERENZ_CACHE), exist_ok=True)
    json.dump({'keys': REFERENZEN, 'urls': urls}, open(REFERENZ_CACHE, 'w', encoding='utf-8'))
    return urls


def bild_erzeugen(auftrag, verhaeltnis, s, warten=240, refs=None):
    """Ein Bild über die Higgsfield-API: Auftrag (mit Rudis Stilvorlagen) abschicken, Status abfragen, Bild holen. Gibt die Bytes zurück.
    Feldname der Vorlagen je Modell verschieden: HF_REFERENZ_FELD in der Schlüsseldatei, sonst «image_urls»; nimmt das Modell keine Vorlagen, Meldung REFERENZ."""
    if any(s[2].startswith(g) for g in GESPERRT):
        raise RuntimeError('MODELL · ' + s[2] + ' kopiert Rudis Plakate und ist gesperrt. HF_BILDMODELL in der Schlüsseldatei ändern.')
    daten = dict({'prompt': auftrag, 'aspect_ratio': verhaeltnis}, **MODELL_FELDER.get(s[2], {}))
    if refs:
        daten[os.environ.get('HF_REFERENZ_FELD') or s[3] or 'image_urls'] = refs
    kennung = hashlib.sha1(f'{auftrag}-{verhaeltnis}-{time.time()}'.encode()).hexdigest()
    try:
        for versuch in range(3):   # Netzfehler beim Abschicken: mit derselben Kennung neu senden (29.10.)
            try:
                r = _hf(s[2], daten, s, kennung=kennung)
                break
            except urllib.error.HTTPError:
                raise
            except (urllib.error.URLError, TimeoutError, OSError):
                if versuch == 2:
                    raise
                time.sleep(3)
    except urllib.error.HTTPError as e:
        if refs and e.code in (400, 422):
            raise RuntimeError('REFERENZ · Das Bildmodell nimmt Rudis Stilvorlagen so nicht an (' + e.read().decode('utf-8', 'replace')[:120] + ').')
        raise
    url = r.get('status_url') or f"{API}/requests/{r.get('request_id')}/status"
    ende = time.time() + warten
    while True:
        if r.get('status') == 'completed' and r.get('images'):
            for versuch in range(4):   # Bild holen, bei Netzfehler bis zu dreimal neu
                try:
                    with urllib.request.urlopen(r['images'][0]['url'], timeout=60) as b:
                        return b.read()
                except (urllib.error.URLError, TimeoutError, OSError):
                    if versuch == 3:
                        raise
                    time.sleep(3)
        if r.get('status') in ('failed', 'nsfw', 'canceled'):
            raise RuntimeError('KI · Das Bild ist nicht entstanden (' + str(r.get('error') or r.get('status'))[:80] + ').')
        if time.time() > ende:
            raise RuntimeError('KI · Das Bild braucht zu lange.')
        time.sleep(3)
        try:
            r = _hf(url, None, s, 'GET')
        except (urllib.error.URLError, TimeoutError, OSError) as e:   # kurzer Netz- oder Serverfehler beim Nachfragen: weiter warten, das Bild entsteht trotzdem (29.10.)
            if isinstance(e, urllib.error.HTTPError) and e.code < 500 and e.code != 429:
                raise


def schrift(roh):
    """True, wenn das Bildmodell Schrift ins Bild gemalt hat (Signatur, Bildunterschrift, Scheinbuchstaben); Prüfung mit macOS Vision (api/schrift)."""
    prog = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schrift')
    if not os.path.exists(prog):
        return False
    import subprocess, tempfile
    with tempfile.NamedTemporaryFile(suffix='.png') as t:
        t.write(roh); t.flush()
        try:
            aus = subprocess.run([prog, t.name], capture_output=True, text=True, timeout=60).stdout
        except Exception:
            return False
    return any(len(re.sub(r'[^0-9A-Za-zÄÖÜäöüß]', '', z.split('\t')[-1])) >= 3 for z in aus.splitlines())


VORSCHAU = os.path.join(HAUS, 'vorschau')   # 600 px breit für die Liste «Alle Vorschläge» (2×), mit Cache-Header ausgeliefert
ZWISCHEN = os.path.join(HIER, 'api', '_daten', 'plakat-vorschau.json')   # Masse, Motivfarbe, Kopfzonen-Messung je Bild: die Liste antwortet ohne ein Bild zu öffnen
ZW_SPERRE = threading.Lock()


def _zwischen():
    try:
        return json.load(open(ZWISCHEN, encoding='utf-8'))
    except Exception:
        return {}


def _zwischen_merken(k, wert):
    with ZW_SPERRE:
        c = _zwischen(); c[k] = wert; t = ZWISCHEN + '.neu'
        json.dump(c, open(t, 'w', encoding='utf-8'), ensure_ascii=False); os.replace(t, ZWISCHEN)


def ablegen(roh, key, alt):
    """Bild als Foto des Hauses ablegen (bilder/ und mini/ wie bau.py); gibt den Eintrag für M.bilder zurück.
    Dazu einmal beim Entstehen die Vorschau (WebP, 600 px breit) und die Motivfarbe für den Platzhalter; danach liest die Liste nur noch den Zwischenspeicher
    (Robert 29.10.2026: die Vorschläge «brauchen ewig zum Laden», 23 s für acht Vorschläge, weil jedes Bild neu geöffnet wurde)."""
    ziel, vz = os.path.join(HAUS, 'bilder', key + '.webp'), os.path.join(VORSCHAU, key + '.webp')
    e = _zwischen().get('bild:' + key)
    if not (e and os.path.exists(ziel) and os.path.exists(vz)):
        from PIL import Image
        im = Image.open(io.BytesIO(roh) if isinstance(roh, bytes) else roh).convert('RGB')
        if not os.path.exists(ziel):
            im.save(ziel, 'WEBP', quality=90, method=5)
            k = im.copy(); k.thumbnail((520, 520)); k.save(os.path.join(HAUS, 'mini', key + '.webp'), 'WEBP', quality=74, method=5)
        os.makedirs(VORSCHAU, exist_ok=True)
        v = im.copy(); v.thumbnail((600, 100000)); v.save(vz, 'WEBP', quality=82, method=5)
        f = im.resize((1, 1), Image.BOX).getpixel((0, 0))
        e = {'w': im.width, 'h': im.height, 'farbe': '#%02x%02x%02x' % f, 'v': int(os.path.getmtime(vz))}
        _zwischen_merken('bild:' + key, e)
    return {'key': key, 'alt': alt, 'w': e['w'], 'h': e['h'], 'gruppe': 'Plakat-Motive', 'vorschau': f"vorschau/{key}.webp?v={e['v']}", 'farbe': e['farbe']}


def _metadaten(vorn, hinten, vk, hk, titel, auftrag, rauftrag, quelle):
    stand = [os.path.getmtime(vorn), os.path.getmtime(hinten)] if os.path.exists(vorn) and os.path.exists(hinten) else None
    z = _zwischen().get('kopf:' + vk)   # Kopfzonen-Messung einmal je Bild (29.10.: die Liste rechnete sie bei jedem Aufruf neu)
    if z and stand and z.get('stand') == stand:
        k, r, kr = z['k'], z['r'], z['kr']
    else:
        k = kopfzone.pruefe(vorn) if kopfzone else {'farbe': 'weiss', 'frei': True}
        r = kopfzone.rueckseite(hinten) if kopfzone else {'dunkel': False}
        kr = kopfzone.rudi_kopf(vorn) if kopfzone and hasattr(kopfzone, 'rudi_kopf') else {'farbe': '#d6262b', 'schatten': 'dunkel'}   # Kopfzeile wie Rudi (29.10.)
        if stand:
            _zwischen_merken('kopf:' + vk, {'stand': stand, 'k': {'farbe': k.get('farbe'), 'frei': bool(k.get('frei'))}, 'r': {'dunkel': bool(r.get('dunkel'))}, 'kr': {'farbe': kr['farbe'], 'schatten': kr['schatten']}})
    return dict(motiv=vk, rueck=hk, kopf_farbe=k.get('farbe') or 'weiss', kopf_frei=bool(k.get('frei')), rueck_dunkel=bool(r.get('dunkel')), kopf_rudi=dict(farbe=kr['farbe'], schatten=kr['schatten']),
                akzent='#ef7649', titel=titel, bildauftrag=auftrag, rueckauftrag=rauftrag, warum=quelle)


def neu_vorschlag(daten):
    """Ein Vorschlag (nr) mit neuem Motiv vorn und hinten: gespeicherter Abend, sonst live über die API (Grenzen, Kopfzonen-Prüfung)."""
    thema = str(daten.get('thema') or '').strip()[:120]; konzept = str(daten.get('konzept') or '').strip()[:600]; gast = str(daten.get('gast') or '').strip()[:60]
    nr = max(0, min(4, int(daten.get('nr') or 0))); titel = (thema or konzept.split('.')[0])[:40]
    g = gespeichert(daten)
    if g and nr < len(g['vorschlaege']):
        v = g['vorschlaege'][nr]; vk, hk = f"ab_{g['id']}_{nr + 1}", f"abr_{g['id']}_{nr + 1}"
        vf, hf = os.path.join(ABENDE, v['vorn']), os.path.join(ABENDE, v['hinten'])
        bilder = [ablegen(vf, vk, f'{titel}, Vorschlag {nr + 1} (KI)'), ablegen(hf, hk, f'{titel}, Vorschlag {nr + 1}, Rückseite (KI)')]
        time.sleep(1.2)   # gespeichert: kommt sofort, nur kurz sichtbar «entsteht»
        m = _metadaten(vf, hf, vk, hk, titel, v['bildauftrag'], v['rueckauftrag'], f"Neu erzeugt für «{g['thema']}» · GPT Image 2.5"); m['idee'] = v.get('idee', '')
        return {'vorschlag': m, 'bilder': bilder, 'ki': True}
    s = schluessel()
    if not s:
        raise RuntimeError('KI-FREIGABE · Für neue Motive fehlt am Server der Schlüssel. Die Vorschläge kommen aus der Motiv-Sammlung.')
    meldung = grenze(str(daten.get('geraet') or '')[:40], str(daten.get('durchgang') or '')[:40], bilder=2)   # vorn und hinten; eine Wiederholung bucht ihr Bild erst, wenn sie gebraucht wird (Robert 29.10.: Vorschlag 3 und 4 abgewiesen)
    if meldung:
        raise RuntimeError('GRENZE · ' + meldung)
    k = daten.get('entwurf') if isinstance(daten.get('entwurf'), dict) and daten['entwurf'].get('bild') else None
    if not k:   # Konzept der Anfrage (gleiche Mischung wie im Plan)
        zahl = max(3, min(5, int(daten.get('zahl') or 4)))
        k = KZ.konzepte(thema, konzept, gast, zahl, FARBWELTEN[jahreszeit_aus(thema + ' ' + konzept)])[0][nr % zahl]
    k = {x: str(k.get(x) or '')[:600] for x in ('idee', 'witz', 'bild', 'rueck', 'farbwelt')}
    jz = jahreszeit_aus(thema + ' ' + konzept)
    auftrag, rauftrag = KZ.bildauftrag(k, thema, SAISON_ORT.get(jz, '')), KZ.rueckauftrag(k, thema)
    refs = referenzen(s) if STILREFERENZ else None
    originale = os.path.join(HAUS, 'bilder')
    andere = FARBEN.setdefault(str(daten.get('durchgang')), {})   # Farbwelten der übrigen Vorschläge dieses Durchgangs
    def eigen(roh, seite):   # klar andere Farbwelt als die übrigen Vorschläge (Abstand ≥ GRENZE_FARBE)
        if not kopfzone:
            return True
        f = kopfzone.farbwelt(io.BytesIO(roh))
        ok = all(kopfzone.farbabstand(f, x[seite]) >= kopfzone.GRENZE_FARBE for k, x in andere.items() if k != nr and seite in x)
        andere.setdefault(nr, {})[seite] = f
        return ok
    vorn, versuche, naehe, gebucht = None, {'vorn': 0, 'hinten': 0}, (0, None), [2]
    def noch_eins():   # Wiederholung nur, wenn die Tagesgrenze noch ein Bild hergibt; sonst bleibt das erste Bild
        with SPERRE:
            z = _zaehler()
            if z['bilder'] + 1 > GRENZEN['bilder_je_tag']:
                return False
            z['bilder'] += 1; _zaehlen(z); gebucht[0] += 1
            return True
    try:
        for i in range(2):   # einmal neu, wenn etwas in der Kopfzone steht oder die Farbwelt einem anderen Vorschlag gleicht
            if i and not noch_eins():
                break
            vorn = bild_erzeugen(auftrag, VORN_FORMAT.get(s[2], '4:3'), s, refs=refs); versuche['vorn'] += 1
            naehe = kopfzone.naehe(io.BytesIO(vorn), originale) if kopfzone else (0, None)
            if (not kopfzone or (kopfzone.pruefe(io.BytesIO(vorn))['frei'] and naehe[0] < kopfzone.GRENZE_NAEHE)) and eigen(vorn, 'vorn') and not schrift(vorn):   # frei, lesbar, keinem Original zu nah, eigene Farbwelt, keine gemalte Schrift
                break
        for i in range(2):
            if i and not noch_eins():
                break
            hinten = bild_erzeugen(rauftrag, '1:1', s, refs=refs); versuche['hinten'] += 1
            if eigen(hinten, 'hinten') and not schrift(hinten):
                break
    finally:   # gebucht und nicht entstanden (Abbruch, Fehler): geht an die Tagesgrenze zurück
        with SPERRE:
            z = _zaehler(); z['bilder'] = max(0, z['bilder'] - (gebucht[0] - versuche['vorn'] - versuche['hinten'])); _zaehlen(z)
    h = hashlib.sha1(f"{daten.get('durchgang')}-{nr}-{time.time()}".encode()).hexdigest()[:10]
    vk, hk = 'ki_' + h, 'kir_' + h
    bilder = [ablegen(vorn, vk, f'{titel}, Vorschlag {nr + 1} (KI)'), ablegen(hinten, hk, f'{titel}, Vorschlag {nr + 1}, Rückseite (KI)')]
    vf, hf = os.path.join(HAUS, 'bilder', vk + '.webp'), os.path.join(HAUS, 'bilder', hk + '.webp')
    m = _metadaten(vf, hf, vk, hk, titel, auftrag, rauftrag, 'Neu erzeugt für diesen Abend · KI'); m['idee'] = k['idee']
    m.update(versuche=versuche, naehe=naehe[0], naehe_zu=naehe[1], modell=s[2], witz=k['witz'], farbwelt=k['farbwelt'])
    return {'vorschlag': m, 'bilder': bilder, 'ki': True}


def alle():
    """Alle schon entstandenen Abende mit ihren Vorschlägen, vorn und hinten, für die Werkstatt («die vorschläge bitte direkt im tool alle anzeigen», Robert
    29.10.2026). Ohne neue Kosten; abgelöste erste Fassungen bleiben im Archiv und erscheinen nicht."""
    f = os.path.join(ABENDE, 'abende.json')
    if not os.path.exists(f):
        return {'abende': [], 'bilder': []}
    abende, bilder = [], []
    for g in json.load(open(f, encoding='utf-8')):
        if g['id'].endswith('erste-fassung'):
            continue
        titel = g['thema'][:40]; vs = []
        for nr, v in enumerate(g['vorschlaege']):
            vk, hk = f"ab_{g['id']}_{nr + 1}", f"abr_{g['id']}_{nr + 1}"
            vf, hf = os.path.join(ABENDE, v['vorn']), os.path.join(ABENDE, v['hinten'])
            bilder += [ablegen(vf, vk, f'{titel}, Vorschlag {nr + 1} (KI)'), ablegen(hf, hk, f'{titel}, Vorschlag {nr + 1}, Rückseite (KI)')]
            m = _metadaten(vf, hf, vk, hk, titel, v['bildauftrag'], v['rueckauftrag'], f"Neu erzeugt für «{g['thema']}» · GPT Image 2.5"); m['idee'] = v.get('idee', '')
            vs.append(m)
        abende.append({'id': g['id'], 'thema': g['thema'], 'konzept': g.get('konzept', ''), 'gast': g.get('gast', ''), 'wochenende': g.get('wochenende', ''),
                       'erzeugt': g.get('erzeugt', ''), 'vorschlaege': vs})
    return {'abende': abende[::-1], 'bilder': bilder}   # zuerst der zuletzt angelegte


HINWEIS_OHNE = ('Neue Motive entstehen hier für jede Anfrage, sobald der Higgsfield-Schlüssel am Server liegt '
                '(~/.config/tasty/higgsfield.env). Bis dahin zeigt die Werkstatt keine fertigen Motive als Ersatz.')


def antwort(daten, live=False):
    """Plan (ohne nr): je Vorschlag ein eigenes Konzept (Idee, Bildwitz, Farbwelt) und ob die Bilder entstehen können. Mit nr: ein neuer Vorschlag, vorn und hinten.
    Robert 28.10.2026: «pro Anfrage 3 4 oder 5 … an neuen» und «komplett neue und weitergedachte konzepte» — nie vorhandene Motive als Vorschläge."""
    if daten.get('nr') is not None:
        return neu_vorschlag(daten)
    vorschlaege(daten)   # prüft die Eingabe
    thema = str(daten.get('thema') or '').strip()[:120]; konzept = str(daten.get('konzept') or '').strip()[:600]; gast = str(daten.get('gast') or '').strip()[:60]
    zahl = max(3, min(5, int(daten.get('zahl') or 4)))
    g = gespeichert(daten)
    if g:
        v = [dict(idee=x.get('idee', ''), bildauftrag=x['bildauftrag'], entwurf=None) for x in g['vorschlaege'][:zahl]]
        return {'vorschlaege': v, 'live': True, 'konzepte': 'gespeichert', 'hinweis': HINWEIS_LIVE}
    jz = jahreszeit_aus(thema + ' ' + konzept)
    ks, quelle = KZ.konzepte(thema, konzept, gast, zahl, FARBWELTEN[jz])
    v = [dict(idee=k['idee'], witz=k.get('witz', ''), bildauftrag=KZ.bildauftrag(k, thema, SAISON_ORT.get(jz, '')), entwurf=k) for k in ks]
    neu = live and bool(schluessel())
    return {'vorschlaege': v, 'live': neu, 'konzepte': quelle, 'hinweis': HINWEIS_LIVE if neu else HINWEIS_OHNE}
