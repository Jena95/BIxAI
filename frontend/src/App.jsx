// App.jsx
import { useState, useEffect } from 'react';
import './App.css';
import LoginForm from './LoginForm';

function App() {
  const [question, setQuestion] = useState('');
  const [dataset, setDataset] = useState('banking_dataset');
  const [table, setTable] = useState('banking_clean');
  const [sql, setSql] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  // Save token on login
  const handleLogin = (newToken) => {
    setToken(newToken);
    localStorage.setItem('token', newToken);
  };

  // Logout
  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    setSql('');
    setResults([]);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // 👈 Add token to headers
        },
        body: JSON.stringify({ question, dataset, table }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Unknown error');
      }

      setSql(data.sql);
      setResults(data.results);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>🧠 BIxAI - Natural Language Analytics</h1>

      {!token ? (
        <LoginForm onLogin={handleLogin} />
      ) : (
        <>
          <p>
            ✅ Logged in.
            <button onClick={handleLogout} style={{ marginLeft: '1rem' }}>
              Logout
            </button>
          </p>

          <input
            type="text"
            placeholder="Ask a question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <input
            type="text"
            placeholder="Dataset (optional)"
            value={dataset}
            onChange={(e) => setDataset(e.target.value)}
          />

          <input
            type="text"
            placeholder="Table (optional)"
            value={table}
            onChange={(e) => setTable(e.target.value)}
          />

          <button onClick={handleSubmit} disabled={loading}>
            {loading ? 'Asking Gemini...' : 'Submit'}
          </button>

          {error && <p style={{ color: 'red' }}>{error}</p>}

          {sql && (
            <div>
              <h3>📝 Generated SQL:</h3>
              <pre>{sql}</pre>
            </div>
          )}

          {results.length > 0 && (
            <div>
              <h3>📊 Query Results:</h3>
              <table border="1">
                <thead>
                  <tr>
                    {Object.keys(results[0]).map((col) => (
                      <th key={col}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {results.map((row, idx) => (
                    <tr key={idx}>
                      {Object.values(row).map((val, i) => (
                        <td key={i}>{val}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;
