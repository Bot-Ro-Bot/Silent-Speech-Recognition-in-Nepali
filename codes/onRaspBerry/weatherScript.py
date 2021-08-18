import requests
import string
import json

# translation
import googletrans
from googletrans import Translator
# text to speech
from gtts import gTTS
from playsound import playsound

# numbers = ['one', 'two', 'three', 'four', 'five'
# 		 'six', 'seven', 'eight', 'nine', 'ten']

def weather_report():
	city = "kathmandu"
	country = "Nepal"

	apiKey = '10a62430af617a949055a46fa6dec32f'
	weatherURL = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "," + country + "&units=metric&appid=" + apiKey

	req = requests.session()
	reqPost = req.post(weatherURL)
	print(reqPost)
	html = reqPost.text

	dataDict = json.loads(html)
	weatherInfo = dataDict['weather'][0]
	weatherTitle = weatherInfo['main']
	weatherDescription = weatherInfo['description']

	def translateSentence(sentenceToTranslate, _from = 'en' , _to = 'ne', verbose = False):
		translatorEngine = Translator()
		translatedSentence = translatorEngine.translate(sentenceToTranslate, dest = _to, src = _from)
		if verbose:
			print(translatedSentence.text)
		return translatedSentence.text

	def textToAudio(text, language = 'ne'):
		textToSpeechEngine = gTTS(text = text, lang = language)
		textToSpeechEngine.save('currentTextAudio.mp3')
		playsound('currentTextAudio.mp3')
		
	textToAudio(translateSentence(weatherTitle, verbose = True))
	textToAudio(translateSentence(weatherDescription, verbose = True))

weather_report()

'''
source :
https://www.how2shout.com/how-to/translate-languages-using-python-and-google-translate-api.html
https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group
--try pip install googletrans==4.0.0-rc1
https://dev.to/po/text-to-speech-using-python-gtts-in-5-lines-of-code-462m
'''