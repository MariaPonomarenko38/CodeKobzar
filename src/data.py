from datasets import Dataset, load_dataset, concatenate_datasets
import datasets
import pandas as pd
import json

TRAINING_PROMPT = """USER: {input} ASSISTANT: {output}"""

TRAINING_PROMPT_EXAM = """USER: {input} ASSISTANT: {output}"""

def format(exam_answer):
    data = eval(exam_answer)

    exam_answers = '\n'.join([f"{item['marker']} - {item['text']}" for item in data])

    return exam_answers

def prepare_instructions(inputs, outputs, exam_answers_format=False):
    instructions = []

    prompt_sample = TRAINING_PROMPT

    for input, output in zip(inputs, outputs):
        example = prompt_sample.format(
            input=input,
            output=output,
        )
        instructions.append(example)

    return instructions


def prepare_instructions_exam(questions, answers, correct_answers):
    instructions = []

    prompt_sample = TRAINING_PROMPT_EXAM

    for question, answer, correct_answer in zip(questions, answers, correct_answers):
        input = (question + format(str(answer))).replace('\n', '')
        #print(correct_answer)
        output = correct_answer[0]
        example = prompt_sample.format(
            input=input,
            output=output,
        )
        instructions.append(example)
        #break
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

def prepare_dataset_exam(dataset_repo, input_field, input_fiels1, output_field, exam_answers_format=False):
    dataset = load_dataset(dataset_repo)
    train_dataset = dataset["train"]
    #val_dataset = dataset["test"]

    questions = train_dataset[input_field]
    answers = train_dataset[input_fiels1]
    correct_answer = train_dataset[output_field]
    
    train_prompt_question = prepare_instructions_exam(questions, answers, correct_answer)

    train_prompt_question_dataset = datasets.Dataset.from_pandas(
        pd.DataFrame(data={"instructions": train_prompt_question})
    )

    #dataset_cc = concatenate_datasets([train_prompt_question_dataset, train_question_response_dataset])
    return train_prompt_question_dataset 



if __name__ == '__main__':

    d = '''[{'marker': 'А', 'text': 'першому'}, {'marker': 'Б', 'text': 'другому'}, {'marker': 'В', 'text': 'третьому'}, {'marker': 'Г', 'text': "п'ятому"}]'''
    data = format(d)
    print(data)