import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
import os

# Configuration for AMD MI300X (Native ROCm)
# Ensure you are running this in a ROCm-optimized container/environment.

def train():
    # Model configuration
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    print(f"Loading model: {model_name}")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,  # float16 is optimized for AMD ROCm
        device_map="auto"
    )

    # LoRA config — only trains small adapters (efficient wallpaper method)
    lora_config = LoraConfig(
        r=16,                    # rank
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load the agricultural drought dataset
    data_path = os.path.join(os.path.dirname(__file__), "drought_training_data.json")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please run the dataset preparation script first.")
        return

    print("Loading dataset...")
    dataset = load_dataset("json", data_files=data_path)

    # Training Arguments
    training_args = SFTConfig(
        output_dir="./droughtsense-lora",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=True,           # Required for AMD ROCm performance
        logging_steps=10,
        save_steps=100,
        max_seq_length=1024,
        report_to="none"
    )

    # Trainer setup
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset["train"],
        args=training_args,
    )

    print("Starting training on AMD MI300X...")
    trainer.train()

    # Save the LoRA adapter
    output_dir = "droughtsense-lora-adapter"
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Fine-tuning complete! Adapter saved to {output_dir}")

if __name__ == "__main__":
    train()
