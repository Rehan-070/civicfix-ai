from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import CivicIssue, Evidence

router = APIRouter()

@router.get("/issues")
def get_map_issues(db: Session = Depends(get_db)):
    issues = db.query(CivicIssue).filter(CivicIssue.latitude.isnot(None), CivicIssue.longitude.isnot(None)).all()
    markers = []
    for issue in issues:
        evidence = db.query(Evidence).filter(Evidence.issue_id == issue.id, Evidence.evidence_type == "BEFORE").first()
        markers.append({
            "id": issue.id,
            "issue_code": issue.issue_code,
            "category": issue.category,
            "severity": issue.severity,
            "status": issue.status,
            "latitude": issue.latitude,
            "longitude": issue.longitude,
            "address": issue.address,
            "ward": issue.ward,
            "department_name": issue.department.name if issue.department else "Road Department",
            "image_url": evidence.image_url if evidence else None,
            "created_at": issue.created_at
        })
    return markers
