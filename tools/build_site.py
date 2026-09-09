# -*- coding: utf-8 -*-
"""
Static site generator for the Wellforge Energy Solutions website.

Run:  python tools/build_site.py
Output: plain HTML files in the project root (no server or build tool needed).

Editing the header, footer or navigation once in tools/templates.py and
re-running this script keeps every page in sync.
"""

import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from templates import (SITE, NAV, PRODUCT_LINKS, icon, rel, head, header, footer, logo,
                       page_hero, stats_block, section_head, enquiry_form, cta_banner,
                       render, REQUIREMENT_OPTIONS, scene, marquee, asset, range_id,
                       photo, photo_figure)
from content_products import CATEGORIES
from content_blog import POSTS, CATEGORIES as BLOG_CATEGORIES, CATEGORY_LABEL
import content_about as ABOUT
import content_services as SERVICES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write(path, text):
    full = os.path.join(ROOT, path)
    folder = os.path.dirname(full)
    if folder and not os.path.isdir(folder):
        os.makedirs(folder)
    with io.open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("  wrote %s" % path)


# ---------------------------------------------------------------------------
# Structured data
# ---------------------------------------------------------------------------
def jsonld(obj):
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(obj, indent=2, ensure_ascii=False))


ORGANISATION = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": SITE["domain"] + "/#organization",
    "name": SITE["legal"],
    "alternateName": SITE["name"],
    "url": SITE["domain"] + "/",
    "logo": SITE["domain"] + "/assets/img/logo-full.png",
    "description": ("Oil and gas equipment sourcing and supply chain company supplying downhole "
                    "completion tools, API certified casing and tubing, plant and machinery, drilling "
                    "fluids and chemicals, and subsea and offshore equipment to drilling companies, "
                    "E&P operators, oilfield contractors and service providers."),
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Gurugram",
        "addressRegion": "Haryana",
        "addressCountry": "IN",
    },
    "contactPoint": [{
        "@type": "ContactPoint",
        "contactType": "sales",
        "name": SITE["contact_person"],
        "telephone": SITE["phone"],
        "email": SITE["email"],
        "areaServed": "Worldwide",
        "availableLanguage": ["English", "Hindi"],
    }],
    "areaServed": "Worldwide",
    "knowsAbout": [
        "oilfield equipment sourcing India",
        "API certified casing and tubing supplier",
        "downhole completion tools supplier",
        "oil and gas procurement partner",
    ],
}


def breadcrumb_schema(items):
    return jsonld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name,
             "item": SITE["domain"] + "/" + path}
            for i, (name, path) in enumerate(items)
        ],
    })


# ---------------------------------------------------------------------------
# Shared copy fragments (verbatim from the approved content document)
# ---------------------------------------------------------------------------
WHY_WELLFORGE = [
    ("user-check", "Single Point of Contact",
     "One dedicated sourcing partner for your entire equipment and product portfolio. No juggling "
     "multiple vendors, no fragmented supplier management."),
    ("shield", "Full API &amp; Compliance Coverage",
     "Strict adherence to API Specifications, ISO standards, and client-specific quality requirements "
     "&mdash; with full documentation at every step."),
    ("bolt", "Compressed Lead Times",
     "Established relationships with global manufacturers and Indian suppliers allow us to compress "
     "procurement lead times significantly."),
    ("tag", "Cost-Competitive Pricing",
     "A multi-vendor network and volume leverage give clients access to competitive pricing without "
     "sacrificing quality or compliance."),
]

CLIENT_TYPES = [
    ("drilling-companies", "derrick", "Drilling Companies &amp; Contractors",
     "Rig consumables, spare parts, BOP components, drill string accessories, safety equipment, and "
     "site services support &mdash; fast, compliant, and cost-effective.",
     "products/drilling-equipment-tools.html"),
    ("ep-operators", "well", "E&amp;P Operators (Exploration &amp; Production)",
     "Completion tools, wellbore hardware, downhole accessories, and production equipment for onshore "
     "and offshore well programmes &mdash; API-certified and inspection-ready.",
     "products/downhole-completion-octg.html"),
    ("service-providers", "wrench", "Oilfield Service Providers",
     "Tool components, machined parts, steel products, and specialist equipment for cementing, "
     "stimulation, wireline, coiled tubing, and production services companies.",
     "products/casting-forging-machining.html"),
    ("epc-contractors", "building", "EPC &amp; Construction Contractors",
     "Structural steel, pipes, flanges, valves, fittings, and plant equipment for upstream and "
     "midstream construction projects &mdash; procured globally and delivered on schedule.",
     "products/plant-machinery-industrial-tools.html"),
]

TECHNOLOGY_PARTNER_CARD = (
    "technology-partners", "network", "Technology &amp; Subsea Partners",
    "For subsea tool manufacturers and offshore technology companies seeking an Indian or "
    "Asia-Pacific distribution, JV, or technology transfer partner &mdash; Wellforge offers market "
    "access, regulatory navigation, local partner networks, and operational support.",
    "product-sourcing.html")

PROCESS = [
    ("01", "Requirement Capture",
     "We study your MR, specifications, quantity, delivery timeline, and compliance requirements in detail."),
    ("02", "Global Vendor Screening",
     "We identify and shortlist qualified, API-approved manufacturers from our global supply network."),
    ("03", "Technical Evaluation",
     "Detailed TBE (technical bid evaluation) against your specifications. No guesswork, no "
     "substitutions without approval."),
    ("04", "QA/QC &amp; Inspection",
     "Factory inspection, material traceability, dimensional verification, and third-party inspection "
     "coordination as required."),
    ("05", "Logistics &amp; Delivery",
     "End-to-end freight management, customs clearance, documentation, and last-mile delivery to your "
     "site or warehouse."),
]

ADVANTAGES = [
    ("Single Point of Contact",
     "One dedicated sourcing partner for your entire equipment and product portfolio. No juggling "
     "multiple vendors, no fragmented supplier management.",
     ["Dedicated account management", "Consolidated procurement reporting",
      "Single invoice, single relationship", "Consistent quality standards across all items"]),
    ("Full API &amp; Compliance Coverage",
     "We maintain strict adherence to API Specifications, ISO standards, and client-specific quality "
     "requirements &mdash; with full documentation at every step.",
     ["API 11D1, API 5CT, API 5L, API 6A, API 7-1", "Material Test Reports (MTR)",
      "Third-party inspection facilitation", "CoC, MTC, dimensional reports"]),
    ("Compressed Lead Times",
     "Our established relationships with global manufacturers and Indian suppliers allow us to "
     "compress procurement lead times significantly.",
     ["Emergency / AOG sourcing capability", "Strategic stock for fast-moving items",
      "Parallel procurement on multi-item MRs", "Expediting and factory follow-up"]),
    ("Cost-Competitive Pricing",
     "Our multi-vendor network and volume leverage give clients access to competitive pricing without "
     "sacrificing quality or compliance.",
     ["Multi-source comparison on every MR", "Import duty optimisation advice",
      "Total cost of ownership analysis", "Flexible commercial terms"]),
    ("Technical Depth",
     "Our team understands what your engineers are specifying &mdash; and can raise technical queries, "
     "evaluate substitutions, and provide engineering support on sourcing decisions.",
     ["TBE preparation and review", "Technical deviation management",
      "Equivalent substitution evaluation", "Vendor technical clarifications"]),
    ("India &amp; Global Access",
     "Relationships with Indian manufacturers (reducing import duty &amp; lead times) combined with "
     "global sourcing from the US, Europe, and Asia.",
     ["Make-in-India capability", "Global OEM access",
      "Cross-border trade expertise", "Customs &amp; EXIM documentation"]),
]

CORE_VALUES = [
    ("Technical Precision",
     "We don't approximate. Every specification, material grade, dimensional tolerance, and compliance "
     "requirement is verified before delivery. Our clients operate in high-stakes environments &mdash; "
     "and we match that standard."),
    ("Partnership Over Transaction",
     "We invest in understanding your operations, your project timelines, and your long-term "
     "requirements. We don't just fulfil purchase orders &mdash; we become part of your supply chain team."),
    ("Compliance Without Compromise",
     "API Specifications, ISO standards, and client-specific quality requirements are non-negotiable. "
     "We maintain rigorous documentation, inspection records, and certification trails for every "
     "product we supply."),
    ("Agility &amp; Speed",
     "Drilling doesn't wait. Completion programmes have windows. Our lean, experienced team responds "
     "fast &mdash; whether it's an emergency sourcing request or a complex multi-item procurement schedule."),
    ("Global Reach, Local Insight",
     "We combine an international supply network spanning Asia, Europe, and the Americas with deep "
     "local market knowledge in India and the Middle East &mdash; giving clients the best of both worlds."),
    ("Continuous Innovation",
     "We actively pursue technology transfer partnerships, JV collaborations, and licensing "
     "arrangements &mdash; ensuring our clients have access to the latest oilfield tools and "
     "technologies from around the world."),
]

EXPERTISE = [
    "Downhole Completion Engineering", "Oilfield Procurement", "API Spec Compliance",
    "International Trade &amp; Logistics", "Quality Management Systems", "Supply Chain Optimisation",
    "Vendor Development", "Project Management", "Technical Inspection &amp; QA/QC",
    "Joint Venture &amp; Partnership Development", "Drilling Fluids &amp; Chemicals",
    "Steel &amp; Industrial Products",
]


def client_card(anchor, ic, title, body, link, depth=0, learn="Learn More"):
    r = rel(depth)
    return """<article class="card reveal tilt" id="{anchor}">
  <span class="card__icon">{icon}</span>
  <h3>{title}</h3>
  <p>{body}</p>
  <a class="link-arrow" href="{r}{link}">{learn} {arrow}</a>
</article>""".format(anchor=anchor, icon=icon(ic), title=title, body=body, r=r, link=link,
                     learn=learn, arrow=icon("arrow-right", "link-arrow__ico"))


def category_cards(depth=0, limit=None):
    r = rel(depth)
    cards = []
    for cat in (CATEGORIES[:limit] if limit else CATEGORIES):
        cards.append("""<article class="cat-card reveal tilt">
  <a class="cat-card__hit" href="{r}products/{slug}.html" aria-label="{plain}"></a>
  <div class="cat-card__media">
    <img src="{art}" alt="" loading="lazy" decoding="async"
         width="860" height="620">
    <span class="cat-card__tag">Category {num}</span>
  </div>
  <div class="cat-card__body">
    <span class="cat-card__icon">{icon}</span>
    <h3>{title}</h3>
    <p>{lead}</p>
    <span class="link-arrow">Explore Category {arrow}</span>
  </div>
</article>""".format(num=cat["num"], icon=icon(cat["icon"]), title=cat["title"],
                     plain=cat["title"].replace("&amp;", "and"),
                     lead=cat["lead"], r=r, slug=cat["slug"],
                     art=asset("assets/img/art/cat-%s.svg" % cat["slug"], depth),
                     arrow=icon("arrow-right", "link-arrow__ico")))
    return "".join(cards)


# Which photograph fronts each product category page. Categories 05 and 06
# (casting/forging, plant and tools) have no entry: no public-domain photograph
# of that subject was good enough, so their technical illustration stands alone
# rather than padding the page with a generic industrial stock shot.
CATEGORY_PHOTO = {
    "drilling-equipment-tools": (
        "offshore-rigs-flare",
        "Rig machinery, drill string, well control and handling tools "
        "&mdash; sourced against the API specification that governs each item."),
    "downhole-completion-octg": (
        "tricone-bit",
        "Downhole hardware is selected against the well envelope &mdash; pressure, "
        "temperature, fluid and deviation &mdash; not a catalogue headline."),
    "surface-production-artificial-lift": (
        "pumpjack",
        "Beam pumping, submersible and gas lift equipment, sourced to the lift "
        "design your production engineers have specified."),
    "fluids-solids-control-workover": (
        "mud-tanks",
        "Pumps, solids control and processing equipment &mdash; the circulating "
        "side of the operation, where wear parts decide uptime."),
}

# Which 3D model fronts each product category page.
CATEGORY_SCENE = {
    "drilling-equipment-tools": "tricone",
    "downhole-completion-octg": "casing",
    "surface-production-artificial-lift": "tree",
    "fluids-solids-control-workover": "mudmotor",
    "casting-forging-machining": "gears",
    "plant-machinery-industrial-tools": "valve",
}


# ===========================================================================
#  HOME
# ===========================================================================
def build_home():
    page = {
        "path": "index.html",
        "nav": "home",
        "title": "Oilfield Equipment Sourcing India | Oil &amp; Gas Procurement Partner | Wellforge Energy Solutions",
        "desc": ("Wellforge Energy Solutions is an oil and gas equipment sourcing partner in Gurugram, "
                 "India - supplying API certified casing and tubing, downhole completion tools, plant and "
                 "machinery, drilling fluids and subsea equipment to clients worldwide."),
        "keywords": ("oilfield equipment sourcing India, oil and gas procurement partner, API certified "
                     "casing and tubing supplier, downhole completion tools supplier, oilfield supply chain "
                     "company Gurugram"),
        "schema": jsonld(ORGANISATION) + jsonld({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE["name"],
            "url": SITE["domain"] + "/",
            "publisher": {"@id": SITE["domain"] + "/#organization"},
        }),
    }

    why = "".join("""<article class="feature reveal tilt">
  <span class="feature__index">{idx}</span>
  <span class="feature__icon">{icon}</span>
  <h3>{title}</h3>
  <p>{body}</p>
</article>""".format(idx="0%d" % (i + 1), icon=icon(ic), title=t, body=b)
        for i, (ic, t, b) in enumerate(WHY_WELLFORGE))

    clients = "".join(client_card(a, i, t, b, l) for a, i, t, b, l in CLIENT_TYPES)

    steps = "".join("""<article class="card card--step reveal">
  <span class="card__step">{num}</span>
  <p class="eyebrow" style="margin-bottom:10px">Step {num}</p>
  <h3>{title}</h3>
  <p>{body}</p>
</article>""".format(num=num, title=title, body=body) for num, title, body in PROCESS)

    body = """<section class="hero" id="top">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="hero__scene">{hero_scene}</div>
  <div class="wrap">
    <div class="hero__inner">
      <p class="eyebrow">Global Oil &amp; Gas Sourcing</p>
      <h1><span class="hero__line">Forged for the Field.</span><span class="hero__line hero__line--accent">Built to Perform.</span></h1>
      <p class="hero__sub">Your Fast, Flexible Sourcing Partner for Oil &amp; Gas Equipment.</p>
      <p class="hero__support">Competitive pricing. Global reach. Delivered fast.</p>
      <div class="btn-row">
        <a class="btn btn--gold" href="contact.html">Request a Quote {arrow}</a>
        <a class="btn btn--outline" href="product-sourcing.html">View Our Products</a>
      </div>
      <ul class="hero__tags">
        <li>API Spec Compliant</li>
        <li>Global Vendor Network</li>
        <li>24-Hour Response</li>
      </ul>
    </div>
  </div>
  <a class="hero__cue" href="#why-wellforge"><span>Explore</span>{down}</a>
</section>

<div class="wrap">
  {stats}
</div>

<section class="section" id="why-wellforge">
  <div class="wrap">
    {why_head}
    <div class="grid grid--4">{why}</div>
  </div>
</section>

<section class="section section--grey">
  <div class="wrap">
    {clients_head}
    <div class="grid grid--4">{clients}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {cats_head}
    <div class="grid grid--3">{cats}</div>
    <div class="btn-row btn-row--center mt-48">
      <a class="btn btn--outline-navy" href="product-sourcing.html">View All Product Categories</a>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="wrap">
    {process_head}
    <figure class="figure figure--flow reveal">
      <img src="{flow_art}" alt="The five step Wellforge sourcing process, from requirement capture through to delivery"
           loading="lazy" decoding="async" width="1120" height="240">
    </figure>
    <div class="grid grid--3">{steps}</div>
    <div class="btn-row btn-row--center mt-48">
      <a class="btn btn--outline-navy" href="strategic-sourcing.html">See the Full Process</a>
    </div>
  </div>
</section>

{photo_band}

{cta}
""".format(
        flow_art=asset("assets/img/art/process-flow.svg", 0),
        photo_band=photo("offshore-platform-dusk", "wide", 0, cls="photo-band--tall",
                         eyebrow="Where We Work",
                         caption="From the rig floor to the fabrication yard &mdash; onshore, "
                                 "offshore and subsea, for clients worldwide."),
        hero_scene=scene("rig", depth=0, cls="scene--stage", poster=False),
        arrow=icon("arrow-right", "btn__arrow"),
        down=icon("arrow-down", "hero__cue-ico"),
        stats=stats_block("stats--float"),
        why_head=section_head("Our Advantage", "Why Wellforge"),
        why=why,
        clients_head=section_head("Client Sectors", "Who We Serve",
                                  "Wellforge supports the full upstream and midstream value chain "
                                  "&mdash; from the rig floor to the fabrication yard."),
        clients=clients,
        cats_head=section_head("Products &amp; Equipment", "What We Source",
                               "Five sourcing verticals, one accountable point of contact.", center=True),
        cats=category_cards(),
        process_head=section_head("How We Work", "Our Sourcing Process",
                                  "A structured, transparent, five-step process &mdash; from your "
                                  "requirement to your doorstep.", center=True),
        steps=steps,
        cta=cta_banner(
            "Interested in Making Wellforge Your Strategic Sourcing Partner?",
            "We welcome conversations with procurement heads, supply chain managers, and operations teams "
            "at drilling companies, E&amp;P operators, contractors, and service providers. Let us "
            "demonstrate how we can simplify your supply chain, reduce your procurement overheads, and "
            "ensure your equipment arrives compliant, on time, and on budget.",
            '<a class="btn btn--gold" href="contact.html">Contact Us to Schedule a Sourcing Consultation</a>'),
    )

    write("index.html", render(page, body, 0))


# ===========================================================================
#  ABOUT
# ===========================================================================
def build_about():
    page = {
        "path": "about.html",
        "nav": "about",
        "title": "About Wellforge Energy Solutions | Our Story, Mission &amp; Leadership",
        "desc": ("Wellforge Energy Solutions is an oilfield equipment and strategic sourcing company "
                 "serving drilling contractors, E&P operators and service providers worldwide. Our "
                 "story and purpose, our mission and vision, our core values, and the leadership and expertise behind the company."),
        "keywords": ("about Wellforge Energy Solutions, oilfield sourcing company India, oil and gas "
                     "supply chain partner, oilfield procurement company Gurugram, oilfield sourcing "
                     "mission and vision"),
        "schema": jsonld(ORGANISATION) + breadcrumb_schema([("Home", "index.html"),
                                                            ("About Us", "about.html")]),
    }

    f = ABOUT.FOUNDATION
    mv = ABOUT.MISSION_VISION
    pe = ABOUT.PEOPLE

    # ---- 1. Our Story ------------------------------------------------------
    facts = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in f["facts"])

    principles = "".join("""<article class="feature reveal">
  <span class="feature__icon">{icon}</span>
  <h3>{title}</h3>
  <p>{body}</p>
</article>""".format(icon=icon(ic), title=t, body=b) for ic, t, b in f["principles"])

    # ---- 2. Mission & Vision -----------------------------------------------
    values = "".join("""<article class="value reveal">
  <span class="value__index">{idx}</span>
  <h3>{title}</h3>
  <p>{body}</p>
</article>""".format(idx="0%d" % (i + 1), title=t, body=b)
        for i, (t, b) in enumerate(mv["values"]))

    # ---- 4. Leadership & Expertise -----------------------------------------
    chips = "".join("<li>%s</li>" % e for e in pe["expertise"])

    # No breadcrumb on this page - the hero leads straight into the eyebrow.
    body = page_hero(ABOUT.HERO["eyebrow"], ABOUT.HERO["title"], ABOUT.HERO["lead"], depth=0,
                     scene_name="gears")

    body += """
<section class="section" id="our-story">
  <div class="wrap">
    {found_head}
    <div class="split split--top">
      <div class="prose reveal">{left}</div>
      <div class="prose reveal">{right}</div>
    </div>
    <dl class="facts facts--3 mt-48 reveal">{facts}</dl>
  </div>
</section>

{story_photo}

<section class="section section--grey">
  <div class="wrap">
    {prin_head}
    <div class="grid grid--3">{principles}</div>
  </div>
</section>

<section class="section section--navy section--rosette">
  <div class="wrap">
    {stats_head}
    {stats}
  </div>
</section>

<section class="section" id="mission-vision">
  <div class="wrap">
    {mv_head}
    <div class="grid grid--2">
      <article class="pillar reveal">
        <span class="pillar__icon">{m_icon}</span>
        <h3>Our Mission</h3>
        <p>{mission}</p>
      </article>
      <article class="pillar reveal">
        <span class="pillar__icon">{v_icon}</span>
        <h3>Our Vision</h3>
        <p>{vision}</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--grey" id="core-values">
  <div class="wrap">
    {values_head}
    <div class="grid grid--3">{values}</div>
  </div>
</section>

<section class="section" id="leadership">
  <div class="wrap">
    {people_head}
    <div class="split split--top">
      <div class="prose reveal">{p_left}</div>
      <div class="stack">
        <div class="prose reveal">{p_right}</div>
        {people_photo}
      </div>
    </div>
  </div>
</section>

<section class="section section--navy section--tight">
  <div class="wrap">
    {exp_head}
    <ul class="chips reveal">{chips}</ul>
  </div>
</section>

{cta}
""".format(
        story_photo=photo("offshore-inspector", "wide", 0,
                          eyebrow="Markets Served",
                          caption="India &middot; Middle East &amp; North Africa &middot; West Africa "
                                  "&middot; Asia-Pacific &middot; North America &middot; South America "
                                  "&middot; CIS countries."),
        found_head=section_head(f["eyebrow"], f["title"], f["lead"]),
        left="".join("<p>%s</p>" % x for x in f["paragraphs_left"]),
        right="".join("<p>%s</p>" % x for x in f["paragraphs_right"]),
        facts=facts,
        prin_head=section_head("Founding Principles", f["principles_head"],
                               f["principles_lead"], center=True),
        principles=principles,
        stats_head=section_head("At a Glance", "Key Milestones &amp; Scale", center=True),
        stats=stats_block("stats--navy"),
        mv_head=section_head(mv["eyebrow"], mv["title"], mv["lead"], center=True),
        mission=mv["mission"], vision=mv["vision"],
        m_icon=icon("target"), v_icon=icon("globe"),
        values_head=section_head(mv["values_head"], mv["values_title"], mv["values_lead"],
                                 center=True),
        values=values,
        people_head=section_head(pe["eyebrow"], pe["title"], pe["lead"]),
        people_photo=photo_figure("crew-transfer", "card", 0,
                                  caption="Our team has worked alongside national oil companies, "
                                          "independent operators, drilling contractors and "
                                          "oilfield service majors."),
        p_left="".join("<p>%s</p>" % x for x in pe["paragraphs_left"]),
        p_right="".join("<p>%s</p>" % x for x in pe["paragraphs_right"]),
        exp_head=section_head("Capabilities", pe["expertise_head"], pe["expertise_lead"]),
        chips=chips,
        cta=cta_banner(ABOUT.CTA["title"], ABOUT.CTA["body"],
                       '<a class="btn btn--gold" href="contact.html">%s</a>' % ABOUT.CTA["button"]),
    )

    write("about.html", render(page, body, 0))


# ===========================================================================
#  STRATEGIC SOURCING   (Who We Serve / Process / Advantage / Compliance)
# ===========================================================================
COMPLIANCE_STANDARDS = [
    "API 11D1 &mdash; Packers &amp; Bridge Plugs",
    "API 5CT &mdash; Casing &amp; Tubing",
    "API 5L &mdash; Line Pipe",
    "API 6A &mdash; Wellhead Equipment",
    "API 7-1 &mdash; Rotary Drill Stem Elements",
    "ASME B16.5 &mdash; Pipe Flanges &amp; Fittings",
    "ISO 11960 &middot; ISO 14310 &middot; ISO 3183",
]

COMPLIANCE_DELIVERABLES = [
    "Material Test Reports (MTR)",
    "Certificates of Conformity (CoC)",
    "Dimensional inspection reports",
    "Third-party inspection facilitation",
    "Client-specific QCPs and ITP compliance",
    "Full material traceability and heat records",
]


def build_strategic_sourcing():
    page = {
        "path": "strategic-sourcing.html",
        "nav": "sourcing",
        "title": "Strategic Sourcing | Oilfield Procurement Partner for Drilling &amp; E&amp;P | Wellforge",
        "desc": ("Strategic sourcing for the oilfield - who we serve, our five-step sourcing process, "
                 "the Wellforge advantage, and the API and ISO compliance standards we supply against "
                 "for clients worldwide."),
        "keywords": ("strategic sourcing oil and gas, oilfield procurement partner, oilfield sourcing "
                     "process, API compliance oilfield supplier, oil and gas supply chain partner India"),
        "schema": breadcrumb_schema([("Home", "index.html"),
                                     ("Strategic Sourcing", "strategic-sourcing.html")]),
    }

    # ---- 1. Who We Serve ---------------------------------------------------
    cards = [client_card(a, i, t, b, l) for a, i, t, b, l in CLIENT_TYPES]
    a, i, t, b, l = TECHNOLOGY_PARTNER_CARD
    cards.append(client_card(a, i, t, b, l))

    # ---- 2. Sourcing Process (5 steps) -------------------------------------
    steps = "".join("""<article class="step reveal" id="step-{num}">
  <div class="step__marker"><span class="step__num">{num}</span></div>
  <div class="step__body">
    <h3>{title}</h3>
    <p>{body}</p>
  </div>
</article>""".format(num=num, title=title, body=body) for num, title, body in PROCESS)

    # ---- 3. The Wellforge Advantage ----------------------------------------
    advantages = "".join("""<article class="advantage reveal tilt">
  <span class="advantage__num">{num}</span>
  <h3>{title}</h3>
  <p>{body}</p>
  <ul class="tick-list">{items}</ul>
</article>""".format(num="0%d" % (i + 1), title=t, body=b,
                     items="".join("<li>%s</li>" % x for x in items))
        for i, (t, b, items) in enumerate(ADVANTAGES))

    # ---- 4. Compliance & Standards -----------------------------------------
    std_chips = "".join("<li>%s</li>" % c for c in COMPLIANCE_STANDARDS)
    deliverables = "".join("<li>%s</li>" % d for d in COMPLIANCE_DELIVERABLES)

    body = page_hero(
        "Strategic Sourcing", "Your Dedicated Sourcing Partner for the Oilfield",
        "Wellforge Energy Solutions is purpose-built to serve as the strategic sourcing arm for drilling "
        "and E&amp;P companies, contractors, and oilfield service providers &mdash; bringing together "
        "global supply networks, deep technical expertise, and uncompromising compliance standards.",
        crumbs=[("Strategic Sourcing", "strategic-sourcing.html")], depth=0,
        scene_name="pdc")

    body += """
<section class="section">
  <div class="wrap">
    <div class="split split--top split--aside">
      <div class="prose reveal">
        <p>The oil and gas industry's supply chain is one of the most complex in the world. Procurement
           teams are under constant pressure to reduce costs, compress lead times, maintain API and HSE
           compliance, and manage an increasingly fragmented global supplier base &mdash; all while keeping
           the rig running.</p>
        <p>Wellforge was specifically designed to remove that burden. We act as your dedicated sourcing
           partner &mdash; a single, technically competent, compliance-driven point of contact for all your
           equipment and product procurement needs.</p>
      </div>
      <div class="prose reveal">
        <p>Whether you are a national oil company running a multi-well development programme, an
           independent E&amp;P operator planning a completion campaign, a drilling contractor managing rig
           consumables and spare parts, or an oilfield service company building out its tool inventory
           &mdash; Wellforge is your sourcing partner.</p>
        <p><strong>We don't replace your procurement team. We extend it</strong> &mdash; adding capacity,
           capability, and global reach precisely where you need it most.</p>
      </div>
      <figure class="figure figure--well reveal">
        <img src="{well_art}" alt="Cased well schematic showing conductor, surface, intermediate and production strings with a production packer and perforated interval"
             loading="lazy" decoding="async" width="420" height="720">
        <figcaption>A cased well in section &mdash; every string, joint and tool on this drawing is
          something we source.</figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="section section--grey" id="who-we-serve">
  <div class="wrap">
    {serve_head}
    <div class="grid grid--3">{cards}</div>
  </div>
</section>

{serve_photo}

<section class="section" id="sourcing-process">
  <div class="wrap">
    {process_head}
    <figure class="figure figure--flow reveal">
      <img src="{flow_art}" alt="The five step Wellforge sourcing process, from requirement capture through to delivery"
           loading="lazy" decoding="async" width="1120" height="240">
    </figure>
  </div>
  <div class="wrap wrap--narrow">
    <div class="stepper">{steps}</div>
  </div>
</section>

<section class="section section--grey" id="wellforge-advantage">
  <div class="wrap">
    {adv_head}
    <div class="grid grid--3">{advantages}</div>
  </div>
</section>

<section class="section section--navy section--rosette" id="compliance-standards">
  <div class="wrap">
    {comp_head}
    <div class="split split--top">
      <div class="reveal">
        <h3>Standards We Supply Against</h3>
        <ul class="chips" style="margin-top:20px">{std_chips}</ul>
      </div>
      <div class="reveal">
        <h3>Documentation Delivered</h3>
        <ul class="tick-list" style="margin-top:20px">{deliverables}</ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {stats}
  </div>
</section>

{cta}
""".format(
        flow_art=asset("assets/img/art/process-flow.svg", 0),
        well_art=asset("assets/img/art/wellbore.svg", 0),
        serve_photo=photo("crew-transfer", "wide", 0,
                          eyebrow="Who We Serve",
                          caption="National oil companies, independent operators, drilling "
                                  "contractors and service companies &mdash; onshore and offshore."),
        serve_head=section_head("Who We Serve", "Who We Serve",
                                "Every client type has a different sourcing profile. Each card links "
                                "through to the product range that supports it.", center=True),
        cards="".join(cards),
        process_head=section_head("How We Work", "Sourcing Process &mdash; 5 Steps",
                                  "A structured, transparent, five-step process &mdash; from your "
                                  "requirement to your doorstep.", center=True),
        steps=steps,
        adv_head=section_head("Why Wellforge", "The Wellforge Advantage",
                              "Six reasons procurement and operations teams consolidate their sourcing "
                              "with Wellforge.", center=True),
        advantages=advantages,
        comp_head=section_head("Compliance", "Compliance &amp; Standards",
                               "API Specifications, ISO standards, and client-specific quality "
                               "requirements are non-negotiable. Every item we source is delivered with "
                               "the documentation trail your quality plan requires."),
        std_chips=std_chips,
        deliverables=deliverables,
        stats=stats_block(),
        cta=cta_banner(
            "Ready to Extend Your Procurement Team?",
            "Send us your material requisition, well programme, or sourcing requirement and we will "
            "respond within 24 hours with a technically reviewed proposal.",
            '<a class="btn btn--gold" href="contact.html">Request a Consultation</a>'
            '<a class="btn btn--outline" href="product-sourcing.html">View Our Products</a>',
            center=True),
    )

    write("strategic-sourcing.html", render(page, body, 0))


# ===========================================================================
#  OUR SERVICES
# ===========================================================================
def build_our_services():
    page = {
        "path": "our-services.html",
        "nav": "services",
        "title": "Our Services | Engineering, Procurement, QA/QC &amp; Logistics | Wellforge Energy Solutions",
        "desc": ("Product sourcing and vendor development, technical bid evaluation, completion engineering "
                 "support, emergency AOG sourcing, custom machining, ITP and third-party inspection "
                 "coordination, EXIM logistics, and technology consultation, licensing and JV "
                 "structuring for the energy industry."),
        "keywords": ("oilfield product sourcing services, vendor development oil and gas, technical bid "
                     "evaluation TBE, AOG emergency sourcing, third party inspection coordination, "
                     "EXIM logistics oil and gas, technology consultation partner India, oilfield QA QC"),
        "schema": breadcrumb_schema([("Home", "index.html"), ("Our Services", "our-services.html")]),
    }

    tones = ["", " section--grey", "", " section--grey", ""]
    sections = []

    for i, svc in enumerate(SERVICES.SERVICES):
        blocks = "".join("""<article class="advantage reveal tilt">
  <h3>{title}</h3>
  <p>{intro}</p>
  <ul class="tick-list">{items}</ul>
</article>""".format(title=b["title"], intro=b["intro"],
                     items="".join("<li>%s</li>" % it for it in b["items"]))
            for b in svc["blocks"])

        grid = "grid--3" if len(svc["blocks"]) > 2 else "grid--2"

        sections.append("""
<section class="section{tone}" id="{sid}">
  <div class="wrap">
    {head}
    <div class="grid {grid}">{blocks}</div>
  </div>
</section>""".format(tone=tones[i % len(tones)], sid=svc["id"], grid=grid, blocks=blocks,
                     head=section_head("Service " + svc["num"] + " &mdash; " + svc["eyebrow"],
                                       svc["title"], svc["lead"])))

    nav_cards = "".join("""<a class="card card--jump reveal tilt" href="#{sid}">
  <span class="card__step">{num}</span>
  <h3>{title}</h3>
  {nav}
  <span class="link-arrow">Jump to section {arrow}</span>
</a>""".format(sid=svc["id"], num=svc["num"], title=svc["title"],
               # Service 01 names the section identically in the menu; do not repeat it.
               nav="" if svc["nav"] == svc["title"] else "<p>%s</p>" % svc["nav"],
               arrow=icon("arrow-right", "link-arrow__ico"))
        for svc in SERVICES.SERVICES)

    body = page_hero(SERVICES.HERO["eyebrow"], SERVICES.HERO["title"], SERVICES.HERO["lead"],
                     crumbs=[("Our Services", "our-services.html")], depth=0,
                     scene_name="valve")

    body += """
{svc_photo}

<section class="section section--tight">
  <div class="wrap">
    <p class="lead reveal" style="max-width:78ch">{intro}</p>
    <div class="btn-row mt-32 reveal">
      <a class="btn btn--gold" href="contact.html">{cta}</a>
      <a class="btn btn--outline-navy" href="product-sourcing.html">View Products &amp; Equipment</a>
    </div>
  </div>
</section>

<section class="section section--grey section--tight">
  <div class="wrap">
    <div class="grid grid--3">{nav_cards}</div>
  </div>
</section>
{sections}

{cta_banner}
""".format(intro=SERVICES.HERO["intro"], cta=SERVICES.HERO["cta"], nav_cards=nav_cards,
           svc_photo=photo("pipeline-inspection", "wide", 0,
                           eyebrow="Quality &amp; Compliance",
                           caption="Inspection is planned at order placement, and the document "
                                   "pack is verified before anything is released."),
           sections="".join(sections),
           cta_banner=cta_banner(SERVICES.CTA["title"], SERVICES.CTA["body"],
                                 '<a class="btn btn--gold" href="contact.html">%s</a>'
                                 % SERVICES.CTA["button"]))

    write("our-services.html", render(page, body, 0))


# ===========================================================================
#  PRODUCT SOURCING HUB
# ===========================================================================
def build_product_hub():
    page = {
        "path": "product-sourcing.html",
        "nav": "products",
        "title": "Products &amp; Equipment | Oilfield Tools, Steel, Machinery &amp; Chemicals | Wellforge",
        "desc": ("Five oilfield sourcing categories - downhole completion tools and wellbore hardware, "
                 "steel and tubular products, plant and machinery, drilling fluids and chemicals, and "
                 "subsea, offshore and onshore equipment."),
        "keywords": ("oilfield equipment sourcing India, downhole completion tools supplier, API certified "
                     "casing and tubing supplier, drilling fluids supplier, subsea equipment sourcing"),
        "schema": breadcrumb_schema([("Home", "index.html"),
                                     ("Products &amp; Equipment", "product-sourcing.html")]) + jsonld({
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Wellforge Products and Equipment Categories",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "name": cat["title"].replace("&amp;", "&"),
                 "url": SITE["domain"] + "/products/" + cat["slug"] + ".html"}
                for i, cat in enumerate(CATEGORIES)],
        }),
    }

    compliance = "".join("<li>%s</li>" % c for c in CATEGORIES[0]["compliance"])

    body = page_hero(
        "Products &amp; Equipment", "Products &amp; Equipment",
        "Five sourcing categories covering downhole completion tools and wellbore hardware, steel and "
        "tubular products, plant and machinery, drilling fluids and chemicals, and subsea, offshore and "
        "onshore equipment &mdash; each backed by the same compliance and documentation standard.",
        crumbs=[("Products &amp; Equipment", "product-sourcing.html")], depth=0,
        scene_name="tricone")

    body += """
<section class="section">
  <div class="wrap">
    <div class="grid grid--3">{cards}</div>
  </div>
</section>

<section class="section section--navy section--rosette">
  <div class="wrap">
    {head}
    <ul class="chips">{compliance}</ul>
  </div>
</section>

{cta}
""".format(
        cards=category_cards(),
        head=section_head("Compliance", "Standards We Supply Against",
                          "Every item we source is delivered with the documentation trail your quality "
                          "plan requires &mdash; material test reports, certificates of conformity, "
                          "dimensional records and third-party inspection facilitation."),
        compliance=compliance,
        cta=cta_banner(
            "Can't Find What You Are Looking For?",
            "Our sourcing network extends well beyond the categories listed here. Send us your requisition "
            "and we will tell you within 24 hours whether we can supply it, and at what lead time.",
            '<a class="btn btn--gold" href="contact.html">Send an Enquiry</a>',
            center=True),
    )

    write("product-sourcing.html", render(page, body, 0))


# ===========================================================================
#  PRODUCT CATEGORY PAGES
# ===========================================================================
# Each category page preselects its own requirement type on the enquiry form.
CATEGORY_PRESELECT = {c["slug"]: c["short"] for c in CATEGORIES}


def build_category(cat):
    path = "products/%s.html" % cat["slug"]
    page = {
        "path": path,
        "nav": "products",
        "title": cat["meta_title"],
        "desc": cat["meta_desc"],
        "keywords": cat["keywords"],
        "schema": breadcrumb_schema([
            ("Home", "index.html"),
            ("Products &amp; Equipment", "product-sourcing.html"),
            (cat["title"].replace("&amp;", "&"), path),
        ]),
    }

    specs = "".join("<tr><th scope=\"row\">%s</th><td>%s</td></tr>" % (k, v) for k, v in cat["specs"])
    spec_table = """<div class="table-wrap reveal">
  <table class="spec-table">
    <caption>{caption}</caption>
    <tbody>{rows}</tbody>
  </table>
</div>""".format(caption=cat["spec_caption"], rows=specs)

    intro_html = "".join("<p>%s</p>" % p for p in cat["intro"]) or \
        "<p>%s</p>" % cat["lead"]

    highlight = ""
    if cat["highlight"]:
        highlight = """
    <div class="panel panel--navy mt-32 reveal">
      <h3>{title}</h3>
      <p>{body}</p>
    </div>""".format(**cat["highlight"])

    applications = ""
    if cat["applications"]:
        items = "".join("<li><strong>%s</strong>%s</li>" % (n, d) for n, d in cat["applications"])
        applications = """
<section class="section section--grey">
  <div class="wrap">
    {head}
    <ul class="app-list reveal">{items}</ul>
  </div>
</section>""".format(head=section_head("Applications", "Applications", center=True), items=items)

    compliance = ""
    if cat["compliance"]:
        chips = "".join("<li>%s</li>" % c for c in cat["compliance"])
        compliance = """
<section class="section section--navy">
  <div class="wrap">
    {head}
    <ul class="chips">{chips}</ul>
  </div>
</section>""".format(head=section_head("Compliance",
                                       cat["compliance_title"] or "Compliance Standards",
                                       center=True),
                     chips=chips)

    ranges = "".join("""<article class="range reveal tilt" id="{rid}">
  <h3>{title}</h3>
  <p class="range__desc">{desc}</p>
  <span class="range__std">{std}</span>
  <ul class="tick-list">{items}</ul>
</article>""".format(rid=range_id(r["title"]), title=r["title"], desc=r["desc"], std=r["std"],
                     items="".join("<li>%s</li>" % i for i in r["items"]))
        for r in cat["ranges"])

    extra_buttons = ""
    if cat.get("cta_extra"):
        extra_buttons = """
      <div class="btn-row" style="margin-bottom:28px">
        <a class="btn btn--navy" href="mailto:{email}?subject=Sourcing%20enquiry%20-%20{slug}">Email Us</a>
        <a class="btn btn--outline-navy" href="mailto:{email}?subject=Request%20-%20Wellforge%20Company%20Profile">Download Company Profile</a>
      </div>""".format(email=SITE["email"], slug=cat["slug"])

    form = enquiry_form(
        form_id="enq-" + cat["slug"],
        subject="Product enquiry - " + cat["title"].replace("&amp;", "&"),
        button_label=cat["cta_button"],
        preselect=CATEGORY_PRESELECT[cat["slug"]])

    body = page_hero(
        "Category " + cat["num"], cat["title"], cat["lead"],
        crumbs=[("Products &amp; Equipment", "product-sourcing.html"), (cat["short"], path)],
        depth=1, scene_name=CATEGORY_SCENE[cat["slug"]])

    body += """
<section class="section">
  <div class="wrap">
    <div class="split split--top split--aside">
      <div class="prose reveal">
        {intro}
        {highlight}
      </div>
      <div class="stack">
        {spec_table}
        <figure class="figure figure--cat reveal">
          <img src="{cat_art}" alt="Technical illustration - {plain}"
               loading="lazy" decoding="async" width="860" height="620">
        </figure>
      </div>
    </div>
  </div>
</section>
{applications}
{compliance}

{cat_photo}

<section class="section">
  <div class="wrap">
    {ranges_head}
    <div class="grid grid--3">{ranges}</div>
  </div>
</section>

<section class="section section--grey">
  <div class="wrap">
    <div class="split split--top">
      <div>
        {cta_head}
        <p class="lead">{cta_body}</p>
        {extra_buttons}
        <ul class="tick-list mt-32">
          <li>Response within 24 hours on every enquiry</li>
          <li>Technically reviewed proposals &mdash; not catalogue quotes</li>
          <li>Full documentation and inspection support</li>
        </ul>
      </div>
      <div>{form}</div>
    </div>
  </div>
</section>
""".format(intro=intro_html, highlight=highlight, spec_table=spec_table,
           slug=cat["slug"], plain=cat["title"].replace("&amp;", "and"),
           cat_art=asset("assets/img/art/cat-%s.svg" % cat["slug"], 1),
           cat_photo=(photo(CATEGORY_PHOTO[cat["slug"]][0], "wide", 1,
                            eyebrow=cat["short"],
                            caption=CATEGORY_PHOTO[cat["slug"]][1])
                      if cat["slug"] in CATEGORY_PHOTO else ""),
           applications=applications, compliance=compliance,
           ranges_head=section_head("Product Range", "Product Range", center=True),
           ranges=ranges,
           cta_head=section_head("Enquire", cat["cta_title"]),
           cta_body=cat["cta_body"], extra_buttons=extra_buttons, form=form)

    write(path, render(page, body, 1))


# ===========================================================================
#  BLOG
# ===========================================================================
# Article cover art is generated by tools/make_art.py.


def post_card(post, depth=0):
    r = rel(depth)
    return """<article class="post-card reveal tilt" data-category="{cat}">
  <a class="post-card__media" href="{r}blog/{slug}.html" tabindex="-1" aria-hidden="true">
    <img src="{cover}" alt="" loading="lazy" decoding="async"
         width="1200" height="675">
  </a>
  <div class="post-card__body">
    <div class="post-card__meta">
      <span class="tag">{label}</span>
      <time datetime="{iso}">{date}</time>
      <span>&middot;</span>
      <span>{read}</span>
    </div>
    <h3><a href="{r}blog/{slug}.html">{title}</a></h3>
    <p>{excerpt}</p>
    <a class="link-arrow" href="{r}blog/{slug}.html">Read Article {arrow}</a>
  </div>
</article>""".format(cat=post["cat"], r=r, slug=post["slug"], label=CATEGORY_LABEL[post["cat"]],
                     iso=post["date_iso"], date=post["date"], read=post["read"],
                     title=post["title"], excerpt=post["excerpt"],
                     cover=asset("assets/img/blog/%s.svg" % post["slug"], depth),
                     arrow=icon("arrow-right", "link-arrow__ico"))


def build_blogs():
    page = {
        "path": "blogs.html",
        "nav": "blogs",
        "title": "Blogs | Oilfield Sourcing Insights, Compliance &amp; Standards | Wellforge Energy Solutions",
        "desc": ("Industry insights, compliance and standards guidance, and practical sourcing tips for oil "
                 "and gas procurement teams - from API 5CT grades to HPHT completions and lead time "
                 "reduction."),
        "keywords": ("oilfield sourcing blog, API 5CT grades guide, HPHT completions, oil and gas "
                     "procurement insights, oilfield compliance standards"),
        "schema": breadcrumb_schema([("Home", "index.html"), ("Blogs", "blogs.html")]),
    }

    filters = "".join(
        '<button class="filter-btn{active}" type="button" data-filter="{key}" aria-pressed="{pressed}">{label}</button>'
        .format(active=" is-active" if key == "all" else "", key=key,
                pressed="true" if key == "all" else "false", label=label)
        for key, label in BLOG_CATEGORIES)

    cards = "".join(post_card(p) for p in POSTS)

    body = page_hero(
        "Blogs", "Sourcing Insights &amp; Industry Perspective",
        "Industry insights, compliance and standards guidance, and practical sourcing tips from the "
        "Wellforge team.",
        crumbs=[("Blogs", "blogs.html")], depth=0)

    body += """
<section class="section">
  <div class="wrap">
    <div class="filter-bar reveal" role="group" aria-label="Filter articles by category">{filters}</div>
    <div class="grid grid--3">{cards}</div>
  </div>
</section>

<section class="section section--grey">
  <div class="wrap">
    <div class="newsletter reveal">
      <div>
        <h3>Get sourcing insights in your inbox</h3>
        <p>Occasional notes on oilfield procurement, compliance standards and lead time management.
           No spam &mdash; unsubscribe any time.</p>
      </div>
      <div>
        <form data-newsletter novalidate>
          <label class="visually-hidden" for="news-email">Email address</label>
          <input id="news-email" type="email" name="email" placeholder="you@company.com" required>
          <button class="btn btn--gold" type="submit">Subscribe</button>
        </form>
        <p class="form-status"></p>
      </div>
    </div>
  </div>
</section>
""".format(filters=filters, cards=cards)

    write("blogs.html", render(page, body, 0))


def build_post(post, index):
    path = "blog/%s.html" % post["slug"]
    plain_title = post["title"].replace("&amp;", "&").replace("&rsquo;", "'")
    page = {
        "path": path,
        "nav": "blogs",
        "title": post["meta_title"],
        "desc": post["meta_desc"],
        "keywords": post["keywords"],
        "ogtype": "article",
        "schema": breadcrumb_schema([("Home", "index.html"), ("Blogs", "blogs.html"),
                                     (plain_title, path)]) + jsonld({
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": plain_title,
            "datePublished": post["date_iso"],
            "dateModified": post["date_iso"],
            "author": {"@type": "Organization", "name": SITE["legal"]},
            "publisher": {"@id": SITE["domain"] + "/#organization"},
            "mainEntityOfPage": SITE["domain"] + "/" + path,
            "image": SITE["domain"] + "/assets/img/blog/" + post["slug"] + ".svg",
            "articleSection": CATEGORY_LABEL[post["cat"]].replace("&amp;", "&"),
        }),
    }

    others = [p for p in POSTS if p["slug"] != post["slug"]][:3]
    related = "".join(post_card(p, depth=1) for p in others)

    body = """<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol>
        <li><a href="../index.html">Home</a></li>
        <li><a href="../blogs.html">Blogs</a></li>
        <li><span aria-current="page">{label}</span></li>
      </ol>
    </nav>
    <p class="eyebrow">{label}</p>
    <h1>{title}</h1>
    <div class="article__meta">
      <time datetime="{iso}">{date}</time>
      <span>&middot;</span>
      <span>{author}</span>
      <span>&middot;</span>
      <span>{read}</span>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">
    <div class="article article--paper">
      <figure class="article__figure">
        <img src="{cover}" alt="{alt}" width="1200" height="675">
      </figure>
      {content}
      <div class="btn-row mt-48">
        <a class="btn btn--gold" href="../contact.html">Talk to Our Sourcing Desk</a>
        <a class="btn btn--outline-navy" href="../blogs.html">All Articles</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="wrap">
    {related_head}
    <div class="grid grid--3">{related}</div>
  </div>
</section>
""".format(label=CATEGORY_LABEL[post["cat"]], title=post["title"], iso=post["date_iso"],
           date=post["date"], author=post["author"], read=post["read"], slug=post["slug"],
           cover=asset("assets/img/blog/%s.svg" % post["slug"], 1),
           alt=plain_title, content=post["body"],
           related_head=section_head("More Reading", "Related Articles", center=True),
           related=related)

    write(path, render(page, body, 1))


# ===========================================================================
#  CONTACT
# ===========================================================================
def build_contact():
    page = {
        "path": "contact.html",
        "nav": "contact",
        "title": "Contact Wellforge Energy Solutions | Oilfield Equipment Sourcing Enquiries",
        "desc": ("Contact Wellforge Energy Solutions Pvt. Ltd., Gurugram, Haryana, India. Call "
                 "+91-8384031002 or email sales@wellforgeenergysolutions.com for oilfield equipment "
                 "sourcing enquiries."),
        "keywords": ("contact Wellforge Energy Solutions, oilfield equipment supplier Gurugram, oil and gas "
                     "sourcing enquiry India, request oilfield equipment quote"),
        "schema": jsonld(ORGANISATION) + jsonld({
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "url": SITE["domain"] + "/contact.html",
            "about": {"@id": SITE["domain"] + "/#organization"},
        }),
    }

    form = enquiry_form(
        form_id="contact",
        subject="Website enquiry",
        button_label="Send Enquiry",
        heading="Drop Us a Line!",
        blurb="Tell us what you need to source. We respond to every enquiry within 24 hours.")

    body = page_hero(
        "Contact Us", "Contact Us",
        "Send us your material requisition, well programme, or sourcing requirement and we will respond "
        "within 24 hours.",
        crumbs=[("Contact Us", "contact.html")], depth=0,
        scene_name="mudmotor")

    body += """
<section class="section">
  <div class="wrap">
    <div class="contact-split">
      <div>{form}</div>

      <aside class="info-card reveal">
        <p class="info-card__tag">Company Details</p>
        <h3>{legal}</h3>
        <ul class="info-list">
          <li>
            <span class="info-list__icon">{pin}</span>
            <span>
              <span class="info-list__label">Office &amp; Works</span>
              <span class="info-list__value">{address}</span>
            </span>
          </li>
          <li>
            <span class="info-list__icon">{user}</span>
            <span>
              <span class="info-list__label">Contact</span>
              <span class="info-list__value">{person}</span>
            </span>
          </li>
          <li>
            <span class="info-list__icon">{phone_i}</span>
            <span>
              <span class="info-list__label">Phone</span>
              <span class="info-list__value"><a href="tel:{phone_link}">{phone}</a></span>
            </span>
          </li>
          <li>
            <span class="info-list__icon">{mail_i}</span>
            <span>
              <span class="info-list__label">Email</span>
              <span class="info-list__value"><a href="mailto:{email}">{email}</a></span>
            </span>
          </li>
          <li>
            <span class="info-list__icon">{globe}</span>
            <span>
              <span class="info-list__label">Markets Served</span>
              <span class="info-list__value">Worldwide</span>
            </span>
          </li>
        </ul>
        <div class="btn-row">
          <a class="btn btn--whatsapp btn--block" href="{whatsapp}" target="_blank" rel="noopener">
            {wa} Message us on WhatsApp
          </a>
          <a class="btn btn--outline btn--block" href="mailto:{email}?subject=Request%20-%20Wellforge%20Company%20Profile">
            {doc} Download Company Profile
          </a>
        </div>
      </aside>
      {contact_photo}
    </div>
  </div>
</section>

""".format(form=form, legal=SITE["legal"], pin=icon("pin"), address=SITE["address_line"],
           contact_photo=photo_figure("offshore-platform-dusk", "card", 0,
                                      caption="Serving drilling companies, E&amp;P operators, "
                                              "contractors and service providers across three "
                                              "continents."),
           user=icon("user-check"), person=SITE["contact_person"], phone_i=icon("phone"),
           phone_link=SITE["phone_link"], phone=SITE["phone"], mail_i=icon("mail"),
           email=SITE["email"], globe=icon("globe"), whatsapp=SITE["whatsapp"], wa=icon("whatsapp"),
           doc=icon("doc"))

    write("contact.html", render(page, body, 0))


# ===========================================================================
#  LEGAL PAGES
# ===========================================================================
LEGAL_NOTE = ('<div class="panel reveal" style="margin-bottom:32px"><p><strong>Note for the Wellforge '
              'team:</strong> this is a standard template. Please have it reviewed against your final '
              'operating and data-handling practices before the site goes live.</p></div>')


def build_legal():
    privacy_body = page_hero(
        "Legal", "Privacy Policy",
        "How Wellforge Energy Solutions Private Limited collects, uses and protects information submitted "
        "through this website.",
        crumbs=[("Privacy Policy", "privacy-policy.html")], depth=0)

    privacy_body += """
<section class="section">
  <div class="wrap wrap--narrow">
    <div class="article article--paper prose">
      {note}
      <p><strong>Last updated:</strong> August 2026</p>

      <h2>Information We Collect</h2>
      <p>We collect only the information you choose to provide through our enquiry forms &mdash; typically
         your name, company, email address, telephone number, requirement type and the details of your
         enquiry. We do not collect payment information through this website.</p>

      <h2>How We Use Your Information</h2>
      <p>Information submitted through this website is used solely to respond to your enquiry, prepare
         quotations, and communicate with you about the products and services you have asked about. We do
         not sell, rent or trade your information.</p>

      <h2>Sharing With Third Parties</h2>
      <p>Where fulfilling your enquiry requires it, we may share relevant technical details of your
         requirement (specification, quantity, delivery location) with manufacturers, inspection agencies
         and logistics providers in our supply network. We share only what is necessary to source and
         deliver your requirement.</p>

      <h2>Cookies and Analytics</h2>
      <p>This website uses only the cookies required for basic functionality. If analytics or marketing
         tools are added in future, this policy will be updated and a cookie notice will be presented.</p>

      <h2>Data Retention</h2>
      <p>Enquiry correspondence is retained for as long as needed to serve the commercial relationship and
         to satisfy statutory record-keeping requirements under Indian law.</p>

      <h2>Your Rights</h2>
      <p>You may request access to, correction of, or deletion of the personal information we hold about
         you by writing to <a href="mailto:{email}">{email}</a>.</p>

      <h2>Contact</h2>
      <p>{legal}<br>{address}<br>
         Email: <a href="mailto:{email}">{email}</a><br>
         Phone: <a href="tel:{phone_link}">{phone}</a></p>
    </div>
  </div>
</section>
""".format(note=LEGAL_NOTE, email=SITE["email"], legal=SITE["legal"], address=SITE["address_line"],
           phone_link=SITE["phone_link"], phone=SITE["phone"])

    write("privacy-policy.html", render({
        "path": "privacy-policy.html", "nav": "", "title": "Privacy Policy | Wellforge Energy Solutions",
        "desc": "Privacy policy for the Wellforge Energy Solutions website.",
        "keywords": "Wellforge privacy policy", "schema": ""}, privacy_body, 0))

    terms_body = page_hero(
        "Legal", "Terms of Use",
        "The terms on which this website is made available by Wellforge Energy Solutions Private Limited.",
        crumbs=[("Terms of Use", "terms-of-use.html")], depth=0)

    terms_body += """
<section class="section">
  <div class="wrap wrap--narrow">
    <div class="article article--paper prose">
      {note}
      <p><strong>Last updated:</strong> August 2026</p>

      <h2>Use of This Website</h2>
      <p>This website is provided for general information about the products and services of
         {legal}. By using it you agree to these terms.</p>

      <h2>Product Information</h2>
      <p>Product specifications, size ranges, pressure and temperature ratings, grades and compliance
         standards shown on this website are indicative and describe the range we are able to source. They
         do not constitute a technical offer. Final specifications, applicable standards and certification
         are confirmed in writing at the quotation and order stage.</p>

      <h2>No Warranty</h2>
      <p>While we take care to keep this website accurate and current, it is provided on an
         &ldquo;as is&rdquo; basis without warranties of any kind. Nothing on this website should be relied
         upon as engineering advice for a specific well, project or application.</p>

      <h2>Intellectual Property</h2>
      <p>The Wellforge name, logo, page content and site design are the property of {legal}. Third-party
         marks, standards designations (including API and ISO specification numbers) and manufacturer names
         remain the property of their respective owners and are used for identification only.</p>

      <h2>External Links</h2>
      <p>This website may link to third-party sites. We are not responsible for their content or
         practices.</p>

      <h2>Governing Law</h2>
      <p>These terms are governed by the laws of India, and the courts at Gurugram, Haryana shall have
         jurisdiction.</p>

      <h2>Contact</h2>
      <p>{legal}<br>{address}<br>
         Email: <a href="mailto:{email}">{email}</a></p>
    </div>
  </div>
</section>
""".format(note=LEGAL_NOTE, legal=SITE["legal"], address=SITE["address_line"], email=SITE["email"])

    write("terms-of-use.html", render({
        "path": "terms-of-use.html", "nav": "", "title": "Terms of Use | Wellforge Energy Solutions",
        "desc": "Terms of use for the Wellforge Energy Solutions website.",
        "keywords": "Wellforge terms of use", "schema": ""}, terms_body, 0))


# ===========================================================================
#  SITEMAP + ROBOTS
# ===========================================================================
def build_sitemap():
    urls = ["index.html", "about.html", "strategic-sourcing.html", "our-services.html",
            "product-sourcing.html"]
    urls += ["products/%s.html" % c["slug"] for c in CATEGORIES]
    urls += ["blogs.html"]
    urls += ["blog/%s.html" % p["slug"] for p in POSTS]
    urls += ["contact.html", "privacy-policy.html", "terms-of-use.html"]

    priority = {"index.html": "1.0", "product-sourcing.html": "0.9", "contact.html": "0.9"}
    entries = []
    for u in urls:
        entries.append(
            "  <url>\n    <loc>%s/%s</loc>\n    <changefreq>monthly</changefreq>\n"
            "    <priority>%s</priority>\n  </url>" % (SITE["domain"], u, priority.get(u, "0.8")))

    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(entries) + "\n</urlset>\n")

    write("robots.txt",
          "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE["domain"])


# ===========================================================================
def main():
    print("Building Wellforge Energy Solutions website...")
    build_home()
    build_about()
    build_strategic_sourcing()
    build_our_services()
    build_product_hub()
    for cat in CATEGORIES:
        build_category(cat)
    build_blogs()
    for i, post in enumerate(POSTS):
        build_post(post, i)
    build_contact()
    build_legal()
    build_sitemap()
    print("Done.")


if __name__ == "__main__":
    main()
