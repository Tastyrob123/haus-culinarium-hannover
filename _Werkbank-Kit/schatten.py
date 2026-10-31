"""Schatten fest ins Bild gerechnet (Robert 12.10.2026, Kofferaufkleber des Grand Beau-Rivage): ein CSS-Schatten (filter: drop-shadow)
auf einem Bild, das sich bewegt, zeichnet Safari erst verspätet und teils als Kasten. Im Bild selbst kostet er nichts und folgt immer der Form."""
from PIL import Image, ImageFilter


def backe(im, rand=.09, tiefe=.03, weich=.022, staerke=.42, farbe=(8, 10, 22)):
    """im: RGBA mit Transparenz → neues RGBA, ringsum Platz, darunter der Schatten aus der eigenen Form."""
    im = im.convert('RGBA')
    w, h = im.size
    p = round(max(w, h) * rand)
    neu = Image.new('RGBA', (w + 2 * p, h + 2 * p), (0, 0, 0, 0))
    a = im.getchannel('A').point(lambda v: int(v * staerke))
    sch = Image.new('RGBA', im.size, farbe + (0,)); sch.putalpha(a)
    lage = Image.new('RGBA', neu.size, (0, 0, 0, 0)); lage.paste(sch, (p, p + round(max(w, h) * tiefe)))
    lage = lage.filter(ImageFilter.GaussianBlur(max(w, h) * weich))
    neu.alpha_composite(lage); neu.alpha_composite(im, (p, p))
    return neu
