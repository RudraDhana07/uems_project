# backend/scripts/merge_weather_data.py

import os
import sys
from pathlib import Path
import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def merge_weather_files(weather_data_dir):
    merged_data = pd.DataFrame()
    
    # Column mappings for standardization
    column_mappings = {
        # Old format to new format
        'TEMP': 'Air_Temperature_C_Avg',
        'RH': 'Relative_Humidity_Avg',
        'WINDSPD': 'Wind_Speed_ms_Avg',
        'WINDIR': 'Wind_Direction_deg',
        'GLOBAL': 'Solar_W_Avg',
        'UVA': 'UVA_W_AVG',
        'UVB': 'UVB_W_AVG',
        'VISIBLE': 'Quantum_umol_AVG',
        'RAIN': 'Rain_mm_Tot',
        'PRESS': 'Air_Pressure_hPa_Avg',
        'MAXGUST': 'Wind_Speed_ms_Max',
        # Standardize date/time columns
        'DATE': 'Date',
        'TIME': 'Time'
    }
    
    # Core columns to keep (excluding GUSTIME)
    core_columns = ['Date', 'Time', 'Air_Temperature_C_Avg', 'Relative_Humidity_Avg',
                   'Wind_Speed_ms_Avg', 'Wind_Direction_deg', 'Solar_W_Avg',
                   'UVA_W_AVG', 'UVB_W_AVG', 'Quantum_umol_AVG', 'Rain_mm_Tot',
                   'Air_Pressure_hPa_Avg', 'Wind_Speed_ms_Max']
    
    file_count = 0
    error_count = 0
    
    logger.info("Starting weather data merge process...")
    
    for file_name in sorted(os.listdir(weather_data_dir)):
        if file_name.endswith('.csv') and file_name.startswith('weather-'):
            file_path = os.path.join(weather_data_dir, file_name)
            try:
                logger.info(f"Processing file: {file_name}")
                
                # Read file, skipping format row
                df = pd.read_csv(file_path, skiprows=[1])
                
                # Determine format based on column names
                if 'TEMP' in df.columns:  # Old format
                    df.rename(columns=column_mappings, inplace=True)
                
                # Drop GUSTIME if it exists
                if 'GUSTIME' in df.columns:
                    df.drop('GUSTIME', axis=1, inplace=True)
                
                # Validate all required columns exist
                missing_cols = set(core_columns) - set(df.columns)
                if missing_cols:
                    logger.warning(f"Missing columns in {file_name}: {missing_cols}")
                    error_count += 1
                    continue
                
                # Keep only core columns
                df = df[core_columns]
                
                # Add metadata
                df['source_file'] = file_name
                df['year_month'] = pd.to_datetime(file_name.replace('weather-', '')
                                                .replace('.csv', ''), format='%Y-%m')
                
                merged_data = pd.concat([merged_data, df], ignore_index=True)
                file_count += 1
                logger.info(f"Successfully processed: {file_name}")
                
            except Exception as e:
                logger.error(f"Error processing {file_name}: {str(e)}")
                error_count += 1
    
    if not merged_data.empty:
        # Save merged data
        output_path = os.path.join(weather_data_dir, 'merged_weather_data.csv')
        merged_data.to_csv(output_path, index=False)
        logger.info(f"\nMerged data saved to: {output_path}")
        logger.info(f"Total files processed: {file_count}")
        logger.info(f"Files with errors: {error_count}")
        logger.info(f"Total records: {len(merged_data)}")
        logger.info("\nColumn statistics:")
        logger.info(merged_data.info())
    else:
        logger.error("No data was merged. Please check the input files.")
    
    return merged_data

def main():
    try:
        # Get the project root directory
        root_dir = Path(__file__).resolve().parent.parent
        weather_dir = root_dir / 'data' / 'Weather'
        
        if not weather_dir.exists():
            raise FileNotFoundError(f"Weather data directory not found at {weather_dir}")
        
        logger.info(f"Processing weather files from: {weather_dir}")
        merged_df = merge_weather_files(str(weather_dir))
        
        logger.info("Weather data merge completed successfully")
        
    except Exception as e:
        logger.error(f"Error during merge process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
