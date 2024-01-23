Here is a README for the Comet/ChatGPT folder:

# ChatGPT Comparison

This folder contains code and data related to comparing COMET against GPT models like GPT-3.5 and GPT-4 for commit message generation.

## Contents
- [Prompts](#prompts)
- [Usage](#usage)

## Prompts <a id="prompts"></a>

The following section contains the prompts used for GPT-3.5 and GPT-4 APIs to generate commit messages:

- "Generate commit messages based on code diffs. Provide concise and descriptive commit messages that accurately reflect the changes made in the code. Use appropriate language and conventions commonly used in commit messages. Your responses should only include commit messages, without any explanations or translations. Generate commit messages for the following code diffs."

- "Generate commit messages for code diffs based on the changes made."

- "You are tasked with creating a commit message for the given code diff. The message should be informative, concise, and follow the conventional commit message format. Please do not include any additional explanations or translations."

- "Generate a commit message for the given code diff that accurately reflects the changes made. The message should be clear, concise, and follow the standard conventions used in commit messages."

- "You are acting as a commit message generator. Your task is to create an appropriate commit message for the given code diff. The commit message should be clear, informative, and brief. Please refrain from adding any explanations or additional words."

- Generate a commit message for the given code diff that accurately reflects the changes made. The message should be clear, concise, and follow the standard conventions used in commit messages.


## Usage <a id="usage"></a>

The `hit_api.py` script hits the GPT-3.5 and GPT-4 APIs with the prompts and code diffs to generate commit messages.

To use:

```
python hit_api.py
```

This will generate commit messages for all prompts and code diffs in `data.csv`(e.g. `single_prompt_output.csv`).

All the required files/data are part of the respective folders (gpt-3.5 and gpt-4).


