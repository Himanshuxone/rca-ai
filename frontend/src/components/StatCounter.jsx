import React from "react";
import CountUp from "react-countup";

const StatCounter = ({ label, value, icon: Icon, color = "text-blue-600" }) => {
  return (
    <div className="flex items-center gap-4 bg-white p-4 rounded-xl shadow-md w-full">
      {Icon && <Icon className={`w-6 h-6 ${color}`} />}
      <div>
        <div className="text-sm text-gray-500">{label}</div>
        <div className={`text-xl font-bold ${color}`}>
          <CountUp end={value} duration={1.5} />
        </div>
      </div>
    </div>
  );
};

export default StatCounter;