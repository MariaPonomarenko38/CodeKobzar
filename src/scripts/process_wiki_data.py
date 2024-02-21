import os
import csv
import re

import bz2
from lxml import etree
from pathlib import Path
import argparse
from tqdm import tqdm
import nltk
from nltk.tokenize import sent_tokenize
from multiprocessing import Pool, cpu_count


def clean_text(text):
    # Remove file/image links, e.g., [[Файл:...]]
    text = re.sub(r"\[\[Файл:[^\]]+\]\]", "", text)
    # Remove templates, caution: might not correctly handle deeply nested templates
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    while re.search(r"\{\{[^{}]*\}\}", text):
        text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    # Remove links and references
    text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]", r"\1", text)
    text = re.sub(r"<ref.*?>.*?</ref>", "", text, flags=re.DOTALL)
    text = re.sub(r"<ref.*?/>", "", text)
    # Remove HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)
    # Attempt to remove table markup, not perfect
    text = re.sub(r"\{\|.*?\|\}", "", text, flags=re.DOTALL)
    # Remove category links
    text = re.sub(r"\[\[Категорія:.*?\]\]", "", text)
    # Remove lists and bullet points
    text = re.sub(r"^\*.*$", "", text, flags=re.MULTILINE)
    # Remove section headings
    text = re.sub(r"==.*?==", "", text)
    # Remove extra spaces and newlines
    text = re.sub(r"\s+", " ", text).strip()
    # Remove non-breaking spaces
    text = text.replace("&nbsp;", " ")
    return text


def save_and_append(file_path, title, sentences):
    """
    Saves or appends a row with 'title' and 'sentence' to a CSV file.

    Parameters:
    - file_path (str): The path to the CSV file.
    - title (str): The title to be saved.
    - sentence (str): The sentence to be saved.
    """
    # Check if the file exists to determine if we need to write headers
    file_exists = os.path.isfile(file_path)

    # Open the file in append mode ('a') so we can add to it without overwriting existing content
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        # Create a writer object
        writer = csv.writer(file)

        # If the file does not exist, write the header first
        if not file_exists:
            writer.writerow(["article_title", "sentence"])  # Writing the header

        # Write the data row
        for sentence in sentences:
            writer.writerow([title, sentence])


def process_article_wrapper(args):
    # Unpack arguments
    title, text, output_path = args
    # Check if text is None and return immediately if so
    if text is None:
        print(f"Skipping article {title}: No text available.")
        return
    # Otherwise, process the article
    return process_article(title, text, output_path)


def process_article(title, text, output_path):
    # Process the article (cleaning text, tokenizing, etc.)
    text = clean_text(text)
    sentences = sent_tokenize(text)
    sentences = [s for s in sentences if len(s) > 100 and "А" <= s[0] <= "Я"]
    # Since multiprocessing doesn't share global state, handle file writing individually
    save_and_append(output_path, title, sentences)


def parse_wikipedia_dump(file_path, output_path):
    # Determine the number of processes to use
    num_processes = cpu_count()

    # Create a pool of processes
    with Pool(processes=num_processes) as pool:
        tasks = []

        with bz2.open(file_path, "rb") as file:
            context = etree.iterparse(
                file,
                events=("end",),
                tag="{http://www.mediawiki.org/xml/export-0.10/}page",
            )

            for event, elem in tqdm(context, desc="Identifying articles"):
                ns = "{http://www.mediawiki.org/xml/export-0.10/}"
                title = elem.find(f"{ns}title").text
                revision = elem.find(f"{ns}revision")
                text = revision.find(f"{ns}text").text
                tasks.append((title, text, output_path))
                # Clear the element to save memory
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]

        # Process articles in parallel
        for _ in tqdm(
            pool.imap_unordered(process_article_wrapper, tasks),
            total=len(tasks),
            desc="Processing articles",
        ):
            pass  # Just consume the iterator to get progress feedback


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Wikipedia Dump")
    parser.add_argument(
        "file_path", type=str, help="Path to the Wikipedia .bz2 dump file"
    )
    parser.add_argument(
        "output_path", type=str, help="Output file path for filtered sentences"
    )

    args = parser.parse_args()

    # Ensure the nltk data is available to all processes
    nltk.download("punkt")

    parse_wikipedia_dump(args.file_path, args.output_path)
