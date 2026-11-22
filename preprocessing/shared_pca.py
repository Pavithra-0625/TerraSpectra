
"""
TerraSpectra - Shared PCA
Fits one scaler and one Incremental PCA model
across multiple hyperspectral images.
"""

from pathlib import Path
import gc
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import IncrementalPCA

from hyperspectral_loader import load_hyperspectral_image

VALID_LIST = Path("outputs/reports/selected_1000_images.txt")
INPUT_DIR = Path("data/raw/HyperLeaf2024")
OUTPUT_DIR = Path("data/processed/shared_pca")

N_COMPONENTS = 20
BATCH_SIZE = 512


def load_image_spectra(image_name):
    image_path = INPUT_DIR / image_name

    image, valid_mask, _ = load_hyperspectral_image(str(image_path))

    spectra = image.reshape(image.shape[0], -1).T
    spectra = spectra[valid_mask.ravel()]

    return spectra.astype(np.float32), valid_mask, image.shape


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image_names = VALID_LIST.read_text().splitlines()

    print("Images selected:", len(image_names))

    # Pass 1: Learn shared scaling statistics.
    scaler = StandardScaler()

    print("\nPASS 1: Fitting shared scaler")

    for index, name in enumerate(image_names, start=1):
        spectra, _, _ = load_image_spectra(name)

        scaler.partial_fit(spectra)

        if index % 100 == 0:
            print(f"Scaler processed: {index}/{len(image_names)}")

        del spectra
        gc.collect()

    
    # Pass 2: Learn one shared PCA model.
    pca = IncrementalPCA(
        n_components=N_COMPONENTS,
        batch_size=BATCH_SIZE
    )

    print("\nPASS 2: Fitting shared PCA")

    pending = np.empty((0, 204), dtype=np.float32)

    for index, name in enumerate(image_names, start=1):
        spectra, _, _ = load_image_spectra(name)

        scaled = scaler.transform(spectra)

        # Combine remaining pixels with the current image.
        pending = np.concatenate((pending, scaled), axis=0)

        # Process complete batches while retaining at least
        # 20 pixels for a valid final batch.
        while len(pending) >= BATCH_SIZE + N_COMPONENTS:
            batch = pending[:BATCH_SIZE]
            pending = pending[BATCH_SIZE:]

            pca.partial_fit(batch)

        if index % 100 == 0:
            print(f"PCA processed: {index}/{len(image_names)}")

        del spectra, scaled
        gc.collect()

    # Process the remaining pixels.
    if len(pending) >= N_COMPONENTS:
        pca.partial_fit(pending)
    else:
        raise ValueError("Not enough remaining pixels for final PCA batch.")

    del pending
    gc.collect()

    # Save the shared scaler and PCA model.
    np.save(OUTPUT_DIR / "scaler_mean.npy", scaler.mean_)
    np.save(OUTPUT_DIR / "scaler_scale.npy", scaler.scale_)

    np.save(OUTPUT_DIR / "pca_components.npy", pca.components_)
    np.save(OUTPUT_DIR / "pca_mean.npy", pca.mean_)
    np.save(
        OUTPUT_DIR / "explained_variance_ratio.npy",
        pca.explained_variance_ratio_
    )

    # Pass 3: Transform all images using the same model.
    print("\nPASS 3: Transforming images")

    for index, name in enumerate(image_names, start=1):
        spectra, valid_mask, original_shape = load_image_spectra(name)

        scaled = scaler.transform(spectra)
        reduced = pca.transform(scaled)

        height, width = original_shape[1:]

        output = np.zeros(
            (N_COMPONENTS, height * width),
            dtype=np.float32
        )

        output[:, valid_mask.ravel()] = reduced.T

        output = output.reshape(N_COMPONENTS, height, width)

        output_path = OUTPUT_DIR / f"{Path(name).stem}_pca.npy"
        np.save(output_path, output)

        if index % 100 == 0:
            print(f"Transformed: {index}/{len(image_names)}")

        del spectra, scaled, reduced, output
        gc.collect()

    print("\nSHARED PCA COMPLETED")
    print("Images processed:", len(image_names))
    print("Components:", N_COMPONENTS)
    print(
        "Explained variance:",
        round(float(pca.explained_variance_ratio_.sum()) * 100, 2),
        "%"
    )
    print("Output directory:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
