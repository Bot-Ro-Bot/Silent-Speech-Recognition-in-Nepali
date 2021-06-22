
import tensorflow as tf
from tensorflow import keras
model = tf.keras.models.load_model('../models/model_CNN2d_3_o.h5')
model.summary()