# 🏙️ CivicFix AI

### From Civic Issues to Accountable Action

**CivicFix AI** is an AI-powered civic issue management platform designed to help citizens report local problems, understand their severity, identify the appropriate authorities, track complaint progress, and verify whether reported issues have been resolved.

The platform combines AI-assisted analysis, location-aware issue management, complaint tracking, escalation workflows, and resolution verification to make civic reporting more organized and transparent.

> **Project status:** Development project. Civic authority submissions currently use a simulated demo API; this project is not an official government portal and does not imply direct integration with municipal systems.

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Key Features](#-key-features)
- [How It Works](#-how-it-works)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Configuration](#-environment-configuration)
- [Docker Setup](#-docker-setup)
- [Security and Privacy](#-security-and-privacy)
- [Future Scope](#-future-scope)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚨 Problem Statement

Citizens regularly encounter civic problems such as:

- 🛣️ Potholes and damaged roads
- 💡 Broken streetlights
- 🗑️ Garbage accumulation and sanitation issues
- 💧 Water leakage and drainage problems
- 🌳 Fallen trees and damaged public infrastructure
- 🚶 Unsafe or damaged footpaths

However, reporting these problems can be difficult because information is often incomplete, complaints may reach the wrong department, duplicate reports create unnecessary workload, and citizens may struggle to track progress.

There is also a need for greater transparency around complaint prioritization, overdue issues, and the verification of completed repairs.

## 💡 Our Solution

CivicFix AI provides an intelligent workflow for turning an informal civic observation into a structured and trackable complaint.

The platform is designed to help users:

1. Describe a civic problem and provide supporting evidence.
2. Analyze the issue using AI-assisted processing.
3. Identify its category, severity, and relevant location.
4. Determine the appropriate department using authority-mapping rules.
5. Generate a structured complaint for user review.
6. Approve the complaint before submitting it to the configured civic service.
7. Track progress and identify overdue complaints.
8. Evaluate resolution evidence and maintain an auditable history.

The goal is to make civic issue management more organized, explainable, and accountable.

---

## ✨ Key Features

### 🤖 1. AI-Assisted Issue Analysis

Designed to help interpret civic complaints and supporting evidence.

- Issue category identification
- Severity assessment
- Structured complaint generation
- Confidence-based review
- Fallback handling for unsuccessful AI operations

### 📍 2. Location-Aware Reporting

Location information helps associate issues with the appropriate administrative area.

- Location and address validation
- Ward or jurisdiction mapping
- Location-aware authority selection
- Map-based issue visualization as supported by the implementation

### 🏢 3. Intelligent Authority Mapping

The platform is designed to select the relevant civic department using configured rules.

- Issue-category-to-department mapping
- Ward-based jurisdiction rules
- Severity-aware routing
- Human review when assignment confidence is insufficient

### 📝 4. Structured Complaint Generation

Convert issue details into a clear complaint draft containing relevant information and a requested action.

Users should review and approve the generated complaint before submission.

### 🔄 5. Complaint Tracking

The planned workflow supports tracking the progress of a complaint through defined states, from initial reporting to resolution and verification.

### ⏱️ 6. SLA Monitoring and Escalation

Service-level agreement (SLA) rules can be used to identify overdue complaints and support escalation workflows.

### 🖼️ 7. Resolution Verification

Before-and-after evidence can help assess whether a reported problem has been addressed.

Uncertain results should be referred for human review instead of being treated as automatically confirmed.

### 📊 8. Dashboards and Auditability

The architecture provides for issue statistics, complaint histories, status changes, and audit records to improve operational visibility.

**Note:** These capabilities describe the intended architecture and workflow. Individual features should be considered implemented only when available and tested in the current codebase.

---

## 🔄 How It Works

```text
Citizen Reports an Issue
          |
          v
   Upload Evidence
          |
          v
   AI-Assisted Analysis
          |
          v
 Location and Authority Mapping
          |
          v
  Generate Complaint Draft
          |
          v
    User Reviews Draft
          |
          v
    Approval Required
          |
          v
 Submit to Demo Civic API
          |
          v
   Track Complaint Status
          |
          v
    Monitor SLA Deadlines
          |
          v
  Evaluate Resolution Evidence
          |
          v
   Verification and Audit
```

The workflow is designed to keep users involved in important decisions and avoid treating AI-generated recommendations as authoritative facts.

---

## 🏗️ System Architecture

CivicFix AI uses a frontend-backend architecture with specialized AI processing and deterministic business rules.

```text
+--------------------------------------+
|          Frontend Interface          |
|          React Application           |
+-------------------+------------------+
                    |
                    | HTTP / REST API
                    v
+--------------------------------------+
|           FastAPI Backend            |
|                                      |
|  Authentication and API Endpoints    |
|  Request Validation                  |
|  Complaint Management                |
+-------------------+------------------+
                    |
                    v
+--------------------------------------+
|        Workflow Orchestrator         |
|                                      |
|  State Management                    |
|  AI Agent Coordination               |
|  Approval and Audit Workflow         |
+-------------+------------+-----------+
              |            |
              v            v
+-------------------+  +-------------------+
| AI-Assisted       |  | Deterministic     |
| Processing        |  | Business Rules    |
|                   |  |                   |
| Issue Analysis    |  | SLA Calculation   |
| Complaint Drafts  |  | Authority Mapping |
| Evidence Review   |  | Status Validation |
+---------+---------+  +---------+---------+
          |                      |
          +----------+-----------+
                     |
                     v
+--------------------------------------+
|        Data and Service Layer        |
|                                      |
| Database / Persistence               |
| Evidence Storage                     |
| Simulated Civic API                  |
| Audit and Tracking Records           |
+--------------------------------------+
```

The architecture is intended to separate AI-generated recommendations from deterministic operations such as state validation, SLA calculation, and authority-rule lookup.

For more technical details, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 🛠️ Technology Stack

The repository architecture identifies the following technologies:

| Technology | Purpose |
|---|---|
| React | Frontend user interface |
| Node.js | Frontend build environment |
| Python | Backend development |
| FastAPI | Backend REST API |
| Uvicorn | ASGI application server |
| SQLAlchemy | Database access and ORM |
| SQLite / PostgreSQL | Relational data persistence, depending on configuration |
| AI provider integrations | Issue analysis and language or vision processing |
| Docker | Containerized application packaging |

The precise dependencies and supported configuration options are defined in the frontend and backend project files.

---

## 📁 Project Structure

```text
civicfix-ai/
│
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── ARCHITECTURE.md
├── IMPLEMENTATION_PLAN.md
├── Dockerfile
└── README.md
```

*Note: The tree is a simplified overview. Consult the actual repository for the complete directory structure.*

---

## 🚀 Getting Started

### Prerequisites

Install the following tools:

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/downloads/) compatible with the backend requirements
- [Node.js](https://nodejs.org/) compatible with the frontend requirements
- npm
- Docker (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/Rehan-070/civicfix-ai.git
cd civicfix-ai
```

### 2. Set Up the Backend

Create and activate a Python virtual environment.

**Windows PowerShell**

```powershell
cd backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

**Linux / macOS**

```bash
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Start the backend from the directory containing the `app` package:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend address:

`http://127.0.0.1:8000`

If the application exposes FastAPI's interactive API documentation, it may be available at:

`http://127.0.0.1:8000/docs`

### 3. Set Up the Frontend

Open another terminal:

```bash
cd civicfix-ai/frontend

npm install
npm run dev
```

Open the local development URL displayed by Vite in the terminal.

### 4. Configure Frontend and Backend Communication

If the frontend calls the backend through an environment variable, configure the API base URL using the variable expected by the existing frontend code.

For local development, the backend address is typically:

`http://127.0.0.1:8000`

Use the actual variable name defined by the project. Configure CORS on the backend if the frontend and backend use different origins.

---

## ⚙️ Environment Configuration

Some configurations may require environment variables for AI providers, database connections, authentication, or other services.

Create the appropriate environment file based on the project's existing configuration and example files.

Example placeholders:

```env
# AI provider configuration
AI_PROVIDER=demo

# Database configuration
DATABASE_URL=sqlite:///./civicfix.db

# Authentication secret
JWT_SECRET=replace_with_a_secure_random_value
```

**Important:** The variable names above are illustrative. Check the backend settings and configuration modules before using them.

Never commit real API keys, database passwords, JWT secrets, or other credentials to GitHub.

The simulated civic service should remain clearly identified as a demo unless an authorized real-world integration is explicitly configured.

---

## 🐳 Docker Setup

A root-level Dockerfile is provided for building the frontend and packaging the Python backend into a container.

From the repository root, run:

```bash
docker build -t civicfix-ai .
```

Start the container:

```bash
docker run --rm -p 7860:7860 civicfix-ai
```

Then open:

`http://localhost:7860`

The Dockerfile configures the application to listen on port `7860`.

**Before deploying:** Verify required environment variables, database persistence, upload storage, frontend asset serving, and the application's startup behavior in the target environment.

---

## 🔐 Security and Privacy

CivicFix AI is designed with the following security principles in mind:

- **Human approval:** Review complaint drafts before submission.
- **Input validation:** Validate issue descriptions, coordinates, and uploaded files.
- **Credential protection:** Store secrets in environment variables or a secure secrets manager.
- **Role-based access:** Restrict administrative operations to authorized users.
- **Privacy-aware location handling:** Avoid unnecessarily exposing precise citizen locations.
- **AI confidence checks:** Flag uncertain classifications and verification results for review.
- **Auditability:** Record important status transitions and administrative actions.
- **Safe integrations:** Clearly distinguish simulated civic services from authorized government integrations.

These are design goals; production readiness requires implementing and testing the relevant controls.

---

## 🔮 Future Scope

Potential improvements include:

- [ ] Multilingual civic issue reporting
- [ ] Voice-based complaint submission
- [ ] Improved image-based issue classification
- [ ] Geospatial duplicate complaint detection
- [ ] More accurate ward and department mapping
- [ ] Real-time notifications and complaint updates
- [ ] Advanced civic issue heatmaps
- [ ] Better SLA analytics and escalation reporting
- [ ] Stronger resolution verification
- [ ] Authorized municipal API integrations
- [ ] Mobile-friendly and accessible reporting experiences
- [ ] Expanded automated testing and deployment pipelines

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.

   ```bash
   git checkout -b feature/your-feature
   ```

3. Make your changes and test them.
4. Commit your changes.

   ```bash
   git commit -m "Add: your feature"
   ```

5. Push your branch.

   ```bash
   git push origin feature/your-feature
   ```

6. Open a pull request describing your changes.

Please avoid including secrets, personal data, or real citizen complaint information in commits, logs, and test fixtures.

---

## 📄 License

Check the repository for a `LICENSE` file and follow the license terms specified there. If no license has been added, contact the repository owner before redistributing the project.

---

## 👨‍💻 Project Information

**Project:** CivicFix AI  
**Repository:** [Rehan-070/civicfix-ai](https://github.com/Rehan-070/civicfix-ai)  
**Category:** Artificial Intelligence · Civic Technology · Smart Cities

### Our Vision

To make civic issue reporting more accessible, transparent, and accountable by combining intelligent assistance with structured workflows and human oversight.

**CivicFix AI — Better reporting. Clearer accountability. Smarter communities.**
