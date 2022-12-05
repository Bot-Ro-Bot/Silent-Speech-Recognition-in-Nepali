import requests
import string
import json
import os

from gtts import gTTS
from playsound import playsound
import pprint
pp = pprint.PrettyPrinter(indent=4)

# mausam_template = "आजको तापक्रम ३२ डिग्री सेल्सियस हुन का साथै मेग गज्रने सम्भावना छ"
# rainy = "बर्सा हुने"
# cloudy = "मेग गज्रने"
# sunny = "घाम लाग्ने"
# windy = " हावा हुरी चल्ने"
# hazy = "तुवालो लाग्ने"
# stormy = "आँधी आउने"
# snowy = "हिमपात हुने"

triggers = {"rain": "बर्सा हुने", "cloud": "मेग गज्रने", "sun": "घाम लाग्ने", "wind": " हावा हुरी चल्ने", "haze": "तुवालो लाग्ने","storm": "आँधी आउने", "snow": "हिमपात हुने"}

# abc = "  पुर्बानुमन अनुसार आजको नुन्यतम तापक्रम 19 डिग्री र अधिकतम तापक्रम २४ डिग्री रहने र"


def get_weather():
	city = "kathmandu"
	country = "Nepal"

	apiKey = '10a62430af617a949055a46fa6dec32f'
	weatherURL = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "," + country + "&units=metric&appid=" + apiKey

	req = requests.session()
	reqPost = req.post(weatherURL)
	# print(reqPost)
	html = reqPost.text

	dataDict = json.loads(html)

	weatherInfo = dataDict['weather'][0]
	# weatherTitle = weatherInfo['main']
	# weatherDescription = weatherInfo['description']
	# pp.pprint(dataDict)
	# print(weatherInfo)
	# print(weatherTitle)
	# print(weatherDescription)
	forecast = weatherInfo['description']
	status_now = weatherInfo['main']
	temp_now = (dataDict['main'])["feels_like"]
	temp_max = (dataDict['main'])["temp_max"]
	temp_min = (dataDict['main'])["temp_min"]

	# print("Forecast: ", forecast)
	# print("Current Status: ", status_now)
	# print("Current Temp. : ", temp_now)
	# print("Maximum Temp. : ", temp_max)
	# print("Minimum Temp. : ", temp_min)
	weather = None

	try:		
		for key,value in triggers.items():
			if(key in forecast):
				# print("KEY: " ,key)
				weather = value
				break
	except:
		return "मलाई थाहा छैन"

	mausam = "आजको तापक्रम" + str(int(temp_now)) + "डिग्री सेल्सियस हुन का साथै" + str(weather) + "सम्भावना छ"
	return mausam


def main():
	mausam = get_weather()
	speak = gTTS(text=mausam, lang="ne", slow=False)
	file = "mausam.mp3"
	speak.save(file)
	playsound(file)
	os.remove(file)

if __name__ == "__main__":
    main()
