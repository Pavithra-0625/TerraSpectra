function Heatmap() {
  return (
    <section className="panel heatmap-panel">
      <div className="panel-heading">
        <div>
          <h3>Hyperspectral Spatial Heatmap</h3>
          <p>Crop spectral intensity visualization using PCA</p>
        </div>
        <span className="tag">PC1</span>
      </div>

      <div className="heatmap-image">
        <img
          src="/images/spectral_heatmap.png"
          alt="Hyperspectral crop spectral intensity heatmap"
        />
      </div>

      <div className="heatmap-info">
        <div>
          <strong>20</strong>
          <span>PCA Components</span>
        </div>

        <div>
          <strong>1,484</strong>
          <span>Valid Pixels</span>
        </div>

        <div>
          <strong>48 × 352</strong>
          <span>Image Dimensions</span>
        </div>

        <div>
          <strong>8.78%</strong>
          <span>Valid Pixel Area</span>
        </div>
      </div>

      <p className="heatmap-note">
        Note: This visualization represents spectral intensity,
        not disease classification.
      </p>
    </section>
  )
}

export default Heatmap