import { useState } from "react";

function App() {
  const [idea, setIdea] = useState("");
  const [result, setResult] = useState("");

  const handleSubmit = async () => {
    const res = await fetch("http://localhost:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idea }),
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="min-h-screen text-align-center bg-gray-50 flex flex-col items-center p-8">
      <h1 className="text-4xl font-bold mb-6 text-indigo-600">💡 PitchCraft</h1>
      <textarea
        placeholder="Type your startup idea..."
        value={idea}
        onChange={(e) => setIdea(e.target.value)}
        rows={4}
        cols={50}
        className="w-full max-w-xl p-5 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
      <br />
      <button onClick={handleSubmit} className="mt-4 px-8 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-800 transition">
        Generate Pitch
      </button>
      {result && !result.error && (
        <div className="mt-8 text-center p-5 border border-gray-300 rounded-xl shadow-sm">
          <h2 className="text-2xl font-semibold text-indigo-700 mb-2">🚀 Your AI-Generated Startup Pitch</h2>
          <p><strong>🏢 Company Name:<br/></strong> {result.company_name}</p>
          <p><strong>💬 Tagline:</strong><br /> {result.tagline}</p>
          <p><strong>😓 Problem:</strong><br /> {result.problem}</p>
          <p><strong>💡 Solution:</strong><br /> {result.solution}</p>
          <p><strong>🎤 Elevator Pitch:</strong><br /> {result.elevator_pitch}</p>
        </div>
      )}

    {result && result.error && (
        <div className="mt-8 text-align-center p-5 border border-gray-300 rounded-xl shadow-sm">
          <p>⚠️ Error: {result.error}</p>
          <pre>{result.raw_text}</pre>
        </div>
      )}

    </div>
  );
}

export default App;
