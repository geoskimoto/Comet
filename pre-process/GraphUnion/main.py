#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:57:42 2023

@author: abhinav
"""
# Importing libraries

# Importing libraries from custom classes
import pre_processing
import graph_functions
import graph_diff
import joern_cpg
import slicing
import json_extractor

def main():
    
    """ PARSING CODE TO GRAPHS """
    
    parser = joern_cpg.Cpg("code/one.java", "code/two.java")
    
    # Input paths of dot files of new and old graph
    input_path_old, input_path_new  = parser.get_dot()
    
    
    # Objects
    prev_object = pre_processing.Preprocess_graph(input_path_old)
    new_object = pre_processing.Preprocess_graph(input_path_new)
    

    # eliminating duplicated nodes
    prev_processed = prev_object.eliminate_duplicate()
    new_processed = new_object.eliminate_duplicate()
    
    
    extraction =  graph_functions.Extract(prev_processed, new_processed)
    
    c_nodes, a_nodes, d_nodes = extraction.extract_nodes()

    c_edges, a_edges, d_edges = extraction.extract_edges()

    graph_components = graph_diff.GraphU(c_nodes, a_nodes, d_nodes, c_edges, a_edges, d_edges)
    
    diff = graph_components.diff_graph()
    
    # TODO : Combine different method diff graphs
    
    # TODO : Slice through the combined graph and get a final graphUnion
    extractor = json_extractor.Extract_json(diff)
    diff_json = extractor.get_json()
    
    slicer = slicing.Slice(diff_json)
    
    final_diff = slicer.slice()
    
    return final_diff
   
    

if __name__ == "__main__":
    
    diff_graph = main()
    
    diff_graph.write_raw("graph.dot")
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    













    