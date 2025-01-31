// src/components/visualizations/EnergyAnalyticsChart.tsx
import React, { useState } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';
import {
  FormGroup, FormControlLabel, Checkbox, Paper, Grid,
  Typography
} from '@mui/material';

interface EnergyData {
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


const styles = {
    paper: {
      p: 2,
      minHeight: '800px',
      width: '100%'
    },
    gridContainer: {
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      gap: '3px' // Reduced from 10px to 0px
    },
    chartGrid: {
      minHeight: '350px' // Reduced from 500px
    },
    pieChartGrid: {
      minHeight: '350px', // Reduced from 400px
      mt: 0 // Changed from -2 to 0 for better control
    }
  };

const COLORS = {
  electricity: '#1a237e',
  mthw: '#2e7d32',
  steam: '#c62828',
  lpg: '#6a1b9a',
  woodchip: '#4a148c',
  solar: '#ef6c00',
  total: '#b71c1c'
};

const EnergyAnalyticsChart: React.FC<{ data: EnergyData[] }> = ({ data }) => {
  const [selectedMetrics, setSelectedMetrics] = useState({
    electricity: true,
    mthw: true,
    steam: true,
    lpg: true,
    woodchip: true,
    solar: true,
    total: true
  });

  const [selectedYears, setSelectedYears] = useState([2022, 2023, 2024]);

  const handleMetricChange = (metric: string) => {
    setSelectedMetrics(prev => ({
      ...prev,
      [metric]: !prev[metric as keyof typeof prev]
    }));
  };

  const handleYearChange = (year: number) => {
    setSelectedYears(prev =>
      prev.includes(year)
        ? prev.filter(y => y !== year)
        : [...prev, year]
    );
  };

  const filteredData = data.filter(item =>
    selectedYears.includes(item.year)
  );

  const getPieChartData = (filteredData: EnergyData[]) => {
    // Calculate sum of each energy type for selected period
    const energySums = filteredData.reduce((sums, item) => {
      if (selectedMetrics.electricity && item.total_stream_dn_electricity_kwh) {
        sums.electricity += item.total_stream_dn_electricity_kwh;
      }
      if (selectedMetrics.mthw && item.mthw_kwh) {
        sums.mthw += item.mthw_kwh;
      }
      if (selectedMetrics.steam && item.steam_kwh) {
        sums.steam += item.steam_kwh;
      }
      if (selectedMetrics.lpg && item.lpg_kwh) {
        sums.lpg += item.lpg_kwh;
      }
      if (selectedMetrics.woodchip && item.woodchip_pellet_kwh) {
        sums.woodchip += item.woodchip_pellet_kwh;
      }
      if (selectedMetrics.solar && item.solar_kwh) {
        sums.solar += item.solar_kwh;
      }
      return sums;
    }, {
      electricity: 0,
      mthw: 0,
      steam: 0,
      lpg: 0,
      woodchip: 0,
      solar: 0
    });
  
    const totalEnergy = Object.values(energySums).reduce((sum, val) => sum + val, 0);
  
    // Create pie data array with percentages
    const pieData = [
      {
        name: 'Electricity',
        value: energySums.electricity ? (energySums.electricity / totalEnergy) * 100 : 0,
        kwhValue: energySums.electricity
      },
      {
        name: 'MTHW',
        value: energySums.mthw ? (energySums.mthw / totalEnergy) * 100 : 0,
        kwhValue: energySums.mthw
      },
      {
        name: 'Steam',
        value: energySums.steam ? (energySums.steam / totalEnergy) * 100 : 0,
        kwhValue: energySums.steam
      },
      {
        name: 'LPG',
        value: energySums.lpg ? (energySums.lpg / totalEnergy) * 100 : 0,
        kwhValue: energySums.lpg
      },
      {
        name: 'Woodchip',
        value: energySums.woodchip ? (energySums.woodchip / totalEnergy) * 100 : 0,
        kwhValue: energySums.woodchip
      },
      {
        name: 'Solar',
        value: energySums.solar ? (energySums.solar / totalEnergy) * 100 : 0,
        kwhValue: energySums.solar
      }
    ].filter(item => item.kwhValue > 0);
  
    return pieData;
  };
  


  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <FormGroup row>
            {Object.entries(selectedMetrics).map(([metric, checked]) => (
              <FormControlLabel
                key={metric}
                control={
                  <Checkbox
                    checked={checked}
                    onChange={() => handleMetricChange(metric)}
                    style={{ color: COLORS[metric as keyof typeof COLORS] }}
                  />
                }
                label={metric.charAt(0).toUpperCase() + metric.slice(1)}
              />
            ))}
          </FormGroup>
        </Grid>

        <Grid item xs={12}>
          <FormGroup row>
            {[2022, 2023, 2024].map(year => (
              <FormControlLabel
                key={year}
                control={
                  <Checkbox
                    checked={selectedYears.includes(year)}
                    onChange={() => handleYearChange(year)}
                  />
                }
                label={year.toString()}
              />
            ))}
          </FormGroup>
        </Grid>

        <Grid item xs={12} sx={styles.chartGrid}>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart 
              data={filteredData}
              margin={{ top: 0, right: 30, left: 65, bottom: 0 }}
            >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
                dataKey="month" 
                tickFormatter={(value, index) => {
                const item = filteredData[index];
                return item ? `${item.month}-${item.year}` : value;
                }}
                angle={-45}
                textAnchor="end"
                height={60}
            />
            <YAxis 
            label={{ 
                value: 'Energy Usage (kWh)', 
                angle: -90, 
                position: 'insideLeft',
                offset: -50
            }}
            tickFormatter={(value) => value.toLocaleString()} 
            />
            <Tooltip 
                labelFormatter={(label, items) => {
                const item = items[0]?.payload;
                return item ? `${item.month}-${item.year}` : label;
                }}
                formatter={(value, name) => [`${Number(value).toFixed(2)} kWh`, name]}
            />
            <Legend />
              
              {selectedMetrics.electricity && (
                <Line type="monotone" dataKey="total_stream_dn_electricity_kwh" stroke={COLORS.electricity} name="Electricity" />
              )}
              {selectedMetrics.mthw && (
                <Line type="monotone" dataKey="mthw_kwh" stroke={COLORS.mthw} name="MTHW" />
              )}
              {selectedMetrics.steam && (
                <Line type="monotone" dataKey="steam_kwh" stroke={COLORS.steam} name="Steam" />
              )}
              {selectedMetrics.lpg && (
                <Line type="monotone" dataKey="lpg_kwh" stroke={COLORS.lpg} name="LPG" />
              )}
              {selectedMetrics.woodchip && (
                <Line type="monotone" dataKey="woodchip_pellet_kwh" stroke={COLORS.woodchip} name="Woodchip" />
              )}
              {selectedMetrics.solar && (
                <Line type="monotone" dataKey="solar_kwh" stroke={COLORS.solar} name="Solar" />
              )}
              {selectedMetrics.total && (
                <Line type="monotone" dataKey="total_kwh" stroke={COLORS.total} name="Total" />
              )}
            </LineChart>
          </ResponsiveContainer>
        </Grid>

        <Grid item xs={12}>
            <Typography variant="h6" align="center" sx={{ mt: 0, mb: 1 }}>Energy Distribution</Typography>
            <ResponsiveContainer width="100%" height={350}>
                <PieChart>
                <Pie
                    data={getPieChartData(filteredData)}
                    innerRadius={80}
                    outerRadius={120}
                    paddingAngle={2}
                    dataKey="value"
                    label={({
                    cx,
                    cy,
                    midAngle,
                    innerRadius,
                    outerRadius,
                    value,
                    name
                    }) => {
                    const RADIAN = Math.PI / 180;
                    const radius = outerRadius * 1.2;
                    const x = cx + radius * Math.cos(-midAngle * RADIAN);
                    const y = cy + radius * Math.sin(-midAngle * RADIAN);
                    return (
                        <text
                        x={x}
                        y={y}
                        fill={COLORS[name.toLowerCase() as keyof typeof COLORS]}
                        textAnchor={x > cx ? 'start' : 'end'}
                        dominantBaseline="central"
                        >
                        {`${name}: ${value.toFixed(2)}%`}
                        </text>
                    );
                    }}
                >
                    {getPieChartData(filteredData).map((entry, index) => (
                    <Cell 
                        key={`cell-${index}`} 
                        fill={COLORS[entry.name.toLowerCase() as keyof typeof COLORS]}
                    />
                    ))}
                </Pie>
                <Tooltip 
                    formatter={(value, name, props) => {
                    const kwhValue = props.payload.kwhValue;
                    return [`${kwhValue.toFixed(2)} kWh`, name];
                    }}
                />
                </PieChart>
            </ResponsiveContainer>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default EnergyAnalyticsChart;
