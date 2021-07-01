from flask import Flask, render_template, request, jsonify
import logging


import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


# initalizing the board
# BoardShim.enable_dev_board_logger()

# boardParameters = BrainFlowInputParams()
# boardParameters.serial_port = '/dev/ttyUSB0'

# board_id = BoardIds.SYNTHETIC_BOARD.value #BoardIds.CYTON_BOARD.value
# board = BoardShim(board_id, boardParameters)

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
			# board.prepare_session()


			return jsonify(result='Started the Recording')
		elif receivedData.lower() == 'stopstream':
			return jsonify(result='Stopped Recording')
	except Exception as e :
		return str(e)


'''
source :
https://pythonprogramming.net/jquery-flask-tutorial/
'''