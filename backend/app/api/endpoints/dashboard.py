from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.entities import CivicIssue, Complaint, Department

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_issues = db.query(func.count(CivicIssue.id)).scalar() or 0
    submitted = db.query(func.count(CivicIssue.id)).filter(CivicIssue.status == "SUBMITTED").scalar() or 0
    in_progress = db.query(func.count(CivicIssue.id)).filter(CivicIssue.status.in_(["ACKNOWLEDGED", "ASSIGNED", "IN_PROGRESS"])).scalar() or 0
    escalated = db.query(func.count(CivicIssue.id)).filter(CivicIssue.status == "ESCALATED").scalar() or 0
    resolved = db.query(func.count(CivicIssue.id)).filter(CivicIssue.status.in_(["RESOLVED", "VERIFICATION_PENDING", "VERIFIED_RESOLVED"])).scalar() or 0

    dept_counts = db.query(
        Department.name, func.count(CivicIssue.id)
    ).join(CivicIssue, CivicIssue.department_id == Department.id, isouter=True).group_by(Department.name).all()

    return {
        "total_issues": total_issues,
        "submitted": submitted,
        "in_progress": in_progress,
        "escalated": escalated,
        "resolved": resolved,
        "department_breakdown": [{"department": d[0] or "Unassigned", "count": d[1]} for d in dept_counts]
    }

@router.get("/complaints")
def list_complaints(db: Session = Depends(get_db)):
    complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).all()
    results = []
    for c in complaints:
        issue = c.issue
        results.append({
            "id": c.id,
            "complaint_number": c.complaint_number,
            "category": issue.category if issue else "Unknown",
            "severity": issue.severity if issue else "MEDIUM",
            "status": issue.status if issue else "DRAFT",
            "address": issue.address if issue else "Unknown",
            "ward": issue.ward if issue else "Demo Ward",
            "department_name": issue.department.name if issue and issue.department else "Road Department",
            "created_at": c.created_at,
            "submitted_at": c.submitted_at
        })
    return results
