#!/usr/bin/env python3
"""Baut die Werkbank eines Hauses nach <Projekt>/werkbank/.   python3 bau.py "<Projektordner>"

Die Bausteine stammen aus der Werkbank des Carlton-Europe (von Robert angenommen). Jedes Haus bekommt daraus seine eigene Werkbank
(Robert 09.10.2026: vier gleich gebaute Werkbänke wirken kopiert): eigener Auftakt (AUFTAKT['art']: stapel · titelblatt · karte · weg),
eigene Reihenfolge (REIHENFOLGE), eigene Kapitelnamen und Titelzeilen (KAPITEL), Brief lang oder kurz, eigene Auslage beim Feed.
Alles Eigene des Hauses steht in <Projekt>/_werkbank/haus.py. Zahlen stehen nirgends von Hand, sie werden gezählt.
Seit 10.10.2026 (Robert, Carlton-Europe) gehören zu jeder Werkbank: kein Tor am Anfang · Bilder mit 40-px-Abbild als Hintergrund (K.VORAB, Klasse ld) ·
«Für Ihre Gäste» (H.GAESTE = [(bild, titel, satz, ausschnitt)], Bilder _werkbank/ansichten/Gaeste/<bild>.jpg; H.GAESTE_TEL = [(bild, unterschrift)] drei Handys,
lange Aufnahmen scrollen innen; H.GAESTE_KNOEPFE = [(text, href)]) · «Rezeption im Chat» (H.REZEPTION = [(titel, satz)], Film _werkbank/film/s-rezeption.mp4 + .jpg,
Bilder _werkbank/ansichten/Chat/{chat,rezeption,rezeption-2..,mappe,chat-h}.jpg, H.MAPPE_ADRESSE für den QR-Code, H.QR_KARTE = Bild der Karte (Pfad im Projekt),
H.REZEPTION_HINWEIS, H.REZEPTION_KARTEN = dict(mappe=(klein, titel, satz), karte=(klein, titel, satz), seite=(klein, titel, satz))) ·
«Geprüft» (H.GEPRUEFT = [(titel, zeichen, zeilen)], H.GEPRUEFT_OFFEN = Satz, H.GEPRUEFT_MEHR = [(titel, zeichen, einleitung, zeilen)] → werkbank/geprueft/index.html,
Zeichen: seite · karte · schloss · schild · auge; seit dem S&S-Stand vom 10.10.2026 als Collage, sobald H.GEPRUEFT_TRIO = [(bildschlüssel, b/h, lage, einkerbung)] ×3 und
H.GEPRUEFT_PUNKTE = [(titel, satz)] ×4 stehen (roter Stempel aus H.LEISTE + Stand, eigener Text über H.STEMPEL_TEXT, Farbe FARBEN['rot'] sonst 'punkt'); H.SCHLUSS['robert'] = False lässt das runde Profilbild im Schluss weg) · Studio mit Standbildern (H.STUDIO['bilder'] = [(name, beschriftung)], _werkbank/ansichten/Studio/<name>.jpg).
Ton: Sie-Form, Schweizer Schreibung, herzlich (Master «Website-Bau», Abschnitt 5)."""
import glob, json, os, shutil, subprocess
from PIL import Image
import kern as K
from kern import H, ROOT, W, e, PF, LI, RE, HZ, kn, titel, kap, kopf, zahl, slug

ZIEL = os.path.join(ROOT, 'werkbank')
IMG = os.path.join(ZIEL, 'img')
AN = os.path.join(W, 'ansichten')
os.makedirs(IMG, exist_ok=True)
ET = H.ETIKETTEN   # dict(ordner, name, einzahl)


def zaehle():
    z = {}
    z['haupt'] = len([s for s in H.SEITEN if not (len(s) > 4 and s[4] == 'recht')])
    u = K.lies('unterlagen.json', [])
    z['unterlagen'] = len(u)
    p = K.lies('papier.json', {'druck': [], 'etiketten': []})
    z['druck'] = len(p['druck']); z['etiketten'] = len(p['etiketten'])
    f = os.path.join(ROOT, 'feed', 'feed.json')
    z['feed'] = len(json.load(open(f))['posts']) if os.path.exists(f) else 0
    return z, p, u


def bilder(liste, papier, unterlagen):
    m = {}
    w = lambda quelle, name, breite, q=78, **kw: m.__setitem__(name, K.webp(quelle, os.path.join(IMG, name + '.webp'), breite, q, **kw))
    R, Ha = os.path.join(AN, 'Rechner'), os.path.join(AN, 'Handy')
    for datei, d in liste.items():
        s = slug(d['name'])
        for k in range(1, d['rechner'] + 1):
            w(os.path.join(R, d['name'] + ('' if k == 1 else f' {k}') + '.jpg'), f'{s}-{k}', 1280, 76)
        w(os.path.join(Ha, d['name'] + '.jpg'), f'{s}-h', 440, 78)
        for k in range(2, d['rechner'] + 1):
            q = os.path.join(Ha, d['name'] + f' {k}.jpg')
            w(q if os.path.exists(q) else os.path.join(Ha, d['name'] + '.jpg'), f'{s}-h{k}', 440, 78)
    w(os.path.join(R, 'Startseite.jpg'), 'auftakt', 2880, 84)   # doppelt so breit, wenn die Aufnahme es hergibt (Robert 11.10.2026: «viel schärfer»)
    w(os.path.join(Ha, 'Startseite.jpg'), 'auftakt-h', 520, 82)
    for v in getattr(H, 'VORHER', []):   # Vorher/Nachher je Seite (node _werkbank/vorher.js), doppelte Pixeldichte
        for t_ in ('alt', 'neu'):
            q = os.path.join(AN, 'Vorher', f'{v[0]}-{t_}.jpg')
            if os.path.exists(q): w(q, f'vh-{v[0]}-{t_}', 2880, 80)
    if os.path.exists(os.path.join(AN, 'Heute', 'Startseite.jpg')):
        w(os.path.join(AN, 'Heute', 'Startseite.jpg'), 'alt', 1440, 80)
    for name, quelle, breite, kw in getattr(H, 'EIGENE_BILDER', []):   # Fotos für die eigenen Abschnitte eines Hauses (H.EIGENE)
        w(K.hausbild(quelle), name, breite, **kw)
    for i, (quelle, _, _, _) in enumerate(H.IDEEN):
        w(os.path.join(AN, quelle + '.jpg'), f'i-{i}', 1160, 76)
    for i, (ziel, _) in enumerate(H.FAECHER):
        aus = os.path.join(W, 'roh', f'pdf-{i}'); os.makedirs(os.path.dirname(aus), exist_ok=True)
        subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-r', '110', '-png', '-singlefile', os.path.join(ROOT, 'unterlagen', 'pdf', ziel + '.pdf'), aus], check=True)
        w(aus + '.png', f'pdf-{i}', 900, 86)
    for name, (key, lage) in (H.GABEN_BILDER.items() if 'mitgebracht' in K.folge() else ()):
        w(K.hausbild(key), 'g-' + name, 1000, 72, **{**dict(dunkel=(0.46, 0.3), schnitt=0.72), **getattr(H, 'GABEN_BILD', {})}, lage=lage)   # H.GABEN_BILD: eigener Zuschnitt/ohne Dunkel (Grand Beau-Rivage 12.10.2026)
    ST = getattr(H, 'STUDIO', None)
    if ST:   # Filme vom Studio (aus _werkbank/film/, aufgenommen mit _werkbank/studio_film.js) als mp4 mit Standbild
        FZ = os.path.join(ZIEL, 'film'); os.makedirs(FZ, exist_ok=True)
        for name, *_ in ST['schritte']:
            q = os.path.join(W, 'film', name + '.webm')
            if not os.path.exists(q):
                q = os.path.join(W, 'film', name + '.mp4')
            if not os.path.exists(q):
                print('  Film fehlt:', name); continue
            z = os.path.join(FZ, name + '.mp4'); b = os.path.join(W, 'roh', 'film-' + name + '.jpg'); os.makedirs(os.path.dirname(b), exist_ok=True)
            if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(q):
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', q, '-vf', 'scale=1920:-2:flags=lanczos,fps=30', '-c:v', 'libx264', '-preset', 'slow', '-crf', '25', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', z], check=True)
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '0.8', '-i', q, '-frames:v', '1', '-vf', 'scale=1600:-2', '-q:v', '3', b], check=True)
            w(b, 'f-' + name, 1600, 80)
        st_bild = os.path.join(W, 'ansichten', 'Studio', ST.get('ansicht', '02 Übersicht') + '.jpg')
        if os.path.exists(st_bild):
            w(st_bild, 'z-studio', 720, 80, schnitt=4 / 3, lage=(0, 0))
        an_bild = os.path.join(W, 'ansichten', 'Anleitung', ST.get('anleitung_bild', 'seiten') + '.jpg')   # Vorschaubild der Anleitung für die Galerie unten
        if ST.get('anleitung') and os.path.exists(an_bild):
            w(an_bild, 'z-anleitung', 720, 80, schnitt=4 / 3, lage=(0, 0))
        if ST.get('bild'):
            w(K.hausbild(ST['bild']), 'g-studio', 1000, 72, dunkel=(0.46, 0.3), schnitt=0.72, lage=ST.get('lage', (.5, .5)))
        for name, _ in ST.get('bilder', []):   # Standbilder unter den Filmen
            q = os.path.join(W, 'ansichten', 'Studio', name + '.jpg')
            if os.path.exists(q):
                w(q, 'c-' + name, 1160, 78)
            else:
                print('  Standbild fehlt:', name)
    # Für Ihre Gäste (ansichten/Gaeste, z. B. node _werkbank/gaeste.js) und Rezeption im Chat (ansichten/Chat, node _werkbank/chat.js)
    for ordner, kuerzel in (('Gaeste', 'gf'), ('Chat', 'ch')):
        d = os.path.join(AN, ordner)
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.endswith('.jpg'):
                    n = f[:-4]
                    q = os.path.join(d, f)
                    if kuerzel == 'gf' and not n.endswith(('-h', '-lang')):
                        q_ = Image.open(q).convert('RGB')
                        if not 1.45 < q_.width / q_.height < 1.75:   # andere Form als die Karte (16:10): ganz zeigen, mittig auf der Grundfarbe statt angeschnitten (Robert 11.10.2026)
                            bw = max(q_.width, round(q_.height * 1.6)) * 1.12; bh = bw / 1.6
                            leer = Image.new('RGB', (round(bw), round(bh)), q_.getpixel((4, 4)))
                            leer.paste(q_, (round((bw - q_.width) / 2), round((bh - q_.height) / 2))); q = leer
                    w(q, f'{kuerzel}-{n}', 440 if n.endswith(('-h', '-lang')) else 1280, 78)
    GA = getattr(H, 'GAESTE', None)
    if GA and 'gf-' + GA[0][0] in m:
        w(os.path.join(AN, 'Gaeste', GA[0][0] + '.jpg'), 'z-gaeste', 720, 80, schnitt=4 / 3)
    if 'ch-rezeption' in m:
        r_ = Image.open(os.path.join(AN, 'Chat', 'rezeption.jpg')).convert('RGB')
        w(r_.crop((0, 0, round(r_.height * 4 / 3), r_.height)), 'z-rezeption', 720, 80, schnitt=4 / 3)
    if getattr(H, 'REZEPTION', None):
        qk = getattr(H, 'QR_KARTE', 'drucksachen/img/zimmermappe.webp')
        if os.path.exists(os.path.join(ROOT, qk)):
            w(os.path.join(ROOT, qk), 'qr-karte', 900, 84)
        FZ = os.path.join(ZIEL, 'film'); os.makedirs(FZ, exist_ok=True)
        for ext in ('.mp4', '.jpg'):
            q = os.path.join(W, 'film', 's-rezeption' + ext)
            if os.path.exists(q):
                shutil.copy2(q, os.path.join(FZ, 's-rezeption' + ext))
            else:
                print('  Rezeptions-Film fehlt:', 's-rezeption' + ext)
    for i, ml_ in enumerate(getattr(H, 'MAILS', {}).get('liste', [])):   # Mails: oberer Teil jeder Mail (Kopf, Titel, Foto), hochkant
        if os.path.exists(ml_[0]):
            w(ml_[0], f'ml-{i}', 720, 80, schnitt=3 / 4, lage=(.5, 0))
    if getattr(H, 'GEPRUEFT', None):
        w(K.hausbild(getattr(H, 'GEPRUEFT_BILD', H.SCHLUSS['bild'])), 'z-geprueft', 720, 80, schnitt=4 / 3)
    w(K.hausbild(H.SCHLUSS['bild']), 'schluss', 1920, 74, dunkel=(0.52, 0.3))
    w(K.hausbild(H.BRIEF['bild']), 'brief', 1300, 80, schnitt=H.BRIEF.get('schnitt', 1.5), lage=H.BRIEF.get('lage', (.5, .5)))
    if H.AUFTAKT.get('bild'):   # Titelblatt: ein Foto über die ganze Fläche, das Dunkel steckt im Bild
        tb = Image.open(K.hausbild(H.AUFTAKT['bild'])).convert('RGB')
        g = Image.new('L', (256, 1)); g.putdata([int(255 * .8 * max(0, 1 - i / 255 / .7) ** 1.15) for i in range(256)])   # links, wo der Text steht, ist das Bild dunkler
        r_, g_, b_ = (int(H.FARBEN['nacht'][i:i + 2], 16) for i in (1, 3, 5))
        tb = Image.composite(Image.new('RGB', tb.size, (r_, g_, b_)), tb, g.resize(tb.size))
        w(tb, 'titelbild', 2200, 74, dunkel=H.AUFTAKT.get('dunkel', (.5, .3)), schnitt=16 / 10, lage=H.AUFTAKT.get('lage', (.5, .5)))
    w(os.path.join(K.KIT, 'robert.jpg'), 'robert', 400, 90)   # Roberts graues Profilbild (von seinem Instagram-Profil)
    for i, (key, verh, lage, _) in enumerate(getattr(H, 'GEPRUEFT_TRIO', [])):   # Geprüft als Collage: drei echte Fotos des Hauses (Schlüssel, Seitenverhältnis b/h, Lage als (x, y) oder «46% 50%», Name in der Einkerbung)
        if isinstance(lage, str):
            lage = tuple(float(x_.rstrip('%')) / 100 for x_ in lage.split()[:2])
        w(K.hausbild(key), f'gt-{i}', 1100, 80, schnitt=verh, lage=lage)
    og = Image.open(os.path.join(R, 'Startseite.jpg')).convert('RGB')   # Vorschaubild für Messenger (1200 × 630)
    nh = round(og.width * 630 / 1200); og = og.crop((0, 0, og.width, min(og.height, nh))).resize((1200, 630), Image.LANCZOS)
    og.save(os.path.join(IMG, 'og.jpg'), 'JPEG', quality=84)
    for key, *_ in list(H.AUFTAKT['abzuege']) + list(H.MATERIAL['streu']) + list(H.BRIEF.get('abzuege', [])):
        w(K.hausbild(key), 'a-' + slug(os.path.basename(key)), 640, 78)
    PR = os.path.join(W, 'roh', 'papier')
    for x in papier['etiketten'][:len(H.PAPIER['orte_e'])]:
        w(os.path.join(PR, x['id'] + '.png'), 'k-' + x['id'], 340, 84)
    for n, _, _, br, _, _ in H.PAPIER['orte_d']:
        if os.path.exists(os.path.join(PR, n + '.png')):
            w(os.path.join(PR, n + '.png'), 'b-' + n, max(200, round(br * 13)), 84)
    ZI = os.path.join(AN, 'Ziele')
    FD_ART = getattr(H, 'FEED', {}).get('art', 'abzuege')
    if os.path.exists(os.path.join(ZI, 'feed-handy.png')):
        hb = Image.open(os.path.join(ZI, 'feed-handy.png')).convert('RGB')
        if FD_ART == 'spalten':   # das Handy liegt über Bildern: die vier Ecken neben dem Gehäuse müssen durchsichtig sein
            from PIL import ImageDraw, ImageFilter
            mk = hb.copy()
            for ecke in ((0, 0), (mk.width - 1, 0), (0, mk.height - 1), (mk.width - 1, mk.height - 1)):
                ImageDraw.floodfill(mk, ecke, (255, 0, 255), thresh=16)
            fl = Image.new('L', mk.size, 0); px, fp = mk.load(), fl.load()
            for y_ in range(mk.height):
                for x_ in list(range(0, 90)) + list(range(mk.width - 90, mk.width)):
                    if (y_ < 90 or y_ >= mk.height - 90) and px[x_, y_] == (255, 0, 255):
                        fp[x_, y_] = 255
            al = Image.eval(fl.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(.7)), lambda v: 255 - v)
            hb = hb.convert('RGBA'); hb.putalpha(al)
        w(hb.convert('RGBA'), 'feed-handy', 720, 88)
        FD = H.FEED
        nrn = [k_[0] for k_ in FD.get('kacheln', [])] + [n for _, l in FD.get('spalten', []) for n in l] + [n for s_ in FD.get('streifen', []) for n in s_[1]] + list(FD.get('bogen', []))
        for nr in dict.fromkeys(nrn):
            w(os.path.join(ROOT, 'feed', 'thumbs', f'{nr:02d}.jpg'), f'fp-{nr}', 540 if FD.get('art') == 'spalten' else 400, 84)
        r = Image.open(os.path.join(ZI, 'feed-raster.png')).convert('RGB')
        w(r.crop((round(r.width * .04), round(r.height * .2), round(r.width * .96), round(r.height * .2 + r.width * .92 * .75))), 'z-feed', 720, 82)
    for name, quelle in (('website', os.path.join(R, 'Startseite.jpg')), ('unterlagen', os.path.join(ZI, 'unterlagen.jpg')), ('drucksachen', os.path.join(ZI, 'drucksachen.jpg')), ('etiketten', os.path.join(ZI, 'etiketten.jpg')), ('material', os.path.join(ZI, 'material.jpg'))):
        if os.path.exists(quelle):
            bq = Image.open(quelle).convert('RGB')
            if name == 'website':
                bq = bq.crop((0, 0, round(bq.height * 4 / 3), bq.height))
            w(bq, 'z-' + name, 720, 80, schnitt=4 / 3)
    return m


ZEICHEN = {k: f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{v}</svg>' for k, v in {
    'seite': '<path d="M6 3h8l4 4v14H6zM14 3v4h4M9 12h6M9 16h6"/>', 'karte': '<path d="M4 5h16v14H4zM4 10h16M9 10v9"/>', 'schloss': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    'schild': '<path d="M12 3 5 6v6c0 4.5 3 7.5 7 9 4-1.5 7-4.5 7-9V6z"/><path d="m9 12 2 2 4-4"/>', 'auge': '<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.6"/>'}.items()}


def google_kapitel():
    """Kapitel «Die Suche» im Prüfbericht (Robert 14.10.2026: Google und KI-Suche «nicht präsent, aber irgendwo mit dazu»).
    Gezählt wird an der gebauten Website mit ~/Desktop/Website-Projekte/_Google/google.py, Zeilen ohne Beleg fallen weg.
    Abschalten: H.GOOGLE_KAPITEL = False. Eigene Zeilen: H.GOOGLE_ZEILEN = [...]."""
    if getattr(H, 'GOOGLE_KAPITEL', True) is False:
        return None
    ein = 'Wie Gäste das Haus finden, wenn sie bei Google suchen oder eine KI fragen. Was heute schon steht und was beim Freigeben dazukommt.'
    if getattr(H, 'GOOGLE_ZEILEN', None):
        return ('Die Suche', 'auge', ein, H.GOOGLE_ZEILEN)
    import sys as _s
    _s.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_Google'))
    try:
        import google as G
        befund, _ = G.pruefen(ROOT, still=True)
        langs = G.sprachordner(ROOT)
    except Exception:
        return None
    n, spr = len(befund), len(langs) + 1
    ohne_text = [r for r, f in befund if any(x in ('Titel', 'Kurzbeschreibung') for x in f)]
    ohne_alt = [r for r, f in befund if any('Bilder ohne Beschreibung' in x for x in f)]
    import glob as _g
    # Querprüfung 21.10.2026 (Demo-Check Schlössli): Restaurants haben keine Zimmer und keinen Booking-Eintrag; Hotel = Zimmer- oder Suitenseite oder H.HAUSART
    rest = getattr(H, 'HAUSART', None) == 'restaurant' or (getattr(H, 'HAUSART', None) is None and not (_g.glob(os.path.join(ROOT, 'zimmer*.html')) or _g.glob(os.path.join(ROOT, 'suiten*.html'))))
    z = ['Solange die Seite ein Entwurf ist, bleibt sie für Suchmaschinen absichtlich unsichtbar. Freigegeben wird sie erst, wenn sie unter Ihrer eigenen Adresse läuft.']
    if n and not ohne_text:
        z.append(('Die Seite trägt' if n == 1 else f'Jede der {n} Seiten trägt') + f' einen eigenen Titel und einen kurzen Text für das Suchergebnis' + (f', in jeder der {spr} Sprachen eigens geschrieben.' if spr > 1 else '.'))
    if spr > 1:
        z.append(f'Die {spr} Sprachfassungen werden beim Freigeben miteinander verknüpft. So bekommt jeder Gast bei Google die Seite in seiner Sprache angezeigt.')
    z.append(('Adresse, Telefon, Reservation, Karte und Öffnungszeiten' if rest else 'Adresse, Telefon, Buchung, Restaurants und Öffnungszeiten') + ' werden beim Freigeben zusätzlich so hinterlegt, dass Google und KI-Assistenten wie ChatGPT sie direkt lesen können, ohne zu raten.')
    if n and not ohne_alt:
        z.append('Jedes Bild trägt eine Beschreibung. Das hilft Gästen, die sich die Seite vorlesen lassen, und der Bildersuche.')
    z.append('Alles Wichtige steht als Text auf der Seite und nicht in Bildern. So kann eine KI, die Gästen bei der Suche hilft, ' + ('Ihre Karte, Anlässe und Angebote' if rest else 'Ihre Zimmer, Restaurants und Angebote') + ' auch wirklich lesen.')
    z.append('Ersetzt die neue Seite Ihre heutige, führt jede bisherige Adresse auf die passende neue Seite. So geht kein Platz in den Suchergebnissen verloren, und kein geteilter Link läuft ins Leere.')
    z.append('Was ausserhalb der Website zählt, gehört genauso dazu: der Eintrag bei Google Maps, Ihre Bewertungen und gleiche Angaben auf ' + ('Tripadvisor, den Restaurantführern und Portalen' if rest else 'Booking, Tripadvisor und den Portalen') + '. Auf diese Quellen stützen sich auch KI-Assistenten stark. Das lässt sich in der laufenden Betreuung mitpflegen.')
    return ('Die Suche', 'auge', ein, z)


def geprueft_seite():
    """Die Seite zum Prüfbericht: werkbank/geprueft/index.html, in Alltagssprache, nur Belegtes (H.GEPRUEFT_MEHR)."""
    ziel = os.path.join(ZIEL, 'geprueft')
    GM = list(H.GEPRUEFT_MEHR)
    gk = google_kapitel()
    stelle = None
    if gk and not any(t_ == gk[0] for t_, *_ in GM):
        stelle = next((i for i, (t_, *_) in enumerate(GM) if 'offen' in t_.lower()), len(GM))   # vor dem Kapitel «Was offen ist»
        GM.insert(stelle, gk)
    bloecke = ''.join(f'<section class="gp" id="g{i + 1}"><div class="gp__k">{ZEICHEN[z_]}<p class="kap"><b>{i + 1:02d}</b><i></i><span>{e(ti)}</span></p></div><h2>{e(ti)}</h2><p class="gp__e">{e(ein)}</p><ul>{"".join(f"<li data-a=\"auf\" style=\"--i:{j}\">{e(x)}</li>" for j, x in enumerate(zeilen))}</ul></section>'
                      for i, (ti, z_, ein, zeilen) in enumerate(GM))
    kurz = list(getattr(H, 'GEPRUEFT_NAV', [t_.split()[-1].rstrip('.') for t_, *_ in GM]))
    if stelle is not None and len(kurz) < len(GM):
        kurz.insert(stelle, 'Suche')
    ein_ = getattr(H, 'GEPRUEFT_EIN', 'Bevor Sie etwas zu sehen bekommen, ist es durchgegangen worden: die Website auf jedem Gerät, die Unterlagen Wort für Wort, das Studio bis zum letzten Knopf, der Umgang mit Ihren Daten. Hier steht, was genau, ohne Fachwörter. Und was ehrlich offen bleibt, steht auch da.')
    seite = f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Geprüft · Werkbank {e(H.NAME)}</title>
<meta name="description" content="Was an der neuen Website des {e(H.NAME)}, an den Unterlagen und am Studio geprüft wurde, in Alltagssprache.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{H.FARBEN['nacht']}">
<link rel="preload" href="../fonts/{H.SCHRIFT['titel'][1]}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../werkbank.css?v={K.v('werkbank.css')}">
<style>{':root{--muster:url(../muster.webp)}' if getattr(H, 'MUSTER_BILD', None) else ''}.gpk{{background-image:var(--muster);background-size:var(--musterb) auto}}</style>
</head>
<body class="haus-{H.KURZ}">
{K.sprite()}
<header class="leiste leiste--sofort"><div class="insel">
  <a class="insel__m" href="../index.html">{HZ}{f"<b>{e(H.LEISTE)}</b>" if H.LEISTE else ""}<span>Werkbank</span></a>
  <nav aria-label="Abschnitte">{''.join(f'<a href="#g{i + 1}">{e(k_)}</a>' for i, k_ in enumerate(kurz))}</nav>
  <a class="glanz" href="../index.html#geprueft">Zur Werkbank{PF}</a>
</div></header>
<main>
<section class="gpk">
  <div class="in">
    <p class="gruss" data-a="auf" style="font-family:var(--serif);color:var(--gold);margin-bottom:18px">Der Prüfbericht</p>
    {titel(['Was alles geprüft', 'wurde.'], 'h1', 't1')}
    <div class="lauf"><p data-a="worte" style="--vz:300ms">{ein_}</p></div>
    <div class="mono" data-a="auf" style="--i:6"><span>Stand {K.STAND}</span><span>Robert Reff · Tasty Studios</span></div>
  </div>
</section>
<section class="gpl">
  <div class="in">
    {bloecke}
    <div class="gpf" data-a="auf"><p>Jede Zeile hier hat eine Prüfung hinter sich, die sich wiederholen lässt. Wenn Sie zu einem Punkt mehr wissen möchten, fragen Sie mich einfach.</p>{kn('Zurück zur Werkbank', '../index.html#geprueft', 'kn--linie')}</div>
  </div>
</section>
</main>
<footer class="fuss fuss--kurz"><div class="in fuss__u">
  <div><b>Prüfbericht zum Entwurf</b><p>Das ist ein Entwurf von Robert Reff, Tasty Studios, und nicht die offizielle Website des Hauses.</p></div>
  <div class="r mono"><a href="mailto:robert@tasty-studios.de">robert@tasty-studios.de</a><span>Stand {K.STAND}</span></div>
</div></footer>
<script src="../werkbank.js?v={K.v('werkbank.js')}"></script>
</body>
</html>
'''
    K.schreib(os.path.join(ziel, 'index.html'), seite)


def gangfuss():
    return f'<div class="gang__f"><button class="rund" type="button" data-zur aria-label="Zurück">{LI}</button><button class="rund" type="button" data-vor aria-label="Weiter">{RE}</button><div class="gang__b"><i></i></div><div class="gang__z"></div></div>'


def baue():
    K.gestaltung()
    z, papier, unterlagen = zaehle()
    liste = json.load(open(os.path.join(AN, 'liste.json')))
    m = bilder(liste, papier, unterlagen)
    g = H.gefuege(z)

    def bild(name, alt='', lazy=True, klasse='', stil=''):
        w, h = m[name]
        st_ = (f'background-image:url({K.VORAB[name]});' if name in K.VORAB else '') + stil   # 40-px-Abbild hinter dem Foto: nie ein dunkler Kasten (Robert 10.10.2026)
        return f'<img src="img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}"{" loading=\"lazy\" decoding=\"async\"" if lazy else ""} class="ld{(" " + klasse) if klasse else ""}{" frei" if name in K.FREI else ""}"{f" style=\"{st_}\"" if st_ else ""}>'

    def abzug(key, unter, klasse='', mehr='', lazy=False):
        return f'<div class="abzug {klasse}" data-a="schweb"{mehr}>{bild("a-" + slug(os.path.basename(key)), lazy=lazy)}<span>{e(unter)}</span></div>'

    seiten = []
    for s in H.SEITEN:
        d = liste.get(s[0])
        if d:
            seiten.append({'d': s[0], 's': slug(d['name']), 't': H.LANG.get(d['name'], d['name']), 'k': H.KURZNAME.get(d['name'], d['name']), 'x': s[3], 'n': d['rechner']})
    wahl = ''.join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}">{e(s["k"])}</button>' for i, s in enumerate(seiten))
    ideen = ''.join(
        f'<article class="idee" data-a="kipp" style="--i:{min(i, 3)}"><div class="idee__b">{bild(f"i-{i}", t, stil=f"--op:{op}")}<span class="idee__n">{i + 1:02d}</span></div><h3>{e(t)}</h3><p>{e(x)}</p></article>'
        for i, (_, t, x, op) in enumerate(H.IDEEN))

    et = papier['etiketten']
    kleb_html = ''.join(f'<div class="kleb" data-a="schweb" style="left:{x}%;top:{y}%;width:{b}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i}">{bild("k-" + et[i]["id"])}</div>'
                        for i, (x, y, b, r) in enumerate(H.PAPIER['orte_e']) if i < len(et))
    bogen_html = ''.join(f'<div class="bogenb{" haengt" if haengt else ""}" data-a="schweb" style="left:{x}%;top:{y}%;width:{b}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i}">{bild("b-" + n)}</div>'
                         for i, (n, x, y, b, r, haengt) in enumerate(H.PAPIER['orte_d']) if 'b-' + n in m)
    streu = ''.join(f'<div class="abzug" data-a="schweb" data-drift="{dr}" style="--i:{i};--r:{d}deg;--r0:{d * 3}deg">{bild("a-" + slug(os.path.basename(k)))}<span>{e(u)}</span></div>'
                    for i, (k, u, d, dr) in enumerate(H.MATERIAL['streu']))
    farben_html = ''.join(f'<li class="farbkarte" data-a="schweb" style="--i:{i};--r:0deg;--r0:{(-1) ** i * 6}deg"><i style="background:{c}"></i><span><b>{n}</b>{c}<br>{wo}</span></li>' for i, (c, n, wo) in enumerate(H.HANDSCHRIFT['farben']))
    laufworte = ''.join(f'<span>{wo}</span>' + getattr(H, 'LAUFTRENNER', HZ) for wo in H.LAUFWORTE)
    namen = ''.join(f'<span>{e(u["name"])}</span>' for u in unterlagen)
    wege = [(n, t, h) for n, t, h in (('website', 'Website', '../index.html'), ('gaeste', 'Für Ihre Gäste', getattr(H, 'GAESTE_LINK', '../index.html')), ('rezeption', 'Rezeption im Chat', getattr(H, 'REZEPTION_LINK', '../rezeption/')), ('studio', getattr(H, 'STUDIO', {}).get('name', 'Studio'), getattr(H, 'STUDIO', {}).get('link', '../studio/')), ('anleitung', 'Anleitung', getattr(H, 'STUDIO', {}).get('anleitung', 'anleitung/')), ('unterlagen', 'Unterlagen', '../unterlagen/index.html'), ('drucksachen', 'Drucksachen', '../drucksachen/index.html'), ('etiketten', ET['name'], f'../{ET["ordner"]}/index.html'), ('feed', 'Feed', '../feed/index.html'), ('material', 'Material', '../material/index.html'), ('geprueft', 'Geprüft', 'geprueft/index.html')) if 'z-' + n in m]
    WEGE_STANDARD = f'''<nav class="in wege" aria-label="Alles auf einen Blick">
  <b class="wege__t" data-a="auf">Alles auf einen Blick</b>
  <div class="wege__r wege__r--{len(wege)}">{''.join(f'<a class="zielk" href="{h}" target="_blank" rel="noopener" data-a="kipp" style="--i:{i}"><span class="zielk__b">{H.zielk_bild(n, t) if callable(getattr(H, 'zielk_bild', None)) else bild("z-" + n, t)}</span><span class="zielk__z"><b>{t}</b><i>{PF}</i></span></a>' for i, (n, t, h) in enumerate(wege))}</div>
</nav>'''   # eigener Fuss je Haus über H.wege_abschnitt(wege) (Grand Beau-Rivage 11.10.2026)
    A, B, U, HS, FD, PA, MA, AU, SL = H.AUFTAKT, H.BRIEF, H.UNTERLAGEN, H.HANDSCHRIFT, H.FEED, H.PAPIER, H.MATERIAL, H.AUSBLICK, H.SCHLUSS
    n_ideen = zahl(len(H.IDEEN))
    feedzahl = zahl(z['feed']) if z['feed'] else ''
    gaben = [('seite', z['haupt'], 'Eine neue Website', H.GABEN['seite'].format(n=z['haupt']), '#seiten', 'Seiten ansehen'),
             ('unterlagen', z['unterlagen'], 'Ihre Unterlagen im selben Stil', H.GABEN['unterlagen'].format(n=z['unterlagen']), '#unterlagen', 'Unterlagen ansehen'),
             ('papier', z['druck'] + z['etiketten'], 'Ideen für Papier', H.GABEN['papier'].format(d=z['druck'], e=z['etiketten']), '#papier', 'Ideen ansehen'),
             ('material', z['feed'], 'Ein Feed für Instagram', H.GABEN['feed'].format(n=feedzahl), '#feed', 'Feed ansehen')]
    if getattr(H, 'GAESTE', None) and 'g-gaeste' in m:
        gaben.insert(1, ('gaeste', len(H.GAESTE), 'Für Ihre Gäste', H.GABEN.get('gaeste', '').format(n=zahl(len(H.GAESTE)), nk=zahl(len(H.GAESTE)).lower()), '#gaeste', 'Ansehen'))
    if getattr(H, 'STUDIO', None) and 'g-studio' in m:
        gaben.append(('studio', len(H.STUDIO['bereiche']), 'Ein Studio dazu' if H.STUDIO.get('name', 'Studio') == 'Studio' else f"Der {H.STUDIO['name']} dazu", H.GABEN.get('studio', '').format(n=zahl(len(H.STUDIO['bereiche'])), nk=zahl(len(H.STUDIO['bereiche'])).lower()), '#studio', 'Studio ansehen'))
    if getattr(H, 'GABEN_NUR', None):   # eine Seite ohne Unterlagen, Papier oder Feed (Familie Maeder, Startseite) nennt nur, was es bei ihr gibt (10.10.2026)
        gaben = [g_ for g_ in gaben if g_[0] in H.GABEN_NUR]
    gabe_eigen = getattr(H, 'gabe_html', None)   # eigene Gestalt der Gaben je Haus (Grand Beau-Rivage 12.10.2026: Kacheln mit Kuhle)
    gaben_html = ''.join(gabe_eigen(dict(i=i, bk=bk, n=n, t=t, x=x, ziel=ziel, kt=kt, bild=bild, e=e, PF=PF)) for i, (bk, n, t, x, ziel, kt) in enumerate(gaben)) if gabe_eigen and 'mitgebracht' in K.folge() else ''.join(f'<a class="gabe" href="{ziel}" data-a="kipp" style="--i:{i}">{bild("g-" + bk, klasse="gabe__b")}<b><span class="odo" data-z="{n}"></span></b><h3>{t}</h3><p>{x}</p><span class="pfeil">{kt}{PF}</span></a>'
                         for i, (bk, n, t, x, ziel, kt) in enumerate(gaben)) if 'mitgebracht' in K.folge() else ''
    schriften = ''.join(f'<div class="bogen__zl"><p class="etik"><span>{e(a)}</span><span>{i + 1:02d}</span></p><div class="schrift__g schrift__g--{kl}">Aa</div><p class="schrift__n">{e(n)}</p><p class="schrift__p">{e(x)}</p><p class="schrift__b{" t3" if kl == "a" else (" mono" if kl == "m" else "")}">{e(bsp)}</p></div>'
                        for i, (a, kl, n, x, bsp) in enumerate(HS['schriften']))
    geschwister = getattr(H, 'UEBERSICHT', None)
    alle_vier = f'<a href="{geschwister[1]}">{e(geschwister[0])}</a>' if geschwister else ''

    # ------------------------------------------------------------ Kapitel: Name, Titelzeilen und Satz. Jedes Haus überschreibt, was bei ihm anders heisst (H.KAPITEL)
    KAP = {
        'brief': dict(name='Guten Tag', zeilen=['Schön, dass Sie', 'hereinschauen.']),
        'mitgebracht': dict(name='Mitgebracht', zeilen=['Was ich Ihnen', 'mitgebracht habe.'], text='Vier Dinge sind es geworden.'),
        'vergleich': dict(name='Vergleich', zeilen=['Ihre Startseite,', 'einmal neu.'], text='Links sehen Sie Ihre Startseite, wie sie heute ist, rechts die neue. Schieben Sie den Griff einfach hin und her.'),
        'ideen': dict(name='Ideen', zeilen=['Die Ideen', 'hinter der Seite.'], text='{n} Gedanken, die ich mir zu Ihrer Seite gemacht habe. Jeder davon ist im Entwurf zu sehen.'),
        'gefuege': dict(name='Gefüge', zeilen=['Wie alles', 'zusammenhängt.'], text='Links steht, was von Ihnen kommt. In der Mitte, was ich daraus gemacht habe, daneben die Seiten und rechts alles, was im Hintergrund mitläuft. Tippen Sie auf eine Kachel oder lassen Sie sich einmal durchführen.'),
        'seiten': dict(name='Seiten', zeilen=['Alle Seiten zum', 'Durchblättern.'], text='Suchen Sie sich eine Seite aus und blättern Sie mit den Pfeilen durch die Ansichten. Rechts daneben sehen Sie dieselbe Stelle am Handy. Über «Öffnen» gelangen Sie auf die echte Seite.'),
        'unterlagen': dict(name='Unterlagen', zeilen=['Ihre Unterlagen,', 'im selben Stil.'], text=U['text'].format(n=zahl(z['unterlagen']), nk=zahl(z['unterlagen']).lower())),
        'handschrift': dict(name='Handschrift', zeilen=['Ihr Haus bleibt', 'Ihr Haus.'], text=HS['text']),
        'studio': dict(name=getattr(H, 'STUDIO', {}).get('name', 'Studio'), zeilen=['Sie pflegen die Seite', 'ganz einfach selbst.'], text=getattr(H, 'STUDIO', {}).get('text', '')),
        'gaeste': dict(name='Für Ihre Gäste', zeilen=['Vorschläge für', 'Ihre Gäste.'], text='{n} Vorschläge, die das Buchen und den Aufenthalt leichter machen. Alle sind im Entwurf gebaut und lassen sich ausprobieren, alle rechnen mit Ihren Zahlen. Nichts davon ist geschätzt.'),
        'rezeption': dict(name='Rezeption im Chat', zeilen=['Eine Rezeption,', 'die nie schläft.'], text='Unten rechts auf jeder Seite sitzt die Rezeption als Gespräch. Ein Gast tippt seine Frage, die Antwort kommt sofort, aus Ihren Seiten und Unterlagen, in seiner Sprache, auch spätabends. Der Film zeigt, wie es sich anfühlt. Alles, was die Rezeption kann, steht auf einer eigenen Seite.'),
        'mails': dict(name='Mails', zeilen=getattr(H, 'MAILS', {}).get('zeilen', ['Ihre Mails,', 'im selben Stil.']), text=getattr(H, 'MAILS', {}).get('text', '')),
        'geprueft': dict(name='Geprüft', zeilen=['Alles geprüft,', 'bevor Sie es sehen.'], text='Bevor diese Werkbank zu Ihnen kommt, ist jedes Teil durchgegangen worden: die Website auf jedem Gerät, die Unterlagen Wort für Wort, das Studio bis zum letzten Knopf, der Umgang mit Ihren Daten. Was genau, steht auf einer eigenen Seite, in Alltagssprache.'),
        'feed': dict(name='Instagram', zeilen=['Ein Feed', 'für Instagram.']),
        'papier': dict(name='Papier', zeilen=['Ein paar Ideen', 'für Papier.'], text='Beim Bauen sind mir noch ein paar Dinge eingefallen, die gut zu Ihrem Haus passen könnten. Das sind alles nur Ideen. Nehmen Sie sich davon, was Ihnen gefällt.'),
        'material': dict(name='Material', zeilen=['Alles liegt für', 'Sie bereit.'], text=MA['text']),
        'dazu': dict(name='Ausblick', zeilen=['Was noch', 'dazukommt.'], text=AU['text']),
        'schluss': dict(name='Danke', zeilen=['Ich freue mich', 'auf Ihre Antwort.'], text='Wenn Ihnen der Entwurf gefällt, freue ich mich sehr, von Ihnen zu hören. Schreiben Sie mir einfach, was Sie denken. Wünsche und Änderungen sind jederzeit willkommen.'),
    }
    for x in getattr(H, 'EIGENE', []):
        KAP[x['key']] = dict(name=x['name'], zeilen=x['zeilen'], text=x.get('text', ''))
    for k_, v_ in getattr(H, 'KAPITEL', {}).items():
        KAP[k_].update(v_)
    KAP['ideen']['text'] = KAP['ideen']['text'].format(n=n_ideen, nk=n_ideen.lower())
    if getattr(H, 'GAESTE', None):
        KAP['gaeste']['text'] = KAP['gaeste']['text'].format(n=zahl(len(H.GAESTE)), nk=zahl(len(H.GAESTE)).lower())
    FOLGE = [f for f in K.folge() if not (f == 'vergleich' and 'alt' not in m) and not (f == 'feed' and 'feed-handy' not in m) and not (f == 'gaeste' and not any('gf-' + g_[0] in m for g_ in getattr(H, 'GAESTE', [])))]
    NR = {f: K.nr(f) for f in FOLGE if f != 'lauf'}
    HELL = {'brief', 'seiten', 'material', 'dazu', 'studio'}
    # Flächen: helle Abschnitte auf Papier (zwei helle hintereinander: der zweite auf Creme), dunkle im Wechsel der Töne des Hauses
    FL, dunkel, vor, di = {}, ['fl--navy tapete', 'fl--nacht', 'fl--blau', 'fl--nacht', 'fl--navy tapete', 'fl--tief'], None, 0
    for f in FOLGE:
        if f in ('lauf', 'schluss'):
            continue
        if f in HELL:
            FL[f] = 'fl--creme' if vor in HELL else 'fl--papier'
        else:
            FL[f] = dunkel[di % len(dunkel)]; di += 1
        vor = f
    if getattr(H, 'GEPRUEFT_TRIO', None) and 'geprueft' in FL:   # die Collage liegt auf der ruhigen Nachtfläche, das grosse Wort dahinter braucht keine Tapete
        FL['geprueft'] = 'fl--nacht'
    FL.update(getattr(H, 'FLAECHE', {}))

    def kopf_(f):   # ohne Satz steht nur die Überschrift da (ein Satz, der in jeder Werkbank gleich wäre, darf fehlen)
        if not KAP[f].get('text'):
            return f'<div class="kopfzeile"><div>{kap(NR[f], KAP[f]["name"])}{titel(KAP[f]["zeilen"])}</div></div>'
        return kopf(NR[f], KAP[f]['name'], KAP[f]['zeilen'], KAP[f]['text'])

    T = {}
    # --- Brief. «lang»: mit Vorstellung und den drei Orten. «kurz»: nur, was dieses Haus betrifft, daneben das Haus und zwei Abzüge.
    brief_art = B.get('art', 'lang')
    brief_text = ''.join(f'<p data-a="auf" style="--i:{i + 1}">{p}</p>' for i, p in enumerate(B['absaetze']))
    gastgeber = f'''<div class="gastgeber" data-a="auf" style="--i:3">
        <span class="gastgeber__b">{bild('robert', 'Robert Reff')}</span>
        <p class="gastgeber__t">{B['schluss']}</p>
        <p class="gastgeber__n"><b>Robert Reff</b><span>Hamburg · Koh Phangan · Siargao</span></p>
      </div>'''
    haus_bild = f'<div class="brief__haus" data-a="gross" style="--sv:{B.get('schnitt', 1.5)}">{bild("brief", B["bild_alt"])}<span class="schild">{e(B["schild"][0])}<small>{e(B["schild"][1])}</small></span></div>'
    orte = '''<div class="karte3" data-a="kipp" style="--i:2">
        <h3>Meine drei Orte</h3>
        <p>Zwischen diesen dreien bin ich das Jahr über unterwegs.</p>
        <svg class="kurs" viewBox="0 0 520 200" role="img" aria-label="Hamburg, Koh Phangan und Siargao als drei Punkte auf einem Kursblatt">
          <path class="weg" d="M52 52 C160 170 262 176 336 150 S446 128 478 136"/>
          <circle class="welle" cx="336" cy="150" r="7"/>
          <circle class="pkt" cx="52" cy="52" r="5"/><circle class="pkt da0" cx="336" cy="150" r="5.5"/><circle class="pkt" cx="478" cy="136" r="5"/>
          <text class="ort" x="66" y="48">Hamburg</text><text x="66" y="64">53°33' N · 9°59' O</text>
          <text class="ort" x="336" y="178" text-anchor="middle">Koh Phangan</text><text x="336" y="194" text-anchor="middle">9°44' N · 100°01' O · gerade hier</text>
          <text class="ort" x="478" y="108" text-anchor="end">Siargao</text><text x="478" y="122" text-anchor="end">9°47' N · 126°09' O</text>
        </svg>
      </div>'''
    zweit = ''.join(abzug(k_, u_, f'brief__a brief__a--{i + 1}', f' data-drift="{dr_}" style="--r:{r_}deg;--r0:{r_ * 3}deg;--i:{i + 2}"', lazy=True) for i, (k_, u_, r_, dr_) in enumerate(B.get('abzuege', [])))
    T['brief'] = f'''
<section class="fl {FL.get('brief', '')} blatt" id="brief">
  <div class="in brief brief--{brief_art}{" brief--links" if B.get('seite') == 'links' else ""}">
    <div>
      {kap(NR['brief'], KAP['brief']['name'])}
      {titel(KAP['brief']['zeilen'])}
      <div class="lauf">{brief_text}</div>
      {gastgeber if B.get('schluss') else ''}
    </div>
    <div class="brief__r">{haus_bild}{orte if brief_art == 'lang' else zweit}</div>
  </div>
</section>'''
    if callable(getattr(H, 'brief_abschnitt', None)):   # eigener Aufbau des Briefs, ganz in haus.py (Grand Beau-Rivage 12.10.2026)
        T['brief'] = H.brief_abschnitt(dict(bild=bild, titel=titel, kap=kap, e=e, m=m, nr=NR['brief'], name=KAP['brief']['name'], zeilen=KAP['brief']['zeilen'], fl=FL.get('brief', '')))
    # ganzer Block der Gaben je Haus (Grand Beau-Rivage 12.10.2026: Entwurf 04 «Die Menükarte»), sonst das Raster
    GABEN_BLOCK = (H.gaben_abschnitt([dict(i=i, bk=bk, n=n, t=t, x=x, ziel=ziel, kt=kt, bild=bild, e=e, PF=PF) for i, (bk, n, t, x, ziel, kt) in enumerate(gaben)])
                   if callable(getattr(H, 'gaben_abschnitt', None)) else f'<div class="gaben gaben--{len(gaben)}{getattr(H, "GABEN_KLASSE", "")}">{gaben_html}</div>')
    T['mitgebracht'] = '' if 'mitgebracht' not in NR else f'''
<section class="fl {FL['mitgebracht']} blatt" id="mitgebracht">
  <div class="in">
    {kopf_('mitgebracht')}
    {GABEN_BLOCK}
  </div>
</section>'''
    T['lauf'] = f'\n<div class="zeile" aria-hidden="true" data-lauf><div class="zeile__z">{laufworte * 6}</div></div>'
    VH = [v for v in getattr(H, 'VORHER', []) if f'vh-{v[0]}-alt' in m and f'vh-{v[0]}-neu' in m]
    if VH and 'vergleich' in NR:
        KAP['vergleich'].update(name='Vorher, nachher', zeilen=['Ihre Website,', 'Seite für Seite.'], text='Links Ihre Seite, wie sie heute ist, rechts der Entwurf. Schieben Sie den Griff hin und her, daneben steht, was neu ist.')
    def vh_feld(i, v):
        sl, name, ti, punkte, link = v
        li = ''.join(f'<li>{e(x)}</li>' for x in punkte)
        return (f'<div class="vh-feld" data-vh="{i}"{"" if i == 0 else " hidden"}><div class="vgl">'
                f'{bild(f"vh-{sl}-alt", "Heute: " + name + " auf " + H.DOMAIN, lazy=i > 0)}{bild(f"vh-{sl}-neu", "Neu: " + name, lazy=i > 0, klasse="neu")}'
                f'<span class="vgl__e vgl__e--l">Heute</span><span class="vgl__e vgl__e--r">Neu</span>'
                f'<div class="vgl__g"><i><svg viewBox="0 0 22 22" aria-hidden="true"><path d="M8 6 3 11l5 5M14 6l5 5-5 5"/></svg></i></div>'
                f'<input type="range" min="0" max="100" value="50" aria-label="Vergleich verschieben"></div>'
                f'<div class="vh-was"><p class="vh-was__k">Was neu ist</p><h3>{e(ti)}</h3><ul>{li}</ul>{kn("Seite ansehen", "../" + link, neu=True)}</div></div>')
    T['vergleich'] = '' if 'vergleich' not in NR else (f'''
<section class="fl {FL['vergleich']} blatt vh" id="vergleich">
  <div class="in">
    {kopf_('vergleich')}
    <div class="vh-wahl" data-a="auf" role="group" aria-label="Seite wählen">{''.join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-vh-zu="{i}">{e(v[1])}</button>' for i, v in enumerate(VH))}</div>
    <div class="vh-felder" data-a="gross">{''.join(vh_feld(i, v) for i, v in enumerate(VH))}</div>
  </div>
</section>''' if VH else f'''
<section class="fl {FL['vergleich']} blatt" id="vergleich">
  <div class="in">
    {kopf_('vergleich')}
    <div class="vgl" data-a="gross">
      {bild('alt', 'Die heutige Startseite von ' + H.DOMAIN)}
      {bild('auftakt', 'Die neue Startseite', klasse='neu')}
      <span class="vgl__e vgl__e--l">Heute</span><span class="vgl__e vgl__e--r">Neu</span>
      <div class="vgl__g"><i><svg viewBox="0 0 22 22" aria-hidden="true"><path d="M8 6 3 11l5 5M14 6l5 5-5 5"/></svg></i></div>
      <input type="range" min="0" max="100" value="50" aria-label="Vergleich verschieben">
    </div>
  </div>
</section>''')
    T['ideen'] = f'''
<section class="fl {FL['ideen']} blatt" id="ideen">
  <div class="in">
    {kopf_('ideen')}
    <div class="gang"><div class="band">{ideen}</div>{gangfuss()}</div>
  </div>
</section>'''
    T['gefuege'] = f'''
<section class="fl {FL['gefuege']} blatt" id="gefuege">
  <div class="in">
    {kopf_('gefuege')}
    <div class="brett-scroll" data-a="auf"><div class="brett-box">
      <div class="brett-k" aria-hidden="true">{''.join(f'<span style="left:{fx * 100:.1f}%"><i>{i + 1:02d}</i>{s}</span>' for i, (fx, s) in enumerate(zip(g['fx'], g['sp'])))}</div>
      <div class="brett" id="brett"><div id="brett-n"></div></div>
      <div class="brett-f">{e(g['fuss'])}</div>
    </div></div>
    <div class="brett-p" aria-live="polite">
      <div class="wechsel"><div class="k" id="bp-k">{g['start'][0]}</div><div class="t" id="bp-t">{g['start'][1]}</div></div>
      <div class="wechsel"><p id="bp-p">{g['start'][2]}</p><p class="weg" id="bp-w"></p></div>
      <div class="brett-p__k"><button class="kn kn--klein" id="brett-rund" type="button">Rundgang starten<i>{PF}</i></button><button class="kn kn--linie kn--klein" id="brett-noch" type="button">Nochmal aufbauen<i>{PF}</i></button></div>
      <span class="brett-uhr"></span>
    </div>
    <p class="brett-h">Am Handy lässt sich das Brett seitlich schieben.</p>
  </div>
</section>'''
    T['seiten'] = f'''
<section class="fl {FL['seiten']} blatt" id="seiten">
  <div class="in">
    {kopf_('seiten')}
    <div class="wahl" data-a="auf" role="group" aria-label="Seite wählen">{wahl}</div>
    <div class="schau" data-a="auf" tabindex="0">
      <div class="schau__f">
        <div class="fen"><div class="fen__k"><i></i><i></i><i></i><span></span></div><div class="schau__s"></div></div>
        <button class="rund schau__p schau__p--l" type="button" data-zur aria-label="Vorige Ansicht">{LI}</button>
        <button class="rund schau__p schau__p--r" type="button" data-vor aria-label="Nächste Ansicht">{RE}</button>
        <div class="schau__u mono"><div class="schau__pk" aria-hidden="true"></div><span class="schau__z"></span></div>
      </div>
      <div class="schau__r">
        <div class="tel"><div></div></div>
        <div class="schau__t"><h3></h3><p></p><a class="kn kn--klein" href="../index.html" target="_blank" rel="noopener">Öffnen<i>{PF}</i></a></div>
      </div>
    </div>
  </div>
</section>'''
    T['unterlagen'] = '' if 'unterlagen' not in NR else f'''
<section class="fl {FL['unterlagen']} blatt" id="unterlagen">
  <div class="in">
    <div class="karten{" karten--r" if U.get('gespiegelt') else ""}">
      <div>
        {kap(NR['unterlagen'], KAP['unterlagen']['name'])}
        {titel(KAP['unterlagen']['zeilen'])}
        <div class="lauf" style="margin-top:clamp(22px,2.6vw,36px)"><p data-a="worte">{KAP['unterlagen']['text']}</p></div>
        <div class="kn-reihe" data-a="auf" style="margin-top:30px">{kn('Unterlagen durchblättern', '../unterlagen/index.html', neu=True)}{kn(U['knopf2'][0], U['knopf2'][1], 'kn--linie', neu=True) if U.get('knopf2') else ''}</div>
      </div>
      <div class="faecher faecher--{len(H.FAECHER)}" data-a="auf">
        {''.join(f'<a class="blattk blattk--{i + 1}" style="--j:{i}" href="../unterlagen/index.html#{f}" target="_blank" rel="noopener">{bild(f"pdf-{i}", "Idee: " + t)}<span>{t}<b>ansehen</b></span></a>' for i, (f, t) in enumerate(H.FAECHER))}
      </div>
    </div>
    <div class="namenzug" aria-hidden="true" data-lauf><div>{namen * max(4, 24 // max(1, len(unterlagen)))}</div></div>
  </div>
</section>'''
    T['handschrift'] = f'''
<section class="fl {FL['handschrift']} blatt" id="handschrift">
  <div class="in">
    {kopf_('handschrift')}
    <div class="bogen" data-a="auf">
      <div class="bogen__z"><div class="bogen__zl">
        <p class="etik"><span>{e(HS['marke_etik'])}</span><span>{e(H.NAME)}</span></p>
        <div class="marke"><div class="marke__w">{K.wortmarke()}</div><p>{HS['marke_text']}</p></div>
      </div></div>
      <div class="bogen__z schriften">{schriften}</div>
      <div class="bogen__z"><div class="bogen__zl">
        <p class="etik"><span>Farben</span><span>{e(HS['farben_etik'])}</span></p>
        <ul class="farbkarten">{farben_html}</ul>
      </div></div>
      <div class="bogen__z tapetenband">{HZ}<div><p class="etik"><span>{e(HS['muster_etik'])}</span></p><p>{HS['muster_text']}</p></div></div>
      <div class="bogen__z"><div class="bogen__zl probe-kn">
        <div><p class="etik"><span>Knöpfe</span></p><p>{HS.get('knopf_text', 'Jeder Knopf hat eine kleine Kante und gibt nach, wenn man ihn drückt. Probieren Sie es gern aus.')}</p></div>
        <div class="kn-reihe hell"><button class="kn" type="button">{HS.get('knoepfe', ('Drücken Sie mich', 'Mich auch'))[0]}<i>{PF}</i></button><button class="kn kn--linie" type="button">{HS.get('knoepfe', ('Drücken Sie mich', 'Mich auch'))[1]}<i>{PF}</i></button></div>
      </div></div>
    </div>
  </div>
</section>'''

    # --- Studio (Kontrollpanel): Schritte links, Film rechts; die Filme laufen nacheinander, ein Klick macht sie gross
    ST = getattr(H, 'STUDIO', None)
    if ST and 'studio' in NR:
        schritte = ''.join(f'<button class="schritt" type="button" aria-pressed="{"true" if i == 0 else "false"}" data-film="film/{n}.mp4" data-bild="img/f-{n}.webp" data-adr="{e(a)}"><i>{i + 1:02d}</i><b>{e(t)}</b><span>{x}</span><u></u></button>'
                           for i, (n, t, x, a) in enumerate(ST['schritte']) if 'f-' + n in m)
        bereiche = ''.join(f'<li data-a="auf" style="--i:{i}"><b>{e(b_)}</b><span>{x_}</span></li>' for i, (b_, x_) in enumerate(ST['bereiche']))
        sb = [(n_, t_) for n_, t_ in ST.get('bilder', []) if 'c-' + n_ in m]
        sb_html = ''.join(f'<figure data-a="kipp" style="--i:{i}">{bild("c-" + n_, t_)}<figcaption>{e(t_)}</figcaption></figure>' for i, (n_, t_) in enumerate(sb))
        studio_kn = f'''{kn(ST.get('knopf', 'Studio ausprobieren'), ST.get('link', '../studio/'), neu=True)}{kn('Zur Anleitung, Schritt für Schritt', ST['anleitung']) if ST.get('anleitung') else ''}{''.join(kn(t_, h_, 'kn--linie', neu=h_.startswith('..')) for t_, h_ in ST.get('mehr', []))}{kn('Website ansehen', '../index.html', 'kn--linie', neu=True) if not ST.get('mehr') else ''}'''   # seit 14.10.2026 mittig unter dem Film (Robert)
        T['studio'] = f'''
<section class="fl {FL['studio']} blatt" id="studio">
  <div class="in">
    {kopf_('studio')}
    {f'''<div class="studio" data-a="auf">
      <div class="schritte">{schritte}</div>
      <div class="studio__r">
        <div class="kino"><div class="fen__k"><i></i><i></i><i></i><span></span></div><div class="kino__s"><video muted playsinline preload="none"></video><span class="kino__play" data-wort="Gross ansehen"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3.5v17l14-8.5z"/></svg></span><span class="kino__hin">Klick oder Esc zum Anhalten</span><div class="kino__k"><button type="button" data-nochmal>Nochmal</button></div></div></div>
        <div class="kn-reihe kn-reihe--mitte">{studio_kn}</div>
      </div>
    </div>''' if schritte else ''}
    <ul class="bereiche">{bereiche}</ul>
    {f'<div class="studio__bilder studio__bilder--{len(sb)}" data-a="auf">{sb_html}</div>' if sb else ''}
    {'' if schritte else f'<div class="kn-reihe" data-a="auf" style="margin-top:clamp(26px,3vw,44px)">{studio_kn}</div>'}
    <p class="hinweis hinweis--breit" data-a="auf">{ST['hinweis']}</p>
  </div>
</section>'''
    else:
        T['studio'] = ''

    # --- Für Ihre Gäste: Band wie bei den Ideen, darunter drei Handys nebeneinander, in jedem lässt sich die Seite scrollen (Robert 10.10.2026)
    GA = getattr(H, 'GAESTE', None)
    if GA and 'gaeste' in NR:
        gaeste_html = ''.join(f'<article class="idee" data-a="kipp" style="--i:{min(i, 3)}"><div class="idee__b">{bild("gf-" + n_, ti, stil=f"--op:{op}")}<span class="idee__n">{i + 1:02d}</span></div><h3>{e(ti)}</h3><p>{e(x)}</p></article>'
                              for i, (n_, ti, x, op) in enumerate(GA) if 'gf-' + n_ in m)
        tel_html = ''.join(f'<figure><div class="tel" data-a="schweb" style="--i:{i}"><div>{bild("gf-" + n_)}</div></div><figcaption>{e(u)}<span class="scroll">im Handy scrollen</span></figcaption></figure>'
                           for i, (n_, u) in enumerate(getattr(H, 'GAESTE_TEL', [])) if 'gf-' + n_ in m)
        gk = getattr(H, 'GAESTE_KNOEPFE', [])
        T['gaeste'] = f'''
<section class="fl {FL['gaeste']} blatt gf" id="gaeste">
  <div class="in">
    {kopf_('gaeste')}
    <div class="gang"><div class="band">{gaeste_html}</div>{gangfuss()}</div>
    {f'<div class="kn-reihe" data-a="auf" style="margin-top:clamp(28px,3.2vw,46px);justify-content:center">{"".join(kn(t_, h_, "" if i == 0 else "kn--linie", neu=True) for i, (t_, h_) in enumerate(gk))}</div>' if gk else ''}
  </div>
</section>'''
    else:
        T['gaeste'] = ''

    # --- Mails: jede Nachricht an die Gäste im Stil der Seite, als Band wie die Ideen, darunter die Sprachen und der Weg zur Übersicht (11.10.2026)
    MLS = getattr(H, 'MAILS', None)
    if MLS and 'mails' in NR:
        ml_html = ''.join(f'<article class="idee" data-a="kipp" style="--i:{min(i, 3)}"><div class="idee__b">{bild(f"ml-{i}", ti, stil="--op:50% 0")}<span class="idee__n">{nr_}</span></div><h3>{e(ti)}</h3><p>{e(x)}</p></article>'
                          for i, (_, nr_, ti, x) in enumerate(MLS['liste']) if f'ml-{i}' in m)
        spr = ''.join(f'<span{" dir=rtl" if n_ == "العربية" else ""}>{e(n_)}</span>' for n_ in MLS.get('sprachen', []))
        T['mails'] = f'''
<section class="fl {FL['mails']} blatt ml" id="mails">
  <div class="in">
    {kopf_('mails')}
    <div class="gang"><div class="band">{ml_html}</div>{gangfuss()}</div>
    {f'<p class="ml__sprachen" data-a="auf">{spr}</p>' if spr else ''}
    <div class="kn-reihe" data-a="auf" style="margin-top:clamp(24px,2.8vw,40px);justify-content:center">{kn(MLS.get('knopf', 'Alle Mails ansehen'), MLS.get('link', '../mails/'), '', neu=True)}</div>
  </div>
</section>'''
    else:
        T['mails'] = ''

    # --- Rezeption im Chat: dunkle Bühne, Film links, Punkte in Gold rechts; darunter Zimmermappe, Karte mit QR-Code, die Seite dazu
    RZ = getattr(H, 'REZEPTION', None)
    if RZ and 'rezeption' in NR:
        film_da = os.path.exists(os.path.join(ZIEL, 'film', 's-rezeption.mp4'))
        rez_pkt = ''.join(f'<li data-a="auf" style="--i:{i}"><i>{i + 1:02d}</i><div><b>{e(ti)}</b><p>{e(x)}</p></div></li>' for i, (ti, x) in enumerate(RZ))
        RK = getattr(H, 'REZEPTION_KARTEN', {})
        km = RK.get('mappe', ('Am Handy', 'Die Zimmermappe.', 'Der Gast scannt die Karte im Zimmer und fragt in der Sprache seines Handys. Ändert sich etwas im Haus, stimmt die Mappe am selben Tag.'))
        kq = RK.get('karte', ('Auf dem Nachttisch', 'Die Karte mit dem Code.', 'Eine kleine Karte im Stil der Drucksachen, mit dem QR-Code zur Mappe.'))
        ks = RK.get('seite', ('Eigene Seite', 'Rezeption im Chat.', 'Ein Gespräch am Handy Schritt für Schritt, echte Antworten aus den Tests, die Buchung im Gespräch und was die Rezeption nicht tut.'))
        rez_link = getattr(H, 'REZEPTION_LINK', '../rezeption/')
        QR = K.qr_svg(H.MAPPE_ADRESSE) if getattr(H, 'MAPPE_ADRESSE', None) else ''
        kino_rez = (f'<div class="kino" data-a="gross"><div class="fen__k"><i></i><i></i><i></i><span>{H.KURZ} / startseite · rezeption im chat</span></div><div class="kino__s"><video muted playsinline preload="metadata" poster="film/s-rezeption.jpg" src="film/s-rezeption.mp4"></video><span class="kino__play" data-wort="Gross ansehen"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3.5v17l14-8.5z"/></svg></span><span class="kino__hin">Klick oder Esc zum Anhalten</span><div class="kino__k"><button type="button" data-nochmal>Nochmal</button></div></div></div>'
                    if film_da else (f'<div class="fen" data-a="gross"><div class="fen__k"><i></i><i></i><i></i><span>{H.KURZ} / startseite · rezeption im chat</span></div>{bild("ch-chat", "Die Rezeption im Chat auf der Startseite")}</div>' if 'ch-chat' in m else ''))
        T['rezeption'] = f'''
<section class="fl {FL['rezeption']} blatt" id="rezeption">
  <div class="in">
    {kopf_('rezeption')}
    <div class="chatb">
      {kino_rez}
      <div><ul class="punkte">{rez_pkt}</ul>
        <div class="chatb__gross" data-a="auf">{kn('Alles, was sie kann: die Seite dazu', rez_link, 'kn--hell', neu=True)}{kn('Rezeption auf der Website öffnen', '../index.html', 'kn--linie', neu=True)}</div></div>
    </div>
    <div class="chatb__dazu">
      {f'<div class="cz" data-a="kipp" style="--i:0"><div class="cz__b cz__b--tel">{bild("ch-chat-h", "Die Rezeption im Chat am Handy")}</div><div class="cz__t"><small>{e(km[0])}</small><h3>{e(km[1])}</h3><p>{km[2]}</p>{kn('Zimmermappe öffnen', getattr(H, 'MAPPE_LINK', '../mappe.html'), 'kn--klein kn--linie', neu=True) if os.path.exists(os.path.join(ROOT, 'mappe.html')) else ''}</div></div>' if 'ch-chat-h' in m else ''}
      <div class="cz" data-a="kipp" style="--i:1"><div class="cz__b cz__b--qr">{bild('qr-karte', 'Die Karte zur Zimmermappe mit QR-Code') if 'qr-karte' in m else QR}</div><div class="cz__t"><small>{e(kq[0])}</small><h3>{e(kq[1])}</h3><p>{kq[2]}</p>{f'<div class="qr">{QR}<div><b>Zum Ausprobieren</b><span>Mit der Kamera des Handys scannen: die Zimmermappe des Entwurfs öffnet sich.</span></div></div>' if QR else ''}</div></div>
      {f'<a class="cz" href="{rez_link}" target="_blank" rel="noopener" data-a="kipp" style="--i:2"><div class="cz__b">{bild("ch-rezeption", "Die Seite «Rezeption im Chat»")}</div><div class="cz__t"><small>{e(ks[0])}</small><h3>{e(ks[1])}</h3><p>{ks[2]}</p><span class="pfeil">Seite ansehen{PF}</span></div></a>' if 'ch-rezeption' in m else ''}
    </div>
    {f'<p class="hinweis hinweis--dunkel" data-a="auf">{H.REZEPTION_HINWEIS}</p>' if getattr(H, 'REZEPTION_HINWEIS', '') else ''}
  </div>
</section>'''
    else:
        T['rezeption'] = ''

    # --- Geprüft: drei Karten, Knopf zur Seite mit dem ganzen Prüfbericht (nur Belegtes, in Alltagssprache)
    GP = getattr(H, 'GEPRUEFT', None)
    TRIO, PUNKTE = getattr(H, 'GEPRUEFT_TRIO', None), getattr(H, 'GEPRUEFT_PUNKTE', None)
    if callable(getattr(H, 'geprueft_abschnitt', None)) and 'geprueft' in NR:   # eigener Aufbau eines Hauses, ganz in haus.py (Grand Beau-Rivage 11.10.2026)
        T['geprueft'] = H.geprueft_abschnitt(dict(bild=bild, kn=kn, titel=titel, e=e, m=m, kap=KAP['geprueft']))
    elif GP and 'geprueft' in NR and TRIO and PUNKTE and all(f'gt-{i}' in m for i in range(len(TRIO))):
        # Collage wie bei Salt & Silver (10.10.2026): drei echte Fotos des Hauses, leicht treibend, Einkerbung mit Ort, roter Stempel auf dem letzten; rechts vier Zeilen mit Nummer und Haken
        stempel_text = getattr(H, 'STEMPEL_TEXT', f'GEPRÜFT · {(H.LEISTE or H.NAME).upper()} · {K.STAND} ·')
        stempel = (f'<svg class="gst" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="gstk" d="M100 100m-74 0a74 74 0 1 1 148 0a74 74 0 1 1-148 0"/></defs>'
                   '<circle cx="100" cy="100" r="94" fill="none" stroke="currentColor" stroke-width="5"/><circle cx="100" cy="100" r="58" fill="none" stroke="currentColor" stroke-width="2"/>'
                   f'<text font-family="DM Mono" font-size="15.5" letter-spacing="3.2" fill="currentColor"><textPath href="#gstk">{e(stempel_text)}</textPath></text>'
                   '<path d="M74 101l17 17 36-38" fill="none" stroke="currentColor" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>')
        trio_html = ''.join(f'<div class="gt__d" data-drift="{d_}"><figure class="gt__b" data-a="auf" style="--i:{i * 2}">{bild(f"gt-{i}", n_)}<span class="kerbe">{e(n_)}</span>{stempel if i == len(TRIO) - 1 else ""}</figure></div>'
                            for i, ((_, _, _, n_), d_) in enumerate(zip(TRIO, ('-0.05', '0.06', '-0.09'))))
        pz_html = ''.join(f'<li class="pz" data-a="auf" style="--i:{i}"><b>{i + 1:02d}</b><div><h3>{e(ti)}</h3><p>{e(x)}</p></div><i class="pz__ok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7"/></svg></i></li>' for i, (ti, x) in enumerate(PUNKTE))
        T['geprueft'] = f'''
<section class="fl {FL['geprueft']} blatt gp2" id="geprueft">
  <span class="gp2__wort" aria-hidden="true">{e(KAP['geprueft']['name'])}</span>
  <div class="in gp3">
    <div class="gt">{trio_html}</div>
    <div class="gp3__t">
      {kap(NR['geprueft'], KAP['geprueft']['name'])}
      {titel(KAP['geprueft']['zeilen'])}
      <div class="lauf" style="margin-top:clamp(18px,2vw,28px)"><p data-a="worte">{KAP['geprueft']['text']}</p></div>
      <ol class="pzl">{pz_html}</ol>
      <div class="gepr__f" data-a="auf"><p>{getattr(H, 'GEPRUEFT_OFFEN', '')}</p>{kn('Den ganzen Prüfbericht lesen', 'geprueft/index.html', neu=True)}</div>
    </div>
  </div>
</section>'''
    elif GP and 'geprueft' in NR:
        gepr_html = ''.join(f'<div class="gk" data-a="kipp" style="--i:{i}">{ZEICHEN[z_]}<h3>{e(ti)}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in zeilen[:4])}</ul></div>' for i, (ti, z_, zeilen) in enumerate(GP))
        T['geprueft'] = f'''
<section class="fl {FL['geprueft']} blatt" id="geprueft">
  <div class="in">
    {kopf_('geprueft')}
    <div class="gepr">{gepr_html}</div>
    <div class="gepr__f" data-a="auf"><p>{getattr(H, 'GEPRUEFT_OFFEN', '')}</p>{kn('Den ganzen Prüfbericht lesen', 'geprueft/index.html', neu=True)}</div>
  </div>
</section>'''
    else:
        T['geprueft'] = ''
    # --- Feed: je Haus eine andere Auslage neben dem Handy, passend zu seinem Aufbau
    if 'feed' in NR:
        fa = FD.get('art', 'abzuege')
        handy = f'<div class="feedb__h" data-a="schweb" style="--i:0">{bild("feed-handy", "Das Instagram-Profil des Hauses als Idee, auf einem Handy")}</div>'
        if fa == 'spalten':      # drei Spalten, jede mit eigenem Thema
            rechts = '<div class="fsp">' + ''.join(   # die Spalten liegen gross und gedämpft hinter dem Handy
                f'<div class="fsp__s" data-a="auf" style="--i:{i}">{"".join(bild("fp-" + str(n_)) for n_ in nrn)}</div>' for i, (name, nrn) in enumerate(FD['spalten'])) + '</div>' + handy.replace('--i:0', '--i:2')
        elif fa == 'streifen':   # Reihen, in denen ein Bild über drei Beiträge läuft
            rechts = handy + '<div class="fst">' + ''.join(
                f'<div class="fst__s" data-a="schweb" data-drift="{dr_}" style="--i:{i + 1};--r:{r_}deg;--r0:{r_ * 3}deg"><div>{"".join(bild("fp-" + str(n_)) for n_ in nrn)}</div><span class="mono">{e(name)}</span></div>'
                for i, (name, nrn, r_, dr_) in enumerate(FD['streifen'])) + '</div>'
        elif fa == 'bogen':      # ein Ausschnitt des Rasters als Bogen: Bild und Blatt im Wechsel
            rechts = handy + f'<div class="fbo" data-a="kipp" style="--i:1"><div class="fbo__r">{"".join(bild("fp-" + str(n_)) for n_ in FD["bogen"])}</div><span class="mono">{e(FD["bogen_zeile"])}</span></div>'
        else:
            rechts = handy + ''.join(f'<div class="abzug feedb__k feedb__k--{i + 1}" data-a="schweb" data-drift="{dr}" style="--i:{i + 2};--r:{r}deg;--r0:{r * 3}deg">{bild("fp-" + str(nr_))}<span>{e(name)}</span></div>' for i, (nr_, name, r, dr) in enumerate(FD['kacheln']))
        T['feed'] = f'''
<section class="fl {FL['feed']} blatt" id="feed">
  <div class="in feedb feedb--{fa}">
    <div>
      {kap(NR['feed'], KAP['feed']['name'])}
      {titel(KAP['feed']['zeilen'])}
      <div class="lauf" style="margin-top:clamp(22px,2.6vw,36px)"><p data-a="worte">{FD['text1']}</p><p data-a="worte">{FD['text2']}</p></div>
      <div class="kn-reihe" data-a="auf" style="margin-top:30px">{kn('Feed ansehen', '../feed/index.html', neu=True)}</div>
    </div>
    <div class="feedb__r" aria-hidden="true">{rechts}</div>
  </div>
</section>'''
    else:
        T['feed'] = ''
    pk_e = f'<div class="pk" data-a="kipp"><div class="pk__b">{kleb_html}</div><h3>{z["etiketten"]} {e(ET["name"])}</h3><p>{PA["etik_text"]}</p>{kn(ET["name"] + " ansehen", f"../{ET['ordner']}/index.html", neu=True)}</div>'
    pk_d = f'<div class="pk pk--hell" data-a="kipp" style="--i:1"><div class="pk__b">{bogen_html}</div><h3>{z["druck"]} Drucksachen</h3><p>{PA["druck_text"]}</p>{kn("Drucksachen ansehen", "../drucksachen/index.html", neu=True)}</div>'
    T['papier'] = '' if 'papier' not in NR else f'''
<section class="fl {FL['papier']} blatt" id="papier">
  <div class="in">
    {kopf_('papier')}
    <div class="papier{" papier--druck" if PA.get('druck_zuerst') else ""}">{pk_d + pk_e if PA.get('druck_zuerst') else pk_e + pk_d}</div>
  </div>
</section>'''
    T['material'] = '' if 'material' not in NR else f'''
<section class="fl {FL['material']} blatt" id="material">
  <div class="in mitte">
    <div class="streu" aria-hidden="true">{streu}</div>
    {kap(NR['material'], KAP['material']['name'], ' style="justify-content:center"')}
    {titel(KAP['material']['zeilen'])}
    <div class="lauf" style="margin-top:clamp(22px,2.6vw,36px)"><p data-a="worte">{KAP['material']['text']}</p></div>
    <div class="kn-reihe" data-a="auf" style="margin-top:clamp(28px,3.2vw,46px);justify-content:center">{kn('Ordner öffnen', '../material/index.html', neu=True)}</div>
  </div>
</section>'''
    T['dazu'] = f'''
<section class="fl {FL['dazu']} blatt" id="dazu">
  <div class="in">
    {kopf_('dazu')}
    <div class="dazu">
      {f'<div class="dazu__gross" data-a="kipp">{HZ}<small>{e(AU["gross"][0])}</small><h3>{e(AU["gross"][1])}</h3><p>{AU["gross"][2]}</p></div>' if AU.get('gross') else f'<div class="dazu__gross" data-a="kipp">{HZ}<small>Der nächste Schritt</small><h3>Das Studio</h3><p>{AU["studio"]}</p></div>' if AU.get('studio') else ''}
      <ul class="dazu__z{'' if AU.get('gross') or AU.get('studio') else ' dazu__z--breit'}">
        {''.join(f'<li data-a="auf" style="--i:{i}"><h3>{e(t)}</h3><p>{x}</p></li>' for i, (t, x) in enumerate(AU['punkte']))}
      </ul>
    </div>
  </div>
</section>'''
    T['schluss'] = f'''
<section class="schluss" id="schluss">
  {bild('schluss', klasse='schluss__b')}
  <div class="in">
    {kap(NR['schluss'], KAP['schluss']['name'])}
    {titel(KAP['schluss']['zeilen'], 'h2', 't1')}
    <div class="lauf">
      <p data-a="worte">{KAP['schluss']['text']}</p>
    </div>
    <p class="gruss-u{' gruss-u--bild' if SL.get('robert', True) else ''}" data-a="auf">{f'<span class="gruss-u__b">{bild("robert", "Robert Reff")}</span>' if SL.get('robert', True) else ''}<b>Freundliche Grüsse, <span class="gruss-u__n">Robert Reff</span></b><small>{SL.get('von', 'aus Koh Phangan')}</small></p>
    <div class="kn-reihe" data-a="auf">{kn('Robert schreiben', 'mailto:robert@tasty-studios.de?subject=' + H.NAME.replace(' ', '%20') + '%20Website')}{kn('Website ansehen', '../index.html', 'kn--linie', neu=True)}</div>
  </div>
</section>'''

    for x in getattr(H, 'EIGENE', []):   # eigene Abschnitte eines Hauses (H.EIGENE), gebaut von seiner Funktion in haus.py
        if x['key'] in NR:
            T[x['key']] = x['bau'](dict(bild=bild, kn=kn, titel=titel, e=e, m=m, kap=KAP[x['key']], nr=NR[x['key']], fl=FL[x['key']], kopf=lambda f=x['key']: kopf_(f), z=z))

    # ------------------------------------------------------------ Auftakt: je Haus eine andere Bühne, damit keine Werkbank wie die andere beginnt
    art = A.get('art', 'stapel')
    erste = [f for f in FOLGE if f != 'lauf'][0]
    knoepfe = f'<div class="kn-reihe" data-a="auf" style="--i:10">{kn("Website ansehen", "../index.html", neu=True)}{kn("Weiterlesen", "#" + erste, "kn--linie")}</div>' + A.get('zusatz', '')
    gruss = f'<p class="gruss" data-a="auf">{e(H.ANREDE)}</p>'
    h1 = titel(A['titel'], 'h1', 't1')
    lauf_a = f'<div class="lauf"><p data-a="worte" style="--vz:2100ms">{A["text"]}</p></div>'
    fen = lambda mehr='': f'<div class="fen" data-a="schweb"{mehr}><div class="fen__k"><i></i><i></i><i></i><span>{H.KURZ} / startseite</span></div>{bild("auftakt", lazy=False)}</div>'
    inhalt = [(t_, z_.format(**z), '#' + a_) for t_, z_, a_ in A.get('inhalt', [])]
    if art == 'titelblatt':   # wie das Titelblatt eines Hausmagazins: ein Foto über die ganze Fläche, Kopfzeile, daneben das Inhaltsverzeichnis
        zeilen_i = ''.join(f'<a href="{a_}"><b>{e(t_)}</b><small>{e(z_)}</small>{PF}</a>' for t_, z_, a_ in inhalt)
        abz = ''.join(abzug(k_, u_, f'tb__a tb__a--{i + 1}', f' data-drift="{dr_}"') for i, ((k_, u_), dr_) in enumerate(zip(A['abzuege'], ('-0.07', '0.08'))))
        buehne = f'''{bild('titelbild', klasse='tb__bild', lazy=False)}
  <div class="in tb__kopf mono" data-a="auf"><span>{e(A['kopfzeile'][0])}</span>{HZ}<span>{e(A['kopfzeile'][1])}</span></div>
  <div class="in tb">
    <div class="auftakt__t">{gruss}{h1}{lauf_a}{knoepfe}</div>
    <div class="tb__r">
      <nav class="tb__inhalt" data-a="kipp" style="--i:3" aria-label="Inhalt"><p class="tb__it">{e(A['inhalt_titel'])}</p>{zeilen_i}</nav>
      {abz}
      <div class="tel" data-a="schweb" aria-hidden="true">{bild('auftakt-h', lazy=False)}</div>
    </div>
  </div>'''
    elif art == 'karte':      # wie eine Karte auf dem Tisch: was es gibt, mit Punktlinie und Zahl, die Abzüge liegen rundherum
        zeilen_i = ''.join(f'<a href="{a_}"><span>{e(t_)}</span><i></i><b>{e(z_)}</b></a>' for t_, z_, a_ in inhalt)
        abz = ''.join(abzug(k_, u_, f'kt__a kt__a--{i + 1}', f' data-drift="{dr_}"') for i, ((k_, u_), dr_) in enumerate(zip(A['abzuege'], ('-0.08', '0.1', '-0.06', '0.07', '-0.05'))))
        buehne = f'''<div class="in kt">
    <div class="auftakt__t">{gruss}{h1}{lauf_a}{knoepfe}</div>
    <div class="kt__tisch">
      {abz}
      <nav class="kt__karte" data-a="kipp" style="--i:2" aria-label="Inhalt">{HZ}<p class="kt__t">{e(A['inhalt_titel'])}</p><p class="kt__u mono">{e(A['inhalt_unter'])}</p>{zeilen_i}<p class="kt__f">{e(A['inhalt_fuss'])}</p></nav>
      <div class="tel" data-a="schweb" aria-hidden="true">{bild('auftakt-h', lazy=False)}</div>
    </div>
  </div>'''
    elif art == 'weg':        # der Weg hinauf: vier Abzüge steigen von links unten an, oben rechts steht die neue Seite
        abz = ''.join(abzug(k_, u_, f'wg__s wg__s--{i + 1}', f' data-drift="{dr_}"') for i, ((k_, u_), dr_) in enumerate(zip(A['abzuege'], ('-0.04', '0.05', '-0.06', '0.07'))))
        buehne = f'''<div class="in wg__kopf">
    <div>{gruss}{h1}</div>
    <div class="wg__t">{lauf_a}{knoepfe}</div>
  </div>
  <div class="in wg" aria-hidden="true">
    <svg class="wg__linie" viewBox="0 0 1000 300" preserveAspectRatio="none"><path d="M10 268 C150 262 196 214 300 206 S452 150 548 136 S690 84 800 70"/></svg>
    {abz}
    <div class="wg__ziel">{fen(' style="--i:6;--r:1.5deg;--r0:5deg"')}<div class="tel" data-a="schweb">{bild('auftakt-h', lazy=False)}</div></div>
  </div>'''
    else:                     # 'stapel': Fenster, drei Abzüge und ein Handy übereinander (so beginnt die Werkbank des Carlton-Europe)
        buehne = f'''<div class="in">
    <div class="auftakt__t">{gruss}{h1}{lauf_a}{knoepfe}</div>
    <div class="stapel" aria-hidden="true">
      {fen(' data-drift="0.05" style="--i:2"')}
      {abzug(A['abzuege'][0][0], A['abzuege'][0][1], 'abzug--1', ' data-drift="-0.09"')}
      {abzug(A['abzuege'][1][0], A['abzuege'][1][1], 'abzug--2', ' data-drift="0.11"')}
      {abzug(A['abzuege'][2][0], A['abzuege'][2][1], 'abzug--3', ' data-drift="-0.06"')}
      <div class="tel" data-a="schweb">{bild('auftakt-h', lazy=False)}</div>
    </div>
  </div>'''
    NAVNAME = {'brief': 'Guten Tag', 'ideen': 'Ideen', 'seiten': 'Seiten', 'gaeste': 'Gäste', 'studio': getattr(H, 'STUDIO', {}).get('name', 'Studio'), 'rezeption': 'Rezeption', 'feed': 'Feed', 'papier': 'Papier', 'mails': 'Mails', 'geprueft': 'Geprüft'}
    if not getattr(H, 'GAESTE', None): NAVNAME['gefuege'] = 'Gefüge'
    if not getattr(H, 'GEPRUEFT', None): NAVNAME['material'] = 'Material'
    NAVNAME.update({x['key']: x['nav'] for x in getattr(H, 'EIGENE', []) if x.get('nav')})
    NAVNAME.update(getattr(H, 'NAVNAME', {}))
    nav = ''.join(f'<a href="#{f}">{NAVNAME[f]}</a>' for f in FOLGE if NAVNAME.get(f))

    seite = f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Werkbank · {e(H.NAME)}</title>
<meta name="description" content="Ein Entwurf für die neue Website des {e(H.NAME)}, mit Unterlagen und Ideen für Papier. Alles auf einen Blick.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{H.FARBEN['nacht']}">
<meta property="og:title" content="Werkbank · {e(H.NAME)}">
<meta property="og:description" content="Ein Entwurf für die neue Website des {e(H.NAME)}, mit Unterlagen, Studio und Ideen für Papier.">
<meta property="og:image" content="{getattr(H, 'ONLINE', '')}werkbank/img/og.jpg">
<meta property="og:type" content="website">
<link rel="preload" href="fonts/{H.SCHRIFT['titel'][1]}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="img/auftakt.webp" as="image">
<link rel="preload" href="img/auftakt-h.webp" as="image">
<link rel="stylesheet" href="werkbank.css?v={K.v('werkbank.css')}">
</head>
<body class="haus-{H.KURZ}">
{K.sprite()}
<div class="gang-linie" aria-hidden="true"></div>
<header class="leiste"><div class="insel">
  <a class="insel__m" href="#oben">{HZ}{f"<b>{e(H.LEISTE)}</b>" if H.LEISTE else ""}<span>Werkbank</span></a>
  <nav aria-label="Abschnitte">{nav}</nav>
  <a class="glanz" href="../index.html" target="_blank" rel="noopener">Zur Website{PF}</a>
</div></header>

<main id="oben">
<section class="auftakt auftakt--{art}">
  {buehne}
  <div class="in auftakt__fuss mono" data-a="auf" style="--i:13"><span class="runter"><i></i>Einfach nach unten scrollen</span><span>Stand {K.STAND}</span><span>Robert Reff · Tasty Studios</span></div>
</section>
{''.join(T[f] for f in FOLGE)}
</main>

<footer class="fuss">
{H.wege_abschnitt(wege) if callable(getattr(H, 'wege_abschnitt', None)) else WEGE_STANDARD}
<div class="in fuss__u">
  <div><b>Werkbank zum Entwurf</b><p>Das ist ein Entwurf von Robert Reff, Tasty Studios, und nicht die offizielle Website des Hauses. Fotos, Zeichen und Texte gehören {H.RECHTE}</p></div>
  <div class="r mono">{alle_vier}<a href="mailto:robert@tasty-studios.de">robert@tasty-studios.de</a><a href="https://www.instagram.com/tasty_studios2026" target="_blank" rel="noopener">@tasty_studios2026</a><span>Stand {K.STAND}</span></div>
</div></footer>

<script>window.GEFUEGE={json.dumps(g, ensure_ascii=False)};window.SEITEN={json.dumps(seiten, ensure_ascii=False)};</script>
<script src="werkbank.js?v={K.v('werkbank.js')}"></script>
</body>
</html>
'''
    K.schreib(os.path.join(ZIEL, 'index.html'), seite)
    if getattr(H, 'GEPRUEFT_MEHR', None):
        geprueft_seite()
    gebraucht = {k + '.webp' for k in m} | {'og.jpg'}
    for f in os.listdir(IMG):
        if f not in gebraucht:
            os.remove(os.path.join(IMG, f))
    json.dump(z, open(os.path.join(W, 'zahlen.json'), 'w'), indent=1)
    print('gebaut:', os.path.join(ZIEL, 'index.html'), z, 'Seiten:', len(seiten), 'Ansichten:', sum(s['n'] for s in seiten))


if __name__ == '__main__':
    baue()
    if callable(getattr(H, 'nach_bau', None)):   # Haus-eigener Schritt nach dem Bau (Grand Beau-Rivage: Werkbank in fünf weiteren Sprachen)
        H.nach_bau()
