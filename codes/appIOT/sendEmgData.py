import requests
import numpy as np 

url = 'http://127.0.0.1:5000/takeEmg'

emgData = np.array([1,2,3,4,5,6])

payload = {'emg' : emgData.tolist()}

r = requests.post(url, json=payload)