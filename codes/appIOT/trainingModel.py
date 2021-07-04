import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from emg_lib import *
MAIN_DIR = "."
while os.path.basename(os.getcwd())!="Silent-Interface-for-IOT-Devices":
    os.chdir("..")
# print("from trainedModel file : ", os.getcwd())
# print("test only : ", getDir())

DATA_DIR = os.path.join(MAIN_DIR,"new dataset")
TEST_DATA_DIR = os.path.join(MAIN_DIR, "test")
FIG_DIR = os.path.join(MAIN_DIR,"figures")
PICKLE_DIR = os.path.join(MAIN_DIR,"pickles")
os.makedirs(FIG_DIR,exist_ok=True)
os.makedirs(PICKLE_DIR,exist_ok=True)

# hardware definitions
"""
https://docs.openbci.com/docs/02Cyton/CytonDataFormat#:~:text=By%20default%2C%20our%20Arduino%20sketch,of%200.02235%20microVolts%20per%20count
"""
SAMPLING_RATE = 250 #Hz
NUM_CHANNELS = 8 
ADC_RESOLUTION = 24 #bits
ADC_GAIN = 24.0
REF_VOLTAGE = 4.5 #Volts
SCALE_FACTOR = (REF_VOLTAGE/float((pow(2,23))-1)/ADC_GAIN)*1000000.0 #micro-volts

# dataset definitions
SPEAKER = ["RL","RN","SR","US"]
SESSION = ["session"+str(i) for i in range(1,9)]
SENTENCES =["अबको समय सुनाउ","एउटा सङ्गित बजाउ","आजको मौसम बताउ","बत्तिको अवस्था बदल","पङ्खाको स्तिथी बदल"]
LABELS = np.array(SENTENCES)[[3, 2, 1, 4, 0, 3, 2, 1, 4, 0, 3, 2, 1, 4, 0]]
label_sets = list(set(SENTENCES))

all_data_feature = getPickleFile('data_dict_melspectrogram.pickle')
X = all_data_feature['data']
Y = all_data_feature['labels']
del all_data_feature

#split dataset
from sklearn.preprocessing import LabelEncoder
labelencoder_y = LabelEncoder()
Y_encode = labelencoder_y.fit_transform(Y)
# Y_encode = Y_encode.reshape((len(Y_encode), 1))

from sklearn.model_selection import StratifiedShuffleSplit
def train_test_split(X, Y, verbose=False):
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_id, test_id = next(split.split(X, Y))
    if verbose:
        print("train set shape: ", X[train_id].shape)
        print("test set shape: 	", X[test_id].shape)
    return 	X[train_id], Y[train_id], X[test_id], Y[test_id]

X_train, Y_train, X_test, Y_test = train_test_split(X, Y_encode, True)

# train model
# cnn 2d classifier 
import tensorflow as tf
from tensorflow import keras
num_label = len(SENTENCES)
# Y_train = tf.keras.utils.to_categorical(Y_train, num_classes = num_label)
# Y_test = tf.keras.utils.to_categorical(Y_test, num_classes = num_label)

print(type(Y_train))
print(Y_train[:5])
print(set(Y_train))

def CNN_2d_Classifier(X_train, Y_train, X_test, Y_test):
    # Y_train = tf.keras.utils.to_categorical(Y_train, num_classes = num_label)
    # Y_test = tf.keras.utils.to_categorical(Y_test, num_classes = num_label)
    CNN_model = keras.Sequential()
    CNN_model.add(keras.layers.Conv2D(64, kernel_size = (2, 3), input_shape = X_train.shape[1:], activation = "relu"))
    CNN_model.add(keras.layers.MaxPool2D(pool_size=(1, 3) ))
    CNN_model.add(keras.layers.BatchNormalization() )
    
    CNN_model.add(keras.layers.Conv2D(128, kernel_size = (1, 3), input_shape = X_train.shape[1:], activation = "relu"))
    CNN_model.add(keras.layers.MaxPool2D(pool_size=(1, 3) ))
    CNN_model.add(keras.layers.BatchNormalization() )
    
    CNN_model.add(keras.layers.Conv2D(512,kernel_size=(1 , 3),activation="relu"))
    CNN_model.add(keras.layers.MaxPool2D(pool_size=(1, 3) ))
    CNN_model.add(keras.layers.BatchNormalization())
    
    CNN_model.add(keras.layers.Flatten())
    CNN_model.add(keras.layers.Dense(100,activation="relu"))
    CNN_model.add(keras.layers.Dropout(0.25))
    CNN_model.add(keras.layers.Dense(num_label,activation="softmax"))

    opt = keras.optimizers.Adam(lr = 0.0001)
    # opt = keras.optimizers.SGD(learning_rate = 0.0001, momentum = 0.9, nesterov = False)
    CNN_model.compile(optimizer = opt, loss = keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'])
    print(CNN_model.summary())

    history = CNN_model.fit(X_train, Y_train, epochs = 10, batch_size = 32, validation_data =(X_test, Y_test) ,verbose = 1)

    CNN_prediction = CNN_model.predict_classes(X_test)

    # confusion_matrix_plt(Y_test, CNN_prediction, label_sets)

    #save model
    CNN_model.save('./models/modelCNN.h5')

    # max_val_acc = max(history.history['accuracy'])
    # print(max_val_acc) #['loss', 'acc']

    print(list(history.history.keys()))
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model acc')
    plt.legend([ 'training_acc','validation_acc'])
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.show()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.legend(['training_loss','validation_loss'])
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.show()

    pred = CNN_model.predict_classes(X_final_test)
    print(pred)
    print(list(labelencoder_y.inverse_transform(list(pred))))

    return CNN_model.evaluate(X_test, Y_test)[1]

print("CNN :",CNN_2d_Classifier(X_train, Y_train, X_test, Y_test))
#'''