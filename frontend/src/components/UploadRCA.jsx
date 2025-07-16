import React, { useState } from 'react';
import axios from 'axios';

const UploadRCA = () => {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setSummary('');
  };

  const handleUpload = async () => {
    if (!file) return alert("Please choose a file.");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/analyze", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setSummary(response.data.summary);
    } catch (err) {
      alert("Upload failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-xl shadow-lg">
      <h2 className="text-xl font-bold mb-2">Upload Log File</h2>
      <input type="file" onChange={handleFileChange} className="mb-4" />
      <button
        onClick={handleUpload}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze RCA"}
      </button>

      {summary && (
        <div className="mt-6 bg-gray-700 p-4 rounded text-sm whitespace-pre-wrap">
          <h3 className="text-lg font-semibold mb-2">RCA Summary:</h3>
          {summary}
        </div>
      )}
    </div>
  );
};

export default UploadRCA;
