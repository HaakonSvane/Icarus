---
title: Labeling
layout: page
order: 2

categories:
    - title: How do we label the data?
      id: howto
    - title: The labeling stages
      id: stages
    - title: Results
      id: results
      
image: assets/img/labeling/labeling_AAPL_2months.png
image_desc: Some description.

---
<div id="howto">
</div>

## How do we label the data?
What determines a buying point, and when is a good time to sell any shares that one is in possession of? 
Looking at a chart of stock prices, perhaps the following rule will suffice:

>For a price $P(t)$, a range $ t_i \in[t_{i,1}, t_{i,2}]$ is considered a buying region if for some time interval
>$t_f \in [t_{f,1}, t_{f,2}]$ where $t_{f,1} > t_{i,2}$, the prices $P(t_f) > \alpha P(t_i)$ for all $t_i, t_f$ and vice versa for a
>selling region. The constant $\alpha$ determines the $\textit{threshold}$ value for buying/selling. 

Any prices that are not a buying point or a selling point will therefore be labeled a holding point.

### Why not just buy or sell all the time?
In theory, a stock price could remain flat for its entire lifespan. In practice however, it often fluctuates in a
(pseudo)random[^1] fashion. Why do we need *hold* regions then?

This might seem like a stupid question to begin with, but when trying to define what a buying and selling point is,
this question requires attention. From a pragmatic perspective, the determination of a hold point is perhaps trivial:
>If for some buying region $\mathbf{B}$, a sale of any potential holdings in a following temporal region $\mathbf{H}$ does 
>not yield any financial gains or losses, the region $\mathbf{H}$ is a holding region.

The only issue with this definition is that it very seldom happens that the net gain after a sale is **exactly** zero.
If there are *any* financial gains associated with selling from a certain position, surely we should sell here?

Let us try another perspective. Let's imagine that you just bought some amount of stocks at a time $t_i$. If a time travelling 
genie where to magically appear and tell you that the stock price in 15 minutes would be 1 point higher than it currently is, 
would you sell your position in 15 minutes? There are a lot of reasons to defend any decision you might choose to take.
Lets take a look at some of the alternatives

![Genie telling you trade secrets](assets/img/labeling/genie.png)

Lets say you decide to sell because you know for a fact that you will make money of the situation. 
In this scenario, you have weighted the risk, which is potentially missing out on a bigger fish just down the road,
and reward, which is the guarantee of some monetary gain. Either way, you have decided to set a threshold value for when
to buy and when to sell.

If you decide to hold your position because you believe that at some time $t_f$, the price of a stock will yield even
greater gains than selling 15 minutes into the future, you would still have to set some threshold value
for when you would actually sell. Surely, waiting for an infinite amount of time is not a good idea. 


CHECK THIS!
Since the determination of the labels for a price point $P(t)$ requires an insight into future values
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


[^1]: Whether or not this is a truly random process will not be discussed here, but it should be noted that the
    author is strongly opinionated when it comes to the subject of "absolute randomness". You may therefore choose to either
    remove the parenthesis, or remove its content depending on your own personal belief.