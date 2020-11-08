import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from src.scripts.preprocessing import utilities as util

'''
    Module responsible for plotting labeled data using the seaborn wrapper for nice plots.
'''

def plot_result_data(label_data):
    sns.set()
    fig, axes = plt.subplots(1, 1, sharex=True)
    plot = sns.lineplot(ax=axes, data=label_data, x=label_data.index, y='close', legend='brief')
    lim = axes.get_ylim()
    axes.fill_between(label_data.index.values, label_data['close'], lim[0], where=label_data['label'] == 'S',
                         color='lightcoral', interpolate=True, label="Sell region")
    axes.fill_between(label_data.index.values, label_data['close'], lim[0], where=label_data['label'] == 'B',
                         color='yellowgreen', interpolate=True, label="Buy region")
    axes.fill_between(label_data.index.values, label_data['close'], lim[0], where=label_data['label'] == 'H',
                         color='gold', interpolate=True, alpha=0.5, label="Hold region")

    plot.set(ylabel='Close price')
    axes.set_xlim(left=label_data.index.values[0], right=label_data.index.values[-1])
    axes.set_ylim(lim)

    axes.set_title('Close price and result')
    plt.xlabel('Time Index')
    fig.suptitle('Labeling using a cubic convolution window')

    handles, labels = axes.get_legend_handles_labels()
    axes.legend(handles=handles[:], labels=labels[:])

    fig.tight_layout()
    plt.show()



def plot_comp_data(label_data):
    sns.set()

    fig, axes = plt.subplots(2, 1, sharex=True)

    s1 = pd.melt(frame=label_data.reset_index(), id_vars='index', value_vars=['close', 'convolution result'])
    plot = sns.lineplot(ax=axes[0], data=s1, x='index', y='value', hue='variable', legend='brief')

    lim1 = axes[0].get_ylim()
    axes[0].fill_between(label_data.index.values, label_data['close'], lim1[0], where=label_data['label'] == 'S',
                         color='lightcoral', interpolate=True, label="Sell region")
    axes[0].fill_between(label_data.index.values, label_data['close'], lim1[0], where=label_data['label'] == 'B',
                         color='yellowgreen', interpolate=True, label="Buy region")
    axes[0].fill_between(label_data.index.values, label_data['close'], lim1[0], where=label_data['label'] == 'H',
                         color='gold', interpolate=True, alpha=0.5, label="Hold region")

    s2 = pd.melt(frame=label_data.reset_index(), id_vars='index', value_vars=['difference', 'median of difference'])
    plot = sns.lineplot(ax=axes[1], data=s2, x='index', y='value', hue='variable', legend='brief')

    lim1 = axes[0].get_ylim()
    axes[1].fill_between(label_data.index.values, label_data['difference'], 0, where=label_data['label'] == 'S',
                         color='lightcoral', interpolate=True)
    axes[1].fill_between(label_data.index.values, label_data['difference'], 0, where=label_data['label'] == 'B',
                         color='yellowgreen', interpolate=True)
    axes[1].fill_between(label_data.index.values, label_data['difference'], 0, where=label_data['label'] == 'H',
                         color='gold', interpolate=True, alpha=0.5)

    plot.set(ylabel='Close price')
    axes[0].set_xlim(left=label_data.index.values[0], right=label_data.index.values[-1])
    axes[0].set_ylim(lim1)

    axes[0].set_title('Close price and result')
    plt.xlabel('Time Index')
    fig.suptitle('Labeling using a cubic convolution window')

    for ax in axes:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=handles[:], labels=labels[:])

    fig.tight_layout()
    plt.show()



if __name__ == '__main__':
    frame = util.load_data(util.DATA_DIR)
    plot_result_data(frame)

