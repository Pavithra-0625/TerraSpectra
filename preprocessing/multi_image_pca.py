
"""
TerraSpectra - Multi-Image PCA Validation

Tests PCA preprocessing on five readable
hyperspectral images.
"""

from pathlib import Path
import numpy as np

from pca_reduction import apply_pca
from hyperspectral_loader import load_hyperspectral_image


# Project paths
VALID_LIST = Path("outputs/reports/valid_hyperspectral_images.txt")
INPUT_DIR = Path("data/raw/HyperLeaf2024")
OUTPUT_DIR = Path("data/processed/multi_image_pca")

N_COMPONENTS = 20
MAX_IMAGES = 50


def process_multiple_images():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image_names = VALID_LIST.read_text().splitlines()
    selected_images = image_names[:MAX_IMAGES]

    successful = 0
    failed = []

    print("\n===== TERRASPECTRA MULTI-IMAGE PCA =====")
    print("Images selected:", len(selected_images))

    for index, image_name in enumerate(selected_images, start=1):

        image_path = INPUT_DIR / image_name

        try:
            print(f"\nProcessing {index}/{len(selected_images)}: {image_name}")

            image, valid_mask, background_mask = (
                load_hyperspectral_image(str(image_path))
            )

            reduced_image, variance_ratio, pca = apply_pca(
                image,
                valid_mask,
                n_components=N_COMPONENTS
            )

            output_path = OUTPUT_DIR / f"{image_path.stem}_pca.npy"

            np.save(output_path, reduced_image)

            explained_variance = float(np.sum(variance_ratio)) * 100

            print("Original shape:", image.shape)
            print("Reduced shape:", reduced_image.shape)
            print(
                "Explained variance:",
                f"{explained_variance:.2f}%"
            )
            print("Saved:", output_path)

            successful += 1

        except Exception as error:
            failed.append((image_name, str(error)))
            print("FAILED:", error)

    print("\n===== VALIDATION SUMMARY =====")
    print("Total selected:", len(selected_images))
    print("Successfully processed:", successful)
    print("Failed:", len(failed))

    for name, error in failed:
        print(f"{name}: {error}")

    print("Output directory:", OUTPUT_DIR)


if __name__ == "__main__":
    process_multiple_images()
