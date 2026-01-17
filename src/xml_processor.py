import gzip
import shutil
from pathlib import Path
import requests
import argparse
import xml.etree.ElementTree as ET
import csv

def unpack_xml_gz(xml_path: Path, path_to_save: Path):
    xml_gz_file_name = xml_path.name
    output_path = path_to_save / xml_gz_file_name.strip('.gz')
    print(output_path)
    with gzip.open(xml_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return output_path


def download_xml_gz(xml_gz_url: str, path_to_save: Path):
    xml_gz_file_name = xml_gz_url.strip('\r').split('/')[-1]
    path = path_to_save / xml_gz_file_name
    response = requests.get(xml_gz_url, stream=True)

    with open(path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    
    return path


def parse_xml(xml_file_path: Path, path_to_save: Path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    with open(path_to_save, 'a', encoding='utf-8') as file:
        for row in root:
            for child in row:
                if child.tag == 'url':
                    file.write(child.text + '\n')
    print(f"Parsed successfully into {path_to_save}")


def main(args):
    with open(args.wikipedia_urls_file, 'r') as f:
        urls = f.readlines()
    urls = [url.strip('\n') for url in urls]
    for url in urls:
        xml_gz_file_path = download_xml_gz(url, 
                        args.xml_gz_folder)
        xml_file_path = unpack_xml_gz(xml_gz_file_path, Path(args.xml_folder))
        parse_xml(xml_file_path, Path(args.wikipedia_urls_file))


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--xml_gz_urls")
    parser.add_argument("--xml_gz_folder")
    parser.add_argument("--xml_folder")
    parser.add_argument("--wikipedia_urls_file")

    args = parser.parse_args()
    main(args)