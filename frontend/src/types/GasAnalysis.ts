// src/types/GasAnalysis.ts
export interface GasClusterResults {
    cluster_id: number;
    meters: string[];
    size: number;
  }
  
  export interface GasConsumptionPattern {
    cluster_id: number;
    consumption_pattern: Record<string, number>;
  }
  
  export interface GasAnomaly {
    meter: string;
    year: string;
    value: number;
    previous_value: number;
    percent_change: number;
  }
  
  export interface GasAnalysisData {
    cluster_results: GasClusterResults[];
    consumption_patterns: GasConsumptionPattern[];
    anomaly_analysis: {
      anomalies: GasAnomaly[];
      threshold: number;
    };
    college_consumption: CollegeConsumption[];
  }

  export interface CollegeConsumption {
    name: string;
    '2022': number;
    '2023': number;
    '2024': number;
  }