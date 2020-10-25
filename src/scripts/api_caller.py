from src.alphavantage import alpha_vantage_api as api
import time

if __name__ == "__main__":
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
