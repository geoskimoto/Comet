#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 12:30:09 2023
@author: anonymous
"""

# Importing libraries
import os
from transformers import AutoTokenizer, AutoModel
import torch
os.environ['DGLBACKEND'] = 'pytorch'
import dgl
import numpy as np
import dgl.data
import GCN
import random
import math

class Code_embeddings:
    
    def __init__ (self):
        self.tokenizer = AutoTokenizer.from_pretrained("codebert-encoder")
        self.model = AutoModel.from_pretrained("codebert-encoder")
        
    
    def dot_to_json(self,graph):
    
      nodes = [{"id":x.get_name() , "CODE":x.get_attributes().get("CODE"), "label":x.get_attributes().get('label'),"TYPE":x.get_attributes().get("TYPE")} for x in graph.get_nodes() if x.get_attributes().get("TYPE")!= None]
    
      edges = [{"tail":graph.get_node(x.get_source())[0].get_name(), "head":graph.get_node(x.get_destination())[0].get_name(), "label":x.get_label()} for x in graph.get_edges()]
    
      graph_ = {"name":"G", 'objects':nodes, "edges":edges}
    
      return graph_
        
    def get_init_embeddings(self,tokens):
        
        # Loding the Initial model        
        print("Loading Pre-trained Models")
        
        embed_input_ids = self.tokenizer(tokens, padding="max_length", max_length=40, truncation=True, return_tensors='pt')['input_ids']
        
        # Embeddings for all the tokens
        embeddings = self.model(torch.tensor(embed_input_ids))["last_hidden_state"]
        
        # Embeddings for CLS token (represents the whole sentence)
        initial_representation = embeddings[:,:1,:].permute(1, 0, 2)  # '0' is the CLS token
        
        return initial_representation
    
    def code_to_ids(self,graph_json):
        
        obj_ids = {}
        [obj_ids.update({obj.get("id").replace('"',''):[i,obj.get("TYPE")]}) for i,obj in enumerate(graph_json.get("objects")) if obj.get("id")!=None]

        for i,x in enumerate(obj_ids):
            obj_ids[x][0]=i
        
        for index in range(len(graph_json.get("edges"))):
           if graph_json.get("edges")[index]["tail"].replace('"','') in obj_ids:
             graph_json.get("edges")[index]["tail"] = obj_ids[graph_json.get("edges")[index]["tail"].replace('"','')][0]
           if graph_json.get("edges")[index]["head"].replace('"','') in obj_ids:
             graph_json.get("edges")[index]["head"] = obj_ids[graph_json.get("edges")[index]["head"].replace('"','')][0]
             
        labels = [obj_ids[x][1] for x in obj_ids]
        
        return graph_json, len(obj_ids), labels
    
    def get_dglGraph(self,graph_dot):
                
        graph = self.dot_to_json(graph_dot)
        
        numid_graph, nodes_length, labels = self.code_to_ids(graph)
            
        """ EDGE INDEX MEHTOD"""
        def edge_index(data):
          edge_index = []
          heads = set([x.get("head") for x in data['edges']])
        
          for h in heads:
            for edges in data['edges']:
              if edges.get("head") == h:
                edge_index.append((edges.get('tail'),edges.get('head')))
                
        
          edge_index = np.array(edge_index)
          assert edge_index.shape[1] == 2 , "edge_index returning incorrect shape. Expected : (E,2)"
          return edge_index
         
        edge_index = edge_index(numid_graph)
        
        print(edge_index)
         
        # Edge source and target tensors 
        source_ids = torch.tensor([x[0] for x in edge_index])
        target_ids = torch.tensor([x[1] for x in edge_index])
        
        mappings = {"ADD":0, "DEL":1,"COMMON":2}
        for i in range(len(labels)):
            if labels[i] in mappings:
                labels[i] = mappings[labels[i]]       
        
        dgl_graph = dgl.graph((source_ids, target_ids), num_nodes=nodes_length)
        dgl_graph = dgl.add_self_loop(dgl_graph)
        
        print('LABELS\n', labels, "LENGTH\n", len(labels) )
        # Adding labels, train, test and val masks
        dgl_graph.ndata["labels"] = torch.tensor(labels)

        # Train, test and validation split 

        # Split ids
        idxs = np.arange(nodes_length)
        # shuffle the indices
        np.random.shuffle(idxs)

        num_train = int(nodes_length * 0.75)
        num_val = math.ceil(nodes_length * 0.15)
        num_test = nodes_length - num_train - num_val

        train_idxs = idxs[:num_train]
        val_idxs = idxs[num_train:num_train + num_val]
        test_idxs = idxs[num_train + num_val:]

        # Setting indexes

        # Generate a list of indices for each mask
        num_nodes = nodes_length
        
        train_size = int(num_nodes * 0.75)
        val_size = int(num_nodes * 0.15)
        test_size = int(num_nodes * 0.1)

        all_indices = set(range(num_nodes))
        train_indices = set(random.sample(all_indices, train_size))
        val_indices = set(random.sample(all_indices - train_indices, val_size))
        test_indices = set(random.sample(all_indices - train_indices - val_indices, test_size))

        # Set the corresponding masks for each index
        train_mask = torch.zeros(num_nodes, dtype=torch.bool)
        train_mask[list(train_indices)] = 1
        dgl_graph.ndata['train_mask'] = train_mask

        val_mask = torch.zeros(num_nodes, dtype=torch.bool)
        val_mask[list(val_indices)] = 1
        dgl_graph.ndata['val_mask'] = val_mask

        test_mask = torch.zeros(num_nodes, dtype=torch.bool)
        test_mask[list(test_indices)] = 1
        dgl_graph.ndata['test_mask'] = test_mask

        #dgl_graph.ndata['train_mask'] = torch.zeros(nodes_length, dtype=torch.bool).bernoulli(0.75)
        #dgl_graph.ndata['val_mask'] = torch.zeros(nodes_length, dtype=torch.bool).bernoulli(0.15)
        #dgl_graph.ndata['test_mask']  = torch.zeros(nodes_length, dtype=torch.bool).bernoulli(0.1)
        
        return dgl_graph
        
    
    def get_graph_embeddings(self, tokens, graph_dot):
        
        print("BULIDNG DGL GRAPH")
        graph = self.get_dglGraph(graph_dot)
        initial_representation = self.get_init_embeddings(tokens)
        
        
        print("HERE ------ CHECK FOR THIS CODE EMBEDDINGS:")
        print(graph)
        print(initial_representation.shape)
        
        model = GCN.GraphCN(768, 256, 3)
        model.load_state_dict(torch.load("gnn_models/code_gnn_final.pth"))
  
        model.eval()
        
        print("Extracting embeddings")
        graph_embeddings = model.extract_embeddings(graph, initial_representation.squeeze())
        
        return graph_embeddings