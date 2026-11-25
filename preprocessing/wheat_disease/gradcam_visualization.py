
import os
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from PIL import Image

device = torch.device("cpu")

# Load dataset
data = np.load("data/processed/Wheat_Disease/wheat_dataset.npz")

X_test = data["X_test"]
y_test = data["y_test"]
classes = data["classes"]

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


model = WheatCNN(len(classes))

checkpoint = torch.load(
    "outputs/wheat_disease/wheat_cnn_v2.pth",
    map_location=device,
    weights_only=True
)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

# Store feature maps and gradients
feature_maps = None
gradients = None

def save_features(module, input, output):
    global feature_maps
    feature_maps = output

def save_gradients(module, grad_input, grad_output):
    global gradients
    gradients = grad_output[0]

# Register hooks on last convolution layer
target_layer = model.features[8]
target_layer.register_forward_hook(save_features)
target_layer.register_full_backward_hook(save_gradients)

# Output folder
os.makedirs("outputs/wheat_disease/gradcam", exist_ok=True)

# Select 5 test images
for i in range(5):

    image = torch.tensor(
        X_test[i]
    ).permute(2, 0, 1).unsqueeze(0).float()

    image.requires_grad_()

    model.zero_grad()

    output = model(image)
    prediction = output.argmax(dim=1).item()

    # Backpropagate predicted class
    score = output[0, prediction]
    score.backward()

    # Grad-CAM
    weights = gradients.mean(dim=(2, 3), keepdim=True)

    cam = (weights * feature_maps).sum(dim=1, keepdim=True)
    cam = torch.relu(cam)

    cam = torch.nn.functional.interpolate(
        cam,
        size=(224, 224),
        mode="bilinear",
        align_corners=False
    )

    cam = cam.squeeze().detach().numpy()

    cam = cam - cam.min()
    cam = cam / (cam.max() + 1e-8)

    # Original image
    original = X_test[i]

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(original)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(cam, cmap="jet")
    plt.title("Grad-CAM")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(original)
    plt.imshow(cam, cmap="jet", alpha=0.4)
    plt.title("Heatmap Overlay")
    plt.axis("off")

    true_label = classes[y_test[i]]
    predicted_label = classes[prediction]

    plt.suptitle(
        f"True: {true_label} | Predicted: {predicted_label}"
    )

    plt.tight_layout()

    plt.savefig(
        f"outputs/wheat_disease/gradcam/image_{i+1}.png"
    )

    plt.close()

print("Grad-CAM visualization completed.")
print("Saved 5 heatmaps in outputs/wheat_disease/gradcam/")
