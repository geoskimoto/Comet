# COMET 
## A Context-Aware Approach to Commit Message Generation


### Data Pre-processing
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

## Models
Please use the following links to download the models concerned with Comet's generation and Quality Assurance modules.

```
https://doi.org/10.5281/zenodo.7901752
```
    .
    ├── ChatGPT                   # Code and survery information of RQ3
    ├── Generation                # Code T5 training script
    ├── Quality Assurance         # QA Module script
    ├── pre-process               # raw code to Delta graph conversion script

```
https://doi.org/10.5281/zenodo.7902315
```
    .
    ├── Delta graph              # Delta graph representations 
    ├── Filter check data        # Data that has been passed through the filer (.java files only)
    ├── Processed Excels         # Extracted data from Delta graph

## Generation Module

This folder contains the code realting to finetuning the Code-T5 model on Delta graph data.
Hyperparameters : 
  Learning rate: 5e-5
  Optimizer: AdamW

To fine tune: 
1. Download the data from the Zenodo link provided above. Place the data in the ./Generation folder.
2. Execute the command below to fine tune Code-T5 on Delta graph data
```
python Generation/model.py 
```

## Quality Assurance Module

The Quality Assurance folder contains the code for the QA Module as described in the paper. 
The messages final embeddings are generated and are then ranked acccording to preference. The code for ranking based on trained examples is given in the folder Quality Assurance/Rank.

## ChatGPT

This folder contains the code related to Research question: 3
