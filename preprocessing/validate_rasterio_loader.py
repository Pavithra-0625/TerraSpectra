from pathlib import Path
from hyperspectral_loader import load_hyperspectral_image

DATA_FOLDER = Path("data/raw/HyperLeaf2024")
VALID_LIST = Path("outputs/reports/valid_hyperspectral_images.txt")
REPORT_FOLDER = Path("outputs/reports")


def main():
    images = VALID_LIST.read_text().splitlines()[:10]
    successful = []
    failed = []

    for name in images:
        try:
            cube, valid_mask, background_mask = load_hyperspectral_image(
                DATA_FOLDER / name
            )
            assert cube.shape == (204, 48, 352)
            assert valid_mask.shape == (48, 352)
            assert background_mask.shape == (48, 352)
            successful.append(name)
        except Exception as error:
            failed.append((name, str(error)))

    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

    report = [
        "TERRASPECTRA - RASTERIO HYBRID LOADER VALIDATION",
        "=" * 55,
        f"Images tested: {len(images)}",
        f"Successful: {len(successful)}",
        f"Failed: {len(failed)}",
        "",
        "Successful images:",
        *successful,
        "",
        "Failed images:",
        *[f"{name}: {error}" for name, error in failed],
        "",
        "OVERALL STATUS: " + (
            "PASS" if len(successful) == len(images) else "FAIL"
        ),
    ]

    report_text = "\n".join(report)
    print(report_text)

    (REPORT_FOLDER / "rasterio_hybrid_validation.txt").write_text(report_text)


if __name__ == "__main__":
    main()
