// src/types/auckland.ts

// Base interface for shared properties
interface BaseConsumption {
    id: number;
    object_name: string;
    object_description: string;
    created_at: string;
    updated_at: string;
  }
  
  // Monthly readings interface
  interface MonthlyData {
    Dec_2021: number | null;
    // 2022
    Jan_2022: number | null;
    Feb_2022: number | null;
    Mar_2022: number | null;
    Apr_2022: number | null;
    May_2022: number | null;
    Jun_2022: number | null;
    Jul_2022: number | null;
    Aug_2022: number | null;
    Sep_2022: number | null;
    Oct_2022: number | null;
    Nov_2022: number | null;
    Dec_2022: number | null;
    // 2023
    Jan_2023: number | null;
    Feb_2023: number | null;
    Mar_2023: number | null;
    Apr_2023: number | null;
    May_2023: number | null;
    Jun_2023: number | null;
    Jul_2023: number | null;
    Aug_2023: number | null;
    Sep_2023: number | null;
    Oct_2023: number | null;
    Nov_2023: number | null;
    Dec_2023: number | null;
    // 2024
    Jan_2024: number | null;
    Feb_2024: number | null;
    Mar_2024: number | null;
    Apr_2024: number | null;
    May_2024: number | null;
    Jun_2024: number | null;
    Jul_2024: number | null;
    Aug_2024: number | null;
    Sep_2024: number | null;
    Oct_2024: number | null;
    Nov_2024: number | null;
    Dec_2024: number | null;
  }
  
  // Specific interfaces for each table type
  export interface ElectricityCalculatedConsumption extends BaseConsumption, MonthlyData {
    meter_location: string;
  }
  
  export interface WaterCalculatedConsumption extends BaseConsumption, MonthlyData {
    meter_location: string;
  }
  
  export interface WaterConsumption extends BaseConsumption, MonthlyData {
    reading_description: string;
  }
  
  // Props interface for the DataTable component
  export interface DataTableProps<T> {
    data: T[];
    title: string;
    isLoading: boolean;
  }