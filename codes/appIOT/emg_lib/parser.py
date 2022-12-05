import numpy as np 
import tqdm

# hardware definitions
"""
https://docs.openbci.com/docs/02Cyton/CytonDataFormat#:~:text=By%20default%2C%20our%20Arduino%20sketch,of%200.02235%20microVolts%20per%20count
"""
SAMPLING_RATE = 250 #Hz
NUM_CHANNELS = 80 
ADC_RESOLUTION = 24 #bits
ADC_GAIN = 24.0
REF_VOLTAGE = 4.5 #Volts
SCALE_FACTOR = (REF_VOLTAGE/float((pow(2,23))-1)/ADC_GAIN)*1000000.0 #micro-volts

# dataset definitions
SPEAKER = ["RL","RN","SR","US"]
SESSION = ["session"+str(i) for i in range(1,9)]
MODE = ["mentally","mouthed"]
SENTENCES =["अबको समय सुनाउ","एउटा सङ्गित बजाउ","आजको मौसम बताउ","बत्तिको अवस्था बदल","पङ्खाको स्तिथी बदल"]
LABELS = np.array(SENTENCES)[[3, 2, 1, 4, 0, 3, 2, 1, 4, 0, 3, 2, 1, 4, 0]]


def parser(files, NORMALIZE=True, DEPLOY=False, utteranceCountPerFile = 15):
    """
    parser function to extract utterances from .txt file and store them in a dictionary
    """
    # PERCENTILES FOR LENGTH NORMALIZATION
    if(NORMALIZE==True):
        percentile_95 = 1602
        percentile_97 = 1614
        percentile_99 = 1648
        percentile_100 = 1875
    else:
        percentile_95 = percentile_97 = percentile_99 = percentile_100 = -1
        
    dataset = {"data":[], "speaker":[],"session":[],"labels":[]}
    
    def get_data(file):
        signal = read_data(file)
        if(DEPLOY==True):
            dataset["data"].extend(signal)
            return
        if(len(signal) != utteranceCountPerFile):
            return

        session = file.split("/")[-2]
        speaker = file.split("/")[-3]
        
        dataset["data"].extend(signal)
        dataset["speaker"].extend([speaker]*len(signal))
        dataset["session"].extend([session]*len(signal))
        dataset["labels"].extend(LABELS)
        
    def read_data(file):
        f = open(file, 'r')
        contents = map(lambda x : x.strip(), f.readlines())
        #the file starts with '%' and some instruction before data and removing these data 
        frames_original = list(filter(lambda x : x and x[0] != '%', contents))[1:]
        #the data row contains channels info digital trigger and accelerometer info separated by comma
        frames_original = list(map(lambda s : list(map( lambda ss: ss.strip(), s.split(','))), frames_original))
        # (8 channels) + digital triggers
        # the digital trigger is in a[16], used to indicate the utterance
        frames = list(map(lambda a: list(map(float, a[1:9])) + [float(a[16])] , frames_original))
        frames = np.array(frames)
        indices = []
        signal = []
        
        for index,f in enumerate(frames[:,-1]):
            if(bool(f) ^ bool(frames[(index+1) if ((index+1)<len(frames)) else index,-1]) ):
                indices.append(index)
                if len(indices)>1 and len(indices)%2==0:
                    frame_len = indices[len(indices)-1] - indices[len(indices)-2]
                    if(frame_len<percentile_99):
                        pad = int(np.ceil((percentile_99 - frame_len)/2))
                    else:
                        pad = 0
                    left_pad = indices[len(indices)-2] - pad
                    right_pad = indices[len(indices)-1] + pad
                    a_frame = (frames[left_pad:right_pad,:-1])[:percentile_99]
                    signal.append(a_frame)
    
        return np.array(signal) # removed scale factor
        
    for file,i in zip(files,tqdm.tqdm(range(1,len(files)+1),desc="PARSING DATA")):
        get_data(file)

    return dataset

def getAugmentedData(all_data, shift_length=100):
    DATA_LENGTH = len(all_data["labels"])

    def time_shift(data,SHIFT_LEN = shift_length, SHIFT_DIR ="RIGHT", index=0):
        if SHIFT_DIR != "RIGHT":
            SHIFT_LEN = - SHIFT_LEN
            index = -1
        shifted_data = np.roll(data,SHIFT_LEN)
        if SHIFT_LEN>0:
            shifted_data[:SHIFT_LEN] = data[index]
        else:
            shifted_data[SHIFT_LEN:] = data[index]
        return shifted_data
    
    for i in range(DATA_LENGTH):
        aug_data = []
        for j in range(8):
            temp_data1 = time_shift(all_data["data"][i][:,j],SHIFT_DIR="LEFT")
            aug_data.append(temp_data1)

        all_data["data"].extend([(np.array(aug_data)).T])
        all_data["labels"].extend([all_data["labels"][i]])
        all_data["speaker"].extend([all_data["speaker"][i]])
        all_data["session"].extend([all_data["session"][i]])

    for i in range(DATA_LENGTH):
        aug_data = []
        for j in range(8):
            temp_data2 = time_shift(all_data["data"][i][:,j],SHIFT_DIR="RIGHT")
            aug_data.append(temp_data2)

        all_data["data"].extend([(np.array(aug_data)).T])
        all_data["labels"].extend([all_data["labels"][i]])
        all_data["speaker"].extend([all_data["speaker"][i]])
        all_data["session"].extend([all_data["session"][i]])
    return all_data