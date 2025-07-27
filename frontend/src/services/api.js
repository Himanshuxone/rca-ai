// src/api/rcaApi.js
const BASE_URL = "http://localhost:8000"; // Update to your actual backend

export const fetchRcaSummary = async () => {
  const res = await fetch(`${BASE_URL}/api/rca-reports`);
  if (!res.ok) throw new Error("Failed to fetch RCA summary");
  return res.json();
};

export const fetchEvents = async () => {
  const res = await fetch(`${BASE_URL}/api/rca-events`);
  if (!res.ok) throw new Error("Failed to fetch events");
  return res.json();
};

export const fetchDashboardData = async () => {
  const res = await fetch(`${BASE_URL}/api/dashboard-data`);
  if (!res.ok) throw new Error("Failed to fetch RCA data");
  return res.json();
};


export const fetchLogSummary = async () => {
  const res = await fetch(`${BASE_URL}/api/log-summary`);
  if (!res.ok) throw new Error("Failed to fetch RCA data");
  return res.json();
};

