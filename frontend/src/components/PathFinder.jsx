import React, { useState } from 'react';
import './PathFinder.css';

const API_BASE_URL = 'http://localhost:5000/api';

function PathFinder({ people, onNotification }) {
  const [startId, setStartId] = useState('');
  const [endId, setEndId] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [algorithm, setAlgorithm] = useState('compare');

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!startId || !endId) {
      onNotification('لطفاً هر دو فرد را انتخاب کنید', 'error');
      return;
    }

    if (startId === endId) {
      onNotification('هر دو فرد یکسان هستند', 'error');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      let endpoint = '';
      if (algorithm === 'bfs') {
        endpoint = 'path/bfs';
      } else if (algorithm === 'dfs') {
        endpoint = 'path/dfs';
      } else {
        endpoint = 'path/compare';
      }

      const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start_id: startId, end_id: endId }),
      });

      const data = await response.json();
      
      if (data.success) {
        setResult(data.data);
        onNotification('مسیر با موفقیت پیدا شد', 'success');
      } else {
        onNotification(data.error, 'error');
      }
    } catch (error) {
      onNotification('خطا در جستجو: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const renderPath = (pathData, algorithmName) => {
    if (!pathData) return null;

    return (
      <div className="path-result">
        <h4>{algorithmName}</h4>
        <div className="algorithm-badge">{pathData.algorithm}</div>
        
        <div className="simplified-relationship">
          <strong>نسبت خانوادگی:</strong>
          <span className="relationship-badge">{pathData.simplified_relationship}</span>
        </div>

        <div className="path-info">
          <span>طول مسیر: {pathData.path_length} گام</span>
        </div>

        <div className="path-visualization">
          {pathData.path.map((step, index) => (
            <React.Fragment key={index}>
              <div className="path-node">
                <div className="node-name">{step.name}</div>
                <div className="node-id">{step.id}</div>
                {step.relation !== 'شروع' && (
                  <div className="node-relation">{step.relation}</div>
                )}
              </div>
              {index < pathData.path.length - 1 && (
                <div className="path-arrow">⬅️</div>
              )}
            </React.Fragment>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="path-finder card">
      <h2>🔍 یافتن نسبت خانوادگی</h2>

      <form onSubmit={handleSearch} className="search-form">
        <div className="form-group">
          <label>از (فرد اول):</label>
          <select
            value={startId}
            onChange={(e) => setStartId(e.target.value)}
            required
          >
            <option value="">انتخاب کنید</option>
            {people.map((person) => (
              <option key={person.id} value={person.id}>
                {person.name} ({person.id})
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>تا (فرد دوم):</label>
          <select
            value={endId}
            onChange={(e) => setEndId(e.target.value)}
            required
          >
            <option value="">انتخاب کنید</option>
            {people.map((person) => (
              <option key={person.id} value={person.id}>
                {person.name} ({person.id})
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>الگوریتم جستجو:</label>
          <select
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value)}
          >
            <option value="compare">مقایسه BFS و DFS</option>
            <option value="bfs">فقط BFS (سطح به سطح)</option>
            <option value="dfs">فقط DFS (عمقی)</option>
          </select>
        </div>

        <button 
          type="submit" 
          className="btn btn-primary" 
          disabled={loading || people.length < 2}
        >
          {loading ? '🔄 در حال جستجو...' : '🔍 جستجوی نسبت'}
        </button>
      </form>

      {result && (
        <div className="results-container">
          {algorithm === 'compare' ? (
            <>
              <div className="comparison-header">
                <h3>📊 مقایسه الگوریتم‌ها</h3>
                {result.same_path ? (
                  <div className="same-path-badge">
                    ✅ هر دو الگوریتم یک نسبت یکسان پیدا کردند
                  </div>
                ) : (
                  <div className="different-path-badge">
                    ⚠️ الگوریتم‌ها مسیرهای متفاوتی پیدا کردند
                  </div>
                )}
              </div>
              
              <div className="comparison-grid">
                {renderPath(result.bfs, 'BFS')}
                {renderPath(result.dfs, 'DFS')}
              </div>
            </>
          ) : (
            renderPath(result, algorithm === 'bfs' ? 'BFS' : 'DFS')
          )}
        </div>
      )}
    </div>
  );
}

export default PathFinder;
