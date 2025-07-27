import React from "react";
import { AlertTriangle, Info, ShieldAlert } from "lucide-react";

const severityStyles = {
  critical: "bg-red-100 border-red-300 text-red-800",
  warning: "bg-yellow-100 border-yellow-300 text-yellow-800",
  info: "bg-blue-100 border-blue-300 text-blue-800",
};

const severityIcon = {
  critical: <ShieldAlert className="inline mr-2 text-red-700" size={18} />,
  warning: <AlertTriangle className="inline mr-2 text-yellow-600" size={18} />,
  info: <Info className="inline mr-2 text-blue-600" size={18} />,
};

const RCAResult = ({ analysis }) => {
  if (!analysis) return null;

  const severity = analysis.severity || "info";
  const severityClass = severityStyles[severity];

  return (
    <div className={`mt-6 p-6 rounded-xl shadow-md border ${severityClass} max-w-xl mx-auto`}>
      <h2 className="text-2xl font-semibold mb-4 flex items-center">
        {severityIcon[severity]} RCA Analysis – {severity.toUpperCase()}
      </h2>

      <div className="space-y-4">
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
