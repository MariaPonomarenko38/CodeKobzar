from datasets import load_dataset
from mistralai.client import MistralClient 
from mistralai.models.chat_completion import ChatMessage
import csv
from pathlib import Path
from tqdm import tqdm
import argparse


key = "nKRbJBixNiFGtW8SpjWr0crOeN0JVt1k"
model = "mistral-medium"
client = MistralClient(api_key=key)


dataset = load_dataset("byebyebye/ukr-wiki-sentences")
dataset = dataset['train'].shuffle(seed=42)
dataset = dataset.rename_column(" sentence", "sentence")



def save_line_to_csv(file_path, data):
    """
    Appends a single line of data to a CSV file. Creates the file with headers if it does not exist.
    
    Args:
    - file_path (str): The path to the CSV file.
    - data (dict): The data to save, where keys are column names and values are the data for one row.
    """
    # Check if the file exists to determine if headers should be written
    file_exists = Path(file_path).is_file()
    
    # Open the file in append mode ('a') for writing
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        
        # If the file does not exist, write the header
        if not file_exists:
            writer.writeheader()
        
        # Write the data row
        writer.writerow(data)


def get_questions(dataset, save_path, starting_idx=0, max_budget=50):
    total_cost = 0
    idx = starting_idx

    pbar = tqdm(total=max_budget, desc = f"idx @ {idx}")
    while total_cost < max_budget:
        
        article_title = dataset[idx]['article_title']
        sentence = dataset[idx]['sentence']

        pbar.set_description(f"idx @ {idx}")
        prompt = f"Придумай запитання яке можна було б поставити до цього реченняю Тема - {article_title}. : {sentence}"
        
        try:
            chat_response = client.chat(
            model=model,
            messages=[ChatMessage(role="user", content=prompt)],
            )
        except:
            idx += 1
            continue

        question = chat_response.choices[0].message.content
        cost = chat_response.usage.prompt_tokens * 2.5/1_000_000 + chat_response.usage.completion_tokens * 7.5/1_000_000

        total_cost += cost

        line = {"prompt": prompt, "topic": article_title, "question": question, "response": sentence}
        save_line_to_csv(save_path, line)
        
        pbar.update(cost)
        idx += 1

    pbar.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generating questions from Wikipedia sentences using Mistral")
    parser.add_argument(
        "save_path", type=str, help="Output file path for processed dataset"
    )
    parser.add_argument(
        "starting_idx", type=int, help="Starting index for the dataset"
    )
    parser.add_argument(
        "max_budget", type=float, help="Maximum Budget for the Mistral API"
    )
    
    args = parser.parse_args()

    get_questions(dataset, args.save_path, args.starting_idx, args.max_budget) 

