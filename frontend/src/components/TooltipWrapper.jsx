import React from "react";

const TooltipWrapper = ({ children, tooltip }) => {
  return (
    <div className="relative group cursor-pointer">
      {children}
      <div className="absolute z-10 invisible group-hover:visible bg-black text-white text-xs rounded px-2 py-1 bottom-full mb-2 left-1/2 -translate-x-1/2 whitespace-nowrap">
        {tooltip}
      </div>
    </div>
  );
};

export default TooltipWrapper;
