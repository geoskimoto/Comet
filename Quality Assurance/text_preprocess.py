#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 03:20:03 2023

@author: anonymous
"""

class Preprocess:
    
    def __init__(self):
        pass
        
    def return_processed(self, jsonfile):
        
        new_nodes = []
        
        first_node = jsonfile.get('objects')[0]
        first_node.update({"i_edge":"none"})
        new_nodes.append(first_node)

        for edge in jsonfile.get('edges'):
          for node in jsonfile.get('objects'):
            if node.get('_gvid') == edge.get("head"):
              temp_node = node
              label = edge.get('label')
              temp_node.update({"i_edge": label})
              new_nodes.append(temp_node)
              
        
        jsonfile['objects'] = new_nodes
        
        return jsonfile