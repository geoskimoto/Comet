#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 21:44:38 2023

@author: abhinav
"""

from glob import glob
import subprocess
import os 
import shutil 
import pydot 

class CodePreProcess:
    
    def __init__(self):
        
        pass
    
    def dot_to_json(self, graph):

      nodes = [{"id":x.get_name() , "CODE":x.get_attributes().get("CODE"), "label":x.get_attributes().get('label')} for x in graph.get_nodes()]
    
      edges = [{"source":graph.get_node(x.get_source())[0].get_name(), "target":graph.get_node(x.get_destination())[0].get_name(), "label":x.get_label()} for x in graph.get_edges()]
    
      graph_ = {"name":"G", 'nodes':nodes, "links":edges}
    
      return graph_
    
    def combine_json(self,jsons):
        
      for index in range(1,len(jsons)):
        jsons[0]['nodes'] += jsons[index]['nodes']
        jsons[0]['links'] += jsons[index]['links']
    
      return jsons[0]
  
    def initial_dot(self, jsons):
      # 2. Create Pydot graph object
      pydot_graph = pydot.Dot(graph_type='graph')
    
      for node in jsons['nodes']:
          pydot_graph.add_node(pydot.Node(node.get("id"), label=node.get("label"), CODE=node.get("CODE")))
    
      for edge in jsons['links']:
          pydot_graph.add_edge(pydot.Edge(edge.get("source"),edge.get("target"), label=edge.get("label")))

      return pydot_graph
  
    def combine_dots(self, folder_name, return_name):
        
        dots = sorted(glob(folder_name+"/*"))
        
        jsons = []
        
        for d in dots:
            try:
                dgs = pydot.graph_from_dot_file(d)[0]
                jsons.append(self.dot_to_json(dgs))
            except:
                pass
        
        combined_json = self.combine_json(jsons)
        
        combined_dot = self.initial_dot(combined_json)
        
        
        shutil.rmtree(folder_name)
        
        write_path = return_name+".dot"
        
        if os.path.exists("cpg.bin"):
            os.remove("cpg.bin")
            
        combined_dot.write_raw(write_path)
        
        return write_path
                
    
    def process(self,file_path, name):
        
        print("Processing :" + name)
                
        class_list = sorted(glob(file_path+"/*"))
        counter = 0
        
        
        os.makedirs("singleDot",exist_ok=True)
                
        for index in range(len(class_list)):

            parse_command1 = ["joern-parse", class_list[index]]
            subprocess.run(parse_command1, check=True)
            
            export_command1 = ["joern-export","--out","dots","--repr","cpg","--format","dot"]
            subprocess.run(export_command1, check=True)
            
            dot_file_path = sorted(glob("dots/"+class_list[index]+"/*"))
            
                                    
            for path_index in range(1,len(dot_file_path)):
                
#               os.rename(dot_file_path[path_index], dot_file_path[path_index]+str(counter))
                
                                
                base_name, extension = os.path.splitext(dot_file_path[path_index])
                
                new_name = base_name +"ren"+str(counter) + extension
                                
                os.rename(dot_file_path[path_index], new_name)
                
                shutil.move(new_name, "singleDot")
               
                counter +=1

            # Not working
            shutil.rmtree("dots")
            
            if index == len(class_list)-1:
                
                path = self.combine_dots("singleDot", name)
                
                counter = 0
                return path
                

            
            
            
                        
            
            
        
                
            