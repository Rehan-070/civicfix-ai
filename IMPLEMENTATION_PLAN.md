# CivicFix AI — Implementation Plan

This document outlines the phased development roadmap for CivicFix AI.

---

## Roadmap Phases

### Phase 0: Environment & Audit Verification
- [x] Inspect local host environment (Python 3.10, Node.js 22, npm 10).
- [x] Perform 26-point architectural audit (A to Z).
- [x] Create `ARCHITECTURE.md`.
- [x] Create `IMPLEMENTATION_PLAN.md`.

### Phase 1: Data Models & Persistence Foundation
- [x] Initialize Python backend project structure (`backend/`).
- [x] Implement SQLAlchemy ORM models (`User`, `Department`, `AuthorityRule`, `CivicIssue`, `Evidence`, `Complaint`, `ComplaintStatusHistory`, `Escalation`, `VerificationResult`, `AgentExecution`, `AuditLog`).
- [x] Setup SQLite/PostgreSQL database initialization script & seed data (Road, Sanitation, Streetlight, Water, Drainage, Tree depts & SLA rules).

### Phase 2: Core Backend Engine & Provider Abstractions
- [x] Configure FastAPI app with CORS, structured logging, request context IDs, and global exception handlers.
- [x] Build provider interfaces (`VisionProvider`, `LLMProvider`, `CivicSubmissionProvider`, `MapProvider`).
- [x] Implement JWT authentication & password hashing utilities.

### Phase 3: Simulated Demo Civic API
- [x] Create dedicated router `/api/v1/demo` for simulated municipal responses:
  - `POST /api/v1/demo/complaints`
  - `GET /api/v1/demo/complaints/{id}`
  - `PATCH /api/v1/demo/complaints/{id}/status`
  - `POST /api/v1/demo/complaints/{id}/escalate`
  - `POST /api/v1/demo/complaints/{id}/evidence`
  - `GET /api/v1/demo/departments`
  - `GET /api/v1/demo/complaints/{id}/timeline`

### Phase 4: Issue Upload & File Management
- [x] Implement file upload validator (magic byte MIME check, JPEG/PNG/WebP, 10MB limit).
- [x] Issue creation endpoints with location parser and image storage.

### Phase 5: Vision Agent
- [x] Build `VisionAgent` service with structured output (`issue_type`, `confidence`, `severity`, `evidence_summary`, `needs_human_review`).
- [x] Support primary demo issue (Pothole) and extended categories (Garbage, Streetlight, Water Leakage, Drainage, Footpath, Tree).

### Phase 6: Location & Authority Agents
- [x] Build `LocationAgent` for geocoding, ward determination, and duplicate detection within 50-meter radius.
- [x] Build `AuthorityAgent` leveraging configured `AuthorityRule` database table with confidence validation.

### Phase 7: Complaint Agent & Human Approval State Machine
- [x] Implement `ComplaintAgent` to generate formal complaint draft.
- [x] Enforce `AWAITING_APPROVAL` status state machine gate.
- [x] Build submission endpoint executing `SubmissionAgent` only upon citizen approval.

### Phase 8: Tracking Agent & Deterministic SLA Engine
- [x] Build `TrackingAgent` to poll Demo Civic API and log status transitions.
- [x] Implement deterministic SLA calculation based on category/department rules.

### Phase 9: Escalation Agent
- [x] Implement SLA breach detection background check.
- [x] Build `EscalationAgent` to summarize breach reasons and update status to `ESCALATED`.

### Phase 10: Resolution Verification Agent
- [x] Build `VerificationAgent` for before-and-after image analysis.
- [x] Support confidence scoring (`VERIFIED_RESOLVED`, `LIKELY_RESOLVED`, `PARTIALLY_RESOLVED`, `NOT_RESOLVED`, `NEEDS_HUMAN_REVIEW`).

### Phase 11: Web Application Frontend (Next.js / React + Tailwind CSS)
- [x] Initialize frontend application with modern typography, dark mode glassmorphism, responsive layout.
- [x] Pages:
  1. Landing Page (Hero, Value Prop, CTA)
  2. Issue Reporting Flow (Photo upload, Location picker, AI Analysis state)
  3. Complaint Preview & Approval UI
  4. Citizen Tracking Dashboard (Status timeline, SLA countdown)
  5. Interactive Civic Issue Map (Leaflet markers)
  6. Admin Control Panel (Demo simulation fast-forward controls, agent activity, audit logs)

### Phase 12: Security, Testing & Audit Trail
- [x] Write unit & integration tests covering state machine, duplicate detection, SLA, agents, and APIs.
- [x] Ensure full audit logging across all state mutations and agent calls.

### Phase 13: End-to-End Hackathon Demo Package
- [x] Seed complete automated end-to-end demo scenario ("Run Demo Scenario" button).
- [x] Verify 5–10 minute hackathon presentation flow.

