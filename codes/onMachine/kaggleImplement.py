import requests
import time

URL = "http://localhost:5000/getEmg"
# URL = "https://silent-app-test.herokuapp.com/getEmg"
res = requests.get(url= URL)
data = res.json()

#this data should be filtered and pass to ml model 
print(data)

time.sleep(1)

payload = {'sentence' : "pass pred word here"}
r = requests.post(URL, json=payload)