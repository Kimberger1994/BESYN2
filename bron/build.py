#!/usr/bin/env python3
"""Bouwt de statische pagina's voor www.besyn.nl.

Gebruik (in de map besyn-website):  python3 bron/build.py

- Inhoud per pagina staat in bron/pages/*.html.
- Header, footer, SEO-metadata, gestructureerde data (schema.org), sitemap.xml,
  llms.txt en de veelgestelde vragen (FAQ) staan in dit bestand.
- Pas een FAQ-antwoord hier aan: het verschijnt dan automatisch op de FAQ-pagina,
  op de dienstpagina's, in de gestructureerde data en in llms.txt.
"""
import json, os, html, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "site")      # hier schrijft het script de website naartoe
SRC = os.path.join(HERE, "pages")            # inhoud per pagina (zonder header/footer)
SITE = "https://www.besyn.nl"
OG = SITE + "/images/og-besyn.jpg"
LINKEDIN = "https://www.linkedin.com/in/kimbergerexitready/"
HUMA = "https://www.huma-advisory.com/"
LASTMOD = "2026-10-20"

ORG_ID = SITE + "/#organisatie"
PERSON_ID = SITE + "/kim-berger/#persoon"

NAV = [
    ("/executive-coaching/", "Executive coaching"),
    ("/zakelijke-mediation/", "Mediation"),
    ("/kim-berger/", "Over Kim"),
    ("/veelgestelde-vragen/", "Veelgestelde vragen"),
]

ORG = {
    "@type": ["ProfessionalService", "Organization"],
    "@id": ORG_ID,
    "name": "BESYN",
    "alternateName": ["BESYN Coaching, Strategie en Mediation", "BESYN executive coaching en mediation"],
    "description": "BESYN is een praktijk voor executive coaching en zakelijke mediation in Utrecht, opgericht door Kim Berger. BESYN begeleidt ondernemers, DGA's en directies bij leiderschap, besluitvorming en samenwerking in de top.",
    "slogan": "Mens, structuur, strategie – in synergie",
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "url": SITE + "/images/besyn-logo-schema.png", "width": 600, "height": 200},
    "image": OG,
    "email": "k.berger@huma-advisory.com",
    "telephone": "+31620050351",
    "address": {"@type": "PostalAddress", "addressLocality": "Utrecht", "addressRegion": "Utrecht", "addressCountry": "NL"},
    "areaServed": [{"@type": "City", "name": "Utrecht"}, {"@type": "AdministrativeArea", "name": "Randstad"}, {"@type": "Country", "name": "Nederland"}],
    "founder": {"@id": PERSON_ID},
    "employee": {"@id": PERSON_ID},
    "legalName": "Berger Advisory Holding B.V.",
    "vatID": "NL869238772B01",
    "identifier": {"@type": "PropertyValue", "propertyID": "KvK-nummer", "value": "42003724"},
    "knowsAbout": ["Executive coaching", "Leiderschapscoaching", "Teamcoaching", "MT-coaching",
                   "Zakelijke mediation", "Conflictbemiddeling", "Bedrijfsopvolging", "Fusies en overnames"],
    "knowsLanguage": "nl",
    "contactPoint": {"@type": "ContactPoint", "contactType": "kennismaking", "email": "k.berger@huma-advisory.com",
                     "telephone": "+31620050351", "availableLanguage": ["nl", "en"], "areaServed": "NL"},
    "makesOffer": [
        {"@type": "Offer", "itemOffered": {"@id": SITE + "/executive-coaching/#dienst"}},
        {"@type": "Offer", "itemOffered": {"@id": SITE + "/zakelijke-mediation/#dienst"}},
    ],
    "sameAs": [LINKEDIN],
}
PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": "Kim Berger",
    "givenName": "Kim",
    "familyName": "Berger",
    "jobTitle": "Executive coach en mediator",
    "description": "Kim Berger (MSc Bedrijfskunde) is executive coach en mediator in Utrecht, oprichter van BESYN en partner bij HUMA Advisory, met acht jaar ervaring in fusies en overnames en strategie. Als director bij Exit Ready begeleidde zij ondernemers bij bedrijfsoverdracht, loslaten en generatiewissels.",
    "url": SITE + "/kim-berger/",
    "image": SITE + "/images/kim-berger-portret.jpg",
    "email": "k.berger@huma-advisory.com",
    "worksFor": [{"@id": ORG_ID}, {"@type": "Organization", "name": "HUMA Advisory", "url": HUMA}],
    "hasOccupation": {"@type": "Occupation", "name": "Executive coach en mediator",
                      "occupationLocation": {"@type": "City", "name": "Utrecht"}},
    "knowsAbout": ["Executive coaching", "Leiderschap", "Besluitvorming", "Zakelijke mediation",
                   "Fusies en overnames", "Bedrijfsopvolging", "Generatiewissel", "Strategie", "Governance",
                   "Teamcoaching", "Turnaround", "M&A-voorbereiding", "Deal readiness", "Synergieonderzoek",
                   "Marktanalyse", "Concurrentieanalyse", "Waardeanalyse", "Businessplannen", "Positionering"],
    "knowsLanguage": ["nl", "en"],
    "sameAs": [LINKEDIN],
}
WEBSITE = {
    "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "BESYN",
    "inLanguage": "nl-NL", "publisher": {"@id": ORG_ID},
}

# ---------- Veelgestelde vragen (bron voor FAQ-pagina, dienstpagina's en schema) ----------
FAQ = [
    ("Executive coaching", "executive-coaching", [
        ("Wat is executive coaching?",
         "Executive coaching is persoonlijke, vertrouwelijke begeleiding van leiders met eindverantwoordelijkheid, zoals DGA's, directeuren en MT-leden. Het richt zich op concrete vraagstukken uit de praktijk: leiderschap, besluitvorming, samenwerking in de top en rolverandering. Anders dan bij een training werk je aan je eigen situatie en doelen."),
        ("Voor wie is executive coaching bij BESYN bedoeld?",
         "Voor ondernemers, DGA's, directeuren, bestuurders, partners en MT-leden, en voor beoogde opvolgers. Kim coacht individueel en werkt ook met managementteams als geheel."),
        ("Met welke vraagstukken kan ik bij BESYN terecht?",
         "Onder meer met vragen over impact en positie als leider, besluitvorming onder druk, rolverandering bij overname, fusie of opvolging, afstand nemen van het eigen bedrijf, generatiewissels in familiebedrijven, spanningen tussen aandeelhouders en directie, belastbaarheid en de effectiviteit van het managementteam."),
        ("Hoe ziet een coachtraject eruit?",
         "Na een vrijblijvende kennismaking leg je in een intake doelen en succescriteria vast. Een traject start doorgaans met vier sessies van ongeveer anderhalf uur, in overleg om de twee à vier weken. Daarna evalueer je het resultaat en bepaal je samen met Kim Berger of en hoe het traject verdergaat."),
        ("Wat levert executive coaching op?",
         "Meer helderheid over je rol en koers, beter onderbouwde besluiten, meer impact als leider en een team dat beter samenwerkt. Welke resultaten passend zijn, wordt bij de start vastgelegd en aan het eind getoetst."),
        ("Welke methoden gebruikt Kim Berger?",
         "Kim Berger combineert een zakelijke, doelgerichte aanpak met beproefde methoden zoals Rationeel-Emotieve Therapie (RET), Gestalt, voice dialogue, ervaringsgerichte werkvormen en rollenspel. De aanpak wordt afgestemd op je vraag en je stijl."),
        ("Wat is het verschil tussen coaching en therapie?",
         "Coaching richt zich op je functioneren en ontwikkeling als leider. Persoonlijke onderwerpen komen soms aan bod, omdat werk en leven niet los van elkaar staan, maar coaching is geen behandeling. Blijkt dat andere hulp beter past, bijvoorbeeld therapie, dan bespreekt Kim Berger dat open met je en denkt zij mee over passende begeleiding."),
    ]),
    ("Zakelijke mediation", "zakelijke-mediation", [
        ("Wat is zakelijke mediation?",
         "Zakelijke mediation is een vertrouwelijke manier om een conflict binnen of tussen ondernemingen op te lossen met hulp van een neutrale bemiddelaar. De partijen zoeken zelf naar afspraken waarmee zij verder kunnen, in plaats van dat een rechter beslist."),
        ("Bij welke conflicten helpt zakelijke mediation?",
         "Bij conflicten tussen aandeelhouders, in de directie of binnen het managementteam, tussen vennoten, in familiebedrijven en rond opvolging, bij samenwerking na een fusie of overname, en bij arbeidsconflicten op sleutelposities."),
        ("Hoe verloopt een mediation bij BESYN?",
         "Een mediation begint met een kennismaking, gevolgd door individuele gesprekken met elke partij. Daarna volgen gezamenlijke sessies, waarin partijen van posities naar belangen en oplossingen werken. De afspraken worden vastgelegd, met een vervolgmoment om te toetsen of ze werken."),
        ("Is mediation vertrouwelijk?",
         "Ja. Wat in de mediation wordt besproken, blijft vertrouwelijk. Dat wordt vooraf schriftelijk vastgelegd met alle betrokkenen."),
        ("Wanneer kies je voor mediation in plaats van een juridische procedure?",
         "Mediation past vooral wanneer partijen de relatie of samenwerking willen behouden, zelf invloed willen houden op de uitkomst en de zaak vertrouwelijk willen houden. Speelt er ook een juridische kwestie, dan kan juridische expertise worden betrokken, bijvoorbeeld via HUMA Advisory."),
    ]),
    ("Praktisch", "praktisch", [
        ("Wat kost executive coaching of mediation bij BESYN?",
         "Elk traject is maatwerk. Na de kennismaking ontvang je een voorstel dat past bij je vraag; werken op basis van een uurtarief is ook mogelijk. Alle tarieven zijn exclusief btw."),
        ("Kan mijn organisatie de kosten betalen?",
         "Ja, dat is gebruikelijk. Doelen en voortgang worden dan desgewenst op hoofdlijnen afgestemd met de opdrachtgever. De inhoud van de gesprekken blijft altijd vertrouwelijk."),
        ("Waar vinden de gesprekken plaats?",
         "In Utrecht, op jouw locatie of online. BESYN werkt voor ondernemingen in Utrecht, de Randstad en de rest van Nederland."),
        ("Hoe wordt vertrouwelijkheid gewaarborgd?",
         "Alles wat je deelt is vertrouwelijk en wordt nooit zonder jouw toestemming gedeeld, ook niet met de opdrachtgever. Kim werkt volgens een strikte beroepscode en gaat zorgvuldig om met persoonsgegevens, zoals beschreven in de privacyverklaring."),
        ("Hoe plan ik een kennismaking?",
         "Via het contactformulier op deze website, per e-mail via k.berger@huma-advisory.com of telefonisch via 06 2005 0351. Kim Berger neemt persoonlijk contact met je op."),
    ]),
    ("Over BESYN en Kim Berger", "over-besyn", [
        ("Wat is BESYN?",
         "BESYN is een praktijk voor executive coaching en zakelijke mediation in Utrecht, opgericht door Kim Berger. BESYN begeleidt ondernemers, DGA's en directies bij leiderschap, besluitvorming en samenwerking, in het bijzonder rond groei, overname en opvolging."),
        ("Wie is Kim Berger?",
         "Kim Berger (MSc Bedrijfskunde) is executive coach en mediator en de oprichter van BESYN. Zij heeft acht jaar ervaring in fusies en overnames en strategie. Als director bij Exit Ready begeleidde zij veel ondernemers bij het loslaten van hun bedrijf en bij generatiewissels. Zij is partner bij HUMA Advisory."),
        ("Hoe werkt Kim Berger als coach?",
         "Direct, nuchter en betrokken. Kim stelt gerichte vragen, benoemt wat zij ziet en laat je nieuwe situaties ook ervaren en oefenen, bijvoorbeeld in een rollenspel. Ze werkt methodisch en doelgericht, en stemt haar aanpak af op je doelen en je manier van denken. Een klimaat van vertrouwen is daarbij de basis."),
        ("Wat is de relatie tussen BESYN en HUMA Advisory?",
         "Kim Berger is partner bij HUMA Advisory, een onafhankelijk adviesbureau in Utrecht voor leiderschap, governance en gedrag rond transacties. Speelt je vraagstuk ook op organisatieniveau, dan kan Kim de expertise van HUMA betrekken. Coaching en mediation zijn ook los af te nemen."),
    ]),
]
FAQ_INDEX = {q: a for _, _, items in FAQ for q, a in items}
FAQ_HOME = ["Wat kost executive coaching of mediation bij BESYN?", "Kan mijn organisatie de kosten betalen?",
            "Waar vinden de gesprekken plaats?"]
FAQ_COACHING = ["Wat is het verschil tussen coaching en therapie?", "Wat kost executive coaching of mediation bij BESYN?",
                "Kan mijn organisatie de kosten betalen?", "Hoe wordt vertrouwelijkheid gewaarborgd?"]
FAQ_MEDIATION = ["Wanneer kies je voor mediation in plaats van een juridische procedure?",
                 "Wat kost executive coaching of mediation bij BESYN?", "Waar vinden de gesprekken plaats?"]

PAGES = [
    dict(src="home.html", out="index.html", path="/", nav=None,
         title="Executive coaching & zakelijke mediation Utrecht | BESYN",
         desc="BESYN begeleidt ondernemers, DGA's en directies met executive coaching en zakelijke mediation. Opgericht door Kim Berger, Utrecht. Plan een kennismaking.",
         kind="home"),
    dict(src="coaching.html", out="executive-coaching/index.html", path="/executive-coaching/", nav="/executive-coaching/",
         title="Executive coaching voor DGA's en directies | BESYN Utrecht",
         desc="Executive coaching voor DGA's, directeuren en MT's: leiderschap, besluitvorming en rolverandering bij overname of opvolging. In Utrecht en online.",
         crumb="Executive coaching", kind="service", service="Executive coaching", faqlist=FAQ_COACHING),
    dict(src="mediation.html", out="zakelijke-mediation/index.html", path="/zakelijke-mediation/", nav="/zakelijke-mediation/",
         title="Zakelijke mediation bij conflicten in de top | BESYN",
         desc="Zakelijke mediation bij conflicten tussen aandeelhouders, in de directie, het MT of familiebedrijven. Neutraal, vertrouwelijk en met kennis van governance.",
         crumb="Zakelijke mediation", kind="service", service="Zakelijke mediation", faqlist=FAQ_MEDIATION),
    dict(src="over-kim.html", out="kim-berger/index.html", path="/kim-berger/", nav="/kim-berger/",
         title="Kim Berger – executive coach en mediator | BESYN",
         desc="Kim Berger, executive coach en mediator in Utrecht: direct, nuchter en betrokken, met acht jaar M&A-ervaring en veel levenservaring. Lees haar visie en aanpak.",
         crumb="Kim Berger", kind="profile", ogtype="profile"),
    dict(src="faq.html", out="veelgestelde-vragen/index.html", path="/veelgestelde-vragen/", nav="/veelgestelde-vragen/",
         title="Veelgestelde vragen over coaching en mediation | BESYN",
         desc="Antwoorden op veelgestelde vragen over executive coaching, zakelijke mediation, kosten, vertrouwelijkheid en werkwijze van BESYN in Utrecht.",
         crumb="Veelgestelde vragen", kind="faq"),
    dict(src="contact.html", out="contact/index.html", path="/contact/", nav="/contact/",
         title="Contact en kennismaking | BESYN Utrecht",
         desc="Plan een vrijblijvende kennismaking met Kim Berger over executive coaching of zakelijke mediation. Bel 06 2005 0351 of stuur een bericht.",
         crumb="Contact", kind="contact"),
    dict(src="bedankt.html", out="contact/bedankt/index.html", path="/contact/bedankt/", nav="/contact/",
         title="Bedankt voor je bericht | BESYN", desc="Je bericht is verzonden.", noindex=True),
    dict(src="privacyverklaring.html", out="privacyverklaring/index.html", path="/privacyverklaring/", nav=None,
         title="Privacyverklaring | BESYN",
         desc="Hoe BESYN (Kim Berger) omgaat met persoonsgegevens van cliënten en websitebezoekers.",
         crumb="Privacyverklaring"),
    dict(src="algemene-voorwaarden.html", out="algemene-voorwaarden/index.html", path="/algemene-voorwaarden/", nav=None,
         title="Algemene voorwaarden | BESYN",
         desc="Algemene voorwaarden voor executive coaching en zakelijke mediation door BESYN.",
         crumb="Algemene voorwaarden"),
    dict(src="cookiebeleid.html", out="cookiebeleid/index.html", path="/cookiebeleid/", nav=None,
         title="Cookiebeleid | BESYN",
         desc="De website van BESYN plaatst geen tracking- of marketingcookies.",
         crumb="Cookiebeleid"),
    dict(src="404.html", out="404.html", path="/404.html", nav=None,
         title="Pagina niet gevonden | BESYN", desc="Deze pagina bestaat niet (meer).", noindex=True),
]


def asset_version(rel):
    """Korte vingerafdruk van een bestand: verandert de opmaak, dan laadt elke browser direct de nieuwe versie."""
    with open(os.path.join(ROOT, rel), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]


def version_images(text):
    """Zet een versienummer achter elke foto, zodat een vervangen foto direct overal zichtbaar is."""
    def repl(m):
        rel = m.group(2).lstrip("/")
        return f'{m.group(1)}="{m.group(2)}?v={asset_version(rel)}"'
    return re.sub(r'\b(src)="(/images/[^"?]+)"', repl, text)


def esc(s):
    return html.escape(s, quote=True)


def slug(s):
    s = s.lower()
    for a, b in (("ë", "e"), ("é", "e"), ("'", ""), ("?", "")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


NAV_SHORT = {"/executive-coaching/": "Coaching", "/veelgestelde-vragen/": "FAQ"}


def header(active):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        short = NAV_SHORT.get(href)
        text = (f'<span class="lbl-long">{label}</span><span class="lbl-short">{short}</span>'
                if short else label)
        items.append(f'<li><a class="nav__link" href="{href}"{cur}>{text}</a></li>')
    cur = ' aria-current="page"' if active == "/contact/" else ""
    return f'''<a class="skip-link" href="#main">Naar de inhoud</a>
<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="BESYN, naar de homepage">
      <img src="/images/besyn-logo-wit.png" alt="BESYN" width="150" height="31">
    </a>
    <nav class="nav" aria-label="Hoofdmenu">
      <ul class="nav__list">
        {"".join(items)}
      </ul>
    </nav>
    <a class="btn btn--gold header-cta" href="/contact/"{cur}><span class="lbl-long">Plan een kennismaking</span><span class="lbl-short">Contact</span></a>
  </div>
</header>'''


FOOTER = '''<footer class="site-footer">
  <div class="container footer__grid">
    <div class="footer__brand">
      <a class="brand" href="/" aria-label="BESYN, naar de homepage">
        <img src="/images/besyn-logo-wit.png" alt="BESYN" width="150" height="31" loading="lazy">
      </a>
      <p>Executive coaching en zakelijke mediation voor ondernemers, DGA's en directies. Opgericht door Kim Berger.</p>
      <p class="footer__claim">Mens, structuur, strategie<br><em>– in synergie</em></p>
    </div>
    <div>
      <h2>Diensten</h2>
      <ul>
        <li><a href="/executive-coaching/">Executive coaching</a></li>
        <li><a href="/zakelijke-mediation/">Zakelijke mediation</a></li>
        <li><a href="/veelgestelde-vragen/">Veelgestelde vragen</a></li>
      </ul>
    </div>
    <div>
      <h2>Over</h2>
      <ul>
        <li><a href="/kim-berger/">Kim Berger</a></li>
        <li><a href="/kim-berger/#ervaring-expertise">Ervaring &amp; expertise</a></li>
        <li><a href="https://www.huma-advisory.com/" rel="noopener">HUMA Advisory ↗</a></li>
        <li><a class="social" href="https://www.linkedin.com/in/kimbergerexitready/" rel="noopener me"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>LinkedIn</a></li>
      </ul>
    </div>
    <div>
      <h2>Contact</h2>
      <address>
        <ul>
          <li><strong class="footer__legal">Berger Advisory Holding B.V.</strong></li>
          <li><a href="mailto:k.berger@huma-advisory.com">k.berger@huma-advisory.com</a></li>
        </ul>
      </address>
    </div>
  </div>
  <div class="container footer__bottom">
    <p class="mb-0">&copy; <span data-year>2026</span> Berger Advisory Holding B.V. &middot; KvK&nbsp;42003724 &middot; btw&nbsp;NL869238772B01</p>
    <ul>
      <li><a href="/privacyverklaring/">Privacyverklaring</a></li>
      <li><a href="/algemene-voorwaarden/">Algemene voorwaarden</a></li>
      <li><a href="/cookiebeleid/">Cookiebeleid</a></li>
    </ul>
  </div>
</footer>'''


def breadcrumbs_html(p):
    if not p.get("crumb"):
        return ""
    return (f'<nav class="breadcrumbs" aria-label="Kruimelpad"><ol>'
            f'<li><a href="/">Home</a></li><li aria-current="page">{esc(p["crumb"])}</li></ol></nav>')


def faq_details(questions):
    out = []
    for q in questions:
        out.append(f'<details><summary>{esc(q)}</summary><div><p>{esc(FAQ_INDEX[q])}</p></div></details>')
    return "\n      ".join(out)


def faq_page_html():
    toc = "".join(f'<li><a href="#{sid}">{esc(t)}</a></li>' for t, sid, _ in FAQ)
    blocks = []
    for title, sid, items in FAQ:
        qa = "".join(
            f'<div class="qa" id="{slug(q)}"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in items)
        blocks.append(f'<section class="faq-group" id="{sid}" aria-labelledby="{sid}-titel">'
                      f'<h2 id="{sid}-titel">{esc(title)}</h2>{qa}</section>')
    return toc, "\n".join(blocks)


def schema(p):
    url = SITE + p["path"]
    graph = [ORG, PERSON, WEBSITE]
    kind = p.get("kind")
    page_type = {"profile": "ProfilePage", "contact": "ContactPage", "faq": "FAQPage"}.get(kind, "WebPage")
    page = {
        "@type": page_type, "@id": url + "#webpagina", "url": url, "name": p["title"],
        "description": p["desc"], "inLanguage": "nl-NL", "isPartOf": {"@id": SITE + "/#website"},
        "dateModified": LASTMOD,
    }
    if kind == "home":
        page["about"] = {"@id": ORG_ID}
        page["primaryImageOfPage"] = {"@type": "ImageObject", "url": OG}
    if kind == "profile":
        page["mainEntity"] = {"@id": PERSON_ID}
        page["about"] = {"@id": PERSON_ID}
    if kind == "faq":
        page["mainEntity"] = [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for _, _, items in FAQ for q, a in items]
    if p.get("crumb"):
        page["breadcrumb"] = {"@id": url + "#kruimelpad"}
        graph.append({"@type": "BreadcrumbList", "@id": url + "#kruimelpad", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url},
        ]})
    graph.append(page)
    if kind == "service":
        graph.append({
            "@type": "Service", "@id": url + "#dienst", "name": p["service"], "url": url,
            "serviceType": p["service"], "provider": {"@id": ORG_ID},
            "areaServed": [{"@type": "City", "name": "Utrecht"}, {"@type": "Country", "name": "Nederland"}],
            "audience": {"@type": "BusinessAudience", "audienceType": "Ondernemers, DGA's, directies en managementteams"},
            "description": p["desc"],
        })
    data = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")


def head(p):
    url = SITE + p["path"] if p["path"] != "/404.html" else SITE + "/"
    robots = "noindex, follow" if p.get("noindex") else "index, follow, max-image-preview:large, max-snippet:-1"
    canonical = "" if p.get("noindex") else f'\n<link rel="canonical" href="{url}">\n<link rel="alternate" hreflang="nl-NL" href="{url}">'
    ld = "" if p.get("noindex") else f'\n<script type="application/ld+json">\n{schema(p)}\n</script>'
    return f'''<!doctype html>
<html lang="nl-NL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}">
<meta name="robots" content="{robots}">
<meta name="author" content="Kim Berger, BESYN">{canonical}
<meta property="og:type" content="{p.get("ogtype", "website")}">
<meta property="og:site_name" content="BESYN">
<meta property="og:locale" content="nl_NL">
<meta property="og:title" content="{esc(p["title"])}">
<meta property="og:description" content="{esc(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="BESYN – executive coaching en zakelijke mediation in Utrecht">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#004443">
<meta name="geo.region" content="NL-UT">
<meta name="geo.placename" content="Utrecht">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/source-serif-4-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={asset_version("assets/css/style.css")}">
<script src="/assets/js/main.js?v={asset_version("assets/js/main.js")}"></script>{ld}
</head>'''


def build():
    toc, faq_blocks = faq_page_html()
    for p in PAGES:
        body = open(os.path.join(SRC, p["src"]), encoding="utf-8").read()
        body = body.replace("{{BREADCRUMBS}}", breadcrumbs_html(p))
        if p.get("faqlist"):
            body = body.replace("{{FAQ}}", faq_details(p["faqlist"]))
        body = body.replace("{{FAQ_TOC}}", toc).replace("{{FAQ_BLOCKS}}", faq_blocks)
        assert "{{" not in body, p["src"]
        body = version_images(body)
        doc = f'''{head(p)}
<body class="on-dark">
{version_images(header(p["nav"]))}
<main id="main">
{body.strip()}
</main>
{version_images(FOOTER)}
</body>
</html>
'''
        out = os.path.join(ROOT, p["out"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(doc)
        print("✓", p["out"])

    # sitemap
    prio = {"/": "1.0", "/executive-coaching/": "0.9", "/zakelijke-mediation/": "0.9", "/kim-berger/": "0.8",
            "/veelgestelde-vragen/": "0.8", "/contact/": "0.7"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in PAGES:
        if p.get("noindex"):
            continue
        sm.append(f'  <url><loc>{SITE}{p["path"]}</loc><lastmod>{LASTMOD}</lastmod>'
                  f'<priority>{prio.get(p["path"], "0.3")}</priority></url>')
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    print("✓ sitemap.xml")

    # llms.txt (samenvatting voor AI-zoekmachines / GEO)
    lines = ["# BESYN", "",
             "> BESYN is een praktijk voor executive coaching en zakelijke mediation in Utrecht, opgericht door Kim Berger (MSc Bedrijfskunde). BESYN begeleidt ondernemers, DGA's en directies bij leiderschap, besluitvorming en samenwerking in de top, in het bijzonder rond groei, overname en opvolging.",
             "",
             "Kernfeiten:",
             "- Naam: BESYN (merkregel: \"Mens, structuur, strategie – in synergie\")",
             "- Oprichter: Kim Berger, executive coach en mediator; partner bij HUMA Advisory",
             "- Diensten: executive coaching (individueel en MT), zakelijke mediation",
             "- Ervaring: acht jaar M&A en strategie; director bij Exit Ready (begeleiding van ondernemers bij afstand nemen, loslaten en generatiewissels); partner bij HUMA Advisory",
             "- Expertise: leiderschap en teamcoaching, mediation in de top, governance, turnaround- en verbetertrajecten, synergie-onderzoeken, M&A-voorbereiding en deal readiness, strategische groei, markt- en concurrentieanalyses, financiële ratio- en waardeanalyses, businessplannen en positionering",
             "- Doelgroep: ondernemers, DGA's, directeuren, bestuurders en managementteams",
             "- Werkgebied: Utrecht, Randstad en online in heel Nederland",
             "- Contact: k.berger@huma-advisory.com, 06 2005 0351, www.besyn.nl/contact/",
             "- Rechtspersoon: Berger Advisory Holding B.V. (KvK 42003724, btw NL869238772B01)", "",
             "## Pagina's", ""]
    for p in PAGES:
        if p.get("noindex") or p["path"] in ("/privacyverklaring/", "/algemene-voorwaarden/", "/cookiebeleid/"):
            continue
        lines.append(f'- [{p["title"]}]({SITE}{p["path"]}): {p["desc"]}')
    lines += ["", "## Veelgestelde vragen", ""]
    for title, sid, items in FAQ:
        lines.append(f"### {title}")
        for q, a in items:
            lines.append(f"- **{q}** {a}")
        lines.append("")
    open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(lines))
    print("✓ llms.txt")


if __name__ == "__main__":
    build()
