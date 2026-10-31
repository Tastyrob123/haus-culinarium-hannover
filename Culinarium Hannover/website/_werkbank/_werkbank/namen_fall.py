"""Werkbank Culinarium: Werkzeug-Namen mit Artikel im Satz (28.10.2026). Robert hat Satz A gewählt («Der Tresen», «Das Schaufenster», «Die Pairing-Karte» …);
die Namen kommen nur aus _werkzeuge/oberflaeche/kleid/culinarium.js. Im Satz braucht der Artikel seinen Fall: «in der Pairing-Karte», «im Schaufenster»,
«Den Tresen öffnen», «und der Tresen führt …». Namen ohne Artikel bleiben, wie sie sind."""


def _teile(n):
    for a in ('Der ', 'Das ', 'Die '):
        if n.startswith(a):
            return a.strip(), n[len(a):]
    return None, n


def in_(n):
    """Ort: im Tresen, im Schaufenster, in der Pairing-Karte."""
    a, r = _teile(n)
    return {'Der': 'im ', 'Das': 'im ', 'Die': 'in der '}.get(a, 'in ') + r


def akk(n):
    """Wen oder was: Den Tresen, Das Schaufenster, Die Pairing-Karte (am Satzanfang, etwa auf Knöpfen)."""
    a, r = _teile(n)
    return ('Den ' + r) if a == 'Der' else n


def klein(n):
    """Mitten im Satz: der Tresen, das Schaufenster."""
    a, r = _teile(n)
    return (a.lower() + ' ' + r) if a else n
