from src.scripts.preprocessing.utilities import *
from src.stocklabeler import labeler as lab

'''
    Module responsible for labeling the raw data provided by Alpha Vantage.
'''


def calc_from_raw():
    p = Path('label_test/raw')
    subdirectories = [x for x in p.iterdir() if x.is_dir()]

    for dir in subdirectories:
        sym = dir.stem
        frame = []
        print(f'Computing labels for {sym}...')
        for y in range(1, 3):
            for m in range(1, 13):
                frame.append(load_data(f'label_test/raw/{sym}/{sym}_15min_y{y}m{m}.csv'))
        frame = pd.concat(frame, ignore_index=True)
        # Data from AV is reversed in the sense that it the first entry is the most recent in time. This code flips it.
        frame = frame.reindex(index=frame.index[::-1])
        frame = frame.reset_index(drop=True)

        win_size = int(16 * 5)
        l = lab.CustomLabeler(frame, win_size, 0.25)
        l.set_conv_win_func('cubic', a=1, b=0, c=0, d=0)
        label_data = l.calculate(thresh_buy=0.004, thresh_sell=0.004, median_size=300 - 1)
        final_data = l.data
        final_data = final_data.join(label_data['label'])
        final_data.to_csv(f'label_test/labeled/{sym}_15min.csv', index=False)
