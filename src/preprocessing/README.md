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
5. The data is saved as a csv file in data/training.
6. The data is clustered to each of the three labels.
7. Label clusters smaller than 

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
All the parameters used in the preprocessing stage can be found in the *prep_config.py* file for this package.
Below is a table of explanations and values used for the preprocessing:

|Parameter      |Value  |Description                                            |
|:---|:---:|:---:|
|DT             |0.25   |Number of hours between each datapoint in the raw data.|
|LAB_CONV_FUNC  |'cubic'|The convolution window to use for the labeler.         |
|HOURS_AHEAD    |150    |Hours ahead used to determine the label points.        |
|HOURS_BEHIND   |150    |Hours behind used in normalization.                    |
|THRESH_BUY     |0.015  |Threshold for determining a buy point.                 |
|THRESH_SELL    |0.015  |Threshold for determining a sell point.                | 
|MED_WIN        |299    |Walking median window size for the custom labeler.     |
|START_TRADE    |'09:30'|Trading hours open time.                               |
|END_TRADE      |'16:00'|Trading hours close time.                              |
|CLUSTER_SIZE   |130    |Minimum size of the clusters to consider.              |

### Normalization
Normalizing the data before feeding it into the neural network can increase the performance of the network. 
Financial data can be hard to normalize, and there are many approaches to take when doing so. First comes the determination
of *what* to normalize, then comes the determination of how to normalize it. We could for example choose to normalize the
closing price of a stock C(t) for some time t, but we would then need to determine

Normalization can have severe effects on the performance of networks. In 
[Efficient approach to Normalization of Multimodal Biometric Scores](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.259.2703&rep=rep1&type=pdf),
the authors present multiple methods and the effects on them in neural networks. A popular normalization method is the
*modified tanh* estimator. This has the advantage of using the standard deviation and mean of the dataset instead of using
the [Hampel estimators](https://en.wikipedia.org/wiki/Redescending_M-estimator). It is thus faster and simpler than
the normal tanh estimator, but has the same qualities such as robustness.

    