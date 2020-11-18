import pandas as pd
import numpy as np
from tqdm import tqdm
from pathlib import Path
from typing import List

from src.preprocessing.preprocessor import Preprocessor
from src.preprocessing.preprocessor.prep_config import *
import config

''''
    WORKFLOW:
        For each file f for every equity e in raw:
            * Concatenate all f in e to a single dataframe df
            * Trim the data to normal trading hours
            * Compute the labels of df
            * Calculate the RSI of the equity
            * Normalize all the variables of each point in df
            * Trim the "look back" and "look forward" values at the endpoints of df due to pollution by 
              the convolutions used in the labeling process
            * Save df as csv
            * Batch all labels and discard those with a period shorter than CLUSTER_SIZE. Larger clusters gets trimmed.
            * For each cluster, create a recurrence plot
'''
prep = Preprocessor()
prog_bar = tqdm(total=100)
tasks = 16 # Total number of distinct tasks to perform. Counted manually :/ For the status bar update.


def import_and_trim(path: str):
    dframe = prep.Utility.load_batch_data(path)
    prog_bar.update(1/tasks*100)
    dframe = prep.Utility.get_trading_hours(dframe, from_time=START_TRADE, to_time=END_TRADE)
    prog_bar.update(1 / tasks * 100)
    return dframe

def label(dframe: pd.DataFrame) -> pd.DataFrame:
    dframe['label'] = prep.DataLabeler.get_labels(dframe)
    prog_bar.update(1/tasks*100)
    return dframe

def normalize(dframe: pd.DataFrame) -> pd.DataFrame:
    norm_frame = pd.DataFrame()
    norm_frame['volume'] = prep.Normalizer.modfified_tanh(dframe['volume'].values)
    prog_bar.update(1 / tasks * 100)
    norm_frame['close'] = prep.Normalizer.modfified_tanh(dframe['close'].values)
    prog_bar.update(1 / tasks * 100)
    norm_frame['open'] = prep.Normalizer.modfified_tanh(dframe['open'].values)
    prog_bar.update(1 / tasks * 100)
    norm_frame['high'] = prep.Normalizer.modfified_tanh(
        (dframe['high'] - (dframe['open'] + dframe['close']) / 2).values)
    prog_bar.update(1 / tasks * 100)
    norm_frame['low'] = prep.Normalizer.modfified_tanh((dframe['low'] - (dframe['open'] + dframe['close']) / 2).values)
    prog_bar.update(1 / tasks * 100)
    norm_frame['label'] = dframe['label']
    prog_bar.update(1 / tasks * 100)
    if 'rsi' in dframe:
        norm_frame['rsi'] = dframe['rsi']/100
    prog_bar.update(1 / tasks * 100)
    return norm_frame

def add_RSI(dframe: pd.DataFrame) -> pd.DataFrame:
    dframe['rsi'] = prep.Function.RSI(dframe)
    prog_bar.update(1 / tasks * 100)
    return dframe

def trim_ends(dframe: pd.DataFrame, start_trim: int = int(HOURS_AHEAD / DT) - 1,
              end_trim: int = int(HOURS_BEHIND / DT + 1)) -> pd.DataFrame:
    dframe = dframe.drop(dframe.head(start_trim).index)
    prog_bar.update(1 / tasks * 100)
    dframe = dframe.drop(dframe.tail(end_trim).index)
    prog_bar.update(1 / tasks * 100)
    return dframe.reset_index(drop=True)


def calc_recurrence(dframe: pd.DataFrame)->np.array:
    if 'label' in dframe:
        dframe = dframe.drop('label', axis=1)
    rec = prep.Utility.calc_recurrence_plot(dframe, percentile=REC_PERC, distance_metric=REC_DIST_MET)
    prog_bar.update(1 / tasks * 100)
    return rec

def save_data(dframe: pd.DataFrame, filemane: str, subdir: str = None):
    prep.save_dataframe_to_file(dframe, filemane, subdir)
    prog_bar.update(1 / tasks * 100)

def save_recurrence_plot(arr: np.array, filename: str, subdir: str = None, extension: str = 'png'):
    prep.save_image_to_file(arr, filename, subdir, extension)
    prog_bar.update(1 / tasks * 100)



syms = [d.name for d in (config.DATA_DIR / 'preprocessing' / 'raw').iterdir() if d.is_dir()]
for sym in syms:
    prog_bar.reset()
    prog_bar.set_description(sym, refresh=True)
    path = config.DATA_DIR / 'preprocessing' / 'raw' / sym
    data = import_and_trim(path)
    data = label(data)
    data = add_RSI(data)
    data = normalize(data)
    data = trim_ends(data)
    #prep.Utility.cluster_data(data)
    prep.save_dataframe_to_file(data,sym+"_15min.csv", sub_dir=Path('labeled'))

    prog_bar.update(100-prog_bar.n)

prog_bar.close()





