
"""
TerraSpectra - PCA Dimensionality Reduction

Reduces 204 spectral bands into 20 principal components
while excluding background pixels.
"""

from pathlib import Path

import numpy as np
import tifffile
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from hyperspectral_loader import load_hyperspectral_image


def apply_pca(image, valid_mask, n_components=20):
    """Apply PCA to valid hyperspectral pixels."""

    bands, height, width = image.shape

    # Convert image from (bands, height, width)
    # to (pixels, bands).
    pixel_spectra = image.reshape(bands, -1).T

    # Select pixels containing spectral information.
    valid_spectra = pixel_spectra[valid_mask.ravel()]

    if valid_spectra.shape[0] < n_components:
        raise ValueError("Not enough valid pixels for PCA.")

    if n_components > bands:
        raise ValueError("Components cannot exceed spectral bands.")

    # Convert to floating-point values.
    valid_spectra = valid_spectra.astype(np.float32)

    # Standardize spectral features.
    scaler = StandardScaler()
    scaled_spectra = scaler.fit_transform(valid_spectra)

    # Apply PCA.
    pca = PCA(n_components=n_components)
    reduced_spectra = pca.fit_transform(scaled_spectra)

    # Reconstruct spatial component images.
    reduced_image = np.zeros(
        (n_components, height * width),
        dtype=np.float32
    )

    reduced_image[:, valid_mask.ravel()] = reduced_spectra.T

    reduced_image = reduced_image.reshape(
        n_components, height, width
    )

    return reduced_image, pca.explained_variance_ratio_, pca


if __name__ == "__main__":

    sample_path = "data/raw/HyperLeaf2024/02392.tiff"

    image, valid_mask, background_mask = (
        load_hyperspectral_image(sample_path)
    )

    reduced_image, variance_ratio, pca = apply_pca(
        image,
        valid_mask,
        n_components=20
    )

    print("\n===== TERRASPECTRA PCA REPORT =====")
    print("Original spectral bands:", image.shape[0])
    print("Reduced components:", reduced_image.shape[0])
    print("Reduced image shape:", reduced_image.shape)

    print(
        "Total explained variance:",
        round(float(np.sum(variance_ratio)) * 100, 2), "%"
    )

    print("First 5 component variance percentages:")

    for index, variance in enumerate(variance_ratio[:5], start=1):
        print(f"PC{index}: {variance * 100:.2f}%")

    # Save PCA output.
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "02392_pca.npy"
    np.save(output_path, reduced_image)

    print("PCA output saved:", output_path)
    print("===================================")
