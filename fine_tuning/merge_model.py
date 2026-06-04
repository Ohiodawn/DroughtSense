import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

def merge():
    # Target the high-performance 7B model
    base_model_name = "Qwen/Qwen2.5-7B-Instruct"
    adapter_path = "droughtsense-lora-adapter-7b"
    output_path = "droughtsense-merged-7b"

    print(f"🚀 Loading base model: {base_model_name}")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    print(f"📂 Loading high-depth adapter: {adapter_path}")
    model = PeftModel.from_pretrained(
        base_model, 
        adapter_path
    )

    print("⚡ Merging adapter with base model for production deployment...")
    merged_model = model.merge_and_unload()

    print(f"💾 Saving 'DroughtSense-7B' to {output_path}...")
    merged_model.save_pretrained(output_path)
    
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    tokenizer.save_pretrained(output_path)
    
    print("\n✅ Final Model Ready! Deploy this folder using vLLM.")

if __name__ == "__main__":
    merge()
