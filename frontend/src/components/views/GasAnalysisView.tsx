// src/components/views/GasAnalysisView.tsx

import React from 'react';
import { CircularProgress } from '@mui/material';
import ClusteringAnalysis from '../visualizations/ClusteringAnalysis';
import AnomalyAnalysis from '../visualizations/AnomalyAnalysis';
import { GasAnalysisData } from '../../types/GasAnalysis';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LabelList } from 'recharts';


interface GasAnalysisViewProps {
    data: GasAnalysisData | null;
    isLoading: boolean;
  }

  const GasAnalysisView: React.FC<GasAnalysisViewProps> = ({ data, isLoading }) => {
  const styles = {
    container: {
      padding: '20px',
      backgroundColor: '#f5f5f5',
      minHeight: '100vh'
    },
    title: {
      fontSize: '1.8rem',
      color: '#333',
      marginBottom: '20px'
    },
    error: {
      padding: '20px',
      color: '#666',
      textAlign: 'center' as const
    },
    loading: {
      display: 'flex',
      justifyContent: 'center',
      padding: '50px'
    },
    chartContainer: {
        width: '100%',
        maxWidth: '1200px',
        margin: '20px auto',
        backgroundColor: 'white',
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    },
    description: {
        backgroundColor: '#f8f9fa',
        padding: '15px 20px',
        borderRadius: '8px',
        marginBottom: '25px',
        fontSize: '1.2rem',
        lineHeight: '1.6',
        color: '#495057',
        border: '1px solid #dee2e6'
    },
    interpretationSection: {
        backgroundColor: '#f8f9fa',
        padding: '20px',
        borderRadius: '8px',
        marginBottom: '25px',
        fontSize: '1rem',
        lineHeight: '1.6'
    },
    keyFindings: {
        marginTop: '15px',
        marginBottom: '20px'
    },
    recommendation: {
        marginTop: '20px',
        padding: '15px',
        backgroundColor: '#e8f5e9',
        borderRadius: '6px',
        borderLeft: '4px solid #4caf50'
    }
  };

  if (isLoading) {
    return (
      <div style={styles.loading}>
        <CircularProgress />
      </div>
    );
  }

  if (!data) {
    return (
      <div style={styles.error}>
        No analysis data available. Please ensure the data is properly loaded.
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Gas Consumption Analysis - Automated Meter</h1>
      
      <div style={styles.description}>
        Based on the automated meter readings available through November 2024, comprehensive data analysis and visualization have been performed. Missing records were handled through statistical imputation to ensure data continuity and reliability. The following insights are derived from this processed dataset, focusing on consumption patterns, cluster analysis, and signficant consumption changes.
      </div>

      <ClusteringAnalysis 
        clusterResults={data.cluster_results}
        consumptionPatterns={data.consumption_patterns}
      />
      
      <AnomalyAnalysis 
        anomalies={data.anomaly_analysis.anomalies}
        threshold={data.anomaly_analysis.threshold}
      />
        {/* Add the new College Consumption Chart section */}
        <div style={styles.chartContainer}>
            <h2>College Gas Consumption Analysis</h2>
            <div style={styles.interpretationSection}>
                <p>Comparative analysis of gas consumption across university colleges reveals distinct patterns and trends from 2022 to 2024:</p>
                
                <div style={styles.keyFindings}>
                    <h4>Key Observations:</h4>
                    <ul>
                        <li><strong>Highest Consumers:</strong> University College (G60X) and St Margaret's College (G608) consistently show the highest gas consumption across all years, likely due to their larger resident populations and facility sizes.</li>
                        
                        <li><strong>Notable Trends:</strong>
                            <ul>
                                <li>St Margaret's College (G608) shows a concerning upward trend, with significant increases each year</li>
                                <li>University College Kitchen (G601) maintains relatively stable consumption patterns</li>
                                <li>Arana and Aquinas colleges demonstrate more moderate consumption levels with slight variations</li>
                            </ul>
                        </li>
                        
                        <li><strong>Year-over-Year Changes:</strong>
                            <ul>
                                <li>2023 saw increased consumption in most colleges compared to 2022</li>
                                <li>2024 data (through November) indicates continued high usage in several facilities</li>
                                <li>K308 and K427 show more variable patterns, suggesting potential operational changes or efficiency improvements</li>
                            </ul>
                        </li>
                    </ul>
                </div>

                <p style={styles.recommendation}>
                    <strong>Recommendations:</strong> Facilities with consistently high or increasing consumption patterns, particularly G60X and G608, 
                    should be prioritized for energy efficiency assessments and potential sustainability interventions. The successful practices from 
                    lower-consuming colleges could serve as benchmarks for improvement strategies.
                </p>
            </div>

            <ResponsiveContainer width="100%" height={500}>
                <BarChart
                data={data.college_consumption}
                margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                    dataKey="name" 
                    angle={-45}
                    textAnchor="end"
                    height={60}
                />
                <YAxis label={{ value: 'Consumption', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="2022" fill="#4394E5" name="2022">
                    <LabelList dataKey="2022" position="top" fontSize={10} />
                </Bar>
                <Bar dataKey="2023" fill="#87BB62" name="2023">
                    <LabelList dataKey="2023" position="top" fontSize={10} />
                </Bar>
                <Bar dataKey="2024" fill="#876FD4" name="2024">
                    <LabelList dataKey="2024" position="top" fontSize={10} />
                </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    </div>
  );
};

export default GasAnalysisView;