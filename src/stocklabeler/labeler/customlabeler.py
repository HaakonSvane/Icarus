from src.stocklabeler.labeler.labeler import Labeler
import pandas as pd
import numpy as np
from scipy.ndimage import convolve1d, median_filter
import inspect


class CustomLabeler(Labeler):
    # Names of the calculated dataframe columns to use.
    class R_COLS:
        conv = 'convolution result'
        diff = 'difference'
        med = 'median of difference'
        meddev = 'median deviation'
        lab = 'label'

    # Supported functions for setting the convolution window.
    _CONV_FUNCS = {'linear': lambda a, x, b: a * x + b,
                   'poly': lambda a, x, b, c: a * np.power(x, 2) + b * x + c,
                   'cubic': lambda a, x, b, c, d: a * np.power(x, 3) + b * np.power(x, 2) + c * x + d,
                   'exp': lambda a, x, b, c: a * np.exp(b * x) + c,
                   'simple': lambda x: 1,
                   'step': lambda x, x0: 0 if x < x0 else 1,
                   }

    def __init__(self, data: pd.DataFrame, time_window: int, data_time_col_name='time',
                 data_price_col_name='close', dt=None):
        super().__init__(data, time_window, data_time_col_name, data_price_col_name, dt)

        self.convolution_window = None
        self.data_results[CustomLabeler.R_COLS.conv] = np.nan
        self.data_results[CustomLabeler.R_COLS.diff] = np.nan
        self.data_results[CustomLabeler.R_COLS.med] = np.nan

    @property
    def convolution_window(self) -> np.array:
        ''' Gets the convolution window used in the labeling process.

        :returns: 1D array representing the convolution window.
        '''
        return self._convolution_window

    @convolution_window.setter
    def convolution_window(self, val: np.array):
        ''' Sets the convolution window used in the labeling process. This can NOT be set manually

        :param val: 1D-array representing the convolution window
        '''
        if val is not None:
            raise ValueError("Can not set the convolution window manually. Use CustomLabeler.set_conv_win_func() "
                             "instead.")
        self._convolution_window = val

    def _calculate_conv_window(self):
        func = CustomLabeler._CONV_FUNCS[self.get_conv_win_func()['name']]
        func = np.vectorize(func)
        args = {arg: val for arg, val in self.get_conv_win_func().items() if arg is not 'name'}
        x_axis = np.linspace(0, 1, super().time_window)
        win = func(**args, x=x_axis)
        self._convolution_window = win / np.sum(win)

    def get_conv_win_func(self):
        return self._conv_win_func

    def set_conv_win_func(self, name: str, **kwargs):
        ''' Sets and calculates the convolution window from a function and parameters.

        :param name: Name of the function. Must be a key in CustomLabeler._CONV_FUNCS
        :param kwargs: Parameters to use with the function. These are listed the lambda function values of
            CusomLabeler._CONV_FUNCS
        '''
        if not name in CustomLabeler._CONV_FUNCS:
            raise ValueError(f'Function name "{name}" is not supported.')
        # Gets the arguments required from the function from CustomLabeler._CONV_FUNCS
        req_args = [arg for arg in inspect.signature(CustomLabeler._CONV_FUNCS[name]).parameters.keys() if
                    arg is not 'x']
        missing_args = [x for x in req_args if x not in kwargs.keys()]
        extra_args = [x for x in kwargs.keys() if x not in req_args]
        if missing_args:
            raise ValueError(f'Missing the following argument(s): {missing_args} for function "{name}"')

        self._conv_win_func = {'name': name}
        self._conv_win_func.update(kwargs)
        for key in extra_args:
            del self._conv_win_func[key]
        self._calculate_conv_window()

    def calculate(self, thresh_buy=0.005, thresh_sell=0.005, conv_mode='reflect', median_mode='reflect',
                  median_size=55, smooth_result: float = 0) -> pd.DataFrame:
        ''' Calculates the labels for the DataFrame "data".

        :param thresh_buy: Relative threshold for determining a buy point. Defaults to 0.005.
        :param thresh_sell: Relative threshold for determining a sell point. Defaults to 0.005.
        :param conv_mode: scipy.ndimage.convolve1d mode for the 1D-convolution. See SciPy docs for information.
        :param median_mode: scipy.ndimage.median_filter mode for the median convolution. See SciPy docs for information.
        :param median_size: scipy.ndimage.median_filter size of window. Must be an odd integer.
            See SciPy docs for information.
        :param smooth_result: The number of hours to smooth the price data before checking threshold. Defaults to 0
            (no smoothing).
        :return: A dataframe with all the intermediate computations, the price column and the calculated label column.
        '''
        if self.convolution_window is None:
            raise ValueError('Convolution window not set. Use CustomLabeler.set_conv_win_func() first')

        self.data_results[self.R_COLS.conv] = convolve1d(self.data[self.price_col_name],
                                                         np.flip(self.convolution_window), mode=conv_mode)
        dat = None
        if smooth_result != 0:  # Computes a running average over smooth_result hours to smooth the price data
            l = int(1 / self.dt) * smooth_result
            dat = convolve1d(self.data[self.price_col_name], [1 / l] * l)
        else:
            dat = self.data[self.price_col_name]

        self.data_results[self.R_COLS.diff] = self.data_results[self.R_COLS.conv] - dat
        self.data_results[self.R_COLS.med] = median_filter(self.data_results[self.R_COLS.diff],
                                                           mode=median_mode, size=median_size)
        self.data_results[self.R_COLS.meddev] = self.data_results[self.R_COLS.diff] - \
                                                self.data_results[self.R_COLS.med]

        arr = self.data_results[self.R_COLS.meddev] / self.data_results[self.price_col_name]
        lab = np.empty(arr.shape, dtype=str)
        lab[arr >= thresh_buy] = Labeler.LABELS.buy
        lab[arr <= -thresh_sell] = Labeler.LABELS.sell
        lab[np.logical_and(arr < thresh_buy, arr > -thresh_sell)] = Labeler.LABELS.hold

        self.data_results[self.R_COLS.lab] = lab

        return self.data_results
