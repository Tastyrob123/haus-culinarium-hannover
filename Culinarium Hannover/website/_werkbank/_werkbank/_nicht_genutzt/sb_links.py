#!/usr/bin/env python3
"""Station 14, Website verbinden: jeden Link der Website, der Werkbank und der Beigaben lokal abrufen (19.10.2026).
   python3 _werkbank/sb_links.py   → _kette/14-verbinden/links.json und links.html

Je Link: Seite, Link, Ziel (aufgelöst), Antwort (HTTP-Status lokal; fremde Adressen nur mit HEAD/GET, ohne etwas abzuschicken), alt_design (führt auf die
heutige Seite des Hauses), mailto (öffnet ein Mailprogramm). Dazu: steht auf einer Seite der Website «Zur Werkbank» oder ein Weg in die Werkbank, ist das ein Fund.
Fremde Adressen werden einmal abgerufen (gratis, kein Formular, nichts gesendet)."""
import glob, html, json, os, re, urllib.parse, urllib.request

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PAKET = os.path.join(W, '_qa', 'links')   # im eigenen Revier (Werkbank-Chat Schäfli)
BASIS = 'http://127.0.0.1:9068/'
ALT = ('schaefli-wigoltingen.ch',)
WEBSITE = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, '*.html')))
BEIGABEN = ['werkbank/index.html', 'werkbank/geprueft/index.html', 'werkbank/impressum.html', 'unterlagen/index.html', 'drucksachen/index.html', 'zigarrenbinden/index.html',
            'feed/index.html', 'material/index.html', 'mails/index.html'] + [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, 'mails', '0*', 'index.html'))]
_cache = {}


def hole(url):
    if url in _cache:
        return _cache[url]
    s = None
    for meth in ('HEAD', 'GET'):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, method=meth, headers={'User-Agent': 'Mozilla/5.0 (Linkpruefung Tasty Studios)'}), timeout=15)
            s = r.status; break
        except urllib.error.HTTPError as e:
            s = e.code
            if meth == 'GET' or e.code not in (403, 405, 400, 501):
                break
        except Exception as e:
            s = f'Fehler: {type(e).__name__}'
    _cache[url] = s
    return s


def main():
    aus, funde = [], []
    for seite in WEBSITE + [b for b in BEIGABEN if os.path.exists(os.path.join(ROOT, b))]:
        t = open(os.path.join(ROOT, seite), encoding='utf-8').read()
        art = 'website' if seite in WEBSITE else 'beigabe'
        if art == 'website' and re.search(r'href="[^"]*werkbank/|>\s*Zur Werkbank\s*<', t):
            funde.append(f'{seite}: Weg zur Werkbank auf der Website')
        for href in sorted(set(html.unescape(h) for h in re.findall(r'<a\b[^>]*\shref="([^"]+)"', t))):
            if href.startswith(('#', 'javascript:', 'data:')) or href.startswith('tel:'):
                continue
            if href.startswith('mailto:'):
                aus.append(dict(seite=seite, link=href, ziel=href, antwort=None, alt_design=False, mailto=True)); continue
            ziel = urllib.parse.quote(urllib.parse.urljoin(BASIS + seite, href).split('#')[0], safe=':/?=&%')
            antwort = hole(ziel)
            aus.append(dict(seite=seite, link=href, ziel=ziel, antwort=antwort, alt_design=any(a in urllib.parse.urlparse(ziel).netloc for a in ALT), mailto=False))
    os.makedirs(PAKET, exist_ok=True)
    json.dump(aus, open(os.path.join(PAKET, 'links.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = [x for x in aus if not x['mailto'] and x['antwort'] != 200]
    alt = [x for x in aus if x['alt_design']]
    mail = [x for x in aus if x['mailto']]
    zeilen = ''.join(f'<tr class="{"rot" if (x["antwort"] != 200 and not x["mailto"]) or x["alt_design"] or x["mailto"] else ""}"><td>{html.escape(x["seite"])}</td><td><a href="{html.escape(x["ziel"])}" target="_blank" rel="noopener">{html.escape(x["link"][:90])}</a></td><td>{html.escape(str(x["antwort"]))}</td><td>{"ja" if x["alt_design"] else ""}</td><td>{"mailto" if x["mailto"] else ""}</td></tr>' for x in sorted(aus, key=lambda x: (x['antwort'] == 200, x['seite'])))
    kopf = (f'<p>{len(aus)} Links auf {len({x["seite"] for x in aus})} Seiten · nicht erreichbar: {len(tot)} · ins alte Design: {len(alt)} · Mailprogramm: {len(mail)} · '
            f'Weg zur Werkbank auf der Website: {len(funde)}</p>' + ''.join(f'<p class="f">{html.escape(f)}</p>' for f in funde))
    open(os.path.join(PAKET, 'links.html'), 'w', encoding='utf-8').write(f'''<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>Links · Taverne zum Schäfli</title><style>body{{margin:0;padding:40px 20px;background:#e7ecf3;color:#041023;font:15px/1.5 system-ui,sans-serif}}h1{{font:400 28px/1.2 system-ui;letter-spacing:.12em;text-transform:uppercase;color:#0b1d3d}}
table{{width:100%;max-width:1400px;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden}}td{{padding:7px 12px;border-top:1px solid #d0dae7;vertical-align:top;word-break:break-all}}tr.rot td{{background:#fff0e8}}a{{color:#113d88}}.f{{color:#b4421f}}</style></head>
<body><h1>Links, Station 14</h1>{kopf}<table><tr><td><b>Seite</b></td><td><b>Link</b></td><td><b>Antwort</b></td><td><b>altes Design</b></td><td><b>Mail</b></td></tr>{zeilen}</table></body></html>''')
    print(len(aus), 'Links · nicht erreichbar', len(tot), '· alt', len(alt), '· mailto', len(mail), '· Werkbank-Wege auf der Website', len(funde))
    for x in tot[:30]:
        print('  ', x['seite'], x['link'], x['antwort'])
    for x in alt[:10] + mail[:10]:
        print('  ', x['seite'], x['link'])
    for f in funde:
        print('  ', f)


if __name__ == '__main__':
    main()
