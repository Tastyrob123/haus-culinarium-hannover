#!/usr/bin/env python3
"""Werkbank Culinarium: «Meine drei Orte», das Kursblatt mit Hamburg, Koh Phangan und Siargao (Robert 29.10.2026: «meine hamburg siargao koh phangan
animation einfügen wie wir sie mal hatte»). Block und Animation kommen unverändert aus dem Werkbank-Kit (bau.py › orte, Brief-Art «lang»; werkbank.css ›
.karte3, .kurs, @keyframes welle, beides lädt die Werkbank ohnehin); hier steht nur das Kleid des Culinarium: Nacht statt Marineblau, Warmweiss und Orange.
Gebraucht im Brief (brief_blatt.py, neben der Unterschrift) und im Schluss (wb_kapitel.py › schluss, unter der Unterschrift)."""
import os
import re

_KIT = os.path.join(os.path.expanduser('~'), 'Desktop', 'Website-Projekte', '_Werkbank-Kit', 'bau.py')


def block(art):
    """Der Block «orte» aus dem Kit, Wort für Wort; art = 'brief' oder 'schluss' für die Lage im Kleid."""
    h = re.search(r"orte = '''(.*?)'''", open(_KIT, encoding='utf-8').read(), re.S).group(1).strip()
    return h.replace('class="karte3"', f'class="karte3 ok ok--{art}"', 1)


CSS = """
/* ---------- «Meine drei Orte» im Kleid des Culinarium (orte_kurs.py, 29.10.2026): Block und Animation aus dem Kit, Farben des Hauses ---------- */
.karte3.ok{background:var(--navy);color:#fbf5ea;text-align:left;box-shadow:inset 0 1px 0 rgba(255,255,255,.08),inset 0 0 0 1px rgba(239,118,73,.26),0 30px 40px -26px rgba(8,7,10,.8)}
.karte3.ok h3{color:#fbf5ea}
.karte3.ok p{color:rgba(251,245,234,.76)}
.ok .kurs text{fill:rgba(251,245,234,.72)}
.ok .kurs .ort{fill:#fbf5ea}
.ok .kurs .weg,.ok .kurs .welle{stroke:var(--gold)}
.ok .kurs .pkt{fill:#fbf5ea}.ok .kurs .da0{fill:var(--gold)}
.ok--schluss{width:min(100%,520px);margin:clamp(22px,2.6vw,36px) auto 0;background:rgba(28,27,33,.82);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
"""
