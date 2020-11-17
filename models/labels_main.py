import torch
import torch.nn as nn
import torch.utils.data as data
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

import config
from models.labels_dataset import get_slice
from models.labels_models import TCN


class TorchDataset(data.Dataset):
    def __init__(self, dataset_x, dataset_y):
        self.dataset_x = dataset_x
        self.dataset_y = dataset_y

    def __getitem__(self, index):
        return self.dataset_x[index], self.dataset_y[index]

    def __len__(self):
        return len(self.dataset_x)


# hyper parameters
slice_len = 320    # 320 or 64
label_extra = 0
sample = 1000

BATCH_SIZE = 32
LR = 0.0005
EPOCH = 500
torch.manual_seed(1)

# TCN
KERNEL_SIZE = 7
LEVEL = 6
NHID = 2
channel_seq = [NHID] * LEVEL


INPUT_SIZE = 1
CLASSES = 3
model = TCN(INPUT_SIZE, CLASSES, channel_seq, KERNEL_SIZE, label_extra)

if slice_len == 320:
    path = config.DATA_DIR / 'training' / 'labeled' / '80H_WIN'
elif slice_len == 64:
    path = config.DATA_DIR / 'training' / 'labeled' / '16H_WIN'
name_all = [f for f in path.iterdir() if f.is_file()]

name_all = name_all[0:1]    # choose companies
print(name_all)

x_train_all = []
x_test_all = []
y_train_all = []
y_test_all = []
for name in name_all:
    X, Y = get_slice(name, slice_len, label_extra, sample)
    X_tensor = torch.Tensor(X)
    Y_tensor = torch.Tensor(Y).to(dtype=torch.int64)
    x_train, x_test, y_train, y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=1)
    x_train_all.append(x_train)
    x_test_all.append(x_test)
    y_train_all.append(y_train)
    y_test_all.append(y_test)
x_train_all = torch.cat(x_train_all, dim=0)
x_test_all = torch.cat(x_test_all, dim=0)
y_train_all = torch.cat(y_train_all, dim=0)
y_test_all = torch.cat(y_test_all, dim=0)

print(x_train_all.shape)
print(x_test_all.shape)

train_unique, train_count = torch.unique(y_train_all, return_counts=True)
train_weight = torch.true_divide(train_count, int(torch.numel(y_train_all)))
print(y_train_all.shape, train_unique, train_count, train_weight)
test_unique, test_count = torch.unique(y_test_all, return_counts=True)
test_weight = torch.true_divide(test_count, int(torch.numel(y_test_all)))
print(y_test_all.shape, test_unique, test_count, test_weight)

CE_weight = torch.true_divide(1, train_weight)

if torch.cuda.is_available():
    model.cuda()
    x_train_all = x_train_all.cuda()
    x_test_all = x_test_all.cuda()
    y_train_all = y_train_all.cuda()
    y_test_all = y_test_all.cuda()
    CE_weight = CE_weight.cuda()
    print('cuda = True')

dataset = TorchDataset(x_train_all, y_train_all)
loader = data.DataLoader(dataset=dataset, batch_size=BATCH_SIZE, shuffle=True)

criterion = nn.CrossEntropyLoss(weight=CE_weight)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

loss_list = []
accuracy_list = []
loss_test_list = []
accuracy_test_list = []
for epoch in range(EPOCH):
    y_test_all = y_test_all.cuda()
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

    accuracy = accuracy_count/(len(y_train_all)*(label_extra+1))
    loss_list.append(loss_epoch.item())
    accuracy_list.append(accuracy)

    with torch.no_grad():
        outputs_test = model(x_test_all)
        outputs_test = outputs_test.view(-1, 3)
        y_test_all = y_test_all.view(-1)
        loss_test = criterion(outputs_test, y_test_all)
        y_pred_test = outputs_test.argmax(dim=1)
        accuracy_test = sum(torch.eq(y_test_all, y_pred_test)).item()/(len(y_test_all)*(label_extra+1))
        loss_test_list.append(loss_test)
        accuracy_test_list.append(accuracy_test)

    if epoch % 10 == 0:
        print('epoch:{:d} \ttrain loss:{:f} \ttrain accuracy:{:f} \ttest loss:{:f} \ttest accuracy:{:f}'.format(epoch, loss_epoch.item(), accuracy, loss_test, accuracy_test))

        plt.plot(y_test_all.cpu())
        plt.plot(y_pred_test.cpu())
        plt.title('epoch={:d} test accuracy={:6f}'.format(epoch, accuracy_test))
        plt.show()

plt.subplot(221)
plt.plot(loss_list)
plt.title('train loss')
plt.xlabel('epoch')

plt.subplot(222)
plt.plot(accuracy_list)
plt.title('train accuracy')
plt.xlabel('epoch')

plt.subplot(223)
plt.plot(loss_test_list)
plt.title('test loss')
plt.xlabel('epoch')

plt.subplot(224)
plt.plot(accuracy_test_list)
plt.title('test accuracy')
plt.xlabel('epoch')
# plt.savefig('{:f}_epoch{:d}.png'.format(LR, EPOCH))
plt.show()