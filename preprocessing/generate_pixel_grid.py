import numpy as np
import json
from pathlib import Path

# Load PCA data
pca = np.load("data/processed/shared_pca/00000_pca.npy")

# Select first PCA component
pc1 = pca[0]

# Identify valid crop pixels
mask = np.any(pca != 0, axis=0)

# Normalize valid values between 0 and 1
values = pc1[mask]

low, high = np.percentile(values, [2, 98])

normalized = np.clip(
    (pc1 - low) / (high - low),
    0,
    1
)

# Keep background pixels as null
grid = []

for row in range(pc1.shape[0]):
    grid_row = []

    for col in range(pc1.shape[1]):
        if mask[row, col]:
            grid_row.append(round(float(normalized[row, col]), 4))
        else:
            grid_row.append(None)

    grid.append(grid_row)

# Prepare output
data = {
    "width": pc1.shape[1],
    "height": pc1.shape[0],
    "component": "PC1",
    "valid_pixels": int(mask.sum()),
    "grid": grid
}

Path("dashboard/public/data").mkdir(
    parents=True, exist_ok=True
)

with open("dashboard/public/data/pixel_grid.json", "w") as f:
    json.dump(data, f)

print("===== PIXEL GRID GENERATED =====")
print("Width:", data["width"])
print("Height:", data["height"])
print("Valid pixels:", data["valid_pixels"])
print("Component:", data["component"])
print("Saved: dashboard/public/data/pixel_grid.json")
print("Status: SUCCESS")