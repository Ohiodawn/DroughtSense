# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Graphify Integration Plan:** Added Phase 4 to the development lifecycle for Knowledge Graph integration.
- **Phase 6 Preparation:** Implemented file-based caching for NASA API and Geocoding using `Flask-Caching`.
- Created `Procfile` for production deployment.
- Created `.gitignore` to protect environment variables and cache data.
- **Phase 5 Preparation:** Implemented `AMDInference` class in `services/ai_service.py`.

### Changed
- Shifted project strategy to **Local-First**, prioritizing local backend/frontend development and data integration before AMD Cloud setup.
- Reorganized `GEMINI.md` and `MASTERPLAN.md` phases to reflect the local-first roadmap.
- Expanded `GEMINI.md` phases into a detailed "System Development Lifecycle," explicitly mapping each phase to a specific architectural layer.
- Created `README.md` providing a high-level overview, live demo placeholder links, features list, tech stack, and instructions for local setup.
- Created `ARCHITECTURE.md` detailing the system architecture, component interactions, prompt engineering strategy, and API integration.
- Created `GEMINI.md` to establish core mandates for the AI agent (reviewing documentation and maintaining this changelog) and to outline the project phases.
- Initialized this `CHANGELOG.md` file.
