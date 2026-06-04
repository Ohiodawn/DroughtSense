import json
from datasets import load_dataset
import os

def prepare():
    """
    Enhanced dataset preparation for high-performance training.
    Processes full datasets for a 3-hour training window.
    """
    print("--- DroughtSense High-Performance Data Curation ---")
    print("Fetching datasets from Hugging Face...")
    
    # 1. CGIAR research publications (Full set)
    print("Loading CGIAR/gardian-ai-ready-docs...")
    cgiar_ds = load_dataset("CGIAR/gardian-ai-ready-docs", split="train", trust_remote_code=True)
    
    # 2. Agri-LLM raw text
    print("Loading dippatel2506/agri-llm-raw-dataset...")
    agri_llm_ds = load_dataset("dippatel2506/agri-llm-raw-dataset", split="train")
    
    # 3. Crop Optimization data
    print("Loading DARJYO/sawotiQ29_crop_optimization...")
    crop_opt_ds = load_dataset("DARJYO/sawotiQ29_crop_optimization", split="train")

    training_data = []

    # Process CGIAR (Filtering for high-quality drought/water context)
    print(f"Processing {len(cgiar_ds)} CGIAR records...")
    for item in cgiar_ds:
        text = item.get('text', item.get('content', ''))
        # Heuristic: Focus on drought-related records to sharpen the 'moat'
        if any(kw in text.lower() for kw in ['drought', 'water deficit', 'precipitation', 'irrigation']):
            training_data.append({
                "instruction": "Explain the scientific principles of agricultural resilience or drought mitigation described in this context.",
                "response": text[:2000] # Increased context window for 7B model
            })

    # Process Crop Optimization (Direct Q&A)
    print(f"Processing {len(crop_opt_ds)} crop optimization records...")
    for item in crop_opt_ds:
        training_data.append({
            "instruction": item.get('question', item.get('instruction', 'Provide agricultural optimization advice.')),
            "response": item.get('answer', item.get('response', ''))
        })

    # Save to JSON
    output_file = os.path.join(os.path.dirname(__file__), "drought_training_data.json")
    with open(output_file, "w") as f:
        json.dump(training_data, f, indent=2)
    
    print(f"\n✅ Dataset preparation complete!")
    print(f"Total high-quality examples: {len(training_data)}")
    print(f"File saved to: {output_file}")

if __name__ == "__main__":
    prepare()
