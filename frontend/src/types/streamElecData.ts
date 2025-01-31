// src/types/streamElecData.ts

export interface StreamElecDataRow {
  meter_reading_month: string;
  meter_reading_year: number;
  
  // Ring Mains
  ring_main_1_mp4889_kwh: number;
  ring_main_2_kwh: number;
  ring_main_3_kwh: number;
  ring_mains_total_kwh: number;
  ring_main_1_mp4889_pf: number;
  ring_main_2_pf: number;
  ring_main_3_pf: number;

  // Libraries
  hocken_library_kwh: number;
  robertson_library_kwh: number;
  libraries_total_kwh: number;
  hocken_library_pf: number;
  robertson_library_pf: number;
  bill_robertson_library_msb: number;
  sayers_adams_msb: number;
  isb_west_excluding_shops: number;
  richardson_library_block_rising_main: number;

  // Allow for dynamic properties
  [key: string]: string | number | null | undefined;
}

export interface ChartColumn {
  key: string;
  name: string;
  color: string;
}

export interface EnergyUsageChartProps {
  data: StreamElecDataRow[];
  columns: ChartColumn[];
}

export interface ProcessedChartData {
  date: string;
  [key: string]: number | string;
}