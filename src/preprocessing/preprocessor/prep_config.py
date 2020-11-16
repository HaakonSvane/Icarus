
DT = 0.25                   # Number of hours between each datapoint in the raw data.
LAB_CONV_FUNC = 'cubic'     # The convolution window to use for the labeler.
HOURS_AHEAD = 6.5 * 5       # Hours ahead used to determine the label points.
HOURS_BEHIND = HOURS_AHEAD  # Hours behind used in normalization.
THRESH_BUY = 0.015          # Threshold for determining a buy point.
THRESH_SELL = 0.015         # Threshold for determining a sell point.
MED_WIN_SIZE = 300-1        # Walking median window size for the custom labeler.
START_TRADE = '09:30'       # Trading hours open time.
END_TRADE = '16:00'         # Trading hours close time
CLUSTER_SIZE = 130          # Minimum size of the clusters to consider. The size n will result in images of size n x n.
REC_PERC = 20               # nth percentile for which distances in the phase plot fall under are considered in the recurrence plot.
