import { getPixelGrid } from './services/mockApi'
import { useEffect, useRef, useState } from 'react'

function PixelGrid() {
  const canvasRef = useRef(null)
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
  getPixelGrid()
    .then(setData)
    .catch(err => setError(err.message))
}, [])

  useEffect(() => {
    if (!data || !canvasRef.current) return

    const canvas = canvasRef.current
    canvas.width = data.width
    canvas.height = data.height

    const ctx = canvas.getContext('2d')
    const image = ctx.createImageData(data.width, data.height)

    data.grid.forEach((row, y) => {
      row.forEach((value, x) => {
        const index = (y * data.width + x) * 4

        if (value === null) {
          image.data[index + 3] = 0
          return
        }

        let r, g, b

        if (value < 0.5) {
          const t = value * 2
          r = Math.round(44 + (255 - 44) * t)
          g = Math.round(123 + (255 - 123) * t)
          b = Math.round(182 + (191 - 182) * t)
        } else {
          const t = (value - 0.5) * 2
          r = 255
          g = Math.round(255 + (25 - 255) * t)
          b = Math.round(191 + (28 - 191) * t)
        }

        image.data[index] = r
        image.data[index + 1] = g
        image.data[index + 2] = b
        image.data[index + 3] = 255
      })
    })

    ctx.putImageData(image, 0, 0)
  }, [data])

  if (error) return <p>{error}</p>
  if (!data) return <p>Loading pixel grid...</p>

  return (
    <section className="panel">
      <h3>Hyperspectral Pixel Grid</h3>
      <p>Colored pixel visualization using PCA Component 1 (PC1)</p>

      <div className="pixel-grid-container">
        <canvas ref={canvasRef} />
      </div>

      <p>Valid pixels: {data.valid_pixels}</p>
      <p>Grid size: {data.width} × {data.height}</p>
      <p>Background pixels are transparent.</p>
    </section>
  )
}

export default PixelGrid
