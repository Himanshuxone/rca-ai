// src/components/BackgroundSelector.jsx
import React, { useState } from "react";

const wallpapers = [
  {
    name: "AI Dark",
    url: "https://source.unsplash.com/1600x900/?ai,technology",
  },
  {
    name: "Cyber Grid",
    url: "https://source.unsplash.com/1600x900/?cyber,grid",
  },
  {
    name: "Server Room",
    url: "https://source.unsplash.com/1600x900/?server,cloud",
  },
  {
    name: "Nebula",
    url: "https://source.unsplash.com/1600x900/?space,nebula",
  },
];

const BackgroundSelector = ({ onChange }) => {
  const [selected, setSelected] = useState(wallpapers[0].url);

  const handleSelect = (url) => {
    setSelected(url);
    onChange(url);
  };

  return (
    <div className="flex flex-wrap gap-4 mt-4 p-4 rounded-lg bg-black/30 backdrop-blur-sm border border-white/20">
      {wallpapers.map((wp, index) => (
        <div
          key={index}
          onClick={() => handleSelect(wp.url)}
          className={`w-28 h-16 rounded-lg overflow-hidden cursor-pointer border-2 transition-all ${
            selected === wp.url ? "border-cyan-400 scale-105" : "border-transparent"
          }`}
        >
          <img
            src={wp.url}
            alt={wp.name}
            className="object-cover w-full h-full hover:opacity-80"
            title={wp.name}
          />
        </div>
      ))}
    </div>
  );
};

export default BackgroundSelector;
