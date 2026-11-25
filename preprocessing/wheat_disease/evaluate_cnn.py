
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load dataset
data = np.load("data/processed/Wheat_Disease/wheat_dataset.npz")

X_test = torch.tensor(data["X_test"]).permute(0, 3, 1, 2)
y_test = data["y_test"]
classes = data["classes"].tolist()

# CNN architecture (same as training)
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

# Load trained model
model = WheatCNN(len(classes))

checkpoint = torch.load(
    "outputs/wheat_disease/wheat_cnn.pth",
    map_location="cpu",
    weights_only=False
)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

# Predict in batches
predictions = []

with torch.no_grad():
    for i in range(0, len(X_test), 16):
        images = X_test[i:i+16]
        outputs = model(images)
        predictions.extend(outputs.argmax(1).numpy())

# Evaluation
print("Test Accuracy:", accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    labels=list(range(len(classes))),
    target_names=classes,
    zero_division=0
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))
