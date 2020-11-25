
DT = 0.25                   # Number of hours between each datapoint in the raw data.
LAB_CONV_FUNC = 'cubic'     # The convolution window to use for the labeler.
HOURS_AHEAD = 6.5 * 5       # Hours ahead used to determine the label points.
HOURS_BEHIND = HOURS_AHEAD  # Hours behind used in normalization.
THRESH_BUY = 0.015          # Threshold for determining a buy point.
THRESH_SELL = 0.015         # Threshold for determining a sell point.
MED_WIN_SIZE = 300-1        # Walking median window size for the custom labeler.
START_TRADE = '09:30'       # Trading hours open time.
END_TRADE = '16:00'         # Trading hours close time
CLUSTER_SIZE = 26           # Minimum size of the clusters to consider. The size n will result in images of size n x n.
REC_PERC = 10               # nth percentile for which distances in the phase plot fall under are considered in the recurrence plot.
REC_DIST_MET = 'euclidean'  # Distance metric to use in the recurrence plots.
REC_ALPHA = 15              # Factor used in the exponential grayscale mapping of the distances over the nth percentile in the recurrence plot.
