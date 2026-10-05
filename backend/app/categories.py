from typing import Dict, Any, List, Optional

CIVIC_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "water_leakage": {
        "key": "water_leakage",
        "display_name": "Water Leakage / Burst Pipeline",
        "department_code": "WATER",
        "department_name": "Water Supply Department",
        "sla_hours": 24,
        "default_severity": "HIGH",
        "keywords": ["water", "leak", "pipe", "pipeline", "burst", "flood", "discharge", "leakage", "plumbing", "wet"],
        "observations": [
            "Visible water discharge detected",
            "Damaged or burst pipeline structure",
            "Continuous liquid leakage from infrastructure"
        ],
        "evidence_summary": "Visible water discharge from a damaged pipeline.",
        "description_template": "A significant water leakage has been detected from a damaged or burst pipeline at {address}. Visible water discharge is present from the damaged pipeline, which may result in water wastage, infrastructure damage, and safety concerns. Visual evidence has been attached for verification.",
        "action_template": "Dispatch the designated water supply maintenance team to inspect the damaged pipeline, stop the leakage, repair or replace the affected section, and restore the affected area."
    },
    "pothole": {
        "key": "pothole",
        "display_name": "Pothole",
        "department_code": "ROAD",
        "department_name": "Road Department",
        "sla_hours": 72,
        "default_severity": "HIGH",
        "keywords": ["pothole", "cavity", "asphalt", "crater", "road damage", "pit", "hole"],
        "observations": [
            "Road surface depression detected",
            "Broken asphalt and tarmac degradation",
            "Hazardous road cavity for traffic"
        ],
        "evidence_summary": "Large asphalt depression with structural degradation consistent with a severe road pothole.",
        "description_template": "A severe pothole and road cavity has been detected at {address}. The asphalt surface exhibits significant structural degradation creating a hazard for vehicles and pedestrians. Visual evidence has been attached for verification.",
        "action_template": "Dispatch the designated road maintenance crew to inspect the site, perform asphalt patching and resurfacing, and restore the road."
    },
    "garbage": {
        "key": "garbage",
        "display_name": "Garbage / Overflowing Bin",
        "department_code": "SANITATION",
        "department_name": "Sanitation Department",
        "sla_hours": 24,
        "default_severity": "MEDIUM",
        "keywords": ["garbage", "trash", "waste", "bin", "litter", "overflow", "refuse", "dump"],
        "observations": [
            "Uncollected solid waste accumulation",
            "Overflowing public garbage container",
            "Sanitary hazard on public thoroughfare"
        ],
        "evidence_summary": "Overflowing solid waste and uncollected garbage accumulated on public walkway.",
        "description_template": "An accumulation of uncollected garbage and overflowing waste container has been detected at {address}. This creates an unsanitary environment and health risk. Visual evidence has been attached.",
        "action_template": "Dispatch sanitation crew to clear accumulated waste, sanitize the site, and empty public garbage containers."
    },
    "streetlight": {
        "key": "streetlight",
        "display_name": "Broken Streetlight",
        "department_code": "STREETLIGHT",
        "department_name": "Electrical / Streetlight Department",
        "sla_hours": 48,
        "default_severity": "MEDIUM",
        "keywords": ["streetlight", "lamp", "light", "fixture", "bulb", "dark", "lighting", "pole"],
        "observations": [
            "Damaged streetlight pole / fixture",
            "Non-functional electrical lighting unit",
            "Inadequate public illumination at night"
        ],
        "evidence_summary": "Damaged streetlight fixture with broken bulb casing or non-functional electrical wiring.",
        "description_template": "A non-functional or damaged streetlight fixture has been reported at {address}. The lack of adequate lighting poses public safety risks at night. Visual evidence is attached.",
        "action_template": "Dispatch electrical maintenance unit to replace damaged bulb/fixture, inspect wiring, and restore streetlight illumination."
    },
    "drainage": {
        "key": "drainage",
        "display_name": "Drainage Problem",
        "department_code": "DRAINAGE",
        "department_name": "Drainage Department",
        "sla_hours": 48,
        "default_severity": "HIGH",
        "keywords": ["drain", "drainage", "sewer", "gutter", "overflow", "clog", "wastewater", "manhole"],
        "observations": [
            "Clogged or overflowing stormwater drain",
            "Stagnant wastewater accumulation",
            "Damaged drainage grate infrastructure"
        ],
        "evidence_summary": "Blocked stormwater drain with stagnant wastewater accumulation.",
        "description_template": "A severe drainage obstruction or sewer overflow has been identified at {address}. Stagnant wastewater is accumulating on public paths. Visual evidence is attached.",
        "action_template": "Dispatch stormwater drainage team to clear blockage, desilt drainage line, and inspect manhole infrastructure."
    },
    "damaged_road": {
        "key": "damaged_road",
        "display_name": "Damaged Road",
        "department_code": "ROAD",
        "department_name": "Road Department",
        "sla_hours": 72,
        "default_severity": "MEDIUM",
        "keywords": ["damaged road", "road crack", "tar", "pavement", "erosion", "asphalt crack"],
        "observations": [
            "Widespread road surface cracking",
            "Sub-base pavement erosion detected",
            "Uneven road carriage way"
        ],
        "evidence_summary": "Extensive road pavement cracking and surface erosion detected.",
        "description_template": "Significant road surface deterioration and pavement cracking observed at {address}. Visual evidence attached for repair scheduling.",
        "action_template": "Inspect road carriage way and execute pavement resurfacing and seal repairs."
    },
    "damaged_footpath": {
        "key": "damaged_footpath",
        "display_name": "Damaged Footpath",
        "department_code": "ROAD",
        "department_name": "Road / Public Works Department",
        "sla_hours": 72,
        "default_severity": "MEDIUM",
        "keywords": ["footpath", "sidewalk", "paver", "walkway", "pedestrian tile"],
        "observations": [
            "Dislodged or broken pedestrian paver tiles",
            "Uneven sidewalk stepping hazard",
            "Broken curb edge"
        ],
        "evidence_summary": "Broken and dislodged pedestrian paver tiles creating tripping hazards.",
        "description_template": "A damaged pedestrian footpath with dislodged paver tiles and tripping hazards reported at {address}. Visual evidence attached.",
        "action_template": "Re-lay dislodged paver tiles, level sidewalk surface, and restore pedestrian safety."
    },
    "fallen_tree": {
        "key": "fallen_tree",
        "display_name": "Fallen Tree",
        "department_code": "HORTICULTURE",
        "department_name": "Horticulture / Tree Department",
        "sla_hours": 12,
        "default_severity": "CRITICAL",
        "keywords": ["tree", "branch", "trunk", "foliage", "fallen", "uprooted"],
        "observations": [
            "Large fallen tree trunk / heavy branch",
            "Obstruction of public thoroughfare / power lines",
            "Hazardous uprooted tree structure"
        ],
        "evidence_summary": "Large fallen tree trunk blocking public thoroughfare and overhead cables.",
        "description_template": "An uprooted tree or heavy fallen branch is blocking the public road at {address}. Immediate removal is required to clear traffic obstruction and hazards.",
        "action_template": "Dispatch emergency horticulture tree-clearing team with equipment to cut, remove trunk, and clear public thoroughfare."
    }
}

VISION_CONFIDENCE_THRESHOLD = 0.75

def normalize_category(category_term: Optional[str]) -> Dict[str, Any]:
    """Resolves any key, display name, or keyword phrase to canonical CIVIC_CATEGORIES dict."""
    if not category_term:
        return CIVIC_CATEGORIES["pothole"]

    term = category_term.strip().lower()

    # Direct key match
    if term in CIVIC_CATEGORIES:
        return CIVIC_CATEGORIES[term]

    # Match display name
    for key, cat in CIVIC_CATEGORIES.items():
        if term == cat["display_name"].lower():
            return cat

    # Keyword match
    for key, cat in CIVIC_CATEGORIES.items():
        for kw in cat["keywords"]:
            if kw in term or term in kw:
                return cat

    return CIVIC_CATEGORIES["pothole"]
