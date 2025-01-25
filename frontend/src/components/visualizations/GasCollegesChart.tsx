// src/components/visualizations/GasCollegesChart.tsx

import React from 'react';
import { DataRow } from '../../types/gas';
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


interface GasCollegesChartProps {
    data: DataRow[];
}

const COLLEGE_METERS = [
    {
        id: 'G601,UNIVERSITY COLLEGE (KITCHEN),315 LEITH',
        label: 'University College'
    },
    {
        id: 'K427,CFC EAST ABBEY COLLEGE,682 CASTLE STREET,DUNEDIN',
        label: 'Caroline Freeman College East'
    },
    {
        id: "G608,ST MARGARET'S COLLEGE,333 LEITH",
        label: "St Margaret's College"
    },
    {
        id: 'ARANA 110 CLYDE STREET,DUNEDIN',
        label: 'Arana'
    },
    {
        id: 'AQUINAS 74 GLADSTONE ROAD,DUNEDIN',
        label: 'Aquinas'
    }
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
    '#8c564b'   // Dark brown
];

const GasCollegesChart: React.FC<GasCollegesChartProps> = ({ data }) => {
    // Filter only college meter data
    const collegeData = data.filter(row => 
        COLLEGE_METERS.some(meter => meter.id === row.meter_description)
    );

    // Transform data for the chart and round to 2 decimal places
    const chartData = MONTHS.map(month => {
        const dataPoint: any = { name: month };
        COLLEGE_METERS.forEach(meter => {
            const meterRow = collegeData.find(row => row.meter_description === meter.id);
            const value = meterRow ? meterRow[month] : null;
            dataPoint[meter.label] = value !== null ? Number(Number(value).toFixed(2)) : null;
        });
        return dataPoint;
    });

    return (
        <div style={{ width: '100%', height: 400, marginBottom: '20px' }}>
            <h3 style={{ textAlign: 'center', marginBottom: '20px' }}>
                Gas Consumption Breakdown - Colleges
            </h3>
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
                    {COLLEGE_METERS.map((meter, index) => (
                        <Line
                            key={meter.id}
                            type="monotone"
                            dataKey={meter.label}
                            stroke={COLORS[index]}
                            strokeWidth={2}
                            dot={false}
                        />
                    ))}
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default GasCollegesChart;