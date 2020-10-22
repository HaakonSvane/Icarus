import os
from functools import wraps
import requests
import inspect
import shutil


class AlphaVantage:
    _API_URL = 'https://www.alphavantage.co/query?'

    def __init__(self, api_key=None, output_format='json'):
        if not api_key:
            api_key = os.getenv('ALPHAVANTAGE_API_KEY')
        if not api_key:
            raise ValueError("Could not find API key. Get one from Alpha Vantage first.")
        if not output_format.lower() == 'json' or output_format.lower() == 'csv':
            raise ValueError('Output format must be either "json" or "csv"')

        self.key = api_key
        self.output_format = output_format.lower()

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
            req_url = f'{AlphaVantage._API_URL}function={function_key}&'
            for key, val in arg_dict.items():
                req_url += f'{key}={val}&' if val is not None else ""
            req_url += f'datatype={self.output_format}&apikey={self.key}'
            return self._get_request(req_url)
        return wrapper

    def _get_request(self, url):
        with requests.get(url, stream=True, headers={'Accept-Encoding': 'identity'}) as r:
            r.raise_for_status()
            with open('testing.csv', 'wb') as outfile:
                shutil.copyfileobj(r.raw, outfile)


