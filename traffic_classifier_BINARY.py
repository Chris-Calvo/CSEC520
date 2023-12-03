import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from sklearn.metrics import confusion_matrix, f1_score

def train_traffic_classifier(train_file_path, test_file_path):
    # Load the training dataset, split into input (X_train) and output (y_train) variables
    train_dataset = np.loadtxt(train_file_path, delimiter=',', skiprows=1)
    X_train = train_dataset[:, 0:28]
    y_train = train_dataset[:, 28]

    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32).reshape(-1, 1)

    # Define the model
    class TrafficClassifier(nn.Module):
        def __init__(self):
            super().__init__()
            self.hidden1 = nn.Linear(28, 12)
            self.act1 = nn.ReLU()
            self.hidden2 = nn.Linear(12, 8)
            self.act2 = nn.ReLU()
            self.output = nn.Linear(8, 1)
            self.act_output = nn.Sigmoid()

        def forward(self, x):
            x = self.act1(self.hidden1(x))
            x = self.act2(self.hidden2(x))
            x = self.act_output(self.output(x))
            return x

    model = TrafficClassifier()

    # Train the model
    loss_fn = nn.BCELoss()  # binary cross-entropy
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    n_epochs = 100
    batch_size = 1000

    for epoch in range(n_epochs):
        total_loss = 0.0  # Initialize total loss for this epoch
        for i in range(0, len(X_train), batch_size):
            X_batch = X_train[i:i + batch_size]
            y_pred = model(X_batch)
            y_batch = y_train[i:i + batch_size]
            loss = loss_fn(y_pred, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f'Finished epoch {epoch}, latest loss {loss}')

    # Load the testing dataset
    test_dataset = np.loadtxt(test_file_path, delimiter=',', skiprows=1)
    random.shuffle(test_dataset)
    X_test = torch.tensor(test_dataset[:, 0:28], dtype=torch.float32)

    # Make predictions on the testing data
    y_pred_test = (model(X_test) > 0.5).int()

    # Print class predictions for the first 5 examples
    for i in range(5):
        print('%s => %d' % (X_test[i].tolist(), y_pred_test[i]))

    # Evaluate the model on the testing data
    # Load true labels from the original testing dataset
    y_true_test = test_dataset[:, 28]
    if y_true_test is not None:
        cm = confusion_matrix(y_true_test, y_pred_test)
        f1 = f1_score(y_true_test, y_pred_test)
        print(f'Confusion Matrix:\n{cm}')
        print(f'F1 Score: {f1}')

# Uncomment the line below if you want to run the training when the script is executed.
#train_traffic_classifier('training_output.csv', 'testing_output.csv')
