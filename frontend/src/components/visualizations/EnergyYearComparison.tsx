// src/components/visualizations/EnergyYearComparison.tsx
import React from 'react';
import { Grid, Paper } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface EnergyData {
  month: string;
  year: number;
  total_stream_dn_electricity_kwh: number;
  mthw_kwh: number;
  steam_kwh: number;
  lpg_kwh: number;
  woodchip_pellet_kwh: number;
  solar_kwh: number;
}

interface YearlyTotals {
  [key: string]: {
    electricity: number;
    mthw: number;
    steam: number;
    lpg: number;
    woodchip: number;
    solar: number;
  };
}

const COLORS = {
  electricity: '#1a73e8',
  mthw: '#34a853',
  steam: '#ea4335',
  lpg: '#fbbc04',
  woodchip: '#9334e8',
  solar: '#ff6d01'
};

const EnergyYearComparison: React.FC<{ data: EnergyData[] }> = ({ data }) => {
  // Calculate yearly totals
  const yearlyTotals = data.reduce((acc: YearlyTotals, curr) => {
    const year = curr.year.toString();
    if (!acc[year]) {
      acc[year] = {
        electricity: 0,
        mthw: 0,
        steam: 0,
        lpg: 0,
        woodchip: 0,
        solar: 0
      };
    }
    
    acc[year].electricity += curr.total_stream_dn_electricity_kwh || 0;
    acc[year].mthw += curr.mthw_kwh || 0;
    acc[year].steam += curr.steam_kwh || 0;
    acc[year].lpg += curr.lpg_kwh || 0;
    acc[year].woodchip += curr.woodchip_pellet_kwh || 0;
    acc[year].solar += curr.solar_kwh || 0;
    
    return acc;
  }, {});

  // Prepare pie chart data for each year
  const getPieChartData = (year: string) => {
    const yearData = yearlyTotals[year];
    if (!yearData) return [];
    
    const total = Object.values(yearData).reduce((sum, val) => sum + val, 0);
    
    return Object.entries(yearData).map(([key, value]) => ({
      name: key.charAt(0).toUpperCase() + key.slice(1),
      value: (value / total) * 100,
      kwhValue: value // Add absolute kWh value
    }));
  };

  // Format number with thousand separators
  const formatNumber = (value: number): string => {
    return new Intl.NumberFormat('en-NZ').format(Math.round(value));
  };

  // Prepare line chart data
  const lineChartData = data.map(item => ({
    date: `${item.month}-${item.year}`,
    electricity: item.total_stream_dn_electricity_kwh,
    mthw: item.mthw_kwh,
    steam: item.steam_kwh,
    lpg: item.lpg_kwh,
    woodchip: item.woodchip_pellet_kwh,
    solar: item.solar_kwh
  }));

  // Custom tooltip content for pie charts
  const CustomPieTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      const color = Object.entries(COLORS).find(([key]) => 
        key.toLowerCase() === data.name.toLowerCase()
      )?.[1] || '#000';

      return (
        <div style={{
          backgroundColor: '#fff',
          padding: '10px',
          border: `2px solid ${color}`,
          borderRadius: '4px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <p style={{ 
            margin: 0,
            color: color,
            fontWeight: 'bold',
            borderBottom: `2px solid ${color}`,
            paddingBottom: '4px',
            marginBottom: '4px'
          }}>
            {data.name}
          </p>
          <p style={{ 
            margin: '4px 0',
            color: color
          }}>
            {`${data.value.toFixed(3)}%`}
          </p>
          <p style={{ 
            margin: '4px 0',
            color: color
          }}>
            {`${formatNumber(data.kwhValue)} kWh`}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <Grid container spacing={3}>
      {/* Line Chart */}
      <Grid item xs={12}>
        <Paper elevation={3} sx={{ p: 2, height: 400 }}>
          <ResponsiveContainer>
            <LineChart data={lineChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                angle={-45} 
                textAnchor="end" 
                height={60}
              />
              <YAxis label={{ value: 'Energy (kWh)', angle: -90, position: 'insideLeft' }} />
              <Tooltip 
                formatter={(value: number, name: string) => [
                  `${formatNumber(value)} kWh`, 
                  name
                ]}
              />
              <Legend />
              {Object.entries(COLORS).map(([key, color]) => (
                <Line
                  key={key}
                  type="monotone"
                  dataKey={key}
                  stroke={color}
                  strokeWidth={2}
                  dot={{ r: 4 }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>

      {/* Pie Charts */}
      <Grid item xs={12}>
        <Grid container spacing={2}>
          {['2022', '2023', '2024'].map((year) => (
            <Grid item xs={12} md={4} key={year}>
              <Paper elevation={3} sx={{ p: 2, height: 400 }}>
                <h3 style={{ textAlign: 'center', margin: '0 0 10px 0' }}>
                  {year} Energy Distribution
                </h3>
                <ResponsiveContainer>
                  <PieChart>
                    <Pie
                      data={getPieChartData(year)}
                      innerRadius={60}
                      outerRadius={120}
                      paddingAngle={5}
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value.toFixed(3)}%`}
                    >
                      {getPieChartData(year).map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={Object.values(COLORS)[index]} 
                        />
                      ))}
                    </Pie>
                    <Tooltip content={<CustomPieTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Grid>
    </Grid>
  );
};

export default EnergyYearComparison;