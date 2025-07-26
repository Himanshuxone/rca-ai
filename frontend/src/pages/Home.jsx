import React, { useEffect, useState } from "react";
import UploadLogs from "../components/UploadLogs";
import { fetchDashboardData } from "../services/api";

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
    </div>
  );
}

export default Dashboard;
