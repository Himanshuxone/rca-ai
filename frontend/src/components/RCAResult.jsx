import React from "react";

const RCAResult = ({ analysis }) => {
  if (!analysis) return null;

  return (
    <div className="mt-6 p-6 rounded-xl shadow-xl bg-gradient-to-br from-blue-50 to-white border border-blue-200 max-w-xl mx-auto">
      <h2 className="text-2xl font-semibold text-blue-800 mb-4">
        🧠 RCA Analysis Summary
      </h2>

      <div className="space-y-4 text-gray-700">
        <div>
          <h3 className="font-bold">📌 Root Cause:</h3>
          <p className="ml-2">{analysis.root_cause}</p>
        </div>

        <div>
          <h3 className="font-bold">🧩 Affected Component:</h3>
          <p className="ml-2">{analysis.component}</p>
        </div>

        <div>
          <h3 className="font-bold">💡 Recommendation:</h3>
          <p className="ml-2 italic">{analysis.recommendation}</p>
        </div>
      </div>
    </div>
  );
};

export default RCAResult;
