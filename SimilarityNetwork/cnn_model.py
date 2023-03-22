#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 21:35:21 2023

@author: abhinav
"""

import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.layers import Input, Dense, Flatten, Conv2D, MaxPool2D, Lambda
from keras.models import Model, Sequential
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as k

