import numpy as np 
import os
import glob
import pickle
from tqdm import tqdm
from scipy.signal import spectrogram, windows


SAMPLING_RATE = 250
NUM_CHANNELS = 8
CURR_DIR = os.getcwd()
MAIN_DIR = "."
if os.path.basename(os.getcwd())!="Silent-Interface-for-IOT-Devices":
    os.chdir("..")
PICKLE_DIR = os.path.join(MAIN_DIR,"pickles")


# ========== IMPORT FILTERED PICKLE DATA =================
Picklefile = "data_dict_filtered_aug.pickle"
if Picklefile in os.listdir(PICKLE_DIR):
    all_data = pickle.load(open(os.path.join(PICKLE_DIR,Picklefile),"rb"))
    print("-------Read Task Accomplished----------")

print(all_data["data"].shape)
print(all_data.keys())
# print(type(all_data["labels"]))



# ============= FEATURE EXTRACTION (SPECTROGRAM) ==============

''' NOTE: 
	We need to optimize between spectral leakage and spectral resolution. In order to increase spectral resolution 
	for a given accepted leakage level we can increase the window length which decreases the time localization of the STFT.
	To accomadate for this latter side effect, we can use overlapping windows so that the next window does not start from 
	the end of the current window, but begins somewhere in the middle. We also need to satisfy COLA constraint to ensure that succesive frames 
	will overlap in time s.t. all data are equally weighted. But increasing nfft and noverlap requires more computation
'''

def feature_pipeline(data):
    feature_data = []
    def getSpect(sdata):
        M = 60
        win = windows.hann(M, sym=False)
        return spectrogram(x=np.array(sdata), fs=SAMPLING_RATE, window=win, nperseg=M, noverlap=3*M/4, nfft=M)
    def process_signal(data):
        f_data = []
        for i in range(8):
            _, _, c_data = getSpect(data[:, i])
            f_data.append(c_data)
        return np.array(f_data)
    
    for d,i in zip(data, tqdm(range(1,len(data)+1),desc="EXTRACTING DATA: ")):
        temp_data = process_signal(d)
        feature_data.extend([temp_data])
    return np.array(feature_data)


fileToImport = "data_dict_sfeature_aug1.pickle"
if fileToImport in os.listdir(PICKLE_DIR):
    print("Fetching feature data from pickle file ...")
    all_data_feature = pickle.load(open(os.path.join(PICKLE_DIR, fileToImport),"rb"))
    print("Done!")
else:
    all_data_feature = all_data.copy()
    all_data_feature["data"] = feature_pipeline(all_data["data"])
    pickle.dump(all_data_feature,open(os.path.join(PICKLE_DIR, fileToImport),"wb"))
    print("Write Task Completed")