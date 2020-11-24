import pandas as pd
import numpy as np

from src.preprocessing.preprocessor.prep_config import *


class _Function:

    def __init__(self, hours_behind: float, dt: float):
        self.hours_behind = hours_behind
        self.dt = dt

    @property
    def hours_behind(self):
        return self._hours_behind

    @hours_behind.setter
    def hours_behind(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError(f'Value {val} is not valid. Must be an integer or float.')
        self._hours_behind = val

    @property
    def dt(self):
        return self._dt

    @dt.setter
    def dt(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError(f'Value {val} is not valid. Must be an integer or float.')
        self._dt = val

    def RSI(self, frame: pd.DataFrame, open_name: str = 'open', close_name: str = 'close', dt: float = DT) -> np.array:
        '''
        Calculates the RSI for a dataframe. The frame must contain a column with open and close prices.

        :param frame: dataframe containing data to calculate RSI for.
        :param open_name: Name of the "open" price column in the dataframe. Defaults to 'open'.
        :param close_name: Name of the "close" price column in the dataframe. Defaults to 'close'.
        :return: dataframe of the calculated RSI.
        '''

        U_calc = lambda diff: diff if diff > 0 else 0
        D_calc = lambda diff: np.abs(diff) if diff < 0 else 0
        f_U = np.vectorize(U_calc, otypes=[np.float])
        f_D = np.vectorize(D_calc, otypes=[np.float])

        n_points = len(frame.index)
        rsi = np.zeros(n_points)
        rsi.fill(np.nan)

        look_back = int(self.hours_behind / dt)

        diffs = (frame[close_name] - frame[open_name]).values
        U = f_U(diffs)
        D = f_D(diffs)

        SMMA_U = np.zeros(n_points - look_back + 1)
        SMMA_D = np.zeros(n_points - look_back + 1)
        SMMA_U[0] = np.mean(U[:look_back])
        SMMA_D[0] = np.mean(D[:look_back])
        for i in range(1, n_points - look_back + 1):
            SMMA_U[i] = (U[i + look_back - 1] + (SMMA_U[i - 1] * (look_back - 1))) / look_back
            SMMA_D[i] = (D[i + look_back - 1] + (SMMA_D[i - 1] * (look_back - 1))) / look_back

        rs = SMMA_U / SMMA_D
        rsi[look_back - 1:] = 100 - 100 / (1 + rs)

        return rsi
