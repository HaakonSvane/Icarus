import os
from functools import wraps
import requests
import inspect
import pandas as pd
import io
import re
import tabulate
import pathlib
from datetime import datetime
import json
from typing import Callable, Any


class AlphaVantage:
    '''
    Parent class of the request classes. The class contains backend decorators for shaping the requests made by
    its children.

    :param api_key: API key provided by Alpha Vantage. Note that you can set the environment variable
        ALPHAVANTAGE_API_KEY if you don't want to explicitly pass this parameter.
    :param output_format: Default request format of the files ('json' or 'csv').
        Note that some requests can not return the desired format.
    :param error_log_dir: Path to directory to save the error log file.
    :param log_errors: Whether or not to create an error log file.

    '''

    _API_URL = 'https://www.alphavantage.co/query?'

    def __init__(self, api_key: str, output_format: str, error_log_dir: str, log_errors: bool):
        if not api_key:
            api_key = os.getenv('ALPHAVANTAGE_API_KEY')

        self.log_errors = log_errors
        self.error_log_dir = error_log_dir
        self.api_key = api_key
        self.output_format = output_format.lower()

    @property
    def output_format(self) -> str:
        '''Gets the current output format.

        :return: Output format.
        '''
        return self._output_format

    @output_format.setter
    def output_format(self, of: str):
        '''Sets a new output format.

        :raises ValueError: Output format is not 'json' or 'csv'.
        :param of: New output format.
        '''
        if not (of.lower() == 'json' or of.lower() == 'csv'):
            raise ValueError('Output format must be either "json" or "csv"')
        self._output_format = of

    @property
    def api_key(self) -> str:
        '''Gets the current API key.

        :return: API key.
        '''
        return self._api_key

    @api_key.setter
    def api_key(self, key: str):
        '''Sets a new API key. This setter does not check whether or not a key is actually valid.

        :raises ValueError: No key is passed.
        :param key: New API key.
        '''
        if not key:
            raise ValueError("Could not find API key. Get one from Alpha Vantage first.")
        self._api_key = key

    @property
    def error_log_dir(self) -> pathlib.Path:
        '''Gets the current error log directory.

        :return: Path to the directory where the error log file is saved.
        '''
        return self._error_log_dir

    @error_log_dir.setter
    def error_log_dir(self, path: str):
        '''Sets a new directory to save the error log file to.

        :raises ValueError: The provided path does not exist.
        :param path: New path.
        '''
        path = pathlib.Path(path)
        if not path.exists():
            raise ValueError("The provided path does not exist. Please enter a valid path.")
        self._error_log_dir = path

    @classmethod
    def _get_arg_dict(cls, func, *args, **kwargs: dict) -> dict:
        '''Given some function/method and the arguments passed into it, this method creates a full directory
        of all the function parameters as keys and the arguments passed as values.

        :param func: Function/method to inspect.
        :return: Dictionary of all parameters and their respective arguments.
        '''
        sig = inspect.signature(func)
        # defining a dictionary with the parameters of func as keys (ignoring 'self') and default values as values
        arg_dict = {param.name: param.default for param in sig.parameters.values() if param.name is not 'self'}
        # updating the dictionary with the keyword arguments (if there are any) in the current function call
        arg_dict.update(kwargs)
        # inserting the non-keyworded arguments (args) correctly into the corresponding dictionary key
        for n, param in enumerate(arg_dict):
            if n >= len(args):
                break
            arg_dict[param] = args[n]
        return arg_dict

    @classmethod
    def _shape_request(cls, func: Callable[[str], str]) -> Callable[[Any], Any]:
        '''Decorator function to shape the request sent by any of the children classes.

        :param func: Function to be wrapped.
        :return: Wrapper for the function
        '''

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Actual wrapper. Shapes the url request from the parameters, arguments and return of the function passed.

            function_key = func(self, *args, **kwargs)
            arg_dict = AlphaVantage._get_arg_dict(func, *args, **kwargs)
            arg_dict.update({'apikey': self.api_key, 'datatype': self.output_format})
            arg_frame = pd.DataFrame.from_dict(arg_dict, orient='index', columns=['Value'])
            arg_frame.index.name = 'Parameter'

            print(f"\n\nSending a request for {function_key} with the folowing parameters:")
            print(tabulate.tabulate(arg_frame, headers='keys', tablefmt='simple'))

            req_url = f'{AlphaVantage._API_URL}function={function_key}&'
            for key, val in arg_dict.items():
                req_url += f'{key}={val}&' if val is not None else ""
            return self._get_request(req_url)

        return wrapper

    def _get_request(self, url: str) -> pd.DataFrame:
        '''
        Given some shaped url, the function sends a url request and checks its response body for data. If the response
        is not valid, it is logged in the error file.

        :param url: Shaped url to request from Alpha Vantage.
        :return: Formatted dataframe of the response body.
        '''
        df = None
        req_format = None
        data = None
        meta_data = None  # TODO: code does nothing with this atm. Maybe use this for later filenaming?

        with requests.get(url, headers={'Accept-Encoding': 'identity'}) as r:
            r.raise_for_status()
            try:
                data = r.json()
            except ValueError:
                try:
                    df = pd.read_csv(io.StringIO(r.content.decode('utf-8')), index_col=0)
                except ValueError:
                    print(f"Request failed with error message from server:\n{r.content}")
                    return
            else:
                if len(data.keys()) > 2:
                    print(
                        f'Check the response of the following url for keys:\n{url}')  # Developer insists on keeping this in case new return values arise in the future
                    return
                try:
                    meta_data = data['Meta Data']
                    del data['Meta Data']
                    key = list(data.keys())[0]
                    df = pd.DataFrame.from_dict(data[key], orient='index')
                    col_names = [re.sub(r'\d+.', '', name).strip(' ') for name in list(df)]
                    df.columns = col_names
                except KeyError:
                    if self.log_errors:
                        date = datetime.today().strftime('%Y-%m-%d')
                        err_json = None
                        try:
                            err_file = open(self.error_log_dir / 'API_ERR_LOG.json', 'r')
                            err_json = json.load(err_file)
                            err_file.close()
                        except (json.decoder.JSONDecodeError, FileNotFoundError):
                            err_json = {}

                        entry = {'time': datetime.now().strftime("%H:%M:%S"), 'url': url,
                                 'message': [{key: val} for key, val in data.items()]}
                        if date in err_json:
                            err_json[date].append(entry)
                        else:
                            err_json[date] = [entry]

                        with open(self.error_log_dir / 'API_ERR_LOG.json', 'w', encoding='utf-8') as f:
                            json.dump(err_json, f, ensure_ascii=False, indent=4)
                    return
        return df

    def save_to_csv(self, dframe: pd.DataFrame, output_path: pathlib.Path, separator: str = ',', show_ind: bool = True):
        '''
        Saves the given dataframe as a csv formatted file at the given path.

        :param pd.DataFrame dframe: dataframe to save.
        :param str output_path: path to save file.
        :param str separator: separator used in the csv file.
        :param bool show_ind: including the index of the data in the output file or not.
        '''

        dframe.to_csv(output_path, sep=separator, index=show_ind)

    def save_to_json(self, dframe: pd.DataFrame, output_path: pathlib.Path, show_ind: bool = True):
        '''
        Saves the given dataframe as a json formatted file at the given path.

        :param pd.DataFrame dframe: dataframe to save.
        :param str output_path: path to save file.
        :param bool show_ind: including the index of the data in the output file or not.
        '''

        cols_as_dict = dframe.apply(dict, axis=1)
        combined = cols_as_dict.groupby(cols_as_dict.index).apply(list)
        combined.to_json(output_path, index=show_ind, orient='index')
