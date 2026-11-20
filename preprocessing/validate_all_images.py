
from pathlib import Path
from hyperspectral_loader import load_hyperspectral_image
from contextlib import redirect_stdout
import io
import gc

DATA_FOLDER = Path("data/raw/HyperLeaf2024")
REPORT_FOLDER = Path("outputs/reports")

def main():

    images = sorted(
        list(DATA_FOLDER.glob("*.tif")) +
        list(DATA_FOLDER.glob("*.tiff"))
    )

    successful = []
    failed = []

    print("TERRASPECTRA FULL DATASET VALIDATION")
    print("=" * 45)
    print("Total images found:", len(images))

    for i, image_path in enumerate(images, start=1):

        try:
            # Suppress detailed output for each image
            with redirect_stdout(io.StringIO()):
                cube, valid_mask, background_mask = (
                    load_hyperspectral_image(image_path)
                )

            assert cube.shape == (204, 48, 352)
            assert valid_mask.shape == (48, 352)
            assert background_mask.shape == (48, 352)

            successful.append(image_path.name)

            del cube, valid_mask, background_mask

        except Exception as error:
            failed.append(
                (image_path.name, str(error))
            )

        if i % 100 == 0 or i == len(images):
            print(
                f"Processed {i}/{len(images)} | "
                f"Passed: {len(successful)} | "
                f"Failed: {len(failed)}"
            )

        gc.collect()

    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

    # Save the updated valid image list
    valid_list = "\n".join(successful)

    if successful:
        valid_list += "\n"

    (REPORT_FOLDER / "valid_hyperspectral_images.txt").write_text(
        valid_list
    )

    report = [
        "TERRASPECTRA - FULL DATASET VALIDATION",
        "=" * 50,
        f"Total images: {len(images)}",
        f"Successful: {len(successful)}",
        f"Failed: {len(failed)}",
        "",
        "FAILED IMAGES:"
    ]

    report.extend(
        [f"{name}: {error}" for name, error in failed]
    )

    report.append("")
    report.append(
        "OVERALL STATUS: " +
        ("PASS" if len(successful) == len(images) else "PARTIAL")
    )

    report_text = "\n".join(report)

    (REPORT_FOLDER / "full_dataset_validation.txt").write_text(
        report_text
    )

    print("\n" + report_text)


if __name__ == "__main__":
    main()
