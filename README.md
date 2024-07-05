# CodeKobzar

<a href="https://huggingface.co/ponoma16/KodKobzar13B">CodeKobzar13B</a> is a generative model that was trained on Ukrainian Wikipedia data and Ukrainian language rules. It has knowledge of Ukrainian history, language, literature and culture.

## Getting Started

1. **Setup conda environment**

   ```shell
   wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.11.0-Linux-x86_64.sh
   bash Miniconda3-py38_4.11.0-Linux-x86_64.sh
   source ~/.bashrc
   conda create --name codekobzar python=3.11
   conda activate codekobzar
   ```

2. **Install relevant packages**

   ```shell
   git clone https://github.com/MariaPonomarenko38/CodeKobzar
   cd CodeKobzar
   pip install -r requirements.txt
   ```

3. **Run Inference**

   ```shell
   cd src
   python inference.py
   ```

## Saving New Requirements

```shell
conda env export > environment.yml --no-builds
```

## Experiment Process

### 1. Seed Dataset Creation

#### Option 1: Build from Scratch

```shell
bash ./src/get_wiki_data.sh
python ./src/process_wiki_data.sh ./data/ukwiki_dump.xml.bz2 ./data/wiki_sentences.csv
```

#### Option 2: Get from Huggingface (based on dump dated Feb 4, 2024)
