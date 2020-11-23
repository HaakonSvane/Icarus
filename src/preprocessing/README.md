# Preprocessor:
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 

### What is it?
This package is responsible for implementing all the computations that are used in the preprocessing stage
of the data.

The data goes through multiple stages of processing using this package. The general workflow is as follows:
1. Raw data gets loaded into memory.
2. The data is trimmed down to normal working hours (09:30-16:00) since some of the equities list before/after-hour trading.
3. The stocklabeler labels the data.
4. RSI is calculated for the equity.
5. The variables in each datapoints are normalized.
6. The data is saved as a csv file in data/training.

 
