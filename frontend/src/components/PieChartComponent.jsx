import React, { useEffect, useState } from "react";
import { fetchLogSummary } from "../services/api";
import { PieChart, Pie, Cell, Tooltip, Legend, Sector, ResponsiveContainer } from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

const PieChartComponent = ({ title }) => {
  const [data, setData] = useState([]);
  const [isFallback, setIsFallback] = useState(false);
  const [activeIndex, setActiveIndex] = useState(null);

  const onPieEnter = (_, index) => {
    setActiveIndex(index);
  };

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const result = await fetchLogSummary();
        const formattedData = [
          { name: "Errors", value: result.summary.errors || 0 },
          { name: "Warnings", value: result.summary.warnings || 0 },
          { name: "Info", value: result.summary.info || 0 },
        ];

        // Check if values are valid numbers
        const isValidData =
          Array.isArray(formattedData) &&
          formattedData.every((d) => typeof d.value === "number");

        if (!isValidData || formattedData.every((d) => d.value === 0)) {
          throw new Error("Invalid or empty data");
        }

        setData(formattedData);
      } catch (error) {
        console.warn("API failed, using fallback data", error);
        setData([
          { name: "Errors", value: 10 },
          { name: "Warnings", value: 5 },
          { name: "Info", value: 15 },
        ]);
        setIsFallback(true);
      }
    };

    fetchChartData();
  }, []);

  const renderActiveShape = (props) => {
    const RADIAN = Math.PI / 180;
    const {
      cx, cy, midAngle, innerRadius, outerRadius, startAngle, endAngle,
      fill, payload, percent, value
    } = props;

    const sin = Math.sin(-RADIAN * midAngle);
    const cos = Math.cos(-RADIAN * midAngle);
    const sx = cx + (outerRadius + 10) * cos;
    const sy = cy + (outerRadius + 10) * sin;

    return (
      <g>
        <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>
          {payload.name}
        </text>
        <Sector
          cx={cx}
          cy={cy}
          innerRadius={innerRadius}
          outerRadius={outerRadius + 6}
          startAngle={startAngle}
          endAngle={endAngle}
          fill={fill}
        />
      </g>
    );
  };

  return (
    <div className="p-4 rounded-xl shadow-md bg-gray-900 text-white w-full md:w-1/2">
      <h3 className="text-lg font-semibold mb-2 text-center">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
      {Array.isArray(data) && data.length > 0 ? (
        <>
          <PieChart width={300} height={250}>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              outerRadius={80}
              activeIndex={activeIndex}
              activeShape={renderActiveShape}
              onMouseEnter={onPieEnter}
              fill="#8884d8"
              dataKey="value"
              label
              isAnimationActive={true}
              animationDuration={1000}
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip contentStyle={{ backgroundColor: '#333', borderColor: '#555', color: '#fff' }} />
            <Legend wrapperStyle={{ color: '#fff' }} />
          </PieChart>
          {isFallback && (
            <p className="text-xs text-center text-yellow-600 mt-2">
              Showing fallback data
            </p>
          )}
        </>
      ) : (
        <p className="text-center text-gray-500">Loading chart data...</p>
      )}
      </ResponsiveContainer>
    </div>
  );
};

export default PieChartComponent;
