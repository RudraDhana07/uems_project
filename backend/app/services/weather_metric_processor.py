# backend/app/services/weather_metric_processor.py

import pandas as pd

class WeatherMetricProcessor:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file

    def load_data(self) -> pd.DataFrame:
        try:
            # Read CSV file with specified range A:T
            df = pd.read_csv(self.csv_file, usecols=range(20))
            
            # Ensure numeric columns are properly converted
            numeric_columns = df.columns.difference(['Month'])
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
            
        except Exception as e:
            raise Exception(f"Error processing Weather data: {str(e)}")