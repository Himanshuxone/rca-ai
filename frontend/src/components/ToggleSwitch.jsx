import React from "react";

const ToggleSwitch = ({
  checked,
  onChange,
  leftLabel = "",
  rightLabel = "",
}) => {
  return (
    <div className="flex items-center gap-3 text-base text-white">
      {leftLabel && <span>{leftLabel}</span>}
      <label className="relative inline-flex items-center cursor-pointer">
        <input
          type="checkbox"
          checked={checked}
          onChange={onChange}
          className="sr-only peer"
        />
        <div className="w-16 h-9 bg-gray-600 rounded-full peer peer-checked:bg-blue-600 transition-all duration-300">
            <div className="absolute w-7 h-7 bg-white rounded-full shadow-md transform transition-transform duration-300 top-1 left-1 peer-checked:translate-x-7"></div>
        </div>
      </label>
      {rightLabel && <span>{rightLabel}</span>}
    </div>
  );
};

export default ToggleSwitch;
