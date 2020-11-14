import pandas as pd


def get_slice(name, slice_len, sample):
    data_15min = pd.read_csv(name)
    data_15min.loc[data_15min.label == 'B', 'label'] = int(0)
    data_15min.loc[data_15min.label == 'H', 'label'] = int(1)
    data_15min.loc[data_15min.label == 'S', 'label'] = int(2)
    X_all = []
    Y_all = []
    for i, data in data_15min.iterrows():
        Y_all.append(data['label'])
        features = [data['open'], data['high'], data['low'], data['close'], data['volume']]
        X_all.append(features)

    X = []
    for i in range(sample - slice_len + 1):
        one_slice = []
        for j in range(i, i+slice_len):
            one_slice.append(X_all[j])
        X.append(one_slice)

    Y = Y_all[int(slice_len/2):int(slice_len/2)+len(X)]
    print('Slices!')
    return X, Y
