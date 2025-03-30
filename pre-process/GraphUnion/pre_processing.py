#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:55:39 2023

@author: abhinav
"""

# Importing libraries
import pydot

class Preprocess_graph:
    
    def __init__(self):
        pass
    
    def dot_to_json(self, graph):

      nodes = [{"id":x.get_name() , "CODE":x.get_attributes().get("CODE"), "label":x.get_attributes().get('label')} for x in graph.get_nodes()]
    
      edges = [{"source":graph.get_node(x.get_source())[0].get_name(), "target":graph.get_node(x.get_destination())[0].get_name(), "label":x.get_label()} for x in graph.get_edges()]
    
      graph_ = {"name":"G", 'nodes':nodes, "links":edges}
    
      return graph_
    
    
    """ ELIMINATING DUPLICATE NODES """
    def eliminate_duplicate(self,dot,save_output=False):
        
        print("ELIMINATING DUPLICATES (I'm in pre_process.py)")
              
        dot = pydot.graph_from_dot_file(dot)[0]
        
        njson = self.dot_to_json(dot)
        
        code_snippets = [[nodes.get("CODE"), nodes.get("id")] for nodes in njson['nodes']]
        
        current = None
        
        final_replace = []
        final_retain = []
        indexes_to_remove = []
        # print()
        for i in range(len(code_snippets)):
          counter = 0
          current = code_snippets[i][1]
          for j in range(i,len(code_snippets)):
            if code_snippets[i][0] == code_snippets[j][0] and i!=j:
                counter +=1
                indexes_to_remove.append(j)
                njson['nodes'][j].update({"id":current})
                final_replace.append(code_snippets[j][1])
        
            if counter>0 and j==(len(code_snippets)-1):
              final_retain.append(current)
        
        nodes_to_pop = [x for i,x in enumerate(njson['nodes']) if i in indexes_to_remove]
        print('A')
        for n in nodes_to_pop:
          njson['nodes'].remove(n)
        
        mappings = [[ret,rep] for ret,rep in zip(final_retain,final_replace)]

        for pairs in mappings:
          for i in njson['links']:
              if i['source'] == pairs[1]:
                  i['source'] = pairs[0]
              if i['target'] == pairs[1]:
                  i['target'] = pairs[0]
        
        print("B")
        l = []

        for i in njson["links"]:
          l.append(i.get("source"))
          l.append(i.get("target"))
          
        
        edges = []
        
        for i in njson['links']:
            edges.append([i['label'],i['source'],i['target']])
            
        new_links = []
        
        for i in edges:
            l,s,d = i[0],i[1],i[2]
            new_links.append({'label':l,'source':s,'target':d})
        
        njson['links'] = new_links
        
        # 2. Create Pydot graph object
        pydot_graph = pydot.Dot(graph_type='digraph')
        
        garbage_nodes = []
        print("C")
        for node in njson['nodes']:
            try:
                name = node.get("CODE")
                pydot_graph.add_node(pydot.Node(name, label=node['label'], CODE=node['CODE']))         
            except:
                garbage_nodes.append([node.get("id"),node.get("CODE")])

        print("D")
        for edge in njson['links']:
        
            nodes_src = dot.get_node(edge['source'])[0]
            nodes_dest = dot.get_node(edge['target'])[0]  
            new_src = nodes_src.get_attributes().get("CODE")
            new_dest =  nodes_dest.get_attributes().get("CODE")
            pydot_graph.add_edge(pydot.Edge(new_src, new_dest, label=edge['label']))
        print("E")            
        if save_output: 
            # 4. Save Pydot graph object to DOT file
            pydot_graph.write_raw('final.dot')    
        print(f'pydot_graph type: {type(pydot_graph)}')
        return pydot_graph


        
    