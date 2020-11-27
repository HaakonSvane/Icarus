# Icarus - Neural networks for classifying stock labels
### What is it?
Icarus is a set of neural network tasked to classify buy/sell/hold labels in stock data. The data is sourced from [Alpha Vantage](https://www.alphavantage.co)
and currently consists of 
The project is for a project in TDT4173 - Machine Learning at [NTNU](https://www.ntnu.edu).

The repository consists of multiple packages and modules that were used in creating the network. Every package found in 
*src/* has its own README.md and all the code is documented.

### Project structure
There are multiple folders in the repository. The table below explains all the directory and their contents.

| Main dir| Subdir 1 | Subdir 2 | Subdir 3 | **Description**|
|:---:|:---:|:---:|:---:|:---|
|data       |               |           |       |All the data that was sourced and generated.|
|----       |preprocessing  |           |       |All the data that was used in the preprocessing stage (raw data).|
|----       |----           |listings   |       |Directory containing company listings.|
|----       |----           |raw        |       |Raw sourced data from Alpha Vantage.|
|----       |training       |labeled    |       |All labeled data (normalized and non-normalized). Files in the directory are normalized.|
|----       |----           |----       |NORM   |All the labeled normalized data used for training.|
|----       |----           |----       |ORIG   |All the labeled non-normalized data used for training.|
|docs       |               |           |       |Source code for the website.|
|models     |               |           |       |Source code for the neural networks models and results.|
|----       |AAPL           |           |       |Network results from training on the AAPL (Apple Inc.) dataset.|
|----       |GOOG           |           |       |Network results from training on the GOOG (Alphabet Inc.) dataset.|
|----       |IBM            |           |       |Network results from training on the IBM (International Business Machines Corp.) dataset.|
|----       |LNC            |           |       |Network results from training on the LNC (Lincoln National Corp.) dataset.|
|src        |               |           |       |Source code for all the processing.|
|----       |alphavantage   |           |       |API wrapper package for fetching data from Alpha Vantage. Contains a README.md.|
|----       |preprocessing  |           |       |Preprocessor package for preprocessing the data. Contains a README.md.|
|----       |scripts        |           |       |Scripts that utilize the alphavantage package and the preprossing package.|
|----       |stocklabeler   |           |       |Stock labeling package for labeling the data.  Contains a README.md.|



### More information
A more in-depth explaination of the different stages of the processing pipeline is explained [here](https://haakonsvane.github.io/Icarus/)