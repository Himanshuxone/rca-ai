import React from 'react';
import { Link } from 'react-router-dom';

export default function Sidebar() {
  return (
    <div className="bg-dark text-white vh-100 p-3" style={{ width: '200px' }}>
      <h4 className="text-white">TechRCA</h4>
      <ul className="nav flex-column mt-4">
        <li className="nav-item">
          <Link to="/" className="nav-link text-white">Home</Link>
        </li>
        <li className="nav-item">
          <Link to="/dashboard" className="nav-link text-white">Dashboard</Link>
        </li>
        <li className="nav-item">
          <Link to="/reports" className="nav-link text-white">RCA Reports</Link>
        </li>
        <li className="nav-item">
          <Link to="/events" className="nav-link text-white">Events</Link>
        </li>
      </ul>
    </div>
  );
}
