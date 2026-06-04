# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Added
- **UI/UX Overhaul:** Implemented a modern "Nature-Tech" design system with a sidebar layout, enhanced typography, and micro-interactions.
- **Input Enforcement:** Restricted location inputs to English (Latin) characters only to ensure compatibility across all downstream APIs and services.
- Updated `location_utils.py` and `app.py` with refined regex sanitization.
- Added frontend validation and user feedback for non-English character inputs.
- **PDF Report Generation:** Added a professional 'Download PDF Report' feature for farmers to share assessments with institutions.
- Created `services/pdf_service.py` using `fpdf2` with custom branding and formatted results.
- Added a new `/api/report` endpoint and UI download button.
- **Interactive Mapping:** Integrated **Leaflet.js** to provide a real visual map of the resolved location.
- Added a visual marker on the map for the exact coordinates being assessed.
- Implemented automatic map centering and zooming based on geocoding results.
- **Google Maps Integration:** Added optional support for the Google Maps Geocoding API.
- Implemented a provider-based geocoding logic: Google Maps (if key present) -> Nominatim (Fallback).
- Added `googlemaps` to `requirements.txt`.
- **Agentic Process Visibility:** Added a terminal-style log to the loading UI to show real-time multi-agent coordination (Climatologist, Agronomist, Synthesizer).
- **Climate Trend Visualization:** Integrated `Chart.js` to visualize 30-day precipitation and temperature trends.
- Updated `services/nasa_service.py` to return daily time-series data alongside summarized averages.
- Added interactive line charts to the dashboard for enhanced visual evidence.
- **Robust Location Resolution System:** Complete overhaul of the geocoding pipeline to ensure geospatial accuracy.
- Created `services/location_utils.py` for coordinate sanity checks, bounding box centroid calculation, and ocean zone rejection.
- Implemented a **Location Confirmation Step** in the UI with a Multiple Match Selector for ambiguous inputs.
- Implemented **NASA POWER Radius Averaging** (5-point average) for large administrative regions to provide more representative climate data.
- Added automated robustness tests in `tests/test_location_robustness.py`.
- **Phase 3 Complete:** Implemented a sophisticated **Multi-Agent Orchestration** workflow.
- **Fine-Tuning Architecture:** Integrated the comprehensive AMD-accelerated Fine-Tuning phase into the project roadmap.
- Created `fine_tuning/` directory containing the full training pipeline:
  - `prepare_dataset.py`: Script to curate agricultural datasets from Hugging Face (CGIAR, Agri-LLM, etc.) into a Q&A format.
  - `fine_tune.py`: AMD-optimized LoRA training script using ROCm, `transformers`, and `peft`.
  - `merge_model.py`: Utility to merge LoRA adapters with the base Qwen model for vLLM deployment.
- **Strategic Pivot:** Redefined project scope to emphasize unique value propositions: Multi-Agent Workflow and AMD Fine-Tuned Models.
- **API Testing:** Created `tests/test_api.py` verifying the full data-to-mock-AI pipeline.
- **llama.cpp Integration:** Added `LlamaCppProvider` to `services/ai_service.py` to support inference via local llama.cpp servers.
- Refactored local provider selection to use `LOCAL_AI_PROVIDER` environment variable (supporting `ollama`, `llama.cpp`, and `mock`).
- **Local LLM Integration:** Added `OllamaProvider` to `services/ai_service.py`.
- **Automated Testing:** Implemented a unit test suite using `pytest` and `requests-mock`.
- Created `tests/test_geocoding.py` and `tests/test_nasa_service.py` with full coverage for data acquisition.
- Added `pytest` and `requests-mock` to `requirements.txt`.
- **Security Hardening:** Implemented input sanitization and validation on both frontend and backend.
- Integrated `bleach` and regex-based cleaning to prevent XSS and injection in the region input.
- Added frontend length and character checks.
- **Public Repository Live:** Synchronized local project with `Ohiodawn/DroughtSense` on GitHub.
- **Production Deployment:** Application is live on **Railway**.
- **Phase 4 & 5 Complete:** Integrated Graphify knowledge retrieval and assembled the final backend orchestration pipeline.
- Created `services/graph_service.py` and updated AI service to include scientific context.
- Updated UI with "Scientific Citations" and improved styling/icons.
- **Phase 6 Preparation:** Implemented file-based caching for NASA API and Geocoding.

### Changed
- Shifted project strategy to **Local-First**, prioritizing local backend/frontend development and data integration before AMD Cloud setup.
- Reorganized `GEMINI.md` and `MASTERPLAN.md` phases to reflect the local-first roadmap.
- Expanded `GEMINI.md` phases into a detailed "System Development Lifecycle," explicitly mapping each phase to a specific architectural layer.
- Created `README.md` providing a high-level overview, live demo placeholder links, features list, tech stack, and instructions for local setup.
- Created `ARCHITECTURE.md` detailing the system architecture, component interactions, prompt engineering strategy, and API integration.
- Created `GEMINI.md` to establish core mandates for the AI agent (reviewing documentation and maintaining this changelog) and to outline the project phases.
- Initialized this `CHANGELOG.md` file.
