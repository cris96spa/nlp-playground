import random

import polars as pl
import torch
from matplotlib import pyplot as plt
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
from tqdm import tqdm

from nlp_playground.neural_network_hello_word import NeuralNetwork

# Load Training Data
training_data = datasets.FashionMNIST(
    root="data", train=True, download=True, transform=ToTensor()
)

# Load Test Data
test_data = datasets.FashionMNIST(
    root="data", train=False, download=True, transform=ToTensor()
)


BATCH_SIZE = 64
LABELS_MAP = {
    0: "T-shirt/top",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle boot",
}
DEBUG = False

# Create Data Loaders
train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE)
test_dataloader = DataLoader(test_data, batch_size=BATCH_SIZE)

if DEBUG:
    figure = plt.figure(figsize=(8, 8))
    cols, rows = 3, 3

    for i in range(1, cols * rows + 1):
        sample_idx = torch.randint(len(training_data), size=(1,)).item()
        img: torch.Tensor = training_data[sample_idx][0]
        label: int = training_data[sample_idx][1]
        figure.add_subplot(rows, cols, i)
        plt.title(LABELS_MAP[label])
        plt.axis("off")
        plt.imshow(img.squeeze())
    plt.show()

    for X, y in iter(train_dataloader):
        print("Shape of X [N, C, H, W]: ", X.shape)
        print("Shape of y: ", y.shape, y.dtype)
        break

device = (
    torch.accelerator.current_accelerator().type
    if torch.accelerator.is_available()
    else "cpu"
)
model = NeuralNetwork().to(device)

loss = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)


def train(dataloader, model: nn.Module, loss_fn, optimizer):
    size = len(dataloader.dataset)
    # Set the model to training mode. In essence, this enables
    # the training-specific behavior (e.g. dropout, batch norm)
    model.train()

    # Iterate over data batches
    for batch, (X, y) in enumerate(dataloader):
        # Assign data to device
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test(dataloader, model: nn.Module, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        test_loss /= num_batches
        correct /= size
        print(
            f"Test Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {test_loss:>8f} \n"
        )


epochs = 100
for t in tqdm(range(epochs), desc="Training Loop"):
    train(train_dataloader, model, loss, optimizer)
    test(test_dataloader, model, loss)
print("Done!")
