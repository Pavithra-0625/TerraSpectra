
import os
import glob
import numpy as np
from PIL import Image

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Dataset location
data_path = "data/raw/Wheat_Disease"

# Output location
output_path = "data/processed/Wheat_Disease"
os.makedirs(output_path, exist_ok=True)

# Disease categories
classes = [
    "BrownRust",
    "Healthy",
    "Mildew",
    "Septoria",
    "YellowRust"
]

images = []
labels = []

# Load and preprocess images
files = glob.glob(data_path + "/*.png") + glob.glob(data_path + "/*.jpeg")

for file in files:
    filename = os.path.basename(file)

    # Get disease name from filename
    label = next(
        (c for c in classes if filename.startswith(c)),
        None
    )

    if label is None:
        continue

    # Convert to RGB and resize
    img = Image.open(file).convert("RGB")
    img = img.resize((224, 224))

    # Normalize pixel values
    img = np.array(img, dtype=np.float32) / 255.0

    images.append(img)
    labels.append(label)

# Convert to arrays
X = np.array(images)
labels = np.array(labels)

# Convert category names to numbers
encoder = LabelEncoder()
y = encoder.fit_transform(labels)

# Split: 70% training, 15% validation, 15% testing
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

# Save datasets
np.savez_compressed(
    output_path + "/wheat_dataset.npz",
    X_train=X_train,
    X_val=X_val,
    X_test=X_test,
    y_train=y_train,
    y_val=y_val,
    y_test=y_test,
    classes=encoder.classes_
)

print("PREPROCESSING COMPLETED")
print("Total images:", len(X))
print("Training images:", len(X_train))
print("Validation images:", len(X_val))
print("Testing images:", len(X_test))
print("Classes:", list(encoder.classes_))
print("Image shape:", X_train.shape[1:])
