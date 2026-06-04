# 🌱 DroughtSense AI

> **Early drought risk intelligence for farmers, powered by AMD MI300X.**

*Created for the **AMD Developer Hackathon ACT II** on lablab.ai*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Live Demo & Pitch
- **Live Application:** [Deploy URL Placeholder]
- **Pitch Video:** [YouTube/Vimeo URL Placeholder]
- **Slide Deck:** [PDF Link Placeholder]

---

## 📖 What is DroughtSense AI?
Droughts are one of the leading causes of crop failure and food insecurity worldwide. Unfortunately, small farmers in developing countries often lack access to early warning systems, and existing tools are too technical or expensive.

**DroughtSense AI** is a web-based AI agent that democratizes access to agricultural intelligence. By simply entering a region or country, the system fetches live climate and weather data, analyzes it using a powerful open-source Large Language Model (LLM), and returns an easy-to-understand drought risk assessment with actionable recommendations.

### Why AMD MI300X?
We leverage **AMD Developer Cloud** and the **MI300X GPU** to run powerful open-source LLMs (like Llama 3.1) privately via vLLM. This ensures rapid inference for complex climate analysis while keeping regional agricultural data secure, avoiding reliance on closed-source, third-party APIs.

---

## ✨ Features
- **Real-Time Climate Data:** Fetches live rainfall, temperature, and soil moisture data using the NASA POWER API.
- **AI-Powered Risk Assessment:** Analyzes data to categorize drought risk (Low, Medium, High, Critical).
- **Actionable Recommendations:** Provides practical advice tailored to the specific risk level to help farmers protect their crops.
- **Privacy-First Inference:** Processes all AI requests through a dedicated AMD MI300X node.
- **Simple, Accessible UI:** Designed to be lightweight and responsive for users with limited bandwidth.

---

## 🛠 Tech Stack
- **AI Hardware:** AMD MI300X (AMD Developer Cloud)
- **Inference Engine:** vLLM Quick Start image (Llama 3.1 / Qwen2.5)
- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Data APIs:** NASA POWER API, Geocoding APIs
- **Deployment:** Render.com / Railway.app (Free Tier)

---

## 💻 How to Run Locally

### Prerequisites
- Python 3.9+
- Access to an AMD Developer Cloud endpoint (or any OpenAI-compatible LLM endpoint for local testing)
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/droughtsense-ai.git
   cd droughtsense-ai
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your AMD vLLM endpoint details:
   ```ini
   AMD_VLLM_BASE_URL="http://<YOUR_AMD_DROPLET_IP>:8000/v1"
   AMD_VLLM_API_KEY="your-api-key"
   ```

5. **Run the Flask application:**
   ```bash
   python app.py
   ```

6. **Access the Web App:**
   Open your browser and navigate to `http://127.0.0.1:5000`

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
