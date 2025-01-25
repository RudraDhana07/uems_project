// src/components/visualizations/GasDNCollegesChart.tsx

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


interface GasDNCollegesChartProps {
    automatedData: DataRow[];
    consumptionData: DataRow[];
}

const DN_COLLEGES_METERS = [
    {
        id: 'F940 PLAZA BUILDING,132 ANZAC AVENUE,FORSYTH',
        label: 'Plaza',
        type: 'automated'
    },
    {
        id: 'G412,SCIENCE 2 BOILER HOUSE,72 UNION PLACE',
        label: 'Science 2 Boiler',
        type: 'automated'
    },
    {
        id: 'ECCLES GREAT KING STREET,UNIVERSITY OF',
        label: 'Eccles',
        type: 'automated'
    },
    {
        id: ' Total Gas Energy - DN',
        label: 'Total DN Gas Consumption',
        type: 'consumption'
    },
    {
        id: 'Total Gas Energy - Colleges',
        label: 'Total Colleges Gas Consumption',
        type: 'consumption'
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

const GasDNCollegesChart: React.FC<GasDNCollegesChartProps> = ({ automatedData, consumptionData }) => {
    // Transform data for the chart and round to 2 decimal places
    const chartData = MONTHS.map(month => {
        const dataPoint: any = { name: month };
        
        DN_COLLEGES_METERS.forEach(meter => {
            let value = null;
            if (meter.type === 'automated') {
                const meterRow = automatedData.find(row => 
                    row.meter_description === meter.id
                );
                value = meterRow ? meterRow[month] : null;
            } else {
                const meterRow = consumptionData.find(row => 
                    row.object_description === meter.id
                );
                value = meterRow ? meterRow[month] : null;
            }
            dataPoint[meter.label] = value !== null ? Number(Number(value).toFixed(2)) : null;
        });
        return dataPoint;
    });

    return (
        <div style={{ width: '100%', height: 400, marginBottom: '20px' }}>
            <h3 style={{ textAlign: 'center', marginBottom: '20px' }}>
                Gas Consumption Break down - DN vs Colleges
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
                    {DN_COLLEGES_METERS.map((meter, index) => (
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

export default GasDNCollegesChart;