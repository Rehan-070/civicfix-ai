import time
from typing import Dict, Any
from app.schemas.domain import AgentResponse
from app.services.providers.demo_providers import DemoLLMProvider

class EscalationAgent:
    def __init__(self, provider=None):
        self.provider = provider or DemoLLMProvider()

    def process(self, complaint_details: Dict[str, Any]) -> AgentResponse:
        start_time = time.time()
        try:
            escalation_payload = self.provider.generate_escalation_notice(complaint_details)
            return AgentResponse(
                agent="escalation_agent",
                status="SUCCESS",
                confidence=1.0,
                data=escalation_payload,
                errors=[],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
        except Exception as e:
            return AgentResponse(
                agent="escalation_agent",
                status="FAILED",
                confidence=0.0,
                data={},
                errors=[str(e)],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
