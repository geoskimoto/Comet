#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 02:34:29 2023

@author: abhinav
"""

import CodePreProcessCode
import sys
import os
sys.path.append("/Users/abhinav/Desktop/Self-Research-study/Commits/GraphUnion")
import pre_processing
import graph_functions
import graph_diff
import slicing
import shutil 

class Cpg:
    def __init__(self):
        
        # Initializing objects
         self.cpg_generator = CodePreProcessCode.CodePreProcess()
         self.clean = pre_processing.Preprocess_graph()
        
    def get_dot(self,old,new):
        
        prev_processed_path = self.cpg_generator.process(old, "prev_file")
        print("PREVIOUS PROCESSED\n\n\n\n")
        new_processed_path = self.cpg_generator.process(new, "new_file")
        print("NEW PROCESSED\n\n\n\n")
        
        prev_processed = self.clean.eliminate_duplicate(prev_processed_path)
        new_processed = self.clean.eliminate_duplicate(new_processed_path)
        
        
        print("CPG GENERATOR PROCESSING COMPLETED")
        
        extraction =  graph_functions.Extract()
        
        print("GRAPH EXTRACTION COMPLETED")
        
        c_nodes, a_nodes, d_nodes = extraction.extract_nodes(prev_processed, new_processed)
                
        print("NODE EXTRACTION COMPLETED")
        
        c_edges, a_edges, d_edges = extraction.extract_edges(prev_processed, new_processed)
        
        print("EDGE EXTRACTION COMPLETED")
        
        
        graph_components = graph_diff.GraphU(c_nodes, a_nodes, d_nodes, c_edges, a_edges, d_edges)
        
        print("GRAPH BUILT")
        complete_diff = graph_components.diff_graph()
        
        # TODO : Combine different method diff graphs
        
        # TODO : Slice through the combined graph and get a final graphUnion
        
        slicer = slicing.Slice(complete_diff)
        
        print("SLICING IN PROGRESS")
        
        sliced_final_diff = slicer.slice()
        
        return sliced_final_diff , complete_diff

        
        
        
        
        
        
        
        
        