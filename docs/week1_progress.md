# TerraSpectra - Week 1 Progress Report

## Project Overview

Week 1 focused on hyperspectral dataset validation, preprocessing,
dimensionality reduction, preliminary machine learning experiments,
and development of the interactive dashboard.

## Day 1: Hyperspectral Data Validation

### Completed Tasks
- Generated synthetic hyperspectral data with 220 spectral bands.
- Stored the data in HDF5 and GeoTIFF formats.
- Inspected dimensions and metadata.
- Developed a Python validation script using h5py, Rasterio and NumPy.
- Checked missing values, data types, reflectance ranges and spectral bands.
- Compared HDF5 and GeoTIFF pixel values for consistency.

### Validation Results
- Total checks: 14
- Passed: 14
- Failed: 0
- Overall status: SUCCESS

## Day 2: Real Dataset Inspection and Loading

### Completed Tasks
- Acquired and inspected the HyperLeaf2024 hyperspectral dataset.
- Examined TIFF image dimensions, data types and metadata.
- Developed a hyperspectral image loading pipeline using tifffile and Rasterio.
- Selected 1,000 valid TIFF images for processing.
- Created image validation and selection reports.

### Dataset Findings
- Original TIFF files inspected: 2,410
- Successfully validated images: 2,363
- Failed images: 47
- Selected images for processing: 1,000
- Hyperspectral image shape: 204 x 48 x 352
- Data type: uint16

## Day 3: Data Preprocessing and PCA

### Completed Tasks
- Implemented image-level PCA dimensionality reduction.
- Developed shared PCA preprocessing using StandardScaler and IncrementalPCA.
- Reduced spectral dimensions from 204 to 20 components.
- Processed the selected 1,000 hyperspectral images.
- Generated PCA output files and preprocessing reports.

### PCA Results
- Original spectral components: 204
- Reduced components: 20
- Explained variance: approximately 99.69%
- PCA output format: NumPy arrays

## Day 4: Feature Extraction and Machine Learning Experiments

### Completed Tasks
- Matched available training labels with hyperspectral image IDs.
- Extracted PCA-based features for machine learning.
- Created a plant trait feature dataset.
- Implemented Random Forest regression for plant trait prediction.
- Implemented a Random Forest cultivar classification experiment.
- Generated prediction results, evaluation metrics and plots.

### Experimental Results
- Matched training images: 634
- Extracted feature dataset: 634 rows and 49 columns
- Cultivar classification accuracy: 66.93%

### Important Note
The available dataset supports plant trait regression and cultivar
classification. It does not provide validated healthy/diseased or
healthy/stressed labels. Therefore, these experiments are not
disease-classification results.

## Day 5: Dashboard and GIS Map Integration

### Completed Tasks
- Developed the React and Vite dashboard.
- Created dashboard sections for overview, farm map, spectral analysis,
  disease monitoring, model performance and cultivar classification.
- Generated a spectral heatmap using the first principal component.
- Developed a pixel-grid visualization.
- Implemented mock API services for dashboard testing.
- Integrated Leaflet with Esri satellite imagery.
- Integrated Deck.gl for the farm boundary overlay.
- Tested map rendering, zooming and panning.
- Verified the dashboard production build successfully.

### Technology Stack
- Python
- NumPy, Pandas and Scikit-learn
- Rasterio and tifffile
- HDF5 and NumPy arrays
- PyTorch
- React and Vite
- Leaflet
- Esri World Imagery
- Deck.gl

## Week 1 Summary

### Major Achievements
- Completed synthetic hyperspectral data validation.
- Inspected and selected real hyperspectral images.
- Developed the image-loading and preprocessing pipeline.
- Implemented shared PCA dimensionality reduction.
- Extracted features and conducted preliminary ML experiments.
- Developed dashboard visualizations.
- Integrated and tested the Deck.gl farm boundary overlay.

### Known Limitations
- The available TIFF images do not contain geographic CRS information.
- The current farm boundary is a synthetic demonstration boundary,
  not a surveyed farm boundary.
- Leaflet, Esri imagery and Deck.gl were used instead of Mapbox.
- GPS validation of real-world image overlays is still pending.
- Validated disease or stress labels are not available in the current dataset.
- Only 1,000 selected TIFF images were retained for processing.

### Overall Status

Week 1 preprocessing, preliminary ML experiments and dashboard
development have been substantially completed.

The remaining limitations are documented and will be considered
during the next development phase.

## Next Phase: Week 2

- Develop memory-efficient hyperspectral tensor batches.
- Improve and test deep learning model architectures.
- Develop the mock backend integration.
- Improve spectral heatmap and pixel-grid visualizations.
- Investigate valid labels for supervised disease or stress classification.
- Continue GIS overlay and coordinate validation where georeferenced
  farm data becomes available.
