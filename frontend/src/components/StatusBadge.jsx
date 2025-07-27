import React from "react";

const statusColors = {
  success: "bg-green-100 text-green-800",
  warning: "bg-yellow-100 text-yellow-800",
  error: "bg-red-100 text-red-800",
  info: "bg-blue-100 text-blue-800",
};

const StatusBadge = ({ status = "info", children }) => {
  return (
    <span className={`text-xs px-2 py-1 rounded-full font-medium ${statusColors[status]}`}>
      {children}
    </span>
  );
};

export default StatusBadge;