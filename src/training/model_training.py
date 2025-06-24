import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.training_args import TrainingArguments
from transformers.trainer import Trainer
from peft import LoraConfig, get_peft_model
from datasets import load_dataset

def train_lora_adapter(
    base_model_id: str,
    dataset_path: str,
    adapter_name: str,
    output_dir: str = "models/lora_adapters",
    training_output_dir: str = "models/trained"
):
    """
    Fine-tunes a LoRA adapter for a given base model and dataset.
    """
    print(f"Loading base model: {base_model_id}")
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Loading and preparing dataset...")
    dataset = load_dataset("text", data_files={"train": dataset_path})
    train_dataset = dataset["train"]

    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

    tokenized_dataset = train_dataset.map(tokenize_function, batched=True, remove_columns=["text"])


    lora_config = LoraConfig(
        r=64,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM"
    )

    peft_model = get_peft_model(model, lora_config)
    peft_model.print_trainable_parameters()

    training_args = TrainingArguments(
        output_dir=os.path.join(training_output_dir, adapter_name),
        per_device_train_batch_size=1,
        num_train_epochs=1,
        logging_steps=10,
        save_steps=100,
        gradient_accumulation_steps=4,
        report_to="none",
    )

    trainer = Trainer(
        model=peft_model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )

    print(f"Starting training for adapter: {adapter_name}")
    trainer.train()

    print("Training complete. Saving adapter.")
    adapter_save_path = os.path.join(output_dir, adapter_name)
    peft_model.save_pretrained(adapter_save_path)
    print(f"Adapter saved to {adapter_save_path}")


if __name__ == '__main__':
    os.makedirs("data/processed", exist_ok=True)
    dummy_dataset_path = "data/processed/dummy_train.txt"
    with open(dummy_dataset_path, "w") as f:
        for i in range(200):
            f.write(f"def dummy_function_{i}():\n    '''This is a dummy function number {i}.'''\n    pass\n")
            
    train_lora_adapter(
        base_model_id="deepseek-ai/DeepSeek-Coder-V2-Lite",
        dataset_path=dummy_dataset_path,
        adapter_name="tanuki-python-coder-test"
    )

    print("\nLoRA adapter training demonstration complete.")
