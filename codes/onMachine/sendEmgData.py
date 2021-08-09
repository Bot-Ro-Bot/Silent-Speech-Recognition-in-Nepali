import requests
import numpy as np 
import time

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

from playsound import playsound

URL = 'http://127.0.0.1:5000/takeEmg'
PORT = '/dev/ttyUSB0'
SESSION_RECORD_INTERVAL = 5 # seconds 

# initalizing the board
BoardShim.enable_dev_board_logger()

boardParameters = BrainFlowInputParams()
boardParameters.serial_port = PORT 

board_id = BoardIds.SYNTHETIC_BOARD.value #BoardIds.CYTON_BOARD.value #
board = BoardShim(board_id, boardParameters)
channels = board.get_emg_channels(board_id)

print("Starting the recording.")
print("Preparing session, speak on beep")
time.sleep(1)
playsound('./resources/beep.mp3')

board.prepare_session()
board.start_stream()
BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')

time.sleep(SESSION_RECORD_INTERVAL)

data = board.get_board_data()
board.stop_stream()
board.release_session()
DataFilter.write_file(data, 'recording/test.csv', 'w')

# TODO : need to trim the length of the recording equal to trained data length
# channel_data = data[:, channels]
# rawdata = []
# rawdata.append(channel_data)
# filteredData = signal_pipeline(rawdata)
# dataFeature = feature_pipeline_melspectrogram(filteredData)
# dataFeature = reshapeChannelIndexToLast(dataFeature)


emgData = np.array([1,2,3,4,5,6])
payload = {'emg' : emgData.tolist()}
r = requests.post(URL, json=payload)