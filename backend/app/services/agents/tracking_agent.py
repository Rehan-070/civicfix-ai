import time
import datetime
from typing import Dict, Any
from app.schemas.domain import AgentResponse
from app.services.providers.demo_providers import DemoCivicProvider
from app.services.sla_engine import is_sla_breached, calculate_sla_deadline

class TrackingAgent:
    def __init__(self, provider=None):
        self.provider = provider or DemoCivicProvider()

    def process(self, complaint_number: str, submitted_at: datetime.datetime, sla_hours: int) -> AgentResponse:
        start_time = time.time()
        try:
            status_data = self.provider.get_complaint_status(complaint_number)
            
            sla_deadline = calculate_sla_deadline(submitted_at, sla_hours)
            breached = is_sla_breached(submitted_at, sla_hours)
            
            status_data["sla_hours"] = sla_hours
            status_data["sla_deadline"] = sla_deadline.isoformat()
            status_data["is_sla_breached"] = breached

            return AgentResponse(
                agent="tracking_agent",
                status="SUCCESS",
                confidence=1.0,
                data=status_data,
                errors=[],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
        except Exception as e:
            return AgentResponse(
                agent="tracking_agent",
                status="FAILED",
                confidence=0.0,
                data={},
                errors=[str(e)],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
