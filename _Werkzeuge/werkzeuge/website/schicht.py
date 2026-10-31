"""Schicht · legt die Änderungen eines Hauses über seine fertig gebauten Seiten.

Die Seiten selbst baut weiter das Haus. Dieses Modul liest eine gebaute Seite, findet jede änderbare Stelle
(Text, Foto, Link, Abschnitt) und setzt darüber, was im Werkzeug gespeichert ist. Bauart wie die Inhalts-Schicht
der bisherigen Studios (studio_inhalt.py), aber ohne ein einziges Wort über ein bestimmtes Haus: was ein Haus
besonders macht, steht in seiner Beschreibung (haeuser/<haus>.json) und kommt als «regeln» herein.

  zerlege(src, regeln)                 alle Stellen einer Seite, jede mit Fingerabdruck (h), Nummer (n) und Pfad
  anwenden(name, src, c, …)            die Schicht c über eine deutsche Seite
  anwenden_sprache(name, src, de, c, sp, …)   dieselbe Schicht über die Seite einer anderen Sprache
  waehle(baum, selektor, ab)           Elemente nach einem einfachen Selektor (für die Bereiche der Beschreibung)
  sauber(html, klassen)                Eingabe säubern: nur einfache Auszeichnung bleibt

Ist die Schicht leer, kommt jede Seite Byte für Byte unverändert zurück.
Nichts hier schreibt eine Datei."""
import hashlib
import html as _h
import posixpath
import re
from html.parser import HTMLParser

LEER = {'texte': [], 'bilder': [], 'links': [], 'aus': [], 'hinweis': {}, 'seo': [], 'angaben': {}}

INLINE = {'br', 'b', 'strong', 'i', 'em', 'span', 'small', 'a', 'u', 'sup', 'sub', 'wbr', 'mark', 's', 'abbr', 'q', 'bdi', 'bdo', 'time'}
VOID = {'br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'wbr', 'col', 'area', 'base', 'embed', 'track', 'param'}
AUS = {'script', 'style', 'svg', 'head', 'template', 'noscript', 'select', 'textarea', 'title', 'option', 'video', 'dialog', 'iframe', 'canvas'}
BLOECKE = {'section', 'article', 'li', 'figure', 'aside'}
FEST = {'header', 'footer', 'nav'}
_TAG = re.compile(r'<[^>]*>')


def leer():
    return {'texte': [], 'bilder': [], 'links': [], 'aus': [], 'hinweis': {}, 'seo': [], 'angaben': {}}


def ist_leer(c):
    return not any((c or {}).get(k) for k in LEER)


def klar(s):
    """Sichtbarer Text eines Stücks HTML, Leerraum zusammengefasst."""
    return re.sub(r'\s+', ' ', _h.unescape(_TAG.sub(' ', str(s))).replace('\xad', '')).strip()


def _hash(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[:10]


# ------------------------------------------------------------------ Seite als Baum (nur Positionen im Quelltext, nichts wird umgeschrieben)
class Baum(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.zl = [0] + [m.end() for m in re.finditer('\n', src)]
        self.wurzel = {'tag': '#', 'attrs': {}, 'kids': [], 'oben': None}
        self.stapel = [self.wurzel]
        self.feed(src)
        self.close()

    def _pos(self):
        z, s = self.getpos()
        return self.zl[z - 1] + s

    def _neu(self, tag, attrs, zu=False):
        s = self._pos()
        e = s + len(self.get_starttag_text())
        oben = self.stapel[-1]
        k = {'tag': tag, 'attrs': {a: (w if w is not None else '') for a, w in attrs}, 's': s, 'se': e, 'es': e if zu else None, 'ee': e if zu else None,
             'kids': [], 'oben': oben}
        oben['kids'].append(k)
        return k

    def handle_starttag(self, tag, attrs):
        k = self._neu(tag, attrs)
        if tag not in VOID:
            self.stapel.append(k)

    def handle_startendtag(self, tag, attrs):
        self._neu(tag, attrs, zu=True)

    def handle_endtag(self, tag):
        s = self._pos()
        for i in range(len(self.stapel) - 1, 0, -1):
            if self.stapel[i]['tag'] == tag:
                self.stapel[i]['es'] = s
                self.stapel[i]['ee'] = self.src.index('>', s) + 1
                del self.stapel[i:]
                break

    def _text(self, n):
        s = self._pos()
        self.stapel[-1]['kids'].append({'t': 1, 's': s, 'e': s + n})

    def handle_data(self, d):
        self._text(len(d))

    def handle_comment(self, d):   # ein Kommentar trennt Textläufe und ist nie selbst eine Stelle
        self.stapel[-1]['kids'].append({'kom': 1})

    def handle_entityref(self, name):
        s = self._pos() + 1 + len(name)
        self._text(1 + len(name) + (self.src[s:s + 1] == ';'))

    def handle_charref(self, name):
        s = self._pos() + 2 + len(name)
        self._text(2 + len(name) + (self.src[s:s + 1] == ';'))


def _elemente(k):
    return [c for c in k['kids'] if 'tag' in c]


def pfad(k):
    """Wo ein Element im Aufbau der Seite sitzt: vom nächsten Element mit id aus, je Stufe «tag:Nummer unter gleichen Geschwistern».
    Der Pfad ist in jeder Sprache einer Seite derselbe und hängt nicht am Text. Damit findet eine deutsche Stelle ihr Gegenstück."""
    teile = []
    while k and k['tag'] != '#':
        i = k['attrs'].get('id')
        if i:
            teile.append('#' + i)
            break
        gleiche = [c for c in _elemente(k['oben']) if c['tag'] == k['tag']]
        teile.append(f"{k['tag']}:{next(n for n, c in enumerate(gleiche) if c is k)}")
        k = k['oben']
    return '/'.join(reversed(teile))


# ------------------------------------------------------------------ Selektoren (für die Beschreibung eines Hauses)
_TEIL = re.compile(r'([a-zA-Z][\w-]*|\*)?((?:[#.][\w-]+|\[[\w-]+(?:[~^$*]?="[^"]*")?\]|:nicht\([^)]*\))*)')
_STUECK = re.compile(r'([#.][\w-]+|\[([\w-]+)(?:([~^$*]?)="([^"]*)")?\]|:nicht\(([^)]*)\))')


def _passt(k, teil):
    m = _TEIL.fullmatch(teil)
    if not m or not (m.group(1) or m.group(2)):
        raise ValueError(f'Selektor nicht lesbar: {teil}')
    if m.group(1) and m.group(1) != '*' and k['tag'] != m.group(1).lower():
        return False
    a = k['attrs']
    kl = (a.get('class') or '').split()
    for st in _STUECK.finditer(m.group(2)):
        s = st.group(1)
        if s[0] == '#':
            if a.get('id') != s[1:]:
                return False
        elif s[0] == '.':
            if s[1:] not in kl:
                return False
        elif s[0] == ':':
            if _passt(k, st.group(5).strip()):
                return False
        else:
            name, art, wert = st.group(2), st.group(3), st.group(4)
            if name not in a:
                return False
            if wert is not None:
                ist = a[name]
                if not {'': ist == wert, '~': wert in ist.split(), '^': ist.startswith(wert), '$': ist.endswith(wert), '*': wert in ist}[art or '']:
                    return False
    return True


def _kette(sel):
    teile, kombi = [], []
    for t in re.findall(r'>|[^\s>]+', sel.strip()):
        if t == '>':
            kombi[-1] = '>'
        else:
            teile.append(t)
            kombi.append(' ')
    return teile, kombi[:-1]


def _trifft(k, teile, kombi, grenze):
    if not _passt(k, teile[-1]):
        return False
    if len(teile) == 1:
        return True
    o = k['oben']
    if kombi[-1] == '>':
        return bool(o) and o is not grenze and o['tag'] != '#' and _trifft(o, teile[:-1], kombi[:-1], grenze)
    while o and o is not grenze and o['tag'] != '#':
        if _trifft(o, teile[:-1], kombi[:-1], grenze):
            return True
        o = o['oben']
    return False


def waehle(wurzel, selektor, ab=None):
    """Alle Elemente unter «ab» (sonst die ganze Seite), auf die der Selektor passt, in der Reihenfolge der Seite.
    Kann: tag, #id, .klasse, [attr], [attr="wert"] (auch ~= ^= $= *=), :nicht(…), Nachfahre (Leerzeichen), Kind (>), mehrere mit Komma."""
    ketten = [_kette(s) for s in selektor.split(',') if s.strip()]
    aus = []

    def gang(k):
        for c in _elemente(k):
            if any(_trifft(c, t, ko, ab) for t, ko in ketten):
                aus.append(c)
            gang(c)
    gang(ab or wurzel)
    return aus


# ------------------------------------------------------------------ Stellen einer Seite
def _nur_inline(k):
    for c in k['kids']:
        if c.get('t') or c.get('kom'):
            continue
        if c['tag'] not in INLINE or c['attrs'].get('aria-hidden') == 'true' or not _nur_inline(c):
            return False
    return True


def bild_schluessel(src, regeln=None):
    """Der Name eines Fotos ohne Ordner, Grössen-Endung und Versionsmarke. Die Endung der Grössen steht in der Beschreibung des Hauses."""
    weg = (regeln or {}).get('bild_groessen') or r'-(?:s|m|l|k|klein|gross|\d{3,4}w?)$'
    name = posixpath.basename(re.split(r'[?#]', src or '')[0])
    name = re.sub(r'\.(webp|jpe?g|png|avif|gif|svg)$', '', name, flags=re.I)
    return re.sub(weg, '', name)


def _erste_aus_satz(satz):
    """Erste Adresse aus einem srcset («a.webp 640w, b.webp 1000w» → a.webp)."""
    erste = (satz or '').split(',')[0].strip().split(' ')[0] if satz else ''
    return '' if erste.startswith('data:') else erste


def quelle_von(attrs, quellen=()):
    """Die echte Adresse eines Fotos: Seiten, die Bilder spät laden, führen sie in data-src und zeigen in src nur einen Platzhalter.
    29.10.2026: Fehlt eine echte Quelle (kein src oder nur ein data:-Platzhalter), gilt die erste Adresse aus data-srcset, srcset
    oder, im <picture>, aus <source data-srcset|srcset> (Culinarium lädt alle Bilder spät, nur mit data-srcset). Wo src steht, bleibt alles wie bisher."""
    q = attrs.get('data-src') or attrs.get('src') or ''
    if q and not q.startswith('data:'):
        return q
    for satz in [attrs.get('data-srcset'), attrs.get('srcset')] + [x for a in quellen for x in (a.get('data-srcset'), a.get('srcset'))]:
        erste = _erste_aus_satz(satz)
        if erste:
            return erste
    return q


def zerlege(src, regeln=None):
    """Alle änderbaren Stellen einer Seite.
      texte    Element mit nur Text und Auszeichnung ('el') oder ein loser Textlauf ('lauf')
      bloecke  section, article, li, figure, aside (zum Ausblenden) sowie header, footer, nav (nur zum Gliedern)
      fotos    jedes <img>, Schlüssel = Name der Bilddatei
      links    jedes <a href>
    Jede Stelle trägt einen Fingerabdruck aus Art und sichtbarem Inhalt (h), eine laufende Nummer für gleiche Fingerabdrücke
    auf der Seite (n), ihren Pfad im Aufbau und, falls ein anderes Werkzeug sie pflegt, dessen Schlüssel (zu)."""
    regeln = regeln or {}
    baum = Baum(src)
    zu = {}
    for g in regeln.get('gesperrt') or []:
        for k in waehle(baum.wurzel, g['wahl']):
            zu[id(k)] = g.get('werkzeug') or 'fest'
    aus_knoten = {id(k) for s in regeln.get('auslassen') or [] for k in waehle(baum.wurzel, s)}
    texte, bloecke, fotos, links = [], [], [], []
    zt, zb, zi, zl = {}, {}, {}, {}

    def versteckt(k):
        return k['tag'] in AUS or k['attrs'].get('aria-hidden') == 'true' or id(k) in aus_knoten or k['tag'] == 'img'

    def gang(k, blk, sperre):
        if k['tag'] != '#':
            if versteckt(k) or k.get('es') is None:
                return
            sperre = zu.get(id(k)) or sperre
            if k['tag'] in BLOECKE | FEST:
                t = klar(src[k['se']:k['es']])
                if re.search(r'\w', t) or k['tag'] == 'figure':
                    h = _hash('B' + k['tag'] + t[:600])
                    n = zb.get(h, 0)
                    zb[h] = n + 1
                    blk = {'h': h, 'n': n, 's': k['s'], 'se': k['se'], 'es': k['es'], 'ee': k['ee'], 'tag': k['tag'], 't': t[:160], 'eltern': blk,
                           'fest': k['tag'] in FEST, 'zu': sperre, 'pfad': pfad(k), 'k': k}
                    bloecke.append(blk)
            if k['tag'] == 'a' and k['attrs'].get('href'):
                gang_link(k, blk, sperre)
        laeufe, lauf = [], None
        for c in k['kids']:
            if c.get('t'):
                lauf = [lauf[0], c['e']] if lauf else [c['s'], c['e']]
            else:
                if lauf:
                    laeufe.append(lauf)
                lauf = None
        if lauf:
            laeufe.append(lauf)
        laeufe = [x for x in laeufe if re.search(r'\w', re.sub(r'&[#\w]+;', '', src[x[0]:x[1]]))]
        if laeufe and k['tag'] != '#':
            if _nur_inline(k):
                t = klar(src[k['se']:k['es']])
                h = _hash('E' + k['tag'] + t)
                n = zt.get(h, 0)
                zt[h] = n + 1
                texte.append({'art': 'el', 's': k['se'], 'e': k['es'], 'ein': k['se'] - 1 - (src[k['se'] - 2] == '/'), 'tag': k['tag'], 'h': h, 'n': n, 't': t,
                              'blk': blk, 'zu': sperre, 'pfad': pfad(k), 'k': k})
                for c in waehle(baum.wurzel, 'a[href]', k):   # Links in einem Satz bleiben eigene Stellen
                    gang_link(c, blk, sperre)
                return
            for i, (s, e) in enumerate(laeufe):
                roh = src[s:e]
                s2, e2 = s + len(roh) - len(roh.lstrip()), e - (len(roh) - len(roh.rstrip()))
                tk = klar(src[s2:e2])
                h = _hash('L' + k['tag'] + tk)
                n = zt.get(h, 0)
                zt[h] = n + 1
                texte.append({'art': 'lauf', 's': s2, 'e': e2, 'tag': k['tag'], 'h': h, 'n': n, 't': tk, 'blk': blk, 'zu': sperre, 'pfad': f'{pfad(k)}/~{i}', 'k': k})
        for c in k['kids']:
            if 'tag' in c:
                gang(c, blk, sperre)

    def gang_link(k, blk, sperre):
        href = k['attrs']['href']
        h = _hash('A' + href)
        n = zl.get(h, 0)
        zl[h] = n + 1
        links.append({'h': h, 'n': n, 's': k['s'], 'se': k['se'], 'href': href, 't': klar(src[k['se']:k['es']])[:120] if k.get('es') else '', 'blk': blk,
                      'zu': sperre, 'pfad': pfad(k), 'k': k})

    gang(baum.wurzel, None, None)

    def suche(k, sperre):
        for c in _elemente(k):
            if c['tag'] in AUS or id(c) in aus_knoten:   # Fotos in Fenstern (dialog), Vorlagen und Skripten gehören nicht zur Seite
                continue
            sp = zu.get(id(c)) or sperre
            if c['tag'] == 'img':
                quelle = quelle_von(c['attrs'], [x['attrs'] for x in _elemente(k) if x['tag'] == 'source'] if k.get('tag') == 'picture' else ())
                if not quelle or quelle.startswith('data:'):
                    continue
                key = bild_schluessel(quelle, regeln)
                n = zi.get(key, 0)
                zi[key] = n + 1
                um = [b for b in bloecke if b['s'] <= c['s'] < b['ee']]
                fotos.append({'b': key, 'n': n, 's': c['s'], 'se': c['se'], 'alt': c['attrs'].get('alt') or '', 'src': quelle, 'attrs': c['attrs'],
                              'blk': max(um, key=lambda b: b['s']) if um else None, 'zu': sp, 'pfad': pfad(c), 'k': c})
            else:
                suche(c, sp)
    suche(baum.wurzel, None)
    links.sort(key=lambda x: x['s'])
    return {'baum': baum, 'texte': texte, 'bloecke': bloecke, 'fotos': fotos, 'links': links}


def stellen_in(z, k):
    """Text-Stellen innerhalb eines Elements (das Element selbst eingeschlossen)."""
    return [t for t in z['texte'] if k['s'] <= t['s'] and t['e'] <= (k.get('ee') or k['se'])]


# ------------------------------------------------------------------ Attribute im Quelltext tauschen
def _attr(tag, name, wert):
    """Setzt ein Attribut in einem Start-Tag. wert None: Attribut entfernen. Fehlt es, wird es angehängt."""
    muster = re.compile(r'(\s)' + re.escape(name) + r'(?:=(?:"[^"]*"|\'[^\']*\'|[^\s>]+))?(?=[\s/>])')
    if wert is None:
        return muster.sub('', tag, 1)
    neu = f'{name}="{_h.escape(wert, quote=True)}"'
    if muster.search(tag):
        return muster.sub(lambda m: m.group(1) + neu, tag, 1)
    ende = len(tag) - (2 if tag.endswith('/>') else 1)
    return tag[:ende].rstrip() + ' ' + neu + tag[ende:]


def _roh_attr(tag, name):
    """Der Wert eines Attributs, wie er im Quelltext steht (ohne Entitäten aufzulösen)."""
    m = re.search(r'\s' + re.escape(name) + r'="([^"]*)"', tag)
    return m.group(1) if m else None


def _setze_roh(tag, name, roh):
    muster = re.compile(r'(\s)' + re.escape(name) + r'="[^"]*"')
    if roh is None:
        return muster.sub('', tag, 1)
    if muster.search(tag):
        return muster.sub(lambda m: f'{m.group(1)}{name}="{roh}"', tag, 1)
    ende = len(tag) - (2 if tag.endswith('/>') else 1)
    return tag[:ende].rstrip() + f' {name}="{roh}"' + tag[ende:]


_HG = re.compile(r'background:[^;"]*url\([^)]*\)[^;"]*;?')
_OP = re.compile(r'object-position:[^;"]*;?')


def bild_tag(tag, spender, alt=None, vorsatz=''):
    """Ein <img> auf ein anderes Foto umstellen. Quelle, Grössen und Masse kommen aus einem Tag, das auf der Website schon steht
    (spender = Quelltext jenes Tags). Nichts wird errechnet oder erraten. vorsatz: «../» für Seiten in einem Sprachordner.
    Lädt die Seite Fotos spät (data-src), bleibt jede Seite bei ihrer Art: getauscht wird die echte Adresse."""
    def mit_vorsatz(adresse):
        adresse = adresse.strip()
        return adresse if (not vorsatz or re.match(r'(https?:|/|data:)', adresse)) else vorsatz + adresse
    quelle = _roh_attr(spender, 'data-src') or _roh_attr(spender, 'src') or ''
    satz = _roh_attr(spender, 'data-srcset') or _roh_attr(spender, 'srcset')
    spaet = _roh_attr(tag, 'data-src') is not None
    tag = _setze_roh(tag, 'data-src' if spaet else 'src', mit_vorsatz(quelle))
    tag = _setze_roh(tag, 'data-srcset' if spaet else 'srcset', ', '.join(mit_vorsatz(t) for t in satz.split(',')) if satz else None)
    w, h = _roh_attr(spender, 'width'), _roh_attr(spender, 'height')
    if w and h:
        tag = _setze_roh(_setze_roh(tag, 'width', w), 'height', h)
        if spaet:   # der Platzhalter hält die Fläche frei: gleiche Masse wie das neue Foto
            platz = _roh_attr(tag, 'src') or ''
            tag = _setze_roh(tag, 'src', re.sub(r"width='\d+' height='\d+'", f"width='{w}' height='{h}'", platz))
    stil = _roh_attr(tag, 'style')
    if stil is not None:   # Ausschnitt und kleines Vorschaubild gehören zum alten Foto
        neu = _OP.sub('', _HG.sub('', stil)).strip().rstrip(';')
        vorab = _HG.search(_roh_attr(spender, 'style') or '')
        if vorab:
            neu = (neu + ';' if neu else '') + vorab.group(0).rstrip(';')
        tag = _setze_roh(tag, 'style', neu or None)
    if alt is not None:
        tag = _attr(tag, 'alt', alt)
    return tag


# ------------------------------------------------------------------ Hinweis für Gäste
def hinweis_html(h, sp=''):
    """Das Band oben auf jeder Seite. Farben und Schrift nimmt es von der Seite (currentColor, inherit), damit es in jedes Haus passt."""
    if not h or not h.get('an') or not str(h.get('text') or '').strip():
        return ''
    ue = ((h.get('sprachen') or {}).get(sp) or {}) if sp else {}
    text = str(ue.get('text') or h.get('text') or '').strip()
    von, bis = (str(h.get(k) or '') if re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(h.get(k) or '')) else '' for k in ('von', 'bis'))
    link = str(h.get('link') or '').strip()
    knopf = ''
    if link and link_gut(link):
        knopf = (f' <a href="{_h.escape(link, quote=True)}" style="color:inherit;text-decoration:underline;text-underline-offset:3px;white-space:nowrap">'
                 f'{_h.escape(str(ue.get("linktext") or h.get("linktext") or "Mehr erfahren"), quote=False)}</a>')
    zeit = (f' data-von="{von}"' if von else '') + (f' data-bis="{bis}"' if bis else '')
    selbst = ('<script>(function(b){var d=new Date(),h=d.getFullYear()+"-"+("0"+(d.getMonth()+1)).slice(-2)+"-"+("0"+d.getDate()).slice(-2),v=b.getAttribute("data-von"),'
              'e=b.getAttribute("data-bis");b.hidden=!!(v&&h<v||e&&h>e)})(document.currentScript.previousElementSibling)</script>') if zeit else ''
    return (f'<div class="ws-hinweis" role="status"{zeit} style="position:relative;z-index:5;padding:14px max(20px,4vw);text-align:center;'
            f'border-bottom:1px solid currentColor;font:inherit;line-height:1.5"><p style="margin:0 auto;max-width:72ch">{_h.escape(text, quote=False)}{knopf}</p></div>{selbst}')


def link_gut(link):
    return bool(re.match(r'(https?://[^\s"<>]+|mailto:[^\s"<>]+|tel:[+\d][\d ]*|#[\w-]*|[\w\-./]+\.(?:html|pdf)(?:#[\w-]*)?)$', link or '')) and not re.search(r'[\s"\'<>`]', link)


# ------------------------------------------------------------------ Die Schicht über eine Seite legen
def _regeln(c, name):
    def nach(feld, was):
        return {(x[was], int(x.get('n') or 0)): (i, x) for i, x in enumerate(c.get(feld) or []) if x.get('seite') == name}
    return {'text': nach('texte', 'h'), 'aus': nach('aus', 'h'), 'bild': nach('bilder', 'b'), 'link': nach('links', 'h')}


def _schneide(src, schnitte, weg):
    """Von hinten nach vorn einsetzen; Einfügungen (s == e) an derselben Stelle vor dem Ersetzen dahinter."""
    for s, e, neu in sorted(schnitte, key=lambda x: (x[0], x[1]), reverse=True):
        if any(a < s < b or a < e < b for a, b in weg if (a, b) != (s, e)):
            continue
        src = src[:s] + neu + src[e:]
    return src


def _band(src, c, sp='', marke=False):
    band = hinweis_html(c.get('hinweis') or {}, sp)
    if not band:
        return src
    if marke:
        band = band.replace('<div class="ws-hinweis"', '<div class="ws-hinweis" data-ws-neu', 1)
    if re.search(r'<main\b[^>]*>', src):
        return re.sub(r'<main\b[^>]*>', lambda m: m.group(0) + band, src, 1)
    return re.sub(r'<body\b[^>]*>', lambda m: m.group(0) + band, src, 1)


_TITEL = re.compile(r'(<title\b[^>]*>)(.*?)(</title>)', re.S)
_BESCHR = re.compile(r'(<meta\b[^>]*\bname="description"[^>]*\bcontent=")([^"]*)(")', re.S)


def _seo(src, c, name, benutzt=None):
    """Google-Texte einer Seite (Titel im Reiter und in der Trefferliste, Beschreibung darunter). Nur auf der deutschen Seite;
    Sprachseiten behalten ihre eigenen, bis das Haus Sprachen hat (21.10.2026, Master Werkzeug-Bau 4.2 I)."""
    for i, x in enumerate(c.get('seo') or []):
        if x.get('seite') != name:
            continue
        neu = src
        if str(x.get('titel') or '').strip():
            neu = _TITEL.sub(lambda m: m.group(1) + _h.escape(x['titel'], quote=False) + m.group(3), neu, 1)
        if str(x.get('beschreibung') or '').strip():
            neu = _BESCHR.sub(lambda m: m.group(1) + _h.escape(x['beschreibung'], quote=True) + m.group(3), neu, 1)
        if benutzt is not None and _TITEL.search(src) and (not str(x.get('beschreibung') or '').strip() or _BESCHR.search(src)):
            benutzt.add(('seo', i))
        src = neu
    return src


def _vorsatz(lang_wert, de_wert):
    """«../» oder ähnliches, das die Seite einer Sprache vor denselben Pfad setzt. None: die Pfade passen nicht zueinander."""
    if lang_wert == de_wert:
        return ''
    if de_wert and lang_wert.endswith(de_wert):
        return lang_wert[:-len(de_wert)]
    return None


def anwenden(name, src, c, marken=False, benutzt=None, regeln=None, spender=None, nur_neu=None):
    """Legt die Schicht c über eine deutsche Seite.
    marken    jede Stelle trägt ihren Fingerabdruck (data-ws-…), für die Vorschau im Werkzeug
    benutzt   Menge, in die jede angewandte Regel kommt (zum Prüfen, ob jede Änderung ihren Platz gefunden hat)
    spender   Fotos der Website: Schlüssel → Quelltext eines <img>, das dieses Foto zeigt
    nur_neu   Menge von Schlüsseln, die als «geändert» markiert werden (Vorher, nachher). None: jede Stelle mit Regel"""
    if ist_leer(c) and not marken:
        return src
    z = zerlege(src, regeln)
    r = _regeln(c, name)
    schnitte, weg = _schnitte(name, src, z, r, c, marken, benutzt, spender or {}, nur_neu, None, None)
    return _seo(_band(_schneide(src, schnitte, weg), c, '', bool(marken and nur_neu and 'hinweis' in nur_neu)), c, name, benutzt)


def anwenden_sprache(name, src, src_de, c, sp, marken=False, benutzt=None, regeln=None, spender=None, nur_neu=None, fehlt=None):
    """Dieselbe Schicht über die Seite einer anderen Sprache. Jede deutsche Stelle findet ihr Gegenstück über den Pfad im Aufbau.
    Steht für eine Änderung keine Übersetzung da, steht dort der neue deutsche Text (und der Schlüssel kommt in «fehlt»)."""
    if ist_leer(c) and not marken:
        return src
    z = zerlege(src, regeln)
    de = zerlege(src_de, regeln)
    r = _regeln(c, name)
    schnitte, weg = _schnitte(name, src, z, r, c, marken, benutzt, spender or {}, nur_neu, (sp, de), fehlt)
    return _band(_schneide(src, schnitte, weg), c, sp, bool(marken and nur_neu and 'hinweis' in nur_neu))


def schluessel(art, seite, a, n):
    return f'{art}|{seite}|{a}|{n}'


def _schnitte(name, src, z, r, c, marken, benutzt, spender, nur_neu, sprache, fehlt):
    sp, de = sprache or ('', None)

    def paare(art):
        """(Stelle dieser Seite, Stelle der deutschen Seite): im Deutschen dieselbe, sonst über den Pfad."""
        if not de:
            return [(st, st) for st in z[art]]
        nach_pfad = {}
        for st in z[art]:
            nach_pfad.setdefault(st['pfad'], st)
        aus = []
        for d in de[art]:
            st = nach_pfad.get(d['pfad'])
            if st and st.get('tag') == d.get('tag') and st.get('art') == d.get('art'):
                aus.append((st, d))
        return aus

    def neu_marke(key, regel):
        """Als «geändert» markieren: in der Vorschau jede Stelle mit Regel, bei «Vorher, nachher» genau die Stellen aus nur_neu
        (auch auf der Vorher-Seite, wo die Regel noch nicht gilt)."""
        return ' data-ws-neu' if (bool(regel) if nur_neu is None else key in nur_neu) else ''

    schnitte, weg = [], []
    for st, d in paare('bloecke'):
        regel = r['aus'].get((d['h'], d['n']))
        if regel and not d.get('fest') and not d.get('zu'):
            weg.append((st['s'], st['ee']))
            if benutzt is not None:
                benutzt.add(('aus', regel[0]))
        elif marken:
            schnitte.append((st['se'] - 1, st['se'] - 1, f' data-ws-blk="{d["h"]}" data-ws-bln="{d["n"]}"' + (f' data-ws-zu="{d["zu"]}"' if d.get('zu') else '') +
                             (' data-ws-neu' if nur_neu and schluessel('aus', name, d['h'], d['n']) in nur_neu else '')))

    def drin(s):
        return any(a <= s < e for a, e in weg)

    for st, d in paare('texte'):
        if drin(st['s']):
            continue
        regel = None if d.get('zu') else r['text'].get((d['h'], d['n']))
        key = schluessel('text', name, d['h'], d['n'])
        neu = None
        if regel:
            x = regel[1]
            neu = x.get('neu', '')
            if sp:
                ue = str((x.get('sprachen') or {}).get(sp) or '').strip()
                if ue:
                    neu = ue
                elif x.get('nur_sprachen') or klar(neu) == d['t']:
                    neu = None   # im Deutschen nichts geändert: diese Sprache bleibt, wie sie ist
                elif fehlt is not None:
                    fehlt.add(key)
            if benutzt is not None:
                benutzt.add(('text', regel[0]))
        attr = f' data-ws-e="{d["h"]}" data-ws-n="{d["n"]}"' + (f' data-ws-zu="{d["zu"]}"' if d.get('zu') else '') + neu_marke(key, regel)
        if st['art'] == 'el':
            if neu is not None:
                schnitte.append((st['s'], st['e'], neu))
            if marken:
                schnitte.append((st['ein'], st['ein'], attr))
        else:
            text = neu if neu is not None else src[st['s']:st['e']]
            if marken:
                schnitte.append((st['s'], st['e'], f'<span{attr} data-ws-lauf>{text}</span>'))
            elif neu is not None:
                schnitte.append((st['s'], st['e'], text))
    for st, d in paare('fotos'):
        if drin(st['s']):
            continue
        regel = None if d.get('zu') else r['bild'].get((d['b'], d['n']))
        tag = src[st['s']:st['se']]
        key = schluessel('bild', name, d['b'], d['n'])
        if regel:
            x = regel[1]
            alt = x.get('alt') if str(x.get('alt') or '').strip() else None
            if sp and alt is not None:
                alt = str((x.get('alt_sprachen') or {}).get(sp) or '').strip() or alt
            ziel = x.get('neu') or d['b']
            vor = _vorsatz(quelle_von(st['attrs']), quelle_von(d['attrs'])) if de else ''
            if ziel != d['b'] and ziel in spender and vor is not None:
                tag = bild_tag(tag, spender[ziel], alt, vor)
            elif alt is not None:
                tag = _attr(tag, 'alt', alt)
            if benutzt is not None:
                benutzt.add(('bild', regel[0]))
        if marken:
            ende = len(tag) - (2 if tag.endswith('/>') else 1)
            tag = tag[:ende].rstrip() + f' data-ws-b="{d["b"]}" data-ws-bn="{d["n"]}"' + (f' data-ws-zu="{d["zu"]}"' if d.get('zu') else '') + neu_marke(key, regel) + tag[ende:]
        if regel or marken:
            schnitte.append((st['s'], st['se'], tag))
    for st, d in paare('links'):
        if drin(st['s']):
            continue
        regel = None if d.get('zu') else r['link'].get((d['h'], d['n']))
        marke = neu_marke(schluessel('link', name, d['h'], d['n']), regel) if marken else ''
        tag = src[st['s']:st['se']]
        if regel:
            ziel = str(regel[1].get('neu') or '')
            vor = _vorsatz(st['href'], d['href']) if de else ''
            if benutzt is not None:
                benutzt.add(('link', regel[0]))
            if link_gut(ziel) and vor is not None:
                if vor and re.match(r'(https?:|mailto:|tel:|#|/)', ziel):
                    vor = ''
                tag = _attr(tag, 'href', vor + ziel)
        if marke:
            tag = tag[:-1] + marke + '>'
        if tag != src[st['s']:st['se']]:
            schnitte.append((st['s'], st['se'], tag))
    for s, e in weg:
        schnitte.append((s, e, ''))
    return schnitte, weg


def paarung(src, src_de, regeln=None):
    """Wie viele deutsche Stellen auf der Seite einer anderen Sprache ein Gegenstück haben (für die Prüfung)."""
    z, de = zerlege(src, regeln), zerlege(src_de, regeln)
    da = {st['pfad']: st['tag'] for st in z['texte']}
    treffer = sum(1 for d in de['texte'] if da.get(d['pfad']) == d['tag'])
    return treffer, len(de['texte'])


# ------------------------------------------------------------------ Eingaben säubern
class _Sauber(HTMLParser):
    ERLAUBT = {'b', 'strong', 'i', 'em', 'span', 'small', 'a', 'br', 'sup', 'sub'}

    def __init__(self, klassen):
        super().__init__(convert_charrefs=True)
        self.aus, self.offen, self.klassen = [], [], klassen

    def handle_starttag(self, tag, attrs):
        if tag in ('div', 'p') and self.aus and self.aus[-1] != '<br>':
            self.aus.append('<br>')
        if tag not in self.ERLAUBT:
            return
        a = dict(attrs)
        o = ''
        kl = ' '.join(k for k in (a.get('class') or '').split() if k in self.klassen)
        if kl:
            o += f' class="{kl}"'
        if tag == 'a':
            if not link_gut(a.get('href') or ''):
                return
            o += f' href="{_h.escape(a["href"], quote=True)}"' + (' target="_blank" rel="noopener"' if a['href'].startswith('http') else '')
        self.aus.append(f'<{tag}{o}>')
        if tag != 'br':
            self.offen.append(tag)

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.aus.append('<br>')

    def handle_endtag(self, tag):
        if tag in self.offen:
            while self.offen:
                t = self.offen.pop()
                self.aus.append(f'</{t}>')
                if t == tag:
                    break

    def handle_data(self, d):
        self.aus.append(d.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\xa0', '&nbsp;'))


def sauber(html, klassen=()):
    """Eingabe aus dem Werkzeug: nur einfache Auszeichnung bleibt (kursiv, fett, Umbruch, Link), dazu Klassen, die an dieser Stelle
    schon vorher standen. Nichts, was den Aufbau der Seite ändern kann."""
    p = _Sauber(set(klassen))
    p.feed(str(html))
    p.close()
    while p.offen:
        p.aus.append(f'</{p.offen.pop()}>')
    s = ''.join(p.aus)
    s = re.sub(r'(<br>\s*)+$', '', s)
    return re.sub(r'[ \t\r\n]+', ' ', s).strip()


def klassen_in(html):
    return {k for m in re.finditer(r'class="([^"]*)"', html or '') for k in m.group(1).split()}
