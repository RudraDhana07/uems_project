// src/components/views/EnergyTotalDashboard.tsx
import React, { useState, useEffect } from 'react';
import { Tabs, Tab, Box, CircularProgress } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import EnergyAnalyticsChart from '../visualizations/EnergyAnalyticsChart';
import EnergyYearComparison from '../visualizations/EnergyYearComparison';

interface EnergyData {
    id: number;
    month: string;
    year: number;
    total_stream_dn_electricity_kwh: number;
    mthw_kwh: number;
    steam_kwh: number;
    lpg_kwh: number;
    woodchip_pellet_kwh: number;
    solar_kwh: number;
    total_kwh: number;
}

interface TabPanelProps {
    children?: React.ReactNode;
    value: number;
    index: number;
}

function CustomTabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;
    return (
        <div role="tabpanel" hidden={value !== index} {...other}>
            {value === index && (
                <Box sx={{ p: 3 }}>{children}</Box>
            )}
        </div>
    );
}

const tableStyles = {
    container: {
        margin: '20px',
        overflowX: 'auto' as const,
        backgroundColor: '#fff',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    },
    table: {
        width: '100%',
        borderCollapse: 'collapse' as const,
        border: '1px solid #ddd'
    },
    th: {
        backgroundColor: '#e6f3ff',
        padding: '12px 8px',
        border: '1px solid #ddd',
        position: 'sticky' as const,
        top: 0,
        fontSize: '0.9rem',
        fontWeight: 'bold',
        textTransform: 'capitalize' as const
    },
    td: {
        padding: '8px',
        border: '1px solid #ddd',
        fontSize: '0.9rem'
    },
    filterContainer: {
        padding: '20px',
        display: 'flex',
        gap: '20px'
    },
    select: {
        padding: '8px',
        borderRadius: '4px',
        border: '1px solid #ddd'
    },
    errorMessage: {
        color: 'red',
        padding: '20px',
        textAlign: 'center' as const
    },
    loadingContainer: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '40px'
    }
};

const getRowStyle = (year: number, index: number) => {
    const yearColors = {
        2022: ['#fff3e0', '#ffe0b2'],
        2023: ['#e8f5e9', '#c8e6c9'],
        2024: ['#e3f2fd', '#bbdefb'],
        2025: ['#f3e5f5', '#e1bee7']
    };
    const colors = yearColors[year as keyof typeof yearColors] || ['#ffffff', '#f5f5f5'];
    return { backgroundColor: colors[index % 2] };
};



const EnergyTotalDashboard: React.FC = () => {
    const [activeTab, setActiveTab] = useState(0);
    const [data, setData] = useState<EnergyData[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedYear, setSelectedYear] = useState<string>('all');
    const [selectedMonth, setSelectedMonth] = useState<string>('all');

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true);
                setError(null);
                const response = await fetch('http://127.0.0.1:5001/api/energy-total/dashboard');
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const jsonText = await response.text();
                const cleanedJsonText = jsonText.replace(/: NaN/g, ': null');
                const result = JSON.parse(cleanedJsonText);
                
                const validData = result.filter((item: EnergyData) => 
                    item.total_stream_dn_electricity_kwh > 0 || 
                    item.mthw_kwh > 0 ||
                    item.steam_kwh > 0 ||
                    item.lpg_kwh > 0
                );
                
                setData(validData);
            } catch (error) {
                setError(error instanceof Error ? error.message : 'Failed to load data');
                console.error('Error fetching data:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, []);

    const filteredData = data.filter(row => {
        const yearMatch = selectedYear === 'all' || row.year.toString() === selectedYear;
        const monthMatch = selectedMonth === 'all' || row.month === selectedMonth;
        return yearMatch && monthMatch;
    });

    const formatValue = (value: number | null): string => {
        if (value === null || isNaN(value)) return '-';
        return new Intl.NumberFormat('en-NZ').format(Math.round(value));
    };

    const chartData = filteredData
    .filter(row => row.total_kwh !== null && !isNaN(row.total_kwh))
    .map(row => ({
        month: `${row.month}-${row.year}`, // Changed from period to month
        'Electricity': row.total_stream_dn_electricity_kwh || 0,
        'MTHW': row.mthw_kwh || 0,
        'Steam': row.steam_kwh || 0,
        'LPG': row.lpg_kwh || 0,
        'Woodchip/Pellet': row.woodchip_pellet_kwh || 0,
        'Solar': row.solar_kwh || 0,
        'Total': row.total_kwh || 0
    }));

    if (error) {
        return <div style={tableStyles.errorMessage}>Error: {error}</div>;
    }

    if (isLoading) {
        return (
            <div style={tableStyles.loadingContainer}>
                <CircularProgress />
            </div>
        );
    }

    return (
        <div>
            <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
                <Tab label="Energy Data" />
                <Tab label="Energy Analytics" />
                <Tab label="Energy Year-wise Comparison" />
            </Tabs>

            <CustomTabPanel value={activeTab} index={0}>
                <div>
                    <div style={tableStyles.filterContainer}>
                        <select
                            style={tableStyles.select}
                            value={selectedYear}
                            onChange={(e) => setSelectedYear(e.target.value)}
                        >
                            <option value="all">All Years</option>
                            {Array.from(new Set(data.map(item => item.year))).sort().map(year => (
                                <option key={year} value={year}>{year}</option>
                            ))}
                        </select>

                        <select
                            style={tableStyles.select}
                            value={selectedMonth}
                            onChange={(e) => setSelectedMonth(e.target.value)}
                        >
                            <option value="all">All Months</option>
                            {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                                .map(month => (
                                    <option key={month} value={month}>{month}</option>
                                ))}
                        </select>
                    </div>

                    <div style={{ height: '600px', padding: '20px 20px 20px 20px' }}>
                        <ResponsiveContainer>
                            <LineChart data={chartData}
                                        margin={{ top: 20, right: 30, left: 50, bottom: 90 }} >
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis 
                                    dataKey="month"
                                    angle={-45}
                                    textAnchor="end"
                                    height={80}
                                    interval={0}
                                    tick={{ fontSize: 12 }}
                                />
                                <YAxis
                                    width={70}  // Increased width for Y-axis
                                    tick={{ fontSize: 12 }}
                                    tickFormatter={(value) => `${value.toLocaleString()}`}  // Format large numbers
                                    label={{ 
                                        value: 'Energy (kWh)', 
                                        angle: -90, 
                                        position: 'insideLeft',
                                        offset: -40  // Adjusted offset
                                    }} 
                                />
                                <Tooltip 
                                    formatter={(value, name) => `${Number(value).toFixed(2)} kWh`}
                                    labelFormatter={(label, payload) => {
                                        if (payload && payload[0]) {
                                        return `${label}`;
                                        }
                                        return label;
                                    }}
                                />[4][5]
                                <Legend wrapperStyle={{ paddingTop: '20px' }}  />
                                <Line type="monotone" dataKey="Electricity" stroke="#8884d8" />
                                <Line type="monotone" dataKey="MTHW" stroke="#82ca9d" />
                                <Line type="monotone" dataKey="Steam" stroke="#ffc658" />
                                <Line type="monotone" dataKey="LPG" stroke="#ff7300" />
                                <Line type="monotone" dataKey="Woodchip/Pellet" stroke="#00C49F" />
                                <Line type="monotone" dataKey="Solar" stroke="#FFBB28" />
                                <Line type="monotone" dataKey="Total" stroke="#FF8042" strokeWidth={2} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>

                    <div style={tableStyles.container}>
                        <table style={tableStyles.table}>
                            <thead>
                                <tr>
                                    <th style={tableStyles.th}>Month</th>
                                    <th style={tableStyles.th}>Year</th>
                                    <th style={tableStyles.th}>Total Stream DN Electricity (kWh)</th>
                                    <th style={tableStyles.th}>MTHW (kWh)</th>
                                    <th style={tableStyles.th}>Steam (kWh)</th>
                                    <th style={tableStyles.th}>LPG (kWh)</th>
                                    <th style={tableStyles.th}>Woodchip/Pellet (kWh)</th>
                                    <th style={tableStyles.th}>Solar (kWh)</th>
                                    <th style={tableStyles.th}>Total (kWh)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredData.map((row, index) => (
                                    <tr key={row.id} style={getRowStyle(row.year, index)}>
                                        <td style={tableStyles.td}>{row.month}</td>
                                        <td style={tableStyles.td}>{row.year}</td>
                                        <td style={tableStyles.td}>{formatValue(row.total_stream_dn_electricity_kwh)}</td>
                                        <td style={tableStyles.td}>{formatValue(row.mthw_kwh)}</td>
                                        <td style={tableStyles.td}>{formatValue(row.steam_kwh)}</td>
                                        <td style={tableStyles.td}>{formatValue(row.lpg_kwh)}</td>
                                        <td style={tableStyles.td}>{formatValue(row.woodchip_pellet_kwh)}</td>
                                        <td style={tableStyles.td}>{formatValue(row.solar_kwh)}</td>
                                        <td style={tableStyles.td}>{formatValue(row.total_kwh)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </CustomTabPanel>

            <CustomTabPanel value={activeTab} index={1}>
                <EnergyAnalyticsChart data={data} />
            </CustomTabPanel>

            <CustomTabPanel value={activeTab} index={2}>
                <EnergyYearComparison data={data} />
            </CustomTabPanel>

        </div>
    );
};

export default EnergyTotalDashboard;
