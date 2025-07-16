import React, { useState } from 'react';

export default function Home() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setSummary(data.summary);
  };

  return (
    <div>
      <h1>Upload Logs for RCA</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} accept=".txt,.json,.csv" />
        <button type="submit">Analyze Logs</button>
      </form>
      {summary && <div className="summary-box"><pre>{summary}</pre></div>}
    </div>
  );
}
