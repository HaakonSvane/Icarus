# Preprocessor:
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 

### What is it?
This package is responsible for implementing all the computations that are used in the preprocessing stage
of the data.

The data goes through multiple stages of processing using this package. The general workflow is as follows:
1. Raw data gets loaded into memory.
2. The data is trimmed down to normal working hours (09:30-16:00) since some of the equities list before/after-hour trading.
3. The stocklabeler labels the data.
4. The dimensions of the datapoints are normalized.
5. Data is saved.

For generating the 2D images that are used in the convolutional neural network, the normalized phase space of the data
is used in recurrence plots.
 
### Window size:
The labeler uses "future" datapoints P(t+n*dt) to determine the label for a datapoint P(t).
In practice, this is done using one or several convolutions depending on which labeling mode is used. Since the label is the only feature we
wish to use future data to determine, the rest of the processing pipeline (normalization, RSI, ...) MUST be restricted to previous datapoints P(t-n*dt).
Because of the nature of discrete non-shifted convolutions, for any datapoint P(t), values that are *window_size*/2 points
away from the point in both directions are used. This means that for a window of 2 days, the labeler will look forward 1 day
(and also 1 day backwards) when determining the label.

The choice of window size determines not only the investment period that we wish to train our network on, but also the 
results of technical indicators (such as RSI). If we set the window size to a 6 month period, we would target larger patterns than
if we set it to 3 days since a bigger window would smooth out any small disturbances that are not relevant to this period.

### Parameters
All the parameters used in the preprocessing stage can be found in the config file for this package.
Below is a table of explanations and values used for the preprocessing:

|Parameter      |Value  |Description                                        |
|:---|:---:|:---:|
|HOURS_AHEAD    |150    |Hours ahead used to determine the label points.    |
|HOURS_BEHIND   |150    |Hours behind used in normalization.                |
|THRESH_BUY     |0.015  |Threshold for determining a buy point.             |
|THRESH_SELL    |0.015  |Threshold for determining a sell point.            | 
|MED_WIN        |299    |Walking median window size for the custom labeler. |


    