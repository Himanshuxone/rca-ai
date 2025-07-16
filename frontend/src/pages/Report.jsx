import React, { useState } from 'react';

export default function Report() {
  const [reportId, setReportId] = useState("");
  const [report, setReport] = useState(null);

  const fetchReport = async () => {
    const res = await fetch(`http://localhost:8000/report/${reportId}`);
    const data = await res.json();
    setReport(data);
  };

  return (
    <div>
      <h1>Fetch RCA Report</h1>
      <input
        type="text"
        placeholder="Enter Report ID"
        value={reportId}
        onChange={(e) => setReportId(e.target.value)}
      />
      <button onClick={fetchReport}>Fetch Report</button>

      {report && !report.error && (
        <div className="summary-box">
          <h2>{report.filename}</h2>
          <pre>{report.summary}</pre>
        </div>
      )}

      {report?.error && <p>{report.error}</p>}
    </div>
  );
}
