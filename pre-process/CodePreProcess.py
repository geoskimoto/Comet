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
import time 
import pathlib
from utils import ensure_file_permissions, ensure_folder_permissions, delete_folder
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
        print('combining dots... (Im in CodePreProcess.py)')
        # print(f'folder_name: {folder_name}')
        # print(f'return_name: {return_name}')
        dots = sorted(glob(folder_name+"/*"))
        # print(f'dots: {dots}')
        jsons = []
        
        for d in dots:
            try:
                # print(f'd: {d}')
                dgs = pydot.graph_from_dot_file(d)[0]
                jsons.append(self.dot_to_json(dgs))
            except Exception as e:
                print("loop failed in .combine_dots.  I'm in CodePreProcess.py")
                print(e)
                pass
        try:
            combined_json = self.combine_json(jsons)
        except Exception as e:
            print(f"combined_json = self.combine_json(jsons) failed.  I'm in CodePreProcess.py")

        try:
            combined_dot = self.initial_dot(combined_json)
        except Exception as e:
            print("combined_dot = self.initial_dot(combined_json) failed.  I'm in CodePreProcess.py")
        
        shutil.rmtree(folder_name)
        
        write_path = return_name+".dot"
        
        if os.path.exists("cpg.bin"):
            os.remove("cpg.bin")
            
        combined_dot.write_raw(write_path)
        
        return write_path
                
    


    def process(self, file_path, name):
                
        class_list = sorted(glob(file_path + "/*"))
        counter = 0
        

        # Clean up the 'singleDot' and 'dots' folders before processing
        # delete_folder('singleDot')
        os.makedirs('singleDot', exist_ok=True)
        ensure_folder_permissions('singleDot')
        # delete_folder('dots')
        
        for index in range(len(class_list)):
            print(f'Starting joern-parse for {class_list[index]}...')
            
            
            # Usage: joern-parse [options] [input]

            #   input                  source file or directory containing source files
            #   -o, --output <value>   output filename
            #   --language <value>     source language
            #   --list-languages       list available language options
            #   --namespaces <value>   namespaces to include: comma separated string
            # Overlay application stage
            #   --nooverlays           do not apply default overlays
            #   --overlaysonly         Only apply default overlays
            #   --max-num-def <value>  Maximum number of definitions in per-method data flow calculation
            # Misc
            #   --help                 display this help message
            # Args specified after the --frontend-args separator will be passed to the front-end verbatim


            print(f'class to be parsed: {class_list[index]}')
            parse_command = [
                "joern-parse", 
                class_list[index],
                # "--language",
                # "python"
                ]
            subprocess.run(parse_command, check=True)
            print('joern-parse finished')
            #have to delete dots from previous iteration or else joern-export will throw a fit.
            print('Deleting the dots/ directory from previous iteration.')
            delete_folder('dots')
            delete_folder('out') #this folder is being created for some reason by joern-export and also crashes 
            delete_folder('singleDot')
            # print('Recreating dots/ directory.')  # doesn't work...even an empty dots folder will make joern-export fail.
            # os.makedirs('dots', exist_ok=True)
            print(f'Starting joern-export.  This should grab the cpg.bin in pre-process/ and export it as a .dot file to /dots.')

            
            
            # Usage: joern-export [options] [cpg]
            #   --help
            #   cpg                input CPG file name - defaults to `cpg.bin`
            #   -o, --out <value>  output directory - will be created and must not yet exist
            #   --repr <value>     representation to extract: [all|ast|cdg|cfg|cpg|cpg14|ddg|pdg] - defaults to `Cpg14`
            #   --format <value>   export format, one of [dot|graphml|graphson|neo4jcsv] - defaults to `Dot`
            print(f'Current working directory {os.getcwd()}')
            
            ensure_file_permissions("/home/mrguy/Projects/comet/Comet/pre-process/cpg.bin")
            
            cpg_path = "/home/mrguy/Projects/comet/Comet/pre-process/cpg.bin"
            output_dir = "/home/mrguy/Projects/comet/Comet/pre-process/dots"

            # Make sure the output directory does not already exist
            if os.path.exists(output_dir):
                print(f"Error: Output directory {output_dir} already exists. Joern requires a non-existent directory.")
                exit(1)

            #this worked in the command line!  joern-export cpg.bin --out "dots"
            # Need to replicate that here:
            print(f'cwd: {os.getcwd()}')
            export_command = [
                "joern-export",
                "cpg.bin",
                "--out", "dots"
            ]
            # export_command = [
            #     "joern-export",
            #     "cpg.bin"
            #     "--out", output_dir   
            #     # "--repr", "cpg",
            #     # "--format", "dot",
            #     # cpg_path               # CPG file should be last
            # ]

            try:
                subprocess.run(export_command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running Joern: {e}")
            
            print('joern-export finished')


            dot_files = sorted(glob("dots/*.dot"))
            # print(f'dot_files in dots/: {dot_files}')
            print(f'Number of dot_files: {len(dot_files)}')

            if not dot_files:  # If the list is empty
                print("Warning: dot_files is not correct, or no .dot files were created.")
                print(dot_files)
            # else:
                # print(f'dot_files: {dot_files}')
                # print(f'Number of dot_files: {len(dot_files)}')

            # Ensure 'singleDot' directory exists
            os.makedirs("singleDot", exist_ok=True)

            counter = 1  # Initialize counter

            # Rename and move files to 'singleDot' folder
            for path_index in range(len(dot_files)):  # Process all files
                # print(f'path_index: {path_index}')
                base_name, extension = os.path.splitext(dot_files[path_index])
                new_name = f"{base_name}_ren{counter}{extension}"
                os.rename(dot_files[path_index], new_name)
                shutil.move(new_name, "singleDot")
                counter += 1

            # dot_files = sorted(glob("dots/*.dot"))
            # print(f'dot_files in dots/ :  {dot_files})
            # # dot_file_path = sorted(glob(output_dir + "/" + class_list[index] + "/*"))
            # print(f'dot_files: {dot_files}.')
            # if not dot_files:  # If the list is empty
            #     print("Warning: dot_files is not correct, or no .dot files were created for", class_list[index])
            #     print(dot_files)
            #     continue  # Skip processing this class
            # else:
            #     print(f'dot_files: {dot_files}')
            #     print(dot_files)
            
            # # Rename and move files to 'singleDot' folder
            # for path_index in range(1, len(dot_files)):
            #     print(f'path_index: {path_index}')
            #     base_name, extension = os.path.splitext(dot_files[path_index])
            #     new_name = f"{base_name}_ren{counter}{extension}"
            #     os.rename(dot_files[path_index], new_name)
            #     shutil.move(new_name, "singleDot")
            #     counter += 1
            
            # Clean up 'dots' folder after processing the current class
            # print('deleting dots folder...')
            # delete_folder('dots')
            # print('dots folder successfully deleted')

        # Combine the files in 'singleDot' after processing all classes
        if len(class_list) > 0:
            print('combining dot files in singleDot')
            path = self.combine_dots("singleDot", name)
            print(f'self.combine_dots ran to completion. path: {path}')
            return path

                
                
                
                            
                
                
            
                    
                