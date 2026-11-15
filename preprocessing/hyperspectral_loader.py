
"""
TerraSpectra - Hyperspectral Data Loader

Loads hyperspectral TIFF files and validates their
spectral dimensions, pixel values, and background mask.
"""

from pathlib import Path

import numpy as np
import tifffile


EXPECTED_BANDS = 204
DAMAGED_FILES = {"02308.tiff"}


def load_hyperspectral_image(file_path):
    """Load and validate one hyperspectral TIFF image."""

    # Convert string path into a Path object first
    file_path = Path(file_path)

    # Skip known damaged files
    if file_path.name in DAMAGED_FILES:
        raise ValueError(f"Known damaged TIFF file: {file_path.name}")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    image = tifffile.imread(file_path)

    if image.ndim != 3:
        raise ValueError(
            f"Expected a 3D array, but received shape {image.shape}"
        )

    bands, height, width = image.shape

    if bands != EXPECTED_BANDS:
        raise ValueError(
            f"Expected {EXPECTED_BANDS} bands, but found {bands}"
        )

    if not np.issubdtype(image.dtype, np.number):
        raise TypeError("Image must contain numeric values")

    if not np.isfinite(image).all():
        raise ValueError("Image contains NaN or infinite values")

    # Identify pixels that are zero across every spectral band.
    background_mask = np.all(image == 0, axis=0)

    # Identify pixels containing at least one non-zero value.
    valid_mask = ~background_mask

    return image, valid_mask, background_mask


def print_image_report(image, valid_mask, background_mask):
    """Print a summary of the loaded hyperspectral image."""

    bands, height, width = image.shape
    total_pixels = height * width

    print("\n===== TERRASPECTRA IMAGE REPORT =====")
    print("Image dimensions:", height, "x", width)
    print("Spectral bands:", bands)
    print("Data type:", image.dtype)
    print("Minimum value:", image.min())
    print("Maximum value:", image.max())
    print("Total spatial pixels:", total_pixels)
    print("Potential valid pixels:", np.sum(valid_mask))
    print("Background pixels:", np.sum(background_mask))
    print(
        "Background percentage:",
        round(np.mean(background_mask) * 100, 2), "%"
    )
    print("=====================================")


if __name__ == "__main__":

    sample_path = (
        "data/raw/HyperLeaf2024/02392.tiff"
    )

    image, valid_mask, background_mask = (
        load_hyperspectral_image(sample_path)
    )

    print_image_report(image, valid_mask, background_mask)
