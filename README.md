# SPOT 71
SPOT 71 is an open source driver assistance system for handmade toy car. \
Model is predicting steering value [-1, 1] based on input image.

## Model
Model is based on Nvidia CNN from 2016. -- https://arxiv.org/pdf/1604.07316.pdf \
Input --> img 320x240x3 \
Output --> steering value [-1, 1]

```
class NvidiaModel(nn.Module):

    def __init__(self, show_first_activation=False):
        super(NvidiaModel, self).__init__()

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

    def forward(self, x):
        x = x.view(x.size(0), 3, 320, 240)

        x = F.elu(self.conv1(x))
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
```

### Training params
optimizer = Adam with weight decay=1e-5 \
n_epochs = 14 \
batch_size = 32 \
training_loss = 0.020 \
validation_loss = 0.027

## Results
