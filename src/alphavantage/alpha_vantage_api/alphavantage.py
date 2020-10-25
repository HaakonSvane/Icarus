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
import codecs


class AlphaVantage:
    _API_URL = 'https://www.alphavantage.co/query?'

    def __init__(self, api_key=None, output_format='csv', error_log_dir = pathlib.Path(__file__).parent.parent.absolute(), log_errors=True):
        if not api_key:
            api_key = os.getenv('ALPHAVANTAGE_API_KEY')

        self.log_errors = log_errors
        self.error_log_dir = error_log_dir
        self.api_key = api_key
        self.output_format = output_format.lower()

    @property
    def output_format(self):
        return self._output_format
    @output_format.setter
    def output_format(self, of):
        if not (of.lower() == 'json' or of.lower() == 'csv'):
            raise ValueError('Output format must be either "json" or "csv"')
        self._output_format = of

    @property
    def api_key(self):
        return self._api_key
    @api_key.setter
    def api_key(self, key):
        if not key:
            raise ValueError("Could not find API key. Get one from Alpha Vantage first.")
        self._api_key = key

    @property
    def error_log_dir(self):
        return self._error_log_dir
    @error_log_dir.setter
    def error_log_dir(self, path):
        if not pathlib.Path(path).exists():
            raise ValueError("The provided path does not exist. Please enter a valid path.")
        self._error_log_dir = path

    @classmethod
    def _get_arg_dict(cls, func, *args, **kwargs):
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
    def _shape_request(cls, func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            function_key = func(self, *args, **kwargs)
            arg_dict = AlphaVantage._get_arg_dict(func, *args, **kwargs)
            arg_dict.update({'apikey': self.api_key, 'datatype':self.output_format})
            arg_frame = pd.DataFrame.from_dict(arg_dict, orient='index', columns=['Value'])
            arg_frame.index.name ='Parameter'

            print(f"\n\nSending a request for {function_key} with the folowing parameters:")
            print(tabulate.tabulate(arg_frame, headers='keys', tablefmt='simple'))

            req_url = f'{AlphaVantage._API_URL}function={function_key}&'
            for key, val in arg_dict.items():
                req_url += f'{key}={val}&' if val is not None else ""
            return self._get_request(req_url)
        return wrapper

    def _get_request(self, url):
        df = None
        req_format = None
        data = None
        meta_data = None #TODO: code does nothing with this atm. Maybe use this for later filenaming?

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
                    print(f'Check the response of the following url for keys:\n{url}') # Developer insists on keeping this in case new return values arise in the future
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

                        entry = {'time': datetime.now().strftime("%H:%M:%S"), 'url':url, 'message': [{key:val} for key, val in data.items()]}
                        if date in err_json:
                            err_json[date].append(entry)
                        else:
                            err_json[date] = [entry]

                        with open(self.error_log_dir / 'API_ERR_LOG.json', 'w', encoding='utf-8') as f:
                            json.dump(err_json, f, ensure_ascii=False, indent=4)
                    return

        return df

    def save_to_csv(self, dframe : pd.DataFrame, output_path, separator=',', show_ind=True):
        dframe.to_csv(output_path, sep=separator, index=show_ind)

    def save_to_json(self, dframe : pd.DataFrame, output_path, show_ind=True):
        cols_as_dict = dframe.apply(dict, axis=1)
        combined = cols_as_dict.groupby(cols_as_dict.index).apply(list)
        combined.to_json(output_path, index=show_ind, orient='index')



