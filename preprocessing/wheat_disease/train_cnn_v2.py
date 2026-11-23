
import os
import copy
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from torchvision import transforms
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import accuracy_score

torch.manual_seed(42)
np.random.seed(42)

device = torch.device("cpu")
print("Training device:", device)

# Load dataset
data = np.load("data/processed/Wheat_Disease/wheat_dataset.npz")

X_train = torch.tensor(data["X_train"]).permute(0, 3, 1, 2).float()
X_val = torch.tensor(data["X_val"]).permute(0, 3, 1, 2).float()

y_train = torch.tensor(data["y_train"], dtype=torch.long)
y_val = torch.tensor(data["y_val"], dtype=torch.long)

classes = data["classes"]
num_classes = len(classes)

# Data augmentation
augment = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15)
])

class WheatDataset(torch.utils.data.Dataset):
    def __init__(self, X, y, training=False):
        self.X = X
        self.y = y
        self.training = training

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        image = self.X[index]
        if self.training:
            image = augment(image)
        return image, self.y[index]

train_loader = DataLoader(
    WheatDataset(X_train, y_train, True),
    batch_size=16,
    shuffle=True
)

val_loader = DataLoader(
    WheatDataset(X_val, y_val),
    batch_size=16
)

# Class weights
weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(data["y_train"]),
    y=data["y_train"]
)

weights = torch.tensor(weights, dtype=torch.float32)

# Improved CNN
class WheatCNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.AdaptiveAvgPool2d((1, 1))
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.4),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        return self.classifier(self.features(x))

model = WheatCNN(num_classes).to(device)

criterion = nn.CrossEntropyLoss(weight=weights)
optimizer = torch.optim.AdamW(
    model.parameters(), lr=0.001, weight_decay=0.0001
)

epochs = 20
best_accuracy = 0
best_model = copy.deepcopy(model.state_dict())
patience = 5
wait = 0

# Training
for epoch in range(epochs):

    model.train()
    train_loss = 0
    train_correct = 0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        train_correct += (outputs.argmax(1) == labels).sum().item()

    model.eval()
    val_loss = 0
    val_correct = 0

    with torch.no_grad():
        for images, labels in val_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)

            val_loss += loss.item()
            val_correct += (outputs.argmax(1) == labels).sum().item()

    train_accuracy = train_correct / len(X_train)
    val_accuracy = val_correct / len(X_val)

    print(
        f"Epoch {epoch+1}/{epochs} | "
        f"Train Loss: {train_loss/len(train_loader):.4f} | "
        f"Train Accuracy: {train_accuracy:.4f} | "
        f"Validation Loss: {val_loss/len(val_loader):.4f} | "
        f"Validation Accuracy: {val_accuracy:.4f}"
    )

    if val_accuracy > best_accuracy:
        best_accuracy = val_accuracy
        best_model = copy.deepcopy(model.state_dict())
        wait = 0
    else:
        wait += 1

    if wait >= patience:
        print("Early stopping.")
        break

# Save best model separately
os.makedirs("outputs/wheat_disease", exist_ok=True)

torch.save(
    {
        "model_state_dict": best_model,
        "classes": classes.tolist()
    },
    "outputs/wheat_disease/wheat_cnn_v2.pth"
)

print("\nTraining completed.")
print("Best validation accuracy:", best_accuracy)
print("Saved: wheat_cnn_v2.pth")
