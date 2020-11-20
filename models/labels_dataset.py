import sys
import random
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def get_slice(name, slice_len, label_extra, sample, input_size):
    print('Begin to slice.')
    random.seed(1)
    data_15min = pd.read_csv(name)
    data_15min.loc[data_15min.label == 'B', 'label'] = int(0)
    data_15min.loc[data_15min.label == 'H', 'label'] = int(1)
    data_15min.loc[data_15min.label == 'S', 'label'] = int(2)

    features_all = []
    label_all = []
    for i, data in data_15min.iterrows():
        if input_size == 5:
            features_all.append([data['open'], data['high'], data['low'], data['close'], data['volume']])
        elif input_size == 4:
            features_all.append([data['open'], data['high'], data['low'], data['close']])
        elif input_size == 1:
            features_all.append([data['close']])
        else:
            print('False INPUT_SIZE')
            sys.exit()
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
    print('Successful!\n')
    return X, Y


def get_slice_normalization(name, slice_len, label_extra, sample, input_size):
    print('Begin to slice.')
    random.seed(1)
    data_15min = pd.read_csv(name)
    data_15min.loc[data_15min.label == 'B', 'label'] = int(0)
    data_15min.loc[data_15min.label == 'H', 'label'] = int(1)
    data_15min.loc[data_15min.label == 'S', 'label'] = int(2)

    features_all = []
    label_all = []
    for i, data in data_15min.iterrows():
        if input_size == 5:
            features_all.append([data['open'], data['high'], data['low'], data['close'], data['volume']])
        elif input_size == 4:
            features_all.append([data['open'], data['high'], data['low'], data['close']])
        elif input_size == 1:
            features_all.append([data['close']])
        else:
            print('False INPUT_SIZE')
            sys.exit()
        label_all.append(data['label'])

    data_len = len(data_15min)
    max_slice_beginning = data_len-slice_len-label_extra

    if max_slice_beginning+1 < sample:
        print('This company has not enough instances. Please reduce the number of instances or change the company.')
        sys.exit()

    X_np = np.array(features_all)
    zscore = StandardScaler()
    X_np = zscore.fit_transform(X_np)

    X = []
    Y = []
    slice_beginnings = random.sample(range(max_slice_beginning + 1), sample)
    for i in slice_beginnings:
        one_slice = X_np[i:i+slice_len+label_extra]
        label_begin = int((i+i+slice_len)/2)
        one_label = label_all[label_begin:label_begin+label_extra+1]
        X.append(one_slice)
        Y.append(one_label)
    print('Successful!\n')
    return X, Y
