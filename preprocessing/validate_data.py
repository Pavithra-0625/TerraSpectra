import os
import h5py
import rasterio
import numpy as np

H5_PATH = "data/mock/crop_hyperspectral.h5"
TIF_PATH = "data/mock/crop_hyperspectral.tif"
REPORT_PATH = "outputs/validation_report.txt"

results = []

def record(name, passed, details):
    status = "PASS" if passed else "FAIL"
    results.append(f"{status}: {name} - {details}")
    print(results[-1])

def validate():
    print("TERRASPECTRA DATA VALIDATION")
    print("=" * 55)

    if not os.path.exists(H5_PATH):
        record("HDF5 file exists", False, H5_PATH)
        return

    if not os.path.exists(TIF_PATH):
        record("GeoTIFF file exists", False, TIF_PATH)
        return

    with h5py.File(H5_PATH, "r") as h5:
        cube = h5["hyperspectral_cube"][:]
        mask = h5["stress_mask"][:]
        wavelengths = h5["wavelengths_nm"][:]

    with rasterio.open(TIF_PATH) as tif:
        raster = tif.read()

        record(
            "GeoTIFF dimensions",
            (tif.height, tif.width) == cube.shape[:2],
            f"{tif.height} x {tif.width}"
        )

        record(
            "GeoTIFF band count",
            tif.count == cube.shape[2],
            f"{tif.count} bands"
        )

        record(
            "GeoTIFF data type",
            all(dtype == "float32" for dtype in tif.dtypes),
            str(tif.dtypes[0])
        )

        record(
    "Coordinate reference system",
    tif.crs is None,
    "Expected: synthetic local grid without geographic CRS"
)

    record(
        "HDF5 cube dimensions",
        cube.ndim == 3 and cube.shape == (64, 64, 220),
        str(cube.shape)
    )

    record(
        "Spectral band count",
        cube.shape[2] == 220,
        f"{cube.shape[2]} bands"
    )

    record(
        "Cube data type",
        cube.dtype == np.float32,
        str(cube.dtype)
    )

    record(
        "No missing values in cube",
        np.isfinite(cube).all(),
        f"Finite values: {np.isfinite(cube).sum()}"
    )

    record(
        "Reflectance values in expected range",
        cube.min() >= 0 and cube.max() <= 1,
        f"Minimum: {cube.min():.5f}, Maximum: {cube.max():.5f}"
    )

    record(
        "Stress mask dimensions",
        mask.shape == cube.shape[:2],
        str(mask.shape)
    )

    record(
        "Stress mask values",
        set(np.unique(mask)).issubset({0, 1}),
        f"Classes: {np.unique(mask).tolist()}"
    )

    record(
        "Wavelength count",
        len(wavelengths) == cube.shape[2],
        f"{len(wavelengths)} wavelengths"
    )

    record(
        "Wavelength values",
        np.isfinite(wavelengths).all()
        and np.all(np.diff(wavelengths) > 0),
        f"Range: {wavelengths.min():.2f} - "
        f"{wavelengths.max():.2f} nm"
    )

    matching = (
        raster.shape == (cube.shape[2], cube.shape[0], cube.shape[1])
        and np.allclose(raster, np.transpose(cube, (2, 0, 1)),
                        rtol=1e-5, atol=1e-6)
    )

    record(
        "HDF5 and GeoTIFF data consistency",
        matching,
        "Pixel values match" if matching
        else "Data or dimensions do not match"
    )

    passed = sum(item.startswith("PASS") for item in results)
    failed = sum(item.startswith("FAIL") for item in results)

    results.append("=" * 55)
    results.append(f"Total checks: {passed + failed}")
    results.append(f"Passed: {passed}")
    results.append(f"Failed: {failed}")
    results.append("Overall status: " +
                   ("SUCCESS" if failed == 0 else "CHECK REQUIRED"))

    os.makedirs("outputs", exist_ok=True)

    with open(REPORT_PATH, "w") as report:
        report.write("\n".join(results))

    print("\n" + "\n".join(results[-5:]))
    print(f"\nReport saved to: {REPORT_PATH}")

if __name__ == "__main__":
    validate()