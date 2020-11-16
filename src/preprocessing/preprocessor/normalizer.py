import numpy as np


class _Normalizer:
    def __init__(self, hours_behind: float, dt: float):
        self.hours_behind = hours_behind
        self.dt = dt

    @property
    def hours_behind(self):
        return self._hours_behind

    @hours_behind.setter
    def hours_behind(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError(f'Value {val} is not valid. Must be an integer or float.')
        self._hours_behind = val

    @property
    def dt(self):
        return self._dt

    @dt.setter
    def dt(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError(f'Value {val} is not valid. Must be an integer or float.')
        self._dt = val

    def modfified_tanh(self, arr: np.array, debug_plot: bool = False) -> np.array:

        '''
        Takes in a 1D numpy array and returns the normalized array using the modified tanh estimator.

        :param arr: 1D-array of values to normalize.
        :param debug_plot: Whether or not to plot the results of the normalizer. For debugging and exploration.
        :return: Normalized array with shape len(arr).
        '''

        n_points = arr.shape[0]
        look_back = int(self.hours_behind / self.dt)

        norm_arr = np.zeros(n_points)
        norm_arr.fill(np.nan)

        mean = np.zeros(n_points - look_back + 1)
        std = np.zeros(n_points - look_back + 1)

        # Calculates running mean and running standard deviation look_back points backwards in time.
        for i in range(0, n_points - look_back + 1):
            mean[i] = np.mean(arr[i:look_back + i])
            std[i] = np.std(arr[i:look_back + i])

        norm_arr[look_back - 1:] = np.tanh(0.1 * (arr[look_back - 1:] - mean) / std)

        if debug_plot:
            import matplotlib.pyplot as plt
            import seaborn as sns
            sns.set()
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
            ax1.plot(np.arange(n_points), arr, label='Original array')
            ax1.plot(np.arange(look_back - 1, n_points), mean, label='Mean or original')
            ax2.plot(np.arange(n_points), norm_arr, label='Normalized array')
            ax1.legend()
            ax2.legend()
            plt.suptitle('Debug plot for the modified tanh normalizer.')
            plt.show()

        return norm_arr
