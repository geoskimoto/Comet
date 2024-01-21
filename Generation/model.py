""" IMPORTING LIBRARRIES """
import pandas as pd
import numpy as np
from glob import glob
import time
from transformers import RobertaTokenizer, T5ForConditionalGeneration
from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer

# Importing the libraries
import datasets
import evaluate
import pyarrow as pa
import pyarrow.dataset as ds
from datasets import Dataset

import torch

# Importing evlauation metrics
import nltk
nltk.download('punkt')
import sys 
sys.path.append("../bleu")
import bleu
#sys.path.append("../meteor")
#import meteor
sys.path.append("../rouge")
import rouge


class CodeT5:
    
    
    def __init__(self):
        
        self.tokenizer = RobertaTokenizer.from_pretrained("codet5-large")
        self.model = T5ForConditionalGeneration.from_pretrained("codet5-large")
        
        self.model.train()
        
        print("LOOK FOR PARAMETERS NUMBER HERE: ",  self.model.num_parameters())
        
        self.batch_size=12
        self.encoder_max_length=512
        self.decoder_max_length=80


        self.bleu_score =  bleu.Bleu()
        #self.meteor_score = meteor.Meteor()
        self.rouge_score = rouge.Rouge()

    
    def compute_metrics(self,pred):
        
        labels_ids = pred.label_ids
        pred_ids = pred.predictions
    
        # all unnecessary tokens are removed
        pred_str = self.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
        labels_ids[labels_ids == -100] = self.tokenizer.pad_token_id
        label_str = self.tokenizer.batch_decode(labels_ids, skip_special_tokens=True)
    
        bleu4_score = self.bleu_score.compute(predictions=pred_str, references=label_str, max_order=4)
        bleu3_score = self.bleu_score.compute(predictions=pred_str, references=label_str, max_order=3)
        bleu2_score = self.bleu_score.compute(predictions=pred_str, references=label_str, max_order=2)
        bleu1_score = self.bleu_score.compute(predictions=pred_str, references=label_str, max_order=1)

        rouge_output = self.rouge_score.compute(predictions=pred_str, references=label_str)
    
        
        return {
            "rougeL": round(rouge_output.get("rougeL"), 4),
            "bleu1_score":round(bleu1_score["bleu"],4),
            "bleu2_score":round(bleu2_score["bleu"],4),
            "bleu3_score":round(bleu3_score["bleu"],4),
            "bleu4_score":round(bleu4_score["bleu"],4)
            }
        
    
    def process_data_to_model_inputs(self, batch):
        # tokenize the inputs and labels
        prefix = "Generate commit message: "
        inputs = self.tokenizer([prefix+a+self.tokenizer.sep_token+b+self.tokenizer.sep_token+c for a,b,c in zip(batch["add"],batch["del"],batch["common"])], padding="max_length", truncation=True, max_length=self.encoder_max_length)
        outputs = self.tokenizer(batch["message"], padding="max_length", truncation=True, max_length=self.decoder_max_length)
      
        batch["input_ids"] = inputs.input_ids
        batch["attention_mask"] = inputs.attention_mask
      
        #This was required in the earlier version, but internal implementation captures this so we don't have to provide
        # batch["decoder_input_ids"] = outputs.input_ids
        # batch["decoder_attention_mask"] = outputs.attention_mask
        
        batch["labels"] = outputs.input_ids.copy()

        batch["labels"] = [[-100 if token == 0 else token for token in labels] for labels in batch["labels"]]
      
        # because BERT automatically shifts the labels, the labels correspond exactly to `decoder_input_ids`. 
        # We have to make sure that the PAD token is ignored
      
        return batch

    def set_config(self):
    
        # sensible parameters for beam search
        self.model.config.no_repeat_ngram_size = 3 # A word will not be repeated more than three times while geenrating a new commit message
        self.model.config.early_stopping = True
        self.model.config.length_penalty = 2.0
        self.model.config.do_sample=True
        self.model.config.top_p=0.95
        self.model.config.top_k=60
        #self.model.config.temperature=0.7
        self.model.config.num_beams = 6 # Top-4 words for beam search rather than considering all words for greedy search
        

def model_eval(dataset):

    print("Now evaluatin the model and returning the scores on test data.")
    
    #dataset["commits"] = dataset["Slice"]
    #dataset["message"] = dataset["message"]

    #dataset.drop(["Slice", "Message","Sliced_ad","Unnamed: 0"], inplace=True, axis=1)
    
    test_data = Dataset(pa.Table.from_pandas(dataset))
    #print(glob("./*"))
    checkpoint_path = [x for x  in glob("./*") if x[:12]=="./checkpoint"]
    
    # Setting the model in eval state
    test_model = T5ForConditionalGeneration.from_pretrained(checkpoint_path[0])
    tokenizer = RobertaTokenizer.from_pretrained(checkpoint_path[0])
    test_model.eval()

    test_model.to("cuda")

    def generate_summary(batch):
        # Tokenizer will automatically set [BOS] <text> [EOS]
        prefix = "Generate commit message: "
        inputs = tokenizer([prefix+a+tokenizer.sep_token+b+tokenizer.sep_token+c for a,b,c in zip(batch["add"],batch["del"],batch["common"])], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        input_ids = inputs["input_ids"].to("cuda")
        attention_mask = inputs["attention_mask"].to("cuda")

        outputs = test_model.generate(input_ids, attention_mask=attention_mask,num_beams=6, max_new_tokens=80,top_p=0.95, top_k=60, do_sample=True,no_repeat_ngram_size=3,early_stopping=True,length_penalty=2.0)

        # all special tokens including will be removed
        output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)

        batch["pred"] = output_str

        return batch

    results = test_data.map(generate_summary, batched=True, batch_size=16)

    pred_str = results["pred"]
    label_str = dataset["Message"]
    
    preds = pd.DataFrame()
    preds["ref"] = label_str
    preds["predictions"] = pred_str
    preds.to_csv("predictions_latest.csv",index=False)
    
    #bleu_score =  bleu.Bleu()
    #self.meteor_score = meteor.Meteor()
    #rouge_score = rouge.Rouge()

    #pred_str = [x.lower() for x in results["pred"]]
    #label_str = [x.lower() for x in dataset["message"]]

    #rouge_output = rouge_score.compute(predictions=pred_str, references=label_str)
    #bleu1 = bleu_score.compute(predictions=pred_str, references=label_str,max_order=1)
    #bleu2 = bleu_score.compute(predictions=pred_str, references=label_str, max_order=2)
    #bleu3 = bleu_score.compute(predictions=pred_str, references=label_str, max_order=3)
    #bleu4 = bleu_score.compute(predictions=pred_str, references=label_str, max_order=4)
    #meteor = self.meteor_score.compute(predictions=pred_str, references=label_str)

    #print("-------------------- @@@@@ LOOK FOR METRICS HERE @@@@@ ------------------------")
    #print("Rouge: ",rouge_output)
    #print("Bleu-1: ", bleu1["bleu"])
    #print("Bleu-2: ",bleu2["bleu"])
    #print("Bleu-3: ",bleu3["bleu"])
    #rint("Bleu-4: ", bleu4["bleu"])
    #print("Meteor: ",meteor["meteor"])
    
    
""" MAIN FUNCTION """
    
if __name__ == "__main__":

    data = pd.read_csv("../train_sep.csv")

#    data.drop(["Unnamed: 0", "message", "ad", "adc"], inplace=True, axis=1)

    train = data.iloc[:int(len(data)*0.90),:]
    train["message"] = [x.split("\n")[0].lower() for x in train["Message"]]
    test = data.iloc[int(len(data)*0.90):,:]
    test["message"] = [x.lower() for x in test["Message"]]

    train , test = Dataset(pa.Table.from_pandas(train)), Dataset(pa.Table.from_pandas(test))
    
    model = CodeT5()

    model.set_config()
    
    train_data = train.map(model.process_data_to_model_inputs, batched=True, batch_size=model.batch_size, remove_columns=["add", "Message","del","common"])        
    train_data.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])    
    
    val_data = test.map(model.process_data_to_model_inputs, batched=True, batch_size= model.batch_size,remove_columns=["add", "Message","del","common"])
    val_data.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
    
    training_args = Seq2SeqTrainingArguments(
        output_dir = "./",
        predict_with_generate=True, 
        overwrite_output_dir=True, # Overwrites previously saved model
        learning_rate=5e-5,
        evaluation_strategy="epoch",
        #logging_steps=1_000, 
        # Batch size for train and validaiton. 
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        save_strategy="epoch",
        #push_to_hub=True, # Set to True, so that we can push our trained model to hugginface hub to share
        warmup_steps=1000,
        save_total_limit=1, # Saves one file.
        num_train_epochs=9 #  epochs
    )
    
    model.model.train()

    trainer = Seq2SeqTrainer(
        model=model.model, # Modelname
        tokenizer=model.tokenizer, # Tokenzier 
        args=training_args, # Hyperparameter arguments
        compute_metrics=model.compute_metrics, # Not mandatory (Manually defined rouge metric function)
        # Datasets
        train_dataset=train_data, 
        eval_dataset=val_data
        )
    
    trainer.train()

    torch.cuda.empty_cache()
    

    eval_dataset = pd.read_csv("../test_sep.csv")

    # Evaluation Stage
    model_eval(eval_dataset)