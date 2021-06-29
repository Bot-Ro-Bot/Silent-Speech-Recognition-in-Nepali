import os
import glob
import numpy as np
from emg_lib import *
MAIN_DIR = "."
if os.path.basename(os.getcwd())!="Silent-Interface-for-IOT-Devices":
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

testfiles = glob.glob(TEST_DATA_DIR+"/[A|B].txt", recursive=True) 
print("The files in the dataset: ",(testfiles))
rawdata = parser(testfiles, NORMALIZE=True, utteranceCountPerFile=10)
print(rawdata['data'][0].shape)

all_data_filtered = rawdata.copy()
all_data_filtered['data'] = signal_pipeline(rawdata['data'])
del rawdata
print(all_data_filtered['data'][0].shape)

all_data_featured = all_data_filtered.copy()
all_data_featured['data'] = feature_pipeline_melspectrogram(all_data_filtered['data'])
del all_data_filtered
print(all_data_featured['data'][0].shape)
all_data_featured = reshapeChannelIndexToLast(all_data_featured)
print(all_data_featured['data'][0].shape)


# import tensorflow as tf
# from tensorflow import keras
# model = tf.keras.models.load_model('../models/model_CNN2d_3_o.h5')
# model.summary()