
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

device = torch.device("cpu")

# Load test data
data = np.load("data/processed/Wheat_Disease/wheat_dataset.npz")

X_test = torch.tensor(data["X_test"]).permute(0, 3, 1, 2).float()
y_test = torch.tensor(data["y_test"], dtype=torch.long)

classes = data["classes"]
num_classes = len(classes)

test_loader = DataLoader(
    TensorDataset(X_test, y_test),
    batch_size=16
)

# CNN V2 architecture
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


# Load V2 checkpoint
model = WheatCNN(num_classes)

checkpoint = torch.load(
    "outputs/wheat_disease/wheat_cnn_v2.pth",
    map_location=device,
    weights_only=True
)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

# Predict
y_true = []
y_pred = []

with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        predictions = outputs.argmax(1)

        y_true.extend(labels.numpy())
        y_pred.extend(predictions.numpy())

# Evaluation
accuracy = accuracy_score(y_true, y_pred)

print("CNN V2 Test Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(
    y_true,
    y_pred,
    labels=list(range(num_classes)),
    target_names=classes,
    zero_division=0
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))
