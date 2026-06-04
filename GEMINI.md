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

### Phase 3: AI Core & Reasoning (Inference Layer)
*   **System Development Focus:** Designing the "Brain" and prompt architecture.
*   **Stages:** Prompt template engineering (System/User), response schema validation, local LLM testing (optional).
*   **Completion Condition:** Backend generates dynamic prompts based on real NASA data.

### Phase 4: Knowledge Graph Integration (Contextual Intelligence Layer)
*   **System Development Focus:** Integrating **Graphify** to manage "Dark Data" and research context.
*   **Stages:** 
    *   Setup `graphify` to index drought research papers, climate documentation, and project code.
    *   Expose Knowledge Graph via MCP (Model Context Protocol) server.
    *   Implement "Graph Retrieval" step in the assessment pipeline to provide the AI with scientific context.
*   **Requirements:** `graphify` installed and indexed; scientific PDFs for the knowledge base.
*   **Completion Condition:** The AI assessment includes a "Research Context" or "Citations" section derived from the graph query.

### Phase 5: Backend Orchestration & API (Integration Layer)
*   **System Development Focus:** Connecting Data, Graph, and AI into a unified pipeline.
*   **Stages:** `/api/assess` route assembly, Error handling, Request/Response normalization.
*   **Completion Condition:** A POST request executes the full workflow (Geocode -> NASA -> Graphify -> AI) and returns a complete assessment.

### Phase 6: Interactive Interface (Presentation Layer)
*   **System Development Focus:** Creating the user-facing web application.
*   **Stages:** Responsive HTML/CSS, Vanilla JS Controller, Visual risk indicators, result rendering.
*   **Completion Condition:** User can input a city and see a formatted, evidence-backed drought report.

### Phase 7: AMD Cloud & AI Integration (Scale Layer)
*   **System Development Focus:** Moving inference to AMD MI300X via vLLM.
*   **Stages:** Provisioning MI300X, deploying vLLM, switching to real `AMDInference` provider.
*   **Completion Condition:** Real-time inference running on AMD hardware.

### Phase 8: Production & Submission (Release Layer)
*   **Stages:** Gunicorn setup, Deployment (Render/Railway), E2E Testing, Video/Deck creation.
*   **Completion Condition:** Project submitted on lablab.ai and publicly accessible.
