#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 15:32:09 2023

@author: abhinav
"""

import subprocess
import os
import json

class Extract_json:
    
    def __init__(self, dot_file_input):
        self.dot_file_input = dot_file_input
        
    
    def get_json(self):
        
        directory = "json"
        
        if os.path.exists(directory)==False:
            os.mkdir(directory)

        command = ["dot", "-Txdot_json", "-o", directory+"/graph.json", self.dot_file_input]
        
        subprocess.run(command, check=True)
        
        file = open(command[3])
        
        data = json.load(file)
        
        return data
    
    def get_json_path(self):
        
        directory = "json"
        
        if os.path.exists(directory)==False:
            os.mkdir(directory)

        command = ["dot", "-Txdot_json", "-o", directory+"/graph.json", self.dot_file_input]
        
        subprocess.run(command, check=True)
        
        return command[3]
        