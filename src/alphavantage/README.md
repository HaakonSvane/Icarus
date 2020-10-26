# Alpha Vantage lightweight API
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 

[![TimeSeries-100%](https://img.shields.io/badge/TimeSeries-100%25-brightgreen)](https://github.com/HaakonSvane/Icarus/blob/master/src/alphavantage/alpha_vantage_api/timeseries.py)
[![FundamentalData-100%](https://img.shields.io/badge/FundamentalData-100%25-brightgreen)](https://github.com/HaakonSvane/Icarus/blob/master/src/alphavantage/alpha_vantage_api/fundamentaldata.py)
[![Forex-0%](https://img.shields.io/badge/Forex-0%25-red)]()
[![Cryptocurrencies-0%](https://img.shields.io/badge/Cryptocurrencies-0%25-red)]()
[![TechnicalIndicators-100%](https://img.shields.io/badge/TechnicalIndicators-100%25-brightgreen)]()
### What is it?
The package is a lightweight python wrapper for the Alpha Vantage API.
Alpha Vantage provides a range of financial data over 20 years. There are multiple categories of data available. 
The descriptions of these are fetched from their website:

* __TimeSeries__: "This suite of APIs provide global equity data in 4 different temporal resolutions: 
(1) daily, (2) weekly, (3) monthly, and (4) intraday. 
Daily, weekly, and monthly time series contain 20+ years of historical data."

* __FundamentalData__: "We offer the following set of fundamental data APIs in various temporal dimensions covering key
 financial metrics, income statements, balance sheets, cash flow, and other fundamental data points."

* __Forex__: "APIs under this section provide a wide range of data feed for realtime and historical forex (FX) rates."

* __Cryptocurrencies__: "APIs under this section provide a wide range of data feed for digital and crypto currencies
 such as Bitcoin."

* __TechnicalIndicators__: "Technical indicator APIs for a given equity or currency exchange pair, 
derived from the underlying time series based stock API and forex data. 
All indicators are calculated from adjusted time series data to eliminate artificial price/volume perturbations from
 historical split and dividend events."

### How to use the wrapper
Before running the script, it is reccomended to take a look at the API documentation for Alpha Vantage found 
[here](https://www.alphavantage.co/documentation/). Remember to make sure that all required packages are installed in
your Python environment.
In short, there are a total of 5 classes, each representing the categories listed above. After creating a class instance,
the method calls to the API is similar to that of the functions listed in the Alpha Vantage documentation. Below is an
example of a call to get daily time-series data from the TimeSeries suite and save it to a local directory using the
in-built json-csv converter in the wrapper. 

```python
from src.alphavantage import alpha_vantage_api as api

ts = api.TimeSeries(api_key='SOME_KEY', output_format='json')
dataframe = ts.get_daily(symbol = 'IBM', outputsize='full')
ts.save_to_csv(dataframe, 'PATH/TO/SAVEDIR/file.csv')
```

#### Errors
The Alpha Vantage server raises several responses in case of any abnormalities. By default, an error log is produced in _json_
format in the /alphavantage directory. The path to this error-file can be changed using the initializer keyword
*error\_log\_dir* when initializing any of the suite objects. The error file categorizes on date, and an entry in the
error file consists of the time of the error, the type of error, the url that was passed as the error occured and the
error message recieved from the Alpha Vantage server.