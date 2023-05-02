#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 02:34:29 2023

@author: abhinav
"""

import subprocess

class Cpg:
    
    def __init__(self, input_path_1, input_path_2):
        self.input_path_1 = input_path_1
        self.input_path_2 = input_path_2

    def get_dot(self):
        
        out_file1, out_file2 = "cpg1.bin" , "cpg2.bin"
        
        """CODE TO .BIN FILES"""
        # Parsing previous code
        parse_command1 = ["joern-parse", self.input_path_1, "--output", out_file1]
        subprocess.run(parse_command1, check=True)
        
        # Parsing new code
        parse_command2= ["joern-parse", self.input_path_2, "--output", out_file2]
        subprocess.run(parse_command2, check=True)
        
        
        """.BIN FILES TO DOT FILES"""
        export_command1 = ["joern-export",out_file1,"--out","code1","--repr","cpg","--format","dot"]
        subprocess.run(export_command1, check=True)
        
        export_command2 = ["joern-export",out_file2,"--out","code2","--repr","cpg","--format","dot"]
        subprocess.run(export_command2, check=True)
        
        
        path1 = "code1/"+ self.input_path_1+"/myMethod.dot"
        path2 = "code2/"+ self.input_path_2+"/myMethod.dot"
        
        return path1, path2
        
