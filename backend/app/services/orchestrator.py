import time
import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.entities import (
    CivicIssue, Complaint, ComplaintStatusHistory, Evidence, VerificationResult, Escalation
)
from app.services.state_machine import ComplaintStatus, validate_transition
from app.services.sla_engine import get_sla_hours, calculate_sla_deadline
from app.services.audit_service import log_audit, log_agent_execution
from app.services.duplicate_detection import check_duplicate_issue

from app.services.agents import (
    VisionAgent,
    LocationAgent,
    AuthorityAgent,
    ComplaintAgent,
    SubmissionAgent,
    TrackingAgent,
    EscalationAgent,
    VerificationAgent
)

class WorkflowOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.vision_agent = VisionAgent()
        self.location_agent = LocationAgent()
        self.authority_agent = AuthorityAgent()
        self.complaint_agent = ComplaintAgent()
        self.submission_agent = SubmissionAgent()
        self.tracking_agent = TrackingAgent()
        self.escalation_agent = EscalationAgent()
        self.verification_agent = VerificationAgent()

    def analyze_issue(self, issue_id: str, image_path: str, lat: Optional[float], lon: Optional[float], address: Optional[str]) -> Dict[str, Any]:
        """Runs Vision, Location, Authority, Cross-Validation, and Complaint agents sequentially."""
        issue = self.db.query(CivicIssue).filter(CivicIssue.id == issue_id).first()
        if not issue:
            raise ValueError("Issue not found")

        # Update status to ANALYZING
        validate_transition(issue.status, ComplaintStatus.ANALYZING)
        issue.status = ComplaintStatus.ANALYZING
        self.db.commit()

        # Step 1: Vision Agent
        t0 = time.time()
        v_res = self.vision_agent.process(image_path)
        log_agent_execution(self.db, "vision_agent", v_res.status, v_res.confidence, int((time.time() - t0) * 1000), issue.id, v_res.data)

        if v_res.status == "FAILED":
            issue.status = ComplaintStatus.FAILED
            self.db.commit()
            return {"status": "FAILED", "error": "Vision analysis failed"}

        issue.category = v_res.data.get("display_name") or v_res.data.get("issue_type", "Pothole")
        issue.severity = v_res.data.get("severity", "HIGH")
        issue.confidence = v_res.confidence

        # Step 2: Spatial Duplicate Detection Check (matching category + location)
        duplicate_info = None
        if lat is not None and lon is not None:
            duplicate_info = check_duplicate_issue(self.db, issue.category, lat, lon)

        # Step 3: Location Agent (Canonical Location Object)
        t1 = time.time()
        l_res = self.location_agent.process(lat, lon, address)
        log_agent_execution(self.db, "location_agent", l_res.status, l_res.confidence, int((time.time() - t1) * 1000), issue.id, l_res.data)

        # Canonical location assignment
        canonical_address = l_res.data.get("address") or address or "4th Cross Road, Demo Ward 04"
        canonical_ward = l_res.data.get("ward") or "Demo Ward 04"
        issue.latitude = l_res.data.get("latitude") or lat
        issue.longitude = l_res.data.get("longitude") or lon
        issue.address = canonical_address
        issue.ward = canonical_ward

        # Step 4: Authority Agent & Rule Validation
        t2 = time.time()
        a_res = self.authority_agent.process(
            self.db,
            issue.category,
            issue.severity,
            issue.ward,
            recommended_department_code=v_res.data.get("department_code")
        )
        log_agent_execution(self.db, "authority_agent", a_res.status, a_res.confidence, int((time.time() - t2) * 1000), issue.id, a_res.data)

        if a_res.status == "SUCCESS":
            issue.department_id = a_res.data.get("department_id")

        dept_name = a_res.data.get("department_name", "Road Department")

        # Step 5: Cross-Validation Pipeline Stage (Section 6)
        validation_checks = {
            "category_supported": True,
            "confidence_threshold_met": issue.confidence >= 0.75,
            "authority_validated": a_res.status == "SUCCESS",
            "location_validated": bool(issue.address and issue.ward),
            "evidence_attached": bool(image_path),
            "severity_valid": issue.severity in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        }

        all_checks_passed = all(validation_checks.values())
        needs_review = (not all_checks_passed) or v_res.data.get("needs_human_review", False) or (issue.confidence < 0.75)

        # Step 6: Complaint Agent Generation
        t3 = time.time()
        issue_details = {
            "category": issue.category,
            "severity": issue.severity,
            "address": issue.address,
            "ward": issue.ward,
            "department_name": dept_name,
            "department_id": issue.department_id,
            "evidence_url": image_path
        }
        c_res = self.complaint_agent.process(issue_details)
        log_agent_execution(self.db, "complaint_agent", c_res.status, c_res.confidence, int((time.time() - t3) * 1000), issue.id, c_res.data)

        # Create or update Draft Complaint record
        complaint = self.db.query(Complaint).filter(Complaint.issue_id == issue.id).first()
        if not complaint:
            random_code = f"CIV-2026-{int(time.time() * 1000) % 90000 + 10000}"
            complaint = Complaint(
                complaint_number=random_code,
                issue_id=issue.id,
                formatted_body=c_res.data.get("formatted_body", ""),
                requested_action=c_res.data.get("requested_action", ""),
                user_approved=False
            )
            self.db.add(complaint)
            self.db.commit()
            self.db.refresh(complaint)

        # Transition to AWAITING_APPROVAL
        validate_transition(issue.status, ComplaintStatus.AWAITING_APPROVAL)
        issue.status = ComplaintStatus.AWAITING_APPROVAL
        self.db.commit()

        log_audit(self.db, "orchestrator", "ANALYSIS_COMPLETED", "civic_issue", issue.id, {
            "category": issue.category,
            "confidence": issue.confidence,
            "department_id": issue.department_id,
            "duplicate": duplicate_info,
            "needs_human_review": needs_review
        })

        return {
            "status": "AWAITING_APPROVAL",
            "issue_id": issue.id,
            "issue_code": issue.issue_code,
            "category": issue.category,
            "category_key": v_res.data.get("category"),
            "confidence": issue.confidence,
            "severity": issue.severity,
            "ward": issue.ward,
            "address": issue.address,
            "department_name": dept_name,
            "observations": v_res.data.get("observations", []),
            "evidence_summary": v_res.data.get("evidence_summary", ""),
            "complaint": {
                "id": complaint.id,
                "complaint_number": complaint.complaint_number,
                "formatted_body": complaint.formatted_body,
                "requested_action": complaint.requested_action
            },
            "authority_confidence": a_res.confidence,
            "needs_human_review": needs_review,
            "duplicate_info": duplicate_info,
            "validation": {
                "passed": all_checks_passed,
                "checks": validation_checks
            }
        }

    def approve_and_submit(self, complaint_id: str, edited_body: Optional[str] = None, edited_action: Optional[str] = None) -> Dict[str, Any]:
        """Human approval step followed by submission to Demo Civic Gateway."""
        complaint = self.db.query(Complaint).filter(Complaint.id == complaint_id).first()
        if not complaint:
            raise ValueError("Complaint not found")
        
        issue = complaint.issue
        validate_transition(issue.status, ComplaintStatus.SUBMITTED)

        if edited_body:
            complaint.formatted_body = edited_body
        if edited_action:
            complaint.requested_action = edited_action

        complaint.user_approved = True
        
        # Dispatch to Submission Agent
        t0 = time.time()
        sub_res = self.submission_agent.process({
            "complaint_number": complaint.complaint_number,
            "category": issue.category,
            "department_id": issue.department_id,
            "formatted_body": complaint.formatted_body
        }, user_approved=True)
        log_agent_execution(self.db, "submission_agent", sub_res.status, sub_res.confidence, int((time.time() - t0) * 1000), issue.id, sub_res.data)

        if sub_res.status == "SUCCESS":
            now = datetime.datetime.now(datetime.timezone.utc)
            complaint.submitted_at = now
            sla_hrs = get_sla_hours(issue.category)
            complaint.sla_deadline = calculate_sla_deadline(now, sla_hrs)

            # State transition to SUBMITTED
            prev_status = issue.status
            issue.status = ComplaintStatus.SUBMITTED
            
            # Log history
            history = ComplaintStatusHistory(
                complaint_id=complaint.id,
                previous_status=prev_status,
                new_status=ComplaintStatus.SUBMITTED,
                changed_by="USER_APPROVED",
                notes="Citizen approved complaint submission to Demo Civic Gateway."
            )
            self.db.add(history)
            self.db.commit()

            log_audit(self.db, "citizen", "COMPLAINT_SUBMITTED", "complaint", complaint.id, {
                "complaint_number": complaint.complaint_number,
                "sla_hours": sla_hrs
            })

            return {"status": "SUBMITTED", "complaint": complaint, "gateway_response": sub_res.data}
        else:
            issue.status = ComplaintStatus.FAILED
            self.db.commit()
            return {"status": "FAILED", "error": "Submission to Demo Civic API failed"}

    def verify_resolution(self, complaint_id: str, after_image_url: str) -> Dict[str, Any]:
        """Evaluates before/after resolution evidence using Verification Agent."""
        complaint = self.db.query(Complaint).filter(Complaint.id == complaint_id).first()
        if not complaint:
            raise ValueError("Complaint not found")

        issue = complaint.issue
        
        # Create Evidence record for AFTER photo
        after_ev = Evidence(
            issue_id=issue.id,
            evidence_type="AFTER",
            image_url=after_image_url
        )
        self.db.add(after_ev)
        self.db.commit()

        # Find BEFORE evidence photo
        before_ev = self.db.query(Evidence).filter(Evidence.issue_id == issue.id, Evidence.evidence_type == "BEFORE").first()
        before_url = before_ev.image_url if before_ev else after_image_url

        # Transition to VERIFICATION_PENDING
        validate_transition(issue.status, ComplaintStatus.VERIFICATION_PENDING)
        issue.status = ComplaintStatus.VERIFICATION_PENDING
        self.db.commit()

        # Run Verification Agent
        t0 = time.time()
        v_res = self.verification_agent.process(before_url, after_image_url)
        log_agent_execution(self.db, "verification_agent", v_res.status, v_res.confidence, int((time.time() - t0) * 1000), issue.id, v_res.data)

        ver_result_str = v_res.data.get("result", "NEEDS_HUMAN_REVIEW")
        conf_score = v_res.confidence
        summary_text = "\n".join(v_res.data.get("evidence", []))

        v_record = VerificationResult(
            complaint_id=complaint.id,
            result_status=ver_result_str,
            confidence_score=conf_score,
            evidence_summary=summary_text,
            needs_human_review=v_res.data.get("needs_human_review", False),
            after_evidence_id=after_ev.id
        )
        self.db.add(v_record)

        # Update Issue final status based on verification result
        target_status = ComplaintStatus.VERIFIED_RESOLVED
        if ver_result_str in ["PARTIALLY_RESOLVED", "NEEDS_HUMAN_REVIEW"]:
            target_status = ComplaintStatus.PARTIALLY_RESOLVED if ver_result_str == "PARTIALLY_RESOLVED" else ComplaintStatus.UNRESOLVED

        validate_transition(issue.status, target_status)
        prev_s = issue.status
        issue.status = target_status

        hist = ComplaintStatusHistory(
            complaint_id=complaint.id,
            previous_status=prev_s,
            new_status=target_status,
            changed_by="VERIFICATION_AGENT",
            notes=f"AI-assisted verification result: {ver_result_str} (Confidence: {int(conf_score*100)}%)"
        )
        self.db.add(hist)
        self.db.commit()

        log_audit(self.db, "system", "RESOLUTION_VERIFIED", "complaint", complaint.id, {
            "result_status": ver_result_str,
            "confidence": conf_score
        })

        return {
            "status": target_status,
            "verification_id": v_record.id,
            "result_status": v_record.result_status,
            "confidence_score": v_record.confidence_score,
            "verification_data": v_res.data
        }
