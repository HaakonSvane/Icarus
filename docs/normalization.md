---
title: Preprocessing
layout: page
image: assets/img/normalization/normalization_all_AAPL.png
image_desc: Normalization of the datapoint variables.
categories:
    - title: Window size
      id: winsize
    - title: Parameters
      id: parameters 
    - title: Normalization
      id: normalization
---



## Pipeline
The preprocessing pipeline consists of several stages. After the data has been [sourced](data-sourcing.md),
it is processed through a series of  


<div id="winsize">
</div>

### Window size:
The labeler uses "future" datapoints $$P(t+ndt)$$ to determine the label for a datapoint *P(t)*.
In practice, this is done using one or several convolutions depending on which labeling mode is used. Since the label is the only feature we
wish to use future data to determine, the rest of the processing pipeline (normalization, RSI, ...) MUST be restricted to previous datapoints P(t-n*dt).
Because of the nature of discrete non-shifted convolutions, for any datapoint *P(t)*, values that are *window_size*/2 points
away from the point in both directions are used. This means that for a window of 2 days, the labeler will look forward 1 day
(and also 1 day backwards) when determining the label.

The choice of window size determines not only the investment period that we wish to train our network on, but also the
results of technical indicators (such as RSI). If we set the window size to a 6 month period, we would target larger patterns than
if we set it to 3 days since a bigger window would smooth out any small disturbances that are not relevant to this period.

<div id="parameters">
</div>

### Parameters
All the parameters used in the preprocessing stage can be found in the *prep_config.py* file for this package.
Below is a table of explanations and values used for the preprocessing:

|Parameter      |Value  |Description                                                                                                            |
|:---|:---:|:---:|
|DT             |0.25       |Number of hours between each datapoint in the raw data.                                                            |
|LAB_CONV_FUNC  |'cubic'    |The convolution window to use for the labeler.                                                                     |
|HOURS_AHEAD    |150        |Hours ahead used to determine the label points.                                                                    |
|HOURS_BEHIND   |150        |Hours behind used in normalization.                                                                                |
|THRESH_BUY     |0.015      |Threshold for determining a buy point.                                                                             |
|THRESH_SELL    |0.015      |Threshold for determining a sell point.                                                                            |
|MED_WIN        |299        |Walking median window size for the custom labeler.                                                                 |
|START_TRADE    |'09:30'    |Trading hours open time.                                                                                           |
|END_TRADE      |'16:00'    |Trading hours close time.                                                                                          |
|CLUSTER_SIZE   |26         |Minimum size of the clusters to consider. The size n will result in images of size n x n.                          |
|REC_PERC       |10         |nth percentile for which distances in the phase plot fall under are considered in the recurrence plot.             |
|REC_DIST_MET   |'euclidean'|Distance metric to use in the recurrence plots.                                                                    |
|REC_ALPHA      |15         | Factor used in the exponential grayscale mapping of the distances over the nth percentile in the recurrence plot. |

<div id="normalization">
</div>

### Normalization
Normalizing the data before feeding it into the neural network can increase the performance of the network.
Financial data can be hard to normalize, and there are many approaches to take when doing so. First comes the determination
of *what* to normalize, then comes the determination of how to normalize it. We could for example choose to normalize the
closing price of a stock *C(t)* for some time *t*, but we would then need to determine how this is to be normalized.
Extra care must also be taken so that no future information is incorporated into the normalizattion process.

Normalization can have severe effects on the performance of networks. In
[Efficient approach to Normalization of Multimodal Biometric Scores](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.259.2703&rep=rep1&type=pdf),
the authors present multiple methods and the effects on them in neural networks. A popular normalization method is the
*modified tanh* estimator. This has the advantage of using the standard deviation and mean of the dataset instead of using
the [Hampel estimators](https://en.wikipedia.org/wiki/Redescending_M-estimator). It is thus faster and simpler than
the normal tanh estimator, but has the same qualities such as robustness.

The modified tanh normalizer was again modified to yield an output range of \[-1, 1\].
This results in a mean of 0 and points within one standard deviation at values around \[0.05, 0.05\]. This new
*modified modified* tanh normalizer (name pending) was used on all the data except for the RSI value which was divided
by 100 to clamp it to the same interval as the other variables.

### Clustering
In order to convert the time-series data to images of the same resolution, successive data points with the same label
are clustered together. Trimming all the clusters of size greater than *CLUSTER_SIZE* down to this value around their
midpoint and discarding the rest, leaves clusters of equal size with the same label for all data points within.

### Recurrence plots
For the 2D convolutional neural network, [recurrence plots](https://en.wikipedia.org/wiki/Recurrence_plot) where created
from the equally partitioned clusters of data. The idea is to have the network find patterns in the different regions
which can be generalized during training. Visually inspecting the recurrence plots generated in this process seem to
indicate that the data resembles the characteristics of brownian motion. This is expected, but not appreciated.

There are two datasets created from the recurrence plots:
1. **Hard recurrence**: This is the normal recurrence plot. Phase space distances below the nth percentile are shown as
black pixels in the images. The rest are white.
2. **Soft recurrence**: This is a proposed modification to the normal recurrence plots. Phase space distances below the nth percentile are shown as
black pixels, while values over the nth percentile are exponentially mapped to values in the range \[1, 0\] where 1 is a black pixel and 0
is a white pixel. This incorporates more information into the recurrence plot, but the significance of it has yet to be tested.


Below are examples of how these plots differ. The dataset used is 125 hours (500 datapoints) of AAPL stock, year 2018:

![](images/AAPL_HARD.png)   |  ![](images/AAPL_SOFT.png)
:-------------------------: | :-------------------------:
Hard recurrence             |  Soft recurrence
