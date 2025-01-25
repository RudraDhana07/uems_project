// src/components/visualization/ClusteringAnalysis.tsx

import React, { useMemo } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { GasClusterResults, GasConsumptionPattern } from '../../types/GasAnalysis';

interface ClusteringAnalysisProps {
    clusterResults: GasClusterResults[];
    consumptionPatterns: GasConsumptionPattern[];
  }

  const ClusteringAnalysis: React.FC<ClusteringAnalysisProps> = ({ clusterResults, consumptionPatterns }) => {
  const styles = {
    section: {
        backgroundColor: 'white',
        padding: '25px',
        borderRadius: '12px',
        boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
        marginBottom: '30px',
        border: '1px solid #e0e0e0'
    },
    title: {
        fontSize: '1.5rem',
        fontWeight: 'bold',
        marginBottom: '20px',
        color: '#333',
        borderBottom: '2px solid #eee',
        paddingBottom: '10px'
    },
    clusterInfo: {
        backgroundColor: '#f9f9f9',
        padding: '20px',
        borderRadius: '8px',
        marginBottom: '15px',
        border: '1px solid #ddd',
        transition: 'transform 0.2s',
        ':hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 6px 12px rgba(0,0,0,0.1)'
        }
    },
    clusterTitle: {
        fontSize: '1.2rem',
        color: '#2c3e50',
        marginBottom: '10px',
        fontWeight: 'bold'
      },
    meterCount: {
        fontSize: '1.1rem',
        color: '#34495e',
        marginBottom: '15px'
      },
    meterList: {
        maxHeight: '200px',
        overflowY: 'auto' as const,
        padding: '12px',
        backgroundColor: 'white',
        borderRadius: '6px',
        border: '1px solid #dee2e6',
        fontSize: '0.9rem',
        lineHeight: '1.6'
    },
    meterItem: {
        padding: '4px 8px',
        borderBottom: '1px solid #eee',
        ':last-child': {
          borderBottom: 'none'
        }
    },
    infoGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
        gap: '25px',
        marginBottom: '30px'
    },
    chartSection: {
        marginTop: '40px',
        padding: '20px',
        backgroundColor: 'white',
        borderRadius: '12px',
        boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
    },
    interpretation: {
        backgroundColor: '#f8f9fa',
        padding: '20px',
        borderRadius: '8px',
        marginBottom: '25px',
        border: '1px solid #e0e0e0'
    },
      analysisText: {
        marginTop: '15px',
        lineHeight: '1.6',
        color: '#2c3e50'
    }
  };

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300'];

  const processedPatternData = useMemo(() => {
    if (!consumptionPatterns?.length) return [];
    
    const monthOrder = [
      'Jan_2022', 'Feb_2022', 'Mar_2022', 'Apr_2022', 'May_2022', 'Jun_2022',
      'Jul_2022', 'Aug_2022', 'Sep_2022', 'Oct_2022', 'Nov_2022', 'Dec_2022',
      'Jan_2023', 'Feb_2023', 'Mar_2023', 'Apr_2023', 'May_2023', 'Jun_2023',
      'Jul_2023', 'Aug_2023', 'Sep_2023', 'Oct_2023', 'Nov_2023', 'Dec_2023',
      'Jan_2024', 'Feb_2024', 'Mar_2024', 'Apr_2024', 'May_2024', 'Jun_2024',
      'Jul_2024', 'Aug_2024', 'Sep_2024', 'Oct_2024', 'Nov_2024'
    ];

    return monthOrder.map(month => ({
      month,
      ...consumptionPatterns.reduce((acc, pattern) => ({
        ...acc,
        [`Cluster ${pattern.cluster_id + 1}`]: pattern.consumption_pattern[month]
      }), {})
    }));
  }, [consumptionPatterns]);

  if (!clusterResults?.length) {
    return <div style={styles.section}>No clustering data available</div>;
  }

  return (
    <div>
      <div style={styles.section}>
        <h3 style={styles.title}>Cluster Distribution Analysis</h3>

        <div style={styles.interpretation}>
            <p>Analysis of automated meter readings reveals three distinct consumption clusters:</p>
            <ul>
                <li><strong>Cluster 1 (Blue):</strong> Low-tier usage - Shows consistently low and stable consumption pattern averaging around 20,000 units throughout the period</li>
                <li><strong>Cluster 2 (Green):</strong> High-tier usage - Demonstrates the highest consumption levels, ranging between 200,000-500,000 units with notable seasonal variations</li>
                <li><strong>Cluster 3 (Yellow):</strong> Medium-tier usage - Shows intermittent spikes in consumption, particularly during October 2023 and July 2024, reaching up to 400,000 units</li>
            </ul>

            <p style={styles.analysisText}>
                The consumption patterns reveal distinct characteristics across clusters:
                <ul>
                <li>Cluster 1 maintains remarkably stable energy consumption throughout all three years, indicating consistent operational patterns</li>
                <li>Cluster 2 shows pronounced seasonal variations with peaks typically occurring in winter months (July-August). There's a noticeable pattern of high consumption during mid-year periods, though the peak intensities have moderated over time</li>
                <li>Cluster 3 exhibits interesting periodic spikes, particularly notable in October 2023 and July 2024, suggesting specific operational events or seasonal activities during these periods</li>
                </ul>
            </p>

            <p style={styles.analysisText}>
                Key observations:
                <ul>
                <li>Seasonal Effects: Most prominent in Cluster 2, with regular winter peaks</li>
                <li>Cyclic Patterns: Cluster 3 shows distinct cyclic behavior with sharp spikes followed by returns to baseline</li>
                <li>Long-term Trends: While Cluster 2 maintains the highest overall consumption, there's evidence of moderation in peak usage compared to early 2022</li>
                </ul>
            </p>
        </div>

        <div style={styles.infoGrid}>
          {clusterResults.map((cluster) => (
            <div key={cluster.cluster_id} style={styles.clusterInfo}>
              <h4 style={styles.clusterTitle}>Cluster {cluster.cluster_id + 1}</h4>
              <p style={styles.meterCount}>Number of meters: {cluster.size}</p>
              <div style={styles.meterList}>
                {cluster.meters.map((meter: string) => (
                  <div key={meter} style={styles.meterItem}>{meter}</div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {processedPatternData.length > 0 && (
        <div style={styles.chartSection}>
          <h3 style={styles.title}>Consumption Patterns by Cluster</h3>
          <div style={{ height: '500px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={processedPatternData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="month" 
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  interval={2}
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  ticks={[0, 100000, 200000, 300000, 400000, 500000]}
                  domain={[0, 500000]}
                  tickFormatter={(value) => `${value.toLocaleString()}`}
                />
                <Tooltip 
                  formatter={(value: number) => value.toLocaleString()}
                />
                <Legend 
                  verticalAlign="top"
                  height={36}
                />
                {consumptionPatterns.map((pattern, index) => (
                  <Line
                    key={pattern.cluster_id}
                    type="monotone"
                    dataKey={`Cluster ${pattern.cluster_id + 1}`}
                    stroke={COLORS[index % COLORS.length]}
                    dot={false}
                    strokeWidth={2}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClusteringAnalysis;