import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from typing import List

from scipy.spatial.distance import cdist
from src.preprocessing.preprocessor.prep_config import *


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
    def get_trading_hours(frame: pd.DataFrame, from_time: str = START_TRADE, to_time: str = END_TRADE):
        frame = frame.set_index('time')
        frame = frame.between_time(start_time=from_time, end_time=to_time, include_start=False, include_end=True)
        frame = frame.reset_index()
        return frame

    @staticmethod
    def show_phase_plot(frame: pd.DataFrame, ax1: str, ax2: str, ax3: str):
        '''
        Plots a 3 dimensional phase plot of the the data in the dataframe on the three axes ax1, ax2 and ax3.

        :param frame: dataframe of the data to be plotted.
        :param ax1: Name of column in axis 1.
        :param ax2: Name of column in axis 2.
        :param ax3: Name of column in axis 3.
        :return:
        '''
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(frame[ax1].values, frame[ax2].values, frame[ax3].values)
        ax.set_xlabel(ax1)
        ax.set_ylabel(ax2)
        ax.set_zlabel(ax3)
        plt.show()

    @staticmethod
    def cluster_data(frame: pd.DataFrame, min_cluster_size: int = CLUSTER_SIZE, label_col_name: str = 'label') -> List[
        pd.DataFrame]:
        '''For a dataframe with an associated labels column, this method finds all the clusters of the same labels
        with size equal or greater than min_cluster_size. Clusters are temporal regions where one and the same label
        reside. For clusters in the data that are larger than min_cluster_size, the cluster is trimmed down to this size
        with the midpoints of the untrimmed cluster corresponding to the midpoint of the trimmed.

        :param frame: DataFrame to cluster.
        :param min_cluster_size: Minimum size of the clusters.
        :param label_col_name: Name of the column to use for cluster detection. Defaults to 'label'.
        :return: A list of DataFrames where each element corresponds to one cluster. All the clusters have size
            min_cluster_size.
        '''
        clusters = frame.groupby((frame[label_col_name].shift() != frame[label_col_name]).cumsum())
        valid = (clusters.size() >= min_cluster_size)
        valid = valid.index[valid].to_numpy()

        result = []
        for i in valid:
            # Getting the indicies for frame in group i
            inds = clusters.groups[i].values

            # In the case that the cluster is bigger than min_cluster_size, we trim it down to this size
            mid = len(inds) // 2
            l_ind = mid - min_cluster_size // 2
            new_inds = inds[l_ind:l_ind + min_cluster_size]
            result.append(frame.iloc[new_inds])

        return result

    @staticmethod
    def calc_recurrence_plot(frame: pd.DataFrame, percentile: int = 2, distance_metric: str = 'euclidean',
                             smooth: bool = False, alpha: float = 10, debug_plot: bool = False) -> np.array:
        '''
        Calculates a recurrence plot (2D-array of values 0 or 1) using a metric on the phase space.
        A recurrence plot is a 2D representation of when a trajectory in phase space at time i is roughly in the same
        region at time j.


        :param frame: dataframe containing all the columns to use in the phase space.
        :param percentile:  The points that are below the nth percentile in the distance defined by the distance metric
                            will be included. Defaults to 2.
        :param distance_metric: The distance metric to use on the phase space. Defaults to 'euclidean'.
        :param smooth: Whether or not to include values that are over the nth percentile as well. These are
            exponentially mapped to a value between 1 and 0 (grayscaling). Defaults to False
        :param alpha: The factor used in the exponential mapping for values that are over the nth percentile.
            Defaults to 10.
        :param debug_plot: Whether or not to plot the resulting recurrence plot or not. For debugging and exploration.
        :return: 2D-array of the results from the recurrence plot.
        '''

        y = frame.to_numpy(dtype=np.float)
        y = y.reshape((-1,1)) if y.ndim == 1 else y
        # cdist calculates the distance from each point i to all other points j. The result is a matrix of distances
        # with zeros on the main diagonal since the distance form each point to itself is always zero.
        dist = cdist(y, y, metric=distance_metric)
        perc = np.percentile(dist, percentile)

        img = None
        if smooth:
            lin_cap = lambda d, p: np.exp(-alpha * (d - p)) if d > p else 1
            fun = np.vectorize(lin_cap, otypes=[np.float])
            img = fun(dist, perc)

        else:
            img = np.where(dist <= perc, 1, 0)

        if debug_plot:
            plt.imshow(img, cmap='Greys', origin='lower')
            plt.show()

        return img
