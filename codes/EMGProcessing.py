def preprocess_data(data):
    #correct dc drift
    #correct dc bias
    #normalize data
    
    #filter data
    def digital_filter(data,HPF=0.5,LPF=10,H_ORDER=4,L_ORDER=4,SR=SAMPLING_RATE):
        hpfSignal = biosppy.signals.tools.filter_signal(data,
                                                     ftype="butter",
                                                     band="highpass",
                                                     order=H_ORDER,
                                                     sampling_rate=SR,
                                                     frequency=HPF)

        b,a = signal.iirnotch(50,30,SR)
        notchFilterSignal = signal.lfilter(b, a, hpfSignal[0])

        lpfSignal = biosppy.signals.tools.filter_signal(notchFilterSignal,
                                                     ftype="butter",
                                                     band="lowpass",
                                                     order=L_ORDER,
                                                     sampling_rate=SR,
                                                     frequency=LPF)
        return lpfSignal[0]
    
    allChannelFilteredData = []
    for channel in range(NUM_CHANNELS):
        dcDriftCorrectedSignal = data[:, channel] - data[0, channel]
        dcBiasCorrectedSignal = dcDriftCorrectedSignal - np.mean(dcDriftCorrectedSignal)
        filteredChannelData = digital_filter(dcBiasCorrectedSignal)
        allChannelFilteredData.append(filteredChannelData)
    
    return np.array(allChannelFilteredData).T