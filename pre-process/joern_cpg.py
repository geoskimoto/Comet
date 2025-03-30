#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 02:34:29 2023

@author: abhinav
"""

import CodePreProcess
import sys
import os
sys.path.append("./GraphUnion")
import pre_processing
print('successfully imported pre_preprocessing.py from~ /Projects/comet/Comet/pre-process/GraphUnion ')
import graph_functions
import graph_diff
import slicing
import shutil 

class Cpg:
    def __init__(self):
        
        # Initializing objects
         print('initializing CodePreProcess.CodePreProcess()')
         self.cpg_generator = CodePreProcess.CodePreProcess()
         print('initializing pre_preprocessing.Preprocess_graph()')
         self.clean = pre_processing.Preprocess_graph()
         print('Cpg initialization complete.')
         
    def get_dot(self,old,new):
        print('starting Cpg.get_dot(...)')
        prev_processed_path = self.cpg_generator.process(old, "prev_file")
        print(f'prev_processed_path: {prev_processed_path}.  Im in joern_cpg.py')
        new_processed_path = self.cpg_generator.process(new, "new_file")
        print(f'new_processed_path: {new_processed_path}. Im in joern_cpg.py')

        prev_processed = self.clean.eliminate_duplicate(prev_processed_path)
        # print(f'prev_processed: {prev_processed}')
        
        new_processed = self.clean.eliminate_duplicate(new_processed_path)
        # print(f'new_processed: {new_processed}')
        
        
        print("CPG GENERATOR PROCESSING COMPLETED.  IM IN joern_cpg.py.")
        
        extraction =  graph_functions.Extract()
        
        print("GRAPH EXTRACTION COMPLETED.  IM IN joern_cpg.py.")
        
        c_nodes, a_nodes, d_nodes = extraction.extract_nodes(prev_processed, new_processed)
        for nodes in [c_nodes, a_nodes, d_nodes]:
            if nodes is None:
                print('nodes are None.')     
        print("NODE EXTRACTION COMPLETED.  IM IN joern_cpg.py.")
        
        c_edges, a_edges, d_edges = extraction.extract_edges(prev_processed, new_processed)
        for edges in [c_edges, a_edges, d_edges]:
            if edges is None:
                print('edges are None.')
            
        print("EDGE EXTRACTION COMPLETED.  IM IN joern_cpg.py.")
        
        
        graph_components = graph_diff.GraphU(c_nodes, a_nodes, d_nodes, c_edges, a_edges, d_edges)
        
        print("GRAPH BUILT.  IM IN joern_cpg.py.")
        try:
            complete_diff = graph_components.diff_graph()
            print(f'complete_diff: {complete_diff}')
        except Exception as e:
            print("Failed at raph_components.diff_graph() in joern_cpg.py")
            print(e)
            if complete_diff:
                print(type('complete_diff'))
            else:
                print('complete_diff returning as None.')

        # TODO : Combine different method diff graphs
        
        # TODO : Slice through the combined graph and get a final graphUnion
        
        slicer = slicing.Slice(complete_diff)
        if slicer is None:
            print('slicer is returning None.')
        print("SLICING IN PROGRESS.  IM IN joern_cpg.py.")
        try:
            sliced_final_diff = slicer.slice()
            return sliced_final_diff 

        except Exception as e:
            print("Failed at slicer.slice() in jeorn_cpg.py")
            print(e)
            pass


        
        
        
        
        
        
        
        
        