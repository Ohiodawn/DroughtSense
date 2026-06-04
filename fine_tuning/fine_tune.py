import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
import os

# ====================================================================
# HIGH-PERFORMANCE TRAINING SCRIPT (3-HOUR BUDGET)
# Optimized for AMD MI300X | Target: Qwen 2.5 7B
# ====================================================================

def train():
    # 1. Model Selection: Upgraded to 7B for superior reasoning
    model_name = "Qwen/Qwen2.5-7B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    print(f"🚀 Loading High-Performance Base Model: {model_name}")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16, # Native ROCm optimization
        device_map="auto"
    )

    # 2. LoRA Config: Increased Rank (64) for deeper domain adaptation
    # Since we have 3 hours and MI300X power, we can learn more complex patterns.
    lora_config = LoraConfig(
        r=64,                    # Rank increased from 16 to 64
        lora_alpha=128,          # Alpha scaled (2 * r)
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # 3. Load Augmented Dataset
    data_path = os.path.join(os.path.dirname(__file__), "drought_training_data.json")
    print(f"📂 Loading high-depth dataset from {data_path}")
    dataset = load_dataset("json", data_files=data_path)

    # 4. Training Arguments: Optimized for 3-hour window
    training_args = SFTConfig(
        output_dir="./droughtsense-lora-7b",
        num_train_epochs=5,           # Increased epochs for better grounding
        per_device_train_batch_size=8, # MI300X handles larger batches easily
        gradient_accumulation_steps=4,
        learning_rate=1e-4,
        fp16=True,                    # Native ROCm support
        logging_steps=5,
        save_steps=50,
        max_seq_length=2048,          # Doubled sequence length for complex research context
        packing=True,                 # More efficient data utilization
        report_to="none"
    )

    # 5. Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset["train"],
        args=training_args,
    )

    print(f"🔥 Starting training on AMD MI300X (Budget: ~3 Hours)...")
    trainer.train()

    # 6. Save Adapter
    output_dir = "droughtsense-lora-adapter-7b"
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"✅ Specialized 'DroughtSense-7B' adapter saved to {output_dir}")

if __name__ == "__main__":
    train()
