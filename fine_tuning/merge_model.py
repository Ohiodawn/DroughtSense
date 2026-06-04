import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

def merge():
    base_model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    adapter_path = "droughtsense-lora-adapter"
    output_path = "droughtsense-merged"

    print(f"Loading base model: {base_model_name}")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    print(f"Loading LoRA adapter: {adapter_path}")
    model = PeftModel.from_pretrained(
        base_model, 
        adapter_path
    )

    print("Merging adapter with base model...")
    merged_model = model.merge_and_unload()

    print(f"Saving merged model to {output_path}...")
    merged_model.save_pretrained(output_path)
    
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    tokenizer.save_pretrained(output_path)
    
    print("Model merged and ready for vLLM deployment!")

if __name__ == "__main__":
    merge()
