# Preprocessor:
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 

### What is it?
This package is responsible for implementing all the computations that are used in the preprocessing stage
of the data.

The main class of the package is the *Preprocessor* class. This class is primarily a container for 4 other processing
classes that each serve different needs. Below is a table of the instance classes that are accessible through *Preprocessor*

|Name       |Description |
|:---:|:---|
|Normalizer |Implements normalizing functions that act on arrays of data. |
|Utility    |Implements several utility functions such as data loaders, phase space plotters and more.|
|Function   |Implements functions that act on the data such as calculating RSI.|
|DataLabeler|Implements functions that implements functions for labeling the data as well as plotting the results of the process.|

### How to use it:
Creating an instance of the Preprocessor class as well as utilizing its member instance functions is shown below:
```python
from src.preprocessing import preprocessor as prep

proc = prep.Preprocessor()

# Loading a dataset from a path.
frame = proc.Utility.load_batch_data('PATH/TO/DIR/OF/FILES')

# Extracting all times that fall within the given time window.
frame = proc.Utility.get_trading_hours(frame, from_time='06:00', to_time='13:00')

# Label the data using the labeler package using a look forward value of 2 hours with data that has 15 min intervals.
frame['label'] = proc.DataLabeler.get_labels(frame, mode='custom', hours_ahead=2,  dt=0.25)

# Calculate the RSI for the frame for data with 15 min intervals.
frame['rsi'] = proc.Function.RSI(frame, open_name='open', close_name='close', dt=0.25)

# Normalize the close price column of data using 2 hours of look back for data with 15 min intervals.
frame['close'] = proc.Normalizer.modified_tanh(frame['close'].values, hours_behind=2, dt=0.25)

```



 
