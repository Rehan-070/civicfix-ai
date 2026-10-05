import time
from typing import Dict, Any
from app.schemas.domain import AgentResponse
from app.services.providers.demo_providers import DemoVisionProvider

class VerificationAgent:
    def __init__(self, provider=None):
        self.provider = provider or DemoVisionProvider()

    def process(self, before_image_url: str, after_image_url: str) -> AgentResponse:
        start_time = time.time()
        
        if not after_image_url:
            return AgentResponse(
                agent="verification_agent",
                status="NEEDS_HUMAN_REVIEW",
                confidence=0.0,
                data={
                    "result": "NEEDS_HUMAN_REVIEW",
                    "evidence": ["Missing resolution evidence after-photo."],
                    "needs_human_review": True
                },
                errors=["MISSING_AFTER_IMAGE"],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )

        try:
            analysis = self.provider.compare_resolution(before_image_url, after_image_url)
            confidence = analysis.get("confidence", 0.9)
            result = analysis.get("result", "LIKELY_RESOLVED")
            needs_review = analysis.get("needs_human_review", False)

            status = "SUCCESS"
            if needs_review or confidence < 0.70:
                status = "NEEDS_HUMAN_REVIEW"
                result = "NEEDS_HUMAN_REVIEW"

            return AgentResponse(
                agent="verification_agent",
                status=status,
                confidence=confidence,
                data={
                    "result": result,
                    "confidence": confidence,
                    "evidence": analysis.get("evidence", []),
                    "needs_human_review": needs_review
                },
                errors=[],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
        except Exception as e:
            return AgentResponse(
                agent="verification_agent",
                status="FAILED",
                confidence=0.0,
                data={"result": "NEEDS_HUMAN_REVIEW", "needs_human_review": True},
                errors=[str(e)],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
