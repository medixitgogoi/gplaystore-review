import { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    setError(null);
    setData(null);

    try {
      // 🚀 FETCH DATA FROM YOUR API
      const response = await fetch(`http://127.0.0.1:8000/search?q=${encodeURIComponent(query)}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch analysis');
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      {/* HEADER & SEARCH */}
      <header className="app-header">
        <h1>🔍 App Review Analyzer</h1>
        <form onSubmit={handleSearch} className="search-bar">
          <input
            type="text"
            placeholder="Enter app category (e.g., 'fitness', 'yoga')"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </form>
      </header>

      {/* ERROR STATE */}
      {error && <div className="error-message">❌ {error}</div>}

      {/* LOADING STATE */}
      {loading && <div className="loading-spinner">🧠 AI is analyzing thousands of reviews...</div>}

      {/* RESULTS DASHBOARD */}
      {data && (
        <div className="dashboard">
          
          {/* 1. EXECUTIVE SUMMARY */}
          <section className="card summary-card">
            <h2>📊 Executive Summary</h2>
            <p className="summary-text">{data.summary}</p>
          </section>

          {/* 2. ACTION PLAN */}
          <section className="card action-card">
            <h2>🚀 Recommended Actions</h2>
            <ul className="action-list">
              {data.actions.map((action, index) => (
                <li key={index}>
                  <span className="check-icon">✅</span> {action}
                </li>
              ))}
            </ul>
          </section>

          {/* 3. PAIN POINTS GRID */}
          <section className="pain-points-section">
            <h2>⚠️ Top Pain Points</h2>
            <div className="grid">
              {data.pain_points.map((point, index) => (
                <div key={index} className={`card point-card ${point.frequency.toLowerCase()}`}>
                  <div className="card-header">
                    <span className="issue-title">{point.issue}</span>
                    <span className={`badge ${point.frequency.toLowerCase()}`}>
                      {point.frequency} Priority
                    </span>
                  </div>
                  <div className="quote-box">
                    <p>"{point.example_quote}"</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* 4. DEEP DIVE DETAILS */}
          <section className="card details-card">
            <h2>📝 Detailed Analysis</h2>
            <p>{data.details}</p>
          </section>

        </div>
      )}
    </div>
  );
}

export default App;