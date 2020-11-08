import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent.parent / 'data'






'''





'''

def load_data(path: str):
    '''
    :param pathlib.Path path: path to file to load.
    :return: loaded csv data in a pandas.DataFrame format
    '''
    return pd.read_csv(path, index_col=None)

def get_week(frame : pd.DataFrame, week_no=1):
    '''
    :param pd.DataFrame frame: dataframe containing a YYYY-MM-DD formatted column named 'time'.
    :param int week_no: The week number to extract from the data.
    :return: pandas DataFrame with data only for the week_no specified.
    '''

    frame['time'] = pd.to_datetime(frame['time'], format='%Y-%m-%d')
    return frame[frame.time.dt.strftime('%W') == str(week_no)]
