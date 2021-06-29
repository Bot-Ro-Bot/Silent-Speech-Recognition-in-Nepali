import tqdm
import biosppy
import numpy as np
import scipy.signal as sig
from scipy.stats import zscore

def signal_pipeline(data,RICKER=False):
    """
    CORRECT DC DRIFT --> CORRECT DC BIAS --> SMOOTHING SIGNAL --> NORMALIZE DATA --> FILTER DATA 	
    """
    filter_data = []
    def digital_filter(data,HPF=0.5,LPF=10,H_ORDER=4,L_ORDER=4,SR=250):
        """
        HPF --> NOTCH --> LPF --> RICKER CONVOLUTION
        """
        # highpass filter
        f_signal = biosppy.signals.tools.filter_signal(data,ftype="butter",band="highpass",order=H_ORDER,sampling_rate=SR,frequency=HPF)
        # notch filter
        b,a = sig.iirnotch(50,30,SR)
        f_signal = sig.lfilter(b,a,f_signal[0])
        # lowpass filter
        f_signal = biosppy.signals.tools.filter_signal(f_signal,ftype="butter",band="lowpass",order=L_ORDER,sampling_rate=SR,frequency=LPF)
        if(RICKER==True):
            # RICKER CONVOLUTION TO REMOVE HEARTBEAT ARTIFACTS
            ricker_width = 35 * SR // 250
            ricker_sigma = 4.0 * SR #/https://www.kaggle.com/davids1992/speech-representation-and-data-exploration#1.-Visualization 250
            ricker = sig.ricker(ricker_width,ricker_sigma)
            # normalize ricker
            ricker = np.array(ricker, np.float32) / np.sum(np.abs(ricker))
            convolution = sig.convolve(f_signal[0],ricker,mode="same")
            return (f_signal[0]-2*convolution)
        return f_signal[0]

    def process_signal(data):
        f_data = []
        for i in range(8):
            # correction of DC drift
            c_data = data[:,i]- data[0,i]
            # correct DC bias
            c_data = c_data - np.mean(c_data)
            # normalize and filter data
            c_data = digital_filter(c_data)
            f_data.append(c_data)
        return np.array(f_data).T

    for d,i in zip(data,tqdm.tqdm(range(1,len(data)+1),desc="PROCESSING DATA: ")):
        temp_data = process_signal(d)
        filter_data.extend([temp_data])
    return np.array(filter_data)