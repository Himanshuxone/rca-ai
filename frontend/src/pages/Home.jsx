import React, { useEffect, useState } from "react";
import UploadLogs from "../components/UploadLogs";
import { fetchDashboardData } from "../services/api";
import PieChartComponent from "../components/PieChartComponent";
import FlowDiagram from "../components/FlowDiagram";

function Dashboard() {
  const [data, setData] = useState(null);

  const fetchData = async () => {
    const res = await fetchDashboardData();
    setData(res);
  };

  useEffect(() => {
    fetchData(); // initial load
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <UploadLogs onUploadSuccess={fetchData} />
      {/* render dashboard data below */}
      <PieChartComponent title="Log Distribution" />
      <FlowDiagram />
    </div>
  );
}

export default Dashboard;
