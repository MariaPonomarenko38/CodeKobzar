from datasets import Dataset, load_dataset, concatenate_datasets
import datasets
import pandas as pd
import json

TRAINING_PROMPT = """
    USER: {input}
    ASSISTANT: {output}
"""

def format(exam_answer):
    data = eval(exam_answer)

    exam_answers = '\n'.join([f"{item['marker']} - {item['text']}" for item in data])

    return exam_answers

def prepare_instructions(inputs, outputs, exam_answers_format=False):
    instructions = []

    prompt_sample = TRAINING_PROMPT

    for input, output in zip(inputs, outputs):
        if exam_answers_format:
            #print(type(output))
            #print(output)
            output = format(str(output))

        example = prompt_sample.format(
            input=input,
            output=output,
        )
        instructions.append(example)

    return instructions


def prepare_dataset(dataset_repo, input_field, output_field, exam_answers_format=False):
    dataset = load_dataset(dataset_repo)
    train_dataset = dataset["train"]
    #val_dataset = dataset["test"]

    inputs = train_dataset[input_field]
    outputs = train_dataset[output_field]
    
    train_prompt_question = prepare_instructions(inputs, outputs, exam_answers_format)

    train_prompt_question_dataset = datasets.Dataset.from_pandas(
        pd.DataFrame(data={"instructions": train_prompt_question})
    )

    #dataset_cc = concatenate_datasets([train_prompt_question_dataset, train_question_response_dataset])
    return train_prompt_question_dataset 


if __name__ == '__main__':

    d = '''[{'marker': 'А', 'text': 'першому'}, {'marker': 'Б', 'text': 'другому'}, {'marker': 'В', 'text': 'третьому'}, {'marker': 'Г', 'text': "п'ятому"}]'''
    data = format(d)
    print(data)