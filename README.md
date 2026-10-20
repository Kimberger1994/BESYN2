# www.besyn.nl — BESYN, executive coaching & zakelijke mediation

Website van BESYN (opgericht door Kim Berger). Statische website (HTML/CSS) voor **GitHub + Netlify**. Er is geen CMS, en er zijn geen externe scripts, trackers of cookies.

```
besyn-website/
├── README.md            ← dit stappenplan
├── FOTOS.md             ← welke foto's en merkelementen waar staan
├── netlify.toml         ← Netlify: redirects van oude adressen, beveiliging, caching
├── bron/                ← bron van de pagina's (alleen nodig bij grotere wijzigingen)
│   ├── build.py              bouwt alle pagina's, sitemap, llms.txt en FAQ opnieuw
│   └── pages/                inhoud per pagina
└── site/                ← de website zelf (dit publiceert Netlify)
    ├── index.html               Home
    ├── executive-coaching/      Executive coaching
    ├── zakelijke-mediation/     Zakelijke mediation
    ├── kim-berger/              Profiel Kim Berger (voor zoeken op haar naam)
    ├── veelgestelde-vragen/     19 vragen en antwoorden
    ├── contact/                 Contactformulier (Netlify Forms) + bedankt-pagina
    ├── privacyverklaring/ · algemene-voorwaarden/ · cookiebeleid/
    ├── 404.html · robots.txt · sitemap.xml · llms.txt
    ├── assets/  (css, js, lettertypen: zelf gehost)
    └── images/  (foto's, BESYN-logo, beeldmerk, stijlelement, deelafbeelding)
```

---

## Snel bekijken (2 minuten, zonder GitHub)
1. Ga naar [app.netlify.com/drop](https://app.netlify.com/drop) en log in.
2. Sleep de map **`site`** (dus niet de hele `besyn-website`-map) in het venster.
3. Je krijgt direct een voorbeeldadres zoals `random-naam.netlify.app`. Redirects en beveiligingsheaders werken pas na stap 2.

## Stap 1 — Op GitHub zetten
**Met GitHub Desktop** (net als bij de HUMA-site):
1. **File → Add Local Repository** → kies `Website/besyn-website`.
2. Meldt GitHub Desktop dat het nog geen repository is? Klik **create a repository** → **Create Repository**. Noem hem bijvoorbeeld `besyn-nl`.
3. Klik **Publish repository**. Laat **Keep this code private** aangevinkt.

Heb je de repository al eerder gepubliceerd? Dan zie je nu alle wijzigingen in GitHub Desktop. Vul links onderin een korte omschrijving in (bijv. "BESYN-huisstijl en FAQ"), klik **Commit to main** en daarna **Push origin**.

## Stap 2 — Koppelen aan Netlify (in hetzelfde team als HUMA Advisory)
1. Log in op [app.netlify.com](https://app.netlify.com) en kies het team waar HUMA Advisory al in staat. Dan monitor je beide sites op één plek.
2. **Add new project → Import an existing project → GitHub** en kies de repository.
3. Build command: **leeg laten**. Publish directory: `site` (staat al in `netlify.toml`).
4. Klik **Deploy**. Na een minuut staat de site live op een adres als `besyn-nl.netlify.app`. Controleer hem daar eerst.

## Stap 3 — Contactformulier aanzetten
1. Netlify: **Project configuration → Forms** → **Enable form detection**.
2. Doe daarna een nieuwe deploy: **Deploys → Trigger deploy → Deploy project**.
3. **Forms → Form notifications → Add notification → Email notification** → `k.berger@huma-advisory.com`.
4. Test het formulier één keer zelf. Spam wordt gefilterd met een verborgen 'honeypot'-veld en het spamfilter van Netlify.

## Stap 4 — Domein www.besyn.nl koppelen
Gebruik je e-mail op een besyn.nl-adres (zoals contact@besyn.nl)? Dan moet die blijven werken. Laat de DNS van besyn.nl daarom **staan waar hij nu is** (Squarespace Domains of je registrar) en pas alleen de twee webrecords aan.

> Maak vóór elke DNS-wijziging een screenshot van je huidige DNS-records. Dan kun je altijd terug.

1. Netlify: **Domain management → Add a domain** → `www.besyn.nl`. Netlify voegt `besyn.nl` (zonder www) toe en stuurt die door naar www.
2. Bij het huidige DNS-beheer van besyn.nl:
   - **A-record** `@` → `75.2.60.5` (verwijder de oude Squarespace A-records)
   - **CNAME** `www` → `besyn-nl.netlify.app` (je eigen Netlify-adres)
   - **MX- en TXT-records (e-mail): niet aanraken.**
3. Netlify regelt HTTPS automatisch. Dat duurt tot ongeveer een uur na de DNS-wijziging.
4. Oude Squarespace-adressen (`/over-mij`, `/coaching-mediation`, `/trajecten`, enz.) sturen via `netlify.toml` met een 301-redirect door naar de nieuwe pagina's. Zo behoud je de Google-waarde die besyn.nl al heeft.

**Optioneel: kimberger.nl.** Heb je dit domein (of registreer je het), voeg het dan in Netlify toe als **domain alias**. Iedereen die kimberger.nl intypt, komt dan op `www.besyn.nl/kim-berger/` terecht. Dat staat al in `netlify.toml`.

## Stap 5 — Squarespace opzeggen
Pas opzeggen als www.besyn.nl via Netlify live staat en het contactformulier werkt. Zeg alleen het **website-abonnement** op. Staat het domein besyn.nl bij Squarespace Domains, dan loopt de domeinregistratie apart door. Wil je het domein verhuizen, vraag dan bij Squarespace de verhuiscode (auth code) op.

---

## Stap 6 — Bovenaan in Google: SEO en SEA

- **SEO** (zoekmachineoptimalisatie) = gratis, gewone zoekresultaten. Kost tijd, maar blijft werken.
- **SEA** (zoekmachineadverteren) = betaalde advertenties (Google Ads) boven de zoekresultaten. Werkt meteen, zolang je betaalt.

De beste aanpak is beide: SEA voor direct zichtbaar zijn, SEO voor blijvend bovenaan staan.

### SEO — al geregeld in de site
- Paginatitels, beschrijvingen en adressen met de zoekwoorden waarop mensen zoeken: "executive coaching Utrecht", "zakelijke mediation", "Kim Berger".
- Een eigen profielpagina `/kim-berger/` met je naam in titel, kop en adres, voor wie op je naam zoekt.
- Gestructureerde data (schema.org) die Google precies vertelt wat BESYN is, wie Kim Berger is (oprichter, partner bij HUMA Advisory, LinkedIn) en welke diensten er zijn.
- Een pagina met veelgestelde vragen en korte, duidelijke antwoorden. Die gebruikt Google voor directe antwoorden in de zoekresultaten.
- Sitemap, 301-redirects van de oude Squarespace-adressen, snelle en mobielvriendelijke pagina's.
- Ook AI-zoekmachines (ChatGPT, Perplexity, Gemini, Copilot) mogen de site lezen, met een korte samenvatting in `llms.txt`.

> Google toont sinds 2023 de uitklapbare FAQ-resultaten bijna alleen nog voor overheids- en zorgsites. De FAQ-pagina blijft wel waardevol voor gewone resultaten en AI-antwoorden.

### SEO — wat jij nog doet (dit maakt het grootste verschil)
1. **Google Search Console** ([search.google.com/search-console](https://search.google.com/search-console)): voeg `besyn.nl` toe als *domeinproperty* (verificatie met een TXT-record bij je DNS-beheer). Dien `https://www.besyn.nl/sitemap.xml` in en vraag indexering aan voor de homepage, `/executive-coaching/`, `/zakelijke-mediation/`, `/kim-berger/` en `/veelgestelde-vragen/`.
2. **Bing Webmaster Tools** ([bing.com/webmasters](https://www.bing.com/webmasters)): kies **Importeren uit Google Search Console**. Bing levert ook resultaten aan onder meer DuckDuckGo en Microsoft Copilot.
3. **Google Bedrijfsprofiel** ([business.google.com](https://business.google.com)): maak een profiel aan voor **BESYN** in Utrecht. Kies een passende hoofdcategorie (bijv. "Mediationdienst" of een coachcategorie die Google aanbiedt). Je kunt je adres verbergen en een servicegebied instellen. Vraag tevreden opdrachtgevers om een Google-review. Dit is de belangrijkste stap voor zoekopdrachten als "executive coach Utrecht".
4. **Overal dezelfde gegevens** (naam, adres, telefoon, website): BESYN · Van Esveldstraat 31-1, 3572 KK Utrecht · 06 2005 0351 · www.besyn.nl. Dat geldt voor het Google-profiel, LinkedIn, KvK en de HUMA-website.
5. **LinkedIn**: zet `www.besyn.nl` als website in je profiel, en "Oprichter BESYN" in je kopregel. Maak eventueel een LinkedIn-bedrijfspagina voor BESYN.
6. **HUMA Advisory**: laat je naam op de teampagina linken naar `https://www.besyn.nl/kim-berger/`. Dat is de sterkste link die je zelf in de hand hebt.
7. **Registers en verenigingen**: ben je aangesloten bij een beroepsvereniging of register voor coaches of mediators? Vraag een vermelding met link naar www.besyn.nl.
8. **Nieuwe inhoud**: voeg af en toe een veelgestelde vraag toe (in `bron/build.py`) of publiceer een artikel op LinkedIn met een link naar de site.

### SEA — Google Ads (direct bovenaan)
Een Google Ads-account maak je zelf aan op [ads.google.com](https://ads.google.com), omdat er betaalgegevens bij horen. Kies **Expertmodus** en een **Zoekcampagne**. Een opzet die past bij BESYN:

| Campagne | Zoekwoorden (voorbeelden) | Landingspagina |
|---|---|---|
| **1. Naam en merk** | "kim berger", "kim berger coach", "besyn", "besyn coaching" | `https://www.besyn.nl/kim-berger/` en de homepage |
| **2. Executive coaching** | "executive coaching utrecht", "executive coach", "coaching dga", "leiderschapscoaching directie" | `https://www.besyn.nl/executive-coaching/` |
| **3. Zakelijke mediation** | "zakelijke mediation", "mediator aandeelhouders", "conflict directie mediation" | `https://www.besyn.nl/zakelijke-mediation/` |

- **Campagne 1** zorgt dat je bij een zoekopdracht op je naam altijd bovenaan staat. Op je eigen naam is er weinig concurrentie, dus dit is meestal goedkoop.
- **Locatie:** Utrecht en omgeving (of heel Nederland voor mediation). **Taal:** Nederlands.
- **Uitsluitingszoekwoorden** (zodat je niet betaalt voor verkeerde klikken): gratis, opleiding, cursus, vacature, worden, salaris, scheiding, echtscheiding.
- **Extensies:** voeg je telefoonnummer toe (belextensie) en links naar "Veelgestelde vragen" en "Contact".
- **Budget:** begin met een vast dagbudget dat je zelf kiest en bekijk na 2 à 4 weken wat het oplevert.
- **Resultaat meten zonder cookies:** laat **automatische tagging** in Google Ads aanstaan. Komt iemand via een advertentie binnen en stuurt die een bericht, dan zie je bij het formulierbericht in Netlify het veld **herkomst**, bijvoorbeeld "Google Ads". Gewone bezoekers krijgen "website". Daarvoor zijn geen cookies of cookiebanner nodig.
- Wil je later de conversietracking van Google zelf gebruiken (de Google-tag), dan zijn een cookiemelding en een aanpassing van het cookiebeleid en de beveiligingsinstellingen nodig. Vraag Claude dan om hulp.

### Realistisch verwachten
- Op **"BESYN"** en **"Kim Berger BESYN"** sta je na indexering normaal snel bovenaan.
- Op alleen **"Kim Berger"** deel je de resultaten met naamgenoten. De profielpagina, LinkedIn, de HUMA-link en een advertentie op je naam (campagne 1) helpen hier het meest.
- Algemene zoektermen zoals **"executive coaching Utrecht"** zijn concurrerend. Organisch duurt dat enkele maanden, met het Google Bedrijfsprofiel en reviews als belangrijkste hefboom. Met SEA sta je er direct.

## Stap 7 — Monitoren (beide sites in één Netlify-team)
- **Netlify-dashboard:** deploys, formulierinzendingen en bezoekersstatistieken per site. Hoe lang statistieken bewaard blijven, hangt af van je abonnement: Free 1 dag, Personal 7 dagen, Pro 30 dagen (stand oktober 2026).
- **Credits:** het gratis plan heeft 300 credits per maand, gedeeld door alle sites in het team. Een productie-deploy kost 15 credits en 1 GB verkeer 20 credits. Raken de credits op, dan wordt de site gepauzeerd. Met twee sites en regelmatige updates is **Personal ($9/maand, 1.000 credits)** de veilige keuze.
- **Google Search Console en Bing Webmaster Tools:** zoekposities, klikken en indexeringsfouten.
- **Google Ads:** kosten per klik en aantal klikken; de **herkomst** in Netlify Forms laat zien welke berichten via een advertentie kwamen.
- Voeg je ooit statistieken met cookies toe (zoals Google Analytics), pas dan het cookiebeleid aan en voeg een cookiemelding toe. Netlify-statistieken en Search Console hebben dat niet nodig.

## Stap 8 — Later iets aanpassen
- **Kleine tekstwijziging:** open in GitHub het bestand (bijv. `site/kim-berger/index.html`), klik op het potloodje, pas de tekst aan en klik **Commit changes**. Netlify zet het binnen een minuut live.
- **Grotere wijziging** (header, footer, menu, FAQ, paginatitels): pas `bron/build.py` of `bron/pages/` aan en voer `python3 bron/build.py` uit in de map `besyn-website`. Dan worden alle pagina's, de sitemap, `llms.txt` en de gestructureerde data in één keer bijgewerkt. Vraag Claude gerust om dit voor je te doen.

---

## Controleer vóór livegang
- [x] **Ervaring**: overal "acht jaar" M&A en strategie (door jou bevestigd).
- [ ] **Algemene voorwaarden**: betaling binnen **14 dagen**, kosteloos verzetten tot **48 uur** vooraf. Klopt dat? Laat ze bij voorkeur door een jurist checken (bijv. je HUMA-collega).
- [ ] **Privacyverklaring**: bewaartermijnen (contactberichten en gespreksaantekeningen 12 maanden, administratie 7 jaar) en verwerkers (Netlify, e-mailprovider, boekhouder).
- [ ] **Handelsnaam BESYN vastleggen bij de KVK**: de site vermeldt "BESYN, een handelsnaam van Berger Advisory Holding B.V." (KvK 42003724, btw NL869238772B01). Bij de KVK staat nu alleen "Berger Advisory Holding B.V.". Voeg BESYN toe als extra handelsnaam: gratis via [Mijn KVK](https://www.kvk.nl/wijzigen/handelsnaam-wijzigen/) (inloggen met DigiD → bedrijf kiezen → handelsnaam toevoegen). Dat koppelt BESYN officieel aan de B.V. en helpt bij de verificatie van het Google Bedrijfsprofiel. Het oude nummer 90775376 van besyn.nl is overal vervangen.
- [x] **Vestigingsadres**: Van Esveldstraat 31-1, 3572 KK Utrecht staat in de footer, op de contactpagina, in de privacyverklaring, de voorwaarden en de gestructureerde data.
- [ ] **Testimonials**: letterlijk overgenomen van de oude site. Vraag klanten of je naam, functie en bedrijf mag tonen; dat maakt ze sterker.
- [ ] **Profielpagina**: het blok "Wat mij heeft gevormd" (ik-vorm) is geschreven op basis van je oude Over mij-tekst, zonder details over familie, gezondheid of verlies. Klopt de toon? Je kernovertuiging ("Ieder kijkt door een eigen bril…") staat op de homepage en als citaat op de profielpagina.
- [ ] **Coachtraject**: "start doorgaans met vier sessies van ±1,5 uur" komt uit je oude Fundament-traject.
- [x] **Telefoon en e-mail**: 06 2005 0351 en k.berger@huma-advisory.com staan op elke pagina en in de gestructureerde data. Berichten via het contactformulier stuurt Netlify naar hetzelfde adres (stap 3).

## Wat er beter is dan op de oude site
- De BESYN-huisstijl blijft: logo, beeldmerk, stijlelement (druppels), petrol, teal en goud. De druppelvorm komt terug in foto's, iconen en het watermerk.
- BESYN staat centraal; Kim Berger is herkenbaar als oprichter, met een eigen profielpagina voor zoekopdrachten op haar naam.
- Zakelijke teksten in de u-vorm, met duidelijke kennismakings-knoppen op elke pagina.
- Nieuwe pagina met veelgestelde vragen, en korte definities voor zoekmachines en AI.
- Juridische pagina's echt ingevuld in plaats van sjablonen; geen dubbele pagina's (`/home`, `/over-mij-1`).
- Geen cookies of trackers, lettertypen zelf gehost (AVG-vriendelijk), dus geen cookiebanner nodig.
- AI-zoekdiensten mogen de site lezen (Squarespace blokkeerde die).
