#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 12:28:44 2023

@author: anonymous
"""

# Importing libararies

# Importing libraries 

import os
os.environ['DGLBACKEND'] = 'pytorch'
import torch
import torch.nn as nn
import torch.nn.functional as F

import dgl
import dgl.data


from dgl.nn import GraphConv

class GraphCN(nn.Module):
    def __init__(self, in_feats, h_feats, num_classes):
        super(GraphCN,self).__init__()
        self.conv1 = GraphConv(in_feats, h_feats)
        self.conv2 = GraphConv(h_feats, num_classes)

    def forward(self, g, in_feat):
        h = self.conv1(g, in_feat)
        h = F.relu(h)
        h = h.detach()
        h = self.conv2(g, h)
        return h
        
    def extract_embeddings(self, g, in_feat):
        h = self.conv1(g, in_feat)
        h = F.relu(h)
        h = h.detach()
        return h