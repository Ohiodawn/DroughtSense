import json
from datasets import load_dataset
import os

def prepare():
    print("Fetching datasets from Hugging Face...")
    
    # 1. CGIAR research publications
    print("Loading CGIAR/gardian-ai-ready-docs...")
    cgiar_ds = load_dataset("CGIAR/gardian-ai-ready-docs", split="train", trust_remote_code=True)
    
    # 2. Agri-LLM raw text
    print("Loading dippatel2506/agri-llm-raw-dataset...")
    agri_llm_ds = load_dataset("dippatel2506/agri-llm-raw-dataset", split="train")
    
    # 3. Crop Optimization data
    print("Loading DARJYO/sawotiQ29_crop_optimization...")
    crop_opt_ds = load_dataset("DARJYO/sawotiQ29_crop_optimization", split="train")

    training_data = []

    # Process CGIAR (Assuming columns like 'text' or 'content')
    # We will wrap them into a drought-specific instruction context
    for i, item in enumerate(cgiar_ds):
        if i > 5000: break # Sample for now
        text = item.get('text', item.get('content', ''))
        if 'drought' in text.lower():
            training_data.append({
                "instruction": "Analyze the following agricultural research context and explain its relevance to drought mitigation.",
                "response": text[:1000] # Trim for efficiency
            })

    # Process Crop Optimization (Q&A format)
    for i, item in enumerate(crop_opt_ds):
        # Map columns to instruction/response
        # Assuming typical Q&A columns for this dataset
        training_data.append({
            "instruction": item.get('question', item.get('instruction', 'Describe crop optimization for this scenario.')),
            "response": item.get('answer', item.get('response', 'No data available.'))
        })

    # Save to JSON for the SFTTrainer
    output_file = os.path.join(os.path.dirname(__file__), "drought_training_data.json")
    with open(output_file, "w") as f:
        json.dump(training_data, f, indent=2)
    
    print(f"Dataset preparation complete! Total examples: {len(training_data)}")
    print(f"File saved to: {output_file}")

if __name__ == "__main__":
    prepare()
