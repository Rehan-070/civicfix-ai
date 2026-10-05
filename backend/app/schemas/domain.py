from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# --- AGENT CONTRACT SCHEMAS ---

class AgentResponse(BaseModel):
    agent: str
    status: str  # SUCCESS, LOW_CONFIDENCE, NEEDS_HUMAN_REVIEW, FAILED, RETRYABLE_FAILURE
    confidence: float = Field(ge=0.0, le=1.0)
    data: Dict[str, Any] = {}
    errors: List[str] = []
    timestamp: str

# --- AUTH SCHEMAS ---

class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    role: Optional[str] = "CITIZEN"

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

# --- ISSUE & COMPLAINT SCHEMAS ---

class IssueCreate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    ward: Optional[str] = None
    description: Optional[str] = None

class EvidenceResponse(BaseModel):
    id: str
    evidence_type: str
    image_url: str
    created_at: datetime

class IssueResponse(BaseModel):
    id: str
    issue_code: str
    title: str
    category: str
    severity: str
    status: str
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str]
    ward: Optional[str]
    department_id: Optional[str]
    department_name: Optional[str] = None
    confidence: float
    description: Optional[str]
    evidences: List[EvidenceResponse] = []
    created_at: datetime
    updated_at: datetime

class ComplaintApproval(BaseModel):
    approved: bool
    edited_body: Optional[str] = None
    edited_requested_action: Optional[str] = None

class VerificationSubmission(BaseModel):
    after_image_url: str
    notes: Optional[str] = None

class AdminSimulateStatus(BaseModel):
    complaint_id: str
    new_status: str
    notes: Optional[str] = None
