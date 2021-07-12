from flask import Flask, render_template, request, jsonify
import logging

import tensorflow as tf
from tensorflow import keras 

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

SENTENCES =["अबको समय सुनाउ","एउटा सङ्गित बजाउ","आजको मौसम बताउ","बत्तिको अवस्था बदल","पङ्खाको स्तिथी बदल"]

from sklearn.preprocessing import LabelEncoder
labelencoder_y = LabelEncoder()
Y_encode = labelencoder_y.fit_transform(SENTENCES)

# initalizing the board
BoardShim.enable_dev_board_logger()

boardParameters = BrainFlowInputParams()
boardParameters.serial_port = '/dev/ttyUSB0'

board_id = BoardIds.SYNTHETIC_BOARD.value #BoardIds.CYTON_BOARD.value #
board = BoardShim(board_id, boardParameters)
channels = board.get_emg_channels(board_id)

app = Flask(__name__)
app.debug = True
# app.run(host="0.0.0.0")

stringPrediction = ""
madePrediction = False 


@app.route('/')
def index():
	return render_template("index.html")

# @app.route('/start_stream', methods=["GET"])
# def start_stream():
# 	print("In start stream")
# 	return 1

@app.route('/start_stream')
def start_stream():
	try:
		receivedData = request.args.get('record', 0, type=str)
		if receivedData.lower() == 'startstream':
			# app.logging.info("inside hero")
			board.prepare_session()
			board.start_stream()
			BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
			return jsonify(result='Started the Recordings')
		elif receivedData.lower() == 'stopstream':
			data = board.get_board_data()
			board.stop_stream()
			board.release_session()
			DataFilter.write_file(data, 'recording/test.csv', 'w')

			modelTest = False 
			if modelTest:
				# TODO : need to trim the length of the recording equal to trained data length
				channel_data = data[:, channels]
				rawdata = []
				rawdata.append(channel_data)
				filteredData = signal_pipeline(rawdata)
				dataFeature = feature_pipeline_melspectrogram(filteredData)
				dataFeature = reshapeChannelIndexToLast(dataFeature)
				 
				#TODO : need to test with a trained model and real data ... 
				# pass to a trained model
				model = tf.keras.models.load_model("<modelname>.h5")
				# model.summary()
				prediction = model.predict_classes(dataFeature)
				print(prediction)
			    stringPrediction = list(labelencoder_y.inverse_transform(list(prediction)))
			    madePrediction = True 
			# return the predicted result to the web interface. 
			return jsonify(result='Stopped Recording. Prediction is ' + stringPrediction )
	except Exception as e :
		return str(e)

# route for ESP to fetch data from
@app.route('/esp')
def esp():
	if madePrediction : 
		madePrediction = False
		return prediction 		#send only number to the arduino relating...
	else : 
		return "hello arduino"

'''
source :
https://pythonprogramming.net/jquery-flask-tutorial/
https://youtu.be/j5wysXqaIV8
'''