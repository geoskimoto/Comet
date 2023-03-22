#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 20:32:32 2023

@author: abhinav
"""

import tensorflow 
from tensorflow import keras 
from tensorflow.keras.models import load_model 


class Siamese:
    
    def __init__(self, vector1, vector2, model_path):
        
        self.vector1 = vector1
        self.vector2 = vector2
        self.model_path = model_path

    def get_similarity(self):
        
        model = load_model(self.model_path, compile=False)
        
        
        similarity = model.predict([self.vector1, self.vector2])
        
        return similarity
    
    
    
        
        
        
        
        
        
        
        