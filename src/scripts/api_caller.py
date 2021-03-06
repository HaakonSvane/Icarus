import datetime as dt
import time
from dateutil.relativedelta import relativedelta
import pandas as pd
import os

import config
from src.alphavantage import alpha_vantage_api as api
from src.scripts.preprocessing.utilities import *


'''
    Module responsible for making API calls to Alpha Vantage. Keeps track of files that are already fetched
    and times the calls such that the API limitations set by AV are not crossed. 
'''


def get_api_listings(save_path: str):
    '''
    Calls the AlphaVantage.get_listing_status() on still active companies. Saves the result to the specified path.

    :param str save_path: path to the
    :return: full list of companies that are listed on Alpha Vantage
    '''
    fd = api.FundamentalData()
    frame = fd.get_listing_status(state='active')
    fd.save_to_csv(frame, save_path)


def trim_listings(frame, last_n_years=2):
    '''
    Removes any companies in the listings that has and IPO date younger than two years.

    :rtype: pd.DataFrame
    :param pd.DataFrame frame: pandas DataFrame with the listings obtained from the AlphaVantage.get_listings_status() call.
    :param integer last_n_years: the number of years to look back to. Defaults to 2.
    :return: trimmed listings with companies with a IPO date older than 2 years.
    '''
    date_today = dt.datetime.today()
    frame['ipoDate'] = pd.to_datetime(frame['ipoDate'], format='%Y-%m-%d')
    frame = frame[[relativedelta(date_today, frame.ipoDate[i]).years >= 2 for i in range(frame.index.size)]]
    return frame


if __name__ == "__main__":
    path_sp = config.DATA_DIR / 'normalization' / 'listings' / 'SP500_companies.csv'
    path_all = config.DATA_DIR / 'normalization' / 'listings' / 'alpha_vantage_companies.csv'
    path_raw = config.DATA_DIR / 'normalization' / 'raw'

    companies_to_find = pd.read_csv(path_sp, index_col=None)
    all_companies = pd.read_csv(path_all, index_col=None)
    all_companies = trim_listings(all_companies)
    companies_to_find = companies_to_find[companies_to_find['Symbol'].isin(all_companies['symbol'])]

    list_c = list(companies_to_find['Symbol'])
    already_found = [d for d in path_raw.iteritems() if d.is_dir()]
    list_c = [a for a in list_c if a not in already_found]

    calls_per_min = 30
    sec_per_call = 60. / calls_per_min + 1
    ts = api.TimeSeries()

    t = time.time()
    dt = 0

    # Each day, a total of 20*24 = 480 API calls are made due to the limits set by Alpha Vantage (free key)
    for i in range(len(list_c)):
        sym = list_c[i]
        os.mkdir(path_raw / f'{sym}')
        for y in range(1, 3):
            for m in range(1, 13):
                data = ts.get_intraday_extended(f'{sym}', '15min', f'year{y}month{m}')
                ts.save_to_csv(data, path_raw / f'{sym}/{sym}_15min_y{y}m{m}.csv')
                dt = time.time() - t
                sleep_time = sec_per_call - dt if sec_per_call - dt >= 0 else 0
                print(f'\nEquity {i+1}/{len(list_c)}')
                print("Waiting for {:.2f} seconds...".format(sleep_time))
                time.sleep(sleep_time)
                t = time.time()
