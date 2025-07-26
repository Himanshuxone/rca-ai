import React, { useState } from "react";
import { CheckCircle } from "lucide-react";
import { uploadFile } from "../services/uploadFile";
import RCAResult from "./RCAResult"; // adjust the path as needed

export default function UploadLogs({ onUploadSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [filePreview, setFilePreview] = useState("");
  const [structuredLogs, setStructuredLogs] = useState([]);   // to store parsed data
  const [uploadResult, setUploadResult] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setUploadStatus("");
    setSuccess(false);
    setFilePreview("");

    if (file && file.type.startsWith("text") || file.name.endsWith(".log") || file.name.endsWith(".json")) {
      const reader = new FileReader();
      reader.onload = () => {
        const content = reader.result;
        const lines = content.split("\n").slice(0, 20).join("\n"); // preview first 20 lines
        setFilePreview(lines);
      };
      reader.readAsText(file);
    } else {
      setFilePreview("⚠️ Preview not supported for this file type.");
    }
  };

  function parseLogLines(content) {
  const lines = content.split("\n");
  const logRegex = /(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}(?:,\d{3})?)?\s?(ERROR|WARN|INFO)?\s?-?\s?(.*)/;

    return lines.map((line, index) => {
        const match = line.match(logRegex);
        return {
            id: index,
            timestamp: match?.[1] || "N/A",
            level: match?.[2] || "N/A",
            message: match?.[3] || line,
            };
        });
    }

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus("⚠️ Please select a file.");
      return;
    }

    setLoading(true);
    setUploadStatus("");
    setSuccess(false);
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      const response = await uploadFile(selectedFile);
      if (response.ok) {
        setUploadStatus("✅ Upload successful!");
        setSuccess(true);
        setSelectedFile(null);
        setFilePreview("");
        setAnalysis(response.analysis);  // RCA results
        if (onUploadSuccess) {
          onUploadSuccess();
        }
      } else {
        setUploadStatus("❌ Upload failed.");
      }
    } catch (error) {
      console.log("=============", error)
      setUploadStatus("❌ Error uploading file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 px-4">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
        📤 Upload RCA Log
      </h2>

      <div className="flex flex-col gap-4">
        <label className="cursor-pointer inline-block w-fit text-blue-600 dark:text-blue-400 font-medium hover:underline">
          📁 Choose File
          <input
            type="file"
            accept=".log,.txt,.json"
            onChange={handleFileChange}
            className="hidden"
          />
        </label>

        {selectedFile && (
          <p className="text-sm text-gray-700 dark:text-gray-300">
            📎 <strong>{selectedFile.name}</strong> selected
          </p>
        )}

        {filePreview && (
          <div className="bg-black/70 dark:bg-white/5 p-3 text-sm text-white dark:text-gray-200 rounded-xl overflow-auto max-h-64 whitespace-pre-wrap border border-white/10 shadow-inner">
            {filePreview}
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={loading}
          className={`text-blue-600 dark:text-blue-400 border border-blue-500 dark:border-blue-400 rounded-xl px-4 py-2 font-semibold hover:bg-blue-50 dark:hover:bg-blue-900/30 transition ${
            loading ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          {loading ? "Uploading..." : "Upload File"}
        </button>

        {uploadResult && (
            <pre className="upload-result">{JSON.stringify(uploadResult, null, 2)}</pre>
        )}

        {uploadStatus && (
          <p className="text-sm mt-2 text-gray-700 dark:text-gray-300">
            {uploadStatus}
          </p>
        )}

        {success && (
          <div className="flex items-center gap-2 mt-2 text-green-600 dark:text-green-400 animate-fade-in">
            <CheckCircle className="w-5 h-5" />
            <span>File uploaded successfully!</span>
          </div>
        )}

        {/* ✅ OPTIONAL: Render structured parsed logs here */}
        {structuredLogs.length > 0 && (
            <div className="mt-4 border-t pt-4">
            <h3 className="text-lg font-semibold mb-2 text-gray-700 dark:text-gray-200">
                🧩 Parsed Log Entries
            </h3>
            <div className="overflow-x-auto rounded-lg border border-gray-300 dark:border-gray-700">
                <table className="w-full text-sm text-left text-gray-800 dark:text-gray-200">
                <thead className="bg-gray-100 dark:bg-gray-800">
                    <tr>
                    <th className="px-3 py-2">Timestamp</th>
                    <th className="px-3 py-2">Level</th>
                    <th className="px-3 py-2">Message</th>
                    <th className="px-3 py-2">Component</th>
                    </tr>
                </thead>
                <tbody>
                    {structuredLogs.map((log, index) => (
                    <tr
                        key={index}
                        className={`border-t border-gray-200 dark:border-gray-600 ${
                        log.level === "ERROR"
                            ? "bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300"
                            : ""
                        }`}
                    >
                        <td className="px-3 py-1">{log.timestamp}</td>
                        <td className="px-3 py-1">{log.level}</td>
                        <td className="px-3 py-1">{log.message}</td>
                        <td className="px-3 py-1">{log.component}</td>
                    </tr>
                    ))}
                </tbody>
                </table>
            </div>
            </div>
        )}
        {/* <div className="rca-card">
        <h2>🧠 RCA Analysis Summary</h2> */}
        {analysis && <RCAResult analysis={analysis} />}
        {/* </div> */}
      </div>
    </div>
  );
}
