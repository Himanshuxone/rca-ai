import React, { useEffect, useState } from "react";
import { Bar, Pie } from "react-chartjs-2";
import { fetchRCASummary } from "../services/api";
import ToggleSwitch from "../components/ToggleSwitch"; // path may vary
import {
  Chart as ChartJS,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(BarElement, ArcElement, CategoryScale, LinearScale, Tooltip, Legend);

const ChartToggle = () => {
  const [chartData, setChartData] = useState(null);
  const [view, setView] = useState("bar"); // Toggle state

  useEffect(() => {
    const loadData = async () => {
      try {
        const result = await fetchRCASummary();
        let chartSummary = {}
        result.summary.forEach(element => {
          chartSummary[element.label] = element.count
        });
        const data = {
          labels: ["Low", "Medium", "High"],
          datasets: [
            {
              label: "RCA Count",
              data: [chartSummary.low, chartSummary.medium, chartSummary.high],
              backgroundColor: ["#3b82f6", "#facc15", "#ef4444"],
              borderColor: "rgba(255,255,255,0.2)",
              borderWidth: 1,
            },
          ],
        };
        setChartData(data);
      } catch (err) {
        console.error("Chart data fetch failed", err);
      }
    };
    loadData();
  }, []);

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: view === "bar" ? "top" : "bottom", labels: { color: "#fff" } },
      tooltip: { enabled: true },
    },
    scales:
      view === "bar"
        ? {
            x: { ticks: { color: "#fff" } },
            y: { beginAtZero: true, ticks: { color: "#fff" } },
          }
        : {},
  };

  return (
    <div className="bg-gray-900 rounded-xl shadow border border-gray-700 p-4 max-w-xl mx-auto">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-white font-semibold text-md">RCA Risk Chart</h3>
        <ToggleSwitch
          checked={view === "pie"}
          onChange={() => setView(view === "bar" ? "pie" : "bar")}
          leftLabel="Bar"
          rightLabel="Pie"
        />
      </div>

      {chartData ? (
        <div className="flex items-center gap-2">
          {view === "bar" ? (
            <div className="w-3/4">
              <Bar data={chartData} options={chartOptions} />
            </div>
          ) : (
            <div className="w-1/3">
              <Pie data={chartData} options={chartOptions} />
            </div>
          )}
        </div>
      ) : (
        <p className="text-gray-400">Loading chart...</p>
      )}
    </div>
  );
};

export default ChartToggle;
