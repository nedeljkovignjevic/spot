import torch.nn as nn
import torch.nn.functional as F


class NvidiaModel(nn.Module):

    def __init__(self):
        super(NvidiaModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 24, kernel_size=(5, 5), stride=(2, 2))
        self.conv2 = nn.Conv2d(24, 36, kernel_size=(5, 5), stride=(2, 2))
        self.conv3 = nn.Conv2d(36, 48, kernel_size=(5, 5), stride=(2, 2))
        self.conv4 = nn.Conv2d(48, 64, kernel_size=(3, 3))
        self.conv5 = nn.Conv2d(64, 64, kernel_size=(3, 3))

        self.dropout = nn.Dropout2d(0.5)

        self.fc1 = nn.Linear(64*1*18, 100)
        self.fc2 = nn.Linear(100, 50)
        self.fc3 = nn.Linear(50, 10)
        self.fc4 = nn.Linear(10, 1)

    def forward(self, x):
        x = x.view(x.size(0), 3, 66, 200)

        x = F.elu(self.conv1(x))
        x = F.elu(self.conv2(x))
        x = F.elu(self.conv3(x))
        x = F.elu(self.conv4(x))
        x = F.elu(self.conv5(x))
        x = self.dropout(x)

        x = x.view(x.size(0), -1)

        x = F.elu(self.fc1(x))
        x = F.elu(self.fc2(x))
        x = F.elu(self.fc3(x))
        return self.fc4(x)
