import sys
import argparse
import torch
import torch.nn as nn
import torch.utils.data as data
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from pandas.core.frame import DataFrame


import config
from models.func_dataset import get_slice
from models.func_models import TCN
from models.func_models import LSTM
from models.func_models import GRU


class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'w')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


class TorchDataset(data.Dataset):
    def __init__(self, dataset_x, dataset_y):
        self.dataset_x = dataset_x
        self.dataset_y = dataset_y

    def __getitem__(self, index):
        return self.dataset_x[index], self.dataset_y[index]

    def __len__(self):
        return len(self.dataset_x)


parser = argparse.ArgumentParser(description='Machine Learning')
parser.add_argument('--company', type=str, default='LNC',
                    help='company (default: LNC)')
parser.add_argument('--model', type=str, default='TCN',
                    help='model (default: TCN)')
parser.add_argument('--slice_length', type=int, default=52,
                    help='slice length (default: 52)')
parser.add_argument('--input_size', type=int, default=6,
                    help='input size (default: 6)')
parser.add_argument('--normalization', type=str, default='YES',
                    help='normalization (default: YES)')
parser.add_argument('--sample', type=int, default=10400,
                    help='sample (default: 10000)')
parser.add_argument('--epoch', type=int, default=1000,
                    help='epoch (default: 1000)')
args = parser.parse_args()

# model
MODEL = args.model  # TCN, LSTM, GRU

slice_len = args.slice_length    # 52, 260
sample = args.sample

BATCH_SIZE = 32
LR = 0.0001
EPOCH = args.epoch
torch.manual_seed(1)
label_extra = 0
INPUT_SIZE = args.input_size  # 4, 5
CLASSES = 3
dir_name = args.company

file_name = str(slice_len) + '_' + str(INPUT_SIZE) + '_' + args.normalization + '_' + MODEL
sys.stdout = Logger(dir_name + '/' + file_name + '.txt', sys.stdout)

if slice_len == 260:
    if MODEL == 'TCN':
        KERNEL_SIZE = 7
        LEVEL = 6
        NHID = 5
        channel_seq = [NHID] * LEVEL
        model = TCN(INPUT_SIZE, CLASSES, channel_seq, KERNEL_SIZE, label_extra)
    elif MODEL == 'LSTM':
        HIDDEN_SIZE = 10
        LAYER = 3
        model = LSTM(INPUT_SIZE, HIDDEN_SIZE, LAYER, CLASSES)
    elif MODEL == 'GRU':
        HIDDEN_SIZE = 11
        LAYER = 3
        model = GRU(INPUT_SIZE, HIDDEN_SIZE, LAYER, CLASSES)
elif slice_len == 52:
    if MODEL == 'TCN':
        KERNEL_SIZE = 5
        LEVEL = 4
        NHID = 5
        channel_seq = [NHID] * LEVEL
        model = TCN(INPUT_SIZE, CLASSES, channel_seq, KERNEL_SIZE, label_extra)
    elif MODEL == 'LSTM':
        HIDDEN_SIZE = 8
        LAYER = 2
        model = LSTM(INPUT_SIZE, HIDDEN_SIZE, LAYER, CLASSES)
    elif MODEL == 'GRU':
        HIDDEN_SIZE = 10
        LAYER = 2
        model = GRU(INPUT_SIZE, HIDDEN_SIZE, LAYER, CLASSES)

total_num = sum(p.numel() for p in model.parameters())
print('model:{}  parameters:{:d}\n'.format(MODEL, total_num))

# dataset
if args.normalization == 'YES':
    name_end = 'NORM'
    if slice_len == 52:
        name_middle = 'W52H'
        path = config.DATA_DIR / 'training' / 'labeled' / name_end / name_middle
    elif slice_len == 260:
        name_middle = 'W260H'
        path = config.DATA_DIR / 'training' / 'labeled' / name_end / name_middle
elif args.normalization == 'NO':
    name_end = 'ORIG'
    if slice_len == 52:
        name_middle = 'W52H'
        path = config.DATA_DIR / 'training' / 'labeled' / name_end / name_middle
    elif slice_len == 260:
        name_middle = 'W260H'
        path = config.DATA_DIR / 'training' / 'labeled' / name_end / name_middle

data_name = dir_name + '_' + name_middle + '_15min_' + name_end + '.csv'
dataset = path /data_name
print('dataset:', dataset, '\n')

X, Y = get_slice(dataset, slice_len, label_extra, sample, INPUT_SIZE)
X_tensor = torch.Tensor(X)
Y_tensor = torch.Tensor(Y).to(dtype=torch.int64)
x_train, x_test, y_train, y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=1)

# x_train = X_tensor[0: 8320]
# y_train = Y_tensor[0: 8320]
# x_test = X_tensor[8320:10400]
# y_test = Y_tensor[8320:10400]

print('training features:', x_train.shape)
print('testing features:', x_test.shape)

train_unique, train_count = torch.unique(y_train, return_counts=True)
train_weight = torch.div(train_count.to(torch.float32), int(torch.numel(y_train)))
print('training labels:', y_train.shape, train_unique, train_count, train_weight)
test_unique, test_count = torch.unique(y_test, return_counts=True)
test_weight = torch.div(test_count.to(torch.float32), int(torch.numel(y_test)))
print('testing labels:', y_test.shape, test_unique, test_count, test_weight)


# train and test
if torch.cuda.is_available():
    model.cuda()
    x_train = x_train.cuda()
    x_test = x_test.cuda()
    y_train = y_train.cuda()
    y_test = y_test.cuda()
    print('\ncuda = True\n')

dataset = TorchDataset(x_train, y_train)
loader = data.DataLoader(dataset=dataset, batch_size=BATCH_SIZE, shuffle=True)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

loss_list = []
accuracy_list = []
loss_test_list = []
accuracy_test_list = []
d_pred = {}
y_list = y_test.view(-1).cpu().numpy().tolist()
d_pred['real'] = y_list
for epoch in range(EPOCH):
    accuracy_count = 0
    loss_epoch = 0

    for batch_num, (batch_x, batch_y) in enumerate(loader):
        optimizer.zero_grad()
        outputs = model(batch_x)
        outputs = outputs.view(-1, 3)
        batch_y = batch_y.view(-1)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

        batch_y_pred = outputs.argmax(dim=1)
        accuracy_count = accuracy_count + sum(torch.eq(batch_y, batch_y_pred)).item()
        loss_epoch = loss_epoch + loss

    accuracy = accuracy_count/(len(y_train)*(label_extra+1))
    loss_list.append(loss_epoch.item())
    accuracy_list.append(accuracy)

    with torch.no_grad():
        outputs_test = model(x_test)
        outputs_test = outputs_test.view(-1, 3)
        y_test = y_test.view(-1)
        loss_test = criterion(outputs_test, y_test)
        y_pred_test = outputs_test.argmax(dim=1)
        accuracy_test = sum(torch.eq(y_test, y_pred_test)).item()/(len(y_test)*(label_extra+1))
        loss_test_list.append(loss_test.item())
        accuracy_test_list.append(accuracy_test)
        y_pred_list = y_pred_test.cpu().numpy().tolist()
        d_pred[str(epoch)] = y_pred_list

    if epoch % 10 == 0:
        print('epoch:{:d} \ttrain loss:{:f} \ttrain accuracy:{:f} \ttest loss:{:f} \ttest accuracy:{:f}'.format(epoch, loss_epoch.item(), accuracy, loss_test, accuracy_test))

    if epoch == EPOCH-1:
        ture_test = y_test.cpu()
        pred_test = y_pred_test.cpu()
        print('\nepoch:{:d} \ttrain loss:{:f} \ttrain accuracy:{:f} \ttest loss:{:f} \ttest accuracy:{:f}'.format(epoch, loss_epoch.item(), accuracy, loss_test, accuracy_test))
        print(file_name)
        print(confusion_matrix(ture_test, pred_test))
        print(classification_report(ture_test, pred_test))

d = {'train loss': loss_list,
     'train accuracy': accuracy_list,
     'test loss': loss_test_list,
     'test accuracy': accuracy_test_list}
data = DataFrame(d)
data.to_csv(dir_name + '/' + file_name + '.csv')

data_pred = DataFrame(d_pred)
data_pred.to_csv(dir_name + '/' + file_name + '_pred.csv')
