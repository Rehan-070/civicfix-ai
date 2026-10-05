import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.services.state_machine import validate_transition, StateMachineError, ComplaintStatus
from app.services.sla_engine import get_sla_hours, is_sla_breached, calculate_sla_deadline
from app.services.duplicate_detection import check_duplicate_issue, haversine_distance
from app.services.agents import VisionAgent, LocationAgent, AuthorityAgent, ComplaintAgent, SubmissionAgent, VerificationAgent

TEST_DATABASE_URL = "sqlite:///./test_civicfix.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    from seed_data import seed_database
    db = TestingSessionLocal()
    seed_database(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_civicfix.db"):
        try:
            os.remove("./test_civicfix.db")
        except PermissionError:
            pass

client = TestClient(app)

# --- 1. STATE MACHINE TESTS ---

def test_state_machine_valid_transitions():
    assert validate_transition("DRAFT", "ANALYZING") is True
    assert validate_transition("ANALYZING", "AWAITING_APPROVAL") is True
    assert validate_transition("AWAITING_APPROVAL", "SUBMITTED") is True
    assert validate_transition("SUBMITTED", "ACKNOWLEDGED") is True
    assert validate_transition("ACKNOWLEDGED", "ASSIGNED") is True
    assert validate_transition("ASSIGNED", "IN_PROGRESS") is True
    assert validate_transition("IN_PROGRESS", "RESOLVED") is True
    assert validate_transition("RESOLVED", "VERIFICATION_PENDING") is True
    assert validate_transition("VERIFICATION_PENDING", "VERIFIED_RESOLVED") is True

def test_state_machine_illegal_transition():
    with pytest.raises(StateMachineError):
        validate_transition("DRAFT", "VERIFIED_RESOLVED")

# --- 2. SLA ENGINE TESTS ---

def test_sla_hours_deterministic():
    assert get_sla_hours("Pothole") == 72
    assert get_sla_hours("Garbage") == 24
    assert get_sla_hours("Broken Streetlight") == 48

def test_sla_breach_calculation():
    import datetime
    past_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=73)
    assert is_sla_breached(past_time, 72) is True

    recent_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=10)
    assert is_sla_breached(recent_time, 72) is False

# --- 3. DUPLICATE DETECTION TESTS ---

def test_haversine_distance():
    # Distance between two nearby coordinates (~10 meters apart)
    d = haversine_distance(12.9716, 77.5946, 12.97169, 77.59469)
    assert d < 20.0

# --- 4. AGENTS TESTS ---

def test_vision_agent():
    agent = VisionAgent()
    res = agent.process("demo_pothole.jpg")
    assert res.agent == "vision_agent"
    assert res.status == "SUCCESS"
    assert res.data["issue_type"] == "Pothole"
    assert res.confidence >= 0.75

def test_authority_agent(setup_db):
    db = TestingSessionLocal()
    agent = AuthorityAgent()
    res = agent.process(db, "Pothole", "HIGH", "Demo Ward 04")
    assert res.status == "SUCCESS"
    assert res.data["department_code"] == "ROAD"
    db.close()

# --- 5. END-TO-END HACKATHON WORKFLOW TEST ---

def test_end_to_end_pothole_workflow():
    # 1. Create Issue with Photo Upload
    test_img = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xFF\xDB\x00C\x00"  # Valid JPEG header
    response = client.post(
        "/api/v1/issues",
        files={"file": ("pothole.jpg", test_img, "image/jpeg")},
        data={
            "latitude": "12.9716",
            "longitude": "77.5946",
            "address": "4th Cross Road, Demo Ward 04",
            "ward": "Demo Ward 04"
        }
    )
    assert response.status_code == 200
    issue_data = response.json()
    issue_id = issue_data["issue_id"]

    # 2. Run AI Analysis Pipeline
    res_analysis = client.post(f"/api/v1/issues/{issue_id}/analyze")
    assert res_analysis.status_code == 200
    analysis_data = res_analysis.json()
    assert analysis_data["status"] == "AWAITING_APPROVAL"
    complaint_id = analysis_data["complaint"]["id"]

    # 3. Citizen Approval & Submission
    res_approve = client.post(
        f"/api/v1/complaints/{complaint_id}/approve",
        json={"approved": True}
    )
    assert res_approve.status_code == 200
    assert res_approve.json()["status"] == "SUBMITTED"

    # 4. Admin Simulation Control: Fast-Forward to SLA Breach & Escalation
    res_esc = client.post(f"/api/v1/complaints/{complaint_id}/escalate")
    assert res_esc.status_code == 200
    assert res_esc.json()["status"] == "ESCALATED"

    # 5. Submit Resolution Evidence (After Photo) & Verify
    after_img = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xFF\xDB\x00C\x00"
    res_verify = client.post(
        f"/api/v1/complaints/{complaint_id}/verify",
        files={"file": ("fixed_pothole.jpg", after_img, "image/jpeg")}
    )
    assert res_verify.status_code == 200
    assert res_verify.json()["status"] == "VERIFIED_RESOLVED"

    # 6. Verify Final Details & Timeline
    res_get = client.get(f"/api/v1/complaints/{complaint_id}")
    assert res_get.status_code == 200
    c_details = res_get.json()
    assert len(c_details["timeline"]) >= 3
    assert c_details["is_sla_breached"] is True or len(c_details["escalations"]) > 0

def test_water_leakage_classification_and_authority():
    test_img = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xFF\xDB\x00C\x00"
    response = client.post(
        "/api/v1/issues",
        files={"file": ("burst_water_pipe.jpg", test_img, "image/jpeg")},
        data={
            "latitude": "12.9716",
            "longitude": "77.5946",
            "address": "4th Cross Road, Demo Ward 04",
            "ward": "Demo Ward 04"
        }
    )
    assert response.status_code == 200
    issue_id = response.json()["issue_id"]

    res_analysis = client.post(f"/api/v1/issues/{issue_id}/analyze")
    assert res_analysis.status_code == 200
    analysis_data = res_analysis.json()

    assert analysis_data["category"] == "Water Leakage / Burst Pipeline"
    assert analysis_data["department_name"] == "Water Supply & Sewerage Board" or "Water" in analysis_data["department_name"]
    assert "water" in analysis_data["complaint"]["formatted_body"].lower()

