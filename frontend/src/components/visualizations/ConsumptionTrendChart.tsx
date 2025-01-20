// src/components/visualizations/ConsumptionTrendChart.tsx
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface TrendChartProps {
  data: any[];
}

const ConsumptionTrendChart: React.FC<TrendChartProps> = ({ data }) => {
  const chartData = data.map(item => ({
    date: `${item.month} ${item.year}`,
    mthw: item.mthw_consumption_kwh,
    medSchool: item.med_school_consumption_kwh,
    totalSteam: item.total_steam_consumption_kwh
  }));

  return (
    <div style={{ width: '100%', height: 400, marginTop: 20 }}>
      <ResponsiveContainer>
        <LineChart
          data={chartData}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            angle={-45}
            textAnchor="end"
            height={70}
          />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="mthw"
            name="MTHW Consumption"
            stroke="#8884d8"
            strokeWidth={2.5}  // Even thicker line
            strokeOpacity={0.6}  // Optional: add some transparency
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="medSchool"
            name="Med School Consumption"
            stroke="#82ca9d"
            strokeWidth={2.5}  // Even thicker line
            strokeOpacity={0.6}  // Optional: add some transparency
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="totalSteam"
            name="Total Steam Consumption"
            stroke="#ff7300"
            strokeWidth={2.5}  // Even thicker line
            strokeOpacity={0.6}  // Optional: add some transparency
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ConsumptionTrendChart;
