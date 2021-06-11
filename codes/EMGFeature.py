class EMG(object):
    """
    preprocessing and feature extraction class for EMG data
    X = List of all instances of input data
    x = an instance of the input data 
    Y = List of all instances of input labels
    y = an instance of the input label
    
    average length of a word utterance: ( 600ms(100 wpm) + 480ms (130 wpm) + 360ms (160 wpm) ) / 3 =  480ms
    """
    
    def __init__(self, SR,FRAME_SIZE,FRAME_SHIFT,MODE):
        """Set the variables """
        self.SR = SR
        self.FRAME_SIZE = FRAME_SIZE
        self.FRAME_SHIFT = FRAME_SHIFT
        self.MODE = MODE
        self.pickle_name = "X_"+MODE+"(features).pickle"
    

    def DNPA(self,seg):
        """Double Nine Point Average"""
        w = []
        for i in range(len(seg)):
            a = i - 4
            b = i + 4
            a = a if a>=0 else 0
            b = b if b<len(seg) else len(seg)
            w.append(int(np.sum(seg[a:b])/9))

        v = []
        for i in range(len(seg)):
            a = i - 4
            b = i + 4
            a = a if a>=0 else 0
            b = b if b<len(seg) else len(seg)
            v.append(int(np.sum(w[a:b])/9))

        return v

    
    def ZCR(self,seg):
        """Zero Crossing Rate"""
        pos = seg>0
        npos = ~pos
        return len(((pos[:-1] & npos[1:]) | (npos[:-1] & pos[1:])).nonzero()[0])

    
    def HFS(self,seg):
        """High frequency signals"""
        return np.subtract(seg,self.DNPA(seg))

    
    def RHFS(self,seg):
        """Rectified High frequency signals"""
        return abs(self.HFS(seg))

    
    def FBP(self,seg):
        """Frame Based Power"""
        return np.sum(np.power(seg,2))

    
    def feature(self,seg,_type="time"):
        """ 
        "time": Features in time domain
        "freq": Features in frequency domain
        "all": Features in both domain
        """
        if _type == "time":
            return np.hstack((self.DNPA(seg),self.RHFS(seg),self.HFS(seg),self.ZCR(seg),self.FBP(seg)))
        elif _type == "freq":
            return 
        elif _type == "all":
            return np.hstack(self.feature(seg,"time"),self.feature(seg,"freq"))

    
    def MFCC(self,seg):
        """Mel Frequency Cepstral Coefficients"""
        mfcc = librosa.feature.mfcc(y=seg,sr=self.SR,n_mfcc=20)
#         return np.mean(mfcc.T,axis=0)
        return mfcc

    
    def STFT(self,seg):
        """Short Time Fourier Transform"""
        stft = librosa.feature.chroma_stft(y=seg,sr=self.SR,n_fft=20)
#         return np.mean(stft.T,axis=0)
        return stft

    
    def segment(self,x):
        """Segmenting the data into frames and sliding them according to the frame shift"""
        f = []
        for channel in range(6):
            for i in range(len(x[0])):
                a = i*self.FRAME_SHIFT
                b = a + self.FRAME_SIZE
                if(b>len(x[0])):
                    break
                seg = x[channel][a:b]
                f.extend(self.feature(seg))
        return f

    def fit(self,X,Y):
        """Extract Features and return the zero padded list of features"""
        if(self.pickle_name in os.listdir() ):
            print("Fetching Pickle file")
            temp_X = pickle.load(open(self.pickle_name,"rb"))
        else:
            temp_X = []
            for x,count in zip(X, tqdm.tqdm(range(len(X)),ncols=100,desc="Extracting Features("+self.MODE+")" ) ):
                temp_X.append(self.segment(x))

            # save all extracted features to a pickle file
            print("Saving features as: ",self.pickle_name)
            pickle.dump(temp_X,open(self.pickle_name,"wb"))
        temp_X = np.array(temp_X)
        print(len(temp_X))
        print(len(Y))
        print(temp_X.shape)
        return self.reduce_dimension(temp_X),self.encode_labels(Y)

    
    def fit_transform(self,X,Y):
        return self.fit(X,Y)