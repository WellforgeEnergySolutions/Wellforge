# -*- coding: utf-8 -*-
"""
Our Services content for the Wellforge Energy Solutions website.

Five service pillars across the energy lifecycle. The section and sub-section
headings and the core bullet points come from the approved services outline;
the introductions and the supporting detail under each heading are elaborated
for the web while staying inside what Wellforge already offers elsewhere on the
site (API/ISO compliance, machining capability, EXIM handling, JV structuring).

Order note: this list drives BOTH the page section order and the "Our Services"
dropdown in tools/templates.py, so reordering here is enough - the menu follows.
"""

HERO = {
    "eyebrow": "Our Services",
    "title": "Comprehensive Services Across the Energy Lifecycle",
    "lead": ("End-to-end technical, procurement, quality, and supply chain solutions engineered to keep "
             "your rigs running and operations fully compliant."),
    "cta": "Speak to a Technical Specialist",
    "intro": ("Sourcing an oilfield component is rarely just a buying decision. It is a vendor "
              "qualification, an engineering review, an inspection plan, a documentation trail and a "
              "logistics problem &mdash; and a failure in any one of them lands on your rig. Wellforge "
              "covers all five, under a single accountable relationship."),
}

SERVICES = [
    # ------------------------------------------------------------------ 01
    {
        "id": "procurement-vendor",
        "num": "01",
        "nav": "Product Sourcing, Procurement &amp; Vendor Development",
        "eyebrow": "Product Sourcing &amp; Procurement",
        "title": "Product Sourcing, Procurement &amp; Vendor Development",
        "lead": ("Sourcing the right product begins with qualifying who can actually make it. We "
                 "pre-screen and audit manufacturers against the specific product, grade and size on your "
                 "requisition &mdash; then run parallel enquiries so price and delivery are both "
                 "competitive, across every category we supply."),
        "blocks": [
            {
                "title": "Product Sourcing Across the Full Portfolio",
                "intro": ("One requisition can span downhole tools, tubulars, machinery and chemicals. We "
                          "source all of it, to one standard, through one relationship."),
                "items": [
                    "Downhole completion tools and wellbore hardware &mdash; packers, plugs, liner hangers, flow control",
                    "API-certified casing, tubing, line pipe, flanges, fittings, valves and structural steel",
                    "Plant, machinery, CNC machine tools, precision components and HSE equipment",
                    "Drilling fluids, mud and cementing chemicals, and rig consumables",
                    "Subsea, offshore and onshore production equipment",
                    "Mixed multi-category requisitions consolidated onto a single schedule and report",
                ],
            },
            {
                "title": "Global Vendor Pre-Screening, Development &amp; Auditing",
                "intro": ("We do not hand you a vendor list. We qualify manufacturers on your behalf and "
                          "put forward only those that can make the item to specification."),
                "items": [
                    "Identifying and qualifying API-licensed and ISO-certified manufacturing facilities globally",
                    "Licence <strong>scope</strong> verification &mdash; product, grade and size range, not just &ldquo;API approved&rdquo;",
                    "Single-source to multi-source commercial comparison on every significant MR",
                    "Capacity, production schedule and threading slot checks before award",
                    "Facility audit and first-order oversight when developing a new vendor",
                    "Ongoing performance review on quality, delivery and documentation",
                ],
            },
            {
                "title": "Emergency &amp; Critical Lead-Time Sourcing",
                "intro": ("Rig downtime is measured in hours. When a critical-path item fails, there is a "
                          "single number to call and a team that already knows who holds stock."),
                "items": [
                    "Expedited and emergency / AOG sourcing for drilling spares, consumables and critical-path rig items",
                    "Strategic stock agreements on fast-moving consumables and wear parts",
                    "Make-in-India manufacturing networks that remove freight, duty and customs from the critical path",
                    "Parallel procurement across qualified vendors instead of sequential enquiry",
                    "Factory expediting and production follow-up through to dispatch",
                    "Long-pole items split onto their own PO so the balance is never held up",
                ],
            },
            {
                "title": "Custom Machining &amp; Component Fabrication to Drawing",
                "intro": ("Where an item is obsolete, proprietary or simply not worth importing, we make "
                          "it &mdash; to your drawing, your material spec and your tolerance."),
                "items": [
                    "Custom CNC and conventional machining for tool components, prototypes and batch manufacturing",
                    "Manufactured strictly to client drawing, material specification and tolerance",
                    "Carbon, alloy, stainless and Inconel; turning to &Oslash; 800 mm and 4- and 5-axis milling",
                    "Tolerances held to &plusmn;0.005 mm, finishes from as-machined to mirror",
                    "First-article inspection and dimensional reporting before batch release",
                    "Reverse engineering of obsolete or long-lead components",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ 02
    {
        "id": "engineering-advisory",
        "num": "02",
        "nav": "Engineering &amp; Technical Advisory",
        "eyebrow": "Engineering &amp; Technical Advisory",
        "title": "Technical Evaluation &amp; Engineering Support",
        "lead": ("Most procurement disputes are specification problems that surfaced too late. Our team "
                 "reads and interrogates the requisition <em>before</em> the enquiry goes out &mdash; so "
                 "deviations, substitutions and technical queries are settled at the bid stage rather than "
                 "at the inspection gate."),
        "blocks": [
            {
                "title": "Technical Bid Evaluation (TBE) &amp; Spec Alignment",
                "intro": ("Every bid is assessed against your Material Requisition line by line &mdash; not "
                          "summarised, not sampled &mdash; so you are comparing genuinely equivalent offers."),
                "items": [
                    "Line-by-line TBE against client Material Requisitions (MRs)",
                    "Technical clarification coordination between your engineering team and the manufacturer",
                    "Specification deviation management, documented and approved before award",
                    "Material substitutions evaluated on engineering merit, never on price alone",
                    "Compliance confirmed against the named specification <em>and edition</em>",
                    "Commercial and technical recommendation issued with a clear audit trail",
                ],
            },
            {
                "title": "Downhole Completion &amp; Wellbore Engineering Support",
                "intro": ("Completion hardware has to be selected against the actual well envelope, not a "
                          "catalogue headline. Share your well data and we will specify to it."),
                "items": [
                    "Well data analysis for HPHT, sour service (H&#8322;S) and deviated or horizontal well designs",
                    "Tool string configuration recommendations for cased-hole and open-hole completions",
                    "Elastomer and metallurgy selection against well fluid, temperature and pressure",
                    "Validation grade guidance (API 11D1 / ISO 14310) so bids are directly comparable",
                    "Derating review &mdash; ratings confirmed at your maximum downhole temperature",
                    "Conveyance and setting mechanism review against the intended running programme",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ 03
    {
        "id": "quality-inspection",
        "num": "03",
        "nav": "Quality Assurance, Inspection &amp; Compliance",
        "eyebrow": "Quality &amp; Compliance",
        "title": "QA/QC, Factory Inspection &amp; Compliance Management",
        "lead": ("Compliance is a deliverable with its own deadline, not paperwork collected after "
                 "production. Inspection is planned at order placement and the document pack is verified "
                 "before anything is released."),
        "blocks": [
            {
                "title": "Inspection &amp; Test Plan (ITP) Coordination",
                "intro": ("Inspectors are nominated and booked when the order is placed &mdash; not when "
                          "the factory declares readiness, which is where weeks are usually lost."),
                "items": [
                    "Dimensional inspection, hydrostatic test verification and non-destructive testing (NDT) monitoring",
                    "Facilitation and coordination of third-party inspection (TPI) agencies prior to dispatch",
                    "ITP agreed and witness / hold points fixed at order placement",
                    "Attendance at critical stages against your quality plan",
                    "Non-conformance reporting and disposition tracked to closure",
                    "Pre-dispatch release note issued only once every hold point is cleared",
                ],
            },
            {
                "title": "Certification &amp; Traceability Auditing",
                "intro": ("Every certificate is checked against the item it belongs to. An incomplete or "
                          "mismatched document pack strands a shipment at the border and fails an audit "
                          "years later."),
                "items": [
                    "Verification and release of complete documentation packages: Material Test Reports (MTRs), Mill Test Certificates (MTCs) and Certificates of Conformance (CoCs)",
                    "Heat and lot traceability from mill through to the delivered item",
                    "Hardness surveys and NACE MR0175 / ISO 15156 evidence for sour service grades",
                    "Strict adherence to API 11D1, API 5CT, API 5L, API 6A, API 7-1, ASME B16.5 and ISO equivalents",
                    "EN 10204 3.1 / 3.2 certification handled to the level your PO specifies",
                    "Document pack completed and approved <em>before</em> release, not after",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ 04
    {
        "id": "logistics-execution",
        "num": "04",
        "nav": "Supply Chain, Logistics &amp; Project Execution",
        "eyebrow": "Logistics &amp; Project Execution",
        "title": "End-to-End Logistics &amp; EXIM Management",
        "lead": ("Goods being ready is not the same as goods arriving. We manage the whole route &mdash; "
                 "factory gate to your stores &mdash; including the customs and documentation steps that "
                 "most product vendors treat as someone else's problem."),
        "blocks": [
            {
                "title": "Freight, Customs &amp; Export-Import Documentation",
                "intro": ("Cross-border competence is a specific capability. Incorrect classification or a "
                          "missing certificate of origin costs more in demurrage than the freight itself."),
                "items": [
                    "Turnkey logistics coordination from global mills and factories directly to project site or warehouse stores",
                    "Customs clearance, international shipping, packing and field marking to project specification",
                    "EXIM documentation, HS classification and certificates of origin",
                    "Marine insurance, Incoterm advice and import duty optimisation",
                    "Preservation, crating and marking suited to offshore and remote-site handling",
                    "Consignment tracking through to confirmed delivery into stores",
                ],
            },
            {
                "title": "Package Integration &amp; Project Procurement Management",
                "intro": ("On a multi-item campaign the coordination is the work. We consolidate it into a "
                          "single schedule, a single report and a single relationship."),
                "items": [
                    "Integrated sourcing packages for EPC construction, rig refurbishments and multi-well completion campaigns",
                    "Consolidated shipping to reduce freight cost and site handling",
                    "Phased delivery aligned to the drilling or construction schedule",
                    "Consolidated procurement reporting across every line and vendor",
                    "Dedicated account management with a single point of contact",
                    "One relationship, one invoice, one accountable owner",
                ],
            },
        ],
    },

    # ------------------------------------------------------------------ 05
    {
        "id": "strategic-alliances",
        "num": "05",
        "nav": "Strategic Alliances &amp; Market Integration",
        "eyebrow": "Strategic Alliances",
        "title": "Technology Consultation, Licensing &amp; Joint Ventures",
        "lead": ("For international manufacturers, this region is difficult to read from the outside and "
                 "difficult to serve on an export-only basis. We act as the advisory layer &mdash; "
                 "assessing where a technology fits, what it takes to get approved, and which commercial "
                 "structure makes sense before anyone commits capital."),
        "blocks": [
            {
                "title": "Technology Consultation &amp; Licensing Arrangements",
                "intro": ("Advisory first, structure second. We assess the opportunity honestly &mdash; "
                          "including when the answer is that the market is not ready for a given "
                          "technology."),
                "items": [
                    "Consulting on technology fit for Indian, Middle Eastern and Asia-Pacific well conditions and operating practice",
                    "Market assessment, demand sizing and competitive positioning before market entry",
                    "Route-to-market advice &mdash; direct export, distribution, licensing, local assembly or full JV",
                    "Structuring joint ventures, technology licensing and localised manufacturing partnerships",
                    "Local partner identification, screening and due diligence",
                    "Commercial structuring that protects the technology owner's intellectual property",
                ],
            },
            {
                "title": "Regulatory &amp; Operator Vendor Empanelment",
                "intro": ("Getting approved to bid is its own project. We run it, so your first tender is "
                          "not spent learning the process."),
                "items": [
                    "Domestic regulatory navigation and market entry support for global technology providers",
                    "Vendor empanelment with national oil companies and private operators",
                    "Tender registration, pre-qualification documentation and approval tracking",
                    "Local content and statutory compliance guidance",
                    "Local representation, after-sales and operational support",
                    "Ongoing account management with the operator once approved",
                ],
            },
        ],
    },
]

CTA = {
    "title": "Every Service, One Accountable Partner",
    "body": ("Whether you need a single technical bid evaluated, an emergency rig spare on a plane "
             "tonight, or a full multi-well procurement package managed end to end &mdash; talk to our "
             "technical desk. We respond to every enquiry within 24 hours."),
    "button": "Speak to a Technical Specialist",
}
