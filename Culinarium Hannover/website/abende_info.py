"""Culinarium · was zu jedem Abend belegt ist (Robert 27.10.2026: «hau alles rein, was wir haben»).
Nur wörtliche Angaben aus den Beiträgen von @culinarium_hannover (_quelle/extern/ig/beitraege.md) und Rudis Beiträgen
(_quelle/extern/ig-team/beitraege.md); Bilder aus den Danke-Beiträgen, den Highlights des Kontos und Rudis Konto.
Schlüssel = Plakat-ID aus bau.ABENDE (None für den 22./23.09.2023 → 'ohne-2023')."""

IG = '_quelle/extern/ig/'
HL = '_quelle/extern/ig-highlights/'
TM = '_quelle/extern/ig-team/'

def ig(datum, code, *nr):
    return [IG + '%s_culinarium_hannover_%s-%d.jpg' % (datum, code, n) for n in nr]

def hl(*namen):
    return [HL + n + '.jpg' for n in namen]

def rudi(datum, code, *nr):
    return [TM + '%s_rudi__san_%s-%d.jpg' % (datum, code, n) for n in (nr or (1,))]

# je Abend: motto, zeilen [(Etikett, wörtlich)], rueckblick (wörtlich, Quelle), bilder, rudi [(datum, gericht, pfad)], quelle
INFO = {
 'CxNkFWTIvL2': dict(titel='Das erste Culinarium-Wochenende', motto='',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gänge-Menü. Hierbei kann ein Upgrade auf Fisch oder Fleisch, ganz nach deinem Geschmack erfolgen.“'),
            ('Drinks', '„fünf von Momos Signature Drinks, kreativ kreiert mit Agave oder Gin“'),
            ('Techniken', '„Fatwashing, Milkwashing oder auch Fermentation“'),
            ('Musik', '„Wir starten mit euch in den Abend mit unserem Live Act @sinibins“'),
            ('Ablauf', 'Beginn 19:00 Uhr, Essen 20:30 Uhr'),
            ('Karten', '„im 11A, Walk on the Wild Side oder bei Momo“')],
    rueckblick=None,  # «Swipe nach links …» ist eine Anweisung für Instagram, kein Rückblick (Robert 27.10.2026: Zitat als breite Kachel)
    bilder=ig('2023-09-15', 'CxNkFWTIvL2', 2) + ig('2023-09-16', 'CxQg56AItz6', 1, 2, 3, 4, 5) + hl('2023-09-15_highlight-5047-01', '2023-09-15_highlight-5047-03', '2023-09-17_highlight-5047-07'),
    rudi=[], quelle='CxNkFWTIvL2, CxQg56AItz6'),
 'ohne-2023': dict(titel='Whisky und Rum', motto='',
    zeilen=[('Rückblick', '„Danke, an alle die bei Whisky und Rum, sowie einem 3 Gänge Menü à la @11a.kuechengarten uns dieses Wochenende im @walkonthewildside_cocktailbar begleitet haben“'),
            ('Musik', '„Ein großes Dankeschön auch an unsere bezaubernde @sinibins, für ihr musikalisches Talent.“')],
    rueckblick=None,
    bilder=ig('2023-09-25', 'CxnB2TiM4Iy', 1, 2, 3, 4) + hl('2023-09-22_highlight-3094-02', '2023-09-22_highlight-3094-03'),
    rudi=[], quelle='CxnB2TiM4Iy'),
 'CyT32RTMB4d': dict(titel='', motto='Goldener Herbst',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gänge-Menü.“'),
            ('Drinks', '„5 von Momos kreativ kreierten Signature Drinks … ganz des Mottos ‚goldener Herbst‘“'),
            ('Techniken', '„Fatwashing, Milkwashing und Klärung von Drinks durch Enzyme“'),
            ('Musik', 'Live Act @sinibins am Samstag'),
            ('Ablauf', 'Beginn 19:00 Uhr, Essen 20:30 Uhr'),
            ('Spirituosen', '„sponsored by @camparideutschland @campari“')],
    rueckblick=('„Passend zu den Drinks gab es ein wunderbar abgestimmtes 3 Gänge Menü à la @11a.kuechengarten“', '25.10.2023'),
    bilder=ig('2023-10-12', 'CyT32RTMB4d', 2) + ig('2023-10-25', 'Cy0KSO7MlDA', 1, 2, 3, 4) + hl('2023-10-21_highlight-3138-02', '2023-10-21_highlight-3138-03', '2023-10-21_highlight-3138-04', '2023-10-21_highlight-3138-05'),
    rudi=[], quelle='CyT32RTMB4d, Cy0KSO7MlDA'),
 'CzMcqNcMCqG': dict(titel='', motto='Winter is coming',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gänge-Menü.“'),
            ('Drinks', '„5 von Momos Signature Drinks, kreativ kreiert diese Woche nach dem Motto Winter is coming“'),
            ('Ablauf', 'Beginn 19:00 Uhr, Essen 20:30 Uhr'),
            ('Karten', '„Vorverkauf per PayPal, schreib uns hierzu gerne an!“')],
    rueckblick=('„In gemütlichem Ambiente, hat @momo012027 uns wieder 5 seiner Signatur Drinks serviert.“', '12.12.2023'),
    bilder=ig('2023-11-03', 'CzMcqNcMCqG', 2) + ig('2023-12-12', 'C0w5_ZEsfY5', 1, 2, 3, 4) + hl('2023-11-18_highlight-0707-02', '2023-11-19_highlight-0707-04', '2023-11-19_highlight-0707-05'),
    rudi=[], quelle='CzMcqNcMCqG, C0w5_ZEsfY5'),
 'C0w6iuCMcnF': dict(titel='Silvester Edition', motto='',
    zeilen=[('Menü', '„Genieße unser Silvester Menü mit 4 Gängen und einem Amuse-Geule, nach Wunsch auch vegetarisch.“'),
            ('Drinks', '„5 von Momos Signature Drinks, kreativ kreiert“'),
            ('Dazu', '„Silvester der Abend des Champagners, stoßt mit uns an und feiert das neue Jahr!“'),
            ('Danach', 'After Show Party im @trustory.linden'),
            ('Ablauf', 'Beginn 20:00 Uhr, Essen 20:30 Uhr')],
    rueckblick=('„2023 mit einem zauberhaften Abschluss .. mit tollen Menschen, mit leckerem Essen und mit wunderbar kreativen Drinks, sowie mit der tollen @sinibins!“', '09.01.2024'),
    bilder=ig('2023-12-12', 'C0w6iuCMcnF', 2) + ig('2024-01-09', 'C15hZ_zIh60', 1, 2, 3, 4, 5, 6),
    rudi=[], quelle='C0w6iuCMcnF, C15hZ_zIh60'),
 'C17kqAXLfs_': dict(titel='', motto='Flashback',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gänge-Menü.“'),
            ('Drinks', '„5 von Momos kreativ kreierten Signature Drinks … ganz des Mottos ‚FLASHBACK‘“'),
            ('Musik', 'Live Act @sinibins am Samstag'),
            ('Ablauf', 'Beginn 19:00 Uhr, Essen 20:00 Uhr')],
    rueckblick=('„oldschool Drinks wie ‚Sex on the Beach‘ neu interpretiert von @momo012027. Es wurde karbonisiert, milchfiltriert, geshaked, gerührt und mit Espuma verziert.“', '29.01.2024'),
    bilder=ig('2024-01-10', 'C17kqAXLfs_', 2) + ig('2024-01-29', 'C2sFkpSscHP', 1),
    rudi=[], quelle='C17kqAXLfs_, C2sFkpSscHP'),
 'C56bJeds8PF': dict(titel='Zum ersten Mal mit Rudi', motto='Kabinett der Illusionen',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gänge-Menü.“'),
            ('Drinks', '„5 von Momos Signature Drinks, kreativ kreiert diese Woche nach dem Motto Kabinett der Illusionen“'),
            ('Ablauf', '„Beginn Aperitif und Musik: 19:00 Uhr, Essen: 19:30 Uhr“'),
            ('Karten', '„Vorverkauf per PayPal, schreib uns hierzu gerne an!“')],
    rueckblick=None,
    bilder=ig('2024-04-18', 'C56bJeds8PF', 2) + hl('2024-04-27_highlight-8299-02', '2024-04-27_highlight-8299-03', '2024-04-29_highlight-8299-04', '2024-04-29_highlight-8299-05'),
    rudi=[], quelle='C56bJeds8PF'),
 'C8cgYVSouVT': dict(titel='', motto='Erdig',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gänge-Menü.“'),
            ('Drinks', '„5 von Momos Signature Drinks, kreativ kreiert nach dem Motto ‚Erdig‘“; auf dem Plakat: 1 Apéritif, 4 Signature Drinks'),
            ('Musik', '„Begleitet wird der Aperitif von der schönen Stimme unserer wunderbaren @sinimusicofficial“'),
            ('Ablauf', '„Beginn Aperitif und Musik: 19:30 Uhr, Essen: ca. 20:00 Uhr“')],
    rueckblick=None,
    bilder=ig('2024-06-20', 'C8cgYVSouVT', 2) + hl('2024-07-20_highlight-4589-02', '2024-07-20_highlight-4589-03', '2024-07-20_highlight-4589-04', '2024-07-20_highlight-4589-05')
           + rudi('2024-07-25', 'C92atzHohOo', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
    rudi=[('25.07.2024', '„Unser Herzensprojekt“', ''), ('30.07.2024', 'ZWIEBELTARTELETT', TM + '2024-07-30_rudi__san_C-DxMFqs5Pz-1.jpg'),
          ('02.08.2024', 'ROTE BEETE / ZWIEBEL / PARMESAN', TM + '2024-08-02_rudi__san_C-Kj2bGMcOb-1.jpg'),
          ('03.08.2024', 'HOKKAIDO / KÜRBISKERN ÖL / HASELNUSS', TM + '2024-08-03_rudi__san_C-OFq0msPA7-1.jpg')],
    quelle='C8cgYVSouVT, @rudi__san C92atzHohOo'),
 'DCCf-ikoaGs': dict(titel='', motto='',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gänge-Menü.“'),
            ('Drinks', '„5 von Momos Signature Drinks, kreativ kreiert“'),
            ('Musik', '„Begleitet wird der Aperitif von der schönen Stimme unserer wunderbaren @sinimusicofficial“'),
            ('Ablauf', 'Freitag 19:00 Uhr, Samstag 17:00 Uhr'),
            ('Plätze', '„nur wenige Plätze pro Abend“')],
    rueckblick=('„Ein riesiges Dankeschön an Koch @rudi__san, der uns mit seinen kreativen Gerichten mal wieder regelrecht verzaubert hat … Und natürlich an @momo012027, der mit seinen perfekt abgestimmten Drinks für die ideale Begleitung gesorgt hat.“', '04.02.2025'),
    bilder=ig('2024-11-06', 'DCCf-ikoaGs', 2) + ig('2025-02-04', 'DFqZn2UMYMV', 1, 2, 3, 4, 5, 6),
    rudi=[], quelle='DCCf-ikoaGs, DFqZn2UMYMV'),
 'DFqbLG2s_dc': dict(titel='', motto='',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gänge-Menü.“'),
            ('Drinks', '„5 von Momos Signature Drinks, kreativ kreiert passend zum Essen“'),
            ('Musik', '„Begleitet wird der Aperitif von der schönen Stimme unserer wunderbaren @sinimusicofficial“'),
            ('Plätze', '„nur 14 Plätze pro Abend“')],
    rueckblick=None,
    bilder=ig('2025-02-04', 'DFqbLG2s_dc', 2) + hl('2025-02-22_highlight-4865-02', '2025-02-22_highlight-4865-06'),
    rudi=[], quelle='DFqbLG2s_dc'),
 'DJw8OqGMY1G': dict(titel='', motto='',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gänge-Menü.“'),
            ('Drinks', '„5 von Momos Signature Drinks, kreativ kreiert passend zum Essen“'),
            ('Ablauf', 'Freitag 13.06. ab 19:00 Uhr, Samstag 14.06. ab 17:00 Uhr')],
    rueckblick=None,
    bilder=ig('2025-05-17', 'DJw8OqGMY1G', 2) + hl('2025-06-15_highlight-6684-07', '2025-06-15_highlight-6684-09', '2025-06-15_highlight-6684-10', '2025-06-15_highlight-6684-11', '2025-06-15_highlight-6684-12'),
    rudi=[('24.06.2025', 'LAUCH / BLUMENKOHL / CHIPOTLE', TM + '2025-06-24_rudi__san_DLSA60BMwiG-1.jpg')],
    quelle='DJw8OqGMY1G, @rudi__san DLSA60BMwiG'),
 'DPwlqcfiKcA': dict(titel='', motto='',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gange-Menü.“'),
            ('Drinks', '„5 von Momos Signature Drinks, kreativ kreiert passend zum Essen“'),
            ('Ablauf', '„Beginn Freitag 14.11.: 19:00 Uhr | bereits ausverkauft!“, Samstag 15.11. ab 17:00 Uhr')],
    rueckblick=None, bilder=ig('2025-10-13', 'DPwlqcfiKcA', 2), rudi=[], quelle='DPwlqcfiKcA'),
 'DVjkofijp6R': dict(titel='', motto='',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gange-Menü.“'),
            ('Drinks', '„5 von Momos Signature Drinks, kreativ kreiert passend zum Essen“'),
            ('Ablauf', 'Freitag 27.03.2026 ab 19:00 Uhr, Samstag 28.03.2026 ab 17:00 Uhr')],
    rueckblick=None, bilder=ig('2026-03-06', 'DVjkofijp6R', 2),
    rudi=[('08.04.2026', 'BLUMENKOHL / ROGUEFORT / KAPERN / QUINOA', TM + '2026-04-08_rudi__san_DW4V45ujR0B-1.jpg')],
    quelle='DVjkofijp6R, @rudi__san DW4V45ujR0B'),
 'DbYnkdkjrNy': dict(titel='', motto='',
    zeilen=[('Menü', '„Genieße unser vegetarisches 3-Gange-Menü.“'),
            ('Drinks', '„5 von Momos Signature Drinks, kreativ kreiert passend zum Essen“'),
            ('Ablauf', 'Freitag 25.09.2026 ab 19:00 Uhr, Samstag 26.09.2026 ab 17:00 Uhr'),
            ('Stand', '„AUSGEBUCHT!“')],
    rueckblick=None, bilder=ig('2026-07-29', 'DbYnkdkjrNy', 2),
    rudi=[('23.10.2026', 'AUBERGINE / KOKOS / LIMETTE / SESAM', TM + '2026-10-23_rudi__san_De1pn9ttMoX-1.jpg')],
    quelle='DbYnkdkjrNy, @rudi__san De1pn9ttMoX'),
}

# Menükarten, abgelesen von Fotos der gedruckten Karten (Robert 27.10.2026). Je Gang: (Gang, Teller, Drink); '' = nicht lesbar.
# quelle: welches Bild; voll=False heisst: nur ein Teil der Karte ist auf dem Foto lesbar.
KARTEN = {
 'CxNkFWTIvL2': dict(quelle='Foto der Karte, Beitrag CxQg56AItz6 (16.09.2023)', voll=True, gaenge=[
    ('Amuse Bouche', '', 'Cleared Strawberry Martini · Gin | Cleared Erdbeer-Wasser'),
    ('Apéritif', '', 'Umami · Tequila | lakto-fermentierte Tomaten | Agave | Limettensaft | Tomatenstaub'),
    ('Vorspeise', 'Das „Brot der Freude“ · Geeister Sugo von allerfeinsten sizilianischen Dattel-Tomaten | Burrata-Mozzarella | Pfirsich | Avocado', 'Cabra · Mezcal | Thymian | Feige | Birne | Limetten | ziegenmilch-filtriert'),
    ('Hauptgang', 'Allerlei geröstete Pilze in Schnittlauch-Rahmsauce · hausgemachte Bandnudeln | grüner Erbsen-Sud', 'Molekulare Aviation · Gin | Zitrone | Maraschino | Veilchen-Caviar'),
    ('Dessert', 'Crème Brulée mit hausgemachtem Sorbet', 'Black Pearl · Black Sesam fatwashed Tequila | Guave | Grapefruit | Limette | MSG Solution')],
    upgrade=['Bunter Salat von der Permakultur Kirchhorst', 'Filet vom Fjord-Lachs mit Bouillabaisse-Sauce', 'Striploin-Steak (grasgefüttert aus Australien) mit Kräuterbutter']),
 'ohne-2023': dict(quelle='Foto der Karte in der Story vom 22.09.2023', voll=True, gaenge=[
    ('Apéritif', '', 'White Mojito'),
    ('Vorspeise', 'Sashimi vom Balfego-Thunfisch · Tomate | Ingwer | Sesam (vegetarische Alternative auf Nachfrage)', 'Birne'),
    ('Hauptgang', 'Risotto vom Hokkaido-Kürbis mit gebratenen Pfifferlingen', 'Butternut Old Fashioned'),
    ('Dessert', 'Crème Brulée mit hausgemachtem Sorbet', 'Escape'),
    ('Absacker', '', 'Autumn Highball')]),
 'CzMcqNcMCqG': dict(quelle='Foto der Karte, Beitrag C0w5_ZEsfY5 (12.12.2023), die rechte Hälfte aus der Story vom 18.11.2023 (Highlight 0707-02)', voll=True, gaenge=[
    ('Apéritif', '', 'Un air de Déjà-vu · Deja Vu Apretiv | Cranberry-Orangen-Sherbet | Rosmarin | Thomas Henry Spicy Ginger'),
    ('Vorspeise', 'Pilzkraftbrühe mit vegetarischen Gyoza', 'Pera Dulce · Cazcabel Tequila Honey | Cleared Pear Water | weiße Schokolade'),
    ('Hauptgang', 'Gebackenes Bio Ei auf Kartoffelstampf mit Champagner-Senf-Soße und Rote Bete', 'Beet it · Beetroot-infused Knut Hansen Gin | Himbeer-Cordial | Absinth | Aztec Bitters | Thomas Henry Soda'),
    ('Dessert', 'Crème Brûlée', 'Russian Winter · Three Sixty Vodka | Vanille | Coldbrew-Kaffee | Maronen | Feigen-Espuma'),
    ('Absacker', '', 'Apfel-Punsch · Ron Piet Rum | Sherry | Limette | Kamille | Apfel | Zimt')]),   # Quelle unvollständig, gekürzt am 29.10.2026 (auf der Karte folgt «Mandel…», danach über den Bildrand beider Fotos)
 'C56bJeds8PF': dict(quelle='Foto der Karte in der Story vom 29.04.2024', voll=True, gaenge=[
    ('Apéritif', 'Sauerteigbrot | Miso-Butter', 'Arcane · Hendrick’s Floral Adora | Rosen-Shrub | CO2'),
    ('Vorspeise', 'Gurke | Sesam | Sternanis', 'Cabinet Collins · Discarded Vodka | gelbe Paprika | grüner Apfel'),
    ('Hauptgang', 'Sellerie | Lauch | Frisée', 'Mystical Mixology · Hendrick’s Neptunia | Gurke | rosa Pfeffer | Sellerie'),
    ('Dessert', 'Amalfi-Zitrone | Vanille', 'Wanderlust · Monkey Shoulder Whisky | Rhabarber | Spargel | weißer Port | Estragon'),
    ('Absacker', '', 'Curiosity Crush · Discarded Banana Peel Rum | Erdbeere | Grana Padano')]),
 'C8cgYVSouVT': dict(quelle='Foto der Karte in der Story vom 20.07.2024, nur der Anfang lesbar', voll=False, gaenge=[
    ('Apéritif', 'Sauerteigbrot | geröstete Kürbisbutter | Senfkaviar', 'Vodka | Bergamotte | Champagner-Säure | Gurke | Dill')]),
 'DCCf-ikoaGs': dict(quelle='Foto der Karte, Beitrag DFqZn2UMYMV (04.02.2025), nur teilweise lesbar', voll=False, gaenge=[
    ('Apéritif', 'Sauerteig | fermentierte Tomate', 'Pallini Limoncello | Basilikum | Olivenöl | Schaumwein'),
    ('Vorspeise', 'Beeten | Salzzitrone | Feta-Käse', 'Purple-Shiso-Blätter | Yuzu | Galgant | Ziegenmilch')]),   # Quelle unvollständig, gekürzt am 29.10.2026 (Anfang des Drinks auf dem Foto unscharf)
 'DFqbLG2s_dc': dict(quelle='Foto der Karte in der Story vom 22.02.2025', voll=True, gaenge=[
    ('Apéritif', 'Sauerteig | Tomate | Butter', 'Cognac | Toasted Pumpkin Samen | Limette | Champagner'),
    ('Vorspeise', 'Miso | Sellerie | Röstzwiebeln', 'Vodka | Tom Yam | Guava | Cocos | Acids | Soda'),
    ('Hauptgang', 'Spinat | braune Butter | Parmesan', 'Tequila | lakto-fermentierte Tomate | Agave | Limette'),
    ('Dessert', 'Kaffee | Molke | Amaretto', 'Vodka | Cacao | Matcha | Mango'),
    ('Absacker', '', 'Gin | Turmeric | Ingwer')]),
}


# Auswahl für die Blätter (Robert 27.10.2026: edel, keine Doppelungen): Fotos der Menükarte stehen schon abgetippt daneben,
# Bildschirmfotos, Textstorys und doppelte Motive fliegen raus; Storys mit Farbrand werden auf das Foto zugeschnitten.
import os as _os
_WEG = {'highlight-4865-06', 'CxQg56AItz6-2', 'CxQg56AItz6-3', 'CxQg56AItz6-5', 'highlight-5047-01', 'highlight-5047-03', 'highlight-5047-07',
        'highlight-4589-05',
        # Robert 27.10.2026 («keine Instagram-Namen, keine komisch formatierten Bilder»): Storys mit Schrift im Motiv und Collagen
        'highlight-3138-04', 'highlight-0707-04', 'highlight-0707-05', 'highlight-8299-02', 'highlight-8299-04', 'highlight-4589-02', 'highlight-4589-04'}
_HIER = _os.path.dirname(_os.path.abspath(__file__))


def _pfad(q):
    """Zugeschnittene Fassung, wenn es eine gibt: zuerst abende_zuschnitt.py (ig-zuschnitt-2), dann der ältere Zuschnitt."""
    for ordner in ('_quelle/extern/ig-zuschnitt-2/', '_quelle/extern/ig-zuschnitt/'):
        z = ordner + _os.path.basename(q)
        if _os.path.exists(_os.path.join(_HIER, '..', z)):
            return z
    return q


for _k, _inf in INFO.items():
    # die zweite Seite der Ankündigung ist eine Grafik, kein Foto (Robert 27.10.2026: das grüne Kachelbild)
    _inf['bilder'] = [_pfad(q) for q in _inf['bilder'] if not any(w in q for w in _WEG) and not q.endswith('_%s-2.jpg' % _k)
                      and _os.path.exists(_os.path.join(_HIER, '..', q))]
