# CivicFix AI — System Architecture & Flaw Audit

## 1. Executive Summary & Product Positioning
CivicFix AI is an AI-powered multi-agent civic issue reporting, tracking, escalation, and resolution-verification platform.

> **Crucial Positioning Statement:**
> CivicFix AI is **NOT** a generic AI chatbot and is **NOT** an official government portal. It is an AI-assisted workflow and orchestration platform designed to empower citizens through structured issue detection, authority mapping, complaint tracking, SLA monitoring, and verification. All civic APIs in this version operate against a **Simulated Demo Civic API** clearly labeled as `CivicFix Demo Civic API — Simulation Only`.

---

## 2. Comprehensive Concept & Architecture Flaw Audit (A to Z)

Before writing production code, we audited the system design across technical, architectural, security, privacy, UX, AI, and legal vectors.

| Flaw ID | Flaw Category | Risk / Hazard | Practical Architectural Mitigation |
|---|---|---|---|
| **A** | **AI Hallucination Risks** | LLM generating non-existent addresses, fake department names, or non-factual complaint details. | Ground LLMs with deterministic JSON schemas, structured prompts, strict rule-based fallback templates, and validated schema output (Pydantic models). |
| **B** | **Wrong Authority Assignment** | AI assigning a pothole to the Sanitation Dept, causing delays and legal rejection. | Deterministic Authority Database lookup. AI outputs candidate department; backend validates against database mapping `(category, ward) -> department`. Low confidence (<0.85) triggers mandatory human confirmation. |
| **C** | **Wrong Jurisdiction** | Submitting ward 4 issue to ward 12 authority. | Boundary polygon / lookup mapping table for wards based on latitude/longitude or user-confirmed ward selection. |
| **D** | **Fake Location** | Citizens submitting complaints with spoofed or invalid GPS coordinates. | Geocoding validation, reverse-geocoding sanity checks, requirement for photo EXIF verification or explicit map confirmation by user. |
| **E** | **Duplicate Complaints** | Multiple citizens reporting the same pothole, creating database spam and authority bloat. | Spatial-Temporal Duplicate Detection Engine: Flag `POSSIBLE_DUPLICATE` if issue of same category occurs within 50 meters and 7 days. Prompt user with existing ticket before submission. |
| **F** | **False Complaints** | Spammers submitting fake images (e.g. photos of internet potholes). | Rate limiting per user IP/account, hash-based duplicate image detection, image authenticity heuristics, and required user authentication. |
| **G** | **Malicious Uploads** | Uploading malware, executable scripts, or extremely large files disguised as images. | Strict MIME-type checking (JPEG/PNG/WebP only), magic byte validation, file size limit (10MB), image re-encoding/sanitization via PIL. |
| **H** | **Complaint Spam** | Automated bot flooding the platform with automated submissions. | JWT authentication, IP & account rate limits (e.g. max 5 reports/hour), CAPTCHA/Turnstile hooks for public forms. |
| **I** | **API Failure** | Demo Civic API or external map service drops offline. | Circuit breaker pattern + `SUBMISSION_PENDING` retry queue. System degrades gracefully without losing user data. |
| **J** | **Agent Failure** | An individual AI agent crashes or returns invalid JSON. | Orchestrator wraps agent calls in try-catch with schema validation; fallback to deterministic logic (e.g. template-based complaint generation). |
| **K** | **LLM Timeout** | Vision/LLM endpoint hangs for >15 seconds. | Asynchronous processing with explicit client polling, 10-second request timeout, and fallback deterministic text generation. |
| **L** | **Vision Model Failure** | Vision model misidentifies or fails to detect an issue in a noisy photo. | Flag `needs_human_review = True`, pre-fill detected category with lowest threshold, and allow manual user correction in the UI. |
| **M** | **Low-Confidence Predictions** | System acting on 30% confidence prediction automatically. | Strict confidence thresholds (e.g., < 0.75 triggers `NEEDS_HUMAN_REVIEW` status; require explicit user override). |
| **N** | **SLA Calculation Errors** | LLM miscalculating hours or confusing timezones. | **Zero LLM SLA Logic.** SLAs are 100% calculated deterministically using UTC timestamps and configured department SLAs (e.g., Potholes = 72h). |
| **O** | **Incorrect Escalation** | Complaints escalated prematurely or to wrong escalation officer. | Backend deterministic trigger (`now() > submit_time + SLA_hours`). Escalation agent only writes the escalation summary notice. |
| **P** | **False Resolution Verification** | AI marking a photo of a clean street as "Pothole Fixed" when it's a different street. | Vision comparison returns probabilistic states (`VERIFIED_RESOLVED`, `LIKELY_RESOLVED`, `PARTIALLY_RESOLVED`, `NEEDS_HUMAN_REVIEW`). Low confidence requires human admin approval. |
| **Q** | **Camera Angle / Lighting Shift** | Before photo is close-up daylight, After photo is wide-angle night. | Verification prompt instructs vision model to score background landmark similarity and lighting disparity; flags `NEEDS_HUMAN_REVIEW` if angle mismatch is high. |
| **R** | **Poor Image Quality** | Blurry, dark, or pixelated evidence photos. | Image pre-analysis checks blur/brightness; prompts user if photo is unusable before running AI pipeline. |
| **S** | **Privacy Risks** | Faces, license plates, or house numbers exposed in public issue maps. | Redact private data, restrict precise location in public views to ward level, require authenticated access for full issue metadata. |
| **T** | **Location Privacy** | Exposing exact home coordinates of citizens. | Public map displays fuzzified coordinates (~100m radius grid) or ward centroids; precise coordinates accessible only to authorized admins/operators. |
| **U** | **Unauthorized Government Access** | Falsely asserting direct access to government internal portals. | Explicit UI banner: `Demo Civic API — Simulation`. Clear API decoupling with `CivicSubmissionProvider` interface. |
| **V** | **Irreversible Automated Actions** | AI autonomously filing complaints to external bodies. | **Mandatory Human Approval Step.** Complaints remain in `AWAITING_APPROVAL` until the user clicks `[Approve & Submit]`. |
| **W** | **Race Conditions** | Concurrent state transitions (e.g., user cancels while authority acknowledges). | Database level transaction locks (`SELECT FOR UPDATE`) and state machine guards enforcing valid next states. |
| **X** | **Concurrent Agent Execution** | Vision, location, and authority agents modifying state out of order. | Orchestrator pipeline follows strict sequential dependency execution: `Vision -> Location -> Authority -> Complaint -> User Approval -> Submission`. |
| **Y** | **Missing Audit Logs** | Inability to track why an authority was selected or when status changed. | Immutable `AuditLog` database entity tracking every actor, action, timestamp, entity ID, and state change payload. |
| **Z** | **Database Consistency Problems** | Foreign key orphan records or missing indices. | SQLAlchemy relational models with explicit foreign key constraints, indexes on status/ward/category, and transactional atomic writes. |

---

## 3. High-Level System Architecture

```
                                  +---------------------------------------+
                                  |         CITIZEN / ADMIN UI            |
                                  |   (React / Next.js / Tailwind CSS)    |
                                  +------------------+--------------------+
                                                     | REST APIs / JWT
                                                     v
                                  +---------------------------------------+
                                  |           FASTAPI BACKEND             |
                                  +------------------+--------------------+
                                                     |
                                                     v
                                  +---------------------------------------+
                                  |         SYSTEM ORCHESTRATOR           |
                                  |  (State Machine + Audit Engine)       |
                                  +--------+---------------------+--------+
                                           |                     |
           +-------------------------------+                     +-------------------------------+
           |                                                                                     |
           v                                                                                     v
+-----------------------+                                                             +-----------------------+
|  SPECIALIZED AGENTS   |                                                             | DETERMINISTIC LOGIC   |
|                       |                                                             |                       |
| - Vision Agent        |                                                             | - State Machine Guard |
| - Location Agent      |                                                             | - SLA Calculator      |
| - Authority Agent     |                                                             | - Dup Detection Engine|
| - Complaint Agent     |                                                             | - Authority Database  |
| - Escalation Agent    |                                                             | - RBAC & Auth Engine  |
| - Verification Agent  |                                                             | - Audit Logger        |
+-----------+-----------+                                                             +-----------+-----------+
            |                                                                                     |
            +-----------------------------------+-------------------------------------------------+
                                                |
                                                v
                               +----------------------------------+
                               |     PERSISTENCE & SIMULATION     |
                               |                                  |
                               | - PostgreSQL / SQLite (SQLAlchemy)|
                               | - Demo Civic API (Simulated)     |
                               | - Local Object / Image Storage   |
                               +----------------------------------+
```

---

## 4. State Machine Architecture

Every civic complaint adheres strictly to a deterministic finite state machine. Arbitrary status strings are prohibited.

```
       [ DRAFT ]
           │
           ▼
      [ ANALYZING ]
           │
           ▼
 [ AWAITING_APPROVAL ]  ◄───── (User edits or reviews generated draft)
           │
           ├──────────────────────────┐
           ▼ (User Approves)          ▼ (User Cancels)
     [ SUBMITTED ]              [ CANCELLED ]
           │
           ▼
   [ ACKNOWLEDGED ]
           │
           ▼
     [ ASSIGNED ]
           │
           ▼
    [ IN_PROGRESS ] ──────────┐ (SLA Breached)
           │                  │
           │                  ▼
           │            [ ESCALATED ]
           │                  │
           ▼                  │
      [ RESOLVED ] ◄──────────┘
           │
           ▼
 [ VERIFICATION_PENDING ]
           │
           ├──────────────────────────┬──────────────────────────┐
           ▼                          ▼                          ▼
 [ VERIFIED_RESOLVED ]      [ PARTIALLY_RESOLVED ]      [ UNRESOLVED ]
                                                                 │
                                                                 ▼
                                                        [ NEEDS_HUMAN_REVIEW ]
```

---

## 5. Agent Definitions & Contracts

All agents return standardized JSON structures conforming to `AgentResponseSchema`:

```json
{
  "agent": "vision_agent",
  "status": "SUCCESS | LOW_CONFIDENCE | NEEDS_HUMAN_REVIEW | FAILED",
  "confidence": 0.94,
  "data": {},
  "errors": [],
  "timestamp": "2026-09-30T17:20:00Z"
}
```

1. **Vision Agent**: Analyzes uploaded issue photos, identifies issue category (`pothole`, `garbage`, `streetlight`, `water_leakage`, `drainage`, `damaged_footpath`, `fallen_tree`), calculates confidence and severity (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
2. **Location Agent**: Validates GPS/address input, maps to administrative jurisdiction and ward, checks boundary accuracy.
3. **Authority Agent**: Queries Authority Rules database for category + ward mapping, applies severity-based routing, produces target department with confidence score.
4. **Complaint Agent**: Formulates a clear, objective, non-hallucinated civic complaint document adhering to civic filing standards.
5. **Submission Agent**: Validates human approval state, dispatches complaint payload to Demo Civic API, records official tracking ID (`CIV-2026-XXXXX`).
6. **Tracking Agent**: Periodically polls/queries Demo Civic API status, updates timeline, monitors SLA deadlines.
7. **Escalation Agent**: Triggered by SLA breach logic to formulate formal escalation brief to senior municipal supervisors.
8. **Verification Agent**: Evaluates before-and-after evidence images, assesses repair completeness, surface consistency, and returns verification confidence score.

---

## 6. Database Model Schema (SQLAlchemy / PostgreSQL)

Entities:
- `users`: ID, email, password_hash, full_name, role (`CITIZEN`, `ADMIN`, `OPERATOR`), created_at.
- `departments`: ID, code, name, contact_email, base_sla_hours.
- `authority_rules`: ID, department_id, category, ward, priority.
- `civic_issues`: ID, issue_code, user_id, title, category, severity, status, latitude, longitude, address, ward, department_id, confidence, description, created_at, updated_at.
- `evidences`: ID, issue_id, evidence_type (`BEFORE`, `AFTER`), image_url, file_size, mime_type, created_at.
- `complaints`: ID, complaint_number, issue_id, formatted_body, requested_action, submitted_at, user_approved.
- `complaint_status_history`: ID, complaint_id, previous_status, new_status, changed_by, notes, created_at.
- `escalations`: ID, complaint_id, escalation_reason, SLA_hours, breached_at, escalation_notes, created_at.
- `verification_results`: ID, complaint_id, result_status, confidence_score, evidence_summary, verified_at.
- `agent_executions`: ID, issue_id, agent_name, status, confidence, execution_time_ms, payload, created_at.
- `audit_logs`: ID, actor, action, entity_type, entity_id, metadata_json, created_at.

---

## 7. API Routing Plan

- `POST /api/v1/auth/register` & `POST /api/v1/auth/login`
- `POST /api/v1/issues` — Create draft issue + upload photo
- `POST /api/v1/issues/{id}/analyze` — Run Vision + Location + Authority agents
- `POST /api/v1/issues/{id}/complaint` — Generate complaint draft
- `POST /api/v1/complaints/{id}/approve` — Human approval step
- `POST /api/v1/complaints/{id}/submit` — Submit to Demo Civic API
- `GET /api/v1/complaints/{id}` — Get complaint details & tracking timeline
- `POST /api/v1/complaints/{id}/escalate` — Check SLA & trigger escalation
- `POST /api/v1/complaints/{id}/verify` — Upload after image & run Verification Agent
- `GET /api/v1/dashboard/stats` — Metrics for Citizen/Admin
- `GET /api/v1/map/issues` — Public/Admin Map markers
- `GET /api/v1/admin/audit-logs` — Audit log trail
- `POST /api/v1/admin/simulate-status` — Hackathon Demo Control Panel status fast-forward
- `POST /api/v1/demo/...` — Demo Civic API simulated endpoints (`/complaints`, `/departments`, etc.)

---

## 8. Provider Abstractions
- `VisionProvider`: `DemoVisionProvider`, `OpenAIVisionProvider`
- `LLMProvider`: `DemoLLMProvider`, `OpenAILLMProvider`
- `CivicSubmissionProvider`: `DemoCivicProvider`, `AuthorizedGovernmentProvider`
