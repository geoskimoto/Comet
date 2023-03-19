#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:57:42 2023

@author: abhinav
"""
# Importing libraries

# Impor

import sys
sys.path.append('./*')

import pre_processing 
import graph_functions
import graph_diff
import joern_cpg
import slicing


class GU:
    def __init__(self):
        pass
        print("GraphUnion Object Created :-))")
        
    def dot_to_json(self, graph):

      nodes = [{"id":x.get_name() , "CODE":x.get_attributes().get("CODE"), "label":x.get_attributes().get('label')} for x in graph.get_nodes()]
    
      edges = [{"source":graph.get_node(x.get_source())[0].get_name(), "target":graph.get_node(x.get_destination())[0].get_name(), "label":x.get_label()} for x in graph.get_edges()]
    
      graph_ = {"name":"G", 'nodes':nodes, "links":edges}
    
      return graph_
        
    def get_graph_union(self,path1, path2):
        
        """ PARSING CODE TO GRAPHS """
        
        parser = joern_cpg.Cpg(path1, path2)
        
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
                        
        slicer = slicing.Slice(diff)
        
        final_diff = slicer.slice()
        
        return final_diff
       
        
        

    
    
    
    
    
    
    













    