
import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.utils.class_weight import compute_class_weight

# Reproducibility
torch.manual_seed(42)
np.random.seed(42)

# Device
device = torch.device("cpu")
print("Training device:", device)

# Load dataset
data = np.load("data/processed/Wheat_Disease/wheat_dataset.npz")

X_train = torch.tensor(data["X_train"]).permute(0, 3, 1, 2)
X_val = torch.tensor(data["X_val"]).permute(0, 3, 1, 2)

y_train = torch.tensor(data["y_train"], dtype=torch.long)
y_val = torch.tensor(data["y_val"], dtype=torch.long)

classes = data["classes"]
num_classes = len(classes)

# Data loaders
train_loader = DataLoader(
    TensorDataset(X_train, y_train),
    batch_size=16,
    shuffle=True
)

val_loader = DataLoader(
    TensorDataset(X_val, y_val),
    batch_size=16
)

# Class weights
weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(data["y_train"]),
    y=data["y_train"]
)

weights = torch.tensor(weights, dtype=torch.float32)

# CNN model
class WheatCNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.AdaptiveAvgPool2d((1, 1))
        )

        self.classifier = nn.Linear(64, num_classes)

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        return self.classifier(x)


model = WheatCNN(num_classes).to(device)

criterion = nn.CrossEntropyLoss(weight=weights)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training
epochs = 10

for epoch in range(epochs):

    model.train()
    train_loss = 0
    correct = 0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        correct += (outputs.argmax(1) == labels).sum().item()

    train_accuracy = correct / len(X_train)

    # Validation
    model.eval()
    val_loss = 0
    val_correct = 0

    with torch.no_grad():
        for images, labels in val_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)

            val_loss += loss.item()
            val_correct += (
                outputs.argmax(1) == labels
            ).sum().item()

    val_accuracy = val_correct / len(X_val)

    print(
        f"Epoch {epoch+1}/{epochs} | "
        f"Train Loss: {train_loss/len(train_loader):.4f} | "
        f"Train Accuracy: {train_accuracy:.4f} | "
        f"Validation Loss: {val_loss/len(val_loader):.4f} | "
        f"Validation Accuracy: {val_accuracy:.4f}"
    )

# Save model
os.makedirs("outputs/wheat_disease", exist_ok=True)

torch.save(
    {
        "model_state_dict": model.state_dict(),
        "classes": classes.tolist()
    },
    "outputs/wheat_disease/wheat_cnn.pth"
)

print("\nCNN TRAINING COMPLETED")
print("Model saved successfully.")
