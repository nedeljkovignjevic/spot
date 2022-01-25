# SPOT
SPOT is an open source driver assistance system for handmade toy car.

## Hardware


## SPOT 71
Model sadrzi blok od 5 konvolucionih slojeva koji se redukuju u 1680-dimenzioni feature vektor. Ovaj blok modela predstavlja nas vision model.
1680-dim vektor zatim prolazi kroz blok od 4 fully-connected slojeva koji
nam sluze kao policy model

Model sadrzi oko 240 hiljana parametera 

Empirijski smo demonstrirali da su konvolucione neuronske mreze u mogucnosti da nauce da prate odredjenu stazu odnosno put bez manuelne dekompozicije problema na detekciju linija, segmentaciju puta i slicno.


We use strided convolutions in the
first three convolutional layers with a 2×2 stride and a 5×5 kernel and a non-strided convolution
with a 3×3 kernel size in the last two convolutional layers.
240 thousand
parameters.

We have empirically demonstrated that CNNs are able to learn the entire task of lane and road
following without manual decomposition into road or lane marking detection, semantic abstraction,
path planning, and control. A small amount of training data from less than a hundred hours of driving
was sufficient to train the car to operate in diverse conditions, on highways, local and residential
roads in sunny, cloudy, and rainy conditions. The CNN is able to learn meaningful road features
from a very sparse training signal (steering alone).
The system learns for example to detect the outline of a road without the need of explicit labels
during training.
More work is needed to improve the robustness of the network, to find methods to verify the robustness, and to improve visualization of the network-internal processing steps.


### Architecture
self.conv1 = nn.Conv2d(3, 12, kernel_size=(5, 5), stride=(2, 2))
self.conv2 = nn.Conv2d(12, 24, kernel_size=(5, 5), stride=(2, 2))
self.conv3 = nn.Conv2d(24, 36, kernel_size=(5, 5), stride=(2, 2))
self.conv4 = nn.Conv2d(36, 48, kernel_size=(3, 3))
self.conv5 = nn.Conv2d(48, 48, kernel_size=(3, 3))                  # 7 x 5 x 48

self.dropout = nn.Dropout2d(0.5)

self.fc1 = nn.Linear(7*5*48, 100)
self.fc2 = nn.Linear(100, 50)
self.fc3 = nn.Linear(50, 10)
self.fc4 = nn.Linear(10, 1)

### Training params
optimizer = Adam with weight decay=1e-5
n_epochs = 14
batch_size = 32
training_loss = 0.020
validation_loss = 0.027