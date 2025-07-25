// src/pages/Dashboard.jsx
import React, { useEffect, useState } from "react";
import { fetchRcaSummary } from "../services/api";
import ChartComponent from "../components/ChartComponent";

const Dashboard = () => {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchRcaSummary();
        setSummary(data);
      } catch (error) {
        console.error("Dashboard API Error:", error.message);
      }
    };
    loadData();
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      {summary ? (
        <div>
          <p>Total RCAs: {summary.total}</p>
          <ChartComponent data={summary.chartData} />
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Dashboard;
