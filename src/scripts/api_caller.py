from src.alphavantage import alpha_vantage_api as api
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

from src.stocklabeler import labeler as lab


def load_listings(path: str):
    return pd.read_csv(path, index_col=None)


def get_api_listings(save_path: str):
    fd = api.FundamentalData()
    frame = fd.get_listing_status(state='active')
    fd.save_to_csv(frame, save_path)


def trim_listings(frame, last_n_years=2):
    date_today = dt.datetime.today()
    frame['ipoDate'] = pd.to_datetime(frame['ipoDate'], format='%Y-%m-%d')
    frame = frame[[relativedelta(date_today, frame.ipoDate[i]).years >= 2 for i in range(frame.index.size)]]
    return frame


def get_week(frame, week_no=1):
    frame['time'] = pd.to_datetime(frame['time'], format='%Y-%m-%d')
    return frame[frame.time.dt.strftime('%W') == str(week_no)]


def get_labels():
    pass


if __name__ == "__main__":
    local_path = 'listings.csv'
    # get_api_listings(local_path)
    # frame_api = load_listings(local_path)
    # frame_sp500 = load_listings('SP500_companies.csv')
    # frame_api = trim_listings(frame_api, last_n_years=2)
    ts = api.TimeSeries()

    f_1min = load_listings('IBM_1min.csv')
    f_15min = load_listings('IBM_15min.csv')
    win_size = int(240 * 4 / 15)

    frame = get_week(f_15min, 41)

    l_lin = lab.CustomLabeler(frame, win_size)
    l_lin.set_conv_win_func('linear', a=1, b=0)
    lin_lab = l_lin.calculate()

    l_poly = lab.CustomLabeler(frame, win_size)
    l_poly.set_conv_win_func('poly', a=1, b=0, c=0)
    poly_lab = l_poly.calculate()

    l_cub = lab.CustomLabeler(frame, win_size)
    l_cub.set_conv_win_func('qubic', a=1, b=0, c=0, d=0)
    cubic_lab = l_cub.calculate()

    l_exp = lab.CustomLabeler(frame, win_size)
    l_exp.set_conv_win_func('exp', a=1, b=0, c=0)
    exp_lab = l_poly.calculate()

    sns.set()

    fig, axes = plt.subplots(1, 1, sharex=False)


    s3 = exp_lab[lab.CustomLabeler.R_COLS.diff] - exp_lab[lab.CustomLabeler.R_COLS.med]
    lin_plot3 = sns.lineplot(ax=axes, data=s3, legend='brief')

    l_arr = s3.values / exp_lab['close']
    buy = axes.fill_between(s3.index, s3.values, 0,
                         where= l_arr >= 0.005, facecolor='yellowgreen', interpolate=True, label='buy')
    sell = axes.fill_between(s3.index, s3.values, 0,
                         where= l_arr <= -0.005, facecolor='lightcoral', interpolate=True, label='sell')

    hold = axes.fill_between(s3.index, s3.values, 0,
                         where= np.logical_and(l_arr >= -0.005, l_arr <= 0.005),
                         facecolor='gold', interpolate=True, label='HOLD')



    lin_plot3.set(ylabel='Close price')


    axes.set_title('Median deviation of difference between convolution and close price with threshold values')
    plt.xlabel('Time Index')
    fig.suptitle('Labeling using a exponential convolution window')

    handles, labels = axes.get_legend_handles_labels()
    axes.legend(handles=handles[:], labels=labels[:])

    fig.tight_layout()
    plt.show()

    '''
    calls_per_min = 5
    sec_per_call = 60./calls_per_min+1
    ts = api.TimeSeries()

    t = time.time()
    dt = 0

    for i in range(10):
        ts.get_daily('IBM')

        if i != 9:
            dt = time.time() - t
            sleep_time = sec_per_call - dt if sec_per_call - dt >= 0 else 0
            print("Waiting for {:.2f} seconds...".format(sleep_time))
            time.sleep(sleep_time)
            t = time.time()
    '''
