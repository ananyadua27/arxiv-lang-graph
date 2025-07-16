import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const BASE_URL = "http://localhost:8000";

function App() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [report, setReport] = useState("");

  const handleSubmit = async () => {
    setLoading(true);
    setError("");
    setReport("");

    try {
      const res = await fetch(`${BASE_URL}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: "test-session",
          topic: topic,
        }),
      });

      if (!res.ok) {
        setError(`Error: ${res.status} ${res.statusText}`);
        return;
      }

      const data = await res.json();

      if (data.report) {
        setReport(data.report);
      } else {
        setError("No report found in response.");
      }
    } catch (error) {
      setError(`Fetch error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const components = {
    a: ({ href, children }) => (
      <a href={href} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
        {children}
      </a>
    ),
  };

  return (
    <div className="max-w-3xl mx-auto p-6 font-sans">
      <div className="indented-text mb-12 max-w-xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">
          🔗 LangGraph: Discover the Pulse of Tomorrow’s Technology
        </h1>
        <h3 className="text-xl mb-6">
          Powered by LangChain, HuggingFace Transformers, FastAPIs and Cornell University's arXiv
        </h3>

        <div className="flex space-x-4">
          <input
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter a topic for further research (e.g., 'CNN, LSTM, computer vision')"
            className="border border-gray-300 rounded px-5 py-4 w-full max-w-xs focus:outline-none focus:ring-2 focus:ring-blue-500 transition text-lg"
          />

          <button
            onClick={handleSubmit}
            disabled={loading || !topic.trim()}
            className="btn-primary w-full max-w-xs py-4"
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>
      </div>

      {error && (
        <div className="text-red-600 mt-4 font-medium"> {error}</div>
      )}

      {report && (
        <div className="mt-8 bg-gray-50 border border-gray-300 rounded p-6 shadow prose prose-sm max-w-none">
          <ReactMarkdown components={components}>{report}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default App;
