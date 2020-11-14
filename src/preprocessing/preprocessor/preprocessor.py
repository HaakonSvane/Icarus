from pathlib import Path
import pandas as pd
import os

from src.preprocessing.preprocessor.normalizer import _Normalizer
from src.preprocessing.preprocessor.data_labeler import _DataLabeler
from src.preprocessing.preprocessor.function import _Function
from src.preprocessing.preprocessor.utility import _Utility
from src.preprocessing.preprocessor.config import *
import config

'''
    Preprocessor:
        This module is responsible for implementing all the computations that are used in the preprocessing stage
        of the data. 
'''

class Preprocessor:
    def __init__(self, raw_dir : str = config.DATA_DIR / 'raw', out_dir : str = config.DATA_DIR / 'training'):
        self.raw_dir = raw_dir
        self.out_dir = out_dir
        self.NORMALIZER = _Normalizer(HOURS_BEHIND)
        self.DATALABELER = _DataLabeler(HOURS_AHEAD)
        self.FUNCTION = _Function()
        self.UTILILITY = _Utility()

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


    def save_to_file(self, frame: pd.DataFrame, sub_dir : str = None):
        d = '' if not sub_dir else sub_dir
        new_path = self.out_dir / d

        if not new_path.is_dir():
            os.mkdir(new_path)

        frame.to_csv(new_path)






if __name__ == '__main__':
    p = Preprocessor()

    path = config.DATA_DIR / 'preprocessing' / 'raw' / 'AAPL'
    frame = p.UTILILITY.load_batch_data(path)
    comp = p.DATALABELER.get_labels(frame, return_full_computation=True)
    p.DATALABELER.plot_computations(comp)