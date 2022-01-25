# SPOT 71

# Resources
## https://arxiv.org/pdf/1604.07316.pdf
- MSE
- 10 FPS
- 3@66x200

# Model

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

# test 1
n_epochs = 9
batch_size = 32
training_loss = 0.027
validation_loss = 0.033

# test2
n_epochs = 11
batch_size = 32
training_loss = 0.026
validation_loss = 0.030

# test3
n_epochs = 14
batch_size = 32
training_loss = 0.020
validation_loss = 0.027

classes = 9 i 11