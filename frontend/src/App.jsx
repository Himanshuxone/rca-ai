import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Report from './pages/Report';
import DarkModeToggle from './components/DarkModeToggle';

export default function App() {
  return (
    <Router>
      <div className="container">
        <DarkModeToggle />
        <nav>
          <Link to="/">Home</Link> | <Link to="/report">View Report</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/report" element={<Report />} />
        </Routes>
      </div>
    </Router>
  );
}
