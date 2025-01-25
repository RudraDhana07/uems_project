// src/components/visualizations/ElectricityConsumptionChart.tsx
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

interface DataRow {
  object_name: string;
  object_description?: string;
  meter_location?: string;
  reading_description?: string;
  [key: string]: string | number | undefined;
}

interface ChartProps {
  data: DataRow[];
}

const ElectricityConsumptionChart: React.FC<ChartProps> = ({ data }) => {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return null;
  }

  // Filter data for XA05 Manukau Dental meter
  const electricityData = data.filter((row: DataRow) => 
    row?.meter_location === 'XA05 Manukau Dental  - kWh '
  );

  if (!electricityData.length || !electricityData[0]) {
    return null;
  }

  // Define months to set as NULL
  const nullValueMonths = ['Apr_2024'];
  
  // Get the column names from the DataTable component's columnOrder
  const columnOrder = [
    'Dec_2021',
    'Jan_2022', 'Feb_2022', 'Mar_2022', 'Apr_2022', 'May_2022', 'Jun_2022',
    'Jul_2022', 'Aug_2022', 'Sep_2022', 'Oct_2022', 'Nov_2022', 'Dec_2022',
    'Jan_2023', 'Feb_2023', 'Mar_2023', 'Apr_2023', 'May_2023', 'Jun_2023',
    'Jul_2023', 'Aug_2023', 'Sep_2023', 'Oct_2023', 'Nov_2023', 'Dec_2023',
    'Jan_2024', 'Feb_2024', 'Mar_2024', 'Apr_2024', 'May_2024', 'Jun_2024',
    'Jul_2024', 'Aug_2024', 'Sep_2024', 'Oct_2024', 'Nov_2024', 'Dec_2024',
    'Jan_2025', 'Feb_2025', 'Mar_2025'
  ];

  // Transform data using the column order and round to 2 decimal places
  const chartData = columnOrder
    .map(month => ({
      date: month.replace('_', ' '),
      consumption: nullValueMonths.includes(month) ? null :
                  (electricityData[0][month] !== null && 
                   electricityData[0][month] !== undefined ? 
                   Number(Number(electricityData[0][month]).toFixed(2)) : null)
    }))
    .filter(item => item.consumption !== null);

  if (!chartData.length) {
    return null;
  }

  return (
    <div style={{ width: '100%', height: 400, marginTop: 20 }}>
      <ResponsiveContainer>
        <LineChart
          data={chartData}
          margin={{ top: 5, right: 30, left: 20, bottom: 25 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date"
            angle={-45}
            textAnchor="end"
            height={70}
            interval={2}
          />
          <YAxis tickFormatter={(value) => value.toFixed(2)} />
          <Tooltip 
            formatter={(value: number) => value.toFixed(2)}
            labelFormatter={(label) => `Month: ${label}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="consumption"
            name="XA05 Manukau Dental  - kWh"
            stroke="#8884d8"
            strokeWidth={4}
            strokeOpacity={0.7}
            dot={{ stroke: '#8884d8', strokeWidth: 2, r: 4 }}
            connectNulls={true}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ElectricityConsumptionChart;