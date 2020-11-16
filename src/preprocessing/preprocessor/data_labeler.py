import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.preprocessing.preprocessor.prep_config import *
from src.stocklabeler import labeler as lab


class _DataLabeler:
    def __init__(self, hours_ahead: float, dt : float):
        '''
        :param hours_ahead: Number of hours to look ahead into the data when determining the label.
        :param dt: Number of hours between each datapoint in the data to be loaded.
        '''

        self.hours_ahead = hours_ahead
        self.dt = dt
        # The convolution window will be double the "look forward" value because of its symmetry.
        self.time_window = 2 * hours_ahead

    @property
    def hours_ahead(self):
        return self._hours_ahead

    @hours_ahead.setter
    def hours_ahead(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError(f'Value {val} is not valid. Must be an integer or float.')
        self._hours_ahead = val

    @property
    def dt(self):
        return self._dt

    @dt.setter
    def dt(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError(f'Value {val} is not valid. Must be an integer or float.')
        self._dt = val

    #TODO: proper docstring
    def get_labels(self, frame: pd.DataFrame, mode='custom', smooth_result: bool = True,
                   med_win_size: int = 300 - 1, return_full_computation: bool = False):
        MODES = {
            'custom': lab.CustomLabeler
        }
        '''
        Labels the data downloaded

        :return: 1D-array of labels with the same length as the number of rows in the dataframe provided.
        '''

        try:
            mode = MODES[mode]
        except KeyError:
            raise ValueError(f'Mode {mode} is not supported. Supported modes are: {MODES.keys()}.')

        labeler = mode(frame, self.time_window, dt=DT)
        labeler.set_conv_win_func(LAB_CONV_FUNC, a=1, b=0, c=0, d=0)
        computation = labeler.calculate(thresh_buy=THRESH_BUY, thresh_sell=THRESH_SELL, median_size=med_win_size,
                                        smooth_result=smooth_result)
        return computation[labeler.R_COLS.lab].values if not return_full_computation else computation

    @staticmethod
    def plot_computations(frame: pd.DataFrame):
        sns.set()

        fig, axes = plt.subplots(2, 1, sharex=True)

        s1 = pd.melt(frame=frame.reset_index(), id_vars='index', value_vars=['close', 'convolution result'])
        plot = sns.lineplot(ax=axes[0], data=s1, x='index', y='value', hue='variable', legend='brief')

        lim1 = axes[0].get_ylim()
        axes[0].fill_between(frame.index.values, frame['close'], lim1[0], where=frame['label'] == 'S',
                             color='lightcoral', interpolate=True, label="Sell region")
        axes[0].fill_between(frame.index.values, frame['close'], lim1[0], where=frame['label'] == 'B',
                             color='yellowgreen', interpolate=True, label="Buy region")
        axes[0].fill_between(frame.index.values, frame['close'], lim1[0], where=frame['label'] == 'H',
                             color='gold', interpolate=True, alpha=0.5, label="Hold region")

        s2 = pd.melt(frame=frame.reset_index(), id_vars='index', value_vars=['difference', 'median of difference'])
        plot = sns.lineplot(ax=axes[1], data=s2, x='index', y='value', hue='variable', legend='brief')

        lim1 = axes[0].get_ylim()
        axes[1].fill_between(frame.index.values, frame['difference'], 0, where=frame['label'] == 'S',
                             color='lightcoral', interpolate=True)
        axes[1].fill_between(frame.index.values, frame['difference'], 0, where=frame['label'] == 'B',
                             color='yellowgreen', interpolate=True)
        axes[1].fill_between(frame.index.values, frame['difference'], 0, where=frame['label'] == 'H',
                             color='gold', interpolate=True, alpha=0.5)

        plot.set(ylabel='Close price')
        axes[0].set_xlim(left=frame.index.values[0], right=frame.index.values[-1])
        axes[0].set_ylim(lim1)

        axes[0].set_title('Close price and result')
        plt.xlabel('Time Index')
        fig.suptitle('Labeling using a cubic convolution window')

        for ax in axes:
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles=handles[:], labels=labels[:])

        fig.tight_layout()
        plt.show()

    @staticmethod
    def plot_labels(frame: pd.DataFrame):
        sns.set()
        fig, axes = plt.subplots(1, 1, sharex=True)
        plot = sns.lineplot(ax=axes, data=frame, x=frame.index, y='close', legend='brief')
        lim = axes.get_ylim()
        axes.fill_between(frame.index.values, frame['close'], lim[0], where=frame['label'] == 'S',
                          color='lightcoral', interpolate=True, label="Sell region")
        axes.fill_between(frame.index.values, frame['close'], lim[0], where=frame['label'] == 'B',
                          color='yellowgreen', interpolate=True, label="Buy region")
        axes.fill_between(frame.index.values, frame['close'], lim[0], where=frame['label'] == 'H',
                          color='gold', interpolate=True, alpha=0.5, label="Hold region")

        plot.set(ylabel='Close price')
        axes.set_xlim(left=frame.index.values[0], right=frame.index.values[-1])
        axes.set_ylim(lim)

        axes.set_title('Close price and result')
        plt.xlabel('Time Index')
        fig.suptitle(f'Labeling using a {LAB_CONV_FUNC} convolution window')

        handles, labels = axes.get_legend_handles_labels()
        axes.legend(handles=handles[:], labels=labels[:])

        fig.tight_layout()
        plt.show()
