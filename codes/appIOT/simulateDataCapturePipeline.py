import time
import tqdm
import numpy as np
# import pandas as pd
from emg_lib import *


import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

BoardShim.enable_dev_board_logger()

boardParameters = BrainFlowInputParams()
boardParameters.serial_port = '/dev/ttyUSB0'

cytonId = BoardIds.SYNTHETIC_BOARD.value # BoardIds.CYTON_BOARD.value #
board = BoardShim(cytonId, boardParameters)

channels = board.get_emg_channels(cytonId)
print(channels)

board.prepare_session()

board.start_stream()
BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
for i in zip(tqdm.tqdm(range(10),desc="PARSING DATA")):
    time.sleep(1)

data = board.get_board_data()
board.stop_stream()
board.release_session()

data = np.transpose(data)
print(data.shape)
channel_data = data[:,channels[:8]]     #[:8] - for synthetic boards only remove this.
rawdata = []
rawdata.append(channel_data)
data_filtered = signal_pipeline(channel_data)
data_feature = feature_pipeline_melspectrogram(data_filtered)
data_featured = reshapeChannelIndexToLast(data_feature)
