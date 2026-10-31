"""Plakatwerkstatt · Konzept je Vorschlag (Oberchef 28.10.2026 nach Robert: «die vorlagen die wir haben nehmen wir als grundlage zum verständnis aber entwickeln
auf der grundlage komplett neue und weitergedachte konzepte … mit jedem plakat komplett neue und zu dem konzept passende richtung … basieren auf den stil grundlagen»).

Vor jedem Bild entsteht eine eigene Bildidee aus Thema, Gerichten, Drinks und Gastkoch. Die Ideen einer Anfrage unterscheiden sich in Bildwitz, Figur und
Farbwelt; keine wiederholt eines der 13 echten Plakate (BESTAND). Stilgrundlagen: stil/stilgrundlagen.md (Kurzform STIL_EN unten).
- Mit Claude (Schlüssel in ~/.config/tasty/anthropic.env oder ANTHROPIC_API_KEY am Server, Modell Haiku 5.5): das Sprachmodell denkt die Ideen weiter.
- Ohne Schlüssel (Probe, auch in allen Prüfläufen): Ideen nach festen Regeln aus Bildwitz-Mustern, Figuren und Farbwelten, je Anfrage gemischt."""
import hashlib, json, os, re, urllib.error, urllib.request

# Kurzform der Stilgrundlagen für den Bildauftrag (stil/stilgrundlagen.md)
STIL_EN = ('A hand-painted mid-century gouache painting, a pure picture without any lettering: gouache and oil painting look with soft brushwork and a '
           'slightly faded printed texture, or cut-out vintage figures on a painted ground. A flat, calm background: one strong wall colour, often with a floor in a '
           'second colour meeting it at one clean edge, or a stage curtain, a plain sky, snow or sand. Only two or three elements: one glamorous figure of the 1920s to '
           '1960s or one animal behaving like a guest, one oversized glass or dish, at most one small extra. Exactly one surreal idea, deliberately wrong scale. '
           'Flat, even light or a single spotlight or candlelight. No photographic look, no glossy rendered food, no cinematic glow, no orange-and-teal grading, '
           'no depth of field, no busy scenery, no crowds, no tables full of plates.')
BESTAND = ('a cat climbing into a cocktail glass', 'legs sticking out of a chequered floor under framed Campari posters', 'a man on a ladder pouring a martini',
           'a showgirl sitting in a giant coupe on stage', 'a giant water tap pouring a cocktail', 'an elephant in a snow globe next to a deer gentleman',
           'a Fiat and a Vespa under an orange sun', 'a skier with a cable car of glasses', 'a woman on a red throne with a panther',
           'a pin-up watering asparagus', 'a pin-up sitting on a pumpkin among candles', 'a black panther eating a spaghetti ice cream',
           'a dancer on a crescent moon')
DRINK_WORTE = ('wein', 'cocktail', 'drink', 'gin', 'whisky', 'whiskey', 'rum', 'bier', 'sekt', 'champagner', 'prosecco', 'punsch', 'spritz', 'negroni', 'martini',
               'tequila', 'mezcal', 'sake', 'tee', 'kaffee', 'espresso', 'portwein', 'sherry', 'cidre', 'aperitif', 'likör', 'saft', 'limonade', 'wasser')

# Bildwitz-Muster für die Probe: (Witz, Idee deutsch, Bild englisch, Rückseite englisch). {D} Hauptgericht, {D2} zweites Gericht, {G} Drink, {F} Figur
MUSTER = [
    ('Massstab', '{D} als Ozeandampfer, {D2} als Möwen darüber',
     'a giant {D} sailing like an ocean liner on a calm sea of {G}, small {D2} flying above it like seagulls, {F} waving from the deck',
     'a ship porthole at night with a single glass of {G} on its rim'),
    ('Tier als Gast', '{T} im Frack serviert auf einem Silbertablett: {D}',   # Bestandteil nie als Objekt oder hinter Präposition, sonst falsche Endung (29.10.)
     '{T} in a tailcoat proudly serving {D} on a silver tray, a glass of {G} balanced on its head, standing on a plain floor',
     'a silver tray with an empty glass and a folded white napkin, quiet and still'),
    ('Bühne', '{D} in Übergrösse auf der Bühne, {F} balanciert darauf, ein Glas {G} als Scheinwerfer',
     'a stage with a plain curtain, {F} balancing gracefully on top of a giant {D}, an oversized glass of {G} hanging above like a spotlight',
     'a closed stage curtain with a single spotlight on one glass of {G}'),
    ('Fremdkörper', 'Aus einem Grammophon fliesst {G}, auf dem Plattenteller: {D}',
     'an old gramophone whose horn pours {G} into a glass, a {D} spinning on the turntable like a record, {F} dancing beside it',
     'a gramophone horn with a few musical notes made of drops of {G}'),
    ('Reise', '{F} rudert über einen stillen See, das Boot: {D}, das Wasser: {G}',
     '{F} rowing a little boat made of {D} across a calm lake of {G}, a single {D2} floating like a buoy',
     'a quiet jetty at dusk with a rowing boat and one glass of {G} on the planks'),
    ('Massstab', '{D} als Luftschiff über der Stadt, {F} winkt aus der Gondel',
     'a {D} floating like an airship over a small painted town, {F} waving from a gondola that is a glass of {G}',
     'a night sky with one small airship far away and the moon'),
]
FIGUREN = ['ein Kapitän der 1950er', 'eine Revuetänzerin', 'ein Herr im Smoking', 'eine Schwimmerin im Badeanzug der 1950er', 'eine Diva mit Fächer',
           'ein Liftboy', 'eine Fliegerin mit Brille', 'ein Zauberer mit Zylinder']
FIGUREN_EN = ['a 1950s sea captain', 'a revue dancer', 'a gentleman in a dinner jacket', 'a 1950s swimmer in a bathing suit', 'a diva with a feather fan',
              'a bellboy', 'an aviatrix with goggles', 'a magician in a top hat']
TIERE = [('Ein Flamingo', 'a flamingo'), ('Ein Eisbär', 'a polar bear'), ('Ein Pfau', 'a peacock'), ('Ein Fuchs', 'a fox'), ('Ein Pelikan', 'a pelican'),
         ('Ein Waschbär', 'a raccoon'), ('Ein Dachs', 'a badger')]


def _teile(konzept):
    # Füllwörter und Satzzeichen ab: aus «dazu ein gereifter Barolo.» wurde sonst «ein Boot aus dazu ein gereifter Barolo.» (29.10.)
    l = [t.strip(' .!?:') for t in re.split(r',|\bund\b|\bmit\b|&|\+|;|/|\.\s', str(konzept or ''))]
    l = [re.sub(r'^(?:(?:dazu|sowie|auch|danach|zum Schluss)\s+)?(?:(?:ein|eine|einen|einem|einer|der|die|das|den)\s+)?', '', t, flags=re.I) for t in l]
    return [t for t in l if t]


def _drink(t):
    return any(w in t.lower() for w in DRINK_WORTE)


def probe(thema, konzept, gast, zahl, farbwelten):
    """Konzepte nach Regeln: je Vorschlag ein anderes Bildwitz-Muster, eine andere Figur und Farbwelt; die Mischung hängt an der Anfrage."""
    t = _teile(konzept)
    gerichte = [x for x in t if not _drink(x)] or [thema or 'das Gericht des Abends']
    drinks = [x for x in t if _drink(x)] or ['Signature Drink']
    h = int(hashlib.sha1(f'{thema}|{konzept}|{gast}'.encode()).hexdigest(), 16)
    muster = sorted(range(len(MUSTER)), key=lambda i: (i * 7 + h) % 11)
    aus = []
    for n in range(zahl):
        m = MUSTER[muster[n % len(muster)]]
        fi = (h // 3 + n * 3) % len(FIGUREN); ti = (h // 5 + n * 2) % len(TIERE)
        D, G = gerichte[n % len(gerichte)], drinks[n % len(drinks)]
        D2 = gerichte[(n + 1) % len(gerichte)] if len(gerichte) > 1 else None   # nur ein Gericht: an zweiter Stelle Gläser des Drinks
        de = m[1].format(D=D, D2=D2 or 'Gläser', G=G, F=FIGUREN[fi], T=TIERE[ti][0])
        en = m[2].format(D=D, D2=D2 or f'little glasses of {G}', G=G, F=FIGUREN_EN[fi], T=TIERE[ti][1])
        if gast:
            en += f'; a white chef\'s toque on a hook at the edge as a nod to the guest chef {gast}'
        aus.append(dict(idee=de[0].upper() + de[1:], witz=m[0], bild=en, rueck=m[3].format(D=D, D2=D2 or G, G=G), farbwelt=farbwelten[n % len(farbwelten)], quelle='probe'))
    return aus


def mit_claude(thema, konzept, gast, zahl, farbwelten, modell, schluessel_wert):
    """Konzepte vom Sprachmodell (nur mit IMPRIMERIE_KI=1 und ANTHROPIC_API_KEY am Server)."""
    werkzeug = {'name': 'konzepte', 'description': 'Bildkonzepte für die Plakate eines Abends',
                'input_schema': {'type': 'object', 'required': ['konzepte'], 'properties': {'konzepte': {'type': 'array', 'items': {'type': 'object',
                    'required': ['idee', 'witz', 'bild', 'rueck'], 'properties': {
                        'idee': {'type': 'string', 'description': 'eine Zeile auf Deutsch, z. B. «Der Döner als Ozeandampfer, die Wings als Möwen»'},
                        'witz': {'type': 'string', 'description': 'Art des Bildwitzes: Massstab, Fremdkörper, Tier als Gast, Bühne, Reise …'},
                        'bild': {'type': 'string', 'description': 'die Bildidee auf Englisch für das Bildmodell, zwei bis drei Elemente, ruhiger Grund'},
                        'rueck': {'type': 'string', 'description': 'ruhiges Begleitbild der Rückseite zum selben Konzept, auf Englisch'}}}}}}}
    auftrag = (f'Entwirf {zahl} Bildkonzepte für die Plakate eines Abends im Culinarium Hannover (Tafel mit Menü und Signature Drinks). '
               f'Thema: {thema or "-"}. Gerichte und Drinks: {konzept or "-"}. Gastkoch: {gast or "keiner"}.\n'
               f'Stil (Korridor, nicht kopieren): {STIL_EN}\n'
               f'Diese Motive gibt es schon, keines davon wiederholen oder abwandeln: {"; ".join(BESTAND)}.\n'
               'Jedes Konzept denkt Thema, Gerichte und Drinks weiter, hat genau eine verrückte Idee mit falschem Massstab oder einem Fremdkörper, zwei bis drei '
               'Elemente, und unterscheidet sich von den anderen in Bildwitz und Figur. Die Gerichte bleiben erkennbar, gemalt, nie wie ein Food-Foto. '
               'Nichts, was nach Masse oder Abfertigung aussieht. Antworte nur über das Werkzeug «konzepte».')
    koerper = {'model': modell, 'max_tokens': 2500, 'tools': [werkzeug], 'tool_choice': {'type': 'auto'}, 'messages': [{'role': 'user', 'content': auftrag}]}
    req = urllib.request.Request('https://api.anthropic.com/v1/messages', data=json.dumps(koerper).encode('utf-8'), method='POST',
                                 headers={'content-type': 'application/json', 'x-api-key': schluessel_wert, 'anthropic-version': '2023-06-01',
                                          'anthropic-workspace-id': os.environ.get('ANTHROPIC_WORKSPACE_ID', '')})
    with urllib.request.urlopen(req, timeout=90) as r:
        antwort = json.loads(r.read())
    for b in antwort.get('content', []):
        if b.get('type') == 'tool_use':
            k = [x for x in b['input'].get('konzepte', []) if x.get('idee') and x.get('bild')][:zahl]
            for n, x in enumerate(k):
                x.update(farbwelt=farbwelten[n % len(farbwelten)], quelle='claude', rueck=x.get('rueck') or 'a calm detail of the same idea')
            if len(k) == zahl:
                return k
    raise RuntimeError('KONZEPT · Das Sprachmodell hat keine vollständigen Konzepte geliefert.')


MODELL = 'claude-haiku-5-5'   # günstigstes passende Claude-Modell für kurze Bildideen (Oberchef 28.10.)
SCHLUESSEL = os.path.expanduser('~/.config/tasty/anthropic.env')


def schluessel():
    """ANTHROPIC_API_KEY aus der Umgebung oder ~/.config/tasty/anthropic.env (chmod 600, nie im Browser); None, solange keiner eingetragen ist."""
    k = os.environ.get('ANTHROPIC_API_KEY', '')
    if not k and os.path.exists(SCHLUESSEL):
        for z in open(SCHLUESSEL, encoding='utf-8'):
            if z.strip().startswith('ANTHROPIC_API_KEY='):
                k = z.split('=', 1)[1].strip().strip('"\'')
    return k or None


def konzepte(thema, konzept, gast, zahl, farbwelten, modell=MODELL):
    """Claude, sobald ein Schlüssel am Server liegt (PLAKAT_KI=0 schaltet ab), sonst Probe nach Regeln. Gibt (liste, quelle) zurück."""
    k = schluessel()
    if k and os.environ.get('PLAKAT_KI', '1') != '0':
        try:
            return mit_claude(thema, konzept, gast, zahl, farbwelten, modell, k), 'claude'
        except Exception:
            pass
    return probe(thema, konzept, gast, zahl, farbwelten), 'probe'


def bildauftrag(k, thema, setting):
    """Bildauftrag aus Konzept und Stilblatt (vorn, 4:3), mit freier Kopfzone in der Farbwelt. Den Bestand schliesst das Konzept aus; im Bildauftrag
    nennt ihn nichts, weil eine Verbotsliste dem Bildmodell die Motive erst vorsagt."""
    return ' '.join(x for x in [
        STIL_EN,
        f'IMAGE IDEA: {k["bild"]}.',
        f'Evening theme: {thema}.' if thema else '',
        f'Setting: {setting}.' if setting else '',
        f'COLOUR WORLD, dominant, used for the background and fabrics: {k["farbwelt"]}.',
        'The top quarter of the image must stay a completely calm, empty area of the plain background in one even colour, very light or very dark, never a '
        'middle tone, with no objects, heads or details reaching into it; all subjects stay in the lower three quarters, without any seam or band. '
        'The main figure and the key objects sit together in the central half of the width, with calm background to the left and right, so the picture can '
        'also be shown in a tall narrow crop without cutting the figure.',   # hohe Formate (Story, DL hoch) zeigen nur die mittlere Hälfte (29.10.)
        'The picture contains no text, letters or marks of any kind.'] if x)


def rueckauftrag(k, thema):
    """Rückseite (1:1): ruhiges Begleitbild zum selben Konzept, Platz für die Schrift wie auf den echten Rückseiten."""
    return ' '.join(x for x in [
        STIL_EN,   # wie vorn: «back of the poster» und «typography» liessen das Bildmodell Scheinschrift malen (29.10.)
        f'IMAGE IDEA: {k["rueck"]}.',
        f'COLOUR WORLD, dominant and saturated: {k["farbwelt"]}.',
        'One single continuous picture, never split into panels, tiles or a grid. Generous calm, empty plain background in one deep, dark, even shade of the '
        'colour world, especially at the top left and along the bottom; the few main objects sit in the right half.',
        'The picture contains no text, letters or marks of any kind.'] if x)
