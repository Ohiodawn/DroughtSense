# DroughtSense AI - Masterplan & Technical Documentation

## 🌍 Overview
**Project Name:** DroughtSense AI  
**Tagline:** Early drought risk intelligence for farmers, powered by AMD MI300X and Knowledge Graphs.

DroughtSense AI is a web-based AI agent designed to help farmers and agricultural communities assess drought risk. It combines real-time climate data with a **Graphify-powered knowledge base** to provide evidence-backed risk assessments and recommendations.

## 🎯 The Problem & Why It Matters
- Droughts cause food insecurity.
- Farmers lack access to scientific context and real-time data.
- **The Solution:** A reasoning engine that connects live data with structured scientific knowledge using Knowledge Graphs (Graphify) and powerful AMD hardware.

## 🛠 Tech Stack
- **AI Inference:** AMD MI300X via vLLM.
- **Knowledge Graph:** **Graphify** (MCP server for scientific context).
- **Backend:** Python, Flask.
- **Frontend:** HTML5, CSS3, Vanilla JavaScript.
- **Data Sources:** NASA POWER API, Geocoding.

## ⚙️ User Flow & System Architecture
1. **Input:** User enters region name.
2. **Geocoding:** Backend converts name to Lat/Lon.
3. **Data Fetching:** Backend fetches live climate data.
4. **Context Retrieval:** Backend queries the **Graphify Knowledge Graph** for relevant scientific context/papers.
5. **AI Inference:** Backend sends climate + graph context to AMD-hosted LLM.
6. **Output:** Frontend displays detailed, evidence-backed report.

---

## 📅 Phased Execution Plan (Local-First Strategy)

### **Phase 1: Local Foundation**
- [x] Initialize Python environment and Flask boilerplate.
- [x] Implement `MockAI` provider.

### **Phase 2: Climate Intelligence**
- [x] Implement Geocoding service.
- [x] Integrate NASA POWER API.

### **Phase 3: AI Core & Reasoning**
- [x] Design prompt architecture.
- [x] Implement backend-to-AI logic (Cloud-ready).

### **Phase 4: Knowledge Graph (Graphify)**
- [x] Install `graphify` and index research/codebase.
- [x] Set up MCP server for graph queries.
- [x] Integrate graph context into the assessment pipeline.

### **Phase 5: Backend Orchestration**
- [x] Create `/api/assess` endpoint.
- [x] Integrate Graphify context into the final API output.

### **Phase 6: Frontend Development**
- [x] Build mobile-responsive UI.
- [x] Implement results rendering (including climate stats).

### **Phase 7: AMD Cloud Integration**
- [ ] Provision AMD MI300X.
- [ ] Switch to real AMD Inference (Awaiting AMD readiness).

### **Phase 8: Submission**
- [x] Deployment to Railway (LIVE).
- [ ] Final Submission materials.
