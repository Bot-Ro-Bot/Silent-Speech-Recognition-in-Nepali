import time
import tqdm
import numpy as np
import pandas as pd

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

BoardShim.enable_dev_board_logger()

boardParameters = BrainFlowInputParams()
boardParameters.serial_port = '/dev/ttyUSB0'

cytonId = BoardIds.SYNTHETIC_BOARD.value #BoardIds.CYTON_BOARD.value
board = BoardShim(cytonId, boardParameters)
board.prepare_session()

board.start_stream()
BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
for i in zip(tqdm.tqdm(range(10),desc="PARSING DATA")):
    time.sleep(1)

data = board.get_board_data()
# data = board.get_emg_channels(cytonId)
board.stop_stream()
board.release_session()

# eeg_channels = BoardShim.get_eeg_channels(cytonId)
df = pd.DataFrame(np.transpose(data))
print('Data From the Board')
print(df.head(10))

# demo for data serialization using brainflow API, we recommend to use it instead pandas.to_csv()
DataFilter.write_file(data, 'test.csv', 'w')  # use 'a' for append mode
restored_data = DataFilter.read_file('test.csv')
restored_df = pd.DataFrame(np.transpose(restored_data))
print('Data From the File')
print(restored_df.head(10))