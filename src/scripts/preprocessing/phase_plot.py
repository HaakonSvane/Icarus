import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from src.scripts.preprocessing import utilities as util
import config

path = config.DATA_DIR / 'preprocessing' / 'raw' / 'AAPL'
frame = util.load_batch_data(path)
frame = util.get_trading_hours(frame)
#ax = fig.add_subplot(111, projection='3d')

fig, (ax1, ax2) = plt.subplots(2,1,sharex=True)

vol = frame['volume'].values

arr = np.arange(10)
n = 40*4
res = np.convolve(vol, np.ones(n)/n, mode='valid')
ax1.plot(frame.index.values, vol)
ax1.plot(np.arange(res.size)+n-1, res)
ratio = vol[n-1:]/res-1
ta = np.tanh(ratio)
ax2.plot(np.arange(res.size)+n-1, ta)

plt.show()

