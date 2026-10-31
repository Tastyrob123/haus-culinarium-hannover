#!/usr/bin/env python3
"""Werkbank Culinarium: Schrift optisch mittig in Knöpfen (Regel «text-mitte» des Messlaufs, Robert 29.10.2026: «Die Schriften in deinen Buttons sitzen
IMMER falsch beim ersten Mal»). Gemessen mit messen.js: Chromium setzt DM Mono in den Knöpfen 0,6 bis 1,0 px zu hoch und hängt die Sperrung hinter den
letzten Buchstaben, WebKit nicht; die Pfeile der Rundknöpfe sitzen in beiden je Richtung 0,5 px aussen. Darum bekommt der Knopftext ein eigenes <span class="tm">,
das nur in Chromium (ohne font:-apple-system-body) ein Stück rückt; Höhe und Polsterung der Knöpfe bleiben. Läuft am Ende von haus.nach_bau über alle Seiten
der Werkbank, wiederholbar.   python3 _werkbank/text_mitte.py [<website/_werkbank>]"""
import glob, os, re, sys

CSS = """.tm{position:relative}
@supports not (font:-apple-system-body){
  .kn>.tm{top:.7px}.kn.kn--klein>.tm{top:0}
  .wahl button>.tm,.vh-wahl button>.tm,.uwahl button>.tm,.uschalter button>.tm{top:1px;left:.065em}
  .mb-kn>span{position:relative;top:.9px}
  .sbf-z>.tm{top:.6px}
}
.rund[aria-label^="Zur"] svg,.rund[aria-label^="Vorig"] svg,.pf[aria-label^="Vorig"] svg{transform:translateX(.5px)}
.rund[aria-label^="Weiter"] svg,.rund[aria-label^="Nächst"] svg,.pf[aria-label^="Nächst"] svg{transform:translateX(-.5px)}
@supports (font:-apple-system-body){.pf[aria-label^="Vorig"] svg{transform:translate(.6px,.5px)}.pf[aria-label^="Nächst"] svg{transform:translate(-.6px,.5px)}}
@supports not (font:-apple-system-body){.pf[aria-label^="Vorig"] svg{transform:translateX(.6px)}.pf[aria-label^="Nächst"] svg{transform:translateX(-.6px)}}"""
JS = ("(function(){function t(){document.querySelectorAll('.kn,.sbf-z,.wahl button,.vh-wahl button,.uwahl button,.uschalter button').forEach(function(k){"
      "var n=k.firstChild;if(n&&n.nodeType===3&&n.textContent.trim()){var s=document.createElement('span');s.className='tm';s.textContent=n.textContent;k.replaceChild(s,n)}})}"
      "t();addEventListener('load',t)})();")
BLOCK = '<style id="text-mitte">' + CSS + '</style><script id="text-mitte-js">' + JS + '</script>'


def anwenden(root):
    n = 0
    for f in glob.glob(os.path.join(root, '**', '*.html'), recursive=True):
        rel = os.path.relpath(f, root)
        if rel.startswith(('_werkbank', '_sicherung', 'node_modules')) or '.vor-' in rel or '</body>' not in open(f, encoding='utf-8', errors='ignore').read():
            continue
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'<style id="text-mitte">.*?</style><script id="text-mitte-js">.*?</script>', '', s, flags=re.S)
        i = s.rfind('</body>'); s = s[:i] + BLOCK + s[i:]
        open(f, 'w', encoding='utf-8').write(s); n += 1
    return n


if __name__ == '__main__':
    print('text-mitte:', anwenden(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Seiten')
