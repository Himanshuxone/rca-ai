// src/pages/Dashboard.jsx
import React, { useEffect, useState } from "react";
import { fetchRCASummary } from "../services/api";
import ChartPanel from "../components/ChartComponent";

const RCAReports = () => {
    const [summary, setSummary] = useState(null);
    useEffect(() => {
      const loadData = async () => {
        try {
          const data = await fetchRCASummary();
          setSummary(data);
        } catch (error) {
          console.error("Dashboard API Error:", error.message);
        }
      };
      loadData();
    }, []);
  return (
    <div>
      <h2>RCAReports</h2>
      {summary ? (
        <div>
          <p>Total RCAs: {summary.length}</p>
          <ChartPanel data={summary} />
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default RCAReports