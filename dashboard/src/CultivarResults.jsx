
function CultivarResults() {
  const results = [
    { name: 'Heerup', precision: 0.71, recall: 0.52, f1: 0.60 },
    { name: 'Kvium', precision: 0.54, recall: 0.46, f1: 0.50 },
    { name: 'Rembrandt', precision: 0.71, recall: 0.73, f1: 0.72 },
    { name: 'Sheriff', precision: 0.69, recall: 0.94, f1: 0.79 }
  ]

  return (
    <section className="panel">
      <h2>Wheat Cultivar Classification</h2>
      <p>Random Forest – Four-class classification</p>

      <div className="heatmap-info">
        <div><strong>66.93%</strong><span>Test Accuracy</span></div>
        <div><strong>507</strong><span>Training Samples</span></div>
        <div><strong>127</strong><span>Testing Samples</span></div>
        <div><strong>0.65</strong><span>Macro F1-score</span></div>
      </div>

      <h3>Class-wise Performance</h3>

      <table>
        <thead>
          <tr>
            <th>Cultivar</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>F1-score</th>
          </tr>
        </thead>
        <tbody>
          {results.map(item => (
            <tr key={item.name}>
              <td>{item.name}</td>
              <td>{item.precision}</td>
              <td>{item.recall}</td>
              <td>{item.f1}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Confusion Matrix</h3>

      <img
        src="/images/cultivar_confusion_matrix.png"
        alt="Wheat cultivar classification confusion matrix"
        style={{ width: '100%', maxWidth: '650px' }}
      />
      <h3>Prediction Summary</h3>

<img
  src="/images/cultivar_prediction_summary.png"
  alt="Correct and incorrect wheat cultivar predictions"
  style={{ width: '100%', maxWidth: '650px' }}
/>

      <p>
        Note: This experiment predicts wheat cultivar classes,
        not crop disease or chemical stress.
      </p>
    </section>
  )
}

export default CultivarResults
