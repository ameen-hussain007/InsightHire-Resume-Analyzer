import React, { useState } from 'react';
import './App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpload, faPlay, faStar } from '@fortawesome/free-solid-svg-icons';

function App() {
  const [fileName, setFileName] = useState("No file selected");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('https://smart-resume-analyzer-full.onrender.com/analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResult({
        bestMatch: {
          title: data.best_match.role,
          percentage: data.best_match.percentage
        },
        scores: data.match_percentages
      });
    } catch (error) {
      console.error("Error analyzing resume:", error);
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <header className="header">
        <h1><FontAwesomeIcon icon={faStar} className="logo-icon" /> Smart Resume Analyzer</h1>
      </header>

      <div className="upload-card">
        <label className="file-label">
          <input type="file" onChange={handleFileChange} />
          <FontAwesomeIcon icon={faUpload} />
          <span>Choose File:</span>
          <em>{fileName}</em>
        </label>
      </div>

      <button className="analyze-button" onClick={handleAnalyze} disabled={loading}>
        <FontAwesomeIcon icon={faPlay} />
        {loading ? 'Analyzing...' : 'Analyze Resume'}
      </button>

      {loading && <div className="loader"></div>}

      {result && !loading && (
        <>
          <div className="best-match-section">
            <div className="best-icon"><FontAwesomeIcon icon={faStar} /></div>
            <div className="best-content">
              <p className="best-label">Top Match</p>
              <h2 className="best-role">{result.bestMatch.title}</h2>
              <p className="best-score">{result.bestMatch.percentage}% match</p>
            </div>
          </div>

          <div className="card match-card">
            <h3>Match Percentages:</h3>
            <ul>
              {Object.entries(result.scores).map(([role, value]) => (
                <li key={role}>
                  <span className="role-title">{role}</span>
                  <div className="bar-wrapper">
                    <div
                      className="bar-fill"
                      style={{ width: `${value}%`, backgroundColor: getBarColor(value) }}
                    ></div>
                  </div>
                  <span className="percent">{value}%</span>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}

function getBarColor(val) {
  if (val === 0) return '#ccc';
  if (val >= 80) return '#38b000';
  if (val >= 60) return '#00b4d8';
  if (val >= 30) return '#fcbf49';
  return '#ef476f';
}

export default App;














