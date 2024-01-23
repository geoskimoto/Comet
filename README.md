# COMET 
COMET (Context-aware Commit Message Generation) is a technique for automatically generating high-quality commit messages by capturing the context of code changes.

## Contents
- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
  - [Data Preprocessing](#data-preprocessing)
  - [Model Training](#model-training)
  - [Quality Assurance](#quality-assurance) 
  - [Evaluation](#evaluation)
- [ChatGPT Comparison](#chatgpt-comparison)

## Overview <a id="overview"></a>

COMET utilizes a novel graph-based representation called delta graphs to capture code changes and context. It leverages transformer models fine-tuned on delta graphs to generate commit messages. COMET also contains a quality assurance module to rank generated messages.

Key highlights:

- Delta graph representation to capture code context 
- Transformer-based generation module
- Customizable quality assurance ranking

## Setup <a id="setup"></a>

### Requirements

- Python 3.6+
- PyTorch 1.3+
- Transformers 4.0+
- Joern
- NLTK
- NumPy
- Pandas

## Usage <a id="usage"></a>

### Data Pre-processing <a id="data-preprocessing"></a>
In order to obtain the Delta graph representation of code changes. Follow these steps: 
1. Make sure the data is in json format with the following arrangement
  - A key:"commit_message" and value: corresponding message in string format.
  - A key:"classes" and value: a list of dictionaries, where each dictionary contains the following attributes : "class_name", "prev_code", "new_code". 
2. Place the json file in the pre-process folder.
3. Run the following script: 
In order to obtain the Delta graph representation of code changes. 
Run the following script: 

```
python pre-process/main.py
```

## Models <a id="model-training"></a>
Please use the following links to download the models concerned with Comet's generation and Quality Assurance modules.

```
use https://doi.org/10.5281/zenodo.7901752 to download:
```
    .
    ├── ChatGPT                   # Code and survery information of RQ3
    ├── Generation                # Code T5 training script
    ├── Quality Assurance         # QA Module script
    ├── pre-process               # raw code to Delta graph conversion script

```
use https://doi.org/10.5281/zenodo.7902315 to download:
```
    .
    ├── Delta graph              # Delta graph representations 
    ├── Filter check data        # Data that has been passed through the filer (.java files only)
    ├── Processed Excels         # Extracted data from Delta graph

## Generation Module

This folder contains the code relating to finetuning the Code-T5 model on Delta graph data.
Hyperparameters : 
  Learning rate: 5e-5
  Optimizer: AdamW

To fine-tune: 
1. Download the data from the Zenodo link provided above. Place the data in the ./Generation folder.
2. Execute the command below to fine-tune Code-T5 on Delta graph data
```
python Generation/model.py 
```

## Quality Assurance Module <a id="quality-assurance"></a>

The quality assurance module code is located in `QualityAssurance` folder. The messages final embeddings are generated and are then ranked acccording to preference. The code for ranking based on trained examples is given in the folder Quality Assurance/Rank. It contains:

- `GCN.py`: Graph convolution network 
- `Rank`: Code for ranking generated messages
- `nlpparser.py`: Parses text to dependency tree
- `text_preprocess.py`: Text preprocessing

To use quality assurance:

1. Train QA model on labeled delta graph - message pairs
2. At inference, pass delta graph and candidate messages
3. Module will rank messages based on training

### Evaluation <a id="evaluation"></a>

The evaluation code for BLEU, METEOR, and ROUGE is located in the `Generation` folder.
For detailed instructions please check the readme for [BLEU](https://github.com/SMART-Dal/Comet/tree/main/Generation/bleu), [METEOR](https://github.com/SMART-Dal/Comet/tree/main/Generation/meteor), [ROUGE](https://github.com/SMART-Dal/Comet/tree/main/Generation/rouge)

## ChatGPT Comparison <a id="chatgpt-comparison"></a>

The `ChatGPT` folder contains code related to comparing COMET against GPT-3.5 and GPT-4 under various settings.

It includes:

- Prompt engineering data
- GPT API requests
- Output formatting and analysis

See `ChatGPT/README.md` for details.

## Data Format

The data must be in the following JSON format:

```json
{
  "commit_message": "Commit message text",
  
  "classes": [
    {
      "class_name": "Class1",
      "prev_code": "Previous code", 
      "new_code": "Updated code"
    },
    {
      "class_name": "Class2",
      "prev_code": "Previous code",
      "new_code": "Updated code" 
    }
  ]
}
```
