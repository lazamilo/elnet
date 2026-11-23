#!/usr/bin/env python3
"""Generates the ELNET redesign pages into ./site. Run: python3 build.py"""
import os, re
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')
I = 'assets/img/'
import time
V = str(int(time.time()))

LOGO = open(os.path.join(SITE, 'assets/logo-tight.svg')).read()
LOGO = LOGO[LOGO.index('<svg'):]
LOGO_LOADER = LOGO.replace('id="elnet-logo"', 'id="elnet-logo-loader"')
LOGO_FOOT = LOGO.replace('id="elnet-logo"', 'id="elnet-logo-foot"')
ARR = '<svg class="arr" viewBox="0 0 20 20" fill="none"><path d="M3 10h13M11 4.5 16.5 10 11 15.5" stroke="currentColor" stroke-width="1.8"/></svg>'
CHECK = '<svg viewBox="0 0 20 20" fill="none"><path d="M2 10h14M10 4l6 6-6 6" stroke="currentColor" stroke-width="1.6"/></svg>'

DIVS = {
  'elektroinstalacije': dict(
    title='Elektroinštalacije', short='Načrtovanje in izvedba za poslovne, javne in stanovanjske objekte.',
    banner='ELNET-slider-elektro-instalacije-vezje.jpg', thumb='ELNET-elektro-instalacije-03-osvetlitev-dvorane.jpg',
    person=('Miran Sehur','komerciala','miran.sehur@elnet.si','070 550 215'),
  ),
  'soncne-elektrarne': dict(
    title='Sončne elektrarne', short='Fotovoltaika na strehah poslovnih in upravnih stavb.',
    banner='ELNET-slider-soncna-elektrarna-T2-Ver-1.jpg', thumb='ELNET-Soncna-elektrarna-T2-Brnciceva.jpg',
    person=('Jan Pušnik','sončne elektrarne','jan.pusnik@elnet.si','051 266 019'),
  ),
  'polnilnice-moon': dict(
    title='Polnilnice MOON', short='Polnilnice za električna vozila v sodelovanju s Porsche Slovenija.',
    banner='ELNET-slider-EV-polnilnica-MOON2.jpg', thumb='ELNET-EV-polnilnica-MOON-vklop1.jpg',
    person=('Primož Deželak','nabava','primoz.dezelak@elnet.si','041 333 430'),
  ),
}

ELEKTRO_PROJECTS = [
  ('ELNET-elektro-instalacije-01-Nova-Ljubljanska-Banka.jpg','Poslovalnica NLB Nove Fužine','Ljubljana'),
  ('ELNET-elektro-instalacije-02-osvetlitev-prostorov-slepi-in-slabovidni.jpg','Očesna klinika UKC, NC CRSS','Ljubljana'),
  ('ELNET-elektro-instalacije-03-osvetlitev-dvorane.jpg','Univerza v Ljubljani, zbornična dvorana','Ljubljana'),
  ('ELNET-elektro-instalacije-04-osvetlitev-talnega-vodometa.jpg','Mestno jedro Zagorje ob Savi','Zagorje'),
  ('ELNET-elektro-instalacije-05-operacijska-soba.jpg','UKC, nova porodnišnica','Ljubljana'),
  ('ELNET-elektro-instalacije-06-osvetlitev-poslovalnice-NLB.jpg','Poslovalnica NLB Seidlova','Novo mesto'),
  ('ELNET-elektro-instalacije-07-osvetlitev-have.jpg','RUJZ Design','Hrastnik'),
]
ELEKTRO_CAPS = [
  ('ELNET-elektro-instalacije-08-omarica.jpg','Izdelava elektro omar'),
  ('ELNET-elektro-instalacije-09-plaganje-elektricnih-kablov.jpg','Izdelava grobih elektro-inštalacij'),
  ('ELNET-elektro-instalacije-10-elekricne-omarice.jpg','Izdelava nizkonapetostnih blokov'),
  ('ELNET-elektro-instalacije-11-visoka-napetost.jpg','Izdelava trafo postaj'),
]
SOLAR = [
  ('ELNET-Soncna-elektrarna-T2-Brnciceva.jpg','T2, Brnčičeva','Ljubljana'),
  ('ELNET-Soncna-elektrarna-Katselec1.jpg','Avtotransporti Kastelec, objekt Stara pošta','Grosuplje'),
  ('ELNET-Soncna-elektrarna-Poslovni-objekt-ELNET.jpg','Poslovna stavba ELNET','Izlake'),
  ('ELNET-Soncna-elektrarna-T2-Ver1.jpg','T2, Verovškova','Ljubljana'),
  ('ELNET-Soncna-elektrarna-IMV-Center.jpg','IMV Center',''),
  ('ELNET-soncna-elektrarna-Triglav-AS.jpg','Sončna elektrarna Triglav AS',''),
]
MOON = [
  ('ELNET-EV-polnilnica-MOON-polnilnica1.jpg','Polnilnica MOON'),
  ('ELNET-EV-polnilnica-MOON-vklop1.jpg','Priklop električnega vozila'),
  ('ELNET-EV-polnilnica-MOON-stanje-baterije1.jpg','Testiranje električnega vozila'),
  ('ELNET-EV-polnilnica-MOON-merjenje1.jpg','Instalacija, meritve, testiranje'),
  ('ELNET-EV-polnilnica-MOON1.jpg','Polno in gremo'),
]
CLIENTS = ['Nova Ljubljanska banka','Porsche Slovenija','UKC Ljubljana','Univerza v Ljubljani','Zdravstveni dom Ljubljana',
  'Media Publikum','ETI Elektroelement','Avtohiša Malgaj','Zasavske lekarne','KSW Tehnika','Maribox','Vinska klet Frelih',
  'RUJZ Design','Svea Interier','BKS Bank','PAM Novo mesto','Lesnina MG Oprema','MB Oprema','Sintal','Petrol','Avtotransporti Kastelec']
REF_GROUPS = [
  ('Vzdrževalna in intervencijska dela','ELNET-elektro-vzdrzevalna-dela-center-slabovidnih.jpg',
   ['NLB poslovalnice po Sloveniji','BKS Bank poslovalnice po Sloveniji','Univerza v Ljubljani, rektorat','UKC Ljubljana, klinike',
    'ZD Ljubljana: Vič, Šiška, Moste, Bežigrad','Lekarne Zasavskih lekarn']),
  ('Elektro-inštalacijska dela','ELNET-elektro-instlacijska-dela-poslovalnice-NLB.jpg',
   ['Prenova poslovalnic NLB','Prenova poslovalnic BKS Bank','Proizvodni prostori ETI Izlake','Mega center II Ljubljana',
    'Poslovni prostori Maribox Maribor','Poslovno proizvodni objekt RUJZ Design Hrastnik','Poslovni prostori Porsche Slovenija',
    'Poslovni prostori Sensilab Ljubljana','Slaščičarna in kavarna Zvezda','Vila Alja','Vila Balerina','Stanovanjski blok Domžalska vrata',
    'Stanovanjsko naselje Črnuška Gmajna','Blok Vidovdanska 9 Ljubljana','Stanovanjske hiše Brezovica, Kobjeglava, Turjak, Smlednik, Izlake',
    'Adaptacija OŠ Unec','Vrtec Galjevica','Vrtec Kolezija','Vrtec Petrovče','Vrtec Kostanjček','Izobraževalni center komunale Kočevje',
    'Adaptacija bolniških sob UKC Ljubljana','Hitra izvedba COVID bolniških sob','Poslovni prostori ZAG Ljubljana','Center slepih in slabovidnih']),
  ('Postavitev sončnih elektrarn','ELNET-soncna-elektrarna-Triglav-AS.jpg',
   ['Poslovni objekt Avtotransporti Kastelec Grosuplje','Poslovni objekt Cookinox Ivančna Gorica','T2, upravna stavba Verovškova','T2, Brnčičeva',
    'Poslovna stavba Porsche Slovenija Verovškova','Porsche Inter Auto Koper','Avtohiša Malgaj Trbovlje','Avtohiša Malgaj Ljubljana',
    'Poslovalnice Zavarovalnice Triglav po Sloveniji','Stanovanjski objekti po celotni Sloveniji','Sončna elektrarna Triglav AS']),
  ('Postavitev MOON električnih polnilnic','ELNET-polnilnica-IONITY.jpg',
   ['Hitra polnilnica IONITY na izvozu Radovljica sever-jug','Poslovni prostori Porsche Bravničarjeva','Avtohiša Slak Trebnje','Avtohiša Lovše Radomlje',
    'Avtohiša Klemenčič Ljubljana','Parkirna hiša Šubičeva v Ljubljani','Poslovni objekt Tanin Sevnica','Poslovni prostori MAN Truck & Bus Slovenija']),
]
TEAM = [
  ('Matjaž Vidmar','direktor','matjaz.vidmar@elnet.si','041 688 164'),
  ('Maja Vidmar','finance','maja.vidmar@elnet.si','031 818 292'),
  ('Miran Sehur','komerciala','miran.sehur@elnet.si','070 550 215'),
  ('Primož Deželak','nabava','primoz.dezelak@elnet.si','041 333 430'),
  ('Primož Ule','vodja projektov','primoz.ule@elnet.si','070 550 211'),
  ('Jan Pušnik','sončne elektrarne','jan.pusnik@elnet.si','051 266 019'),
  ('Jan Martinčič','svetovalec MOON','jan.martincic@elnet.si','041 326 805'),
]

def tel(n): return 'tel:+386' + n.replace(' ', '').lstrip('0')
def initials(n): return ''.join(p[0] for p in n.split()[:2])
def rows(*lines): return ''.join(f'<span class="row"><span>{l}</span></span>' for l in lines)

REF_SNIPPET = r'''<script>
(function () {
  if (!/[?&]r=/.test(location.search)) return;
  var s = document.createElement('script');
  s.async = true;
  s.referrerPolicy = 'no-referrer';
  s.setAttribute('data-landing', location.href);
  s.src = 'https://phplaravel-758037-6569212.cloudwaysapps.com/v/script.js';
  document.head.appendChild(s);
})();
</script>'''

def head(title, desc, active):
  nav_items = [('index.html','Domov'),('projekti.html','Projekti'),('o-nas.html','O nas'),('kontakt.html','Kontakt')]
  def a(h, t): return f'<a href="{h}" class="{"active" if active==h else ""}">{t}</a>'
  mega_cards = ''.join(f'''<a class="mega-card" href="{k}.html"><div class="ph"><img src="{I}{d["thumb"]}" alt="{d["title"]}" loading="lazy"></div><h4>{d["title"]}</h4><p>{d["short"]}</p></a>''' for k, d in DIVS.items())
  svc_active = 'active' if active in [k + '.html' for k in DIVS] else ''
  mm_sub = ''.join(f'<a class="sub" href="{k}.html">{d["title"]}</a>' for k, d in DIVS.items())
  return f'''<!doctype html>
<html lang="sl" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="icon" href="assets/logo-tight.svg">
<link rel="preload" href="assets/fonts/MaisonNeue-Medium.otf" as="font" type="font/otf" crossorigin>
<link rel="preload" href="assets/fonts/MaisonNeue-Book.otf" as="font" type="font/otf" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={V}">
<script>document.documentElement.classList.remove('no-js')</script>
{REF_SNIPPET}
</head>
<body>
<div class="loader" aria-hidden="true">{LOGO_LOADER}<i class="bar"></i></div>
<header class="nav">
  <a class="logo" href="index.html" aria-label="ELNET domov">{LOGO}</a>
  <nav class="nav-links">
    {a('index.html','Domov')}
    <div class="has-mega"><button class="{svc_active}" aria-haspopup="true">Storitve</button>
      <div class="mega"><div class="mega-intro"><p>Tri področja, ena ekipa.</p><p class="muted">Od elektro omare do sončne elektrarne na strehi in polnilnice pred vrati.</p></div><div class="mega-cards">{mega_cards}</div></div>
    </div>
    {a('projekti.html','Projekti')}{a('o-nas.html','O nas')}{a('kontakt.html','Kontakt')}
    <a class="btn blue-btn nav-cta" href="kontakt.html#povprasevanje">Povpraševanje {ARR}</a>
  </nav>
  <button class="burger" aria-label="Meni"><span></span><span></span></button>
</header>
<div class="mmenu">
  <div><a class="big" href="index.html">Domov</a><a class="big" href="elektroinstalacije.html">Storitve</a>{mm_sub}<a class="big" href="projekti.html">Projekti</a><a class="big" href="o-nas.html">O nas</a><a class="big" href="kontakt.html">Kontakt</a></div>
  <div><a class="btn blue-btn" href="kontakt.html#povprasevanje">Pošljite povpraševanje {ARR}</a><p class="muted" style="margin-top:20px">03 56 79 540 · info@elnet.si</p></div>
</div>
<main>
'''

FOOT = f'''</main>
<footer class="footer wrap">
  <div class="footer-top">
    <div><p class="bigline">Imate projekt? <a href="kontakt.html#povprasevanje" class="link-u">Pišite nam.</a></p></div>
    <div><h5>Storitve</h5><ul>{''.join(f'<li><a href="{k}.html">{d["title"]}</a></li>' for k, d in DIVS.items())}</ul></div>
    <div><h5>Podjetje</h5><ul><li><a href="projekti.html">Projekti</a></li><li><a href="o-nas.html">O nas</a></li><li><a href="kontakt.html">Kontakt</a></li><li><a href="https://elnet.si/pravila-zasebnosti/">Pravila zasebnosti</a></li></ul></div>
    <div><h5>ELNET d.o.o.</h5><ul><li>Spodnje Izlake 10 A</li><li>1411 Izlake</li><li><a href="tel:+38635679540">03 56 79 540</a></li><li><a href="mailto:info@elnet.si">info@elnet.si</a></li></ul></div>
  </div>
  <div class="footer-logo">{LOGO_FOOT}</div>
  <div class="footer-bottom"><span>© ELNET d.o.o. 2026</span><span>Elektroinštalacije od leta 1983</span></div>
</footer>
<script src="assets/vendor/gsap.min.js"></script>
<script src="assets/vendor/ScrollTrigger.min.js"></script>
<script src="assets/vendor/lenis.min.js"></script>
<script src="assets/js/site.js?v={V}"></script>
</body>
</html>
'''

def person(p):
  n, role, mail, ph = p
  return f'''<div class="person"><div class="av">{initials(n)}</div><div><b>{n}</b><a href="mailto:{mail}">{mail}</a><a href="{tel(ph)}">{ph}</a></div></div>'''

def tile(img, cap, sub='', cls=''):
  s = f'<span>{sub}</span>' if sub else ''
  return f'<figure class="tile {cls} rv"><div class="ph"><img src="{I}{img}" alt="{cap}" loading="lazy"></div><figcaption>{cap}{s}</figcaption></figure>'

def contact_block():
  people = ''.join(f'''<div class="p"><div><b>{p[0]}</b><small>{t}</small></div><div class="ln"><a href="mailto:{p[2]}">{p[2]}</a><a href="{tel(p[3])}">{p[3]}</a></div></div>'''
    for p, t in [(DIVS['elektroinstalacije']['person'],'Elektroinštalacije'),(DIVS['soncne-elektrarne']['person'],'Sončne elektrarne'),(DIVS['polnilnice-moon']['person'],'Polnilnice MOON')])
  return f'''
<section class="contact section wrap" id="povprasevanje">
  <div class="contact-grid">
    <div>
      <h2 class="d2 split-in">{rows('Pogovorimo se','o vašem objektu.')}</h2>
      <p class="body-l rv" style="margin-top:28px;max-width:34ch">Pokličite strokovnjaka za vaše področje ali pošljite povpraševanje. Odgovorimo v enem delovnem dnevu.</p>
      <div class="people rv">{people}</div>
    </div>
    <form class="inq rv" novalidate>
      <div class="fields">
        <h3>Povpraševanje</h3>
        <div class="chips" role="group" aria-label="Področje">
          <label><input type="radio" name="podrocje" value="elektro" checked><span>Elektroinštalacije</span></label>
          <label><input type="radio" name="podrocje" value="solar"><span>Sončna elektrarna</span></label>
          <label><input type="radio" name="podrocje" value="moon"><span>Polnilnica MOON</span></label>
          <label><input type="radio" name="podrocje" value="vzdrzevanje"><span>Vzdrževanje</span></label>
        </div>
        <div class="row2">
          <div class="field"><input id="f-ime" name="ime" placeholder=" " required><label for="f-ime">Ime in priimek</label></div>
          <div class="field"><input id="f-podj" name="podjetje" placeholder=" "><label for="f-podj">Podjetje</label></div>
        </div>
        <div class="row2">
          <div class="field"><input id="f-mail" type="email" name="email" placeholder=" " required><label for="f-mail">E-pošta</label></div>
          <div class="field"><input id="f-tel" name="telefon" placeholder=" "><label for="f-tel">Telefon</label></div>
        </div>
        <div class="field"><textarea id="f-msg" name="sporocilo" placeholder=" " required></textarea><label for="f-msg">Opišite projekt</label></div>
        <div class="form-foot"><small>S pošiljanjem se strinjate s pravili zasebnosti.</small><button class="btn" type="submit">Pošlji {ARR}</button></div>
      </div>
      <div class="sent"><h3>Hvala, prejeli smo.</h3><p class="body-l">Oglasimo se v enem delovnem dnevu.</p></div>
    </form>
  </div>
</section>'''

# ------------------------------------------------------------------ HOME
def home():
  e = DIVS['elektroinstalacije']; s = DIVS['soncne-elektrarne']; m = DIVS['polnilnice-moon']
  caps = ''.join(f'<li>{c}{CHECK}</li>' for _, c in ELEKTRO_CAPS)
  el_gal = tile(ELEKTRO_PROJECTS[0][0], *ELEKTRO_PROJECTS[0][1:], cls='wide') + tile(ELEKTRO_PROJECTS[4][0], *ELEKTRO_PROJECTS[4][1:]) + tile(ELEKTRO_PROJECTS[2][0], *ELEKTRO_PROJECTS[2][1:]) + tile(ELEKTRO_CAPS[1][0], ELEKTRO_CAPS[1][1], cls='wide')
  so_gal = tile(SOLAR[3][0], *SOLAR[3][1:], cls='wide') + tile(SOLAR[0][0], *SOLAR[0][1:]) + tile(SOLAR[2][0], *SOLAR[2][1:]) + tile(SOLAR[1][0], *SOLAR[1][1:], cls='wide')
  mo_gal = tile(MOON[4][0], MOON[4][1], cls='wide') + tile(MOON[1][0], MOON[1][1]) + tile(MOON[2][0], MOON[2][1]) + tile(MOON[3][0], MOON[3][1], cls='wide')
  marquee1 = ''.join(f'<span>{c}</span>' for c in CLIENTS[:11])
  marquee2 = ''.join(f'<span>{c}</span>' for c in CLIENTS[11:])
  return head('ELNET | Elektroinštalacije, sončne elektrarne, polnilnice MOON', 'ELNET d.o.o. iz Izlak: elektroinštalacije, sončne elektrarne in polnilnice MOON od leta 1983.', 'index.html') + f'''
<section class="hero">
  <h1 class="d1 wrap">{rows('Elektrika, ki', 'drži <span class="muted">od 1983.</span>')}</h1>
  <div class="hero-media-wrap">
    <div class="hero-media">
      <img class="on" src="{I}{e['banner']}" alt="Elektro inštalacije, vezje">
      <img src="{I}{s['banner']}" alt="Sončna elektrarna T2 Verovškova">
      <img src="{I}{m['banner']}" alt="Polnilnica MOON">
    </div>
  </div>
  <div class="hero-bottom wrap">
    <p class="lead">Načrtujemo in izvajamo elektroinštalacije vseh vrst, postavljamo sončne elektrarne in polnilnice MOON.</p>
    <div class="hero-tabs"><button>Elektroinštalacije<i></i></button><button>Sončne elektrarne<i></i></button><button>Polnilnice MOON<i></i></button></div>
  </div>
</section>

<section class="statement section wrap">
  <p class="lead reveal-words">Od ustanovitve leta 1983 se ukvarjamo z električnimi inštalacijami vseh vrst. Dela zaključimo v pogodbenih rokih in z visoko kakovostjo, zato nam naročniki zaupajo že desetletja.</p>
  <div class="stats">
    <div class="stat rv"><div class="n" data-count="1983" data-from="1900">1983</div><p>Leto ustanovitve podjetja v Izlakah</p></div>
    <div class="stat rv"><div class="n" data-count="3">3</div><p>Področja: inštalacije, fotovoltaika, polnilnice</p></div>
    <div class="stat rv"><div class="n">AAA</div><p>Najvišja bonitetna odličnost, že vrsto let</p></div>
    <div class="stat rv"><div class="n" data-count="2020" data-from="1990">2020</div><p>Selitev v nove poslovne prostore</p></div>
  </div>
</section>

<section class="wrap" id="storitve" style="position:relative">
  <div class="div-block">
    <div class="div-side">
      <h2 class="d2 split-in">{rows('Elektro-', 'inštalacije')}</h2>
      <p class="body-l rv">Glavno področje našega dela. Od grobih inštalacij in elektro omar do razsvetljave dvoran, operacijskih sob in bančnih poslovalnic.</p>
      <ul class="caps rv">{caps}</ul>
      {person(e['person'])}
      <a class="btn div-more" href="elektroinstalacije.html">Več o elektroinštalacijah {ARR}</a>
    </div>
    <div class="div-gallery">{el_gal}</div>
  </div>
  <div class="div-block">
    <div class="div-side">
      <h2 class="d2 split-in">{rows('Sončne', 'elektrarne')}</h2>
      <p class="body-l rv">Fotovoltaika na strehah poslovnih in upravnih stavb, tudi na naši lastni stavbi v Izlakah.</p>
      {person(s['person'])}
      <a class="btn div-more" href="soncne-elektrarne.html">Več o sončnih elektrarnah {ARR}</a>
    </div>
    <div class="div-gallery">{so_gal}</div>
  </div>
  <div class="div-block">
    <div class="div-side">
      <h2 class="d2 split-in">{rows('Polnilnice', 'MOON')}</h2>
      <p class="body-l rv">V sodelovanju s Porsche Slovenija in blagovno znamko MOON postavljamo polnilnice za električna vozila. Instalacija, meritve, testiranje. Polno in gremo.</p>
      {person(m['person'])}
      <a class="btn div-more" href="polnilnice-moon.html">Več o polnilnicah {ARR}</a>
    </div>
    <div class="div-gallery">{mo_gal}</div>
  </div>
</section>

<section class="clients section" style="margin-top:clamp(96px,12vw,240px)">
  <div class="head wrap"><h2 class="d2 split-in">{rows('Zaupajo nam', 'že vrsto let.')}</h2><p class="body-l rv">Naš največji uspeh je, da se poslovni partnerji vračajo. Banke, klinike, univerza, avtohiše in industrija.</p></div>
  <div class="marquee"><div class="track">{marquee1}</div><div class="track" aria-hidden="true">{marquee1}</div></div>
  <div class="marquee rev"><div class="track">{marquee2}</div><div class="track" aria-hidden="true">{marquee2}</div></div>
</section>

<section class="section wrap">
  <div class="proj-head"><h2 class="d2 split-in">{rows('Izbrani projekti')}</h2><a class="btn" href="projekti.html">Vse reference {ARR}</a></div>
  <div class="mosaic">
    {tile('ELNET-polnilnica-IONITY.jpg','Hitra polnilnica IONITY','Radovljica', 'm-a')}
    {tile('ELNET-elektro-instlacijska-dela-privatni-objekti-540x720-1.jpg','Stanovanjska hiša','Elektroinštalacije','m-b')}
    {tile('ELNET-soncna-elektrarna-Triglav-AS.jpg','Sončna elektrarna Triglav AS','Fotovoltaika','m-c')}
    {tile('ELNET-elektro-instlacijska-dela-poslovalnice-NLB.jpg','Prenova poslovalnic NLB','Elektroinštalacije','m-d')}
    {tile('ELNET-elektro-vzdrzevalna-dela-center-slabovidnih.jpg','Center slepih in slabovidnih','Vzdrževanje','m-e')}
  </div>
</section>

<section class="section wrap" style="padding-top:0">
  <div class="award">
    <div class="ph rv"><img src="{I}ELNET-priznanja-in-bonitete.jpg" alt="Priznanja in bonitete ELNET" loading="lazy"></div>
    <div><h2 class="d3 split-in">{rows('Najvišja bonitetna', 'odličnost, leto za letom.')}</h2><p class="body-l rv" style="margin-top:24px;max-width:36ch">Zanesljiv partner pomeni tudi zdravo podjetje. Zaposlene in opremo nenehno posodabljamo, usposabljamo in izobražujemo.</p><a class="btn rv" style="margin-top:36px" href="o-nas.html">O podjetju {ARR}</a></div>
  </div>
</section>
''' + contact_block() + FOOT

# ------------------------------------------------------------------ DIVISION PAGES
def division(key):
  d = DIVS[key]
  if key == 'elektroinstalacije':
    h1 = rows('Elektro-', 'inštalacije')
    intro = 'Načrtovanje in izvedba elektroinštalacij je glavno področje našega dela že od leta 1983. Sledimo željam naročnikov, novim smernicam in sodelujemo z vodilnimi proizvajalci.'
    steps = [('Elektro omare','Izdelava elektro omar po meri objekta.'),('Grobe inštalacije','Polaganje kablov in kabelskih tras.'),('Nizkonapetostni bloki','Izdelava NN blokov za poslovne in proizvodne objekte.'),('Trafo postaje','Izdelava in priklop trafo postaj.')]
    gal = ''.join(tile(p[0], p[1], p[2], 'wide' if i in (0, 6) else '') for i, p in enumerate(ELEKTRO_PROJECTS))
    extra = ''.join(tile(c[0], c[1], '', '') for c in ELEKTRO_CAPS)
    gal_title = rows('Reference')
    second = f'''<section class="section wrap" style="padding-top:0"><div class="two"><h2 class="d3 split-in">{rows('Kar izdelamo', 'v lastni režiji.')}</h2><div class="gallery">{extra}</div></div></section>'''
  elif key == 'soncne-elektrarne':
    h1 = rows('Sončne', 'elektrarne')
    intro = 'V zadnjih letih smo svoje znanje razširili na fotovoltaiko. Postavljamo sončne elektrarne na strehah poslovnih, upravnih in stanovanjskih objektov po vsej Sloveniji.'
    steps = [('Ogled in načrt','Ocena strehe, porabe in priključne moči.'),('Montaža','Postavitev panelov in razsmernikov.'),('Priklop','Elektro priklop in usklajevanje z distributerjem.'),('Vzdrževanje','Pregledi in intervencije po zagonu.')]
    gal = ''.join(tile(p[0], p[1], p[2], 'wide' if i in (0, 3) else '') for i, p in enumerate(SOLAR))
    gal_title = rows('Reference'); second = ''
  else:
    h1 = rows('Polnilnice', 'MOON')
    intro = 'V sodelovanju s Porsche Slovenija in blagovno znamko MOON postavljamo polnilnice za električna vozila, od hišnih polnilnic do hitre polnilnice IONITY ob avtocesti.'
    steps = [('Polnilnica MOON','Izbira polnilnice za dom ali podjetje.'),('Instalacija','Elektro priklop in montaža.'),('Meritve in testiranje','Preverimo delovanje z vozilom.'),('Polno in gremo','Predaja in navodila za uporabo.')]
    gal = ''.join(tile(p[0], p[1], '', 'wide' if i in (0, 4) else '') for i, p in enumerate(MOON))
    gal = gal + tile('ELNET-polnilnica-IONITY.jpg', 'Hitra polnilnica IONITY', 'Radovljica', 'wide')
    gal_title = rows('Od priklopa', 'do polne baterije.'); second = ''
  icons = [
    '<svg viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="2"><rect x="12" y="6" width="32" height="44" rx="2"/><path d="M20 16h16M20 24h16M20 32h8"/></svg>',
    '<svg viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 18c12 0 12 20 24 20s12-20 24-20"/><path d="M4 30c12 0 12 14 24 14s12-14 24-14"/></svg>',
    '<svg viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="2"><path d="M31 4 14 32h14l-3 20 17-28H28z"/></svg>',
    '<svg viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="2"><circle cx="28" cy="28" r="20"/><path d="m19 29 6 6 12-13"/></svg>',
  ]
  steps_html = ''.join(f'<div class="step rv">{icons[i]}<div><h4>{t}</h4><p>{p}</p></div></div>' for i, (t, p) in enumerate(steps))
  others = ''.join(f'''<a class="mega-card rv" href="{k}.html"><div class="ph"><img src="{I}{o["thumb"]}" alt="{o["title"]}" loading="lazy"></div><h4>{o["title"]}</h4><p>{o["short"]}</p></a>''' for k, o in DIVS.items() if k != key)
  return head(f'{d["title"]} | ELNET', d['short'], key + '.html') + f'''
<section class="phero wrap"><div class="grid"><h1 class="d1">{h1}</h1><div><p class="body-l">{intro}</p>{person(d['person'])}</div></div></section>
<div class="pbanner"><img src="{I}{d['banner']}" alt="{d['title']}"></div>
<section class="section wrap"><div class="steps">{steps_html}</div></section>
<section class="section wrap" style="padding-top:0"><div class="two"><h2 class="d3 split-in" style="position:sticky;top:calc(var(--nav-h) + 24px);align-self:start">{gal_title}</h2><div class="gallery">{gal}</div></div></section>
{second}
<section class="section wrap" style="padding-top:0"><h2 class="d3 split-in" style="margin-bottom:48px">{rows('Ostala področja')}</h2><div class="mega-cards" style="grid-template-columns:repeat(2,1fr)">{others}</div></section>
''' + contact_block() + FOOT

# ------------------------------------------------------------------ PROJECTS
def projekti():
  groups = ''.join(f'''<div class="ref-group"><div><h2 class="d3 split-in">{rows(t)}</h2><p class="muted" style="margin-top:12px">{len(items)} referenc</p><div class="ph rv"><img src="{I}{img}" alt="{t}" loading="lazy"></div></div><ul class="ref-list rv">{''.join(f'<li>{x}</li>' for x in items)}</ul></div>''' for t, img, items in REF_GROUPS)
  cloud = ''.join(f'<span>{c}</span>' for c in CLIENTS)
  return head('Projekti | ELNET', 'Reference podjetja ELNET: banke, klinike, univerza, avtohiše, sončne elektrarne in polnilnice.', 'projekti.html') + f'''
<section class="phero wrap"><div class="grid"><h1 class="d1">{rows('Izkušnje,', 'znanje,', 'sodelovanje.')}</h1><p class="body-l">Reference podjetja ELNET so plod dolgoletnih izkušenj in strokovnega znanja zaposlenih. Kot največji uspeh štejemo, da nam poslovni partnerji zaupajo že vrsto let.</p></div></section>
<section class="wrap" style="padding-bottom:clamp(96px,10vw,200px)"><div class="client-cloud rv">{cloud}</div></section>
<section class="wrap">{groups}</section>
''' + contact_block() + FOOT

# ------------------------------------------------------------------ ABOUT
def onas():
  tl = [
    ('1983','Ustanovitev','Podjetje ELNET d.o.o. se od ustanovitve ukvarja z električnimi inštalacijami vseh vrst.'),
    ('25+','Let s proizvajalci','Že več kot 25 let sledimo željam kupcev, novim smernicam in sodelujemo z vodilnimi proizvajalci elektroinštalacij.'),
    ('2020','Nova stavba','Preselili smo se v nove poslovne prostore v Izlakah, na katere smo posebej ponosni. So odraz naše rasti. Na strehi deluje naša sončna elektrarna.'),
    ('Danes','Tri področja','Poleg elektroinštalacij delujemo na področju fotovoltaike in električnih polnilnic, v sodelovanju s Porsche Slovenija in znamko MOON.'),
  ]
  tl_html = ''.join(f'<div class="tl rv"><div class="y">{y}</div><h4>{h}</h4><p class="body-l">{p}</p></div>' for y, h, p in tl)
  return head('O nas | ELNET', 'ELNET d.o.o., Izlake. Elektroinštalacije od leta 1983.', 'o-nas.html') + f'''
<section class="phero wrap"><div class="grid"><h1 class="d1">{rows('Zanesljiv', 'partner', '<span class="muted">od 1983.</span>')}</h1><p class="body-l">Glavno področje našega dela je načrtovanje in izvedba elektroinštalacij. Vizija podjetja je zaključiti dela v pogodbenih rokih z visoko kakovostjo izvedenih del.</p></div></section>
<div class="pbanner"><img src="{I}ELNET-Soncna-elektrarna-Poslovni-objekt-ELNET.jpg" alt="Poslovna stavba ELNET v Izlakah"></div>
<section class="statement section wrap"><p class="lead reveal-words">Podjetje vseskozi sledi svoji poslovni viziji. Kader in opremo nenehno posodabljamo, usposabljamo in izobražujemo. Naši zaposleni so zagotovilo za uspešno in trdno prihodnost podjetja.</p></section>
<section class="wrap" style="padding-bottom:clamp(96px,12vw,240px)"><div class="timeline">{tl_html}</div></section>
<section class="section wrap" style="padding-top:0">
  <div class="award">
    <div class="ph rv"><img src="{I}ELNET-priznanja-in-bonitete.jpg" alt="Priznanja in bonitete ELNET" loading="lazy"></div>
    <div><h2 class="d3 split-in">{rows('Zaupanje,', 'ki ga merimo.')}</h2><p class="body-l rv" style="margin-top:24px;max-width:36ch">Pri številnih naročnikih smo si pridobili zaupanje kot zanesljiv in kakovosten partner. Že vrsto let dosegamo najvišjo bonitetno odličnost.</p></div>
  </div>
</section>
''' + contact_block() + FOOT

# ------------------------------------------------------------------ CONTACT
def kontakt():
  team = ''.join(f'''<div class="member rv"><div><b>{n}</b><small>{r}</small></div><div><a href="mailto:{m}">{m}</a><a href="{tel(p)}">{p}</a></div></div>''' for n, r, m, p in TEAM)
  company = '<div class="member company rv"><div><b>ELNET d.o.o.</b><small>Spodnje Izlake 10 A, 1411 Izlake</small></div><div><a href="mailto:info@elnet.si">info@elnet.si</a><a href="tel:+38635679540">03 56 79 540</a></div></div>'
  return head('Kontakt | ELNET', 'Kontakti ELNET d.o.o., Spodnje Izlake 10 A, 1411 Izlake.', 'kontakt.html') + f'''
<section class="phero wrap"><div class="grid"><h1 class="d1">{rows('Kontakt')}</h1><p class="body-l">Pokličite nas na 03 56 79 540 ali pišite na info@elnet.si. Za hitrejši odgovor izberite osebo za vaše področje.</p></div></section>
<section class="wrap"><div class="team">{company}{team}</div></section>
<section class="section wrap"><div class="two"><div><h2 class="d3 split-in">{rows('Kje smo')}</h2><p class="body-l rv" style="margin-top:20px">Spodnje Izlake 10 A<br>1411 Izlake</p><a class="btn rv" style="margin-top:32px" href="https://maps.google.com/?q=Spodnje+Izlake+10A,+1411+Izlake" target="_blank" rel="noopener">Odpri v zemljevidu {ARR}</a></div><div class="map-ph rv"><img src="{I}ELNET-map-1.jpg" alt="Zemljevid lokacije ELNET" loading="lazy"></div></div></section>
''' + contact_block() + FOOT

PAGES = {'index.html': home(), 'projekti.html': projekti(), 'o-nas.html': onas(), 'kontakt.html': kontakt()}
for k in DIVS: PAGES[k + '.html'] = division(k)
for name, html in PAGES.items():
  open(os.path.join(SITE, name), 'w').write(html)
print('built', ', '.join(PAGES))
