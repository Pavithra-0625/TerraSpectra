import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load shared PCA data
pca = np.load("data/processed/shared_pca/00000_pca.npy")

# Select first PCA component
component = pca[0]

# Identify valid pixels across all components
mask = np.any(pca != 0, axis=0)

# Mask background pixels
heatmap = np.ma.masked_where(~mask, component)

# Calculate colour limits using valid pixels only
valid_values = component[mask]
low, high = np.percentile(valid_values, [2, 98])

# Generate heatmap
cmap = plt.get_cmap("RdYlBu_r").copy()
cmap.set_bad("lightgray")

plt.figure(figsize=(12, 5))

plt.imshow(
    heatmap,
    cmap=cmap,
    vmin=low,
    vmax=high,
    aspect="auto"
)

plt.colorbar(label="PC1 Spectral Intensity")
plt.title("TerraSpectra - Crop Spectral Intensity Heatmap")
plt.xlabel("Pixel Width")
plt.ylabel("Pixel Height")

plt.tight_layout()

Path("outputs/plots").mkdir(parents=True, exist_ok=True)

plt.savefig(
    "outputs/plots/spectral_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("===== TERRASPECTRA HEATMAP =====")
print("PCA components:", pca.shape[0])
print("Valid crop pixels:", np.sum(mask))
print("Background pixels:", np.sum(~mask))
print("Valid area:", round(mask.mean() * 100, 2), "%")
print("Saved: outputs/plots/spectral_heatmap.png")
print("Status: SUCCESS")