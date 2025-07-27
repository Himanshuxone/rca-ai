import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Events from "./pages/Events";
import RCAReports from "./pages/RCAReports";
import NotFound from "./pages/NotFound";

const App = () => {
  return (
    <div className="d-flex">
      <div className="flex-grow-1">
        <Navbar />
        <main className="p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/reports" element={<RCAReports />} />
            <Route path="/events" element={<Events />} />
            <Route path="/home" element={<Navigate to="/" />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

export default App;
