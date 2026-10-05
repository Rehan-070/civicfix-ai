import os
import random
import time
from typing import Dict, Any
from PIL import Image
from app.services.providers.abstract_providers import (
    BaseVisionProvider,
    BaseLLMProvider,
    BaseCivicSubmissionProvider
)

from app.categories import CIVIC_CATEGORIES, normalize_category, VISION_CONFIDENCE_THRESHOLD

class DemoVisionProvider(BaseVisionProvider):
    def analyze_image(self, image_path_or_url: str) -> Dict[str, Any]:
        """Performs structured Vision AI analysis using visual perception and evidence heuristics."""
        path_lower = str(image_path_or_url).lower()
        filename_lower = os.path.basename(path_lower)

        cat_key = None
        confidence = 0.92
        needs_human_review = False
        observations = []

        # 1. Filename / Path Keyword Heuristics
        if any(w in filename_lower for w in ["water", "leak", "pipe", "burst", "flood", "plumbing"]):
            cat_key = "water_leakage"
            confidence = 0.94
        elif any(w in filename_lower for w in ["garbage", "trash", "waste", "bin", "litter", "refuse"]):
            cat_key = "garbage"
            confidence = 0.93
        elif any(w in filename_lower for w in ["light", "lamp", "bulb", "pole", "fixture", "dark"]):
            cat_key = "streetlight"
            confidence = 0.91
        elif any(w in filename_lower for w in ["tree", "branch", "trunk", "foliage", "wood"]):
            cat_key = "fallen_tree"
            confidence = 0.95
        elif any(w in filename_lower for w in ["drain", "sewer", "gutter", "clog"]):
            cat_key = "drainage"
            confidence = 0.90
        elif any(w in filename_lower for w in ["footpath", "sidewalk", "paver", "walkway"]):
            cat_key = "damaged_footpath"
            confidence = 0.89
        elif any(w in filename_lower for w in ["pothole", "cavity", "crater"]):
            cat_key = "pothole"
            confidence = 0.94
        elif any(w in filename_lower for w in ["crack", "road_damage", "tarmac"]):
            cat_key = "damaged_road"
            confidence = 0.88

        # 2. Image Color & Texture Feature Analysis via PIL
        if os.path.exists(image_path_or_url):
            try:
                img = Image.open(image_path_or_url).convert("RGB")
                width, height = img.size

                # Low resolution / blurry check
                if width < 150 or height < 150:
                    confidence = 0.62
                    needs_human_review = True

                # Sample pixel colors (thumbnailed 40x40)
                small_img = img.resize((40, 40))
                pixels = list(small_img.getdata())
                n = len(pixels)

                avg_r = sum(p[0] for p in pixels) / n
                avg_g = sum(p[1] for p in pixels) / n
                avg_b = sum(p[2] for p in pixels) / n

                # Color signature matching if category not strictly set by filename
                if not cat_key:
                    # Blue/water saturation check (water leakage or mud/pipe liquid)
                    if (avg_b > avg_r + 5) or (avg_g + avg_b > 2 * avg_r + 15):
                        cat_key = "water_leakage"
                        confidence = 0.88
                    # Foliage green check (tree/branch)
                    elif avg_g > avg_r + 15 and avg_g > avg_b + 10:
                        cat_key = "fallen_tree"
                        confidence = 0.90
                    # High brightness spot against dark (streetlight)
                    elif max(max(p) for p in pixels) > 240 and avg_r < 100:
                        cat_key = "streetlight"
                        confidence = 0.86
                    # Asphalt dark neutral gray (pothole / damaged road)
                    elif abs(avg_r - avg_g) < 10 and abs(avg_g - avg_b) < 10 and avg_r < 120:
                        cat_key = "pothole"
                        confidence = 0.85
                    else:
                        cat_key = "pothole"
                        confidence = 0.70
                        needs_human_review = True

            except Exception:
                pass

        if not cat_key:
            cat_key = "pothole"

        cat_info = CIVIC_CATEGORIES.get(cat_key, CIVIC_CATEGORIES["pothole"])

        if confidence < VISION_CONFIDENCE_THRESHOLD:
            needs_human_review = True

        return {
            "category": cat_info["key"],
            "display_name": cat_info["display_name"],
            "issue_type": cat_info["display_name"],  # Backward compatibility
            "confidence": round(confidence, 2),
            "severity": cat_info["default_severity"],
            "observations": cat_info["observations"],
            "evidence_summary": cat_info["evidence_summary"],
            "needs_human_review": needs_human_review,
            "department_name": cat_info["department_name"]
        }

    def compare_resolution(self, before_url: str, after_url: str) -> Dict[str, Any]:
        """Simulates before/after resolution verification using vision heuristics."""
        result = "VERIFIED_RESOLVED"
        confidence = 0.92
        needs_human_review = False
        evidence = [
            "Reported asphalt depression/pothole is no longer visible.",
            "Fresh bitumen resurfacing confirmed in target coordinate zone.",
            "Road surface is level and accessible for vehicular traffic."
        ]

        # Check for keywords in after URL if demoing negative or partial test cases
        after_lower = after_url.lower()
        if "unresolved" in after_lower or "dirty" in after_lower:
            result = "NOT_RESOLVED"
            confidence = 0.88
            evidence = [
                "Issue remains visible in the submitted evidence photo.",
                "No visible repairs or cleaning performed."
            ]
        elif "partial" in after_lower:
            result = "PARTIALLY_RESOLVED"
            confidence = 0.76
            needs_human_review = True
            evidence = [
                "Debris partially cleared, but main road damage persists.",
                "Surface patch incomplete."
            ]
        elif "blurry" in after_lower or "dark" in after_lower:
            result = "NEEDS_HUMAN_REVIEW"
            confidence = 0.55
            needs_human_review = True
            evidence = [
                "Camera angle or lighting disparity prevents definitive AI verification.",
                "Human operator review recommended."
            ]

        return {
            "result": result,
            "confidence": confidence,
            "evidence": evidence,
            "needs_human_review": needs_human_review
        }


class DemoLLMProvider(BaseLLMProvider):
    def generate_complaint_text(self, issue_details: Dict[str, Any]) -> Dict[str, Any]:
        category_name = issue_details.get("category", "Pothole")
        address = issue_details.get("address", "4th Cross Road, Demo Ward 04")
        cat_info = normalize_category(category_name)

        title = f"Urgent Civic Repair Request: {cat_info['display_name']} at {address}"
        body = cat_info["description_template"].format(address=address)
        action = cat_info["action_template"]

        return {
            "title": title,
            "formatted_body": body,
            "requested_action": action
        }

    def generate_escalation_notice(self, complaint_details: Dict[str, Any]) -> Dict[str, Any]:
        complaint_num = complaint_details.get("complaint_number", "CIV-2026-00000")
        category = complaint_details.get("category", "Civic Issue")
        dept = complaint_details.get("department", "Municipal Department")
        sla_hours = complaint_details.get("sla_hours", 72)

        reason = f"Service Level Agreement (SLA) breach: Resolution exceeded configured deadline of {sla_hours} hours."
        notes = (
            f"Formal Escalation Notice for Ticket #{complaint_num}.\n"
            f"Department: {dept}\n"
            f"Category: {category}\n"
            f"Reason: No field resolution reported within mandatory {sla_hours}h SLA.\n"
            f"Action Required: High-priority supervisor intervention and status update."
        )

        return {
            "escalation_reason": reason,
            "escalation_notes": notes
        }


class DemoCivicProvider(BaseCivicSubmissionProvider):
    def submit_complaint(self, complaint_payload: Dict[str, Any]) -> Dict[str, Any]:
        random_num = random.randint(10000, 99999)
        complaint_num = f"CIV-2026-{random_num}"
        return {
            "complaint_number": complaint_num,
            "status": "SUBMITTED",
            "gateway_message": "Complaint successfully ingested into CivicFix Demo Civic Gateway — Simulation Only",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    def get_complaint_status(self, complaint_number: str) -> Dict[str, Any]:
        return {
            "complaint_number": complaint_number,
            "status": "ACKNOWLEDGED",
            "department": "Road Department",
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
