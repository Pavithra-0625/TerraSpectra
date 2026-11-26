# TerraSpectra - Mid-Project Progress Report

## Project Overview

TerraSpectra is a hyperspectral crop monitoring project focused on
spectral data preprocessing, machine learning, deep learning,
visualization and geospatial analysis.

Project duration: 4 weeks
Progress at mid-review: 2 weeks completed

## 1. Week 1: Data Validation and Preprocessing

### Completed Tasks
- Generated and validated synthetic hyperspectral data.
- Inspected the HyperLeaf2024 dataset.
- Selected 1,000 valid TIFF images for processing.
- Developed hyperspectral image loading pipelines.
- Implemented shared PCA preprocessing.
- Reduced spectral dimensions from 204 to 20 components.
- Extracted features for machine learning experiments.
- Developed the initial interactive dashboard.

### Results
- Synthetic validation: 14/14 checks passed.
- Successfully validated HyperLeaf images: 2,363.
- Selected images: 1,000.
- PCA explained variance: approximately 99.69%.
- Cultivar classification accuracy: 66.93%.

## 2. Week 2: Deep Learning and Model Experiments

### Completed Tasks
- Developed and tested 3D-CNN architecture.
- Developed and tested Vision Transformer architecture.
- Implemented a hybrid deep learning architecture.
- Tested model forward passes.
- Developed a wheat disease classification experiment using RGB images.
- Generated Grad-CAM visualizations.
- Conducted memory profiling of DataLoader batches.
- Developed a synthetic hyperspectral stress classification experiment.

### Model Architecture Experiments

| Model | Parameters |
|---|---:|
| 3D-CNN | 3,730 |
| Vision Transformer | 149,058 |
| Hybrid model | 8,178 |

All three architectures completed the initial forward-pass tests.

### Wheat Disease Classification Experiment

- Dataset: 999 RGB images.
- Classes: 5.
- Training images: 699.
- Validation images: 150.
- Testing images: 150.
- Test accuracy: 58.00%.
- Macro F1-score: 0.49.
- Grad-CAM visualizations generated for sample test images.

This is a separate RGB image experiment and should not be interpreted
as hyperspectral stress classification.

## 3. Synthetic Hyperspectral Stress Classification

### Dataset
- Source: Synthetic HDF5 demonstration dataset.
- Image dimensions: 64 x 64 pixels.
- Spectral bands: 220.
- Input patch size: 5 x 5.
- Model: 3D Convolutional Neural Network.

### Evaluation Method
A spatially separated training and testing split was used.

- Training samples: 2,432.
- Testing samples: 1,024.
- Training stress pixels: 625.
- Testing stress pixels: 26.
- Training epochs: 15.

### Results

| Metric | Result |
|---|---:|
| Accuracy | 99.90% |
| Precision | 100% |
| Recall | 96.15% |
| F1-score | 98.04% |

Confusion matrix:

[[998, 0],
 [1, 25]]

Model saved at:
outputs/synthetic_stress_3dcnn.pth

Important: These results apply only to the synthetic demonstration
dataset. They do not establish real-world chemical-stress detection
performance. The test region contains only 26 stress-class pixels.

## 4. Dashboard Development

### Completed Components
- Overview dashboard.
- Farm Map.
- Spectral Analysis.
- Disease Monitoring.
- Model Performance.
- Spectral Heatmap.
- Pixel Grid.
- Mock API Test.
- Cultivar Classification.
- Wheat Disease Explainability.

### Technologies
- React and Vite.
- Leaflet.
- Deck.gl.
- Esri World Imagery.
- Python and PyTorch.

The dashboard production build was successfully tested.

## 5. Geospatial Integration: Investigation and Limitation

### Investigation Performed
- Inspected HyperLeaf2024 CSV columns.
- Checked original TIFF metadata.
- Checked synthetic GeoTIFF metadata.
- Inspected CRS, bounds and affine transforms.

### Findings
- Original TIFF images do not contain a geographic CRS or geotransform.
- Synthetic GeoTIFF uses a local pixel grid without geographic CRS.
- HyperLeaf CSV files do not provide GPS coordinates.
- The current farm boundary and demonstration markers are synthetic.

### Current Status
The PC1 pixel-grid visualization is available as a separate
analytical component. Accurate overlay on the farm map is pending
georeferenced imagery or GPS control points.

No arbitrary GPS coordinates have been assigned.

## 6. Challenges Faced

- Large hyperspectral dataset processing.
- TIFF validation and damaged image files.
- Memory optimization during data loading.
- Deep learning model input dimension corrections.
- Limited availability of validated stress labels.
- Missing geographic reference information.

## 7. Mid-Project Summary

### Completed
- Hyperspectral dataset validation.
- Image loading and preprocessing.
- PCA dimensionality reduction.
- Preliminary machine learning experiments.
- Deep learning architecture development and testing.
- RGB wheat disease classification experiment.
- Synthetic hyperspectral stress classification demonstration.
- Dashboard development and visualization.
- Geospatial metadata investigation.

### Pending / Future Work
- Real-world validation of hyperspectral stress classification.
- Georeferencing and accurate pixel-grid map integration.
- Further model evaluation and improvement.
- Continued dashboard and backend integration.
- Remaining Week 3 and Week 4 development activities.

## Conclusion

During the first two weeks, TerraSpectra established its
hyperspectral preprocessing pipeline, preliminary machine learning
experiments, deep learning prototypes and interactive dashboard.

The synthetic stress classifier demonstrated the proposed
classification workflow. Geospatial integration remains dependent
on obtaining suitable geographic reference data.

The next phase will focus on improving model validation,
integration and overall system functionality.
