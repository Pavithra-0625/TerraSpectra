
import { useEffect, useState } from 'react'
import { getModelMetrics, getFarmInfo } from './services/mockApi'

function ApiTest() {
  const [metrics, setMetrics] = useState(null)
  const [farm, setFarm] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([getModelMetrics(), getFarmInfo()])
      .then(([modelData, farmData]) => {
        setMetrics(modelData)
        setFarm(farmData)
      })
      .catch(err => setError(err.message))
  }, [])

  if (error) return <p>{error}</p>
  if (!metrics || !farm) return <p>Loading mock API data...</p>

  return (
    <section className="panel">
      <h2>Mock Backend API Status</h2>

      <h3>Model Performance</h3>
      <p>Model: {metrics.model}</p>
      <p>Best target: {metrics.bestTarget}</p>
      <p>Best R²: {metrics.bestR2.toFixed(4)}</p>
      <p>Dataset images: {metrics.datasetImages}</p>

      <h3>Farm Information</h3>
      <p>Farm: {farm.farmName}</p>
      <p>Crop: {farm.crop}</p>
      <p>Location: {farm.location}</p>
      <p>Valid pixels: {farm.validPixels}</p>
      <p>Image size: {farm.imageWidth} × {farm.imageHeight}</p>

      <p>API Status: {metrics.status} / {farm.status}</p>
    </section>
  )
}

export default ApiTest
