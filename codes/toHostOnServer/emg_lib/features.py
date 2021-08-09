import tqdm
import biosppy
import numpy as np
import scipy.signal as sig
import librosa
import librosa.display
from scipy.fft import fft,fftfreq
from scipy.fftpack import fft
import matplotlib.pyplot as plt


SAMPLING_RATE = 250

def feature_pipeline(data):
    feature_data = []
    def getSpect(sdata):
        M = 60
        win = sig.windows.hann(M, sym=False)
        return sig.spectrogram(x=np.array(sdata), fs=SAMPLING_RATE, window=win,
                                nperseg=len(win), noverlap=3*M/4, nfft=M)
    def process_signal(data):
        f_data = []
        for i in range(8):
            _, _, c_data = getSpect(data[:, i])
            f_data.append(c_data)
        return np.array((f_data-np.mean(f_data))/np.std(f_data))
    
    for d,i in zip(data,tqdm.tqdm(range(1,len(data)+1),desc="EXTRACTING DATA: ")):
        temp_data = process_signal(d)
        feature_data.extend([temp_data])
    return np.array(feature_data)

# spectorgram features...
def getSpectrogram(sdata):
    M = 60
    win = sig.windows.hann(M, sym=False)
    return sig.spectrogram(x=np.array(sdata), fs=SAMPLING_RATE, window=win,
                       nperseg=M, noverlap=3*M/4, nfft=M)

def feature_pipeline_Spectrogram(data):
    feature_data = []
    def process_signal(data):
        f_data = []
        for i in range(8):
            _, _, c_data = getSpectrogram(data[:, i])
            f_data.append(c_data)
        return np.array(f_data)
    
    for d,i in zip(data, tqdm.tqdm(range(1,len(data)+1),desc="EXTRACTING DATA: ")):
        temp_data = process_signal(d)
        feature_data.extend([temp_data])
    return np.array(feature_data)

def plotSpectrogram(singleChannelData):
    freq, time, spec = getSpectrogram(singleChannelData)
    plt.pcolormesh(time, freq, spec, shading='gouraud')
    plt.title('spectrogram')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    return freq, time, spec