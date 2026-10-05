import time
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.schemas.domain import AgentResponse
from app.models.entities import Department, AuthorityRule
from app.categories import normalize_category, CIVIC_CATEGORIES

class AuthorityAgent:
    def process(
        self,
        db: Session,
        issue_type: str,
        severity: str,
        ward: Optional[str] = None,
        recommended_department_code: Optional[str] = None
    ) -> AgentResponse:
        start_time = time.time()
        
        # Resolve category dictionary
        cat_info = normalize_category(issue_type)
        expected_dept_code = cat_info["department_code"]

        mismatch_corrected = False
        mismatch_note = ""

        # Validate against recommended department if provided
        if recommended_department_code and recommended_department_code != expected_dept_code:
            mismatch_corrected = True
            mismatch_note = f"Authority mismatch detected. Category '{cat_info['display_name']}' is configured for {cat_info['department_name']} ({expected_dept_code}). Overriding recommendation ({recommended_department_code})."

        # 1. Query AuthorityRule DB
        query = db.query(AuthorityRule).filter(AuthorityRule.category.ilike(f"%{cat_info['display_name']}%"))
        rule_ward = None
        if ward:
            rule_ward = query.filter((AuthorityRule.ward == ward) | (AuthorityRule.ward.is_(None))).first()
        else:
            rule_ward = query.first()

        dept = None
        source = "authority_rules_db"

        if rule_ward and rule_ward.department:
            dept = rule_ward.department
        else:
            # Fallback query by code
            dept = db.query(Department).filter(Department.code == expected_dept_code).first()
            source = "deterministic_category_rule"

        if not dept:
            # Fallback to any department or create fallback record
            dept = db.query(Department).filter(Department.code == "ROAD").first()

        confidence = 0.95 if not mismatch_corrected else 0.88

        return AgentResponse(
            agent="authority_agent",
            status="SUCCESS",
            confidence=confidence,
            data={
                "department_id": dept.id if dept else 1,
                "department_code": dept.code if dept else expected_dept_code,
                "department_name": dept.name if dept else cat_info["department_name"],
                "base_sla_hours": dept.base_sla_hours if dept else cat_info["sla_hours"],
                "category": cat_info["display_name"],
                "category_key": cat_info["key"],
                "severity": severity,
                "source": source,
                "mismatch_corrected": mismatch_corrected,
                "mismatch_note": mismatch_note
            },
            errors=[],
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )

