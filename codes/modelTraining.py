import os
import glob 
import pickle 
import biosppy
import librosa
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt	
import librosa.display as display


from scipy import signal 
from scipy.fftpack import fft
from scipy.stats import zscore
from scipy.fft import fft, fftfreq

from EMGProcessing import *

import matplotlib as mlp 
mlp.rc("xtick", labelsize=10)
mlp.rc("ytick", labelsize=10)
mlp.rc("axes", labelsize=11)
plt.rcParams["figure.figsize"] = [11, 5]
plt.rcParams["figure.dpi"] = 300

CURR_DIR = os.getcwd()

# necessary definitions
# directories definitions
MAIN_DIR = '.'
if os.path.basename(os.getcwd()) != "Silent-Interface-for-IOT-Devices":
	os.chdir("..")

DATA_DIR = os.path.join(MAIN_DIR, "dataset")
NEW_DATA_DIR = os.path.join(MAIN_DIR, "new dataset")
FIG_DIR = os.path.join(MAIN_DIR, "figures")
PICKLE_DIR = os.path.join(MAIN_DIR, "pickles")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(PICKLE_DIR, exist_ok=True)

#hardware definitions
SAMPLING_RATE = 250	#Hz
NUM_CHANNELS = 8	
ADC_RESOULTION  = 24 #bits
ADC_GAIN = 24.0
REF_VOLTAGE = 4.5 #volts
SCALE_FACTOR = (REF_VOLTAGE / float(2**23 - 1) / ADC_GAIN )*1000000.0 #micro-volts

# dataset definitions
SPEAKER = ["RL","RN","SR","US"]
SESSION = ["session1","session2","session3"]
MODE = ["mentally","mouthed","audible"]
SENTENCES =["अबको समय सुनाउ","एउटा सङ्गित बजाउ","आजको मौसम बताउ","बत्तिको अवस्था बदल","पङ्खाको स्तिथी बदल"]
WORDS = ["समय","सङ्गित","मौसम","बत्ति","पङ्खा"]


SENTENCE_LABEL= np.array(SENTENCES)[[0,1,2,0,3,1,0,3,0,0,1,1,3,3,4,4,2,3,1,2,2,2,4,4,4]]
WORD_LABEL= np.array(WORDS)[[4,0,3,1,0,1,1,0,4,0,3,2,4,4,2,1,4,1,2,2,2,0,3,3,3]]
NEW_LABEL = np.array(SENTENCES)[[3, 2, 1, 4, 0, 3, 2, 1, 4, 0, 3, 2, 1, 4, 0]]

LABELS = {"word":WORD_LABEL,"sentence":SENTENCE_LABEL}

# a function to save plotted figures
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
	path = os.path.join(FIG_DIR, fig_id + "." + fig_extension)
	print("Saving figure", fig_id)
	if tight_layout:
		plt.tight_layout()
	plt.savefig(path, format=fig_extension, dpi=resolution)


#data access : exported from ipynb.
df_pickleDataFile = 'new_data_dict_dataframe_preprocess.pickle'
if df_pickleDataFile in os.listdir(PICKLE_DIR):
    df = pd.read_pickle(os.path.join(PICKLE_DIR,  df_pickleDataFile))
print(df.info())

print(df["data"].iloc[1])
plt.plot(df["data"].iloc[1])
plt.show()
#preprocessing
dataPreprocessed = True
if not dataPreprocessed:
	for dataIndex in range(len(df["data"].iloc[:])):
		df["data"].iloc[dataIndex] = preprocess_data(df["data"].iloc[dataIndex])

#feature extraction


#split dataset

# train model

# test model 



