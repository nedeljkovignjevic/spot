# spot
spot is an open source driver assistance system for handmade toy car.

## Hardware
- 4WD Smart Car Chassis
- ESP32 - system on a chip microcontroller with integrated Wi-Fi
- Mobile phone camera 

<img src="https://user-images.githubusercontent.com/54076398/151218678-e9c0dc6c-fb38-47d0-bfe0-3ae9b75d015a.png" width="50%" height="50%">

## Self-driving model
Self-driving model architecture is inspired by [Nvidia Network from 2016.](https://developer.nvidia.com/blog/deep-learning-self-driving-cars/) \
Model is trained fully end-to-end. \
It takes an image and outputs how you should drive, in our case the model outputs a steering angle value [-1, 1]

Model starts with a block of 5 fully-convolutional layers that reduces down to a 1680-dimensional vector. \
This block represents our vision model and it should extract all features from an image that are essential to driving. \
The resulting 1680-dim feature vector then goes into a block of 4 fully connected layers that represent our policy model.

## Results
Model has successfully learned to drive on a track he has never seen before, neither on the training dataset nor on the validation dataset.

![](https://media.giphy.com/media/6tmKCC5sMNMcBLoEnr/giphy-downsized-large.gif)
