
import { useState } from 'react'
import FarmMap from './FarmMap'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('Overview')

  const metrics = [
    { title: 'Hyperspectral Images', value: '99', detail: 'Images inspected' },
    { title: 'Spectral Bands', value: '204', detail: 'Bands per image' },
    { title: 'PCA Components', value: '20', detail: 'Reduced dimensions' },
    { title: 'Valid Pixels', value: '18.16%', detail: 'Sample image 02392' },
  ]

  const tabs = [
  'Overview',
  'Farm Map',
  'Spectral Analysis',
  'Disease Monitoring',
  'Model Performance'
]

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">T</div>
          <div>
            <h2>TerraSpectra</h2>
            <span>HYPERSPECTRAL AI</span>
          </div>
        </div>

        <p className="menu-heading">WORKSPACE</p>

        <nav>
          {tabs.map((tab) => (
            <button
              key={tab}
              className={activeTab === tab ? 'nav-item active' : 'nav-item'}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <span>PROJECT STATUS</span>
          <p>Development in progress</p>
          <div className="status-dot">● Online</div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="breadcrumb">TerraSpectra / Dashboard</p>
            <h1>{activeTab}</h1>
          </div>
          <div className="profile">
            <span>Research Workspace</span>
            <div className="avatar">TS</div>
          </div>
        </header>

        {activeTab === 'Farm Map' && (
          <section className="panel farm-map-panel">
            <div className="panel-heading">
              <div>
                <h3>Farm Geographical Map</h3>
                <p>Interactive satellite map powered by Mapbox</p>
              </div>
              <span className="tag">MAPBOX</span>
            </div>
            <div style={{ marginTop: '20px' }}>
              <FarmMap />
            </div>
          </section>
        )}
 {activeTab === 'Model Performance' && (
  <section className="model-performance">
    <div className="panel">
      <h3>Plant Trait Prediction Results</h3>
      <p>Regression model evaluation using 634 matched images</p>
      <p>Best model: Random Forest</p>
    </div>

    <div className="panel">
      <h3>R² Score Comparison</h3>
      <img src="/images/r2_comparison.png" alt="R2 comparison" />
    </div>

    <div className="panel">
      <h3>MAE Comparison</h3>
      <img src="/images/mae_comparison.png" alt="MAE comparison" />
    </div>

    <div className="panel">
      <h3>RMSE Comparison</h3>
      <img src="/images/rmse_comparison.png" alt="RMSE comparison" />
    </div>
  </section>
)}
        <section className="welcome">
          <div>
            <p className="eyebrow">HYPERSPECTRAL CROP INTELLIGENCE</p>
            <h2>Monitor crop health with spectral insights.</h2>
            <p>
              Explore hyperspectral data, analyze spectral patterns,
              and monitor crop stress indicators.
            </p>
          </div>
          <div className="welcome-symbol">🌱</div>
        </section>

        <section className="metrics-grid">
          {metrics.map((metric) => (
            <div className="metric-card" key={metric.title}>
              <p>{metric.title}</p>
              <h2>{metric.value}</h2>
              <span>{metric.detail}</span>
            </div>
          ))}
        </section>

        <section className="content-grid">
          <div className="panel analysis-panel">
            <div className="panel-heading">
              <div>
                <h3>Hyperspectral Analysis</h3>
                <p>Current dataset processing summary</p>
              </div>
              <span className="tag">PCA</span>
            </div>

            {/* Actual PCA visualization */}
            <div className="analysis-placeholder pca-display">
              <img
                src="/images/pca_components.png"
                alt="Hyperspectral PCA Components"
              />
              <p>Principal Component Analysis</p>
              <span>20 components · Image 02392</span>
            </div>
          </div>

          <div className="panel status-panel">
            <h3>Pipeline Status</h3>
            <p className="panel-subtitle">Current project progress</p>

            <div className="pipeline-item">
              <span>Dataset inspection</span>
              <strong className="completed">Completed</strong>
            </div>

            <div className="pipeline-item">
              <span>Hyperspectral loader</span>
              <strong className="completed">Completed</strong>
            </div>

            <div className="pipeline-item">
              <span>PCA preprocessing</span>
              <strong className="completed">Completed</strong>
            </div>

            <div className="pipeline-item">
              <span>GIS integration</span>
              <strong className="pending">In progress</strong>
            </div>

            <div className="pipeline-item">
              <span>Crop disease model</span>
              <strong className="pending">Pending</strong>
            </div>
          </div>
        </section>

        <footer className="dashboard-footer">
          TerraSpectra · Hyperspectral Crop Monitoring · Development Version
        </footer>
      </main>
    </div>
  )
}

export default App
