import datetime as dt
import time
from dateutil.relativedelta import relativedelta
import pandas as pd
import os

from src.alphavantage import alpha_vantage_api as api
from src.scripts.preprocessing import utilities as util


def get_api_listings(save_path: str):
    fd = api.FundamentalData()
    frame = fd.get_listing_status(state='active')
    fd.save_to_csv(frame, save_path)


def trim_listings(frame, last_n_years=2):
    date_today = dt.datetime.today()
    frame['ipoDate'] = pd.to_datetime(frame['ipoDate'], format='%Y-%m-%d')
    frame = frame[[relativedelta(date_today, frame.ipoDate[i]).years >= 2 for i in range(frame.index.size)]]
    return frame


if __name__ == "__main__":
    path_sp = util.DATA_DIR / 'preprocessing' / 'listings' / 'SP500_companies.csv'
    path_all = util.DATA_DIR / 'preprocessing' / 'listings' / 'alpha_vantage_companies.csv'
    path_raw = util.DATA_DIR / 'preprocessing' / 'raw'

    companies_to_find = pd.read_csv(path_sp, index_col=None)
    all_companies = pd.read_csv(path_all, index_col=None)
    all_companies = trim_listings(all_companies)
    companies_to_find = companies_to_find[companies_to_find['Symbol'].isin(all_companies['symbol'])]

    list_c = list(companies_to_find['Symbol'])
    already_found = [d.parts[-1] for d in (util.DATA_DIR / 'preprocessing' / 'raw').glob('**/*') if d.is_dir()]
    list_c = [a for a in list_c if a not in already_found]

    calls_per_min = 5
    sec_per_call = 60./calls_per_min+1
    ts = api.TimeSeries()

    t = time.time()
    dt = 0

    # Each day, a total of 20*24 = 480 API calls are made due to the limits set by Alpha Vantage
    for i in range(20):
        sym = list_c[i]
        os.mkdir(path_raw / f'{sym}')
        for y in range(1, 3):
            for m in range(1, 13):
                data = ts.get_intraday_extended(f'{sym}', '15min', f'year{y}month{m}')
                ts.save_to_csv(data, path_raw / f'{sym}/{sym}_15min_y{y}m{m}.csv')
                dt = time.time() - t
                sleep_time = sec_per_call - dt if sec_per_call - dt >= 0 else 0
                print("Waiting for {:.2f} seconds...".format(sleep_time))
                time.sleep(sleep_time)
                t = time.time()

