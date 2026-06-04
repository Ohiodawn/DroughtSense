import os
import json
from openai import OpenAI
from services.graph_service import GraphService

# ==========================================
# 1. UNDERLYING AI ENGINE (AMD MI300X)
# ==========================================

class AIProvider:
    """Handles interaction with the AMD MI300X vLLM endpoint."""
    @staticmethod
    def get_client():
        base_url = os.getenv('AMD_VLLM_BASE_URL')
        api_key = os.getenv('AMD_VLLM_API_KEY', 'not-needed')
        
        if base_url:
            return OpenAI(base_url=base_url, api_key=api_key), "amd"
            
        return None, "mock"

    @staticmethod
    def call(messages, model="llama-3.1-8b-instruct"):
        client, provider_name = AIProvider.get_client()
        
        if provider_name == "mock":
            return None # Fallback handled in agent logic
            
        try:
            # Native inference on AMD MI300X via vLLM
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AMD Inference Error: {e}")
            return None

# ==========================================
# 2. SPECIALIZED AGENTS
# ==========================================

class ClimatologistAgent:
    """Agent responsible for analyzing NASA climate data and Graphify context."""
    
    SYSTEM_PROMPT = (
        "You are an expert Climatologist specialized in drought indices (SPI, SPEI, PDSI). "
        "Your goal is to analyze recent weather patterns for a specific region and "
        "provide a professional meteorological risk assessment. "
        "Focus on: Rainfall deficits, temperature anomalies, and soil moisture trends. "
        "Output a detailed paragraph of your findings and assign a risk level: "
        "Low, Medium, High, or Critical."
    )

    @staticmethod
    def analyze(region, climate_data, graph_context):
        user_content = (
            f"Region: {region}\n"
            f"30-Day Climate Data:\n"
            f"- Avg Temp: {climate_data['temperature']}°C\n"
            f"- Total Precip: {climate_data['precipitation']}mm\n"
            f"- Root Zone Soil Moisture: {climate_data['soil_moisture']}\n\n"
            f"Relevant Scientific Context:\n{graph_context}\n\n"
            "Assess the meteorological drought risk."
        )
        
        messages = [
            {"role": "system", "content": ClimatologistAgent.SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]
        
        result = AIProvider.call(messages)
        return result if result else f"Meteorological analysis for {region} suggests a baseline risk level based on precipitation levels."

class AgronomistAgent:
    """Agent responsible for translating climate risk into farm-level actions."""
    
    SYSTEM_PROMPT = (
        "You are an expert Agronomist. Your goal is to provide specific, actionable "
        "farming recommendations based on a climatology report. "
        "Provide at least 3 distinct, hyper-local recommendations for crop protection, "
        "irrigation management, or soil preservation. "
        "Focus on practical steps for small-to-medium scale farmers."
    )

    @staticmethod
    def advise(region, climatology_report):
        user_content = (
            f"Based on this climatology report for {region}:\n\n"
            f"{climatology_report}\n\n"
            "What are your specific agricultural recommendations for the farmers in this region?"
        )
        
        messages = [
            {"role": "system", "content": AgronomistAgent.SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]
        
        result = AIProvider.call(messages)
        return result if result else "1. Mulch heavily. 2. Conserve water. 3. Monitor crop stress."

class SynthesizerAgent:
    """Agent responsible for final formatting and JSON schema compliance."""
    
    SYSTEM_PROMPT = (
        "You are a Data Synthesizer. Your job is to take reports from a Climatologist "
        "and an Agronomist and merge them into a strict JSON format. "
        "JSON SCHEMA:\n"
        "{\n"
        "  \"risk_level\": \"Low\" | \"Medium\" | \"High\" | \"Critical\",\n"
        "  \"explanation\": \"A 2-3 sentence summary combining the findings\",\n"
        "  \"recommendations\": [\"Tip 1\", \"Tip 2\", \"Tip 3\"],\n"
        "  \"citations\": \"Source of scientific context\"\n"
        "}\n"
        "DO NOT include any text outside the JSON object."
    )

    @staticmethod
    def finalize(climatology_report, agronomy_report, graph_context):
        """
        Synthesizes the final report. 
        Always returns the raw assessment object (not wrapped in logs).
        """
        user_content = (
            f"CLIMATOLOGIST REPORT:\n{climatology_report}\n\n"
            f"AGRONOMIST REPORT:\n{agronomy_report}\n\n"
            f"SCIENTIFIC CONTEXT USED:\n{graph_context}\n\n"
            "Synthesize these into the final JSON output."
        )
        
        messages = [
            {"role": "system", "content": SynthesizerAgent.SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]
        
        result = AIProvider.call(messages)
        
        if result:
            try:
                clean_json = result.replace('```json', '').replace('```', '').strip()
                return json.loads(clean_json)
            except:
                print("WARN: Failed to parse synthesizer JSON, using fallback.")
        
        return MockAI.generate_flat_report(climatology_report, agronomy_report, graph_context)

# ==========================================
# 3. ORCHESTRATOR
# ==========================================

class AIAgentOrchestrator:
    @staticmethod
    def assess_drought(region_data):
        """
        Executes the multi-agent workflow powered by AMD MI300X.
        Includes global failover to MockAI.
        """
        try:
            region = region_data.get('region')
            graph_context = GraphService.get_drought_context()
            
            climatology_report = ClimatologistAgent.analyze(region, region_data, graph_context)
            agronomy_report = AgronomistAgent.advise(region, climatology_report)
            
            final_json = SynthesizerAgent.finalize(climatology_report, agronomy_report, graph_context)

            return {
                "assessment": final_json,
                "agent_logs": [
                    {"agent": "Climatologist", "status": "Analyzing environmental patterns on AMD MI300X...", "report": climatology_report},
                    {"agent": "Agronomist", "status": "Devising hyper-local strategies...", "report": agronomy_report},
                    {"agent": "Synthesizer", "status": "Finalizing agricultural report...", "report": "Consolidated insights."}
                ]
            }
        except Exception as e:
            print(f"ORCHESTRATOR_CRITICAL_ERROR: {e}")
            return MockAI.generate_full_response(region_data)

# ==========================================
# 4. MOCK FALLBACK (FOR SAFETY)
# ==========================================

class MockAI:
    @staticmethod
    def generate_flat_report(clim_report, agro_report, graph_context):
        """Heuristic-based fallback returning a raw assessment object."""
        risk = "Low"
        combined = f"{clim_report} {agro_report}".lower()
        for r in ["Critical", "High", "Medium"]:
            if r.lower() in combined:
                risk = r
                break
        
        return {
            "risk_level": risk,
            "explanation": f"System determined a {risk} vulnerability level based on environmental indicators.",
            "recommendations": [
                "Optimize irrigation cycles for maximum water efficiency.",
                "Implement soil moisture conservation techniques.",
                "Review crop selection for drought-tolerant alternatives."
            ],
            "citations": "Knowledge Graph Context applied." if graph_context else "General meteorological patterns."
        }

    @staticmethod
    def generate_full_response(region_data):
        """Mock fallback for the entire orchestrator flow if AI provider fails."""
        precip = region_data.get('precipitation', 100)
        risk = "Low"
        if precip < 30: risk = "High"
        elif precip < 70: risk = "Medium"

        assessment = {
            "risk_level": risk,
            "explanation": f"Sensor analysis for {region_data.get('region')} indicates {risk} risk conditions.",
            "recommendations": [
                "Prioritize water allocation.",
                "Implement mulching.",
                "Monitor forecasts."
            ],
            "citations": "System Baseline"
        }
        
        return {
            "assessment": assessment,
            "agent_logs": [
                {"agent": "System", "status": "Executing Failover Protocol...", "report": "AI Core Connectivity Interrupted."},
                {"agent": "MockAI", "status": "Generating Heuristic Report...", "report": "Heuristic analysis complete."}
            ]
        }

class AMDInference:
    @staticmethod
    def assess_drought(region_data):
        return AIAgentOrchestrator.assess_drought(region_data)
