import os
import json
from openai import OpenAI

class AMDInference:
    @staticmethod
    def assess_drought(region_data):
        """
        Analyzes climate data using real AI inference on AMD MI300X via vLLM.
        """
        base_url = os.getenv('AMD_VLLM_BASE_URL')
        api_key = os.getenv('AMD_VLLM_API_KEY', 'not-needed')
        
        if not base_url:
            print("AMD_VLLM_BASE_URL not set, falling back to MockAI")
            return MockAI.assess_drought(region_data)

        client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        
        system_prompt = (
            "You are an expert agricultural and climatology AI assistant. "
            "Analyze the provided climate data for a region and determine the drought risk level. "
            "Your output must be a valid, parsable JSON object with the following schema:\n"
            "{\n"
            "  \"risk_level\": \"Low\" | \"Medium\" | \"High\" | \"Critical\",\n"
            "  \"explanation\": \"2-3 sentence summary\",\n"
            "  \"recommendations\": [\"tip 1\", \"tip 2\", \"tip 3\"]\n"
            "}\n"
            "Do not include any text outside the JSON object."
        )
        
        user_content = (
            f"Analyze drought risk for {region_data.get('region')}.\n"
            f"Last 30 days data:\n"
            f"- Avg Temp: {region_data.get('temperature')}°C\n"
            f"- Total Precip: {region_data.get('precipitation')}mm\n"
            f"- Soil Moisture: {region_data.get('soil_moisture')}"
        )
        
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instruct", 
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ]
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            print(f"AMD Inference Error: {e}")
            return MockAI.assess_drought(region_data)

class MockAI:
    @staticmethod
    def assess_drought(region_data):
        """
        Simulates an AI assessment based on real climate data.
        """
        risk_level = "Low"
        precip = region_data.get('precipitation', 0)
        temp = region_data.get('temperature', 20)
        soil = region_data.get('soil_moisture', 0.5)
        
        if precip < 30 or soil < 0.3:
            risk_level = "High"
        elif precip < 70 or soil < 0.5:
            risk_level = "Medium"
        
        if temp > 35 and risk_level == "High":
            risk_level = "Critical"

        return {
            "risk_level": risk_level,
            "explanation": (
                f"In {region_data.get('region')}, the last 30 days saw {precip}mm of rain "
                f"and an average temperature of {temp}°C. Soil moisture is at {soil*100}%. "
                f"These conditions (simulated) indicate a {risk_level} drought risk."
            ),
            "recommendations": [
                "Prioritize water allocation for high-value crops.",
                "Implement mulching to retain soil moisture.",
                "Monitor local weather forecasts for upcoming rain events."
            ]
        }
