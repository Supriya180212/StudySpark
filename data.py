"""Static study content: syllabus, quiz questions and map-work lists.

Kept in Python so the database only stores per-user progress.
"""

_RAW = [
    ("Mathematics", "📐", "#5b82bc", "#eaf1ff", [
        ("Number Systems", [
            ("Real Numbers", "Fundamental Theorem of Arithmetic; irrationality proofs for √2, √3 and √5."),
        ]),
        ("Algebra", [
            ("Polynomials", "Zeros and relationship between zeros and coefficients of quadratic polynomials."),
            ("Pair of Linear Equations in Two Variables", "Graphical and algebraic methods; consistency; substitution and elimination; situational problems."),
            ("Quadratic Equations", "Factorisation, quadratic formula, discriminant and nature of roots; applications."),
            ("Arithmetic Progressions", "Derive nth term and sum of first n terms; applications."),
        ]),
        ("Coordinate Geometry", [
            ("Coordinate Geometry", "Linear graphs, distance formula and section formula for internal division."),
        ]),
        ("Geometry", [
            ("Triangles", "Similarity; Basic Proportionality Theorem; AAA, SSS and SAS similarity criteria."),
            ("Circles", "Tangent at point of contact; tangent perpendicular to radius; equal tangents from an external point."),
        ]),
        ("Trigonometry", [
            ("Introduction to Trigonometry", "Ratios of acute angles; values for 30°, 45° and 60°; relationships."),
            ("Trigonometric Identities", "Prove and apply sin²A + cos²A = 1; simple identities."),
            ("Some Applications of Trigonometry", "Heights and distances; at most two right triangles; angles 30°, 45° and 60°."),
        ]),
        ("Mensuration", [
            ("Areas Related to Circles", "Sectors, segments and perimeters; central angles 60°, 90° and 120°."),
            ("Surface Areas and Volumes", "Combinations of two cubes, cuboids, spheres, hemispheres, cylinders or cones."),
        ]),
        ("Statistics and Probability", [
            ("Statistics", "Mean, median and mode for grouped data."),
            ("Probability", "Classical definition and simple event probabilities."),
        ]),
    ]),
    ("Science", "🔬", "#36947b", "#e5f7ef", [
        ("Chemical Substances — Nature and Behaviour · 25 marks", [
            ("Chemical Reactions and Equations", "Balancing; combination, decomposition, displacement, double displacement, precipitation, endothermic/exothermic, oxidation and reduction."),
            ("Acids, Bases and Salts", "Properties, indicators, pH and everyday importance; NaOH, bleaching powder, baking soda, washing soda and Plaster of Paris."),
            ("Metals and Non-Metals", "Physical and chemical properties, reactivity series, ionic compounds, metallurgy, corrosion and prevention."),
            ("Carbon and its Compounds", "Covalent bonding, homologous series, nomenclature, reactions, ethanol, ethanoic acid, soaps and detergents."),
        ]),
        ("World of Living · 25 marks", [
            ("Life Processes", "Nutrition, respiration, transport and excretion in plants and animals."),
            ("Control and Coordination", "Tropic movements, plant hormones, nervous system, reflex actions and animal hormones."),
            ("How do Organisms Reproduce?", "Asexual and sexual reproduction; reproductive health, family planning, safe sex and HIV/AIDS."),
            ("Heredity", "Mendel’s experiments, laws of inheritance and brief sex determination. Evolution is formative/internal assessment only according to the details provided."),
        ]),
        ("Natural Phenomena · 12 marks", [
            ("Light — Reflection and Refraction", "Curved mirrors, image formation, mirror formula, magnification, refraction, lenses, lens formula and power. Formula derivations excluded in the supplied outline."),
            ("The Human Eye and the Colourful World", "Prism, dispersion, scattering, atmospheric refraction, common vision defects and their correction."),
        ]),
        ("Effects of Current · 13 marks", [
            ("Electricity", "Current, potential difference, Ohm’s law, resistance, resistivity, series/parallel circuits, heating effect and power."),
            ("Magnetic Effects of Electric Current", "Magnetic fields, conductor, coil and solenoid; force, Fleming’s left-hand rule, DC/AC and domestic circuits."),
        ]),
        ("Natural Resources · 5 marks", [
            ("Our Environment", "Ecosystem, environmental problems, ozone depletion, waste and biodegradable/non-biodegradable substances."),
        ]),
    ]),
    ("Social Science", "🌏", "#c38a42", "#fff2df", [
        ("History", [
            ("The Rise of Nationalism in Europe", "Nationalism, unification movements and the making of nation-states."),
            ("Nationalism in India", "National movement, major events and participation."),
            ("The Making of a Global World", "Use the specific sections prescribed by your school."),
            ("The Age of Industrialisation", "Internal/formative coverage was indicated in the earlier notes; confirm with your teacher."),
            ("Print Culture and the Modern World", "Print, society and the spread of ideas."),
        ]),
        ("Geography", [
            ("Resources and Development", "Resource planning, sustainable development and major soil types."),
            ("Forest and Wildlife Resources", "Biodiversity, conservation and community involvement."),
            ("Water Resources", "Water scarcity, conservation, multipurpose projects and dams."),
            ("Agriculture", "Types of farming, cropping patterns and major crops."),
            ("Minerals and Energy Resources", "Minerals, conventional and non-conventional energy."),
            ("Manufacturing Industries", "Industrial location, major industries and environmental impacts."),
            ("Lifelines of National Economy", "Transport, communication, trade, ports and airports."),
        ]),
        ("Political Science", [
            ("Power Sharing", "Forms and need for power sharing."),
            ("Federalism", "Features, levels of government and decentralisation."),
            ("Gender, Religion and Caste", "Social differences and their relationship with politics."),
            ("Political Parties", "Party systems, functions, challenges and reforms."),
            ("Outcomes of Democracy", "Accountable, responsive and legitimate government."),
        ]),
        ("Economics", [
            ("Development", "Development goals, income and other indicators."),
            ("Sectors of the Indian Economy", "Primary, secondary and tertiary sectors; employment."),
            ("Money and Credit", "Money, formal and informal credit, self-help groups."),
            ("Globalisation and the Indian Economy", "Use the prescribed portions from your school’s current syllabus."),
            ("Consumer Rights", "Project/internal assessment as indicated in the earlier notes; confirm school instructions."),
        ]),
    ]),
    ("English", "📖", "#9273bd", "#f1eaff", [
        ("Section A — Reading Skills · 20 marks", [
            ("Discursive Passage", "Unseen passage of 400–450 words: analysis, inference and vocabulary · 10 marks."),
            ("Case-Based Factual Passage", "Unseen passage of 200–250 words with visual inputs such as charts or statistics · 10 marks."),
        ]),
        ("Section B — Writing Skills and Grammar · 20 marks", [
            ("Grammar", "Context-based gap filling, editing or transformation: tenses and modals, subject-verb concord, determiners, reported speech."),
            ("Formal Letter", "Structured formal letter based on a situation; 100–120 words · 5 marks."),
            ("Analytical Paragraph", "Describe/analyse a graph, chart, map or cues; 100–120 words · 5 marks."),
        ]),
        ("First Flight — Prose", [(t, "") for t in [
            "A Letter to God", "Nelson Mandela: Long Walk to Freedom", "Stories About Flying",
            "From the Diary of Anne Frank", "Glimpses of India", "Mijbil the Otter",
            "Madam Rides the Bus", "The Sermon at Benares", "The Proposal (Play)"]]),
        ("First Flight — Poetry", [(t, "") for t in [
            "Dust of Snow", "Fire and Ice", "A Tiger in the Zoo", "How to Tell Wild Animals",
            "The Ball Poem", "Amanda!", "The Trees", "Fog",
            "The Tale of Custard the Dragon", "For Anne Gregory"]]),
        ("Footprints Without Feet — Supplementary Reader", [(t, "") for t in [
            "A Triumph of Surgery", "The Thief’s Story", "The Midnight Visitor", "A Question of Trust",
            "Footprints Without Feet", "The Making of a Scientist", "The Necklace", "Bholi",
            "The Book that Saved the Earth"]]),
    ]),
    ("Hindi Course A", "✍️", "#c66c85", "#ffedf2", [
        ("खंड क — अपठित बोध · 14 अंक", [
            ("अपठित गद्यांश", "अपठित गद्यांश पर आधारित बोध और विश्लेषण के प्रश्न।"),
        ]),
        ("खंड ख — व्याकरण · 16 अंक", [
            ("रचना के आधार पर वाक्य रूपांतरण", "निर्देशानुसार वाक्य रूपांतरण का अभ्यास।"),
            ("वाच्य", "कर्तृवाच्य, कर्मवाच्य और भाववाच्य।"),
            ("पद परिचय", "वाक्य में पदों का व्याकरणिक परिचय।"),
            ("अलंकार", "श्लेष, उत्प्रेक्षा, अतिशयोक्ति और मानवीकरण।"),
        ]),
        ("क्षितिज भाग 2 — काव्य", [(t, "") for t in [
            "सूरदास — पद", "तुलसीदास — राम-लक्ष्मण-परशुराम संवाद", "जयशंकर प्रसाद — आत्मकथ्य",
            "सूर्यकांत त्रिपाठी ‘निराला’ — उत्साह", "सूर्यकांत त्रिपाठी ‘निराला’ — अट नहीं रही है",
            "नागार्जुन — यह दंतुरित मुस्कान", "नागार्जुन — फसल", "मंगलेश डबराल — संगतकार"]]),
        ("क्षितिज भाग 2 — गद्य", [(t, "") for t in [
            "स्वयं प्रकाश — नेताजी का चश्मा", "रामवृक्ष बेनीपुरी — बालगोबिन भगत", "यशपाल — लखनवी अंदाज़",
            "मन्नू भंडारी — एक कहानी यह भी", "यतीन्द्र मिश्र — नौबतखाने में इबादत",
            "भदंत आनंद कौसल्यायन — संस्कृति"]]),
        ("कृतिका भाग 2", [(t, "") for t in [
            "शिवपूजन सहाय — माता का अँचल", "अज्ञेय — मैं क्यों लिखता हूँ",
            "मधु कांकरिया — साना-साना हाथ जोड़ि..."]]),
        ("खंड घ — लेखन · 20 अंक", [
            ("लेखन अभ्यास", "अपने विद्यालय द्वारा बताए गए लेखन प्रारूप और शब्द-सीमा के अनुसार अभ्यास करें।"),
        ]),
    ]),
    ("Artificial Intelligence", "💻", "#3f9ba7", "#e2f7fa", [
        ("Part A — Employability Skills · 10 theory marks", [(t, "") for t in [
            "Communication Skills-II", "Self-Management Skills-II", "ICT Skills-II",
            "Entrepreneurial Skills-II", "Green Skills-II"]]),
        ("Part B — Subject Specific Skills · 40 theory + 10 practical", [(t, "") for t in [
            "Introduction to AI", "AI Project Cycle",
            "Advanced Python (Optional / non-evaluative for theory)", "Data Science",
            "Computer Vision", "Natural Language Processing (NLP)", "Evaluation"]]),
        ("Part C and Part D — Practical / Internal", [
            ("Practical Work / Project Work", "35 practical marks."),
            ("Project File / Student Portfolio & Viva", "5 practical marks."),
        ]),
    ]),
]


def _build():
    subjects = []
    for name, icon, accent, tint, groups in _RAW:
        built_groups, total = [], 0
        for gname, topics in groups:
            items = [
                {"title": t, "desc": d, "key": f"{name}::{gname}::{t}"}
                for t, d in topics
            ]
            total += len(items)
            built_groups.append({"name": gname, "topics": items})
        subjects.append({
            "name": name, "icon": icon, "accent": accent, "tint": tint,
            "groups": built_groups, "total": total,
        })
    return subjects


SUBJECTS = _build()

QUIZZES = [
    {"subject": "Science", "q": "What is the SI unit of electric current?",
     "a": ["Ampere", "Volt", "Ohm", "Watt"], "correct": 0,
     "why": "Electric current is measured in amperes (A)."},
    {"subject": "Science", "q": "Which gas is usually released when an acid reacts with a metal?",
     "a": ["Oxygen", "Hydrogen", "Nitrogen", "Carbon dioxide"], "correct": 1,
     "why": "A typical acid + metal reaction releases hydrogen gas."},
    {"subject": "Mathematics", "q": "What is sin 30°?",
     "a": ["0", "1", "1/2", "√3/2"], "correct": 2, "why": "sin 30° = 1/2."},
    {"subject": "Mathematics", "q": "The common difference of 3, 7, 11, 15, … is:",
     "a": ["3", "4", "7", "11"], "correct": 1,
     "why": "Subtract consecutive terms: 7 − 3 = 4."},
    {"subject": "English", "q": "Which is the most suitable tone for a formal letter to an authority?",
     "a": ["Slang and jokes", "Polite and clear", "Very casual", "Only poetic"], "correct": 1,
     "why": "Formal letters use a respectful, clear and appropriately formal tone."},
    {"subject": "Social Science", "q": "Which soil is commonly associated with cotton cultivation in India?",
     "a": ["Black soil", "Arid soil", "Forest soil", "Laterite soil"], "correct": 0,
     "why": "Black soil retains moisture and is particularly suitable for cotton."},
    {"subject": "Hindi Course A", "q": "‘मानवीकरण’ अलंकार में क्या होता है?",
     "a": ["बढ़ा-चढ़ाकर वर्णन", "निर्जीव को मानव-गुण देना", "एक ही शब्द के कई अर्थ", "उपमा देना"], "correct": 1,
     "why": "मानवीकरण में निर्जीव वस्तु या प्रकृति को मानवीय गुण दिए जाते हैं।"},
    {"subject": "Artificial Intelligence", "q": "In the AI project cycle, which stage helps define the problem and goal?",
     "a": ["Problem Scoping", "Modelling only", "Deployment only", "Decoration"], "correct": 0,
     "why": "Problem Scoping identifies the problem, stakeholders and goal."},
]

_MAP_RAW = [
    ("Resources & Development — Soils", [
        "Alluvial soil", "Black soil", "Red and Yellow soil", "Laterite soil",
        "Arid soil", "Forest and Mountain soil"]),
    ("Water Resources — Dams", [
        "Salal Dam", "Bhakra Nangal Dam", "Tehri Dam", "Rana Pratap Sagar Dam",
        "Sardar Sarovar Dam", "Hirakud Dam"]),
    ("More items from your school's map-work sheet", [
        "Major crops", "Iron ore mines", "Coal mines", "Oil fields", "Thermal power plants",
        "Nuclear power plants", "Major manufacturing industries", "Major sea ports",
        "International airports"]),
]

MAP_GROUPS = [
    {"name": name, "items": [{"title": t, "key": f"map::{name}::{t}"} for t in items]}
    for name, items in _MAP_RAW
]

# Every key the progress API is allowed to store.
ALL_KEYS = (
    {it["key"] for s in SUBJECTS for g in s["groups"] for it in g["topics"]}
    | {it["key"] for g in MAP_GROUPS for it in g["items"]}
)
