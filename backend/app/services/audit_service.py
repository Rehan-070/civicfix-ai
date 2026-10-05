from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.entities import AuditLog, AgentExecution

def log_audit(
    db: Session,
    actor: str,
    action: str,
    entity_type: str,
    entity_id: str,
    metadata: Optional[Dict[str, Any]] = None
) -> AuditLog:
    """Creates an immutable audit record for system and user operations."""
    entry = AuditLog(
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata_json=metadata or {}
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def log_agent_execution(
    db: Session,
    agent_name: str,
    status: str,
    confidence: float,
    execution_time_ms: int,
    issue_id: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None
) -> AgentExecution:
    """Logs detailed agent performance metrics and response contract output."""
    execution = AgentExecution(
        issue_id=issue_id,
        agent_name=agent_name,
        status=status,
        confidence=confidence,
        execution_time_ms=execution_time_ms,
        payload=payload or {}
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    return execution
