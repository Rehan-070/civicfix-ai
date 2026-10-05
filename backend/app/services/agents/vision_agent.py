import time
from typing import Dict, Any
from app.schemas.domain import AgentResponse
from app.services.providers.demo_providers import DemoVisionProvider

class VisionAgent:
    def __init__(self, provider=None):
        self.provider = provider or DemoVisionProvider()

    def process(self, image_path: str) -> AgentResponse:
        start_time = time.time()
        try:
            analysis = self.provider.analyze_image(image_path)
            execution_ms = int((time.time() - start_time) * 1000)
            
            confidence = analysis.get("confidence", 0.9)
            needs_review = analysis.get("needs_human_review", False)
            
            status = "SUCCESS"
            if needs_review or confidence < 0.75:
                status = "LOW_CONFIDENCE" if confidence < 0.75 else "NEEDS_HUMAN_REVIEW"

            return AgentResponse(
                agent="vision_agent",
                status=status,
                confidence=confidence,
                data=analysis,
                errors=[],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
        except Exception as e:
            return AgentResponse(
                agent="vision_agent",
                status="FAILED",
                confidence=0.0,
                data={},
                errors=[str(e)],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )
