from emg_lib.parser import parser, getAugmentedData
from emg_lib.filter import signal_pipeline
from emg_lib.features import *
from emg_lib.usefulFunction import reshapeChannelIndexToLast, confusion_matrix_plt, getDir, getPickleFile, storePickleFile