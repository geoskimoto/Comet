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
        print('initializing parser')
        parser = joern_cpg.Cpg(path1, path2)
        print('parsing using jeorn_cpg.Cpg')
        # Input paths of dot files of new and old graph
        input_path_old, input_path_new  = parser.get_dot()
        
        print('creating prev_object and new_object')
        # Objects
        prev_object = pre_processing.Preprocess_graph(input_path_old)
        new_object = pre_processing.Preprocess_graph(input_path_new)
        
    
        # eliminating duplicated nodes
        try:
          prev_processed = prev_object.eliminate_duplicate()
          print("elim duplicates in prev_processed success")
          new_processed = new_object.eliminate_duplicate()
          print("elim duplicates in new_processed success.")
        except Exception as e:
           print(e)
           pass
        
        print('extracting from prev_processed and new_processed.')
        extraction =  graph_functions.Extract(prev_processed, new_processed)
        
        print('extracting nodes')
        c_nodes, a_nodes, d_nodes = extraction.extract_nodes()
        print('extracting edges')
        c_edges, a_edges, d_edges = extraction.extract_edges()
        print('graph components')
        graph_components = graph_diff.GraphU(c_nodes, a_nodes, d_nodes, c_edges, a_edges, d_edges)
        print('determining diff in graphs')
        diff = graph_components.diff_graph()
        print('slicing bread')
        slicer = slicing.Slice(diff)
        print('final diff')
        final_diff = slicer.slice()
        
        return final_diff
       
        
        

    
    
    
    
    
    
    













    