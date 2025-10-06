import { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [dataset, setDataset] = useState('banking_dataset');
  const [table, setTable] = useState('banking_clean');
  const [sql, setSql] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    setSql('');
    setResults([]);

    try {
      const response = await fetch('https://8000-cs-d9f0ebd2-9b75-4534-8070-65868fb45d2a.cs-asia-southeast1-seal.cloudshell.dev/api/query', {

        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
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
    </div>
  );
}

export default App;
