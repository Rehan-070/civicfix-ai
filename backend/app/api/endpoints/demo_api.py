import time
import random
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Body

router = APIRouter()

# In-memory store for demo simulated complaints
DEMO_COMPLAINTS_DB: Dict[str, Dict[str, Any]] = {}

@router.post("/complaints")
def create_demo_complaint(payload: Dict[str, Any] = Body(...)):
    random_id = f"CIV-2026-{random.randint(10000, 99999)}"
    record = {
        "complaint_id": random_id,
        "category": payload.get("category", "Pothole"),
        "department": payload.get("department", "Road Department"),
        "jurisdiction": payload.get("jurisdiction", "Demo Ward 04"),
        "status": "SUBMITTED",
        "sla_hours": payload.get("sla_hours", 72),
        "gateway_notice": "CivicFix Demo Civic API — Simulation Only",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    DEMO_COMPLAINTS_DB[random_id] = record
    return record

@router.get("/complaints/{id}")
def get_demo_complaint(id: str):
    if id in DEMO_COMPLAINTS_DB:
        return DEMO_COMPLAINTS_DB[id]
    return {
        "complaint_id": id,
        "category": "Pothole",
        "department": "Road Department",
        "jurisdiction": "Demo Ward 04",
        "status": "ACKNOWLEDGED",
        "sla_hours": 72,
        "gateway_notice": "CivicFix Demo Civic API — Simulation Only"
    }

@router.patch("/complaints/{id}/status")
def update_demo_complaint_status(id: str, new_status: str = Body(..., embed=True)):
    if id in DEMO_COMPLAINTS_DB:
        DEMO_COMPLAINTS_DB[id]["status"] = new_status
    return {
        "complaint_id": id,
        "new_status": new_status,
        "gateway_notice": "CivicFix Demo Civic API — Simulation Only"
    }

@router.post("/complaints/{id}/escalate")
def escalate_demo_complaint(id: str):
    if id in DEMO_COMPLAINTS_DB:
        DEMO_COMPLAINTS_DB[id]["status"] = "ESCALATED"
    return {
        "complaint_id": id,
        "status": "ESCALATED",
        "escalation_officer": "Senior Municipal Inspection Officer",
        "gateway_notice": "CivicFix Demo Civic API — Simulation Only"
    }

@router.post("/complaints/{id}/evidence")
def upload_demo_evidence(id: str, evidence_type: str = Body("AFTER")):
    return {
        "complaint_id": id,
        "evidence_type": evidence_type,
        "status": "EVIDENCE_RECEIVED",
        "gateway_notice": "CivicFix Demo Civic API — Simulation Only"
    }

@router.get("/departments")
def get_demo_departments():
    return {
        "gateway_notice": "CivicFix Demo Civic API — Simulation Only",
        "departments": [
            {"code": "ROAD", "name": "Road Department", "sla_hours": 72},
            {"code": "SANITATION", "name": "Sanitation Department", "sla_hours": 24},
            {"code": "STREETLIGHT", "name": "Streetlight Department", "sla_hours": 48},
            {"code": "WATER", "name": "Water Department", "sla_hours": 24},
            {"code": "DRAINAGE", "name": "Drainage Department", "sla_hours": 48},
            {"code": "HORTICULTURE", "name": "Tree/Horticulture Department", "sla_hours": 12}
        ]
    }

@router.get("/complaints/{id}/timeline")
def get_demo_timeline(id: str):
    return {
        "complaint_id": id,
        "gateway_notice": "CivicFix Demo Civic API — Simulation Only",
        "timeline": [
            {"status": "SUBMITTED", "timestamp": "2026-09-30T10:00:00Z", "notes": "Ingested via Demo Civic Gateway"},
            {"status": "ACKNOWLEDGED", "timestamp": "2026-09-30T10:05:00Z", "notes": "Acknowledged by Road Dept Dispatcher"},
            {"status": "ASSIGNED", "timestamp": "2026-09-30T11:00:00Z", "notes": "Assigned to Maintenance Unit #4"}
        ]
    }
