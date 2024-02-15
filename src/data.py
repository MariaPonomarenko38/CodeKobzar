from datasets import Dataset, load_dataset
import datasets
import pandas as pd

TRAINING_QA_PROMPT = """Дай відповідь на наступне запитання, розділене потрійними лапками.

### Запитання: ```{question}```
### Відповідь: {answer}
"""

def prepare_instructions(questions, answers):
    instructions = []

    prompt = TRAINING_QA_PROMPT

    for question, answer in zip(questions, answers):
        example = prompt.format(
            dialogue=question,
            summary=answer,
        )
        instructions.append(example)

    return instructions


def prepare_dataset(dataset_repo):
    dataset = load_dataset(dataset_repo)
    train_dataset = dataset["train"]
    val_dataset = dataset["test"]

    questions = train_dataset["question"]
    answers = train_dataset["answer"]
    train_instructions = prepare_instructions(questions, answers)
    train_dataset = datasets.Dataset.from_pandas(
        pd.DataFrame(data={"instructions": train_instructions})
    )

    return train_dataset