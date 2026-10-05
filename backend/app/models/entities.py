import uuid
import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

def generate_timestamp():
    return datetime.datetime.now(datetime.timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="CITIZEN")  # CITIZEN, ADMIN, OPERATOR
    created_at = Column(DateTime(timezone=True), default=generate_timestamp)

class Department(Base):
    __tablename__ = "departments"

    id = Column(String, primary_key=True, default=generate_uuid)
    code = Column(String, unique=True, index=True, nullable=False)  # ROAD, SANITATION, STREETLIGHT, WATER, DRAINAGE, HORTICULTURE
    name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)
    base_sla_hours = Column(Integer, nullable=False, default=72)

class AuthorityRule(Base):
    __tablename__ = "authority_rules"

    id = Column(String, primary_key=True, default=generate_uuid)
    department_id = Column(String, ForeignKey("departments.id"), nullable=False)
    category = Column(String, index=True, nullable=False)  # Pothole, Garbage, Broken Streetlight, etc.
    ward = Column(String, index=True, nullable=True)  # Specific ward or null for all
    priority = Column(Integer, default=1)

    department = relationship("Department")

class CivicIssue(Base):
    __tablename__ = "civic_issues"

    id = Column(String, primary_key=True, default=generate_uuid)
    issue_code = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=False)
    category = Column(String, index=True, nullable=False)
    severity = Column(String, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String, index=True, default="DRAFT")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    ward = Column(String, nullable=True)
    department_id = Column(String, ForeignKey("departments.id"), nullable=True)
    confidence = Column(Float, default=1.0)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=generate_timestamp)
    updated_at = Column(DateTime(timezone=True), default=generate_timestamp, onupdate=generate_timestamp)

    department = relationship("Department")
    evidences = relationship("Evidence", back_populates="issue", cascade="all, delete-orphan")
    complaints = relationship("Complaint", back_populates="issue", cascade="all, delete-orphan")
    agent_executions = relationship("AgentExecution", back_populates="issue", cascade="all, delete-orphan")

class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(String, primary_key=True, default=generate_uuid)
    issue_id = Column(String, ForeignKey("civic_issues.id"), nullable=False)
    evidence_type = Column(String, default="BEFORE")  # BEFORE, AFTER
    image_url = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=generate_timestamp)

    issue = relationship("CivicIssue", back_populates="evidences")

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(String, primary_key=True, default=generate_uuid)
    complaint_number = Column(String, unique=True, index=True, nullable=False)  # CIV-2026-XXXXX
    issue_id = Column(String, ForeignKey("civic_issues.id"), nullable=False)
    formatted_body = Column(Text, nullable=False)
    requested_action = Column(Text, nullable=False)
    user_approved = Column(Boolean, default=False)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    sla_deadline = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=generate_timestamp)

    issue = relationship("CivicIssue", back_populates="complaints")
    status_history = relationship("ComplaintStatusHistory", back_populates="complaint", cascade="all, delete-orphan")
    escalations = relationship("Escalation", back_populates="complaint", cascade="all, delete-orphan")
    verifications = relationship("VerificationResult", back_populates="complaint", cascade="all, delete-orphan")

class ComplaintStatusHistory(Base):
    __tablename__ = "complaint_status_history"

    id = Column(String, primary_key=True, default=generate_uuid)
    complaint_id = Column(String, ForeignKey("complaints.id"), nullable=False)
    previous_status = Column(String, nullable=True)
    new_status = Column(String, nullable=False)
    changed_by = Column(String, default="SYSTEM")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=generate_timestamp)

    complaint = relationship("Complaint", back_populates="status_history")

class Escalation(Base):
    __tablename__ = "escalations"

    id = Column(String, primary_key=True, default=generate_uuid)
    complaint_id = Column(String, ForeignKey("complaints.id"), nullable=False)
    escalation_reason = Column(String, nullable=False)
    sla_hours = Column(Integer, nullable=False)
    breached_at = Column(DateTime(timezone=True), default=generate_timestamp)
    escalation_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=generate_timestamp)

    complaint = relationship("Complaint", back_populates="escalations")

class VerificationResult(Base):
    __tablename__ = "verification_results"

    id = Column(String, primary_key=True, default=generate_uuid)
    complaint_id = Column(String, ForeignKey("complaints.id"), nullable=False)
    result_status = Column(String, nullable=False)  # VERIFIED_RESOLVED, LIKELY_RESOLVED, PARTIALLY_RESOLVED, NOT_RESOLVED, NEEDS_HUMAN_REVIEW
    confidence_score = Column(Float, nullable=False)
    evidence_summary = Column(Text, nullable=False)
    needs_human_review = Column(Boolean, default=False)
    after_evidence_id = Column(String, nullable=True)
    verified_at = Column(DateTime(timezone=True), default=generate_timestamp)

    complaint = relationship("Complaint", back_populates="verifications")

class AgentExecution(Base):
    __tablename__ = "agent_executions"

    id = Column(String, primary_key=True, default=generate_uuid)
    issue_id = Column(String, ForeignKey("civic_issues.id"), nullable=True)
    agent_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # SUCCESS, LOW_CONFIDENCE, NEEDS_HUMAN_REVIEW, FAILED
    confidence = Column(Float, default=1.0)
    execution_time_ms = Column(Integer, default=0)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=generate_timestamp)

    issue = relationship("CivicIssue", back_populates="agent_executions")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    actor = Column(String, nullable=False)  # system, user_id, admin_id
    action = Column(String, nullable=False)  # ISSUE_CREATED, AUTHORITY_SELECTED, COMPLAINT_APPROVED, etc.
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=generate_timestamp)
