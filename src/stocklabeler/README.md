# Index Labeler
![image](images/LabelerFront.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 

[![CustomLabeler-100%](https://img.shields.io/badge/CustomLabeler-100%25-brightgreen)](https://github.com/HaakonSvane/Icarus/blob/master/src/alphavantage/alpha_vantage_api/timeseries.py)


### What is it?
This package is responsible for labeling provided stock market data with the three labels __buy__, __sell__ and __hold__. 
The script uses multiple 1D convolutions and threshold values to determine the different labels given data
of closing prices for stock indices. There is support 

#### CustomLabeler
The CustomLabeler is a labeler that was written specifically for this project. The idea behind the labeler is to use
convolutions (weighted averages) with the ability to look into future values to determine what to label a datapoint.

### How to use it:
Creating a Labeler instance requires the initialization of any of its child classes. At the current time, only CustomLabeler
has been made.

#### CustomLabeler
An example of initializing a CustomLabeler instance and using the instance to label data is shown below:

```python
from src.stocklabeler import labeler as lab
# Let "frame" represent a pandas.DataFrame containing financial data.
# Creating a CustomLabeler instance with the data in frame and a time window of 50 hours with 15 min resolution.
cl = lab.CustomLabeler(data=frame, time_window=50, data_time_col_name='time', data_price_col_name='close', dt=0.25)

# Setting the convolution window of the CustomLabeler to be a linear window (on the form ax+b) with a=2 and b=0
cl.set_conv_win_func('linear', a=2, b=0)

# Calculates the labels for the data using threshold for selling and buying = 0.5 with smooth results over 2 hours.
# The cl.calculate() also returns all computations that where used in the process determining the labels.
labeled_data = cl.calculate(thresh_buy=0.5, thresh_sell=0.5, median_size=50, smooth_result=2)

```