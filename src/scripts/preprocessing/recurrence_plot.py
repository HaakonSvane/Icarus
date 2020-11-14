from pyts.image import RecurrencePlot
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

import config
from src.scripts.preprocessing.utilities import *

path = config.DATA_DIR / 'training' / 'labeled' / '80H_WIN' / 'AAPL_15min.csv'

data = load_data(path)
H = data[data.label == 'H']
B = data[data.label == 'B']
S = data[data.label == 'S']

H_DAT = H.drop(['time', 'label'], axis=1).to_numpy()
B_DAT = B.drop(['time', 'label'], axis=1).to_numpy()
S_DAT = S.drop(['time', 'label'], axis=1).to_numpy()
ALL_DAT = data.drop(['time', 'label'], axis=1).to_numpy()

rp = RecurrencePlot(threshold='point', percentage=10, flatten=False)

X_rp = rp.fit_transform(B_DAT.transpose())


plt.imshow(X_rp[0], cmap='binary', origin='lower')
plt.show()

