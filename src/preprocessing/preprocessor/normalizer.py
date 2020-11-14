import numpy as np
import pandas as pd

class _Normalizer:
    def __init__(self, hours_behind: float):
        self.hours_behind = hours_behind

    @property
    def hours_behind(self):
        return self._hours_behind

    @hours_behind.setter
    def hours_behind(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError(f'Value {val} is not valid. Must be an integer or float.')
        self._hours_behind = val

    def normalize_volume(self, frame: pd.DataFrame, column_name: str = 'volume') -> np.array:
        '''
        Normalizes the volume traded based on the

        :param frame: dataframe with stock data.
        :param column_name: Name of the volume column. Defaults to 'volume'.
        :return: 1D-array of the normalized volume
        '''
        pass
