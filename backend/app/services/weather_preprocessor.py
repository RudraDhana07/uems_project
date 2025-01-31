# backend/app/services/weather_preprocessor.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class WeatherDataPreprocessor:
    def __init__(self):
        self.header_rows = 2
        self.known_missing_dates = [
            pd.to_datetime('2023-08-01'),
            pd.to_datetime('2023-08-02'),
            pd.to_datetime('2023-08-03')
        ]
        # Define expected columns for the weather data
        self.expected_columns = [
            'Date', 'Time', 'Air_Temperature_C_Avg', 'Relative_Humidity_Avg',
            'Wind_Speed_ms_Avg', 'Wind_Direction_deg', 'Solar_W_Avg',
            'UVA_W_AVG', 'UVB_W_AVG', 'Quantum_umol_AVG', 'Rain_mm_Tot',
            'Air_Pressure_hPa_Avg', 'Wind_Speed_ms_Max'
        ]

    def read_csv_file(self, file_path: str) -> pd.DataFrame:
        """Read and process CSV file with proper column handling"""
        try:
            # Read CSV with no header and handle mixed types
            df = pd.read_csv(
                file_path,
                header=None,
                names=range(15),
                low_memory=False
            )
            
            logger.info(f"Initial read: {len(df)} rows")
            
            # Remove separator rows
            df = df[~df[0].astype(str).str.contains('weather-', na=False)]
            df = df[~df[0].astype(str).str.contains('-' * 20, na=False)]
            
            # Rename columns to match expected format
            column_mapping = {
                0: 'Date',
                1: 'Time',
                2: 'Air_Temperature_C_Avg',
                3: 'Relative_Humidity_Avg',
                4: 'Wind_Speed_ms_Avg',
                5: 'Wind_Direction_deg',
                6: 'Solar_W_Avg',
                7: 'UVA_W_AVG',
                8: 'UVB_W_AVG',
                9: 'Quantum_umol_AVG',
                10: 'Rain_mm_Tot',
                11: 'Air_Pressure_hPa_Avg',
                12: 'Wind_Speed_ms_Max'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Select only needed columns
            df = df[self.expected_columns]
            
            return df
            
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            raise

    def preprocess_data(self, file_path: str) -> pd.DataFrame:
        """Preprocess the weather data file"""
        try:
            # Read the CSV file
            raw_df = self.read_csv_file(file_path)
            
            if raw_df.empty:
                raise ValueError("No data found in the file")
            
            # Convert date and time to datetime
            raw_df['DATETIME'] = pd.to_datetime(
                raw_df['Date'] + ' ' + raw_df['Time'],
                format='%d/%m/%Y %H:%M:%S',
                errors='coerce'
            )
            
            # Drop rows with invalid dates
            raw_df = raw_df.dropna(subset=['DATETIME'])
            
            # Convert numeric columns
            numeric_columns = [
                'Air_Temperature_C_Avg',
                'Relative_Humidity_Avg',
                'Wind_Speed_ms_Avg',
                'Wind_Direction_deg',
                'Solar_W_Avg',
                'UVA_W_AVG',
                'UVB_W_AVG',
                'Quantum_umol_AVG',
                'Rain_mm_Tot',
                'Air_Pressure_hPa_Avg',
                'Wind_Speed_ms_Max'
            ]
            
            for col in numeric_columns:
                raw_df[col] = pd.to_numeric(raw_df[col], errors='coerce')
            
            # Sort by datetime
            raw_df = raw_df.sort_values('DATETIME')
            
            # Remove known missing dates
            raw_df = raw_df[~raw_df['DATETIME'].dt.date.isin(
                [d.date() for d in self.known_missing_dates]
            )]
            
            logger.info(f"Processed {len(raw_df)} weather records")
            logger.info(f"Date range: {raw_df['DATETIME'].min()} to {raw_df['DATETIME'].max()}")
            
            return raw_df
            
        except Exception as e:
            logger.error(f"Error preprocessing weather data: {str(e)}")
            raise

    def validate_data(self, df: pd.DataFrame) -> dict:
        """Validate the processed data and return validation results"""
        try:
            validation_results = {
                'total_records': len(df),
                'date_range': {
                    'start': df['DATETIME'].min().strftime('%Y-%m-%d %H:%M:%S'),
                    'end': df['DATETIME'].max().strftime('%Y-%m-%d %H:%M:%S')
                },
                'missing_values': {},
                'value_ranges': {},
                'readings_per_day': {},
                'data_quality': {
                    'completeness': {},
                    'validity': {}
                }
            }
            
            # Check missing values
            for col in df.columns:
                missing = df[col].isnull().sum()
                if missing > 0:
                    validation_results['missing_values'][col] = {
                        'count': int(missing),
                        'percentage': float((missing / len(df)) * 100)
                    }
            
            # Calculate value ranges for numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                validation_results['value_ranges'][col] = {
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'mean': float(df[col].mean()),
                    'std': float(df[col].std())
                }
            
            # Calculate readings per day
            daily_counts = df.groupby(df['DATETIME'].dt.date).size()
            validation_results['readings_per_day'] = {
                'mean': float(daily_counts.mean()),
                'min': int(daily_counts.min()),
                'max': int(daily_counts.max()),
                'complete_days': int(sum(daily_counts == 288)),
                'incomplete_days': int(sum(daily_counts < 288))
            }
            
            # Check data completeness
            expected_readings = len(pd.date_range(
                df['DATETIME'].min(),
                df['DATETIME'].max(),
                freq='5min'
            ))
            validation_results['data_quality']['completeness'] = {
                'total_expected': expected_readings,
                'total_actual': len(df),
                'percentage': float((len(df) / expected_readings) * 100)
            }
            
            logger.info("Data Validation Summary:")
            logger.info(f"Total Records: {validation_results['total_records']}")
            logger.info(f"Date Range: {validation_results['date_range']}")
            logger.info(f"Complete Days: {validation_results['readings_per_day']['complete_days']}")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating data: {str(e)}")
            raise