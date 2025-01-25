// src/components/visualizations/LTHWConsumptionChart.tsx
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
    [key: string]: string | number | null | undefined;
}

interface LTHWChartProps {
    data: DataRow[];
}

const WOOD_BOILERS = [
    'F622 Psychology wood boiler (IP 10.81.146.160)',
    'F916 College of Education wood boiler (10.81.147.145)',
    'H538 Childcare boiler (IP 10.81.149.14)',
    'H633 Arana Boiler (IP 10.81.148.22)',
    'J122 Carrington Jenkins boiler',
    'XI01 Invercargill Boiler (IP 10.85.4.21)'
];

const MONTHS = [
    'Jan_2022', 'Feb_2022', 'Mar_2022', 'Apr_2022', 'May_2022', 'Jun_2022',
    'Jul_2022', 'Aug_2022', 'Sep_2022', 'Oct_2022', 'Nov_2022', 'Dec_2022',
    'Jan_2023', 'Feb_2023', 'Mar_2023', 'Apr_2023', 'May_2023', 'Jun_2023',
    'Jul_2023', 'Aug_2023', 'Sep_2023', 'Oct_2023', 'Nov_2023', 'Dec_2023',
    'Jan_2024', 'Feb_2024', 'Mar_2024', 'Apr_2024', 'May_2024', 'Jun_2024',
    'Jul_2024', 'Aug_2024', 'Sep_2024', 'Oct_2024', 'Nov_2024', 'Dec_2024',
    'Jan_2025', 'Feb_2025', 'Mar_2025'
];

const COLORS = [
    '#1f77b4',  // Dark blue
    '#2ca02c',  // Dark green
    '#d62728',  // Dark red
    '#9467bd',  // Dark purple
    '#8c564b',  // Dark brown
    '#e377c2'   // Dark pink
];

const LTHWConsumptionChart: React.FC<LTHWChartProps> = ({ data }) => {
    // Filter only wood boiler data
    const boilerData = data.filter(row => WOOD_BOILERS.includes(row.object_name));

    // Transform data for the chart and round to 2 decimal places
    const chartData = MONTHS.map(month => {
        const dataPoint: any = { name: month };
        WOOD_BOILERS.forEach(boiler => {
            const boilerRow = boilerData.find(row => row.object_name === boiler);
            const value = boilerRow ? boilerRow[month] : null;
            dataPoint[boiler] = value !== null ? Number(Number(value).toFixed(2)) : null;
        });
        return dataPoint;
    });

    return (
        <div style={{ width: '100%', height: 400, marginBottom: '20px' }}>
            <ResponsiveContainer>
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                        dataKey="name" 
                        angle={-45} 
                        textAnchor="end" 
                        height={80}
                        interval={2}
                    />
                    <YAxis 
                        label={{ 
                            value: 'Consumption (kWh)', 
                            angle: -90, 
                            position: 'insideLeft' 
                        }}
                        tickFormatter={(value) => value.toFixed(2)}
                    />
                    <Tooltip 
                        formatter={(value: number) => value.toFixed(2)}
                        labelFormatter={(label) => `Month: ${label}`}
                    />
                    <Legend />
                    {WOOD_BOILERS.map((boiler, index) => (
                        <Line
                            key={boiler}
                            type="monotone"
                            dataKey={boiler}
                            stroke={COLORS[index]}
                            strokeWidth={2.5}
                            dot={false}
                            name={boiler.split('(')[0].trim()}
                        />
                    ))}
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default LTHWConsumptionChart;