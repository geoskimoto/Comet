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
import cv2
from glob import glob
import numpy as np
import pandas as pd
import sklearn

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

if __name__ == "__main__":


	# <-- MODEL --> 
	# Common Layers
	input_layer = Input((224,224,1))
	first_conv1 = Conv2D(64, (3,3), activation="relu")(input_layer)
	first_conv2 = Conv2D(64, (3,3), activation="relu")(first_conv1)
	max_pool1 = MaxPool2D((2,2))(first_conv2)
	second_conv1 = Conv2D(128, (3,3), activation="relu")(max_pool1)
	second_conv2 = Conv2D(128, (3,3), activation="relu")(second_conv1)
	max_pool2 = MaxPool2D((2,2))(second_conv2)
	third_conv1 = Conv2D(256,(3,3), activation="relu")(max_pool2)
	third_conv2 = Conv2D(256,(3,3), activation="relu")(third_conv1)
	max_pool3 = MaxPool2D((2,2))(third_conv2)
	flatten_layer = Flatten()(max_pool3)
	last_second_layer = Dense(2048, activation="relu")(flatten_layer)
	one_last_layer = Dense(1024, activation="relu")(last_second_layer)
	output_layer = Dense(128, activation="relu")(one_last_layer)

	embeddings_model = Model(input_layer, output_layer)

	# Model specific inputs
	diff_input = Input((224,224,1))
	message_input = Input((224,224,1))

	# Model specific initialization
	diff_model = embeddings_model(diff_input)
	message_model = embeddings_model(message_input)

	# Merge layer
	merge_layer = Lambda(euclidean_distance)([diff_model,message_model])

	# Output layer
	output_layer = Dense(1, activation="sigmoid")(merge_layer)

	# Siamese Model
	siamese = Model(inputs=[diff_input, message_input], outputs=output_layer)


	# Add the weights file name here
	siamese.load_weights("final_weights.h5", skip_mismatch=False, by_name=False, options=None)


	pred_one = [np.load(x) for x in sorted(glob("embeddings_pred1_final/*"))]
	pred_two = [np.load(x) for x in sorted(glob("embeddings_pred2_final/*"))]
	pred_three = [np.load(x) for x in sorted(glob("embeddings_pred3_final/*"))]
	#pred_four = [np.load(x) for x in sorted(glob("embeddings_pred4_final/*"))]
	#pred_five = [np.load(x) for x in sorted(glob("embeddings_pred5_final/*"))]

	assert len(pred_one) == len(pred_two) == len(pred_three)

	pred_one_res = np.array([cv2.resize(c, (224, 224)) for c in pred_one])
	pred_two_res = np.array([cv2.resize(c, (224, 224)) for c in pred_two])
	pred_three_res = np.array([cv2.resize(c, (224, 224)) for c in pred_three])
	#pred_four_res = np.array([cv2.resize(c, (224, 224)) for c in pred_four])
	#pred_five_res = np.array([cv2.resize(c, (224, 224)) for c in pred_five])
	code = np.array([np.load(x) for x in sorted(glob("code/*"))])

	print("_____SHAPES HERE_________")
	print(code[0].shape)
	print(pred_one_res[0].shape)
	print("_______CHECK FOR THE END OF THE SHAPES_______")

	results1 = siamese.predict([code,pred_one_res])
	results2 = siamese.predict([code,pred_two_res])
	results3 = siamese.predict([code,pred_three_res])
	#results4 = siamese.predict([code,pred_four_res])
	#results5 = siamese.predict([code,pred_five_res])

	final_results = []

	np.random.seed(90)
	for i,j,z in zip(results1,results2,results3):
	    final_results.append(np.argmax(np.array([i[0],j[0],z[0]])))
	    print(np.array([i[0],j[0],z[0]]))

	df = pd.DataFrame(final_results,columns=["predicitons"])

	df["predicitons"] = final_results

	print(df["predicitons"].value_counts())

	df.to_csv("pred_new.csv",index=False)

