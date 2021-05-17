import torch
import numpy as np
import pandas as pd
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from transformation.policy_sample_generate import get_policy_sample


# dataset
class DoudizhuData(Dataset):
    def __init__(self, x, y):    
        self.x = torch.from_numpy(x).float()
        self.y = torch.from_numpy(y).float()
        self.n_samples = x.shape[0]

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples


# net definition
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
        self.out = nn.Linear(4096, 309)

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

if __name__ == '__main__':
    # read data
    print('\n' + '-' * 50)
    print('Reading data...')
    data = pd.read_csv('data/game_data.csv')
    primal_out = pd.read_csv('data/primal_out.csv')
    print('shape of game data: {}'.format(data.shape))
    print('Finished Reading data!')

    # transform
    print('\n' + '-' * 50)
    print('Transforming data...')
    x, y = get_policy_sample(data, primal_out)
    x = x.transpose(0, 3, 1, 2)
    y = y.reshape((len(y),))
    print('\nFinished Transforming data!')


    # split data
    print('\n' + '-' * 50)
    print('Spliting data...')
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)
    print('Finished spliting data !')


    # load data to dataloader
    print('\n' + '-' * 50)
    print('Loading data...')
    doudizhu_train = DoudizhuData(X_train, y_train)
    doudizhu_test = DoudizhuData(X_test, y_test)
    train_loader = DataLoader(dataset=doudizhu_train, batch_size=4, shuffle=True)
    test_loader = DataLoader(dataset=doudizhu_test, batch_size=4, shuffle=True)
    print('Finished loading data!')


    # Hyper-parameters 
    num_epochs = 5
    learning_rate = 0.006
    model = Net()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adagrad(
        model.parameters(), lr=learning_rate,
        #momentum=0.9, 
        weight_decay=0.003
    )


    # function to calculate accuracy
    def get_accuracy(model, data_loader):
        n_samples = 0
        n_correct = 0
        for i, (images, labels) in enumerate(data_loader):
            outputs = model.forward(images)
            predicts = torch.max(outputs, 1)[1]
            n_samples += labels.size(0)
            n_correct += (predicts == labels).sum().item()
        return n_correct/n_samples

    # start training
    print('\n' + '-' * 50)
    print('Start training...')
    n_total_steps = len(train_loader)
    test_accuracy1 = list()
    train_accuracy1 = list()
    loss_list = list()
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels.long())
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # print result
            if (i + 1) % 10 == 0: 
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{n_total_steps}], Loss: {loss.item():.4f}')
                torch.save(model.state_dict(), 'result/policy_net.pkl')
            loss_list.append(float(loss.detach().numpy()))
        # get accuracy
        test_accuracy = get_accuracy(model, test_loader)
        train_accuracy = get_accuracy(model, train_loader)
        test_accuracy1.append(test_accuracy)
        train_accuracy1.append(train_accuracy)
    print('Taining finished!')


    # save accuracy
    print('\n' + '-' * 50)
    print('Saving accuracy dataframe...')
    accuracy_df = pd.DataFrame({
        'train_accuracy': train_accuracy1,
        'test_accuracy': test_accuracy1
    })
    accuracy_df.to_csv('result/policy_accuracy_df.csv', index=False)
    print('Accuracy dataframe saved!')


    # save loss
    print('\n' + '-' * 50)
    print('Saving loss dataframe...')
    loss_df = pd.DataFrame({'loss': loss_list})
    loss_df.to_csv('result/policy_loss_df.csv', index=False)
    print('Loss dataframe saved!')