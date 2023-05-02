# COMET 💫 
## A Context-Aware Approach to Commit Message Generation


### Data Pre-processing
In order to obtain the Delta graph representation of code changes. Follow these steps: 
1. Make sure the data is in json format with the following arrangement
  - A key:"commit_message" and value: corresponding message in string format.
  - A key:"classes" and value: a list of dictionaries, where each dictionary contains the following attributes : "class_name", "prev_code", "new_code". The variables are self-explanatory.
2. Place the data file in the `pre-process' folder
3. Run the following script: 

```
python pre-process/main.py
```
