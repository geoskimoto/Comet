#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 17:56:20 2023

@author: abhinav
"""

import pydot


class Slice:
    
    def __init__(self, graph):
        self.graph = graph
        
    def dot_to_json(self, graph):

      nodes = [{"_gvid":x.get_name() , "CODE":x.get_attributes().get("CODE"), "label":x.get_attributes().get('label'),"TYPE":x.get_attributes().get("TYPE")} for x in graph.get_nodes()]
    
      edges = [{"tail":graph.get_node(x.get_source())[0].get_name(), "head":graph.get_node(x.get_destination())[0].get_name(), "label":x.get_label()} for x in graph.get_edges()]
    
      graph_ = {"name":"G", 'objects':nodes, "edges":edges}
    
      return graph_
        
    def slice(self):
        
        graph = self.dot_to_json(self.graph)

        # Gathering the edited nodes (Added, deleted)
        edited_nodes = []
        for nodes in graph['objects']:
            if nodes.get('TYPE') == "DEL" or nodes.get('TYPE') == "ADD": 
                edited_nodes.append(nodes.get('_gvid'))
                
        
        #Gathering all the edges related to the edited nodes (1 hop)
        new_edges = []
        
        for edges in graph['edges']:
            if edges.get('tail') in edited_nodes or edges.get('head') in edited_nodes:
                new_edges.append(edges)
        
        # Gathering the nodes related to the new edges
        related_nodes = []

        for edge in new_edges:
          related_nodes.append(edge.get("tail"))
          related_nodes.append(edge.get("head"))
        
        related_nodes = set(related_nodes)
        
        # Storing the new nodes 
        new_nodes = []
    
        for nodes in graph['objects']:
          if nodes.get('_gvid') in related_nodes:
              new_nodes.append(nodes)
              
        
        # Constructing a graph for new edges and nodes
        new_graph = graph
        new_graph['objects'] = new_nodes
        new_graph['edges'] = new_edges
        
        # 2. Create Pydot graph object
        pydot_graph = pydot.Dot(graph_type='graph')
        
        # 3. Traverse JSON object and add nodes and edges
        for node in new_graph['objects']:
            pydot_graph.add_node(pydot.Node(node.get('_gvid'), label=node.get('label'), CODE=node.get('CODE'), TYPE=node.get('TYPE')))
          
        for edge in new_graph['edges']:
            new_src = [x.get('_gvid') for x in graph['objects'] if x.get('_gvid')==edge.get('tail')][0]
            new_dest = [x.get('_gvid') for x in graph['objects'] if x.get('_gvid')==edge.get('head')][0]
            pydot_graph.add_edge(pydot.Edge(new_src, new_dest, label=edge['label']))
            
        return pydot_graph        
                            