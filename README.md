```text
 ____                             _   ____                         _    ___ 
|  _ \ _ __ ___  _   _  __ _ | | |  _ \  ___ _ __  ___  ___  / \  |_ _|
| | | | '__/ _ \| | | |/ _` | '_ \ | | | |/ _ \ '_ \/ __|/ _ \/ _ \  | | 
| |_| | | | (_) | |_| | (_| | | | | |_| |  __/ | | \__ \  __/ ___ \ | | 
|____/|_|  \___/ \__,_|\__, |_| |_|____/ \___|_| |_|___/\___/_/   \_\___|
                       |___/                                            
```

# 🌱 DroughtSense AI
### Early drought risk intelligence for farmers — powered by AMD MI300X

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AMD ROCm](https://img.shields.io/badge/AMD-ROCm-red.svg)](https://www.amd.com/en/graphics/servers-solutions-rocm)
[![Built for AMD Hackathon ACT II](https://img.shields.io/badge/Hackathon-AMD_ACT_II-orange.svg)](https://lablab.ai/event/amd-developer-hackathon-act-ii)
[![Deployment Status](https://img.shields.io/badge/Deployment-Live-success.svg)](https://web-production-2344f.up.railway.app/)
[![Pytest Passing](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](https://github.com/Ohiodawn/DroughtSense/actions)

**DroughtSense AI is a professional multi-agent reasoning system that transforms live NASA climate data into actionable agricultural intelligence using a custom 7B model fine-tuned on the AMD Instinct™ MI300X.**

---

## 🚀 Live Demo

[![View Live Application](https://img.shields.io/badge/View_Live_Application-Click_Here-0b0d0e?style=for-the-badge&logo=railway)](https://web-production-2344f.up.railway.app/)

*The dashboard features a hyper-local 5-point climate average, interactive 30-day trends, a live Leaflet.js map, and agentic reasoning grounded in 45,000+ scientific publications.*

---

## 🌾 The Problem
Droughts are the single most devastating climate event for global food security, accounting for over **80% of total crop losses** in developing nations. Existing tools fail small farmers because they are either too technical, lack local environmental context, or rely on generic, closed-source LLMs that haven't been trained on specialized agricultural science.

---

## 🧠 The Solution
DroughtSense AI bridges the gap between raw scientific data and farm-level action by leveraging an **exclusive AMD AI infrastructure**.

*   **Real Data:** Live, 30-day agroclimatology stats (Precip, Temp, Soil) from **NASA's POWER API**.
*   **The Moat: DroughtSense-7B:** A custom model specifically fine-tuned on **45,000+ CGIAR research publications** using the AMD MI300X.
*   **Agentic Reasoning:** A collaborative workflow where specialized **Climatologist** and **Agronomist** agents perform deep analysis on the MI300X.
*   **Data Sovereignty:** By hosting our own model on private AMD hardware, sensitive food security data remains secure and independent of proprietary third-party APIs.

---

## 🏗️ Architecture Diagram

```mermaid
graph TD
    User[User Browser] -->|1. Search| Flask[Flask App on Railway]
    
    subgraph Context & Data
        Flask -->|2. Geocode| Geo[Nominatim / Google Maps]
        Flask -->|3. Fetch Stats| NASA[NASA POWER API]
        Flask -->|4. Query Graph| Graphify[Graphify Knowledge Base]
    end

    subgraph Multi-Agent AI Core (AMD MI300X)
        Flask -->|5. Dispatch| Orchestrator[Orchestrator Agent]
        Orchestrator -->|Analyze| Climatologist[Climatologist Agent]
        Orchestrator -->|Strategize| Agronomist[Agronomist Agent]
        Climatologist -.->|vLLM Request| MI300X[AMD MI300X Node]
        Agronomist -.->|vLLM Request| MI300X
        MI300X -->|DroughtSense-7B| Orchestrator
    end
    
    subgraph Presentation & Utility
        Flask -->|6. Render UI| UI[Interactive Dashboard]
        UI -->|Chart.js| Trends[30-Day Trends]
        UI -->|Leaflet.js| Map[Geospatial Map]
        UI -->|fpdf2| PDF[Branded PDF Report]
    end

    UI --> User
```

---

## ✨ Features
*   📡 **Live Climate Data:** Real-time retrieval of Precipitation, Temperature, and Soil Moisture via NASA POWER API.
*   🤖 **Multi-Agent Coordination:** Real-time terminal-style logs showing the collaboration between Climatologist and Agronomist agents.
*   🧠 **Custom 7B Fine-Tuning:** Powered by `DroughtSense-7B`, a specialized Qwen 2.5 model optimized for agricultural reasoning.
*   📍 **Interactive Mapping:** Visual location confirmation using **Leaflet.js** and high-accuracy **Google Maps** geocoding.
*   📊 **30-Day Trend Charts:** Interactive **Chart.js** visualizations of rainfall and temperature patterns.
*   📖 **Scientific Citations:** Transparent reasoning using the **Graphify** Knowledge Graph to cite scientific sources.
*   📄 **Portable Reports:** Downloadable, branded **PDF reports** for farmers to share with banks or aid agencies.
*   ⚡ **Production Hardened:** 24-hour intelligent caching, input sanitization, and 100% `pytest` pass rate.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **AI Hardware** | AMD Instinct™ MI300X GPU |
| **AI Runtime** | AMD ROCm™ 6.x |
| **Model Serving** | vLLM (OpenAI-compatible) |
| **Base Model** | Qwen 2.5 **7B** Instruct |
| **Fine-Tuned Model** | **DroughtSense-7B** (Custom LoRA Adapter) |
| **Knowledge Graph** | **Graphify** (Context Retrieval) |
| **Backend** | Python / Flask / Flask-Caching |
| **Frontend** | HTML5 / CSS3 / Vanilla JS / Chart.js / Leaflet.js |
| **Data APIs** | NASA POWER API / Google Maps / Nominatim |
| **Reporting** | fpdf2 (PDF Generation) |
| **Hosting** | Railway.app |
| **Testing** | Pytest / Requests-Mock |

---

## 🧪 Fine-Tuning Details

**DroughtSense-7B** represents the core intelligence of our system, specialized for agricultural risk.

*   **Training Hardware:** AMD MI300X Accelerator.
*   **Technique:** LoRA (Low-Rank Adaptation) with **Rank 64** for deep pattern recognition.
*   **Budget:** Optimized for a high-performance **3-hour** training window.
*   **Datasets:** 
    *   `CGIAR/gardian-ai-ready-docs`: Full corpus of agricultural research.
    *   `dippatel2506/agri-llm-raw-dataset`: Agriculture-focused text.
    *   `DARJYO/sawotiQ29_crop_optimization`: Specialized irrigation Q&A.
*   **Why it matters:** Unlike generic models, `DroughtSense-7B` understands specific drought response factors (Ky) and critical growth stages for 20+ crops.

---

## 💻 Getting Started (Local Setup)

### Prerequisites
*   Python 3.9+
*   An active **AMD Developer Cloud** vLLM endpoint.

### Installation
1.  **Clone & Install:**
    ```bash
    git clone https://github.com/Ohiodawn/DroughtSense.git
    cd DroughtSense
    pip install -r requirements.txt
    ```
2.  **Configure `.env`:**
    ```ini
    AMD_VLLM_BASE_URL="http://<YOUR_AMD_IP>:8000/v1"
    AMD_API_KEY="your-key"
    GOOGLE_MAPS_API_KEY="your-optional-key"
    FLASK_SECRET_KEY="your-secret"
    ```

### Run Commands
*   **Launch App:** `python app.py`
*   **Run Tests:** `pytest tests/`

---

## 🧬 Fine-Tuning & Knowledge Extraction

Reproduce our AMD-optimized pipeline in two steps:

1.  **Extract Knowledge Graph:**
    ```bash
    export OPENAI_API_BASE="http://<YOUR_AMD_IP>:8000/v1"
    graphify extract . --backend openai --model llama-3.1-8b-instruct --no-cluster
    ```
2.  **Run Fine-Tuning (3 Hours):**
    ```bash
    python fine_tuning/prepare_dataset.py
    python fine_tuning/fine_tune.py  # Optimized for AMD ROCm
    python fine_tuning/merge_model.py
    ```

---

## 📂 Project Structure
```bash
├── fine_tuning/      # AMD Training pipeline (Qwen-7B, LoRA, ROCm)
├── research/         # Agricultural Knowledge Base (Markdown/PDF)
├── services/         # Multi-agent logic, NASA API, Geospatial utils
├── static/           # Modern UI Assets (Nature-Tech CSS, main.js)
├── templates/        # Responsive Flask templates
├── tests/            # Full Pytest suite (Location, API, Services)
├── app.py            # Flask API & Agentic Orchestration
└── README.md         # Professional project documentation
```

---

## 🏆 Hackathon
**AMD Developer Hackathon ACT II | lablab.ai**
*   **Track:** AI Agents and Agentic Workflows
*   **Infrastructure:** Powered by **AMD Instinct™ MI300X**, **ROCm™**, and **vLLM**.

---

## 📄 License
Released under the [MIT License](LICENSE).
