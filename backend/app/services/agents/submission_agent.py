import time
from typing import Dict, Any
from app.schemas.domain import AgentResponse
from app.services.providers.demo_providers import DemoCivicProvider

class SubmissionAgent:
    def __init__(self, provider=None):
        self.provider = provider or DemoCivicProvider()

    def process(self, complaint_data: Dict[str, Any], user_approved: bool) -> AgentResponse:
        start_time = time.time()

        if not user_approved:
            return AgentResponse(
                agent="submission_agent",
                status="NEEDS_HUMAN_REVIEW",
                confidence=0.0,
                data={"message": "Human approval required before complaint submission."},
                errors=["NOT_APPROVED_BY_USER"],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )

        try:
            response = self.provider.submit_complaint(complaint_data)
            return AgentResponse(
                agent="submission_agent",
                status="SUCCESS",
                confidence=1.0,
                data=response,
                errors=[],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
        except Exception as e:
            return AgentResponse(
                agent="submission_agent",
                status="RETRYABLE_FAILURE",
                confidence=0.0,
                data={"message": "Demo Civic Gateway temporarily unavailable. Stored in SUBMISSION_PENDING queue."},
                errors=[str(e)],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
