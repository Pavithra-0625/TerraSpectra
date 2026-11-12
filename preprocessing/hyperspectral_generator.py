
"""
TerraSpectra - Synthetic Hyperspectral Data Generator
Week 1, Day 1

Generates a mock 220-band crop data cube for testing
the satellite preprocessing pipeline.
"""

import os
import h5py
import numpy as np
import rasterio
import matplotlib.pyplot as plt

from rasterio.transform import from_origin


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

HEIGHT = 64
WIDTH = 64
BANDS = 220
RANDOM_SEED = 42

OUTPUT_DIR = "data/mock"
PLOT_DIR = "outputs/plots"

HDF5_PATH = os.path.join(OUTPUT_DIR, "crop_hyperspectral.h5")
GEOTIFF_PATH = os.path.join(OUTPUT_DIR, "crop_hyperspectral.tif")


# --------------------------------------------------
# 2. CREATE OUTPUT DIRECTORIES
# --------------------------------------------------

def create_directories():
    """Create directories required by the generator."""

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PLOT_DIR, exist_ok=True)


# --------------------------------------------------
# 3. GENERATE WAVELENGTH INFORMATION
# --------------------------------------------------

def generate_wavelengths():
    """Generate 220 wavelengths between 400 and 2500 nm."""

    return np.linspace(400, 2500, BANDS, dtype=np.float32)


# --------------------------------------------------
# 4. GENERATE HEALTHY CROP SPECTRAL SIGNATURE
# --------------------------------------------------

def healthy_signature(wavelengths):
    """Simulate a simplified healthy crop reflectance curve."""

    blue_absorption = 0.025 * np.exp(
        -((wavelengths - 450) / 45) ** 2
    )

    red_absorption = 0.08 * np.exp(
        -((wavelengths - 680) / 35) ** 2
    )

    red_edge = 0.35 / (
        1 + np.exp(-(wavelengths - 720) / 25)
    )

    water_absorption = 0.12 * np.exp(
        -((wavelengths - 1450) / 90) ** 2
    )

    signature = (
        0.12
        - blue_absorption
        - red_absorption
        + red_edge
        - water_absorption
    )

    return np.clip(signature, 0.01, 0.85)


# --------------------------------------------------
# 5. GENERATE STRESSED CROP SIGNATURE
# --------------------------------------------------

def stressed_signature(wavelengths, healthy):
    """Simulate illustrative crop stress spectral changes."""

    chlorophyll_effect = 0.04 * np.exp(
        -((wavelengths - 680) / 45) ** 2
    )

    nir_effect = 0.10 * np.exp(
        -((wavelengths - 850) / 180) ** 2
    )

    stressed = healthy - chlorophyll_effect - nir_effect

    return np.clip(stressed, 0.01, 0.85)


# --------------------------------------------------
# 6. CREATE SPATIAL STRESS MASK
# --------------------------------------------------

def generate_stress_mask():
    """Create a synthetic crop stress region."""

    mask = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

    rows, cols = np.ogrid[:HEIGHT, :WIDTH]

    center_y = HEIGHT // 2
    center_x = WIDTH // 2

    distance = (
        (rows - center_y) ** 2
        + (cols - center_x) ** 2
    )

    mask[distance < 16 ** 2] = 1

    return mask


# --------------------------------------------------
# 7. GENERATE HYPERSPECTRAL DATA CUBE
# --------------------------------------------------

def generate_hyperspectral_cube():
    """
    Create a synthetic H x W x B data cube.

    Class 0: Healthy crop
    Class 1: Illustrative stressed crop
    """

    rng = np.random.default_rng(RANDOM_SEED)

    wavelengths = generate_wavelengths()

    healthy = healthy_signature(wavelengths)

    stressed = stressed_signature(
        wavelengths, healthy
    )

    mask = generate_stress_mask()

    cube = np.zeros(
        (HEIGHT, WIDTH, BANDS),
        dtype=np.float32
    )

    for band in range(BANDS):

        healthy_value = healthy[band]
        stressed_value = stressed[band]

        cube[:, :, band] = np.where(
            mask == 1,
            stressed_value,
            healthy_value
        )

    noise = rng.normal(
        loc=0,
        scale=0.008,
        size=cube.shape
    )

    cube += noise.astype(np.float32)

    cube = np.clip(cube, 0, 1)

    return cube, mask, wavelengths


# --------------------------------------------------
# 8. SAVE DATA IN HDF5 FORMAT
# --------------------------------------------------

def save_hdf5(cube, mask, wavelengths):
    """Save hyperspectral data and metadata in HDF5."""

    with h5py.File(HDF5_PATH, "w") as file:

        file.create_dataset(
            "hyperspectral_cube",
            data=cube,
            compression="gzip"
        )

        file.create_dataset(
            "stress_mask",
            data=mask
        )

        file.create_dataset(
            "wavelengths_nm",
            data=wavelengths
        )

        file.attrs["project"] = "TerraSpectra"
        file.attrs["height"] = HEIGHT
        file.attrs["width"] = WIDTH
        file.attrs["bands"] = BANDS
        file.attrs["data_type"] = "Synthetic mock data"

    print(f"HDF5 saved: {HDF5_PATH}")


# --------------------------------------------------
# 9. SAVE DATA IN GEOTIFF FORMAT
# --------------------------------------------------

def save_geotiff(cube):
    """Save the spectral cube as a multiband GeoTIFF.

    This uses a synthetic local grid, not real farm
    coordinates or a validated geographic location.
    """

    raster_data = np.transpose(cube, (2, 0, 1))

    with rasterio.open(
        GEOTIFF_PATH,
        "w",
        driver="GTiff",
        height=HEIGHT,
        width=WIDTH,
        count=BANDS,
        dtype="float32",
        transform=from_origin(0, HEIGHT, 1, 1)
    ) as dataset:

        dataset.write(raster_data)

        dataset.update_tags(
            project="TerraSpectra",
            data_type="Synthetic mock data",
            bands=BANDS
        )

    print(f"GeoTIFF saved: {GEOTIFF_PATH}")


# --------------------------------------------------
# 10. CREATE VISUALIZATIONS
# --------------------------------------------------

def create_visualizations(cube, mask, wavelengths):
    """Save sample band, stress mask and spectra plots."""

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    axes[0].imshow(cube[:, :, 100], cmap="viridis")
    axes[0].set_title("Sample Spectral Band 101")
    axes[0].set_xlabel("Column")
    axes[0].set_ylabel("Row")

    axes[1].imshow(mask, cmap="gray")
    axes[1].set_title("Synthetic Stress Mask")
    axes[1].set_xlabel("Column")
    axes[1].set_ylabel("Row")

    plt.tight_layout()

    plt.savefig(
        os.path.join(PLOT_DIR, "sample_band_and_mask.png"),
        dpi=150
    )

    plt.close()

    healthy = healthy_signature(wavelengths)
    stressed = stressed_signature(wavelengths, healthy)

    plt.figure(figsize=(10, 5))

    plt.plot(
        wavelengths,
        healthy,
        label="Healthy crop"
    )

    plt.plot(
        wavelengths,
        stressed,
        label="Illustrative stressed crop"
    )

    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Reflectance")
    plt.title("Synthetic Crop Spectral Signatures")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        os.path.join(PLOT_DIR, "spectral_signatures.png"),
        dpi=150
    )

    plt.close()

    print("Visualization files generated.")


# --------------------------------------------------
# 11. DISPLAY DATA INFORMATION
# --------------------------------------------------

def display_information(cube, mask, wavelengths):
    """Print generated data information."""

    print("\n--- TerraSpectra Data Summary ---")

    print("Image height:", HEIGHT)
    print("Image width:", WIDTH)
    print("Spectral bands:", BANDS)

    print("Cube shape:", cube.shape)
    print("Mask shape:", mask.shape)

    print("Minimum reflectance:", cube.min())
    print("Maximum reflectance:", cube.max())

    print("Wavelength range:",
          wavelengths[0], "-", wavelengths[-1], "nm")

    print("Healthy pixels:", np.sum(mask == 0))
    print("Stressed pixels:", np.sum(mask == 1))


# --------------------------------------------------
# 12. MAIN EXECUTION
# --------------------------------------------------

def main():

    print("Starting TerraSpectra data generation...")

    create_directories()

    cube, mask, wavelengths = generate_hyperspectral_cube()

    save_hdf5(cube, mask, wavelengths)

    save_geotiff(cube)

    create_visualizations(cube, mask, wavelengths)

    display_information(cube, mask, wavelengths)

    print("\nTerraSpectra data generation completed!")


if __name__ == "__main__":
    main()
