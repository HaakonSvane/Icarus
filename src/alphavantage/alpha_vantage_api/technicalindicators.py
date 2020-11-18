from src.alphavantage.alpha_vantage_api.alphavantage import AlphaVantage
from functools import wraps
import pathlib
from typing import Callable, Any


def _validate_args(func: Callable[[str], str]) -> Callable[[Any], Any]:
    '''Decorator function to validate the arguments passed to a TechnicalIndicator method.

    :param func: TechnicalIndicator method to be validated.
    :raises ValueError: One or more arguments failed validation.
    '''
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Actual wrapper. Validates the arguments from the parameter function dictionary
        # TechnicalIndicators._ARG_RESTRICTIONS.
        func(self, *args, **kwargs)
        arg_dict = AlphaVantage._get_arg_dict(func, *args, **kwargs)
        for key, val in arg_dict.items():
            if not TechnicalIndicators._ARG_RESTRICTIONS[key](val):
                raise ValueError(f"Value of {key} is invalid! Check the documentation for requirement.")
        return func(self, *args, **kwargs)
    return wrapper

def is_positive_integer(x : int) -> bool:
    '''Checks whether or not the argument is a positive integer.

    :param x: Value to be validated.
    :return: Boolean value of the truth value.
    '''
    return isinstance(x, int) and x > 0

def is_positive_float(x : float) -> bool:
    '''Checks whether or not the argument is a positive floating point number.

    :param x: Value to be validated.
    :return: Boolean value of the truth value.
    '''
    return isinstance(x, float) and x > 0

class TechnicalIndicators(AlphaVantage):

    '''
    Class for calling the Alpha Vantage Technical indicators class.

    :param api_key: API key provided by Alpha Vantage. Note that you can set the environment variable
        ALPHAVANTAGE_API_KEY if you don't want to explicitly pass this parameter. Defaults to None.
    :param output_format: Default request format of the files ('json' or 'csv').
        Note that some requests can not return the desired format. Defaults to 'json'.
    :param error_log_dir: Path to directory to save the error log file. Defaults to the package directory.
    :param log_errors: Whether or not to create an error log file. Defaults to True

    '''

    # Restrictions to all arguments in the call methods. Each value is a boolean lambda function that returns False for
    # invalid values.
    _ARG_RESTRICTIONS = {
        'symbol': lambda var: isinstance(var, str),
        'interval': lambda var: var in ["1min", "5min", "15min", "30min", "60min", 'daily', 'weekly', 'monthly'],
        'time_period': is_positive_integer,
        'series_type': lambda var: var in ['close', 'open', 'high', 'low'],
        'fastlimit': is_positive_float,
        'slowlimit': is_positive_float,
        'fastperiod': is_positive_integer,
        'slowperiod': is_positive_integer,
        'signalperiod': is_positive_integer,
        'fastmatype': lambda var: isinstance(var, int) and 0 <= var <= 8,
        'slowmatype': lambda var: isinstance(var, int) and 0 <= var <= 8,
        'signalmatype': lambda var: isinstance(var, int) and 0 <= var <= 8,
        'fastkperiod': is_positive_integer,
        'slowkperiod': is_positive_integer,
        'slowdperiod': is_positive_integer,
        'slowkmatype': lambda var: isinstance(var, int) and 0 <= var <= 8,
        'slowdmatype': lambda var: isinstance(var, int) and 0 <= var <= 8,
        'matype': lambda var: isinstance(var, int) and 0 <= var <= 8,
        'nbdevup': is_positive_integer,
        'nbdevdn': is_positive_integer,
        'acceleration': is_positive_float,
        'maximum': is_positive_float
    }

    def __init__(self, api_key=None, output_format='json',
                 error_log_dir=pathlib.Path(__file__).parent.parent.absolute(), log_errors=True):
        super().__init__(api_key, output_format, error_log_dir, log_errors)

    @AlphaVantage._shape_request
    @_validate_args
    def SMA(self, symbol, interval, time_period, series_type):
        return "SMA"

    @AlphaVantage._shape_request
    @_validate_args
    def EMA(self, symbol, interval, time_period, series_type):
        return "EMA"

    @AlphaVantage._shape_request
    @_validate_args
    def WMA(self, symbol, interval, time_period, series_type):
        return "WMA"

    @AlphaVantage._shape_request
    @_validate_args
    def DEMA(self, symbol, interval, time_period, series_type):
        return "DEMA"

    @AlphaVantage._shape_request
    @_validate_args
    def TEMA(self, symbol, interval, time_period, series_type):
        return "TEMA"

    @AlphaVantage._shape_request
    @_validate_args
    def TRIMA(self, symbol, interval, time_period, series_type):
        return "TRIMA"

    @AlphaVantage._shape_request
    @_validate_args
    def KAMA(self, symbol, interval, time_period, series_type):
        return "KAMA"

    @AlphaVantage._shape_request
    @_validate_args
    def MAMA(self, symbol, interval, series_type, fastlimit=0.01, slowlimit=0.01):
        return "MAMA"

    @AlphaVantage._shape_request
    @_validate_args
    def VWAP(self, symbol, interval):
        return "VWAP"

    @AlphaVantage._shape_request
    @_validate_args
    def T3(self, symbol, interval, time_period, series_type):
        return "T3"

    @AlphaVantage._shape_request
    @_validate_args
    def MACD(self, symbol, interval, series_type, fastperiod=12, slowperiod=26, signalperiod=9):
        return "MACD"

    @AlphaVantage._shape_request
    @_validate_args
    def MACDEXT(self, symbol, interval, series_type, fastperiod=12, slowperiod=26, signalperiod=9, fastmatype=0, slowmatype=0, signalmatype=0):
        return "MACDEXT"

    @AlphaVantage._shape_request
    @_validate_args
    def STOCH(self, symbol, interval, fastkperiod=5, slowkperiod=3, slowdperiod=3, slowkmatype=0, slowdmatype=0):
        return "STOCH"

    @AlphaVantage._shape_request
    @_validate_args
    def STOCHF(self, symbol, interval, fastkperiod=5, fastdperiod=3, fastdmatype=0):
        return "STOCHF"

    @AlphaVantage._shape_request
    @_validate_args
    def RSI(self, symbol, interval, time_period, series_type):
        return "RSI"

    @AlphaVantage._shape_request
    @_validate_args
    def STOCHRSI(self, symbol, interval, time_period, series_type, fastkperiod=5, fastdperiod=3, fasrtdmatype=0):
        return "STOCHRSI"

    @AlphaVantage._shape_request
    @_validate_args
    def WILLR(self, symbol, interval, time_period):
        return "WILLR"

    @AlphaVantage._shape_request
    @_validate_args
    def ADX(self, symbol, interval, time_period):
        return "ADX"

    @AlphaVantage._shape_request
    @_validate_args
    def ADXR(self, symbol, interval, time_period):
        return "ADXR"

    @AlphaVantage._shape_request
    @_validate_args
    def APO(self, symbol, interval, series_type, fastperiod=12, slowperiod=26, matype=0):
        return "APO"

    @AlphaVantage._shape_request
    @_validate_args
    def PPO(self, symbol, interval, series_type, fastperiod=12, slowperiod=26, matype=0):
        return "PPO"

    @AlphaVantage._shape_request
    @_validate_args
    def MOM(self, symbol, interval, time_period, series_type):
        return "MOM"

    @AlphaVantage._shape_request
    @_validate_args
    def BOP(self, symbol, interval):
        return "BOP"

    @AlphaVantage._shape_request
    @_validate_args
    def CCI(self, symbol, interval, time_period):
        return "CCI"

    @AlphaVantage._shape_request
    @_validate_args
    def CMO(self, symbol, interval, time_period, series_type):
        return "CMO"

    @AlphaVantage._shape_request
    @_validate_args
    def ROC(self, symbol, interval, time_period, series_type):
        return "ROC"

    @AlphaVantage._shape_request
    @_validate_args
    def ROCR(self, symbol, interval, time_period, series_type):
        return "ROCR"

    @AlphaVantage._shape_request
    @_validate_args
    def AROON(self, symbol, interval, time_period):
        return "AROON"

    @AlphaVantage._shape_request
    @_validate_args
    def AROONOSC(self, symbol, interval, time_period):
        return "AROONOSC"

    @AlphaVantage._shape_request
    @_validate_args
    def MFI(self, symbol, interval, time_period):
        return "MFI"

    @AlphaVantage._shape_request
    @_validate_args
    def TRIX(self, symbol, interval, time_period, series_type):
        return "TRIX"

    @AlphaVantage._shape_request
    @_validate_args
    def ULTOSC(self, symbol, interval, time_period1=7, timeperiod2=14, timeperiod3=28):
        return "ULTOSC"

    @AlphaVantage._shape_request
    @_validate_args
    def DX(self, symbol, interval, time_period):
        return "DX"

    @AlphaVantage._shape_request
    @_validate_args
    def MINUS_DI(self, symbol, interval, time_period):
        return "MINUS_DI"

    @AlphaVantage._shape_request
    @_validate_args
    def PLUS_DI(self, symbol, interval, time_period):
        return "PLUS_DI"

    @AlphaVantage._shape_request
    @_validate_args
    def MINUS_DM(self, symbol, interval, time_period):
        return "MINUS_DM"

    @AlphaVantage._shape_request
    @_validate_args
    def PLUS_DM(self, symbol, interval, time_period):
        return "PLUS_DM"

    @AlphaVantage._shape_request
    @_validate_args
    def BBANDS(self, symbol, interval, time_period, series_type, nbdevup=2, nbdevdn=2, matype=0):
        return "BBANDS"

    @AlphaVantage._shape_request
    @_validate_args
    def MIDPOINT(self, symbol, interval, time_period, series_type):
        return "MIDPOINT"

    @AlphaVantage._shape_request
    @_validate_args
    def MIDPRICE(self, symbol, interval, time_period):
        return "MIDPRICE"

    @AlphaVantage._shape_request
    @_validate_args
    def SAR(self, symbol, interval, acceleration=0.01, maximum=0.20):
        return "SAR"

    @AlphaVantage._shape_request
    @_validate_args
    def TRANGE(self, symbol, interval):
        return "TRANGE"

    @AlphaVantage._shape_request
    @_validate_args
    def ATR(self, symbol, interval, time_period):
        return "ATR"

    @AlphaVantage._shape_request
    @_validate_args
    def NATR(self, symbol, interval, time_period):
        return "NATR"

    @AlphaVantage._shape_request
    @_validate_args
    def AD(self, symbol, interval):
        return "AD"

    @AlphaVantage._shape_request
    @_validate_args
    def ADOSC(self, symbol, interval, fastperiod=3, slowperiod=10):
        return "ADOSC"

    @AlphaVantage._shape_request
    @_validate_args
    def OBV(self, symbol, interval):
        return "OBV"

    @AlphaVantage._shape_request
    @_validate_args
    def HT_TRENDLINE(self, symbol, interval, time_period, series_type):
        return "HT_TRENDLINE"

    @AlphaVantage._shape_request
    @_validate_args
    def HT_SINE(self, symbol, interval, time_period, series_type):
        return "HT_SINE"

    @AlphaVantage._shape_request
    @_validate_args
    def HT_TRENDMODE(self, symbol, interval, time_period, series_type):
        return "HT_TRENDMODE"

    @AlphaVantage._shape_request
    @_validate_args
    def HT_DCPERIOD(self, symbol, interval, time_period, series_type):
        return "HT_DCPERIOD"

    @AlphaVantage._shape_request
    @_validate_args
    def HT_DCPHASE(self, symbol, interval, time_period, series_type):
        return "HT_DCPHASE"

    @AlphaVantage._shape_request
    @_validate_args
    def HT_PHASOR(self, symbol, interval, time_period, series_type):
        return "HT_PHASOR"
