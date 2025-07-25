import React from 'react';
import StatCard from '../components/StatCard';
import ChartCard from '../components/ChartCard';
import { Bar } from 'react-chartjs-2';

export default function Dashboard() {
  const barData = {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [
      {
        label: 'Resolved RCAs',
        data: [5, 8, 6],
        backgroundColor: '#0d6efd',
      },
    ],
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <div className="d-flex flex-wrap gap-3 my-4">
        <StatCard title="Total RCAs" value={34} color="primary" />
        <StatCard title="Pending" value={5} color="warning" />
        <StatCard title="Resolved" value={29} color="success" />
        <StatCard title="Avg Time (min)" value={43} color="info" />
      </div>

      <ChartCard title="Monthly RCA Summary">
        <Bar data={barData} />
      </ChartCard>
    </div>
  );
}
