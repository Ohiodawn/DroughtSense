# 🏗 Architecture & Technical Documentation

This document provides a technical deep-dive into the architecture of **DroughtSense AI**, explaining how the various components interact to deliver real-time agricultural intelligence.

---

## 🗺 System Architecture Diagram

```mermaid
graph TD
    A[User / Farmer] -->|Enters Region Name| B[Frontend UI HTML/JS]
    B -->|POST /api/assess {region}| C[Flask Backend]
    
    subgraph Data Acquisition
        C -->|1. Geocode Region| D[Geocoding Service]
        D -->|Lat/Lon| C
        C -->|2. Fetch Climate Data| E[NASA POWER API]
        E -->|Precipitation, Temp, Soil Moisture| C
    end
    
    subgraph AI Inference / AMD Developer Cloud
        C -->|3. Constructed Prompt| F[AMD MI300X Node]
        F -->|vLLM Endpoint| G[Llama 3.1 Model]
        G -->|Structured JSON Output| F
        F -->|Response| C
    end
    
    C -->|4. Parsed JSON Results| B
    B -->|Displays Risk & Recommendations| A
```

---

## 🧩 Component Breakdown

### 1. Frontend (Client Interface)
- **Tech:** HTML5, CSS3, Vanilla JavaScript.
- **Role:** Provides a lightweight, accessible interface. Crucial for users in regions with poor internet connectivity.
- **Flow:** 
  - Captures the user's target region.
  - Sends an asynchronous `POST` request to the backend.
  - Displays a loading state while external APIs and AI inference run.
  - Renders the resulting JSON payload (Risk Level, Explanation, Recommendations) dynamically into the DOM.

### 2. Backend Server (Application Logic)
- **Tech:** Python, Flask, `requests`.
- **Role:** Acts as the central orchestrator (The "Agent"). It handles data fetching, data formatting, and communication with the AI model.
- **Flow:**
  - **Geocoding:** Converts the user's string input (e.g., "Nairobi, Kenya") into latitude and longitude coordinates.
  - **NASA POWER API Call:** Uses the coordinates to query the NASA Prediction Of Worldwide Energy Resources (POWER) API. We request recent agroclimatology data (e.g., last 30-60 days of precipitation, average temperature, and soil moisture).
  - **Prompt Assembly:** The backend aggregates this data and injects it into a strict System/User prompt template.
  - **Error Handling:** Catches API timeouts or missing data and returns graceful fallbacks to the frontend.

### 3. AI Inference Backend (AMD Infrastructure)
- **Tech:** AMD Developer Cloud, MI300X GPU, ROCm, vLLM.
- **Model:** Meta Llama 3.1 8B Instruct (or equivalent Qwen2.5 open-source model).
- **Role:** Analyzes the numerical climate data and applies agricultural reasoning to output a risk assessment.
- **Why vLLM on MI300X?** 
  - **High Throughput:** vLLM optimizes memory management (PagedAttention), allowing the MI300X to serve requests extremely fast.
  - **OpenAI Compatibility:** The vLLM server exposes an OpenAI-compatible REST API (`/v1/chat/completions`). This allows us to use standard Python `openai` libraries in our Flask backend, simply by overriding the `base_url`.
  - **Data Sovereignty:** By hosting the model ourselves on AMD infrastructure, regional agricultural vulnerability data is not shared with proprietary Big Tech APIs.

---

## 🧠 Prompt Engineering Strategy

The success of DroughtSense AI relies on strict prompt engineering to force the LLM to output usable, structured data rather than conversational text.

### System Prompt (Persona & Constraints)
```text
You are an expert agricultural and climatology AI assistant.
Your goal is to analyze recent climate data for a specific region and determine the drought risk level.
You must output YOUR ENTIRE RESPONSE as a valid, parsable JSON object.
Do not include markdown blocks, pleasantries, or any text outside of the JSON object.

JSON Schema:
{
  "risk_level": "Low" | "Medium" | "High" | "Critical",
  "explanation": "A plain language explanation (2-3 sentences) of why this risk level was assigned based on the data.",
  "recommendations": [
    "Actionable tip 1",
    "Actionable tip 2",
    "Actionable tip 3"
  ]
}
```

### User Prompt (Dynamic Data Injection)
```text
Analyze the drought risk for {Region Name}.
Recent Data (Last 30 days):
- Average Temperature: {avg_temp}°C
- Cumulative Precipitation: {total_precip} mm
- Soil Moisture Index: {soil_moisture}

Provide your assessment in the requested JSON format.
```

---

## 🔌 API Integrations

### NASA POWER API
- **Endpoint:** `https://power.larc.nasa.gov/api/temporal/daily/point`
- **Parameters:** `parameters=PRECTOTCORR,T2M,GWETROOT`, `community=AG`, `longitude={lon}`, `latitude={lat}`, `start={start_date}`, `end={end_date}`, `format=JSON`.
- **Note:** Free to use, no API key required, highly reliable for historical and near-real-time agroclimatology data.

## 🚀 Deployment Strategy
1. **AMD Droplet:** Left running during the hackathon period, exposing the vLLM port (e.g., 8000) securely (via IP whitelisting or bearer tokens).
2. **Web App:** Deployed on Render.com or Railway.app as a standard Python WSGI web service (using `gunicorn`). 
3. **Environment Secrets:** The deployed Web App holds the `AMD_VLLM_BASE_URL` and `AMD_VLLM_API_KEY` to authenticate against the MI300X instance.
