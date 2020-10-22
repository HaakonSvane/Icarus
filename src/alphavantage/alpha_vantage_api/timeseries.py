from src.alphavantage.alpha_vantage_api.alphavantage import AlphaVantage
import re

class TimeSeries(AlphaVantage):
    def __init__(self, api_key=None, output_format='json'):
        super().__init__(api_key, output_format)

    @AlphaVantage._make_request
    def get_intraday(self, symbol, interval, adjusted=True, outputsize='full'):
        allowed_interval = ["1min", "5min", "15min", "30min", "60min"]
        if interval not in allowed_interval:
            raise ValueError(f'"interval" must be one of the following values:\n{allowed_interval}')
        if not isinstance(adjusted, bool):
            raise ValueError('"adjusted" must be a boolean value')
        if not (outputsize == 'full' or outputsize == 'compact'):
            raise ValueError('"outputsize" must be either "full" or "compact"')
        return "TIME_SERIES_INTRADAY"

    @AlphaVantage._make_request
    def get_intraday_extended(self, symbol, interval, slice, adjusted=True):
        allowed_interval = ["1min", "5min", "15min", "30min", "60min"]
        if interval not in allowed_interval:
            raise ValueError(f'"interval" must be one of the following values:\n{allowed_interval}')
        if not re.match(r"year[0-9]+month[0-9]{1,2}", slice):
            raise ValueError('"slice" must have the following format: year[Y|YY]month[M|MM]')
        if not isinstance(adjusted, bool):
            raise ValueError('"adjusted" must be a boolean value')
        return "TIME_SERIES_INTRADAY_EXTENDED"

    @AlphaVantage._make_request
    def get_daily(self, symbol, outputsize='full'):
        if not (outputsize == 'full' or outputsize == 'compact'):
            raise ValueError('"outputsize" must be either "full" or "compact"')
        return "TIME_SERIES_DAILY"

    @AlphaVantage._make_request
    def get_daily_adjusted(self, symbol, outputsize='full'):
        if not (outputsize == 'full' or outputsize == 'compact'):
            raise ValueError('"outputsize" must be either "full" or "compact"')
        return "TIME_SERIES_DAILY_ADJUSTED"

    @AlphaVantage._make_request
    def get_weekly(self, symbol):
        return "TIME_SERIES_WEEKLY"

    @AlphaVantage._make_request
    def get_weekly_adjusted(self, symbol):
        return "TIME_SERIES_WEEKLY_ADJUSTED"

    @AlphaVantage._make_request
    def get_monthly(self, symbol):
        return "TIME_SERIES_MONTHLY"

    @AlphaVantage._make_request
    def get_monthly_adjusted(self, symbol):
        return "TIME_SERIES_MONTHLY_ADJUSTED"

    @AlphaVantage._make_request
    def get_quote_endpoint(self, symbol):
        return "GLOBAL_QUOTE"


if __name__ == "__main__":
    ts = TimeSeries()
    ts.get_daily('IBM')
