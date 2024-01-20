import pandas as pd

df = pd.read_csv("test.csv")

import torch
from transformers import AutoTokenizer, AutoModel

codbert_model = AutoModel.from_pretrained('microsoft/codebert-base')
tokenizer = AutoTokenizer.from_pretrained('microsoft/codebert-base')

code_vectors = []

for i,diff in enumerate(tqdm(df['diff'])):

  tokenized_code = tokenizer(diff, truncation=True, max_length=512, return_tensors='pt')

  outputs = codbert_model(input_ids = tokenized_code['input_ids'], attention_mask=tokenized_code['attention_mask'])

  code_vectors.append(outputs[0][:,0,:])

  if i%5 == 0:
    torch.cuda.empty_cache()
    time.sleep(15)

df['vectors'] = code_vectors


df.to_csv("df_with_vectors.csv", index=False)