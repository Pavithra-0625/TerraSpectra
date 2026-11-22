
import { useEffect, useState, useMemo, useCallback } from 'react'
import { DeckGL } from '@deck.gl/react'
import { GeoJsonLayer } from '@deck.gl/layers'
import { useMap } from 'react-leaflet'

function DeckOverlay({ data }) {
  const map = useMap()

  const getViewState = useCallback(() => {
    const center = map.getCenter()
    const size = map.getSize()

    return {
      longitude: center.lng,
      latitude: center.lat,
      zoom: map.getZoom() - 1,
      pitch: 0,
      bearing: 0,
      width: size.x,
      height: size.y
    }
  }, [map])

  const [viewState, setViewState] = useState(getViewState)

  useEffect(() => {
    const updateView = () => {
      setViewState(getViewState())
    }

    map.on('moveend zoomend resize', updateView)
    updateView()

    return () => {
      map.off('moveend zoomend resize', updateView)
    }
  }, [map, getViewState])

  const layers = useMemo(() => [
    new GeoJsonLayer({
      id: 'farm-boundary-overlay',
      data,
      filled: true,
      stroked: true,
      getFillColor: [37, 182, 138, 65],
      getLineColor: [20, 120, 85, 255],
      getLineWidth: 3,
      lineWidthMinPixels: 2,
      pickable: true
    })
  ], [data])

  return (
    <DeckGL
      viewState={viewState}
      controller={false}
      layers={layers}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: 450
      }}
    />
  )
}

export default DeckOverlay
