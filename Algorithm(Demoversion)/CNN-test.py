from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
import os
import numpy as np


class Config:
    def __init__(self):
        self.batch_size = 64
        self.test_batch_size = 1000
        self.epochs = 20
        self.lr = 0.01
        self.momentum = 0.5
        self.no_cuda = False
        self.seed = 1
        self.log_interval = 30
        self.cuda = None


args = Config()
args.cuda = not args.no_cuda and torch.cuda.is_available()
torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)

kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}

# transform = transforms.Compose([transforms.ToTensor(),
#                                 transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5)),
#                                 ])

trainset =
testset =
train_loader =
test_loader =





class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=21, out_channels=42, kernel_size=3, stride=1)
        self.bn1 = nn.BatchNorm2d(42)
        self.relu1 = nn.ReLU()
        #self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(in_channels=42, out_channels=84, kernel_size=3, stride=1)
        self.bn2 = nn.BatchNorm2d(84)
        self.relu2 = nn.ReLU()
        #self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(in_channels=84, out_channels=128, kernel_size=5, stride=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.relu3 = nn.ReLU()
        self.conv4 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=1)
        self.bn4 = nn.BatchNorm2d(256)
        self.relu4 = nn.ReLU()
        self.conv5 = nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, stride=2)
        self.bn5 = nn.BatchNorm2d(512)
        self.relu5 = nn.ReLU()
        #self.fc2 = nn.Linear(120, 84)
        #self.bn4 = nn.BatchNorm1d(84)
        #self.dp2 = nn.Dropout(0.5)
        self.out = nn.Linear(2*2*512, 309)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu3(x)
        x = self.conv4(x)
        x = self.bn4(x)
        x = self.relu4(x)
        x = self.conv5(x)
        x = self.bn5(x)
        x = self.relu5(x)
        x = torch.flatten(x, start_dim=1)
        out = self.out(x)
        return out


def train(epoch, model, optimizer, isSoft=False):
    model.train()
    train_loss = 0
    correct = 0
    for batch_idx, (data, target) in enumerate(train_loader):
        if args.cuda:
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data), Variable(target)
        optimizer.zero_grad()
        output = model(data)

        # predicted labels
        pred = output.data.max(1)[1]  # get the index of the max log-probability
        correct += pred.eq(target.data).cpu().sum()

        if isSoft:
            loss = F.cross_entropy(output, target)  # is it true to use such a loss over cross-entropy loss?
        else:
            loss = F.nll_loss(output, target)

        train_loss += loss.item()

        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), loss.item()))
        del data, target, loss
        torch.cuda.empty_cache()

    return train_loss / len(train_loader), np.float(correct) / len(train_loader.dataset)


def test(epoch, model, optimizer, isSoft=False):
    model.eval()
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        if args.cuda:
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data, volatile=True), Variable(target)
        output = model(data)
        if isSoft:
            test_loss += F.cross_entropy(output, target).item()
        else:
            test_loss += F.nll_loss(output, target).data[0]
        pred = output.data.max(1)[1]  # get the index of the max log-probability
        correct += pred.eq(target.data).cpu().sum()
        del data, target
        torch.cuda.empty_cache()
    test_loss = test_loss
    test_loss /= len(test_loader)  # loss function already averages over batch size
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

    return test_loss, np.float(correct) / len(test_loader.dataset)

model_policy_net = Net()

if args.cuda:
    model_policy_net.cuda()


optimizer_model_policy_net = optim.SGD(model_policy_net.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=0.001)

model_policy_net_train_acc = []
model_policy_net_train_loss = []
model_policy_net_test_acc = []
model_policy_net_test_loss = []
for epoch in range(1, args.epochs + 1):
    train_loss, train_acc = train(epoch, model_policy_net, optimizer_model_policy_net, True)
    test_loss, test_acc = test(epoch, model_policy_net, optimizer_model_policy_net, True)
    model_policy_net_train_loss.append(train_loss)
    model_policy_net_train_acc.append(train_acc)
    model_policy_net_test_acc.append(test_acc)
    model_policy_net_test_loss.append(test_loss)