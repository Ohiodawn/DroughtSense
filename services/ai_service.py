import os
import json
from openai import OpenAI
from services.graph_service import GraphService

# ==========================================
# 1. UNDERLYING AI ENGINES (PROVIDERS)
# ==========================================

class AIProvider:
    """Base class for AI interaction logic."""
    @staticmethod
    def get_client():
        base_url = os.getenv('AMD_VLLM_BASE_URL')
        api_key = os.getenv('AMD_VLLM_API_KEY', 'not-needed')
        
        if base_url:
            return OpenAI(base_url=base_url, api_key=api_key), "amd"
            
        local_provider = os.getenv('LOCAL_AI_PROVIDER', 'mock').lower()
        if local_provider == 'ollama':
            return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"), "ollama"
        elif local_provider == 'llama.cpp':
            return OpenAI(base_url="http://localhost:8080/v1", api_key="llama.cpp"), "llama.cpp"
            
        return None, "mock"

    @staticmethod
    def call(messages, model="llama-3.1-8b-instruct"):
        client, provider_name = AIProvider.get_client()
        
        if provider_name == "mock":
            return None # Mock logic handled in agent fallback
            
        try:
            # Adjust model name for local providers if needed
            target_model = model
            if provider_name == "ollama": target_model = "llama3.1"
            if provider_name == "llama.cpp": target_model = "local-model"

            response = client.chat.completions.create(
                model=target_model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling {provider_name}: {e}")
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
        return result if result else f"Meteorological analysis for {region} suggests a baseline risk level based on precipitation levels of {climate_data['precipitation']}mm."

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
        
        # Parse or Fallback
        if result:
            try:
                # Clean markdown if present
                clean_json = result.replace('```json', '').replace('```', '').strip()
                return json.loads(clean_json)
            except:
                print("Failed to parse synthesizer JSON, using fallback.")
        
        # Hardcoded fallback if all AI steps fail or we are in Mock mode
        return MockAI.assess_drought(climatology_report, agronomy_report, graph_context)

# ==========================================
# 3. ORCHESTRATOR (PUBLIC INTERFACE)
# ==========================================

class AIAgentOrchestrator:
    @staticmethod
    def assess_drought(region_data):
        """
        Executes the multi-agent workflow:
        1. Context -> Climatologist
        2. Climatologist -> Agronomist
        3. Both -> Synthesizer -> Final JSON
        """
        region = region_data.get('region')
        graph_context = GraphService.get_drought_context()
        
        # Agent 1: Climatology
        climatology_report = ClimatologistAgent.analyze(region, region_data, graph_context)
        
        # Agent 2: Agronomy
        agronomy_report = AgronomistAgent.advise(region, climatology_report)
        
        # Agent 3: Synthesis
        return SynthesizerAgent.finalize(climatology_report, agronomy_report, graph_context)

# ==========================================
# 4. MOCK FALLBACK (FOR SAFETY/DEV)
# ==========================================

class MockAI:
    @staticmethod
    def assess_drought(clim_report, agro_report, graph_context):
        """Heuristic-based fallback if AI steps fail."""
        # Detect risk level from the climatologist's text if possible
        risk = "Low"
        for r in ["Critical", "High", "Medium"]:
            if r.lower() in clim_report.lower():
                risk = r
                break
        
        return {
            "risk_level": risk,
            "explanation": f"The climatology analysis indicates a {risk} risk. Recent data shows specific environmental stresses in the region.",
            "recommendations": [
                "Implement water-saving irrigation.",
                "Select drought-tolerant crop varieties.",
                "Increase organic matter in soil to improve water retention."
            ],
            "citations": "Knowledge Graph Context utilized." if graph_context else "Standard meteorological patterns."
        }

# Maintain original interface name for compatibility
class AMDInference:
    @staticmethod
    def assess_drought(region_data):
        return AIAgentOrchestrator.assess_drought(region_data)
