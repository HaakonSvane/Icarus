import sys
import random
import pandas as pd


def get_slice(name, slice_len, label_extra, sample):
    random.seed(1)
    data_15min = pd.read_csv(name)
    data_15min.loc[data_15min.label == 'B', 'label'] = int(0)
    data_15min.loc[data_15min.label == 'H', 'label'] = int(1)
    data_15min.loc[data_15min.label == 'S', 'label'] = int(2)

    features_all = []
    label_all = []
    for i, data in data_15min.iterrows():
        # features_all.append([data['open'], data['high'], data['low'], data['close'], data['volume']])
        features_all.append([data['close']])
        label_all.append(data['label'])

    data_len = len(data_15min)
    max_slice_beginning = data_len-slice_len-label_extra

    if max_slice_beginning+1 < sample:
        print('This company has not enough instances. Please reduce the number of instances or change the company.')
        sys.exit()

    X = []
    Y = []
    slice_beginnings = random.sample(range(max_slice_beginning + 1), sample)
    for i in slice_beginnings:
        one_slice = features_all[i:i+slice_len+label_extra]
        label_begin = int((i+i+slice_len)/2)
        one_label = label_all[label_begin:label_begin+label_extra+1]
        X.append(one_slice)
        Y.append(one_label)
    print('Slices!')
    return X, Y
