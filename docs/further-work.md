---
title: Further work

categories: 
    - title: What remains?
      id: remains
    - title: What is next?
      id: next
---

#
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