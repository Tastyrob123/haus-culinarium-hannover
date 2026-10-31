"""Culinarium · Station 05 · Fotos fürs Markenbuch (26.10.2026): nur Rudis eigene Dateien (_quelle/vom-kunden/) und die Plakate des Hauses
(_quelle/extern/ig/, eigenes Instagram-Konto). Verkleinert auf höchstens 1800 px, JPEG 84; Herkunft in marke/bilder/herkunft.json."""
import os, json
from PIL import Image, ImageOps
P = os.path.expanduser('~/Desktop/Website-Projekte/Culinarium Hannover/')
Z = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'marke', 'bilder'); os.makedirs(Z, exist_ok=True)
D, K, IG = '_quelle/vom-kunden/drive/', '_quelle/vom-kunden/', '_quelle/extern/ig/'
B = {  # Schlüssel: (Quelle, was zu sehen ist; keine Namen, wer wer ist, ist nicht belegt)
 'tresen': (D + '4568.jpg', 'Am Tresen wird geschüttelt, vor dem Regal mit den Flaschen'),
 'tafel-koch': (D + '5301.jpg', 'Am Tisch der Gäste, im Gespräch'),
 'tafel-kerzen': (D + '4972.jpg', 'Die lange Tafel, gedeckt, mit Kerzen'),
 'kerzen': (D + '3855.jpg', 'Kerzen auf der Tafel, dahinter das Mikrofon für den Live-Act'),
 'putz': (D + '4029.jpg', 'Durchbruch in der Wand, dahinter ein Tisch mit Kerze und Apothekerflasche'),
 'flur': (D + '3887.jpg', 'Der Flur zur Bar im Licht der Hängelampe'),
 'ballons': (D + '3937.jpg', 'Glasballons mit Sirup und Zapfhähnen an der Bar'),
 'glas-dunkel': (D + '5369.jpg', 'Ein Glas auf dunklem Tisch'),
 'ecke': (D + '5541.jpg', 'Die Schilder WILD SIDE an der Klinkerecke, darunter Bänder und Graffiti'),
 'anstossen': (D + '4026.jpg', 'Ein roter Drink wird über den Tisch gereicht'),
 'anstossen2': (D + '4024.jpg', 'Anstossen über der Tafel'),
 'pass': (K + '36740.png', 'Angerichtete Teller in Reihe'),
 'teller': (D + '5045.jpg', 'Ein Teller auf dunklem Grund'),
 'glas-hell': (D + '4921.jpg', 'Ein heller Drink im Weinglas'),
 'giessen': (D + '3823.jpg', 'Ein Drink wird am Tresen eingegossen'),
 'schaum': (D + '63963.jpg', 'Schaum aus dem Siphon auf einem Drink'),
 'team': (D + '63873.jpg', 'Drei vor dem Schriftzug NEGRONI an der Bar'),
 'schild-nacht': (D + '4096.jpg', 'Das Schild WILD SIDE in der Nacht'),
 'teller-gold': (D + '5146.jpg', 'Ein Gericht auf einem Teller mit Goldrand'),
 'plakat-2024-11': (IG + '2024-11-06_culinarium_hannover_DCCf-ikoaGs-1.jpg', 'Plakat 29./30.11.2024, Ski'),
 'plakat-2025-02': (IG + '2025-02-04_culinarium_hannover_DFqbLG2s_dc-1.jpg', 'Plakat 21./22.02.2025, Panther auf dem Thron'),
 'plakat-2025-06': (IG + '2025-05-17_culinarium_hannover_DJw8OqGMY1G-1.jpg', 'Plakat 13./14.06.2025, Gärtnerin'),
 'plakat-2025-11': (IG + '2025-10-13_culinarium_hannover_DPwlqcfiKcA-1.jpg', 'Plakat 14./15.11.2025, Kürbis'),
 'plakat-2026-03': (IG + '2026-03-06_culinarium_hannover_DVjkofijp6R-1.jpg', 'Plakat 27./28.03.2026, Panther mit Eisbecher'),
 'plakat-2026-09': (IG + '2026-07-29_culinarium_hannover_DbYnkdkjrNy-1.jpg', 'Plakat 25./26.09.2026, Mondfrau'),
}
her = {}
for k, (q, was) in B.items():
    im = ImageOps.exif_transpose(Image.open(P + q)).convert('RGB'); w, h = im.size
    im.thumbnail((1800, 1800), Image.LANCZOS); im.save(os.path.join(Z, k + '.jpg'), 'JPEG', quality=84, optimize=True, progressive=True)
    her[k] = dict(quelle=q, was=was, original=[w, h], hier=list(im.size))
json.dump(her, open(os.path.join(Z, 'herkunft.json'), 'w'), ensure_ascii=False, indent=1)
print(len(her), 'Bilder')
