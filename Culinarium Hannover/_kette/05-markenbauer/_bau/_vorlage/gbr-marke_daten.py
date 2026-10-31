"""Gemeinsame Daten der Gestaltung des Grand Beau-Rivage: Farben der neuen Website (Wahrheit: assets/css/main.css, :root, Stand 11.10.2026),
Herkunft der Farben aus den Hausfotos, Messung der Farbstreifen, Kontrast nach WCAG 2.1. Genutzt vom Markenbuch (markenbuch.py → marke/)
und vom Abschnitt Handschrift der Werkbank (marke_werkbank.py). Farben nur hier ändern."""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'img')

# ---------------------------------------------------------------- Farben (Werte aus assets/css/main.css :root, Stand 11.10.2026)
GRUPPEN = [
    ('hell', 'Helle Flächen', 'Der Normalzustand. Hier wird gelesen.', [
        ('weiss', 'Weiss', '#fdf9f1', 'Blätter, Karten, Briefbogen'),
        ('papier', 'Papierton', '#f7f0e3', 'Grundfläche der Seite'),
        ('creme', 'Creme', '#efe4cf', 'zweite helle Fläche, Tapete hell'),
        ('sand', 'Sand', '#e2d2b5', 'Kanten, Unterseite der Knöpfe')]),
    ('dunkel', 'Dunkle Töne', 'Eine dunkle Fläche, immer mit Tapete.', [
        ('marine', 'Marine', '#1b2033', 'die dunkle Fläche, mit Tapete'),
        ('blau', 'Blau', '#2c334d', 'Knöpfe auf hellem Grund'),
        ('tinte', 'Tinte', '#1a1d28', 'Schrift auf Papier und Creme')]),
    ('gold', 'Gold', 'Zeichnet, schreibt nie den Lesetext.', [
        ('gold', 'Gold', '#e6d2a2', 'Zeichen und Zeilen auf Marine'),
        ('taupe', 'Taupe', '#b0934f', 'Linien, Zeichen auf Papier'),
        ('akzent', 'Akzent', '#967d40', 'zweite Titelzeile auf Hell'),
        ('taupe-tief', 'Taupe tief', '#826c35', 'kleine Goldschrift auf Hell')]),
    ('rot', 'Sonderfarbe', 'Nur für die Bar.', [
        ('rot', 'Bar-Rot', '#7a1f2b', 'Bar «Le Vieux Rivage»')]),
]
F = {k: (n, h) for _, _, _, l in GRUPPEN for k, n, h, _ in l}

# Glanzgold (Robert 14.10.2026: «an manchen Stellen, wie im Hero oder in den Balken oben, arbeiten wir auch mit diesem Gold»): kein einzelner Ton,
# sondern ein Verlauf wie poliertes Messing, wie das Gold im Logo des Hauses. Werte aus assets/css/main.css (jeweils die letzte Regel):
# Fläche = .goldband und #oben form[data-leiste] button, Zeichen = .hero .hero__ort; das Zeichen im Kopf ist das Goldlogo assets/logo/zeichen-gold.webp.
GLANZ_SATZ = 'Wie das Gold im Logo des Hauses: kein Ton, sondern ein Verlauf wie poliertes Messing. Nur an festen Stellen, im Kopf der Startseite und in den Goldbändern, nie für Lesetext.'
GLANZ = [
    ('glanzgold-flaeche', 'Glanzgold Fläche', 'linear-gradient(180deg,#f8eac6 0%,#ead09a 20%,#d6b679 52%,#c2a062 80%,#aa874f 100%)',
     'Goldband unter dem Kopf und am Ende jeder Seite, Knopf «Verfügbarkeit prüfen» im Kopf', '#1a1d28'),
    ('glanzgold-zeichen', 'Glanzgold Zeichen', 'linear-gradient(180deg,#fff6dc 0%,#f1dcaa 32%,#dcbd7c 50%,#c4a062 60%,#e6cd95 78%,#f7e9c2 100%)',
     'Zeichen des Hauses und Ortszeile im Kopf der Startseite', '#1a1d28'),
]


def glanz_stopps(verlauf):
    """Die Farbwerte eines Verlaufs, in Reihenfolge."""
    import re
    return re.findall(r'#[0-9a-fA-F]{6}', verlauf)

# Woher die Farben kommen: (Foto in assets/img, Titel, Satz, Töne, die daraus geworden sind, Ausschnitt)
HERKUNFT = [
    ('decke', 'Stuck in der Halle', 'Warmes Weiss mit einem Hauch Ocker, wie der Stuck an der Decke der Halle. Daraus sind die hellen Flächen geworden, auf denen gelesen wird.', ['weiss', 'papier', 'creme', 'sand'], '50% 50%'),
    ('hk-leuchter', 'Messing und Kristall', 'Der Goldton der Leuchter und Beschläge. Auf Marine bleibt er hell, auf Papier ist er dunkler gezogen, damit er lesbar bleibt.', ['gold', 'taupe', 'akzent', 'taupe-tief'], '50% 40%'),
    ('haus-abend', 'Der Himmel über dem Haus', 'Das Blau ist eine Entscheidung des Entwurfs: der Himmel über der Fassade, so tief gezogen, dass Gold und Creme darauf leuchten.', ['marine', 'blau'], '50% 30%'),
    ('hist-karte', 'Post aus dem Archiv', 'Dunkle Schrift auf warmem Papier, wie auf der Post aus den frühen Jahren des Hauses. Geschrieben wird in Tinte, einem Schwarz mit etwas Blau, nie in reinem Schwarz.', ['tinte', 'papier'], '50% 50%'),
    ('bar-theke', 'Bar «Le Vieux Rivage»', 'Das Rot der Wände und Hocker. Es bleibt der Bar vorbehalten und taucht in der übrigen Gestaltung nicht auf.', ['rot'], '50% 55%'),
    ('aare-wasser', 'Die Aare', 'Das Türkis der Aare bleibt im Foto und wird bewusst nicht Teil der Palette. Neben Gold und Marine würde es den warmen Grundton des Hauses kippen.', [], '50% 50%'),
]


def foto(key, groesse='m'):
    """Pfad (relativ zu marke/) zur passenden Fassung eines Hausfotos."""
    folge = {'l': ('-l', '', '-m', '-s'), 'm': ('-m', '', '-l', '-s'), 's': ('-s', '-m', '', '-l')}[groesse]
    for s in folge:
        if os.path.exists(os.path.join(IMG, f'{key}{s}.webp')):
            return f'../assets/img/{key}{s}.webp'
    raise FileNotFoundError(key)


def streifen(key, n=5):
    """Die Töne eines Fotos, gemessen: Median-Schnitt auf n Farben, sortiert nach Helligkeit, Breite = Anteil im Bild."""
    p = os.path.join(ROOT, foto(key, 'm').replace('../', '', 1))
    im = Image.open(p).convert('RGB'); im.thumbnail((360, 360))
    q = im.quantize(n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:n * 3]
    ges = im.size[0] * im.size[1]
    t = [(c / ges, '#%02x%02x%02x' % tuple(pal[i * 3:i * 3 + 3])) for c, i in q.getcolors()]
    t.sort(key=lambda x: -lum(x[1]))
    return t


def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(h):
    def k(c):
        c /= 255; return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = rgb(h); return .2126 * k(r) + .7152 * k(g) + .0722 * k(b)


def kontrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)


