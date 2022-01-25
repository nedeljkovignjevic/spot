import matplotlib.pyplot as plt
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torchvision import utils


def show_activation(x):
    tensor = x.detach().clone()
    n, c, w, h = tensor.shape

    # tensor = tensor.view(n * c, -1, w, h)
    tensor = tensor[:, 0, :, :].unsqueeze(dim=1)

    rows = np.min((tensor.shape[0] // 8 + 1, 32))
    grid = utils.make_grid(tensor, nrow=8, normalize=True, padding=0)
    plt.figure(figsize=(8, rows))
    plt.imshow(grid.numpy().transpose((1, 2, 0)))
    plt.show()


class NvidiaModel(nn.Module):

    def __init__(self, show_first_activation=False):
        super(NvidiaModel, self).__init__()
        # self.show_first_activation = show_first_activation

        self.conv1 = nn.Conv2d(3, 12, kernel_size=(5, 5), stride=(2, 2))
        self.conv2 = nn.Conv2d(12, 24, kernel_size=(5, 5), stride=(2, 2))
        self.conv3 = nn.Conv2d(24, 36, kernel_size=(5, 5), stride=(2, 2))
        self.conv4 = nn.Conv2d(36, 48, kernel_size=(3, 3))
        self.conv5 = nn.Conv2d(48, 48, kernel_size=(3, 3))                  # 33 x 23 x 48

        self.dropout = nn.Dropout2d(0.5)

        self.fc1 = nn.Linear(7*5*48, 100)
        self.fc2 = nn.Linear(100, 50)
        self.fc3 = nn.Linear(50, 10)
        self.fc4 = nn.Linear(10, 1)

    def get_params_number(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def forward(self, x):
        x = x.view(x.size(0), 3, 320, 240)

        x = F.elu(self.conv1(x))

        if self.show_first_activation:
            show_activation(x)
            self.show_first_activation = False

        x = F.elu(self.conv2(x))
        x = F.elu(self.conv3(x))
        x = F.elu(F.max_pool2d(self.conv4(x), 2))
        x = F.elu(F.max_pool2d(self.conv5(x), 2))
        x = self.dropout(x)

        x = x.view(x.size(0), -1)

        x = F.elu(self.fc1(x))
        x = F.elu(self.fc2(x))
        x = F.elu(self.fc3(x))
        return self.fc4(x)
