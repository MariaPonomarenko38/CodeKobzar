# KodKobzar

## Getting Started

1. **Setup conda environment**

   ```shell
   wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.11.0-Linux-x86_64.sh
   bash Miniconda3-py38_4.11.0-Linux-x86_64.sh
   source ~/.bashrc
   conda create --name kodkobzar python=3.11
   conda activate kodkobzar
   ```

2. **Install relevant packages**

   ```shell
   git clone https://github.com/MariaPonomarenko38/KodKobzar
   cd Kodobzar
   pip install -r requirements.txt
   ```

3. **Run Inference**
   ```
   cd src
   python inference.py
   ```

## Saving New Requirements

    ```shell
    conda env export > environment.yml --no-builds
    ```
