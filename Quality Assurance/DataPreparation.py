#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:43:11 2023

@author: anonymous
"""

import os
from glob import glob
import initial_representation_code
import initial_representation_text
import text_preprocess
import nlpparser
import pandas as pd
from dgl.data.utils import save_graphs
import numpy as np 
import pydot
import torch 
import re

def dot_to_json(graph):

  nodes = [{"_gvid":x.get_name() ,"CODE":x.get_attributes().get('CODE'),"TYPE":x.get_attributes().get('TYPE')} for x in graph.get_nodes()]

  edges = [{"tail":graph.get_node(x.get_source())[0].get_name(), "head":graph.get_node(x.get_destination())[0].get_name(), "label":x.get_label()} for x in graph.get_edges()]

  graph_ = {"name":"G", 'objects':nodes, "edges":edges}

  return graph_

if __name__ == "__main__":

    os.makedirs("text_embeddings", exist_ok=True)
    os.makedirs("code_embeddings", exist_ok=True)
    
    preprocess_obj = text_preprocess.Preprocess()
    print("GRAPH STARTED")

    folders = sorted(glob("data/*"))

    # Objects
    init_rep_obj = initial_representation_code.Code_embeddings()
    init_rep_obj_text = initial_representation_text.Embeddings()

    for f in folders:

        files = sorted(glob(f+"/*"))
        graphs = [x for x in files if x[-3:]=="dot"][478:]
        text = [x for x in files if x[-3:]=="txt"][478:]
        print(len(graphs))
        print("GRAPH READING  NOW ")
        index = 478
        for s,t in zip(graphs,text):
            try:

                print("-------------------Now doing for folder: ", f," and in that check for this number: ",index, "-------------------")
                s_ = pydot.graph_from_dot_file(s)[0]
                with open(t,"r") as f:
                    t__ = f.read()
                t_ = " ".join(re.sub('[^a-zA-Z0-9]', ' ', t__).split())
                nlpparser_obj = nlpparser.TextParser(t_)
                parsed_data_dot = nlpparser_obj.get_parsed_dot()
                parsed_data_json = dot_to_json(parsed_data_dot)
                final_json = preprocess_obj.return_processed(parsed_data_json)

                tokens = list(set([x.get_attributes().get('CODE') for x in s_.get_nodes() if x.get_attributes().get('CODE')!= None]))

                print("Now parsing", index," ........")
                
                # THIS IS FOR CODE EMBEDDINGS
                tensors_path = "code_embeddings/t"+str(index)+".npy"
                # Initial representation object
                initial_representation = init_rep_obj.get_graph_embeddings(tokens, s_)
                print(initial_representation.shape)
                # Save tensors
                np.save(tensors_path,initial_representation.detach().numpy())

                # THIS IS FOR TEXT EMBEDDINGS

                tensors_path_text = "text_embeddings/t"+str(index)+".npy"
                # Initial representation object
                initial_representation = init_rep_obj_text.get_graph_embeddings(final_json)
                print(initial_representation.shape)
                # Save tensors
                np.save(tensors_path_text,initial_representation.detach().numpy())

                #torch.cuda.empty_cache()
                print("COMPLETED : ", index)
                index += 1
                torch.cuda.empty_cache()
            except:
                 try:
                 #    os.remove(tensor_path)
                     torch.cuda.empty_cache()
                     #os.remove(graphs_path)
                 except:
                     pass

                 index += 1
                 print('FAILED AT :'. index)
         
         