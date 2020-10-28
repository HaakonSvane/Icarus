# Index Labeler
![image](images/LabelerFront.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 

[![CustomLabeler-100%](https://img.shields.io/badge/CustomLabeler-100%25-brightgreen)](https://github.com/HaakonSvane/Icarus/blob/master/src/alphavantage/alpha_vantage_api/timeseries.py)


### What is it?

This package is responsible for labeling provided stock market data with the three labels __buy__, __sell__ and __hold__. 
The script uses multiple 1D convolutions and threshold values to determine the different labels given data
of closing prices for stock indices. 