import React from 'react';

export default function StatCard({ title, value, color }) {
  return (
    <div className={`card text-white bg-${color} mb-3`} style={{ minWidth: '12rem' }}>
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
        <h3 className="card-text">{value}</h3>
      </div>
    </div>
  );
}
