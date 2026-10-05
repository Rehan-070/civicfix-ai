import time
from typing import Optional, Dict, Any
from app.schemas.domain import AgentResponse

class LocationAgent:
    def process(
        self,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        address: Optional[str] = None,
        ward: Optional[str] = None
    ) -> AgentResponse:
        start_time = time.time()

        if lat is None and lon is None and not address:
            return AgentResponse(
                agent="location_agent",
                status="NEEDS_HUMAN_REVIEW",
                confidence=0.0,
                data={"message": "Location information is missing. Please provide GPS coordinates or address."},
                errors=["MISSING_LOCATION"],
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            )

        # Deterministic Ward / Jurisdiction Mapping for Demo
        # Default coordinates around Demo Ward 04 if not given
        resolved_lat = lat if lat is not None else 12.9716
        resolved_lon = lon if lon is not None else 77.5946
        resolved_ward = ward or "Demo Ward 04"
        jurisdiction = "Demo Municipal Corporation Zone 1"
        
        resolved_address = address or f"Main Arterial Road, {resolved_ward}, Metro Area"

        return AgentResponse(
            agent="location_agent",
            status="SUCCESS",
            confidence=0.95,
            data={
                "latitude": resolved_lat,
                "longitude": resolved_lon,
                "address": resolved_address,
                "jurisdiction": jurisdiction,
                "ward": resolved_ward
            },
            errors=[],
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
