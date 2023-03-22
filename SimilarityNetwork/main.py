#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 21:07:41 2023

@author: abhinav
"""

import numpy as np
import siamese
import tensorflow

def main():
    
    model_path = "models/siamese.h5"
    
    vec1 = np.random.randn(1,200,200,1)
    vec2 = np.random.randn(1,200,200,1)
    
    model = siamese.Siamese(vec1, vec2, model_path)
    
    similarity = model.get_similarity()
    
    return similarity

if __name__ == "__main__":
    
    print(tensorflow.__version__)
  
    score = main()
    
    print(score[0])
   
   