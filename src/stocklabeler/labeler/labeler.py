import pandas as pd

class Labeler:
    def __init__(self, data : pd.DataFrame, time_window : int, data_time_col_name : str, data_price_col_name : str):
        '''

        :param data: Pandas DataFrame containing the timeseries data. Must contain
        :param time_window: Number of hours (integer) used as the window in the convolutions.
        :param data_time_col_name: Name of the column in the DataFrame referring to the time data.
        :param data_close_col_name: Name of the column in the DataFrame referring to the price

        '''

        self.data = data
        self.time_window = time_window
        self.time_col_name = data_time_col_name
        self.price_col_name = data_price_col_name

        self.data_results = pd.DataFrame(index=data.index)
        self.data_results[self.time_col_name] = self.data[self.time_col_name]
        self.data_results[self.price_col_name] = self.data[self.price_col_name]

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, val):
        if not isinstance(val, pd.DataFrame):
            raise ValueError
        self._data = val

    @property
    def time_window(self):
        return self._time_window
    @time_window.setter
    def time_window(self, val):
        if not (val > 0 and isinstance(val, int)):
            raise ValueError("Time window must be a positive integer")
        self._time_window = val

    @property
    def time_col_name(self):
        return self._time_col_name
    @time_col_name.setter
    def time_col_name(self, val):
        if val not in self.data.columns:
            raise ValueError(f'Column name {val} does not exist in the data provided.')
        self._time_col_name = val

    @property
    def price_col_name(self):
        return self._price_col_name

    @price_col_name.setter
    def price_col_name(self, val):
        if val not in self.data.columns:
            raise ValueError(f'Column name {val} does not exist in the data provided.')
        self._price_col_name = val






