import pandas as pd
import os
from src.scripts.preprocessing.utilities import *
from src.stocklabeler import labeler as lab
from src.scripts.preprocessing import utilities as util
import config

'''
    Module responsible for labeling the raw data provided by Alpha Vantage.
'''


def label_data(win_size: int = 16 * 5, which: str = 'all', save: bool = True,
               return_computations: bool = False) -> pd.DataFrame:
    '''
    Labels the data downloaded

    :param int win_size:    The window size used in the labeling process

    :param str which:   optional argument deciding which files to compute. If set to 'all', all the data in in the "raw"
                        folder will be labeled. If provided with a single symbol or a list of symbols, the labels will
                        only be computed for the given equities.

    :param bool save: if set to true, the labeled data will be saved to the "labeled" folder.

    :param bool return_computations:    if set to true, the function will output a list of all the dataframes used in
                                        the computations.
    :return: list of dataframes with computational results if "return_computations" is set to True.
    :rtype: list(pd.DataFrame)
    '''

    path_raw = config.DATA_DIR / 'preprocessing' / 'raw'
    path_labeled = config.DATA_DIR / 'training' / 'labeled'
    subdirectories = [x.name for x in path_raw.iterdir() if x.is_dir()]
    new_subdir = []

    if which is not 'all':
        if isinstance(which, list):
            for w in which:
                if w not in subdirectories:
                    raise ValueError(f'The symbol {w} was not found in {path_raw}.')
                new_subdir.append(path_raw / w)
        else:
            if which not in subdirectories:
                raise ValueError(f'The symbol {which} was not found in {path_raw}.')
            new_subdir.append(path_raw / which)
    else:
        new_subdir = [path_raw / sd for sd in subdirectories]

    return_list = []
    for d in new_subdir:
        sym = d.name
        print(f'Computing labels for {sym}...')
        frame = util.load_batch_data(path=d, reverse=True, format_time=True)

        # win_size is in hours
        win_size = int(win_size)
        l = lab.CustomLabeler(frame, win_size, dt=0.25)
        l.set_conv_win_func('cubic', a=1, b=0, c=0, d=0)
        lab_data = l.calculate(thresh_buy=0.015, thresh_sell=0.015, median_size=300 - 1, smooth_result=True)

        if save:
            save_path = path_labeled / f'{win_size}H_WIN'
            if not save_path.is_dir():
                os.mkdir(save_path)
            final_data = l.data
            final_data = final_data.join(lab_data['label'])
            final_data.to_csv(save_path / f'{sym}_15min.csv', index=False)
        if return_computations:
            return_list.append(lab_data)

    if return_computations:
        print('\nAverage label distribution:')
        counts = [r['label'].value_counts(normalize=True) for r in return_list]
        [print(f'{new_subdir[i]}\n{c}') for i, c in enumerate(counts)]
        return return_list


if __name__ == '__main__':
    label_data(win_size=16*1, which='all', save=False, return_computations=False)
