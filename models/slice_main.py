# If sample = 2000, it will generate 2000-320+1=1681 samples, 1344 for training and 337 for testing.
sample = 1000

import glob
import os
import torch
import torch.nn as nn
import torch.utils.data as data
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from slice import get_slice
from slice_models import TCN


class TorchDataset(data.Dataset):
    def __init__(self, dataset_x, dataset_y):
        self.dataset_x = dataset_x
        self.dataset_y = dataset_y

    def __getitem__(self, index):
        return self.dataset_x[index], self.dataset_y[index]

    def __len__(self):
        return len(self.dataset_x)


# hyper parameters
slice_len = 320
BATCH_SIZE = 32
learning_rate = 0.001
EPOCH = 500

# CNN
KERNEL_SIZE = 7
LEVEL = 6
nhid = 2
channel_seq = [nhid] * LEVEL


INPUT_SIZE = 5
CLASSES = 3

model = TCN(INPUT_SIZE, CLASSES, channel_seq, KERNEL_SIZE, 0)


# path = r'./labeled/'
# name_all = glob.glob(os.path.join(path, "*.csv"))
name_all = ['./labeled/AAL_15min.csv']

x_train_all = []
x_test_all = []
y_train_all = []
y_test_all = []
for name in name_all:
    X, Y = get_slice(name, slice_len, sample)
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
print(y_train_all.shape)
print(y_test_all.shape)

dataset = TorchDataset(x_train_all, y_train_all)
loader = data.DataLoader(dataset=dataset, batch_size=BATCH_SIZE, shuffle=True)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

loss_list = []
accuracy_list = []
loss_test_list = []
accuracy_test_list = []
for epoch in range(EPOCH):
    accuracy_count = 0
    loss_epoch = 0

    for batch_num, (batch_x, batch_y) in enumerate(loader):
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

        batch_y_pred = outputs.argmax(dim=1)
        accuracy_count = accuracy_count + sum(torch.eq(batch_y, batch_y_pred)).item()
        loss_epoch = loss_epoch + loss

    accuracy = accuracy_count/len(y_train_all)
    loss_list.append(loss_epoch.item())
    accuracy_list.append(accuracy)

    with torch.no_grad():
        outputs_test = model(x_test_all)
        loss_test = criterion(outputs_test, y_test_all)
        y_pred_test = outputs_test.argmax(dim=1)
        accuracy_test = sum(torch.eq(y_test_all, y_pred_test)).item()/len(y_test_all)
        loss_test_list.append(loss_test)
        accuracy_test_list.append(accuracy_test)

    if epoch % 10 == 0:
        print('epoch:{:d} \ttrain loss:{:f} \ttrain accuracy:{:f} \ttest loss:{:f} \ttest accuracy:{:f}'.format(epoch, loss_epoch.item(), accuracy, loss_test, accuracy_test))
        plt.plot(y_test_all)
        plt.plot(y_pred_test)
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
plt.show()
