import wandb
from peft import PeftConfig, AutoPeftModelForCausalLM
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from huggingface_hub import HfApi, HfFolder
import json
from predictor import Predictor
import pandas as pd
from data import format
import re
from transformers import AutoTokenizer
#'mariiaponomarenko10/ukrainian-finetuned-model/model-k9mac9is:v0'

def download_atrifact(wandb_model_name):
    run = wandb.init()
    artifact = run.use_artifact(wandb_model_name, type='model')
    artifact_dir = artifact.download()


def merge_model(model_load_path,repo_id):
    model = AutoPeftModelForCausalLM.from_pretrained(
                            model_load_path,
                            low_cpu_mem_usage=True,
                            torch_dtype=torch.float16,
                            device_map='auto',
                        )
    tokenizer = AutoTokenizer.from_pretrained(model_load_path)
    #model = model.merge_and_unload()
    tokenizer.push_to_hub(repo_id)
    #model.save_pretrained(model_path_merged, push_to_hub=True, repo_id=repo_id)
    #tokenizer.save_pretrained(model_path_merged, push_to_hub=True, repo_id=repo_id)

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


def generate_open_question_anwers(file_path, model_path, output_file_path)
    data = []
    predictor = Predictor(model_load_path=model_path)
    with open(file_path, 'r') as file:
        for line in file:
            json_obj = json.loads(line)
            data.append(json_obj)

    df = pd.DataFrame(data)
    for i, row in df.iterrows(): 
        ins = row['instruction']
        result = predictor.predict(f'USER: {ins} ASSISTANT: ') 
        result = result.split('ASSISTANT: ')[1]
        df.at[i, 'output'] = result  
        
    df.to_json(output_file_path, orient='records', lines=True, force_ascii=False)

if __name__ == '__main__':
   
   merge_model('./models/kodkobzar13B_x2_lit_history_lang_finetuned/assets', 'ponoma16/kodkobzar13B_x2_lit_history_lang_finetuned-merged')
   #merge_model('./models/kodkobzar13B_x2_lit_history_lang_finetuned/assets', './models/kodkobzar13B_x2_lit_history_lang_finetuned-merged', 'ponoma16/kodkobzar13B_x2_lit_history_lang_finetuned')
   #upload_model_to_huggingface('ponoma16/kodkobzar13B_x2_lit_history_lang_finetuned', '/root/kodkobzar/KodKobzar/src/models/kodkobzar13B_x2_lit_history_lang_finetuned/assets')