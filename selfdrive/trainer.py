import os

import torch
import torch.utils.data

from torch import optim
import torch.nn as nn


class TrainerConfig:

    def __init__(self, n_epochs, batch_size, weight_decay, checkpoint_path):
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.weight_decay = weight_decay
        self.checkpoint_path = checkpoint_path


class Trainer:

    def __init__(self, model, train_data, validation_data, config):
        self.model = model
        self.train_data = train_data
        self.validation_data = validation_data
        self.config = config

        self.device = 'cpu'
        if torch.cuda.is_available():
            self.device = torch.cuda.current_device()
            self.model = self.model.to(self.device)

    def save_checkpoint(self, epoch, state_dict, optimizer_dict):
        state = {
            'epoch': epoch,
            'state_dict': state_dict,
            'optimizer_dict': optimizer_dict
        }

        if not os.path.exists(self.config.checkpoint_path):
            os.makedirs(self.config.checkpoint_path)

        torch.save(state_dict, f'{self.config.checkpoint_path}-{epoch}')

    def train(self):
        model = self.model
        device = self.device

        train_data, validation_data = self.train_data, self.validation_data

        n_epochs = self.config.n_epochs
        batch_size = self.config.batch_size
        weight_decay = self.config.weight_decay

        train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size)
        validation_loader = torch.utils.data.DataLoader(validation_data, batch_size=batch_size)

        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), weight_decay=weight_decay)

        for epoch in range(n_epochs):

            train_loss = 0
            n_train_losses = 0
            model.train()
            for batch_idx, (x, y) in enumerate(train_loader):
                input, target = x.to(device).float(), y.to(device).float().unsqueeze(-1)

                optimizer.zero_grad()
                output = model(input)

                loss = criterion(output, target)
                loss.backward()
                optimizer.step()

                train_loss += loss.item()
                n_train_losses += 1

            print(f'epoch: {epoch + 1}, loss: {train_loss / n_train_losses}')

            valid_loss = 0
            n_valid_losses = 0
            model.eval()
            with torch.no_grad():
                for (x, y) in validation_loader:
                    input, target = x.to(device).float(), y.to(device).float().unsqueeze(-1)

                    output = model(input)
                    loss = criterion(output, target)
                    valid_loss += loss.item()
                    n_valid_losses += 1

            print(f'epoch: {epoch + 1}, validation loss: {valid_loss / n_valid_losses}')
            self.save_checkpoint(epoch, model.state_dict(), optimizer.state_dict())