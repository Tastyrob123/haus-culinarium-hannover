#!/usr/bin/env python3
"""Werkbank Culinarium: Rücksprung-Höhe (Robert 1.11.2026) in alle Seiten der Werkbank setzen. Das Skript steht in ruecksprung.js und kommt als
<script id="ruecksprung"> vor </body>, ein vorhandener Block wird ersetzt (wiederholbar). Läuft am Ende von haus.nach_bau.
   python3 _werkbank/ruecksprung.py [<website/_werkbank>]"""
import glob, os, re, sys

W = os.path.dirname(os.path.abspath(__file__))
JS = open(os.path.join(W, 'ruecksprung.js'), encoding='utf-8').read()
JS = re.sub(r'^/\*.*?\*/\s*', '', JS, count=1, flags=re.S).strip()   # der Kopfkommentar bleibt in der Quelle
BLOCK = '<script id="ruecksprung">' + JS + '</script>'


def anwenden(root):
    n = 0
    for f in sorted(glob.glob(os.path.join(root, '**', '*.html'), recursive=True)):
        rel = os.path.relpath(f, root)
        if rel.split(os.sep)[0] in ('_werkbank', 'assets', 'pruefung', 'node_modules', '_sicherung') or '.vor-' in rel or os.path.basename(f).startswith('_'):   # Druckbögen wie feed/_bogen.html bleiben ohne
            continue
        s = open(f, encoding='utf-8').read()
        if '</body>' not in s:
            continue
        neu = re.sub(r'<script id="ruecksprung">.*?</script>\n?', '', s, flags=re.S)
        i = neu.rindex('</body>')
        neu = neu[:i] + BLOCK + '\n' + neu[i:]
        if neu != s:
            open(f, 'w', encoding='utf-8').write(neu); n += 1
    return n


if __name__ == '__main__':
    print('ruecksprung:', anwenden(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(W)), 'Seiten')
