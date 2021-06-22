import scipy.signal as sig
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

# melspectrogram features...
def getMelspectrogram(mdata):
    S = librosa.feature.melspectrogram(np.asfortranarray(mdata), sr=SAMPLING_RATE,
                            n_mels=2,
                            n_fft = int(32*10**-3*SAMPLING_RATE),
                            hop_length=int(10*10**-3*SAMPLING_RATE)
                            )

    # Convert to log scale (dB). We'll use the peak power (max) as reference.
    log_S = librosa.power_to_db(S, ref=np.max)
    return log_S

def feature_pipeline_melspectrogram(data):
    feature_data = []
    def process_signal(data):
        f_data = []
        for i in range(8):
            c_data = getMelspectrogram(data[:, i])
            f_data.append(c_data)
        return np.array(f_data)
    
    for d,i in zip(data,tqdm.tqdm(range(1,len(data)+1),desc="EXTRACTING DATA: ")):
        temp_data = process_signal(d)
        feature_data.extend([temp_data])
    return np.array(feature_data)

def plotMelspectrogram(singleChannelData):
    log_S = getMelspectrogram(singleChannelData)
    librosa.display.specshow(log_S, sr=SAMPLING_RATE, x_axis='time', y_axis='mel', fmax = 250/2)
    plt.title('Mel power spectrogram ')
    plt.colorbar(format='%+02.0f dB')
    plt.tight_layout()
    return log_S

# mfcc features

def feature_pipeline_mfcc(data):
    feature_data = []
    def getMFCC(mdata):
        return librosa.feature.mfcc(y=np.asfortranarray(mdata),
                                    sr=SAMPLING_RATE,
                                    n_mfcc=13,
                                    n_mels = 30,
                                    n_fft=int(16*(10**-3)*SAMPLING_RATE),
                                    hop_length=int(10*(10**-3)*SAMPLING_RATE)
                                   )

    def process_signal(data):
        f_data = []
        for i in range(8):
            c_data = getMFCC(data[:, i])
            f_data.append(c_data)
    return np.array(f_data)
    
    for d,i in zip(data,tqdm.tqdm(range(1,len(data)+1),desc="EXTRACTING DATA: ")):
        temp_data = process_signal(d)
        feature_data.extend([temp_data])
    return np.array(feature_data)
