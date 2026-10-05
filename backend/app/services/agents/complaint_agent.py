import time
from typing import Dict, Any
from app.schemas.domain import AgentResponse
from app.services.providers.demo_providers import DemoLLMProvider

class ComplaintAgent:
    def __init__(self, provider=None):
        self.provider = provider or DemoLLMProvider()

    def process(self, issue_details: Dict[str, Any]) -> AgentResponse:
        start_time = time.time()
        try:
            generated = self.provider.generate_complaint_text(issue_details)
            
            payload = {
                "title": generated.get("title"),
                "category": issue_details.get("category"),
                "severity": issue_details.get("severity"),
                "address": issue_details.get("address"),
                "ward": issue_details.get("ward"),
                "department_name": issue_details.get("department_name"),
                "department_id": issue_details.get("department_id"),
                "formatted_body": generated.get("formatted_body"),
                "requested_action": generated.get("requested_action"),
                "evidence_url": issue_details.get("evidence_url")
            }

            return AgentResponse(
                agent="complaint_agent",
                status="SUCCESS",
                confidence=0.95,
                data=payload,
                errors=[],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
        except Exception as e:
            return AgentResponse(
                agent="complaint_agent",
                status="FAILED",
                confidence=0.0,
                data={},
                errors=[str(e)],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
