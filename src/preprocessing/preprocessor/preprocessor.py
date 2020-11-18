from pathlib import Path
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

from src.preprocessing.preprocessor.normalizer import _Normalizer
from src.preprocessing.preprocessor.data_labeler import _DataLabeler
from src.preprocessing.preprocessor.function import _Function
from src.preprocessing.preprocessor.utility import _Utility
from src.preprocessing.preprocessor.prep_config import *
import config

'''
    Preprocessor:
        This module is responsible for implementing all the computations that are used in the preprocessing stage
        of the data. 
'''


class Preprocessor:
    def __init__(self, raw_dir: str = config.DATA_DIR / 'raw', out_dir: str = config.DATA_DIR / 'training'):
        self.raw_dir = raw_dir
        self.out_dir = out_dir
        self.Normalizer = _Normalizer(hours_behind=HOURS_BEHIND, dt=DT)
        self.DataLabeler = _DataLabeler(hours_ahead=HOURS_AHEAD, dt=DT)
        self.Function = _Function(hours_behind=HOURS_BEHIND, dt=DT)
        self.Utility = _Utility()

    @property
    def raw_dir(self):
        return self._raw_dir

    @raw_dir.setter
    def raw_dir(self, val):
        try:
            path = Path(val)
        except TypeError:
            raise TypeError(f'Path "{val}" is not valid.')
        self._raw_dir = path

    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    def out_dir(self, val):
        try:
            path = Path(val)
        except TypeError:
            raise TypeError(f'Path "{val}" is not valid.')
        if not path.is_dir():
            raise ValueError(f'Path "{path}" does not exist.')
        self._out_dir = path

    def save_dataframe_to_file(self, frame: pd.DataFrame, filename: str, sub_dir: str = None):
        '''
        Saves a dataframe as a csv to a path with provided filename. If subdir is not None, this should be a path to a
        subdirectory to save the file to.

        :param frame: dataframe to save.
        :param filename: name of file to save.
        :param sub_dir: name of subdir to save in. Defaults to None
        :return:
        '''
        d = '' if not sub_dir else sub_dir
        new_path = self.out_dir / d
        filename = filename if filename.endswith('.csv') else filename + '.csv'

        if not new_path.is_dir():
            os.mkdir(new_path)

        frame.to_csv(new_path / filename, index=False)

    def save_image_to_file(self, arr: np.array, filename: str, sub_dir: str = None, extension: str = 'png'):
        '''
        Saves a 2D-array as a binary mage to a path with provided filename. Iif subdir is not None, this should be a
        path to a subdirectory to save the file to.

        :param arr: dataframe to save.
        :param filename: Name of file to save.
        :param sub_dir: Name of subdir to save in. Defaults to None
        :param extension: File format extension to use. Defaults to 'png'. Accepted values are 'jpg','png' and 'svg'.
        :return:
        '''

        d = '' if not sub_dir else sub_dir
        new_path = self.out_dir / d
        filename = filename if filename.endswith('.' + extension) else filename + '.' + extension

        if not new_path.is_dir():
            os.mkdir(new_path)

        plt.imsave(new_path / filename, arr, cmap='binary', format=extension, origin='lower')
