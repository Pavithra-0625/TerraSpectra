
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup
} from 'react-leaflet'

import 'leaflet/dist/leaflet.css'
import farmGeoJson from './data/farm_boundaries.geojson?raw'
import diseaseGeoJson from './data/disease_predictions.geojson?raw'
import DeckOverlay from './components/DeckOverlay'

const farmData = JSON.parse(farmGeoJson)
const diseaseData = JSON.parse(diseaseGeoJson)

const diseaseColors = {
  BrownRust: '#e63946',
  Healthy: '#2a9d8f',
  Septoria: '#f4a261',
  YellowRust: '#e9c46a',
  Mildew: '#8e44ad'
}

function FarmMap() {
  const center = [30.9941, 75.7340]

  return (
    <div style={{ width: '100%' }}>

      {/* Farm Map */}
      <div
        style={{
          width: '100%',
          height: '460px',
          borderRadius: '12px',
          overflow: 'hidden'
        }}
      >
        <MapContainer
          center={center}
          zoom={15}
          style={{ width: '100%', height: '100%' }}
        >
          <TileLayer
            attribution="Tiles &copy; Esri — Sources: Esri, Maxar, Earthstar Geographics"
            url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
          />

          {/* Farm Boundary */}
          <DeckOverlay data={farmData} />

          {/* Disease Prediction Markers */}
          {diseaseData.features.map((feature) => {
            const [longitude, latitude] = feature.geometry.coordinates
            const properties = feature.properties

            return (
              <CircleMarker
                key={properties.prediction_id}
                center={[latitude, longitude]}
                radius={9}
                pathOptions={{
                  color: '#ffffff',
                  weight: 2,
                  fillColor: diseaseColors[properties.disease] || '#808080',
                  fillOpacity: 0.9
                }}
              >
                <Popup>
                  <b>{properties.prediction_id}</b>
                  <br />
                  Class: {properties.disease}
                  <br />
                  Confidence: {(properties.confidence * 100).toFixed(0)}%
                  <br />
                  Source: {properties.source}
                </Popup>
              </CircleMarker>
            )
          })}
        </MapContainer>
      </div>

      {/* Disease Legend */}
      <div style={{ marginTop: '12px' }}>
        <h4>Disease Prediction Legend</h4>

        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '15px',
            fontSize: '13px'
          }}
        >
          {Object.entries(diseaseColors).map(([disease, color]) => (
            <div
              key={disease}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <span
                style={{
                  width: '13px',
                  height: '13px',
                  borderRadius: '50%',
                  backgroundColor: color,
                  display: 'inline-block'
                }}
              />
              {disease}
            </div>
          ))}
        </div>

        <p style={{ fontSize: '12px', color: '#b45309', marginTop: '10px' }}>
          Note: Markers are synthetic demonstration points, not real
          GPS-based detections or verified model predictions.
        </p>
      </div>

    </div>
  )
}

export default FarmMap
