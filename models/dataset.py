import pandas as pd


def get_dataset(name, slice_len):
    data_15min = pd.read_csv(name)
    # print(len(data_15min))
    data_15min.loc[data_15min.label == 'B', 'label'] = int(0)
    data_15min.loc[data_15min.label == 'H', 'label'] = int(1)
    data_15min.loc[data_15min.label == 'S', 'label'] = int(2)
    
    slice_length = slice_len
    # print(int(len(data_15min)/slice_length))
    X = []
    Y = []
    for i, data in data_15min.iterrows():
        if i < slice_length * (int(len(data_15min)/slice_length)):
            if i % slice_length == 0:
                features = []
                labels = []
            features.append([data['open'], data['high'], data['low'], data['close'], data['volume']])
            labels.append(data['label'])
            if i % slice_length == 0:
                X.append(features)
                Y.append(labels)
   
    return X, Y


