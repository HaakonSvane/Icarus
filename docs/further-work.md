---
title: Further work
layout: page
order: 4

categories: 
    - title: What remains?
      id: remains
    - title: New ideas
      id: ideas
    - title: What is next?
      id: next
      
image: assets/img/further_work/sin_squared_rec.png
image_desc: Soft reccurence plot of the function $\sin(\frac{1}{10}x^2) + sin(\frac{1}{10}x), x\in[0,25]$.

---

<div id="remains">
</div>

## What remains?
### Parameter tuning and small changes
#### Labeler
Studying the first results from the training process, there seems to be minor differences in how the network learns for
the different company datasets. The labeler might be partly to blame for this. While tuning the labeler, a very small 
range of companies was tested. This means that the threshold values, sliding median window, smoothing factor and maybe 
even the label criteria might need some rework. A good labeler should be dynamic and robust, but verifying this is a lengthy
process and was therefore not prioritized for the first test runs [^1].

#### Normalization
Optimization of the normalization process has not yet been done. This process involves testing multiple normalization routines
and studying their result. This will become especially important in the future as the next section presents.


<div id="ideas">
</div>

## New Ideas

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

[^1]: I should clarify what is meant by "first test runs". These runs refer to the series of runs we performed before
    finalizing the university project. The project itself is by no means finished yet (I hope).