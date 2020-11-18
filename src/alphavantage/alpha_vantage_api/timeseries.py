from src.alphavantage.alpha_vantage_api.alphavantage import AlphaVantage
import pathlib
import re


class TimeSeries(AlphaVantage):
    '''
    Class for calling the Alpha Vantage Time series class.

    :param api_key: API key provided by Alpha Vantage. Note that you can set the environment variable
        ALPHAVANTAGE_API_KEY if you don't want to explicitly pass this parameter. Defaults to None.
    :param output_format: Default request format of the files ('json' or 'csv').
        Note that some requests can not return the desired format. Defaults to 'json'.
    :param error_log_dir: Path to directory to save the error log file. Defaults to the package directory.
    :param log_errors: Whether or not to create an error log file. Defaults to True

    '''

    def __init__(self, api_key=None, output_format='json',
                 error_log_dir=pathlib.Path(__file__).parent.parent.absolute(), log_errors=True):
        super().__init__(api_key, output_format, error_log_dir, log_errors)

    @AlphaVantage._shape_request
    def get_intraday(self, symbol, interval, adjusted=True, outputsize='full'):
        allowed_interval = ["1min", "5min", "15min", "30min", "60min"]
        if interval not in allowed_interval:
            raise ValueError(f'"interval" must be one of the following values:\n{allowed_interval}')
        if not isinstance(adjusted, bool):
            raise ValueError('"adjusted" must be a boolean value')
        if not (outputsize == 'full' or outputsize == 'compact'):
            raise ValueError('"outputsize" must be either "full" or "compact"')
        return "TIME_SERIES_INTRADAY"

    @AlphaVantage._shape_request
    def get_intraday_extended(self, symbol, interval, slice, adjusted=True):
        allowed_interval = ["1min", "5min", "15min", "30min", "60min"]
        if interval not in allowed_interval:
            raise ValueError(f'"interval" must be one of the following values:\n{allowed_interval}')
        if not re.match(r"year[0-9]+month[0-9]{1,2}", slice):
            raise ValueError('"slice" must have the following format: year[Y|YY]month[M|MM]')
        if not isinstance(adjusted, bool):
            raise ValueError('"adjusted" must be a boolean value')
        return "TIME_SERIES_INTRADAY_EXTENDED"

    @AlphaVantage._shape_request
    def get_daily(self, symbol, outputsize='full'):
        if not (outputsize == 'full' or outputsize == 'compact'):
            raise ValueError('"outputsize" must be either "full" or "compact"')
        return "TIME_SERIES_DAILY"

    @AlphaVantage._shape_request
    def get_daily_adjusted(self, symbol, outputsize='full'):
        if not (outputsize == 'full' or outputsize == 'compact'):
            raise ValueError('"outputsize" must be either "full" or "compact"')
        return "TIME_SERIES_DAILY_ADJUSTED"

    @AlphaVantage._shape_request
    def get_weekly(self, symbol):
        return "TIME_SERIES_WEEKLY"

    @AlphaVantage._shape_request
    def get_weekly_adjusted(self, symbol):
        return "TIME_SERIES_WEEKLY_ADJUSTED"

    @AlphaVantage._shape_request
    def get_monthly(self, symbol):
        return "TIME_SERIES_MONTHLY"

    @AlphaVantage._shape_request
    def get_monthly_adjusted(self, symbol):
        return "TIME_SERIES_MONTHLY_ADJUSTED"

    @AlphaVantage._shape_request
    def get_quote_endpoint(self, symbol):
        return "GLOBAL_QUOTE"


if __name__ == "__main__":
    ts = TimeSeries()
    ts.get_intraday_extended("IBM", "1min", 'year1month1', True)
