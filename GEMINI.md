# DroughtSense AI - Project Instructions

## 🚨 Core Mandates

1. **Mandatory Documentation Review:** Before planning or executing any new feature, task, or significant code change, you MUST review `MASTERPLAN.md` and `ARCHITECTURE.md`. Your work must strictly align with the documented system architecture, prompt engineering strategy, and target tech stack (Flask, Vanilla JS, AMD MI300X vLLM).
2. **Mandatory Changelog Tracking:** Every time you complete a task, implement a feature, or fix a bug, you MUST append an entry to `CHANGELOG.md` detailing the changes made. Do not finish a task or session without ensuring the changelog is up to date.
3. **Mandatory Suggestion Tracking:** You MUST proactively look for areas of improvement (code quality, architecture, UX, security) and log them in `SUGGESTIONS.md`. Before starting a new phase, you MUST check `SUGGESTIONS.md` to see if any relevant suggestions should be incorporated. When a suggestion's status changes (Approved, Denied, Completed), you MUST update its status in `SUGGESTIONS.md`.

---

## 📅 System Development Lifecycle & Project Phases (Local-First Strategy)

The project follows a **Local-First** strategy, building out the intelligence and data layers before cloud deployment.

### Phase 1: Local Foundation (Infrastructure Layer)
*   **System Development Focus:** Establishing the local runtime and mock inference logic.
*   **Stages:** Python environment, Flask boilerplate, MockAI provider.
*   **Completion Condition:** Flask app returns hardcoded mock JSON assessments.

### Phase 2: Climate Intelligence (Data Acquisition Layer)
*   **System Development Focus:** Building the data ingestion engine.
*   **Stages:** Geocoding service, NASA POWER API integration, Data normalization.
*   **Completion Condition:** Utility script returns real, structured climate JSON for any region.

### Phase 3: Multi-Agent Architecture (The Differentiator)
*   **System Development Focus:** Moving from a simple prompt wrapper to a multi-agent orchestration framework.
*   **Stages:** Implement Climatologist, Agronomist, and Orchestrator agent roles; define agent interaction protocols.
*   **Completion Condition:** The backend orchestrates a multi-step conversation between agents to generate hyper-local recommendations based on NASA data.

### Phase 4: Knowledge Graph Integration (Contextual Intelligence Layer)
*   **System Development Focus:** Integrating **Graphify** to manage "Dark Data" and research context.
*   **Stages:** 
    *   Setup `graphify` to index drought research papers, climate documentation, and project code.
    *   Expose Knowledge Graph via MCP (Model Context Protocol) server.
    *   Implement "Graph Retrieval" step in the assessment pipeline to provide the AI with scientific context.
*   **Requirements:** `graphify` installed and indexed; scientific PDFs for the knowledge base.
*   **Completion Condition:** The AI assessment includes a "Research Context" or "Citations" section derived from the graph query.

### Phase 5: Backend Orchestration & API (Integration Layer)
*   **System Development Focus:** Connecting Data, Graph, and Agents into a unified pipeline.
*   **Stages:** `/api/assess` route assembly, Error handling, Request/Response normalization.
*   **Completion Condition:** A POST request executes the full workflow (Geocode -> NASA -> Graphify -> Multi-Agent) and returns a complete assessment.

### Phase 6: Interactive Interface (Presentation Layer)
*   **System Development Focus:** Creating the user-facing web application.
*   **Stages:** Responsive HTML/CSS, Vanilla JS Controller, Visual risk indicators, result rendering.
*   **Completion Condition:** User can input a city and see a formatted, evidence-backed drought report.

### Phase 7: AMD Fine-Tuning & Deployment (The Moat)
*   **System Development Focus:** Fine-tuning an open-source model on agricultural data and deploying to MI300X.
*   **Stages:** Dataset curation, Fine-tuning process, Provisioning MI300X, deploying vLLM with the custom model.
*   **Completion Condition:** Real-time multi-agent inference running on the custom fine-tuned model via AMD hardware.

### Phase 8: Production & Submission (Release Layer)
*   **Stages:** Gunicorn setup, Deployment (Render/Railway), E2E Testing, Video/Deck creation.
*   **Completion Condition:** Project submitted on lablab.ai and publicly accessible.
