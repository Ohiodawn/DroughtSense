# 💡 Project Suggestions & Improvements

This file tracks potential improvements, optimizations, and feature ideas for DroughtSense AI. As the AI agent works, it must proactively identify areas for improvement and log them here. 

**Status Options:**
- 🟡 `Proposed`: A new suggestion awaiting review.
- 🟢 `Approved`: Approved to be implemented during the relevant phase.
- 🔴 `Denied`: Decided against implementing (provide reason in Notes).
- ✅ `Completed`: Successfully implemented.

---

## Suggestions Log

| ID | Date | Suggestion / Idea | Context / Reasoning | Status | Notes |
|---|---|---|---|---|---|
| 001 | [Current Date] | *Example: Add caching for NASA API calls* | *NASA API data for the same region doesn't change by the minute. Caching will speed up the UI and save network calls.* | ✅ `Completed` | *Implemented via Flask-Caching.* |
| 002 | [Current Date] | *Local LLM Integration (Ollama)* | *For a more realistic local development experience before Phase 5, we can use Ollama to run Llama 3 locally.* | ✅ `Completed` | *Added Ollama provider.* |
| 006 | [Current Date] | *llama.cpp Integration* | *Add support for high-performance GGUF models via a local llama.cpp server.* | ✅ `Completed` | *Added LlamaCppProvider.* |
| 003 | [Current Date] | *Graphify Integration* | *Use Knowledge Graphs to connect climate data with scientific research papers and regional policies.* | ✅ `Completed` | *Infrastructure logic implemented.* |
| 004 | [Current Date] | *Input Sanitization & Validation* | *Ensure the region input is sanitized on the frontend and backend to prevent XSS or injection.* | ✅ `Completed` | *Implemented via bleach and regex.* |
| 005 | [Current Date] | *Automated Unit Testing* | *Add Python unit tests for the Geocoding and NASA services to ensure reliability.* | ✅ `Completed` | *Added pytest suite with requests-mock.* |
| 007 | [Current Date] | *Multi-Agent Architecture* | *Refactor the AI service to use specialized personas (Climatologist, Agronomist) collaborating to form the final report.* | ✅ `Completed` | *Implemented Climatologist, Agronomist, and Synthesizer agents.* |
| 008 | [Current Date] | *Agricultural Fine-Tuning* | *Curate a specialized dataset (crop tolerances, drought mitigation tactics) to fine-tune Llama 3.1 before deploying to AMD MI300X.* | 🟢 `Approved` | *Creates a strong "moat" against generic LLMs. Assigned to Phase 7.* |
| 009 | [Current Date] | *Agentic Process Visibility (UI)* | *Show 'Agent logs' in the UI (e.g., 'Climatologist is analyzing rainfall patterns...') to make the multi-agent workflow visible to users and judges.* | ✅ `Completed` | *Added terminal-style logs to the loading UI.* |
| 010 | [Current Date] | *30-Day Climate Trend Visualization* | *Visualize the 30-day precipitation and temperature trends using Chart.js to provide visual historical context.* | ✅ `Completed` | *Integrated interactive charts into the result dashboard.* |

*(New suggestions will be added below)*
