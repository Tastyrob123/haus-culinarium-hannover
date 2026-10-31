#!/usr/bin/env python3
"""Das Besucherbuch (Le Registre) · Culinarium Hannover, 28.10.2026: jede Auswertung unabhängig aus den Rohdaten nachrechnen (Vorlage: nachrechnen.py
der Taverne zum Schäfli, dort des Schlössli, Gasterntal, Doldenhorn und Carlton-Europe; angepasst an die Wege und Seiten von Culinarium: neun Werte «Zum Platz»,
«zum Platz» = Platz gebucht oder auf die Warteliste gesetzt, «Platz buchen» ohne Buchung = geöffnet − gebucht, Startseite und «Alle Abende» zum Platz = Aufrufe
in Besuchen, die danach zum Platz kamen, Warteliste, Instagram, Bar und Dirty Chicken, Route, Sprache des Browsers). Regeln hier selbst geschrieben, nicht aus registre.py übernommen.
Eigene Rechnung (nichts aus registre.stand übernommen) gegen das, was registre.py ausgibt:
  A  Beispielwerte des Dienstes (stand beispiel) für 7/30/90 Tage, Rohdaten aus registre._beispiel
  B  Abgelegte Beispielwerte, heute bis zu verschiedenen Uhrzeiten gekürzt (ablage_heute), und A == B zur selben Uhrzeit
  C  Abgelegte Werte, um 1, 3 und 7 Tage auf später geschoben (Wochentage, Wochen, Vergleichszeitraum)
  D  Echte Zählung: Wegwerf-Zeilen über melde() in einen eigenen Ordner, Ergebnis gegen die Tagesdateien
  E  Datenschutz: in Tagesdateien und Ausgaben keine Adresse, kein Browser-Text, kein Kürzel
     python3 nachrechnen.py            → Bericht nachrechnen.txt, Rückgabe 1 bei einer Abweichung"""
import collections, datetime, json, os, random, re, shutil, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))
TMP = tempfile.mkdtemp(prefix='registre-pruef-')
os.environ['REGISTRE_ORDNER'] = os.path.join(TMP, 'daten')
import registre as RG  # noqa: E402

AUS, FEHL = [], [0]


def log(*a):
    s = ' '.join(str(x) for x in a); AUS.append(s); print(s)


def gleich(name, ist, soll):
    if ist != soll:
        FEHL[0] += 1
        log('  ABWEICHUNG', name, '\n    ist ', json.dumps(ist, ensure_ascii=False)[:600], '\n    soll', json.dumps(soll, ensure_ascii=False)[:600])
        return False
    return True


# ---------- eigene Rechnung ----------
def sek(z):
    h, m, s = map(int, z.split(':')); return h * 3600 + m * 60 + s


def art(s):
    if s == 'index.html': return 'start'
    if s == 'abende.html': return 'karte'
    if s == 'abend.html': return 'abend'
    if s == 'dirty-chicken.html': return 'essen'
    if s in ('bar.html', 'leute.html'): return 'erleben'
    if s == 'weg.html': return 'weg'
    return 'sonst'


BUCHUNG = {'buchung', 'booking'}   # Platz gebucht oder auf die Warteliste gesetzt


QUELLEN = [('google.', 'Google'), ('bing.', 'Bing'), ('duckduckgo.', 'DuckDuckGo'), ('ecosia.', 'Ecosia'), ('yahoo.', 'Yahoo'), ('instagram.', 'Instagram'),
           ('facebook.', 'Facebook'), ('threads.', 'Threads'), ('tiktok.', 'TikTok'), ('linkedin.', 'LinkedIn'), ('tripadvisor.', 'Tripadvisor'),
           ('visit-hannover.', 'Hannover Marketing'), ('hannover.de', 'Stadt Hannover'), ('chatgpt.', 'ChatGPT'), ('perplexity.', 'Perplexity')]


def quelle(h):
    if not h: return 'Direkt aufgerufen'
    for a, n in QUELLEN:
        if a in h: return n
    return h[4:] if h.startswith('www.') else h


def besuche(roh):
    """Rohdaten {tag: {'b': {gast: {l,o,r,g,h,a}}}} → Besuche (eigene Gruppierung: halbe Stunde Pause trennt)."""
    out = []
    for tag in sorted(roh):
        for g in (roh[tag].get('b') or {}).values():
            seiten = sorted(g['a'], key=lambda x: x['z'])
            gruppen, akt, ende = [], [], None
            for x in seiten:
                if akt and sek(x['z']) - ende > 30 * 60:
                    gruppen.append(akt); akt = []
                akt.append(x); ende = sek(x['z']) + int(x['sek'])
            if akt: gruppen.append(akt)
            for gr in gruppen:
                ev = {e for x in gr for e in x['e']}
                out.append(dict(tag=tag, zs=gr[0]['z'], l=g['l'], o=g['o'], g=g['g'], sp=gr[0]['sp'], h=quelle(g['h']), dauer=sum(x['sek'] for x in gr),
                                n=len(gr), buchung=bool(ev & BUCHUNG), anfrage=bool(ev & {'tisch', 'anfrage'}), kontakt=bool(ev & {'anruf', 'mail'}), route='route' in ev, weg=gr))
    return out


def py_rund(x, st=0):
    return round(x, st) if st else round(x)


def rechne(roh, liste, vorher):
    """Erwartete Ausgabe für einen Zeitraum, nur aus den Rohdaten."""
    alle = besuche(roh)
    B = [b for b in alle if b['tag'] in liste]
    V = [b for b in alle if b['tag'] in vorher]
    e = {}

    def kurz(X):
        z = [b['dauer'] for b in X if b['dauer'] > 0]; s = sum(b['n'] for b in X)
        return dict(besuche=len(X), seiten=s, buchung=sum(b['buchung'] for b in X), anfrage=sum(b['anfrage'] for b in X), kontakt=sum(b['kontakt'] for b in X), route=sum(b['route'] for b in X),
                    dauer_mittel=py_rund(sum(z) / len(z)) if z else None, seiten_je_besuch=py_rund(s / len(X), 1) if X else None,
                    laender=len({b['l'] for b in X if b['l'] and b['l'] != '??'}))
    e['summe'] = dict(kurz(B), heute=sum(1 for b in B if b['tag'] == liste[-1]))
    e['vorher'] = kurz(V)
    e['je_tag'] = [dict(tag=t, besuche=sum(1 for b in B if b['tag'] == t), seiten=sum(b['n'] for b in B if b['tag'] == t),
                        buchung=sum(1 for b in B if b['tag'] == t and b['buchung'])) for t in liste]
    e['vor_tag'] = [sum(1 for b in V if b['tag'] == t) for t in vorher]
    e['stunden'] = [sum(1 for b in B if int(b['zs'][:2]) == h) for h in range(24)]
    e['raster'] = [[sum(1 for b in B if int(b['zs'][:2]) == h and datetime.date.fromisoformat(b['tag']).weekday() == w) for h in range(24)] for w in range(7)]

    def rangliste(werte, n):
        c = collections.Counter(werte)
        return [dict(k=k, n=v) for k, v in sorted(c.items(), key=lambda x: (-x[1], str(x[0])))][:n]
    e['laender'] = rangliste([b['l'] or '??' for b in B], 20)
    e['sprachen'] = rangliste([b['sp'] for b in B], 12)
    e['geraete'] = rangliste([b['g'] for b in B], 12)
    e['herkunft'] = rangliste([b['h'] for b in B], 14)
    oc = collections.Counter((b['o'], b['l']) for b in B if b['o'])
    e['orte'] = [dict(k=o, l=l, n=v) for (o, l), v in sorted(oc.items(), key=lambda x: (-x[1], x[0]))][:20]
    sc = {}
    for b in B:
        bis = next((i for i, x in enumerate(b['weg']) if BUCHUNG & set(x['e'])), -1)   # alle Seiten bis zum Platz lagen auf dem Weg dorthin
        for i, x in enumerate(b['weg']):
            s = sc.setdefault(x['s'], [0, 0, 0, 0]); s[0] += 1
            if x['sek'] > 0: s[1] += x['sek']; s[2] += 1
            if i <= bis: s[3] += 1
    e['seiten'] = sorted((dict(s=k, n=v[0], sek=py_rund(v[1] / v[2]) if v[2] else None, buchung=v[3]) for k, v in sc.items()), key=lambda x: (-x['n'], x['s']))

    def zaehl(ereignis, a=None, g=None):
        z = 0
        for b in B:
            if g and b['g'] != g: continue
            bis = next((i for i, x in enumerate(b['weg']) if BUCHUNG & set(x['e'])), -1)
            for i, x in enumerate(b['weg']):
                if a and art(x['s']) != a: continue
                z += 1 if ereignis == 'seite' else (1 if i <= bis else 0) if ereignis == 'vor_platz' else x['e'].count(ereignis)
        return z

    def wert(z, v, **m):
        return dict(zahl=z, von=v, anteil=round(min(100.0, 100.0 * z / v), 1) if v else None, **m)
    auf = zaehl('seite')
    e['werte'] = dict(start=wert(zaehl('vor_platz', 'start'), zaehl('seite', 'start')),
                      karte=wert(zaehl('vor_platz', 'karte'), zaehl('seite', 'karte')),
                      booking=wert(zaehl('booking'), zaehl('buchung') + zaehl('booking'), anfrage=zaehl('buchung')),
                      abbruch=wert(max(0, zaehl('fenster') - zaehl('buchung')), zaehl('fenster')),
                      tisch=wert(zaehl('tisch'), auf, abend=zaehl('tisch', 'abend')),
                      anfrage=wert(zaehl('anfrage'), auf, start=zaehl('anfrage', 'start')),
                      kontakt=wert(zaehl('anruf') + zaehl('mail'), auf, anruf=zaehl('anruf'), mail=zaehl('mail')), chat=wert(zaehl('chat'), auf, dc=zaehl('chat', 'essen')),
                      route=wert(zaehl('route'), auf, weg=zaehl('route', 'weg')))
    wo = collections.OrderedDict()
    for t in e['je_tag']:
        d = datetime.date.fromisoformat(t['tag']); mo = d - datetime.timedelta(days=d.weekday())
        w = wo.setdefault(mo, dict(von=t['tag'], bis=t['tag'], tage=0, besuche=0, buchung=0))
        w['bis'] = t['tag']; w['tage'] += 1; w['besuche'] += t['besuche']; w['buchung'] += t['buchung']
    e['wochen'] = list(wo.values())
    top = [x['k'] for x in rangliste([b['l'] or '??' for b in B], 5) if x['k'] != '??'][:4]
    e['land_verlauf'] = [dict(k=l, n=[sum(1 for b in B if b['tag'] == t and (b['l'] or '??') == l) for t in liste]) for l in top]
    e['leer'] = not B
    mit = [t['tag'] for t in e['je_tag'] if t['besuche']]
    e['seit'] = mit[0] if mit else None
    neu = sorted(B, key=lambda b: (b['tag'], b['zs']), reverse=True)[:400]
    e['besuche'] = [dict(tag=b['tag'], z=b['zs'][:5], l=b['l'], o=b['o'], g=b['g'], sp=b['sp'], h=b['h'], dauer=b['dauer'], seiten=b['n'],
                         buchung=b['buchung'], anfrage=b['anfrage'], kontakt=b['kontakt'], route=b['route'], weg=[dict(z=x['z'][:5], s=x['s'], sek=x['sek'], e=x['e']) for x in b['weg']]) for b in neu]
    return e


FELDER = ['summe', 'vorher', 'je_tag', 'vor_tag', 'stunden', 'raster', 'laender', 'sprachen', 'geraete', 'herkunft', 'orte', 'seiten', 'werte', 'wochen',
          'land_verlauf', 'leer', 'seit', 'besuche']


def vergleiche(name, ist, soll):
    ok = True
    for f in FELDER:
        i = ist.get(f)
        if f == 'vorher':
            i = {k: v for k, v in i.items() if k not in ('von', 'bis')}
        if f == 'besuche':
            i = [dict(tag=b['tag'], z=b['z'], l=b['l'], o=b['o'], g=b['g'], sp=b['sp'], h=b['h'], dauer=b['dauer'], seiten=b['seiten'], buchung=b['buchung'],
                      anfrage=b['anfrage'], kontakt=b['kontakt'], route=b['route'], weg=[dict(z=x['z'], s=x['s'], sek=x['sek'], e=x['e']) for x in b['weg']]) for b in i]
        ok &= gleich(f'{name} · {f}', i, soll[f])
    return ok


def zeitraum(heute, t):
    liste = [(heute - datetime.timedelta(days=t - 1 - i)).isoformat() for i in range(t)]
    von = heute - datetime.timedelta(days=t - 1)
    vorher = [(von - datetime.timedelta(days=t - i)).isoformat() for i in range(t)]
    return liste, vorher


def kuerze(roh, heute, uhr):
    """Rohdaten: heute nur Besuche, die bis uhr begonnen haben (je Gast der erste Seitenaufruf)."""
    r = json.loads(json.dumps(roh))
    if heute in r:
        r[heute]['b'] = {k: g for k, g in r[heute]['b'].items() if min(x['z'] for x in g['a']) <= uhr}
    return r


def schiebe_roh(roh, um):
    return {(datetime.date.fromisoformat(t) + datetime.timedelta(days=um)).isoformat(): v for t, v in roh.items()}


def main():
    jetzt = RG.jetzt(); heute = jetzt.date(); uhr = jetzt.strftime('%H:%M:%S')
    log(f'Nachrechnen Das Besucherbuch · Culinarium Hannover, {jetzt:%d.%m.%Y %H:%M:%S} (Hannover, Europe/Berlin)')
    # A: Dienst, Beispielwerte
    for t in (7, 30, 90):
        liste, vorher = zeitraum(heute, t)
        roh = RG._beispiel(vorher + liste)
        d = RG.stand(t, beispiel=True)
        ok = vergleiche(f'A {t} Tage', d, rechne(roh, liste, vorher))
        log(f'A {t:>2} Tage, Beispiel des Dienstes: {"gleich" if ok else "ABWEICHUNG"} ({d["summe"]["besuche"]} Besuche, heute {d["summe"]["heute"]})')
    # B: Ablage (heute, ganz) auf verschiedene Uhrzeiten gekürzt; zur jetzigen Uhrzeit gleich wie der Dienst
    meta = json.load(open(os.path.join(os.path.dirname(HIER), 'beispiel', '30.json')))
    a_bis = datetime.date.fromisoformat(meta['bis'])
    for t in (7, 30, 90):
        liste, vorher = zeitraum(a_bis, t)
        voll = RG._beispiel(vorher + liste, voll=True) if a_bis == heute else None
        for u in ('00:00:00', '07:59:59', '12:00:00', uhr, '20:30:15', '23:59:59'):
            ist = RG.ablage_heute(t, heute=a_bis.isoformat(), uhr=u)
            if voll is None:
                log('B übersprungen: Ablage nicht von heute'); break
            ok = vergleiche(f'B {t} Tage bis {u}', ist, rechne(kuerze(voll, a_bis.isoformat(), u), liste, vorher))
            log(f'B {t:>2} Tage, Ablage bis {u}: {"gleich" if ok else "ABWEICHUNG"} ({ist["summe"]["besuche"]} Besuche, heute {ist["summe"]["heute"]})')
        if a_bis == heute:
            d = RG.stand(t, beispiel=True); ist = RG.ablage_heute(t, heute=heute.isoformat(), uhr=RG.jetzt().strftime('%H:%M:%S'))
            ok = vergleiche(f'A=B {t}', ist, {f: (d[f] if f != 'vorher' else {k: v for k, v in d[f].items() if k not in ('von', 'bis')}) if f != 'besuche' else
                                               [dict(tag=b['tag'], z=b['z'], l=b['l'], o=b['o'], g=b['g'], sp=b['sp'], h=b['h'], dauer=b['dauer'], seiten=b['seiten'],
                                                     buchung=b['buchung'], anfrage=b['anfrage'], kontakt=b['kontakt'], route=b['route'], weg=[dict(z=x['z'], s=x['s'], sek=x['sek'], e=x['e']) for x in b['weg']]) for b in d['besuche']]
                                               for f in FELDER})
            log(f'A=B {t:>2} Tage: Dienst und Ablage zur selben Uhrzeit {"gleich" if ok else "ABWEICHUNG"}')
    # C: Ablage um um Tage geschoben
    for um in (1, 3, 7):
        neu = a_bis + datetime.timedelta(days=um)
        for t in (7, 30, 90):
            liste0, vorher0 = zeitraum(a_bis, t)
            voll = schiebe_roh(RG._beispiel(vorher0 + liste0, voll=True), um) if a_bis == heute else None
            if voll is None:
                break
            liste, vorher = zeitraum(neu, t)
            for u in ('09:15:00', '21:45:30'):
                ist = RG.ablage_heute(t, heute=neu.isoformat(), uhr=u)
                ok = vergleiche(f'C +{um} {t} Tage bis {u}', ist, rechne(kuerze(voll, neu.isoformat(), u), liste, vorher))
                gleich(f'C +{um} {t} bis/von', [ist['bis'], ist['von'], ist['vorher']['von'], ist['vorher']['bis']], [liste[-1], liste[0], vorher[0], vorher[-1]])
                log(f'C +{um} Tage, {t:>2} Tage bis {u}: {"gleich" if ok else "ABWEICHUNG"}')
    # D: echte Zählung mit Wegwerf-Zeilen
    z = random.Random(1610)
    ua = ['Mozilla/5.0 (Macintosh) AppleWebKit Safari', 'Mozilla/5.0 (iPhone) Mobile Safari', 'Mozilla/5.0 (Windows NT 10.0) Firefox/131']
    ips = ['203.0.113.%d' % i for i in range(1, 9)]
    seiten = ['index.html', 'abende.html', 'abend.html', 'bar.html', 'leute.html', 'weg.html', 'dirty-chicken.html', 'impressum.html', 'datenschutz.html']
    angenommen = 0
    for i in range(160):
        pv = 'p%04d' % i; s = z.choice(seiten); e = z.choice(['-', 'fenster', 'fenster,buchung', 'booking', 'anruf', 'mail', 'chat', 'tisch', 'tisch,anfrage', 'route', 'anfrage', 'fenster,buchung,chat', 'route,anruf', '-', '-'])
        roh = f'r1 {pv} {s} {z.choice(["de", "en", "fr", "nl", "xx"])} {z.choice(["handy", "rechner", "tablet"])} {z.randint(0, 400)} {e} {z.choice(["-", "www.google.ch", "guide.michelin.com", "m.facebook.com", "www.gaultmillau.ch", "www.thurgau-bodensee.ch", "www.schloessli-bottighofen.ch", "www.wigoltingen.ch", "bookings.zenchef.com"])}'
        angenommen += RG.melde(roh.encode(), z.choice(ips), z.choice(ua), z.choice(['CH', 'DE', 'NL']), z.choice(['Bern', 'Thun', 'Utrecht', '']), 'BE')
        if z.random() < 0.3:   # Ende desselben Seitenaufrufs: Sekunden und Klicks dazu
            RG.melde(f'r1 {pv} {s} de rechner {z.randint(0, 900)} chat -'.encode(), ips[0], ua[0], 'CH', 'Bern', 'BE')
    falsch = [b'r1 abcd index.html qq rechner 5 - -', b'r1 abcd index.html de rechner 5 hack -', b'r1 abcd index.html de rechner 5 spa -', b'r2 abcd index.html de rechner 5 - -', b'x' * 301,
              'r1 abcd indëx.html de rechner 5 - -'.encode(), b'r1 abcd ../etc.html de rechner 5 - -', b'r1 abcd index.html de rechner 5 - <script>']
    abgelehnt = [RG.melde(f, ips[0], ua[0]) for f in falsch] + [RG.melde(b'r1 abcd index.html de rechner 5 - -', ips[0], 'Googlebot/2.1'),
                                                               RG.melde(b'r1 abcd index.html de rechner 5 - -', ips[0], 'Mozilla HeadlessChrome'),
                                                               RG.melde(b'r1 abcd index.html de rechner 5 - -', ips[0], '')]
    gleich('D ungültige Zeilen abgelehnt', abgelehnt, [False] * len(abgelehnt))
    # frühere Tage als Tagesdateien (wie sie der Speicher hält): mehrere Besuche je Gast, Pausen über und unter einer halben Stunde, ohne Ort
    for alt in z.sample(range(1, 180), 60):
        tag = (heute - datetime.timedelta(days=alt)).isoformat(); b = {}
        for g in range(z.randint(0, 9)):
            t = z.randint(6 * 3600, 22 * 3600); a = []
            for k in range(z.randint(1, 7)):
                sk = z.choice([0, 0, 5, 40, 200, 1800])
                a.append({'k': f'q{g}{k}', 'z': '%02d:%02d:%02d' % (t // 3600, t // 60 % 60, t % 60), 's': z.choice(seiten), 'sp': z.choice(['de', 'en', 'fr', 'it']),
                          'sek': sk, 'e': sorted(set(z.sample(['fenster', 'buchung', 'booking', 'tisch', 'anfrage', 'anruf', 'mail', 'chat', 'route'], z.choice([0, 0, 0, 1, 2]))))})
                t += sk + z.choice([3, 60, 1799, 1801, 2400])
                if t > 23 * 3600: break
            z.shuffle(a)
            b['%010x' % z.getrandbits(40)] = {'l': z.choice(['CH', 'DE', 'NL', 'US', '']), 'o': z.choice(['Kreuzlingen', 'Konstanz', '', 'Zürich']), 'r': '', 'g': z.choice(['handy', 'rechner', 'tablet']),
                                              'h': z.choice(['', 'www.google.com', 'www.gaultmillau.ch', 'www.thurgau-bodensee.ch', 'example.org']), 'a': a}
        json.dump({'b': b}, open(os.path.join(os.environ['REGISTRE_ORDNER'], tag + '.json'), 'w'))
    roh = {}
    for f in os.listdir(os.environ['REGISTRE_ORDNER']):
        if f.endswith('.json'):
            roh[f[:-5]] = json.load(open(os.path.join(os.environ['REGISTRE_ORDNER'], f)))
    for t in (7, 30, 90):
        liste, vorher = zeitraum(heute, t)
        d = RG.stand(t)
        ok = vergleiche(f'D {t} Tage', d, rechne({k: v for k, v in roh.items() if k in liste + vorher}, liste, vorher))
        log(f'D {t:>2} Tage, echte Zählung ({angenommen} Zeilen angenommen, {len(falsch) + 3} ungültige abgelehnt): {"gleich" if ok else "ABWEICHUNG"} ({d["summe"]["besuche"]} Besuche)')
    # E: Datenschutz
    text = ''.join(open(os.path.join(os.environ['REGISTRE_ORDNER'], f)).read() for f in os.listdir(os.environ['REGISTRE_ORDNER']))
    funde = [x for x in ips + ['Macintosh', 'iPhone', 'Windows', 'Mozilla', 'Firefox'] if x in text]
    gleich('E Tagesdatei ohne Adresse und Browser-Text', funde, [])
    aus = json.dumps(RG.stand(30), ensure_ascii=False)
    kz = set(re.findall(r'"([0-9a-f]{10})"', text))
    gleich('E Ausgabe ohne Kürzel, Adresse, Browser-Text', [x for x in list(kz) + ips + ['Mozilla'] if x in aus], [])
    for t in (7, 30, 90):
        a = json.dumps(json.load(open(os.path.join(os.path.dirname(HIER), 'beispiel', f'{t}.json'))))
        gleich(f'E Ablage {t} ohne Adresse', [x for x in ('ip', 'ua', 'Mozilla', '"kz"') if f'"{x}"' in a or x in ('Mozilla',) and x in a], [])
    log('E Datenschutz: Tagesdateien ohne Adresse/Browser-Text, Ausgabe ohne Kürzel')
    shutil.rmtree(TMP, ignore_errors=True)
    log(f'Ergebnis: {FEHL[0]} Abweichungen')
    open(os.path.join(HIER, 'nachrechnen.txt'), 'w', encoding='utf-8').write('\n'.join(AUS) + '\n')
    return 1 if FEHL[0] else 0


if __name__ == '__main__':
    sys.exit(main())
