import numpy as np
import pandas as pd
import sklearn
from glob import glob
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.layers import Input, Dense, Flatten, Conv2D, MaxPool2D, Lambda
from keras.models import Model, Sequential
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as k
from keras.callbacks import EarlyStopping
from keras.applications.vgg16 import VGG16

from glob import glob
import numpy as np
import pandas as pd
import sklearn

# Eucledian distance
def euclidean_distance(vects):
    """Find the Euclidean distance between two vectors.

    Arguments:
        vects: List containing two tensors of same length.

    Returns:
        Tensor containing euclidean distance
        (as floating point value) between vectors.
    """

    x, y = vects
    sum_square = tf.math.reduce_sum(tf.math.square(x - y), axis=1, keepdims=True)
    return tf.math.sqrt(tf.math.maximum(sum_square, tf.keras.backend.epsilon()))


# Loss function
# Loss function 
def loss(margin=1):
    """Provides 'constrastive_loss' an enclosing scope with variable 'margin'.

    Arguments:
        margin: Integer, defines the baseline for distance for which pairs
                should be classified as dissimilar. - (default is 1).

    Returns:
        'constrastive_loss' function with data ('margin') attached.
    """

    # Contrastive loss = mean( (1-true_value) * square(prediction) +
    #                         true_value * square( max(margin-prediction, 0) ))
    def contrastive_loss(y_true, y_pred):
        """Calculates the constrastive loss.

        Arguments:
            y_true: List of labels, each label is of type float32.
            y_pred: List of predictions of same length as of y_true,
                    each label is of type float32.

        Returns:
            A tensor containing constrastive loss as floating point value.
        """

        square_pred = tf.math.square(y_pred)
        margin_square = tf.math.square(tf.math.maximum(margin - (y_pred), 0))
        return tf.math.reduce_mean(
            (1 - y_true) * square_pred + (y_true) * margin_square
        )

    return contrastive_loss



#!/usr/bin/python
# -*- coding: utf-8 -*-
if __name__ == '__main__':

    code = [np.load(x) for x in sorted(glob('new_final_data/code/*'))]
    neg = [np.load(x) for x in sorted(glob('new_final_data/neg_samples/*'))]
    pos = [np.load(x) for x in sorted(glob('new_final_data/text_pos/*'))]
    long_code = code + code
    long_samp = neg + pos
    x_pairs = np.array([np.array([d, m]) for (d, m) in zip(long_code,long_samp)])
    
    y_ = [*list(np.zeros(len(neg))),*list(np.ones(len(pos)))]
    y_labels = np.array(y_)

    y_labels = y_labels.astype('float64')

    # Train-test split

    (train_X, test_X, train_y, test_y) = train_test_split(x_pairs,y_labels, test_size=0.15, random_state=101, shuffle=True)


	# <-- MODEL --> 
	# Common Layers
    input_layer = Input((224, 224, 1))
    first_conv1 = Conv2D(64, (3, 3), activation='relu')(input_layer)
    first_conv2 = Conv2D(64, (3, 3), activation='relu')(first_conv1)
    max_pool1 = MaxPool2D((2, 2))(first_conv2)
    second_conv1 = Conv2D(128, (3, 3), activation='relu')(max_pool1)
    second_conv2 = Conv2D(128, (3, 3), activation='relu')(second_conv1)
    max_pool2 = MaxPool2D((2, 2))(second_conv2)
    third_conv1 = Conv2D(256, (3, 3), activation='relu')(max_pool2)
    third_conv2 = Conv2D(256, (3, 3), activation='relu')(third_conv1)
    max_pool3 = MaxPool2D((2, 2))(third_conv2)
    flatten_layer = Flatten()(max_pool3)
    last_second_layer = Dense(2048, activation='relu')(flatten_layer)
    one_last_layer = Dense(1024, activation='relu')(last_second_layer)
    output_layer = Dense(128, activation='relu')(one_last_layer)

    embeddings_model = Model(input_layer, output_layer)

    # Model specific inputs

    diff_input = Input((224, 224, 1))
    message_input = Input((224, 224, 1))

    # Model specific initialization

    diff_model = embeddings_model(diff_input)
    message_model = embeddings_model(message_input)

    # Merge layer

    merge_layer = Lambda(euclidean_distance)([diff_model,
            message_model])

    # Output layer

    output_layer = Dense(1, activation='sigmoid')(merge_layer)

    # Siamese Model

    siamese = Model(inputs=[diff_input, message_input],
                    outputs=output_layer)

    stop_call = EarlyStopping(monitor='val_loss', patience=4)

    siamese.compile(optimizer="adam", loss=loss(margin=1),
                    metrics='accuracy')

    siamese.fit(
        x=[train_X[:, 0, :, :], train_X[:, 1, :, :]],
        y=train_y,
        validation_data=([test_X[:, 0, :, :], test_X[:, 1, :, :]],
                         test_y),
        epochs=7,
        batch_size=16,
        callbacks=[stop_call],
        )

    siamese.save_weights("final_weights.h5", overwrite=True, save_format=None, options=None)