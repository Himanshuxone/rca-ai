// src/pages/Dashboard.jsx
import React, { useEffect, useState } from "react";
import { fetchRCASummary } from "../services/api";
import UploadLogs from "../components/UploadLogs";
import PieChartComponent from "../components/PieChartComponent";
import FlowDiagram from "../components/FlowDiagram";
import ChartPanel from "../components/ChartComponent";

const RCAReports = () => {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchRCASummary();
        setSummary(data);
      } catch (error) {
        console.error("Dashboard API Error:", error.message);
      }
    };
    loadData();
  }, []);

  return (
    <div className="p-6 text-white h-full overflow-auto">
      <h2 className="text-xl font-bold mb-4">RCA Reports</h2>
      {summary ? (
        <>
          <p className="mb-4">Total RCAs: {summary.length}</p>
          <ChartPanel data={summary} />
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default function Dashboard() {
  return (
    <div className="fixed inset-0 flex flex-row bg-gray-900 text-white">
      
      {/* Left Panel */}
      <div className="w-1/2 flex flex-col border-r border-gray-700 overflow-hidden">
        
        {/* Header */}
        <header className="flex items-center gap-4 p-4 border-b border-gray-700 bg-gray-800">
          <h1 className="text-2xl font-bold">Dashboard</h1>
        </header>

        {/* Upload Section */}
        <div className="p-4 border-b border-gray-700 bg-gray-800">
          <UploadLogs />
        </div>

        {/* Charts & Flow Diagram */}
        <div className="flex-1 grid grid-rows-2 gap-4 p-4 overflow-auto">
          <div className="bg-gray-800 rounded-lg p-4">
            <PieChartComponent title="Log Distribution" />
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <FlowDiagram />
          </div>
        </div>
      </div>

      {/* Right Panel */}
      <div className="w-1/2 bg-gray-800 overflow-auto">
        <RCAReports />
      </div>
    </div>
  );
}
