import pandas as pd
from typing import Union


class Labeler:
    class LABELS:
        buy = 'B'
        sell = 'S'
        hold = 'H'

    def __init__(self, data: pd.DataFrame, time_window: int, data_time_col_name: str, data_price_col_name: str,
                 dt: float):
        '''
        :param data: Pandas DataFrame containing the timeseries data. Must contain
        :param int time_window: Number of hours used as the window in the convolutions.
        :param data_time_col_name: Name of the column in the DataFrame referring to the time data.
        :param data_close_col_name: Name of the column in the DataFrame referring to the price
        :param dt: Resolution of data in hours. If None, this value is inferred automatically from the first to entries in the data.
        '''

        self.data = data
        self.time_col_name = data_time_col_name
        self.price_col_name = data_price_col_name
        self.data[self.time_col_name] = pd.to_datetime(self.data[self.time_col_name])
        # Delta time in hours
        if not dt:
            self.dt = abs((self.data[self.time_col_name][1] - self.data[self.time_col_name][0]).total_seconds()) / 3600
        else:
            self.dt = dt
        self.time_window = time_window
        self.data_results = pd.DataFrame(index=data.index)
        self.data_results[self.time_col_name] = self.data[self.time_col_name]
        self.data_results[self.price_col_name] = self.data[self.price_col_name]

    @property
    def data(self) -> pd.DataFrame:
        ''' Gets the data used in the calculation of the labels.

        :returns: Name of the time column.
        '''
        return self._data

    @data.setter
    def data(self, val: pd.DataFrame):
        ''' Sets the data used in the calculation of the labels.

        :param val: The data to store in the labeler.
        '''
        if not isinstance(val, pd.DataFrame):
            raise ValueError
        self._data = val

    @property
    def time_window(self) -> int:
        ''' Gets the time window used by the labeler.

        :returns: Time window.
        '''
        return self._time_window

    @time_window.setter
    def time_window(self, val: Union[int, float]):
        ''' Sets the time window used in the determination of labels.

        :param val: The number of hours for the time window.
        '''
        if not (val > 0 and isinstance(val, (int, float))):
            raise ValueError("Time window must be a positive integer")
        self._time_window = int(1 / self.dt * val)

    @property
    def time_col_name(self) -> str:
        ''' Gets the name of the time column used in the data.

        :returns: Name of the time column.
        '''
        return self._time_col_name

    @time_col_name.setter
    def time_col_name(self, val: str):
        ''' Sets name of the data column containing the time values.

        :param val: The name of the pandas DataFrame column to consider as time values.
        '''
        if val not in self.data.columns:
            raise ValueError(f'Column name {val} does not exist in the data provided.')
        self._time_col_name = val

    @property
    def price_col_name(self) -> str:
        ''' Gets the name of the price column used in the data.

        :returns: Name of the price column.
        '''
        return self._price_col_name

    @price_col_name.setter
    def price_col_name(self, val: str):
        ''' Sets name of the data column containing the price values.

        :param val: The name of the pandas DataFrame column to consider as price values.
        '''
        if val not in self.data.columns:
            raise ValueError(f'Column name {val} does not exist in the data provided.')
        self._price_col_name = val
