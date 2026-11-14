# HyperLeaf2024 Dataset Analysis

## 1. Dataset Overview

HyperLeaf2024 is being investigated as a supplementary
crop-image dataset for the TerraSpectra project.

## 2. Dataset Files

- train.csv: 1,590 records
- test.csv: 820 records
- solution.csv: 820 records
- sample_submission.csv: 820 records
- Original image collection: 2,410 TIFF files

## 3. CSV Structure

Training columns:
- ImageId
- GrainWeight
- Gsw
- PhiPS2
- Fertilizer
- Heerup
- Kvium
- Rembrandt
- Sheriff

These fields describe plant and field-related properties.
They are not confirmed disease labels.

## 4. TIFF Sample Inspection

Four TIFF images were inspected.

| Property | Observed value |
|---|---|
| Width | 352 pixels |
| Height | 48 pixels |
| Bands | 1 |
| Data type | uint16 |
| CRS | None |
| Individual size | Approximately 6.7 MB |

## 5. Pixel Statistics

| Image | Minimum | Maximum | Mean |
|---|---:|---:|---:|
| 02389.tiff | 0 | 23135 | 2754.22 |
| 02390.tiff | 0 | 20452 | 1609.86 |
| 02391.tiff | 0 | 19108 | 1791.51 |
| 02392.tiff | 0 | 22970 | 2381.29 |

## 6. Preliminary Findings

- All four inspected TIFF images contain one band.
- The images contain varying pixel values.
- The sample does not demonstrate a 200+ band hyperspectral cube.
- Geographic referencing is absent.
- More dataset documentation is needed to establish the
  physical meaning of the TIFF pixel values.

## 7. TerraSpectra Suitability

HyperLeaf2024 is retained as a supplementary dataset candidate.
It is not yet approved as the primary hyperspectral disease
classification dataset.

The INRAE wheat disease dataset remains the primary candidate
for investigating disease-labelled hyperspectral measurements.

## 8. Pending Work

- Verify the official HyperLeaf2024 image format documentation.
- Investigate the spectral characteristics of the TIFF images.
- Acquire and inspect the INRAE hyperspectral data.
- Identify suitable disease labels and wavelength information.

## 9. Inspection Methodology

The initial dataset inspection was performed using Python,
Pandas, Rasterio and NumPy.

### CSV Inspection
- Loaded train.csv using Pandas.
- Checked the number of training records.
- Identified all available columns.
- Inspected the first ten ImageId values.
- Confirmed that the training file contains 1,590 records.

### TIFF Inspection
- Opened four sample TIFF files using Rasterio.
- Checked image width and height.
- Retrieved the number of raster bands.
- Examined the pixel data type.
- Calculated minimum and maximum pixel values.
- Calculated mean and standard deviation.
- Counted unique pixel values.

### Data Handling Considerations
- Raw dataset files are retained separately from source code.
- Raw data directories are excluded through .gitignore.
- Sample inspection results are documented for reproducibility.
- Additional images must be inspected before generalizing
  the findings to the complete image collection.

### Current Limitation
The physical interpretation of the TIFF pixel values and
their relationship to spectral measurements require further
verification from the official dataset documentation.
