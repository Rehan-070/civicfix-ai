from typing import List, Dict

class ComplaintStatus:
    DRAFT = "DRAFT"
    ANALYZING = "ANALYZING"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    SUBMITTED = "SUBMITTED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    VERIFICATION_PENDING = "VERIFICATION_PENDING"
    VERIFIED_RESOLVED = "VERIFIED_RESOLVED"
    PARTIALLY_RESOLVED = "PARTIALLY_RESOLVED"
    UNRESOLVED = "UNRESOLVED"
    ESCALATED = "ESCALATED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

    ALL_STATES = {
        DRAFT, ANALYZING, AWAITING_APPROVAL, SUBMITTED, ACKNOWLEDGED,
        ASSIGNED, IN_PROGRESS, RESOLVED, VERIFICATION_PENDING,
        VERIFIED_RESOLVED, PARTIALLY_RESOLVED, UNRESOLVED, ESCALATED, FAILED, CANCELLED
    }

# Allowed State Transitions Matrix
VALID_TRANSITIONS: Dict[str, List[str]] = {
    ComplaintStatus.DRAFT: [ComplaintStatus.ANALYZING, ComplaintStatus.CANCELLED],
    ComplaintStatus.ANALYZING: [ComplaintStatus.AWAITING_APPROVAL, ComplaintStatus.FAILED, ComplaintStatus.CANCELLED],
    ComplaintStatus.AWAITING_APPROVAL: [ComplaintStatus.SUBMITTED, ComplaintStatus.CANCELLED, ComplaintStatus.ANALYZING],
    ComplaintStatus.SUBMITTED: [ComplaintStatus.ACKNOWLEDGED, ComplaintStatus.FAILED, ComplaintStatus.ESCALATED, ComplaintStatus.VERIFICATION_PENDING, ComplaintStatus.RESOLVED],
    ComplaintStatus.ACKNOWLEDGED: [ComplaintStatus.ASSIGNED, ComplaintStatus.IN_PROGRESS, ComplaintStatus.ESCALATED, ComplaintStatus.VERIFICATION_PENDING, ComplaintStatus.RESOLVED],
    ComplaintStatus.ASSIGNED: [ComplaintStatus.IN_PROGRESS, ComplaintStatus.ESCALATED, ComplaintStatus.RESOLVED, ComplaintStatus.VERIFICATION_PENDING],
    ComplaintStatus.IN_PROGRESS: [ComplaintStatus.RESOLVED, ComplaintStatus.ESCALATED, ComplaintStatus.FAILED, ComplaintStatus.VERIFICATION_PENDING],
    ComplaintStatus.ESCALATED: [ComplaintStatus.IN_PROGRESS, ComplaintStatus.ASSIGNED, ComplaintStatus.RESOLVED, ComplaintStatus.FAILED, ComplaintStatus.VERIFICATION_PENDING],
    ComplaintStatus.RESOLVED: [ComplaintStatus.VERIFICATION_PENDING, ComplaintStatus.VERIFIED_RESOLVED, ComplaintStatus.UNRESOLVED],
    ComplaintStatus.VERIFICATION_PENDING: [ComplaintStatus.VERIFIED_RESOLVED, ComplaintStatus.PARTIALLY_RESOLVED, ComplaintStatus.UNRESOLVED],
    ComplaintStatus.PARTIALLY_RESOLVED: [ComplaintStatus.IN_PROGRESS, ComplaintStatus.VERIFICATION_PENDING, ComplaintStatus.ESCALATED],
    ComplaintStatus.UNRESOLVED: [ComplaintStatus.ESCALATED, ComplaintStatus.IN_PROGRESS, ComplaintStatus.FAILED, ComplaintStatus.VERIFICATION_PENDING],
    ComplaintStatus.FAILED: [ComplaintStatus.SUBMITTED, ComplaintStatus.ANALYZING, ComplaintStatus.CANCELLED],
    ComplaintStatus.VERIFIED_RESOLVED: [],
    ComplaintStatus.CANCELLED: [],
}

class StateMachineError(Exception):
    def __init__(self, current_status: str, target_status: str):
        self.current_status = current_status
        self.target_status = target_status
        super().__init__(f"Invalid status transition from {current_status} to {target_status}")

def validate_transition(current_status: str, target_status: str) -> bool:
    """
    Validates if transitioning from current_status to target_status is allowed.
    Raises StateMachineError if illegal.
    """
    if target_status not in ComplaintStatus.ALL_STATES:
        raise ValueError(f"Unknown status '{target_status}'")
    
    allowed = VALID_TRANSITIONS.get(current_status, [])
    if target_status not in allowed:
        raise StateMachineError(current_status, target_status)
    return True
