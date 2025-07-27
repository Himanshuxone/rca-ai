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

const ChartComponent = (summary) => {
  const [data, setData] = useState(null);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await fetchLogSummary();
        const formattedData = {
          labels: ['Low', 'Medium', 'High'],
          datasets: [
            {
              label: 'RCA Count',
              data: [result.low, result.medium, result.high],
              backgroundColor: [
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(255, 99, 132, 0.6)'
              ]
            }
        ]}
        setData(formattedData);
      } catch (error) {
        console.error("API failed, using fallback data", error);
        setData({
          labels: ['Low', 'Medium', 'High'],
          datasets: [
            {
              label: 'RCA Count (Fallback)',
              data: [2, 5, 7],
              backgroundColor: [
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(255, 99, 132, 0.6)'
              ],
              borderColor: '#333',
              borderWidth: 1,
            },
          ],
        });      
      }
    }; fetchData(); // initial load
  }, []);
  return (
    <div className="p-4 bg-gray-900 rounded-xl shadow-lg w-full md:w-1/2">
      <h3 className="text-white text-lg font-semibold mb-4 text-center">RCA Severity Breakdown</h3>
      {data ? (
        <Bar data={data} options={options} />
      ) : (
        <p className="text-center text-gray-400">Loading chart...</p>
      )}
    </div>
  );
};

export default ChartComponent;

