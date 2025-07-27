import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

import { Bar } from 'react-chartjs-2';
import React, { useEffect, useState } from "react";
import { fetchLogSummary } from "../services/api";

const options = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Monthly RCA Trends' },
  },
};

const formattedData = {
  labels: ['low', 'medium', 'high'],
  datasets: [
    {
      label: 'RCA Count',
      data: [1,1,2],
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
    }
]}

// let chartDataSet = {labels: ['low', 'medium', 'high']};

const ChartComponent = (summary) => {
  const [data, setData] = useState(null);
  useEffect(() => {
    const fetchData = async () => {
    try {
      const result = await fetchLogSummary();
      const formattedData = {
        labels: ['low', 'medium', 'high'],
        datasets: [
          {
            label: 'RCA Count',
            data: [result.low, result.medium, result.high],
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
          }
      ]}
      setData(formattedData);
    } catch (error) {
      console.warn("API failed, using fallback data", error);
      setData([formattedData]);
      setIsFallback(true);
    }
  }; fetchData(); // initial load
  }, []);
  return (<Bar data={data} options={options} />);
};

export default ChartComponent;

