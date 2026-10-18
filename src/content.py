# -*- coding: utf-8 -*-
"""All words on artizanni.com live here. Edit, then run `python3 build.py`.

Truth rules (Artizanni marketing standard ART-KB-BRAND):
- Facts come only from the Company Fact Sheet, Corporate Profile 2026, the Project Portfolio or the MD.
- No invented clients, values, awards, testimonials or statistics. No "best in Nigeria".
- Panic-room / secure-space work is never shown: no photos, no clients, no specifications.
- Diaspora clients are private by default.
"""

SITE = {
    "domain": "artizanni.com",
    "name": "Artizanni",
    "legal": "Artizanni Business Services Limited",
    "rc": "RC 1065469",
    "founded": "2012",
    "incorporated": "17 September 2012",
    "address": "No. 30 Anthony Enahoro Crescent, Utako District, Abuja, FCT, Nigeria",
    "street": "No. 30 Anthony Enahoro Crescent",
    "locality": "Utako, Abuja",
    "region": "FCT",
    "geo": [9.0700, 7.4400],             # Utako district centre (approximate)
    "phone": "+234 803 920 4361",
    "phone_href": "+2348039204361",
    "whatsapp": "2348039204361",
    "email": "aec@artizanni.com",
    "md_email": "kola@artizanni.com",
    "alt_email": "artizanni@gmail.com",
    "md": "Engr. Akolade Maruf Ibrahim",
    "md_short": "Engr. Kola Ibrahim",
    "md_post": "MNSE, PMP · COREN Reg. No. R29685",
    "md_quals": "B.Tech Civil Engineering · MSc Housing (University of Ibadan) · MSc Information Technology",
    "tagline": "Design, engineering and construction under one accountable team.",
    "description": ("Artizanni is an Abuja-based design-build firm (RC 1065469, since 2012): architecture, civil, "
                    "structural and MEP engineering, construction, interiors, real estate, project and property "
                    "management, and an escrow-backed property service for Nigerians abroad."),
}

# ---------------------------------------------------------------- services
# slug, name, short, intro, what we do (list), how it works / notes, related photo keys, sectors
SERVICES = [
 dict(slug="design-build", name="Design & Build", icon="build",
  short="One contract, one team, one point of responsibility from brief to handover.",
  intro=("With design and build, the people who design your project are the people who price it and build it. "
         "You deal with one company and one contract, and design gaps cannot become someone else's problem."),
  items=["Brief, site appraisal and feasibility",
         "Architectural, structural and services design, coordinated in-house",
         "Bills of quantities, material and labour schedules, construction programme",
         "Construction of substructure, frame, envelope, services and finishes",
         "Testing, snagging, as-built records and handover",
         "Defects-period support and optional facility management"],
  notes=("Every drawing issued for construction is checked and sealed by a COREN-registered engineer, "
         "and by an ARCON-registered architect where the approving authority requires it."),
  photos=["duplex-3", "frame-4", "slab-2", "retail-1"]),

 dict(slug="architecture", name="Architecture", icon="arch",
  short="Briefs, concepts, construction drawings and development-permit packs.",
  intro=("Good architecture in Nigeria has to work with real plots, real budgets, approval offices and the "
         "climate. We design homes, estates, commercial and institutional buildings that can be approved, priced "
         "and built without surprises."),
  items=["Client brief and space programme",
         "Concept and schematic design with options",
         "Rendered 3D models and walk-through animation",
         "Planning and development-permit drawing packs",
         "Construction drawings, schedules and specifications",
         "Design for phased or incremental building",
         "Value engineering during design, so the drawings match the budget"],
  notes=("Our recorded design work includes architectural plans, 3D models and animation for a 1,680-bed student "
         "village delivered on a PPP model, and architectural visualisation for a central mosque in Ikoyi, Lagos."),
  photos=["duplex-1", "duplex-5", "brick-clad", "site-2"]),

 dict(slug="engineering", name="Civil, Structural & MEP Engineering", icon="eng",
  short="Structural design, civil works, drainage, foundations and building services.",
  intro=("Engineering is our founding discipline. The practice is led by a COREN-registered civil and structural "
         "engineer, and our designs come from people who also stand on site when the concrete is poured."),
  items=["Structural design of reinforced concrete and steel buildings",
         "Foundations, retaining structures and heavy equipment plinths",
         "Roads, drainage, erosion control and site infrastructure",
         "Geotechnical / soil investigation coordination",
         "Mechanical, electrical and plumbing (MEP) design and coordination, including solar and back-up power",
         "Structural integrity assessments of existing buildings",
         "Independent technical review of designs prepared by others"],
  notes=("Typical recorded work: an 80-tonne, 60MVA transformer plinth at a 132/33kV substation, substation control "
         "building structural design, and the full structural and civil design of a student village "
         "(buildings, roads and drainage networks)."),
  photos=["slab-1", "trench-rebar", "stair-2", "frame-1"]),

 dict(slug="construction", name="Construction & Civil Works", icon="crane",
  short="Buildings, substations, dams, drainage, reclamation and roads, self-delivered.",
  intro=("We build what we design, and we build for other designers too. Our site teams have delivered "
         "reinforced-concrete frames, power-infrastructure civils, dam rehabilitation, cofferdams, channelisation "
         "and land reclamation."),
  items=["Residential, commercial and industrial buildings",
         "Power infrastructure civils: substation earthworks, foundations, access roads, fencing",
         "Water works: cofferdams, dam and reservoir rehabilitation, dewatering",
         "Drainage, gabion revetment, erosion control and land reclamation",
         "Roads, hardstanding, kerbs and external works",
         "Specialist sub-contract work for main contractors"],
  notes=("We own and operate earthmoving and compaction plant, including an SDLG LG953N wheel loader acquired in 2021, and hire "
         "specialist equipment where a scheme needs it. Where a group company supplies, we disclose it and compare at least one independent quote."),
  photos=["reclaim-aerial", "cofferdam", "channel-gabion", "frame-2"]),

 dict(slug="interiors", name="Artizanni Interiors", icon="int",
  short="Interior design, fit-out, joinery and furnishing in Abuja, Lagos and Port Harcourt.",
  intro=("Artizanni Interiors carries our finishing work: homes, offices, retail and hospitality spaces. Tolerances "
         "are visible here, so we plan fit-outs around drying times, delivery dates and the day you need to open."),
  items=["Interior design concepts, mood boards and space planning",
         "Materials, finishes and FF&E schedules (local and imported)",
         "Ceilings, partitions, tiling, stone and decoration",
         "Kitchens, wardrobes, counters and bespoke joinery",
         "Lighting schemes and electrical fit-out",
         "Retail fit-out: shelving, gondolas and display systems"],
  notes="Fit-outs are run as projects: a fixed programme, a snag list and a handover pack, not an open-ended job.",
  photos=["int-3", "int-1", "int-6", "int-5"]),

 dict(slug="real-estate", name="Real Estate & Land", icon="land",
  short="Land sourcing, title verification, acquisition and development.",
  intro=("Most property losses in Nigeria start before anything is built: the wrong title, the wrong seller or "
         "the wrong plot. We help you find, verify and secure land or property, then develop it."),
  items=["Land and property sourcing against your brief, with comparable-price analysis and negotiation support",
         "Title due diligence with a lawyer and surveyor (C of O, Governor's consent, survey charting, excision)",
         "Acquisition, documentation and perfection of title",
         "Feasibility studies and development appraisals",
         "Estate planning, design and delivery",
         "Technical due diligence before purchase: site, soil, drainage, access and structural condition",
         "Sales advisory for owners disposing of property",
         "Customer due diligence (KYC/AML) as required for real-estate transactions"],
  notes=("We are SCUML-registered. Real-estate transactions require customer due diligence before any money changes hands."),
  photos=["site-2", "reclaim-aerial-2", "duplex-6", "yard-2"]),

 dict(slug="project-management", name="Project & Property Management", icon="pm",
  short="Cost, programme and quality control for your project, then care of the asset.",
  intro=("If you already have a designer or a contractor, we can stand on your side of the table: plan the work, "
         "check the quantities, certify valuations and report progress, then manage the property after handover."),
  items=["Project planning, programmes and procurement plans",
         "Bills of quantities, cost plans and valuation checks",
         "Site supervision, quality inspections and progress reports with photos",
         "Contract administration, variations and payment certificates",
         "Property and facility management: tenant sourcing and screening, lease administration, rent collection",
         "Planned and reactive maintenance with documented work orders and service-charge reporting",
         "Long-term estate management strategy"],
  notes=("Recorded work includes a construction programme, a procurement plan and a ten-year inflation-tied facility "
         "and estate management strategy for a student hostel scheme."),
  photos=["site-1", "slab-3", "retail-3", "panel-1"]),

 dict(slug="personnel", name="Built-Environment Personnel", icon="people",
  short="Engineers, supervisors and skilled artisans supplied and managed for your project.",
  intro=("Projects stall when the right people are not on site. We supply and manage qualified engineers, site "
         "supervisors, foremen and artisans for clients' projects, on short or long engagements."),
  items=["Site engineers and supervisors",
         "Foremen and trade gangs: masons, steel fixers, carpenters, tilers, plumbers, electricians",
         "Quantity surveying and planning support",
         "HSE officers and storekeepers",
         "Vetting, onboarding and site induction",
         "Supervision and replacement cover"],
  notes="Professionals who want to be considered for placements can register their interest below.",
  photos=["frame-3", "trench-rebar-2", "site-1", "stair-1"]),

 dict(slug="secure-spaces", name="Secure Spaces", icon="shield",
  short="Discreet design and construction of safe rooms for homes and offices.",
  intro=("We design and build protected rooms within new and existing buildings. This work is handled on a "
         "strict need-to-know basis: we do not publish projects, photographs, clients or specifications."),
  items=["Confidential consultation at a place of your choosing",
         "Protection level agreed with you before design",
         "Integration with the building's structure, services and escape routes",
         "Small, vetted delivery team",
         "Confidential documentation and handover"],
  notes="Please do not send plans or addresses on WhatsApp. Ask for a call and we will arrange a private consultation.",
  photos=[]),
]

DIASPORA = dict(
  slug="diaspora", name="Build from Abroad",
  short="For Nigerians abroad: your money is held in escrow by First Trustees and released only against verified milestones.",
)

# ---------------------------------------------------------------- sectors (portfolio chapters)
SECTORS = [
 dict(slug="water", name="Water Resources & Marine Works", hero="cofferdam",
  standfirst="Cofferdams, barrage works, dam rehabilitation and reservoir expansion, built in the wet.",
  body=["Our water work runs from temporary works in live watercourses to the rehabilitation of dams in service. "
        "Dewatering sequences, rock armour, geomembrane protection and working platforms that must survive a rising river "
        "shape how we manage risk on every other project.",
        "As specialist sub-contractor we have worked on a cofferdam for the Ogun State Waterworks barrage at Akomoje, "
        "Abeokuta (an AFD-funded project), and on reservoir expansion and rehabilitation of irrigation dams in Osun, "
        "Nasarawa, Benue and Cross River States."],
  facts=[("Cofferdam", "Ogun State Waterworks barrage, Akomoje"), ("Dams", "Osun · Nasarawa · Benue · Cross River"),
         ("Methods", "Dewatering · rock armour · geomembrane")]),
 dict(slug="power", name="Power Infrastructure", hero="deck-tower",
  standfirst="Civil and structural works for 132/33kV transmission substations.",
  body=["A 60MVA transformer arrives on a programme fixed months earlier and sets down on a plinth whose tolerances "
        "were fixed at design stage. We have delivered earthworks design and construction, transformer and equipment "
        "foundations, geotechnical investigation, site layout and control-building structural design for substations "
        "in South-Western and North-Central Nigeria.",
        "Our scope has also covered access roads, perimeter fencing, borehole water supply and staff quarters: the full "
        "civil envelope around the electrical works."],
  facts=[("Voltage class", "132/33kV substations"), ("Heaviest plinth", "80-tonne, 60MVA transformer"),
         ("Perimeter", "1,800m substation fence")]),
 dict(slug="drainage", name="Drainage, Erosion Control & Reclamation", hero="reclaim-aerial",
  standfirst="Channelisation, gabion revetment and land reclamation: building ground where there was water.",
  body=["Our erosion control work began on the Osogbo–Ikeja high-voltage transmission line network and now extends to "
        "channelisation and reclamation schemes in Lagos.",
        "The methods are conventional (dredge, line, protect, fill, compact); the sequencing is what matters. Gabions "
        "are prepared ahead of the working front, geotextile goes down before the hydrology changes, and fill is placed "
        "and compacted in layers that can be tested."],
  facts=[("Transmission corridor", "Erosion control, Osogbo–Ikeja HV lines"), ("Lagos", "Channel and reclamation works"),
         ("Systems", "Gabion · stone pitching · geotextile")]),
 dict(slug="residential", name="Residential Development", hero="duplex-3",
  standfirst="Detached and semi-detached homes and estates, from setting out to handover.",
  body=["Housing is repetitive work, and repetition is where a builder's systems show. We run residential schemes as "
        "production: substructure across several plots, then blockwork, roof, render and finishes moving through in "
        "sequence so every trade has a continuous working front.",
        "Our work covers 2- and 3-bedroom semi-detached staff quarters on an infrastructure site and private duplexes "
        "with classical detailing, arched openings and moulded entrance bays."],
  facts=[("Unit types", "Semi-detached · detached duplexes"), ("Scope", "Setting out to handover"),
         ("Method", "Trade-sequenced production")]),
 dict(slug="structures", name="Structures in Frame", hero="slab-2",
  standfirst="Reinforced concrete from foundation to roof.",
  body=["Most of what a builder is judged on is hidden by handover: foundations, column cages, formwork, slab "
        "reinforcement, stairs and the blockwork that follows the frame.",
        "Reinforcement is offered for inspection before every pour, and we have provided foundation setting-out for "
        "multi-storey framed buildings as a specialist sub-contractor."],
  facts=[("Substructure", "Raft · pad · strip foundations"), ("Superstructure", "RC frames and suspended slabs"),
         ("Quality gate", "Inspection before each pour")]),
 dict(slug="mep", name="Mechanical & Electrical", hero="p296",
  standfirst="Ductwork fabricated on site, services routed before ceilings close, conduit set into the structure as it rises.",
  body=["We fabricate and install galvanised sheet-metal ductwork on our own projects, forming sections on site so that runs follow "
        "the structure as built rather than as drawn. On retail and industrial work this removes a common cause of delay: the clash "
        "found after the ceiling grid is up.",
        "Electrical containment follows the same principle. Conduit and back boxes are set into blockwork during construction, and "
        "external routes are laid and protected before hard landscaping closes over them."],
  facts=[("Ductwork", "On-site fabrication, galvanised sheet"), ("Coordination", "Routed against as-built structure"),
         ("Containment", "Conduit cast and chased in during build")]),
 dict(slug="commercial", name="Commercial & Retail", hero="retail-1",
  standfirst="Trading buildings that must open on the date advertised.",
  body=["In retail the client's return starts the day the doors open, so the fit-out programme, not the frame, is the "
        "critical path. We seal the envelope early, route services before ceilings close and sequence finishes so "
        "shop-fitting can start in one zone while building continues in another."],
  facts=[("Building types", "Plazas · supermarkets · shopfronts"), ("Scope", "Substructure to signage"),
         ("Model", "Design & build or build-only")]),
 dict(slug="industrial", name="Industrial, Warehousing & Cold Chain", hero="panel-1",
  standfirst="Portal frames, clear-span stores, insulated cold rooms and the yards that serve them.",
  body=["A clear span is only useful if the floor takes the load, the doors suit the vehicle and the envelope holds the "
        "temperature. We build steel-framed stores, insulated panel cold rooms and chilled stores, hardstanding and "
        "loading canopies, and we erected a prefabricated engineering camp for the AKK gas pipeline project."],
  facts=[("Structures", "Portal frames · clear-span stores"), ("Cold chain", "Insulated panel cold rooms"),
         ("Camp", "Prefabricated camp, AKK project")]),
 dict(slug="interiors", name="Interiors, Fit-out & Finishes", hero="int-3",
  standfirst="The last ten per cent: the finishes your clients and family actually touch.",
  body=["Completed work includes food production areas fitted out to operating standard, retail floors with shelving "
        "and gondola systems, tiled wet areas, stone worktops cut and finished on site, and full decoration packages."],
  facts=[("Brand", "Artizanni Interiors"), ("Cities", "Abuja · Lagos · Port Harcourt"),
         ("Packages", "Tiling · joinery · stone · shop-fitting")]),
 dict(slug="roads", name="Roads, Paving & External Works", hero="channel-road",
  standfirst="Access roads, estate carriageways and hardstanding.",
  body=["Access is the first thing built and the last thing finished. We construct substation access roads, estate "
        "roads and yards from formation and sub-base through kerbing to surfacing and drainage connection."],
  facts=[("Road types", "Access roads · estate roads · yards"), ("Scope", "Formation to surfacing"),
         ("Related", "Boundary walls · paving · drainage")]),
 dict(slug="consultancy", name="Design & Consultancy", hero="site-1",
  standfirst="Feasibility, design, quantities and programmes before anyone breaks ground.",
  body=["About half of our recorded commissions are consultancy. For a 1,680-bed student village on a public–private "
        "partnership within a Federal Government university, we prepared the financial feasibility study, the "
        "architectural, structural and civil design, bills of quantities, material and labour schedules, rendered 3D "
        "models and animation, the construction programme, the procurement plan and a ten-year facility and estate "
        "management strategy.",
        "Because we build, we can price and programme what we design."],
  facts=[("Feasibility", "1,680-bed student village, PPP"), ("Design", "Architecture · structures · civils"),
         ("Commercial", "BoQs · procurement plans")]),
]

# Transcribed from the EPC Contracting Experience schedule in the Corporate Profile.
# sector keys map to SECTORS slugs. Years and values are left out until the MD supplies them.
REGISTER = [
 (1, "Rhuoga Energy Limited", "Earthwork design and construction for a 132/33kV transmission substation, South-Western Nigeria", "Design & build consultant / sub-contractor", "power"),
 (2, "Rhuoga Energy Limited", "Design of a plinth foundation for an 80-tonne, 60MVA transformer at a 132/33kV substation, North-Central Nigeria", "Design consultant", "power"),
 (3, "Rhuoga Energy Limited", "High-voltage transmission substation site layout design", "Design consultant", "power"),
 (4, "Novatis Estates Limited", "Financial feasibility study and report for a 1,680-bed student village within a Federal Government university, on a PPP model", "Consultant", "consultancy"),
 (5, "Rhuoga Energy Limited", "Construction of 1,800m perimeter fence at a transmission substation", "Sub-contractor", "power"),
 (6, "Novatis Estates Limited", "Architectural plans and detailed design of a high-capacity student village with sports facilities, shopping mall and maintenance facilities", "Design consultant", "consultancy"),
 (7, "Novatis Estates Limited", "Detailed structural and civil engineering design of the student village: buildings, roads and drainage networks", "Design consultant", "consultancy"),
 (8, "Novatis Estates Limited", "Quantity and cost estimation of the student village: bills of quantities, material and labour schedules", "Design consultant", "consultancy"),
 (9, "Novatis Estates Limited", "Rendered 3D models and internal and external animation of the student village", "Design consultant", "consultancy"),
 (10, "Rhuoga Energy Limited", "Construction of 2- and 3-bedroom semi-detached staff quarters at a transmission substation, South-West", "Sub-contractor", "residential"),
 (11, "West Transmission Line Network", "Erosion control for HV transmission lines, Osogbo–Ikeja", "Sub-contractor", "drainage"),
 (12, "Wiz Engineering", "Prefabricated engineering camp erection for the AKK oil and gas project", "Sub-contractor", "industrial"),
 (13, "AFD-funded project", "Cofferdam for the Ogun State Waterworks barrage, Akomoje, Abeokuta, Ogun State", "Sub-contractor", "water"),
 (14, "Novatis Estates Limited", "Construction programme, procurement plan and ten-year inflation-tied facility and estate management strategy for the student hostels", "Consultant", "consultancy"),
 (15, "Dolphin Estate Muslim Community", "Rendered 3D models and animation for the Dolphin Estate central mosque, Ikoyi, Lagos", "Design consultant", "consultancy"),
 (16, "Rhuoga Energy Limited", "High-voltage transmission substation site layout design", "Design consultant", "power"),
 (17, "Rhuoga Energy Limited", "Geotechnical / soil investigation for a high-voltage transmission substation", "Sub-contractor", "power"),
 (18, "Poadit Constructions Ltd", "Setting out foundations for multi-storey framed buildings", "Sub-contractor", "structures"),
 (19, "Rhuoga Energy Limited", "Construction of 60MVA transformer equipment foundation", "Sub-contractor", "power"),
 (20, "Rhuoga Energy Limited", "Design and construction of substation access roads", "Sub-contractor", "roads"),
 (21, "Rhuoga Energy Limited", "Structural design of a high-voltage substation control building", "Design sub-contractor", "power"),
 (22, "Rhuoga Energy Limited", "Water borehole drilling", "Sub-contractor", "water"),
 (23, "Isaac Udezue and Associates Ltd", "Rehabilitation of irrigation dam at Ilesha, Osun State", "Sub-contractor", "water"),
 (24, "Enamux Design Associates Ltd", "Rehabilitation and reservoir expansion of Marmara Dam, Nasarawa State", "Sub-contractor", "water"),
 (25, "Enamux Design Associates Ltd", "Rehabilitation of irrigation dam at Wannune, Benue State", "Sub-contractor", "water"),
 (26, "Isaac Udezue and Associates Ltd", "Rehabilitation and reservoir expansion of Buyam Dam, Cross River State", "Sub-contractor", "water"),
]

STAGES = [
 ("01", "Brief & feasibility", "Site visit, brief, budget check, title and approvals review. Most project risk is priced or ignored here."),
 ("02", "Design", "Architecture, structure and services designed together, with 3D views where you need to see it before you build."),
 ("03", "Quantities & programme", "Bills of quantities, material schedules, procurement plan and programme, prepared by the team that will build to them."),
 ("04", "Construction", "Self-delivered site works with weekly photo reports, inspections before every pour and certified valuations."),
 ("05", "Handover", "Testing, snagging, as-built drawings, operation manuals and keys against a closed defects list."),
 ("06", "Aftercare", "Defects-period support, then optional property and facility management."),
]

# Diaspora escrow milestones (delivery stage model, default set; adjusted per contract)
MILESTONES = [
 ("M0", "Title verified and permit obtained", "Lawyer's title report; permit copy"),
 ("M1", "Site cleared, set out, foundation complete", "Geotagged photos and video; foundation inspection record"),
 ("M2", "Ground-floor slab / DPC", "7-day concrete cube results; photos; QS valuation"),
 ("M3", "Frame to roof level (each floor a sub-milestone)", "28-day cube results; reinforcement inspection sign-offs"),
 ("M4", "Roof covered", "Photos and valuation"),
 ("M5", "Services first fix, windows, plaster", "Inspection records"),
 ("M6", "Finishes, services second fix, external works", "Draft snag list"),
 ("M7", "Practical completion and handover", "Handover certificate, as-built drawings, keys"),
 ("M8", "End of defects liability period", "Defects closed; retention released"),
]

DIASPORA_FAQ = [
 ("Do I pay anything up front?",
  "No. There are no upfront payments. Once scope and price are agreed, construction funds go into escrow with First Trustees, and every "
  "payment after that is pro rata against certified progress."),
 ("Who holds my money?",
  "Your construction funds are paid into an escrow arrangement with First Trustees, an independent trustee company, not into Artizanni's account. "
  "Funds are released to us in stages, only when the milestone agreed in your contract has been completed and evidenced."),
 ("How do I know a milestone has really been reached?",
  "For every release we prepare a Milestone Verification Pack: dated, geotagged photographs, a video walk-through, inspection and test records "
  "(for example concrete cube results) and a quantity surveyor's valuation. It is countersigned by our Managing Director and, where your "
  "escrow deed requires it, by an independent verifier."),
 ("Do I need to buy the land first?",
  "No. We can source land against your brief. Before any money moves for land, a lawyer and surveyor carry out title due diligence "
  "(C of O, Governor's consent, survey charting, excision and family-land checks) and you receive a go / no-go report."),
 ("Will I get regular updates?",
  "Yes: a weekly written report with photos and video, scheduled calls in your time zone, and the verification pack at every milestone."),
 ("What do you need from me to start?",
  "A short discovery call, then identity and source-of-funds checks. As a SCUML-registered business we must complete customer due "
  "diligence before any real-estate transaction. Your details are kept confidential."),
 ("Should I give someone power of attorney?",
  "Only after legal advice, and never as a substitute for escrow. A power of attorney can be misused; the escrow and milestone structure "
  "is designed so you do not have to rely on any one person's honesty."),
 ("Can you manage the property after it is built?",
  "Yes. We offer property and facility management after handover: tenancy support, maintenance and periodic inspection reports."),
]

GENERAL_FAQ = [
 ("Which locations do you work in?",
  "We are based in Utako, Abuja. Our recorded work spans Lagos, Ogun, Osun, Nasarawa, Benue and Cross River States and transmission sites in the South-West and North-Central. "
  "Interiors are offered in Abuja, Lagos and Port Harcourt. Tell us where your project is and we will confirm."),
 ("Do you only take design-and-build contracts?",
  "No. You can appoint us for design only, engineering only, construction to someone else's design, project management, or interiors."),
 ("How do you price a project?",
  "After the brief and a site visit we prepare an estimate that states its basis, date and accuracy. A firm price follows design and a "
  "bill of quantities. Prices show VAT separately."),
 ("Are your designs approved and sealed?",
  "Engineering drawings are sealed by a COREN-registered engineer; architectural drawings for permits are sealed by an ARCON-registered architect."),
]

STATES = ["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo",
          "Ekiti", "Enugu", "FCT (Abuja)", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos",
          "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara"]

GROUP = [
 ("Yellowmetal", "https://yellowmetal.store/", "Plant and equipment hire"),
 ("Buildocrat", "https://buildocrat.store/", "Building materials and Price Lock"),
 ("Nigeria Construction Rate Book", "https://rates.buildocrat.store/", "Weekly construction prices"),
]

# Portfolio chapter order (Project Portfolio 2026)
_ORDER = ["water", "power", "drainage", "commercial", "industrial", "residential", "structures", "mep", "interiors", "roads", "consultancy"]
SECTORS.sort(key=lambda s: _ORDER.index(s["slug"]))

# Status as printed in the Corporate Profile 2026, Selected Projects (sheet 11). All other rows: Completed.
REGISTER_STATUS = {5: "Ongoing", 10: "Ongoing"}

# ---------------------------------------------------------------- from the Corporate Profile 2026 and Project Portfolio 2026
PROFILE = dict(
  mission="To deliver buildings and infrastructure of dependable quality: on programme, on budget, and exactly as specified.",
  vision="To be the most trusted delivery partner for Nigerians building at home, wherever in the world they live.",
  how="Lean, technology-enabled teams; transparent milestones; independent escrow; strict confidentiality.",
  md_quote=("We built Artizanni to prove a simple thing: a home, a road or a building can be delivered exactly as promised, "
            "even when the owner is on another continent. Certainty is the product."),
  story=["Artizanni was incorporated in Abuja in 2012 as a general contractor. What we became was set less by strategy than by the "
         "work that came in: earthworks for a transmission substation, then a transformer plinth, then a cofferdam in a live river, "
         "then housing, then retail, then the drainage and reclamation schemes that now occupy much of our plant.",
         "Each of those moves taught us something we could not subcontract: how a barrage behaves when you dewater it, how a 60MVA "
         "transformer arrives and what it will not forgive, how a retail programme collapses if the ductwork is drawn rather than "
         "measured. We kept that knowledge in-house. That is why we design, quantify, programme and build, rather than doing only one of them."],
  team=("A multidisciplinary bench of architects, civil and structural engineers, quantity surveyors and mechanical and electrical "
        "engineers, working as one delivery team."),
  memberships="COREN · NSE · NIA · NIQS · PMP",
  workforce=("A trained artisan base drawn from Nigeria, Ghana and Togo, selected for close attention to finish quality, and a directly "
             "employed site team for setting out, reinforcement, formwork and finishes."),
  model=("Central coordination, remote project teams and lean, six-sigma-informed practice keep overheads low and quality consistent on every site."),
  coverage="Head office in Utako, Abuja, with active project delivery in Lagos and Port Harcourt, and remote delivery and reporting for clients across the diaspora.",
  serves="Real-estate developers, corporate and security organisations, community associations, private individuals, and Nigerian professionals living abroad.",
  nda="Every engagement is governed by a non-disclosure agreement. Client and project identities are protected as standard.",
  payments="There are no upfront payments. Every payment is pro rata against certified progress: the client pays Artizanni, and Artizanni pays the team.",
)

PLANT = [("Wheel loader", "SDLG LG953N, owned, acquired 2021"), ("Compaction", "Vibrating rollers"),
         ("Earthmoving", "Excavators and dozers, deployed with hired long-reach units where needed"),
         ("Fabrication", "In-house sheet-metal ductwork"), ("Supply partner", "SMT Nigeria Ltd")]

NUMBERS = [("132/33", "kV class of transmission substations served with civil works"),
           ("1,800m", "Perimeter fence built at a transmission substation"),
           ("1,680", "Student-village beds taken through full feasibility and design"),
           ("60MVA", "Transformer foundation designed and built")]

# Three-stage journey (Corporate Profile, sheet 06)
JOURNEY = [("Pre-contract", "Design & define", "Brief, feasibility, design and a fixed cost plan. Nothing is committed until scope and price are agreed."),
           ("Pre-contract", "Secure & mobilise", "Proposal accepted, funds placed in escrow or trust, procurement and site mobilisation."),
           ("Post-contract", "Build & hand over", "Construction to programme, payments released on verified milestone valuations, then handover.")]

# Ways to work with us (Corporate Brochure)
ENGAGEMENTS = [("Advisory only", "Transaction advisory, title and technical due diligence, and investment appraisal as a standalone service."),
               ("Design & engineering", "Architecture and engineering packages for clients building with their own contractor."),
               ("Design & build", "One contract from concept through certified handover."),
               ("Turnkey from abroad", "End to end for remote owners: acquire, design, build and manage, with escrow-backed milestones."),
               ("Management only", "Property and facility management for buildings you already own.")]

# Selected clients & partners (Corporate Profile, sheet 10)
CLIENTS = [("Rhuoga Energy Limited", "Power · transmission"), ("Novatis Estates Limited", "Real estate · PPP"),
           ("Ogun State Waterworks", "Water · AFD-funded"), ("Wiz Engineering", "Oil & gas"),
           ("West Transmission Line Network", "HV transmission"), ("Dolphin Estate Muslim Community", "Community"),
           ("Isaac Udezue & Associates", "Dams · water"), ("Enamux Design Associates", "Dams · water"),
           ("Poadit Constructions Ltd", "Foundations")]
