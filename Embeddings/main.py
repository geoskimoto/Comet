#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 18:19:43 2023

@author: abhinav
"""
import initial_representation


def main():
    
    input_path = "nosymb.dot"
    
    representation = initial_representation.Embeddings()
    
    embeddings = representation.get_graph_embeddings(input_path)
    
    return embeddings
    

if __name__ == "__main__":
    
    embeddings = main()
    
    print(embeddings.shape)
    