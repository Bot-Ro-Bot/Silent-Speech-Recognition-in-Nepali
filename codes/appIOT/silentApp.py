from flask import Flask, render_template, request, jsonify
import logging


import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


# initalizing the board
BoardShim.enable_dev_board_logger()

boardParameters = BrainFlowInputParams()
boardParameters.serial_port = '/dev/ttyUSB0'

board_id = BoardIds.SYNTHETIC_BOARD.value #BoardIds.CYTON_BOARD.value
board = BoardShim(board_id, boardParameters)

app = Flask(__name__)
app.run(debug=True)


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
			# TODO : 
			# extract the channel data
			# pass it to pipeline 
			# pass to a trained model
			# return the predicted result to the web interface. 
			return jsonify(result='Stopped Recording')
			# need to add iot devices
			# routes for iot device to check the predicted word for action to be performed
	except Exception as e :
		return str(e)


'''
source :
https://pythonprogramming.net/jquery-flask-tutorial/
'''