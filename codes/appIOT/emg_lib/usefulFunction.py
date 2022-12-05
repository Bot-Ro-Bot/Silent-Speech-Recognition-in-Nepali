import os 
import numpy as np
import pickle

MAIN_DIR = "."
while os.path.basename(os.getcwd())!="Silent-Interface-for-IOT-Devices":
    os.chdir("..")
PICKLE_DIR = os.path.join(MAIN_DIR,"pickles")
FONT_DIR = [os.path.join(MAIN_DIR,"fonts")]

print("from font ", FONT_DIR)

#TODO : rename this file later
def reshapeChannelIndexToLast(data_feature):
    if type(data_feature) == dict:
        reshape_feature = np.zeros((data_feature['data'].shape[0], data_feature['data'].shape[2],
                            data_feature['data'].shape[3], data_feature['data'].shape[1]))
        for i in range(data_feature['data'].shape[0]):
            for j in range(8):
                reshape_feature[i,:,:,j] = data_feature['data'][i,j,:,:]
        data_feature['data'] = reshape_feature
    else :
        reshape_feature = np.zeros((data_feature.shape[0], data_feature.shape[2],
                            data_feature.shape[3], data_feature.shape[1]))
        for i in range(data_feature.shape[0]):
            for j in range(8):
                reshape_feature[i,:,:,j] = data_feature[i,j,:,:]
        data_feature = reshape_feature

    return data_feature

#confusion matrix
# TODO : remove the addfont method error
# import matplotlib.pyplot as plt
# from matplotlib import font_manager
# font_files = font_manager.findSystemFonts(fontpaths=FONT_DIR)
# for font_file in font_files:
#     font_manager.fontManager.addfont(font_file)

# # set font
# plt.rcParams['font.family'] = 'mangal'

from sklearn.metrics import confusion_matrix
def confusion_matrix_plt(y_value , pred_value, labels, normalize = None):
    print(y_value)
    print(pred_value)
    plt.matshow(confusion_matrix(y_value, pred_value,  normalize = 'true'), interpolation = 'nearest', cmap = plt.cm.Reds)
    plt.xticks(range(len(labels)), labels, rotation = 45)
    plt.yticks(range(len(labels)), labels)

    cm = confusion_matrix(y_value, pred_value, normalize = normalize)
    for i in range(len(labels)):
        for j in range(len(labels)):
            plt.text(j, i, "%.2f"%cm[i][j], horizontalalignment='center', verticalalignment='center')
    plt.show()

def getPickleFile(pickelFileName):
    if pickelFileName in os.listdir(PICKLE_DIR):
        print("[*] Fetching raw data from pickle file : ",pickelFileName)
        importedData = pickle.load(open(os.path.join(PICKLE_DIR, pickelFileName),"rb"))
        print("[+] Done!")
        return importedData
    else: 
        print("[-] Failed to get file :", pickelFileName)
        return False

def storePickleFile(dataToStore, pickelFileName):
    pickle.dump(dataToStore,open(os.path.join(PICKLE_DIR, pickelFileName),"wb"))
    print('[+] data saved to file : ',pickelFileName)

def getDir():
    print(os.getcwd())