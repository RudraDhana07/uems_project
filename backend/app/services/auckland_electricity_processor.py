# backend/app/services/auckland_electricity_processor.py

import pandas as pd
from typing import Dict
import numpy as np

class AucklandElectricityProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.raw_data = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load and process Auckland electricity consumption data from Excel.
        Returns processed DataFrame with standardized column names.
        """
        try:
            # Read the specific range from Excel including column A for meter_location
            df = pd.read_excel(
                self.excel_file,
                sheet_name='AKL-WLG-CHC',
                skiprows=27,     # Skip to actual data rows
                nrows=10,        # Read 10 rows
                usecols='A:AQ'   # Columns A through AQ (including A for meter_location)
            )
            
             # Create new DataFrame
            new_data = pd.DataFrame()
            new_data['meter_location'] = df.iloc[:, 0]
            new_data['object_name'] = df.iloc[:, 1]
            new_data['object_description'] = df.iloc[:, 2]

            # Generate all expected column names
            date_columns = ['Dec_2021']
            for year in [2022, 2023, 2024]:
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                date_columns.extend([f"{month}_{year}" for month in months])
            date_columns.extend([f"{month}_2025" for month in ['Jan', 'Feb', 'Mar']])

            # Map data columns to date columns maintaining position
            data_cols = df.iloc[:, 3:].columns  # Skip first 3 columns
            data_values = df.iloc[:, 3:]        # Get all data values

            # Create a mapping of Excel columns to date columns
            for i, date_col in enumerate(date_columns):
                if i < len(data_cols):
                    new_data[date_col] = data_values.iloc[:, i]
                else:
                    new_data[date_col] = None

            # Handle missing values properly
            for col in date_columns:
                new_data[col] = pd.to_numeric(new_data[col], errors='coerce')
                new_data[col] = new_data[col].where(pd.notnull(new_data[col]), None)

            self.raw_data = new_data
            return self.raw_data

        except Exception as e:
            raise Exception(f"Error loading Auckland Electricity data: {str(e)}")
    
    def validate_data(self) -> Dict:
        """
        Validate loaded data and return validation report.
        """
        if self.raw_data is None:
            self.load_data()
            
        validation_report = {
            'total_rows': len(self.raw_data),
            'columns': self.raw_data.columns.tolist(),
            'missing_values': self.raw_data.isnull().sum().to_dict(),
            'value_ranges': {
                col: {
                    'min': self.raw_data[col].min(),
                    'max': self.raw_data[col].max(),
                    'null_count': self.raw_data[col].isnull().sum()
                }
                for col in self.raw_data.columns 
                if col not in ['object_name', 'object_description', 'meter_location']
            }
        }
        
        return validation_report