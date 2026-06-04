# DroughtSense AI - Masterplan & Technical Documentation

## 🌍 Overview
**Project Name:** DroughtSense AI  
**Tagline:** Hyper-local drought intelligence through multi-agent coordination and AMD-accelerated fine-tuned models.

DroughtSense AI is an advanced, web-based agentic system designed to help farmers assess drought risk. It goes beyond simple LLM wrappers by combining **live NASA climate data**, a **custom fine-tuned model** running on AMD hardware, and a **multi-agent workflow** to provide hyper-local, evidence-backed agricultural intelligence that general-purpose AI models cannot replicate.

## 🎯 The Problem & Our Unique Value Proposition
- General LLMs (like ChatGPT) lack real-time local data and specific agricultural training, often providing generic advice.
- **The DroughtSense Formula:**
  - **Live NASA Data:** Hyper-local precision (Temperature, Precipitation, Soil Moisture).
  - **Fine-Tuned Model on AMD:** A custom model specifically trained on agricultural risk and drought mitigation, hosted on AMD MI300X.
  - **Multi-Agent Coordination:** An agentic workflow where specialized AI personas (Data Analyst, Climatologist, Agronomist) collaborate to form the final assessment.
  - **Hyper-Local Specificity:** Actionable recommendations tailored to the exact coordinates and current soil conditions.

## 🛠 Tech Stack
- **AI Inference & Fine-Tuning:** AMD MI300X via vLLM (Custom Fine-Tuned **DroughtSense-Qwen**).
- **Fine-Tuning Method:** LoRA (Low-Rank Adaptation) via ROCm-optimized `transformers` & `peft`.
- **Agentic Framework:** Multi-agent orchestration.
- **Knowledge Graph:** **Graphify** (MCP server for scientific context).
- **Backend:** Python, Flask.
- **Frontend:** HTML5, CSS3, Vanilla JavaScript.
- **Data Sources:** NASA POWER API, Geocoding, CGIAR/Gardian (Training).

## 🚀 The Moat: Custom Fine-Tuning on AMD
We don't just use a model; we build one. **DroughtSense-Qwen** is fine-tuned on 45,000+ agricultural research publications (CGIAR) and crop optimization datasets using AMD MI300X and LoRA.
- **Efficiency:** 0.5% trainable parameters via LoRA (Fast training, low compute cost).
- **Hardware:** Native ROCm support on MI300X (No CUDA dependency).
- **Domain Expertise:** Optimized for specific drought indices (SPI, SPEI) and agricultural mitigation strategies that general models fail to grasp.

## ⚙️ User Flow & System Architecture
1. **Input:** User enters region name.
2. **Context Gathering:** Backend geocodes, fetches live NASA climate data, and queries the Graphify knowledge base.
3. **Multi-Agent Orchestration:**
   - *Agent 1 (Climatologist):* Analyzes the NASA data and Graphify context to determine the meteorological risk.
   - *Agent 2 (Agronomist):* Takes the Climatologist's report and generates hyper-local crop mitigation strategies.
   - *Agent 3 (Orchestrator):* Synthesizes the final JSON report.
4. **AI Inference:** All agents run against the **custom fine-tuned** AMD-hosted LLM.
5. **Output:** Frontend displays detailed, evidence-backed report.

---

## 📅 Phased Execution Plan (Local-First Strategy)

### **Phase 1: Local Foundation**
- [x] Initialize Python environment and Flask boilerplate.
- [x] Implement `MockAI`, `Ollama`, and `llama.cpp` providers.

### **Phase 2: Climate Intelligence**
- [x] Implement Geocoding service and NASA POWER API.
- [x] Implement caching and automated unit testing.

### **Phase 3: Multi-Agent Architecture (The Differentiator)**
- [x] Design prompt architecture.
- [ ] Refactor AI service into a Multi-Agent workflow (Climatologist, Agronomist, Orchestrator).
- [ ] Ensure the workflow produces hyper-local recommendations.

### **Phase 4: Knowledge Graph (Graphify)**
- [x] Install `graphify` and setup infrastructure.
- [ ] Build the localized knowledge base (drought indices, regional crop data).

### **Phase 5: Backend Orchestration & Security**
- [x] Create `/api/assess` endpoint with input sanitization.
- [ ] Connect the Multi-Agent pipeline to the API output.

### **Phase 6: Frontend Development**
- [x] Build mobile-responsive UI with climate stats and citations.

### **Phase 7: AMD Fine-Tuning & Deployment (The Moat)**
- [ ] Install ROCm-optimized dependencies on AMD Droplet.
- [ ] **Dataset Curation:** Combine CGIAR, agri-llm-raw, and crop_optimization datasets into Q&A format.
- [ ] **LoRA Training:** Run fine-tuning on MI300X (Approx. 5 mins for Qwen-1.5B).
- [ ] **Model Merging:** Merge LoRA adapters into base model for high-speed vLLM inference.
- [ ] **Deployment:** Serve the unique `DroughtSense-Qwen` model via vLLM.

### **Phase 8: Submission**
- [x] Deployment to Railway (LIVE).
- [ ] Final Submission materials highlighting the unique formula.
