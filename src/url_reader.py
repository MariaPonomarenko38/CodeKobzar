from newspaper import Article
import re
from nltk.tokenize import sent_tokenize
import argparse
from pathlib import Path

def clean_text(text: str):
    tags = re.compile(r'<[^>]+>')
    text = tags.sub('', text)
    pattern = re.compile(r'\[\d+]+')
    text = pattern.sub('', text)
    text = text.replace('\n', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    return text


def retrieve_text(url: str):
    article = Article(url=url)
    article.download()
    article.parse()
    body = article.text
    body = clean_text(body)
    return body


def main(args):
    text = retrieve_text(args.url.strip())

    file_path = Path(args.output_file_path)

    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)

    sentences = sent_tokenize(text)
    with open(args.output_file_path, 'a', encoding='utf-8') as f:
        for sent in sentences:
            if len(sent.split()) >= 5:
                f.write(sent)
                f.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--url")
    parser.add_argument("--output_file_path")

    args = parser.parse_args()
    main(args)