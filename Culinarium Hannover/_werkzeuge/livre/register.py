#!/usr/bin/env python3
"""Le Livre · Culinarium Hannover: liest das Bildregister der Website (BILD in website/bau.py), ohne bau.py auszuführen (Falle 9: der Import baut die Website).
Die festen Einträge kommen per ast aus dem Text, die Bilder je Abend genau so, wie bau.py sie dazurechnet (abende_info.INFO, ABENDE), die geschärften
Quellen aus GESCHAERFT (culinarium-bilder) genau so, wie bau.py sie darüberlegt.

   python3 _werkzeuge/livre/register.py sichern   → _register-vor-schaerfen.json (einmal, vor dem Schärfen; danach nie überschreiben)"""
import ast, json, os, sys, time

HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(PROJEKT, 'website')


def _baum():
    return ast.parse(open(os.path.join(WEB, 'bau.py'), encoding='utf-8').read())


def _konstanten(baum):
    werte = {}
    for n in baum.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            try:
                v = ast.literal_eval(_einsetzen(n.value, werte))
            except (ValueError, KeyError, SyntaxError, TypeError):
                continue
            if isinstance(v, str):
                werte[n.targets[0].id] = v
    return werte


def _einsetzen(knoten, werte):
    class Ein(ast.NodeTransformer):
        def visit_Name(self, x):
            return ast.copy_location(ast.Constant(werte[x.id]), x)

        def visit_BinOp(self, x):
            self.generic_visit(x)
            if isinstance(x.op, ast.Add) and isinstance(x.left, ast.Constant) and isinstance(x.right, ast.Constant):
                return ast.copy_location(ast.Constant(x.left.value + x.right.value), x)
            return x
    import copy
    v = Ein().visit(copy.deepcopy(knoten))
    ast.fix_missing_locations(v)
    return v


def lesen():
    """{schlüssel: (quelle relativ zum Projekt, ausschnitt, alt)} wie BILD nach dem Laden von bau.py."""
    baum = _baum()
    werte = _konstanten(baum)
    bild = abende = None
    geschaerft = {}
    for n in baum.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            if n.targets[0].id == 'BILD':
                bild = ast.literal_eval(_einsetzen(n.value, werte))
            elif n.targets[0].id == 'ABENDE':
                abende = ast.literal_eval(n.value)
            elif n.targets[0].id == 'GESCHAERFT':                 # culinarium-bilder, 28.10.2026: geschärfte Quellen nach BILD
                geschaerft = ast.literal_eval(_einsetzen(n.value, werte))
    if bild is None or abende is None:
        raise SystemExit('BILD oder ABENDE fehlt in website/bau.py, erst klären')
    sys.path.insert(0, WEB)
    import importlib
    ai = importlib.import_module('abende_info')      # nur Daten (Listen und Wörter), baut nichts
    for key, inf in ai.INFO.items():
        for i, q in enumerate(inf['bilder']):
            bild['ab_%s_%d' % (key.replace('-', '_'), i)] = (q, '50% 50%', 'Culinarium, Bild zum Abend')
        for i, (_dat, ger, q) in enumerate(inf['rudi']):
            if q:
                bild['abr_%s_%d' % (key.replace('-', '_'), i)] = (q, '50% 50%', ger)
    ig = werte['IG']
    for j, d, _z, _p, pid, _m in abende:
        if pid:
            f = [f for f in os.listdir(os.path.join(PROJEKT, ig)) if pid in f and f.endswith('-1.jpg')][0]
            bild['p_' + pid] = (ig + f, '50% 50%', 'Plakat Culinarium, %s %s' % (d, j))
    for k, (alt, neu) in geschaerft.items():                  # wie website/bau.py: greift nur, solange der Schlüssel noch das alte Original zeigt
        if k in bild and bild[k][0] == alt:
            bild[k] = (neu,) + tuple(bild[k][1:])
    return bild, abende


def sichern():
    z = os.path.join(HIER, '_register-vor-schaerfen.json')
    if os.path.exists(z):
        raise SystemExit('Sicherung steht schon (%s), nie überschreiben' % z)
    bild, _ = lesen()
    if any('/ki/geschaerft/' in q for q, *_ in bild.values()):
        raise SystemExit('Register enthält schon geschärfte Quellen: Stand vor dem Schärfen aus einer Sicherung von website/bau.py nehmen')
    json.dump({'stand': time.strftime('%Y-%m-%d %H:%M'), 'woher': 'website/bau.py BILD (+ Bilder je Abend), vor dem Schärfen',
               'quelle': {k: v[0] for k, v in bild.items()}}, open(z, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('gesichert:', len(bild), 'Einträge →', z)


if __name__ == '__main__':
    if sys.argv[1:] == ['sichern']:
        sichern()
    else:
        b, a = lesen()
        print(len(b), 'Einträge,', len(a), 'Abende')
