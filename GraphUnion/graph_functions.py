#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:52:53 2023

@author: abhinav
"""

class Extract:
    
    def __init__(self):
        pass
    
    """ NODE MANIPULATION """
    def extract_nodes(self,prev_graph, new_graph):
        previous_code_nodes = [(x.get_attributes().get('CODE'),x.get_attributes().get('label')) for x in prev_graph.get_nodes()]
        new_code_nodes = [(x.get_attributes().get('CODE'),x.get_attributes().get('label')) for x in new_graph.get_nodes()]
        
        # Resulting codes after set operations
        added_nodes_code = set(new_code_nodes) - set(previous_code_nodes)
        deleted_nodes_code = set(previous_code_nodes) - set(new_code_nodes)
        common_nodes_code = set(new_code_nodes) & set(previous_code_nodes)
        
        
        # Resulting edges from grabbed code and labels
        deleted_nodes = [x for x in prev_graph.get_nodes() if (x.get_attributes().get('CODE'),x.get_attributes().get('label')) in deleted_nodes_code and (x.get_attributes().get('label')!= None and x.get_attributes().get('CODE'))]
        common_nodes_old = [x for x in prev_graph.get_nodes() if (x.get_attributes().get('CODE'),x.get_attributes().get('label')) in common_nodes_code and (x.get_attributes().get('label')!= None and x.get_attributes().get('CODE'))]
        
        added_nodes = [x for x in new_graph.get_nodes() if (x.get_attributes().get('CODE'),x.get_attributes().get('label')) in added_nodes_code and (x.get_attributes().get('label')!= None and x.get_attributes().get('CODE'))]
        common_nodes_new = [x for x in new_graph.get_nodes() if (x.get_attributes().get('CODE'),x.get_attributes().get('label')) in common_nodes_code and (x.get_attributes().get('label')!= None and x.get_attributes().get('CODE'))]
        
        
        # Adding node types to the attribute section 
        for x in added_nodes:
            x.obj_dict["attributes"]["TYPE"] = "ADD"
    
        for x in deleted_nodes:
            x.obj_dict["attributes"]["TYPE"] = "DEL"
    
        for x in common_nodes_old:
            x.obj_dict["attributes"]["TYPE"] = "COMMON"
    
        for x in common_nodes_new:
            x.obj_dict["attributes"]["TYPE"] = "COMMON"
        
        return common_nodes_new, added_nodes, deleted_nodes
    
    
    def extract_edges(self,prev_graph, new_graph):
        prev_code_edges = [(prev_graph.get_node(x.get_source())[0].get_attributes()['CODE'], prev_graph.get_node(x.get_destination())[0].get_attributes()['CODE'], x.get_label()) for x in prev_graph.get_edges()]
        new_code_edges = [(new_graph.get_node(x.get_source())[0].get_attributes()['CODE'], new_graph.get_node(x.get_destination())[0].get_attributes()['CODE'], x.get_label()) for x in new_graph.get_edges()]
        
        deleted_edges_code = set(prev_code_edges) - set(new_code_edges)
        added_edges_code = set(new_code_edges) - set(prev_code_edges)
        common_edges_code = set(new_code_edges) & set(prev_code_edges)
        
        
        added_edges = [x for x in new_graph.get_edges() if (new_graph.get_node(x.get_source())[0].get_attributes()['CODE'], new_graph.get_node(x.get_destination())[0].get_attributes()['CODE'], x.get_label()) in added_edges_code]
        common_edges_new = [x for x in new_graph.get_edges() if (new_graph.get_node(x.get_source())[0].get_attributes()['CODE'], new_graph.get_node(x.get_destination())[0].get_attributes()['CODE'], x.get_label()) in common_edges_code]
        
        deleted_edges = [x for x in prev_graph.get_edges() if (prev_graph.get_node(x.get_source())[0].get_attributes()['CODE'], prev_graph.get_node(x.get_destination())[0].get_attributes()['CODE'], x.get_label()) in deleted_edges_code]
  #      common_edges_old = [x for x in prev_graph.get_edges() if (prev_graph.get_node(x.get_source())[0].get_attributes()['CODE'], prev_graph.get_node(x.get_destination())[0].get_attributes()['CODE'], x.get_label()) in common_edges_code]
        
        
        return common_edges_new, added_edges, deleted_edges
    
    
        
    