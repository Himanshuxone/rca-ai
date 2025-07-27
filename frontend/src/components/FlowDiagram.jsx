import React from "react";

const FlowDiagram = () => {
  return (
    <div className="p-6 bg-gray-100 border border-gray-300 rounded-xl shadow-sm mt-4">
      <h2 className="text-xl font-semibold mb-4 text-center">System Flow Diagram</h2>
      <div className="flex flex-col md:flex-row justify-center items-center gap-4">
        <div className="bg-blue-100 px-6 py-4 rounded-lg shadow border border-blue-300">User Upload</div>
        <div className="text-xl">➡️</div>
        <div className="bg-green-100 px-6 py-4 rounded-lg shadow border border-green-300">Log Processor</div>
        <div className="text-xl">➡️</div>
        <div className="bg-yellow-100 px-6 py-4 rounded-lg shadow border border-yellow-300">RCA Engine</div>
        <div className="text-xl">➡️</div>
        <div className="bg-purple-100 px-6 py-4 rounded-lg shadow border border-purple-300">Dashboard Report</div>
      </div>
    </div>
  );
};

export default FlowDiagram;