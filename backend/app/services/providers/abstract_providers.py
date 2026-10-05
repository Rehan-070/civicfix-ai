from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseVisionProvider(ABC):
    @abstractmethod
    def analyze_image(self, image_path_or_url: str) -> Dict[str, Any]:
        """Analyzes an image for civic issue identification."""
        pass

    @abstractmethod
    def compare_resolution(self, before_url: str, after_url: str) -> Dict[str, Any]:
        """Compares before and after images for resolution verification."""
        pass

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_complaint_text(self, issue_details: Dict[str, Any]) -> Dict[str, Any]:
        """Generates formatted complaint text."""
        pass

    @abstractmethod
    def generate_escalation_notice(self, complaint_details: Dict[str, Any]) -> Dict[str, Any]:
        """Generates escalation notice."""
        pass

class BaseCivicSubmissionProvider(ABC):
    @abstractmethod
    def submit_complaint(self, complaint_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Submits complaint to municipal/civic gateway."""
        pass

    @abstractmethod
    def get_complaint_status(self, complaint_number: str) -> Dict[str, Any]:
        """Fetches complaint status from civic gateway."""
        pass
