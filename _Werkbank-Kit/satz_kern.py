#!/usr/bin/env python3
"""Unterlagen des Hauses im Stil der neuen Seite setzen: Bausteine.
   Je Haus: <Projekt>/_werkbank/satz_daten.py  →  DOKS = [dok(...)], jede Seite aus den Bausteinen unten.
   python3 satz.py "<Projekt>"          schreibt _werkbank/satz/u-<ziel>.html und unterlagen.json
   node satz_druck.js "<Projekt>"       druckt nach unterlagen/pdf/<ziel>.pdf
   python3 satz_pruefe.py "<Projekt>"   vergleicht den Wortlaut jeder Unterlage mit dem Original des Hauses

Regeln (Master «Website-Bau», Abschnitt 8): Wortlaut und Seitenzahl bleiben. Eindeutige Tippfehler und Widersprüche des Originals
werden seit 09.10.2026 berichtigt, jede Stelle in einer Liste in satz_daten.py (Muster: Berghotel Gasterntal, BERICHTIGT) und an Robert gemeldet. Titel gut doppelt so gross wie der Lesetext, in der Titelschrift und normaler Schreibung,
kurze Linie darunter; Zwischentitel klein in gesperrten Versalien; Preise in der Titelschrift. Keine weichen Schatten."""
import html
import kern as K
from kern import H

e = html.escape
F = H.FARBEN


def dok(ziel, quelle, name, gruppe, seiten, quer=False, format=None, dazu='', fehlt=''):
    """quelle: Pfad des Originals relativ zum Projekt. seiten: Liste fertiger Seiten (blatt(...)). dazu/fehlt: Wörter, die bewusst
    hinzukommen (z. B. Fusszeile mit Adresse) oder wegfallen (z. B. Text im gezeichneten Zeichen)."""
    return dict(ziel=ziel, quelle=quelle, name=name, gruppe=gruppe, seiten=seiten, quer=quer, format=format, dazu=dazu, fehlt=fehlt)


def blatt(*teile, kl='', kopf=None, fuss=True, quer=False, format=None):
    """Eine Seite. kopf: None (kein Band), str (Band mit Titel) oder fertiges HTML. Inhalt füllt den Rest."""
    b, h = format or ((297, 210) if quer else (210, 297))
    k = ''
    if kopf is not None:
        k = kopf if kopf.startswith('<') else band(kopf)
    f = f'<footer class="ufuss2">{H.SATZ_FUSS}</footer>' if fuss is True else (f'<footer class="ufuss2">{fuss}</footer>' if fuss else '')
    return f'<section class="blatt {kl}" data-b="{b}" data-h="{h}" style="width:{b}mm;height:{h}mm">{k}<div class="inhalt">{"".join(teile)}</div>{f}</section>'


def band(titel, unter='', klein=False):
    """Kopfband in der dunklen Farbe des Hauses mit Muster, Zeichen und Titel."""
    return (f'<header class="uband{" uband--klein" if klein else ""}"><span class="uband__z">{K.zeichen()}</span><div><h1>{titel}</h1>' + (f'<p>{unter}</p>' if unter else '') + '</div></header>')


def leiste(text=''):
    """Schmale Kopfzeile nur mit dem Zeichen des Hauses (für Seiten, deren Original keinen Titel hat)."""
    return f'<header class="uleiste"><span>{K.zeichen()}</span>{f"<b>{text}</b>" if text else ""}</header>'


def titelblatt(titel, unter='', zeilen=(), bild=None):
    """Grosse Titelfläche (für Deckblätter): Zeichen, Titel, Linie, Zeilen darunter."""
    z = ''.join(f'<p>{x}</p>' for x in zeilen)
    return f'<div class="udeck"><span class="udeck__z">{K.zeichen()}</span><h1>{titel}</h1><i></i>' + (f'<p class="udeck__u">{unter}</p>' if unter else '') + z + '</div>'


def spalten(*sp, kl=''):
    return f'<div class="spalten spalten--{len(sp)} {kl}">' + ''.join(f'<div class="sp">{s}</div>' for s in sp) + '</div>'


def rubrik(titel, zusatz='', kopf=()):
    """Überschrift einer Gruppe, optional mit Zusatz und Spaltenköpfen (für Preisspalten)."""
    k = '<span class="rk">' + ''.join(f'<b>{e(x)}</b>' for x in kopf) + '</span>' if kopf else ''
    z = f'<small>{zusatz}</small>' if zusatz else ''
    return f'<h2 class="rubrik"><span>{titel}{z}</span>{k}</h2>'


def zwischen(text):
    return f'<h3 class="zw">{text}</h3>'


def posten(name, text='', fremd='', preise=(), zusatz='', kl=''):
    """Ein Gericht oder Getränk. preise: Liste aus Preis oder (Angabe, Preis); mehrere werden untereinander gesetzt."""
    pr = ''
    for p in preise:
        if isinstance(p, (tuple, list)):
            pr += f'<span class="pz"><em>{p[0]}</em><b>{p[1]}</b></span>'
        else:
            pr += f'<span class="pz"><b>{p}</b></span>'
    z = f' <small>{zusatz}</small>' if zusatz else ''
    return (f'<div class="po {kl}"><div class="po__t"><h4>{name}{z}</h4>' + (f'<p>{text}</p>' if text else '') + (f'<p class="fr">{fremd}</p>' if fremd else '')
            + f'</div><div class="po__p">{pr}</div></div>')


def reihe(name, werte, zusatz='', kl=''):
    """Eine Zeile mit festen Preisspalten (Getränke: 3 dl, 5 dl, 1,5 l). Leere Werte bleiben leer."""
    z = f' <small>{zusatz}</small>' if zusatz else ''
    return f'<div class="re {kl}"><span class="re__n">{name}{z}</span><span class="rk">' + ''.join(f'<b>{x}</b>' for x in werte) + '</span></div>'


def absatz(text, kl=''):
    return f'<p class="ab {kl}">{text}</p>'


def titel(text, kl=''):
    return f'<h2 class="ut {kl}">{text}</h2>'


def kasten(titel_, *teile, kl=''):
    return f'<div class="ukasten {kl}">' + (f'<h3>{titel_}</h3>' if titel_ else '') + ''.join(teile) + '</div>'


def liste(punkte, kl=''):
    return f'<ul class="ul {kl}">' + ''.join(f'<li>{p}</li>' for p in punkte) + '</ul>'


def linie():
    return '<i class="ulin"></i>'


def luft(mm=4):
    return f'<i style="display:block;height:{mm}mm"></i>'


def bild(key, hoehe_mm, lage='50% 50%', kl=''):
    import os
    pfad = os.path.relpath(K.hausbild(key), os.path.join(K.W, 'satz'))
    return f'<img class="ubild {kl}" src="{e(pfad)}" style="height:{hoehe_mm}mm;object-position:{lage}" alt="">'


def zeichen_gross(kl=''):
    return f'<span class="uz {kl}">{K.zeichen()}</span>'


def wortmarke(kl=''):
    return f'<span class="uw {kl}">{K.wortmarke()}</span>'
