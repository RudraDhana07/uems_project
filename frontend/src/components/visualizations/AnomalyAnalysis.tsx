import React from 'react';
import {
  ComposedChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, Bar, ReferenceLine
} from 'recharts';
import { GasAnomaly } from '../../types/GasAnalysis';

interface AnomalyAnalysisProps {
  anomalies: GasAnomaly[];
  threshold: number;
}

const AnomalyAnalysis: React.FC<AnomalyAnalysisProps> = ({ anomalies, threshold }) => {
  const styles = {
    container: {
      backgroundColor: 'white',
      padding: '20px',
      borderRadius: '8px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      marginBottom: '20px'
    },
    title: {
      fontSize: '1.2rem',
      fontWeight: 'bold',
      marginBottom: '15px',
      color: '#333'
    },
    table: {
      width: '100%',
      borderCollapse: 'collapse' as const,
      marginTop: '10px',
      marginBottom: '20px'
    },
    th: {
      backgroundColor: '#f8f9fa',
      padding: '8px',
      textAlign: 'left' as const,
      borderBottom: '2px solid #dee2e6'
    },
    td: {
      padding: '8px',
      borderBottom: '1px solid #dee2e6'
    },
    anomalyValue: {
      color: '#d32f2f',
      fontWeight: 'bold'
    },
    chartContainer: {
      height: '300px',
      marginTop: '15px',
      maxWidth: '800px',  // Add maximum width
      margin: '15px auto' // Center the chart
    },
    meterSection: {
      marginBottom: '30px',
      padding: '20px',
      backgroundColor: '#f8f9fa',
      borderRadius: '8px',
      maxWidth: '1000px',  // Add maximum width to section
      margin: '0 auto'     // Center the section
    },
    interpretation: {
      backgroundColor: '#f8f9fa',
      padding: '20px',
      borderRadius: '8px',
      marginBottom: '25px',
      fontSize: '1rem',
      lineHeight: '1.6',
      color: '#333'
    }
  };

  // Group anomalies by meter
  const groupedData = React.useMemo(() => {
    const grouped: { [key: string]: GasAnomaly[] } = {};
    anomalies.forEach(anomaly => {
      if (!grouped[anomaly.meter]) {
        grouped[anomaly.meter] = [];
      }
      grouped[anomaly.meter].push(anomaly);
    });
    return grouped;
  }, [anomalies]);

  // Convert anomalies to chart data
  const getChartData = (meterAnomalies: GasAnomaly[]) => {
    // Initialize data for all years
    const valueMap: { [key: string]: number } = {
      '2022': 0,
      '2023': 0,
      '2024': 0
    };
    
    // Fill in the values and calculate changes
    meterAnomalies.forEach(anomaly => {
      valueMap[anomaly.year] = anomaly.value;
      valueMap[String(parseInt(anomaly.year) - 1)] = anomaly.previous_value;
    });
  
    return Object.entries(valueMap)
      .map(([year, consumption]) => {
        const anomaly = meterAnomalies.find(a => a.year === year);
        return {
          year,
          consumption,
          // Set change value for all years to ensure line connectivity
          change: anomaly ? anomaly.percent_change : 
                 year === '2022' ? 0 : // Start from 0 for 2022
                 null // Keep other years' changes as calculated
        };
      })
      .sort((a, b) => parseInt(a.year) - parseInt(b.year));
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>
        Gas Consumption Significant Consumption Changes (Threshold: ±{threshold}%)
      </h3>
      <div style={styles.interpretation}>
        <p>Analysis of significant consumption changes (exceeding ±50%) reveals notable patterns across various meter locations:</p>
        
        <p>Several buildings demonstrate substantial variations in their mean consumption, which can be attributed to:</p>
        <ul>
          <li>Potential automated meter reading anomalies or calculation discrepancies</li>
          <li>Temporary closures for renovation or construction works</li>
          <li>Implementation of energy sustainability initiatives</li>
        </ul>

        <p>Key observations:</p>
        <ul>
          <li>Buildings like St Margaret's College show a consistent increase trend (+96.4% in 2023, +168.2% in 2024)</li>
          <li>Some locations like CHILDCARE CENTRE exhibit fluctuating patterns (+66.2% in 2023, -55.0% in 2024)</li>
          <li>Notable improvements in buildings like DENTAL showing sustained reduction in consumption (-66.5% in 2023, -30.4% in 2024)</li>
        </ul>
      </div>
      {Object.entries(groupedData).map(([meter, meterAnomalies]) => (
        <div key={meter} style={styles.container}>
          <h4>{meter}</h4>

          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Year</th>
                <th style={styles.th}>Consumption</th>
                <th style={styles.th}>Previous Year</th>
                <th style={styles.th}>Change (%)</th>
              </tr>
            </thead>
            <tbody>
              {meterAnomalies.map((anomaly, index) => (
                <tr key={index}>
                  <td style={styles.td}>{anomaly.year}</td>
                  <td style={styles.td}>
                    {anomaly.value.toLocaleString(undefined, {
                      maximumFractionDigits: 2
                    })}
                  </td>
                  <td style={styles.td}>
                    {anomaly.previous_value.toLocaleString(undefined, {
                      maximumFractionDigits: 2
                    })}
                  </td>
                  <td style={{
                    ...styles.td,
                    color: anomaly.percent_change > 0 ? '#d32f2f' : '#2e7d32',
                    fontWeight: Math.abs(anomaly.percent_change) > threshold ? 'bold' : 'normal'
                      }}>
                    {anomaly.percent_change > 0 ? '+' : ''}
                    {anomaly.percent_change.toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div style={styles.chartContainer}>
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={getChartData(meterAnomalies)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="year"
                  padding={{ left: 20, right: 20 }}
                />
                <YAxis 
                  yAxisId="consumption"
                  label={{ 
                    value: 'Mean Consumption', 
                    angle: -90, 
                    position: 'insideLeft',
                    style: { textAnchor: 'middle' }
                  }}
                />
                <YAxis 
                  yAxisId="change"
                  orientation="right"
                  label={{ 
                    value: 'Change %', 
                    angle: 90, 
                    position: 'insideRight',
                    style: { textAnchor: 'middle' }
                  }}
                />
                <Tooltip 
                  formatter={(value: number) => value.toFixed(2)}
                />
                <Legend 
                  verticalAlign="top"
                  height={36}
                />
                <Bar 
                  dataKey="consumption" 
                  fill="#8884d8" 
                  yAxisId="consumption"
                  name="Mean Consumption"
                  barSize={40}
                />
                <Line
                  type="monotone"
                  dataKey="change"
                  stroke="#82ca9d"
                  yAxisId="change"
                  name="% Change"
                  dot={{ r: 6 }}
                  connectNulls={true}
                  strokeWidth={2}
                  activeDot={{ r: 8 }}
                  isAnimationActive={true}  // Optional: disable animation if needed
                />
                {/* Reference lines for anomalies */}
                {meterAnomalies.map((anomaly, index) => (
                  Math.abs(anomaly.percent_change) > threshold && (
                    <ReferenceLine
                      key={index}
                      x={anomaly.year}
                      stroke="#ff0000"
                      strokeDasharray="3 3"
                      yAxisId="consumption"
                    />
                  )
                ))}
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </div>
      ))}
    </div>
  );
};

export default AnomalyAnalysis;