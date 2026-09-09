# -*- coding: utf-8 -*-
"""
Products & Equipment content for the Wellforge Energy Solutions website.

Taxonomy: six categories, each holding named product groups, each holding the
individual products. The category names, the group names and every product name
come from the approved product list supplied by Wellforge and are reproduced
verbatim. The supporting copy - category leads, introductions, specification
tables and compliance lists - is written for the web against that list and
restates capability already described elsewhere on the site (API/ISO
compliance, machining capability, EXIM handling, global vendor network).

Structure of each entry:
    num, slug, nav_title, title, short   identity and page routing
    meta_title / meta_desc / keywords    SEO
    icon                                 inline icon key from templates.py
    lead, intro, highlight               page opening copy
    applications                         optional (label, detail) pairs
    spec_caption, specs                  the specification table
    compliance_title, compliance         standards chips
    ranges                               the product groups and their products
    cta_*                                enquiry block
"""

CATEGORIES = [
    # ----------------------------------------------------------------- 01
    {
        "num": "01",
        "slug": "drilling-equipment-tools",
        "nav_title": "Drilling Equipment &amp; Tools",
        "title": "Drilling Equipment &amp; Tools",
        "short": "Drilling Equipment &amp; Tools",
        "meta_title": "Drilling Equipment &amp; Tools Supplier | Rig Machinery, BOPs, Drill String | Wellforge",
        "meta_desc": ("Drilling equipment and tools supplier - rotary tables, drawworks, swivels and hook "
                      "blocks, drill pipe and collars, mud motors and RSS, ram and annular BOPs, choke "
                      "and kill manifolds, elevators, slips and tongs."),
        "keywords": ("drilling equipment supplier, rig machinery supplier India, blowout preventer supplier, "
                     "drawworks rotary table swivel, drill pipe and drill collars, power tongs and elevators, "
                     "mud motor rotary steerable system"),
        "icon": "derrick",
        "lead": ("Rig machinery, drill string components, well control equipment and handling tools "
                 "&mdash; sourced from API-licensed manufacturers and delivered inspection-ready to your "
                 "rig site or warehouse."),
        "intro": [
            "Wellforge Energy Solutions supplies the equipment that turns the drill string and keeps the "
            "well under control. Our scope runs from individual rig machinery items and consumable wear "
            "parts through to complete onshore and offshore drilling rig assemblies and workover rig "
            "packages.",

            "Every item is sourced against the API specification that governs it &mdash; API 7K and API 8C "
            "for hoisting and rotary equipment, API 7-1 for rotary drill stem elements, API 16A and API 16C "
            "for drill-through and choke and kill equipment. Licence scope is verified for the specific "
            "product, size and pressure rating on your requisition, not simply the manufacturer's overall "
            "approval.",

            "Rig downtime is measured in hours, so this category is also where our emergency and "
            "critical-path sourcing capability is used most. Tell us the rig, the failed item and the "
            "required date and we will tell you within 24 hours what can be delivered and from where.",
        ],
        "highlight": {
            "title": "Well Control Equipment &mdash; Certification Before Dispatch",
            "body": ("Blowout preventers, manifolds and control units are supplied with the full "
                     "documentation package your quality plan requires: material test reports, hydrostatic "
                     "and function test records, and third-party inspection where the purchase order calls "
                     "for it. Pressure ratings are confirmed against your wellhead and casing programme "
                     "before the order is placed."),
        },
        "applications": [
            ("Onshore Drilling", "Land rig packages, rig moves, rig refurbishment and upgrades"),
            ("Offshore Drilling", "Platform and jack-up rig equipment, marine-rated packages"),
            ("Workover &amp; Intervention", "Workover rig assemblies, snubbing and pulling operations"),
            ("Directional Drilling", "Mud motors, RSS, stabilizers, jars and reamers"),
            ("Well Control", "BOP stacks, choke and kill systems, accumulator control units"),
            ("Rig Floor Operations", "Elevators, slips, tongs, safety clamps and handling equipment"),
        ],
        "spec_caption": "Key Specifications",
        "specs": [
            ("Rotary Table Sizes", "17&#189;&quot; &ndash; 60&#189;&quot;"),
            ("BOP Working Pressure", "2,000 &ndash; 15,000 psi"),
            ("Drill Pipe Sizes", "2&#8541;&quot; &ndash; 6&#8541;&quot;"),
            ("Hook Load Capacity", "Up to 1,000 tons"),
            ("Service", "Standard &amp; Sour (H&#8322;S) Service"),
            ("Standards", "API 7K &middot; 8C &middot; 7-1 &middot; 16A &middot; 16C"),
        ],
        "compliance_title": "Compliance Standards",
        "compliance": [
            "API Spec 7K &mdash; Drilling &amp; Well Servicing Equipment",
            "API Spec 8C &mdash; Hoisting Equipment",
            "API Spec 7-1 &mdash; Rotary Drill Stem Elements",
            "API Spec 16A &mdash; Drill-through Equipment",
            "API Spec 16C &mdash; Choke &amp; Kill Systems",
            "NACE MR0175 / ISO 15156 &mdash; Sour Service",
        ],
        "ranges": [
            {
                "title": "Drilling Rig Components (Rig Machinery)",
                "desc": ("Rotating, hoisting and power transmission equipment for the rig floor and "
                         "drawworks, supplied as individual items or as complete rig packages."),
                "std": "API 7K &middot; API 8C &middot; Onshore &amp; Offshore",
                "items": [
                    "Rotary Table",
                    "Hook Block",
                    "Swivel",
                    "Drawworks",
                    "Brake Band",
                    "Pneumatic Clutch",
                    "Air Tube Disc Clutch",
                    "Roller Kelly Bushing",
                    "Master Bushing",
                    "Drilling Rig Assemblies (Complete Onshore/Offshore Rigs)",
                    "Workover Rig Assemblies",
                    "Drilling Rotary Hose",
                ],
            },
            {
                "title": "Drill String and Downhole Tools",
                "desc": ("Drill string components and the downhole tools that steer, stabilise and free "
                         "it &mdash; specified against your well profile and drilling programme."),
                "std": "API 7-1 &middot; Directional &amp; Vertical",
                "items": [
                    "Drill Pipes &amp; Heavy-Weight Drill Collars",
                    "Mud Motors &amp; Rotary Steerable Systems (RSS)",
                    "Drilling Stabilizers &amp; Jars",
                    "IBOP (Internal Blowout Preventer)",
                    "Core Bits &amp; Reamers",
                ],
            },
            {
                "title": "Well Control Equipment",
                "desc": ("Blowout prevention and pressure control equipment, supplied with hydrostatic "
                         "and function test records and full material traceability."),
                "std": "API 16A &middot; API 16C &middot; Up to 15,000 psi",
                "items": [
                    "Ram Blowout Preventers (BOP)",
                    "Annular Blowout Preventers",
                    "Choke &amp; Kill Manifolds",
                    "BOP Control Units (Koomey Units)",
                ],
            },
            {
                "title": "Handling Tools",
                "desc": ("Rig floor handling and make-up equipment, sized to your tubular programme and "
                         "rated for the loads your operation runs."),
                "std": "API 7K &middot; API 8C",
                "items": [
                    "Manual &amp; Power Elevators",
                    "Rotary Slips &amp; Drill Collar Slips",
                    "Manual Tongs &amp; Power Tongs",
                    "Safety Clamps",
                ],
            },
        ],
        "cta_title": "Ready to Source with Wellforge?",
        "cta_body": ("Send us your material requisition, rig specification, or sourcing requirement and we "
                     "will respond within 24 hours."),
        "cta_button": "Send Enquiry",
        "cta_extra": True,
    },

    # ----------------------------------------------------------------- 02
    {
        "num": "02",
        "slug": "downhole-completion-octg",
        "nav_title": "Downhole, Completion &amp; OCTG",
        "title": "Downhole, Completion &amp; OCTG",
        "short": "Downhole, Completion &amp; OCTG",
        "meta_title": "OCTG &amp; Well Completion Products Supplier | Casing, Tubing, Packers | Wellforge",
        "meta_desc": ("API 5CT casing and tubing, premium gas-tight connections, line pipe, production "
                      "packers, bridge plugs, sliding sleeves, subsurface safety valves, sand control "
                      "screens, TCP guns and cementing products."),
        "keywords": ("OCTG supplier India, API 5CT casing and tubing supplier, premium connections, "
                     "production packers supplier, subsurface safety valve, sand control screens, "
                     "cementing float equipment, bridge plugs supplier"),
        "icon": "downhole",
        "lead": ("Oil country tubular goods, well completion hardware and cementing products &mdash; "
                 "sourced from API-approved mills and tool manufacturers and delivered with full material "
                 "traceability."),
        "intro": [
            "This category covers the string itself and everything that completes it. Wellforge supplies "
            "API 5CT casing and tubing across the full grade range, premium gas-tight connections for gas "
            "and HPHT wells, and the line pipe that carries production away from the wellhead.",

            "Alongside the tubulars we source the completion hardware that goes into the well &mdash; "
            "packers in mechanical, hydraulic and swellable configurations, bridge plugs and cement "
            "retainers, flow control equipment, subsurface safety valves, sand control screens and "
            "tubing-conveyed perforating systems.",

            "Cementing products complete the scope. Float equipment, centralizers, stop rings and cement "
            "heads are matched to the casing programme and the hole conditions rather than ordered from a "
            "catalogue, because standoff and float performance decide the quality of the cement job.",
        ],
        "highlight": {
            "title": "HPHT, Sour Service &amp; Premium Connection Capability",
            "body": ("Wellforge sources tubulars and completion tools rated for high-pressure, "
                     "high-temperature applications and sour service (H&#8322;S) environments, including "
                     "restricted-yield grades to NACE MR0175 / ISO 15156 and premium gas-tight "
                     "connections. Provide your well data and casing design and we will recommend the "
                     "appropriate grade, connection and tool specification."),
        },
        "applications": [
            ("Casing &amp; Cementing", "Conductor through production strings, float equipment, centralization"),
            ("Well Completion", "Packers, flow control, landing nipples, tubing strings"),
            ("Well Isolation", "Bridge plugs, cement retainers, plug and abandon"),
            ("Sand Control", "Wire-wrapped and premium mesh screens"),
            ("Perforation", "Tubing-conveyed perforating guns and shaped charges"),
            ("Well Safety", "Subsurface safety valves and surface-controlled systems"),
        ],
        "spec_caption": "Key Specifications",
        "specs": [
            ("Casing Sizes", "4&#189;&quot; &ndash; 20&quot;"),
            ("Tubing Sizes", "2&#8541;&quot; &ndash; 5&#189;&quot;"),
            ("Grades", "J55 &middot; K55 &middot; N80 &middot; L80 &middot; C90 &middot; T95 &middot; P110 &middot; Q125"),
            ("Pressure Rating", "Up to 15,000 psi"),
            ("Temperature", "Up to 400&deg;F (HPHT)"),
            ("Standards", "API 5CT &middot; API 5B &middot; API 11D1 &middot; API 10D"),
        ],
        "compliance_title": "Compliance Standards",
        "compliance": [
            "API Spec 5CT &mdash; Casing &amp; Tubing",
            "API Spec 5B &mdash; Threading &amp; Gauging",
            "API Spec 5L &mdash; Line Pipe",
            "API Spec 11D1 / ISO 14310 &mdash; Packers &amp; Bridge Plugs",
            "API Spec 10D &mdash; Bow-Spring Centralizers",
            "API Spec 14A &mdash; Subsurface Safety Valves",
            "NACE MR0175 / ISO 15156 &mdash; Sour Service",
        ],
        "ranges": [
            {
                "title": "OCTG and Pipes",
                "desc": ("Casing, tubing and line pipe from API-licensed mills, delivered with mill test "
                         "certificates and heat traceability from mill to delivered joint."),
                "std": "API 5CT &middot; API 5B &middot; API 5L",
                "items": [
                    "API Casing (Conductor, Surface, Intermediate, Production)",
                    "Production Tubing",
                    "Premium Gas-Tight Connections &amp; Couplings",
                    "Line Pipes for Oil &amp; Gas Transport",
                ],
            },
            {
                "title": "Well Completion Products",
                "desc": ("Completion hardware selected against the well envelope &mdash; pressure, "
                         "temperature, fluid and deviation &mdash; not against a catalogue headline."),
                "std": "API 11D1 &middot; ISO 14310 &middot; API 14A &middot; HPHT",
                "items": [
                    "Production Packers (Mechanical, Hydraulic, &amp; Swellable)",
                    "Bridge Plugs &amp; Cement Retainers",
                    "Sliding Sleeves &amp; Landing Nipples",
                    "Subsurface Safety Valves (SSSV)",
                    "Sand Control Screens (Wire-Wrapped &amp; Premium Mesh)",
                    "Tubing-Conveyed Perforating (TCP) Guns &amp; Charges",
                ],
            },
            {
                "title": "Cementing Products",
                "desc": ("Float equipment and centralization matched to the casing programme, hole "
                         "geometry and required standoff for a reliable primary cement job."),
                "std": "API 10D &middot; API 10F",
                "items": [
                    "Casing Float Shoes &amp; Float Collars",
                    "Centralizers (Bow-Spring &amp; Rigid)",
                    "Stop Rings &amp; Cementing Plugs",
                    "Cement Heads / Manifolds",
                ],
            },
        ],
        "cta_title": "Ready to Source with Wellforge?",
        "cta_body": ("Send us your casing design, completion programme, or material requisition and we will "
                     "respond within 24 hours."),
        "cta_button": "Send Enquiry",
        "cta_extra": True,
    },

    # ----------------------------------------------------------------- 03
    {
        "num": "03",
        "slug": "surface-production-artificial-lift",
        "nav_title": "Surface Production, Valves &amp; Artificial Lift",
        "title": "Surface Production, Valves &amp; Artificial Lift",
        "short": "Surface Production &amp; Artificial Lift",
        "meta_title": "Wellhead Equipment &amp; Artificial Lift Supplier | Christmas Trees, ESP, Pumpjacks | Wellforge",
        "meta_desc": ("Wellhead and flowline equipment supplier - casing and tubing heads, conventional "
                      "and block christmas trees, choke valves and actuators, production manifolds, "
                      "pumping units, sucker rods, rod pumps, ESP systems and gas lift equipment."),
        "keywords": ("wellhead equipment supplier, christmas tree supplier India, choke valve supplier, "
                     "artificial lift equipment, electrical submersible pump ESP, sucker rods and pumping "
                     "units, gas lift valves, production manifold"),
        "icon": "well",
        "lead": ("Wellhead equipment, flowline valves and artificial lift systems &mdash; API 6A compliant "
                 "and specified against your production profile, fluid and reservoir pressure."),
        "intro": [
            "Once the well is completed, production depends on the equipment above the ground. Wellforge "
            "supplies the full surface package &mdash; casing and tubing heads, conventional and block "
            "christmas trees, choke valves with hydraulic or electric actuation, and the high-pressure "
            "flowline and manifold assemblies that route production and injection.",

            "Wellhead equipment is supplied to API 6A, with the material class, temperature class, product "
            "specification level and performance requirement confirmed against your service conditions "
            "before the order is placed. Where the well produces H&#8322;S, material selection is verified "
            "to NACE MR0175 / ISO 15156 rather than assumed.",

            "The artificial lift range covers the main lift methods used across mature and low-pressure "
            "fields: beam pumping with sucker rod strings and downhole rod pumps, electrical submersible "
            "pumps for higher rate wells, and gas lift where reservoir and facility conditions favour it. "
            "Share your well and production data and we will source to the lift design your engineers have "
            "specified.",
        ],
        "highlight": {
            "title": "Specified Against Service Conditions, Not a Catalogue",
            "body": ("API 6A equipment carries a material class, temperature class, product specification "
                     "level and performance requirement, and they are not interchangeable. We confirm each "
                     "of them against your wellhead pressure, produced fluid and operating temperature "
                     "before award, and raise the technical query at bid stage rather than at the "
                     "inspection gate."),
        },
        "applications": [
            ("Wellhead &amp; Tree", "Casing and tubing heads, christmas trees, adapters and connectors"),
            ("Flow Control", "Choke valves, actuators, high-pressure flowline and fittings"),
            ("Production Gathering", "Production and injection manifolds, headers and skids"),
            ("Beam Pumping", "Pumping units, sucker rods, polished rods, downhole rod pumps"),
            ("Submersible Lift", "ESP assemblies, motors, cables and surface equipment"),
            ("Gas Lift", "Gas lift valves, side-pocket mandrels and installation tools"),
        ],
        "spec_caption": "Key Specifications",
        "specs": [
            ("Wellhead Pressure", "2,000 &ndash; 20,000 psi (API 6A)"),
            ("Bore Sizes", "1&#8541;&quot; &ndash; 13&#8541;&quot;"),
            ("Material Class", "AA &ndash; HH"),
            ("Temperature Class", "K &ndash; Y (&minus;60&deg;F to 350&deg;F)"),
            ("Service", "Standard &amp; Sour (H&#8322;S) Service"),
            ("Standards", "API 6A &middot; API 6D &middot; API 11B &middot; API 11E"),
        ],
        "compliance_title": "Compliance Standards",
        "compliance": [
            "API Spec 6A &mdash; Wellhead &amp; Christmas Tree Equipment",
            "API Spec 6D &mdash; Pipeline &amp; Piping Valves",
            "API Spec 11B &mdash; Sucker Rods",
            "API Spec 11E &mdash; Pumping Units",
            "API RP 11S &mdash; Electrical Submersible Pump Systems",
            "NACE MR0175 / ISO 15156 &mdash; Sour Service",
        ],
        "ranges": [
            {
                "title": "Wellhead Equipment &amp; Flowline Valves",
                "desc": ("Pressure-containing surface equipment from the casing head to the flowline, "
                         "supplied to API 6A with the documentation your quality plan requires."),
                "std": "API 6A &middot; API 6D &middot; Up to 20,000 psi",
                "items": [
                    "Casing Heads &amp; Casing Spools",
                    "Tubing Heads &amp; Tubing Adapters",
                    "Conventional &amp; Block Christmas Trees",
                    "Choke Valves &amp; Hydraulic/Electric Actuators",
                    "Flowline Products (High-Pressure Piping, Elbows, Tees)",
                    "Manifold Assemblies (Production &amp; Injection)",
                ],
            },
            {
                "title": "Artificial Lift Equipment and Accessories",
                "desc": ("Beam pumping, submersible and gas lift equipment, sourced to the lift design and "
                         "duty your production engineers have specified."),
                "std": "API 11B &middot; API 11E &middot; API RP 11S",
                "items": [
                    "Beam Pumping Units (Pumpjacks)",
                    "Sucker Rods, Polished Rods, &amp; Rod Guides",
                    "Downhole Rod Pumps",
                    "Electrical Submersible Pumps (ESP) &amp; Motors",
                    "Gas Lift Valves &amp; Side-Pocket Mandrels",
                ],
            },
        ],
        "cta_title": "Ready to Source with Wellforge?",
        "cta_body": ("Send us your wellhead specification, lift design, or material requisition and we will "
                     "respond within 24 hours."),
        "cta_button": "Send Enquiry",
        "cta_extra": True,
    },

    # ----------------------------------------------------------------- 04
    {
        "num": "04",
        "slug": "fluids-solids-control-workover",
        "nav_title": "Fluids, Solids Control &amp; Workover Processing",
        "title": "Fluids, Solids Control &amp; Workover Processing",
        "short": "Fluids, Solids Control &amp; Workover",
        "meta_title": "Mud Pumps, Solids Control &amp; Workover Equipment Supplier | Wellforge Energy Solutions",
        "meta_desc": ("Triplex and quintuplex mud pumps and fluid end spares, shale shakers and screens, "
                      "desanders, desilters and centrifuges, fishing and wellbore cleanout tools, "
                      "separators, heater-treaters and SCADA automation."),
        "keywords": ("mud pump spare parts supplier, triplex mud pump, shale shaker screens, decanting "
                     "centrifuge, solids control equipment India, fishing tools overshot spear, "
                     "production separator supplier, heater treater"),
        "icon": "fluids",
        "lead": ("Mud pumps and fluid end spares, solids control equipment, workover and fishing tools, "
                 "and surface processing vessels &mdash; the circulating and processing side of the "
                 "operation."),
        "intro": [
            "Wellforge supplies the equipment that moves, cleans and processes fluid. The mud pump range "
            "covers complete triplex and quintuplex units together with the fluid end modules, valves and "
            "seats, liners, pistons and packings that wear out fastest &mdash; the items that stop a rig "
            "when they are not on site.",

            "Solids control equipment follows the fluid back from the well: shale shakers and screens, "
            "desanders and desilters, decanting centrifuges, agitators and degassers. Screens are matched "
            "to the shaker make and model and to the cut point your mud programme requires, because a "
            "screen that does not fit is a screen that does not work.",

            "The workover and cleaning range covers casing scrapers, wellbore cleanout tools and the "
            "fishing tools needed when something is left in the hole. Surface processing completes the "
            "scope with test and production separators, heater-treaters, glycol dehydration and the "
            "metering and SCADA automation that reports what the facility is actually producing.",
        ],
        "highlight": {
            "title": "Strategic Stock on Fast-Moving Wear Parts",
            "body": ("Liners, pistons, packings, valves and seats are consumables with predictable "
                     "consumption and unpredictable failure timing. Wellforge holds strategic stock "
                     "agreements on fast-moving items and maintains parallel qualified sources, so a "
                     "fluid end failure does not become a multi-week lead time."),
        },
        "applications": [
            ("Mud Circulation", "Triplex and quintuplex pumps, fluid ends, pulsation control"),
            ("Solids Removal", "Shakers, desanders, desilters, centrifuges, degassers"),
            ("Wellbore Cleanup", "Casing scrapers, cleanout tools, bailers and sand pumps"),
            ("Fishing Operations", "Overshots, spears, mills and recovery tooling"),
            ("Production Testing", "2-phase and 3-phase test and production separators"),
            ("Facility Automation", "Multiphase flow metering and SCADA integration"),
        ],
        "spec_caption": "Key Specifications",
        "specs": [
            ("Mud Pump Power", "800 &ndash; 2,200 HP"),
            ("Pump Working Pressure", "Up to 7,500 psi"),
            ("Shaker Capacity", "Up to 1,200 GPM"),
            ("Centrifuge Bowl Speed", "Up to 3,900 RPM"),
            ("Separator Design", "ASME Section VIII, Division 1"),
            ("Standards", "API 7K &middot; API 13C &middot; API 12J &middot; ASME VIII"),
        ],
        "compliance_title": "Compliance Standards",
        "compliance": [
            "API Spec 7K &mdash; Drilling &amp; Well Servicing Equipment",
            "API RP 13C &mdash; Solids Control Screen Designation",
            "API Spec 12J &mdash; Oil &amp; Gas Separators",
            "ASME Section VIII &mdash; Pressure Vessels",
            "ATEX / IECEx &mdash; Hazardous Area Equipment",
            "Client-specific QCPs",
        ],
        "ranges": [
            {
                "title": "Mud Pump &amp; Spare Parts",
                "desc": ("Complete pump units and the fluid end wear parts that determine how long they "
                         "keep running between change-outs."),
                "std": "API 7K &middot; Up to 7,500 psi",
                "items": [
                    "Triplex &amp; Quintuplex Mud Pumps",
                    "Fluid End Modules &amp; Valves/Seats",
                    "Liners, Pistons, &amp; Packings",
                    "Pulsation Dampeners",
                ],
            },
            {
                "title": "Solid Control Equipment",
                "desc": ("Shaker, hydrocyclone and centrifuge equipment sized to your circulating rate, "
                         "with screens matched to the shaker model and required cut point."),
                "std": "API RP 13C &middot; ATEX / IECEx",
                "items": [
                    "Shale Shakers &amp; Shaker Screens",
                    "Mud Desanders &amp; Desilters",
                    "Decanting Centrifuges",
                    "Mud Agitators &amp; Degassers",
                ],
            },
            {
                "title": "Workover &amp; Cleaning",
                "desc": ("Wellbore cleanout and fishing tooling for workover, intervention and recovery "
                         "operations in cased hole."),
                "std": "Workover &amp; Intervention",
                "items": [
                    "Casing Scrapers &amp; Wellbore Cleanout Tools",
                    "Fishing Tools (Overshots, Spears, Mills)",
                    "Bailers &amp; Sand Pumps",
                ],
            },
            {
                "title": "Processing Vessels &amp; Automation",
                "desc": ("Surface separation, treating and measurement equipment, designed and code-stamped "
                         "to the pressure vessel standard your project specifies."),
                "std": "API 12J &middot; ASME VIII Div. 1",
                "items": [
                    "2-Phase &amp; 3-Phase Test/Production Separators",
                    "Heater-Treaters &amp; Glycol Dehydration Systems",
                    "Multiphase Flow Meters &amp; SCADA System Automation",
                ],
            },
        ],
        "cta_title": "Ready to Source with Wellforge?",
        "cta_body": ("Send us your pump model and part numbers, shaker make and screen sizes, or processing "
                     "specification and we will respond within 24 hours."),
        "cta_button": "Send Enquiry",
        "cta_extra": True,
    },

    # ----------------------------------------------------------------- 05
    {
        "num": "05",
        "slug": "casting-forging-machining",
        "nav_title": "Casting, Forging &amp; Machining Components",
        "title": "Casting, Forging &amp; Machining Components",
        "short": "Casting, Forging &amp; Machining",
        "meta_title": "Custom Casting, Forging &amp; CNC Machining for Oilfield | Wellforge Energy Solutions",
        "meta_desc": ("Sand, investment and centrifugal castings, open die and closed die forgings, forged "
                      "rings and flanges, and precision CNC turning, milling, boring and threading with "
                      "cladding, nitriding and phosphating surface treatments."),
        "keywords": ("custom casting supplier oilfield, investment casting lost wax, centrifugal casting, "
                     "open die forging, forged rings and flanges API, CNC machining oilfield components, "
                     "API threading services, cladding nitriding phosphating"),
        "icon": "machinery",
        "lead": ("Castings, forgings and precision machined components manufactured to your drawing, your "
                 "material specification and your tolerance &mdash; with first-article inspection before "
                 "batch release."),
        "intro": [
            "Where an item is obsolete, proprietary, or simply not worth importing, we make it. Wellforge "
            "operates a manufacturing route alongside its sourcing route, taking components from raw "
            "casting or forging through machining, heat treatment and surface finishing to a fully "
            "certified part.",

            "Work is manufactured strictly to client drawing, material specification and tolerance. "
            "Carbon, alloy, stainless and Inconel are all within scope; turning is available to "
            "&Oslash;&nbsp;800&nbsp;mm with 4- and 5-axis milling, and tolerances are held to "
            "&plusmn;0.005&nbsp;mm with finishes from as-machined to mirror.",

            "This capability also supports reverse engineering. Where a component is out of production or "
            "carries an unacceptable lead time, we can work from a sample or a measured drawing, agree the "
            "material and tolerance with your engineering team, and produce a first article for approval "
            "before committing to a batch.",
        ],
        "highlight": {
            "title": "First-Article Inspection Before Batch Release",
            "body": ("Nothing goes into batch production until a first article has been dimensionally "
                     "inspected and reported against the drawing, and approved by your engineering team. "
                     "Material certification is issued to EN 10204 3.1 or 3.2 as your purchase order "
                     "specifies, with full heat traceability from melt to finished component."),
        },
        "applications": [
            ("Valve &amp; Pump Bodies", "Heavy sand castings for pressure-containing housings"),
            ("Intricate Components", "Investment castings for complex structural geometry"),
            ("Tubular Components", "Centrifugal castings for sleeves and cylindrical parts"),
            ("High-Pressure Connections", "Closed die forgings for fittings and connections"),
            ("Large Rotating Parts", "Open die forgings for shafts, rings and cylinders"),
            ("Obsolete Spares", "Reverse engineering and low-volume batch manufacture"),
        ],
        "spec_caption": "Key Specifications",
        "specs": [
            ("Turning Capacity", "Up to &Oslash; 800 mm"),
            ("Milling", "4-axis &amp; 5-axis"),
            ("Tolerance", "&plusmn;0.005 mm"),
            ("Materials", "Carbon &middot; Alloy &middot; Stainless &middot; Inconel"),
            ("Surface Finish", "As-machined to mirror"),
            ("Certification", "EN 10204 3.1 / 3.2"),
        ],
        "compliance_title": "Compliance Standards",
        "compliance": [
            "ASTM A216 / A487 &mdash; Steel Castings",
            "ASTM A105 / A182 / A350 &mdash; Forged Fittings &amp; Flanges",
            "API Spec 6A &mdash; Material &amp; Temperature Classes",
            "ASME B16.5 &mdash; Pipe Flanges &amp; Flanged Fittings",
            "EN 10204 3.1 / 3.2 &mdash; Material Certification",
            "NACE MR0175 / ISO 15156 &mdash; Sour Service",
        ],
        "ranges": [
            {
                "title": "Custom Casting Components",
                "desc": ("Cast components produced by the route best suited to the part &mdash; section "
                         "thickness, geometry and volume decide the process, not habit."),
                "std": "ASTM A216 &middot; A487 &middot; EN 10204 3.1",
                "items": [
                    "Sand Castings (For heavy valves, pumps, and housings)",
                    "Investment Castings / Lost Wax (For intricate structural parts)",
                    "Centrifugal Castings (For tubular components and sleeves)",
                ],
            },
            {
                "title": "Industrial Forging Components",
                "desc": ("Forged components where grain flow and mechanical properties matter &mdash; "
                         "pressure-containing parts, rotating parts and load-bearing connections."),
                "std": "ASTM A105 &middot; A182 &middot; A350 &middot; API 6A",
                "items": [
                    "Open Die Forgings (For large shafts, rings, and cylinders)",
                    "Closed Die / Drop Forgings (For high-pressure connections and fittings)",
                    "Forged Rings &amp; Flanges (ANSI, API, and custom dimensions)",
                ],
            },
            {
                "title": "Precision Machining Services",
                "desc": ("Finish machining, API threading and surface engineering, with dimensional "
                         "reporting against the drawing before release."),
                "std": "&plusmn;0.005 mm &middot; API Threading",
                "items": [
                    "CNC Turning &amp; Milling (For tight-tolerance internal parts)",
                    "Heavy-Duty Boring &amp; Threading (For API-certified connections)",
                    "Surface Treatments &amp; Coatings (Cladding, Nitriding, Phosphating)",
                ],
            },
        ],
        "cta_title": "Ready to Source with Wellforge?",
        "cta_body": ("Send us your drawing, material specification and quantity and we will respond within "
                     "24 hours with a manufacturing proposal."),
        "cta_button": "Send Enquiry",
        "cta_extra": True,
    },

    # ----------------------------------------------------------------- 06
    {
        "num": "06",
        "slug": "plant-machinery-industrial-tools",
        "nav_title": "Plant, Machinery &amp; Industrial Tools",
        "title": "Plant, Machinery &amp; Industrial Tools",
        "short": "Plant, Machinery &amp; Industrial Tools",
        "meta_title": "Industrial Plant, Machinery &amp; Tools Supplier | Generators, Compressors, Workshop | Wellforge",
        "meta_desc": ("Industrial plant and machinery supplier - diesel and gas generator sets, "
                      "transformers and switchgear, MCC and VFD, air compressors, HVAC, boilers and heat "
                      "exchangers, workshop machinery, welding plant and hydraulic torque tools."),
        "keywords": ("industrial machinery supplier India, diesel generator set supplier, power "
                     "transformer switchgear, air compressor supplier, hydraulic torque wrench bolt "
                     "tensioner, workshop machinery, material handling equipment, plant equipment sourcing"),
        "icon": "wrench",
        "lead": ("Power generation and distribution, heavy industrial utilities, workshop machinery and "
                 "industrial tooling &mdash; the plant that keeps a site, a yard or a workshop running."),
        "intro": [
            "Beyond wellsite equipment, projects need power, air, heat, lifting and a workshop capable of "
            "supporting them. Wellforge sources that plant on the same terms as its oilfield scope: "
            "specification verified before enquiry, competitive multi-source comparison, and a single "
            "accountable point of contact through to delivery.",

            "The power range covers diesel and gas generator sets, transformers and switchgear, motor "
            "control centres and variable frequency drives. Utilities cover air compressors, industrial "
            "HVAC, boilers, heat exchangers, cooling towers and material handling equipment including "
            "overhead cranes, hoists and forklifts.",

            "Workshop machinery and industrial tooling complete the package &mdash; lathes, shaping "
            "machines and radial drills, welding and plasma cutting plant, pipe threading and grooving "
            "machines, hydraulic presses, and the hydraulic and pneumatic torque tooling used for "
            "controlled bolting on flanged joints.",
        ],
        "highlight": {
            "title": "Hazardous Area Classification Confirmed Before Award",
            "body": ("Equipment destined for a classified area carries a zone, gas group and temperature "
                     "class, and a certificate that has to match. We confirm the area classification "
                     "against the equipment certification &mdash; ATEX or IECEx as your specification "
                     "requires &mdash; before the order is placed, rather than discovering a mismatch at "
                     "site acceptance."),
        },
        "applications": [
            ("Site Power", "Generator sets, transformers, switchgear, MCC and VFD"),
            ("Compressed Air", "Screw, reciprocating and centrifugal compressors"),
            ("Process Utilities", "Boilers, heat exchangers, cooling towers, HVAC"),
            ("Material Handling", "Overhead cranes, hoists and forklifts"),
            ("Fabrication &amp; Workshop", "Lathes, drills, welding plant, presses, pipe machines"),
            ("Controlled Bolting", "Hydraulic torque wrenches, tensioners, flange alignment tools"),
        ],
        "spec_caption": "Key Specifications",
        "specs": [
            ("Generator Output", "10 kVA &ndash; 2,500 kVA"),
            ("Transformer Rating", "Up to 33 kV"),
            ("Compressor Capacity", "Up to 3,000 CFM"),
            ("Crane Capacity", "Up to 100 tons"),
            ("Torque Tool Range", "Up to 50,000 Nm"),
            ("Area Classification", "Safe Area &middot; ATEX / IECEx Zone 1 &amp; 2"),
        ],
        "compliance_title": "Compliance Standards",
        "compliance": [
            "IEC 60034 / IS 4722 &mdash; Rotating Electrical Machines",
            "IEC 60076 &mdash; Power Transformers",
            "ASME Section VIII &mdash; Pressure Vessels",
            "ATEX / IECEx &mdash; Hazardous Area Equipment",
            "ISO 4413 / 4414 &mdash; Hydraulic &amp; Pneumatic Systems",
            "CE Marking &amp; Client-specific QCPs",
        ],
        "ranges": [
            {
                "title": "Power Generation &amp; Distribution",
                "desc": ("Prime and standby power, distribution and motor control, sized to the site load "
                         "schedule and the area classification it sits in."),
                "std": "IEC 60034 &middot; IEC 60076 &middot; ATEX / IECEx",
                "items": [
                    "Industrial Diesel &amp; Gas Generator Sets",
                    "Power Transformers &amp; Switchgears",
                    "Motor Control Centers (MCC) &amp; Variable Frequency Drives (VFD)",
                ],
            },
            {
                "title": "Heavy Industrial Machinery &amp; Utilities",
                "desc": ("Compressed air, heating, cooling and lifting plant for process facilities, "
                         "fabrication yards and site infrastructure."),
                "std": "ASME VIII &middot; ISO 8573 &middot; FEM / IS 3177",
                "items": [
                    "Air Compressors (Screw, Reciprocating, &amp; Centrifugal)",
                    "Industrial Heating, Ventilation, &amp; Air Conditioning (HVAC) Units",
                    "Boilers, Heat Exchangers, &amp; Cooling Towers",
                    "Material Handling Equipment (Overhead Cranes, Hoists, &amp; Forklifts)",
                ],
            },
            {
                "title": "Workshop Machinery &amp; Equipment",
                "desc": ("Machine tools and fabrication plant for maintenance workshops, tool rooms and "
                         "pipe fabrication shops."),
                "std": "Workshop &amp; Fabrication",
                "items": [
                    "Heavy-Duty Lathe Machines, Shaping Machines, &amp; Radial Drills",
                    "Industrial Welding Machines &amp; Plasma Cutters",
                    "Pipe Threading, Cutting, &amp; Grooving Machines",
                    "Hydraulic Presses &amp; Bending Machines",
                ],
            },
            {
                "title": "Industrial Hand, Pneumatic &amp; Hydraulic Tools",
                "desc": ("Controlled bolting, powered hand tools and flange handling equipment for "
                         "maintenance, turnaround and construction work."),
                "std": "ISO 4413 / 4414 &middot; Up to 50,000 Nm",
                "items": [
                    "High-Torque Hydraulic Torque Wrenches &amp; Bolt Tensioners",
                    "Pneumatic Impact Wrenches, Grinders, &amp; Scalers",
                    "Heavy-Duty Manual Hand Tools (Slogging Spanners, Pipe Wrenches)",
                    "Flange Alignment &amp; Spreading Tools",
                ],
            },
        ],
        "cta_title": "Ready to Source with Wellforge?",
        "cta_body": ("Send us your equipment specification, load schedule, or material requisition and we "
                     "will respond within 24 hours."),
        "cta_button": "Send Enquiry",
        "cta_extra": True,
    },
]
