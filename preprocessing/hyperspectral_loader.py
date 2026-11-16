
"""
TerraSpectra - Hybrid Hyperspectral Data Loader

Uses Rasterio for raster metadata and spatial validation.
Uses tifffile to reconstruct the complete hyperspectral cube.
"""

from pathlib import Path
import json

import numpy as np
import rasterio
import tifffile


EXPECTED_BANDS = 204
EXPECTED_HEIGHT = 48
EXPECTED_WIDTH = 352

DAMAGED_FILES = {
    "02308.tiff",
    "01870.tiff",
    "01871.tiff",
    "01873.tiff",
    "01874.tiff",
    "01876.tiff",
}


def load_hyperspectral_image(file_path):
    """Load and validate a hyperspectral TIFF using both libraries."""

    file_path = Path(file_path)

    if file_path.name in DAMAGED_FILES:
        raise ValueError(f"Known damaged TIFF file: {file_path.name}")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Step 1: Read spatial raster information using Rasterio.
    with rasterio.open(file_path) as src:

        raster_width = src.width
        raster_height = src.height
        raster_band_count = src.count
        raster_dtypes = src.dtypes
        raster_crs = src.crs

        # Read the spatial raster band.
        raster_spatial = src.read(1)

        # Read TIFF metadata.
        tags = src.tags()
        description = tags.get("TIFFTAG_IMAGEDESCRIPTION", "")

        metadata_shape = None

        if description:
            try:
                metadata_shape = json.loads(description).get("shape")
            except (json.JSONDecodeError, AttributeError):
                metadata_shape = None

    if raster_spatial.shape != (raster_height, raster_width):
        raise ValueError("Rasterio spatial dimensions are inconsistent")

    if (raster_height, raster_width) != (
        EXPECTED_HEIGHT, EXPECTED_WIDTH
    ):
        raise ValueError(
            f"Unexpected spatial dimensions: "
            f"{raster_height} x {raster_width}"
        )

    if metadata_shape is not None:
        if metadata_shape != [
            EXPECTED_BANDS, EXPECTED_HEIGHT, EXPECTED_WIDTH
        ]:
            raise ValueError(
                f"Unexpected TIFF metadata shape: {metadata_shape}"
            )

    # Step 2: Reconstruct the complete spectral cube using tifffile.
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

    if (height, width) != (raster_height, raster_width):
        raise ValueError(
            "Rasterio and tifffile spatial dimensions do not match"
        )

    if not np.issubdtype(image.dtype, np.number):
        raise TypeError("Image must contain numeric values")

    if not np.isfinite(image).all():
        raise ValueError("Image contains NaN or infinite values")

    # Step 3: Identify background and valid pixels.
    background_mask = np.all(image == 0, axis=0)
    valid_mask = ~background_mask

    print("\n===== HYBRID LOADER REPORT =====")
    print("File:", file_path.name)
    print("Rasterio dimensions:", raster_height, "x", raster_width)
    print("Rasterio stored bands:", raster_band_count)
    print("Rasterio data types:", raster_dtypes)
    print("Rasterio CRS:", raster_crs)
    print("Hyperspectral cube shape:", image.shape)
    print("Hyperspectral bands:", bands)
    print("Data type:", image.dtype)
    print("Valid pixels:", np.sum(valid_mask))
    print("Background pixels:", np.sum(background_mask))
    print("================================")

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

    sample_path = "data/raw/HyperLeaf2024/02392.tiff"

    image, valid_mask, background_mask = (
        load_hyperspectral_image(sample_path)
    )

    print_image_report(image, valid_mask, background_mask)
