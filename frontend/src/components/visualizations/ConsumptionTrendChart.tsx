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
    mthw: item.mthw_consumption_kwh ? Number(Number(item.mthw_consumption_kwh).toFixed(2)) : null,
    medSchool: item.med_school_consumption_kwh ? Number(Number(item.med_school_consumption_kwh).toFixed(2)) : null,
    totalSteam: item.total_steam_consumption_kwh ? Number(Number(item.total_steam_consumption_kwh).toFixed(2)) : null
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
          <YAxis tickFormatter={(value) => value.toFixed(2)} />
          <Tooltip 
            formatter={(value: number) => value.toFixed(2)}
            labelFormatter={(label) => `Month: ${label}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="mthw"
            name="MTHW Consumption"
            stroke="#8884d8"
            strokeWidth={2.5}
            strokeOpacity={0.6}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="medSchool"
            name="Med School Consumption"
            stroke="#82ca9d"
            strokeWidth={2.5}
            strokeOpacity={0.6}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="totalSteam"
            name="Total Steam Consumption"
            stroke="#ff7300"
            strokeWidth={2.5}
            strokeOpacity={0.6}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ConsumptionTrendChart;