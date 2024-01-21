#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 20:53:29 2023

@author: anonymous

Credits : https://towardsdatascience.com/natural-language-processing-dependency-parsing-cf094bbbe3f7
"""
from nltk.parse.stanford import StanfordDependencyParser
import pydot 

class TextParser:
    def __init__(self, sentence):
        self.sentence = sentence
                # Path to CoreNLP jar unzipped
        self.jar_path = 'stanford-corenlp-4.5.2/stanford-corenlp-4.5.2.jar'
        
        # Path to CoreNLP model jar
        self.models_jar_path = 'stanford-corenlp-4.5.2/stanford-corenlp-4.5.2-models.jar'
    
    def get_parsed_dot(self):
                      
        # Initialize StanfordDependency Parser from the path
        parser = StanfordDependencyParser(path_to_jar = self.jar_path, path_to_models_jar = self.models_jar_path)
        
        # Parse the sentence
        result = parser.raw_parse(self.sentence)
        dependency = result.__next__()
                
        dot_def = dependency.to_dot()
        
        graph = pydot.graph_from_dot_data(dot_def)[0]
        
        return graph