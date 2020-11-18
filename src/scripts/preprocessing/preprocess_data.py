import pandas as pd
from src.preprocessing.preprocessor import Preprocessor
from src.preprocessing.preprocessor.prep_config import *
import config
from tqdm import tqdm

''''
    WORKFLOW:
        For each file f for every equity e in raw:
            * Concatenate all f in e to a single dataframe df
            * Trim the data to normal trading hours
            * Compute the labels of df
            * Normalize all the dimensions of each point in df
            * Save df as csv
            * Batch all labels and discard those with a period shorter than 
'''
prep = Preprocessor()

def import_and_trim(path: str):

    pass

def label():
    pass

def normalize(frame : pd.DataFrame):
    norm_frame = pd.DataFrame()
    pass

def save_data(frame : pd.DataFrame):
    pass

def save_recurrence_plot(frame : pd.DataFrame):
    pass



norm_frame = pd.DataFrame()
path = config.DATA_DIR / 'preprocessing' / 'raw' / 'GOOGL'
frame = prep.Utility.load_batch_data(path)
frame = prep.Utility.get_trading_hours(frame)
frame['label'] = prep.DataLabeler.get_labels(frame)
norm_frame['volume'] = prep.Normalizer.modfified_tanh(frame['volume'].values)
norm_frame['close'] = prep.Normalizer.modfified_tanh(frame['close'].values)
norm_frame['open'] = prep.Normalizer.modfified_tanh(frame['open'].values)
norm_frame['high'] = prep.Normalizer.modfified_tanh((frame['high'] - (frame['open'] + frame['close']) / 2).values)
norm_frame['low'] = prep.Normalizer.modfified_tanh((frame['low'] - (frame['open'] + frame['close']) / 2).values)
norm_frame['rsi'] = prep.Function.RSI(frame) / 100
norm_frame['label'] = frame['label']

norm_frame.drop(norm_frame.head(int(HOURS_AHEAD / DT) - 1).index, inplace=True)
norm_frame.drop(norm_frame.tail(int(HOURS_BEHIND / DT + 1)).index, inplace=True)
norm_frame.reset_index(drop=True, inplace=True)

prep.Utility.calc_recurrence_plot(norm_frame.head(2880).drop('label', axis=1), percentile=REC_PERC, debug_plot=True)
