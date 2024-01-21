#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 12:30:09 2023

@author: anonymous
"""

# Importing libraries
import GCN
import dgl.data
import numpy as np
import dgl
import os
from transformers import AutoTokenizer, AutoModel
import torch
os.environ['DGLBACKEND'] = "pytorch"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import random

class Embeddings:

    def __init__(self):
        print("Loading Pre-trained Models")
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncase")
        self.model = AutoModel.from_pretrained("bert-base-uncase")

    def get_init_embeddings(self, data):

        data_embeds = []
        sep_token = self.tokenizer.sep_token

        # Extracting the features form graph
        for nodes in data.get('objects'):
            
            if nodes.get("label") == None:
                labels = "null"
            else:
                labels  = nodes.get("label")
            if nodes.get('i_edge') == None:
                incoming_edges = "null"
            else:
                incoming_edges = nodes.get('i_edge')
            
            data_embeds.append(str(labels+sep_token+incoming_edges))

        assert len(data_embeds) == len(data['objects']), "Sizes do not match"+str(len(data_embeds))+" "+str(len(data["objects"]))

        embed_input_ids = self.tokenizer(data_embeds, padding="max_length", max_length=20, truncation=True, return_tensors='pt')['input_ids']

        # Embeddings for all the tokens
        embeddings = self.model(embed_input_ids)["last_hidden_state"]

        # Embeddings for CLS token (represents the whole sentence)
        initial_representation = embeddings[:, :1, :].permute(1, 0, 2)  # '0' is the CLS token

        return initial_representation

    def get_dglGraph(self, data):
        """ EDGE INDEX MEHTOD"""
        def edge_index(data):
            edge_index = []
            heads = set([x.get("head") for x in data.get('edges')])

            for h in heads:
                for edges in data.get('edges'):
                    if edges.get("head") == h:
                        edge_index.append(
                            (edges.get('tail'), edges.get('head')))

            edge_index = np.array(edge_index)
            assert edge_index.shape[1] == 2, "edge_index returning incorrect shape. Expected : (E,2)"
            return edge_index

        edge_index = edge_index(data)

        # Edge source and target tensors
        source_ids = torch.tensor([int(x[0]) for x in edge_index])
        target_ids = torch.tensor([int(x[1]) for x in edge_index])

        # Total Nodes
        total_nodes = len(data.get("objects"))

        dgl_graph = dgl.graph((source_ids, target_ids), num_nodes=total_nodes)
        dgl_graph = dgl.add_self_loop(dgl_graph)
        
        # Nominals || Clauses || Modifier words || Functional words
        mappings = {"nsubj":0,"obj":0,"iobj":0,"obl":0,"vocative":0,"expl":0,"dislocated":0,"nmod":0,
                    "appos":0,"nummod":0,"csubj":1,"ccomp":1,"xcomp":1,"acl":1,"advcl":1,"advmod*":2,
                    "amod":2,"discourse":2,"aux":3,"cop":3,"mark":3,"det":3,"clf":3,"case":3,"null":4}     

        # Labels
        labels = [x.get("i_edge").replace('"','') for x in data.get('objects')]

        print("------- LABELS HERE ------")
        for i in range(len(labels)):
            if labels[i] in mappings.keys():
                labels[i] = mappings[labels[i]]
            else:
                labels[i] = 4
        print(len(set(labels)), " is the label set length")
        # TODO : Map these labels to numerics https://universaldependencies.org/u/dep/index.html # DONE

        dgl_graph.ndata['labels'] = torch.tensor(labels)
        train_size = int(total_nodes * 0.75)
        val_size = int(total_nodes * 0.15)
        test_size = int(total_nodes * 0.1)

        all_indices = set(range(total_nodes))
        train_indices = set(random.sample(all_indices, train_size))
        val_indices = set(random.sample(all_indices - train_indices, val_size))
        test_indices = set(random.sample(all_indices - train_indices - val_indices, test_size))

        # Set the corresponding masks for each index
        train_mask = torch.zeros(total_nodes, dtype=torch.bool)
        train_mask[list(train_indices)] = 1
        dgl_graph.ndata['train_mask'] = train_mask

        val_mask = torch.zeros(total_nodes, dtype=torch.bool)
        val_mask[list(val_indices)] = 1
        dgl_graph.ndata['val_mask'] = val_mask

        test_mask = torch.zeros(total_nodes, dtype=torch.bool)
        test_mask[list(test_indices)] = 1
        dgl_graph.ndata['test_mask'] = test_mask

        return dgl_graph

    def get_graph_embeddings(self, data, nothing=None):

        print("BULIDNG DGL GRAPH")
        graph = self.get_dglGraph(data)
        initial_representation = self.get_init_embeddings(data)

        model = GCN.GraphCN(768, 256, 5)
        model.load_state_dict(torch.load("gnn_models/text_gnn_final.pth"))

        model.eval()

        print("Extracting embeddings")
        graph_embeddings = model.extract_embeddings(graph, initial_representation.squeeze())

        return graph_embeddings
