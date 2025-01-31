// src/components/visualizations/MTHWConsumptionChart.tsx

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

// Match the DataRow interface with MthwDataView
interface DataRow {
    meter_location?: string;
    multiplier_for_unit?: number;
    misc1?: string;
    misc2?: string;
    [key: string]: string | number | null | undefined;
}

interface MTHWChartProps {
    data: DataRow[];
}

const HIGHLIGHTED_METERS = [
    "St Margaret's MTHW ",
    "G404, Microbiology " , 
    "G405, Science 3 ", 
    "F505, Richardson Total", 
    "G413, Science 2 total" , 
    "F419, ISB ", 
    "E201 Dental Steam Total",
    "F402, Union", 
    "F518, Arts Building ",
    "G401 Mellor Lab total"
];

const MONTHS = [
    'Nov_2021', 'Dec_2021',
    'Jan_2022', 'Feb_2022', 'Mar_2022', 'Apr_2022', 'May_2022', 'Jun_2022',
    'Jul_2022', 'Aug_2022', 'Sep_2022', 'Oct_2022', 'Nov_2022', 'Dec_2022',
    'Jan_2023', 'Feb_2023', 'Mar_2023', 'Apr_2023', 'May_2023', 'Jun_2023',
    'Jul_2023', 'Aug_2023', 'Sep_2023', 'Oct_2023', 'Nov_2023', 'Dec_2023',
    'Jan_2024', 'Feb_2024', 'Mar_2024', 'Apr_2024', 'May_2024', 'Jun_2024',
    'Jul_2024', 'Aug_2024', 'Sep_2024', 'Oct_2024', 'Nov_2024', 'Dec_2024',
    'Jan_2025', 'Feb_2025', 'Mar_2025'
];

const COLORS = [
    '#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
    '#e377c2', '#ff7f0e', '#17becf', '#bcbd22'
];

const MTHWConsumptionChart: React.FC<MTHWChartProps> = ({ data }) => {
    // Filter only highlighted meter data
    const meterData = data.filter(row => 
        row.meter_location && HIGHLIGHTED_METERS.includes(row.meter_location));

    // Transform data for the chart
    const chartData = MONTHS.map(month => {
        const dataPoint: { [key: string]: string | number } = { name: month };
        HIGHLIGHTED_METERS.forEach(meter => {
            const meterRow = meterData.find(row => row.meter_location === meter);
            if (meterRow && meterRow[month] !== undefined) {
                const value = Number(meterRow[month]);
                dataPoint[meter] = !isNaN(value) ? Number(value.toFixed(2)) : 0;
            } else {
                dataPoint[meter] = 0;
            }
        });
        return dataPoint;
    });

    return (
        <ResponsiveContainer width="100%" height={500}>
            <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                    dataKey="name"
                    angle={-45}
                    textAnchor="end"
                    height={100}
                    interval={0}
                    fontSize={12}
                />
                <YAxis 
                    label={{ 
                        value: 'Consumption', 
                        angle: -90, 
                        position: 'insideLeft' 
                    }}
                />
                <Tooltip 
                    formatter={(value: number) => value.toFixed(2)}
                    labelFormatter={(label) => `Month: ${label}`}
                />
                <Legend 
                    layout="vertical" 
                    align="right" 
                    verticalAlign="middle"
                />
                {HIGHLIGHTED_METERS.map((meter, index) => (
                    <Line
                        key={meter}
                        type="monotone"
                        dataKey={meter}
                        stroke={COLORS[index % COLORS.length]}
                        dot={false}
                        name={meter}
                    />
                ))}
            </LineChart>
        </ResponsiveContainer>
    );
};

export default MTHWConsumptionChart;
