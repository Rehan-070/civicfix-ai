import math
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.models.entities import CivicIssue

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates distance between two lat/lon points in meters using Haversine formula."""
    R = 6371000  # Radius of Earth in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

from app.categories import normalize_category

def check_duplicate_issue(
    db: Session,
    category: str,
    lat: float,
    lon: float,
    radius_meters: float = 50.0
) -> Optional[Dict[str, Any]]:
    """
    Checks if an active issue of the matching category exists within specified radius.
    """
    if lat is None or lon is None:
        return None

    target_cat = normalize_category(category)["display_name"]

    active_issues = db.query(CivicIssue).filter(
        CivicIssue.status.notin_(["VERIFIED_RESOLVED", "CANCELLED"])
    ).all()

    for issue in active_issues:
        issue_cat = normalize_category(issue.category)["display_name"]
        if issue_cat == target_cat:
            if issue.latitude is not None and issue.longitude is not None:
                dist = haversine_distance(lat, lon, issue.latitude, issue.longitude)
                if dist <= radius_meters:
                    return {
                        "is_duplicate": True,
                        "existing_issue_id": issue.id,
                        "existing_issue_code": issue.issue_code,
                        "distance_meters": round(dist, 1),
                        "category": issue_cat,
                        "status": issue.status,
                        "created_at": issue.created_at.isoformat()
                    }
                    
    return None
