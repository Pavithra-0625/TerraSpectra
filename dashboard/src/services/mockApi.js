const API_DELAY = 800

// Get hyperspectral pixel grid
export async function getPixelGrid() {
  await new Promise(resolve => setTimeout(resolve, API_DELAY))

  const response = await fetch('/data/pixel_grid.json')

  if (!response.ok) {
    throw new Error('Unable to load pixel grid data')
  }

  return response.json()
}

// Get model performance information
export async function getModelMetrics() {
  await new Promise(resolve => setTimeout(resolve, API_DELAY))

  return {
    status: 'success',
    model: 'Random Forest Regressor',
    targets: 8,
    bestTarget: 'Fertilizer',
    bestR2: 0.8053,
    datasetImages: 634
  }
}

// Get farm information
export async function getFarmInfo() {
  await new Promise(resolve => setTimeout(resolve, API_DELAY))

  return {
    status: 'success',
    farmName: 'Demonstration Farm',
    crop: 'Wheat',
    location: 'Ladhowal, Ludhiana, Punjab',
    imageWidth: 352,
    imageHeight: 48,
    validPixels: 1484
  }
}