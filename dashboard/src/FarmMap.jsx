import { MapContainer, TileLayer, GeoJSON, CircleMarker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

import farmGeoJson from './data/farm_boundaries.geojson?raw'

const farmData = JSON.parse(farmGeoJson)

function FarmMap() {
  const center = [30.9941, 75.7340]

  const farmStyle = {
    color: '#147855',
    weight: 3,
    fillColor: '#25b68a',
    fillOpacity: 0.35
  }

  return (
    <div
      style={{
        width: '100%',
        height: '500px',
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
  attribution='Tiles &copy; Esri — Sources: Esri, Maxar, Earthstar Geographics'
  url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
/>
<CircleMarker
  center={center}
  radius={8}
  pathOptions={{
    color: '#ffffff',
    fillColor: '#e63946',
    fillOpacity: 1
  }}
>
  <Popup>
    <b>Ladhowal Farm</b><br />
    Ludhiana, Punjab, India<br />
    Latitude: 30.9941<br />
    Longitude: 75.7340
  </Popup>
</CircleMarker>

        <GeoJSON
          data={farmData}
          style={farmStyle}
          onEachFeature={(feature, layer) => {
            const properties = feature.properties

            layer.bindPopup(
              `<b>${properties.farm_name}</b><br/>` +
              `Crop: ${properties.crop}<br/>` +
              `Status: ${properties.status}<br/>` +
              `Source: ${properties.data_source}`
            )
          }}
        />
      </MapContainer>
    </div>
  )
}

export default FarmMap
