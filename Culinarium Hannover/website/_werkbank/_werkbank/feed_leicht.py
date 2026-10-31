"""Feed der Werkbank leicht (Oberchef 18.10.2026, Regel M19, Robert 14:20 «es dauert sehr lange, bis es lädt»):
das Raster und die Highlights im Feed (feed/index.html) laden 400-px-WebP aus feed/thumbs-w/, die grossen Bilder erst beim Antippen eines Beitrags.
Läuft am Ende jedes Werkbank-Baus mit (haus.py) und allein: python3 _werkbank/feed_leicht.py
Gegenprobe Oberchef 29.10.2026: die Zahl der Beiträge im Kopf kommt aus feed.json; die ersten zwölf Kacheln laden sofort (eager) und stehen bis dahin
in der Farbe ihres Motivs statt als dunkles Loch (auch die übrigen); das Bild der geöffneten Ansicht hat einen leeren Platzhalter statt img ohne src."""
import glob, json, os, re, shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, 'feed')
IG = os.path.join(ROOT, '..', '..', '_quelle', 'extern')


def bisher():
    """Die echten bisherigen Beiträge von @culinarium_hannover (neuester zuerst), je das erste Bild, mit ihrem Text; dazu Rudis Beitrag mit
    Culinarium als Mitautor. Im Profil stehen sie unter den 60 neuen, so wie es nach dem Nachposten aussieht (Oberchef 29.10.2026)."""
    posts = {}
    for ordner in ('ig', 'ig-team'):
        try:
            h = json.load(open(os.path.join(IG, ordner, 'herkunft.json'), encoding='utf-8'))
        except OSError:
            continue
        for datei, v in h.items():
            if v.get('konto') != 'culinarium_hannover' and 'culinarium_hannover' not in (v.get('mitautoren') or []):
                continue
            pid = datei.rsplit('-', 1)[0][-11:]
            if v.get('bild_nr') == 1 or pid not in posts:   # das erste Bild eines Beitrags ist seine Kachel
                posts[pid] = dict(datei=os.path.join(IG, ordner, datei), datum=v.get('datum', ''), text=(v.get('text') or '').strip())
    return sorted(posts.values(), key=lambda x: x['datum'], reverse=True)


def mach():
    seite = os.path.join(F, 'index.html')
    if not os.path.exists(seite):
        return 0
    os.makedirs(os.path.join(F, 'thumbs-w'), exist_ok=True)
    for q in glob.glob(os.path.join(F, 'thumbs', '*.jpg')):
        z = os.path.join(F, 'thumbs-w', os.path.basename(q)[:-4] + '.webp')
        if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(q) or Image.open(z).width > 360:
            im = Image.open(q).convert('RGB')
            if im.width > 360:   # 3 Spalten am Handy, doppelte Dichte (Gegenprobe Oberchef 29.10.2026)
                im = im.resize((360, round(im.height * 360 / im.width)), Image.LANCZOS)
            im.save(z + '.neu', 'WEBP', quality=74, method=6)
            os.replace(z + '.neu', z)
    t = open(seite, encoding='utf-8').read()
    n = 0

    def um(m):
        nonlocal n
        name = m.group(1)
        if not os.path.exists(os.path.join(F, 'thumbs-w', name + '.webp')):
            return m.group(0)
        n += 1
        return f'src="thumbs-w/{name}.webp" decoding="async"'
    t2 = re.sub(r'src="thumbs/([A-Za-z0-9_-]+)\.jpg"', um, t)
    # Zahl der Beiträge aus feed.json
    try:
        zahl = len(json.load(open(os.path.join(F, 'feed.json'), encoding='utf-8'))['posts'])
        m_ = re.search(r'^BISHER = (\d+)', open(os.path.join(ROOT, '_werkbank', 'feed_daten.py'), encoding='utf-8').read(), re.M)
        zahl += int(m_.group(1)) if m_ else 0   # Gesamtzahl nach dem Nachposten: neue plus die heute schon geposteten
        t2 = re.sub(r'<b>[0-9.’]+</b><span>Beiträge</span>', f'<b>{zahl}</b><span>Beiträge</span>', t2, count=1)
    except (OSError, KeyError, ValueError):
        pass
    # Kacheln: Motivfarbe als Platzhalter, die ersten zwölf sofort laden
    def farbe(name):
        try:
            r, g, b = Image.open(os.path.join(F, 'thumbs-w', name + '.webp')).convert('RGB').resize((1, 1), Image.BOX).getpixel((0, 0))
            return f'#{r:02x}{g:02x}{b:02x}'
        except OSError:
            return '#222028'

    def kachel(m):
        i, label, name = int(m.group(1)), m.group(2), m.group(3)
        lade = ' loading="eager" fetchpriority="high"' if i < 12 else ' loading="lazy"'
        return f'style="--i:{i};background:{farbe(name)}" aria-label="{label}"><img src="thumbs-w/{name}.webp" decoding="async" alt=""{lade}>'
    t2 = re.sub(r'style="--i:(\d+)(?:;background:#[0-9a-f]{6})?" aria-label="([^"]*)"><img src="thumbs-w/([0-9]+)\.webp" decoding="async" alt=""'
                r'(?: loading=lazy| loading="eager" fetchpriority="high"| loading="lazy")?>', kachel, t2)
    # die echten bisherigen Beiträge unter den neuen: Kacheln, grosse Bilder, Texte (wiederholbar: vorige Fassung erst entfernen)
    t2 = re.sub(r'<button class="t alt"[^>]*>.*?</button>', '', t2)
    t2 = re.sub(r'<div class="band">.*?</div>', '', t2); t2 = re.sub(r'<i class="nr">\d+</i>', '', t2)
    try:
        n_neu = len(json.load(open(os.path.join(F, 'feed.json'), encoding='utf-8'))['posts'])
    except (OSError, KeyError, ValueError):
        n_neu = 0
    alt = bisher() if n_neu else []
    kacheln = ''
    for j, b_ in enumerate(alt):
        nr = n_neu + j + 1; i = nr - 1
        im = Image.open(b_['datei']).convert('RGB')
        im.resize((1080, round(im.height * 1080 / im.width)), Image.LANCZOS).save(os.path.join(F, 'posts', f'{nr:02d}.jpg'), quality=90)
        im.resize((360, round(im.height * 360 / im.width)), Image.LANCZOS).save(os.path.join(F, 'thumbs-w', f'{nr:02d}.webp'), 'WEBP', quality=74, method=6)
        kacheln += (f'<button class="t alt" type="button" data-i="{i}" style="--i:{i};background:{farbe(f"{nr:02d}")}" aria-label="Beitrag {nr} öffnen (bisher)">'
                    f'<img src="thumbs-w/{nr:02d}.webp" decoding="async" alt="" loading="lazy"></button>')
    if kacheln:   # dazwischen das Band (Bausteine uebergang.css / uebergang.js)
        band = '<div class="band"><b>↑</b> Die nächsten 60 · Euer Feed heute <b>↓</b></div>'
        k = t2.index('<div class="grid"'); e_ = t2.index('</div>', t2.index('>', k))
        t2 = t2[:e_] + band + kacheln + t2[e_:]
        # Nummer auf jeder neuen Kachel: Reihenfolge des Postens (Beitrag 1 = als Nächstes, unten im neuen Block)
        t2 = re.sub(r'(aria-label="Beitrag (\d+) öffnen"><img [^>]*>)', lambda m: m.group(1) + (f'<i class="nr">{n_neu + 1 - int(m.group(2))}</i>' if int(m.group(2)) <= n_neu else ''), t2)
        m_ = re.search(r'^BISHER = (\d+)', open(os.path.join(ROOT, '_werkbank', 'feed_daten.py'), encoding='utf-8').read(), re.M)
        heute = int(m_.group(1)) if m_ else len(alt)
        t2 = re.sub(r'<div class="grid"[^>]*id="grid"[^>]*>', f'<div class="grid" id="grid" data-heute="{heute}" data-gesamt="{n_neu + heute}">', t2)
        if 'uebergang.css' not in t2:
            t2 = t2.replace('</head>', '<link rel="stylesheet" href="uebergang.css">\n</head>', 1)
        if 'uebergang.js' not in t2:
            t2 = t2.replace('</body>', '<script src="uebergang.js" defer></script>\n</body>', 1)
    for f in glob.glob(os.path.join(F, 'posts', '*.jpg')) + glob.glob(os.path.join(F, 'thumbs-w', '[0-9]*.webp')):   # Reste früherer, längerer Fassungen
        nr = os.path.basename(f)[:2]
        if nr.isdigit() and int(nr) > n_neu + len(alt):
            os.remove(f)
    # Texte der Beiträge im Skript der Seite: die 60 neuen aus feed.json, dahinter die bisherigen
    dec = json.JSONDecoder()
    for name, neu in (('D', [p['cap'] for p in json.load(open(os.path.join(F, 'feed.json'), encoding='utf-8'))['posts']] + [b_['text'] for b_ in alt] if n_neu else None),
                      ('O', None)):
        k = t2.find(('var ' if name == 'D' else ' ') + name + ' = [')
        if k < 0:
            continue
        a0 = t2.index('[', k); liste, e_ = dec.raw_decode(t2, a0)
        if name == 'D' and neu is not None:
            liste = neu
        elif name == 'O':
            liste = (liste + [''] * (n_neu + len(alt)))[:n_neu + len(alt)]
        t2 = t2[:a0] + json.dumps(liste, ensure_ascii=False) + t2[e_:]
    # Bild der geöffneten Ansicht: verborgen, bis ein Beitrag geöffnet ist (uebergang.js zeigt es beim Öffnen)
    t2 = re.sub(r'<img class="img" id="pimg"[^>]*>', '<img class="img" id="pimg" alt="" hidden>', t2)
    # die ersten zwölf Kacheln im Kopf vorladen, mit hoher Priorität
    t2 = re.sub(r'<link rel="preload" as="image" href="thumbs-w/\d+\.webp"[^>]*>\n?', '', t2)
    vor = ''.join(f'<link rel="preload" as="image" href="thumbs-w/{i:02d}.webp" fetchpriority="high">\n' for i in range(1, 13) if os.path.exists(os.path.join(F, 'thumbs-w', f'{i:02d}.webp')))
    t2 = t2.replace('<meta name="viewport"', vor + '<meta name="viewport"', 1) if '<meta name="viewport"' in t2 else t2.replace('</head>', vor + '</head>', 1)
    if t2 != t:
        open(seite, 'w', encoding='utf-8').write(t2)
    return n


if __name__ == '__main__':
    print('feed leicht:', mach(), 'Vorschaubilder umgestellt')
