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
      <h2>📊 RCA Summary Dashboard</h2>
      {summary ? (
        <div>
          <div style={styles.cards}></div>
          <p>Total RCAs: {summary.total}</p>
          <ChartComponent data={summary.chartData} />
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

const styles = {
  cards: {
    display: "flex",
    gap: "2rem",
    margin: "2rem 0",
    flexWrap: "wrap",
  },
  card: {
    backgroundColor: "rgba(255, 255, 255, 0.1)",
    padding: "1.5rem",
    borderRadius: "12px",
    minWidth: "180px",
    flex: 1,
    textAlign: "center",
    boxShadow: "0 2px 8px rgba(0,0,0,0.3)"
  }
};

export default Dashboard;
