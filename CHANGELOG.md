# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Added
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
