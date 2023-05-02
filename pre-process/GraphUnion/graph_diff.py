#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:55:31 2023

@author: abhinav
"""

import pydot

class GraphU:
    def __init__(self,common_nodes_new, added_nodes, deleted_nodes,common_edges_new, added_edges, deleted_edges):
        self.common_nodes_new = common_nodes_new
        self.added_nodes = added_nodes
        self.deleted_nodes = deleted_nodes
        self.common_edges_new = common_edges_new
        self.added_edges = added_edges
        self.deleted_edges = deleted_edges
        
    def diff_graph(self,save_output=False):
      """Generated a pydot graph from graph."""
      
      pydot_graph = pydot.Dot(graph_type='digraph')
    
      # Nodes
      for node in self.added_nodes:
        pydot_graph.add_node(node)
      for node in self.deleted_nodes:
        pydot_graph.add_node(node)
      for node in self.common_nodes_new:
        pydot_graph.add_node(node)
    
    
      # Edges
      for edge in self.added_edges:
          pydot_graph.add_edge(edge)
      for edge in self.deleted_edges:
          pydot_graph.add_edge(edge)
      for edge in self.common_edges_new:
          pydot_graph.add_edge(edge)
          
    
      return pydot_graph
    
    
    

