#!/usr/bin/env python3
"""Fassungsnummern aus dem Inhalt (Master Werkzeug-Bau M20): setzt in index.html, pruefung.html und anleitung.html jedes ?v=… einer eigenen Datei
und des gemeinsamen Kleids (/assets/oberflaeche/ → _werkzeuge/oberflaeche/) auf die ersten 10 Zeichen der Prüfsumme der Datei. Nach jeder Änderung laufen lassen."""
import hashlib, os, re
C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
OB = os.path.join(os.path.dirname(C), 'oberflaeche')
def datei(href):
    href = href.split('?')[0]
    if href.startswith('/assets/oberflaeche/'):
        return os.path.join(OB, href[len('/assets/oberflaeche/'):])
    if href.startswith(('/', 'http', '../')):
        return None
    return os.path.join(C, href)
for seite in ('index.html', 'pruefung.html', 'anleitung.html'):
    p = os.path.join(C, seite); s = open(p, encoding='utf-8').read(); n = 0
    def neu(m):
        global n
        f = datei(m.group(2))
        if not f or not os.path.isfile(f):
            return m.group(0)
        n += 1
        return f'{m.group(1)}{m.group(2)}?v={hashlib.sha1(open(f, "rb").read()).hexdigest()[:10]}{m.group(4)}'
    s2 = re.sub(r'((?:src|href)=")([^"?]+)(\?v=[^"]*)?(")', neu, s)
    if s2 != s:
        open(p, 'w', encoding='utf-8').write(s2)
    print(seite, n, 'Dateien')
