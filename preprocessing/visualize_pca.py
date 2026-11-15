
import numpy as np
import matplotlib.pyplot as plt
import tifffile

# Load PCA output
pca_image = np.load("data/processed/02392_pca.npy")

# Load original image to identify background
original = tifffile.imread("data/raw/HyperLeaf2024/02392.tiff")
valid_mask = np.any(original > 0, axis=0)

print("PCA array shape:", pca_image.shape)

# Create a larger visualization
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for i in range(3):

    component = pca_image[i]

    # Exclude background when calculating display limits
    valid_values = component[valid_mask]
    lower = np.percentile(valid_values, 2)
    upper = np.percentile(valid_values, 98)

    # Hide background pixels
    display_image = np.ma.masked_where(
        ~valid_mask, component
    )

    axes[i].imshow(
        display_image,
        cmap="viridis",
        aspect="auto",
        vmin=lower,
        vmax=upper
    )

    axes[i].set_title(f"Principal Component {i + 1}", fontsize=13)
    axes[i].set_xlabel("Image Width")
    axes[i].set_ylabel("Image Height")

fig.suptitle(
    "TerraSpectra - PCA Visualization",
    fontsize=17,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "outputs/plots/pca_components.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Improved PCA visualization saved successfully!")
