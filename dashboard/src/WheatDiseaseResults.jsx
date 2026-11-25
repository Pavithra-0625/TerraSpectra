
import './App.css'

function WheatDiseaseResults() {
  const images = [1, 2, 3, 4, 5]

  return (
    <div className="wheat-results">
      <section className="panel">
        <h2>Wheat Disease Explainability</h2>
        <p>
          CNN V2 predictions with Grad-CAM visual explanations
        </p>

        <div className="wheat-metrics">
          <div className="metric-card">
            <p>Test Accuracy</p>
            <h2>58%</h2>
          </div>

          <div className="metric-card">
            <p>Number of Classes</p>
            <h2>5</h2>
          </div>

          <div className="metric-card">
            <p>Test Images</p>
            <h2>150</h2>
          </div>
        </div>
      </section>

      <section className="panel">
        <h3>Grad-CAM Visualizations</h3>
        <p>
          Highlighted regions show image areas influencing
          the model's predicted class.
        </p>

        <div className="wheat-image-grid">
          {images.map((number) => (
            <div className="wheat-image-card" key={number}>
              <img
                src={`/images/wheat_disease/image_${number}.png`}
                alt={`Wheat disease Grad-CAM visualization ${number}`}
              />
              <p>Test Image {number}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <h3>Model Performance</h3>
        <p>Classification results on the held-out test set.</p>

        <table>
          <thead>
            <tr>
              <th>Class</th>
              <th>Precision</th>
              <th>Recall</th>
              <th>F1-score</th>
            </tr>
          </thead>

          <tbody>
            <tr><td>BrownRust</td><td>0.56</td><td>0.47</td><td>0.51</td></tr>
            <tr><td>Healthy</td><td>0.56</td><td>0.74</td><td>0.64</td></tr>
            <tr><td>Mildew</td><td>0.00</td><td>0.00</td><td>0.00</td></tr>
            <tr><td>Septoria</td><td>0.73</td><td>0.69</td><td>0.71</td></tr>
            <tr><td>YellowRust</td><td>0.47</td><td>0.78</td><td>0.58</td></tr>
          </tbody>
        </table>
      </section>

      <p>
        Note: Grad-CAM is an explanatory visualization, not
        a verified map of disease-affected tissue.
      </p>
    </div>
  )
}

export default WheatDiseaseResults
