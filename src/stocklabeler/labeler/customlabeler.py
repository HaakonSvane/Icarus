from src.stocklabeler.labeler.labeler import Labeler
import pandas as pd
import numpy as np
from scipy.ndimage import convolve1d, median_filter
import inspect


class CustomLabeler(Labeler):

    class R_COLS:
        conv = 'Convolution Results'
        diff = 'Difference'
        med = 'Median of Difference'
        lab = 'Assigned Label'

    _CONV_FUNCS = {'linear': lambda a, x, b: a * x + b,
                   'poly': lambda a, x, b, c: a * np.power(x, 2) + b * x + c,
                   'qubic': lambda a, x, b, c, d: a * np.power(x, 3) + b * np.power(x, 2) + c * x + d,
                   'exp': lambda a, x, b, c: a * np.exp(b * x) + c,
                   'simple': lambda x: 0,
                   'step': lambda x: 0,
                   }

    def __init__(self, data: pd.DataFrame, time_window: int, convolution_mode='poly', data_time_col_name='time',
                 data_price_col_name='close', **kwargs):
        super().__init__(data, time_window, data_time_col_name, data_price_col_name)

        self.convolution_window = None
        self.data_results[CustomLabeler.R_COLS.conv] = np.nan
        self.data_results[CustomLabeler.R_COLS.diff] = np.nan
        self.data_results[CustomLabeler.R_COLS.med] = np.nan

    @property
    def convolution_window(self):
        return self._convolution_window
    @convolution_window.setter
    def convolution_window(self, val):
        if val is not None:
            raise ValueError("Can not set the convolution window manually. Use CustomLabeler.set_conv_win_func() "
                             "instead.")
        self._convolution_window = val


    def _calculate_conv_window(self):
        func = CustomLabeler._CONV_FUNCS[self.get_conv_win_func()['name']]
        args = {arg:val for arg, val in self.get_conv_win_func().items() if arg is not 'name'}
        x_axis = np.linspace(0, 1, super().time_window)
        win = func(**args, x=x_axis)
        self._convolution_window = win/np.sum(win)

    def get_conv_win_func(self):
        return self._conv_win_func

    def set_conv_win_func(self, name: str, **kwargs):
        if not name in CustomLabeler._CONV_FUNCS:
            raise ValueError(f'Function name "{name}" is not supported.')
        req_args = [arg for arg in inspect.signature(CustomLabeler._CONV_FUNCS[name]).parameters.keys() if arg is not 'x']
        missing_args = [x for x in req_args if x not in kwargs.keys()]
        extra_args = [x for x in kwargs.keys() if x not in req_args]
        if missing_args:
            raise ValueError(f'Missing the following argument(s): {missing_args} for function "{name}"')

        self._conv_win_func = {'name': name}
        self._conv_win_func.update(kwargs)
        for key in extra_args:
            del self._conv_win_func[key]
        self._calculate_conv_window()

    def calculate(self, conv_mode='reflect', median_mode='reflect', median_size=55):
        if self.convolution_window is None:
            raise ValueError('Convolution window not set. Use CustomLabeler.set_conv_win_func() first')

        thresh_buy = 0.1  # The relative gain needed to classify as a "buy" point
        thresh_sell = 0.1  # The relative gain needed to classify as a "sell" point


        self.data_results[CustomLabeler.R_COLS.conv] = convolve1d(self.data[self.price_col_name], np.flip(self.convolution_window), mode=conv_mode)
        self.data_results[CustomLabeler.R_COLS.diff] = self.data_results[CustomLabeler.R_COLS.conv] - self.data[self.price_col_name]
        self.data_results[CustomLabeler.R_COLS.med] = median_filter(self.data_results[CustomLabeler.R_COLS.diff], mode=median_mode, size=median_size)


        return self.data_results


