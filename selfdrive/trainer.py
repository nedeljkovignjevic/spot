import os
import torch
import torch.utils.data

from torch import optim


class TrainerConfig:

    def __init__(self, n_epochs, batch_size, criterion, checkpoint_path):
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.criterion = criterion
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

        torch.save(state, f'{self.config.save_path}model-{epoch}')

    def train(self):
        model, train_data, validation_data, config, device = self.model, self.train_data, self.validation_data, self.config, self.device

        train_loader = torch.utils.data.DataLoader(train_data, batch_size=config.batch_size, shuffle=True)
        validation_loader = torch.utils.data.DataLoader(validation_data, batch_size=config.batch_size, shuffle=True)

        n_epochs = config['n_epochs']
        criterion = config['criterion']
        optimizer = optim.Adam(model.parameters())

        for epoch in range(n_epochs):

            train_loss = 0
            n_train_losses = 0
            model.train()
            for batch_idx, (x, y) in enumerate(train_loader):
                input, target = x.to(device).float(), y.to(device).long()

                optimizer.zero_grad()
                output = model(input)

                loss = criterion(output, target)
                loss.backward()
                optimizer.step()

                train_loss += loss.item()
                n_train_losses += 1

            print(f'epoch: {epoch}, loss: {train_loss / n_train_losses}')

            valid_loss = 0
            n_valid_losses = 0
            model.eval()
            with torch.no_grad():
                for (x, y) in validation_loader:
                    input, target = x.to(device).float(), y.to(device).long()

                    output = model(input)
                    loss = criterion(output, target)
                    valid_loss += loss.item()
                    n_valid_losses += 1

            print(f'epoch: {epoch}, validation loss: {valid_loss / n_valid_losses}')
            self.save_checkpoint(epoch, model.state_dict(), optimizer.state_dict())
