#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 12:30:09 2023
@author: abhinav
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

class Code_embeddings:
    
    def __init__ (self,tokens, graph_dot):
        self.tokens = tokens
        self.graph_dot = graph_dot
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = AutoModel.from_pretrained("microsoft/codebert-base")
        
    
    def dot_to_json(self,graph):
    
      nodes = [{"id":x.get_name() , "CODE":x.get_attributes().get("CODE"), "label":x.get_attributes().get('label'),"TYPE":x.get_attributes().get("TYPE")} for x in graph.get_nodes() if x.get_attributes().get("TYPE")!= None]
    
      edges = [{"tail":graph.get_node(x.get_source())[0].get_name(), "head":graph.get_node(x.get_destination())[0].get_name(), "label":x.get_label()} for x in graph.get_edges()]
    
      graph_ = {"name":"G", 'objects':nodes, "edges":edges}
    
      return graph_
        
    def get_init_embeddings(self):
        
        # Loding the Initial model        
        print("Loading Pre-trained Models")

        embed_input_ids = self.tokenizer(self.tokens, padding="max_length", max_length=40, truncation=True, return_tensors='pt')['input_ids']
        
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
    
    def get_dglGraph(self):
                
        graph = self.dot_to_json(self.graph_dot)
        
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
        dgl_graph.ndata['train_mask'] = torch.zeros(nodes_length, dtype=torch.bool)
        dgl_graph.ndata['val_mask'] = torch.zeros(nodes_length, dtype=torch.bool)
        dgl_graph.ndata['test_mask']  = torch.zeros(nodes_length, dtype=torch.bool)      
        
        return dgl_graph
        
    
    def get_graph_embeddings(self):
        
        print("BULIDNG DGL GRAPH")
        graph = self.get_dglGraph()
        initial_representation = self.get_init_embeddings()
        
        
        print("HERE ------ CHECK FOR THIS CODE EMBEDDINGS:")
        print(graph)
        print(initial_representation.shape)
        
        model = GCN.GCN(768, 256, 11)
        model.load_state_dict(torch.load("/Users/abhinav/Desktop/Self-Research-study/Commits/Embeddings/models/graph_embedding_weights.pth"))
  
        model.eval()
        
        print("Extracting embeddings")
        graph_embeddings = model.extract_embeddings(graph, initial_representation.squeeze())
        
        return graph_embeddings