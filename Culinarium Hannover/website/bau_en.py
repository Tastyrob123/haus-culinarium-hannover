#!/usr/bin/env python3
"""Culinarium Hannover · englische Fassung unter website/en/ (29.10.2026, Auftrag des Oberchefs; Robert: «die Seite auf Englisch können wir ja auch schon übersetzen»).
Liest die fertig gebauten deutschen Seiten (website/*.html, Ergebnis von bau.py) und die Tabelle en/texte.json und schreibt daraus:
  en/<seite>.html          die zehn Seiten, Englisch, mit lang="en", hreflang, og-Angaben; Bilder, Stile und Skripte aus ../assets/
  en/assets/culinarium.js  Kopie mit englischen Texten (Menü-Knopf, Warteliste)
  en/assets/buchen.js      Kopie mit englischen Texten (Terminplakate, Buchen-Dialog, Pflegeseite)
  en/assets/en.css         nur Ergänzungen (englische Zeile unter Momos Karten)
  en/fehlt.txt             deutsche Reste, die die Tabelle nicht kennt (Ziel: leer)
  en/bleibt.txt            was bewusst nicht übersetzt wurde (für die Meldung)
Aufruf: python3 website/bau_en.py   (nach bau.py; bau.py wird hier nicht angefasst).
Wie es übersetzt: Textknoten und sichtbare Attribute (alt, title, placeholder, aria-label, description, data-lauf, data-t für den Neon-Schein) werden einzeln in der Tabelle nachgeschlagen.
Daten («Fr 25. und Sa 26. September 2026»), Preise («89,00 EUR»), Monatsangaben, Zeilen mit « · » und Quellenangaben übersetzt das Skript nach Regeln.
Momos Menükarten (mk2-t, mk2-d) bleiben Deutsch und bekommen aus «gloss» eine englische Zeile darunter. Rudis Zeilen, Namen, Adressen stehen in «bleibt».
Knöpfe mit gestalteten «i» (<em class="ki">i</em>) werden zusammengesetzt, übersetzt und wieder gesetzt."""
import html, json, os, re, subprocess, sys

HIER = os.path.dirname(os.path.abspath(__file__))
EN = os.path.join(HIER, 'en')
A_EN = os.path.join(EN, 'assets')
T = json.load(open(os.path.join(EN, 'texte.json'), encoding='utf-8'))
TEXTE, BLEIBT, GLOSS, MON, WT = T['texte'], T['bleibt'], T['gloss'], T['monate'], T['wochentage']
SEITEN = ['index', 'abend', 'abende', 'bar', 'leute', 'weg', 'dirty-chicken', 'termine-pflege', 'impressum', 'datenschutz']
VERSION = re.search(r"^VERSION = '(\w+)'", open(os.path.join(HIER, 'bau.py'), encoding='utf-8').read(), re.M).group(1)
ADRESSE = 'https://culinarium-hannover-entwurf.vercel.app/'
JS_EN = list(T['js'])                                     # Skripte, die in en/assets/ als übersetzte Kopie liegen
ALT_WEG = 'href="../../Walk%20on%20the%20Wild%20Side%20Hannover/'   # Knopf «Zur Website der Bar» (bar.html), lokal eine Ebene tiefer
KI = '<em class="ki">i</em>'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr',
        'use', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'ellipse', 'stop', 'textpath'}
MONATE = '|'.join(MON)
DATUM = re.compile(r'^(Mo|Di|Mi|Do|Fr|Sa|So) (\d{1,2})\.(?: und (Mo|Di|Mi|Do|Fr|Sa|So) (\d{1,2})\.)? (%s) (\d{4})$' % MONATE)
NEUTRAL = [re.compile(r'^[A-Za-z0-9_-]+ \(\d\d\.\d\d\.\d{4}\)$'),           # Beitragskennung (Datum)
           re.compile(r'^@[\w.]+ \([^)]*\)$'), re.compile(r'^\d\d\.\d\d\.\d{4}$')]

fehlt, bleibt_hits, fertig = {}, {}, set(TEXTE.values()) | set(GLOSS.values())


def norm(s):
    return ' '.join(s.split())


def neutral(s):
    return (not re.search(r'[A-Za-zÄÖÜäöüß]', s) or s.startswith('@') or s.startswith('+49') or re.fullmatch(r'[IVX]+', s)
            or len(s) <= 1 or any(r.match(s) for r in NEUTRAL))


def uebersetze(s, seite):
    s = norm(s)
    if not s or neutral(s):
        return s
    if s in TEXTE:
        return TEXTE[s]
    if s in BLEIBT:
        bleibt_hits.setdefault(s, set()).add(seite)
        return s
    if s in fertig:
        return s
    r = regel(s, seite)
    if r is not None:
        fertig.add(r)
        return r
    fehlt.setdefault(s, set()).add(seite)
    return s


def regel(s, seite):
    if ' · ' in s:
        return ' · '.join(uebersetze(t, seite) for t in s.split(' · '))
    m = DATUM.match(s)
    if m:
        a = '%s %d' % (WT[m[1]], int(m[2]))
        if m[3]:
            a += ' and %s %d' % (WT[m[3]], int(m[4]))
        return '%s %s %s' % (a, MON[m[5]], m[6])
    m = re.fullmatch(r'(\d+),(\d\d) EUR', s)
    if m:
        return '%s.%s EUR' % (m[1], m[2])
    m = re.fullmatch(r'(\d+) Plätze', s)
    if m:
        return '%s seats' % m[1]
    m = re.fullmatch(r'(%s) (\d{4})' % MONATE, s)
    if m:
        return '%s %s' % (MON[m[1]], m[2])
    for de, en in T['praefixe']:
        if s.startswith(de):
            rest = s[len(de):]
            rest2 = rest
            for d2, e2 in T['stuecke']:
                rest2 = rest2.replace(d2, e2)
            if rest2 != rest or neutral(rest2):
                return en + rest2
            return en + uebersetze(rest2, seite)
    return None


def esc_text(s):
    return s.replace('&', '&amp;').replace('<', '&lt;')


def esc_attr(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')


def ki_knoepfe(h, seite):
    """Knöpfe, deren Text bau.py mit <em class="ki">i</em> gesetzt hat: Text zusammensetzen, übersetzen, «i» wieder setzen. data-en schützt vor dem zweiten Durchlauf."""
    def f(m):
        inner = m.group(2)
        if KI not in inner:
            return m.group(0)
        plain = html.unescape(inner.replace(KI, 'i'))
        en = uebersetze(plain, seite)
        return m.group(1) + '<span data-en>' + esc_text(en).replace('i', KI) + '</span>'
    return re.sub(r'(<(?:a|button)\b[^>]*\bclass="knopf[^"]*"[^>]*>)<span>(.*?)</span>', f, h, flags=re.S)


def sprachschalter(h, name):
    """Schalter DE/EN, sobald bau.py ihn setzt (.leiste-sprache «EN», .menue-sprache/.fu-sprache «English», href en/<seite>): hier zurück auf Deutsch."""
    def f(m):
        tag, text = m.group(1), m.group(2)
        tag = tag.replace('href="en/' + name + '.html"', 'href="../' + name + '.html"').replace('hreflang="en"', 'hreflang="de"').replace('lang="en"', 'lang="de"')
        tag = tag.replace('aria-label="English version"', 'aria-label="Deutsche Fassung"')
        return tag + ('DE' if text.strip() == 'EN' else 'Deutsch' if text.strip() == 'English' else text) + '</a>'
    h = re.sub(r'(<a\b[^>]*\bclass="(?:leiste|menue|fu)-sprache"[^>]*>)([^<]*)</a>', f, h)
    def g(m):   # Knopf unten links: «English» + Kreis «EN» → «Deutsch» + «DE»
        tag = m.group(1).replace('href="en/' + name + '.html"', 'href="../' + name + '.html"').replace('hreflang="en"', 'hreflang="de"').replace('lang="en"', 'lang="de"').replace('aria-label="English version"', 'aria-label="Deutsche Fassung"')
        return tag + '<span>Deutsch</span><i><span>DE</span></i></a>'
    return re.sub(r'(<a\b[^>]*\bclass="knopf sprache-knopf"[^>]*>)<span>.*?</span><i><span>EN</span></i></a>', g, h)


def attribute(tag, seite):
    def f(m):
        a, v = m.group(1), m.group(2)
        if not v.strip():
            return m.group(0)
        if a == 'content' and not re.search(r'name="description"|property="og:', tag):
            return m.group(0)
        if a == 'value' and 'type="submit"' not in tag:
            return m.group(0)
        s = html.unescape(v)
        en = uebersetze(s, seite)
        if en == norm(s):
            return m.group(0)
        return '%s="%s"' % (a, esc_attr(en))
    return re.sub(r'\b(alt|title|placeholder|aria-label|content|value|data-lauf|data-t)="([^"]*)"', f, tag)


def pfade(tag):
    """assets/ liegt eine Ebene höher; die übersetzten Skripte liegen in en/assets/."""
    for js in JS_EN:
        tag = tag.replace('src="assets/%s?' % js, 'src="\x00%s?' % js)
    tag = re.sub(r'(?<=["\s,(])assets/', '../assets/', tag)
    tag = tag.replace('src="\x00', 'src="assets/')
    tag = tag.replace(ALT_WEG, ALT_WEG.replace('href="../../', 'href="../../../'))
    return tag


def seite_bauen(name):
    h = open(os.path.join(HIER, name + '.html'), encoding='utf-8').read().replace('\u00a0', ' ')   # waisen.py (30.10.2026) setzt nach dem Bau &nbsp; in Titel; für die Übersetzung wieder normale Leerzeichen
    h = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', h)       # die deutschen hreflang-Zeilen; unten kommen die eigenen
    h = sprachschalter(h, name)
    h = ki_knoepfe(h, name)
    teile = re.split(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->|<[^>]+>)', h, flags=re.S)
    stapel, aus = [], []          # stapel: (tag, class, geschuetzt, sammel oder None)
    for t in teile:
        if not t:
            continue
        if t.startswith('<'):
            if t.startswith(('<script', '<style', '<!--', '<!')):
                aus.append(pfade(t) if t.startswith('<script') else t)
                continue
            m = re.match(r'<\s*(/?)([a-zA-Z0-9-]+)', t)
            if not m:
                aus.append(t); continue
            schliesst, tn = m.group(1) == '/', m.group(2).lower()
            if schliesst:
                while stapel:
                    e = stapel.pop()
                    if e[0] == tn:
                        break
                aus.append(t)
                if e[0] == tn and e[3] is not None:
                    text = norm(html.unescape(''.join(e[3])))
                    if text in GLOSS:
                        aus.append('<p class="mk2-en">%s</p>' % esc_text(GLOSS[text]))
                continue
            cls = (re.search(r'\bclass="([^"]*)"', t) or [None, ''])[1]
            geschuetzt = ' data-en' in t or (stapel and stapel[-1][2])
            if not geschuetzt:
                t = attribute(t, name)
            t = pfade(t)
            aus.append(t)
            if tn not in VOID and not t.endswith('/>'):
                sammel = [] if re.search(r'\bmk2-[td]\b', cls) else None
                stapel.append((tn, cls, bool(geschuetzt), sammel))
            continue
        # Text
        if stapel and stapel[-1][3] is not None:
            stapel[-1][3].append(t)
            aus.append(t); continue
        if (stapel and stapel[-1][2]) or not t.strip():
            aus.append(t); continue
        s = html.unescape(t)
        core = s.strip()
        en = uebersetze(core, name)
        if en == norm(core):
            aus.append(t)
        else:
            lead = s[:len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
            aus.append(lead + esc_text(en) + trail)
    out = ''.join(aus).replace(' data-en>', '>')
    out = out.replace('<html lang="de"', '<html lang="en"', 1)
    # Metadaten: hreflang auf beide Fassungen, og mit Titel und Beschreibung, eigene Stil-Ergänzung
    titel = html.unescape(re.search(r'<title>(.*?)</title>', out, re.S).group(1))
    besch = html.unescape((re.search(r'<meta name="description" content="([^"]*)"', out) or [None, ''])[1])
    de = ADRESSE + ('' if name == 'index' else name + '.html')
    en = ADRESSE + 'en/' + ('' if name == 'index' else name + '.html')
    meta = ('\n<link rel="alternate" hreflang="de" href="%s">\n<link rel="alternate" hreflang="en" href="%s">\n<link rel="alternate" hreflang="x-default" href="%s">'
            '\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:locale" content="en_GB">\n<meta property="og:type" content="website">'
            % (de, en, de, esc_attr(titel), esc_attr(besch)))
    out = re.sub(r'(<meta name="description" content="[^"]*">)', lambda m: m.group(1) + meta, out, count=1)
    out = out.replace('</head>', '<link rel="stylesheet" href="assets/en.css?v=%s">\n</head>' % VERSION, 1)
    open(os.path.join(EN, name + '.html'), 'w', encoding='utf-8').write(out)
    return out


def skripte():
    for js, ers in T['js'].items():
        q = open(os.path.join(HIER, 'assets', js), encoding='utf-8').read()
        for a, b in ers:
            if a == b:
                continue
            if a not in q:
                fehlt.setdefault('JS %s: Stelle nicht gefunden: %s' % (js, a[:70]), set()).add(js)
                continue
            q = q.replace(a, b)
        # was im Skript noch deutsch aussieht (Text in Anführungszeichen mit Umlaut, ausserhalb von Kommentaren)
        ohne = re.sub(r'/\*.*?\*/', '', q, flags=re.S)
        ohne = re.sub(r'//[^\n]*', '', ohne)
        for m in re.finditer(r"'([^'\n]*[äöüÄÖÜß][^'\n]*)'", ohne):
            if m.group(0) not in T.get('js_bleibt', []):
                fehlt.setdefault('JS %s: %s' % (js, m.group(1)[:80]), set()).add(js)
        open(os.path.join(A_EN, js), 'w', encoding='utf-8').write(q)
    open(os.path.join(A_EN, 'en.css'), 'w', encoding='utf-8').write(
        '/* Culinarium · englische Fassung (bau_en.py): nur Ergänzungen, alles andere kommt aus ../assets/ */\n'
        '.mk2-en{margin-top:3px;font:400 10.5px/1.45 var(--text);letter-spacing:.02em;color:#8A8590;text-transform:none}\n')


def nachpruefung():
    """Deutsche Reste in den fertigen Seiten: sichtbare Texte mit Umlaut oder typischen Wörtern, die nicht in «bleibt» stehen."""
    verdacht = re.compile(r'[äöüÄÖÜß]|\b(und|der|die|das|mit|für|nicht|ein|eine|auf|von|zum|zur|bei|ab)\b')
    funde = {}
    for name in SEITEN:
        h = open(os.path.join(EN, name + '.html'), encoding='utf-8').read()
        h = re.sub(r'<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>', '', h, flags=re.S)
        texte = [html.unescape(x) for x in re.findall(r'>([^<>]+)<', h)]
        texte += [html.unescape(x) for x in re.findall(r'\b(?:alt|title|placeholder|aria-label|data-lauf)="([^"]*)"', h)]
        texte += [html.unescape(x) for x in re.findall(r'name="description" content="([^"]*)"', h)]
        for s in texte:
            s = norm(s)
            if not s or neutral(s) or s in BLEIBT or s in fertig or s in GLOSS:
                continue
            if verdacht.search(s) and not re.fullmatch(r'[A-ZÄÖÜ\- ]+', s):
                funde.setdefault(s, set()).add(name)
    return funde


if __name__ == '__main__':
    os.makedirs(A_EN, exist_ok=True)
    for n in SEITEN:
        seite_bauen(n)
    skripte()
    funde = nachpruefung()
    with open(os.path.join(EN, 'fehlt.txt'), 'w', encoding='utf-8') as f:
        f.write('# Deutsche Reste, die en/texte.json nicht kennt (bau_en.py, Version %s)\n' % VERSION)
        for s, ps in sorted(fehlt.items(), key=lambda x: sorted(x[1])):
            f.write('%s\t%s\n' % (', '.join(sorted(ps)), s))
        if funde:
            f.write('\n# Nachprüfung der fertigen Seiten (Verdacht auf Deutsch)\n')
            for s, ps in sorted(funde.items(), key=lambda x: sorted(x[1])):
                f.write('%s\t%s\n' % (', '.join(sorted(ps)), s))
    with open(os.path.join(EN, 'bleibt.txt'), 'w', encoding='utf-8') as f:
        f.write('# Bewusst nicht übersetzt (bau_en.py, Version %s): Text\tGrund\tSeiten\n' % VERSION)
        for s, ps in sorted(bleibt_hits.items(), key=lambda x: (BLEIBT[x[0]], x[0])):
            f.write('%s\t%s\t%s\n' % (s, BLEIBT[s], ', '.join(sorted(ps))))
        f.write('\n# Momos Menükarten: Zutaten Deutsch, englische Zeile darunter (%d Zeilen)\n' % len(GLOSS))
    print('en/: %d Seiten, Version %s · fehlt: %d · Nachprüfung: %d · bleibt: %d Stellen · Gloss: %d'
          % (len(SEITEN), VERSION, len(fehlt), len(funde), len(bleibt_hits), len(GLOSS)))
    for s, ps in list(fehlt.items())[:40]:
        print('   FEHLT', ', '.join(sorted(ps)), '|', s[:110])
    for s, ps in list(funde.items())[:40]:
        print('   VERDACHT', ', '.join(sorted(ps)), '|', s[:110])
    # Kriterium 7 (30.10.2026): letzte zwei Wörter jeder Überschrift zusammenhalten, de und en, nach der Übersetzung
    subprocess.run([sys.executable, os.path.join(HIER, 'waisen.py')], check=True)
