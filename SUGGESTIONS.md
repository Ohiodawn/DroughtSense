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
| 002 | [Current Date] | *Local LLM Integration (Ollama)* | *For a more realistic local development experience before Phase 5, we can use Ollama to run Llama 3 locally.* | 🟡 `Proposed` | *Useful if the user wants to test prompt responses without mocking.* |
| 003 | [Current Date] | *Graphify Integration* | *Use Knowledge Graphs to connect climate data with scientific research papers and regional policies.* | ✅ `Completed` | *Infrastructure logic implemented.* |
| 004 | [Current Date] | *Input Sanitization & Validation* | *Ensure the region input is sanitized on the frontend and backend to prevent XSS or injection.* | ✅ `Completed` | *Implemented via bleach and regex.* |
| 005 | [Current Date] | *Automated Unit Testing* | *Add Python unit tests for the Geocoding and NASA services to ensure reliability.* | 🟡 `Proposed` | *Prevents regressions during AMD integration.* |

*(New suggestions will be added below)*
