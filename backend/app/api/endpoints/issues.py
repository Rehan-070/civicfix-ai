import os
import uuid
import time
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.models.entities import CivicIssue, Evidence
from app.services.orchestrator import WorkflowOrchestrator
from app.services.audit_service import log_audit

router = APIRouter()

@router.post("")
async def create_issue(
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    address: Optional[str] = Form(None),
    ward: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # 1. File Upload Validation (MIME & Size)
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image format '{file.content_type}'. Allowed: JPEG, PNG, WebP"
        )

    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum size of {settings.MAX_FILE_SIZE_MB}MB"
        )

    # Save image to upload folder
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)

    relative_url = f"/uploads/{filename}"

    # 2. Create Civic Issue Database record
    issue_code = f"ISS-2026-{int(time.time() * 1000) % 90000 + 10000}"
    issue = CivicIssue(
        issue_code=issue_code,
        title=f"Civic Issue at {address or 'Demo Ward'}",
        category="Pending Perception",
        severity="MEDIUM",
        status="DRAFT",
        latitude=latitude,
        longitude=longitude,
        address=address,
        ward=ward,
        description=description
    )
    db.add(issue)
    db.commit()
    db.refresh(issue)

    # 3. Create Evidence record (BEFORE photo)
    evidence = Evidence(
        issue_id=issue.id,
        evidence_type="BEFORE",
        image_url=relative_url,
        file_size=len(content),
        mime_type=file.content_type
    )
    db.add(evidence)
    db.commit()

    log_audit(db, "citizen", "ISSUE_CREATED", "civic_issue", issue.id, {
        "issue_code": issue.issue_code,
        "image_url": relative_url
    })

    return {
        "issue_id": issue.id,
        "issue_code": issue.issue_code,
        "status": issue.status,
        "image_url": relative_url,
        "local_file_path": file_path
    }

@router.post("/{issue_id}/analyze")
def analyze_issue(
    issue_id: str,
    db: Session = Depends(get_db)
):
    issue = db.query(CivicIssue).filter(CivicIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Civic Issue not found")

    evidence = db.query(Evidence).filter(Evidence.issue_id == issue.id, Evidence.evidence_type == "BEFORE").first()
    if not evidence:
        raise HTTPException(status_code=400, detail="No evidence photo found for this issue")

    # Map web upload path back to physical disk path for Vision Agent
    file_path = os.path.join(settings.UPLOAD_DIR, os.path.basename(evidence.image_url))

    orchestrator = WorkflowOrchestrator(db)
    result = orchestrator.analyze_issue(
        issue_id=issue.id,
        image_path=file_path if os.path.exists(file_path) else evidence.image_url,
        lat=issue.latitude,
        lon=issue.longitude,
        address=issue.address
    )

    return result

@router.get("/{issue_id}")
def get_issue(issue_id: str, db: Session = Depends(get_db)):
    issue = db.query(CivicIssue).filter(CivicIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Civic Issue not found")
    
    evidences = db.query(Evidence).filter(Evidence.issue_id == issue.id).all()
    dept_name = issue.department.name if issue.department else None

    return {
        "id": issue.id,
        "issue_code": issue.issue_code,
        "title": issue.title,
        "category": issue.category,
        "severity": issue.severity,
        "status": issue.status,
        "latitude": issue.latitude,
        "longitude": issue.longitude,
        "address": issue.address,
        "ward": issue.ward,
        "department_id": issue.department_id,
        "department_name": dept_name,
        "confidence": issue.confidence,
        "description": issue.description,
        "evidences": [{"id": e.id, "type": e.evidence_type, "url": e.image_url, "created_at": e.created_at} for e in evidences],
        "created_at": issue.created_at
    }
