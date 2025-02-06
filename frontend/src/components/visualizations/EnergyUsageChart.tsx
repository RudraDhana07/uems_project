// src/components/visualizations/EnergyUsageChart.tsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { EnergyUsageChartProps, ProcessedChartData } from '../../types/streamElecData';

const isValidNumber = (value: any): boolean => {
  return value !== null && 
         value !== undefined && 
         value !== '-' && 
         !isNaN(value) && 
         value !== 0;  // Exclude 0 if it's a default value
};


const EnergyUsageChart: React.FC<EnergyUsageChartProps> = ({ data, columns }) => {
  const processedData: ProcessedChartData[] = data.map(row => ({
    date: `${row.meter_reading_year}-${row.meter_reading_month}`,
    ...columns.reduce((acc, col) => ({
      ...acc,
      [col.key]: isValidNumber(row[col.key]) ? Number(row[col.key]) : undefined
    }), {})
  }));

  // Custom tooltip formatter
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ 
          backgroundColor: 'white', 
          padding: '10px', 
          border: '1px solid #ccc' 
        }}>
          <p>{`Date: ${label}`}</p>
          {payload.map((entry: any) => (
            <p key={entry.name} style={{ color: entry.color }}>
              {`${entry.name}: ${Number(entry.value).toFixed(2)} kWh`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div style={{ width: '100%', height: '400px', marginBottom: '20px' }}>
      <ResponsiveContainer>
        <LineChart
          data={processedData}
          margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            angle={-45}
            textAnchor="end"
            height={60}
          />
          <YAxis 
            label={{ 
              value: 'Energy Usage (kWh)', 
              angle: -90, 
              position: 'insideLeft' 
            }}
            tickFormatter={(value) => value.toFixed(2)}  // Format Y-axis ticks
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          {columns.map((col) => (
            <Line
              key={col.key}
              type="monotone"
              dataKey={col.key}
              name={col.name}
              stroke={col.color}
              strokeWidth={2}
              dot={{
                r: 2,
                strokeWidth: 1,
                fill: "#fff" 
              }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EnergyUsageChart;
