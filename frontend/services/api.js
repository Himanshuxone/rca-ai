// src/api/rcaApi.js
const BASE_URL = "http://localhost:8000"; // Update to your actual backend

export const fetchRcaSummary = async () => {
  const res = await fetch(`${BASE_URL}/api/rca/summary`);
  if (!res.ok) throw new Error("Failed to fetch RCA summary");
  return res.json();
};

export const fetchEvents = async () => {
  const res = await fetch(`${BASE_URL}/api/events`);
  if (!res.ok) throw new Error("Failed to fetch events");
  return res.json();
};
