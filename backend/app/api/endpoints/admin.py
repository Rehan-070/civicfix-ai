from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import AuditLog, AgentExecution, Complaint, CivicIssue, ComplaintStatusHistory
from app.schemas.domain import AdminSimulateStatus
from app.services.state_machine import ComplaintStatus, validate_transition
from app.services.audit_service import log_audit

router = APIRouter()

@router.get("/audit-logs")
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
    return [{
        "id": log.id,
        "actor": log.actor,
        "action": log.action,
        "entity_type": log.entity_type,
        "entity_id": log.entity_id,
        "metadata": log.metadata_json,
        "created_at": log.created_at
    } for log in logs]

@router.get("/agent-executions")
def get_agent_executions(limit: int = 50, db: Session = Depends(get_db)):
    executions = db.query(AgentExecution).order_by(AgentExecution.created_at.desc()).limit(limit).all()
    return [{
        "id": ex.id,
        "issue_id": ex.issue_id,
        "agent_name": ex.agent_name,
        "status": ex.status,
        "confidence": ex.confidence,
        "execution_time_ms": ex.execution_time_ms,
        "payload": ex.payload,
        "created_at": ex.created_at
    } for ex in executions]

@router.post("/simulate-status")
def simulate_status_transition(payload: AdminSimulateStatus, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter((Complaint.id == payload.complaint_id) | (Complaint.complaint_number == payload.complaint_id)).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    issue = complaint.issue
    prev_status = issue.status
    target_status = payload.new_status

    if target_status not in ComplaintStatus.ALL_STATES:
        raise HTTPException(status_code=400, detail=f"Invalid status '{target_status}'")

    issue.status = target_status
    history = ComplaintStatusHistory(
        complaint_id=complaint.id,
        previous_status=prev_status,
        new_status=target_status,
        changed_by="ADMIN_SIMULATION_CONTROL",
        notes=payload.notes or f"Hackathon Demo Simulation fast-forwarded status to {target_status}."
    )
    db.add(history)
    db.commit()

    log_audit(db, "admin", "SIMULATED_STATUS_CHANGE", "complaint", complaint.id, {
        "previous_status": prev_status,
        "new_status": target_status,
        "notes": payload.notes
    })

    return {
        "complaint_id": complaint.id,
        "complaint_number": complaint.complaint_number,
        "previous_status": prev_status,
        "new_status": target_status,
        "message": f"Status successfully fast-forwarded to {target_status} via Demo Control Panel."
    }
