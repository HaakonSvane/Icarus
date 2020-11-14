import pandas as pd
from pathlib import Path


class _Utility:

    @staticmethod
    def format_time_col(frame: pd.DataFrame, time_col_name: str = 'time',
                        format: str = '%Y-%m-%d %H:%M:%S') -> pd.DataFrame:
        '''
        Formats the dataframe column with name "time_col_name" to the datetime format "format"

        :param frame: The dataframe to apply the formatting to.
        :param time_col_name: The name of the time column to apply the formatting to.
        :param format: datetime format to apply to the time column.
        :return: The input frame with the time column formatted to the specified format.
        '''
        if not isinstance(time_col_name, str):
            raise ValueError('The name of the time column to format must be a string')

        frame[time_col_name] = pd.to_datetime(frame[time_col_name], format=format)
        return frame

    @staticmethod
    def load_data(path: str) -> pd.DataFrame:
        '''
        :param pathlib.Path path: path to file to load.
        :return: loaded csv data in a pandas.DataFrame format
        '''
        frame = pd.read_csv
        return pd.read_csv(path, index_col=None)

    @staticmethod
    def load_batch_data(path: str, reverse: bool = True, format_time: bool = True) -> pd.DataFrame:
        '''
        Loads a batch of data from within the given directory and concatenates it to one single dataframe.

        :param path: Path or to directory of the equity data to load.
        :param reverse: Whether or not to column-reverse the dataframe before returning. Defaults to True.
        :param format_time: Whether or not to format the time of the time data in the frame. Defaults to True.
        :return: A concatenated dataframe of all the files. The frame is column-reversed if "reverse" is set to True.
        '''

        path = Path(path)
        sym = path.name
        frame = []
        for y in range(1, 3):
            for m in range(1, 13):
                data = _Utility.load_data(path / f'{sym}_15min_y{y}m{m}.csv')
                # In the case that we are opening an empty file
                if data.index.stop == 1:
                    continue
                else:
                    frame.append(data)
        frame = pd.concat(frame, ignore_index=True)

        if reverse:
            # Data from AV is reversed in the sense that it the first entry is the most recent in time. This code flips it.
            frame = frame.reindex(index=frame.index[::-1])
            frame = frame.reset_index(drop=True)
        if format_time:
            frame = _Utility.format_time_col(frame)
        return frame

    @staticmethod
    def get_week(frame: pd.DataFrame, week_no=1):
        '''
        :param pd.DataFrame frame: dataframe containing a YYYY-MM-DD formatted column named 'time'.
        :param int week_no: The week number to extract from the data.
        :return: pandas DataFrame with data only for the week_no specified.
        '''

        frame['time'] = pd.to_datetime(frame['time'], format='%Y-%m-%d')
        return frame[frame.time.dt.strftime('%W') == str(week_no)]

    @staticmethod
    def get_trading_hours(frame: pd.DataFrame, from_time: str = '09:30', to_time: str = '16:00'):
        frame = frame.set_index('time')
        frame = frame.between_time(start_time=from_time, end_time=to_time, include_start=False, include_end=True)
        frame = frame.reset_index()
        return frame
