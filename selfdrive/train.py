from model import NvidiaModel
from trainer import TrainerConfig, Trainer
from processing import load_data

import numpy as np


def main():
    model = NvidiaModel()
    print(f'Number of parameters: {model.get_params_number()}')

    data = load_data()

    np.random.shuffle(data)

    validation_fraction = 0.1

    valid_idx = int(len(data) * (1 - validation_fraction))

    train_data = data[:valid_idx]
    print(f'Training dataset size: {len(train_data)}')

    validation_data = data[valid_idx:]
    print(f'Validation dataset size: {len(validation_data)}')

    config = TrainerConfig(n_epochs=20,
                           batch_size=32,
                           weight_decay=1e-5,
                           checkpoint_path='./models/model-final')

    trainer = Trainer(model=model,
                      train_data=train_data,
                      validation_data=validation_data,
                      config=config)

    trainer.train()


if __name__ == '__main__':
    main()



