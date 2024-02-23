import wandb
from peft import PeftConfig, AutoPeftModelForCausalLM
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from huggingface_hub import HfApi, HfFolder
#'mariiaponomarenko10/ukrainian-finetuned-model/model-k9mac9is:v0'

def download_atrifact(wandb_model_name):
    run = wandb.init()
    artifact = run.use_artifact(wandb_model_name, type='model')
    artifact_dir = artifact.download()


def merge_model(model_load_path, model_path_merged, repo_id):
    model = AutoPeftModelForCausalLM.from_pretrained(
                            model_load_path,
                            low_cpu_mem_usage=True,
                            torch_dtype=torch.float16,
                            device_map='auto',
                        )
    tokenizer = AutoTokenizer.from_pretrained(model_load_path)
    model = model.merge_and_unload()
    model.save_pretrained(model_path_merged, push_to_hub=True, repo_id=repo_id)
    tokenizer.save_pretrained(model_path_merged, push_to_hub=True, repo_id=repo_id)

def upload_model_to_huggingface(model_id, model_directory):
    # Authenticate using the token from HfFolder (assumes you have already logged in via `huggingface-cli login`)
    token = HfFolder.get_token()
    # Create an API instance
    api = HfApi()

    # Upload the model
    api.upload_folder(
        token=token,
        folder_path=model_directory,
        repo_id=model_id,
        repo_type="model"
    )


if __name__ == '__main__':
   upload_model_to_huggingface('ponoma16/kodkobzar13b-2x', '/root/kobkobzar/KodKobzar/src/models/13B_v2/assets')