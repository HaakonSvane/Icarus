import pandas as pd
import numpy as np

class _Function:

    @staticmethod
    def RSI(frame: pd.DataFrame, hours_behind: int, dt: float = 0.25) -> np.array:
        '''
        :param frame: dataframe containing data to calculate RSI for.
        :param hours_behind: Number of hours to look back in the calculation.
        :param dt: The resolution of the data in hours.
        :return: dataframe of the calculated RSI
        '''

        U_calc = lambda diff: diff if diff > 0 else 0
        D_calc = lambda diff: np.abs(diff) if diff < 0 else 0
        f_U = np.vectorize(U_calc, otypes=[np.float])
        f_D = np.vectorize(D_calc, otypes=[np.float])

        n_points = len(frame.index)
        rsi = np.zeros(n_points)
        rsi.fill(np.nan)

        look_back = int(hours_behind / dt)

        diffs = (frame['close'] - frame['open']).values
        U = f_U(diffs)
        D = f_D(diffs)

        SMMA_U = np.zeros(n_points - look_back + 1)
        SMMA_D = np.zeros(n_points - look_back + 1)
        SMMA_U[0] = np.mean(U[:look_back])
        SMMA_D[0] = np.mean(D[:look_back])
        for i in range(1, n_points - look_back + 1):
            SMMA_U[i] = (U[i + look_back - 1] + (SMMA_U[i - 1] * (look_back - 1))) / look_back
            SMMA_D[i] = (D[i + look_back - 1] + (SMMA_D[i - 1] * (look_back - 1))) / look_back

        rs = SMMA_U / SMMA_D
        rsi[look_back - 1:] = 100 - 100 / (1 + rs)

        return rsi