---
title: Labeling
categories:
    - title: How do we label the data?
      id: howto
    - title: The labeling stages
      id: stages
    - title: Results
      id: results
      
image: assets/img/labeling/labeling_AAPL_2months.png

---
<div id="howto">
</div>

## How do we label the data?
What determines a buying point, and when is a good time to sell any shares that one is in possession of? 
Looking at a chart of stock prices, perhaps the following rule will suffice:

>For a price $P(t)$, a range $ t_i \in[t_{i,1}, t_{i,2}]$ is considered a buying region if for some time interval
$t_f \in [t_{f,1}, t_{f,2}]$ where $t_{f,1} > t_{i,2}$ the prices $P(t_f) > \alpha P(t_i)$ and vice versa for a
selling region. The constant $\alpha$ determines the threshold. 

Any prices that are not a buying point or a selling point will therefore be labeled a holding point.

CHECK THIS!
Since the determination of the labels for a point $P(t)$ requires an insight into future values
$P(t+n*\Delta t), n \in \mathbf{Z}^+$ where $\Delta t$ is the temporal resolution, the idea behind the new labeling 
algorithm is to use convolutions with a weighted window to determine how a closing price $P(t)$ compares to future 
prices. Multiple convolution windows was tried, but a cubic weighted window gave the best results. 
The results of applying this window is shown in Figure~\ref{fig:conv_cubic}. 
For a convolution window of size \texttt{WIN\_SIZE}, the \textit{look ahead} period for the labeler is
$\texttt{WIN\_SIZE}/2$. 


AND THIS!
Due to fluctuations in the stock price over small time-scales, a smoothing factor is also applied to the closing price.
This is a small simple average (flat convolution window of small size).
This is done to even out the small-scale fluctuations in the price and give more coherent label regions.

<div id="stages">
</div>

## The labeling stages 

### First stage

### Second stage

### Third stage


## Results