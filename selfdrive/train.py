import torch.nn as nn


n_epochs = 5
batch_size = 64
criterion = nn.MSELoss()
checkpoint_path = "./models"

# lr = 1e-4
# weight_decay = 1e-5
# num_workers = 8
test_size = 0.8
shuffle = True