import requests
import string
import json

# translation
import googletrans
from googletrans import Translator
# text to speech
from gtts import gTTS
from playsound import playsound

from datetime import datetime

numerals = {0: 'one', 1 : 'one', 2 : 'two', 3 : 'three', 4:'four', 5 : 'five',
			6: 'six', 7 : 'seven', 8: 'eight', 9 : 'nine', 10 : 'ten', 
			11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen', 15 : 'fifteen',
			16 : 'sixteen', 17: 'seventeen', 18 : 'eighteen', 19 : 'nineteen', 20 : 'twenty',
			21 : 'twenty one', 22 : 'twenty two' }

def current_time_report():
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Current Time =", current_time)
	hours, minutes, seconds = current_time.split(':')
	print(hours, minutes, seconds)

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

	textToAudio(hours)
	textToAudio(translateSentence('hours', verbose = True))
	textToAudio(minutes)
	textToAudio(translateSentence('minutes', verbose = True))


current_time_report()
